import unittest

from scripts.probe_gigamidi_csv_header import parse_header, summarize_paths


class CsvHeaderProbeTests(unittest.TestCase):
    def test_header_only(self):
        content = b'file_path,"recording,title",md5\nsecret song,private title,abcdef\n'
        self.assertEqual(parse_header(content), ["file_path", "recording,title", "md5"])
        self.assertNotIn("secret song", str(parse_header(content)))

    def test_classify_path_shapes_without_logging_values(self):
        content = (b"file_path,md5,title\n"
                   b"XMIDI_sad_rock_12345678.midi,0123456789abcdef0123456789abcdef,secret song\n"
                   b"collection/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.mid,aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa,private title\n")
        report = summarize_paths(content)
        self.assertEqual(report["rows_examined"], 2)
        self.assertEqual(report["file_path_basename_patterns"]["xmidi_labeled_basename"], 1)
        self.assertEqual(report["md5_matches_filename"], 1)
        self.assertNotIn("private title", str(report))
        self.assertNotIn("12345678", str(report))


if __name__ == "__main__":
    unittest.main()
