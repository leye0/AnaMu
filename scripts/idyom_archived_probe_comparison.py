"""Audit third-party IDyOM probabilities against two *human* probe studies.

Precomputed probabilities are NOT a locally executed original IDyOM model;
the original training configuration and test-overlap remain unverified. All
model predictions are read or calculated before opening Schellenberg ratings.
Compare within-fragment ranks, never raw probability to 1–7 human ratings.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

from anamu.human_probe_expectancy import load_contexts
from anamu.idyom_archive import (archived_cuddy_cpitch, archived_schellenberg_probs,
                                 schellenberg_workbook_pitches)
from anamu.research_contracts import check_registered_experiment
from anamu.schellenberg_expectancy import (schellenberg_human_means,
                                           schellenberg_midi_stimuli)
from scripts.cudlun_probe_benchmark import PINNED_THESIS_COMMIT, UPSTREAM
from scripts.schellenberg_external_transfer import (_frozen_training,
                                                     _predict_without_target_labels)


ARCHIVES = {
    "idyom_cpitch_archived": "schellenberg_idyom_selected_probe_probs.csv",
    "idyom_optimal_viewpoint_archived_secondary":
        "schellenberg_optimal_viewpoint_idyom_selected_probe_probs.csv",
    "idyom_cpint_cpintfref_archived_secondary":
        "schellenberg_cpint_cpintfref_idyom_selected_probe_probs.csv",
}


def _mean_context_rank(prediction: list[np.ndarray],
                       actual: list[np.ndarray]) -> dict:
    if len(prediction) != len(actual) or not prediction:
        raise ValueError("nonmatching_human_archived_contexts")
    correlations = []
    for a, b in zip(actual, prediction):
        if a.shape != b.shape:
            raise ValueError("nonmatching_human_archived_pitches")
        coefficient = float(spearmanr(a, b).statistic)
        if not np.isfinite(coefficient):
            raise ValueError("undefined_archived_probe_rank")
        correlations.append(coefficient)
    return {"mean_spearman": round(float(np.mean(correlations)), 5),
            "by_context_spearman": [round(v, 5) for v in correlations]}


def _paired_difference(one: list[float], other: list[float]) -> dict:
    if len(one) != 8 or len(other) != 8:
        raise ValueError("expected_eight_contexts_for_bootstrap")
    difference = np.asarray(one) - np.asarray(other)
    rng = np.random.default_rng(31415)
    sampling = rng.choice(difference, size=(5000, 8), replace=True).mean(axis=1)
    return {
        "mean_rank_gain": round(float(difference.mean()), 5),
        "fragments_better": int(np.sum(difference > 0)),
        "paired_fragment_bootstrap_95pct_interval":
            [round(float(v), 5) for v in np.quantile(sampling, [.025, .975])],
    }


def run(source: Path) -> dict:
    check_registered_experiment("idyom_archived_schell_probe_comparison")
    sha = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"],
                                  text=True).strip()
    if sha != PINNED_THESIS_COMMIT:
        raise ValueError("unpinned_upstream_thesis_source")
    folder = source / UPSTREAM
    archive = folder / "probe_prediction_results"

    # Freeze every prediction before target test labels enter memory.
    cuddy = load_contexts(folder / "cudlun95.data",
                          folder / "cudlun_midi_stimuli_with_probe")
    template, learned_models = _frozen_training(cuddy)
    stimuli = schellenberg_midi_stimuli(folder / "schellenberg_midi_stimuli_with_probe")
    workbook_pitches = schellenberg_workbook_pitches(
        folder / "schellenberg_midi_notes_predicted.xlsx")
    for index, (stimulus, source_pitches) in enumerate(zip(stimuli, workbook_pitches)):
        if not np.array_equal(stimulus["candidates"], source_pitches):
            raise ValueError(f"sch_1996_candidate_pitch_misalignment_{index+1}")
    if len(stimuli) != 8 or len(workbook_pitches) != 8:
        raise ValueError("schell_stimulus_count_mismatch")

    proxies = _predict_without_target_labels(stimuli, template, learned_models)
    references = {name: archived_schellenberg_probs(archive / filename)
                  for name, filename in ARCHIVES.items()}
    cuddy_reference = archived_cuddy_cpitch(
        archive / "cudlun_idyom_probe_probs_midi54_78.csv")

    # Open published 1996 target values only after all predictions are frozen.
    ratings = schellenberg_human_means(folder / "schell96.data")
    scores = {name: _mean_context_rank(pieces, ratings)
              for name, pieces in {**proxies, **references}.items()}
    main = scores["idyom_cpitch_archived"]["by_context_spearman"]
    against_contour = scores["narmour_contour_proxy"]["by_context_spearman"]
    against_template = scores["pitch_template_only"]["by_context_spearman"]
    cuddy_ratings = [np.asarray([(a + b) / 2
                                 for a, b in zip(context["trained"], context["untrained"])])
                     for context in cuddy]
    return {
        "status": "exploratory_archived_predictions_only_not_locally_executed_idyom",
        "source_thesis": "https://github.com/yiannisem/MSc-Thesis---modelling-pitch-expectation",
        "source_commit": sha,
        "original_idyom_engine_executed": False,
        "external_pretraining_corpus_or_test_overlap_verified": False,
        "comparability": "descriptive only: Cuddy-source-trained last-two-note proxies vs externally pretrained full-context IDyOM probabilities; model inputs and training are not matched",
        "target": "quality_of_next_note_continuation_from_20_listener_group_means_not_emotion",
        "held_out_human_test": "Schellenberg_1996_eight_fragments_15_diatonic_candidates_each",
        "candidate_alignment": "120/120 workbook_pitches_equal_independently_reconstructed_midi_and_key_candidates",
        "archived_idyom_origin": "probabilities exported by 2025 thesis author using IDyOM and candidate extraction scripts; original .dat and training parameters not in inspected release",
        "variant_selection": "cpitch main reference chosen for comparability; optimal viewpoint and cpint+cpintfref reported as secondary, not selected as winner",
        "scores": scores,
        "precomputed_cpitch_vs_frozen_contour": _paired_difference(main, against_contour),
        "precomputed_cpitch_vs_frozen_pitch_template": _paired_difference(main, against_template),
        "cuddy_1995_archived_cpitch_descriptive": _mean_context_rank(
            cuddy_reference, cuddy_ratings),
        "limitations": "only 8 independent Schellenberg fragments and group mean ratings; no human per-listener data; previous human labels and archived outputs examined, so not a confirmatory test; no original audio timbre, emotion or mystery annotation",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = run(args.source.resolve())
    body = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(body, encoding="utf-8")
    print(body)


if __name__ == "__main__":
    main()
