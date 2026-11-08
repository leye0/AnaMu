"""Are PIAST emotion scores probabilities of individual expert endorsement?

Post-hoc diagnostics on all previously inspected 1900 human-labelled piano
MIDI clips. Fold-separated scores remain useful for methodology, but are NOT
new independent validation. No new tuning, audio or labels in MIDI features.

Contrast class-balanced learning, class-balanced learning with an analytic
training-prior odds correction, and an unweighted fractional-Bernoulli model.
Measure both the original majority-label ranking (AP) and the probability
of one randomly chosen expert voting yes (expected Bernoulli Brier/log loss).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from anamu.tonal_motion import TONAL_DISTRIBUTION_FEATURE_NAMES, TONAL_MOTION_FEATURE_NAMES
from .piast_at_benchmark import make_matrix, run
from .piast_tension_experiment import HARD_MOODS, NONCALM_MOODS
from .piast_tonal_cv import SEED, _ap, _predict, source_group_folds
from .piast_votes_experiment import expert_vote_fraction, predict_soft_votes


ARMS = ("hard_balanced", "soft_balanced", "soft_prior_corrected",
        "soft_unweighted", "prior_null")
FOCUS = ("Mysterious", "Epic", "Tense", "Dark", "Happy")


def prior_odds_correction(predicted: np.ndarray, positive_rate: float) -> np.ndarray:
    """Undo *train-derived* inverse-prevalence class weights on output odds.

    Exact odds relation for an unregularized, fully specified logistic model;
    a fixed analytic approximation here, not a fitted probability calibrator.
    """
    if not 0 < positive_rate < 1:
        raise ValueError("invalid_positive_prior")
    p = np.clip(np.asarray(predicted, dtype=float), 1e-8, 1 - 1e-8)
    return p * positive_rate / (p * positive_rate + (1 - p) * (1 - positive_rate))


def fractional_brier(q: np.ndarray, predicted: np.ndarray) -> float:
    """Expected Brier if Y is a randomly drawn Bernoulli(q) annotator vote."""
    q = np.asarray(q, dtype=float)
    p = np.asarray(predicted, dtype=float)
    if q.shape != p.shape or not np.isfinite(q).all() or not np.isfinite(p).all():
        raise ValueError("invalid_brier_input")
    if np.any((q < 0) | (q > 1) | (p < 0) | (p > 1)):
        raise ValueError("invalid_probability_range")
    return float(np.mean(q * (1 - p) ** 2 + (1 - q) * p ** 2))


def fractional_logloss(q: np.ndarray, predicted: np.ndarray) -> float:
    q = np.asarray(q, dtype=float)
    p = np.clip(np.asarray(predicted, dtype=float), 1e-8, 1 - 1e-8)
    if q.shape != p.shape or not np.isfinite(q).all() or not np.isfinite(p).all():
        raise ValueError("invalid_logloss_input")
    if np.any((q < 0) | (q > 1)):
        raise ValueError("invalid_vote_range")
    return float(-np.mean(q * np.log(p) + (1 - q) * np.log1p(-p)))


def summarize_scores(votes: dict, majority: dict, predictions: dict) -> dict:
    scores = {}
    for arm in ARMS:
        by_mood = {}
        for mood in NONCALM_MOODS:
            q, p = votes[mood], predictions[arm][mood]
            by_mood[mood] = {
                "ap_majority": _ap(majority[mood], p),
                "brier_individual_vote": fractional_brier(q, p),
                "logloss_individual_vote": fractional_logloss(q, p),
                "mean_predicted": float(np.mean(p)),
                "observed_mean_vote_fraction": float(np.mean(q)),
                "mean_majority_positive": float(np.mean(majority[mood])),
            }
        scores[arm] = {
            "by_mood": by_mood,
            "hard5_macro_ap": float(np.mean([by_mood[m]["ap_majority"] for m in HARD_MOODS])),
            "hard5_macro_brier": float(np.mean([by_mood[m]["brier_individual_vote"] for m in HARD_MOODS])),
            "hard5_macro_logloss": float(np.mean([by_mood[m]["logloss_individual_vote"] for m in HARD_MOODS])),
            "noncalm14_macro_ap": float(np.mean([v["ap_majority"] for v in by_mood.values()])),
            "noncalm14_macro_brier": float(np.mean([v["brier_individual_vote"] for v in by_mood.values()])),
        }
    return scores


def group_brier_bootstrap(groups: np.ndarray, votes: dict, predictions: dict,
                          *, repetitions: int = 500) -> dict:
    """Paired video-bootstrap on *already fitted* OOF predictions only."""
    distinct, inverse = np.unique(groups, return_inverse=True)
    indexes = [np.flatnonzero(inverse == index) for index in range(len(distinct))]
    rng = np.random.default_rng(SEED + 347)
    candidates = [arm for arm in ARMS if arm != "soft_balanced"]
    metrics = ("hard5_macro", "noncalm14_macro") + FOCUS
    samples = {arm: {metric: [] for metric in metrics} for arm in candidates}
    for _ in range(repetitions):
        draws = rng.integers(0, len(indexes), size=len(indexes))
        idx = np.concatenate([indexes[int(i)] for i in draws])
        baseline = {m: fractional_brier(votes[m][idx], predictions["soft_balanced"][m][idx])
                    for m in NONCALM_MOODS}
        for arm in candidates:
            improvement = {m: baseline[m] - fractional_brier(
                votes[m][idx], predictions[arm][m][idx]) for m in NONCALM_MOODS}
            for mood in FOCUS:
                samples[arm][mood].append(improvement[mood])
            for name, labelset in (("hard5_macro", HARD_MOODS),
                                   ("noncalm14_macro", NONCALM_MOODS)):
                samples[arm][name].append(float(np.mean([improvement[m] for m in labelset])))
    return {arm: {metric: {"ci_95_low": float(np.quantile(v, .025)),
                           "ci_95_high": float(np.quantile(v, .975)),
                           "fraction_positive": float(np.mean(np.asarray(v) > 0))}
                  for metric, v in by_metric.items()}
            for arm, by_metric in samples.items()}


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
    features = [(clip, {**{k: v for k, v in f.items()
                          if k not in TONAL_MOTION_FEATURE_NAMES},
                       **{k: f[k] for k in TONAL_DISTRIBUTION_FEATURE_NAMES}})
                for clip, f in records]
    feature_names = sorted({key for _, f in features for key in f})
    x = make_matrix(features, feature_names)
    votes = {mood: np.asarray([expert_vote_fraction(c, mood) for c in clips], dtype=float)
             for mood in NONCALM_MOODS}
    majority = {mood: (q >= 2 / 3).astype(int) for mood, q in votes.items()}
    if any(not np.array_equal(majority[m], [int(m in c.mood_tags()) for c in clips])
           for m in NONCALM_MOODS):
        raise AssertionError("majority_targets_mismatch")
    n = len(records)
    predicted = {arm: {mood: np.full(n, np.nan) for mood in NONCALM_MOODS}
                 for arm in ARMS}
    folds = []
    for fold, (train, test) in enumerate(source_group_folds(records, n_splits=5), 1):
        for mood in NONCALM_MOODS:
            q = votes[mood][train]
            positive_rate = float(np.mean(q))
            hard = _predict(x[train], x[test], majority[mood][train])
            balanced = predict_soft_votes(x[train], x[test], q)
            unweighted = predict_soft_votes(x[train], x[test], q, class_balanced=False)
            calibrated = prior_odds_correction(balanced, positive_rate)
            values = {"hard_balanced": hard, "soft_balanced": balanced,
                      "soft_prior_corrected": calibrated,
                      "soft_unweighted": unweighted,
                      "prior_null": np.full(len(test), positive_rate)}
            for arm, value in values.items():
                predicted[arm][mood][test] = value
        folds.append({"fold": fold, "test_clips": len(test),
                      "test_video_groups": len({clips[i].song_group for i in test})})
        print(f"Vote probability calibration fold {fold}/5 complete", flush=True)
    if any(np.isnan(predicted[arm][mood]).any()
           for arm in ARMS for mood in NONCALM_MOODS):
        raise AssertionError("incomplete_oof")
    scored = summarize_scores(votes, majority, predicted)
    uncertainty = group_brier_bootstrap(np.asarray([c.song_group for c in clips]),
                                        votes, predicted, repetitions=bootstrap_repetitions)
    summary = {
        "title": "Are class-balanced soft-vote outputs calibrated probabilities of expert agreement?",
        "research_status": "post-hoc exploratory on previously inspected 1900 PIAST annotated MIDI",
        "independent_new_holdout": False,
        "corpus": "PIAST-AT 1900/1900 matched; only symbolic MIDI; 3 aggregate expert votes per mood",
        "semantics": "per-mood Bernoulli probability of a similarly sampled expert selecting the descriptor, not mutually exclusive emotion mass",
        "metric_definition": "E[(p-Y)^2|q]=q(1-p)^2+(1-q)p^2; q takes values 0, 1/3, 2/3 or 1; expected Bernoulli log loss also reported",
        "prior_correction": "p*q_prior/[p*q_prior+(1-p)*(1-q_prior)], using TRAIN-fold mean vote fraction only; no fitted calibration",
        "model": "same fixed H1+10 tonal distribution features, C=.5 logistic with median imputation and scaling",
        "original_target": "majority >= 2 of 3 for AP; soft votes never enter MIDI features or held-out predictions",
        "splits": "five original-source-video-disjoint GroupKFold folds",
        "arms": list(ARMS), "feature_count": len(feature_names),
        "oof": scored, "folds": folds,
        "paired_video_bootstrap_brier_improvement_vs_soft_balanced": uncertainty,
        "caveats": [
            "Empirical 3-rater fractions are noisy and rater selection is not a universal population measure.",
            "These are descriptive expert tags, not directly felt emotion or a mutually exclusive emotion probability.",
            "Balanced logistic scores target reweighted odds and are not calibrated by construction.",
            "Prior odds correction is an analytic approximation, not a guarantee with penalization/misspecification.",
            "Bootstrap conditional on fitted OOF predictions; repeated use of all 1900 labels prevents confirmatory claims.",
        ],
    }
    (out / "calibration-summary.json").write_text(json.dumps(
        summary, ensure_ascii=False, allow_nan=False, indent=2) + "\n", encoding="utf-8")

    def f(v):
        return f"{v:.3f}"

    captions = {"hard_balanced": "Majorité binaire, classes équilibrées",
                "soft_balanced": "Votes fractionnaires, classes équilibrées",
                "soft_prior_corrected": "Votes fractionnaires, correction des cotes",
                "soft_unweighted": "Votes fractionnaires, sans rééquilibrage",
                "prior_null": "Taux moyen des votes à l'entraînement (null)"}
    lines = ["# 0,5 signifie-t-il vraiment une probabilité émotionnelle de 50 % ?", "",
             "**Non automatiquement : ce sont des scores multi-étiquettes rééquilibrés.**", "",
             "Même cohorte de 1900 MIDI et même configuration que les tests précédents ; protocole exploratoire.",
             "Les pertes Brier/logarithmiques évaluent une voix d'expert tirée au hasard, "
             "d'après les trois votes disponibles ; une valeur plus basse est meilleure.",
             "", "| Modèle | Hard5 AP ↑ | Hard5 Brier ↓ | Hard5 Log-loss ↓ | Noncalm14 AP ↑ | Noncalm14 Brier ↓ |",
             "|---|---:|---:|---:|---:|---:|"]
    for arm in ARMS:
        s = scored[arm]
        lines.append(f"| {captions[arm]} | {f(s['hard5_macro_ap'])} | "
                     f"{f(s['hard5_macro_brier'])} | {f(s['hard5_macro_logloss'])} | "
                     f"{f(s['noncalm14_macro_ap'])} | {f(s['noncalm14_macro_brier'])} |")
    lines += ["", "## Les cinq émotions difficiles : erreur de probabilité par voix", "",
              "| Émotion | Taux de vote humain | Balanced : préd. moy. | Balanced : Brier | Odds corrigés : Brier | Sans poids : Brier |",
              "|---|---:|---:|---:|---:|---:|"]
    for mood in FOCUS:
        a = scored["soft_balanced"]["by_mood"][mood]
        b = scored["soft_prior_corrected"]["by_mood"][mood]
        c = scored["soft_unweighted"]["by_mood"][mood]
        lines.append(f"| {mood} | {f(a['observed_mean_vote_fraction'])} | "
                     f"{f(a['mean_predicted'])} | {f(a['brier_individual_vote'])} | "
                     f"{f(b['brier_individual_vote'])} | {f(c['brier_individual_vote'])} |")
    lines += ["", "## Brier : gains contre le modèle fractionnaire rééquilibré", "",
              "| Modèle | Hard5 amélioration (IC95% par vidéo) | Noncalm14 amélioration (IC95% par vidéo) |",
              "|---|---:|---:|"]
    for arm in ARMS:
        if arm == "soft_balanced":
            continue
        ss = []
        for metric, field in (("hard5_macro", "hard5_macro_brier"),
                              ("noncalm14_macro", "noncalm14_macro_brier")):
            delta = scored["soft_balanced"][field] - scored[arm][field]
            ci = uncertainty[arm][metric]
            ss.append(f"{delta:+.3f} [{f(ci['ci_95_low'])}, {f(ci['ci_95_high'])}]")
        lines.append(f"| {captions[arm]} | " + " | ".join(ss) + " |")
    lines += ["", "Dans ce protocole, une sortie 0,5 pour *Epic* doit seulement être "
              "interprétée comme « une moitié des annotateurs de ce type diraient Epic » "
              "si la calibration est démontrée ; jamais 50 % de toute la masse d'émotions possibles.",
              "", "La classe *Relaxing/Calm* est exclue des moyennes ciblées.", ""]
    (out / "calibration-summary.md").write_text("\n".join(lines), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    experiment(args.directory, args.out)
    print((args.out / "calibration-summary.md").read_text(encoding="utf-8"), flush=True)


if __name__ == "__main__":
    main()
