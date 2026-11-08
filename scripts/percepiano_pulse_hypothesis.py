"""Falsifiable, score-free MIDI pulse hypothesis on difficult PercePiano axes.

Strictly hold out a complete parent work (four folds) when learning to rank
performances of the SAME scored excerpt. New rhythm features are compared to
an identical-capacity negative control permuted within each scored excerpt.

This is exploratory: 4 parent works are too few to establish a general law.
The additional beat/autocorrelation and local IOI regularity descriptors are
proxies, NOT recovered metrical accents or psychological surprise ratings.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from anamu.expressive_pulse import PULSE_FEATURE_NAMES, expressive_pulse_features
from anamu.expressive_accent import ACCENT_FEATURE_NAMES, expressive_accent_features
from .percepiano_hard_benchmark import (
    TARGETS, cluster_bootstrap_pair_difference, contrastive_rank_oof,
    evaluate, load_examples,
)


def work_regression(x: np.ndarray, y: np.ndarray,
                    works: np.ndarray) -> np.ndarray:
    """Fixed-capacity Ridge baseline; same coefficient penalty in all arms."""
    estimate = np.zeros_like(y)
    for train, test in LeaveOneGroupOut().split(x, y, works):
        model = make_pipeline(StandardScaler(), Ridge(alpha=20.0))
        model.fit(x[train], y[train])
        estimate[test] = model.predict(x[test])
    return estimate


def center_within_score(x: np.ndarray, groups: np.ndarray) -> np.ndarray:
    centered = x.copy()
    for group in np.unique(groups):
        sel = groups == group
        centered[sel] -= centered[sel].mean(axis=0)
    return centered


def shuffled_within_score(x: np.ndarray, groups: np.ndarray,
                          seed: int) -> np.ndarray:
    """Negative control: same score, distribution, and feature count.

    Preserves any score-specific patterns; destroys which *performance* had
    which extra feature. Base expressive features are not permuted.
    """
    rng = np.random.default_rng(seed)
    shuffled = x.copy()
    for group in np.unique(groups):
        sel = np.flatnonzero(groups == group)
        shuffled[sel] = x[rng.permutation(sel)]
    return shuffled


def benchmark(root: Path, cache: Path | None = None,
              feature_pack: str = "pulse") -> dict:
    base, y, score_groups, examples = load_examples(root)
    work_names = sorted({e["work"] for e in examples})
    if len(work_names) != 4:
        raise ValueError(f"unexpected_parent_works:{work_names}")
    work_groups = np.asarray([work_names.index(e["work"]) for e in examples])

    if feature_pack == "pulse":
        feature_names, extractor = PULSE_FEATURE_NAMES, expressive_pulse_features
    elif feature_pack == "accent":
        feature_names, extractor = ACCENT_FEATURE_NAMES, expressive_accent_features
    else:
        raise ValueError(f"unsupported_feature_pack:{feature_pack}")
    stems = [e["stem"] for e in examples]
    extra = None
    if cache and cache.is_file():
        saved = json.loads(cache.read_text(encoding="utf-8"))
        if saved.get("stems") == stems and saved.get("features") == list(feature_names):
            extra = np.asarray(saved["values"], dtype=float)
    if extra is None:
        rows = []
        for index, stem in enumerate(stems):
            path = root / "virtuoso" / "data" / "all_2rounds" / (stem + ".mid")
            values = extractor(path)
            rows.append([values[name] for name in feature_names])
            if (index + 1) % 200 == 0:
                print(f"{feature_pack} extracted: {index + 1}/{len(stems)}", flush=True)
        extra = np.asarray(rows, dtype=float)
        if cache:
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_text(json.dumps({"stems": stems,
                                         "features": list(feature_names),
                                         "values": extra.tolist()}) + "\n",
                             encoding="utf-8")
    if extra.shape != (len(examples), len(feature_names)):
        raise ValueError("invalid_feature_cache_shape")
    if not np.isfinite(extra).all():
        raise ValueError("nonfinite_extra_features")
    extra = center_within_score(extra, score_groups)

    systems = {"baseline_expressivity": base,
               "additional_features": np.column_stack((base, extra)),
               "permuted_control": np.column_stack((
                   base, shuffled_within_score(extra, score_groups, 20261108)))}
    results = {}
    predictions = {}
    for name, x in systems.items():
        ridge_pred = work_regression(x, y, work_groups)
        rank_pred = contrastive_rank_oof(x, y, score_groups, cv_groups=work_groups)
        ridge_eval = evaluate(y, ridge_pred, score_groups)
        rank_eval = evaluate(y, rank_pred, score_groups)
        for value in rank_eval.values():
            del value["centered_delta_r2"]
        results[name] = {"ridge": ridge_eval, "ranker": rank_eval}
        predictions[name] = {"ridge": ridge_pred, "ranker": rank_pred}
        results[name]["per_parent_work"] = {}
        for work_id, work in enumerate(work_names):
            mask = work_groups == work_id
            work_ridge = evaluate(y[mask], ridge_pred[mask], score_groups[mask])
            work_rank = evaluate(y[mask], rank_pred[mask], score_groups[mask])
            results[name]["per_parent_work"][work] = {
                "ridge": {axis: {"hard_correct": met["hard_pair_correct"],
                                 "hard_total": met["hard_pair_evaluable"]}
                          for axis, met in work_ridge.items()},
                "ranker": {axis: {"hard_correct": met["hard_pair_correct"],
                                  "hard_total": met["hard_pair_evaluable"]}
                           for axis, met in work_rank.items()},
            }
        print(name, {axis: round(rank_eval[axis]["hard_pair_accuracy"], 3)
                     for axis in ("dark", "imaginative", "dramatic_expressive")},
              flush=True)

    comparisons = {}
    for algorithm in ("ridge", "ranker"):
        base_pred = predictions["baseline_expressivity"][algorithm]
        comparisons[algorithm] = {
            "augmentation_minus_baseline": cluster_bootstrap_pair_difference(
                y, base_pred, predictions["additional_features"][algorithm], score_groups,
                repetitions=2_000),
            "shuffled_control_minus_baseline": cluster_bootstrap_pair_difference(
                y, base_pred, predictions["permuted_control"][algorithm], score_groups,
                repetitions=2_000),
        }
    return {
        "dataset": "PercePiano (human-performed MIDI, expert perceptions)",
        "examples": len(examples),
        "parent_works": work_names,
        "scored_excerpts": len(np.unique(score_groups)),
        "cv": "strict leave-one-parent-work-out (4 folds)",
        "feature_pack": feature_pack,
        "new_features": list(feature_names),
        "inferred_pulse_not_score_meter": feature_pack == "pulse",
        "self_fitted_ioi_regularity_not_listener_surprise": feature_pack == "pulse",
        "taxonomies_not_equated": "PercePiano Dark/Dramatic/Imaginative != PIAST Dark/Epic/Mysterious",
        "models": results,
        "comparisons": comparisons,
        "inference_limitations": [
            "Four independent parent compositions, all piano, high uncertainty",
            "Score-group bootstrap ignores correlation among movements of parent works",
            "All labeled tests exploratory; selection after inspecting prior benchmark",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset_directory", type=Path)
    parser.add_argument("--cache", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--feature-pack", choices=("pulse", "accent"), default="pulse")
    args = parser.parse_args()
    report = benchmark(args.dataset_directory, args.cache, args.feature_pack)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n",
                               encoding="utf-8")


if __name__ == "__main__":
    main()
