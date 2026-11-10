"""Exact part-to-part voice-leading and reversible-looking what-if proposals."""

from __future__ import annotations

import unittest
from pathlib import Path

from anamu.orchestral_voice_leading import (
    propose_voice_motion_edit, score_voice_leading,
)
from anamu.score_texture import score_texture_from_mxl
from tests.test_score_texture import _note, _score


def _pair(a, b, *, transpose=""):
    return score_texture_from_mxl(_score([
        ("P1", "Violin", "", [a]),
        ("P2", "Clarinet", transpose, [b]),
    ]))


class ScoreVoiceLeadingTests(unittest.TestCase):
    def test_contrary_parallel_similar_oblique_and_static(self):
        examples = [
            ("contrary", [_note("G", 5), _note("F", 5), _note("E", 5)]),
            ("parallel", [_note("G", 4), _note("A", 4), _note("B", 4)]),
            ("similar", [_note("G", 4), _note("B", 4), _note("C", 5)]),
            ("oblique", [_note("G", 4)] * 3),
        ]
        upper = _note("C", 4) + _note("D", 4) + _note("E", 4)
        for expected, b in examples:
            with self.subTest(motion=expected):
                obs = score_voice_leading(_pair(upper, "".join(b)))
                self.assertEqual(len(obs), 2)
                self.assertEqual(obs[0].motion_type, expected)
                self.assertEqual(obs[0].source_sha256,
                                 _pair(upper, "".join(b)).source_sha256)
        both_static = _pair(_note("C", 4) * 3, _note("G", 4) * 3)
        self.assertEqual({o.motion_type for o in score_voice_leading(both_static)},
                         {"static"})

    def test_parallel_fifths_and_octaves_are_observations_not_errors(self):
        c_d_e = _note("C", 4) + _note("D", 4) + _note("E", 4)
        perfect_fifths = _pair(c_d_e, _note("G", 4) + _note("A", 4) + _note("B", 4))
        fifths = score_voice_leading(perfect_fifths)
        self.assertTrue(all(o.parallel_perfect_class == "fifth" for o in fifths))
        perfect_octaves = _pair(c_d_e, _note("C", 5) + _note("D", 5) + _note("E", 5))
        octaves = score_voice_leading(perfect_octaves)
        self.assertTrue(all(o.parallel_perfect_class == "unison_or_octave"
                            for o in octaves))
        self.assertTrue(all(o.status == "exact_two_part_notation_observation"
                            for o in fifths + octaves))

    def test_transposing_instrument_compared_at_concert_pitch(self):
        violin = _note("C", 4) + _note("D", 4)
        clarinet = _note("D", 5) + _note("E", 5)
        score = _pair(violin, clarinet,
                      transpose="<transpose><chromatic>-2</chromatic></transpose>")
        observations = score_voice_leading(score)
        self.assertEqual(len(observations), 1)
        self.assertEqual(observations[0].pitches, (60, 62, 72, 74))
        self.assertEqual(observations[0].interval_before, 12)

    def test_voice_crossing_and_contact_not_conflated(self):
        cross = _pair(_note("C", 4) + _note("E", 4),
                      _note("E", 4) + _note("C", 4))
        self.assertTrue(score_voice_leading(cross)[0].crossing)
        touch = _pair(_note("C", 4) + _note("E", 4),
                      _note("G", 4) + _note("E", 4))
        self.assertFalse(score_voice_leading(touch)[0].crossing)

    def test_chords_and_tied_fragments_break_pairwise_proofs(self):
        source = _note("C", 4) + _note("D", 4) + _note("E", 4)
        chord = (_note("G", 4) + _note("A", 4)
                 + _note("E", 5, extra="<chord/>") + _note("B", 4))
        tied = (_note("G", 4) + _note("A", 4, extra='<tie type="start"/>')
                + _note("B", 4))
        self.assertFalse(score_voice_leading(_pair(source, chord)))
        self.assertFalse(score_voice_leading(_pair(source, tied)))

    def test_different_notated_voices_and_distant_measures_do_not_fake_line(self):
        second_voice = _note("D", 4).replace("<voice>1</voice>", "<voice>2</voice>")
        evidence = _pair(_note("C", 4) + second_voice,
                         _note("G", 4) + _note("A", 4))
        self.assertFalse(score_voice_leading(evidence))
        distant = score_texture_from_mxl(_score([
            ("P1", "Violin", "", [_note("C", 4), "", _note("D", 4)]),
            ("P2", "Flute", "", [_note("G", 4), "", _note("A", 4)]),
        ], measure_names=("1", "2", "3")))
        self.assertFalse(score_voice_leading(distant))

    def test_counterfactual_changes_only_b1_and_is_not_a_quality_label(self):
        score = _pair(_note("C", 4) + _note("D", 4),
                      _note("G", 4) + _note("F", 4))
        observed = score_voice_leading(score)[0]
        self.assertEqual(observed.motion_type, "contrary")
        parallel = propose_voice_motion_edit(observed, "parallel")
        self.assertEqual(parallel.proposed_sounding_pitch, 69)
        self.assertEqual(parallel.resulting_motion_type, "parallel")
        self.assertEqual(parallel.causes_parallel_perfect, "fifth")
        self.assertEqual(parallel.target_note_id, observed.source_note_ids[3])
        self.assertEqual(parallel.status,
                         "counterfactual_note_edit_not_validated_arrangement")
        oblique = propose_voice_motion_edit(observed, "oblique")
        self.assertEqual(oblique.proposed_sounding_pitch, 67)
        self.assertEqual(oblique.resulting_motion_type, "oblique")
        # Source evidence remains immutable: no mutation of any score note.
        self.assertEqual(score_voice_leading(score)[0], observed)
        with self.assertRaisesRegex(ValueError, "unsupported_motion_edit"):
            propose_voice_motion_edit(observed, "good_music")

    def test_real_beethoven_part_pairs_are_bounded_and_source_backed(self):
        root = Path(__file__).resolve().parents[1] / "data/orchestral"
        for filename in ("hauptstimme-beethoven5-movement1.mxl",
                         "hauptstimme-beethoven7-movement2.mxl"):
            with self.subTest(filename=filename):
                evidence = score_texture_from_mxl((root / filename).read_bytes())
                observed = score_voice_leading(evidence)
                self.assertGreater(len(observed), 1000)
                self.assertTrue(any(o.motion_type == "contrary" for o in observed))
                by_id = {n.source_note_id: n for n in evidence.notes}
                for motion in observed[:30]:
                    self.assertEqual(motion.source_sha256, evidence.source_sha256)
                    a0, a1, b0, b1 = [by_id[x] for x in motion.source_note_ids]
                    self.assertEqual((a0.measure_index, a0.onset_quarters),
                                     (b0.measure_index, b0.onset_quarters))
                    self.assertEqual((a1.measure_index, a1.onset_quarters),
                                     (b1.measure_index, b1.onset_quarters))
                    self.assertEqual(a1.sounding_midi_pitch - a0.sounding_midi_pitch,
                                     motion.motion_a)


if __name__ == "__main__":
    unittest.main()
