"""Academic G1 interval-algebra and transparent transform contracts."""

from __future__ import annotations

import io
import unittest
from fractions import Fraction

import mido

from anamu.grammar_foundation import midi_evidence
from anamu.grammar_relations import (
    AllenRelation, NoteRelationIndex, compare_note_spans, exact_pattern_transform,
    interval_relation,
)


def _from_messages(messages, *, division=480):
    midi = mido.MidiFile(type=0, ticks_per_beat=division)
    midi.tracks.append(mido.MidiTrack(messages))
    stream = io.BytesIO()
    midi.save(file=stream)
    return midi_evidence(stream.getvalue())


class AllenRelationTests(unittest.TestCase):
    def test_all_thirteen_interval_relations(self):
        cases = [
            ((0, 2), (3, 5), "before"),
            ((0, 2), (2, 5), "meets"),
            ((0, 3), (2, 5), "overlaps"),
            ((0, 2), (0, 5), "starts"),
            ((2, 3), (0, 5), "during"),
            ((2, 5), (0, 5), "finishes"),
            ((0, 5), (0, 5), "equals"),
            ((3, 5), (0, 2), "after"),
            ((2, 5), (0, 2), "met_by"),
            ((2, 5), (0, 3), "overlapped_by"),
            ((0, 5), (0, 2), "started_by"),
            ((0, 5), (2, 3), "contains"),
            ((0, 5), (2, 5), "finished_by"),
        ]
        self.assertEqual(len(cases), 13)
        for (a0, a1), (b0, b1), expected in cases:
            with self.subTest(expected=expected):
                self.assertEqual(interval_relation(a0, a1, b0, b1).value, expected)

    def test_all_possible_strict_intervals_have_one_relation(self):
        # Exhaustive small-domain partition property, not example-only tests.
        domain = [(a, b) for a in range(6) for b in range(a + 1, 7)]
        for a0, a1 in domain:
            for b0, b1 in domain:
                self.assertIsInstance(interval_relation(a0, a1, b0, b1), AllenRelation)

    def test_reverse_relation_is_the_expected_inverse(self):
        inverse = {
            "before": "after", "meets": "met_by",
            "overlaps": "overlapped_by", "starts": "started_by",
            "during": "contains", "finishes": "finished_by",
            "equals": "equals",
        }
        for value, reverse in list(inverse.items()):
            inverse[reverse] = value
        domain = [(a, b) for a in range(5) for b in range(a + 1, 6)]
        for a0, a1 in domain:
            for b0, b1 in domain:
                forward = interval_relation(a0, a1, b0, b1).value
                backward = interval_relation(b0, b1, a0, a1).value
                self.assertEqual(backward, inverse[forward])

    def test_translation_and_positive_scaling_leave_relation_invariant(self):
        for a0, a1, b0, b1 in [(0, 4, 0, 4), (0, 2, 2, 8),
                                (3, 8, 1, 6), (2, 4, 0, 8), (0, 5, 3, 7)]:
            baseline = interval_relation(a0, a1, b0, b1)
            transformed = interval_relation(3 * a0 + 40, 3 * a1 + 40,
                                            3 * b0 + 40, 3 * b1 + 40)
            self.assertEqual(baseline, transformed)

    def test_zero_length_and_negative_intervals_refused(self):
        for invalid in [(0, 0), (10, 1), (-1, 5)]:
            with self.subTest(invalid=invalid):
                with self.assertRaisesRegex(ValueError, "positive_length"):
                    interval_relation(*invalid, 0, 5)


