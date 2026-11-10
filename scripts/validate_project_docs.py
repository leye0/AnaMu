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
                root / "docs/roadmap.md", root / "docs/README.md"]
    for path in required:
        if not path.is_file():
            errors.append(f"missing required documentation: {path}")
    if (root / "docs/archive").exists():
        errors.append("obsolete documentation archive must not exist")
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
