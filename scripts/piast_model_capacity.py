"""Fixed-capacity ablation on existing MIDI features; exploratory, not a holdout."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from threadpoolctl import threadpool_limits

from anamu.tonal_motion import TONAL_DISTRIBUTION_FEATURE_NAMES, TONAL_MOTION_FEATURE_NAMES
from .piast_at_benchmark import make_matrix, run
from .piast_tension_experiment import HARD_MOODS, NONCALM_MOODS
from .piast_tonal_cv import SEED, _ap, group_bootstrap, source_group_folds
from .piast_votes_experiment import expert_vote_fraction, predict_soft_votes

ARMS = ("linear_votes", "linear_unbalanced", "additive_votes", "interaction_votes")


def predict_tree_votes(train_x, test_x, votes, *, depth):
    votes = np.asarray(votes, dtype=float)
    if votes.ndim != 1 or len(votes) != len(train_x) or not len(votes):
        raise ValueError("invalid_vote_dimensions")
    if not np.isfinite(votes).all() or np.any((votes < 0) | (votes > 1)):
        raise ValueError("invalid_vote_fraction")
    if depth not in (1, 3):
        raise ValueError("unregistered_depth")
    observed = np.isfinite(train_x).any(axis=0)
    if not observed.any():
        return np.full(len(test_x), float(votes.mean()))
    train_x, test_x = train_x[:, observed], test_x[:, observed]
    # Native missing-value routing and bin boundaries are fit on training only.
    # No internal random validation split can leak another clip of a test video.
    model = HistGradientBoostingRegressor(
        loss="squared_error", max_iter=150, learning_rate=.05,
        max_depth=depth, max_leaf_nodes=2 ** depth, min_samples_leaf=30,
        l2_regularization=5, early_stopping=False, random_state=SEED)
    model.fit(train_x, votes)
    return np.clip(model.predict(test_x), 0, 1)


def experiment(root: Path, out: Path, *, bootstrap_repetitions=500):
    out.mkdir(parents=True, exist_ok=True)
    extraction = run(root, feature_set="research_tonal_motion", limit=1900,
                     cache_dir=out / "h1-cache", extract_only=True)
    records = extraction["records"]
    if extraction["matched"] != 1900 or len(records) != 1900 or extraction["rejected"]:
        raise AssertionError("incomplete_piast_cohort")
    excluded = set(TONAL_MOTION_FEATURE_NAMES) - set(TONAL_DISTRIBUTION_FEATURE_NAMES)
    records = [(c, {k: v for k, v in f.items() if k not in excluded}) for c, f in records]
    clips = [c for c, _ in records]
    names = sorted({k for _, f in records for k in f})
    x = make_matrix(records, names)
    votes = {m: np.asarray([expert_vote_fraction(c, m) for c in clips]) for m in NONCALM_MOODS}
    labels = {m: (v >= 2 / 3).astype(int) for m, v in votes.items()}
    for m in NONCALM_MOODS:
        if not np.array_equal(labels[m], [int(m in c.mood_tags()) for c in clips]):
            raise AssertionError("majority_reconstruction_failed")
    predictions = {a: {m: np.full(len(clips), np.nan) for m in NONCALM_MOODS} for a in ARMS}
    control = {m: np.full(len(clips), np.nan) for m in HARD_MOODS}
    fold_ids = np.full(len(clips), -1, dtype=int)
    folds = []
    for fold, (train, test) in enumerate(source_group_folds(records), 1):
        fold_ids[test] = fold
        for m in NONCALM_MOODS:
            predictions["linear_votes"][m][test] = predict_soft_votes(x[train], x[test], votes[m][train])
            predictions["linear_unbalanced"][m][test] = predict_soft_votes(
                x[train], x[test], votes[m][train], class_balanced=False)
            for arm, depth in (("additive_votes", 1), ("interaction_votes", 3)):
                predictions[arm][m][test] = predict_tree_votes(x[train], x[test], votes[m][train], depth=depth)
            if m in HARD_MOODS:
                shuffled = np.random.default_rng(SEED + fold).permutation(votes[m][train])
                control[m][test] = predict_tree_votes(x[train], x[test], shuffled, depth=3)
        scores = {a: {m: _ap(labels[m][test], predictions[a][m][test]) for m in NONCALM_MOODS}
                  for a in ARMS}
        folds.append({"fold": fold, "train": len(train), "test": len(test), "ap": scores})
        print(f"Capacity fold {fold}/5 complete", flush=True)
    if (fold_ids < 1).any() or any(not np.isfinite(p).all() for arm in predictions.values() for p in arm.values()):
        raise AssertionError("incomplete_oof")
    scores = {}
    for a in ARMS:
        ap = {m: _ap(labels[m], predictions[a][m]) for m in NONCALM_MOODS}
        scores[a] = {"by_mood": ap, "hard5_macro_ap": float(np.mean([ap[m] for m in HARD_MOODS])),
                     "noncalm14_macro_ap": float(np.mean(list(ap.values())))}
    groups = np.asarray([c.song_group for c in clips])
    oof = {"groups": groups, "labels": labels, "predictions": predictions}
    contrasts = {baseline: group_bootstrap(oof, repetitions=bootstrap_repetitions,
                    baseline_arm=baseline, arms=ARMS, focus_moods=tuple(HARD_MOODS))
                 for baseline in ("linear_unbalanced", "additive_votes")}
    result = {"status": "exploratory; previously examined cohort, no independent confirmation",
              "matched": len(clips), "source_groups": len(set(groups)), "feature_names": names,
              "protocol": "docs/piast-nonlinear-protocol.md", "scores": scores, "folds": folds,
              "negative_control_ap": {m: _ap(labels[m], control[m]) for m in HARD_MOODS},
              "prevalence": {m: float(labels[m].mean()) for m in NONCALM_MOODS},
              "paired_group_bootstrap": contrasts,
              "limitations": ["Bootstrap conditions on fitted OOF models; it does not account for hypothesis search.",
                              "A nonlinear gain is not evidence of a temporal or causal musical mechanism.",
                              "Missing timbre is a hypothesis, not established by a MIDI-only comparison."]}
    (out / "capacity-summary.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    # No raw MIDI, only identities, annotations and derived held-out predictions.
    audit = {"clip_ids": [c.clip_id for c in clips], "groups": groups.tolist(), "folds": fold_ids.tolist(),
             "labels": {m: v.tolist() for m, v in labels.items()},
             "predictions": {a: {m: p.tolist() for m, p in v.items()} for a, v in predictions.items()},
             "negative_control": {m: p.tolist() for m, p in control.items()}}
    (out / "capacity-oof.json").write_text(json.dumps(audit, allow_nan=False) + "\n")
    lines = ["# Capacité non linéaire sur les mêmes indices MIDI", "",
             "Exploratoire : les 1 900 clips avaient déjà été examinés. Aucun modèle promu.", "",
             "| Modèle | " + " | ".join(HARD_MOODS) + " | Hard5 mAP | Noncalm14 mAP |",
             "|---|" + "---:|" * (len(HARD_MOODS) + 2)]
    for a in ARMS:
        s = scores[a]
        vals = [s["by_mood"][m] for m in HARD_MOODS] + [s["hard5_macro_ap"], s["noncalm14_macro_ap"]]
        lines.append(f"| {a} | " + " | ".join(f"{v:.3f}" for v in vals) + " |")
    lines += ["", "Les prédictions hors pli, contrôles négatifs, résultats par pli et intervalles",
              "par bootstrap de vidéos sont enregistrés dans les JSON associés.", ""]
    (out / "capacity-summary.md").write_text("\n".join(lines))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    with threadpool_limits(limits=2):
        experiment(args.directory, args.out)
    print((args.out / "capacity-summary.md").read_text())


if __name__ == "__main__":
    main()
