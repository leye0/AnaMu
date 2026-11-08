"""Can a within-composition *ranking objective* beat MIDI emotion regression?

All models use 288 symbolic CP-WTC piano performances and *human* labels.
Six outer GroupKFold folds hold out entire Bach compositions. Training pairs
are made ONLY from outer-training works, and C is selected by inner 4-fold
work-held-out validation. A label-shuffled-training arm audits spurious gains.

This is an exploratory experiment, not the ISMIR 2026 Delta-VA model.
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler

from .cp_wtc_relative_benchmark import (
    cluster_bootstrap_improvement, evaluate_pairs, load_examples,
    predict_out_of_fold, FEATURES,
)


DIMENSIONS = ((0, "arousal", 10.0), (1, "valence", 1.0))
CS = (0.01, 0.1, 1.0, 10.0)


def _pair_data(x: np.ndarray, y: np.ndarray, groups: np.ndarray,
               threshold: float) -> tuple[np.ndarray, np.ndarray]:
    diffs, targets = [], []
    for group in np.unique(groups):
        ids = np.flatnonzero(groups == group)
        for i, j in combinations(ids, 2):
            gap = float(y[i] - y[j])
            if abs(gap) < threshold:
                continue
            diff = x[i] - x[j]
            # Mirror pairs: a ranker's orientation must be arbitrary, and the
            # zero-intercept rank score must be antisymmetric.
            diffs.extend((diff, -diff))
            targets.extend((int(gap > 0), int(gap < 0)))
    if not diffs:
        raise ValueError("no_eligible_hard_training_pairs")
    return np.asarray(diffs), np.asarray(targets)


def _fit_ranker(x: np.ndarray, y: np.ndarray, groups: np.ndarray,
                *, threshold: float, c: float):
    scaler = StandardScaler().fit(x)
    normalized = scaler.transform(x)
    diffs, targets = _pair_data(normalized, y, groups, threshold)
    ranker = LogisticRegression(C=c, fit_intercept=False, max_iter=2000)
    ranker.fit(diffs, targets)
    return scaler, ranker


def _score(x: np.ndarray, model) -> np.ndarray:
    scaler, ranker = model
    return ranker.decision_function(scaler.transform(x)).reshape(-1)


def _hard_direction_counts(y: np.ndarray, pred: np.ndarray,
                           groups: np.ndarray, threshold: float) -> tuple[int, int]:
    correct = total = 0
    for group in np.unique(groups):
        ids = np.flatnonzero(groups == group)
        for i, j in combinations(ids, 2):
            gap = y[i] - y[j]
            if abs(gap) < threshold:
                continue
            estimated = pred[i] - pred[j]
            correct += int((gap > 0) == (estimated > 0))
            total += 1
    return correct, total


def _inner_select_c(x: np.ndarray, y: np.ndarray,
                    groups: np.ndarray, threshold: float) -> tuple[float, dict]:
    scores = []
    for c in CS:
        correct = total = 0
        for train, test in GroupKFold(n_splits=4).split(x, y, groups):
            fit = _fit_ranker(x[train], y[train], groups[train], threshold=threshold, c=c)
            estimated = _score(x[test], fit)
            wins, count = _hard_direction_counts(y[test], estimated, groups[test], threshold)
            correct += wins
            total += count
        scores.append((correct / total if total else -1., c))
    # Tie-break to *stronger regularization*, chosen without outer labels.
    accuracy, selected = max(scores, key=lambda v: (v[0], -v[1]))
    return selected, {str(c): score for score, c in scores}


def _permuted_labels(y: np.ndarray, groups: np.ndarray, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    result = y.copy()
    for group in np.unique(groups):
        ids = np.flatnonzero(groups == group)
        result[ids] = result[rng.permutation(ids)]
    return result


def benchmark(root: Path) -> dict:
    x, y, groups, _ = load_examples(root)
    baseline = predict_out_of_fold(x, y, groups, FEATURES)
    ranked = np.zeros_like(y)
    shuffled = np.zeros_like(y)
    inner_audit = {}
    outer = list(GroupKFold(n_splits=6).split(x, y, groups))
    for fold_id, (train, test) in enumerate(outer):
        if set(groups[train]) & set(groups[test]):
            raise AssertionError("composition_leakage")
        for dim, label, threshold in DIMENSIONS:
            c, inner = _inner_select_c(x[train], y[train, dim], groups[train], threshold)
            fit = _fit_ranker(x[train], y[train, dim], groups[train], threshold=threshold, c=c)
            ranked[test, dim] = _score(x[test], fit)
            shuffled_y = _permuted_labels(y[train, dim], groups[train],
                                          seed=20261109 + fold_id * 2 + dim)
            control_fit = _fit_ranker(x[train], shuffled_y, groups[train],
                                      threshold=threshold, c=c)
            shuffled[test, dim] = _score(x[test], control_fit)
            inner_audit[f"fold_{fold_id}_{label}"] = {
                "selected_c": c, "inner_hard_accuracy_by_c": inner,
                "held_out_works": [int(v) for v in np.unique(groups[test])],
            }
    result = {}
    for name, pred in (("ridge_original", baseline),
                       ("work_pairwise_ranking", ranked),
                       ("shuffled_training_labels", shuffled)):
        # evaluate_pairs computes R² too, but a logistic *rank score* has no
        # calibrated absolute magnitude, so omit R² for rankers.
        result[name] = {axis: {key: value for key, value in stats.items()
                               if key != "delta_r2"}
                        for axis, stats in evaluate_pairs(y, pred, groups).items()}
    comparisons = {}
    for name, pred in (("pairwise_minus_ridge", ranked),
                       ("shuffled_labels_minus_ridge", shuffled)):
        raw = cluster_bootstrap_improvement(
            y, baseline, pred, groups, repetitions=5_000)
        comparisons[name] = {axis: {
            "hard_accuracy_gain": vals["hard_accuracy_gain_vs_tempo"],
            "hard_gain_95pct_cluster_bootstrap": vals["hard_gain_95pct_cluster_bootstrap"],
        } for axis, vals in raw.items()}
    return {
        "dataset": "CP-WTC, 288 symbolic MIDI, 48 full compositions x 6 pianists",
        "protocol": "GroupKFold(6) outer compositions; GroupKFold(4) inner C selection; no audio",
        "features": list(FEATURES),
        "targets": "human valence/arousal deviations centered within each work",
        "human_difficult_pair_thresholds": {label: threshold for _, label, threshold in DIMENSIONS},
        "selected_hyperparameters": inner_audit,
        "models": result,
        "cluster_bootstrap_vs_ridge": comparisons,
        "limitations": [
            "Cannot distinguish musician identity/annotator group from expressivity",
            "Human listeners evaluated recordings; performance MIDI was transcribed by authors",
            "No new independent validation; same 48 compositions already used in prior exploration",
            "This ranks arousal and valence, not PIAST Dark/Mysterious/Epic",
            "Inner selection is performed by work, not by pair",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset_directory", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = benchmark(args.dataset_directory)
    for name, dimensions in report["models"].items():
        print(name, {label: (v["hard_direction_correct"], v["hard_direction_evaluable"],
                             round(v["hard_accuracy"], 4))
                     for label, v in dimensions.items()}, flush=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                               encoding="utf-8")


if __name__ == "__main__":
    main()
