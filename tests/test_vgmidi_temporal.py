"""Checks for time alignment, human disagreement and genuine group holdout."""

import json
import tempfile
import unittest
from pathlib import Path

import mido

from anamu.vgmidi_temporal import (extract_midi_measures, load_human_pieces,
                                   select_splits)


class VgmidiTemporalTests(unittest.TestCase):
    def test_raw_annotators_aggregate_per_measure_without_erasing_variance(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = {
                "pieces": {"piece0": {"midi": "One.mid", "name": "One", "measures": 4,
                                      "duration": 8.0}},
                "annotations": {
                    f"piece0_{i}": {"valence": [i / 10] * 4,
                                    "arousal": [-i / 10] * 4} for i in range(10)
                },
            }
            (root / "raw.json").write_text(json.dumps(content))
            pieces = load_human_pieces([root / "raw.json"])
            self.assertEqual(len(pieces), 1)
            self.assertEqual(pieces[0].human[0]["annotators"], 10)
            self.assertAlmostEqual(pieces[0].human[0]["valence_median"], .45)
            self.assertGreater(pieces[0].human[0]["valence_q75"],
                               pieces[0].human[0]["valence_q25"])
            self.assertEqual(len(pieces[0].human), 4)

    def test_split_uses_only_file_identity_not_human_ratings(self):
        from dataclasses import replace
        from anamu.vgmidi_temporal import HumanPiece
        originals = [HumanPiece(f"a{i}.mid", str(i), 4, 8, ({"valence_median": i},))
                     for i in range(40)]
        original = select_splits(originals, n_test=10, n_validation=5)
        changed = [replace(piece, human=({"valence_median": -99},)) for piece in originals]
        self.assertEqual(original, select_splits(changed, n_test=10, n_validation=5))
        self.assertEqual(list(original.values()).count("test"), 10)
        self.assertEqual(list(original.values()).count("validation"), 5)

    def test_midi_features_work_in_measure_units_even_with_tempo_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fixture.mid"
            score = mido.MidiFile(ticks_per_beat=480)
            track = mido.MidiTrack()
            score.tracks.append(track)
            track.append(mido.MetaMessage("time_signature", numerator=4, denominator=4,
                                          time=0))
            track.append(mido.MetaMessage("set_tempo", tempo=500000, time=0))
            for i in range(4):
                track.append(mido.Message("note_on", note=60 + i, velocity=60 + i,
                                          time=0))
                track.append(mido.Message("note_off", note=60 + i, velocity=0,
                                          time=1920))
                if i == 1:
                    track.append(mido.MetaMessage("set_tempo", tempo=1000000, time=0))
            score.save(path)
            features, meta = extract_midi_measures(path, 4)
            self.assertEqual(len(features), 4)
            self.assertTrue(all(row["note_density"] == .25 for row in features))
            self.assertEqual(meta["beats_per_measure"], 4)
            self.assertAlmostEqual(meta["midi_duration_seconds"], 12)

    def test_bad_temporal_grid_is_rejected_not_silently_rescaled(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fixture.mid"
            score = mido.MidiFile(ticks_per_beat=480)
            track = mido.MidiTrack()
            score.tracks.append(track)
            track.append(mido.Message("note_on", note=60, velocity=64, time=0))
            track.append(mido.Message("note_off", note=60, velocity=0, time=1920))
            score.save(path)
            with self.assertRaisesRegex(ValueError, "measure_alignment_not_confirmed"):
                extract_midi_measures(path, 12)


if __name__ == "__main__":
    unittest.main()