class MidiG1RelationsTests(unittest.TestCase):
    def test_polyphony_relation_preserves_partial_overlap(self):
        # Type 0 two key presses with partial overlap.
        evidence = _from_messages([
            mido.Message("note_on", note=60, time=0),
            mido.Message("note_on", note=67, time=120),
            mido.Message("note_off", note=60, time=120),
            mido.Message("note_off", note=67, time=120),
        ])
        a, b = evidence.notes
        relation = compare_note_spans(evidence, a, b)
        self.assertEqual(relation.operator, "PARALLEL")
        self.assertEqual(relation.allen_relation, AllenRelation.OVERLAPS)
        self.assertEqual(relation.start_delta_ticks, 120)
        self.assertEqual(relation.start_delta_beats, Fraction(1, 4))
        self.assertEqual(relation.overlap_ticks, 120)
        self.assertEqual(relation.pitch_delta_semitones, 7)
        self.assertEqual(len(relation.source_event_ids), 4)
        self.assertEqual(relation.source_sha256, evidence.sha256)

    def test_note_relation_index_supports_fast_source_id_queries(self):
        evidence = _from_messages([
            mido.Message("note_on", note=60, time=0),
            mido.Message("note_on", note=64, time=0),
            mido.Message("note_off", note=60, time=240),
            mido.Message("note_off", note=64, time=0),
        ])
        index = NoteRelationIndex(evidence)
        result = index.compare(evidence.notes[0].onset_event_id,
                               evidence.notes[1].onset_event_id)
        self.assertEqual(result.allen_relation, AllenRelation.EQUALS)
        self.assertEqual(result.operator, "PARALLEL")
        with self.assertRaisesRegex(ValueError, "unknown_note_onset_id"):
            index.compare("not-in-source", evidence.notes[0].onset_event_id)

    def test_sequence_meeting_is_not_simultaneity(self):
        evidence = _from_messages([
            mido.Message("note_on", note=60, time=0),
            mido.Message("note_off", note=60, time=240),
            mido.Message("note_on", note=62, time=0),
            mido.Message("note_off", note=62, time=240),
        ])
        relation = compare_note_spans(evidence, *evidence.notes)
        self.assertEqual(relation.operator, "SEQUENCE")
        self.assertEqual(relation.allen_relation, AllenRelation.MEETS)
        self.assertEqual(relation.overlap_ticks, 0)

    def test_channel_ten_percussion_has_no_tonal_semitone_claim(self):
        evidence = _from_messages([
            mido.Message("note_on", channel=9, note=36, time=0),
            mido.Message("note_on", channel=0, note=60, time=0),
            mido.Message("note_off", channel=9, note=36, time=240),
            mido.Message("note_off", channel=0, note=60, time=0),
        ])
        relation = compare_note_spans(evidence, *evidence.notes)
        self.assertIsNone(relation.pitch_delta_semitones)
        self.assertEqual(relation.operator, "PARALLEL")

    def test_relation_rejects_self_comparison(self):
        evidence = _from_messages([
            mido.Message("note_on", note=60),
            mido.Message("note_off", note=60, time=240),
        ])
        with self.assertRaisesRegex(ValueError, "self_relation"):
            compare_note_spans(evidence, evidence.notes[0], evidence.notes[0])

    def test_rejects_zero_duration_key_span_without_fabricating_relation(self):
        evidence = _from_messages([
            mido.Message("note_on", note=60),
            mido.Message("note_off", note=60),
            mido.Message("note_on", note=62, time=120),
            mido.Message("note_off", note=62, time=120),
        ])
        with self.assertRaisesRegex(ValueError, "positive_length"):
            compare_note_spans(evidence, *evidence.notes)

    @staticmethod
    def _example_motif():
        return _from_messages([
            mido.Message("note_on", note=60, time=0),
            mido.Message("note_off", note=60, time=120),
            mido.Message("note_on", note=62, time=120),
            mido.Message("note_off", note=62, time=120),
            mido.Message("note_on", note=67, time=120),
            mido.Message("note_off", note=67, time=240),
            mido.Message("note_on", note=69, time=240),
            mido.Message("note_off", note=69, time=240),
        ])

    def test_exact_transposition_and_augmentation_from_explicit_matching(self):
        evidence = self._example_motif()
        motif = exact_pattern_transform(evidence, evidence.notes[:2], evidence.notes[2:])
        self.assertIsNotNone(motif)
        self.assertEqual(motif.operator, "TRANSFORM")
        self.assertEqual(motif.transposition_semitones, 7)
        self.assertEqual(motif.time_scale, Fraction(2))
        self.assertEqual(motif.temporal_shift_ticks, 480)
        self.assertEqual(len(motif.source_event_ids), 8)

    def test_pitch_or_rhythm_change_fails_exact_transform(self):
        evidence = self._example_motif()
        notes = evidence.notes
        self.assertIsNone(exact_pattern_transform(evidence, notes[:2],
                                                  (notes[2], notes[1])))

    def test_exact_transform_requires_correspondence_not_auto_detection(self):
        evidence = self._example_motif()
        with self.assertRaisesRegex(ValueError, "at_least_two"):
            exact_pattern_transform(evidence, evidence.notes[:1], evidence.notes[2:3])
        with self.assertRaisesRegex(ValueError, "duplicate_source"):
            exact_pattern_transform(evidence, (evidence.notes[0], evidence.notes[0]),
                                    evidence.notes[2:4])


if __name__ == "__main__":
    unittest.main()
