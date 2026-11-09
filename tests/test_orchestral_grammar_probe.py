"""G0/G1 orchestral probe: observed events, no musical-semantic inference."""

import io
import json
import tempfile
import unittest
from pathlib import Path

import mido

from anamu.grammar_foundation import midi_evidence
from scripts.orchestral_grammar_probe import audit, run_manifest


class OrchestralGrammarProbeTests(unittest.TestCase):
    @staticmethod
    def _polyphonic_midi():
        midi = mido.MidiFile(type=1, ticks_per_beat=480)
        control = mido.MidiTrack()
        control.append(mido.MetaMessage("set_tempo", tempo=550000, time=0))
        midi.tracks.append(control)
        for channel, pitch in ((0, 60), (1, 64)):
            track = mido.MidiTrack()
            track.append(mido.MetaMessage("instrument_name", name="sample", time=0))
            track.append(mido.Message("program_change", channel=channel,
                                      program=40, time=0))
            track.append(mido.Message("note_on", channel=channel, note=pitch,
                                      velocity=90, time=0))
            track.append(mido.Message("note_off", channel=channel, note=pitch,
                                      velocity=0, time=240))
            midi.tracks.append(track)
        output = io.BytesIO()
        midi.save(file=output)
        return output.getvalue()

    def test_polyphonic_parallel_relation_and_concurrency(self):
        observations = audit(midi_evidence(self._polyphonic_midi()))
        g0 = observations["g0"]
        g1 = observations["g1_adjacent_note_probe"]
        self.assertEqual(g0["track_count"], 3)
        self.assertEqual(g0["unambiguous_key_spans"], 2)
        self.assertEqual(g0["onset_ticks_with_two_or_more_key_spans"], 1)
        self.assertEqual(g0["max_simultaneous_key_down_spans"], 2)
        self.assertEqual(g1["evaluated_pairs"], 1)
        self.assertEqual(g1["allen_relations"], {"equals": 1})
        self.assertEqual(g1["operators"], {"PARALLEL": 1})
        self.assertIsNone(g0["audio_loudness"])
        self.assertIsNone(g0["inferred_instrument"])
        self.assertEqual(g0["track_observations"][1]["instrument_names"],
                         ["sample"])

    def test_pair_budget_is_explicit_and_zero_is_allowed(self):
        evidence = midi_evidence(self._polyphonic_midi())
        self.assertEqual(audit(evidence, max_adjacent_pairs=0)[
            "g1_adjacent_note_probe"]["evaluated_pairs"], 0)
        with self.assertRaisesRegex(ValueError, "negative_pair_budget"):
            audit(evidence, max_adjacent_pairs=-1)

    def test_manifest_checksum_guard(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sources.json"
            path.write_text(json.dumps({"version": 1, "pieces": [{
                "id": "intentionally-corrupt-checksum",
                "file": "data/orchestral/beethoven5-movement1.mid",
                "sha256": "0" * 64}]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "source_checksum_mismatch"):
                run_manifest(path, pair_budget=2)

    def test_real_multitrack_sources_have_unambiguous_notes(self):
        report = run_manifest(Path(__file__).resolve().parents[1] /
                              "data/orchestral/SOURCES.json", pair_budget=7)
        self.assertEqual(len(report["pieces"]), 2)
        for entry in report["pieces"]:
            self.assertGreater(entry["observations"]["g0"]["track_count"], 8)
            self.assertGreater(entry["observations"]["g0"]["unambiguous_key_spans"],
                               1000)
            self.assertEqual(entry["observations"]["g1_adjacent_note_probe"][
                "evaluated_pairs"], 7)


if __name__ == "__main__":
    unittest.main()
