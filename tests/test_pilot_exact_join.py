import io
import unittest
import zipfile
from unittest.mock import patch

from scripts.pilot_exact_join import optional_matching_metadata, sample_hashes, scan_groups


class FakeColumn:
    def __init__(self, values):
        self.values = values

    def to_pylist(self):
        return self.values


class FakeTable:
    def __init__(self, columns):
        self.columns = columns

    def column(self, name):
        return FakeColumn(self.columns[name])


class FakeParquet:
    def __init__(self, groups):
        self.groups = groups
        self.num_row_groups = len(groups)
        self.schema_arrow = type("Schema", (), {"names": ["md5"]})()
        self.requests = []

    def read_row_group(self, index, columns, use_threads):
        self.requests.append((index, columns, use_threads))
        return FakeTable({name: self.groups[index][name] for name in columns})


class JoinPilotTests(unittest.TestCase):
    def test_samples_hashed_in_memory_and_human_label_kept(self):
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("XMIDI_Sad_Rock_00000001.mid", b"MThd" + b"x" * 300)
            archive.writestr("XMIDI_Happy_Pop_00000002.mid", b"MThd" + b"y" * 300)
            archive.writestr("XMIDI_Happy_Pop_00000003.mid", b"oops" + b"z" * 300)
        with zipfile.ZipFile(buf) as archive:
            candidates, report = sample_hashes(archive)
        self.assertEqual(report["selected_entries"], 3)
        self.assertEqual(report["valid_midi_headers"], 2)
        self.assertEqual(len(candidates), 2)
        self.assertEqual({r["emotion"] for r in candidates.values()}, {"Sad", "Happy"})

    def test_exact_match_stops_reading_groups(self):
        target = "f" * 32
        parquet = FakeParquet([{"md5": ["a" * 32]},
                               {"md5": ["b" * 32, target]},
                               {"md5": ["c" * 32]}])
        with patch("scripts.pilot_exact_join.time.monotonic", return_value=0):
            result = scan_groups(parquet, {target: {"emotion": "Happy"}}, deadline=100)
        self.assertEqual(result["status"], "exact_md5_match")
        self.assertEqual(result["groups_read"], 2)
        self.assertEqual(result["md5_rows_examined"], 3)
        self.assertEqual(result["match"]["row_in_group"], 1)
        self.assertEqual(parquet.requests, [(0, ["md5"], False), (1, ["md5"], False)])
        self.assertNotIn(target, str(result))

    def test_no_match_is_not_global_negative(self):
        parquet = FakeParquet([{"md5": ["a" * 32]}])
        with patch("scripts.pilot_exact_join.time.monotonic", return_value=0):
            result = scan_groups(parquet, {"b" * 32: {}}, deadline=100)
        self.assertEqual(result["status"], "no_match_in_one_shard")

    def test_deadline_interrupts_without_extra_reads(self):
        parquet = FakeParquet([{"md5": []}])
        with patch("scripts.pilot_exact_join.time.monotonic", return_value=100):
            result = scan_groups(parquet, {}, deadline=100)
        self.assertEqual(result["status"], "time_budget_exceeded")
        self.assertEqual(parquet.requests, [])

    def test_optional_metadata_requests_only_named_columns(self):
        parquet = FakeParquet([{"title": ["Song"], "md5": ["a" * 32]}])
        parquet.schema_arrow.names = ["title", "md5", "music"]
        table = FakeTable({"title": ["Song"]})
        table.column = lambda name: type("Array", (), {
            "__getitem__": lambda self, ix: type("Scalar", (), {"as_py": lambda self: "Song"})()
        })()
        parquet.read_row_group = lambda index, columns, use_threads: (
            parquet.requests.append((index, columns, use_threads)) or table)
        details = optional_matching_metadata(parquet, {"row_group": 0, "row_in_group": 0})
        self.assertEqual(details, {"title": "Song"})
        self.assertEqual(parquet.requests, [(0, ["title"], False)])


if __name__ == "__main__":
    unittest.main()
