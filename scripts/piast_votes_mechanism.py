"""Audit whether specific minority expert votes outperform generic label smoothing.

Exploratory follow-up after the SAME 1900 PIAST votes proved useful. Every
permutation uses training folds only, and preserves original >=2/3 hard tags.
No new unseen human labels; this cannot confirm the selected hypothesis.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from anamu.tonal_motion import TONAL_DISTRIBUTION_FEATURE_NAMES, TONAL_MOTION_FEATURE_NAMES
from .piast_at_benchmark import make_matrix, run
from .piast_tension_experiment import HARD_MOODS, NONCALM_MOODS
from .piast_tonal_cv import SEED, _ap, _predict, group_bootstrap, source_group_folds
from .piast_votes_experiment import expert_vote_fraction, predict_soft_votes


ARMS = ("baseline", "minority_only", "majority_only", "full_votes", "within_class_sham")


def training_vote_variant(votes: np.ndarray, variant: str, *, seed: int = SEED) -> np.ndarray:
    """Mutate vote strengths only, never MIDI features or held-out labels."""
    q = np.asarray(votes, dtype=float)
    if not np.isfinite(q).all() or np.any(~np.isin(q, (0, 1 / 3, 2 / 3, 1))):
        raise ValueError("invalid_original_vote_levels")
    if variant == "minority_only":
        return np.where(q >= 2 / 3, 1, q)
    if variant == "majority_only":
        return np.where(q >= 2 / 3, q, 0)
    if variant == "full_votes":
        return q.copy()
    if variant == "within_class_sham":
        new = q.copy()
        # Preserve membership in the human majority classes and the exact
        # vote-count distribution within each class, but break which clip
        # got the minority/unanimous annotation; seed fixed beforehand.
        rng = np.random.default_rng(seed)
        positive = q >= 2 / 3
        for mask in (positive, ~positive):
            idx = np.flatnonzero(mask)
            new[idx] = rng.permutation(q[idx])
        if not np.array_equal(positive, new >= 2 / 3):
            raise AssertionError("sham_modified_hard_targets")
        return new
    raise ValueError(f"unknown_vote_variant:{variant}")


def experiment(root: Path, out: Path, *, limit: int = 1900,
               bootstrap_repetitions: int = 500) -> dict:
    if limit != 1900:
        raise ValueError("requires_exact_previously_seen_1900")
    out.mkdir(parents=True, exist_ok=True)
    extraction = run(root, feature_set="research_tonal_motion", limit=limit,
                     cache_dir=out / "h1-cache", extract_only=True)
    records = extraction["records"]
    if extraction["matched"] != limit or len(records) != limit or extraction["rejected"]:
        raise AssertionError("incomplete_piast_cohort")
    clips = [c for c, _ in records]
    # Use the exact H1 + distribution partition from the preceding CV.
    features = [(c, {**{k: v for k, v in original.items()
                         if k not in TONAL_MOTION_FEATURE_NAMES},
                      **{k: original[k] for k in TONAL_DISTRIBUTION_FEATURE_NAMES}})
                for c, original in records]
    names = sorted({key for _, row in features for key in row})
    x = make_matrix(features, names)
    votes = {mood: np.asarray([expert_vote_fraction(clip, mood) for clip in clips])
             for mood in NONCALM_MOODS}
    truth = {mood: (v >= 2 / 3).astype(int) for mood, v in votes.items()}
    n = len(records)
    predictions = {arm: {mood: np.full(n, np.nan) for mood in NONCALM_MOODS}
                   for arm in ARMS}
    folds = []
    for fold, (train, test) in enumerate(source_group_folds(records, n_splits=5), 1):
        detail = {"fold": fold, "test": len(test), "groups": len({clips[i].song_group for i in test})}
        for mood in NONCALM_MOODS:
            y = truth[mood]
            for arm in ARMS:
                predicted = (_predict(x[train], x[test], y[train]) if arm == "baseline"
                             else predict_soft_votes(
                                 x[train], x[test], training_vote_variant(
                                     votes[mood][train], arm,
                                     seed=SEED + 97 * fold + NONCALM_MOODS.index(mood))))
                predictions[arm][mood][test] = predicted
        folds.append(detail)
        print(f"Within-class vote mechanism fold {fold}/5 finished", flush=True)
    if any(np.isnan(predictions[arm][mood]).any()
           for arm in ARMS for mood in NONCALM_MOODS):
        raise AssertionError("incomplete_oof")
    scored = {}
    for arm in ARMS:
        ap = {mood: _ap(truth[mood], predictions[arm][mood]) for mood in NONCALM_MOODS}
        if any(v is None for v in ap.values()):
            raise AssertionError("unscorable_tag")
        scored[arm] = {"by_mood": ap,
                       "hard5_macro_ap": float(np.mean([ap[m] for m in HARD_MOODS])),
                       "noncalm14_macro_ap": float(np.mean(list(ap.values()))),
                       "feature_count": len(names)}
    oof = {"groups": np.asarray([c.song_group for c in clips]),
           "labels": truth, "predictions": predictions}
    bootstrap = group_bootstrap(oof, repetitions=bootstrap_repetitions,
                                baseline_arm="baseline", arms=ARMS,
                                focus_moods=tuple(HARD_MOODS))
    summary = {
        "title": "Does clip-specific annotator disagreement, not generic label smoothing, drive the vote gain?",
        "research_status": "post-hoc mechanism audit on 1900 previously examined PIAST clips",
        "independent_new_holdout": False,
        "midi_only": True,
        "labels_in_features": False,
        "target": "original >=2/3 majority human mood labels on held-out video groups",
        "source": "PIAST-AT 1900/1900 matched MIDI, aggregate three-expert vote counts",
        "model": "fixed C=.5 class-balanced logistic; same H1+tonal distribution features in every arm",
        "sham_definition": "Within each training-fold mood, permute [0,1/3] among negatives and [2/3,1] among positives, retaining the exact original majority target and vote histograms",
        "hypothesis": "Actual per-clip vote fractions outperform within-class randomly assigned fractions",
        "arms": list(ARMS),
        "oof": scored,
        "folds": folds,
        "paired_video_bootstrap_delta_ap_vs_binary": bootstrap,
        "caveats": [
            "Mechanism-specific analysis selected after seeing the positive 1900-item soft-label result.",
            "Permutation maintains training majority categories, not original rater identities (unavailable).",
            "Bootstrap conditions on the trained out-of-fold predictions, not hypothesis search.",
            "No new independent human test set; differences remain exploratory.",
            "PIAST expert descriptors are not listeners' felt emotions.",
        ],
    }
    (out / "mechanism-summary.json").write_text(json.dumps(
        summary, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")

    def fmt(v):
        return "—" if v is None else f"{v:.3f}"

    label = {"baseline": "Majorité binaire", "minority_only": "Votes minoritaires seulement",
             "majority_only": "Incertitude des positifs seulement", "full_votes": "Vrais votes 0/⅓/⅔/1",
             "within_class_sham": "Votes réattribués dans chaque classe (placebo)"}
    lines = ["# D'où vient le gain des votes humains ?", "",
             "**Audit mécanistique exploratoire sur les mêmes 1900 clips PIAST déjà étudiés.**", "",
             "Même distribution tonale et mêmes cinq plis sans vidéo partagée dans toutes les variantes.",
             "", "| Variante | Tense AP | Mysterious AP | Epic AP | Dark AP | Happy AP | Hard5 mAP | Noncalm14 mAP |",
             "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for arm in ARMS:
        s = scored[arm]
        lines.append("| " + label[arm] + " | " + " | ".join(
            [fmt(s["by_mood"][m]) for m in ("Tense", "Mysterious", "Epic", "Dark", "Happy")]
            + [fmt(s["hard5_macro_ap"]), fmt(s["noncalm14_macro_ap"])]) + " |")
    lines += ["", "## Incertitude par groupe, Δ contre la majorité binaire", "",
              "| Variante | Tense Δ et IC95% | Mysterious Δ et IC95% | Epic Δ et IC95% | Dark Δ et IC95% | Hard5 Δ et IC95% |",
              "|---|---:|---:|---:|---:|---:|"]
    for arm in ARMS[1:]:
        cells = []
        for metric in ("Tense", "Mysterious", "Epic", "Dark", "hard5_macro"):
            delta = ((scored[arm]["hard5_macro_ap"] - scored["baseline"]["hard5_macro_ap"])
                     if metric == "hard5_macro" else
                     (scored[arm]["by_mood"][metric] - scored["baseline"]["by_mood"][metric]))
            ci = bootstrap[arm][metric]
            cells.append(f"{delta:+.3f} [{fmt(ci['ci_95_low'])}, {fmt(ci['ci_95_high'])}]")
        lines.append(f"| {label[arm]} | " + " | ".join(cells) + " |")
    lines += ["", "**Test central** : la différence entre les vrais votes et les votes réattribués "
              "dans la même classe élimine les effets de prévalence et de lissage de la seule "
              "majorité binaire ; seule l'association précise avec les morceaux diffère.",
              "", "Ce contrôle n'annule pas la sélection post-hoc de notre hypothèse.", ""]
    (out / "mechanism-summary.md").write_text("\n".join(lines), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    experiment(args.directory, args.out)
    print((args.out / "mechanism-summary.md").read_text(encoding="utf-8"), flush=True)


if __name__ == "__main__":
    main()
