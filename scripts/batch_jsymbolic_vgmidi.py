"""Run the ORIGINAL jSymbolic 2.2 Java on VGMIDI, in bounded batches.

This does not synthesize jSymbolic-like features: it runs the official JAR
and saves its native ACE XML. A run is resumable by existing verified files.
The source MIDI is never copied into the result directory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

from anamu.jsymbolic_ace import read_jsymbolic_ace
from anamu.vgmidi_temporal import extract_midi_measures, load_human_pieces


def run(root: Path, jar: Path, output: Path, *, window_seconds: float = 10.,
        batch_size: int = 25, max_minutes_per_batch: int = 20) -> dict:
    if not jar.is_file() or window_seconds <= 0 or batch_size < 1:
        raise ValueError("invalid_original_jsymbolic_configuration")
    pieces = load_human_pieces([root / f"vgmidi_raw_{i}.json" for i in (1, 2)])
    admitted = []
    rejected = {}
    for piece in pieces:
        path = root / "midi" / piece.filename
        try:
            extract_midi_measures(path, piece.n_measures)
            admitted.append(path)
        except (ValueError, OSError) as exc:
            rejected[piece.filename] = str(exc)
    output.mkdir(parents=True, exist_ok=True)
    manifest = {"origin": "jSymbolic original 2.2 Java", "source": "VGMIDI original MIDI files",
                "window_seconds": window_seconds, "overlap": 0.0,
                "eligible": len(admitted), "rejected": rejected, "batches": []}
    for idx in range(0, len(admitted), batch_size):
        batch = admitted[idx:idx + batch_size]
        prefix = output / f"batch-{idx // batch_size:03d}"
        xml = prefix.with_suffix(".xml")
        definitions = output / "definitions.xml"
        if xml.is_file():
            parsed = read_jsymbolic_ace(xml, max_bytes=300_000_000,
                                        nonfinite_as_missing=True)
            if parsed["data_set_count"] > len(batch):
                raise ValueError(f"existing_batch_count_mismatch: {xml}")
        else:
            # Stable symlink names (not copied MIDI) preserve exact original
            # identifiers and make ACE data-set identities auditable.
            with tempfile.TemporaryDirectory(prefix="anamu-jsym-") as temp:
                input_directory = Path(temp)
                for path in batch:
                    (input_directory / path.name).symlink_to(path.resolve())
                command = ["java", "-Xmx3g", "-jar", str(jar.resolve()),
                           "-csv", "-window", str(input_directory),
                           str(xml.resolve()), str(definitions.resolve()),
                           str(window_seconds), "0"]
                result = subprocess.run(command, cwd=jar.parent, capture_output=True,
                                        text=True, timeout=max_minutes_per_batch * 60)
                if result.returncode:
                    raise RuntimeError(f"jsymbolic_batch_failed_{idx}: " + result.stderr[-1200:])
                parsed = read_jsymbolic_ace(xml, max_bytes=300_000_000,
                                            nonfinite_as_missing=True)
        names = {Path(record["source_id"]).name for record in parsed["data_sets"]}
        expected = {p.name for p in batch}
        if not names.issubset(expected):
            raise ValueError(f"jsymbolic_unexpected_midi_in_batch_{idx}")
        missing = sorted(expected - names)
        manifest["batches"].append({
            "file": xml.name, "sha256": hashlib.sha256(xml.read_bytes()).hexdigest(),
            "pieces": sorted(names), "failed_original_java": missing,
            "windows": parsed["window_count"],
            "bytes": xml.stat().st_size,
        })
        print(f"jSymbolic original batch {idx // batch_size + 1}: "
              f"{len(names)}/{len(batch)} pieces, {parsed['window_count']} windows",
              flush=True)
    target = output / "manifest.json"
    target.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--jar", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--window-seconds", type=float, default=10.)
    parser.add_argument("--batch-size", type=int, default=25)
    args = parser.parse_args()
    manifest = run(args.root, args.jar, args.out,
                   window_seconds=args.window_seconds, batch_size=args.batch_size)
    print(f"done: {manifest['eligible']} eligible pieces, "
          f"{len(manifest['batches'])} original Java batches")


if __name__ == "__main__":
    main()
