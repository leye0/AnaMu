"""Bounded upstream jSymbolic 2.2 smoke test on generated, non-copyright MIDI.

The official user ZIP is obtained and SHA-256 checked by GitHub Actions.
This file does not download binaries. It runs the *original* Java program
and verifies usable ACE windowed output, which must not be conflated with
the earlier Python reimplementations of jSymbolic feature definitions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from anamu.jsymbolic_ace import read_jsymbolic_ace


def synthetic_polyphonic_midi(destination: Path) -> None:
    import mido

    midi = mido.MidiFile(type=1, ticks_per_beat=480)
    track = mido.MidiTrack()
    midi.tracks.append(track)
    track.append(mido.MetaMessage("set_tempo", tempo=500_000, time=0))
    for cycle in range(4):
        for chord in ([60, 64, 67], [62, 65, 69], [59, 62, 67], [60, 64, 67]):
            for pitch in chord:
                track.append(mido.Message("note_on", note=pitch, velocity=70 + cycle,
                                          channel=0, time=0))
            for i, pitch in enumerate(chord):
                track.append(mido.Message("note_off", note=pitch, velocity=0,
                                          channel=0, time=480 if i == 0 else 0))
    midi.save(destination)


def run_smoke(distribution: Path, output: Path) -> dict:
    jars = sorted(distribution.rglob("jSymbolic2.jar"))
    if len(jars) != 1:
        raise RuntimeError(f"expected_one_original_jsymbolic_jar_found_{len(jars)}")
    jar = jars[0]
    if not (jar.parent / "lib").is_dir():
        raise RuntimeError("original_jsymbolic_dependencies_directory_missing")
    output.mkdir(parents=True, exist_ok=True)
    midi = output / "synthetic_piano.mid"
    synthetic_polyphonic_midi(midi)
    values = output / "parsed_features.json"
    output_dir = output / "raw"
    completed = subprocess.run(
        [sys.executable, "-m", "scripts.run_jsymbolic", str(midi),
         "--jar", str(jar), "--out", str(output_dir),
         "--window-seconds", "3", "--overlap", "0.5",
         "--heap-gb", "2", "--max-minutes", "3", "--execute",
         "--json-out", str(values)],
        check=True, text=True, capture_output=True, timeout=200,
    )
    parsed = read_jsymbolic_ace(output_dir / "features.xml")
    if parsed["data_set_count"] != 1 or parsed["window_count"] < 2:
        raise RuntimeError("original_jsymbolic_smoke_missing_multiple_windows")
    features = {name for dataset in parsed["data_sets"]
                for window in dataset["windows"] for name in window["features"]}
    if not features:
        raise RuntimeError("original_jsymbolic_smoke_no_feature_values")
    summary = {"status": "original_java_executed", "distribution": "jSymbolic 2.2 user",
               "jar_sha256": hashlib.sha256(jar.read_bytes()).hexdigest(),
               "midi_sha256": hashlib.sha256(midi.read_bytes()).hexdigest(),
               "ace_sha256": parsed["input_sha256"],
               "window_count": parsed["window_count"],
               "observed_window_feature_names": len(features),
               "limitations": ["synthetic_music_only_no_human_emotion_validation",
                               "default_jsymbolic_features_not_all_available_features"]}
    (output / "smoke_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(completed.stdout[-800:])
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--distribution", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(run_smoke(args.distribution, args.out), indent=2))


if __name__ == "__main__":
    main()
