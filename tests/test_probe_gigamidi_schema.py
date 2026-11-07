import unittest

from scripts.probe_gigamidi_schema import summarize


class SchemaProbeTests(unittest.TestCase):
    def test_schema_without_values(self):
        result = summarize({
            "features": [{"name": "md5"}, {"name": "music"}],
            "rows": [{"row": {"md5": "secret-value", "music": "midi-binary-payload"}}],
            "num_rows_total": 2,
            "partial": False,
        }, 190)
        self.assertEqual(result["row_count"], 1)
        self.assertEqual(result["feature_names"], ["md5", "music"])
        self.assertNotIn("secret-value", str(result))
        self.assertNotIn("midi-binary-payload", str(result))


if __name__ == "__main__":
    unittest.main()
