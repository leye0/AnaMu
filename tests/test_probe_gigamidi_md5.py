import base64
import hashlib
import unittest

from scripts.probe_gigamidi_md5 import embedded_midi, summarize_row


class Md5ProbeTests(unittest.TestCase):
    def test_matching_midi_without_leaking_values(self):
        midi = b"MThd\x00\x00\x00\x06example"
        secret_hash = hashlib.md5(midi).hexdigest()
        result = summarize_row({"rows": [{"row": {
            "music": {"bytes": base64.b64encode(midi).decode(), "path": "/private"},
            "md5": secret_hash,
            "title": "unpublished-title",
        }}]}, 99, 0)
        self.assertTrue(result["hash_matches_embedded_midi"])
        self.assertEqual(result["embedded_midi_bytes"], len(midi))
        self.assertNotIn(secret_hash, str(result))
        self.assertNotIn("unpublished-title", str(result))
        self.assertNotIn("/private", str(result))

    def test_mismatching_midi(self):
        midi = b"MThd\x00\x00\x00\x06example"
        result = summarize_row({"rows": [{"row": {
            "music": {"bytes": base64.b64encode(midi).decode()}, "md5": "0" * 32,
        }}]}, 99, 1000)
        self.assertFalse(result["hash_matches_embedded_midi"])

    def test_unknown_representation_is_not_a_false_negative(self):
        self.assertEqual(embedded_midi({"src": "https://example.invalid"}),
                         (None, "music_object_without_embedded_base64"))
        result = summarize_row({"rows": [{"row": {
            "music": {"src": "https://example.invalid"}, "md5": "0" * 32,
        }}]}, 99, 10000)
        self.assertIsNone(result["hash_matches_embedded_midi"])


if __name__ == "__main__":
    unittest.main()
