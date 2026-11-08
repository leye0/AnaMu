"""No real listener tags or downloads: pure transfer protocol invariants."""

import unittest

from anamu.tonal_motion import (
    TONAL_DISTRIBUTION_FEATURE_NAMES, TONAL_MOTION_FEATURE_NAMES,
)
from scripts.piast_to_isovat_tension_transfer import (
    ARMS, _family, permutation_null,
)
from scripts.isovat_tension_benchmark import HUMAN_TENSION_ORDER, score_order


class IsoVATTransferTests(unittest.TestCase):
    def test_static_only_and_order_features_not_mixed(self):
        record = {"baseline": 4.5,
                  **{name: i / 100 for i, name in enumerate(TONAL_MOTION_FEATURE_NAMES)}}
        self.assertEqual(_family(record, "baseline"), {"baseline": 4.5})
        self.assertEqual(set(_family(record, "distribution")),
                         {"baseline", *TONAL_DISTRIBUTION_FEATURE_NAMES})
        self.assertEqual(set(_family(record, "temporal")),
                         {"baseline", *TONAL_MOTION_FEATURE_NAMES})

    def test_human_order_differs_from_composed_order(self):
        self.assertEqual(len(HUMAN_TENSION_ORDER), 10)
        self.assertEqual(HUMAN_TENSION_ORDER[6], "LMH")
        ranking = score_order({"H": .1, "M": .5, "L": .9}, HUMAN_TENSION_ORDER[6])
        self.assertTrue(ranking["exact_order"])

    def test_familywise_null_deterministic_and_no_fitted_iso_parameters(self):
        mock = {}
        for arm in ARMS:
            mock[arm] = {"by_set": {str(index): {
                "scores": {"H": .9, "M": .5, "L": .1}}
                for index in HUMAN_TENSION_ORDER},
                "correct_pairs": 0, "exact_orders": 0}
            for i, order in HUMAN_TENSION_ORDER.items():
                row = score_order(mock[arm]["by_set"][str(i)]["scores"], order)
                mock[arm]["correct_pairs"] += row["pairwise_correct"]
                mock[arm]["exact_orders"] += int(row["exact_order"])
        first = permutation_null(mock, repetitions=40)
        self.assertEqual(first, permutation_null(mock, repetitions=40))
        self.assertEqual(first["iterations"], 40)
        self.assertGreaterEqual(first["familywise_p_pairs"], 1 / 41)


if __name__ == "__main__":
    unittest.main()
