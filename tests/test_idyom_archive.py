"""Scientific guardrails for third-party IDyOM probabilities, no download."""

from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

import numpy as np

from anamu.idyom_archive import (archived_cuddy_cpitch, archived_schellenberg_probs,
                                 schellenberg_workbook_pitches)
from scripts.idyom_archived_probe_comparison import (_mean_context_rank,
                                                     _paired_difference)


class ArchivedIdyomTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)

    def _schell_csv(self, value="0.02", broken=None):
        path = self.root / "schell.csv"
        rows = [["fragment", *["idyom probability"] * 15]]
        rows.extend([[str(index), *[value] * 15] for index in range(1, 9)])
        if broken:
            broken(rows)
        with path.open("w", newline="") as stream:
            csv.writer(stream).writerows(rows)
        return path

    def _cuddy_csv(self, broken=None):
        path = self.root / "cuddy.csv"
        rows = [["melody.id", "melody.name", *
                 [f"idyom prob {pitch}" for pitch in range(54, 79)]]]
        rows.extend([[str(i), f"cudlun95-{i}_with_probe", *["0.01"] * 25]
                     for i in range(1, 9)])
        if broken:
            broken(rows)
        with path.open("w", newline="") as stream:
            csv.writer(stream).writerows(rows)
        return path

    def test_valid_archived_tables_have_eight_fixed_pitch_contexts(self):
        self.assertEqual([len(p) for p in archived_schellenberg_probs(self._schell_csv())],
                         [15] * 8)
        self.assertEqual([len(p) for p in archived_cuddy_cpitch(self._cuddy_csv())],
                         [25] * 8)

    def test_prohibits_stale_or_reordered_fragment_ids(self):
        def swap(rows):
            rows[1], rows[2] = rows[2], rows[1]
        with self.assertRaisesRegex(ValueError, "fragment_identity_mismatch"):
            archived_schellenberg_probs(self._schell_csv(broken=swap))

    def test_prohibits_reordered_absolute_pitches(self):
        def swap(rows):
            rows[0][1], rows[0][2] = rows[0][2], rows[0][1]
        # Header names have pitch IDs, not merely 25 anonymous slots.
        with self.assertRaisesRegex(ValueError, "pitch_header_mismatch"):
            archived_cuddy_cpitch(self._cuddy_csv(broken=swap))

    def test_rejects_missing_or_unphysical_probabilities(self):
        for number in ("nan", "inf", "-0.1", "1.1", "garbage", ""):
            with self.subTest(value=number):
                with self.assertRaisesRegex(ValueError, "invalid_archived_probability"):
                    archived_schellenberg_probs(self._schell_csv(value=number))
        with self.assertRaisesRegex(ValueError, "probability_mass"):
            archived_schellenberg_probs(self._schell_csv(value="0.2"))

    def test_ooxml_workbook_candidates_in_column_order_without_extra_library(self):
        pitch_rows = []
        for row in range(2, 17):
            cells = "".join(f'<c r="{col}{row}"><v>{48 + row + offset}</v></c>'
                            for offset, col in enumerate("ABCDEFGH"))
            pitch_rows.append(f'<row r="{row}">{cells}</row>')
        xml = ('<worksheet xmlns="http://schemas.openxmlformats.org/'
               'spreadsheetml/2006/main"><sheetData><row r="1"/>' +
               "".join(pitch_rows) + '</sheetData></worksheet>')
        workbook = self.root / "pitches.xlsx"
        with ZipFile(workbook, "w") as archive:
            archive.writestr("xl/worksheets/sheet1.xml", xml)
        result = schellenberg_workbook_pitches(workbook)
        self.assertEqual(result[0].tolist(), list(range(50, 65)))
        self.assertEqual(result[-1].tolist(), list(range(57, 72)))

    def test_rank_metrics_use_contexts_not_raw_probability_scales(self):
        y = [np.arange(15, dtype=float) for _ in range(8)]
        prediction = [np.arange(15, dtype=float) / 100 for _ in range(8)]
        self.assertEqual(_mean_context_rank(prediction, y)["mean_spearman"], 1.0)
        comparison = _paired_difference([.8] * 8, [.6] * 8)
        self.assertEqual(comparison["fragments_better"], 8)
        self.assertAlmostEqual(comparison["mean_rank_gain"], .2)


if __name__ == "__main__":
    unittest.main()
