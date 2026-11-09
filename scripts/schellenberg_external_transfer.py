"""Frozen Cuddy(1995) -> Schellenberg(1996) human expectancy transfer.

Do not fit on or select features from Schellenberg responses. The architecture,
alpha=10, 25 relative pitch template and Krumhansl proxies are exactly those
introduced in the prior Cuddy benchmark. The human Schellenberg answers are
read *only after* the prediction arrays are built.

This is a genuinely distinct listening experiment but a retrospective,
exploratory transfer, because we inspected the archival labels when locating
the materials, and the model was post-hoc selected on Cuddy.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import numpy as np
from scipy.stats import pearsonr, spearmanr
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from anamu.human_probe_expectancy import load_contexts, theory_features, training_arrays
from anamu.research_contracts import check_registered_experiment
from anamu.schellenberg_expectancy import (schellenberg_human_means,
                                           schellenberg_midi_stimuli)
from scripts.cudlun_probe_benchmark import PINNED_THESIS_COMMIT, UPSTREAM


def _frozen_training(cuddy_contexts: list[dict]) -> tuple[np.ndarray, dict]:
    """Fit source-only proxies without accessing any target-context ratings."""
    inputs = training_arrays(cuddy_contexts)
    y = inputs["labels"]
    template = y.reshape(8, 25).mean(axis=0)
    models = {}
    for name, features in inputs["features"].items():
        direct = make_pipeline(StandardScaler(), Ridge(alpha=10.0))
        direct.fit(features, y)
        models[name] = direct
    contextual = inputs["features"]["contour_plus_tonal_hierarchy"]
    residual = make_pipeline(StandardScaler(), Ridge(alpha=10.0))
    residual.fit(contextual, y - np.tile(template, 8))
    models["tonal_context_residual"] = residual
    return template, models


def _predict_without_target_labels(stimuli: list[dict], template: np.ndarray,
                                   models: dict) -> dict[str, list[np.ndarray]]:
    result = {name: [] for name in ("pitch_template_only", *models)}
    for fragment in stimuli:
        first, second = fragment["last_two"]
        candidates = fragment["candidates"]
        indices = candidates - second + 12
        if not (np.all(indices >= 0) and np.all(indices <= 24)):
            raise ValueError("probe_exceeds_frozen_25_pitch_template")
        baseline = template[indices]
        result["pitch_template_only"].append(baseline)
        x = theory_features(first, second, candidates)
        for name, model in models.items():
            feature_name = ("contour_plus_tonal_hierarchy"
                            if name == "tonal_context_residual" else name)
            candidate = model.predict(x[feature_name])
            result[name].append(baseline + candidate if name == "tonal_context_residual"
                                else candidate)
    return result


def _assess(predictions: dict[str, list[np.ndarray]],
            targets: list[np.ndarray]) -> dict:
    y = np.concatenate(targets)
    output = {}
    for name, pieces in predictions.items():
        if len(pieces) != 8 or any(len(x) != 15 for x in pieces):
            raise ValueError("predictions_do_not_match_8_by_15_targets")
        overall = np.concatenate(pieces)
        by_piece = np.asarray([spearmanr(truth, predicted).statistic
                               for truth, predicted in zip(targets, pieces)])
        output[name] = {
            "mean_fragment_spearman": round(float(by_piece.mean()), 5),
            "per_fragment_spearman": [round(float(value), 5) for value in by_piece],
            "overall_pearson": round(float(pearsonr(y, overall).statistic), 5),
            "overall_r2": round(float(r2_score(y, overall)), 5),
        }
    ref = np.array(output["pitch_template_only"]["per_fragment_spearman"])
    comparisons = {}
    for name in predictions:
        if name == "pitch_template_only":
            continue
        diffs = np.array(output[name]["per_fragment_spearman"]) - ref
        rng = np.random.default_rng(31415)
        boot = rng.choice(diffs, size=(5000, 8), replace=True).mean(axis=1)
        comparisons[name] = {
            "mean_spearman_gain": round(float(diffs.mean()), 5),
            "fragments_improved": int(np.sum(diffs > 0)),
            "total_fragments": 8,
            "context_resampling_95pct_interval": [round(float(x), 5) for x in
                                                  np.quantile(boot, [.025, .975])],
        }
    return {"models": output, "comparisons_vs_source_fitted_template": comparisons}


def run(source: Path) -> dict:
    check_registered_experiment("schell_1996_external_transfer")
    sha = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"],
                                  text=True).strip()
    if sha != PINNED_THESIS_COMMIT:
        raise ValueError("unpinned_upstream_thesis_source")
    folder = source / UPSTREAM

    # Freeze the complete source-based estimator and compute out-of-study
    # predictions first; the target labels cannot inform these steps.
    cuddy = load_contexts(folder / "cudlun95.data",
                          folder / "cudlun_midi_stimuli_with_probe")
    template, models = _frozen_training(cuddy)
    stimuli = schellenberg_midi_stimuli(folder / "schellenberg_midi_stimuli_with_probe")
    predictions = _predict_without_target_labels(stimuli, template, models)

    # Only now open the external test answers.
    human_means = schellenberg_human_means(folder / "schell96.data")
    scores = _assess(predictions, human_means)
    return {
        "status": "external_study_exploratory_frozen_cuddy_architecture_no_schellenberg_training",
        "primary_external_paper": "https://doi.org/10.1016/0010-0277(95)00665-6",
        "source_training_paper": "https://doi.org/10.3758/BF03213071",
        "reconstructed_source": "https://github.com/yiannisem/MSc-Thesis---modelling-pitch-expectation",
        "source_commit": sha,
        "training": "cuddy_1995_8_two_note_contexts_25_probes_each_only",
        "external_target": "schellenberg_1996_20_other_listeners_8_long_folk_fragments_15_diatonic_probes_each_published_group_means",
        "target_votes_individual_available": False,
        "target_labels_used_for_fitting_or_selection": False,
        "frozen_context_window": "last_two_real_notes_of_each_long_fragment",
        "frozen_ridge_alpha": 10.0,
        "external_probe_order": "ascending_diatonic_pitches_reversing_thesis_original_descending_ratings",
        "stimuli": [{"id": x["id"], "key": x["key_signature"],
                     "context_note_count": x["context_note_count"],
                     "last_two": x["last_two"],
                     "candidates": x["candidates"].tolist()} for x in stimuli],
        "uncertainty_limit": "8 stimuli rated by the same 20 people; bootstrap samples stimuli not individual listeners; prior Cuddy model selected post-hoc",
        **scores,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path,
                        help="2025 thesis checkout at pinned commit")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = run(args.source.resolve())
    body = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(body, encoding="utf-8")
    print(body)


if __name__ == "__main__":
    main()
