"""Temporal dynamics, order controls and missing-data guardrails."""

import math
import tempfile
import unittest
from pathlib import Path

import mido

from anamu.piast_tension_hypothesis import tension_trend_features
from scripts.piast_at_benchmark import run


def bars(velocities):
    return [{"vertical_interval_clash": v / 300,
             "mean_velocity": v,
             "onset_density": v / 20,
             "weak_beat_onset_fraction": v / 127,
             "pitch_range": v / 2}
            for v in velocities]


class TensionHypothesisTests(unittest.TestCase):
    def test_flat_piece_has_no_illusory_tension_curve(self):
        features = tension_trend_features(bars([65] * 20))
        self.assertEqual(len(features), 22)
        self.assertEqual(features["farbood_w2_cumulative_excursion"], 0.)
        self.assertEqual(features["farbood_w4_max_drawdown"], 0.)

    def test_rising_then_falling_piece_has_rise_release_and_reversal(self):
        dynamics = list(range(25, 110, 5)) + list(range(110, 25, -5))
        f = tension_trend_features(bars(dynamics))
        self.assertGreater(f["farbood_w2_rise_total_per_bar"], 0.)
        self.assertGreater(f["farbood_w2_fall_total_per_bar"], 0.)
        self.assertGreater(f["farbood_w2_max_drawdown"], 0.)
        self.assertGreater(f["farbood_w2_reversal_fraction"], 0.)
        self.assertGreater(f["farbood_w4_peak_to_end_release"], 0.)

    def test_shuffling_only_changes_time_order_not_measure_distribution(self):
        rows = bars(list(range(20, 115, 3)))
        before = [row.copy() for row in rows]
        chronological = tension_trend_features(rows)
        shuffled = tension_trend_features(rows, shuffle=True, group="song-a")
        self.assertEqual(shuffled, tension_trend_features(
            rows, shuffle=True, group="song-a"))
        self.assertNotEqual(chronological, shuffled)
        self.assertEqual(rows, before)

    def test_missing_values_do_not_create_false_negative_tension(self):
        rows = [{"mean_velocity": float("nan"), "onset_density": None}
                for _ in range(12)]
        result = tension_trend_features(rows)
        self.assertEqual(result["farbood_w2_cumulative_excursion"], 0.)
        self.assertTrue(all(math.isfinite(v) for v in result.values()))

    def test_real_benchmark_integration_on_synthetic_symbolic_midi(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            midi_root = root / "midi"
            midi_root.mkdir()
            lines = ["AudioFile,Agreements_3,Agreements_2,Agreements_1"]
            for i in range(35):
                name = f"video{i:06d}"
                lines.append(f"{name},,{('Tense' if i % 2 else 'Happy')},")
                midi = mido.MidiFile(ticks_per_beat=480)
                track = mido.MidiTrack()
                midi.tracks.append(track)
                for k in range(24):
                    pitch = 55 + ((k + i) % 12)
                    track.append(mido.Message("note_on", note=pitch, velocity=45+i,
                                              time=240 if k else 0))
                    track.append(mido.Message("note_off", note=pitch,
                                              velocity=0, time=240))
                midi.save(midi_root / (name + ".mid"))
            (root / "at_text.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")
            baseline = run(root, feature_set="research_cues")
            tension = run(root, feature_set="research_tension")
            combined = run(root, feature_set="research_surprise_tension")
            self.assertEqual(tension["accepted"], 35)
            self.assertEqual(combined["accepted"], 35)
            self.assertEqual(tension["feature_count"], baseline["feature_count"] + 22)
            self.assertEqual(combined["feature_count"], baseline["feature_count"] + 34)
            self.assertIsNone(tension["expectancy_protocol"])
            self.assertEqual(combined["expectancy_protocol"]["prior_max_order"], 3)


if __name__ == "__main__":
    unittest.main()
