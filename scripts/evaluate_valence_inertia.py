"""Cheap research check: temporal valence memory vs original human ratings.

Reuses already published per-measure labels/predictions. It NEVER trains on
human labels, downloads MIDI, reruns academic engines or overwrites baselines.
All comparisons here are exploratory: both ten-piece sets were inspected.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from anamu.emotion_models import causal_valence_inertia


def _correlation(human: np.ndarray, predicted: np.ndarray) -> float | None:
    if len(human) < 2 or human.std() < 1e-8 or predicted.std() < 1e-8:
        return None
    return float(np.corrcoef(human, predicted)[0, 1])


def compare(report: dict, alpha: float) -> dict:
    pieces = []
    for piece in report["ten_held_out_pieces"]:
        human = np.asarray([[r["valence_median"], r["arousal_median"]]
                            for r in piece["time_series"]], dtype=float)
        raw = np.asarray([[r["model_valence"], r["model_arousal"]]
                          for r in piece["time_series"]], dtype=float)
        if len(raw) != piece["measures"] or len(raw) < 2:
            raise ValueError(f"invalid_emotion_report_measure_grid:{piece['piece']}")
        memory = causal_valence_inertia(raw, alpha=alpha)
        pieces.append({
            "title": piece["piece"], "measures": len(raw),
            "raw_valence_mae": float(np.abs(raw[:, 0] - human[:, 0]).mean()),
            "memory_valence_mae": float(np.abs(memory[:, 0] - human[:, 0]).mean()),
            "raw_valence_temporal_correlation": _correlation(human[:, 0], raw[:, 0]),
            "memory_valence_temporal_correlation": _correlation(human[:, 0], memory[:, 0]),
            "raw_arousal_mae": float(np.abs(raw[:, 1] - human[:, 1]).mean()),
            "memory_arousal_mae": float(np.abs(memory[:, 1] - human[:, 1]).mean()),
        })
    gains = np.asarray([p["raw_valence_mae"] - p["memory_valence_mae"]
                        for p in pieces])
    bootstrap = np.random.default_rng(20261107).integers(
        0, len(gains), size=(20_000, len(gains)))
    uncertainty = np.quantile(gains[bootstrap].mean(axis=1), [.025, .975])
    return {
        "seed": report["seed"], "selected_baseline_model": report["selected_model"],
        "pieces": pieces,
        "pieces_with_positive_valence_gain": int(np.sum(gains > 0)),
        "valence_gain_piece_bootstrap_95_interval": uncertainty.tolist(),
        "macro_valence_mae_raw": float(np.mean([p["raw_valence_mae"] for p in pieces])),
        "macro_valence_mae_memory": float(np.mean([p["memory_valence_mae"] for p in pieces])),
        "macro_arousal_mae_raw": float(np.mean([p["raw_arousal_mae"] for p in pieces])),
        "macro_arousal_mae_memory": float(np.mean([p["memory_arousal_mae"] for p in pieces])),
        "macro_temporal_valence_corr_raw": float(np.mean([
            p["raw_valence_temporal_correlation"] for p in pieces
            if p["raw_valence_temporal_correlation"] is not None])),
        "macro_temporal_valence_corr_memory": float(np.mean([
            p["memory_valence_temporal_correlation"] for p in pieces
            if p["memory_valence_temporal_correlation"] is not None])),
    }


def markdown(experiment: dict) -> str:
    a, b = experiment["datasets"]
    lines = [
        "# AnaMu — mémoire temporelle de la valence : expérience exploratoire",
        "",
        "**Pas un nouveau modèle appris, ni une preuve indépendante.** Les mêmes "
        "analyses d'émotion, calculées antérieurement à partir des MIDI, "
        "sont comparées aux mêmes annotations humaines.",
        "",
        f"Hypothèse : la valence persiste d'une mesure à l'autre. "
        f"Mémoire causale fixée à `alpha={experiment['alpha']}`. "
        "L'activation reste inchangée. Il s'agit d'une hypothèse temporelle "
        "inspirée des modèles de tension à mémoire (Farbood), **pas** de "
        "leur reproduction originale.",
        "",
        "Le coefficient a été choisi en regardant le premier groupe de dix "
        "morceaux. Le deuxième groupe avait déjà été examiné lors d'une "
        "expérience antérieure : cette répétition confirme une tendance "
        "exploratoire, mais ne constitue **pas** un test indépendant vierge.",
        "",
        "| Groupe de 10 morceaux | Valence : erreur initiale | "
        "Valence : avec mémoire | Corrélation temporelle initiale → mémoire | "
        "Activation (inchangée) |",
        "|---|---:|---:|---:|---:|",
    ]
    for label, data in (("Premiers dix", a), ("Dix complémentaires", b)):
        lines.append(f"| {label} | {data['macro_valence_mae_raw']:.3f} | "
                     f"{data['macro_valence_mae_memory']:.3f} | "
                     f"{data['macro_temporal_valence_corr_raw']:+.2f} → "
                     f"{data['macro_temporal_valence_corr_memory']:+.2f} | "
                     f"{data['macro_arousal_mae_raw']:.3f} |")
    lines += ["", "**Attention : effet irrégulier entre les morceaux.** "
              "Les intervalles ci-dessous sont des intervalles bootstrap "
              "exploratoires (20 000 rééchantillonnages de morceaux) :",
              "", "| Groupe | Morceaux améliorés | Gain moyen V | "
              "Intervalle bootstrap 95 % du gain |",
              "|---|---:|---:|---:|"]
    for label, data in (("Premiers dix", a), ("Dix complémentaires", b)):
        lo, hi = data["valence_gain_piece_bootstrap_95_interval"]
        lines.append(f"| {label} | {data['pieces_with_positive_valence_gain']}/10 | "
                     f"{data['macro_valence_mae_raw'] - data['macro_valence_mae_memory']:+.3f} | "
                     f"[{lo:+.4f} ; {hi:+.4f}] |")
    lines += ["", "## Détail par morceau", "",
              "| Groupe | Morceau | Mesures | Erreur V initiale | "
              "Erreur V mémoire | Gain (positif = mieux) |",
              "|---|---|---:|---:|---:|---:|"]
    for group, data in (("Premier", a), ("Complémentaire", b)):
        for piece in data["pieces"]:
            lines.append(f"| {group} | {piece['title']} | {piece['measures']} | "
                         f"{piece['raw_valence_mae']:.3f} | "
                         f"{piece['memory_valence_mae']:.3f} | "
                         f"{piece['raw_valence_mae'] - piece['memory_valence_mae']:+.3f} |")
    lines += ["", "## Conclusion", "",
              "Cette mémoire diminue les erreurs moyennes sur les deux "
              "groupes, mais **les deux intervalles comprennent zéro**. "
              "Les gains peuvent être dus à quelques morceaux; ce n'est "
              "pas encore une amélioration statistiquement robuste ni une "
              "solution aux grandes erreurs de valence. Une vraie validation "
              "nécessitera de sélectionner "
              "l'hyperparamètre **uniquement sur les morceaux de validation**, "
              "puis de le tester une fois sur de nouveaux morceaux non inspectés.",
              ""]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--alpha", type=float, default=.2)
    parser.add_argument("--first", type=Path,
                        default=Path("reports/vgmidi-temporal-ten-full.json"))
    parser.add_argument("--second", type=Path,
                        default=Path("reports/vgmidi-temporal-ten-confirmatory.json"))
    parser.add_argument("--out", type=Path,
                        default=Path("reports/vgmidi-valence-memory-experiment.json"))
    parser.add_argument("--markdown-out", type=Path,
                        default=Path("reports/vgmidi-valence-memory-experiment.md"))
    args = parser.parse_args()
    datasets = [compare(json.loads(p.read_text(encoding="utf-8")), args.alpha)
                for p in (args.first, args.second)]
    if datasets[0]["seed"] == datasets[1]["seed"]:
        raise ValueError("expected_distinct_exploratory_group_seeds")
    experiment = {"status": "exploratory_already_inspected_sets_not_independent",
                  "alpha": args.alpha,
                  "hypothesis": "causal_valence_persistence_not_original_farbood",
                  "datasets": datasets}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(experiment, indent=2, ensure_ascii=False,
                                   allow_nan=False) + "\n", encoding="utf-8")
    args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_out.write_text(markdown(experiment), encoding="utf-8")
    print("Valence MAE original -> temporal memory:",
          [(round(x["macro_valence_mae_raw"], 3),
            round(x["macro_valence_mae_memory"], 3)) for x in datasets])


if __name__ == "__main__":
    main()
