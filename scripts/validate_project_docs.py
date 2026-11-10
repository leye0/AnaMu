"""Validate academic source inventories and the sole course-collection workflow.

The scanner checks local Markdown destinations (not HTTP targets or anchors).
It does not pretend to be a complete Markdown parser.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
CURRICULUM_ITEM = re.compile(r"^- \[([ xX])\] ([A-L]\d{2})\b(.*)$", re.MULTILINE)
RETIRED_DIRECTION = re.compile(r"(?i)\b(?:piast|emopia|vgmidi|mysterious|mystérieux)\b")
RETIRED_FILES = (
    "docs/studies", "docs/roadmap.md", "docs/research-evidence-gates.md",
    "docs/music-grammar-research-program.md", "docs/composition-grammar.md",
    "docs/orchestral-corpus-audit.md",
)


def university_catalog_issues(catalog: dict) -> list[str]:
    """Validate the catalog census, without mistaking it for syllabus coverage."""
    issues: list[str] = []
    courses = catalog.get("courses", [])
    blocks = catalog.get("blocks", [])
    codes = [c.get("code") for c in courses]
    if len(courses) != 190 or len(set(codes)) != len(codes):
        issues.append("UdeM A26 catalog must have 190 uniquely identified courses")
    if not all(c.get("title") and c.get("block") and isinstance(c.get("credits"), (int, float))
               and c["credits"] >= 0 for c in courses):
        issues.append("UdeM catalog has missing titles, blocks or invalid credits")
    if {b.get("code") for b in blocks} != {f"75{c}" for c in "ABCDEFGH"}:
        issues.append("UdeM catalog must account for blocks 75A–75H")
    for block in blocks:
        if block.get("listed_courses") != sum(c.get("block") == block.get("code") for c in courses):
            issues.append(f"{block.get('code')}: course count differs from catalog inventory")
    mandatory = [c for c in courses if c.get("block") == "75A"]
    if len(mandatory) != 22 or sum(c.get("credits", 0) for c in mandatory) != 63:
        issues.append("UdeM mandatory inventory must contain 22 courses / 63 credits")
    if len([c for c in courses if c.get("block") != "75A"]) != 168:
        issues.append("UdeM 168 optional course choices must remain available for knowledge review")
    if catalog.get("mandatory_credits") != 63 or catalog.get("total_credits") != 90:
        issues.append("UdeM published credit requirements are inconsistent")
    if catalog.get("status") != "public_catalog_course_inventory_only_syllabi_not_audited":
        issues.append("UdeM catalog must not masquerade as a syllabus audit")
    if not (catalog.get("source_url") or "").startswith(
            "https://admission.umontreal.ca/programmes/baccalaureat-en-musique-composition/"):
        issues.append("UdeM catalog missing its official source URL")
    return issues


def mcgill_catalog_issues(catalog: dict) -> list[str]:
    """Check the published 124-credit course/choice structure, not mastery."""
    issues: list[str] = []
    credits = catalog.get("requirements", {})
    if sum(credits.get(k, 0) for k in
           ("foundation_credits", "required_credits", "complementary_credits",
            "elective_credits")) != 124 or catalog.get("total_credits") != 124:
        issues.append("McGill program credit blocks do not sum to 124")
    if (credits.get("foundation_listed_prerequisite_credits") != 22
            or credits.get("foundation_large_ensemble_credits") != 4
            or credits.get("foundation_non_music_electives_credits") != 6):
        issues.append("McGill 32-credit foundation subgroups do not match the catalog")
    if (credits.get("complementary_music_theory_credits") != 3
            or credits.get("complementary_music_history_credits") != 6
            or credits.get("complementary_ensemble_credits") != 4):
        issues.append("McGill complementary choices do not sum to 13")
    courses = catalog.get("courses", [])
    if len(courses) != 58 or len({c.get("code") for c in courses}) != len(courses):
        issues.append("McGill catalog must have 58 distinct named course choices")
    for name, expected_count, expected_credits in (
            ("foundation", 10, 22), ("required", 25, 61),
            ("complementary", 15, 35), ("recommended", 8, 24)):
        subset = [c for c in courses if c.get("category") == name]
        if len(subset) != expected_count or sum(c.get("credits", 0) for c in subset) != expected_credits:
            issues.append(f"McGill {name}: course count/credits differ from the catalog")
    if not all(c.get("title") for c in courses if c.get("category") in ("complementary", "recommended")):
        issues.append("McGill complementary and recommended learning options require course titles")
    if catalog.get("status") != "public_program_requirement_list_only_syllabi_not_audited":
        issues.append("McGill named-course inventory must not claim syllabus validation")
    return issues


def berklee_grid_issues(catalog: dict) -> list[str]:
    """Verify the current grid's required credit buckets and alternatives."""
    issues: list[str] = []
    groups = catalog.get("groups", [])
    expected = {"major": 32, "major_specific_core_and_liberal_arts": 22,
                "core_music": 35, "liberal_arts_and_africana_studies": 24,
                "general_electives": 7}
    if {g.get("code"): g.get("credits") for g in groups} != expected:
        issues.append("Berklee 2026F group credits differ from official grid")
    if catalog.get("catalog_year") != "2026F" or catalog.get("total_credits") != 120:
        issues.append("Berklee catalog year/total is not the 2026F 120-credit degree")
    requirements = [r for g in groups for r in g.get("requirements", [])]
    if len(requirements) != 44:
        issues.append("Berklee 2026F grid should have 44 documented requirement lines")
    for g in groups:
        if sum(r.get("credits", 0) for r in g.get("requirements", [])) != g.get("credits"):
            issues.append(f"Berklee {g.get('code')}: requirements do not sum to group credits")
    if not any(r.get("rule") == "required_uncredited_portfolio" and r.get("credits") == 0
               for r in requirements):
        issues.append("Berklee mandatory uncredited composition portfolio missing")
    major = next((g for g in groups if g.get("code") == "major"), {})
    electives = next((g for g in groups if g.get("code") == "general_electives"), {})
    if not any(r.get("rule") == "credit_pool" and r.get("credits") == 8
               for r in major.get("requirements", [])):
        issues.append("Berklee eight major elective credits must remain visible for further inventory")
    if not any(r.get("rule") == "credit_pool" and r.get("credits") == 7
               for r in electives.get("requirements", [])):
        issues.append("Berklee seven general elective credits must remain visible for further inventory")
    if catalog.get("status") != "official_credit_grid_only_course_family_choices_and_detailed_syllabi_not_audited":
        issues.append("Berklee grid must not claim complete course/syllabus coverage")
    return issues


