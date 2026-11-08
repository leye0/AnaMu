"""Post-hoc source-video-disjoint tonal ablation on all known PIAST MIDI.

This is EXPLORATORY: all 1900 titles/labels have been examined before.
The fixed model and feature partitions are *not* a new holdout experiment.
No audio, no mood labels in any feature, and no model tuning on CV outcomes.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from anamu.tonal_motion import (
    TONAL_DISTRIBUTION_FEATURE_NAMES,
    TONAL_MOTION_FEATURE_NAMES,
    TONAL_SEQUENCE_FEATURE_NAMES,
    midi_tonal_motion,
)
from .piast_at_benchmark import make_matrix, run
from .piast_tension_experiment import HARD_MOODS, NONCALM_MOODS


SEED = 20261108
FOLDS = 5
ARMS = (
    "baseline",
    "distribution",
    "temporal",
    "permuted_temporal",
)


def source_group_folds(records: list[tuple], n_splits: int = FOLDS):
    """Yield indices with *entire original videos* isolated per test fold."""
    groups = np.asarray([clip.song_group for clip, _ in records])
    splitter = GroupKFold(n_splits=n_splits)
    for train_indices, test_indices in splitter.split(np.zeros(len(records)), groups=groups):
        if set(groups[train_indices]) & set(groups[test_indices]):
            raise AssertionError("source_video_leakage")
        yield train_indices, test_indices


def _predict(train_x: np.ndarray, test_x: np.ndarray,
             y_train: np.ndarray) -> np.ndarray:
    if len(set(y_train)) < 2:
        return np.full(len(test_x), float(np.mean(y_train)))
    model = Pipeline([
        ("missing", SimpleImputer(strategy="median", keep_empty_features=True,
                                   add_indicator=True)),
        ("scale", StandardScaler()),
        ("classifier", LogisticRegression(C=.5, class_weight="balanced",
                                           max_iter=1200, random_state=SEED)),
    ])
    model.fit(train_x, y_train)
    return model.predict_proba(test_x)[:, 1]


def _ap(y: np.ndarray, prediction: np.ndarray) -> float | None:
    return float(average_precision_score(y, prediction)) if 3 <= y.sum() < len(y) else None


def evaluate_arms(records: dict[str, list[tuple]], *, folds: int = FOLDS,
                  negative_label_control: bool = True,
                  arms: tuple[str, ...] = ARMS,
                  negative_control_arm: str | None = None) -> tuple[dict, dict]:
    """Fixed models evaluated out of fold, never tuned to folds or test tags."""
    if not arms or arms[0] != "baseline" or len(set(arms)) != len(arms) or set(records) != set(arms):
        raise ValueError("missing_arms")
    if negative_control_arm is None:
        negative_control_arm = "temporal" if "temporal" in arms else arms[-1]
    if negative_control_arm not in arms:
        raise ValueError("missing_negative_control_arm")
    reference = records["baseline"]
    identities = [(c.clip_id, c.song_group) for c, _ in reference]
    for arm, rows in records.items():
        if [(c.clip_id, c.song_group) for c, _ in rows] != identities:
            raise AssertionError(f"unequal_examples:{arm}")
    n = len(reference)
    labels = {m: np.asarray([int(m in clip.mood_tags()) for clip, _ in reference])
              for m in NONCALM_MOODS}
    features = {arm: sorted({key for _, row in rows for key in row})
                for arm, rows in records.items()}
    matrices = {arm: make_matrix(records[arm], features[arm]) for arm in arms}
    predictions = {arm: {label: np.full(n, np.nan) for label in NONCALM_MOODS}
                   for arm in arms}
    scrambled_dark = np.full(n, np.nan)
    fold_details = []
    for k, (train, test) in enumerate(source_group_folds(reference, n_splits=folds)):
        result = {
            "fold": k + 1,
            "train": len(train), "test": len(test),
            "train_groups": len({reference[i][0].song_group for i in train}),
            "test_groups": len({reference[i][0].song_group for i in test}),
            "positives": {m: int(labels[m][test].sum()) for m in NONCALM_MOODS},
            "ap": {},
        }
        for arm in arms:
            result["ap"][arm] = {}
            x_train, x_test = matrices[arm][train], matrices[arm][test]
            for mood in NONCALM_MOODS:
                p = _predict(x_train, x_test, labels[mood][train])
                predictions[arm][mood][test] = p
                result["ap"][arm][mood] = _ap(labels[mood][test], p)
        if negative_label_control:
            # This control *scrambles training tags only*: held-out true tags
            # are left untouched. Not a feature permutation or an easy class.
            rng = np.random.default_rng(SEED + k)
            y_scrambled = rng.permutation(labels["Dark"][train])
            scrambled_dark[test] = _predict(matrices[negative_control_arm][train],
                                            matrices[negative_control_arm][test], y_scrambled)
        fold_details.append(result)
        print(f"CV fold {k+1}/{folds}: {len(test)} test clips, "
              f"{result['test_groups']} independent video groups", flush=True)
    if any(np.isnan(predictions[arm][mood]).any()
           for arm in arms for mood in NONCALM_MOODS):
        raise AssertionError("incomplete_oof_predictions")
    pooled = {}
    for arm in arms:
        ap = {m: _ap(labels[m], predictions[arm][m]) for m in NONCALM_MOODS}
        if any(x is None for x in ap.values()):
            raise AssertionError("mood_has_no_positives")
        pooled[arm] = {
            "by_mood": ap,
            "hard5_macro_ap": float(np.mean([ap[m] for m in HARD_MOODS])),
            "noncalm14_macro_ap": float(np.mean(list(ap.values()))),
            "features": len(features[arm]),
        }
    negative = {"train_label_permutation_dark_ap": _ap(labels["Dark"], scrambled_dark)} \
        if negative_label_control else {}
    diagnostics = {
        "mood_positives": {m: int(np.sum(v)) for m, v in labels.items()},
        "folds": fold_details,
        "negative_control": negative,
    }
    # Reuse OOF scores in the separate group bootstrap without refitting.
    return {"scores": pooled, "diagnostics": diagnostics}, {
        "labels": labels, "predictions": predictions,
        "groups": np.asarray([clip.song_group for clip, _ in reference]),
    }


def group_bootstrap(oof: dict, *, repetitions: int = 700,
                    baseline_arm: str = "baseline",
                    arms: tuple[str, ...] = ARMS) -> dict:
    """Approximate paired OOF AP uncertainty; resample *videos*, not clips.

    The interval conditions on already fitted OOF models; it does not account
    for selection of hypotheses after previous 1900-item examinations.
    """
    groups = oof["groups"]
    unique_groups, group_indexes = np.unique(groups, return_inverse=True)
    by_group = [np.flatnonzero(group_indexes == i) for i in range(len(unique_groups))]
    rng = np.random.default_rng(SEED + 19)
    y = oof["labels"]
    p = oof["predictions"]
    out = {}
    if baseline_arm not in arms or any(arm not in p for arm in arms):
        raise ValueError("unknown_bootstrap_arm")
    for candidate in arms:
        if candidate == baseline_arm:
            continue
        draws = {"Dark": [], "hard5_macro": [], "noncalm14_macro": []}
        for _ in range(repetitions):
            sample_groups = rng.integers(0, len(unique_groups), size=len(unique_groups))
            idx = np.concatenate([by_group[int(g)] for g in sample_groups])
            contrasts = {}
            for mood in NONCALM_MOODS:
                a, b = _ap(y[mood][idx], p[candidate][mood][idx]), \
                       _ap(y[mood][idx], p[baseline_arm][mood][idx])
                if a is not None and b is not None:
                    contrasts[mood] = a - b
            if "Dark" in contrasts:
                draws["Dark"].append(contrasts["Dark"])
            for metric, target in (("hard5_macro", HARD_MOODS),
                                   ("noncalm14_macro", NONCALM_MOODS)):
                if all(m in contrasts for m in target):
                    draws[metric].append(float(np.mean([contrasts[m] for m in target])))
        out[candidate] = {
            metric: {
                "valid_draws": len(values),
                "ci_95_low": float(np.quantile(values, .025)) if values else None,
                "ci_95_high": float(np.quantile(values, .975)) if values else None,
                "fraction_positive": float(np.mean(np.asarray(values) > 0)) if values else None,
            } for metric, values in draws.items()
        }
    return out


def experiment(root: Path, out: Path, *, limit: int = 1900,
               bootstrap_repetitions: int = 700) -> dict:
    if limit != 1900:
        raise ValueError("requires_exact_previously_seen_1900")
    out.mkdir(parents=True, exist_ok=True)
    extraction = run(root, feature_set="research_tonal_motion", limit=limit,
                     cache_dir=out / "cache", extract_only=True)
    original = extraction["records"]
    if extraction["matched"] != limit or len(original) != limit or extraction["rejected"]:
        raise AssertionError("incomplete_piast_cohort")
    distribution = frozenset(TONAL_DISTRIBUTION_FEATURE_NAMES)
    sequence = frozenset(TONAL_SEQUENCE_FEATURE_NAMES)
    tonal = frozenset(TONAL_MOTION_FEATURE_NAMES)
    if (distribution & sequence or distribution | sequence != tonal):
        raise AssertionError("invalid_tonal_feature_partition")
    rows = {arm: [] for arm in ARMS}
    for i, (clip, all_features) in enumerate(original, 1):
        base = {k: v for k, v in all_features.items() if k not in tonal}
        static = {k: all_features[k] for k in distribution}
        dynamic = {k: all_features[k] for k in sequence}
        shuffled = midi_tonal_motion(root / "midi" / clip.midi_name,
                                     shuffle=True, seed=SEED)
        if not all(abs(static[k] - shuffled[k]) < 1e-9 for k in distribution):
            raise AssertionError(f"permutation_altered_distribution:{clip.clip_id}")
        rows["baseline"].append((clip, base))
        rows["distribution"].append((clip, {**base, **static}))
        rows["temporal"].append((clip, {**base, **static, **dynamic}))
        rows["permuted_temporal"].append((clip, {**base, **static,
                                                **{k: shuffled[k] for k in sequence}}))
        if i % 200 == 0:
            print(f"Permutation control {i}/{limit}", flush=True)
    evaluated, oof = evaluate_arms(rows)
    uncertainty = group_bootstrap(oof, repetitions=bootstrap_repetitions)
    summary = {
        "title": "PIAST MIDI key trajectories: distribution versus temporal path",
        "research_status": "post-hoc exploration only; all 1900 labelled MIDI previously examined",
        "independent_new_holdout": False,
        "dataset": "PIAST-AT, 1900/1900 exact matched MIDI, human expert-majority mood tags",
        "inputs": "symbolic MIDI only; no audio or mood labels in feature extraction",
        "split": "five GroupKFold folds over original song/video identifiers",
        "model": "fixed C=.5 class-balanced logistic regression, median imputation, scaling",
        "selected_or_tuned_on_oof": False,
        "arms": list(ARMS),
        "tonal_distribution_features": list(TONAL_DISTRIBUTION_FEATURE_NAMES),
        "tonal_sequence_features": list(TONAL_SEQUENCE_FEATURE_NAMES),
        "hypothesis": "directional/adjoining key movement improves hard human mood ranking beyond tonal distribution",
        "oof": evaluated["scores"],
        "diagnostics": evaluated["diagnostics"],
        "paired_video_bootstrap_delta_ap_vs_baseline": uncertainty,
        "caveats": [
            "Exploratory repeated use of previously inspected 1900 labels; not external validation.",
            "Groups split by original song/video; within-group variants never cross train/test.",
            "Bootstrap conditional on fitted out-of-fold predictions; not a CI over training and hypothesis search.",
            "No per-mood variant selection, feature engineering, or hyperparameter fitting on fold outcomes.",
            "The random-order comparator preserves distribution but disrupts temporal adjacency.",
            "Average precision is not classification accuracy and varies with positive prevalence.",
        ],
    }
    (out / "tonal-cv-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    def fmt(value):
        return "—" if value is None else f"{value:.3f}"
    lines = ["# La tonalité suit-elle vraiment les émotions difficiles ?", "",
             "**Exploratoire : 1900 MIDI déjà examinés. Aucun nouveau test externe.**", "",
             "Cinq plis sans aucune œuvre/vidéo partagée ; les 10 statistiques de distribution sont séparées des 8 signatures de transition.",
             "", "| Variante | Dark (AP hors pli) | Hard 5 (mAP hors pli) | Noncalm 14 (mAP hors pli) |",
             "|---|---:|---:|---:|"]
    captions = {"baseline": "H1", "distribution": "H1 + distribution tonale",
                "temporal": "H1 + distribution + ordre réel",
                "permuted_temporal": "H1 + distribution + ordre mélangé"}
    for arm in ARMS:
        s = summary["oof"][arm]
        lines.append(f"| {captions[arm]} | {fmt(s['by_mood']['Dark'])} | "
                     f"{fmt(s['hard5_macro_ap'])} | {fmt(s['noncalm14_macro_ap'])} |")
    lines += ["", "## Émotions réellement difficiles", "",
              "| Émotion | Positifs / 1900 | H1 | Distribution | Ordre réel | Ordre mélangé |",
              "|---|---:|---:|---:|---:|---:|"]
    for mood in HARD_MOODS:
        lines.append(f"| {mood} | {summary['diagnostics']['mood_positives'][mood]} | " +
                     " | ".join(fmt(summary["oof"][arm]["by_mood"][mood]) for arm in ARMS) + " |")
    lines += ["", "## Incertitude (rééchantillonnage des vidéos ; Δ AP vs H1)", "",
              "| Variante | Dark Δ et IC 95 % | Hard 5 Δ et IC 95 % | Noncalm 14 Δ et IC 95 % |",
              "|---|---:|---:|---:|"]
    for arm in ARMS[1:]:
        fields = []
        for metric in ("Dark", "hard5_macro", "noncalm14_macro"):
            diff = (summary["oof"][arm]["by_mood"]["Dark"] - summary["oof"]["baseline"]["by_mood"]["Dark"])
            if metric != "Dark":
                key = "hard5_macro_ap" if metric == "hard5_macro" else "noncalm14_macro_ap"
                diff = summary["oof"][arm][key] - summary["oof"]["baseline"][key]
            ci = uncertainty[arm][metric]
            fields.append(f"{diff:+.3f} [{fmt(ci['ci_95_low'])}, {fmt(ci['ci_95_high'])}]")
        lines.append(f"| {captions[arm]} | " + " | ".join(fields) + " |")
    lines += ["", f"Contrôle étiquettes Dark mélangées **sur l'entraînement seulement** : "
              f"AP hors pli {fmt(summary['diagnostics']['negative_control']['train_label_permutation_dark_ap'])}.",
              "", "Attention : les intervalles conditionnent sur les prédictions déjà entraînées ; ce ne sont **pas** des preuves de nouvelle découverte.",
              "La sélection d'une variante à partir de ces résultats exigera un autre corpus d'annotations humaines indépendant.", ""]
    (out / "tonal-cv-summary.md").write_text("\n".join(lines), encoding="utf-8")
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    experiment(args.directory, args.out)
    print((args.out / "tonal-cv-summary.md").read_text(encoding="utf-8"), flush=True)


if __name__ == "__main__":
    main()
