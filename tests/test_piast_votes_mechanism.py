"""Training-only, within-class randomization cannot change majority tags."""

import unittest

import numpy as np

from scripts.piast_votes_mechanism import training_vote_variant


class VoteMechanismTests(unittest.TestCase):
    def test_each_cue_is_distinct_and_keeps_votes_valid(self):
        q = np.array([0., 1 / 3, 2 / 3, 1.] * 25)
        self.assertTrue(np.array_equal(
            training_vote_variant(q, "minority_only")[:4], [0, 1 / 3, 1, 1]))
        self.assertTrue(np.array_equal(
            training_vote_variant(q, "majority_only")[:4], [0, 0, 2 / 3, 1]))
        self.assertTrue(np.array_equal(training_vote_variant(q, "full_votes"), q))

    def test_sham_preserves_vote_counts_and_majority_per_item(self):
        q = np.array([0.] * 70 + [1 / 3] * 70 + [2 / 3] * 70 + [1.] * 70)
        original = q.copy()
        sham = training_vote_variant(q, "within_class_sham", seed=19)
        self.assertTrue(np.array_equal(q, original))
        self.assertTrue(np.array_equal(np.sort(sham), np.sort(q)))
        self.assertTrue(np.array_equal(sham >= 2 / 3, q >= 2 / 3))
        self.assertFalse(np.array_equal(sham, q))
        self.assertTrue(np.array_equal(sham, training_vote_variant(q, "within_class_sham", seed=19)))

    def test_reject_fake_vote_levels_and_unknown_mode(self):
        with self.assertRaisesRegex(ValueError, "invalid_original_vote_levels"):
            training_vote_variant(np.asarray([0.2]), "full_votes")
        with self.assertRaisesRegex(ValueError, "unknown_vote_variant"):
            training_vote_variant(np.asarray([1 / 3]), "something_else")


if __name__ == "__main__":
    unittest.main()
