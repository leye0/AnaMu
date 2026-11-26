"""Maintenable source-to-material catalogue for AnaMu.

An inventory fragment is a *candidate* material unit, not a validated concept.
Course Markdown stays authoritative; the catalogue stores only metadata and locators.
No external service or model is involved.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Iterator

from .knowledge import REPO_ROOT, compile_knowledge


def digest(value: Any) -> str:
    if isinstance(value, str):
        value = value.encode("utf-8")
    elif not isinstance(value, bytes):
        value = json.dumps(value, sort_keys=True, ensure_ascii=False,
                           separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(value).hexdigest()


def read_json(path: Path, default: Any) -> Any:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else deepcopy(default)


def save_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    serialized = json.dumps(value, indent=2, ensure_ascii=False) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == serialized:
        return
    temporary.write_text(serialized, encoding="utf-8")
    temporary.replace(path)


def load_catalog(folder: Path) -> dict:
    base = folder / "materials"
    manifest = read_json(base / "catalog.json", {"schema_version": 1, "units": []})
    if "chunks" not in manifest:
        return manifest
    units = []
    for chunk in manifest["chunks"]:
        units.extend(read_json(base / chunk, {"units": []})["units"])
    return {"schema_version": 1, "units": units}


def save_catalog(folder: Path, units: list[dict], fingerprint: str) -> None:
    base = folder / "materials"
    groups = defaultdict(list)
    for unit in units:
        groups[unit_source(unit)["document_path"]].append(unit)
    chunks = []
    for source_path, group in sorted(groups.items()):
        relative = "sources/" + digest(source_path)[:20] + ".json"
        save_json(base / relative, {"source_document": source_path,
                                    "units": sorted(group, key=lambda u: number(u["id"]))})
        chunks.append(relative)
    save_json(base / "catalog.json", {
        "schema_version": 1, "source_fingerprint": fingerprint,
        "chunks": chunks, "material_units": len(units),
        "note": "Manifest only; source-specific chunks carry stable identities and editorial metadata."
    })


def json_pointer_part(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def json_records(value: Any, pointer: str = "", depth: int = 0
                 ) -> Iterator[tuple[str, Any]]:
    """Bounded subdivisions, not inferred semantic lessons.

    The root is subdivided so registry objects (including nested courses) get
    locators. At depth four, retain the entire record as one JSON value.
    """
    if isinstance(value, dict) and value and depth < 4:
        if depth > 0 and any(key in value for key in
                             ("id", "course_id", "code", "title", "description", "name")):
            yield pointer, value
        else:
            for key, child in value.items():
                yield from json_records(child, pointer + "/" + json_pointer_part(str(key)),
                                        depth + 1)
    elif isinstance(value, list) and value and depth < 4 and any(
            isinstance(item, (dict, list)) for item in value):
        for index, child in enumerate(value):
            yield from json_records(child, pointer + "/" + str(index), depth + 1)
    else:
        yield pointer, value


def excerpt(value: str, limit: int = 240) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return value[:limit].rstrip() + ("…" if len(value) > limit else "")


def json_record_identity(value: Any) -> str | None:
    """An explicit row key is stronger than an array index, but not proof of semantics."""
    if not isinstance(value, dict):
        return None
    for key in ("id", "course_id"):
        if isinstance(value.get(key), (str, int)) and str(value[key]).strip():
            return key + ":" + str(value[key])
    if isinstance(value.get("code"), str) and isinstance(value.get("institution"), str):
        return "institution_code:" + value["institution"] + ":" + value["code"]
    return None


def candidates(knowledge: dict) -> Iterator[dict]:
    documents = {doc["path"]: doc for doc in knowledge["documents"]}
    courses = {row["path"]: row for row in knowledge["courses"]}
    for fragment in knowledge["fragments"]:
        path = fragment["document_path"]
        doc = documents[path]
        lines = fragment["text"].splitlines()
        body = "\n".join(lines[1:]).strip() if fragment["heading"] != "Preamble" else fragment["text"].strip()
        preview = next((line.strip() for line in body.splitlines()
                        if line.strip() and not line.lstrip().startswith(("#", "|", "---"))), "")
        preview = excerpt(preview)
        title = fragment["heading"]
        if title == "Preamble":
            title = "Préambule — " + doc["title"]
        course = courses.get(path)
        yield {
            "kind": "markdown_section",
            "title": title,
            "proposed_description": ("Extrait documentaire à qualifier : " + preview
                                     if preview else "Titre ou passage sans description éditoriale vérifiée."),
            "course_id": course["course_id"] if course else None,
            "source": {
                "document_path": path,
                "document_sha256": doc["sha256"],
                "locator": {"kind": "markdown_fragment",
                            "anchor": fragment["id"],
                            "heading_path": fragment["heading_path"],
                            "start_line": fragment["start_line"],
                            "end_line": fragment["end_line"],
                            "subtree_end_line": fragment["subtree_end_line"]},
                "content_sha256": fragment["content_sha256"],
                "body_sha256": digest(body) if body else None,
            },
        }
    for source in knowledge["structured_sources"]:
        for pointer, value in json_records(source["data"]):
            title = None
            description = None
            if isinstance(value, dict):
                title = next((str(value[key]) for key in
                              ("title", "name", "code", "id", "course_id")
                              if isinstance(value.get(key), (str, int))), None)
                description = next((value[key] for key in ("description", "summary", "label")
                                    if isinstance(value.get(key), str)), None)
            title = title or (pointer.split("/")[-1].replace("~1", "/").replace("~0", "~")
                              if pointer else Path(source["path"]).stem)
            yield {
                "kind": "json_record",
                "title": excerpt(str(title), 140),
                "proposed_description": ("Description documentaire non revue : " + excerpt(description)
                                         if description else
                                         "Enregistrement JSON retrouvé ; périmètre pédagogique à qualifier."),
                "course_id": None,
                "source": {
                    "document_path": source["path"],
                    "document_sha256": source["sha256"],
                    "locator": {"kind": "json_pointer", "anchor": pointer,
                                "json_pointer": pointer,
                                "record_identity": json_record_identity(value)},
                    "content_sha256": digest(value),
                    "body_sha256": None,
                },
            }


def source_key(source: dict) -> tuple[str, str, str]:
    locator = source["locator"]
    return source["document_path"], locator["kind"], locator["anchor"]


def unit_source(unit: dict) -> dict:
    return next(binding for binding in unit["source_bindings"]
                if binding.get("role") == "primary")


def number(identifier: str) -> int:
    try:
        return int(identifier.rsplit(":", 1)[-1])
    except ValueError:
        raise ValueError("Malformed persistent material or binding ID: " + identifier)


def choose_old(candidate: dict, unused: dict[str, dict],
               exact: dict, content: dict, body: dict, identities: dict,
               protected_anchors: set[tuple[str, str, str]]) -> tuple[dict | None, str]:
    source = candidate["source"]
    locator = source["locator"]
    identity = locator.get("record_identity")
    matches = [u for u in exact.get(source_key(source), []) if u["id"] in unused]
    if len(matches) > 1:
        raise ValueError("Duplicate source locator: " + str(source_key(source)))
    exact_match = matches[0] if matches else None
    if identity:
        identified = [u for u in identities.get((source["document_path"], identity), [])
                      if u["id"] in unused]
        if len(identified) == 1:
            old = identified[0]
            return old, ("anchor" if source_key(unit_source(old)) == source_key(source)
                         else "relocated_unreviewed")
        if exact_match:
            old_identity = unit_source(exact_match)["locator"].get("record_identity")
            if old_identity and old_identity != identity:
                # An array index now addresses a different identifiable row.
                return None, "changed_row_identity"
            # Duplicate business keys do not invalidate an unchanged locator.
            return exact_match, "anchor"
        if len(identified) > 1:
            return None, "ambiguous_locator"
    elif exact_match:
        return exact_match, "anchor"
    # Relocations are proposals, never silently validated. Match only a UNIQUE
    # unchanged passage; duplicate boilerplate and empty headings are excluded.
    for index, key in (
        (content, (source["document_path"], source["content_sha256"])),
        (body, (source["document_path"], source["body_sha256"])),
        (content, (None, source["content_sha256"])),
    ):
        if key[1] is None:
            continue
        matches = [u for u in index.get(key, []) if u["id"] in unused
                   and source_key(unit_source(u)) not in protected_anchors]
        if len(matches) == 1:
            return matches[0], "relocated_unreviewed"
        if len(matches) > 1:
            return None, "ambiguous_locator"
    return None, "new"


def refresh(repo: Path = REPO_ROOT) -> dict:
    repo = repo.resolve()
    folder = repo / "analysis/knowledge"
    materials_path = folder / "materials/catalog.json"
    courses_path = folder / "course-material-maps/links.json"
    links_path = folder / "material-knowledge-maps/links.json"
    index_path = folder / "material-index.json"
    previous = load_catalog(folder)
    old_course = read_json(courses_path, {"schema_version": 1, "bindings": []})
    old_links = read_json(links_path, {"schema_version": 1, "bindings": []})
    old_units = previous["units"]
    ids = [u["id"] for u in old_units]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate persisted material IDs")
    unused = {u["id"]: u for u in old_units}
    exact, content, body, identities = (defaultdict(list), defaultdict(list),
                                       defaultdict(list), defaultdict(list))
    for unit in old_units:
        source = unit_source(unit)
        exact[source_key(source)].append(unit)
        record_identity = source["locator"].get("record_identity")
        if record_identity:
            identities[(source["document_path"], record_identity)].append(unit)
        content[(source["document_path"], source["content_sha256"])].append(unit)
        content[(None, source["content_sha256"])].append(unit)
        if source.get("body_sha256"):
            body[(source["document_path"], source["body_sha256"])].append(unit)

    knowledge = compile_knowledge(repo)
    next_unit = max((number(i) for i in ids), default=0)
    units = []
    ambiguities = []
    discovered = list(candidates(knowledge))
    protected_anchors = {source_key(c["source"]) for c in discovered}
    if len(protected_anchors) != len(discovered):
        raise ValueError("Duplicate newly discovered source locators")
    for candidate in discovered:
        prior, how = choose_old(candidate, unused, exact, content, body,
                                identities, protected_anchors)
        source = dict(candidate["source"], role="primary")
        if prior is None:
            next_unit += 1
            unit = {
                "id": f"material:{next_unit:07d}", "revision": 1,
                "kind": candidate["kind"], "title": candidate["title"],
                "title_origin": "source_heading_or_key",
                "description": candidate["proposed_description"],
                "description_origin": "source_proposal_unreviewed",
                "editorial_review": "unreviewed",
                "review_required": True,
                "covers": [], "does_not_cover": [], "notes": [],
                "source_bindings": [source], "lifecycle": "active",
                "locator_review": "unreviewed",
            }
            if how in ("ambiguous_locator", "changed_row_identity"):
                ambiguities.append(unit["id"])
        else:
            unused.pop(prior["id"])
            unit = deepcopy(prior)
            old_primary = unit_source(unit)
            changed = old_primary["content_sha256"] != source["content_sha256"]
            relocated = how != "anchor"
            if changed:
                unit["revision"] += 1
                unit["review_required"] = True
                if unit["description_origin"] == "source_proposal_unreviewed":
                    unit["description"] = candidate["proposed_description"]
            if relocated:
                unit["review_required"] = True
            if unit.get("title_origin") == "source_heading_or_key":
                unit["title"] = candidate["title"]
            unit["kind"] = candidate["kind"]
            unit["source_bindings"] = [source] + [
                b for b in unit["source_bindings"] if b.get("role") != "primary"]
            unit["lifecycle"] = "active"
            unit["locator_review"] = "relocated_requires_review" if relocated else "resolved"
        units.append(unit)
    for missing in unused.values():
        unit = deepcopy(missing)
        unit["lifecycle"] = "source_missing_not_deleted"
        unit["review_required"] = True
        units.append(unit)
    units.sort(key=lambda u: number(u["id"]))

    previous_bindings = {(b["course_id"], b["material_id"]): b
                         for b in old_course["bindings"]}
    if len(previous_bindings) != len(old_course["bindings"]):
        raise ValueError("Duplicate persisted course-material binding")
    next_binding = max((number(b["id"]) for b in old_course["bindings"]), default=0)
    bindings = []
    for unit in units:
        if unit["lifecycle"] != "active":
            continue
        source = unit_source(unit)
        doc = next((c for c in knowledge["courses"]
                    if c["path"] == source["document_path"]), None)
        if not doc:
            continue
        key = (doc["course_id"], unit["id"])
        if key in previous_bindings:
            binding = deepcopy(previous_bindings.pop(key))
            binding["source_path"] = source["document_path"]
        else:
            next_binding += 1
            binding = {
                "id": f"course-material:{next_binding:07d}",
                "course_id": doc["course_id"], "material_id": unit["id"],
                "source_path": source["document_path"],
                "attribution": "not_yet_reviewed",
                "presentation_order": None,
                "pedagogical_group": None,
                "editorial_review": "unreviewed",
            }
        binding["lifecycle"] = "active"
        bindings.append(binding)
    for binding in previous_bindings.values():
        binding = deepcopy(binding)
        binding["lifecycle"] = "source_missing_not_deleted"
        bindings.append(binding)
    bindings.sort(key=lambda b: number(b["id"]))

    unit_by_id = {u["id"]: u for u in units}
    if len(unit_by_id) != len(units):
        raise ValueError("Duplicate generated material IDs")
    for link in old_links["bindings"]:
        target = unit_by_id.get(link["material_id"])
        if target is None:
            raise ValueError("Knowledge link to unknown material: " + link["material_id"])
    stale_links = [link["id"] for link in old_links["bindings"]
                   if unit_by_id[link["material_id"]]["revision"] !=
                   link.get("reviewed_material_revision") or
                   unit_by_id[link["material_id"]]["lifecycle"] != "active"]
    by_course, by_document, by_concept = defaultdict(list), defaultdict(list), defaultdict(list)
    for unit in units:
        by_document[unit_source(unit)["document_path"]].append(unit["id"])
    for binding in bindings:
        if binding["lifecycle"] == "active":
            by_course[binding["course_id"]].append(binding["material_id"])
    for link in old_links["bindings"]:
        target = link.get("target", {})
        if target.get("id"):
            by_concept[target["id"]].append(link["material_id"])
    coverage = {
        "course_documents": knowledge["coverage"]["course_documents_indexed"],
        "shared_documents": knowledge["coverage"]["shared_documents"],
        "structured_json_files": knowledge["coverage"]["structured_source_documents"],
        "material_units_active": sum(u["lifecycle"] == "active" for u in units),
        "material_units_missing_source": len(unused),
        "descriptions_human_reviewed": sum(u.get("editorial_review") == "human_reviewed"
                                             for u in units if u["lifecycle"] == "active"
                                             and not u["review_required"]),
        "descriptions_assistant_source_checked_drafts": sum(
            u.get("editorial_review") == "assistant_source_checked_draft"
            for u in units if u["lifecycle"] == "active"),
        "material_units_requiring_review": sum(u["review_required"]
                                                for u in units if u["lifecycle"] == "active"),
        "course_material_bindings_active": sum(b["lifecycle"] == "active" for b in bindings),
        "material_knowledge_bindings": len(old_links["bindings"]),
        "material_knowledge_bindings_stale": len(stale_links),
        "material_knowledge_bindings_proposed": sum(
            b.get("state") == "assistant_source_checked_proposed_link"
            for b in old_links["bindings"]),
        "material_knowledge_bindings_unresolved": sum(
            b.get("target", {}).get("id") is None
            for b in old_links["bindings"]),
        "material_knowledge_bindings_confirmed": sum(
            b.get("state") == "confirmed"
            for b in old_links["bindings"]),
        "ambiguous_identity_candidates": ambiguities,
        "note": "Documentary coverage, not semantic mastery or validated musical reasoning.",
    }
    save_catalog(folder, units, knowledge["source_fingerprint"])
    save_json(courses_path, {"schema_version": 1, "bindings": bindings})
    if not links_path.exists():
        save_json(links_path, {"schema_version": 1, "bindings": []})
    save_json(index_path, {
        "schema_version": 1, "coverage": coverage,
        "by_course": dict(sorted(by_course.items())),
        "by_document": dict(sorted(by_document.items())),
        "by_concept": dict(sorted(by_concept.items())),
        "knowledge_links_requiring_review": stale_links,
    })
    return coverage


def show(repo: Path, identifier: str, include_source: bool) -> dict:
    root = repo / "analysis/knowledge"
    catalog = load_catalog(root)
    unit = next((u for u in catalog["units"] if u["id"] == identifier), None)
    if unit is None:
        raise ValueError("Unknown material ID: " + identifier)
    result = {"unit": unit,
              "course_bindings": [b for b in read_json(
                  root / "course-material-maps/links.json", {"bindings": []})["bindings"]
                  if b["material_id"] == identifier],
              "knowledge_bindings": [b for b in read_json(
                  root / "material-knowledge-maps/links.json", {"bindings": []})["bindings"]
                  if b["material_id"] == identifier]}
    selected_mentions = []
    selected_assertions = []
    # A single material is a point of entry to the semantic extraction.
    # Read pilot and subsequent mention batches without treating them as
    # verified musical facts.
    for path in sorted((root / "mentions").glob("*.json")):
        batch = read_json(path, {})
        selected_mentions.extend(
            item for item in batch.get("mentions", [])
            if item.get("material_id") == identifier)
        selected_assertions.extend(
            item for item in batch.get("assertions", [])
            if item.get("material_id") == identifier)
    result["mentions"] = selected_mentions
    result["candidate_assertions"] = selected_assertions
    if include_source:
        source = unit_source(unit)
        document = repo / source["document_path"]
        locator = source["locator"]
        if not document.exists():
            result["source_preview"] = {"state": "missing"}
        elif locator["kind"] == "markdown_fragment":
            lines = document.read_text(encoding="utf-8").splitlines(keepends=True)
            start, end = locator["start_line"], locator["end_line"]
            snippet = "".join(lines[start - 1:end])
            result["source_preview"] = {
                "state": "unchanged" if digest(snippet) == source["content_sha256"]
                         else "source_may_have_changed",
                "text": snippet,
            }
        else:
            value = json.loads(document.read_text(encoding="utf-8"))
            try:
                for part in locator["json_pointer"].split("/")[1:]:
                    part = part.replace("~1", "/").replace("~0", "~")
                    value = value[int(part)] if isinstance(value, list) else value[part]
                result["source_preview"] = {
                    "state": "unchanged" if digest(value) == source["content_sha256"]
                             else "source_may_have_changed",
                    "value": value,
                }
            except (KeyError, IndexError, TypeError, ValueError):
                result["source_preview"] = {"state": "locator_not_resolved"}
    return result


def describe(repo: Path, identifier: str, description: str,
             reviewed: bool = False) -> None:
    path = repo / "analysis/knowledge/materials/catalog.json"
    catalog = load_catalog(repo / "analysis/knowledge")
    unit = next((u for u in catalog["units"] if u["id"] == identifier
                 and u["lifecycle"] == "active"), None)
    if unit is None:
        raise ValueError("Unknown active material ID: " + identifier)
    if not description.strip():
        raise ValueError("Description cannot be empty")
    unit["description"] = description.strip()
    unit["description_origin"] = "human_editorial"
    unit["editorial_review"] = "human_reviewed" if reviewed else "draft"
    unit["review_required"] = not reviewed
    unit["editorial_revision"] = unit.get("editorial_revision", 0) + 1
    save_catalog(repo / "analysis/knowledge", catalog["units"],
                 read_json(path, {}).get("source_fingerprint", "not_built"))


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="AnaMu — référentiel de matières")
    parser.add_argument("--repo", type=Path, default=REPO_ROOT)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("refresh", help="Create/update stable material metadata and mappings")
    search_parser = commands.add_parser("search", help="Search titles, descriptions and source paths")
    search_parser.add_argument("query", nargs="?", default="",
                               help="Optional words in a title, description or source path")
    search_parser.add_argument("--limit", type=int, default=20)
    search_parser.add_argument("--course", help="Filter by course ID, e.g. berklee:CM-211")
    search_parser.add_argument("--concept", help="Filter by linked analytical concept ID")
    search_parser.add_argument("--review", help="Filter by editorial review state")
    show_parser = commands.add_parser("show", help="Show a material and its two mappings")
    show_parser.add_argument("id")
    show_parser.add_argument("--source", action="store_true")
    describe_parser = commands.add_parser("describe", help="Edit one persistent description")
    describe_parser.add_argument("id")
    describe_parser.add_argument("description")
    describe_parser.add_argument("--reviewed", action="store_true")
    args = parser.parse_args(argv)
    repo = args.repo.resolve()
    try:
        if args.command == "refresh":
            print(json.dumps(refresh(repo), ensure_ascii=False, indent=2))
        elif args.command == "show":
            print(json.dumps(show(repo, args.id, args.source), ensure_ascii=False, indent=2))
        elif args.command == "describe":
            describe(repo, args.id, args.description, args.reviewed)
            print("Description saved; identity and source text unchanged.")
        else:
            root = repo / "analysis/knowledge"
            catalog = load_catalog(root)
            course_links = read_json(root / "course-material-maps/links.json",
                                     {"bindings": []})["bindings"]
            concept_links = read_json(root / "material-knowledge-maps/links.json",
                                      {"bindings": []})["bindings"]
            course_ids = {b["material_id"] for b in course_links
                          if b.get("course_id") == args.course
                          and b.get("lifecycle") == "active"} if args.course else None
            concept_ids = {b["material_id"] for b in concept_links
                           if b.get("target", {}).get("id") == args.concept
                           } if args.concept else None
            needle = args.query.casefold()
            matched = [
                {"id": unit["id"], "title": unit["title"],
                 "description": unit["description"], "review": unit["editorial_review"],
                 "source": unit_source(unit)["document_path"],
                 "concept_ids": sorted({b.get("target", {}).get("id")
                                        for b in concept_links
                                        if b["material_id"] == unit["id"]
                                        and b.get("target", {}).get("id")})}
                for unit in catalog["units"]
                if needle in " ".join((unit["title"], unit["description"],
                                      unit_source(unit)["document_path"])).casefold()
                and (course_ids is None or unit["id"] in course_ids)
                and (concept_ids is None or unit["id"] in concept_ids)
                and (args.review is None or unit.get("editorial_review") == args.review)
            ]
            print(json.dumps({"total_matches": len(matched),
                              "results": matched[:max(0, args.limit)]},
                             ensure_ascii=False, indent=2))
    except (OSError, KeyError, ValueError, TypeError, StopIteration) as error:
        parser.exit(2, "Material registry stopped: " + str(error) + "\n")


if __name__ == "__main__":
    main()
