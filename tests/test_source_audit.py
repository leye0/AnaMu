import unittest

from scripts.source_audit import summarize_hf, summarize_zenodo


class SourceAuditTests(unittest.TestCase):
    def test_hf_gate_and_parquet(self):
        data = summarize_hf({
            "id": "Metacreation/GigaMIDI",
            "gated": "auto",
            "cardData": {"license": "cc-by-nc-4.0"},
            "siblings": [{"rfilename": "v2.0.0/train/00001.parquet"}],
        })
        self.assertEqual(data["gated"], "auto")
        self.assertTrue(data["has_parquet"])
        self.assertEqual(data["license"], "cc-by-nc-4.0")

    def test_zenodo_does_not_emit_file_links(self):
        data = summarize_zenodo({
            "id": 123,
            "access": {"record": "public", "files": "restricted"},
            "files": [{"key": "test.zip", "size": 50, "links": {"self": "hidden"}}],
        })
        self.assertEqual(data["files"], [{"name": "test.zip", "size": 50}])
        self.assertNotIn("hidden", str(data))


if __name__ == "__main__":
    unittest.main()
