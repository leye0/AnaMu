"""Exploratory human-expert cadence retrieval from note-level symbolic inputs.

Sample invocation (data clones are *outside* the AnaMu repo):
  PYTHONPATH=. python scripts/dcml_cadence_benchmark.py \
    --corpus chopin=../chopin_mazurkas \
    --corpus mozart=../mozart_piano_sonatas \
    --corpus bach=../bach_en_fr_suites

No DLC harmony analysis (chords, keys, phrase markers) is used as input.
An expert cadence is a musicological event, not a human-rated emotion.
The observed data have been inspected; results are EXPLORATORY.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from anamu.cadence_events import load_corpora
from anamu.research_contracts import check_registered_experiment


def _model():
    return make_pipeline(StandardScaler(), LogisticRegression(
        max_iter=600, solver="liblinear", class_weight="balanced", random_state=19))


def _metrics(labels: np.ndarray, scores: np.ndarray, groups: np.ndarray) -> dict:
    precision_top5 = []
    recall_top5 = []
    per_parent_work_ap = []
    for group in sorted(set(groups)):
        positions = np.flatnonzero(groups == group)
        top = positions[np.argsort(-scores[positions], kind="stable")[:5]]
        total = int(labels[positions].sum())
        precision_top5.append(float(labels[top].sum()) / len(top))
        if total:
            recall_top5.append(float(labels[top].sum()) / total)
            per_parent_work_ap.append(float(average_precision_score(labels[positions], scores[positions])))
    return {
        "average_precision": round(float(average_precision_score(labels, scores)), 5),
        "roc_auc": round(float(roc_auc_score(labels, scores)), 5),
        "mean_parent_work_precision_at_5": round(float(np.mean(precision_top5)), 5),
        "mean_parent_work_recall_at_5": round(float(np.mean(recall_top5)), 5),
        "mean_parent_work_average_precision": round(float(np.mean(per_parent_work_ap)), 5),
    }


def _evaluate(x: np.ndarray, labels: np.ndarray, groups: np.ndarray,
              composer: np.ndarray, *, cross_composer: bool = False) -> tuple[dict, np.ndarray]:
    scores = np.full(len(labels), np.nan)
    if cross_composer:
        splits = [((composer != held).nonzero()[0], (composer == held).nonzero()[0])
                  for held in sorted(set(composer))]
    else:
        cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=19)
        splits = list(cv.split(x, labels, groups))
    for train, test in splits:
        if len(set(labels[train])) < 2 or len(set(labels[test])) < 2:
            raise ValueError("split_lacks_positive_and_negative_events")
        estimator = _model()
        estimator.fit(x[train], labels[train])
        scores[test] = estimator.predict_proba(x[test])[:, 1]
    if not np.isfinite(scores).all():
        raise ValueError("incomplete_group_disjoint_predictions")
    metrics = _metrics(labels, scores, groups)
    metrics["by_composer"] = {
        name: _metrics(labels[composer == name], scores[composer == name], groups[composer == name])
        for name in sorted(set(composer))
    }
    return metrics, scores


def _piece_paired_gain(labels: np.ndarray, baseline: np.ndarray,
                       candidate: np.ndarray, groups: np.ndarray) -> dict:
    """Parent-work-cluster bootstrap, using matched predictions and labels."""
    deltas = []
    for group in sorted(set(groups)):
        mask = groups == group
        if not labels[mask].any() or labels[mask].all():
            continue
        deltas.append(float(average_precision_score(labels[mask], candidate[mask]) -
                            average_precision_score(labels[mask], baseline[mask])))
    if not deltas:
        raise ValueError("no_pieces_with_positive_and_negative_cadence_events")
    values = np.asarray(deltas)
    rng = np.random.default_rng(73)
    draws = rng.choice(values, size=(2000, len(values)), replace=True).mean(axis=1)
    return {
        "mean_parent_work_AP_absolute_gain": round(float(values.mean()), 5),
        "paired_parent_work_bootstrap_95pct_CI": [round(float(x), 5) for x in np.quantile(draws, [.025, .975])],
        "parent_works_improved": int((values > 0).sum()),
        "parent_works_compared": len(values),
        "bootstrap_unit": "parent_work_not_movement_or_onset",
    }


def run(roots: dict[str, Path]) -> dict:
    check_registered_experiment("dcml_cadence_exploratory")
    loaded = load_corpora(roots)
    pieces = loaded["pieces"]
    if len(pieces) < 10:
        raise ValueError("at_least_ten_annotated_pieces_required")
    rhythm = np.vstack([np.asarray(p["rhythm"], dtype=float) for p in pieces])
    harmonic = np.vstack([np.asarray(p["harmony"], dtype=float) for p in pieces])
    labels = np.concatenate([np.asarray(p["labels"], dtype=int) for p in pieces])
    groups = np.concatenate([np.repeat(p["parent_work"], p["n_onsets"]) for p in pieces])
    piece_ids = np.concatenate([np.repeat(p["piece"], p["n_onsets"]) for p in pieces])
    composer = np.concatenate([np.repeat(p["composer"], p["n_onsets"]) for p in pieces])
    if len(set(composer)) < 3:
        raise ValueError("three_composers_required_for_domain_shift_test")
    rng = np.random.default_rng(19)
    shuffled = harmonic.copy()
    # Break the alignment between musical harmonic events and gold cadences,
    # preserving each piece's distributions and all rhythmic features.
    for piece in sorted(set(piece_ids)):
        idx = np.flatnonzero(piece_ids == piece)
        shuffled[idx] = harmonic[rng.permutation(idx)]
    features = {
        "rhythm_only": rhythm,
        "harmony_only": harmonic,
        "rhythm_plus_harmony": np.column_stack((rhythm, harmonic)),
        "rhythm_plus_shuffled_harmony": np.column_stack((rhythm, shuffled)),
    }
    result = {
        "claim": "expert_musicological_cadence_event_retrieval_not_emotion_prediction",
        "status": "exploratory_previous_labels_inspected",
        "sources": {name: {"url": f"https://github.com/DCMLab/{root.name}",
                             "git_sha": subprocess.check_output(
                                 ["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()}
                    for name, root in roots.items()},
        "pieces": len(pieces), "independent_parent_works": len(set(groups)),
        "onset_candidates": int(len(labels)),
        "expert_cadences": int(sum(p["n_annotated_cadences"] for p in pieces)),
        "matched_cadences": int(labels.sum()),
        "positive_prevalence": round(float(labels.mean()), 5),
        "skipped": loaded["skipped"],
        "evaluation": "5_fold_parent_work_disjoint_and_leave_one_composer_out",
        "features": "notes_tsv_midi_pitches_durations_onsets_only; no annotated chords/keys/phrases",
        "models": {},
    }
    out_of_fold = {}
    out_of_composer = {}
    for key, x in features.items():
        cv_metrics, cv_predictions = _evaluate(x, labels, groups, composer)
        composer_metrics, composer_predictions = _evaluate(
            x, labels, groups, composer, cross_composer=True)
        result["models"][key] = {
            "composition_disjoint": cv_metrics,
            "leave_one_composer_out": composer_metrics,
        }
        out_of_fold[key] = cv_predictions
        out_of_composer[key] = composer_predictions
    result["paired_harmonic_gain"] = {
        "composition_disjoint": _piece_paired_gain(
            labels, out_of_fold["rhythm_only"], out_of_fold["rhythm_plus_harmony"], groups),
        "leave_one_composer_out": _piece_paired_gain(
            labels, out_of_composer["rhythm_only"], out_of_composer["rhythm_plus_harmony"], groups),
    }
    # Harder diagnostic: both positive and negative candidates are bar starts.
    # Models are trained without human cadence/phrase labels on all onsets;
    # only evaluation is conditioned on *unannotated* meter position.
    bar_starts = rhythm[:, 6] == 1.0
    if labels[bar_starts].sum() > 10:
        result["barline_onset_diagnostic"] = {
            "n_candidates": int(bar_starts.sum()),
            "n_cadences": int(labels[bar_starts].sum()),
            "prevalence": round(float(labels[bar_starts].mean()), 5),
            "composition_disjoint": {
                key: _metrics(labels[bar_starts], predictions[bar_starts], groups[bar_starts])
                for key, predictions in out_of_fold.items()
            },
            "leave_one_composer_out": {
                key: _metrics(labels[bar_starts], predictions[bar_starts], groups[bar_starts])
                for key, predictions in out_of_composer.items()
            },
        }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", action="append", required=True,
                        help="composer=/absolute/path/to/checked-out/DCMLab/repo")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    roots = {}
    for spec in args.corpus:
        if "=" not in spec:
            parser.error("--corpus expects name=path")
        name, value = spec.split("=", 1)
        if not name or name in roots or not Path(value).is_dir():
            parser.error(f"invalid or duplicate corpus: {name}")
        roots[name] = Path(value).resolve()
    result = run(roots)
    serialized = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(serialized, encoding="utf-8")
    print(serialized)


if __name__ == "__main__":
    main()
