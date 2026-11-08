"""Inspect schema safely without requiring Zenodo or real copyrighted MIDI."""

import io
import unittest
import zipfile

from scripts.inspect_emopia_votes import inspect_archive


class EMOPIASchemaTests(unittest.TestCase):
    @staticmethod
    def _zip(add_midi=True):
        output = io.BytesIO()
        with zipfile.ZipFile(output, "w") as archive:
            archive.writestr("EMOPIA_2.2/tagging_lists/A.csv", "clip,score\na,1\n")
            archive.writestr("EMOPIA_2.2/label.csv", "clip,quadrant\na,Q1\n")
            if add_midi:
                archive.writestr("EMOPIA_2.2/midis/A.mid", b"MThd" + bytes(40))
        return output.getvalue()

    def test_schema_only_and_no_midi_contents(self):
        outcome = inspect_archive(self._zip())
        self.assertEqual(outcome["midi_files"], 1)
        self.assertEqual(outcome["raw_tag_files"], 1)
        self.assertEqual(outcome["label_csv_files"], 1)
        self.assertNotIn("MThd", str(outcome))

    def test_reject_missing_midi(self):
        with self.assertRaisesRegex(AssertionError, "missing_raw_tags_midis_or_label_csv"):
            inspect_archive(self._zip(add_midi=False))


if __name__ == "__main__":
    unittest.main()
