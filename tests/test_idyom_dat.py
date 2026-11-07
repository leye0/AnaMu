"""Native IDyOM .dat parsing, based on actual upstream py2lispIDyOM data."""

import tempfile
import unittest
from pathlib import Path

from anamu.idyom_dat import read_idyom_dat


HEADER = ("dataset.id melody.id note.id melody.name onset tempo "
          "cpitch.probability cpitch.information.content cpitch.entropy "
          "onset.probability onset.information.content onset.entropy "
          "probability information.content entropy information.gain "
          "cpitch.55 cpitch.67 onset.0")
FIRST = ("42 1 1 \"Nocturne in C\" 0 600000 "
         "0.033281446 4.909138 4.807867 "
         "0.15525937 2.6872478 3.157853 "
         "0.005167256 7.5963855 7.965716 NA 0.02 0.07 0.15")
SECOND = ("42 1 2 \"Nocturne in C\" 24 600000 "
          "0.106121935 3.236205 3.2992885 "
          "0.42446643 1.2362776 2.0731294 "
          "NA 4.4724827 5.3724103 2.466142 0.03 NA 0.16")
THIRD = ("42 2 1 \"Other piece\" 0 500000 "
         "0.1 NA 2.4 0.5 1.2 1.1 0.2 3.2 3.0 NA NA NA NA")


class IDyOMDatTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.file = Path(self.tmp.name) / "original.dat"

    def parse(self, *rows):
        self.file.write_text("\n".join((HEADER, *rows)) + "\n", encoding="utf-8")
        return read_idyom_dat(self.file)

    def test_actual_format_multiple_viewpoints_and_melodies(self):
        result = self.parse(FIRST, SECOND, THIRD)
        self.assertEqual((result["melody_count"], result["event_count"]), (2, 3))
        self.assertEqual(set(result["viewpoint_columns"]), {"joint", "cpitch", "onset"})
        first = result["melodies"][0]
        self.assertEqual(first["melody_name"], "Nocturne in C")
        self.assertEqual(first["events"][1]["onset_quarter_beats"], 1)
        self.assertEqual(first["events"][0]["viewpoints"]["joint"]["surprisal_bits"], 7.5963855)
        self.assertEqual(first["events"][0]["viewpoints"]["onset"]["entropy_bits_before"], 3.157853)
        self.assertEqual(first["events"][0]["predicted_event_probabilities"]["cpitch"]["67"], 0.07)
        self.assertEqual(first["events"][1]["information_gain_native_if_reported"], 2.466142)
        self.assertIsNone(first["events"][1]["predicted_event_probabilities"]["cpitch"]["67"])
        self.assertIsNone(first["events"][1]["viewpoints"]["joint"]["event_probability"])
        self.assertIsNone(result["melodies"][1]["events"][0]["viewpoints"]["cpitch"]["surprisal_bits"])
        self.assertNotIn("time_seconds", first["events"][1])
        self.assertEqual(len(result["input_sha256"]), 64)

    def test_lossless_original_columns_optional(self):
        self.parse(FIRST)
        result = read_idyom_dat(self.file, keep_original_fields=True)
        original = result["melodies"][0]["events"][0]["original_fields"]
        self.assertEqual(original["melody.name"], "Nocturne in C")
        self.assertEqual(original["cpitch.55"], "0.02")
        self.assertIsNone(original["information.gain"])
        self.assertTrue(result["original_fields_preserved"])

    def test_nonfinite_and_negative_measure_rejected(self):
        for bad in ("NaN", "Inf", "-1", "hello"):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                self.parse(FIRST.replace("7.5963855", bad))

    def test_invalid_probability_rejected(self):
        with self.assertRaisesRegex(ValueError, "idyom_probability_exceeds_one"):
            self.parse(FIRST.replace("0.033281446", "1.01"))

    def test_duplicate_note_and_chronology_rejected(self):
        with self.assertRaisesRegex(ValueError, "idyom_duplicate_note_id"):
            self.parse(FIRST, FIRST)
        with self.assertRaisesRegex(ValueError, "idyom_nonmonotonic_onsets"):
            self.parse(SECOND, FIRST)

    def test_mismatched_row_and_unclosed_quotes_rejected(self):
        with self.assertRaisesRegex(ValueError, "idyom_field_count_mismatch"):
            self.parse("42 1 1")
        with self.assertRaisesRegex(ValueError, "idyom_invalid_quoted_fields"):
            self.parse(FIRST.replace('"Nocturne in C"', '"Nocturne in C'))

    def test_missing_pair_or_identity_rejected(self):
        with self.assertRaisesRegex(ValueError, "idyom_missing_entropy_column"):
            self.file.write_text(HEADER.replace("cpitch.entropy", "BAD") + "\n" + FIRST + "\n")
            read_idyom_dat(self.file)
        with self.assertRaisesRegex(ValueError, "idyom_missing_columns"):
            self.file.write_text("melody.id note.id onset information.content entropy\n1 1 0 2 2\n")
            read_idyom_dat(self.file)

    def test_bounds_and_empty(self):
        self.parse(FIRST, SECOND)
        with self.assertRaisesRegex(ValueError, "over_event_limit"):
            read_idyom_dat(self.file, max_events=1)
        with self.assertRaisesRegex(ValueError, "over_size_limit"):
            read_idyom_dat(self.file, max_bytes=20)
        with self.assertRaisesRegex(ValueError, "invalid_event_limit"):
            read_idyom_dat(self.file, max_events=0)
        self.file.write_text(HEADER + "\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "idyom_dat_no_events"):
            read_idyom_dat(self.file)


if __name__ == "__main__":
    unittest.main()
