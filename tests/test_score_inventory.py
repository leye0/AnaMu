"""Evidence-based MusicXML inventory and source-label mismatch tests."""

import io
import unittest
import zipfile
from pathlib import Path

import mido

from anamu.grammar_foundation import midi_evidence
from anamu.score_inventory import (compare_score_to_midi, instrument_family,
                                   score_part_inventory)
from scripts.score_midi_orchestration_audit import run


class MusicXmlInventoryTests(unittest.TestCase):
    def test_distinguishes_english_horn_from_horn(self):
        self.assertEqual(instrument_family("english horn"), "english_horn")
        self.assertEqual(instrument_family("Horn in E♭"), "horn")
        self.assertEqual(instrument_family("B♭ Clarinet"), "clarinet")
        self.assertEqual(instrument_family("Violoncello"), "cello")

    def test_score_metadata_is_not_sound_or_aligned_midi(self):
        musicxml = b'''<?xml version="1.0"?>
<score-partwise version="4.0"><part-list>
  <score-part id="P1"><part-name>Horn in E</part-name>
    <score-instrument id="i1"><instrument-name>Horn</instrument-name></score-instrument>
  </score-part></part-list><part id="P1"><measure number="1">
    <note><pitch><step>C</step><octave>4</octave></pitch><duration>1</duration></note>
    <note><rest/><duration>1</duration></note>
  </measure></part></score-partwise>'''
        content = io.BytesIO()
        with zipfile.ZipFile(content, "w", compression=zipfile.ZIP_DEFLATED) as z:
            z.writestr("score.xml", musicxml)
        score = score_part_inventory(content.getvalue())
        self.assertEqual(score["score_part_count"], 1)
        self.assertEqual(score["pitched_note_elements"], 1)
        self.assertEqual(score["score_parts"][0]["declared_family"], "horn")

        midi = mido.MidiFile(ticks_per_beat=480)
        track = mido.MidiTrack()
        track.append(mido.MetaMessage("instrument_name", name="english horn"))
        track.append(mido.Message("note_on", note=60, velocity=72, time=0))
        track.append(mido.Message("note_off", note=60, velocity=0, time=240))
        midi.tracks.append(track)
        output = io.BytesIO()
        midi.save(file=output)
        compare = compare_score_to_midi(score, midi_evidence(output.getvalue()))
        self.assertEqual(compare["families_declared_only_in_score"], ["horn"])
        self.assertEqual(compare["families_declared_only_in_midi"], ["english_horn"])

    def test_unexpected_zip_layout_refused(self):
        with self.assertRaisesRegex(ValueError, "not_a_compressed"):
            score_part_inventory(b"not a zip")

    def test_two_independent_symphony_scores_and_midi_are_audited(self):
        root = Path(__file__).resolve().parents[1]
        report = run(root / "data/orchestral/SOURCES.json")
        expected_parts = {"beethoven5-movement1": 18,
                          "beethoven7-movement2": 19}
        for entry in report["pieces"]:
            c = entry["midi_score_comparison"]
            self.assertEqual(c["score_part_count"], expected_parts[entry["id"]])
            self.assertEqual(c["midi_active_track_count"], 12)
            self.assertEqual(c["families_declared_only_in_score"],
                             ["horn", "trumpet"])
            self.assertEqual(c["families_declared_only_in_midi"], ["english_horn"])


if __name__ == "__main__":
    unittest.main()
