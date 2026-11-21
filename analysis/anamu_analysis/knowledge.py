"""Lossless document inventory and explicitly curated concept reconciliation.

Sections are evidence fragments, not automatically learned musical rules.
Only the curated registry binds a concept to a detector or a source section.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import re
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
MODULE_ROOT = Path(__file__).resolve().parents[1]
MODALITIES = {"midi", "audio", "score", "lyrics", "context"}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sections(path: str, text: str) -> list[dict[str, Any]]:
    """Partition every source line exactly once; preserve heading ancestry.

    Heading-level fragments also retain their subtree span so a citation can
    identify a complete learning section instead of just its first paragraph.
    """
    lines = text.splitlines(keepends=True)
    starts = []
    fence = None
    for i, line in enumerate(lines):
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            char, length = marker[1][0], len(marker[1])
            if fence is None:
                fence = (char, length)
            elif char == fence[0] and length >= fence[1]:
                fence = None
            continue
        if fence is not None:
            continue
        match = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line.rstrip("\r\n"))
        if match:
            starts.append((i, len(match[1]), match[2]))
    if not starts or starts[0][0] > 0:
        starts.insert(0, (0, 0, "Preamble"))
    result = []
    stack = []
    occurrences: dict[tuple[str, ...], int] = {}
    for j, (start, level, title) in enumerate(starts):
        while stack and stack[-1][0] >= level:
            stack.pop()
        heading_path = tuple([item[1] for item in stack] + [title])
        occurrence = occurrences.get(heading_path, 0)
        occurrences[heading_path] = occurrence + 1
        fragment_id = "fragment:" + sha256((path + "\n" + repr(heading_path) + f"\n{occurrence}").encode())[:24]
        own_end = starts[j + 1][0] if j + 1 < len(starts) else len(lines)
        subtree_end = next((s for s, lev, _ in starts[j + 1:] if lev <= level), len(lines))
        content = "".join(lines[start:own_end])
        result.append({
            "id": fragment_id, "document_path": path, "heading": title,
            "heading_path": list(heading_path), "parent_id": stack[-1][2] if stack else None,
            "start_line": start + 1, "end_line": own_end,
            "subtree_end_line": subtree_end, "text": content,
            "content_sha256": sha256(content.encode()),
            "declared_applicability_tokens": sorted(set(re.findall(
                r"\b(?:MIDI_DIRECT|MIDI_PROXY|AUDIO_REQUIRED|CONTEXT_REQUIRED|NOT_MUSIC_ALGORITHM|UNKNOWN)\b", content))),
            "semantic_review": "unreviewed_source_fragment",
        })
        stack.append((level, title, fragment_id))
    if "".join(fragment["text"] for fragment in result) != text:
        raise ValueError(f"Source partition lost text: {path}")
    return result


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def compile_knowledge(repo: Path = REPO_ROOT) -> dict[str, Any]:
    repo = repo.resolve()
    progress_path = repo / "docs/data/course-material-progress.json"
    assessments_path = repo / "docs/data/course-algorithmic-assessments.json"
    progress = load_json(progress_path)
    assessments = load_json(assessments_path)["assessments"]
    by_path = {row["material_file"]: row for row in assessments if row.get("material_file")}
    by_code = {(row["institution"], row["code"].replace(" ", "-")): row
               for row in assessments if row.get("material_file")}
    course_documents = sorted((repo / "docs/courses").rglob("*.md"))
    operational = {"docs/README.md", "docs/STATUS.md", "docs/OBJECTIVES.md",
                   "docs/todo-university-coverage.md", "docs/course-material-collection.md"}
    # Course outlines sometimes live only in source batches or JSON registers.
    # Read those too; do not silently restrict knowledge to polished fiches.
    shared_documents = [p for p in sorted((repo / "docs").rglob("*.md"))
        if p not in course_documents and p.relative_to(repo).as_posix() not in operational]
    documents = []
    fragments = []
    course_rows = []
    for path in course_documents + shared_documents:
        rel = path.relative_to(repo).as_posix()
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        parts = sections(rel, text)
        fragments.extend(parts)
        title = next((f["heading"] for f in parts if len(f["heading_path"]) == 1 and f["heading"] != "Preamble"), path.stem)
        document = {"path": rel, "title": title, "sha256": sha256(raw),
                    "git_blob_sha1": hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest(),
                    "line_count": len(text.splitlines()), "fragment_ids": [f["id"] for f in parts],
                    "kind": "course" if path in course_documents else "shared_reference"}
        if path in course_documents:
            row = by_path.get(rel, by_code.get((path.parent.name, path.stem.replace(" ", "-")), {}))
            institution = row.get("institution", path.parent.name)
            code = row.get("code", path.stem)
            course_id = institution + ":" + code
            document["course_id"] = course_id
            material = progress.get("courses", {}).get(institution, {}).get(code, {})
            course_rows.append({"id": course_id + "::document:" + sha256(rel.encode())[:12],
                "course_id": course_id, "institution": institution, "code": code,
                "title": title, "path": rel, "registered_course": bool(row),
                "primary_registered_material_file": rel in by_path,
                "topic_outline_state": material.get("topic_outline", {}).get("state"),
                "declared_course_applicability": row.get("algorithmic_tags", []),
                "non_algorithmic_declared": row.get("non_algorithmic"),
                "first_assessment_state": row.get("review_state"),
                "source_register_ref": {"path": "docs/data/course-material-progress.json",
                    "json_pointer": "/courses/" + institution + "/" + code.replace("~", "~0").replace("/", "~1")} if material else None,
                "fragment_count": len(parts), "concept_ids": [],
                "semantic_integration": "indexed_not_reconciled"})
        documents.append(document)

    missing_courses = [row for row in assessments if row.get("material_file")
                       and row["material_file"] not in {d["path"] for d in documents}]
    if missing_courses:
        raise ValueError("Registered course documents missing: " + str([r["material_file"] for r in missing_courses]))
    if len({c["id"] for c in course_rows}) != len(course_rows):
        raise ValueError("Duplicate source-document IDs")
    identity_groups = {}
    for row in course_rows:
        identity_groups.setdefault(row["course_id"], []).append(row["path"])
    pools = [{"institution": r["institution"], "code": r["code"],
              "state": "unresolved_choice_family_not_an_individual_course"}
             for r in assessments if not r.get("material_file")]

    registry_path = MODULE_ROOT / "knowledge/concepts.json"
    registry_raw = registry_path.read_bytes()
    registry = json.loads(registry_raw)
    concepts = registry["concepts"]
    ids = [c["id"] for c in concepts]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate canonical concept IDs")
    by_document = {d["path"]: d for d in documents}
    courses_by_path = {c["path"]: c for c in course_rows}
    all_ids = set(ids)
    for concept in concepts:
        for field in ("id", "name", "definition", "question", "requires", "sources", "limits", "prerequisites", "detectors"):
            if field not in concept:
                raise ValueError(f"Concept {concept.get('id')} missing {field}")
        if not set(concept["requires"]) <= MODALITIES:
            raise ValueError("Unknown input modality: " + concept["id"])
        if not set(concept["prerequisites"]) <= all_ids:
            raise ValueError("Unknown prerequisite: " + concept["id"])
        if not concept["sources"] or not concept["limits"]:
            raise ValueError("Source or limitations missing: " + concept["id"])
        concept["reconciliation_state"] = "curated_bootstrap_not_independent_musical_validation"
        for ref in concept["sources"]:
            path = ref["path"]
            document = by_document.get(path)
            if document is None:
                raise ValueError(f"Concept source not indexed: {concept['id']} -> {path}")
            if ref.get("heading"):
                hits = [f for f in fragments if f["document_path"] == path and f["heading"] == ref["heading"]]
                if len(hits) != 1:
                    raise ValueError(f"Ambiguous or missing source heading: {concept['id']} -> {ref['heading']}")
                fragment = hits[0]
                ref.update({"fragment_id": fragment["id"], "start_line": fragment["start_line"],
                            "end_line": fragment["subtree_end_line"], "scope": "explicit_section"})
            else:
                ref.update({"start_line": 1, "end_line": document["line_count"], "scope": "whole_document_reference"})
            ref["document_sha256"] = document["sha256"]
            if path in courses_by_path:
                courses_by_path[path]["concept_ids"].append(concept["id"])
        for course in course_rows:
            if course["concept_ids"]:
                course["semantic_integration"] = "partially_linked_not_exhaustive"

    # Reject cycles: a prerequisite graph must not manufacture a proof of itself.
    graph = {c["id"]: c["prerequisites"] for c in concepts}
    visiting, visited = set(), set()
    def visit(node):
        if node in visiting:
            raise ValueError("Concept prerequisite cycle: " + node)
        if node in visited:
            return
        visiting.add(node)
        for other in graph[node]: visit(other)
        visiting.remove(node); visited.add(node)
    for node in graph: visit(node)

    structured_sources = []
    for path in sorted((repo / "docs/data").glob("*.json")):
        raw = path.read_bytes()
        structured_sources.append({"path": path.relative_to(repo).as_posix(), "sha256": sha256(raw),
            "data": json.loads(raw), "semantic_state": "source_metadata_not_automatically_a_rule"})
    inputs = [{"path": d["path"], "sha256": d["sha256"]} for d in documents]
    inputs += [{"path": s["path"], "sha256": s["sha256"]} for s in structured_sources]
    inputs += [{"path": "analysis/knowledge/concepts.json", "sha256": sha256(registry_raw)}]
    fingerprint = sha256(json.dumps(sorted(inputs, key=lambda p: p["path"]), sort_keys=True).encode())
    return {"schema_version": 1, "source_fingerprint": fingerprint,
        "indexing_contract": "All course text indexed losslessly; indexed fragments are not automatically reconciled knowledge or implemented detectors.",
        "input_files": inputs, "documents": documents, "courses": course_rows,
        "choice_families": pools, "fragments": fragments, "concepts": concepts,
        "course_identity_groups": identity_groups,
        "structured_sources": structured_sources,
        "excluded_operational_documents": [{"path": p, "reason": "operational instructions, not additional musical evidence"} for p in sorted(operational)],
        "coverage": {"course_documents_discovered": len(course_documents), "course_documents_indexed": len(course_rows),
            "unique_course_identities": len(identity_groups),
            "registered_course_documents": sum(c["primary_registered_material_file"] for c in course_rows),
            "additional_documents_of_registered_courses": sum(c["registered_course"] and not c["primary_registered_material_file"] for c in course_rows),
            "supplementary_course_documents": sum(not c["registered_course"] for c in course_rows),
            "shared_documents": len(shared_documents), "source_fragments": len(fragments),
            "structured_source_documents": len(structured_sources),
            "choice_families": len(pools), "curated_concepts": len(concepts),
            "course_documents_with_curated_links": sum(bool(c["concept_ids"]) for c in course_rows),
            "course_documents_fully_semantically_integrated": 0}}


def write_coverage(knowledge: dict, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as file:
        fields = ["id", "course_id", "institution", "code", "title", "path", "registered_course", "fragment_count", "semantic_integration", "concept_ids"]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for row in knowledge["courses"]:
            writer.writerow({k: ";".join(row[k]) if isinstance(row[k], list) else row[k] for k in fields})
