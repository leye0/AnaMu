import tempfile
import unittest
from pathlib import Path

from scripts.validate_project_docs import broken_local_links, university_coverage_issues


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

    def test_real_university_checklist_is_structurally_consistent(self):
        root = Path(__file__).resolve().parents[1]
        text = (root / "docs/todo-university-coverage.md").read_text(encoding="utf-8")
        self.assertEqual(university_coverage_issues(text), [])

    def test_checklist_requires_evidence_before_checking(self):
        root = Path(__file__).resolve().parents[1]
        text = (root / "docs/todo-university-coverage.md").read_text(encoding="utf-8")
        modified = text.replace("- [ ] C01", "- [x] C01", 1)
        self.assertTrue(any("C01: checked without linked evidence" in issue
                            for issue in university_coverage_issues(modified)))

    def test_composition_gate_rejects_partial_academic_coverage(self):
        root = Path(__file__).resolve().parents[1]
        text = (root / "docs/todo-university-coverage.md").read_text(encoding="utf-8")
        modified = text.replace("- [ ] L05", "- [x] L05", 1)
        self.assertTrue(any("composition gate L cannot open" in issue
                            for issue in university_coverage_issues(modified)))


if __name__ == "__main__":
    unittest.main()
