"""Plan all curated knowledge, run bounded observations, and expose omissions."""
from __future__ import annotations

from collections import Counter
from pathlib import Path

from . import __version__
from .detectors import DETECTORS, run_detectors
from .knowledge import MODULE_ROOT, REPO_ROOT, compile_knowledge, sha256
from .midi_io import read_midi


def analyse(path: Path, profile="unknown", repo: Path = REPO_ROOT, extra_inputs=None):
    repo = repo.resolve()
    knowledge = compile_knowledge(repo)
    for concept in knowledge["concepts"]:
        unknown = set(concept["detectors"]) - DETECTORS.keys()
        if unknown:
            raise ValueError(f"Unknown detector contract {concept['id']}: {sorted(unknown)}")
    features = read_midi(path, profile)
    resolved = path.resolve()
    features["input_path"] = resolved.relative_to(repo).as_posix() if resolved.is_relative_to(repo) else resolved.name
    modalities = {"midi": {"state": "parsed", "sha256": features["sha256"]}}
    for modality in ["audio", "score", "lyrics", "context"]:
        supplied = (extra_inputs or {}).get(modality)
        if supplied:
            supplied = Path(supplied)
            if not supplied.is_file():
                raise ValueError("Additional input is not a file: " + str(supplied))
            modalities[modality] = {"state": "provided_not_interpreted", "sha256": sha256(supplied.read_bytes()),
                                    "adapter_status": "not_implemented"}
        else:
            modalities[modality] = {"state": "not_provided"}
    observations, execution = run_detectors(features)
    by_detector = {d["id"]: d for d in execution}
    counts = Counter(c for observation in observations for c in observation["concept_ids"])
    known_ids = {c["id"] for c in knowledge["concepts"]}
    if not set(counts) <= known_ids:
        raise ValueError("Observation not bound to a curated concept")
    plan = []
    for concept in knowledge["concepts"]:
        missing = [name for name in concept["requires"] if modalities[name]["state"] != "parsed"]
        if not concept["detectors"]:
            state = "documented_not_implemented"
        elif missing:
            state = "blocked_missing_interpreted_inputs"
        elif any(by_detector[d]["status"] == "blocked" for d in concept["detectors"]):
            state = "blocked_detector_contract"
        elif counts[concept["id"]]:
            state = "limited_observations_available"
        else:
            state = "mechanism_ran_no_matching_observation"
        plan.append({"concept_id": concept["id"], "name": concept["name"], "state": state,
            "missing_interpreted_inputs": missing, "provided_but_not_interpreted": [n for n in missing if modalities[n]["state"] == "provided_not_interpreted"],
            "observation_count": counts[concept["id"]], "prerequisites": concept["prerequisites"],
            "definition": concept["definition"], "question": concept["question"],
            "source_refs": concept["sources"], "limits": concept["limits"],
            "meaning": "Observations do not certify complete musical analysis or complete coverage of this concept"})
    by_concept = {p["concept_id"]: p for p in plan}
    courses = []
    for course in knowledge["courses"]:
        courses.append({"source_document_id": course["id"], "course_id": course["course_id"], "path": course["path"],
            "source_fragment_count": course["fragment_count"], "semantic_integration": course["semantic_integration"],
            "linked_concepts": [{"id": c, "state": by_concept[c]["state"]} for c in course["concept_ids"]],
            "complete_course_analysis": False})
    return {"schema_version": 1, "engine_version": __version__,
        "implementation_sha256": {p.name: sha256(p.read_bytes()) for p in sorted((MODULE_ROOT / "anamu_analysis").glob("*.py"))},
        "knowledge_source_fingerprint": knowledge["source_fingerprint"],
        "coverage": knowledge["coverage"], "input_modalities": modalities,
        "features": features, "observations": observations, "detector_execution": execution,
        "concept_plan": plan, "course_audit": courses, "course_identity_groups": knowledge["course_identity_groups"],
        "choice_families": knowledge["choice_families"],
        "summary": {"note_attacks": len(features["notes"]), "observations": len(observations),
            "concept_states": dict(sorted(Counter(p["state"] for p in plan).items())),
            "course_documents_indexed": len(courses),
            "course_documents_fully_integrated": 0, "complete_piece_analysis": False},
        "limits": [
            "Every course document is indexed; only the explicitly curated initial concepts are reconciled.",
            "Unreconciled fragments are visible integration work; they are not silently treated as analysed knowledge.",
            "The first mechanisms report encoded facts and conditional structural candidates, not an academic analysis of the complete piece.",
            "No key, Roman-numeral function, cadence, voice role, perceptual phrase or style is asserted from pitch-set matches.",
            "Audio, score, lyric association and contextual interpretation adapters are not implemented; supplied files do not change this.",
            "No composition generator or external model is called.",
        ]}


