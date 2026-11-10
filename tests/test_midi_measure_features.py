"""Per-measure MIDI observations never depend on human labels."""

import tempfile
import unittest
from pathlib import Path

import mido

from anamu.midi_measure_features import extract_midi_measures


class MidiMeasureTests(unittest.TestCase):
    @staticmethod
    def write_midi(path: Path, *, notes=4):
        midi = mido.MidiFile(ticks_per_beat=480)
        track = mido.MidiTrack()
        midi.tracks.append(track)
        track.append(mido.MetaMessage("time_signature", numerator=4,
                                      denominator=4, time=0))
        track.append(mido.MetaMessage("set_tempo", tempo=500000, time=0))
        for i in range(notes):
            track.append(mido.Message("note_on", note=60 + i,
                                      velocity=60 + i, time=0))
            track.append(mido.Message("note_off", note=60 + i,
                                      velocity=0, time=1920))
            if i == 1:
                track.append(mido.MetaMessage("set_tempo", tempo=1000000, time=0))
        midi.save(path)

    def test_midi_measure_features_keep_beats_and_tempo_changes_separate(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fixture.mid"
            self.write_midi(path)
            rows, metadata = extract_midi_measures(path, 4)
            self.assertEqual(len(rows), 4)
            self.assertTrue(all(row["note_density"] == .25 for row in rows))
            self.assertEqual(metadata["beats_per_measure"], 4)
            self.assertAlmostEqual(metadata["midi_duration_seconds"], 12)
            self.assertEqual(len(metadata["source_sha256"]), 64)

    def test_rejects_incompatible_bar_grid(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fixture.mid"
            self.write_midi(path)
            with self.assertRaisesRegex(ValueError, "measure_alignment_not_confirmed"):
                extract_midi_measures(path, 12)


if __name__ == "__main__":
    unittest.main()
