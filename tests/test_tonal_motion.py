"""Synthetic tests: tonal trajectories use only musical notes, no labels."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import mido
import numpy as np

from anamu.tonal_motion import (
    TONAL_MOTION_FEATURE_NAMES, midi_tonal_motion, tonal_motion_features,
)


class TonalMotionTests(unittest.TestCase):
    @staticmethod
    def _sequence(notes_by_window):
        notes = []
        for window, pitches in enumerate(notes_by_window):
            for position, pitch in enumerate(pitches):
                start = window * 4800 + position * 200
                notes.append((start, start + 350, pitch, 72))
        return np.asarray(notes, dtype=float)

    def test_minor_to_major_motion_differs_from_reverse(self):
        minor = [60, 63, 67, 72, 63, 67, 60, 67]
        major = [60, 64, 67, 72, 64, 67, 60, 67]
        forward = tonal_motion_features(self._sequence([minor] * 4 + [major] * 4))
        reverse = tonal_motion_features(self._sequence([major] * 4 + [minor] * 4))
        self.assertEqual(set(forward), set(TONAL_MOTION_FEATURE_NAMES))
        self.assertGreater(reverse["tonal_motion_minor_evidence_last_first"],
                           forward["tonal_motion_minor_evidence_last_first"])
        self.assertAlmostEqual(forward["tonal_motion_minor_evidence_mean"],
                               reverse["tonal_motion_minor_evidence_mean"], places=10)

    def test_shuffled_windows_keep_histograms_but_break_motion(self):
        minor = [60, 63, 67, 72, 63, 67, 60, 67]
        major = [60, 64, 67, 72, 64, 67, 60, 67]
        notes = self._sequence([minor] * 4 + [major] * 4)
        original = tonal_motion_features(notes)
        shuffled = tonal_motion_features(notes, shuffle=True, seed=13)
        for metric in ("tonal_motion_minor_evidence_mean",
                       "tonal_motion_minor_evidence_std",
                       "tonal_motion_confidence_mean"):
            self.assertAlmostEqual(original[metric], shuffled[metric], places=12)
        self.assertNotAlmostEqual(original["tonal_motion_minor_evidence_late_early"],
                                  shuffled["tonal_motion_minor_evidence_late_early"])

    def test_midi_time_signature_does_not_change_tonal_inference(self):
        with TemporaryDirectory() as tmp:
            features = []
            for numerator in (3, 4):
                path = Path(tmp) / f"{numerator}-signature.mid"
                midi = mido.MidiFile(ticks_per_beat=480)
                track = mido.MidiTrack()
                midi.tracks.append(track)
                track.append(mido.MetaMessage("time_signature", numerator=numerator,
                                               denominator=4, time=0))
                for i in range(40):
                    track.append(mido.Message("note_on", note=(60, 63, 67, 72, 64)[i % 5],
                                               velocity=67, time=240))
                    track.append(mido.Message("note_off", note=(60, 63, 67, 72, 64)[i % 5],
                                               time=120))
                midi.save(path)
                features.append(midi_tonal_motion(path))
            for name in TONAL_MOTION_FEATURE_NAMES:
                self.assertAlmostEqual(features[0][name], features[1][name], places=10)


if __name__ == "__main__":
    unittest.main()
