"""Read-only extraction ledger over persistent material units and review batches.

Documentary presence, extracted assertions, and closure of an extraction pass
are different states. A closed pass is scoped to one source revision, never
an assertion that a concept or a musical operation has been validated.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
from typing import Any

from .materials import digest, load_catalog, read_json, unit_source
from .knowledge import REPO_ROOT

DISPOSITIONS = {
    "partial_extraction", "no_analytic_assertion_in_passage",
    "extraction_complete_for_passage",
}
CLOSED = {"no_analytic_assertion_in_passage", "extraction_complete_for_passage"}
REVIEW_DIMENSIONS = {"definitions", "methods", "conditions", "exceptions",
                     "counterexamples", "source_attribution"}


def current_revision(row: dict, unit: dict) -> bool:
    return (unit["lifecycle"] == "active" and
            row.get("reviewed_material_revision") == unit["revision"])


def exact_span(row: dict, unit: dict) -> bool:
    span = row.get("source_span")
    if not isinstance(span, dict):
        return False
    source = unit_source(unit)
    return all(span.get(k) == source.get(k) for k in
               ("document_path", "document_sha256", "content_sha256", "locator"))


def load_ledger(folder: Path) -> dict:
    units = {u["id"]: u for u in load_catalog(folder)["units"]}
    manifest = read_json(folder / "source-manifest.json", {})["sources"]
    kinds = {row["path"]: row["kind"] for row in manifest}
    index = read_json(folder / "material-index.json", {})
    registry = read_json(folder / "evidence-facts.json", {})["facts"]
    fact_ids = {row["id"] for row in registry}
    mentions, assertions, reviews = defaultdict(list), defaultdict(list), defaultdict(list)
    all_ids = set()
    anchored_assertions = []
    unresolved_subjects = []
    assertions_by_id = {}
    mentions_by_id = {}
    for path in sorted((folder / "mentions").glob("*.json")):
        batch = read_json(path, {})
        if batch.get("schema_version") != 1:
            raise ValueError("Unsupported extraction batch: " + path.name)
        for field, target in (("mentions", mentions), ("assertions", assertions),
                              ("passage_reviews", reviews)):
            for row in batch.get(field, []):
                material = row["material_id"]
                if material not in units:
                    raise ValueError("Orphan " + field + ": " + material)
                if field != "passage_reviews":
                    identifier = row["id"]
                    if identifier in all_ids:
                        raise ValueError("Duplicate extraction identity: " + identifier)
                    all_ids.add(identifier)
                    if field == "mentions":
                        mentions_by_id[identifier] = row
                    else:
                        assertions_by_id[identifier] = row
                else:
                    if row["disposition"] not in DISPOSITIONS:
                        raise ValueError("Unknown passage disposition: " + material)
                    if not isinstance(row.get("reason"), str) or not row["reason"].strip():
                        raise ValueError("Passage review requires a reason: " + material)
                if batch.get("extraction_contract") == "passage_review_v2":
                    if field == "passage_reviews":
                        dims = row.get("review_dimensions", {})
                        if (set(dims) != REVIEW_DIMENSIONS or
                                any(v not in {"examined", "not_present", "open"}
                                    for v in dims.values())):
                            raise ValueError("Invalid review dimensions: " + material)
                        remaining = row.get("remaining_questions", [])
                        if (row["disposition"] in CLOSED and
                                (remaining or "open" in dims.values())):
                            raise ValueError("Closed review retains open dimensions: " + material)
                        if row["disposition"] == "partial_extraction" and not remaining:
                            raise ValueError("Partial review needs remaining questions: " + material)
                    elif field == "assertions":
                        anchor = row.get("source_anchor", {})
                        start, end = anchor.get("start_codepoint"), anchor.get("end_codepoint_exclusive")
                        if (anchor.get("kind") != "exact_source_excerpt" or
                                type(start) is not int or type(end) is not int or
                                start < 0 or end <= start or
                                not isinstance(anchor.get("excerpt_sha256"), str) or
                                len(anchor["excerpt_sha256"]) != 64 or
                                not row.get("applicability_conditions") or
                                not row.get("inference_limit")):
                            raise ValueError("Invalid assertion anchor or limits: " + row["id"])
                        anchored_assertions.append(row)
                    elif field == "mentions" and row.get("unresolved_subject"):
                        unresolved_subjects.append(row)
                target[material].append(dict(row, batch=path.name))
    for identifier, row in assertions_by_id.items():
        mention = mentions_by_id.get(row["mention_id"])
        if (mention is None or mention["material_id"] != row["material_id"] or
                mention.get("reviewed_material_revision") != row.get("reviewed_material_revision") or
                identifier not in mention.get("candidate_assertion_ids", [])):
            raise ValueError("Inconsistent assertion-to-mention edge: " + identifier)
    for identifier, mention in mentions_by_id.items():
        refs = mention.get("candidate_assertion_ids", [])
        if len(refs) != len(set(refs)) or any(
                ref not in assertions_by_id or assertions_by_id[ref]["mention_id"] != identifier
                for ref in refs):
            raise ValueError("Inconsistent mention-to-assertion edges: " + identifier)
    if sum(map(len, mentions.values())) != index["coverage"]["extracted_candidate_mentions"]:
        raise ValueError("Mention count disagrees with material index")
    if sum(map(len, assertions.values())) != index["coverage"]["extracted_candidate_assertions"]:
        raise ValueError("Assertion count disagrees with material index")

    rows = []
    requirements = defaultdict(set)
    for identifier, unit in units.items():
        source = unit_source(unit)
        current_mentions = [m for m in mentions[identifier]
                            if current_revision(m, unit) and
                            ("source_span" not in m or exact_span(m, unit))]
        current_mention_ids = {m["id"] for m in current_mentions}
        current_assertions = [a for a in assertions[identifier]
                              if current_revision(a, unit) and
                              a["mention_id"] in current_mention_ids and
                              ("source_span" not in a or exact_span(a, unit))]
        explicit = [r for r in reviews[identifier]
                    if current_revision(r, unit) and exact_span(r, unit)]
        dispositions = {r["disposition"] for r in explicit}
        stale_count = (len(mentions[identifier]) - len(current_mentions) +
                       len(assertions[identifier]) - len(current_assertions) +
                       len(reviews[identifier]) - len(explicit))
        if unit["lifecycle"] != "active":
            state = "inactive_source_retained"
        elif (len(dispositions) > 1 or
              ("no_analytic_assertion_in_passage" in dispositions and current_assertions)):
            state = "conflicting_reviews"
        elif dispositions:
            state = next(iter(dispositions))
        elif stale_count:
            state = "review_stale"
        elif current_mentions or current_assertions:
            state = "legacy_partial_extraction"
        else:
            state = "not_examined_for_extraction"
        for assertion in current_assertions:
            for requirement in assertion.get("requires_evidence", []):
                requirements[requirement].add(assertion["id"])
        rows.append({
            "material_id": identifier, "material_revision": unit["revision"],
            "title": unit["title"], "source_kind": kinds.get(source["document_path"], "unknown"),
            "source_path": source["document_path"], "source_span": {
                k: source[k] for k in ("document_path", "document_sha256",
                                       "content_sha256", "locator")},
            "extraction_state": state, "current_mentions": len(current_mentions),
            "current_assertions": len(current_assertions), "stale_records": stale_count,
            "explicit_passage_reviews": len(explicit),
            "remaining_questions": sorted({q for r in explicit
                                           for q in r.get("remaining_questions", [])}),
        })
    return {"rows": rows, "requirements": requirements, "fact_ids": fact_ids,
            "anchored_assertions": anchored_assertions,
            "unresolved_subjects": unresolved_subjects}


def status(ledger: dict) -> dict:
    rows = ledger["rows"]
    by_kind = defaultdict(Counter)
    by_document = defaultdict(Counter)
    for row in rows:
        state = row["extraction_state"]
        by_kind[row["source_kind"]][state] += 1
        by_document[row["source_path"]][state] += 1
    active = [r for r in rows if r["extraction_state"] != "inactive_source_retained"]
    closed = [r for r in active if r["extraction_state"] in CLOSED]
    requirements = ledger["requirements"]
    missing_vocabulary = [{"requirement": key, "assertion_ids": sorted(ids)}
                          for key, ids in sorted(requirements.items())
                          if key not in ledger["fact_ids"]]
    return {
        "active_units": len(active),
        "units_with_current_assertions": sum(r["current_assertions"] > 0 for r in active),
        "units_with_explicit_passage_review": sum(r["explicit_passage_reviews"] > 0 for r in active),
        "units_closed_for_current_pass": len(closed),
        "units_open_for_extraction": len(active) - len(closed),
        "current_assertions": sum(r["current_assertions"] for r in active),
        "assertions_with_exact_excerpt_anchor": len(ledger["anchored_assertions"]),
        "mentions_with_unresolved_subject": len(ledger["unresolved_subjects"]),
        "stale_records": sum(r["stale_records"] for r in rows),
        "states": dict(sorted(Counter(r["extraction_state"] for r in rows).items())),
        "by_source_kind": {k: dict(v) for k, v in sorted(by_kind.items())},
        "by_document": {k: dict(v) for k, v in sorted(by_document.items())},
        "distinct_requirement_labels": len(requirements),
        "unregistered_requirement_labels": missing_vocabulary,
        "limitation": ("Closure means a stated extraction pass was completed at the "
                       "current source span; not semantic mastery, human review, "
                       "operation implementation, or musical validation."),
    }


def queue(ledger: dict, *, kind: str | None = None,
          source: str | None = None, limit: int = 20) -> list[dict]:
    if limit < 0:
        raise ValueError("Limit must be nonnegative")
    groups = defaultdict(list)
    for row in ledger["rows"]:
        if row["extraction_state"] in CLOSED | {"inactive_source_retained"}:
            continue
        if kind and row["source_kind"] != kind:
            continue
        if source and row["source_path"] != source:
            continue
        groups[row["source_path"]].append(row)
    # Revisit conflicts/stale records first within each document, then round-robin
    # to avoid starving small courses behind large registers.
    priority = {"conflicting_reviews": 0, "review_stale": 1,
                "partial_extraction": 2, "legacy_partial_extraction": 3,
                "not_examined_for_extraction": 4}
    for rows in groups.values():
        rows.sort(key=lambda r: (priority[r["extraction_state"]],
                                 r["material_id"]))
    selected = []
    if limit == 0:
        return selected
    documents = sorted(groups)
    for offset in range(max(map(len, groups.values()), default=0)):
        for path in documents:
            rows = groups[path]
            if offset < len(rows):
                selected.append(rows[offset])
                if len(selected) == limit:
                    return selected
    return selected


def source_packet(repo: Path, row: dict, cache: dict | None = None) -> dict:
    span = row["source_span"]
    path = (repo / span["document_path"]).resolve()
    if not path.is_relative_to(repo / "docs"):
        raise ValueError("Source is outside read-only docs/")
    cache = {} if cache is None else cache
    if path not in cache:
        raw = path.read_bytes()
        cache[path] = (raw, digest(raw))
    raw, document_hash = cache[path]
    if document_hash != span["document_sha256"]:
        raise ValueError("Source bytes changed; refresh and review before extraction")
    loc = span["locator"]
    if loc["kind"] == "markdown_fragment":
        lines = raw.decode("utf-8").splitlines(keepends=True)
        value: Any = "".join(lines[loc["start_line"] - 1:loc["end_line"]])
    elif loc["kind"] == "json_pointer":
        value = json.loads(raw)
        for part in loc["json_pointer"].split("/")[1:]:
            part = part.replace("~1", "/").replace("~0", "~")
            value = value[int(part)] if isinstance(value, list) else value[part]
    else:
        raise ValueError("Unknown source locator: " + loc["kind"])
    if digest(value) != span["content_sha256"]:
        raise ValueError("Located content does not match material fingerprint")
    return dict(row, source_verified_at_read=True, source_content=value)


def packets(repo: Path, rows: list[dict]) -> list[dict]:
    """Verify each passage while reading each source document only once."""
    cache: dict = {}
    return [source_packet(repo, row, cache) for row in rows]


def audit_anchors(repo: Path, ledger: dict) -> dict:
    """Check the exact source excerpt of every current v2 assertion."""
    rows = {r["material_id"]: r for r in ledger["rows"]}
    cache: dict = {}
    errors, stale = [], []
    verified = 0
    for assertion in ledger["anchored_assertions"]:
        row = rows[assertion["material_id"]]
        if (row["material_revision"] != assertion["reviewed_material_revision"] or
                row["source_span"] != assertion["source_span"] or
                row["extraction_state"] == "inactive_source_retained"):
            stale.append(assertion["id"])
            continue
        try:
            value = source_packet(repo, row, cache)["source_content"]
            anchor = assertion["source_anchor"]
            if not isinstance(value, str):
                raise ValueError("Exact text anchor needs a string source")
            start, end = anchor["start_codepoint"], anchor["end_codepoint_exclusive"]
            excerpt = value[start:end]
            if (end > len(value) or digest(excerpt) != anchor["excerpt_sha256"] or
                    value.find(excerpt) != value.rfind(excerpt)):
                raise ValueError("Exact excerpt does not match uniquely")
            verified += 1
        except (OSError, ValueError, KeyError, IndexError) as exc:
            errors.append({"assertion_id": assertion["id"], "reason": str(exc)})
    return {"verified_excerpt_anchors": verified, "stale_assertions": stale,
            "errors": errors, "musicological_validation": False}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="AnaMu: source-checked extraction ledger")
    parser.add_argument("--repo", type=Path, default=REPO_ROOT)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("status")
    todo = commands.add_parser("queue")
    todo.add_argument("--kind", choices=["course_markdown", "shared_markdown", "structured_register_json"])
    todo.add_argument("--source")
    todo.add_argument("--limit", type=int, default=20)
    todo.add_argument("--packets", action="store_true", help="Include verified bounded source content")
    commands.add_parser("audit-anchors", help="Read source bytes and verify exact assertion excerpts")
    show = commands.add_parser("packet")
    show.add_argument("material_id")
    args = parser.parse_args(argv)
    repo = args.repo.resolve()
    try:
        ledger = load_ledger(repo / "analysis/knowledge")
        if args.command == "status":
            result = status(ledger)
        elif args.command == "queue":
            result = queue(ledger, kind=args.kind, source=args.source, limit=args.limit)
            if args.packets:
                result = packets(repo, result)
        elif args.command == "audit-anchors":
            result = audit_anchors(repo, ledger)
            if result["errors"] or result["stale_assertions"]:
                print(json.dumps(result, ensure_ascii=False, indent=2))
                parser.exit(1)
        else:
            row = next((r for r in ledger["rows"] if r["material_id"] == args.material_id), None)
            if row is None:
                raise ValueError("Unknown material: " + args.material_id)
            result = source_packet(repo, row)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (OSError, ValueError, TypeError, KeyError, IndexError, StopIteration) as exc:
        parser.exit(2, "Extraction ledger stopped: " + str(exc) + "\n")


if __name__ == "__main__":
    main()
