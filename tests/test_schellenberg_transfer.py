"""Synthetic fixtures for the independent 1996 transfer; no listener data bundled."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import mido
import numpy as np

from anamu.schellenberg_expectancy import (schellenberg_human_means,
                                           schellenberg_midi_stimuli)
from scripts.schellenberg_external_transfer import (_assess, _frozen_training,
                                                    _predict_without_target_labels)
from tests.test_human_probe_expectancy import _write_fake_corpus
from anamu.human_probe_expectancy import load_contexts


EXAMPLES = [
    ("D", 69, 67), ("Db", 70, 72), ("G", 74, 71), ("F", 62, 65),
    ("Bb", 74, 65), ("C", 60, 69), ("G", 74, 64), ("F", 62, 72),
]


def _write_fake_schell(directory: Path) -> tuple[Path, Path]:
    ratings = directory / "schell96.data"
    midi_dir = directory / "schell"
    midi_dir.mkdir()
    lines = ["rating"]
    for index, (key, penultimate, final) in enumerate(EXAMPLES, start=1):
        lines.append(f"#fragment{index}")
        lines.extend(str(1.0 + 0.25 * i) for i in range(15))
        midi = mido.MidiFile()
        track = mido.MidiTrack()
        track.append(mido.MetaMessage("key_signature", key=key))
        # Earlier notes constitute a full fragment and must not displace the
        # penultimate, final note or be treated as a probe after the fact.
        for pitch in (penultimate - 1, penultimate, final, 84):
            track.append(mido.Message("note_on", note=pitch, velocity=64))
            track.append(mido.Message("note_off", note=pitch, velocity=0, time=100))
        midi.tracks.append(track)
        midi.save(midi_dir / f"schell96-{index}_with_probe.mid")
    ratings.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return ratings, midi_dir


class IndependentHumanTransferTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.cuddy_data, self.cuddy_midi = _write_fake_corpus(root)
        self.schell_data, self.schell_midi = _write_fake_schell(root)

    def test_human_responses_reversed_to_ascending_probe_pitches(self):
        answers = schellenberg_human_means(self.schell_data)
        self.assertEqual(len(answers), 8)
        self.assertTrue(all(len(x) == 15 for x in answers))
        self.assertEqual(answers[0][0], 4.5)
        self.assertEqual(answers[0][-1], 1.0)

    def test_rejects_non_contiguous_or_non_aggregate_ratings(self):
        original = self.schell_data.read_text()
        self.schell_data.write_text(original.replace("#fragment2", "#fragment1"))
        with self.assertRaisesRegex(ValueError, "fragment_order_mismatch"):
            schellenberg_human_means(self.schell_data)
        self.schell_data.write_text(original.replace("1.0", "9.0", 1))
        with self.assertRaisesRegex(ValueError, "ratings_outside_1_to_7"):
            schellenberg_human_means(self.schell_data)

    def test_midi_contexts_ignore_placeholder_and_preserve_key(self):
        stimuli = schellenberg_midi_stimuli(self.schell_midi)
        self.assertEqual(len(stimuli), 8)
        self.assertEqual(stimuli[0]["last_two"], [69, 67])
        self.assertEqual(stimuli[0]["context_note_count"], 3)
        np.testing.assert_array_equal(stimuli[0]["candidates"],
                                      [55, 57, 59, 61, 62, 64, 66, 67,
                                       69, 71, 73, 74, 76, 78, 79])
        self.assertEqual(len(stimuli[7]["candidates"]), 15)
        self.assertNotIn(84, stimuli[0]["candidates"])

    def test_rejects_placeholder_leakage_or_invalid_signature(self):
        path = self.schell_midi / "schell96-1_with_probe.mid"
        midi = mido.MidiFile(path)
        note_ons = [m for m in midi.tracks[0]
                    if m.type == "note_on" and m.velocity > 0]
        note_ons[-1].note = 83
        midi.save(path)
        with self.assertRaisesRegex(ValueError, "missing_reconstructed_probe_placeholder"):
            schellenberg_midi_stimuli(self.schell_midi)

    def test_source_training_predicts_before_opening_target_answers(self):
        cuddy = load_contexts(self.cuddy_data, self.cuddy_midi)
        template, models = _frozen_training(cuddy)
        stimuli = schellenberg_midi_stimuli(self.schell_midi)
        predicted = _predict_without_target_labels(stimuli, template, models)
        self.assertEqual(len(predicted), 5)
        self.assertTrue(all(len(predicted[name]) == 8 for name in predicted))
        self.assertTrue(all(np.isfinite(value).all() for group in predicted.values()
                            for value in group))
        report = _assess(predicted, schellenberg_human_means(self.schell_data))
        self.assertEqual(report["comparisons_vs_source_fitted_template"]
                         ["tonal_context_residual"]["total_fragments"], 8)


if __name__ == "__main__":
    unittest.main()
