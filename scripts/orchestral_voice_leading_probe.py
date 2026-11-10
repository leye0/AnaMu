"""Part-writing report: observed motions and one counterfactual note edit.

Usage: python -m scripts.orchestral_voice_leading_probe [MXL ...] [--top 2]
No generated audio, fake aesthetic score, network calls or files by default.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from anamu.orchestral_voice_leading import (
    propose_voice_motion_edit, score_voice_leading,
)
from anamu.score_texture import score_texture_from_mxl


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MXL = (
    ROOT / "data/orchestral/hauptstimme-beethoven5-movement1.mxl",
    ROOT / "data/orchestral/hauptstimme-beethoven7-movement2.mxl",
)
MOTIONS = ("contrary", "oblique", "parallel", "similar", "static")


def inspect(paths: list[Path], *, top: int = 2) -> dict:
    if not 0 <= top <= 30:
        raise ValueError("invalid_voice_leading_preview_budget")
    rows = []
    for path in paths:
        evidence = score_texture_from_mxl(path.read_bytes())
        observed = score_voice_leading(evidence)
        names = {p.id: p.label for p in evidence.parts}
        counts = Counter(o.motion_type for o in observed)
        examples = []
        for motion in MOTIONS:
            for obs in (o for o in observed if o.motion_type == motion):
                if sum(row["motion_type"] == motion for row in examples) >= top:
                    break
                case = {
                    "motion_type": motion,
                    "parts": [{"id": obs.part_a, "label": names[obs.part_a]},
                              {"id": obs.part_b, "label": names[obs.part_b]}],
                    "first_measure_index": obs.from_moment.measure_index,
                    "second_measure_index": obs.to_moment.measure_index,
                    "pitches_sounding_midi_A0_A1_B0_B1": obs.pitches,
                    "source_note_ids": obs.source_note_ids,
                    "pitch_deltas": [obs.motion_a, obs.motion_b],
                    "intervals_before_after": [obs.interval_before,
                                               obs.interval_after],
                    "crossing": obs.crossing,
                    "perfect_parallel_class": obs.parallel_perfect_class,
                }
                if motion == "contrary":
                    try:
                        alternative = propose_voice_motion_edit(obs, "parallel")
                    except ValueError as exc:
                        case["what_if_parallel_instead"] = {
                            "status": "unavailable", "reason": str(exc)}
                    else:
                        case["what_if_parallel_instead"] = {
                            "target_source_note_id": alternative.target_note_id,
                            "original_pitch": alternative.original_sounding_pitch,
                            "proposed_pitch": alternative.proposed_sounding_pitch,
                            "status": alternative.status,
                            "perfect_parallel_class": alternative.causes_parallel_perfect,
                            "changes_crossing": alternative.changes_voice_crossing,
                        }
                examples.append(case)
        rows.append({
            "file": str(path), "score_sha256": evidence.source_sha256,
            "notated_pitch_fragments": len(evidence.notes),
            "observed_voice_leading_quartets": len(observed),
            "motion_counts": {motion: counts[motion] for motion in MOTIONS},
            "strict_crossings": sum(o.crossing for o in observed),
            "parallel_unison_or_octave": sum(
                o.parallel_perfect_class == "unison_or_octave" for o in observed),
            "parallel_fifth": sum(o.parallel_perfect_class == "fifth"
                                   for o in observed),
            "examples": examples,
        })
    return {
        "claim": "score_notation_voice_motion_not_automatic_arrangement_quality",
        "method": "consecutive_synchronized_attacks_same_notated_staff_and_voice",
        "theory_context": "traditional_Western_voice_leading_motions_not_universal_prohibitions",
        "limitations": [
            "score_parts_are_not_inferred_independent_perceptual_voices",
            "no_note_matching_on_unsynchronized_attacks_or_ties_or_chords",
            "no_transcription_audio_instrument_range_or_human_listening_test",
            "parallel_perfect_intervals_can_be_intentional_orchestral_doubling",
            "descriptive_counts_share_notes_and_are_not_independent_samples",
        ],
        "parameters": {"preview_per_motion": top},
        "pieces": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scores", type=Path, nargs="*")
    parser.add_argument("--top", default=2, type=int)
    parser.add_argument("--output", type=Path, help="Optional JSON output")
    args = parser.parse_args()
    payload = json.dumps(inspect(args.scores or list(DEFAULT_MXL), top=args.top),
                         ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
        print(f"Written {args.output}")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
