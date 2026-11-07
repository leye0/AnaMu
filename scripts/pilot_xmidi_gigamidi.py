#!/usr/bin/env python3
"""Bounded, ephemeral XMIDI sample + exact GigaMIDI MD5 lookup.

Google Drive supports byte ranges for the public XMIDI ZIP. ZipFile can use
those ranges to read the central directory and a few safe-sized entries.
The runner never persists MIDI bytes or exposes file hashes in the logs.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import random
import re
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import PurePosixPath


XMIDI_ID = "1qDkSH31x7jN8X-2RyzB9wuxGji4QxYyA"
XMIDI_URL = f"https://drive.usercontent.google.com/download?id={XMIDI_ID}&export=download&confirm=t"
HF_DATASET = "Metacreation/GigaMIDI"
HF_ENDPOINT = "https://datasets-server.huggingface.co"
MAX_ZIP_TRANSFER = 24_000_000
MAX_ZIP_REQUESTS = 30
MAX_MIDI_SIZE = 180_000
MAX_COMPRESSED_SIZE = 100_000
SAMPLE_SIZE = 3
MAX_API_RESPONSE = 400_000
RANGE_PATTERN = re.compile(r"bytes (\d+)-(\d+)/(\d+)")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


class RangeFile:
    """Seekable remote file with a hard byte and request budget."""

    def __init__(self, url: str, max_bytes: int = MAX_ZIP_TRANSFER):
        self.url = url
        self.pos = 0
        self.total_size = None
        self.downloaded = 0
        self.requests = 0
        self.max_bytes = max_bytes
        self._get_range(0, 0)

    def _get_range(self, first: int, last: int) -> bytes:
        count = last - first + 1
        if count < 0 or count + self.downloaded > self.max_bytes:
            raise ValueError("zip_byte_budget_exceeded")
        if self.requests >= MAX_ZIP_REQUESTS:
            raise ValueError("zip_request_budget_exceeded")
        self.requests += 1
        req = urllib.request.Request(self.url, headers={
            "Range": f"bytes={first}-{last}", "User-Agent": "AnaMu-Pilot/0.1",
        })
        with urllib.request.urlopen(req, timeout=60) as resp:
            if resp.status != 206:
                raise ValueError("range_not_honored")
            returned_range = RANGE_PATTERN.fullmatch(resp.headers.get("Content-Range", ""))
            if not returned_range:
                raise ValueError("missing_content_range")
            actual_first, actual_last, total_size = map(int, returned_range.groups())
            if actual_first != first or actual_last != last:
                raise ValueError("unexpected_content_range")
            if self.total_size is not None and total_size != self.total_size:
                raise ValueError("zip_size_changed")
            self.total_size = total_size
            data = resp.read(count + 1)
            if len(data) != count:
                raise ValueError("unexpected_range_size")
            self.downloaded += len(data)
            return data

    def seek(self, offset: int, whence: int = io.SEEK_SET) -> int:
        if whence == io.SEEK_END:
            self.pos = self.total_size + offset
        elif whence == io.SEEK_CUR:
            self.pos += offset
        elif whence == io.SEEK_SET:
            self.pos = offset
        else:
            raise ValueError("invalid_seek_mode")
        if self.pos < 0 or self.pos > self.total_size:
            raise ValueError("invalid_seek_position")
        return self.pos

    def tell(self) -> int:
        return self.pos

    def read(self, size: int = -1) -> bytes:
        if size < 0:
            size = self.total_size - self.pos
        size = min(size, self.total_size - self.pos)
        if size == 0:
            return b""
        result = self._get_range(self.pos, self.pos + size - 1)
        self.pos += len(result)
        return result


def select_entries(infos: list[zipfile.ZipInfo]) -> tuple[int, list[zipfile.ZipInfo]]:
    eligible = [i for i in infos if i.filename.lower().endswith((".mid", ".midi"))
                and not i.is_dir() and 200 <= i.file_size <= MAX_MIDI_SIZE
                and i.compress_size <= MAX_COMPRESSED_SIZE]
    rng = random.Random(20261107)
    return len(eligible), rng.sample(eligible, min(SAMPLE_SIZE, len(eligible)))


def labels_from_filename(name: str) -> dict:
    base = PurePosixPath(name).name
    parts = base.rsplit(".", 1)[0].removeprefix("XMIDI_").rsplit("_", 2)
    if not base.startswith("XMIDI_") or len(parts) != 3:
        return {"emotion": None, "genre": None}
    return {"emotion": parts[0], "genre": parts[1]}


def hf_json(token: str, endpoint: str, args: dict) -> dict:
    url = HF_ENDPOINT + endpoint + "?" + urllib.parse.urlencode(args)
    req = urllib.request.Request(url, headers={
        "Authorization": "Bearer " + token, "User-Agent": "AnaMu-Pilot/0.1",
    })
    with urllib.request.build_opener(NoRedirect()).open(req, timeout=20) as resp:
        body = resp.read(MAX_API_RESPONSE + 1)
        if len(body) > MAX_API_RESPONSE:
            raise ValueError("hf_response_budget_exceeded")
        return json.loads(body)


def lookup_md5(token: str, md5: str, split: str) -> bool:
    payload = hf_json(token, "/filter", {
        "dataset": HF_DATASET, "config": "v2.0.0", "split": split,
        "where": f'"md5"=\'{md5}\'', "offset": 0, "length": 1,
    })
    rows = payload.get("rows") or []
    return any((r.get("row") or {}).get("md5") == md5 for r in rows)


def control_filter(token: str) -> bool:
    payload = hf_json(token, "/rows", {
        "dataset": HF_DATASET, "config": "v2.0.0", "split": "validation",
        "offset": 0, "length": 1,
    })
    rows = payload.get("rows") or []
    if not rows:
        raise ValueError("no_control_row")
    md5 = rows[0]["row"]["md5"]
    return lookup_md5(token, md5, "validation")


def main() -> None:
    token = os.environ.get("HF_TOKEN", "").strip()
    report: dict = {
        "operation": "XMIDI remote ZIP index and 3 MIDI at most; exact MD5 GigaMIDI filter",
        "zip_max_transfer_bytes": MAX_ZIP_TRANSFER,
        "max_midi_size_bytes": MAX_MIDI_SIZE,
        "hf_credential_configured": bool(token),
    }
    try:
        remote = RangeFile(XMIDI_URL)
        with zipfile.ZipFile(remote, "r") as archive:
            info = archive.infolist()
            eligible_count, chosen = select_entries(info)
            report["archive"] = {
                "total_bytes": remote.total_size,
                "total_entries": len(info),
                "eligible_entries": eligible_count,
                "selected_entries": len(chosen),
            }
            samples = []
            for entry in chosen:
                midi = archive.read(entry)
                if not midi.startswith(b"MThd"):
                    continue
                samples.append({**labels_from_filename(entry.filename),
                                "file_bytes": len(midi), "md5": hashlib.md5(midi).hexdigest()})
            report["archive"]["network_bytes"] = remote.downloaded
            report["archive"]["range_requests"] = remote.requests

        if token:
            try:
                report["filter_control_works"] = control_filter(token)
            except (urllib.error.HTTPError, urllib.error.URLError, ValueError, TimeoutError) as exc:
                report["filter_control_error"] = (f"http_{exc.code}" if isinstance(exc, urllib.error.HTTPError)
                                                  else type(exc).__name__)

        for sample in samples:
            md5 = sample.pop("md5")
            sample["matched_splits"] = []
            if report.get("filter_control_works"):
                for split in ("validation", "test", "train"):
                    try:
                        if lookup_md5(token, md5, split):
                            sample["matched_splits"].append(split)
                            break
                    except (urllib.error.HTTPError, urllib.error.URLError, ValueError, TimeoutError) as exc:
                        sample["filter_error"] = (f"http_{exc.code}" if isinstance(exc, urllib.error.HTTPError)
                                                  else type(exc).__name__)
                        break
            else:
                sample["matched_splits"] = None
        report["samples"] = samples
    except (urllib.error.HTTPError, urllib.error.URLError, zipfile.BadZipFile,
            RuntimeError, ValueError, TimeoutError) as exc:
        report["error"] = (f"http_{exc.code}" if isinstance(exc, urllib.error.HTTPError)
                           else str(exc) if isinstance(exc, ValueError) else type(exc).__name__)

    # No MIDI, filename, full MD5, remote URLs, or credential is ever printed.
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
