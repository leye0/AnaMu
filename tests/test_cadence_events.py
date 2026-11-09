"""Synthetic audit: gold DCML harmony columns never become model features."""

import csv
import tempfile
import unittest
from pathlib import Path

from anamu.cadence_events import build_piece, load_corpora
from anamu.research_contracts import ResearchContractError, check_experiment, load_catalog


def _write_tsv(path, records):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=records[0].keys(), delimiter="\t")
        writer.writeheader()
        writer.writerows(records)


class CadenceEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.notes = Path(self.temp.name) / "test.notes.tsv"
        self.harmony = Path(self.temp.name) / "test.harmonies.tsv"
        _write_tsv(self.notes, [{
            "quarterbeats": str(t), "mc_onset": str((t % 4) / 4),
            "midi": str(60 + (t % 5)), "duration_qb": "1"
        } for t in range(16)])
        self.labels = [
            {"quarterbeats": "4", "cadence": "PAC", "globalkey": "C",
             "localkey": "V", "chord": "V7"},
            {"quarterbeats": "12", "cadence": "HC", "globalkey": "G",
             "localkey": "ii", "chord": "ii6"},
        ]
        _write_tsv(self.harmony, self.labels)

    def test_label_positions_are_time_aligned(self):
        piece = build_piece(self.notes, self.harmony)
        self.assertEqual(piece["n_annotated_cadences"], 2)
        self.assertEqual(piece["n_matched_cadences"], 2)
        self.assertEqual([i for i, label in enumerate(piece["labels"]) if label], [4, 12])
        self.assertEqual(len(piece["rhythm"]), len(piece["harmony"]))

    def test_changing_expert_chords_and_keys_cannot_change_features(self):
        first = build_piece(self.notes, self.harmony)
        for row in self.labels:
            row["globalkey"] = "F#"
            row["localkey"] = "viio"
            row["chord"] = "bII6"
        _write_tsv(self.harmony, self.labels)
        changed = build_piece(self.notes, self.harmony)
        self.assertEqual(first["rhythm"], changed["rhythm"])
        self.assertEqual(first["harmony"], changed["harmony"])

    def test_reject_using_cadences_as_emotion_ground_truth(self):
        catalog = load_catalog()
        entry = dict(catalog["experiments"]["dcml_cadence_exploratory"])
        entry["claim_scope"] = "global_mood_association"
        with self.assertRaisesRegex(ResearchContractError, "incompatible"):
            check_experiment("not_emotion", entry, catalog)

    def test_sonata_movements_share_parent_work(self):
        mozart = Path(self.temp.name) / "mozart"
        (mozart / "notes").mkdir(parents=True)
        (mozart / "harmonies").mkdir()
        for name in ["K279-1", "K279-2"]:
            _write_tsv(mozart / "notes" / (name + ".notes.tsv"), [{
                "quarterbeats": str(t), "mc_onset": str((t % 4) / 4),
                "midi": str(60 + (t % 5)), "duration_qb": "1"
            } for t in range(16)])
            _write_tsv(mozart / "harmonies" / (name + ".harmonies.tsv"), self.labels)
        pieces = load_corpora({"mozart": mozart})["pieces"]
        self.assertEqual(len(pieces), 2)
        self.assertNotEqual(pieces[0]["piece"], pieces[1]["piece"])
        self.assertEqual(pieces[0]["parent_work"], pieces[1]["parent_work"])


if __name__ == "__main__":
    unittest.main()
