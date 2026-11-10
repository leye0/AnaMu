"""Validate local Markdown links and the single active documentation entrypoint.

The scanner checks local Markdown destinations (not HTTP targets or anchors).
It does not pretend to be a complete Markdown parser.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
CURRICULUM_ITEM = re.compile(r"^- \[([ xX])\] ([A-L]\d{2})\b(.*)$", re.MULTILINE)


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
                root / "docs/todo-university-coverage.md"]
    for path in required:
        if not path.is_file():
            errors.append(f"missing required documentation: {path}")
    if (root / "docs/archive").exists():
        errors.append("obsolete documentation archive must not exist")
    todo = root / "docs/todo-university-coverage.md"
    if todo.is_file():
        errors.extend(university_coverage_issues(todo.read_text(encoding="utf-8")))
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
