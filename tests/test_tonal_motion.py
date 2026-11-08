"""Synthetic tests: tonal trajectories use only musical notes, no labels."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import mido
import numpy as np

from anamu.tonal_motion import (
    TONAL_MOTION_FEATURE_NAMES, midi_tonal_motion, tonal_motion_features,
)
from anamu.piast_at import PIASTClip
from scripts.piast_at_benchmark import run
from scripts.piast_tonal_motion_experiment import validation_only_selection, ARMS


class TonalMotionTests(unittest.TestCase):
    def test_tonal_arm_selection_never_chooses_using_test_scores(self):
        values = {}
        for index, arm in enumerate(ARMS):
            values[arm] = {
                "validation": {"hard_five": {"ap_by_mood": {"Dark": .2 + index * .1}}},
                "test": {"hard_five": {"ap_by_mood": {"Dark": 1. - index * .2}}},
                "fresh_test": {"hard_five": {"ap_by_mood": {"Dark": .5}}},
            }
        first = validation_only_selection(values, moods=("Dark",))
        for arm in ARMS:
            values[arm]["test"]["hard_five"]["ap_by_mood"]["Dark"] *= 0.01
        second = validation_only_selection(values, moods=("Dark",))
        self.assertEqual(first["choices"]["Dark"]["arm_selected_by_validation"],
                         second["choices"]["Dark"]["arm_selected_by_validation"])

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

    def test_piast_tonal_features_do_not_contaminate_shared_baseline_cache(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "midi").mkdir()
            clips = []
            for i in range(55):
                name = f"t{i:04}.mid"
                (root / "midi" / name).write_bytes(i.to_bytes(2, "little"))
                clips.append(PIASTClip(f"t{i:04}", name, f"song-{i}",
                                       frozenset(), frozenset(), frozenset()))
            dummy_scores = {"named_moods": {}, "all_moods": {}, "per_mood": {}}
            with (patch("scripts.piast_at_benchmark.load_annotations", return_value=clips),
                  patch("scripts.piast_at_benchmark.available_annotations", return_value=clips),
                  patch("scripts.piast_at_benchmark.infer_measure_count", return_value=2),
                  patch("scripts.piast_at_benchmark.extract_academic_rows",
                        return_value=([{"foo": 1.}, {"foo": 2.}], None, None)),
                  patch("scripts.piast_at_benchmark.midi_emotion_cues",
                        return_value={"cue_minor_minus_major_fit": .25}),
                  patch("scripts.piast_at_benchmark.midi_tonal_motion",
                        side_effect=lambda *args, **kwargs: {
                            "tonal_motion_minor_evidence_mean": 0.7 if not kwargs["shuffle"] else -0.7}),
                  patch("scripts.piast_at_benchmark.score_labels", return_value=dummy_scores)):
                tonal = run(root, feature_set="research_tonal_motion", cache_dir=root/"cache")
                baseline = run(root, feature_set="research_cues", cache_dir=root/"cache")
                shuffled = run(root, feature_set="research_tonal_motion_shuffled",
                               cache_dir=root/"cache")
            self.assertIn("tonal_motion_minor_evidence_mean", tonal["feature_names"])
            self.assertIn("tonal_motion_minor_evidence_mean", shuffled["feature_names"])
            self.assertNotIn("tonal_motion_minor_evidence_mean", baseline["feature_names"])
            self.assertEqual(tonal["split_sizes"], baseline["split_sizes"])
            self.assertEqual(shuffled["split_sizes"], baseline["split_sizes"])


if __name__ == "__main__":
    unittest.main()
