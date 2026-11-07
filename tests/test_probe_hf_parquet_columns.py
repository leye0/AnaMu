import io
import unittest

from scripts.probe_hf_parquet_columns import BudgetFile, safe_error_detail


class ParquetColumnBudgetTests(unittest.TestCase):
    def test_seeks_and_bounded_reads(self):
        file = BudgetFile(io.BytesIO(b"1234567890"), limit=5)
        file.seek(5)
        self.assertEqual(file.read(3), b"678")
        with self.assertRaisesRegex(ValueError, "budget"):
            file.read(3)
        file.seek(0)
        self.assertEqual(file.read(2), b"12")
        self.assertEqual(file.read_bytes, 5)
        self.assertFalse(file.closed)
        file.close()
        self.assertTrue(file.closed)

    def test_refuse_unbounded_read(self):
        file = BudgetFile(io.BytesIO(b"data"), limit=12)
        with self.assertRaisesRegex(ValueError, "budget"):
            file.read()

    def test_redact_signed_urls_and_credentials(self):
        info = safe_error_detail(ValueError("Bad https://example.com/object?signature=abcdef secret-token"),
                                 "secret-token")
        self.assertNotIn("example.com", info)
        self.assertNotIn("secret-token", info)


if __name__ == "__main__":
    unittest.main()
