"""Validate local Markdown links and the single active documentation entrypoint.

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
    if catalog.get("mandatory_credits") != 63 or catalog.get("total_credits") != 90:
        issues.append("UdeM published credit requirements are inconsistent")
    if catalog.get("status") != "public_catalog_course_inventory_only_syllabi_not_audited":
        issues.append("UdeM catalog must not masquerade as a syllabus audit")
    if not (catalog.get("source_url") or "").startswith(
            "https://admission.umontreal.ca/programmes/baccalaureat-en-musique-composition/"):
        issues.append("UdeM catalog missing its official source URL")
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
    required = [root / "README.md", root / "docs/OBJECTIVES.md",
                root / "docs/roadmap.md", root / "docs/README.md",
                root / "docs/university-curriculum.md",
                root / "docs/todo-university-coverage.md",
                root / "docs/udem-curriculum-a26-audit.md",
                root / "docs/data/udem-composition-a26.json"]
    for path in required:
        if not path.is_file():
            errors.append(f"missing required documentation: {path}")
    if (root / "docs/archive").exists():
        errors.append("obsolete documentation archive must not exist")
    todo = root / "docs/todo-university-coverage.md"
    if todo.is_file():
        errors.extend(university_coverage_issues(todo.read_text(encoding="utf-8")))
    catalog = root / "docs/data/udem-composition-a26.json"
    if catalog.is_file():
        try:
            errors.extend(university_catalog_issues(json.loads(catalog.read_text(encoding="utf-8"))))
        except (json.JSONDecodeError, ValueError, TypeError) as exc:
            errors.append(f"UdeM catalog JSON invalid: {exc}")
    for md in [root / "README.md", *sorted((root / "docs").rglob("*.md"))]:
        if md.is_file():
            errors.extend(broken_local_links(md))
    return errors


if __name__ == "__main__":
    issues = validate()
    for issue in issues:
        print(issue, file=sys.stderr)
    print(f"Documentation: {'FAIL' if issues else 'OK'} — {len(issues)} problème(s)")
    sys.exit(bool(issues))
