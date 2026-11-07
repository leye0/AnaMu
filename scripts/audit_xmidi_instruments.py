#!/usr/bin/env python3
"""Bounded, in-memory audit of MIDI instrumentation in XMIDI.

Two non-overlapping, deterministic samples: 100 random eligible XMIDI files
and 100 additional files labelled pop, rock, or grunge. The latter is a
targeted supplement, NOT part of the unbiased random population estimate.

Reads each ZIP member with one HTTP range whenever its local-header extra
field is reasonably small. No MIDI is stored or sent to job artifacts.
"""

from __future__ import annotations

import io
import json
import os
import random
import statistics
import struct
import time
import zlib
import zipfile
from collections import Counter

from scripts.pilot_xmidi_gigamidi import (
    MAX_COMPRESSED_SIZE, MAX_MIDI_SIZE, XMIDI_URL, RangeFile, labels_from_filename,
)


RANDOM_SIZE = 100
TARGETED_SIZE = 100
SAMPLE_SEED = 20261107
MAX_ZIP_BYTES = 32_000_000
MAX_ZIP_REQUESTS = 250
MAX_SECONDS = 345
MIN_INSTRUMENT_NOTES = 16
TIME_BUCKETS = 16
MIN_ACTIVE_BUCKETS = 4
ZIP_LOCAL_HEADER = struct.Struct("<IHHHHHIIIHH")
ZIP_LOCAL_SIGNATURE = 0x04034B50

FAMILIES = (
    "piano", "chromatic_percussion", "organ", "guitar", "bass", "strings",
    "ensemble", "brass", "reed", "pipe", "synth_lead", "synth_pad",
    "synth_fx", "ethnic", "percussive_fx", "sound_fx",
)


def is_eligible(info: zipfile.ZipInfo) -> bool:
    return (not info.is_dir() and info.filename.lower().endswith((".mid", ".midi"))
            and 200 <= info.file_size <= MAX_MIDI_SIZE
            and info.compress_size <= MAX_COMPRESSED_SIZE
            and info.compress_type in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED)
            and not info.flag_bits & 1)


def choose_samples(infos: list[zipfile.ZipInfo]) -> tuple[dict[str, list[zipfile.ZipInfo]], dict]:
    eligible = [item for item in infos if is_eligible(item)]
    genres = Counter((labels_from_filename(item.filename)["genre"] or "unknown").lower()
                     for item in eligible)
    rng = random.Random(SAMPLE_SEED)
    general = rng.sample(eligible, min(RANDOM_SIZE, len(eligible)))
    already = {item.filename for item in general}
    targeted_pool = [item for item in eligible if item.filename not in already
                     and any(word in (labels_from_filename(item.filename)["genre"] or "").lower()
                             for word in ("pop", "rock", "grunge"))]
    targeted = rng.sample(targeted_pool, min(TARGETED_SIZE, len(targeted_pool)))
    return {"general_random": general, "pop_rock_targeted": targeted}, {
        "zip_entries": len(infos),
        "eligible_midis": len(eligible),
        "eligible_pop_rock_grunge": sum(count for genre, count in genres.items()
                                       if any(word in genre for word in ("pop", "rock", "grunge"))),
        "eligible_genres_top": dict(genres.most_common(15)),
        "selection_seed": SAMPLE_SEED,
    }


