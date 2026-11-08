"""Hard-mood-first Farbood-inspired MIDI ablation, evaluated on unseen clips.

Hard moods were fixed from the *previous* 1400-piece validation, before the
new 1400..1900 MIDI were loaded: the five lowest AP eligible moods were
Mysterious, Epic, Tense, Dark and Happy. Generic Emotional and easy Calm
never contribute to the two primary evaluation metrics.
"""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

from anamu.piast_at import MOOD_LABELS

from .piast_at_benchmark import run


HARD_MOODS = ("Mysterious", "Epic", "Tense", "Dark", "Happy")
NONCALM_MOODS = tuple(x for x in MOOD_LABELS if x not in ("Emotional", "Relaxing/Calm"))
VARIANTS = (
    ("research_cues", "H1 : indices physiques, aucune attente"),
    ("research_surprise", "H1 + surprise melodique seule"),
    ("research_tension", "H1 + tendances de tension"),
    ("research_tension_shuffled", "H1 + tension sur mesures melangees"),
    ("research_surprise_tension", "H1 + surprise + tendances de tension"),
)


def focus_stats(split: dict | None, tags: tuple[str, ...]) -> dict | None:
    if split is None:
        return None
    labels = [split["per_mood"][x] for x in tags if split["per_mood"][x]["eligible"]]
    return {
        "target_labels": list(tags),
        "eligible_labels": len(labels),
        "required_labels": len(tags),
        "all_targets_eligible": len(labels) == len(tags),
        "mean_ap": statistics.mean(x["average_precision"] for x in labels)
            if labels else None,
        "mean_frequency_baseline": statistics.mean(x["prevalence_baseline_ap"]
                                                   for x in labels) if labels else None,
        "positive_counts": {x: split["per_mood"][x]["evaluated_positives"] for x in tags},
        "ap_by_mood": {x: split["per_mood"][x]["average_precision"] for x in tags},
    }


def experiment(root: Path, out: Path, *, limit: int = 1900,
               fresh_after: int = 1400, seed: int = 20261108) -> dict:
    if limit <= fresh_after or fresh_after < 1400:
        raise ValueError("requires_truly_unseen_cohort_after_prior_1400")
    out.mkdir(parents=True, exist_ok=True)
    outcomes = {}
    for name, _ in VARIANTS:
        outcome = run(root, feature_set=name, cache_dir=out / "feature-cache",
                      limit=limit, fresh_after=fresh_after, seed=seed)
        outcomes[name] = outcome
        (out / (name + ".json")).write_text(json.dumps(
            outcome, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
            encoding="utf-8")
    baseline = outcomes["research_cues"]
    if baseline["local_matched_midis"] != limit:
        raise ValueError("incomplete_piast_cohort")
    assert all(x["split_sizes"] == baseline["split_sizes"]
               and x["split_source_groups"] == baseline["split_source_groups"]
               and x["fresh_heldout_test_size"] == baseline["fresh_heldout_test_size"]
               for x in outcomes.values())
    metrics = {name: {split_name: {
        "hard_five": focus_stats(outcome[split_name], HARD_MOODS),
        "all_noncalm": focus_stats(outcome[split_name], NONCALM_MOODS),
        "all_named_including_calm": outcome[split_name]["named_moods"]
            if outcome[split_name] else None,
    } for split_name in ("validation", "test", "fresh_test")}
        for name, outcome in outcomes.items()}
    summary = {
        "study": "Farbood 2012 inspired trend salience and memory-window MIDI approximation",
        "preregistration": "hard-five labels selected only from 1400-piece validation, before 1900-piece test",
        "hard_moods": list(HARD_MOODS),
        "noncalm_moods": list(NONCALM_MOODS),
        "source": "PIAST-AT human-majority piano mood descriptors; no audio",
        "seed": seed, "limit": limit, "fresh_after": fresh_after,
        "fresh_test_n": baseline["fresh_heldout_test_size"],
        "split_sizes": baseline["split_sizes"],
        "variants": [name for name, _ in VARIANTS],
        "scores": metrics,
        "success_rule": "Only hard-five + noncalm improvements on validation AND genuinely fresh test warrant further investigation; not a significance claim",
        "limitation": "not the published Farbood equation or empirically calibrated weights; 5 target mood labels are not directly measured felt emotions",
    }
    (out / "tension-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8")
    table = [
        "# Tension : la performance sur les humeurs DIFFICILES, pas Calm",
        "", f"- {limit} MIDI analysés, dont {summary['fresh_test_n']} tests encore jamais vus (groupes des premiers {fresh_after} exclus).",
        f"- {baseline['split_sizes']} ; aucun rejet : {all(not x['rejected'] for x in outcomes.values())}.",
        "- **Cible primaire fixée d'avance** : Mysterious, Epic, Tense, Dark, Happy,",
        "  cinq dernières AP de validation sur l'expérience précédente (1400 MIDI).",
        "- Seconde mesure : les 14 étiquettes sans Emotional ni Relaxing/Calm.",
        "- Une troisième moyenne incluant Calm n'est présentée que pour détecter les illusions de progrès.",
        "- Tous les modèles gardent le même découpage et le même classificateur ;",
        "  toutes les variantes étaient définies avant de mesurer le nouveau test.",
        "", "| Variante | Hard 5 validation | Hard 5 test nouveau | Noncalm 14 test nouveau | Avec Calm test nouveau (diagnostic) |",
        "|---|---:|---:|---:|---:|",
    ]
    def fmt(value):
        return f"{value:.3f}" if value is not None else "—"
    for name, caption in VARIANTS:
        v = metrics[name]
        hard_val = v["validation"]["hard_five"]
        hard = v["fresh_test"]["hard_five"]
        noncalm = v["fresh_test"]["all_noncalm"]
        all_named = v["fresh_test"]["all_named_including_calm"]
        table.append("| " + caption + " | " + " | ".join(
            fmt(x) for x in (
                hard_val["mean_ap"], hard["mean_ap"], noncalm["mean_ap"],
                all_named["mean_average_precision"])) + " |")
    table += ["", "## Cinq humeurs-cibles, sur le nouveau test", "",
              "| Humeur | Nombre de positifs | H1 AP | Tension AP | Surprise + tension AP |",
              "|---|---:|---:|---:|---:|"]
    for mood in HARD_MOODS:
        target = metrics["research_cues"]["fresh_test"]["hard_five"]
        table.append("| " + mood + " | " + str(target["positive_counts"][mood]) +
                     " | " + " | ".join(fmt(metrics[name]["fresh_test"]["hard_five"]
                     ["ap_by_mood"][mood]) for name in
                     ("research_cues", "research_tension", "research_surprise_tension")) + " |")
    table += ["", "**Garde-fous :** ne pas confondre AP et taux de bonnes réponses ;",
              "vérifier le contrôle temporel mélangé ; ne pas annoncer de victoire",
              "si un gain vient seulement de Calm, si la validation se dégrade,",
              "ou si les cinq humeurs sont trop rares pour être évaluées.",
              "Ces résultats ne prouvent ni causalité ni émotion ressentie.", ""]
    (out / "tension-summary.md").write_text("\n".join(table), encoding="utf-8")
    return summary


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("directory", type=Path)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--limit", type=int, default=1900)
    p.add_argument("--fresh-after", type=int, default=1400)
    args = p.parse_args()
    outcome = experiment(args.directory, args.out, limit=args.limit,
                         fresh_after=args.fresh_after)
    print((args.out / "tension-summary.md").read_text(encoding="utf-8"))
    print("Splits:", outcome["split_sizes"])


if __name__ == "__main__":
    main()
