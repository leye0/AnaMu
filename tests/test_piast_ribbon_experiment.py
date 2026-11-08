"""Small offline tests: no MIDI download or interpretation of human labels."""

import unittest
from unittest.mock import patch

import numpy as np

from anamu.piast_at import PIASTClip
from anamu.tonal_motion import TONAL_DISTRIBUTION_FEATURE_NAMES
from scripts.piast_ribbon_experiment import (
    ARMS, FIELDS, RIBBON_FEATURES, build_arms, ribbon_features_from_samples,
)
from scripts.piast_tonal_cv import evaluate_arms, group_bootstrap
from scripts.piast_tension_experiment import NONCALM_MOODS


class RibbonAblationTests(unittest.TestCase):
    def test_published_tension_axes_are_summarized_independently(self):
        samples = [{"cloud_diameter": 1.0, "cloud_momentum": 10.0, "tensile_strain": 2.0},
                   {"cloud_diameter": 3.0, "cloud_momentum": 20.0, "tensile_strain": 4.0}]
        result = ribbon_features_from_samples(samples)
        self.assertEqual(set(result), set(RIBBON_FEATURES))
        self.assertAlmostEqual(result["ribbon_cloud_diameter_mean"], 2.0)
        self.assertAlmostEqual(result["ribbon_cloud_diameter_std"], 1.0)
        self.assertAlmostEqual(result["ribbon_cloud_diameter_p90"], 2.8)
        self.assertAlmostEqual(result["ribbon_cloud_momentum_mean"], 15.0)
        self.assertEqual(len(FIELDS), 3)
        with self.assertRaisesRegex(ValueError, "empty_ribbon_samples"):
            ribbon_features_from_samples([])
        with self.assertRaisesRegex(ValueError, "nonfinite_ribbon"):
            ribbon_features_from_samples([{**samples[0], "cloud_diameter": float("nan")}])

    @staticmethod
    def _cohort():
        records = []
        ribbons = []
        for i in range(60):
            tags = frozenset(NONCALM_MOODS) if i % 3 == 0 else frozenset()
            clip = PIASTClip(f"r{i}", f"r{i}.mid", f"video{i//2}", tags,
                             frozenset(), frozenset())
            features = {"base": float(i % 7)}
            features.update({key: float(i % 5) for key in TONAL_DISTRIBUTION_FEATURE_NAMES})
            records.append((clip, features))
            ribbons.append(None if i == 3 else {key: float(i + j) for j, key in
                                                  enumerate(RIBBON_FEATURES)})
        return records, ribbons

    def test_arms_share_exact_clips_and_keep_missing_ribbon_rows(self):
        records, ribbons = self._cohort()
        arms = build_arms(records, ribbons)
        self.assertEqual(tuple(arms), ARMS)
        for candidate in ARMS:
            self.assertEqual([c.clip_id for c, _ in arms[candidate]],
                             [c.clip_id for c, _ in records])
        self.assertEqual(set(arms["baseline"][0][1]), {"base"})
        self.assertEqual(len(arms["cloud_diameter"][0][1]),
                         len(arms["distribution"][0][1]) + 3)
        self.assertEqual(len(arms["full_ribbons"][0][1]),
                         len(arms["distribution"][0][1]) + 9)
        self.assertFalse(any(k in arms["full_ribbons"][3][1] for k in RIBBON_FEATURES))
        self.assertNotEqual(arms["full_ribbons"][0][1], arms["sham_ribbons"][0][1])

    def test_custom_arm_evaluation_preserves_video_split_and_bootstrap_comparator(self):
        records, ribbons = self._cohort()
        arms = build_arms(records, ribbons)
        with patch("scripts.piast_tonal_cv._predict", side_effect=lambda x, xt, y:
                   np.full(len(xt), float(np.mean(y)))):
            evaluated, oof = evaluate_arms(arms, arms=ARMS,
                                           negative_control_arm="full_ribbons")
        self.assertEqual(set(evaluated["scores"]), set(ARMS))
        self.assertEqual(len(oof["groups"]), 60)
        self.assertEqual(len(evaluated["diagnostics"]["folds"]), 5)
        contrasts = group_bootstrap(oof, repetitions=20, baseline_arm="distribution", arms=ARMS)
        self.assertNotIn("distribution", contrasts)
        for name, values in contrasts.items():
            self.assertAlmostEqual(values["hard5_macro"]["ci_95_low"], 0.0, msg=name)
            self.assertAlmostEqual(values["hard5_macro"]["ci_95_high"], 0.0, msg=name)


if __name__ == "__main__":
    unittest.main()
