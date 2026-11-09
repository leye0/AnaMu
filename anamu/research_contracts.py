"""Fail-closed contracts for the human labels and academic methods used by AnaMu.

This validates *what an experiment can claim*, not the predictive correctness
of its implementation. In particular, extracting temporal features from MIDI
does not create temporally annotated human labels.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


CATALOG_PATH = Path(__file__).resolve().parents[1] / "data" / "research-evidence.json"

CLAIM_TARGETS = {
    "global_mood_association": {"mood_tags", "named_emotion_song"},
    "temporal_valence_arousal_association": {"valence_arousal_continuous"},
    "relative_perceived_tension": {"relative_tension"},
    "relative_performance_attributes": {"performance_perceptual_attributes"},
    "relative_performance_valence_arousal": {"performance_valence_arousal"},
    "musicological_cadence_detection": {"cadence_event"},
}


class ResearchContractError(ValueError):
    """A scientific claim lacks the observations or provenance it requires."""


def load_catalog(path: Path = CATALOG_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ResearchContractError(message)


def check_experiment(name: str, experiment: dict, catalog: dict) -> None:
    """Refuse unsupported target, time resolution, grouping, or engine claims."""
    _require(isinstance(experiment, dict), f"{name}: experiment must be an object")
    source_id = experiment.get("source")
    sources = catalog["sources"]
    methods = catalog["methods"]
    _require(isinstance(source_id, str) and source_id in sources,
             f"{name}: unknown source {source_id!r}")
    source = sources[source_id]

    target = experiment.get("target")
    _require(target in source["human_targets"],
             f"{name}: {source_id} does not expose human target {target!r}; "
             f"available: {source['human_targets']}")
    _require(experiment.get("requires_temporal_human_labels") is True or
             experiment.get("requires_temporal_human_labels") is False,
             f"{name}: explicitly declare requires_temporal_human_labels")
    _require(experiment.get("requires_individual_votes") is True or
             experiment.get("requires_individual_votes") is False,
             f"{name}: explicitly declare requires_individual_votes")
    _require(not experiment["requires_temporal_human_labels"] or
             source["temporal_human_labels"],
             f"{name}: {source_id} has no time-resolved human labels")
    _require(not experiment["requires_individual_votes"] or
             source["individual_votes_available"],
             f"{name}: {source_id} does not expose independently usable votes")
    _require(experiment.get("split_group") == source["independent_group"],
             f"{name}: split must group by {source['independent_group']!r} "
             f"(requested {experiment.get('split_group')!r})")

    scope = experiment.get("claim_scope")
    _require(scope in CLAIM_TARGETS, f"{name}: unknown or unsupported claim scope {scope!r}")
    _require(target in CLAIM_TARGETS[scope],
             f"{name}: claim scope {scope!r} incompatible with {target!r}")
    if scope == "temporal_valence_arousal_association":
        _require(experiment["requires_temporal_human_labels"],
                 f"{name}: temporal claim requires actual time-resolved human labels")

    status = experiment.get("status")
    _require(status in {"exploratory", "confirmatory"},
             f"{name}: status must be exploratory or confirmatory")
    _require(isinstance(experiment.get("previously_examined"), bool),
             f"{name}: explicitly declare whether test data were previously examined")
    if status == "confirmatory":
        _require(not experiment["previously_examined"],
                 f"{name}: already examined test data cannot confirm a new hypothesis")
        _require(experiment.get("independent_test_preregistered") is True,
                 f"{name}: confirmation requires independently frozen selection and test")

    claimed_methods = experiment.get("methods")
    _require(isinstance(claimed_methods, list) and bool(claimed_methods),
             f"{name}: declare at least one method with its exact provenance")
    ids = []
    for entry in claimed_methods:
        _require(isinstance(entry, dict), f"{name}: invalid method entry")
        method_id = entry.get("id")
        _require(isinstance(method_id, str) and method_id in methods,
                 f"{name}: unknown method {method_id!r}")
        ids.append(method_id)
        method = methods[method_id]
        claimed = entry.get("claim")
        if claimed == "published_engine_executed":
            _require(method["kind"] == "published_engine" and method["executed"],
                     f"{name}: {method_id} original engine not executed")
        elif claimed == "theory_inspired_proxy":
            _require(method["kind"] == "theory_inspired_proxy" and method["executed"],
                     f"{name}: {method_id} is not an executed proxy")
        else:
            raise ResearchContractError(
                f"{name}: unsupported provenance claim {claimed!r} for {method_id}")
    _require(len(set(ids)) == len(ids), f"{name}: duplicate method entries")


def validate_catalog(catalog: dict) -> None:
    _require(isinstance(catalog, dict) and catalog.get("schema_version") == 1,
             "unsupported research-evidence schema")
    for section in ("sources", "methods", "experiments"):
        _require(isinstance(catalog.get(section), dict) and bool(catalog[section]),
                 f"missing or empty {section}")
    for name, source in catalog["sources"].items():
        _require(isinstance(source, dict), f"{name}: invalid source entry")
        _require(str(source.get("primary_url", "")).startswith("https://"),
                 f"{name}: missing primary source URL")
        _require(isinstance(source.get("human_targets"), list) and
                 bool(source["human_targets"]) and
                 len(set(source["human_targets"])) == len(source["human_targets"]),
                 f"{name}: human targets must be a unique non-empty list")
        for field in ("temporal_human_labels", "individual_votes_available"):
            _require(isinstance(source.get(field), bool), f"{name}: missing boolean {field}")
        for field in ("unit", "midi_origin", "independent_group", "local_evidence", "limits"):
            _require(isinstance(source.get(field), str) and bool(source[field].strip()),
                     f"{name}: missing {field}")
    for name, method in catalog["methods"].items():
        _require(isinstance(method, dict), f"{name}: invalid method")
        _require(str(method.get("primary_url", "")).startswith("https://"),
                 f"{name}: missing method source URL")
        _require(method.get("kind") in {"published_engine", "theory_inspired_proxy"},
                 f"{name}: invalid method kind")
        _require(isinstance(method.get("executed"), bool),
                 f"{name}: missing engine execution status")
        _require(isinstance(method.get("observables"), list) and
                 bool(method["observables"]), f"{name}: missing observables")
        _require(isinstance(method.get("limit"), str) and bool(method["limit"].strip()),
                 f"{name}: missing limitation")
    for name, experiment in catalog["experiments"].items():
        check_experiment(name, experiment, catalog)


def check_registered_experiment(name: str) -> None:
    """Call at a benchmark entry point, before expensive data acquisition."""
    catalog = load_catalog()
    validate_catalog(catalog)
    _require(name in catalog["experiments"], f"unregistered experiment: {name}")

