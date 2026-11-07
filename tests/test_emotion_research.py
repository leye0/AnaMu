import json
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from anamu.emopia import (EmopiaClip, assert_song_disjoint, assign_song_splits,
                          hold_out_entire_emopia, inventory_emopia,
                          parse_emopia_filename, split_summary)
from anamu.emotion_evaluation import evaluate_quadrants, majority_class_baseline
from anamu.theory_features import (music21_harmonic_hypotheses, partitura_tension,
                                   read_idyom_export)
from scripts.run_jsymbolic import build_jsymbolic_command


def synthetic_clips():
    return [EmopiaClip(clip_id=f"video{song:06d}_{segment}",
                       song_id=f"video{song:06d}", segment_index=segment,
                       quadrant=(song % 4) + 1, path="unused.mid", sha256="0" * 64)
            for song in range(20) for segment in range(3)]


class EmopiaResearchTests(unittest.TestCase):
    def test_official_muspy_filename_convention(self):
        self.assertEqual(parse_emopia_filename("Q1_0vLPYiPN7qY_0.mid"),
                         ("0vLPYiPN7qY", 0, 1))
        self.assertEqual(parse_emopia_filename("Q4_X-y_A2B1234_12.mid"),
                         ("X-y_A2B1234", 12, 4))
        self.assertIsNone(parse_emopia_filename("Q5_0vLPYiPN7qY_0.mid"))
        self.assertIsNone(parse_emopia_filename("unknown.mid"))

    def test_inventory_is_auditable_and_never_uses_corrupt_filenames(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root / "Q1_0vLPYiPN7qY_0.mid").write_bytes(b"midi-bytes")
            (root / "unknown.mid").write_bytes(b"other")
            (root / "Q4_0vLPYiPN7qY_0.mid").write_bytes(b"duplicate-song-segment")
            (root / "Q2_1234567890A_1.mid").write_bytes(b"midi-bytes")
            inventory = inventory_emopia(root)
            self.assertEqual(len(inventory["clips"]), 1)
            self.assertEqual(len(inventory["rejected"]), 3)
            self.assertEqual(len(inventory["clips"][0].sha256), 64)
            self.assertIn("duplicate_song_segment", [v["reason"] for v in inventory["rejected"]])
            self.assertIn("duplicate_midi_content", [v["reason"] for v in inventory["rejected"]])

    def test_song_group_split_is_stable_and_no_clip_leaks(self):
        raw = synthetic_clips()
        first = assign_song_splits(raw)
        self.assertEqual(first, assign_song_splits(raw))
        summary = split_summary(first)
        self.assertEqual(sum(group["clips"] for group in summary.values()), 60)
        self.assertEqual(sum(group["songs"] for group in summary.values()), 20)
        for song_id in {c.song_id for c in first}:
            self.assertEqual(len({c.split for c in first if c.song_id == song_id}), 1)

    def test_strict_external_protocol_never_trains_on_emopia(self):
        clips = hold_out_entire_emopia(synthetic_clips())
        summary = split_summary(clips)
        self.assertEqual(summary["train"]["clips"], 0)
        self.assertEqual(summary["validation"]["clips"], 0)
        self.assertEqual(summary["test"]["clips"], len(clips))
        predictions = {c.clip_id: c.quadrant for c in clips}
        self.assertEqual(evaluate_quadrants(clips, predictions)["macro_f1_fixed_four_classes"], 1.0)

    def test_song_leakage_is_rejected(self):
        clips = assign_song_splits(synthetic_clips())
        changed = replace(clips[1], split="test" if clips[0].split != "test" else "train")
        with self.assertRaisesRegex(ValueError, "song_leakage"):
            assert_song_disjoint([clips[0], changed])

    def test_metrics_penalize_abstentions_instead_of_cherry_picking(self):
        clips = assign_song_splits(synthetic_clips())
        test = [c for c in clips if c.split == "test"]
        predictions = {test[0].clip_id: test[0].quadrant}
        metrics = evaluate_quadrants(clips, predictions)
        self.assertEqual(metrics["total_clips"], len(test))
        self.assertAlmostEqual(metrics["coverage"], 1 / len(test))
        self.assertAlmostEqual(metrics["clip_accuracy_including_abstentions"], 1 / len(test))
        self.assertGreater(metrics["confusion"][str(test[0].quadrant)][str(test[0].quadrant)], 0)
        self.assertTrue(any(row["abstain"] for row in metrics["confusion"].values()))

    def test_macro_f1_perfect_predictions_uses_all_four_classes(self):
        clips = assign_song_splits(synthetic_clips())
        test = [c for c in clips if c.split == "test"]
        metrics = evaluate_quadrants(clips, {c.clip_id: c.quadrant for c in test})
        self.assertAlmostEqual(metrics["clip_accuracy_including_abstentions"], 1)
        for quadrant in range(1, 5):
            if metrics["class_support"][str(quadrant)]:
                self.assertEqual(metrics["per_class_f1"][str(quadrant)], 1)
        self.assertEqual(metrics["macro_f1_fixed_four_classes"],
                         sum(v > 0 for v in metrics["class_support"].values()) / 4)

    def test_baseline_only_sees_training_labels(self):
        clips = assign_song_splits(synthetic_clips())
        train = [c for c in clips if c.split == "train"]
        held_out = [c for c in clips if c.split == "test"]
        predicted = majority_class_baseline(train, held_out)
        self.assertEqual(len(predicted), len(held_out))
        with self.assertRaisesRegex(ValueError, "baseline_target_is_not_held_out"):
            majority_class_baseline(train, train)
        with self.assertRaisesRegex(ValueError, "evaluation_must_be_held_out"):
            evaluate_quadrants(clips, predicted, split="train")

    def test_external_cli_holds_every_emopia_clip_out(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root / "Q1_0vLPYiPN7qY_0.mid").write_bytes(b"midi1")
            (root / "Q4_1234567890A_0.mid").write_bytes(b"midi2")
            response = subprocess.run(
                [sys.executable, "-m", "scripts.emopia_benchmark", str(root)],
                capture_output=True, text=True, check=True,
            )
            data = json.loads(response.stdout)
            self.assertEqual(data["protocol"], "external")
            self.assertEqual(data["counts"]["test"]["clips"], 2)
            self.assertEqual(data["counts"]["train"]["clips"], 0)
            self.assertNotIn("baseline_majority_train_only", data)
            self.assertNotIn("model", data)


