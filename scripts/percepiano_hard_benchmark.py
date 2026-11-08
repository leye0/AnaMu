"""MIDI-only expert-rated PercePiano challenge on DIFFICULT emotional axes.

Uses PercePiano's original 2024 19-dimensional expert listener ratings on
the human-performed MIDI files. Excludes mechanical 'Score' renditions.

Only differences between interpretations of the *same scored excerpt* count
for the relative ranking metrics. The labels 'dark', 'dramatic' and
'imaginative' are expert perceptual axes, NOT identical to PIAST's Dark, Epic
or Mysterious tags. Never merge them as if they were the same taxonomy.

CV holds out scored excerpt groups, but Beethoven variations and Schubert
movements share musical themes. It is not a truly independent composer split.
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from .cp_wtc_relative_benchmark import (
    FEATURES, MODELS, midi_expression, predict_out_of_fold,
)


# Verified against Table 2 and the paper's ordered 19 perceptual axes.
TARGETS = {
    "dramatic_expressive": 14,
    "dark": 15,
    "high_energy_diagnostic": 16,
    "imaginative": 17,
}
HARD_DIFFERENCE = 1.0 / 7.0  # 1 complete step on the original 7-point scale.


def scored_excerpt(stem: str) -> str:
    """Group performers of the same score, not whole unrelated variations."""
    fields = stem.split("_")
    if stem.startswith("Beethoven_WoO80_"):
        return "_".join(fields[:-2])  # one 8-bar variation per scored excerpt
    if stem.startswith("Schubert_D"):
        return "_".join(fields[:-2]) + "__bars_" + fields[-1]
    raise ValueError(f"unknown_score_group:{stem}")


def parent_work(stem: str) -> str:
    if stem.startswith("Beethoven_WoO80_"):
        return "Beethoven_WoO80"
    for token in ("Schubert_D960_mv2", "Schubert_D960_mv3", "Schubert_D935"):
        if stem.startswith(token):
            return token
    raise ValueError(f"unknown_parent_work:{stem}")


def load_examples(root: Path):
    path = root / "labels" / "label_2round_mean_reg_19_with0_rm_highstd0.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    examples = []
    missing_midis = []
    for stem, annotations in sorted(data.items()):
        if "Score" in stem:
            continue  # avoid easy artificial-versus-human proxy
        if len(annotations) != 20:
            raise ValueError("expected_19_ratings_plus_pianist_code")
        midi_path = root / "virtuoso" / "data" / "all_2rounds" / (stem + ".mid")
        if not midi_path.is_file():
            missing_midis.append(stem)
            continue
        expressions = midi_expression(midi_path)
        examples.append({"stem": stem, "score": scored_excerpt(stem),
                         "work": parent_work(stem), **expressions,
                         **{name: float(annotations[i]) for name, i in TARGETS.items()}})
    x = np.array([[example[feat] for feat in FEATURES] for example in examples], dtype=float)
    if missing_midis != ["Schubert_D935_no.3_4bars_2_1"]:
        raise ValueError(f"unexpected_missing_midis:{missing_midis}")
    y = np.array([[example[target] for target in TARGETS] for example in examples], dtype=float)
    # Integer group indices needed by GroupKFold and pairwise scoring.
    ids = {name: i for i, name in enumerate(sorted({e["score"] for e in examples}))}
    groups = np.array([ids[e["score"]] for e in examples], dtype=int)
    if not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ValueError("nonfinite_data")
    for group in np.unique(groups):
        selection = groups == group
        x[selection] -= x[selection].mean(axis=0)
        y[selection] -= y[selection].mean(axis=0)
    return x, y, groups, examples


def evaluate(y: np.ndarray, pred: np.ndarray, groups: np.ndarray) -> dict:
    outcomes = {}
    for col, label in enumerate(TARGETS):
        numerator = denominator = 0
        hard_correct = hard_total = 0
        for group in np.unique(groups):
            indices = np.flatnonzero(groups == group)
            for i, j in combinations(indices, 2):
                observed = y[i, col] - y[j, col]
                forecast = pred[i, col] - pred[j, col]
                if observed == 0 or forecast == 0:
                    continue
                denominator += 1
                numerator += (observed > 0) == (forecast > 0)
                if abs(observed) >= HARD_DIFFERENCE:
                    hard_total += 1
                    hard_correct += (observed > 0) == (forecast > 0)
        ss = float(np.sum(y[:, col] ** 2))
        residual = float(np.sum((y[:, col] - pred[:, col]) ** 2))
        outcomes[label] = {
            "centered_delta_r2": 1 - residual / ss if ss > 0 else None,
            "pair_correct": int(numerator), "pair_evaluable": int(denominator),
            "pair_accuracy": numerator / denominator if denominator else None,
            "hard_threshold_original_likert_steps": 1,
            "hard_pair_correct": int(hard_correct),
            "hard_pair_evaluable": int(hard_total),
            "hard_pair_accuracy": hard_correct / hard_total if hard_total else None,
        }
    return outcomes


def contrastive_rank_oof(x: np.ndarray, y: np.ndarray,
                         groups: np.ndarray) -> np.ndarray:
    """Learning-to-rank ablation: train on LARGE within-score disagreements.

    Inspired by rank-based affect research, not a reproduction of RnC loss.
    A pair x_a-x_b is supervised by which listener-rated performance was more
    dark/dramatic/imaginative. Every score group is withheld in its entirety.
    """
    estimated = np.zeros_like(y)
    for train, test in GroupKFold(n_splits=6).split(x, y, groups):
        train_groups = groups[train]
        for dim in range(y.shape[1]):
            pair_x = []
            pair_y = []
            for group in np.unique(train_groups):
                members = train[train_groups == group]
                for i, j in combinations(members, 2):
                    change = y[i, dim] - y[j, dim]
                    if abs(change) < HARD_DIFFERENCE:
                        continue
                    contrast = x[i] - x[j]
                    pair_x.extend((contrast, -contrast))
                    pair_y.extend((int(change > 0), int(change < 0)))
            if len(pair_x) < 20:
                raise ValueError("insufficient_hard_pairs_to_train_ranker")
            classifier = make_pipeline(StandardScaler(), LogisticRegression(C=0.5,
                                                                             max_iter=500))
            classifier.fit(np.asarray(pair_x), np.asarray(pair_y))
            # Linear decision values are meaningful as within-score rankings,
            # but NOT calibrated affect levels; no R² is computed for them.
            estimated[test, dim] = classifier.decision_function(x[test])
    return estimated


def cluster_bootstrap_pair_difference(y: np.ndarray, reference: np.ndarray,
                                      experimental: np.ndarray,
                                      groups: np.ndarray, *,
                                      repetitions: int = 5_000) -> dict:
    """Paired confidence intervals resampling scored-excerpt groups, not pairs.

    Individual pairs within one musical score are strongly correlated; naive
    binomial confidence bounds on thousands of pairs would be misleading.
    """
    rng = np.random.default_rng(20261108)
    group_ids = np.unique(groups)
    comparisons = {}
    for dim, label in enumerate(TARGETS):
        per_group = np.zeros((len(group_ids), 3), dtype=float)
        for index, group in enumerate(group_ids):
            indices = np.flatnonzero(groups == group)
            for i, j in combinations(indices, 2):
                observed = y[i, dim] - y[j, dim]
                if abs(observed) < HARD_DIFFERENCE:
                    continue
                ref = reference[i, dim] - reference[j, dim]
                exp = experimental[i, dim] - experimental[j, dim]
                per_group[index, 0] += 1
                per_group[index, 1] += (observed > 0) == (ref > 0)
                per_group[index, 2] += (observed > 0) == (exp > 0)
        point = float((per_group[:, 2].sum() - per_group[:, 1].sum()) /
                      per_group[:, 0].sum())
        draws = rng.integers(0, len(group_ids), size=(repetitions, len(group_ids)))
        sums = per_group[draws].sum(axis=1)
        diff = (sums[:, 2] - sums[:, 1]) / sums[:, 0]
        comparisons[label] = {
            "difference_rank_minus_ridge": point,
            "cluster_bootstrap_95pct_interval": [float(v) for v in np.quantile(diff, [.025, .975])],
            "resampling_unit": "scored-excerpt group, not pair; related variations are still dependent",
        }
    return comparisons


def benchmark(root: Path) -> dict:
    x, y, groups, examples = load_examples(root)
    results = {}
    full_pred = None
    dynamics_pred = None
    for name, features in MODELS.items():
        pred = predict_out_of_fold(x, y, groups, features)
        results[name] = {"features": list(features), "evaluation": evaluate(y, pred, groups)}
        if name == "expressivity_all":
            full_pred = pred
        elif name == "dynamics_only":
            dynamics_pred = pred
    rank_pred = contrastive_rank_oof(x, y, groups)
    rank_eval = evaluate(y, rank_pred, groups)
    for metric in rank_eval.values():
        del metric["centered_delta_r2"]  # ranking scores have arbitrary scale
    results["hard_pairwise_logistic"] = {
        "features": list(FEATURES),
        "loss": "symmetric logistic pairwise classification on >=1 Likert-step gaps",
        "calibrated_predictions": False,
        "evaluation": rank_eval,
    }
    confidence = cluster_bootstrap_pair_difference(y, full_pred, rank_pred, groups)
    confidence_against_dynamics = cluster_bootstrap_pair_difference(
        y, dynamics_pred, rank_pred, groups)
    return {
        "dataset": "PercePiano, Park et al. 2024, listener-annotated MIDI performances",
        "claim_scope": "perceptual axes Dark/Dramatic/Imaginative, NOT PIAST category equivalence",
        "no_audio": True,
        "excluded": "mechanical score renditions",
        "examples": len(examples),
        "scored_excerpt_groups": len(np.unique(groups)),
        "cross_validation": "GroupKFold(6) by scored excerpt; related variations share themes",
        "features": "score-free MIDI expressive approximation of performance features",
        "training_condition": "all 19 ratings originally gathered from human music experts",
        "threshold": "at least one full response category on 1..7 Likert scale (1/7 normalized)",
        "models": results,
        "rank_vs_regression_cluster_bootstrap": confidence,
        "rank_vs_dynamics_cluster_bootstrap": confidence_against_dynamics,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset_directory", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = benchmark(args.dataset_directory)
    print("Human recordings:", report["examples"], "score groups:", report["scored_excerpt_groups"])
    for name, result in report["models"].items():
        print(name)
        for label, metrics in result["evaluation"].items():
            print(" ", label, "R2", round(metrics["centered_delta_r2"], 3)
                  if "centered_delta_r2" in metrics else "not calibrated",
                  "hard", metrics["hard_pair_correct"], "/",
                  metrics["hard_pair_evaluable"], "=",
                  round(metrics["hard_pair_accuracy"], 3)
                  if metrics["hard_pair_accuracy"] is not None else None)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n",
                               encoding="utf-8")


if __name__ == "__main__":
    main()
