"""Connect actual encoded MIDI events to scoped proof planning.

This adapter exposes observed note attacks, not musical voices, harmonic
functions, audible decay or physical performers. Templates supply questions
and proof routes only; their hypothetical evidence profiles are never copied.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from .midi_io import read_midi
from .proof_planner import plan


def observe_midi(report: dict, start_tick: int = 0,
                 end_tick: int | None = None) -> dict:
    """Inventory attacks in one half-open tick window, without sounding-state inference."""
    if end_tick is None:
        end_tick = report["end_tick"] + 1
    if (type(start_tick) is not int or type(end_tick) is not int or
            not 0 <= start_tick < end_tick <= report["end_tick"] + 1):
        raise ValueError("Invalid half-open MIDI tick window")
    profile = report["profile_declared"]
    if profile not in {"unknown", "gm1"}:
        raise ValueError("Unknown MIDI profile")
    scope = (f'midi:sha256:{report["sha256"]}:'
             f'ticks:{start_tick}:{end_tick}:profile:{profile}')
    short = hashlib.sha256(scope.encode()).hexdigest()[:24]
    source = {"path": report["input_path"], "sha256": report["sha256"],
              "medium": "midi", "clock": "absolute_midi_ticks",
              "ticks_per_quarter": report["ticks_per_quarter"],
              "start_tick_inclusive": start_tick,
              "end_tick_exclusive": end_tick, "profile_declared": profile}
    notes = sorted((n for n in report["notes"]
                    if start_tick <= n["onset_tick"] < end_tick),
                   key=lambda n: (n["onset_tick"], n["track"], n["channel"], n["id"]))
    event_ids = [n["id"] for n in notes]
    if len(event_ids) != len(set(event_ids)):
        raise ValueError("Duplicate note event identities")
    observation = {
        "id": "observation:midi-attacks:" + short,
        "epistemic_kind": "encoded_observation", "scope_ref": scope,
        "source_ref": source, "event_refs": event_ids,
        "note_attacks": notes, "attack_count": len(notes),
        "limitations": ["No assignment of musical voices",
                        "Attack window, not all sounding or held notes",
                        "Key durations do not establish acoustic decay"],
    }
    observations = [observation]
    evidence = []

    def add(fact: str, state: str, note: str, refs: list[str],
            events: list[str], kind: str) -> None:
        evidence.append({
            "id": "evidence:" + short + ":" + fact,
            "scope_ref": scope, "state": state, "facts": [fact],
            "provenance": "MIDI bytes " + report["sha256"] + "; " + note,
            "note": note, "source_ref": source, "observation_refs": refs,
            "event_refs": events, "epistemic_kind": kind,
        })

    if notes:
        add("midi_note_events_verified", "verified",
            "Note attacks read by the MIDI parser in the stated tick window; "
            "verification is internal to the reader, not independent musicology.",
            [observation["id"]], event_ids, "encoded_observation")
    if profile == "gm1":
        add("gm_profile_declared", "declared",
            "GM1 explicitly chosen by the caller; not an inferred device profile.",
            [], [], "hypothesis")
        percussion = [n for n in notes if n["channel"] == 9]
        if percussion:
            percussion_ids = [n["id"] for n in percussion]
            gm = {
                "id": "observation:gm-channel10-attacks:" + short,
                "epistemic_kind": "derived_observation", "scope_ref": scope,
                "source_ref": source, "event_refs": percussion_ids,
                "note_attacks": percussion, "attack_count": len(percussion),
                "derived_from": [observation["id"]],
                "limitations": ["GM1 assumed", "No real instrument or player inferred"],
            }
            observations.append(gm)
            add("gm_percussion_events_supplied", "declared",
                "Channel-10 attacks observed under the caller's GM1 assumption.",
                [gm["id"]], percussion_ids, "derived_observation")
    return {
        "schema_version": 1, "scope_ref": scope, "source_ref": source,
        "observations": observations, "evidence_profile": evidence,
        "reader_warnings": report["warnings"],
        "boundary": "Only localized encoded note attacks and explicit GM1 assumption; "
                    "no inferred pitch spelling, voices, tonal function, physical "
                    "gestures, audio or perceptual judgments.",
    }


def instantiate_case(template: dict, packet: dict) -> dict:
    """Make a planning instance using actual evidence, never template evidence."""
    if template.get("schema_version") != 1 or not template.get("tasks"):
        raise ValueError("Expected a schema-1 case template with tasks")
    scope = packet["scope_ref"]
    old_scope = template.get("scope_ref")
    tasks = deepcopy(template["tasks"])
    for task in tasks:
        if task.get("scope_ref") != old_scope:
            raise ValueError("Template task has incompatible scope: " + task["id"])
        task["scope_ref"] = scope
    profile = deepcopy(packet["evidence_profile"])
    if any(item.get("scope_ref") != scope for item in profile):
        raise ValueError("Observation packet contains foreign evidence scope")
    return {
        "schema_version": 1,
        "case_id": template.get("case_id", "template") + "@" + scope,
        "question": template.get("question"),
        "source_note": ("Questions and routes chosen from a template by the caller; "
                        "applicability to this work has not been established. "
                        "Template profiles have been discarded."),
        "fact_registry_ref": template.get("fact_registry_ref"),
        "scope_ref": scope, "profiles": {"actual_midi_observations": profile},
        "tasks": tasks,
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="AnaMu: scoped evidence from real MIDI bytes")
    parser.add_argument("midi", type=Path)
    parser.add_argument("--midi-profile", choices=["unknown", "gm1"], default="unknown")
    parser.add_argument("--start-tick", type=int, default=0)
    parser.add_argument("--end-tick", type=int)
    parser.add_argument("--case-template", type=Path,
                        help="Optional proof-route template; prior profiles are ignored")
    args = parser.parse_args(argv)
    try:
        packet = observe_midi(read_midi(args.midi, args.midi_profile),
                              args.start_tick, args.end_tick)
        result = {"observation_packet": packet}
        if args.case_template:
            template = json.loads(args.case_template.read_text(encoding="utf-8"))
            case = instantiate_case(template, packet)
            result["case"] = case
            result["plan"] = plan(case, "actual_midi_observations")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (OSError, ValueError, TypeError, KeyError) as exc:
        parser.exit(2, "Proof inputs stopped: " + str(exc) + "\n")


if __name__ == "__main__":
    main()
