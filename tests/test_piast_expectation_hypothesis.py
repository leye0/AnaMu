"""Leakage guards and falsification controls for the PIAST-AT surprise idea."""

from __future__ import annotations

import math
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import mido

from anamu.expectation import VariableOrderExpectancy
from anamu.piast_expectation_hypothesis import (
    add_out_of_fold_expectancy, melodic_intervals, shuffled_events,
    surprise_observations,
)


class SurpriseHypothesisTests(unittest.TestCase):
    def test_extracts_actual_intervals_from_midi_onsets(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "upper.mid"
            midi = mido.MidiFile(ticks_per_beat=480)
            track = mido.MidiTrack()
            midi.tracks.append(track)
            for pitch in (60, 62, 65, 60, 61, 64):
                track.append(mido.Message("note_on", note=pitch,
                                          velocity=60, time=120 if len(track) else 0))
                track.append(mido.Message("note_off", note=pitch, velocity=0, time=120))
            midi.save(path)
            self.assertEqual(melodic_intervals(path), (2, 3, -5, 1, 3))

    def test_event_shuffle_preserves_histogram_and_is_reproducible(self):
        events = tuple([0, 2, -1, 4] * 40)
        once = shuffled_events(events, "piano-song", 9)
        self.assertEqual(once, shuffled_events(events, "piano-song", 9))
        self.assertEqual(Counter(once), Counter(events))
        self.assertNotEqual(once, events)

    def test_order_sensitive_model_predicts_repeated_pattern(self):
        pattern = tuple([2, 3, -5] * 80)
        model = VariableOrderExpectancy(max_order=3, smoothing=2.0).fit(
            [pattern, pattern, pattern])
        real = surprise_observations(model, pattern)
        scrambled = surprise_observations(model, shuffled_events(pattern, "song", 11))
        self.assertLess(real["surprise_ic_mean"], scrambled["surprise_ic_mean"])
        for feature in real.values():
            self.assertTrue(math.isfinite(feature))

    def test_zero_order_model_ignores_context(self):
        model = VariableOrderExpectancy(max_order=0, smoothing=2.0).fit([[1, 2, 3] * 8])
        self.assertEqual(model.probability(2, (1, 3, 3)), model.probability(2, ()))

    def test_training_features_never_use_own_song_group(self):
        # Each song owns a unique interval token; using its MIDI in the prior
        # would trigger the spy's assertion, even if grouped clips share a song.
        clips = [SimpleNamespace(clip_id=f"train-{i}", song_group=f"song-{i}",
                                 midi_name=f"train-{i}.mid") for i in range(20)]
        clips.append(SimpleNamespace(clip_id="train-extra", song_group="song-0",
                                     midi_name="train-extra.mid"))
        validation = SimpleNamespace(clip_id="validation", song_group="other-val",
                                     midi_name="validation.mid")
        test = SimpleNamespace(clip_id="test", song_group="other-test",
                               midi_name="test.mid")
        groups = {clip.clip_id: (0 if clip.song_group == "song-0" else i + 1)
                  for i, clip in enumerate(clips)}
        groups["validation"] = 500
        groups["test"] = 501
        splits = {"train": [(clip, {}) for clip in clips],
                  "validation": [(validation, {})], "test": [(test, {})]}

        class OwnGroupGuard:
            def __init__(self, max_order, smoothing):
                self.max_order = max_order

            def fit(self, training_sequences):
                self.seen = {event for sequence in training_sequences for event in sequence}
                return self

            def probability(self, event, context=()):
                if event in self.seen:
                    raise AssertionError("source group leaked into training prior")
                return .1

            def entropy(self, context=()):
                return 1.0

        with patch("anamu.piast_expectation_hypothesis.melodic_intervals",
                   side_effect=lambda path: (groups[path.stem],) * 5), \
             patch("anamu.piast_expectation_hypothesis.VariableOrderExpectancy",
                   OwnGroupGuard):
            metadata = add_out_of_fold_expectancy(splits, Path("/fake"), order=3)
        self.assertEqual(metadata["training_prior"], "out-of-fold, source-group-exclusive")
        self.assertEqual(len(splits["train"]), 21)
        self.assertTrue(all("surprise_ic_mean" in fields for section in splits.values()
                            for _, fields in section))


if __name__ == "__main__":
    unittest.main()
