"""Real Bach/Chopin scores -> MIDI -> AnaMu emotion analysis.

Uses scores distributed with music21's public-domain corpus. These pieces
have NO VGMIDI human emotion annotations; outputs are inferred trajectories,
not quantitative validation against their listeners.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from anamu.emotion_pipeline import (analyze_known_midi, execute_original_jsymbolic,
                                    load_ridge_artifact)


SCORES = (
    ("Bach — BWV 66.6, chorale", "bach/bwv66.6", "bach-bwv66-6.mid"),
    ("Chopin — Mazurka op. 6 no. 2", "chopin/mazurka06-2", "chopin-mazurka-op6-no2.mid"),
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--jsymbolic-jar", type=Path,
                        help="run the genuine original Java engine on these two works")
    args = parser.parse_args()
    from music21 import corpus, stream

    artifact = load_ridge_artifact(args.model)
    args.out.mkdir(parents=True, exist_ok=True)
    analyses = []
    for title, work, filename in SCORES:
        score = corpus.parse(work)
        score_caveat = None
        if work.startswith("chopin/"):
            # The distributed Humdrum Mazurka has malformed repeat symbols
            # for music21's automatic repeat expander. Preserve its original
            # written note order/timing by flattening each part; do not invent
            # an unverified performed repeat sequence.
            linear = stream.Score()
            for part in score.parts:
                target = stream.Part()
                for event in part.flatten():
                    target.insert(event.offset, event)
                linear.insert(0, target)
            score = linear
            score_caveat = "notated order only; malformed source repeats not performed/unrolled"
        midi = args.out / filename
        score.write("midi", fp=str(midi))
        record = None
        original_java_error = None
        if args.jsymbolic_jar:
            try:
                record = execute_original_jsymbolic(midi, args.jsymbolic_jar)
            except Exception as exc:
                # Keep the known composition, mark the original tool missing.
                original_java_error = f"original_jsymbolic_unavailable:{type(exc).__name__}:{str(exc)[:160]}"
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
    report = args.out / "bach-chopin-emotions.json"
    report.write_text(json.dumps({"status": "inferred_not_human_verified",
                                  "calibrated_artifact_sha256": hashlib.sha256(
                                      args.model.read_bytes()).hexdigest(),
                                  "analyses": analyses}, ensure_ascii=False,
                                 indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(f"Wrote {report}")


if __name__ == "__main__":
    main()
