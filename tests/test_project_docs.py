import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_project_docs import (
    agent_onboarding_issues,
    berklee_grid_issues,
    broken_local_links,
    course_material_progress_issues,
    legacy_mission_issues,
    mcgill_catalog_issues,
    optional_knowledge_issues,
    university_catalog_issues,
    university_coverage_issues,
)


class DocumentationLinkTests(unittest.TestCase):
    def test_course_tracker_covers_all_named_courses_and_links_material(self):
        root = Path(__file__).resolve().parents[1]
        sources = {
            "udem": "udem-composition-a26.json",
            "mcgill": "mcgill-composition-2026.json",
            "berklee": "berklee-composition-2026f.json",
            "optional": "optional-knowledge-seeds-2026.json",
        }
        catalogs = {key: json.loads((root / "docs/data" / filename).read_text(encoding="utf-8"))
                    for key, filename in sources.items()}
        progress = json.loads((root / "docs/data/course-material-progress.json")
                              .read_text(encoding="utf-8"))
        self.assertEqual(course_material_progress_issues(progress, catalogs, root), [])
        self.assertEqual(sum(len(rows) for rows in progress["courses"].values()), 332)
        progress["courses"]["udem"].pop("MCT 1601")
        self.assertTrue(any("udem" in issue for issue in
                            course_material_progress_issues(progress, catalogs, root)))

    def test_only_course_collection_is_active_and_old_campaign_docs_are_absent(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(legacy_mission_issues(root), [])
        for relpath in ("README.md", "docs/OBJECTIVES.md", "docs/course-material-collection.md"):
            text = (root / relpath).read_text(encoding="utf-8")
            self.assertIn("cours", text)

    def test_old_experimental_direction_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("PIAST mysterious", encoding="utf-8")
            self.assertTrue(any("retired research direction" in issue
                                for issue in legacy_mission_issues(root)))

    def test_fresh_agent_finds_academic_knowledge_mission_and_documents(self):
        root = Path(__file__).resolve().parents[1]
        text = (root / "AGENTS.md").read_text(encoding="utf-8")
        self.assertEqual(agent_onboarding_issues(text), [])
        knowledge = (root / "docs/knowledge-base.md").read_text(encoding="utf-8")
        self.assertIn("base de concepts réconciliés", knowledge)
        self.assertIn("reste à construire", " ".join(knowledge.split()))

    def test_fresh_agent_contract_cannot_lose_key_navigation(self):
        root = Path(__file__).resolve().parents[1]
        text = (root / "AGENTS.md").read_text(encoding="utf-8")
        altered = text.replace("](docs/knowledge-base.md)", "](somewhere-else.md)")
        self.assertTrue(any("docs/knowledge-base.md" in issue
                            for issue in agent_onboarding_issues(altered)))

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

    def test_optional_course_union_is_an_explicit_gate(self):
        root = Path(__file__).resolve().parents[1]
        text = (root / "docs/todo-university-coverage.md").read_text(encoding="utf-8")
        for marker in ("A13", "A14", "A15", "A16", "A17", "A18"):
            self.assertIn(f"- [ ] {marker}", text)
        altered = text.replace("- [ ] A13", "- [ ] Z13", 1)
        self.assertTrue(any("A13" in issue for issue in university_coverage_issues(altered)))

    def test_udem_public_catalog_census_is_complete_and_explicitly_unreviewed(self):
        root = Path(__file__).resolve().parents[1]
        catalog = json.loads((root / "docs/data/udem-composition-a26.json")
                             .read_text(encoding="utf-8"))
        self.assertEqual(university_catalog_issues(catalog), [])
        courses = {course["code"]: course for course in catalog["courses"]}
        self.assertEqual(courses["MTE 12041"]["credits"], 0)
        self.assertEqual(courses["MTE 2114"]["block"], "75A")
        self.assertEqual(courses["MUS 3127X"]["block"], "75F")
        self.assertEqual(courses["EMU 1310"]["block"], "75H")

    def test_udem_catalog_cannot_lose_a_required_course(self):
        root = Path(__file__).resolve().parents[1]
        catalog = json.loads((root / "docs/data/udem-composition-a26.json")
                             .read_text(encoding="utf-8"))
        catalog["courses"] = [c for c in catalog["courses"] if c["code"] != "MTE 2114"]
        self.assertTrue(any("22 courses / 63 credits" in issue
                            for issue in university_catalog_issues(catalog)))

    def test_mcgill_program_credit_structure_and_named_options(self):
        root = Path(__file__).resolve().parents[1]
        catalog = json.loads((root / "docs/data/mcgill-composition-2026.json")
                             .read_text(encoding="utf-8"))
        self.assertEqual(mcgill_catalog_issues(catalog), [])
        courses = {c["code"]: c for c in catalog["courses"]}
        self.assertEqual(courses["MUCO 460"]["category"], "required")
        self.assertEqual(courses["MUTH 202"]["category"], "complementary")
        self.assertEqual(courses["MUTH 204"]["category"], "complementary")
        self.assertEqual(courses["MUTH 528"]["category"], "recommended")

    def test_mcgill_program_detects_lost_required_or_option_credit(self):
        root = Path(__file__).resolve().parents[1]
        catalog = json.loads((root / "docs/data/mcgill-composition-2026.json")
                             .read_text(encoding="utf-8"))
        catalog["requirements"]["complementary_credits"] = 12
        self.assertTrue(any("124" in issue for issue in mcgill_catalog_issues(catalog)))

    def test_berklee_current_grid_is_not_2024_sample_curriculum(self):
        root = Path(__file__).resolve().parents[1]
        catalog = json.loads((root / "docs/data/berklee-composition-2026f.json")
                             .read_text(encoding="utf-8"))
        self.assertEqual(berklee_grid_issues(catalog), [])
        self.assertEqual(catalog["catalog_year"], "2026F")
        self.assertIn("registrar/major-grids-search", catalog["source_index_url"])

    def test_berklee_detects_missing_portfolio_and_altered_group_credit(self):
        root = Path(__file__).resolve().parents[1]
        catalog = json.loads((root / "docs/data/berklee-composition-2026f.json")
                             .read_text(encoding="utf-8"))
        catalog["groups"][0]["requirements"] = [r for r in catalog["groups"][0]["requirements"]
                                               if r["rule"] != "required_uncredited_portfolio"]
        self.assertTrue(any("portfolio" in issue for issue in berklee_grid_issues(catalog)))

    def test_berklee_open_elective_pools_cannot_disappear(self):
        root = Path(__file__).resolve().parents[1]
        catalog = json.loads((root / "docs/data/berklee-composition-2026f.json")
                             .read_text(encoding="utf-8"))
        for group in catalog["groups"]:
            group["requirements"] = [r for r in group["requirements"]
                                      if r.get("rule") != "credit_pool"]
        issues = berklee_grid_issues(catalog)
        self.assertTrue(any("eight major elective credits" in issue for issue in issues))
        self.assertTrue(any("seven general elective credits" in issue for issue in issues))

    def test_optional_knowledge_seeds_have_primary_sources_and_live_todo_targets(self):
        root = Path(__file__).resolve().parents[1]
        register = json.loads((root / "docs/data/optional-knowledge-seeds-2026.json")
                              .read_text(encoding="utf-8"))
        mcgill = json.loads((root / "docs/data/mcgill-composition-2026.json")
                            .read_text(encoding="utf-8"))
        todo = (root / "docs/todo-university-coverage.md").read_text(encoding="utf-8")
        self.assertEqual(optional_knowledge_issues(register, todo, mcgill), [])
        self.assertEqual(len(register["candidates"]), 30)

    def test_optional_knowledge_does_not_assume_adjacent_major_admissibility(self):
        root = Path(__file__).resolve().parents[1]
        register = json.loads((root / "docs/data/optional-knowledge-seeds-2026.json")
                              .read_text(encoding="utf-8"))
        todo = (root / "docs/todo-university-coverage.md").read_text(encoding="utf-8")
        entry = next(c for c in register["candidates"] if c["code"] == "FILM-205")
        entry["relation_to_baseline"] = "required_composition_course"
        issues = optional_knowledge_issues(register, todo)
        self.assertTrue(any("adjacent major eligibility unverified" in issue for issue in issues))


if __name__ == "__main__":
    unittest.main()
