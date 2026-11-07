import unittest

from scripts.probe_gigamidi_csv_header import parse_header


class CsvHeaderProbeTests(unittest.TestCase):
    def test_header_only(self):
        content = b'file_path,"recording,title",md5\nsecret song,private title,abcdef\n'
        self.assertEqual(parse_header(content), ["file_path", "recording,title", "md5"])
        self.assertNotIn("secret song", str(parse_header(content)))


if __name__ == "__main__":
    unittest.main()
