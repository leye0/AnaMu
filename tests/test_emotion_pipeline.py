"""Short deployment checks; the expensive academic corpus run is separate."""

import tempfile
import unittest
from pathlib import Path

import numpy as np

from anamu.emotion_pipeline import (export_ridge_artifact, load_ridge_artifact,
                                    predict_ridge_artifact, infer_measure_count)
from anamu.expectation import VariableOrderExpectancy
from scripts.vgmidi_temporal_benchmark import create_model, fit, predict


class EmotionPipelineTests(unittest.TestCase):
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