def read_midi_one_range(remote: RangeFile, info: zipfile.ZipInfo) -> bytes:
    """Read and verify a member without ZipFile's 3 HTTP reads per member."""
    if not is_eligible(info):
        raise ValueError("ineligible_midi")
    # A 256-byte buffer accommodates small differences between ZIP local and
    # central-directory extras. Larger extras use one bounded tail request.
    guess = ZIP_LOCAL_HEADER.size + len(info.filename.encode("utf-8")) + len(info.extra)
    end = min(remote.total_size, info.header_offset + guess + info.compress_size + 256)
    start = info.header_offset
    raw = remote._get_range(start, end - 1)
    if len(raw) < ZIP_LOCAL_HEADER.size:
        raise ValueError("truncated_zip_local_header")
    (signature, _, flags, method, _, _, _, _, _, name_size, extra_size) = ZIP_LOCAL_HEADER.unpack_from(raw)
    if signature != ZIP_LOCAL_SIGNATURE or flags & 1 or method != info.compress_type:
        raise ValueError("unsupported_zip_local_header")
    offset = ZIP_LOCAL_HEADER.size + name_size + extra_size
    finish = offset + info.compress_size
    if finish > MAX_COMPRESSED_SIZE + 70_000:
        raise ValueError("zip_member_limit_exceeded")
    if finish > len(raw):
        tail_end = start + finish
        if tail_end > remote.total_size:
            raise ValueError("zip_member_out_of_bounds")
        raw += remote._get_range(start + len(raw), tail_end - 1)
    compressed = raw[offset:finish]
    if method == zipfile.ZIP_STORED:
        midi = compressed
    else:
        inflater = zlib.decompressobj(-15)
        midi = inflater.decompress(compressed, MAX_MIDI_SIZE + 1)
        if not inflater.eof or inflater.unconsumed_tail or not inflater.flush() == b"":
            raise ValueError("invalid_zip_deflate_stream")
    if (len(midi) != info.file_size or len(midi) > MAX_MIDI_SIZE
            or zlib.crc32(midi) & 0xffffffff != info.CRC):
        raise ValueError("zip_member_checksum_mismatch")
    return midi


