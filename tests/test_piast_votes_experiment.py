"""Ensure vote learning is comparable with historic binary label training."""

import unittest

import numpy as np

from anamu.piast_at import PIASTClip
from scripts.piast_tonal_cv import _predict
from scripts.piast_votes_experiment import (
    expert_vote_fraction, predict_soft_votes, vote_agreement_diagnostics,
)


class PIASVotesTests(unittest.TestCase):
    def test_exact_fraction_and_original_majority(self):
        tags = [frozenset(), frozenset({"Epic"}), frozenset(), frozenset({"Epic"})]
        clips = [PIASTClip("x1", "x1.mid", "v1", frozenset(), frozenset(), tags[1]),
                 PIASTClip("x2", "x2.mid", "v2", frozenset(), frozenset({"Epic"}), frozenset()),
                 PIASTClip("x3", "x3.mid", "v3", frozenset({"Epic"}), frozenset(), frozenset()),
                 PIASTClip("x4", "x4.mid", "v4", frozenset(), frozenset(), frozenset())]
        self.assertEqual([expert_vote_fraction(c, "Epic") for c in clips],
                         [1 / 3, 2 / 3, 1.0, 0.0])
        self.assertEqual([int("Epic" in c.mood_tags()) for c in clips], [0, 1, 1, 0])
        audit = vote_agreement_diagnostics(clips)["Epic"]
        self.assertEqual([audit["zero_votes"], audit["one_vote"],
                          audit["two_votes"], audit["three_votes"]], [1, 1, 1, 1])

    def test_hard_votes_reproduce_historic_weighted_logistic_predictions(self):
        rng = np.random.default_rng(121)
        train_x = rng.normal(size=(90, 9))
        test_x = rng.normal(size=(30, 9))
        train_x[3:7, 2] = np.nan
        train_x[7:13, 4] = np.nan
        test_x[2, 4] = np.nan
        hard = (rng.random(90) < .25).astype(int)
        binary = _predict(train_x, test_x, hard)
        soft = predict_soft_votes(train_x, test_x, hard.astype(float))
        np.testing.assert_allclose(binary, soft, rtol=1e-6, atol=1e-6)

    def test_fractional_votes_change_training_but_never_clip_labels(self):
        rng = np.random.default_rng(13)
        x = rng.normal(size=(70, 4))
        majority = (rng.random(70) < .2).astype(int)
        q = majority.astype(float)
        q[:20] = 1 / 3
        predicted = predict_soft_votes(x, x[:3], q)
        self.assertEqual(predicted.shape, (3,))
        self.assertTrue(np.isfinite(predicted).all())
        self.assertTrue(((predicted > 0) & (predicted < 1)).all())
        unweighted = predict_soft_votes(x, x[:3], q, class_balanced=False)
        self.assertTrue(np.isfinite(unweighted).all())
        self.assertFalse(np.allclose(predicted, unweighted))
        with self.assertRaisesRegex(ValueError, "invalid_vote_fraction"):
            predict_soft_votes(x, x[:3], np.full(70, 1.1))


if __name__ == "__main__":
    unittest.main()
