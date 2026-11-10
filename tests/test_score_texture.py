"""MusicXML orchestral writing facts: transposition, voices, exact doubling."""

from __future__ import annotations

import io
import unittest
import zipfile
from fractions import Fraction
from pathlib import Path

from anamu.score_texture import score_texture_from_mxl, discover_exact_octave_doublings


def _note(step, octave, duration=4, *, alter=0, extra=""):
    pitch = (f"<pitch><step>{step}</step><alter>{alter}</alter>"
             f"<octave>{octave}</octave></pitch>")
    return f"<note>{extra}{pitch}<duration>{duration}</duration><voice>1</voice></note>"


def _score(parts, *, measure_names=("1",)):
    """parts: [(id, label, transpose_xml, [measure body, ...])]."""
    part_list = "".join(f'<score-part id="{id}"><part-name>{label}</part-name></score-part>'
                        for id, label, _, _ in parts)
    bodies = []
    for id, _, transpose, measures in parts:
        ms = "".join(f'<measure number="{measure_names[i]}">'
                     + (f"<attributes><divisions>4</divisions>{transpose}</attributes>"
                        if i == 0 else "") + body + "</measure>"
                     for i, body in enumerate(measures))
        bodies.append(f'<part id="{id}">{ms}</part>')
    xml = (f'<score-partwise version="4.0"><part-list>{part_list}</part-list>'
           f'{"".join(bodies)}</score-partwise>').encode("utf-8")
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("score.xml", xml)
    return stream.getvalue()


