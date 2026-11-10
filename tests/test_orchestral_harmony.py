"""Score-local sonorities and consequences of an orchestral note edit."""

from __future__ import annotations

import unittest
from fractions import Fraction
from pathlib import Path

from anamu.orchestral_harmony import ScoreSonorityIndex
from anamu.orchestral_voice_leading import (
    ScoreMoment, propose_voice_motion_edit, score_voice_leading,
)
from anamu.score_texture import score_texture_from_mxl
from scripts.orchestral_harmonic_context_probe import DEFAULT_SCORES, inspect
from tests.test_score_texture import _note, _score


def _fixture():
    # At the second attack: C4 is sustained, E4 and G4 form C-major pitch set.
    # A0=D4 -> A1=E4; B0=A4 -> B1=G4: contrary motion.
    return score_texture_from_mxl(_score([
        ("P1", "Violin", "", [_note("D", 4) + _note("E", 4)]),
        ("P2", "Flute", "", [_note("A", 4) + _note("G", 4)]),
        ("P3", "Violoncello", "", [_note("C", 4, duration=8)]),
    ]))


class OrchestralHarmonyTests(unittest.TestCase):
    def test_sustained_notated_bass_part_of_vertical_triad(self):
        evidence = _fixture()
        index = ScoreSonorityIndex(evidence)
        sonority = index.at(ScoreMoment(0, Fraction(1)))
        self.assertEqual(sonority.pitch_classes, (0, 4, 7))
        self.assertEqual(len(sonority.active_source_note_ids), 3)
        self.assertEqual(sonority.bass_sounding_pitch, 60)
        self.assertEqual(len(sonority.matching_templates), 1)
        match = sonority.matching_templates[0]
        self.assertEqual(match.shape, "major_triad")
        self.assertEqual(match.root_pitch_class, 0)
        self.assertEqual(match.bass_chord_member_index, 0)
        self.assertEqual(match.status,
                         "pitch_class_template_match_not_functional_harmony")

    def test_counterfactual_captures_harmonic_material_changed_without_quality(self):
        evidence = _fixture()
        observed = next(o for o in score_voice_leading(evidence)
                        if o.part_a == "P1" and o.part_b == "P2")
        self.assertEqual(observed.motion_type, "contrary")
        variant = propose_voice_motion_edit(observed, "parallel")
        self.assertEqual(variant.proposed_sounding_pitch, 71)  # B4 instead of G4
        context = ScoreSonorityIndex(evidence).context_for_edit(observed, variant)
        self.assertEqual(context.original.pitch_classes, (0, 4, 7))
        self.assertEqual(context.proposed.pitch_classes, (0, 4, 11))
        self.assertEqual(context.pitch_classes_added, (11,))
        self.assertEqual(context.pitch_classes_removed, (7,))
        self.assertTrue(context.original.matching_templates)
        self.assertFalse(context.proposed.matching_templates)
        self.assertFalse(context.changes_lowest_sounding_pitch)
        self.assertEqual(context.original.active_source_note_ids,
                         context.proposed.active_source_note_ids)
        self.assertEqual(context.status,
                         "counterfactual_vertical_effect_not_quality_judgment")

    def test_transposed_instrument_uses_concert_pitch_for_sonority(self):
        score = score_texture_from_mxl(_score([
            ("P1", "Clarinet", "<transpose><chromatic>-2</chromatic></transpose>",
             [_note("D", 5)]),
            ("P2", "Violin", "", [_note("E", 4)]),
            ("P3", "Violoncello", "", [_note("G", 4)]),
        ]))
        context = ScoreSonorityIndex(score).at(ScoreMoment(0, Fraction(0)))
        self.assertEqual(context.pitch_classes, (0, 4, 7))
        self.assertEqual(context.bass_sounding_pitch, 64)
        self.assertEqual(context.matching_templates[0].bass_chord_member_index, 1)

    def test_symmetrical_augmented_triad_keeps_multiple_roots(self):
        evidence = score_texture_from_mxl(_score([
            ("P1", "Violin", "", [_note("C", 4)]),
            ("P2", "Viola", "", [_note("E", 4)]),
            ("P3", "Violoncello", "", [_note("G", 4, alter=1)]),
        ]))
        sonority = ScoreSonorityIndex(evidence).at(ScoreMoment(0, Fraction(0)))
        roots = {(t.shape, t.root_pitch_class) for t in sonority.matching_templates}
        self.assertEqual(roots, {("augmented_triad", 0),
                                 ("augmented_triad", 4),
                                 ("augmented_triad", 8)})

    def test_sparse_pitch_set_is_unknown_not_forced_chord(self):
        evidence = score_texture_from_mxl(_score([
            ("P1", "Flute", "", [_note("C", 4)]),
        ]))
        index = ScoreSonorityIndex(evidence)
        self.assertFalse(index.at(ScoreMoment(0, Fraction(0))).matching_templates)
        self.assertEqual(index.at(ScoreMoment(0, Fraction(10))).pitch_classes, ())
        with self.assertRaisesRegex(ValueError, "sonority_moment_outside_score"):
            index.at(ScoreMoment(2, Fraction(0)))

    def test_rejects_edited_note_of_another_source(self):
        first = _fixture()
        observed = next(o for o in score_voice_leading(first)
                        if o.part_a == "P1" and o.part_b == "P2")
        edit = propose_voice_motion_edit(observed, "parallel")
        other = score_texture_from_mxl(_score([
            ("P1", "Violin", "", [_note("C", 4)]),
        ]))
        with self.assertRaisesRegex(ValueError, "source_or_correspondence_mismatch"):
            ScoreSonorityIndex(other).context_for_edit(observed, edit)

    def test_real_orchestral_score_reconstructs_source_tied_sonorities(self):
        root = Path(__file__).resolve().parents[1] / "data/orchestral"
        for filename in ("hauptstimme-beethoven5-movement1.mxl",
                         "hauptstimme-beethoven7-movement2.mxl"):
            with self.subTest(filename=filename):
                evidence = score_texture_from_mxl((root / filename).read_bytes())
                index = ScoreSonorityIndex(evidence)
                motions = score_voice_leading(evidence)
                checked = 0
                for motion in motions:
                    if motion.motion_type != "contrary":
                        continue
                    try:
                        proposed = propose_voice_motion_edit(motion, "parallel")
                    except ValueError:
                        continue
                    context = index.context_for_edit(motion, proposed)
                    self.assertEqual(context.target_note_id, motion.source_note_ids[3])
                    self.assertTrue(context.original.active_source_note_ids)
                    self.assertEqual(context.original.moment, motion.to_moment)
                    checked += 1
                    if checked >= 10:
                        break
                self.assertEqual(checked, 10)

    def test_probe_reports_source_tied_counts_without_quality_claim(self):
        report = inspect(list(DEFAULT_SCORES), top=0)
        self.assertEqual(report["claim"],
                         "vertical_pitch_material_effect_not_harmonic_function_or_quality")
        self.assertEqual(len(report["pieces"]), 2)
        self.assertEqual([row["hypothetical_parallel_edits_examined"]
                          for row in report["pieces"]], [1932, 977])
        self.assertEqual([row["exact_template_no_longer_matches"]
                          for row in report["pieces"]], [353, 269])
        self.assertTrue(all(not row["examples"] for row in report["pieces"]))

    def test_probe_rejects_invalid_preview_limit(self):
        with self.assertRaisesRegex(ValueError, "invalid_harmonic_preview_limit"):
            inspect([], top=-1)


if __name__ == "__main__":
    unittest.main()
