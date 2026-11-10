"""Fusion invariants: source provenance, MIDI chronology, missingness and no labels."""

import tempfile
import json
import hashlib
import unittest
from pathlib import Path

import mido

from anamu.academic_expectations import (add_expectancy_observations,
                                         fit_training_expectancies, piece_symbolic_events)
from anamu.academic_idyom import import_original_idyom_directory
from anamu.academic_fusion import (THEORY_REGISTRY, _flatten_numeric,
                                   _melody_numeric_descriptor,
                                   add_idyom_dat, add_jsymbolic_ace, add_multiscale_motion,
                                   add_theory_observations)
from anamu.tempo_map import MidiTempoMap
from anamu.midi_measure_features import extract_midi_measures


class AcademicFusionTests(unittest.TestCase):
    def make_midi(self, path):
        midi = mido.MidiFile(ticks_per_beat=480)
        part = mido.MidiTrack()
        midi.tracks.append(part)
        part.append(mido.MetaMessage("time_signature", numerator=4, denominator=4))
        part.append(mido.MetaMessage("set_tempo", tempo=500000))
        for i in range(4):
            part.append(mido.Message("note_on", note=60 + (i % 2) * 7,
                                     velocity=45 + i * 12, time=0))
            part.append(mido.Message("note_off", note=60 + (i % 2) * 7,
                                     velocity=0, time=1920))
            if i == 1:
                part.append(mido.MetaMessage("set_tempo", tempo=1_000_000))
        midi.save(path)

    def test_tempo_exact_inverse_with_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "p.mid"
            self.make_midi(source)
            tempo = MidiTempoMap.from_bytes(source.read_bytes())
            for beat in (0, 2, 4, 8, 9, 12, 16):
                self.assertAlmostEqual(tempo.seconds_to_beats(tempo.beats_to_seconds(beat)),
                                       beat, places=8)

    def test_nonredundant_proxy_features_are_temporal(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "p.mid"
            self.make_midi(source)
            rows, meta = extract_midi_measures(source, 4)
            for row in rows:
                row["music21_tonic_pc"] = 0
                row["music21_key_is_minor"] = 0
            result = add_theory_observations(source, rows, meta["beats_per_measure"])
            self.assertEqual(result["status"], "ok")
            self.assertGreater(len(THEORY_REGISTRY), 20)
            self.assertIn("theory_tonic_restoration_proxy", rows[1])
            self.assertIsNone(rows[0]["theory_density_change"])
            self.assertGreater(rows[3]["theory_dynamics_change"], 0)
            self.assertEqual(rows[0]["theory_memory_energy_2bars"],
                             rows[0]["theory_memory_energy_8bars"])

    def test_original_java_overlap_weights_not_window_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "p.mid"
            self.make_midi(source)
            rows = [{}, {}]
            ace = {"data_set_count": 1, "data_sets": [{
                "whole_piece_features": {"Whole": [3.]},
                "windows": [
                    {"start_seconds_if_j_symbolic_windowed": 0.,
                     "stop_seconds_if_j_symbolic_windowed": 1.,
                     "features": {"Texture": [1., 2.], "Undefined": [None]}},
                    {"start_seconds_if_j_symbolic_windowed": 1.,
                     "stop_seconds_if_j_symbolic_windowed": 4.,
                     "features": {"Texture": [5., 6.]}},
                ]}]}
            result = add_jsymbolic_ace(rows, ace, MidiTempoMap.from_bytes(source.read_bytes()), 4.)
            self.assertEqual(result["status"], "ok")
            self.assertEqual(rows[0]["jsym_global.Whole.0"], 3.)
            self.assertAlmostEqual(rows[0]["jsym_window.Texture.0"], 3.)
            self.assertAlmostEqual(rows[1]["jsym_window.Texture.0"], 5.)
            self.assertNotIn("jsym_window.Undefined.0", rows[0])

    def test_train_only_ngram_features_no_human_arguments(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "p.mid"
            self.make_midi(source)
            models = fit_training_expectancies([(source, 4., 4)], max_order=2)
            rows = [{} for _ in range(4)]
            result = add_expectancy_observations(source, rows, 4., models)
            self.assertEqual(result["status"], "ok")
            self.assertTrue(any(key.startswith("ngram_melodic_interval") for key in rows[1]))
            self.assertIn("ngram_harmonic_sonority.entropy_x_surprisal", rows[1])

    def test_imported_original_idyom_remains_separate_from_ngram(self):
        event = {"onset_quarter_beats": 4., "viewpoints": {
            "cpitch": {"surprisal_bits": 5., "entropy_bits_before": 2.,
                       "event_probability": .03125}}}
        export = {"melodies": [{"melody_name": "p", "events": [event]}],
                  "viewpoint_columns": {"cpitch": {}}}
        rows = [{}, {}]
        result = add_idyom_dat(rows, export, 4.)
        self.assertEqual(result["engine"], "original IDyOM Lisp .dat")
        self.assertEqual(rows[1]["idyom_cpitch.entropy_x_surprisal"], 10.)
        self.assertNotIn("idyom_cpitch.entropy_x_surprisal", rows[0])

    def test_flatten_does_not_encode_categories_or_nonfinite(self):
        self.assertEqual(_flatten_numeric({"a": [2, None, 4], "b": "minor", "c": float("nan")},
                                          "root"), {"root.a.0": 2., "root.a.2": 4.})

    def test_unbounded_motif_keys_never_create_incompatible_song_columns(self):
        a = _melody_numeric_descriptor({"motif-A": 1, "motif-B": 2}, "melody_patterns")
        b = _melody_numeric_descriptor({"unrelated-motif-X": 4}, "melody_patterns")
        self.assertEqual(set(a), set(b))
        self.assertNotIn("melody_patterns.motif-A", a)
        histogram = _melody_numeric_descriptor({"60": 2, "72": 1},
                                                "melody_absolute_pitch.basic_pitch_histogram")
        self.assertEqual(histogram["melody_absolute_pitch.basic_pitch_histogram.pitch060"], 2)
        self.assertEqual(histogram["melody_absolute_pitch.basic_pitch_histogram.pitch061"], 0)

    def test_idyom_original_import_refuses_trained_on_test_midi(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "midi").mkdir()
            source = root / "midi" / "test.mid"
            self.make_midi(source)
            (root / "idyom").mkdir()
            (root / "idyom" / "manifest.json").write_text(json.dumps({
                "engine": "original_idyom_lisp",
                "training_midi_sha256": [hashlib.sha256(source.read_bytes()).hexdigest()],
                "outputs": [],
            }))
            with self.assertRaisesRegex(ValueError, "overlaps_validation_or_test"):
                import_original_idyom_directory(root / "idyom", root,
                                                {"test.mid": "test"},
                                                {"test.mid": [{}] * 4},
                                                {"test.mid": 4.})

    def test_temporal_motion_never_uses_future_or_static_piece_descriptors(self):
        rows = [{"partitura_tensile_strain": x, "melody_global_pitch": 33}
                for x in [2., 5., None, 1.]]
        result = add_multiscale_motion(rows)
        self.assertEqual(result["original_signals_with_temporal_derivatives"], 1)
        self.assertIsNone(rows[0]["motion_delta.partitura_tensile_strain"])
        self.assertEqual(rows[1]["motion_delta.partitura_tensile_strain"], 3.)
        self.assertIsNone(rows[2]["motion_delta.partitura_tensile_strain"])
        self.assertEqual(rows[3]["motion_memory4.partitura_tensile_strain"], 8 / 3)
        self.assertFalse(any("motion_" in key and "melody_global_pitch" in key
                             for row in rows for key in row))


if __name__ == "__main__":
    unittest.main()
