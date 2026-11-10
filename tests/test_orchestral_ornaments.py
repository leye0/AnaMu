"""Diatonic passing/neighbor gestures are evidence, not harmonic verdicts."""

from __future__ import annotations

import unittest
from fractions import Fraction
from pathlib import Path

from anamu.orchestral_ornaments import score_ornamental_figures
from anamu.score_texture import score_texture_from_mxl
from scripts.orchestral_ornament_probe import DEFAULT_SCORES, inspect
from tests.test_score_texture import _note, _score


def _with_triad(line: str):
    return score_texture_from_mxl(_score([
        ("P1", "Violin", "", [line]),
        ("P2", "Violoncello", "", [_note("C", 3, duration=12)]),
        ("P3", "Viola", "", [_note("E", 3, duration=12)]),
        ("P4", "Horn", "", [_note("G", 3, duration=12)]),
    ]))


class OrchestralOrnamentTests(unittest.TestCase):
    def test_stepwise_passing_gesture_has_stable_notated_backing(self):
        evidence = _with_triad(_note("C", 4) + _note("D", 4)
                               + _note("E", 4))
        figures = score_ornamental_figures(evidence)
        self.assertEqual(len(figures), 1)
        gesture = figures[0]
        self.assertEqual(gesture.kind, "diatonic_passing_figure")
        self.assertEqual(gesture.sounding_pitches, (60, 62, 64))
        self.assertEqual(gesture.other_parts_pitch_classes,
                         ((0, 4, 7), (0, 4, 7), (0, 4, 7)))
        self.assertTrue(gesture.stable_accompaniment_support_candidate)
        self.assertEqual(gesture.source_sha256, evidence.source_sha256)
        self.assertEqual(gesture.moments[1].onset_quarters, Fraction(1))
        self.assertEqual(gesture.status,
                         "three_note_linear_figure_not_nonchord_tone_annotation")

    def test_neighbor_returns_to_exact_written_pitch(self):
        evidence = _with_triad(_note("C", 4) + _note("D", 4)
                               + _note("C", 4))
        gestures = score_ornamental_figures(evidence)
        self.assertEqual([g.kind for g in gestures], ["diatonic_neighbor_figure"])
        self.assertTrue(gestures[0].stable_accompaniment_support_candidate)

    def test_written_enharmonic_information_is_not_discarded(self):
        evidence = _with_triad(_note("D", 4, alter=-1)
                               + _note("E", 4, alter=-1)
                               + _note("F", 4))
        notes = [n for n in evidence.notes if n.part_id == "P1"]
        self.assertEqual([(n.written_step, n.written_alter, n.written_octave)
                          for n in notes], [("D", -1, 4), ("E", -1, 4),
                                           ("F", 0, 4)])
        # D-flat -> E-flat -> F: two written seconds, each by a whole tone.
        self.assertEqual(score_ornamental_figures(evidence)[0].kind,
                         "diatonic_passing_figure")

    def test_chromatic_fragment_is_not_mislabeled_diatonic(self):
        evidence = _with_triad(_note("C", 4)
                               + _note("C", 4, alter=1) + _note("D", 4))
        self.assertEqual(score_ornamental_figures(evidence), ())

    def test_discontinuous_or_tied_and_chorded_gestures_are_rejected(self):
        cases = (
            _note("C", 4) + '<note><rest/><duration>4</duration></note>'
            + _note("D", 4) + _note("E", 4),
            _note("C", 4) + _note("D", 4, extra='<tie type="stop"/>')
            + _note("E", 4),
            _note("C", 4) + _note("D", 4)
            + _note("G", 4, extra="<chord/>") + _note("E", 4),
        )
        for line in cases:
            with self.subTest(line=line):
                self.assertFalse(score_ornamental_figures(_with_triad(line)))

    def test_melodic_figure_does_not_assert_harmonic_support(self):
        # A parallel moving accompaniment never proves fixed chord tones.
        evidence = score_texture_from_mxl(_score([
            ("P1", "Violin", "", [_note("C", 4) + _note("D", 4)
                                       + _note("E", 4)]),
            ("P2", "Cello", "", [_note("G", 3) + _note("A", 3)
                                      + _note("B", 3)]),
        ]))
        first = next(f for f in score_ornamental_figures(evidence)
                     if f.part_id == "P1")
        self.assertFalse(first.accompaniment_unchanged)
        self.assertFalse(first.stable_accompaniment_support_candidate)

    def test_transposing_part_keeps_written_steps_and_sounding_context(self):
        score = score_texture_from_mxl(_score([
            ("P1", "Clarinet", "<transpose><chromatic>-2</chromatic></transpose>",
             [_note("D", 4) + _note("E", 4) + _note("F", 4, alter=1)]),
            ("P2", "Bassoon", "", [_note("C", 3, duration=12)]),
            ("P3", "Viola", "", [_note("E", 3, duration=12)]),
        ]))
        f = next(g for g in score_ornamental_figures(score) if g.part_id == "P1")
        self.assertEqual(f.sounding_pitches, (60, 62, 64))
        self.assertEqual(f.written_pitches,
                         (("D", 0, 4), ("E", 0, 4), ("F", 1, 4)))

    def test_budget_and_real_scores_have_observable_figures(self):
        with self.assertRaisesRegex(ValueError, "ornamental_figure_budget_invalid"):
            score_ornamental_figures(_with_triad(_note("C", 4)), max_figures=0)
        with self.assertRaisesRegex(ValueError, "ornamental_figure_budget_exceeded"):
            score_ornamental_figures(_with_triad(_note("C", 4) + _note("D", 4)
                                                + _note("E", 4)
                                                + _note("F", 4)), max_figures=1)
        root = Path(__file__).resolve().parents[1] / "data/orchestral"
        for filename in ("hauptstimme-beethoven5-movement1.mxl",
                         "hauptstimme-beethoven7-movement2.mxl"):
            with self.subTest(filename=filename):
                evidence = score_texture_from_mxl((root / filename).read_bytes())
                gestures = score_ornamental_figures(evidence)
                self.assertGreater(len(gestures), 10)
                self.assertTrue(all(g.source_sha256 == evidence.source_sha256
                                    for g in gestures))

    def test_reproducible_probe_has_explicit_support_not_harmony_claim(self):
        report = inspect(list(DEFAULT_SCORES), top=0)
        self.assertEqual(report["claim"],
                         "melodic_ornamental_figures_not_nonchord_tone_labels")
        self.assertEqual([p["total_strict_three_note_figures"]
                          for p in report["pieces"]], [118, 753])
        self.assertEqual([p["figures_with_strict_backing_support"]
                          for p in report["pieces"]], [0, 9])
        self.assertTrue(all(not p["examples"] for p in report["pieces"]))

    def test_probe_rejects_invalid_limit(self):
        with self.assertRaisesRegex(ValueError, "invalid_ornament_preview_limit"):
            inspect([], top=-1)


if __name__ == "__main__":
    unittest.main()
