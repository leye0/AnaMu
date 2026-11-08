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
from anamu.score_aligned_expression import (
    SCORE_FEATURE_NAMES, alignment_quality, score_aligned_features,
)
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


def nested_emotion_selector(y: np.ndarray, groups: np.ndarray,
                            works: np.ndarray, systems: dict,
                            outer_predictions: dict,
                            *, minimum_inner_gain: float = .02) -> dict:
    """Choose score-aware vs baseline arm separately for each target axis.

    For each unseen outer parent work, do inner leave-one-WORK-out validation
    only on the other three works. The held-out work's human labels are never
    available to the choice. Require >2pp relative gain to change arms.
    Compare with the same selector using within-score shuffled features.
    """
    results = {}
    for extra_arm in ("additional_features", "permuted_control"):
        selected = np.zeros_like(y)
        choices = {}
        for outer_work in np.unique(works):
            train = works != outer_work
            test = works == outer_work
            inner_metric = {}
            for arm in ("baseline_expressivity", extra_arm):
                inner_pred = contrastive_rank_oof(
                    systems[arm][train], y[train], groups[train],
                    cv_groups=works[train])
                inner_metric[arm] = evaluate(y[train], inner_pred, groups[train])
            choice_by_axis = {}
            for dim, axis in enumerate(TARGETS):
                base_score = inner_metric["baseline_expressivity"][axis]["hard_pair_accuracy"]
                extra_score = inner_metric[extra_arm][axis]["hard_pair_accuracy"]
                selected_arm = (extra_arm if extra_score - base_score >= minimum_inner_gain
                                else "baseline_expressivity")
                choice_by_axis[axis] = {"arm": selected_arm,
                                        "inner_baseline_accuracy": base_score,
                                        "inner_additional_accuracy": extra_score}
                selected[test, dim] = outer_predictions[selected_arm]["ranker"][test, dim]
            choices[int(outer_work)] = choice_by_axis
        metric = evaluate(y, selected, groups)
        for v in metric.values():
            del v["centered_delta_r2"]
        results[extra_arm] = {"evaluation": metric, "choices_by_work_id": choices}
    return results


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
    elif feature_pack == "score":
        feature_names, extractor = SCORE_FEATURE_NAMES, score_aligned_features
    else:
        raise ValueError(f"unsupported_feature_pack:{feature_pack}")
    stems = [e["stem"] for e in examples]
    extra = None
    diagnostics = []
    excluded_alignment = []
    if cache and cache.is_file():
        saved = json.loads(cache.read_text(encoding="utf-8"))
        if saved.get("stems") == stems and saved.get("features") == list(feature_names):
            extra = np.asarray(saved["values"], dtype=float)
            diagnostics = saved.get("diagnostics", [])
            excluded_alignment = saved.get("excluded_alignment", [])
    if extra is None:
        rows = []
        for index, stem in enumerate(stems):
            path = root / "virtuoso" / "data" / "all_2rounds" / (stem + ".mid")
            try:
                values = extractor(path)
            except ValueError as error:
                if feature_pack != "score" or str(error) != "unreliable_alignment_coverage":
                    raise
                # MIDI-only quality gate, fixed BEFORE labels/predictions.
                # Only two of 1,072 are affected in the observed corpus;
                # fill with same-score neutral values below, without a flag.
                excluded_alignment.append({"stem": stem, **alignment_quality(path)})
                rows.append([None] * len(feature_names))
                continue
            rows.append([values[name] for name in feature_names])
            if "alignment_diagnostics" in values:
                diagnostics.append(values["alignment_diagnostics"])
            if (index + 1) % 200 == 0:
                print(f"{feature_pack} extracted: {index + 1}/{len(stems)}", flush=True)
        extra = np.asarray(rows, dtype=float)
        if cache:
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_text(json.dumps({"stems": stems,
                                         "features": list(feature_names),
                                         "diagnostics": diagnostics,
                                         "excluded_alignment": excluded_alignment,
                                         "values": extra.tolist()}) + "\n",
                             encoding="utf-8")
    if extra.shape != (len(examples), len(feature_names)):
        raise ValueError("invalid_feature_cache_shape")
    missing = np.any(~np.isfinite(extra), axis=1)
    if np.any(missing):
        if feature_pack != "score" or np.sum(missing) != len(excluded_alignment):
            raise ValueError("unexpected_missing_features")
        for group in np.unique(score_groups):
            members = score_groups == group
            valid = members & ~missing
            if np.any(members & missing):
                # Impute from MIDI observations of other interpretations of
                # exactly the same score. Never use emotion labels or labels
                # from any held-out work for this imputation.
                replacement = extra[valid].mean(axis=0) if np.any(valid) else np.zeros(
                    len(feature_names))
                extra[members & missing] = replacement
    if not np.isfinite(extra).all():
        raise ValueError("nonfinite_extra_features_after_imputation")
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

    nested = nested_emotion_selector(y, score_groups, work_groups,
                                    systems, predictions)
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
        "alignment_audit": {
            "matched_coverage_min": float(min(d["match_fraction"] for d in diagnostics)),
            "matched_coverage_median": float(np.median([
                d["match_fraction"] for d in diagnostics])),
            "relative_time_error_median": float(np.median([
                d["median_relative_position_error"] for d in diagnostics])),
        } if diagnostics else None,
        "neutralized_low_quality_alignment": excluded_alignment,
        "inferred_pulse_not_score_meter": feature_pack == "pulse",
        "self_fitted_ioi_regularity_not_listener_surprise": feature_pack == "pulse",
        "taxonomies_not_equated": "PercePiano Dark/Dramatic/Imaginative != PIAST Dark/Epic/Mysterious",
        "models": results,
        "nested_emotion_aware_selection": {
            "rule": "inner 3-work LOOW per target, require >=2 percentage point hard-pair gain",
            "never_uses_outer_test_labels": True,
            "arms": nested,
        },
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
    parser.add_argument("--feature-pack", choices=("pulse", "accent", "score"),
                        default="pulse")
    args = parser.parse_args()
    report = benchmark(args.dataset_directory, args.cache, args.feature_pack)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n",
                               encoding="utf-8")


if __name__ == "__main__":
    main()