def university_coverage_issues(todo_text: str) -> list[str]:
    """Catch accidental completion or erosion of the academic coverage gate."""
    issues: list[str] = []
    items = CURRICULUM_ITEM.findall(todo_text)
    codes = [code for _, code, _ in items]
    if len(codes) != len(set(codes)):
        issues.append("university TODO has duplicate checkbox identifiers")
    families = {code[0] for code in codes}
    if families != set("ABCDEFGHIJKL"):
        issues.append(f"university TODO families incomplete: {sorted(set('ABCDEFGHIJKL') - families)}")
    for checked, code, description in items:
        if checked.strip() and not re.search(r"\[[^\]]+\]\([^)]+\)", description):
            issues.append(f"{code}: checked without linked evidence dossier")
    if any(checked.strip() for checked, code, _ in items if code == "L05"):
        if any(not checked.strip() for checked, _, _ in items):
            issues.append("university composition gate L cannot open with unchecked competencies")
    for course in ("MTE 2114", "MUCO 460", "CM-441"):
        if course not in todo_text:
            issues.append(f"university TODO missing curriculum anchor: {course}")
    for code in ("A13", "A14", "A15", "A16", "A17", "A18"):
        if code not in codes:
            issues.append(f"university TODO missing academic knowledge-base gate: {code}")
    if "K13" not in codes:
        issues.append("university TODO missing knowledge-to-analysis integration gate: K13")
    return issues


def agent_onboarding_issues(text: str) -> list[str]:
    """Guard the standalone onboarding contract against mission drift."""
    issues: list[str] = []
    required_links = ("README.md", "docs/OBJECTIVES.md", "docs/knowledge-base.md",
                      "docs/university-curriculum.md", "docs/course-material-collection.md",
                      "docs/todo-university-coverage.md")
    for path in required_links:
        if f"]({path})" not in text:
            issues.append(f"agent onboarding missing canonical document: {path}")
    for concept in ("base unifiée de connaissances", "programmes universitaires",
                    "analyser", "composer", "optionnels", "L01–L05", "MIDI"):
        if concept not in text:
            issues.append(f"agent onboarding missing mission guardrail: {concept}")
    return issues


def legacy_mission_issues(root: Path) -> list[str]:
    """Prevent retired, non-curricular experiments re-entering the active project."""
    issues = [f"retired project path still present: {path}"
              for path in RETIRED_FILES if (root / path).exists()]
    for doc in (root / "README.md", root / "AGENTS.md", *((root / "docs").rglob("*.md"))):
        if doc.is_file() and RETIRED_DIRECTION.search(doc.read_text(encoding="utf-8")):
            issues.append(f"retired research direction mentioned in active doc: {doc}")
    return issues


