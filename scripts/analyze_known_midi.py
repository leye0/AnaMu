"""Analyze any existing MIDI with AnaMu's previously calibrated emotion model.

No emotion annotations are read. Each input MIDI receives per-measure
valence/arousal estimates and honest coverage/warning metadata.

Example:
  python -m scripts.analyze_known_midi --model /tmp/anamu-model.json \
      --json-out /tmp/bach-emotions.json /path/to/known-bach.mid

Optional: --jsymbolic-ace /path/to/original-jSymbolic-output.xml
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from anamu.emotion_pipeline import (analyze_known_midi, execute_original_jsymbolic,
                                    load_ridge_artifact)
from anamu.jsymbolic_ace import read_jsymbolic_ace


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, type=Path,
                        help="safe JSON model produced by --model-out on VGMIDI")
    parser.add_argument("--json-out", required=True, type=Path)
    java_group = parser.add_mutually_exclusive_group()
    java_group.add_argument("--jsymbolic-ace", type=Path,
                        help="optional original Java ACE XML OR checksum-verified jSymbolic batch directory")
    java_group.add_argument("--jsymbolic-jar", type=Path,
                            help="run the original Java engine on each new piece")
    parser.add_argument("--measure-count", type=int,
                        help="explicit measure count if known from verified human grid")
    parser.add_argument("midis", type=Path, nargs="+", help="known original MIDI compositions")
    args = parser.parse_args()
    artifact = load_ridge_artifact(args.model)
    java = {}
    if args.jsymbolic_ace:
        if args.jsymbolic_ace.is_dir():
            from scripts.vgmidi_temporal_benchmark import load_original_jsymbolic_index
            java = load_original_jsymbolic_index(args.jsymbolic_ace)
        else:
            parsed = read_jsymbolic_ace(args.jsymbolic_ace, nonfinite_as_missing=True,
                                        max_bytes=300_000_000)
            for record in parsed["data_sets"]:
                name = Path(record["source_id"]).name
                if name in java:
                    parser.error(f"duplicate_original_jsymbolic_piece: {name}")
                java[name] = record
    results = []
    for midi in args.midis:
        record = java.get(midi.name)
        error = None
        if args.jsymbolic_jar:
            try:
                record = execute_original_jsymbolic(midi, args.jsymbolic_jar)
            except Exception as exc:
                # A single upstream Java failure must never become a fake
                # academic observation or block the rest of the batch.
                error = f"original_jsymbolic_unavailable:{type(exc).__name__}:{str(exc)[:160]}"
        results.append(analyze_known_midi(
            midi, artifact, jsymbolic_record=record,
            n_measures=args.measure_count))
        if error:
            results[-1]["warnings"].append(error)
        print(f"{midi.name}: {results[-1]['measure_count']} bars, "
              f"{results[-1]['available_feature_columns']}/"
              f"{results[-1]['trained_feature_columns']} model features available", flush=True)
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps({"model": str(args.model),
                                         "analyses": results},
                                        ensure_ascii=False, allow_nan=False,
                                        indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
