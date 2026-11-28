"""Compile explicit source-versioned assertion routes into proof-planner cases.

Only editorially authored route mappings are accepted. A missing assertion,
changed assertion, stale material revision, or changed source refuses the case.
Neither extracting an assertion nor compiling a task executes an analysis.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from .proof_planner import plan

REPO_ROOT = Path(__file__).resolve().parents[2]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(value) -> str:
    if isinstance(value, str):
        raw = value.encode("utf-8")
    elif isinstance(value, bytes):
        raw = value
    else:
        raw = json.dumps(value, sort_keys=True, ensure_ascii=False,
                         separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def operations(repo: Path) -> dict:
    registry = read_json(repo / "analysis/knowledge/assertion-routes.json")
    if registry.get("schema_version") != 1:
        raise ValueError("Unsupported assertion route registry schema")
    rows = registry["operations"]
    by_id = {row["id"]: row for row in rows}
    if len(rows) != len(by_id):
        raise ValueError("Duplicate operation identity")
    return by_id


def assertion_index(folder: Path) -> dict:
    found = {}
    for path in sorted((folder / "mentions").glob("*.json")):
        for assertion in read_json(path).get("assertions", []):
            identifier = assertion["id"]
            if identifier in found:
                raise ValueError("Duplicate assertion: " + identifier)
            found[identifier] = assertion
    return found


def verify_assertion(repo: Path, ref: dict, assertions: dict,
                     cache: dict) -> dict:
    identifier = ref["assertion_id"]
    assertion = assertions.get(identifier)
    if assertion is None:
        raise ValueError("Missing route assertion: " + identifier)
    if digest(assertion) != ref["assertion_sha256"]:
        raise ValueError("Route assertion changed; review mapping: " + identifier)
    if (assertion["material_id"] != ref["material_id"] or
            assertion["reviewed_material_revision"] != ref["material_revision"]):
        raise ValueError("Route assertion material/revision disagreement: " + identifier)
    span = assertion.get("source_span")
    if not span:
        raise ValueError("Route assertion has no versioned source span: " + identifier)
    path = span["document_path"]
    if path not in cache:
        chunk_path = (repo / "analysis/knowledge/materials/sources" /
                      (digest(path)[:20] + ".json"))
        chunk = read_json(chunk_path)
        if chunk["source_document"] != path:
            raise ValueError("Material chunk source mismatch: " + path)
        raw_path = (repo / path).resolve()
        if not raw_path.is_relative_to(repo / "docs"):
            raise ValueError("Knowledge source outside read-only docs/")
        raw = raw_path.read_bytes()
        cache[path] = (chunk, raw)
    chunk, raw = cache[path]
    matches = [u for u in chunk["units"] if u["id"] == ref["material_id"]]
    if len(matches) != 1:
        raise ValueError("Missing or duplicate route material: " + ref["material_id"])
    unit = matches[0]
    if unit["lifecycle"] != "active" or unit["revision"] != ref["material_revision"]:
        raise ValueError("Route material revision stale: " + ref["material_id"])
    primary = next(b for b in unit["source_bindings"] if b["role"] == "primary")
    if any(primary[k] != span[k] for k in
           ("document_path", "document_sha256", "content_sha256", "locator")):
        raise ValueError("Assertion source span no longer matches material: " + identifier)
    if digest(raw) != span["document_sha256"]:
        raise ValueError("Source document bytes changed: " + path)
    loc = span["locator"]
    if loc["kind"] == "markdown_fragment":
        lines = raw.decode("utf-8").splitlines(keepends=True)
        value = "".join(lines[loc["start_line"] - 1:loc["end_line"]])
    elif loc["kind"] == "json_pointer":
        value = json.loads(raw)
        for part in loc["json_pointer"].split("/")[1:]:
            part = part.replace("~1", "/").replace("~0", "~")
            value = value[int(part)] if isinstance(value, list) else value[part]
    else:
        raise ValueError("Unknown source locator: " + loc["kind"])
    if digest(value) != span["content_sha256"]:
        raise ValueError("Assertion source passage changed: " + identifier)
    return {"assertion_id": identifier, "material_id": unit["id"],
            "material_revision": unit["revision"], "source_span": span,
            "statement": assertion["statement"], "scope": assertion["scope"],
            "review_state": assertion["review_state"]}


def compile_case(repo: Path, operation_id: str, packet: dict | None = None) -> dict:
    repo = repo.resolve()
    operation = operations(repo).get(operation_id)
    if operation is None:
        raise ValueError("Unknown operation: " + operation_id)
    assertions = assertion_index(repo / "analysis/knowledge")
    scope = "unbound-planning:" + operation_id if packet is None else packet["scope_ref"]
    evidence = [] if packet is None else deepcopy(packet["evidence_profile"])
    tasks = []
    provenance = {}
    cache = {}
    for spec in operation["tasks"]:
        refs = spec["assertion_refs"]
        if not refs:
            raise ValueError("Operation task must have source assertion references")
        for ref in refs:
            verified = verify_assertion(repo, ref, assertions, cache)
            provenance[verified["assertion_id"]] = verified
        tasks.append({
            "id": spec["id"], "question": spec["question"], "scope_ref": scope,
            "knowledge_refs": [r["assertion_id"] for r in refs],
            "material_refs": sorted({r["material_id"] for r in refs}),
            "proof_routes": deepcopy(spec["proof_routes"]),
            "cannot_establish": spec["cannot_establish"],
            "depends_on": spec.get("depends_on", []),
            "revisit_when": ["source_assertion_revision_changed",
                             "new_or_revised_observation"],
        })
    case = {
        "schema_version": 1, "case_id": operation_id + "@" + scope,
        "question": operation["question"], "source_note": operation["scope_note"],
        "scope_ref": scope, "fact_registry_ref": "analysis/knowledge/evidence-facts.json",
        "profiles": {"scoped_inputs": evidence}, "tasks": tasks,
        "knowledge_provenance": list(provenance.values()),
        "boundary": "Source mappings verified; task readiness is not task execution "
                    "or independent musical validation.",
    }
    return case


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="AnaMu: source-versioned knowledge routes")
    parser.add_argument("--repo", type=Path, default=REPO_ROOT)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list")
    run = commands.add_parser("plan")
    run.add_argument("operation")
    run.add_argument("--evidence", type=Path,
                     help="Observation packet or proof_inputs output; absent means no evidence")
    args = parser.parse_args(argv)
    repo = args.repo.resolve()
    try:
        if args.command == "list":
            result = [{"id": row["id"], "question": row["question"],
                       "task_count": len(row["tasks"])}
                      for row in operations(repo).values()]
        else:
            packet = None
            if args.evidence:
                value = read_json(args.evidence)
                packet = value.get("observation_packet", value)
            case = compile_case(repo, args.operation, packet)
            result = {"case": case, "plan": plan(case, "scoped_inputs")}
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except (OSError, ValueError, TypeError, KeyError, IndexError, StopIteration) as exc:
        parser.exit(2, "Knowledge routes stopped: " + str(exc) + "\n")


if __name__ == "__main__":
    main()
