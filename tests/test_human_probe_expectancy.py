"""Synthetic-only checks. The copyrighted human means are not test fixtures."""

from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

import mido
import numpy as np

from anamu.human_probe_expectancy import (
    load_contexts, load_group_means, theory_features, training_arrays,
)
from scripts.cudlun_probe_benchmark import _evaluate, _predict_leave_one_context_out


INTERVALS = [("M2 ascending", 2), ("M2 descending", -2),
             ("m3 ascending", 3), ("m3 descending", -3),
             ("M6 ascending", 9), ("M6 descending", -9),
             ("m7 ascending", 10), ("m7 descending", -10)]


def _write_fake_corpus(directory: Path) -> tuple[Path, Path]:
    data = directory / "test.data"
    midi_folder = directory / "midi"
    midi_folder.mkdir()
    rows = ["trained\tuntrained"]
    for i, (label, interval) in enumerate(INTERVALS, start=1):
        rows.append(f"#{label}")
        for step in range(25):
            rows.append(f"{2 + (step % 5) * .5:.2f}\t{3 + (step % 4) * .25:.2f}")
        track = mido.MidiTrack()
        second = 66
        for pitch in (second - interval, second, second):
            track.append(mido.Message("note_on", note=pitch, velocity=70, time=0))
            track.append(mido.Message("note_off", note=pitch, velocity=0, time=120))
        midi = mido.MidiFile()
        midi.tracks.append(track)
        midi.save(midi_folder / f"cudlun95-{i}_with_probe.mid")
    data.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return data, midi_folder


class HumanExpectancyTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.data, self.midi = _write_fake_corpus(Path(self.temp.name))

    def test_public_group_means_schema_is_strict(self):
        blocks = load_group_means(self.data)
        self.assertEqual(len(blocks), 8)
        self.assertTrue(all(len(block["trained"]) == 25 for block in blocks))
        self.data.write_text(self.data.read_text().replace("1.00", "99.00", 1)
                             .replace("2.00", "99.00", 1))
        with self.assertRaisesRegex(ValueError, "rating_outside_1_to_7"):
            load_group_means(self.data)

    def test_reconstructed_contexts_have_only_two_input_notes(self):
        contexts = load_contexts(self.data, self.midi)
        self.assertEqual(len(contexts), 8)
        self.assertEqual(contexts[0]["first"], 64)
        self.assertEqual(contexts[0]["second"], 66)
        self.assertEqual(list(contexts[0]["probes"]), list(range(54, 79)))
        self.assertEqual(training_arrays(contexts)["labels"].shape, (200,))

    def test_midi_interval_validation_rejects_wrong_context(self):
        source = self.midi / "cudlun95-1_with_probe.mid"
        midi = mido.MidiFile(source)
        midi.tracks[0][0].note = 60
        midi.save(source)
        with self.assertRaisesRegex(ValueError, "midi_context_does_not_match"):
            load_contexts(self.data, self.midi)

    def test_midi_validation_rejects_non_placeholder_third_note(self):
        source = self.midi / "cudlun95-1_with_probe.mid"
        midi = mido.MidiFile(source)
        midi.tracks[0][4].note = 67
        midi.save(source)
        with self.assertRaisesRegex(ValueError, "requires_two_context_notes"):
            load_contexts(self.data, self.midi)

    def test_theory_features_are_transposition_invariant(self):
        a = theory_features(64, 66, np.arange(54, 79))
        b = theory_features(70, 72, np.arange(60, 85))
        for method in a:
            np.testing.assert_allclose(a[method], b[method])

    def test_context_holdout_is_immune_to_its_own_rating_changes(self):
        original = load_contexts(self.data, self.midi)
        array1 = training_arrays(original)
        prediction1 = _predict_leave_one_context_out(array1)
        changed = copy.deepcopy(original)
        changed[0]["trained"] = [6.5] * 25
        changed[0]["untrained"] = [6.5] * 25
        array2 = training_arrays(changed)
        prediction2 = _predict_leave_one_context_out(array2)
        held_out = array1["groups"] == 0
        for model in prediction1:
            np.testing.assert_allclose(prediction1[model][held_out],
                                       prediction2[model][held_out])
        # Holding out both directions of one interval removes that interval
        # entirely from fitting, including the residual model's template.
        paired = [(0, 1), (2, 3), (4, 5), (6, 7)]
        pair1 = _predict_leave_one_context_out(array1, paired)
        pair2 = _predict_leave_one_context_out(array2, paired)
        held_pair = np.isin(array1["groups"], [0, 1])
        for model in pair1:
            np.testing.assert_allclose(pair1[model][held_pair], pair2[model][held_pair])
        with self.assertRaisesRegex(ValueError, "held_out_sets_must_partition"):
            _predict_leave_one_context_out(array1, [(0,), (0,)])
        report = _evaluate(original)
        self.assertEqual(len(report["models"]), 5)
        self.assertEqual(set(report["robustness_stricter_groupings"]),
                         {"leave_interval_size_out", "leave_direction_out"})
        self.assertEqual(report["paired_context_comparison"]["proximity"]
                         ["contexts_total"], 8)


if __name__ == "__main__":
    unittest.main()
