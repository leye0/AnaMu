import unittest
import urllib.error

from scripts.probe_hf_lookup import classify_error


class LookupTests(unittest.TestCase):
    def test_error_types_do_not_expose_urls_or_token(self):
        error = urllib.error.HTTPError("https://example.invalid/?token=secret", 403, "denied", None, None)
        self.assertEqual(classify_error(error), "http_403")
        self.assertEqual(classify_error(TimeoutError("token is secret")), "TimeoutError")


if __name__ == "__main__":
    unittest.main()
