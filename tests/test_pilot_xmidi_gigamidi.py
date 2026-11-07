import io
import unittest
import zipfile

from scripts.pilot_xmidi_gigamidi import labels_from_filename, select_entries


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


if __name__ == "__main__":
    unittest.main()
