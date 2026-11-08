"""Grouped emotion regression learns local transitions separately from mood."""

import unittest
import numpy as np

from anamu.emotion_models import GroupedTemporalRegressor, causal_valence_inertia


class GroupedTemporalTests(unittest.TestCase):
    def test_valence_inertia_is_causal_and_keeps_arousal(self):
        original = np.asarray([[.2, -.3], [.9, .4], [-.6, .7]])
        smoothed = causal_valence_inertia(original, alpha=.2)
        np.testing.assert_allclose(smoothed[:, 0], [.2, .34, .152])
        np.testing.assert_array_equal(smoothed[:, 1], original[:, 1])
        np.testing.assert_array_equal(original[:, 0], [.2, .9, -.6])
        with self.assertRaises(ValueError):
            causal_valence_inertia(original, alpha=0.)

    def test_different_piece_means_and_opposite_intrapiece_changes(self):
        # 4 compositions, each with a different global climate and a local
        # four-measure rise/fall. We never mark the piece identity as a feature.
        rows = []
        truth = []
        for climate in (-.6, -.2, .2, .6):
            for step in (-1, -.5, .5, 1):
                rows.append([climate, step, np.nan])
                truth.append([climate + .1 * step, climate * .5 - .3 * step])
        model = GroupedTemporalRegressor(global_alpha=.01, local_alpha=.01)
        model.fit(rows, truth, [4] * 4)
        predictions = model.predict(rows, [4] * 4)
        self.assertEqual(predictions.shape, (16, 2))
        self.assertLess(np.mean(np.abs(predictions - truth)), .02)
        self.assertLess(predictions[0, 0], predictions[3, 0])
        self.assertLess(predictions[12, 0], predictions[15, 0])

    def test_mismatched_length_and_untrained_predict_refused(self):
        with self.assertRaises(RuntimeError):
            GroupedTemporalRegressor().predict([[0, 1]], [1])
        with self.assertRaises(ValueError):
            GroupedTemporalRegressor().fit([[0, 1]], [[0, 0]], [2])


if __name__ == "__main__":
    unittest.main()
