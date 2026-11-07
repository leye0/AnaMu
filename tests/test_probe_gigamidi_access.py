import unittest

from scripts.probe_gigamidi_access import classify_status


class AccessProbeTests(unittest.TestCase):
    def test_redirect_indicates_possible_file_access(self):
        self.assertEqual(classify_status(302), "accessible_or_redirected_to_file")

    def test_rejection_and_missing_file_are_not_success(self):
        self.assertEqual(classify_status(401), "access_denied")
        self.assertEqual(classify_status(403), "access_denied")
        self.assertEqual(classify_status(404), "file_not_found")


if __name__ == "__main__":
    unittest.main()
