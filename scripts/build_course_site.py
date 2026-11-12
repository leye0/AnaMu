#!/usr/bin/env python3
"""Build the dependency-free static AnaMu course library for GitHub Pages.

Reads the real per-course Markdown, the assessment registry and MIDI binaries.
Does not alter university materials, statuses, source files or tests.
"""
from __future__ import annotations

import argparse
import html
import json
import posixpath
import re
import shutil
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
REPO_URL = "https://github.com/leye0/AnaMu/blob/main/"
ASSESSMENTS = ROOT / "docs/data/course-algorithmic-assessments.json"
STATIC = ROOT / "site"
HEADINGS = re.compile(r"^#{1,6}\s+(.+)$")
APPLICATION = re.compile(r"^##\s+Application à l.analyse et à la création\b", re.I | re.M)
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
INLINE_CODE = re.compile(r"\x60([^\x60]+)\x60")


def clean(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return re.sub(r"[\x60*_#]", "", text).strip()


def href(url: str, source_path: str) -> str:
    parsed = urlsplit(url)
    if parsed.scheme in ("http", "https") and parsed.netloc:
        return url
    if parsed.scheme or url.startswith("//"):
        return ""
    if url.startswith("#"):
        return REPO_URL + source_path + url
    relative = posixpath.normpath(posixpath.join(posixpath.dirname(source_path), url))
    if relative == ".." or relative.startswith("../"):
        return ""
    return REPO_URL + relative


def inline(text: str, source_path: str) -> str:
    # Escape first, then introduce only limited, safe HTML elements.
    parts: list[str] = []
    pos = 0
    tokens = re.compile(r"(\x60[^\x60]+\x60|\[[^\]]+\]\([^)]+\))")
    for token in tokens.finditer(text):
        parts.append(html.escape(text[pos:token.start()]))
        chunk = token.group()
        if chunk.startswith("\x60"):
            parts.append("<code>" + html.escape(chunk[1:-1]) + "</code>")
        else:
            link = LINK.fullmatch(chunk)
            if link:
                address = href(link.group(2), source_path)
                label = html.escape(link.group(1))
                if address:
                    parts.append(
                        '<a href="' + html.escape(address, quote=True)
                        + '" target="_blank" rel="noopener noreferrer">'
                        + label + "</a>"
                    )
                else:
                    parts.append(label)
            else:
                parts.append(html.escape(chunk))
        pos = token.end()
    parts.append(html.escape(text[pos:]))
    result = "".join(parts)
    result = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", result)
    result = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", result)
    return result


def markdown_html(md: str, source_path: str) -> str:
    out: list[str] = []
    paragraph: list[str] = []
    list_kind: str | None = None
    in_code = False
    code: list[str] = []
    table: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            out.append("<p>" + inline(" ".join(paragraph), source_path) + "</p>")
            paragraph.clear()

    def flush_list() -> None:
        nonlocal list_kind
        if list_kind:
            out.append("</" + list_kind + ">")
            list_kind = None

    def flush_table() -> None:
        if not table:
            return
        out.append('<div class="table-wrap"><table>')
        for idx, row in enumerate(table):
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            if idx == 1 and all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                continue
            tag = "th" if idx == 0 else "td"
            out.append("<tr>" + "".join(
                "<" + tag + ">" + inline(c, source_path) + "</" + tag + ">"
                for c in cells
            ) + "</tr>")
        out.append("</table></div>")
        table.clear()

    lines = md.splitlines()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("\x60\x60\x60"):
            flush_paragraph()
            flush_list()
            flush_table()
            if in_code:
                out.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>")
                code.clear()
            in_code = not in_code
            continue
        if in_code:
            code.append(line)
            continue
        if not stripped:
            flush_paragraph()
            flush_list()
            flush_table()
            continue
        if stripped.startswith("|") and stripped.endswith("|"):
            flush_paragraph()
            flush_list()
            table.append(stripped)
            continue
        flush_table()
        heading = HEADINGS.match(stripped)
        if heading:
            flush_paragraph()
            flush_list()
            level = min(stripped.index(" ") + 1, 5)
            out.append("<h" + str(level) + ">" + inline(heading.group(1), source_path) + "</h" + str(level) + ">")
            continue
        bullet = re.match(r"^[-*]\s+(.+)$", stripped)
        ordered = re.match(r"^\d+[.)]\s+(.+)$", stripped)
        if bullet or ordered:
            flush_paragraph()
            target = "ul" if bullet else "ol"
            if list_kind != target:
                flush_list()
                out.append("<" + target + ">")
                list_kind = target
            out.append("<li>" + inline((bullet or ordered).group(1), source_path) + "</li>")
            continue
        flush_list()
        if stripped.startswith(">"):
            flush_paragraph()
            out.append("<blockquote>" + inline(stripped.lstrip("> "), source_path) + "</blockquote>")
        elif stripped == "---":
            flush_paragraph()
            out.append("<hr>")
        else:
            paragraph.append(stripped)
    flush_paragraph()
    flush_list()
    flush_table()
    if in_code:
        out.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>")
    return "\n".join(out)


def extract(md: str) -> tuple[str, str, str, str]:
    lines = md.splitlines()
    heading = next((clean(line.lstrip("# ")) for line in lines if line.startswith("# ")), "")
    md_body = re.sub(r"^# [^\n]*\n?", "", md, count=1)
    match = APPLICATION.search(md_body)
    if match:
        introduction, application = md_body[:match.start()], md_body[match.start():]
    else:
        introduction, application = md_body, ""
    candidates = []
    for segment in re.split(r"\n\s*\n", introduction):
        value = clean(segment)
        if value.startswith("##") or value.startswith("http"):
            continue
        if len(value) >= 70 and not value.startswith(("Berklee College", "Sources publiques", "Université de Montréal", "UdeM A26")):
            candidates.append(value)
    snippet = (candidates[0] if candidates else clean(introduction[:300]))[:280]
    return heading, introduction, application, snippet


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="_site", help="Output folder (relative to repository)")
    args = parser.parse_args()
    destination = (ROOT / args.output).resolve()
    if destination == ROOT or not destination.is_relative_to(ROOT):
        parser.error("Output must be a subdirectory of the repository")
    if destination == STATIC or STATIC in destination.parents:
        parser.error("Cannot overwrite site source files")
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    for asset in ("index.html", "app.js", "styles.css"):
        shutil.copyfile(STATIC / asset, destination / asset)
    (destination / ".nojekyll").write_text("", encoding="utf-8")

    inventory = json.loads(ASSESSMENTS.read_text(encoding="utf-8"))
    metadata = []
    for row in inventory["assessments"]:
        school, code = row["institution"], row["code"]
        slug = re.sub(r"[^a-zA-Z0-9-]+", "-", code).strip("-")
        identifier = school + ":" + code
        material = row.get("material_file")
        source = ROOT / material if material else None
        markdown = source.read_text(encoding="utf-8") if source and source.is_file() else ""
        title, overview, application, snippet = extract(markdown) if markdown else (
            code + " — choix de cours" if row["review_state"] == "course_choice_placeholder" else code,
            "", "", "La fiche descriptive individuelle de ce cours n'a pas encore été créée."
        )
        link = row.get("example_midi")
        midi_url = None
        if link:
            actual = ROOT / link
            if not actual.is_file():
                raise FileNotFoundError("Registered MIDI is missing: " + link)
            midi_url = "midi/" + school + "/" + slug + ".mid"
            dest = destination / midi_url
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(actual, dest)
        description_url = "courses/" + school + "/" + slug + ".json"
        details = {
            "id": identifier, "title": title, "code": code, "institution": school,
            "overview_html": markdown_html(overview, material) if markdown else "",
            "application_html": markdown_html(application, material) if application else "",
            "source_repo": REPO_URL + material if material else "",
            "source_course": row.get("source_url") or "",
            "coverage": row.get("course_coverage"),
            "midi": midi_url,
            "non_algorithmic": row.get("non_algorithmic"),
            "algorithmic_tags": row.get("algorithmic_tags") or [],
            "review_state": row["review_state"],
            "note": row.get("limit_note") or "",
        }
        target = destination / description_url
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(details, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        metadata.append({
            "id": identifier, "code": code, "title": title,
            "institution": school, "excerpt": snippet,
            "review_state": row["review_state"], "coverage": row.get("course_coverage"),
            "midi": midi_url, "detail": description_url,
            "non_algorithmic": row.get("non_algorithmic"),
            "algorithmic_tags": row.get("algorithmic_tags") or [],
        })

    catalog = {"generated_from": "docs/data/course-algorithmic-assessments.json",
               "courses": metadata, "summary": inventory["summary"]}
    (destination / "catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )
    print("Built AnaMu Pages: " + str(len(metadata)) + " entries; "
          + str(sum(bool(x["midi"]) for x in metadata)) + " original MIDI examples, "
          + str(sum(x["review_state"] == "course_choice_placeholder" for x in metadata))
          + " choice families")


if __name__ == "__main__":
    main()
