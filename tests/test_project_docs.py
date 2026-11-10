import tempfile
import unittest
from pathlib import Path

from scripts.validate_project_docs import broken_local_links


class DocumentationLinkTests(unittest.TestCase):
    def test_local_links_are_checked_but_external_links_are_not(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "valid.md").write_text("# valid", encoding="utf-8")
            source = root / "index.md"
            source.write_text("[ok](valid.md) [bad](missing.md) "
                              "[web](https://example.org/path) [anchor](#x)",
                              encoding="utf-8")
            self.assertEqual(len(broken_local_links(source)), 1)
            self.assertIn("missing.md", broken_local_links(source)[0])


if __name__ == "__main__":
    unittest.main()
