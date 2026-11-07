import unittest

from scripts.probe_xmidi_range import summarize


class XmidiRangeProbeTests(unittest.TestCase):
    def test_partial_content_zip_footer(self):
        result = summarize(206, {
            "Content-Type": "application/zip", "Content-Range": "bytes 900-999/1000",
            "Content-Length": "100",
        }, b"abcPK\x05\x06xyz", "https://drive.google.com/download?id=private", "test")
        self.assertTrue(result["suffix_range_honored"])
        self.assertTrue(result["zip_end_marker_present"])
        self.assertEqual(result["final_host"], "drive.google.com")
        self.assertNotIn("private", str(result))

    def test_html_no_range(self):
        result = summarize(200, {"Content-Type": "text/html"}, b"<html></html>",
                           "https://drive.usercontent.google.com/uc", "test")
        self.assertFalse(result["suffix_range_honored"])
        self.assertFalse(result["zip_end_marker_present"])


if __name__ == "__main__":
    unittest.main()