def course_material_progress_issues(progress: dict, catalogs: dict[str, dict],
                                    root: Path) -> list[str]:
    """Keep the course-by-course documentation queue in sync with catalog names."""
    issues: list[str] = []
    if progress.get("phase") != "course_material_collection":
        issues.append("course material tracker must remain in collection phase")
    tracked = progress.get("courses", {})
    expected = {
        "udem": {c["code"] for c in catalogs["udem"]["courses"]},
        "mcgill": {c["code"] for c in catalogs["mcgill"]["courses"]},
        "berklee": {code for group in catalogs["berklee"]["groups"]
                    for requirement in group["requirements"]
                    for code in requirement.get("codes", [])},
    }
    for entry in catalogs["optional"]["candidates"]:
        if entry["institution"] == "McGill":
            expected["mcgill"].add(entry["code"])
        elif entry["institution"] == "Berklee":
            expected["berklee"].add(entry["code"])
    for program, codes in expected.items():
        rows = tracked.get(program, {})
        missing = codes - set(rows)
        if missing:
            issues.append(f"{program}: {len(missing)} catalog courses not in material tracker")
        for code, record in rows.items():
            status = record.get("status") if isinstance(record, dict) else None
            if status not in ("catalog_only", "partially_documented",
                              "syllabus_documented", "blocked"):
                issues.append(f"{program} {code}: unknown material status")
                continue
            relative_path = record.get("material_file")
            if status != "catalog_only" and not relative_path:
                issues.append(f"{program} {code}: progress without cited material file")
            if relative_path:
                candidate = (root / relative_path).resolve()
                if (not candidate.is_relative_to(root.resolve()) or
                        not candidate.is_file() or candidate.suffix != ".md"):
                    issues.append(f"{program} {code}: missing or invalid material file")
    if not progress.get("unresolved_course_pools"):
        issues.append("course material tracker hides unresolved elective pools")
    return issues


def optional_knowledge_issues(register: dict, todo_text: str,
                              mcgill_catalog: dict | None = None) -> list[str]:
    """Check that optional teaching is traceable, not falsely treated as a degree or validated."""
    issues: list[str] = []
    if register.get("status") != "public_course_descriptions_only_not_syllabi_or_analytical_coverage":
        issues.append("optional knowledge register must explicitly remain unvalidated")
    source_urls = register.get("sources", {})
    for name, url in source_urls.items():
        if urlsplit(url).hostname not in ("www.mcgill.ca", "college.berklee.edu"):
            issues.append(f"optional knowledge source {name} must be an official university page")
    entries = register.get("candidates", [])
    counts = {
        "mcgill_recommended": 8,
        "berklee_composition_department": 5,
        "berklee_jazz_department": 9,
        "berklee_screen_scoring_department": 8,
    }
    for source, minimum in counts.items():
        if sum(c.get("source") == source for c in entries) < minimum:
            issues.append(f"optional knowledge source {source}: missing discovered teaching")
    todo_ids = {code for _, code, _ in CURRICULUM_ITEM.findall(todo_text)}
    seen: set[tuple[str, str]] = set()
    for entry in entries:
        key = (entry.get("institution", ""), entry.get("code", ""))
        if key in seen or not all(key):
            issues.append(f"optional knowledge duplicate or unidentified course: {key}")
        seen.add(key)
        if (not entry.get("title") or not entry.get("knowledge_increment")
                or entry.get("source") not in source_urls):
            issues.append(f"optional knowledge entry {key}: missing title, source or contribution")
        if not entry.get("todo_ids") or set(entry["todo_ids"]) - todo_ids:
            issues.append(f"optional knowledge entry {key}: missing or unknown TODO mapping")
        if entry.get("source") in ("berklee_jazz_department", "berklee_screen_scoring_department"):
            if not entry.get("relation_to_baseline", "").startswith("adjacent_"):
                issues.append(f"optional knowledge entry {key}: adjacent major eligibility unverified")
        if entry.get("source") == "mcgill_recommended":
            if entry.get("relation_to_baseline") != "recommended_not_required":
                issues.append(f"optional knowledge entry {key}: McGill recommendation misclassified")
    if mcgill_catalog is not None:
        recommended = {c.get("code") for c in mcgill_catalog.get("courses", [])
                       if c.get("category") == "recommended"}
        mapped = {c.get("code") for c in entries if c.get("source") == "mcgill_recommended"}
        if not recommended.issubset(mapped):
            issues.append("optional knowledge register omits McGill recommended courses")
    return issues


