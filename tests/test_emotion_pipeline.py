"""Short deployment checks; the expensive academic corpus run is separate."""

import tempfile
import unittest
import subprocess
from pathlib import Path
from unittest.mock import patch

import numpy as np

from anamu.emotion_pipeline import (export_ridge_artifact, load_ridge_artifact,
                                    predict_ridge_artifact, infer_measure_count,
                                    execute_original_jsymbolic)
from anamu.expectation import VariableOrderExpectancy
from anamu.jsymbolic_segments import split_midi_measures
from scripts.vgmidi_temporal_benchmark import create_model, fit, predict


class EmotionPipelineTests(unittest.TestCase):
    def test_bounded_original_java_segments_preserve_crossing_notes_and_tempo(self):
        import mido
        with tempfile.TemporaryDirectory() as tmp:
            origin = Path(tmp) / "source.mid"
            midi = mido.MidiFile(ticks_per_beat=480)
            track = mido.MidiTrack()
            midi.tracks.append(track)
            track.append(mido.MetaMessage("set_tempo", tempo=600000, time=0))
            track.append(mido.Message("program_change", program=11, time=0))
            track.append(mido.Message("note_on", note=67, velocity=81, time=3700))
            track.append(mido.Message("note_off", note=67, velocity=0, time=400))
            midi.save(origin)
            segments = split_midi_measures(origin, Path(tmp) / "segments",
                                           measure_count=4, max_measures=2)
            self.assertEqual(len(segments), 2)
            self.assertAlmostEqual(segments[1].start_seconds, 4.8)
            for segment in segments:
                messages = list(mido.MidiFile(segment.path).tracks[0])
                self.assertTrue(any(m.type == "set_tempo" and m.tempo == 600000
                                    for m in messages))
                self.assertTrue(any(m.type == "program_change" and m.program == 11
                                    for m in messages))
                self.assertEqual(sum(m.type == "note_on" for m in messages), 1)
                self.assertEqual(sum(m.type == "note_off" for m in messages), 1)
            self.assertEqual(segments[0].source_unmatched_note_off_count, 0)

    def test_original_java_timeout_falls_back_to_real_longer_windows(self):
        with tempfile.TemporaryDirectory() as tmp:
            midi, jar = Path(tmp) / "known.mid", Path(tmp) / "jSymbolic2.jar"
            midi.touch()
            jar.touch()
            attempted = []

            def fake_java(command, **kwargs):
                window = float(command[-2])
                attempted.append(window)
                if window == 10.:
                    raise subprocess.TimeoutExpired(command, kwargs["timeout"])
                Path(command[-4]).write_text("original-java-output")
                return subprocess.CompletedProcess(command, 0, "", "")

            # This validates fallback selection and provenance without
            # pretending a mock executed any real academic feature algorithm.
            ace = {"data_sets": [{"source_id": str(midi),
                                  "whole_piece_features": {}, "windows": []}]}
            with patch("anamu.emotion_pipeline.subprocess.run", side_effect=fake_java), \
                 patch("anamu.emotion_pipeline.read_jsymbolic_ace", return_value=ace):
                record = execute_original_jsymbolic(midi, jar, timeout_seconds=1,
                                                     fallback_timeout_seconds=1)
            self.assertEqual(attempted, [10., 30.])
            self.assertTrue(record["anamu_window_fallback_used"])
            self.assertEqual(record["anamu_extraction_window_seconds"], 30.)

    def test_safe_json_ridge_roundtrip_matches_sklearn_with_missing_features(self):
        matrix = np.asarray([[1.0, np.nan, 5.0], [2.0, 3.0, np.nan],
                             [5.0, 4.0, 4.0], [7.0, np.nan, 6.0]])
        targets = np.asarray([[.2, -.2], [.3, .4], [.9, .1], [-.3, .5]])
        model = fit(create_model("ridge_100"), matrix, targets, np.ones(4) / 4)
        prior = VariableOrderExpectancy(max_order=2).fit([["a", "b", "a"], ["b", "a"]])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "model.json"
            export_ridge_artifact(path, model, ["a", "b", "c"],
                                  {"melodic_interval": prior}, metadata={"train": "fixture"})
            artifact = load_ridge_artifact(path)
            restored_prior = VariableOrderExpectancy.from_state(
                artifact["expectancy_models"]["melodic_interval"])
            self.assertAlmostEqual(prior.probability("a", ["b"]),
                                   restored_prior.probability("a", ["b"]))
            rows = [{"a": x[0], "b": x[1], "c": x[2]} for x in matrix]
            result = predict_ridge_artifact(artifact, rows)
            np.testing.assert_allclose(result, predict(model, matrix), atol=1e-10)

    def test_infers_last_sounding_bar_ignoring_trailing_silence(self):
        import mido
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "known.mid"
            midi = mido.MidiFile(ticks_per_beat=480)
            track = mido.MidiTrack()
            midi.tracks.append(track)
            track.append(mido.Message("note_on", note=60, velocity=64, time=0))
            track.append(mido.Message("note_off", note=60, velocity=0, time=3840))
            track.append(mido.MetaMessage("end_of_track", time=9600))
            midi.save(path)
            self.assertEqual(infer_measure_count(path), 2)


if __name__ == "__main__":
    unittest.main()
