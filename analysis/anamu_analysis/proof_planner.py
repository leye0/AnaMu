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
        if status == "verified" and (not isinstance(item.get("provenance"), str)
                                   or not item["provenance"].strip()):
            raise ValueError("verified-labelled evidence requires source provenance")
        facts = require_strings(item.get("facts", []), "evidence.facts")
        for fact in facts:
            if fact in found:
                raise ValueError("Same fact claimed by multiple evidence items: " +
                                 fact + ". Reconcile its provenance first.")
            # 'verified' is the state *declared by the upstream evidence
            # provider*. This planner does not independently authenticate
            # files, resolve sources or inspect musical assertions.
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


def fact_vocabulary(case: dict) -> set[str] | None:
    """Optional shared vocabulary. Validate names, never assert their truth."""
    ref = case.get("fact_registry_ref")
    if ref is None:
        return None
    if not isinstance(ref, str) or not ref:
        raise ValueError("fact_registry_ref must be a nonempty repository-relative path")
    repo = Path(__file__).resolve().parents[2]
    path = (repo / ref).resolve()
    allowed = repo / "analysis/knowledge"
    if not path.is_relative_to(allowed):
        raise ValueError("Fact registry must reside within analysis/knowledge")
    registry = load_json(path)
    if registry.get("schema_version") != 1:
        raise ValueError("Unsupported evidence fact registry schema")
    values = registry.get("facts")
    if not isinstance(values, list):
        raise ValueError("Evidence fact registry must have a facts array")
    ids = require_strings([f.get("id") for f in values
                           if isinstance(f, dict)], "registry.facts")
    if len(ids) != len(values):
        raise ValueError("Malformed evidence fact definition")
    return set(ids)


def check_fact_vocabulary(case: dict, known: set[str] | None) -> None:
    if known is None:
        return
    for name, entries in case["profiles"].items():
        for entry in entries:
            for fact in entry.get("facts", []):
                if fact not in known:
                    raise ValueError("Unknown evidence fact in profile " +
                                     name + ": " + str(fact))
    for task in case["tasks"]:
        for route in task.get("proof_routes", []):
            for fact in route.get("all_of", []):
                if fact not in known:
                    raise ValueError("Unknown evidence fact in route " +
                                     route.get("id", "?") + ": " + str(fact))


def execution_order(tasks: list[dict]) -> list[str]:
    """Order *candidate* operations, not musical events or proven claims."""
    by_id = {task["id"]: task for task in tasks}
    if len(by_id) != len(tasks):
        raise ValueError("Duplicate candidate operation IDs")
    dependencies: dict[str, list[str]] = {}
    for task in tasks:
        needed = require_strings(task.get("depends_on", []),
                                 "task.depends_on")
        if any(ref not in by_id for ref in needed):
            raise ValueError("Unknown execution prerequisite in: " + task["id"])
        if task["id"] in needed:
            raise ValueError("Self-dependency in task: " + task["id"])
        dependencies[task["id"]] = needed
    ordered = []
    active: set[str] = set()
    complete: set[str] = set()

    def visit(identifier: str) -> None:
        if identifier in active:
            raise ValueError("Execution prerequisite cycle: " + identifier)
        if identifier in complete:
            return
        active.add(identifier)
        for predecessor in dependencies[identifier]:
            visit(predecessor)
        active.remove(identifier)
        complete.add(identifier)
        ordered.append(identifier)

    for task in tasks:
        visit(task["id"])
    return ordered


