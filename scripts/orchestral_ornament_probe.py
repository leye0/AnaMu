"""Inventory strictly notated passing/neighbor figures in orchestral scores.

Usage: python -m scripts.orchestral_ornament_probe [MXL ...] [--top 3]
Neither a functional-harmony classifier nor an aesthetic evaluation.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from anamu.orchestral_ornaments import score_ornamental_figures
from anamu.score_texture import score_texture_from_mxl


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCORES = (
    ROOT / "data/orchestral/hauptstimme-beethoven5-movement1.mxl",
    ROOT / "data/orchestral/hauptstimme-beethoven7-movement2.mxl",
)


def inspect(paths: list[Path], *, top: int = 3) -> dict:
    if not 0 <= top <= 100:
        raise ValueError("invalid_ornament_preview_limit")
    rows = []
    for path in paths:
        evidence = score_texture_from_mxl(path.read_bytes())
        figures = score_ornamental_figures(evidence)
        # Examples with unchanged, supporting accompaniment are easiest to
        # audit. This does not imply musical superiority or an NCT label.
        examples = sorted(figures, key=lambda f: (
            not f.stable_accompaniment_support_candidate,
            f.moments[0].measure_index, f.moments[0].onset_quarters,
            f.part_id))[:top]
        rows.append({
            "file": str(path),
            "source_sha256": evidence.source_sha256,
            "total_strict_three_note_figures": len(figures),
            "diatonic_passing_figures": sum(f.kind == "diatonic_passing_figure"
                                            for f in figures),
            "diatonic_neighbor_figures": sum(f.kind == "diatonic_neighbor_figure"
                                             for f in figures),
            "figures_with_unchanged_accompaniment": sum(
                f.accompaniment_unchanged for f in figures),
            "figures_with_strict_backing_support": sum(
                f.stable_accompaniment_support_candidate for f in figures),
            "distinct_measures_with_figure": len({
                f.moments[0].measure_index for f in figures}),
            "examples": [{
                "part_id": f.part_id,
                "voice": f.voice,
                "staff": f.staff,
                "kind": f.kind,
                "source_note_ids": f.source_note_ids,
                "measure_index": f.moments[0].measure_index,
                "onsets_quarters": [str(m.onset_quarters) for m in f.moments],
                "sounding_pitches": f.sounding_pitches,
                "written_pitches": f.written_pitches,
                "other_parts_pitch_classes": f.other_parts_pitch_classes,
                "stable_accompaniment_support_candidate": (
                    f.stable_accompaniment_support_candidate),
                "status": f.status,
            } for f in examples],
        })
    return {
        "claim": "melodic_ornamental_figures_not_nonchord_tone_labels",
        "method": "spelled_diatonic_steps_three_contiguous_notated_attacks",
        "limitations": [
            "no_verified_harmonic_reduction_or_local_key",
            "no_metric_accent_or_suspension_classification",
            "chromatic_neighbors_and_passing_figures_not_detected",
            "no_cross_measure_linking_rests_ties_chords_or_repeat_unfolding",
            "accompaniment_pitch_class_support_not_equivalent_to_chord_membership",
            "overlapping_three_note_windows_not_independent_samples",
        ],
        "pieces": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scores", nargs="*", type=Path)
    parser.add_argument("--top", type=int, default=3)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.dumps(inspect(args.scores or list(DEFAULT_SCORES),
                                 top=args.top), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
        print(f"Written {args.output}")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
