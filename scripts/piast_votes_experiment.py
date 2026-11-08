"""Do minority human votes improve difficult PIAST emotion ranking?

Per-label soft Bernoulli likelihoods use 0, 1/3, 2/3 and 1 based on
three aggregated annotator votes. Held-out evaluation STILL targets the
original hard majority (>=2/3) on isolated source video groups.

All 1900 labels were previously examined: this is an exploratory ablation,
not a new independent holdout or a human agreement ceiling estimate.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from anamu.piast_at import PIASTClip
from anamu.tonal_motion import TONAL_DISTRIBUTION_FEATURE_NAMES, TONAL_MOTION_FEATURE_NAMES
from .piast_at_benchmark import make_matrix, run
from .piast_tension_experiment import HARD_MOODS, NONCALM_MOODS
from .piast_tonal_cv import SEED, _ap, _predict, group_bootstrap, source_group_folds


ARMS = ("h1_hard", "h1_votes", "distribution_hard", "distribution_votes")


def expert_vote_fraction(clip: PIASTClip, label: str) -> float:
    """Exactly 0, 1/3, 2/3 or 1; never reconstruct individual rater IDs."""
    if label in clip.agreement_3:
        return 1.0
    if label in clip.agreement_2:
        return 2 / 3
    if label in clip.agreement_1:
        return 1 / 3
    return 0.0


def predict_soft_votes(train_x: np.ndarray, test_x: np.ndarray,
                       vote_fractions: np.ndarray) -> np.ndarray:
    """Optimize class-balanced expected log loss under fractional Bernoulli tags.

    Each source contributes positive and negative loss in proportion to its
    vote fraction. For {0,1} fractions this has the same objective as the
    historic class_weight='balanced' logistic regression, with total weight N.
    No threshold, cut-off or label-dependent feature is engineered.
    """
    votes = np.asarray(vote_fractions, dtype=float)
    if votes.ndim != 1 or len(votes) != len(train_x) or len(votes) == 0:
        raise ValueError("invalid_vote_dimensions")
    if not np.isfinite(votes).all() or np.any((votes < 0) | (votes > 1)):
        raise ValueError("invalid_vote_fraction")
    n = len(votes)
    positives = float(votes.sum())
    if positives <= 0 or positives >= n:
        return np.full(len(test_x), positives / n)
    model = Pipeline([
        ("missing", SimpleImputer(strategy="median", keep_empty_features=True,
                                   add_indicator=True)),
        ("scale", StandardScaler()),
        ("classifier", LogisticRegression(C=.5, max_iter=1200, random_state=SEED)),
    ])
    duplicated = np.concatenate([train_x, train_x], axis=0)
    outcomes = np.concatenate([np.ones(n, dtype=int), np.zeros(n, dtype=int)])
    weights = np.concatenate([votes * n / (2 * positives),
                              (1 - votes) * n / (2 * (n - positives))])
    model.fit(duplicated, outcomes, classifier__sample_weight=weights)
    return model.predict_proba(test_x)[:, 1]


def vote_agreement_diagnostics(clips: list[PIASTClip]) -> dict:
    counts = {}
    for mood in NONCALM_MOODS:
        levels = [sum(mood in getattr(c, f"agreement_{vote}") for c in clips)
                  for vote in (1, 2, 3)]
        minority, majority_two, unanimous = levels
        any_votes = sum(levels)
        counts[mood] = {
            "zero_votes": len(clips) - any_votes,
            "one_vote": minority, "two_votes": majority_two, "three_votes": unanimous,
            "majority_positive": majority_two + unanimous,
            "fraction_any_to_majority": (majority_two + unanimous) / any_votes if any_votes else None,
            "fraction_majority_to_unanimity": unanimous / (majority_two + unanimous)
            if majority_two + unanimous else None,
        }
    return counts


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
    clips = [clip for clip, _ in records]
    base = [(clip, {k: v for k, v in features.items()
                    if k not in TONAL_MOTION_FEATURE_NAMES}) for clip, features in records]
    distribution = [(clip, {**basics, **{k: features[k] for k in TONAL_DISTRIBUTION_FEATURE_NAMES}})
                    for (clip, basics), (_, features) in zip(base, records)]
    features_by_arm = {"h1_hard": base, "h1_votes": base,
                       "distribution_hard": distribution, "distribution_votes": distribution}
    matrices = {arm: make_matrix(rows, sorted({k for _, feat in rows for k in feat}))
                for arm, rows in features_by_arm.items()}
    votes = {mood: np.asarray([expert_vote_fraction(clip, mood) for clip in clips])
             for mood in NONCALM_MOODS}
    labels = {mood: (v >= (2 / 3)).astype(int) for mood, v in votes.items()}
    for mood in NONCALM_MOODS:
        if not np.array_equal(labels[mood], [int(mood in c.mood_tags()) for c in clips]):
            raise AssertionError("majority_vote_reconstruction_failed")

    n = len(clips)
    predictions = {arm: {mood: np.full(n, np.nan) for mood in NONCALM_MOODS}
                   for arm in ARMS}
    scrambled_dark = np.full(n, np.nan)
    fold_details = []
    for fold, (train, test) in enumerate(source_group_folds(records, n_splits=5), 1):
        fold_result = {"fold": fold, "test": len(test),
                       "test_source_groups": len({clips[i].song_group for i in test}),
                       "ap": {arm: {} for arm in ARMS}}
        for arm in ARMS:
            x_train, x_test = matrices[arm][train], matrices[arm][test]
            for mood in NONCALM_MOODS:
                prediction = (predict_soft_votes(x_train, x_test, votes[mood][train])
                              if arm.endswith("_votes") else _predict(x_train, x_test, labels[mood][train]))
                predictions[arm][mood][test] = prediction
                fold_result["ap"][arm][mood] = _ap(labels[mood][test], prediction)
        # Break training-vote/feature association, leaving held-out truth untouched.
        permuted_votes = np.random.default_rng(SEED + fold).permutation(votes["Dark"][train])
        scrambled_dark[test] = predict_soft_votes(matrices["distribution_votes"][train],
                                                   matrices["distribution_votes"][test],
                                                   permuted_votes)
        fold_details.append(fold_result)
        print(f"Vote-learning CV fold {fold}/5 finished; {len(test)} test clips", flush=True)
    if any(np.isnan(predictions[arm][mood]).any() for arm in ARMS for mood in NONCALM_MOODS):
        raise AssertionError("incomplete_oof")
    scores = {}
    for arm in ARMS:
        ap = {mood: _ap(labels[mood], predictions[arm][mood]) for mood in NONCALM_MOODS}
        if any(v is None for v in ap.values()):
            raise AssertionError("insufficient_mood_labels")
        scores[arm] = {"by_mood": ap, "hard5_macro_ap": float(np.mean([ap[m] for m in HARD_MOODS])),
                       "noncalm14_macro_ap": float(np.mean(list(ap.values()))),
                       "feature_count": matrices[arm].shape[1]}
    oof = {"groups": np.asarray([c.song_group for c in clips]),
           "labels": labels, "predictions": predictions}
    contrasts = group_bootstrap(oof, repetitions=bootstrap_repetitions,
                                baseline_arm="distribution_hard", arms=ARMS,
                                focus_moods=tuple(HARD_MOODS))
    summary = {
        "title": "PIAST expert-vote fractions versus majority hard-label learning",
        "research_status": "post-hoc exploratory; all 1900 human tags previously examined",
        "independent_new_holdout": False,
        "corpus": "1900 of 1900 original PIAST-AT symbolic MIDI, no audio",
        "targets": "original majority labels evaluated; no test-vote softening or changed metric",
        "train_vote_fractions": [0, 1 / 3, 2 / 3, 1],
        "principle": "class-balanced fractional Bernoulli cross entropy via weighted duplicated examples",
        "literature": "Xin Geng (2016) Label Distribution Learning; per-label Bernoulli adaptation, not normalized multiclass LDL",
        "fixed_classifier": "C=.5 logistic, median imputation + indicators, standard scaling",
        "fixed_splits": "five source-video-disjoint GroupKFold folds",
        "matched": len(records),
        "arms": list(ARMS),
        "votes_by_mood": vote_agreement_diagnostics(clips),
        "oof": scores,
        "fold_diagnostics": fold_details,
        "negative_control_shuffled_train_votes_dark_ap": _ap(labels["Dark"], scrambled_dark),
        "paired_video_bootstrap_delta_ap_vs_distribution_hard": contrasts,
        "caveats": [
            "Soft votes reveal annotator disagreement; they do not establish a human-performance ceiling.",
            "Individual annotator identities unavailable: three consensus counts, not individual vote vectors.",
            "PIAST target is descriptive expert mood annotations, not listeners' felt emotion.",
            "Every label and previous baseline examined repeatedly; no fresh independent confirmation.",
            "Group bootstrap conditions on fitted OOF predictions, not hypothesis search.",
            "Average precision depends on prevalence and is not a classification accuracy.",
        ],
    }
    (out / "votes-summary.json").write_text(json.dumps(
        summary, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")

    def fmt(value):
        return "—" if value is None else f"{value:.3f}"

    captions = {"h1_hard": "H1 : majorité binaire", "h1_votes": "H1 : votes fractionnaires",
                "distribution_hard": "Distribution tonale : majorité binaire",
                "distribution_votes": "Distribution tonale : votes fractionnaires"}
    lines = ["# Est-ce qu'ignorer les votes minoritaires nous prive de signal ?", "",
             "**Exploratoire seulement : même cohorte humaine de 1 900 extraits déjà examinée.**", "",
             "Apprentissage sur 0, ⅓, ⅔, 1 vote; évaluation strictement sur la majorité humaine (2 ou 3 votes).",
             "", "## Cohérence des annotations originales", "",
             "| Émotion | 0 vote | 1 vote | 2 votes | 3 votes | Part majoritaire parmi les mentions |",
             "|---|---:|---:|---:|---:|---:|"]
    for mood in ("Mysterious", "Epic", "Tense", "Dark", "Happy", "Relaxing/Calm"):
        if mood == "Relaxing/Calm":
            continue  # This run focuses exclusively on non-calm labels.
        row = summary["votes_by_mood"][mood]
        lines.append(f"| {mood} | {row['zero_votes']} | {row['one_vote']} | "
                     f"{row['two_votes']} | {row['three_votes']} | "
                     f"{row['fraction_any_to_majority']:.1%} |")
    lines += ["", "## Prédiction hors vidéo d'entraînement (AP)", "",
              "| Variante | Tense | Mysterious | Epic | Dark | Happy | Hard5 mAP | Noncalm14 mAP |",
              "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for arm in ARMS:
        result = scores[arm]
        lines.append("| " + captions[arm] + " | " + " | ".join(
            [fmt(result["by_mood"][mood]) for mood in ("Tense", "Mysterious", "Epic", "Dark", "Happy")]
            + [fmt(result["hard5_macro_ap"]), fmt(result["noncalm14_macro_ap"])]) + " |")
    lines += ["", "## Incertitude : comparaison au meilleur modèle binaire actuel", "",
              "| Variante | Tense ΔAP | Mysterious ΔAP | Epic ΔAP | Dark ΔAP | Happy ΔAP | Hard5 ΔmAP |",
              "|---|---:|---:|---:|---:|---:|---:|"]
    for arm in ARMS:
        if arm == "distribution_hard":
            continue
        fields = []
        for mood in ("Tense", "Mysterious", "Epic", "Dark", "Happy"):
            value = scores[arm]["by_mood"][mood] - scores["distribution_hard"]["by_mood"][mood]
            bounds = contrasts[arm][mood]
            fields.append(f"{value:+.3f} [{fmt(bounds['ci_95_low'])}, {fmt(bounds['ci_95_high'])}]")
        value = scores[arm]["hard5_macro_ap"] - scores["distribution_hard"]["hard5_macro_ap"]
        bounds = contrasts[arm]["hard5_macro"]
        fields.append(f"{value:+.3f} [{fmt(bounds['ci_95_low'])}, {fmt(bounds['ci_95_high'])}]")
        lines.append(f"| {captions[arm]} | " + " | ".join(fields) + " |")
    lines += ["", "Contrôle négatif : votes *Dark* mélangés uniquement à l'entraînement, "
              f"AP hors pli {fmt(summary['negative_control_shuffled_train_votes_dark_ap'])}.",
              "", "Cette méthode suit une adaptation multi-étiquettes de l'idée de *Label Distribution Learning* "
              "(Xin Geng, TKDE 2016) : chaque vote informe une probabilité par émotion, et les étiquettes "
              "ne sont pas normalisées entre elles.",
              "", "Les votes d'experts sont eux-mêmes inclus dans la majorité de référence : "
              "ces chiffres ne calculent pas un plafond de performance humaine. Les mêmes 1 900 clips "
              "avaient déjà servi à d'autres recherches.", ""]
    (out / "votes-summary.md").write_text("\n".join(lines), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    experiment(args.directory, args.out)
    print((args.out / "votes-summary.md").read_text(encoding="utf-8"), flush=True)


if __name__ == "__main__":
    main()
