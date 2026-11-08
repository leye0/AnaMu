"""Small contract checks; the real 1900-clip run is the primary validation."""
import unittest
import numpy as np
from threadpoolctl import threadpool_limits
from scripts.piast_model_capacity import predict_tree_votes


class CapacityTests(unittest.TestCase):
    def test_constant_votes_and_missing_features(self):
        x = np.full((80, 2), np.nan)
        with threadpool_limits(limits=1):
            for fraction in (0, 1 / 3, 1):
                p = predict_tree_votes(x, x[:3], np.full(80, fraction), depth=3)
                np.testing.assert_allclose(p, fraction)

    def test_invalid_votes_rejected(self):
        for votes in ([np.nan, 0], [-1, 0], [0, 2], [0]):
            with self.assertRaises(ValueError):
                predict_tree_votes(np.zeros((2, 1)), np.zeros((1, 1)), votes, depth=1)


if __name__ == "__main__":
    unittest.main()
