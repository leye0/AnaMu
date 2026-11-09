"""G0 contracts: exact source preservation, no invented musical meaning."""

from __future__ import annotations

import hashlib
import io
import unittest
from fractions import Fraction

import mido

from anamu.grammar_foundation import midi_evidence, midi_evidence_from_file


def _midi(*tracks, ticks_per_beat=480, midi_type=1):
    source = mido.MidiFile(type=midi_type, ticks_per_beat=ticks_per_beat)
    for messages in tracks:
        track = mido.MidiTrack(messages)
        source.tracks.append(track)
    output = io.BytesIO()
    source.save(file=output)
    return output.getvalue()


class MidiEvidenceTests(unittest.TestCase):
    def test_preserves_source_and_all_meta_and_sysex_events(self):
        source = _midi([
            mido.MetaMessage("track_name", name="strings", time=0),
            mido.Message("program_change", channel=2, program=42, time=3),
            mido.Message("sysex", data=[1, 2, 3], time=7),
            mido.MetaMessage("text", text="expression mark", time=0),
            mido.MetaMessage("end_of_track", time=5),
        ])
        evidence = midi_evidence(source)
        self.assertEqual(evidence.raw_bytes, source)
        self.assertEqual(evidence.sha256, hashlib.sha256(source).hexdigest())
        self.assertEqual(evidence.track_count, 1)
        self.assertEqual([e.type for e in evidence.events],
                         ["track_name", "program_change", "sysex", "text", "end_of_track"])
        self.assertEqual([e.tick for e in evidence.events], [0, 3, 10, 10, 15])
        self.assertEqual([e.delta_ticks for e in evidence.events], [0, 3, 7, 0, 5])
        self.assertEqual(evidence.events[2].field("data"), (1, 2, 3))
        self.assertEqual(evidence.events[3].field("text"), "expression mark")
        self.assertEqual(evidence.events[0].id, "t0:e0")
        self.assertIs(evidence.events[0].is_meta, True)

    def test_polyphony_and_simultaneity_are_not_collapsed_to_melody(self):
        source = _midi(
            [mido.Message("note_on", note=60, velocity=75, time=0),
             mido.Message("note_on", note=64, velocity=85, time=0),
             mido.Message("note_off", note=60, velocity=20, time=240),
             mido.Message("note_off", note=64, velocity=30, time=240)],
            [mido.Message("note_on", channel=1, note=67, velocity=93, time=0),
             mido.Message("note_off", channel=1, note=67, time=960)],
        )
        evidence = midi_evidence(source)
        self.assertEqual(len(evidence.notes), 3)
        self.assertEqual([(n.pitch, n.start_tick, n.end_tick) for n in evidence.notes],
                         [(60, 0, 240), (64, 0, 480), (67, 0, 960)])
        self.assertTrue(evidence.notes[0].overlaps(evidence.notes[1]))
        self.assertTrue(evidence.notes[1].overlaps(evidence.notes[2]))
        self.assertEqual(evidence.diagnostics, ())
        self.assertEqual({(n.track, n.channel) for n in evidence.notes},
                         {(0, 0), (1, 1)})
        # Source track is only a tie-breaker, not an inter-track causal claim.
        self.assertEqual([e.tick for e in evidence.events[:3]], [0, 0, 0])

    def test_exact_beats_and_piecewise_tempo_seconds(self):
        source = _midi([
            mido.MetaMessage("set_tempo", tempo=500_000, time=0),
            mido.MetaMessage("set_tempo", tempo=1_000_000, time=480),
        ])
        evidence = midi_evidence(source)
        self.assertEqual(evidence.beat_at_tick(720), Fraction(3, 2))
        self.assertEqual(evidence.seconds_at_tick(0), Fraction(0))
        self.assertEqual(evidence.seconds_at_tick(480), Fraction(1, 2))
        self.assertEqual(evidence.seconds_at_tick(720), Fraction(1))
        self.assertEqual(evidence.seconds_at_tick(960), Fraction(3, 2))
        self.assertEqual([a.tick for a in evidence.tempo_anchors], [0, 480])

    def test_default_tempo_and_time_conversion_invariant_under_tempo_change(self):
        baseline = midi_evidence(_midi([
            mido.Message("note_on", note=60, time=0),
            mido.Message("note_off", note=60, time=480),
        ]))
        slower = midi_evidence(_midi([
            mido.MetaMessage("set_tempo", tempo=1_000_000, time=0),
            mido.Message("note_on", note=60, time=0),
            mido.Message("note_off", note=60, time=480),
        ]))
        self.assertEqual(baseline.beat_at_tick(480), slower.beat_at_tick(480))
        self.assertEqual(baseline.seconds_at_tick(480), Fraction(1, 2))
        self.assertEqual(slower.seconds_at_tick(480), Fraction(1))

    def test_conflicting_simultaneous_tempos_fail_closed(self):
        evidence = midi_evidence(_midi(
            [mido.MetaMessage("set_tempo", tempo=500_000, time=0)],
            [mido.MetaMessage("set_tempo", tempo=750_000, time=0)],
        ))
        self.assertEqual(len(evidence.events_of_type("set_tempo")), 2)
        self.assertIn("conflicting_tempo_at_tick", [d.code for d in evidence.diagnostics])
        self.assertEqual(evidence.beat_at_tick(480), Fraction(1))
        with self.assertRaisesRegex(ValueError, "ambiguous_or_invalid_tempo_map"):
            evidence.seconds_at_tick(480)

    def test_same_tempo_repeated_is_not_ambiguous(self):
        evidence = midi_evidence(_midi(
            [mido.MetaMessage("set_tempo", tempo=750_000, time=0)],
            [mido.MetaMessage("set_tempo", tempo=750_000, time=0)],
        ))
        self.assertEqual(evidence.seconds_at_tick(480), Fraction(3, 4))
        self.assertEqual(evidence.diagnostics, ())

    def test_sequential_same_track_tempo_changes_are_not_conflicts(self):
        evidence = midi_evidence(_midi([
            mido.MetaMessage("set_tempo", tempo=650_000, time=0),
            mido.MetaMessage("set_tempo", tempo=900_000, time=0),
        ]))
        self.assertEqual(len(evidence.events_of_type("set_tempo")), 2)
        self.assertEqual(evidence.seconds_at_tick(480), Fraction(9, 10))
        self.assertEqual(evidence.diagnostics, ())

    def test_velocity_zero_note_on_is_key_release(self):
        evidence = midi_evidence(_midi([
            mido.Message("note_on", note=62, velocity=111, time=48),
            mido.Message("note_on", note=62, velocity=0, time=96),
        ]))
        self.assertEqual(len(evidence.notes), 1)
        span = evidence.notes[0]
        self.assertEqual((span.velocity, span.release_velocity), (111, 0))
        self.assertEqual((span.start_tick, span.end_tick), (48, 144))
        self.assertEqual((span.onset_event_id, span.release_event_id),
                         ("t0:e0", "t0:e1"))

    def test_pedal_expression_and_program_are_sources_not_acoustics(self):
        evidence = midi_evidence(_midi([
            mido.Message("program_change", program=89, time=0),
            mido.Message("control_change", control=7, value=40, time=0),
            mido.Message("control_change", control=11, value=64, time=0),
            mido.Message("control_change", control=64, value=127, time=0),
            mido.Message("note_on", note=60, velocity=100, time=0),
            mido.Message("note_off", note=60, time=240),
            mido.Message("control_change", control=64, value=0, time=240),
        ]))
        self.assertEqual(len(evidence.events_of_type("control_change")), 4)
        self.assertEqual(evidence.notes[0].end_tick, 240)
        self.assertEqual(evidence.events_of_type("program_change")[0].field("program"), 89)
        self.assertEqual(evidence.summary()["audio_loudness"], None)
        self.assertEqual(evidence.summary()["sounding_end_after_pedal"], None)
        self.assertEqual(evidence.summary()["inferred_instrument"], None)

    def test_same_pitch_retrigger_and_ambiguous_release_never_guessed(self):
        evidence = midi_evidence(_midi([
            mido.Message("note_on", note=60, time=0),
            mido.Message("note_on", note=60, time=120),
            mido.Message("note_off", note=60, time=120),
        ]))
        self.assertEqual(evidence.notes, ())
        codes = [d.code for d in evidence.diagnostics]
        self.assertIn("same_pitch_retrigger_ambiguous", codes)
        self.assertIn("ambiguous_key_release", codes)
        self.assertEqual(codes.count("unclosed_key_press"), 2)

    def test_unmatched_release_and_unclosed_press_reported(self):
        evidence = midi_evidence(_midi([
            mido.Message("note_off", note=60, time=0),
            mido.Message("note_on", note=61, time=20),
        ]))
        self.assertEqual(evidence.notes, ())
        self.assertEqual([d.code for d in evidence.diagnostics],
                         ["unmatched_key_release", "unclosed_key_press"])

    def test_zero_length_span_explicitly_reported(self):
        evidence = midi_evidence(_midi([
            mido.Message("note_on", note=60, time=0),
            mido.Message("note_off", note=60, time=0),
        ]))
        self.assertEqual(len(evidence.notes), 1)
        self.assertEqual(evidence.notes[0].start_tick, evidence.notes[0].end_tick)
        self.assertFalse(evidence.notes[0].overlaps(evidence.notes[0]))
        self.assertIn("zero_duration_key_span", [d.code for d in evidence.diagnostics])

    def test_separate_channels_allow_same_pitch_to_overlap(self):
        evidence = midi_evidence(_midi([
            mido.Message("note_on", channel=0, note=60, time=0),
            mido.Message("note_on", channel=1, note=60, time=0),
            mido.Message("note_off", channel=1, note=60, time=120),
            mido.Message("note_off", channel=0, note=60, time=120),
        ]))
        self.assertEqual(len(evidence.notes), 2)
        self.assertTrue(evidence.notes[0].overlaps(evidence.notes[1]))

    def test_format_two_independent_tracks_rejected(self):
        with self.assertRaisesRegex(ValueError, "unrelated_format_two"):
            midi_evidence(_midi([mido.MetaMessage("end_of_track")], midi_type=2))

    def test_smpte_division_retains_raw_ticks_without_inventing_beats(self):
        source = bytearray(_midi([
            mido.Message("note_on", note=60, time=20),
            mido.Message("note_off", note=60, time=40),
        ]))
        # SMF header time-division: -25 frames/second, 40 ticks/frame.
        # The generic mido reader exposes a signed division, not PPQ beats.
        source[12:14] = b"\xe7\x28"
        evidence = midi_evidence(source)
        self.assertEqual(evidence.timebase, "smpte")
        self.assertEqual(evidence.notes[0].start_tick, 20)
        self.assertEqual(evidence.notes[0].end_tick, 60)
        with self.assertRaisesRegex(ValueError, "musical_beat_unknown"):
            evidence.beat_at_tick(40)
        with self.assertRaisesRegex(ValueError, "seconds_conversion_unsupported"):
            evidence.seconds_at_tick(40)

    def test_invalid_negative_tick_lookup_rejected(self):
        evidence = midi_evidence(_midi([mido.MetaMessage("end_of_track")]))
        with self.assertRaisesRegex(ValueError, "negative_midi_tick"):
            evidence.beat_at_tick(-1)
        with self.assertRaisesRegex(ValueError, "negative_midi_tick"):
            evidence.seconds_at_tick(-1)


if __name__ == "__main__":
    unittest.main()
