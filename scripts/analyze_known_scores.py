"""Real classical scores -> MIDI -> AnaMu emotion analysis.

Uses scores distributed with music21's public-domain corpus. These pieces
have NO VGMIDI human emotion annotations; outputs are inferred trajectories,
not quantitative validation against their listeners.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path

from anamu.emotion_pipeline import (analyze_known_midi, execute_original_jsymbolic,
                                    load_ridge_artifact)


SCORES = (
    ("Bach — BWV 66.6, chorale", "bach/bwv66.6", "bach-bwv66-6.mid"),
    ("Chopin — Mazurka op. 6 no. 2", "chopin/mazurka06-2", "chopin-mazurka-op6-no2.mid"),
)

EXTRA_SCORES = (
    ("Bach — BWV 140.7, chorale", "bach/bwv140.7", "bach-bwv140-7.mid"),
    ("Mozart — Sonate K. 545, exposition", "mozart/k545/movement1_exposition",
     "mozart-k545-exposition.mid"),
    ("Beethoven — Quatuor op. 18 no 1, mouvement 3",
     "beethoven/opus18no1/movement3", "beethoven-op18no1-movement3.mid"),
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path,
                        default=Path("models/vgmidi-piano-ridge.json.gz"))
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--jsymbolic-jar", type=Path,
                        help="run the genuine original Java engine on these two works")
    parser.add_argument("--jsymbolic-timeout", type=int, default=120,
                        help="seconds for the original 10-second Java window run")
    parser.add_argument("--jsymbolic-fallback-window", type=float, default=30.,
                        help="longer original Java windows after a timeout")
    parser.add_argument("--jsymbolic-fallback-timeout", type=int, default=120)
    parser.add_argument("--expanded", action="store_true",
                        help="analyze five identified classical works instead of two")
    args = parser.parse_args()
    from music21 import corpus, stream

    artifact = load_ridge_artifact(args.model)
    # Fingerprint the model's uncompressed JSON, irrespective of whether it
    # came from the CI artifact or the compressed checked-in distribution.
    model_bytes = (gzip.decompress(args.model.read_bytes())
                   if args.model.suffix == ".gz" else args.model.read_bytes())
    args.out.mkdir(parents=True, exist_ok=True)
    analyses = []
    for title, work, filename in SCORES + (EXTRA_SCORES if args.expanded else ()):
        score = corpus.parse(work)
        # music21's MIDI writer expands some imported repeat marks, yielding
        # unverified playback lengths (e.g. Beethoven op.18/1 mov.3: 456 MIDI
        # bars vs 145 written measures). Analyze the unrolled *written score*
        # consistently across composers, without guessing performance repeats.
        linear = stream.Score()
        for part in score.parts:
            target = stream.Part()
            for event in part.flatten():
                target.insert(event.offset, event)
            linear.insert(0, target)
        score = linear
        score_caveat = "written-score order; original repeats not expanded"
        if work.startswith("chopin/"):
            score_caveat += "; source repeat marks malformed"
        midi = args.out / filename
        score.write("midi", fp=str(midi))
        record = None
        original_java_error = None
        if args.jsymbolic_jar:
            try:
                record = execute_original_jsymbolic(
                    midi, args.jsymbolic_jar, timeout_seconds=args.jsymbolic_timeout,
                    fallback_window_seconds=args.jsymbolic_fallback_window,
                    fallback_timeout_seconds=args.jsymbolic_fallback_timeout)
            except Exception as exc:
                # Keep the known composition, mark the original tool missing.
                original_java_error = f"original_jsymbolic_unavailable:{type(exc).__name__}"
        analyzed = analyze_known_midi(midi, artifact, jsymbolic_record=record)
        if original_java_error:
            analyzed["warnings"].append(original_java_error)
        analyzed.update({"known_composition": title,
                         "original_score_reference": work,
                         "source": "music21 bundled corpus; rendered as MIDI for analysis"})
        if score_caveat:
            analyzed["warnings"].append(score_caveat)
        analyses.append(analyzed)
        print(f"{title}: {analyzed['measure_count']} mesures; "
              f"{analyzed['available_feature_columns']}/"
              f"{analyzed['trained_feature_columns']} features", flush=True)
    report = args.out / ("known-classics-emotions.json" if args.expanded
                         else "bach-chopin-emotions.json")
    report.write_text(json.dumps({"status": "inferred_not_human_verified",
                                  "calibrated_artifact_sha256": hashlib.sha256(
                                      model_bytes).hexdigest(),
                                  "analyses": analyses}, ensure_ascii=False,
                                 indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(f"Wrote {report}")


if __name__ == "__main__":
    main()
