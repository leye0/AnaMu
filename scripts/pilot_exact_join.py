#!/usr/bin/env python3
"""Test byte-identical XMIDI/GigaMIDI overlap without a corpus download.

Read 100 bounded XMIDI files from a remote ZIP, hash in memory, then project
ONLY the md5 column from one GigaMIDI validation Parquet shard. Stop at the
first exact match. No MIDI/audio is retained or included in logs.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
import zipfile

from scripts.pilot_xmidi_gigamidi import XMIDI_URL, RangeFile, labels_from_filename, select_entries
from scripts.probe_hf_parquet_columns import BudgetFile, PATH, safe_error_detail


SAMPLE_SIZE = 100
MAX_ZIP_BYTES = 30_000_000
MAX_ZIP_REQUESTS = 340
MAX_PARQUET_LOGICAL_BYTES = 24_000_000
MAX_SECONDS = 350
PARQUET_BLOCK_BYTES = 4_096
META_COLUMNS = (
    "title", "artist", "musicbrainz_id", "spotify_id",
    "audio_text_matches_mbid", "audio_text_matches_score",
)


def sample_hashes(archive: zipfile.ZipFile) -> tuple[dict[str, dict], dict]:
    """Return deterministic examples keyed by MD5 (never serialized)."""
    eligible_count, chosen = select_entries(archive.infolist(), sample_size=SAMPLE_SIZE)
    records: dict[str, dict] = {}
    bad_headers = 0
    for index, item in enumerate(chosen):
        data = archive.read(item)
        if not data.startswith(b"MThd"):
            bad_headers += 1
            continue
        digest = hashlib.md5(data).hexdigest()
        # Same file in multiple labels is one MD5 candidate for the lookup.
        records.setdefault(digest, {"sample_index": index, **labels_from_filename(item.filename)})
    return records, {
        "eligible_archive_entries": eligible_count,
        "selected_entries": len(chosen),
        "valid_midi_headers": len(chosen) - bad_headers,
        "unique_md5_candidates": len(records),
    }


def scan_groups(parquet, candidates: dict[str, dict], deadline: float) -> dict:
    """Scan only an explicitly named Parquet column, stop on first match."""
    if "md5" not in parquet.schema_arrow.names:
        return {"status": "missing_md5_column"}

    groups_read = 0
    rows_read = 0
    for group_index in range(parquet.num_row_groups):
        if time.monotonic() >= deadline:
            return {"status": "time_budget_exceeded", "groups_read": groups_read,
                    "md5_rows_examined": rows_read}
        values = parquet.read_row_group(
            group_index, columns=["md5"], use_threads=False,
        ).column("md5").to_pylist()
        groups_read += 1
        rows_read += len(values)
        for row_index, digest in enumerate(values):
            if digest in candidates:
                return {
                    "status": "exact_md5_match",
                    "groups_read": groups_read,
                    "md5_rows_examined": rows_read,
                    "match": {**candidates[digest], "row_group": group_index,
                              "row_in_group": row_index, "digest_verified": True},
                }
    return {"status": "no_match_in_one_shard", "groups_read": groups_read,
            "md5_rows_examined": rows_read}


def optional_matching_metadata(parquet, match: dict) -> dict:
    """Fetch optional *text* columns, never the music or MIDI payload."""
    available = [name for name in META_COLUMNS if name in parquet.schema_arrow.names]
    if not available:
        return {}
    group = parquet.read_row_group(match["row_group"], columns=available, use_threads=False)
    row = match["row_in_group"]
    details = {}
    for name in available:
        value = group.column(name)[row].as_py()
        if isinstance(value, (str, int, float, bool)) and len(str(value)) <= 160:
            details[name] = value
    return details


def run(token: str) -> dict:
    import pyarrow.parquet as pq
    from huggingface_hub import HfFileSystem

    deadline = time.monotonic() + MAX_SECONDS
    report = {
        "scope": "100 XMIDI samples and one GigaMIDI validation Parquet shard",
        "zip_byte_cap": MAX_ZIP_BYTES,
        "parquet_logical_read_cap": MAX_PARQUET_LOGICAL_BYTES,
        "note": "Parquet logical bytes are not the total HTTP transfer including read-ahead.",
    }
    remote = RangeFile(XMIDI_URL, max_bytes=MAX_ZIP_BYTES, max_requests=MAX_ZIP_REQUESTS)
    with zipfile.ZipFile(remote) as archive:
        candidates, samples_report = sample_hashes(archive)
    report["xmidi"] = {
        **samples_report,
        "zip_total_bytes": remote.total_size,
        "zip_network_bytes": remote.downloaded,
        "range_requests": remote.requests,
    }
    if time.monotonic() >= deadline:
        report["scan"] = {"status": "time_budget_exceeded_before_parquet"}
        return report

    fs = HfFileSystem(token=token)
    with fs.open(PATH, "rb", block_size=PARQUET_BLOCK_BYTES,
                 cache_type="readahead") as stream:
        bounded = BudgetFile(stream, limit=MAX_PARQUET_LOGICAL_BYTES)
        parquet = pq.ParquetFile(bounded, pre_buffer=False)
        report["gigamidi"] = {
            "split": "validation", "shard": "00001.parquet",
            "shard_rows": parquet.metadata.num_rows,
            "shard_row_groups": parquet.num_row_groups,
        }
        result = scan_groups(parquet, candidates, deadline)
        if result["status"] == "exact_md5_match":
            try:
                result["match"]["text_metadata"] = optional_matching_metadata(
                    parquet, result["match"])
            except Exception:
                # An exact MD5 match is still proven even if an optional column
                # or its data representation cannot be decoded.
                result["match"]["text_metadata_status"] = "unavailable"
        report["scan"] = result
        report["gigamidi"]["logical_bytes_read"] = bounded.read_bytes
    return report


def main() -> None:
    token = os.getenv("HF_TOKEN", "").strip()
    if not token:
        print(json.dumps({"status": "missing_HF_TOKEN"}))
        raise SystemExit(1)
    try:
        result = run(token)
    except Exception as exc:
        print(json.dumps({"status": "inconclusive_error", "error_type": type(exc).__name__,
                          "detail_redacted": safe_error_detail(exc, token)}))
        raise SystemExit(1) from None
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result.get("scan", {}).get("status") not in ("exact_md5_match", "no_match_in_one_shard"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
