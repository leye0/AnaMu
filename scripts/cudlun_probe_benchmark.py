"""Human-rated next-note plausibility, grouped by original two-note melody.

Run after checking out the independent 2025 thesis data, with no labels bundled:
    PYTHONPATH=. python scripts/cudlun_probe_benchmark.py --source ../melodic_expectancy_thesis

This is an exploratory proxy comparison, not the published original IDyOM,
Narmour/Schellenberg algorithm, a listener-level vote model, or an emotion
classifier. All hyperparameters and features are fixed in the source.
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

from anamu.human_probe_expectancy import load_contexts, training_arrays
from anamu.research_contracts import check_registered_experiment


UPSTREAM = Path("Code/MusicAnalysis/MusicModels/MT/MusicTransformer-Pytorch-private")
PINNED_THESIS_COMMIT = "e9eb23384393c83de97e1a69d00133ae4673c425"


def _predict_leave_one_context_out(
    content: dict, held_out_sets: list[tuple[int, ...]] | None = None,
) -> dict[str, np.ndarray]:
    y = content["labels"]
    groups = content["groups"]
    ids = sorted(set(groups))
    splits = held_out_sets or [(int(i),) for i in ids]
    if sorted(i for block in splits for i in block) != ids:
        raise ValueError("held_out_sets_must_partition_all_contexts_once")
    predictions = {name: np.full(len(y), np.nan) for name in
                   ("pitch_template_only", *content["features"],
                    "tonal_context_residual")}
    for held in splits:
        train = ~np.isin(groups, held)
        test = ~train
        train_count = len(ids) - len(held)
        # Explicit, trained-on-seven-contexts universal response to each
        # relative probe pitch. A hard baseline: familiar pitches can be
        # preferred without considering the first note at all.
        mean_template = y[train].reshape(train_count, 25).mean(axis=0)
        predictions["pitch_template_only"][test] = np.tile(mean_template, len(held))
        for name, x in content["features"].items():
            model = make_pipeline(StandardScaler(), Ridge(alpha=10.0))
            model.fit(x[train], y[train])
            predictions[name][test] = model.predict(x[test])
        # Separate general pitch salience from context-dependent effects:
        # learn only the residual left by the training-set pitch template.
        # This is a post-hoc hypothesis on already published data.
        contextual = content["features"]["contour_plus_tonal_hierarchy"]
        residual_model = make_pipeline(StandardScaler(), Ridge(alpha=10.0))
        residual_model.fit(contextual[train], y[train] - np.tile(mean_template, train_count))
        predictions["tonal_context_residual"][test] = (
            np.tile(mean_template, len(held)) + residual_model.predict(contextual[test]))
    return predictions


def _evaluate(contexts: list[dict]) -> dict:
    content = training_arrays(contexts)
    y = content["labels"]
    groups = content["groups"]
    ids = sorted(set(groups))
    predictions = _predict_leave_one_context_out(content)
    output = {}
    for name, predicted in predictions.items():
        if not np.isfinite(predicted).all():
            raise ValueError("missing_out_of_group_predictions")
        per_context = [float(spearmanr(y[groups == i], predicted[groups == i]).statistic)
                       for i in ids]
        output[name] = {
            "out_of_context_r2": round(float(r2_score(y, predicted)), 5),
            "out_of_context_pearson": round(float(pearsonr(y, predicted).statistic), 5),
            "mean_context_spearman": round(float(np.mean(per_context)), 5),
            "context_spearman": [round(value, 5) for value in per_context],
            "mean_trained_spearman": round(float(np.mean([
                spearmanr(content["trained"][groups == i], predicted[groups == i]).statistic
                for i in ids])), 5),
            "mean_untrained_spearman": round(float(np.mean([
                spearmanr(content["untrained"][groups == i], predicted[groups == i]).statistic
                for i in ids])), 5),
        }
    baseline = np.array(output["pitch_template_only"]["context_spearman"])
    comparison = {}
    for model_name in ("proximity", "narmour_contour_proxy",
                       "contour_plus_tonal_hierarchy", "tonal_context_residual"):
        candidate = np.array(output[model_name]["context_spearman"])
        differences = candidate - baseline
        boot = np.random.default_rng(37).choice(differences, size=(2000, len(ids)),
                                                replace=True).mean(axis=1)
        comparison[model_name] = {
            "mean_context_spearman_gain_vs_template": round(float(differences.mean()), 5),
            "group_bootstrap_95pct_CI": [round(float(value), 5)
                                         for value in np.quantile(boot, [.025, .975])],
            "contexts_improved": int(sum(differences > 0)),
            "contexts_total": len(ids),
        }
    robustness = {}
    for split_name, blocks in (
        ("leave_interval_size_out", [(0, 1), (2, 3), (4, 5), (6, 7)]),
        ("leave_direction_out", [(0, 2, 4, 6), (1, 3, 5, 7)]),
    ):
        group_predictions = _predict_leave_one_context_out(content, blocks)
        robustness[split_name] = {}
        for method_name in ("pitch_template_only", "tonal_context_residual"):
            predicted = group_predictions[method_name]
            robustness[split_name][method_name] = {
                "out_of_group_r2": round(float(r2_score(y, predicted)), 5),
                "mean_context_spearman": round(float(np.mean([
                    spearmanr(y[groups == i], predicted[groups == i]).statistic
                    for i in ids])), 5),
            }
    return {"models": output, "paired_context_comparison": comparison,
            "robustness_stricter_groupings": robustness}


def run(source: Path) -> dict:
    check_registered_experiment("cudlun_human_expectancy")
    upstream_commit = subprocess.check_output(
        ["git", "-C", str(source), "rev-parse", "HEAD"], text=True
    ).strip()
    if upstream_commit != PINNED_THESIS_COMMIT:
        raise ValueError(f"unpinned_thesis_checkout: {upstream_commit}")
    root = source / UPSTREAM
    contexts = load_contexts(root / "cudlun95.data", root / "cudlun_midi_stimuli_with_probe")
    result = _evaluate(contexts)
    return {
        "claim": "human_perceived_melodic_continuation_not_emotion",
        "status": "exploratory_original_paper_and_labels_previously_public",
        "source": {
            "primary_paper": "https://doi.org/10.3758/BF03213071",
            "secondary_digitized_tables_and_midi": "https://github.com/yiannisem/MSc-Thesis---modelling-pitch-expectation",
            "commit_sha": upstream_commit,
        },
        "human_target": "published_continuation_goodness_mean_by_12_trained_and_12_untrained_listeners",
        "raw_individual_votes_available": False,
        "original_two_note_contexts": 8,
        "probe_pitches_per_context": 25,
        "human_group_means": 400,
        "independent_splits": "leave_one_two_note_context_out_8_folds",
        "input": "reconstructed_transposition_normalized_context_midi_pitches_only_no_probe_or_rating_features",
        "transposition_caveat": "original experiment alternated C4/F#4 anchors; thesis MIDI fixes F#4, features and probes analyzed relative to second pitch",
        "contexts": [{"id": b["id"], "name": b["name"], "notes": [b["first"], b["second"]]}
                     for b in contexts],
        **result,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True,
                        help="Checked-out, pinned GitHub thesis repository")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.source.resolve())
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
