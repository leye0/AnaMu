"""G2 invariants for exact, source-backed motif hypotheses (not human themes)."""

from __future__ import annotations

import io
import unittest
from fractions import Fraction

import mido

from anamu.grammar_foundation import midi_evidence, midi_evidence_from_file
from anamu.grammar_motifs import discover_exact_motifs


def _fixture(strands):
    """Each strand: (channel, [(absolute_onset, pitch, duration), ...])."""
    midi = mido.MidiFile(type=1, ticks_per_beat=480)
    for channel, notes in strands:
        events = []
        for onset, pitch, duration in notes:
            # Zero-length keypress explicitly orders onset before release.
            events.extend(((onset, -1 if duration == 0 else 1, 1, pitch),
                           (onset + duration, 0, 0, pitch)))
        track = mido.MidiTrack()
        midi.tracks.append(track)
        previous = 0
        for tick, _, kind, pitch in sorted(events):
            track.append(mido.Message("note_on" if kind else "note_off",
                                      channel=channel, note=pitch,
                                      velocity=80 if kind else 0, time=tick - previous))
            previous = tick
    stream = io.BytesIO()
    midi.save(file=stream)
    return midi_evidence(stream.getvalue())


class ExactMotifDiscoveryTests(unittest.TestCase):
    def test_real_orchestral_corpus_is_bounded_and_source_backed(self):
        from pathlib import Path
        corpus = Path(__file__).resolve().parents[1] / "data/orchestral"
        for name in ("beethoven5-movement1.mid", "beethoven7-movement2.mid"):
            with self.subTest(name=name):
                evidence = midi_evidence_from_file(corpus / name)
                found = discover_exact_motifs(evidence)
                self.assertGreater(found.windows_examined, 0)
                self.assertGreater(len(found.candidates), 0)
                self.assertEqual(found.source_sha256, evidence.sha256)
                self.assertTrue(all(c.source_sha256 == evidence.sha256
                                    for c in found.candidates))

    def test_transposition_and_augmentation_have_explicit_g1_proofs(self):
        first = [(0, 60, 80), (120, 64, 80), (240, 67, 160)]
        transposed = [(480, 65, 80), (600, 69, 80), (720, 72, 160)]
        augmented = [(1200, 72, 160), (1440, 76, 160), (1680, 79, 320)]
        evidence = _fixture([(0, first + transposed + augmented)])
        discovered = discover_exact_motifs(evidence, min_onsets=3, max_onsets=3)
        matches = [candidate for candidate in discovered.candidates
                   if candidate.note_count == 3 and len(candidate.occurrences) == 3]
        self.assertEqual(len(matches), 1)
        candidate = matches[0]
        self.assertEqual(candidate.operator, "GROUP")
        self.assertEqual(candidate.status, "structural_candidate")
        self.assertEqual(candidate.source_sha256, evidence.sha256)
        self.assertEqual([o.start_tick for o in candidate.occurrences], [0, 480, 1200])
        self.assertEqual([t.transposition_semitones for t in candidate.transforms_from_first],
                         [5, 12])
        self.assertEqual([t.time_scale for t in candidate.transforms_from_first],
                         [Fraction(1), Fraction(2)])
        self.assertTrue(all(t.source_event_ids for t in candidate.transforms_from_first))

    def test_polyphonic_onset_groups_preserve_chords_in_same_midi_strand(self):
        notes = [(0, 60, 100), (0, 64, 100),
                 (240, 62, 100), (240, 65, 100),
                 (720, 65, 100), (720, 69, 100),
                 (960, 67, 100), (960, 70, 100)]
        evidence = _fixture([(0, notes)])
        discovered = discover_exact_motifs(evidence, min_onsets=2, max_onsets=2)
        matches = [c for c in discovered.candidates if c.note_count == 4]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].transforms_from_first[0].transposition_semitones, 5)
        self.assertEqual(matches[0].onset_count, 2)
        self.assertEqual([len(o.notes) for o in matches[0].occurrences], [4, 4])

    def test_cross_track_matches_do_not_infer_voice_identity(self):
        first = [(0, 60, 70), (120, 64, 70), (240, 67, 70)]
        second = [(720, 72, 70), (840, 76, 70), (960, 79, 70)]
        evidence = _fixture([(0, first), (0, second)])
        matches = discover_exact_motifs(evidence, max_onsets=3).candidates
        self.assertEqual(len(matches), 1)
        self.assertEqual([o.track for o in matches[0].occurrences], [0, 1])
        self.assertEqual(matches[0].status, "structural_candidate")

    def test_inversion_and_local_rhythm_change_do_not_match(self):
        first = [(0, 60, 80), (120, 64, 80), (240, 67, 80)]
        inversion = [(600, 72, 80), (720, 68, 80), (840, 65, 80)]
        changed_rhythm = [(1200, 60, 80), (1350, 64, 80), (1440, 67, 80)]
        evidence = _fixture([(0, first + inversion + changed_rhythm)])
        self.assertFalse(discover_exact_motifs(evidence, max_onsets=3).candidates)

    def test_simultaneous_duplicate_is_not_repeated_in_time(self):
        notes = [(0, 60, 80), (120, 64, 80), (240, 67, 80)]
        evidence = _fixture([(0, notes), (1, notes)])
        self.assertFalse(discover_exact_motifs(evidence, max_onsets=3).candidates)

    def test_percussion_and_zero_length_keypress_are_explicitly_excluded(self):
        regular = [(0, 60, 70), (120, 64, 70), (240, 67, 70),
                   (600, 72, 70), (720, 76, 70), (840, 79, 70),
                   (1000, 65, 0)]
        drum = [(0, 36, 80), (120, 38, 80), (240, 42, 80)]
        evidence = _fixture([(0, regular), (9, drum)])
        found = discover_exact_motifs(evidence, max_onsets=3)
        self.assertEqual(found.percussion_notes_excluded, 3)
        self.assertEqual(found.nonpositive_notes_excluded, 1)
        self.assertEqual(found.strands_examined, 1)
        self.assertTrue(found.candidates)

    def test_bounded_search_fails_explicitly(self):
        notes = [(i * 120, 60 + i, 70) for i in range(10)]
        evidence = _fixture([(0, notes)])
        with self.assertRaisesRegex(ValueError, "motif_window_budget_exceeded"):
            discover_exact_motifs(evidence, max_windows=1)
        with self.assertRaisesRegex(ValueError, "motif_onset_range_invalid"):
            discover_exact_motifs(evidence, min_onsets=1)


if __name__ == "__main__":
    unittest.main()
