"""Check score-vertical effects of a proposed contrary-to-parallel edit.

Usage: python -m scripts.orchestral_harmonic_context_probe [MXL ...] [--top 3]
No tonal-function inference, aesthetic scores, audio or paid services.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from anamu.orchestral_harmony import ScoreSonorityIndex
from anamu.orchestral_voice_leading import (
    propose_voice_motion_edit, score_voice_leading,
)
from anamu.score_texture import score_texture_from_mxl


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCORES = (
    ROOT / "data/orchestral/hauptstimme-beethoven5-movement1.mxl",
    ROOT / "data/orchestral/hauptstimme-beethoven7-movement2.mxl",
)


def inspect(paths: list[Path], *, top: int = 3) -> dict:
    if not 0 <= top <= 100:
        raise ValueError("invalid_harmonic_preview_limit")
    rows = []
    for path in paths:
        evidence = score_texture_from_mxl(path.read_bytes())
        index = ScoreSonorityIndex(evidence)
        observed = score_voice_leading(evidence)
        examined = shape_before = shape_disappeared = added = bass_change = 0
        rejected_out_of_range = 0
        examples = []
        for motion in observed:
            if motion.motion_type != "contrary":
                continue
            try:
                edit = propose_voice_motion_edit(motion, "parallel")
            except ValueError as exc:
                if str(exc) != "hypothetical_pitch_outside_midi_range":
                    raise
                rejected_out_of_range += 1
                continue
            context = index.context_for_edit(motion, edit)
            examined += 1
            original_match = bool(context.original.matching_templates)
            shape_before += original_match
            shape_disappeared += (original_match and
                                  not context.proposed.matching_templates)
            added += bool(context.pitch_classes_added)
            bass_change += context.changes_lowest_sounding_pitch
            # Favor examples with a specific original pitch-class template;
            # this is a preview choice, not model selection or quality ranking.
            if len(examples) < top and original_match:
                examples.append({
                    "score_note_id_to_change": edit.target_note_id,
                    "parts": [motion.part_a, motion.part_b],
                    "measure_index": motion.to_moment.measure_index,
                    "onset_quarters": str(motion.to_moment.onset_quarters),
                    "original_pitch": edit.original_sounding_pitch,
                    "proposed_pitch": edit.proposed_sounding_pitch,
                    "active_source_note_ids": context.original.active_source_note_ids,
                    "original_pitch_classes": context.original.pitch_classes,
                    "proposed_pitch_classes": context.proposed.pitch_classes,
                    "added_pitch_classes": context.pitch_classes_added,
                    "removed_pitch_classes": context.pitch_classes_removed,
                    "original_template_matches": [
                        {"shape": t.shape, "root_pitch_class": t.root_pitch_class,
                         "bass_member_index": t.bass_chord_member_index}
                        for t in context.original.matching_templates],
                    "proposed_template_matches": [
                        {"shape": t.shape, "root_pitch_class": t.root_pitch_class,
                         "bass_member_index": t.bass_chord_member_index}
                        for t in context.proposed.matching_templates],
                    "changed_lowest_note": context.changes_lowest_sounding_pitch,
                    "status": context.status,
                })
        rows.append({
            "file": str(path), "source_sha256": evidence.source_sha256,
            "score_note_fragments": len(evidence.notes),
            "contrary_motions_total": sum(o.motion_type == "contrary"
                                            for o in observed),
            "hypothetical_parallel_edits_examined": examined,
            "hypothetical_edits_outside_midi_range": rejected_out_of_range,
            "original_exact_template_matches": shape_before,
            "exact_template_no_longer_matches": shape_disappeared,
            "edits_adding_pitch_class": added,
            "edits_changing_notated_lowest_pitch": bass_change,
            "examples": examples,
        })
    return {
        "claim": "vertical_pitch_material_effect_not_harmonic_function_or_quality",
        "method": "score_local_sustained_notes_and_exact_pitch_class_set_templates",
        "limitations": [
            "nonchord_tones_key_modulation_and_enharmonic_spelling_not_resolved",
            "no_long_range_ties_or_repeat_unfolding_beyond_local_measure",
            "the_edit_is_not_an_aesthetic_or_orchestration_recommendation",
            "observations_share_notes_within_each_composition",
        ],
        "parameters": {"preview_top": top},
        "pieces": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scores", nargs="*", type=Path)
    parser.add_argument("--top", type=int, default=3)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = inspect(args.scores or list(DEFAULT_SCORES), top=args.top)
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
        print(f"Written {args.output}")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
