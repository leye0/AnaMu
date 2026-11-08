"""Checks for research-inspired MIDI mechanisms, never learned from labels."""

import tempfile
import unittest
from pathlib import Path

import mido

from anamu.piast_research_cues import midi_emotion_cues


def write_piano(path: Path, *, tempo: int = 500_000, duration: int = 240,
                pitches: tuple[int, ...] = (60, 64, 67, 60, 64, 67, 72, 60)) -> None:
    midi = mido.MidiFile(ticks_per_beat=480)
    track = mido.MidiTrack()
    midi.tracks.append(track)
    track.append(mido.MetaMessage("set_tempo", tempo=tempo, time=0))
    for index, note in enumerate(pitches):
        track.append(mido.Message("note_on", note=note, velocity=64, time=0 if index == 0
                                  else 480 - duration))
        track.append(mido.Message("note_off", note=note, velocity=0, time=duration))
    midi.save(path)


class ResearchCuesTests(unittest.TestCase):
    def test_actual_midi_tempo_not_onset_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            slow, fast = Path(tmp) / "slow.mid", Path(tmp) / "fast.mid"
            write_piano(slow, tempo=750_000)
            write_piano(fast, tempo=375_000)
            self.assertAlmostEqual(midi_emotion_cues(slow)["cue_performed_bpm"], 80.)
            self.assertAlmostEqual(midi_emotion_cues(fast)["cue_performed_bpm"], 160.)

    def test_staccato_and_legato_are_distinct(self):
        with tempfile.TemporaryDirectory() as tmp:
            short, long = Path(tmp) / "short.mid", Path(tmp) / "long.mid"
            write_piano(short, duration=160)
            write_piano(long, duration=480)
            short_cues = midi_emotion_cues(short)
            long_cues = midi_emotion_cues(long)
            self.assertGreater(short_cues["cue_detached_fraction"], .9)
            self.assertLess(long_cues["cue_detached_fraction"], .1)
            self.assertGreater(long_cues["cue_articulation_median_ratio"],
                               short_cues["cue_articulation_median_ratio"])

    def test_mode_profile_and_interactions(self):
        with tempfile.TemporaryDirectory() as tmp:
            major, minor = Path(tmp) / "major.mid", Path(tmp) / "minor.mid"
            write_piano(major)
            write_piano(minor, pitches=(60, 63, 67, 60, 63, 67, 72, 60))
            maj = midi_emotion_cues(major, interactions=True)
            minr = midi_emotion_cues(minor, interactions=True)
            self.assertLess(maj["cue_minor_minus_major_fit"],
                            minr["cue_minor_minus_major_fit"])
            self.assertIn("cue_x_mode_tempo", maj)
            self.assertTrue(all(isinstance(value, float) for value in maj.values()))


if __name__ == "__main__":
    unittest.main()
