"""Download a bounded, pinned PIAST-AT CSV+MIDI subset (no audio).

Examples:
  python -m scripts.fetch_piast_at /tmp/piast-at --limit 200
  python -m scripts.fetch_piast_at /tmp/piast-at --limit 0  # all MIDI matches

The HF tree endpoint is paginated; the dataset has 1,900 exact CSV↔MIDI
filename matches at the pinned revision, not all 2,023 annotated clips.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import quote

from anamu.piast_at import REPOSITORY, REVISION, available_annotations, load_annotations


BASE = f"https://huggingface.co/datasets/{REPOSITORY}/resolve/{REVISION}/piast_at"
API = f"https://huggingface.co/api/datasets/{REPOSITORY}/tree/{REVISION}/piast_at/midi?recursive=true"


def _read_limited(url: str, cap: int) -> bytes:
    with urllib.request.urlopen(url, timeout=35) as response:
        payload = response.read(cap + 1)
    if len(payload) > cap:
        raise ValueError("piast_download_exceeds_size_limit")
    return payload


def fetch_index() -> set[str]:
    names = set()
    next_url = API
    while next_url:
        with urllib.request.urlopen(next_url, timeout=35) as response:
            items = json.loads(response.read(400_000))
            link = response.headers.get("Link", "")
        for item in items:
            path = item.get("path", "")
            if item.get("type") == "file" and path.startswith("piast_at/midi/"):
                name = path.rsplit("/", 1)[-1]
                if re.fullmatch(r"[A-Za-z0-9_-]{6,80}\.mid", name):
                    names.add(name)
        match = re.search(r'<([^>]+)>;\s*rel="next"', link)
        next_url = match.group(1) if match else None
    return names


def fetch(root: Path, *, limit: int = 200, workers: int = 8,
          seed: int = 20261108) -> dict:
    if limit < 0 or not 1 <= workers <= 16:
        raise ValueError("invalid_piast_fetch_budget")
    root.mkdir(parents=True, exist_ok=True)
    csv_path = root / "at_text.csv"
    csv_data = _read_limited(f"{BASE}/at_text.csv", 1_000_000)
    csv_path.write_bytes(csv_data)
    all_clips = load_annotations(csv_path)
    names = fetch_index()
    available = available_annotations(all_clips, names)
    # The benchmark's split uses an independent salt ("split-v1|").
    order = sorted(available, key=lambda c: hashlib.sha256(
        f"{seed}|{c.clip_id}".encode()).hexdigest())
    chosen = order[:limit] if limit else order
    midi_root = root / "midi"
    midi_root.mkdir(exist_ok=True)

    def one(clip):
        target = midi_root / clip.midi_name
        if target.is_file() and target.stat().st_size >= 14:
            return clip, "existing"
        source = BASE + "/midi/" + quote(clip.midi_name)
        content = _read_limited(source, 1_000_000)
        if not content.startswith(b"MThd"):
            raise ValueError("piast_download_not_midi")
        target.write_bytes(content)
        return clip, "downloaded"

    errors = []
    fetched = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        tasks = {pool.submit(one, clip): clip for clip in chosen}
        for index, future in enumerate(as_completed(tasks), 1):
            try:
                clip, state = future.result()
                fetched.append(clip.clip_id)
            except (OSError, ValueError, RuntimeError) as exc:
                errors.append({"clip": tasks[future].clip_id, "reason": str(exc)[:120]})
            if index % 50 == 0:
                print(f"PIAST MIDI {index}/{len(chosen)}, errors={len(errors)}", flush=True)
    result = {
        "source": REPOSITORY, "revision": REVISION,
        "annotated_clips": len(all_clips), "published_midis": len(names),
        "exact_midi_matches": len(available),
        "unmatched_annotations": len(all_clips) - len(available),
        "requested": len(chosen), "downloaded_or_present": len(fetched),
        "errors": errors, "selected_clips": sorted(fetched),
        "annotation_sha256": hashlib.sha256(csv_data).hexdigest(),
    }
    (root / "fetch-manifest.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--limit", type=int, default=200, help="0 downloads all matches")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=20261108)
    args = parser.parse_args()
    print(json.dumps(fetch(args.directory, limit=args.limit, workers=args.workers,
                           seed=args.seed), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