def broken_local_links(markdown_file: Path) -> list[str]:
    errors = []
    text = markdown_file.read_text(encoding="utf-8")
    for destination in LINK.findall(text):
        target = destination.split(maxsplit=1)[0].strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or target.startswith(("#", "//")):
            continue
        local_path = unquote(parsed.path)
        if local_path and not (markdown_file.parent / local_path).exists():
            errors.append(f"{markdown_file}: missing {target}")
    return errors


def validate(root: Path = ROOT) -> list[str]:
    errors = []
    required = [root / "README.md", root / "AGENTS.md",
                root / "docs/OBJECTIVES.md", root / "docs/knowledge-base.md",
                root / "docs/course-material-collection.md", root / "docs/README.md",
                root / "docs/data/course-material-progress.json",
                root / "docs/university-curriculum.md",
                root / "docs/todo-university-coverage.md",
                root / "docs/udem-curriculum-a26-audit.md",
                root / "docs/data/udem-composition-a26.json",
                root / "docs/mcgill-curriculum-2026-audit.md",
                root / "docs/data/mcgill-composition-2026.json",
                root / "docs/berklee-curriculum-2026f-audit.md",
                root / "docs/data/berklee-composition-2026f.json",
                root / "docs/optional-knowledge-audit.md",
                root / "docs/data/optional-knowledge-seeds-2026.json"]
    for path in required:
        if not path.is_file():
            errors.append(f"missing required documentation: {path}")
    if (root / "docs/archive").exists():
        errors.append("obsolete documentation archive must not exist")
    errors.extend(legacy_mission_issues(root))
    agents_file = root / "AGENTS.md"
    if agents_file.is_file():
        errors.extend(agent_onboarding_issues(agents_file.read_text(encoding="utf-8")))
    todo = root / "docs/todo-university-coverage.md"
    if todo.is_file():
        errors.extend(university_coverage_issues(todo.read_text(encoding="utf-8")))
    catalog = root / "docs/data/udem-composition-a26.json"
    if catalog.is_file():
        try:
            errors.extend(university_catalog_issues(json.loads(catalog.read_text(encoding="utf-8"))))
        except (json.JSONDecodeError, ValueError, TypeError) as exc:
            errors.append(f"UdeM catalog JSON invalid: {exc}")
    for path, label, inspector in (
            (root / "docs/data/mcgill-composition-2026.json", "McGill", mcgill_catalog_issues),
            (root / "docs/data/berklee-composition-2026f.json", "Berklee", berklee_grid_issues)):
        if path.is_file():
            try:
                errors.extend(inspector(json.loads(path.read_text(encoding="utf-8"))))
            except (json.JSONDecodeError, ValueError, TypeError) as exc:
                errors.append(f"{label} catalog JSON invalid: {exc}")
    optional_path = root / "docs/data/optional-knowledge-seeds-2026.json"
    if optional_path.is_file():
        try:
            register = json.loads(optional_path.read_text(encoding="utf-8"))
            mcgill_path = root / "docs/data/mcgill-composition-2026.json"
            mcgill = (json.loads(mcgill_path.read_text(encoding="utf-8"))
                      if mcgill_path.is_file() else None)
            errors.extend(optional_knowledge_issues(
                register, todo.read_text(encoding="utf-8") if todo.is_file() else "", mcgill))
        except (json.JSONDecodeError, ValueError, TypeError) as exc:
            errors.append(f"optional knowledge register invalid: {exc}")
    progress_path = root / "docs/data/course-material-progress.json"
    if progress_path.is_file():
        try:
            catalogs = {
                "udem": json.loads((root / "docs/data/udem-composition-a26.json").read_text(encoding="utf-8")),
                "mcgill": json.loads((root / "docs/data/mcgill-composition-2026.json").read_text(encoding="utf-8")),
                "berklee": json.loads((root / "docs/data/berklee-composition-2026f.json").read_text(encoding="utf-8")),
                "optional": json.loads(optional_path.read_text(encoding="utf-8")),
            }
            progress = json.loads(progress_path.read_text(encoding="utf-8"))
            errors.extend(course_material_progress_issues(progress, catalogs, root))
        except (json.JSONDecodeError, ValueError, TypeError, OSError) as exc:
            errors.append(f"course material progress invalid: {exc}")
    for md in [root / "README.md", root / "AGENTS.md", *sorted((root / "docs").rglob("*.md"))]:
        if md.is_file():
            errors.extend(broken_local_links(md))
    return errors


if __name__ == "__main__":
    issues = validate()
    for issue in issues:
        print(issue, file=sys.stderr)
    print(f"Documentation: {'FAIL' if issues else 'OK'} — {len(issues)} problème(s)")
    sys.exit(bool(issues))
