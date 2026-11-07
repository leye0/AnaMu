import io
import unittest
import zipfile

from scripts.pilot_xmidi_gigamidi import RangeFile, labels_from_filename, select_entries


class PilotTests(unittest.TestCase):
    def test_labels(self):
        self.assertEqual(labels_from_filename("folder/XMIDI_Happy_Pop_abcd1234.midi"),
                         {"emotion": "Happy", "genre": "Pop"})
        self.assertEqual(labels_from_filename("random.mid"),
                         {"emotion": None, "genre": None})

    def test_bounded_deterministic_selection(self):
        inmem = io.BytesIO()
        with zipfile.ZipFile(inmem, "w", compression=zipfile.ZIP_DEFLATED) as z:
            for i in range(12):
                z.writestr(f"XMIDI_Happy_Pop_{i:08d}.midi", b"MThd" + b"0" * 200)
        with zipfile.ZipFile(inmem) as z:
            count, selected = select_entries(z.infolist())
            self.assertEqual(count, 12)
            self.assertEqual(len(selected), 3)
            self.assertEqual([i.filename for i in selected],
                             [i.filename for i in select_entries(z.infolist())[1]])

    def test_zipfile_can_read_via_seekable_rangefile(self):
        inmem = io.BytesIO()
        with zipfile.ZipFile(inmem, "w", compression=zipfile.ZIP_DEFLATED) as z:
            z.writestr("XMIDI_Happy_Pop_12345678.midi", b"MThd" + b"0" * 200)
        data = inmem.getvalue()
        remote = RangeFile.__new__(RangeFile)
        remote.pos = 0
        remote.total_size = len(data)
        remote._get_range = lambda first, last: data[first:last + 1]
        with zipfile.ZipFile(remote) as z:
            self.assertTrue(remote.seekable())
            self.assertEqual(z.read("XMIDI_Happy_Pop_12345678.midi"), b"MThd" + b"0" * 200)


if __name__ == "__main__":
    unittest.main()