STATE_FR = {
    "documented_not_implemented": "Documenté, mécanisme à construire",
    "blocked_missing_interpreted_inputs": "Entrées interprétées manquantes",
    "blocked_detector_contract": "Contrat d'observation non satisfait",
    "limited_observations_available": "Observations limitées disponibles",
    "mechanism_ran_no_matching_observation": "Mécanisme exécuté sans observation correspondante",
}


def markdown_report(report):
    coverage = report["coverage"]
    counts = Counter(candidate["pitch_set_template"] for observation in report["observations"]
                     for candidate in observation["candidate_interpretations"])
    lines = ["# AnaMu — première lecture d'un morceau", "",
        f"Entrée : `{report['features']['input_path']}`. Profil déclaré : `{report['features']['profile_declared']}`.",
        f"Empreinte MIDI : `{report['features']['sha256']}`.", "",
        "## Périmètre effectivement mobilisé", "",
        f"{coverage['course_documents_indexed']} fiches indexées, {coverage['source_fragments']} fragments conservés, "
        f"{coverage['curated_concepts']} premiers concepts rapprochés. "
        f"{coverage['course_documents_with_curated_links']} fiches ont un lien curaté; aucune n'est entièrement intégrée.", "",
        f"{report['summary']['note_attacks']} attaques lues; {report['summary']['observations']} observations limitées. "
        "Ce rapport n'est pas une analyse complète du morceau.", "",
        "## Observations et interprétations candidates", "",
        "Les sonorités sont calculées sur les intervalles de touches actives. La pédale et la résonance ne sont pas rendues. "
        "Les comptes ci-dessous portent sur des fenêtres et lectures candidates, pas sur un nombre d'accords fonctionnels.", "",
        "| Famille de sonorité candidate | Lectures / fenêtres |", "|---|---:|"]
    lines += [f"| {name} | {n} |" for name, n in sorted(counts.items())]
    if not counts:
        lines.append("| Aucune lecture verticale produite dans le contrat courant | 0 |")
    lines += ["", "## État de chaque connaissance rapprochée", "",
        "| Concept | État | Observations | Source / section |", "|---|---|---:|---|"]
    for concept in report["concept_plan"]:
        ref = concept["source_refs"][0]
        source = f"{ref['path']}:{ref['start_line']}"
        lines.append(f"| {concept['name']} | {STATE_FR[concept['state']]} | {concept['observation_count']} | `{source}` |")
    lines += ["", "## Couverture et inconnus", "",
        "Le JSON contient une ligne d'audit pour chaque cours, les références exactes des concepts, les observations "
        "et les événements qui les établissent. Une ligne sans concept rapproché est une lacune d'intégration explicite.", "",
        "La fonction harmonique, les cadences, les voix, la forme perceptive, les instruments réels et le texte chanté "
        "ne sont pas déduits automatiquement. Les entrées supplémentaires fournies restent signalées comme non interprétées.", "",
        f"Empreinte des sources de connaissance : `{report['knowledge_source_fingerprint']}`.", ""]
    return "\n".join(lines)
