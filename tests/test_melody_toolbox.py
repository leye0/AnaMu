"""Bounded tests of the real melody-features library and accurate MIDI time."""

from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path

import mido

from anamu.melody_toolbox import _json_value, extract_melody_toolbox
from anamu.tempo_map import MidiTempoMap


def make_midi(*, overlapping: bool = False, tempo_change: bool = False) -> bytes:
    midi = mido.MidiFile(type=1, ticks_per_beat=480)
    tempo = mido.MidiTrack()
    notes = mido.MidiTrack()
    midi.tracks.extend((tempo, notes))
    if tempo_change:
        tempo.append(mido.MetaMessage("set_tempo", tempo=500_000, time=0))
        tempo.append(mido.MetaMessage("set_tempo", tempo=1_000_000, time=480))
    pitches = [60, 62, 64, 65, 67, 69, 67, 64, 60]
    if overlapping:
        for pitch in pitches:
            notes.append(mido.Message("note_on", channel=0, note=pitch,
                                      velocity=80, time=0))
        for pitch in pitches:
            notes.append(mido.Message("note_off", channel=0, note=pitch, time=480))
    else:
        for pitch in pitches:
            notes.append(mido.Message("note_on", channel=0, note=pitch,
                                      velocity=80, time=0))
            notes.append(mido.Message("note_off", channel=0, note=pitch, time=480))
    stream = io.BytesIO()
    midi.save(file=stream)
    return stream.getvalue()


class MidiTempoMapTests(unittest.TestCase):
    def test_piecewise_tempo_is_in_seconds_not_score_beats(self):
        timing = MidiTempoMap.from_bytes(make_midi(tempo_change=True))
        self.assertEqual(timing.ticks_per_quarter, 480)
        self.assertAlmostEqual(timing.beats_to_seconds(0), 0)
        self.assertAlmostEqual(timing.beats_to_seconds(1), 0.5)
        self.assertAlmostEqual(timing.beats_to_seconds(1.5), 1)
        self.assertAlmostEqual(timing.beats_to_seconds(3), 2.5)
        self.assertEqual(timing.tempo_changes_seconds(), [(0.0, 120.0), (0.5, 60.0)])

    def test_tempo_at_zero_replaces_default(self):
        midi = mido.MidiFile(ticks_per_beat=480)
        track = mido.MidiTrack()
        midi.tracks.append(track)
        track.append(mido.MetaMessage("set_tempo", tempo=1_000_000, time=0))
        stream = io.BytesIO()
        midi.save(file=stream)
        timing = MidiTempoMap.from_bytes(stream.getvalue())
        self.assertEqual(len(timing.segments), 1)
        self.assertEqual(timing.beats_to_seconds(2), 2)

    def test_negative_beat_rejected(self):
        timing = MidiTempoMap.from_bytes(make_midi())
        with self.assertRaises(ValueError):
            timing.beats_to_seconds(-0.1)


class PublishedMelodyToolboxTests(unittest.TestCase):
    def test_nonfinite_values_are_explicitly_null(self):
        self.assertEqual(_json_value([float("nan"), float("inf"), -float("inf")]),
                         [None, None, None])

    def test_real_published_algorithm_produces_features_and_narmour_time_series(self):
        try:
            import melody_features  # noqa: F401
        except ImportError:
            self.skipTest("melody-features==1.3.3 is an optional integration dependency")
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "monophonic.mid"
            path.write_bytes(make_midi(tempo_change=True))
            result = extract_melody_toolbox(path)
        self.assertEqual(result["status"], "features_extracted")
        self.assertEqual(result["candidate_count"], 1)
        self.assertFalse(result["included_original_idyom"])
        self.assertFalse(result["candidates_are_verified_melodies"])
        part = result["parts"][0]
        self.assertEqual(part["notes_count"], 9)
        self.assertGreaterEqual(len(part["features"]), 200)
        self.assertIn("absolute_pitch.pitch_range", part["features"])
        self.assertEqual(len(part["narmour_triplet_realizations"]), 7)
        self.assertAlmostEqual(part["narmour_triplet_realizations"][0]["time_seconds"], 1.5)
        self.assertEqual(len(part["narmour_triplet_realizations"][0]["scores"]), 5)
        self.assertEqual(json.loads(json.dumps(result))["candidate_count"], 1)

    def test_polyphonic_piano_never_becomes_fake_monophonic_melody(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "polyphonic.mid"
            path.write_bytes(make_midi(overlapping=True))
            result = extract_melody_toolbox(path)
        self.assertEqual(result["status"], "no_reliable_monophonic_part")
        self.assertEqual(result["candidate_count"], 0)
        self.assertIn("polyphonic_or_overlapping_notes",
                      result["rejected_parts"][0]["reasons"])


if __name__ == "__main__":
    unittest.main()
