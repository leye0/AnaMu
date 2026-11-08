"""Synthetic split, ablation and confidence checks without any PIAST download."""

import unittest
from unittest.mock import patch

import numpy as np

from anamu.piast_at import PIASTClip
from anamu.tonal_motion import (
    TONAL_DISTRIBUTION_FEATURE_NAMES, TONAL_MOTION_FEATURE_NAMES,
    TONAL_SEQUENCE_FEATURE_NAMES, tonal_motion_features,
)
from scripts.piast_tonal_cv import ARMS, evaluate_arms, group_bootstrap, source_group_folds
from scripts.piast_tension_experiment import NONCALM_MOODS


class TonalCVTests(unittest.TestCase):
    def test_feature_partition_exhaustive(self):
        self.assertEqual(set(TONAL_DISTRIBUTION_FEATURE_NAMES) |
                         set(TONAL_SEQUENCE_FEATURE_NAMES), set(TONAL_MOTION_FEATURE_NAMES))
        self.assertFalse(set(TONAL_DISTRIBUTION_FEATURE_NAMES) &
                         set(TONAL_SEQUENCE_FEATURE_NAMES))

    def test_every_distribution_metric_invariant_to_shuffle(self):
        notes = []
        for w in range(8):
            for i in range(13):
                pitch = (60, 62, 63, 65, 67, 68, 70, 72, 64, 71)[(w * 3 + i) % 10]
                start = w * 6000 + i * 240
                notes.append((start, start + 280, pitch, 63))
        n = np.asarray(notes, dtype=float)
        real = tonal_motion_features(n)
        control = tonal_motion_features(n, shuffle=True, seed=11)
        for metric in TONAL_DISTRIBUTION_FEATURE_NAMES:
            self.assertAlmostEqual(real[metric], control[metric], places=11, msg=metric)
        self.assertTrue(any(abs(real[metric] - control[metric]) > .001
                            for metric in TONAL_SEQUENCE_FEATURE_NAMES))

    @staticmethod
    def _records():
        clips = []
        for i in range(60):
            tags = frozenset(NONCALM_MOODS) if i % 3 == 0 else frozenset()
            clip = PIASTClip(f"clip{i}", f"clip{i}.mid", f"video{i//2}", tags,
                             frozenset(), frozenset())
            clips.append((clip, {"common": float(i % 7)}))
        return clips

    def test_group_folds_never_mix_original_videos(self):
        records = self._records()
        assignments = []
        for train, test in source_group_folds(records):
            train_groups = {records[i][0].song_group for i in train}
            test_groups = {records[i][0].song_group for i in test}
            self.assertFalse(train_groups & test_groups)
            assignments.extend(test.tolist())
        self.assertEqual(sorted(assignments), list(range(len(records))))

    def test_identical_arms_produce_identical_oof_and_group_bootstrap(self):
        reference = self._records()
        arms = {name: [(c, dict(row)) for c, row in reference] for name in ARMS}
        with patch("scripts.piast_tonal_cv._predict", side_effect=lambda x, xt, y:
                   np.full(len(xt), float(np.mean(y)))):
            evaluation, oof = evaluate_arms(arms)
        for name in ARMS:
            self.assertAlmostEqual(evaluation["scores"]["baseline"]["hard5_macro_ap"],
                                   evaluation["scores"][name]["hard5_macro_ap"])
        intervals = group_bootstrap(oof, repetitions=15)
        for name in ARMS[1:]:
            self.assertAlmostEqual(intervals[name]["Dark"]["ci_95_low"], 0)
            self.assertAlmostEqual(intervals[name]["Dark"]["ci_95_high"], 0)

    def test_reject_different_examples_across_arms(self):
        reference = self._records()
        arms = {name: list(reference) for name in ARMS}
        arms["temporal"] = arms["temporal"][:-1]
        with self.assertRaisesRegex(AssertionError, "unequal_examples"):
            evaluate_arms(arms)


if __name__ == "__main__":
    unittest.main()
