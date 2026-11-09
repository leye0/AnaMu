"""Synthetic-only tests: Manzara outcome and actual-note alignment contracts."""

from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

import mido
import numpy as np

from anamu.manzara_expectancy import (CHORALE_LENGTHS, human_note_bits,
                                     reconstructed_chorale_notes,
                                     softmax_information_bits)
from anamu.human_probe_expectancy import load_contexts
from scripts.manzara_cross_target import (_import_2025_idyom_reference, _statistics,
                                         frozen_cuddy_surprisals)
from scripts.schellenberg_external_transfer import _frozen_training
from tests.test_human_probe_expectancy import _write_fake_corpus


class HumanBettingTransferTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        root = Path(self.folder.name)
        self.cuddy_labels, self.cuddy_midis = _write_fake_corpus(root)
        self.stimuli_dir = root / "chorale_midis"
        self.stimuli_dir.mkdir()
        self.human_source = root / "manzetal92.data"
        lines = ["chorale note average weighted best"]
        self.pitches = {}
        for chorale, length in CHORALE_LENGTHS.items():
            pitches = [65 + i % 3 for i in range(length)]
            self.pitches[chorale] = pitches
            midi = mido.MidiFile()
            track = mido.MidiTrack()
            for pitch in pitches:
                track.append(mido.Message("note_on", note=pitch, velocity=88))
                track.append(mido.Message("note_off", note=pitch, velocity=0, time=96))
            midi.tracks.append(track)
            midi.save(self.stimuli_dir / f"chorale{chorale}.mid")
            lines.extend(f"{chorale}\t{i + 1}  {1.0 + (i % 6) * .2:.3f} 1.0 0.1"
                         for i in range(length))
        self.human_source.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def test_stimuli_and_human_bits_match_but_remain_distinct(self):
        target = human_note_bits(self.human_source)
        notes = reconstructed_chorale_notes(self.stimuli_dir)
        self.assertEqual([len(notes[k]) for k in CHORALE_LENGTHS], [29, 57])
        self.assertEqual([len(target[k]) for k in CHORALE_LENGTHS], [29, 57])
        self.assertEqual(target[151][0, 1], 1.0)
        self.assertEqual(target[151][1, 1], 1.2)
        self.assertEqual(target[61][0, 0], 1)

    def test_rejects_duplicate_unordered_and_missing_human_rows(self):
        original = self.human_source.read_text()
        self.human_source.write_text(original.replace("151\t2 ", "151\t3 ", 1))
        with self.assertRaisesRegex(ValueError, "out_of_order"):
            human_note_bits(self.human_source)
        self.human_source.write_text(original.replace("151\t29 ", "", 1))
        with self.assertRaises(ValueError):
            human_note_bits(self.human_source)

    def test_rejects_unmatched_midi_or_unreachable_realized_note(self):
        midi_path = self.stimuli_dir / "chorale151.mid"
        midi = mido.MidiFile(midi_path)
        midi.tracks[0].insert(0, mido.Message("note_on", note=96, velocity=88))
        midi.save(midi_path)
        with self.assertRaisesRegex(ValueError, "midi_note_count"):
            reconstructed_chorale_notes(self.stimuli_dir)

    def test_softmax_is_probability_on_25_support_and_not_a_rating(self):
        self.assertAlmostEqual(softmax_information_bits(np.zeros(25), 12),
                               np.log2(25))
        more_likely = np.zeros(25)
        more_likely[12] = 5
        self.assertLess(softmax_information_bits(more_likely, 12), 1)
        self.assertGreater(softmax_information_bits(more_likely, 13), 5)
        with self.assertRaisesRegex(ValueError, "actual_note_outside"):
            softmax_information_bits(more_likely, 25)

    def test_source_only_scores_run_without_opening_human_data(self):
        notes = reconstructed_chorale_notes(self.stimuli_dir)
        template, models = _frozen_training(load_contexts(self.cuddy_labels, self.cuddy_midis))
        self.human_source.unlink()
        predicted = frozen_cuddy_surprisals(notes, template, models)
        self.assertEqual(len(predicted[151]["pitch_template_only"]), 27)
        self.assertEqual(len(predicted[61]["narmour_contour_proxy"]), 55)
        self.assertTrue(np.isfinite(predicted[151]["narmour_contour_proxy"]).all())

    def test_reference_predictions_strict_pitch_and_index_alignment(self):
        file = Path(self.folder.name) / "external.csv"
        with file.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(["filename", "note_index", "actual_pitch",
                             "idyom_probability", "idyom_ic"])
            for chorale, notes in self.pitches.items():
                for i, pitch in enumerate(notes):
                    writer.writerow([f"chorale{chorale}.mid", i, pitch, .25, 2])
        data = _import_2025_idyom_reference(file, reconstructed_chorale_notes(self.stimuli_dir))
        self.assertEqual(len(data[151]), 27)
        with file.open("r+", encoding="utf-8") as stream:
            content = stream.read().replace("chorale151.mid,0,65", "chorale151.mid,0,70")
            stream.seek(0)
            stream.write(content)
            stream.truncate()
        with self.assertRaisesRegex(ValueError, "mismatch"):
            _import_2025_idyom_reference(file, reconstructed_chorale_notes(self.stimuli_dir))

    def test_note_level_metrics_do_not_claim_independent_votes(self):
        human = human_note_bits(self.human_source)
        notes = reconstructed_chorale_notes(self.stimuli_dir)
        template, models = _frozen_training(load_contexts(self.cuddy_labels, self.cuddy_midis))
        predicted = frozen_cuddy_surprisals(notes, template, models)
        result = _statistics(predicted, human)
        self.assertEqual(result["pitch_template_only"]["per_chorale"]["151"]
                         ["notes_after_two_context_notes"], 27)
        self.assertIn("pooled_note_spearman_descriptive_only", result["narmour_contour_proxy"])


if __name__ == "__main__":
    unittest.main()