class ExistingPublishedAlgorithmsTests(unittest.TestCase):
    def test_upstream_jsymbolic_command_windows_are_not_mock_features(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            jar, midi = root / "jSymbolic2.jar", root / "piano.mid"
            jar.write_bytes(b"fake; dry run only")
            midi.write_bytes(b"fake; dry run only")
            command = build_jsymbolic_command(
                jar, midi, root / "results.xml", root / "defs.xml", 5, 0.5)
            self.assertEqual(command[0], "java")
            self.assertEqual(command[4:6], ["-csv", "-window"])
            self.assertEqual(len(command), 11)
            self.assertEqual(command[7], str((root / "results.xml").resolve()))
            self.assertEqual(command[8], str((root / "defs.xml").resolve()))
            self.assertEqual(command[-2:], ["5", "0.5"])
            with self.assertRaises(ValueError):
                build_jsymbolic_command(jar, midi, root / "a", root / "b", 5, 1.0)

    def test_idyom_external_output_columns_are_explicit(self):
        with tempfile.TemporaryDirectory() as name:
            path = Path(name) / "export.csv"
            path.write_text("melody.information.content,melody.entropy,onset\n2.5,1.2,0\n0.3,0.8,1\n")
            result = read_idyom_export(
                path, surprisal_column="melody.information.content",
                entropy_column="melody.entropy", onset_column="onset")
            self.assertEqual(result["samples"][0]["surprisal_bits"], 2.5)
            self.assertEqual(result["samples"][1]["entropy_bits_before"], 0.8)
            with self.assertRaisesRegex(ValueError, "missing_idyom_columns"):
                read_idyom_export(path, surprisal_column="not_an_idyom_column",
                                  entropy_column="melody.entropy")

    def test_partitura_real_implementation_on_polyphonic_piano_midi(self):
        try:
            import partitura
        except ImportError:
            self.skipTest("Partitura optional; separate integration CI installs it")
        import mido
        with tempfile.TemporaryDirectory() as name:
            path = Path(name) / "piano.mid"
            mid = mido.MidiFile(ticks_per_beat=480)
            track = mido.MidiTrack()
            mid.tracks.append(track)
            for pitches in ([60, 64, 67], [62, 65, 69], [67, 71, 74], [60, 64, 67]):
                for note in pitches:
                    track.append(mido.Message("note_on", note=note, velocity=75, time=0))
                for index, note in enumerate(pitches):
                    track.append(mido.Message("note_off", note=note, velocity=0,
                                              time=480 if index == 0 else 0))
            mid.save(path)
            result = partitura_tension(path, window_seconds=0.6, hop_seconds=0.5)
            self.assertEqual(result["engine"], "partitura.musicanalysis.estimate_tonaltension")
            self.assertGreater(len(result["samples"]), 1)
            for row in result["samples"]:
                self.assertGreaterEqual(row["cloud_diameter"], 0)
                self.assertGreaterEqual(row["cloud_momentum"], 0)
                self.assertGreaterEqual(row["tensile_strain"], 0)

    def test_music21_harmony_is_labeled_hypothesis_not_truth(self):
        try:
            import music21
        except ImportError:
            self.skipTest("music21 optional; separate integration CI installs it")
        import mido
        with tempfile.TemporaryDirectory() as name:
            path = Path(name) / "harmony.mid"
            midi = mido.MidiFile(ticks_per_beat=480)
            track = mido.MidiTrack()
            midi.tracks.append(track)
            for pitches in ([60, 64, 67], [62, 65, 69], [67, 71, 74], [60, 64, 67]):
                for pitch in pitches:
                    track.append(mido.Message("note_on", note=pitch, velocity=80, time=0))
                for index, pitch in enumerate(pitches):
                    track.append(mido.Message("note_off", note=pitch, velocity=0,
                                              time=480 if index == 0 else 0))
            midi.save(path)
            result = music21_harmonic_hypotheses(path)
            self.assertIn(result["key_hypothesis"]["mode"], ("major", "minor"))
            self.assertTrue(result["sonorities"])
            self.assertTrue(all(event["candidate_not_verified_chord"]
                                for event in result["sonorities"]))
            self.assertTrue(any(event["roman_numeral_hypothesis"]
                                for event in result["sonorities"]))


if __name__ == "__main__":
    unittest.main()
