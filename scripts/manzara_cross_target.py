"""Exploratory Cuddy -> Manzara human *note-surprisal*, not probe ratings.

All Cuddy parameters and a fixed 25-state softmax mapping are frozen BEFORE
the Manzara human target is opened. This is a deliberately difficult transfer
between different tasks. Only two chorales exist; correlations on 82 notes
are descriptive, not evidence of 82 independent samples or emotion prediction.

PYTHONPATH=. python -m scripts.manzara_cross_target \
  --source ../melodic_expectancy_thesis
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

from anamu.human_probe_expectancy import load_contexts, theory_features
from anamu.manzara_expectancy import (CHORALE_LENGTHS, human_note_bits,
                                     reconstructed_chorale_notes,
                                     softmax_information_bits)
from anamu.research_contracts import check_registered_experiment
from scripts.cudlun_probe_benchmark import PINNED_THESIS_COMMIT, UPSTREAM
from scripts.schellenberg_external_transfer import _frozen_training


def frozen_cuddy_surprisals(notes: dict[int, np.ndarray],
                           template: np.ndarray, models: dict) -> dict:
    """Forecast each *realized* next note using only its two-note prefix."""
    results = {}
    for chorale, pitches in notes.items():
        predictions = {name: [] for name in ("pitch_template_only", *models)}
        for i in range(2, len(pitches)):
            first, second = (int(pitches[i - 2]), int(pitches[i - 1]))
            actual = int(pitches[i])
            choices = np.arange(second - 12, second + 13, dtype=int)
            answer_index = actual - second + 12
            if not 0 <= answer_index < 25:
                raise ValueError("actual_note_outside_frozen_cuddy_support")
            base = np.asarray(template, dtype=float)
            feature_vectors = theory_features(first, second, choices)
            scores = {"pitch_template_only": base}
            for name, predictor in models.items():
                feature_name = ("contour_plus_tonal_hierarchy"
                                if name == "tonal_context_residual" else name)
                predicted = predictor.predict(feature_vectors[feature_name])
                scores[name] = base + predicted if name == "tonal_context_residual" else predicted
            for name, rating_scores in scores.items():
                predictions[name].append(softmax_information_bits(rating_scores, answer_index))
        results[chorale] = {name: np.asarray(series, dtype=float)
                            for name, series in predictions.items()}
    return results


def _import_2025_idyom_reference(path: Path, notes: dict[int, np.ndarray]) -> dict:
    """Independent precomputed thesis output: original IDyOM *not* run by us.

    The source author's training contamination and model selection have not
    been independently audited. This is a descriptive comparator, not a fair
    claim of head-to-head generalization or original-engine reproduction.
    """
    by_chorale = {id_: [] for id_ in CHORALE_LENGTHS}
    with path.open(newline="", encoding="utf-8") as stream:
        rows = csv.DictReader(stream)
        needed = {"filename", "note_index", "actual_pitch", "idyom_probability", "idyom_ic"}
        if not needed.issubset(rows.fieldnames or []):
            raise ValueError("incomplete_upstream_idyom_probabilities")
        for row in rows:
            filename = row["filename"]
            if not filename.startswith("chorale") or not filename.endswith(".mid"):
                raise ValueError("unexpected_upstream_chorale_filename")
            chorale = int(filename.removeprefix("chorale").removesuffix(".mid"))
            if chorale not in by_chorale:
                raise ValueError("unexpected_upstream_chorale")
            i = len(by_chorale[chorale])
            if int(row["note_index"]) != i or int(row["actual_pitch"]) != notes[chorale][i]:
                raise ValueError("upstream_idyom_pitch_or_note_index_mismatch")
            probability = float(row["idyom_probability"])
            bits = float(row["idyom_ic"])
            if not (0 < probability <= 1 and np.isfinite(bits) and
                    abs(bits + np.log2(probability)) < 1e-3):
                raise ValueError("inconsistent_upstream_idyom_probability_or_bits")
            by_chorale[chorale].append(bits)
    if any(len(by_chorale[id_]) != n for id_, n in CHORALE_LENGTHS.items()):
        raise ValueError("upstream_idyom_does_not_align_to_86_notes")
    return {id_: np.asarray(values[2:], dtype=float)
            for id_, values in by_chorale.items()}


def _statistics(predictions: dict[int, dict], targets: dict[int, np.ndarray]) -> dict:
    model_names = list(next(iter(predictions.values())))
    if any(list(predictions[id_]) != model_names for id_ in CHORALE_LENGTHS):
        raise ValueError("inconsistent_models_across_chorales")
    result = {}
    for model in model_names:
        by_chorale = {}
        for chorale in CHORALE_LENGTHS:
            y = targets[chorale][2:, 1]  # `average` human information bits.
            estimated = predictions[chorale][model]
            if len(y) != len(estimated) or not np.isfinite(estimated).all():
                raise ValueError("misaligned_human_bits_and_predictions")
            statistic = float(spearmanr(y, estimated).statistic)
            cyclic = [float(spearmanr(y, np.roll(estimated, shift)).statistic)
                      for shift in range(1, len(estimated))]
            by_chorale[str(chorale)] = {
                "notes_after_two_context_notes": len(y),
                "spearman_human_vs_predicted_bits": round(statistic, 5),
                "human_mean_bits": round(float(y.mean()), 5),
                "predicted_mean_bits": round(float(estimated.mean()), 5),
                "circular_shift_control_median_spearman": round(float(np.median(cyclic)), 5),
                "aligned_rho_exceeds_shift_median": bool(statistic > np.median(cyclic)),
            }
        concatenated_human = np.concatenate([targets[id_][2:, 1] for id_ in CHORALE_LENGTHS])
        concatenated_model = np.concatenate([predictions[id_][model] for id_ in CHORALE_LENGTHS])
        result[model] = {
            "per_chorale": by_chorale,
            "pooled_note_spearman_descriptive_only": round(float(spearmanr(
                concatenated_human, concatenated_model).statistic), 5),
            "mean_of_two_chorale_rhos_descriptive_only": round(float(np.mean([
                by_chorale[str(id_)]["spearman_human_vs_predicted_bits"]
                for id_ in CHORALE_LENGTHS])), 5),
        }
    return result


def run(source: Path) -> dict:
    check_registered_experiment("manzara_1992_cross_target")
    sha = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"],
                                  text=True).strip()
    if sha != PINNED_THESIS_COMMIT:
        raise ValueError("unpinned_upstream_thesis_source")
    root = source / UPSTREAM
    training = load_contexts(root / "cudlun95.data", root / "cudlun_midi_stimuli_with_probe")
    template, models = _frozen_training(training)
    notes = reconstructed_chorale_notes(root / "manz_midi_stimuli")

    # Freeze predicted bits before ANY human Manzara rows are read.
    predictions = frozen_cuddy_surprisals(notes, template, models)
    idyom_import = _import_2025_idyom_reference(
        root / "probe_prediction_results/manz_cpitch_idyom_actual_note_probs.csv", notes)
    for chorale in CHORALE_LENGTHS:
        predictions[chorale]["third_party_idyom_cpitch_import_not_executed"] = idyom_import[chorale]

    # The human data are intentionally opened last; no parameters get tuned.
    human = human_note_bits(root / "manzetal92.data")
    scores = _statistics(predictions, human)
    return {
        "status": "exploratory_heterogeneous_outcome_only_two_chorales_no_confirmatory_claim",
        "primary_study": "https://researchcommons.waikato.ac.nz/items/97793e93-66e4-4354-8159-9b1dbadda2f0",
        "digitized_reference": "https://github.com/yiannisem/MSc-Thesis---modelling-pitch-expectation",
        "source_commit": sha,
        "model_training": "Cuddy_1995_only_8_contexts_25_group_mean_probes_each",
        "target": "Manzara_1992_human_gambling_realized_next_note_average_information_bits",
        "target_used_in_training_or_selection": False,
        "source_data_previously_inspected": True,
        "target_human_votes_individually_available": False,
        "context_notes_used": 2,
        "first_two_target_notes_excluded_per_chorale": True,
        "effective_notes": 82,
        "parent_chorales": 2,
        "human_target_not_equivalent_to_Cuddy_probe_ratings": True,
        "score_to_probability": "softmax_all_25_chromatic_candidates_fixed_temperature_1_rating_unit_not_human_calibrated",
        "third_party_idyom_import": "precomputed_2025_cpitch_csv_pitch_aligned_not_original_engine_executed_by_AnaMu_training_exclusion_unverified",
        "uncertainty_limit": "Two parent melodies only; per-note observations autocorrelated; no participant-level bets; no inferential bootstrap or p-values; circular shifts are descriptive alignment diagnostics.",
        "models": scores,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = run(args.source.resolve())
    body = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(body, encoding="utf-8")
    print(body)


if __name__ == "__main__":
    main()
