"""Preregistered PIAST-AT MIDI surprise ablation; no tuning on held-out labels.

Run after fetching a subset (e.g. first 1400), with research_cues as reference:
  python -m scripts.piast_surprise_experiment /tmp/piast --limit 1400 \
    --fresh-after 850 --out /tmp/piast-report

The four fixed models share train/test groups and classifier settings.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .piast_at_benchmark import run


VARIANTS = (
    ("research_cues", "H1 : indices perceptifs seuls"),
    ("research_surprise", "H1 + attente conditionnelle (ordre 3)"),
    ("research_surprise_unigram", "H1 + fréquence des notes, sans ordre (ordre 0)"),
    ("research_surprise_shuffled", "H1 + attente sur notes mélangées (contrôle)"),
)


def experiment(root: Path, out: Path, *, limit: int = 1400,
               fresh_after: int = 850, seed: int = 20261108) -> dict:
    if limit <= fresh_after or fresh_after < 1:
        raise ValueError("experiment_requires_new_unexamined_pieces")
    out.mkdir(parents=True, exist_ok=True)
    outcomes = {}
    for variant, _ in VARIANTS:
        result = run(root, feature_set=variant, cache_dir=out / "feature-cache",
                     seed=seed, limit=limit, fresh_after=fresh_after)
        outcomes[variant] = result
        (out / (variant + ".json")).write_text(
            json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
            encoding="utf-8")
    baseline = outcomes["research_cues"]
    if baseline["local_matched_midis"] != limit:
        raise ValueError("incomplete_piast_cohort: expected all requested MIDI files")
    sizes = baseline["split_sizes"]
    split_groups = baseline["split_source_groups"]
    assert all(result["split_sizes"] == sizes and result["split_source_groups"] == split_groups
               and result["fresh_heldout_test_size"] == baseline["fresh_heldout_test_size"]
               for result in outcomes.values())
    metrics = {}
    for variant, _ in VARIANTS:
        result = outcomes[variant]
        metrics[variant] = {
            split: (result[split]["named_moods"] if result[split] else None)
            for split in ("validation", "test", "fresh_test")
        }
    summary = {
        "research_question": "Does conditional melodic surprise add information beyond physical cues?",
        "source": "PIAST-AT: MIDI symbolic piano, human majority-rated mood tags",
        "hypotheses": [name for name, _ in VARIANTS],
        "fixed_before_scoring": True,
        "seed": seed, "limit": limit, "previously_examined": fresh_after,
        "fresh_test_n": baseline["fresh_heldout_test_size"], "split_sizes": sizes,
        "results": metrics,
        "limits": "Mood descriptors are not measured felt emotions; sequence model is not original IDyOM; descriptive AP, not significance or causality",
    }
    (out / "surprise-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = ["# PIAST-AT : est-ce que la surprise d'une note aide ?", "",
          f"- {limit} premières pièces MIDI disponibles, {fresh_after} déjà examinées auparavant.",
          f"- {sizes}; test nouveau réellement exclu des groupes déjà vus : **{summary['fresh_test_n']}** extraits.",
          "- Les mêmes humeurs humaines, mêmes partitions entraînement/test, même classificateur.",
          "- Pour l'entraînement : calcul des surprises hors pli par groupe vidéo (aucune fuite).",
          "- Pour le test : prior appris uniquement à partir des exemples d'entraînement.",
          "- Les paramètres et les quatre variantes étaient fixés avant les scores du test.",
          "", "| Variante | Validation AP | Test AP | Nouveau test AP |",
          "|---|---:|---:|---:|"]
    for variant, label in VARIANTS:
        values = metrics[variant]
        md.append(f"| {label} | " + " | ".join(
            f"{values[s]['mean_average_precision']:.3f}" if values[s] and
            values[s]["mean_average_precision"] is not None else "—"
            for s in ("validation", "test", "fresh_test")) + " |")
    md.extend(["", "**Interprétation :** seule une amélioration de la variante d'ordre 3",
               "au-delà des deux contrôles (ordre 0 et notes mélangées) serait un signal",
               "que la succession des notes fournit de l'information supplémentaire.",
               "Une différence faible ou négative invaliderait l'intérêt pratique de",
               "cette hypothèse *dans cette expérience*.", "",
               "**Limites :** scores descriptifs; pas de test de significativité ni",
               "d'émotions ressenties par les auditeurs. Le prior est un n-gramme",
               "simplifié inspiré d'IDyOM, pas le vrai IDyOM.", ""])
    (out / "surprise-summary.md").write_text("\n".join(md), encoding="utf-8")
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=1400)
    parser.add_argument("--fresh-after", type=int, default=850)
    args = parser.parse_args()
    summary = experiment(args.directory, args.out, limit=args.limit,
                         fresh_after=args.fresh_after)
    print((args.out / "surprise-summary.md").read_text(encoding="utf-8"))
    print("Extract summary:", json.dumps(summary["split_sizes"]))


if __name__ == "__main__":
    main()
