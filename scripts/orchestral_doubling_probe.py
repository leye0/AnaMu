"""Inspect orchestral unison/octave writing and honest in-piece reconstruction.

Usage: python -m scripts.orchestral_doubling_probe [MXL ...] [--top 5]
No playback, learned model, human quality judgment or file writes by default.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from anamu.orchestral_counterfactual import doubling_reconstruction_trials
from anamu.score_texture import discover_exact_octave_doublings, score_texture_from_mxl


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCORES = (
    ROOT / "data/orchestral/hauptstimme-beethoven5-movement1.mxl",
    ROOT / "data/orchestral/hauptstimme-beethoven7-movement2.mxl",
)


def inspect(paths: list[Path], *, top: int = 5,
            training_notes: int = 3, prediction_notes: int = 3) -> dict:
    if not 0 <= top <= 100:
        raise ValueError("invalid_orchestration_preview_budget")
    rows = []
    for path in paths:
        evidence = score_texture_from_mxl(path.read_bytes())
        discovered = discover_exact_octave_doublings(evidence)
        trials = doubling_reconstruction_trials(
            evidence, training_notes=training_notes,
            prediction_notes=prediction_notes)
        parts = {part.id: part for part in evidence.parts}
        correct = sum(sum(trial.exact_matches) for trial in trials)
        baseline = sum(sum(trial.constant_pitch_baseline_matches)
                       for trial in trials)
        unison_baseline = sum(sum(trial.unison_copy_baseline_matches)
                              for trial in trials)
        predictions = sum(len(trial.generated) for trial in trials)
        rows.append({
            "file": str(path), "source_sha256": evidence.source_sha256,
            "notated_pitch_fragments": len(evidence.notes),
            "score_parts": len(evidence.parts),
            "score_measures_in_written_order": evidence.measure_count,
            "grace_notes_excluded": evidence.grace_notes_excluded,
            "cue_notes_excluded": evidence.cue_notes_excluded,
            "exact_unison_octave_doubling_candidates": len(discovered),
            "doubling_examples": [{
                "part_a": {"id": c.part_a, "label": parts[c.part_a].label},
                "part_b": {"id": c.part_b, "label": parts[c.part_b].label},
                "octave_offset": c.octave_offset,
                "notated_note_pairs": len(c.source_note_pairs),
                "first_measure_index": c.start_measure_index,
                "last_measure_index": c.end_measure_index,
                "source_note_pairs_preview": c.source_note_pairs[:3],
                "status": c.status,
            } for c in discovered[:top]],
            "in_piece_counterfactual": {
                "trials": len(trials),
                "held_out_target_notes_predicted": predictions,
                "exact_matches": correct,
                "constant_last_pitch_baseline_matches": baseline,
                "copy_source_unison_baseline_matches": unison_baseline,
                "exact_match_rate": (correct / predictions if predictions else None),
                "baseline_match_rate": (baseline / predictions if predictions else None),
                "unison_baseline_match_rate": (
                    unison_baseline / predictions if predictions else None),
            },
        })
    return {
        "claim": "exact_score_orchestration_structure_not_composition_quality",
        "scoring": "prefix_only_target_observed_then_future_target_hidden_until_comparison",
        "independence_warning": "multiple_overlapping_instrument_pairs_from_same_compositions",
        "limitations": [
            "no_human_listening_or_arrangement_quality_test",
            "no_repeat_unfolding_no_audio_or_timbre_extraction",
            "ties_not_merged_chord_attacks_not_used_for_doubling",
            "no_held_out_composer_or_independent_composition",
        ],
        "parameters": {"training_notes": training_notes,
                       "prediction_notes": prediction_notes,
                       "preview_top": top},
        "pieces": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scores", nargs="*", type=Path)
    parser.add_argument("--top", default=5, type=int)
    parser.add_argument("--training-notes", default=3, type=int)
    parser.add_argument("--prediction-notes", default=3, type=int)
    parser.add_argument("--output", type=Path,
                        help="Optional JSON report path; stdout by default")
    args = parser.parse_args()
    report = inspect(args.scores or list(DEFAULT_SCORES),
                     top=args.top, training_notes=args.training_notes,
                     prediction_notes=args.prediction_notes)
    result = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(result, encoding="utf-8")
        print(f"Written {args.output}")
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
