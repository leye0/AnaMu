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
    center_within_score, nested_emotion_selector, shuffled_within_score,
    work_regression,
)
from anamu.expressive_pulse import PULSE_FEATURE_NAMES, expressive_pulse_features
from anamu.expressive_accent import ACCENT_FEATURE_NAMES, expressive_accent_features
from anamu.score_aligned_expression import (
    SCORE_FEATURE_NAMES, _read_midi, score_aligned_features,
)


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

    def test_aligned_score_uses_real_corresponding_written_notes(self):
        with TemporaryDirectory() as tmp:
            data = Path(tmp)
            perf_folder = data / "all_2rounds"
            score_folder = data / "score_midi"
            perf_folder.mkdir()
            score_folder.mkdir()
            names = (score_folder / "Schubert_D960_mv3_8bars_Score_25.mid",
                     perf_folder / "Schubert_D960_mv3_8bars_1_25.mid")
            for index, path in enumerate(names):
                midi = mido.MidiFile(ticks_per_beat=480)
                tr = mido.MidiTrack()
                midi.tracks.append(tr)
                tr.append(mido.MetaMessage("time_signature", numerator=3 if not index else 4,
                                           denominator=4, time=0))
                tr.append(mido.MetaMessage("set_tempo", tempo=500_000, time=0))
                for i in range(24):
                    tr.append(mido.Message("note_on", note=60 + i % 6,
                                           velocity=60 + index * 10, time=500 + index * 30))
                    tr.append(mido.Message("note_on", note=72 + i % 5,
                                           velocity=85 + index * 5, time=0))
                    tr.append(mido.Message("note_off", note=60 + i % 6,
                                           velocity=0, time=250))
                    tr.append(mido.Message("note_off", note=72 + i % 5,
                                           velocity=0, time=0))
                midi.save(path)
            values = score_aligned_features(names[1])
            diagnostics = values.pop("alignment_diagnostics")
            self.assertEqual(set(values), set(SCORE_FEATURE_NAMES))
            self.assertTrue(all(np.isfinite(v) for v in values.values()))
            self.assertGreater(diagnostics["match_fraction"], .99)
            self.assertGreater(values["score_register_dynamic_contrast"], 0.)
            # CP-WTC uses an external MusicXML-derived score-note array.
            supplied = score_aligned_features(names[1], score_notes=_read_midi(names[0]))
            for feature in SCORE_FEATURE_NAMES:
                self.assertAlmostEqual(values[feature], supplied[feature], places=10)
            unrelated_score = _read_midi(names[0]).copy()
            unrelated_score[:, 1] += 24
            with self.assertRaisesRegex(ValueError, "insufficient_pitch_matching"):
                score_aligned_features(names[1], score_notes=unrelated_score)

    def test_work_holdout_regression_can_generalize_identical_relationship(self):
        rng = np.random.default_rng(19)
        work = np.repeat(np.arange(4), 30)
        x = rng.standard_normal((120, 3))
        y = x[:, :2] * 2
        estimate = work_regression(x, y, work)
        self.assertEqual(estimate.shape, y.shape)
        self.assertGreater(np.corrcoef(y[:, 0], estimate[:, 0])[0, 1], .95)

    def test_nested_selection_never_reads_held_out_work_labels(self):
        rng = np.random.default_rng(129)
        works = np.repeat(np.arange(4), 15)
        score_groups = np.repeat(np.arange(12), 5)
        base = rng.normal(size=(len(works), 4))
        extra = np.column_stack((base, rng.normal(size=(len(works), 2))))
        control = np.column_stack((base, rng.normal(size=(len(works), 2))))
        y = base * 1.5
        systems = {"baseline_expressivity": base,
                   "additional_features": extra, "permuted_control": control}
        # Outer predictions are intentionally arbitrary; inner selection must
        # depend on other works' train labels only, never on these predictions.
        predictions = {arm: {"ranker": np.zeros_like(y)} for arm in systems}
        first = nested_emotion_selector(y, score_groups, works,
                                        systems, predictions)
        y_mutated = y.copy()
        y_mutated[works == 0] *= -12
        second = nested_emotion_selector(y_mutated, score_groups, works,
                                         systems, predictions)
        for arm in ("additional_features", "permuted_control"):
            self.assertEqual(first[arm]["choices_by_work_id"][0],
                             second[arm]["choices_by_work_id"][0])


if __name__ == "__main__":
    unittest.main()
