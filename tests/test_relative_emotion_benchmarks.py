"""Small synthetic regression guards: no third-party dataset files required."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import mido
import numpy as np

from scripts.cp_wtc_relative_benchmark import (
    FEATURES, evaluate_pairs, midi_expression, predict_out_of_fold,
)
from scripts.isovat_tension_benchmark import HUMAN_TENSION_ORDER, score_order
from scripts.percepiano_hard_benchmark import (
    HARD_DIFFERENCE, evaluate, parent_work, scored_excerpt,
)
from scripts.percepiano_pulse_hypothesis import (
    center_within_score, shuffled_within_score, work_regression,
)
from anamu.expressive_pulse import PULSE_FEATURE_NAMES, expressive_pulse_features
from anamu.expressive_accent import ACCENT_FEATURE_NAMES, expressive_accent_features


class SymbolicEmotionBenchmarkTests(unittest.TestCase):
    def test_isovat_uses_distinct_human_listener_order_and_credits_pairs(self):
        self.assertEqual(len(HUMAN_TENSION_ORDER), 10)
        self.assertEqual(HUMAN_TENSION_ORDER[6], "LMH")
        score = score_order({"H": 0.7, "M": 0.1, "L": 0.4}, "HLM")
        self.assertEqual(score["pairwise_correct"], 3)
        self.assertTrue(score["exact_order"])
        tied = score_order({"H": 1., "M": 1., "L": 0.}, "HML")
        self.assertFalse(tied["exact_order"])

    def test_midi_expression_uses_note_timing_without_audio(self):
        with TemporaryDirectory() as tmp:
            filename = Path(tmp) / "performed.mid"
            midi = mido.MidiFile(ticks_per_beat=480)
            track = mido.MidiTrack()
            midi.tracks.append(track)
            track.append(mido.MetaMessage("set_tempo", tempo=500_000, time=0))
            for index in range(16):
                track.append(mido.Message("note_on", note=60 + index % 7,
                                          velocity=50 + index * 3, time=240))
                track.append(mido.Message("note_off", note=60 + index % 7,
                                          velocity=0, time=240))
            midi.save(filename)
            features = midi_expression(filename)
            self.assertEqual(set(FEATURES), set(features))
            self.assertGreater(features["onset_density"], 0)
            self.assertGreater(features["velocity_sd"], 0)
            self.assertTrue(all(np.isfinite(v) for v in features.values()))

    def test_group_cv_keeps_held_out_piece_unseen(self):
        rng = np.random.default_rng(44)
        groups = np.repeat(np.arange(12), 6)
        x = rng.normal(size=(len(groups), len(FEATURES)))
        y = x[:, :2] * 1.5
        for piece in np.unique(groups):
            mask = groups == piece
            x[mask] -= x[mask].mean(axis=0)
            y[mask] -= y[mask].mean(axis=0)
        pred = predict_out_of_fold(x, y, groups, FEATURES[:2])
        result = evaluate_pairs(y, pred, groups)
        self.assertGreater(result["arousal"]["delta_r2"], 0.7)
        self.assertGreater(result["valence"]["delta_r2"], 0.7)

    def test_percepiano_score_groups_do_not_mix_interpretations(self):
        a = "Schubert_D960_mv3_8bars_1_25"
        b = "Schubert_D960_mv3_8bars_2_25"
        c = "Schubert_D960_mv3_8bars_1_26"
        self.assertEqual(scored_excerpt(a), scored_excerpt(b))
        self.assertNotEqual(scored_excerpt(a), scored_excerpt(c))
        self.assertEqual(scored_excerpt("Beethoven_WoO80_var27_8bars_1_15"),
                         scored_excerpt("Beethoven_WoO80_var27_8bars_22_2"))
        self.assertEqual(parent_work(a), "Schubert_D960_mv3")

    def test_hard_comparisons_require_one_full_likert_step(self):
        self.assertAlmostEqual(HARD_DIFFERENCE, 1 / 7)
        groups = np.array([0, 0, 0, 1, 1, 1])
        y = np.zeros((6, 4))
        y[:, 1] = [0, 1/7, 2/7, 0, 1/14, 1/7]
        pred = y.copy()
        result = evaluate(y, pred, groups)
        self.assertEqual(result["dark"]["hard_pair_accuracy"], 1.0)
        self.assertLess(result["dark"]["hard_pair_evaluable"],
                        result["dark"]["pair_evaluable"])

    def test_pulse_proxies_ignore_unreliable_time_signature_metadata(self):
        with TemporaryDirectory() as tmp:
            values = []
            for signature in ((3, 4), (4, 4)):
                path = Path(tmp) / f"{signature[0]}-four.mid"
                midi = mido.MidiFile(ticks_per_beat=480)
                tr = mido.MidiTrack()
                midi.tracks.append(tr)
                tr.append(mido.MetaMessage("time_signature", numerator=signature[0],
                                           denominator=signature[1], time=0))
                tr.append(mido.MetaMessage("set_tempo", tempo=500_000, time=0))
                for i in range(24):
                    tr.append(mido.Message("note_on", note=60 + i % 5,
                                           velocity=50 + i % 7 * 9, time=240))
                    tr.append(mido.Message("note_off", note=60 + i % 5,
                                           velocity=0, time=120))
                midi.save(path)
                values.append(expressive_pulse_features(path))
            self.assertEqual(set(values[0]), set(PULSE_FEATURE_NAMES))
            for feat in PULSE_FEATURE_NAMES:
                self.assertTrue(np.isfinite(values[0][feat]), feat)
                self.assertAlmostEqual(values[0][feat], values[1][feat], places=10)

    def test_negative_control_reassigns_performances_but_preserves_score_means(self):
        x = np.arange(60, dtype=float).reshape(20, 3)
        groups = np.repeat(np.arange(4), 5)
        z = center_within_score(x, groups)
        shuffled = shuffled_within_score(z, groups, seed=13)
        self.assertFalse(np.array_equal(z, shuffled))
        for group in np.unique(groups):
            self.assertTrue(np.allclose(z[groups == group].mean(axis=0), 0))
            for col in range(x.shape[1]):
                self.assertEqual(sorted(z[groups == group, col]),
                                 sorted(shuffled[groups == group, col]))

    def test_score_free_accent_tracks_high_note_anticipation_and_midi_velocity(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "chords.mid"
            midi = mido.MidiFile(ticks_per_beat=480)
            tr = mido.MidiTrack()
            midi.tracks.append(tr)
            tr.append(mido.MetaMessage("set_tempo", tempo=500_000, time=0))
            for i in range(16):
                # Higher voice is stronger and slightly early (one MIDI tick).
                tr.append(mido.Message("note_on", note=72, velocity=102, time=480))
                tr.append(mido.Message("note_on", note=48, velocity=42, time=4))
                tr.append(mido.Message("note_off", note=72, velocity=0, time=230))
                tr.append(mido.Message("note_off", note=48, velocity=0, time=0))
            midi.save(path)
            v = expressive_accent_features(path)
            self.assertEqual(set(v), set(ACCENT_FEATURE_NAMES))
            self.assertTrue(all(np.isfinite(z) for z in v.values()))
            self.assertGreater(v["high_vs_low_velocity"], 0.1)
            self.assertLess(v["high_note_lead_ms"], -2.0)

    def test_work_holdout_regression_can_generalize_identical_relationship(self):
        rng = np.random.default_rng(19)
        work = np.repeat(np.arange(4), 30)
        x = rng.standard_normal((120, 3))
        y = x[:, :2] * 2
        estimate = work_regression(x, y, work)
        self.assertEqual(estimate.shape, y.shape)
        self.assertGreater(np.corrcoef(y[:, 0], estimate[:, 0])[0, 1], .95)


if __name__ == "__main__":
    unittest.main()
