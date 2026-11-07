"""Fetch only the 200 original labelled MIDI files and human annotations.

No audio, unlabelled music, Git repository mirror or corpus files are committed.
Run: python -m scripts.fetch_vgmidi_temporal /tmp/anamu-vgmidi
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

from anamu.vgmidi_temporal import load_human_pieces


PIN = "1e62f0af8c866ded8e665cefad06dc02c35cb739"
BASE = f"https://raw.githubusercontent.com/lucasnfe/vgmidi/{PIN}"


def fetch(url: str, destination: Path, *, cap: int) -> None:
    if destination.is_file() and 0 < destination.stat().st_size <= cap:
        return
    with urlopen(url, timeout=35) as response:
        content = response.read(cap + 1)
    if not 0 < len(content) <= cap:
        raise ValueError(f"source_missing_or_abnormally_large: {destination.name}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(content)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--workers", type=int, default=12)
    args = parser.parse_args()
    if args.workers < 1 or args.workers > 16:
        parser.error("workers must be in 1..16")
    root = args.destination.resolve()
    human_files = [root / f"vgmidi_raw_{i}.json" for i in (1, 2)]
    for i, path in enumerate(human_files, 1):
        fetch(f"{BASE}/labelled/annotations/vgmidi_raw_{i}.json", path, cap=10_000_000)
    pieces = load_human_pieces(human_files)
    def get_midi(piece):
        path = root / "midi" / piece.filename
        fetch(f"{BASE}/labelled/midi/{quote(piece.filename)}", path, cap=2_000_000)
        return piece.filename
    errors = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(get_midi, p): p.filename for p in pieces}
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                errors.append(f"{futures[future]}: {exc}")
    if errors:
        raise RuntimeError(f"{len(errors)} MIDI fetches failed:\n" + "\n".join(errors[:10]))
    print(f"VGMIDI pinned {PIN}: {len(pieces)} labelled pieces available under {root}")


if __name__ == "__main__":
    main()
