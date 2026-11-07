"""Human-vs-AnaMu emotion analysis on ten known piano themes held out from training.

All 200 raw MIDI and human annotations must be downloaded by
`python -m scripts.fetch_vgmidi_temporal /tmp/anamu-vgmidi` first.
No labels are passed into feature extraction. Split is piece-disjoint,
chosen by a filename-only hash *before* target labels are assembled.

Run:
  python -m scripts.vgmidi_temporal_benchmark /tmp/anamu-vgmidi \
    --json-out /tmp/vgmidi-ten.json --markdown-out /tmp/vgmidi-ten.md
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
from collections import Counter
from pathlib import Path

import numpy as np
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from anamu.vgmidi_temporal import (enrich_published_mechanisms,
                                   extract_midi_measures, load_human_pieces,
                                   select_splits)


def flat_rows(features: list[list[dict]], pieces, names: list[str]):
    rows = [r for p in features for r in p]
    matrix = np.asarray([[float(r[k]) if r.get(k) is not None and math.isfinite(r[k])
                          else np.nan for k in names] for r in rows], dtype=float)
    truth = np.asarray([[h["valence_median"], h["arousal_median"]]
                        for p in pieces for h in p.human], dtype=float)
    weight = np.asarray([1 / len(p.human) for p in pieces for _ in p.human])
    return matrix, truth, weight


def create_model(name: str):
    imputer = SimpleImputer(strategy="median", keep_empty_features=True, add_indicator=True)
    if name == "ridge_10":
        return Pipeline([("missing", imputer), ("scale", StandardScaler()),
                         ("model", Ridge(alpha=10))])
    if name == "ridge_100":
        return Pipeline([("missing", imputer), ("scale", StandardScaler()),
                         ("model", Ridge(alpha=100))])
    if name == "forest":
        return Pipeline([("missing", imputer), ("model", RandomForestRegressor(
            n_estimators=125, min_samples_leaf=12, max_features=.75,
            n_jobs=-1, random_state=20261107))])
    if name == "constant":
        return DummyRegressor(strategy="mean")
    raise ValueError(name)


def fit(model, features, truth, weights):
    kw = {"model__sample_weight": weights} if isinstance(model, Pipeline) else {"sample_weight": weights}
    model.fit(features, truth, **kw)
    return model


def predict(model, features):
    return np.clip(np.asarray(model.predict(features), dtype=float), -1, 1)


def piece_weighted_mae(targets, preds, pieces) -> dict:
    current = 0
    errors = []
    for piece in pieces:
        span = len(piece.human)
        errors.append(np.abs(targets[current:current + span] - preds[current:current + span]).mean(axis=0))
        current += span
    return {"valence": float(np.mean([e[0] for e in errors])),
            "arousal": float(np.mean([e[1] for e in errors])),
            "both": float(np.mean(errors))}


def measure_time_shape_diagnostics(piece_results: list[dict]) -> dict:
    """Within-piece Pearson: whether changing emotions follow changing music.

    This is separate from mean absolute error, which can be low for an almost
    constant output. Correlations do not prove mechanism or causality.
    """
    per_piece = []
    for piece in piece_results:
        dims = {}
        for key in ("valence", "arousal"):
            human = np.asarray([row[f"{key}_median"] for row in piece["time_series"]])
            model = np.asarray([row[f"model_{key}"] for row in piece["time_series"]])
            dims[key] = (float(np.corrcoef(human, model)[0, 1])
                         if np.std(human) > 1e-6 and np.std(model) > 1e-6 else None)
        per_piece.append({"piece": piece["piece"], **dims})
    return {
        "description": "Pearson within each held-out piece; not pooled cross-song correlation",
        "per_piece": per_piece,
        "mean_valence": float(np.mean([p["valence"] for p in per_piece if p["valence"] is not None])),
        "mean_arousal": float(np.mean([p["arousal"] for p in per_piece if p["arousal"] is not None])),
    }


def run(root: Path, *, academic: bool = True) -> dict:
    originals = load_human_pieces([root / f"vgmidi_raw_{i}.json" for i in (1, 2)])
    accepted = []
    all_features = []
    rejected = []
    engine_counts = Counter()
    for i, piece in enumerate(originals, 1):
        source = root / "midi" / piece.filename
        try:
            measures, meta = extract_midi_measures(source, piece.n_measures)
            if academic:
                sources = enrich_published_mechanisms(source, measures, meta["beats_per_measure"])
                engine_counts.update(f"{name}:{status}" for name, status in sources.items())
            accepted.append(piece)
            all_features.append(measures)
        except (OSError, ValueError, RuntimeError, IndexError, ZeroDivisionError) as exc:
            rejected.append({"midi": piece.filename, "reason": str(exc)[:160]})
        if i % 25 == 0:
            print(f"analyzed {i}/{len(originals)}, accepted {len(accepted)}", flush=True)
    # Test choice sees feature *availability* and musical identity, NEVER the
    # labels or a model result. The ten test pieces are isolated before fitting.
    split = select_splits(accepted)
    by_split = {}
    for name in ("train", "validation", "test"):
        chosen = [(p, f) for p, f in zip(accepted, all_features) if split[p.filename] == name]
        by_split[name] = ([p for p, _ in chosen], [f for _, f in chosen])
    features = sorted({key for sequence in all_features for row in sequence for key in row})
    datasets = {name: flat_rows(x, p, features) for name, (p, x) in by_split.items()}
    train_x, train_y, train_w = datasets["train"]
    val_x, val_y, val_w = datasets["validation"]
    test_x, test_y, test_w = datasets["test"]
    candidates = {}
    for name in ("constant", "ridge_10", "ridge_100", "forest"):
        model = fit(create_model(name), train_x, train_y, train_w)
        predictions = predict(model, val_x)
        candidates[name] = piece_weighted_mae(val_y, predictions, by_split["validation"][0])
    # This choice is made on validation only. A constant baseline is a
    # candidate, so if musical signals fail to help, report that explicitly.
    winner = min(candidates, key=lambda k: (candidates[k]["both"], k))
    final = fit(create_model(winner),
                np.concatenate([train_x, val_x]), np.concatenate([train_y, val_y]),
                np.concatenate([train_w, val_w]))
    predictions = predict(final, test_x)
    constant = fit(create_model("constant"),
                   np.concatenate([train_x, val_x]), np.concatenate([train_y, val_y]),
                   np.concatenate([train_w, val_w]))
    baseline_predictions = predict(constant, test_x)
    result = []
    cursor = 0
    for piece in by_split["test"][0]:
        size = len(piece.human)
        result.append({
            "piece": piece.title, "midi_source": piece.filename,
            "measures": size,
            "human_annotators_min": min(h["annotators"] for h in piece.human),
            "human_mean": [float(v) for v in test_y[cursor:cursor + size].mean(axis=0)],
            "model_mean": [float(v) for v in predictions[cursor:cursor + size].mean(axis=0)],
            "mae": [float(v) for v in np.abs(test_y[cursor:cursor + size] -
                                              predictions[cursor:cursor + size]).mean(axis=0)],
            "time_series": [{**h, "model_valence": float(predictions[cursor + i, 0]),
                             "model_arousal": float(predictions[cursor + i, 1])}
                            for i, h in enumerate(piece.human)],
        })
        cursor += size
    return {
        "status": "real_human_vs_model_emotion_estimation_by_measure",
        "dataset": "Ferreira & Whitehead VGMIDI, 200 piano pieces, 2019-2022",
        "source": "https://github.com/lucasnfe/vgmidi",
        "source_commit": "1e62f0af8c866ded8e665cefad06dc02c35cb739",
        "experiment": "internal VGMIDI song-disjoint temporal pilot; not external EMOPIA proof",
        "seed": 20261107,
        "initial_pieces": len(originals), "eligible_pieces": len(accepted),
        "rejected": rejected,
        "split": {n: {"pieces": len(p), "measure_samples": sum(len(z.human) for z in p)}
                  for n, (p, _) in by_split.items()},
        "algorithm": "trained supervised V/A regressor on existing MIDI-domain academic mechanism features",
        "model_selection": "validation-only group-averaged MAE, then refit train+validation; test exactly once",
        "selected_model": winner,
        "validation_mae_candidates": candidates,
        "test_mae": piece_weighted_mae(test_y, predictions, by_split["test"][0]),
        "test_constant_baseline_mae": piece_weighted_mae(test_y, baseline_predictions, by_split["test"][0]),
        "feature_names": features, "published_engines": dict(engine_counts),
        "human_aggregation": "median per musical measure across all valid individual 30-rater V/A series",
        "ten_held_out_pieces": result,
        "temporal_shape": measure_time_shape_diagnostics(result),
        "limitations": [
            "emotion estimates learned from other VGMIDI human ratings: not unsupervised theory-to-emotion",
            "VGMIDI self-reports are subjective; median and quartiles preserve disagreement",
            "MIDI metre and raw annotation measure grids aligned by bar count; invalid files rejected",
            "no original IDyOM Lisp or jSymbolic Java features in this bounded run",
            "no independent external EMOPIA validation, no causal inference",
            "possible stylistic similarities across different arrangements, despite filename-disjoint pieces",
        ],
    }


def markdown_report(data: dict) -> str:
    parts = [
        "# VGMIDI — émotions humaines vs analyse AnaMu sur 10 thèmes connus",
        "",
        "**Expérience exécutée**, pas un résultat simulé. AnaMu **estime les émotions",
        "exprimées dans une musique déjà composée** à partir de ses MIDI originaux ;",
        "il ne cherche pas à prévoir les notes ou les émotions futures.",
        "Les humains ont évalué valence et activation",
        "à chaque mesure. Les courbes complètes sont dans le JSON associé.",
        "« Jamais vus » signifie exclusivement *absents de l'entraînement du modèle* :",
        "il s'agit de thèmes connus de jeux vidéo, par exemple *Chrono Trigger* et *Goron City*.",
        "",
        "![Trajectoires : médianes humaines et sorties AnaMu sur dix pièces](vgmidi-temporal-ten.svg)",
        "",
        f"- Pièces téléchargées : **{data['initial_pieces']}**, éligibles : **{data['eligible_pieces']}**, "
        f"refusées : **{len(data['rejected'])}**.",
        f"- Partitions : **{data['split']['train']['pieces']}** entraînement, "
        f"**{data['split']['validation']['pieces']}** validation, "
        f"**{data['split']['test']['pieces']}** test (aucune pièce partagée).",
        f"- Modèle retenu sur la validation : **{data['selected_model']}**.",
        f"- Erreur moyenne absolue (MAE, sur échelle −1 à +1), test : "
        f"**V = {data['test_mae']['valence']:.3f}, A = {data['test_mae']['arousal']:.3f}** ; "
        f"baseline constante : V = {data['test_constant_baseline_mae']['valence']:.3f}, "
        f"A = {data['test_constant_baseline_mae']['arousal']:.3f}.",
        f"- **Forme temporelle**, corrélation intra-pièce moyenne : "
        f"**valence {data['temporal_shape']['mean_valence']:+.2f}**, "
        f"**activation {data['temporal_shape']['mean_arousal']:+.2f}** "
        "(mesure plus exigeante que la moyenne par chanson).",
        "",
        "| Morceau connu (réservé au test) | Humains V | AnaMu V | Humains A | AnaMu A | MAE V / A |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in data["ten_held_out_pieces"]:
        parts.append(f"| {row['piece']} ({row['measures']} mesures) | "
                     f"{row['human_mean'][0]:+.2f} | {row['model_mean'][0]:+.2f} | "
                     f"{row['human_mean'][1]:+.2f} | {row['model_mean'][1]:+.2f} | "
                     f"{row['mae'][0]:.2f} / {row['mae'][1]:.2f} |")
    parts += [
        "",
        "## Trajectoires temporelles (mêmes mesures, mêmes pièces)",
        "",
        "Chaque nombre est V ou A sur [−1, +1]. Voir le JSON pour **toutes** les mesures,",
        "les quartiles humains (désaccords individuels) et les sorties du modèle.",
    ]
    for piece in data["ten_held_out_pieces"]:
        samples = piece["time_series"]
        indices = sorted({0, len(samples) // 4, len(samples) // 2,
                          3 * len(samples) // 4, len(samples) - 1})
        parts += ["", f"### {piece['piece']}", "",
                  "| Mesure | Humains V | AnaMu V | Humains A | AnaMu A | N humains |",
                  "|---:|---:|---:|---:|---:|---:|"]
        for index in indices:
            s = samples[index]
            parts.append(f"| {s['measure']} | {s['valence_median']:+.2f} | "
                         f"{s['model_valence']:+.2f} | {s['arousal_median']:+.2f} | "
                         f"{s['model_arousal']:+.2f} | {s['annotators']} |")
    parts += [
        "", "## Interprétation et limites", "",
        "- **Les scores ne sont pas des émotions créées directement par Partitura ou music21.** "
        "Les deux outils produisent des caractéristiques musicales qui ont ensuite été "
        "reliées aux évaluations des humains par un modèle supervisé.",
        "- Le test est **interne à VGMIDI** ; le corpus EMOPIA est réservé à une future validation externe.",
        "- Les MIDI à mesure/tempo ambigu ont été refusés *avant* le choix des dix pièces.",
        "- Le cas échéant, la baseline constante peut battre le moteur : on le signale, "
        "sans masquer les échecs.",
        "- Les évaluations sont subjectives ; 30 personnes peuvent ne pas être d'accord, "
        "leurs quartiles sont conservés dans le JSON.",
        "- Les sorties Java jSymbolic et Lisp IDyOM ne figurent pas dans cette run ; "
        "leur intégration à cette expérience est un travail encore ouvert.",
        "- La corrélation des formes temporelles doit être examinée séparément : "
        "un bon score moyen ne signifie pas que tous les crescendos affectifs sont bien détectés.",
        "", "**Source :** [VGMIDI, Ferreira & Whitehead](https://github.com/lucasnfe/vgmidi), "
        "révision `1e62f0a`. Articles originaux : *Learning to Generate Music with Sentiment* "
        "(ISMIR 2019), Herremans & Chew (Tension Ribbons), Krumhansl–Schmuckler.", "",
    ]
    return "\n".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--json-out", type=Path, required=True)
    parser.add_argument("--markdown-out", type=Path, required=True)
    parser.add_argument("--no-published-engines", action="store_true",
                        help="fast debugging only; not the complete academic benchmark")
    parser.add_argument("--reformat-existing", action="store_true",
                        help="rebuild report/diagnostics from an already executed JSON, no re-training")
    args = parser.parse_args()
    report = (json.loads(args.json_out.read_text(encoding="utf-8"))
              if args.reformat_existing else run(args.root, academic=not args.no_published_engines))
    report["status"] = "real_human_vs_model_emotion_estimation_by_measure"
    report["temporal_shape"] = measure_time_shape_diagnostics(report["ten_held_out_pieces"])
    args.json_out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.markdown_out.write_text(markdown_report(report), encoding="utf-8")
    print(f"test={report['split']['test']['pieces']} model={report['selected_model']} "
          f"MAE={report['test_mae']} baseline={report['test_constant_baseline_mae']}")


if __name__ == "__main__":
    main()
