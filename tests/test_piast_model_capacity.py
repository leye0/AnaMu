"""Small contract checks; the real 1900-clip run is the primary validation."""
import unittest
import gzip
import json
from pathlib import Path
from types import SimpleNamespace
import numpy as np
from threadpoolctl import threadpool_limits
from scripts.piast_model_capacity import FOLD_MANIFEST, predict_tree_votes, replay_folds


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

    def test_replays_exact_completed_experiment_even_if_records_reordered(self):
        path = Path(__file__).resolve().parents[1] / 'reports/piast-model-capacity-oof-2026-11-08.json.gz'
        with gzip.open(path, 'rt') as handle:
            oof = json.load(handle)
        records = [(SimpleNamespace(clip_id=c, song_group=g), {})
                   for c, g in zip(oof['clip_ids'], oof['groups'])]
        expected = dict(zip(oof['clip_ids'], oof['folds']))
        records.reverse()
        seen = []
        for fold, (train, test) in enumerate(replay_folds(records, json.loads(FOLD_MANIFEST.read_text())), 1):
            self.assertFalse({records[i][0].song_group for i in train} &
                             {records[i][0].song_group for i in test})
            self.assertTrue(all(expected[records[i][0].clip_id] == fold for i in test))
            seen.extend(test.tolist())
        self.assertEqual(sorted(seen), list(range(1900)))

    def test_rejects_group_leakage_and_incomplete_cohort(self):
        records = [(SimpleNamespace(clip_id=str(i), song_group=str(i)), {}) for i in range(5)]
        manifest = {'folds': {str(i): {'group': str(i), 'fold': i+1} for i in range(5)}}
        with self.assertRaisesRegex(ValueError, 'cohort_mismatch'):
            list(replay_folds(records[:-1], manifest))
        records[1][0].song_group = '0'
        manifest['folds']['1']['group'] = '0'
        with self.assertRaisesRegex(ValueError, 'source_video_leakage'):
            list(replay_folds(records, manifest))


if __name__ == "__main__":
    unittest.main()
