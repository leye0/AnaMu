"""Exact probability semantics and train-only prior correction tests."""

import unittest

import numpy as np

from scripts.piast_vote_calibration import (
    fractional_brier, fractional_logloss, prior_odds_correction,
)
from scripts.piast_votes_experiment import predict_soft_votes


class VoteCalibrationTests(unittest.TestCase):
    def test_expected_brier_score_is_exact_for_fractional_labels(self):
        q = np.array([0., 1 / 3, 2 / 3, 1.])
        p = np.array([.2, .2, .6, .8])
        expected = float(np.mean(q * (1 - p) ** 2 + (1 - q) * p ** 2))
        self.assertAlmostEqual(fractional_brier(q, p), expected)
        self.assertAlmostEqual(fractional_logloss(q, q.clip(1e-8, 1 - 1e-8)),
                               -np.mean(q * np.log(q.clip(1e-8, 1 - 1e-8)) +
                                        (1 - q) * np.log1p(-q.clip(1e-8, 1 - 1e-8))))

    def test_priors_undo_abstract_balanced_constant_odds(self):
        for pi in (.07, .2, .5, .8):
            self.assertAlmostEqual(prior_odds_correction(np.array([.5]), pi)[0], pi)
        self.assertTrue(np.all(np.diff(prior_odds_correction(
            np.array([.1, .4, .8]), .15)) > 0))
        with self.assertRaisesRegex(ValueError, "invalid_positive_prior"):
            prior_odds_correction(np.array([.5]), 0.)

    def test_unweighted_model_can_learn_actual_base_rate(self):
        rng = np.random.default_rng(16)
        train = rng.normal(size=(100, 4))
        zero = np.zeros((10, 4))
        votes = np.zeros(100, dtype=float)
        votes[:20] = 1 / 3
        votes[20:30] = 1
        balanced = predict_soft_votes(train, zero, votes)
        unweighted = predict_soft_votes(train, zero, votes, class_balanced=False)
        self.assertTrue(np.isfinite(balanced).all())
        self.assertTrue(np.isfinite(unweighted).all())
        self.assertLess(float(np.mean(unweighted)), float(np.mean(balanced)))


if __name__ == "__main__":
    unittest.main()