def plan(case: dict, profile: str) -> dict:
    if case.get("schema_version") != 1:
        raise ValueError("unsupported planner case schema")
    profiles = case.get("profiles")
    if not isinstance(profiles, dict) or profile not in profiles:
        raise ValueError("unknown evidence profile: " + profile)
    scope = case.get("scope_ref")
    if scope is not None:
        if not isinstance(scope, str) or not scope.strip():
            raise ValueError("scope_ref must be a nonempty string")
        for name, items in profiles.items():
            for item in items:
                if item.get("scope_ref") != scope:
                    raise ValueError("Evidence scope mismatch in profile " + name +
                                     ": " + str(item.get("id")))
        for task in case.get("tasks", []):
            if task.get("scope_ref") != scope:
                raise ValueError("Task scope mismatch: " + str(task.get("id")))
    evidence, audit = evidence_index(profiles[profile])
    known_facts = fact_vocabulary(case)
    check_fact_vocabulary(case, known_facts)
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
    ordering = execution_order(tasks)
    rank = {identifier: index + 1 for index, identifier in enumerate(ordering)}
    declarations = {task["id"]: task for task in tasks}
    for task in evaluated:
        predecessors = declarations[task["id"]].get("depends_on", [])
        task["depends_on"] = predecessors
        task["schedule_rank"] = rank[task["id"]]
        task["predecessors_are_executed"] = False if predecessors else None
        task["executable_now"] = (
            task["state"] != "blocked_missing_or_unverified_evidence"
            and not predecessors)
        # Dependencies being *ready* never makes their observations exist.
    counts = Counter(task["state"] for task in evaluated)
    return {"schema_version": 1, "case_id": case.get("case_id"),
            "question": case.get("question"), "source_note": case.get("source_note"),
            "scope_ref": case.get("scope_ref"),
            "evidence_profile": profile,
            "fact_registry_ref": case.get("fact_registry_ref"),
            "vocabulary_note": (
                "A registered proof requirement is a known question, not proof "
                "that the required fact holds for this piece."),
            "limitation": "Proof-route scheduling only. No observations, musical conclusions or evaluations have been executed.",
            "verification_boundary": (
                "Evidence states, including verified, are supplied by the case profile; "
                "the planner requires provenance but cannot authenticate it. "
                "Ready_verified_inputs is not an independent proof audit."),
            "evidence_audit": audit, "task_counts": dict(sorted(counts.items())),
            "candidate_execution_order": ordering,
            "execution_order_note": (
                "Scheduling prerequisites are not proofs. An upstream task "
                "must actually run before a dependent task can be executed."),
            "tasks": evaluated}


def compare_profiles(case: dict, before: str, after: str) -> dict:
    """Describe changes in task readiness, without inferring musical conclusions."""
    first, second = plan(case, before), plan(case, after)
    prior = {task["id"]: task for task in first["tasks"]}
    current = {task["id"]: task for task in second["tasks"]}
    changed = [
        {"task_id": identifier, "before": prior[identifier]["state"],
         "after": task["state"],
         "newly_ready_under_assumptions": (
             prior[identifier]["state"] == "blocked_missing_or_unverified_evidence"
             and task["state"] == "ready_under_declared_assumptions"),
         "newly_ready_verified": (
             prior[identifier]["state"] == "blocked_missing_or_unverified_evidence"
             and task["state"] == "ready_verified_inputs")}
        for identifier, task in current.items()
        if task["state"] != prior[identifier]["state"]
    ]
    left_facts, _ = evidence_index(case["profiles"][before])
    right_facts, _ = evidence_index(case["profiles"][after])
    improved = sorted({fact for fact, entry in right_facts.items()
                       if fact in left_facts
                       and STATES[entry["state"]] > STATES[left_facts[fact]["state"]]} |
                      {fact for fact in right_facts if fact not in left_facts})
    return {"schema_version": 1, "case_id": case["case_id"],
            "before_profile": before, "after_profile": after,
            "newly_available_or_upgraded_facts": improved,
            "changed_task_states": changed,
            "task_counts_before": first["task_counts"],
            "task_counts_after": second["task_counts"],
            "limitation": "Planning comparison only; no musical interpretation executed."}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="AnaMu: plan evidence routes without interpreting a work")
    parser.add_argument("case", type=Path, help="case contract JSON with tasks and evidence profiles")
    parser.add_argument("--profile", required=True, help="name of an evidence profile in the case")
    parser.add_argument("--compare", help="optional second profile for a change-of-evidence comparison")
    parser.add_argument("--out", type=Path, help="optional JSON report path; stdout by default")
    args = parser.parse_args(argv)
    try:
        case = load_json(args.case)
        report = compare_profiles(case, args.profile, args.compare) if args.compare else plan(case, args.profile)
        rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
        if args.out:
            destination = args.out.resolve()
            repository = Path(__file__).resolve().parents[2]
            analysis = Path(__file__).resolve().parents[1]
            if destination.is_relative_to(repository) and not destination.is_relative_to(analysis):
                raise ValueError("Write planning outputs inside analysis/ or outside the repository")
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(rendered, encoding="utf-8")
        else:
            print(rendered, end="")
    except (OSError, ValueError, TypeError, KeyError) as exc:
        parser.exit(2, "Planning stopped: " + str(exc) + "\n")


if __name__ == "__main__":
    main()
