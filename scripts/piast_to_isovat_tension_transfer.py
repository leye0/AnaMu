"""Zero-shot MIDI-only transfer: PIAST 'Tense' -> IsoVAT listener tension.

PIAST labels fit the models; IsoVAT 30 MIDIs are **never** used for tuning,
calibration or feature selection. We rank within ten controlled triplets,
using the aggregate human order (NOT the composer's intended H/M/L).

Status: exploratory because the researcher previously inspected IsoVAT's
human orders in a different test, and the two emotion definitions differ.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from anamu.emotion_pipeline import extract_academic_rows, infer_measure_count
from anamu.piast_research_cues import midi_emotion_cues
from anamu.tonal_motion import (
    TONAL_DISTRIBUTION_FEATURE_NAMES, TONAL_MOTION_FEATURE_NAMES,
    midi_tonal_motion,
)
from .isovat_tension_benchmark import HUMAN_TENSION_ORDER, physical_observables, ribbon_observables, score_order
from .piast_at_benchmark import make_matrix, run, summarize_measures


ARMS = ("baseline", "distribution", "temporal")
SEED = 20261108


def _features(path: Path) -> dict:
    measures = infer_measure_count(path)
    rows, _, _ = extract_academic_rows(path, measures, academic=False, full_fusion=False)
    return {**summarize_measures(rows), **midi_emotion_cues(path),
            **midi_tonal_motion(path, seed=SEED)}


def _family(data: dict, name: str) -> dict:
    base = {k: v for k, v in data.items() if k not in TONAL_MOTION_FEATURE_NAMES}
    if name == "baseline":
        return base
    return {**base, **{k: data[k] for k in (
        TONAL_DISTRIBUTION_FEATURE_NAMES if name == "distribution"
        else TONAL_MOTION_FEATURE_NAMES)}}


def permutation_null(results: dict[str, dict], *, repetitions: int = 20000) -> dict:
    """Familywise null for best-of-3, randomly ordered listeners within set."""
    randomizer = random.Random(SEED)
    orders = ("HML", "HLM", "MHL", "MLH", "LHM", "LMH")
    observed_max = max(r["correct_pairs"] for r in results.values())
    observed_exact = max(r["exact_orders"] for r in results.values())
    exceed_pairs = exceed_exact = 0
    for _ in range(repetitions):
        shuffled = {i: randomizer.choice(orders) for i in HUMAN_TENSION_ORDER}
        max_pairs = max_exact = 0
        for arm, result in results.items():
            counts = [score_order(result["by_set"][str(i)]["scores"], shuffled[i])
                      for i in HUMAN_TENSION_ORDER]
            max_pairs = max(max_pairs, sum(c["pairwise_correct"] for c in counts))
            max_exact = max(max_exact, sum(c["exact_order"] for c in counts))
        exceed_pairs += max_pairs >= observed_max
        exceed_exact += max_exact >= observed_exact
    return {"iterations": repetitions, "best_of_3_observed_pairs": observed_max,
            "best_of_3_observed_exact": observed_exact,
            "familywise_p_pairs": (exceed_pairs + 1) / (repetitions + 1),
            "familywise_p_exact": (exceed_exact + 1) / (repetitions + 1),
            "null": "independent uniform listener rank permutations within ten sets",
            "caveat": "does not adjust for selection of this research direction after previous results"}


def experiment(piast: Path, isovat: Path, out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    extraction = run(piast, feature_set="research_tonal_motion", limit=1900,
                     cache_dir=out / "piast-cache", extract_only=True)
    training = extraction["records"]
    if extraction["matched"] != len(training) or len(training) != 1900 or extraction["rejected"]:
        raise AssertionError("incomplete_piast_training")
    sample_paths = {f"T-{i:02d}-{level}": isovat / f"T-{i:02d}-{level}.mid"
                    for i in HUMAN_TENSION_ORDER for level in "HML"}
    if not all(path.is_file() for path in sample_paths.values()):
        raise FileNotFoundError("incomplete_isovat_tension_dataset")
    samples = {}
    for key, path in sample_paths.items():
        samples[key] = _features(path)
        print(f"IsoVAT MIDI {len(samples)}/30: {key}", flush=True)
    labels = np.asarray([int("Tense" in clip.mood_tags()) for clip, _ in training])
    if not 0 < np.sum(labels) < len(labels):
        raise AssertionError("untrainable_tense")
    models = {}
    for arm in ARMS:
        rows = [(c, _family(data, arm)) for c, data in training]
        columns = sorted({k for _, data in rows for k in data})
        train_x = make_matrix(rows, columns)
        test_keys = sorted(samples)
        test_x = np.asarray([[_family(samples[k], arm).get(col, np.nan) for col in columns]
                             for k in test_keys], dtype=float)
        model = Pipeline([
            ("missing", SimpleImputer(strategy="median", keep_empty_features=True,
                                       add_indicator=True)),
            ("scale", StandardScaler()),
            ("classifier", LogisticRegression(C=.5, class_weight="balanced",
                                               max_iter=1200, random_state=SEED)),
        ])
        model.fit(train_x, labels)
        probs = model.predict_proba(test_x)[:, 1]
        models[arm] = {key: float(prob) for key, prob in zip(test_keys, probs)}
    ranks = {}
    for arm in ARMS:
        by_set = {}
        for i, human in HUMAN_TENSION_ORDER.items():
            scores = {level: models[arm][f"T-{i:02d}-{level}"] for level in "HML"}
            by_set[str(i)] = {**score_order(scores, human), "scores": scores}
        ranks[arm] = {
            "exact_orders": sum(r["exact_order"] for r in by_set.values()),
            "correct_pairs": sum(r["pairwise_correct"] for r in by_set.values()),
            "by_set": by_set,
        }
    control_scores = {}
    for i, human in HUMAN_TENSION_ORDER.items():
        scores = {}
        for level in "HML":
            midi = sample_paths[f"T-{i:02d}-{level}"]
            physical = physical_observables(midi)
            ribbon = ribbon_observables(midi)
            scores[level] = {
                "note_density": physical["arousal_onsets_per_second"],
                "cloud_diameter": ribbon["cloud_diameter_mean"],
            }
        control_scores[str(i)] = {
            name: score_order({level: scores[level][name] for level in "HML"}, human)
            for name in ("note_density", "cloud_diameter")
        }
    controls = {name: {
        "correct_pairs": sum(control_scores[str(i)][name]["pairwise_correct"]
                             for i in HUMAN_TENSION_ORDER),
        "exact_orders": sum(control_scores[str(i)][name]["exact_order"]
                            for i in HUMAN_TENSION_ORDER),
    } for name in ("note_density", "cloud_diameter")}
    result = {
        "study": "Independent-corpus transfer of PIAST Tense onto IsoVAT listener-ranked tension",
        "status": "exploratory; IsoVAT human ranks previously examined for different observables",
        "corpus": "1900 PIAST training MIDI; 30 IsoVAT symbolic MIDI, ten controlled listener triplets",
        "source_isovat_commit": "f62317920edd85ef4862e8f77633dc19f1a54c92",
        "human_ground_truth": "Plut et al. (2022) Table 8, Aggregate G-T Order",
        "train_tag": "PIAST Tense consensus >=2 of 3 expert mood annotators",
        "test_concept": "relative tension as perceived in IsoVAT listener judgments",
        "model": "one fixed class-balanced logistic regression C=.5 per feature family",
        "no_isovat_model_selection_or_tuning": True,
        "input": "MIDI alone; no audio, lyrics or emotion text for features",
        "train_clip_count": len(training), "positive_train": int(np.sum(labels)),
        "isovat_test_count": len(samples),
        "results": ranks, "controls": controls,
        "random_order_null": permutation_null(ranks),
        "limitations": [
            "PIAST 'Tense' is a perceived adjective, whereas IsoVAT ranks perceived tension; not identical measurement.",
            "Mixed-genre, multi-instrument four-bar clips differ substantially from PIAST solo piano.",
            "Only 10 triplets; their human orders were inspected in prior work. No claim of independent scientific confirmation.",
            "Class probabilities cannot be compared as calibrated perceived-tension intensities.",
        ],
    }
    (out / "tense-transfer.json").write_text(json.dumps(result, indent=2,
                        ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    lines = ["# PIAST Tense → IsoVAT tension : transfert entre corpus", "",
             "**Exploratoire ; aucun ajustement des modèles sur IsoVAT.**", "",
             "| Modèle | Paires correctement classées / 30 | Ordres exacts / 10 |",
             "|---|---:|---:|"]
    for name in ARMS:
        lines.append(f"| {name} | {ranks[name]['correct_pairs']} | {ranks[name]['exact_orders']} |")
    for name, row in controls.items():
        lines.append(f"| Témoin : {name} | {row['correct_pairs']} | {row['exact_orders']} |")
    lines += ["", f"Contrôle de sélection parmi les trois modèles : "
              f"p permutations par groupe = {result['random_order_null']['familywise_p_pairs']:.4f} "
              f"pour les paires, {result['random_order_null']['familywise_p_exact']:.4f} pour les ordres complets.",
              "", "## Détail des classements humains", "",
              "| Triplet | Ordre humain | Baseline | Distribution | Séquence |",
              "|---|---|---|---|---|"]
    for i, human in HUMAN_TENSION_ORDER.items():
        lines.append(f"| T-{i:02d} | {human} | " + " | ".join(
            ranks[arm]["by_set"][str(i)]["predicted"] for arm in ARMS) + " |")
    lines += ["", "IsoVAT = 30 MIDI composés en groupes de trois de même genre et instrumentation ; "
              "les ordres de référence viennent des auditeurs, **pas** des noms H/M/L.",
              "Les deux taxonomies émotionnelles et les domaines musicaux diffèrent : "
              "une réussite serait encourageante, pas une preuve d'une loi universelle.", ""]
    (out / "tense-transfer.md").write_text("\n".join(lines), encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("piast", type=Path)
    parser.add_argument("isovat_tension", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    experiment(args.piast, args.isovat_tension, args.out)
    print((args.out / "tense-transfer.md").read_text(encoding="utf-8"), flush=True)


if __name__ == "__main__":
    main()