class ScoreOrchestrationEvidenceTests(unittest.TestCase):
    def test_written_transposing_instrument_becomes_exact_sounding_octave(self):
        flute = (_note("C", 4) + _note("E", 4) + _note("G", 4))
        clarinet = (_note("D", 5) + _note("F", 5, alter=1) + _note("A", 5))
        mxl = _score([
            ("P1", "Flute", "", [flute]),
            ("P2", "Clarinet", "<transpose><chromatic>-2</chromatic></transpose>",
             [clarinet]),
        ])
        evidence = score_texture_from_mxl(mxl)
        self.assertEqual(len(evidence.notes), 6)
        self.assertEqual(evidence.notes[0].sounding_midi_pitch, 60)
        self.assertEqual(evidence.notes[3].written_midi_pitch, 74)
        self.assertEqual(evidence.notes[3].sounding_midi_pitch, 72)
        candidates = discover_exact_octave_doublings(evidence)
        self.assertEqual(len(candidates), 1)
        match = candidates[0]
        self.assertEqual((match.part_a, match.part_b), ("P1", "P2"))
        self.assertEqual(match.octave_offset, 1)
        self.assertEqual(len(match.source_note_pairs), 3)
        self.assertEqual(match.status, "exact_notational_doubling_candidate")
        self.assertEqual(match.source_sha256, evidence.source_sha256)

    def test_local_rhythm_and_pitch_mismatch_refuse_doubling(self):
        first = _note("C", 4) + _note("D", 4) + _note("E", 4)
        changed_duration = _note("C", 5) + _note("D", 5, duration=2) + _note("E", 5)
        pitch_mismatch = _note("C", 5) + _note("F", 5) + _note("E", 5)
        for second in (changed_duration, pitch_mismatch):
            with self.subTest(second=second):
                evidence = score_texture_from_mxl(_score([
                    ("P1", "Violin", "", [first]),
                    ("P2", "Violin", "", [second]),
                ]))
                self.assertFalse(discover_exact_octave_doublings(evidence))

    def test_polyphonic_chord_and_tie_are_not_hidden_as_melody(self):
        anchor = _note("C", 4) + _note("D", 4) + _note("E", 4)
        chord = (_note("C", 5) +
                 _note("G", 5, extra="<chord/>") +
                 _note("D", 5) + _note("E", 5))
        tied = (_note("C", 5) +
                _note("D", 5, extra='<tie type="start"/>') +
                _note("E", 5))
        for second in (chord, tied):
            with self.subTest(second=second):
                evidence = score_texture_from_mxl(_score([
                    ("P1", "Violin", "", [anchor]),
                    ("P2", "Flute", "", [second]),
                ]))
                self.assertFalse(discover_exact_octave_doublings(evidence))
                if second == tied:
                    self.assertEqual(sum(n.tied for n in evidence.notes), 1)

    def test_backup_and_forward_preserve_polyphonic_onset(self):
        # Multiple voices have separate cursor positions, even within one part.
        poly = (_note("C", 4) + _note("D", 4)
                + "<backup><duration>8</duration></backup>"
                + _note("G", 3, duration=8)
                + "<forward><duration>4</duration></forward>")
        evidence = score_texture_from_mxl(_score([("P1", "Violin", "", [poly])]))
        self.assertEqual([n.onset_quarters for n in evidence.notes],
                         [Fraction(0), Fraction(1), Fraction(0)])
        self.assertEqual([n.duration_quarters for n in evidence.notes],
                         [Fraction(1), Fraction(1), Fraction(2)])

    def test_grace_notes_are_reported_without_fake_duration(self):
        main = _note("C", 4)
        with_grace = ('<note><grace/><pitch><step>D</step><octave>4</octave></pitch></note>'
                      '<note><grace/><chord/><pitch><step>F</step>'
                      '<octave>4</octave></pitch></note>'
                      + main)
        evidence = score_texture_from_mxl(_score([("P1", "Flute", "", [with_grace])]))
        self.assertEqual(evidence.grace_notes_excluded, 2)
        self.assertEqual(len(evidence.notes), 1)

    def test_cue_notes_are_excluded_without_losing_measure_time(self):
        cue = _note("G", 4, extra="<cue/>")
        evidence = score_texture_from_mxl(_score([
            ("P1", "Flute", "", [cue + _note("C", 5)])
        ]))
        self.assertEqual(evidence.cue_notes_excluded, 1)
        self.assertEqual(len(evidence.notes), 1)
        self.assertEqual(evidence.notes[0].onset_quarters, Fraction(1))

    def test_score_measure_number_is_preserved_not_reinterpreted_as_time(self):
        content = _note("C", 4) + _note("D", 4)
        evidence = score_texture_from_mxl(_score([
            ("P1", "Flute", "", [content, content])
        ], measure_names=("0", "7")))
        self.assertEqual([(n.measure_index, n.measure_number)
                          for n in evidence.notes],
                         [(0, "0"), (0, "0"), (1, "7"), (1, "7")])

    def test_microtonal_pitch_must_not_be_rounded(self):
        microtone = _note("C", 4, alter="0.5")
        with self.assertRaisesRegex(ValueError, "microtonal_musicxml_pitch_not_supported"):
            score_texture_from_mxl(_score([("P1", "Violin", "", [microtone])]))

    def test_staff_specific_transposition_must_not_be_silently_generalized(self):
        transpose = '<transpose number="1"><chromatic>-2</chromatic></transpose>'
        with self.assertRaisesRegex(ValueError, "staff_specific_transpose_not_supported"):
            score_texture_from_mxl(_score([
                ("P1", "Clarinet", transpose, [_note("C", 4)])
            ]))

    def test_both_beethoven_scores_yield_source_backed_orchestral_candidates(self):
        root = Path(__file__).resolve().parents[1] / "data/orchestral"
        for filename in ("hauptstimme-beethoven5-movement1.mxl",
                         "hauptstimme-beethoven7-movement2.mxl"):
            with self.subTest(filename=filename):
                evidence = score_texture_from_mxl((root / filename).read_bytes())
                candidates = discover_exact_octave_doublings(evidence)
                self.assertGreater(len(evidence.notes), 5000)
                self.assertGreater(len(candidates), 0)
                by_id = {n.source_note_id: n for n in evidence.notes}
                for candidate in candidates[:20]:
                    self.assertEqual(candidate.source_sha256, evidence.source_sha256)
                    self.assertGreaterEqual(len(candidate.source_note_pairs), 3)
                    for id_a, id_b in candidate.source_note_pairs:
                        a, b = by_id[id_a], by_id[id_b]
                        self.assertEqual(a.measure_index, b.measure_index)
                        self.assertEqual(a.onset_quarters, b.onset_quarters)
                        self.assertEqual(a.duration_quarters, b.duration_quarters)
                        self.assertEqual(b.sounding_midi_pitch - a.sounding_midi_pitch,
                                         12 * candidate.octave_offset)


if __name__ == "__main__":
    unittest.main()
