"""Conservative proof-route planner for AnaMu, not a music detector.

It never executes musical operations or promotes observations to conclusions.
It lists which proof routes are admissible, assumed, or missing in one profile.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
from typing import Any

STATES = {"unavailable": 0, "candidate": 1, "declared": 2, "verified": 3}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Case file must be a JSON object")
    return value


def require_strings(values: Any, field: str, nonempty: bool = False) -> list[str]:
    if not isinstance(values, list) or (nonempty and not values):
        raise ValueError(f"{field} must be a {'nonempty ' if nonempty else ''}list")
    if any(not isinstance(x, str) or not x.strip() for x in values):
        raise ValueError(f"{field} must contain nonempty strings")
    if len(values) != len(set(values)):
        raise ValueError(f"{field} contains duplicate identifiers")
    return values


def evidence_index(items: Any) -> tuple[dict[str, dict], list[dict]]:
    if not isinstance(items, list):
        raise ValueError("evidence profile must be a list")
    found: dict[str, dict] = {}
    audit: list[dict] = []
    evidence_ids: set[str] = set()
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            raise ValueError("evidence item requires a string id")
        if item["id"] in evidence_ids:
            raise ValueError("duplicate evidence id: " + item["id"])
        evidence_ids.add(item["id"])
        status = item.get("state", "candidate")
        if status not in STATES:
            raise ValueError("unknown evidence state: " + str(status))
        facts = require_strings(item.get("facts", []), "evidence.facts")
        for fact in facts:
            previous = found.get(fact)
            if previous is None or STATES[status] > STATES[previous["state"]]:
                found[fact] = {"state": status, "evidence_id": item["id"]}
        audit.append({"id": item["id"], "state": status, "facts": facts,
                      "provenance": item.get("provenance"),
                      "note": item.get("note")})
    return found, audit


def evaluate_route(route: dict, evidence: dict[str, dict]) -> dict:
    if not isinstance(route, dict) or not isinstance(route.get("id"), str):
        raise ValueError("route requires a string id")
    required = require_strings(route.get("all_of"), "route.all_of", nonempty=True)
    missing = [fact for fact in required if fact not in evidence or
               evidence[fact]["state"] == "unavailable"]
    candidate = [fact for fact in required if fact in evidence and
                 evidence[fact]["state"] == "candidate"]
    assumptions = [fact for fact in required if fact in evidence and
                   evidence[fact]["state"] == "declared"]
    verified = [fact for fact in required if fact in evidence and
                evidence[fact]["state"] == "verified"]
    status = "blocked_missing_or_unverified_evidence"
    if not missing and not candidate:
        status = "ready_under_declared_assumptions" if assumptions else "ready_verified_inputs"
    return {"route_id": route["id"], "state": status,
            "required": required, "verified": verified,
            "assumptions": assumptions, "candidate_not_accepted": candidate,
            "missing": missing,
            "candidate_outputs_only": route.get("candidate_outputs_only", []),
            "does_not_establish": route.get("does_not_establish", [])}


def plan(case: dict, profile: str) -> dict:
    if case.get("schema_version") != 1:
        raise ValueError("unsupported planner case schema")
    profiles = case.get("profiles")
    if not isinstance(profiles, dict) or profile not in profiles:
        raise ValueError("unknown evidence profile: " + profile)
    evidence, audit = evidence_index(profiles[profile])
    tasks = case.get("tasks", [])
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("nonempty tasks array required")
    seen_ids: set[str] = set()
    evaluated = []
    for task in tasks:
        if not isinstance(task, dict) or not isinstance(task.get("id"), str):
            raise ValueError("task requires a string id")
        if task["id"] in seen_ids:
            raise ValueError("duplicate task: " + task["id"])
        seen_ids.add(task["id"])
        routes = task.get("proof_routes", [])
        if not isinstance(routes, list) or not routes:
            raise ValueError("task requires at least one proof route: " + task["id"])
        checked = [evaluate_route(r, evidence) for r in routes]
        route_ids = [r["route_id"] for r in checked]
        if len(route_ids) != len(set(route_ids)):
            raise ValueError("duplicate route in task: " + task["id"])
        ready = [r for r in checked if r["state"] != "blocked_missing_or_unverified_evidence"]
        task_state = "blocked_missing_or_unverified_evidence"
        if any(r["state"] == "ready_verified_inputs" for r in ready):
            task_state = "ready_verified_inputs"
        elif ready:
            task_state = "ready_under_declared_assumptions"
        evaluated.append({"id": task["id"], "question": task.get("question"),
                          "state": task_state, "proof_routes": checked,
                          "knowledge_refs": task.get("knowledge_refs", []),
                          "material_refs": task.get("material_refs", []),
                          "cannot_establish": task.get("cannot_establish", []),
                          "revisit_when": task.get("revisit_when", []),
                          "execution_state": "not_executed_by_planner"})
    counts = Counter(task["state"] for task in evaluated)
    return {"schema_version": 1, "case_id": case.get("case_id"),
            "question": case.get("question"), "evidence_profile": profile,
            "limitation": "Proof-route scheduling only. No observations, musical conclusions or evaluations have been executed.",
            "evidence_audit": audit, "task_counts": dict(sorted(counts.items())),
            "tasks": evaluated}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="AnaMu: plan evidence routes without interpreting a work")
    parser.add_argument("case", type=Path, help="case contract JSON with tasks and evidence profiles")
    parser.add_argument("--profile", required=True, help="name of an evidence profile in the case")
    parser.add_argument("--out", type=Path, help="optional JSON report path; stdout by default")
    args = parser.parse_args(argv)
    try:
        report = plan(load_json(args.case), args.profile)
        rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(rendered, encoding="utf-8")
        else:
            print(rendered, end="")
    except (OSError, ValueError, TypeError, KeyError) as exc:
        parser.exit(2, "Planning stopped: " + str(exc) + "\n")


if __name__ == "__main__":
    main()
