"""Counterfactual target notes must be generated without target continuation."""

from __future__ import annotations

import unittest

from anamu.orchestral_counterfactual import doubling_reconstruction_trials
from anamu.score_texture import score_texture_from_mxl
from tests.test_score_texture import _note, _score


class DoublingReconstructionTests(unittest.TestCase):
    def test_prefix_learns_rule_and_reconstructs_hidden_sounding_pitches(self):
        notes_a = (_note("C", 4) + _note("D", 4) + _note("E", 4)
                   + _note("F", 4) + _note("G", 4) + _note("A", 4))
        notes_b = (_note("C", 5) + _note("D", 5) + _note("E", 5)
                   + _note("F", 5) + _note("G", 5) + _note("A", 5))
        score = score_texture_from_mxl(_score([
            ("P1", "Violin", "", [notes_a]),
            ("P2", "Flute", "", [notes_b]),
        ]))
        trials = doubling_reconstruction_trials(score)
        self.assertEqual(len(trials), 2)  # A→B and B→A both legitimate.
        forward = next(t for t in trials if t.source_part == "P1")
        self.assertEqual(forward.octave_offset, 1)
        self.assertEqual([n.predicted_sounding_pitch for n in forward.generated],
                         [77, 79, 81])
        self.assertEqual(forward.exact_matches, (True, True, True))
        self.assertEqual(forward.constant_pitch_baseline_matches,
                         (False, False, False))
        self.assertEqual(forward.unison_copy_baseline_matches,
                         (False, False, False))
        self.assertTrue(all(t.score_sha256 == score.source_sha256 for t in trials))

    def test_altered_target_future_fails_without_changing_predicted_notes(self):
        source = (_note("C", 4) + _note("D", 4) + _note("E", 4)
                  + _note("F", 4) + _note("G", 4) + _note("A", 4))
        prefix = _note("C", 5) + _note("D", 5) + _note("E", 5)
        exact = _score([
            ("P1", "Violin", "", [source]),
            ("P2", "Flute", "", [prefix + _note("F", 5)
                                    + _note("G", 5) + _note("A", 5)]),
        ])
        altered = _score([
            ("P1", "Violin", "", [source]),
            ("P2", "Flute", "", [prefix + _note("G", 5)
                                    + _note("A", 5) + _note("B", 5)]),
        ])
        original_trial = next(t for t in doubling_reconstruction_trials(
            score_texture_from_mxl(exact)) if t.source_part == "P1")
        altered_trial = next(t for t in doubling_reconstruction_trials(
            score_texture_from_mxl(altered)) if t.source_part == "P1")
        self.assertEqual(original_trial.generated, altered_trial.generated)
        self.assertEqual(altered_trial.exact_matches, (False, False, False))

    def test_unproven_rule_creates_no_completion(self):
        source = _note("C", 4) + _note("D", 4) + _note("E", 4) + _note("F", 4)
        target = _note("C", 5) + _note("F", 5) + _note("G", 5) + _note("A", 5)
        score = score_texture_from_mxl(_score([
            ("P1", "Violin", "", [source]),
            ("P2", "Flute", "", [target]),
        ]))
        self.assertFalse(doubling_reconstruction_trials(
            score, training_notes=2, prediction_notes=2))

    def test_refuses_invalid_experiment_budget(self):
        score = score_texture_from_mxl(_score([("P1", "Violin", "", [_note("C", 4)])]))
        with self.assertRaisesRegex(ValueError, "counterfactual_trial_budget_invalid"):
            doubling_reconstruction_trials(score, training_notes=1)


if __name__ == "__main__":
    unittest.main()