def family(program: int, channel: int) -> str:
    if channel == 9:  # General MIDI percussion channel (0-indexed).
        return "drums"
    return FAMILIES[program // 8] if 0 <= program < 128 else "unknown"


def inspect_midi(midi_data: bytes) -> dict:
    """Count note-bearing instruments, not merely nominal tracks/programs."""
    import mido

    score = mido.MidiFile(file=io.BytesIO(midi_data), clip=True)
    counts: Counter[str] = Counter()
    active_tracks: set[int] = set()
    active_parts: set[tuple[int, int, int]] = set()
    timeline: list[tuple[int, str]] = []
    undeclared_program_notes = 0
    for track_index, track in enumerate(score.tracks):
        ticks = 0
        programs: dict[int, int] = {}
        for msg in track:
            ticks += msg.time
            if msg.type == "program_change":
                programs[msg.channel] = msg.program
            elif msg.type == "note_on" and msg.velocity > 0:
                channel = msg.channel
                program = programs.get(channel, 0)
                if channel != 9 and channel not in programs:
                    undeclared_program_notes += 1
                category = family(program, channel)
                counts[category] += 1
                timeline.append((ticks, category))
                active_tracks.add(track_index)
                active_parts.add((track_index, channel, -1 if channel == 9 else program))

    max_tick = max((tick for tick, _ in timeline), default=0)
    category_buckets: dict[str, set[int]] = {}
    for tick, category in timeline:
        bucket = min(TIME_BUCKETS - 1, (tick * TIME_BUCKETS) // max(1, max_tick + 1))
        category_buckets.setdefault(category, set()).add(bucket)
    trio = ("guitar", "bass", "drums")
    trio_present = all(counts[item] >= MIN_INSTRUMENT_NOTES for item in trio)
    trio_sustained = (trio_present and score.type in (0, 1)
                      and all(len(category_buckets.get(item, ())) >= MIN_ACTIVE_BUCKETS
                              for item in trio))
    try:
        length_sec = float(score.length)
    except (ValueError, TypeError):
        length_sec = None
    return {
        "midi_type": score.type,
        "duration_seconds": round(length_sec, 1) if length_sec is not None else None,
        "declared_tracks": len(score.tracks),
        "note_bearing_tracks": len(active_tracks),
        "note_bearing_parts": len(active_parts),
        "total_notes": sum(counts.values()),
        "notes_by_family": dict(counts),
        "families": sorted(counts),
        "undeclared_program_notes": undeclared_program_notes,
        "piano_only": set(counts) == {"piano"},
        "drums_only": set(counts) == {"drums"},
        "guitar_bass_drums_present": trio_present,
        "guitar_bass_drums_sustained": trio_sustained,
        "family_active_buckets": {name: len(buckets)
                                  for name, buckets in category_buckets.items()},
    }


def summarize(rows: list[dict], failures: Counter[str]) -> dict:
    categories = Counter()
    family_present = Counter()
    family_notes = Counter()
    tracks = Counter()
    notes = []
    durations = []
    for result in rows:
        for flag in ("piano_only", "drums_only", "guitar_bass_drums_present",
                     "guitar_bass_drums_sustained"):
            if result[flag]:
                categories[flag] += 1
        if result["note_bearing_tracks"] >= 2:
            categories["two_or_more_note_tracks"] += 1
        if result["note_bearing_parts"] >= 3:
            categories["three_or_more_note_parts"] += 1
        for instrument, n in result["notes_by_family"].items():
            family_present[instrument] += 1
            family_notes[instrument] += n
        tracks[str(min(result["note_bearing_tracks"], 8)) + ("+" if result["note_bearing_tracks"] >= 8 else "")] += 1
        notes.append(result["total_notes"])
        if result["duration_seconds"] is not None:
            durations.append(result["duration_seconds"])
    denom = len(rows)
    return {
        "parsed_files": denom,
        "failed_files": sum(failures.values()),
        "failure_types": dict(failures),
        "flag_counts": dict(categories),
        "flag_percent_of_parsed": {name: round(100 * count / denom, 1)
                                   for name, count in categories.items()} if denom else {},
        "files_with_family": dict(family_present),
        "notes_by_family": dict(family_notes),
        "note_track_distribution_8_plus": dict(tracks),
        "median_notes": round(statistics.median(notes), 1) if notes else None,
        "median_duration_seconds": round(statistics.median(durations), 1) if durations else None,
        "duration_available_count": len(durations),
    }


def run_audit() -> dict:
    deadline = time.monotonic() + MAX_SECONDS
    remote = RangeFile(XMIDI_URL, max_bytes=MAX_ZIP_BYTES, max_requests=MAX_ZIP_REQUESTS)
    with zipfile.ZipFile(remote) as archive:
        groups, population = choose_samples(archive.infolist())
    print(json.dumps({"phase": "indexed", "selection": {name: len(entries)
                      for name, entries in groups.items()}, "zip_requests": remote.requests}), flush=True)
    result = {
        "method": "actual MIDI note events and GM program/channel, not audio stem recognition",
        "sampling": population,
        "limits": {"max_zip_bytes": MAX_ZIP_BYTES, "max_zip_requests": MAX_ZIP_REQUESTS,
                   "max_seconds": MAX_SECONDS, "max_midi_uncompressed_bytes": MAX_MIDI_SIZE},
    }
    for group_name, entries in groups.items():
        rows = []
        failures: Counter[str] = Counter()
        for i, entry in enumerate(entries):
            if time.monotonic() > deadline:
                result["status"] = "time_budget_exceeded"
                break
            try:
                data = read_midi_one_range(remote, entry)
                rows.append(inspect_midi(data))
            except (ValueError, EOFError, OSError, IndexError, TypeError) as exc:
                failures[type(exc).__name__] += 1
            if (i + 1) % 50 == 0:
                print(json.dumps({"phase": "sample_progress", "group": group_name,
                                  "processed": i + 1, "selected": len(entries),
                                  "zip_requests": remote.requests}), flush=True)
        result[group_name] = {
            "selected": len(entries),
            "summary": summarize(rows, failures),
            "sample_genres": dict(Counter((labels_from_filename(item.filename)["genre"]
                                          or "unknown").lower() for item in entries).most_common(12)),
        }
        if result.get("status"):
            break
    result["zip_network_bytes"] = remote.downloaded
    result["zip_range_requests"] = remote.requests
    result["elapsed_seconds"] = round(MAX_SECONDS - max(0, deadline - time.monotonic()), 1)
    result.setdefault("status", "complete")
    result["limitations"] = [
        "The general sample alone estimates XMIDI overall; targeted pop/rock must not be pooled.",
        "MIDI programs are declared timbres, not proof of acoustically faithful parts.",
        "The sustained trio flag only measures note-on coverage of 4/16 temporal bins.",
        "MIDI filenames contain emotion/genre but no verified artist/title identifiers.",
    ]
    return result


def main() -> None:
    try:
        result = run_audit()
    except Exception as exc:
        # Never log potentially signed URLs or musical payloads.
        print(json.dumps({"status": "inconclusive_error", "exception_type": type(exc).__name__}))
        raise SystemExit(1) from None
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["status"] != "complete":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
