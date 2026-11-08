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
import hashlib
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
from anamu.academic_fusion import (THEORY_REGISTRY, add_multiscale_motion,
                                   add_jsymbolic_ace, mechanism_execution_audit)
from anamu.academic_expectations import (add_expectancy_observations,
                                         fit_training_expectancies)
from anamu.academic_idyom import import_original_idyom_directory
from anamu.emotion_pipeline import (extract_academic_rows, export_ridge_artifact,
                                    load_ridge_artifact, predict_ridge_artifact)
from anamu.emotion_models import GroupedTemporalRegressor
from anamu.jsymbolic_ace import read_jsymbolic_ace
from anamu.tempo_map import MidiTempoMap


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
                         ("model", Ridge(alpha=10, solver="lsqr"))])
    if name == "ridge_100":
        return Pipeline([("missing", imputer), ("scale", StandardScaler()),
                         ("model", Ridge(alpha=100, solver="lsqr"))])
    if name == "forest":
        return Pipeline([("missing", imputer), ("model", RandomForestRegressor(
            n_estimators=80, min_samples_leaf=12, max_features=.6,
            n_jobs=-1, random_state=20261107))])
    if name == "constant":
        return DummyRegressor(strategy="mean")
    if name == "grouped_temporal":
        return GroupedTemporalRegressor(global_alpha=100, local_alpha=100)
    raise ValueError(name)


def fit(model, features, truth, weights, lengths=None):
    if isinstance(model, GroupedTemporalRegressor):
        if lengths is None:
            raise ValueError("grouped_model_requires_piece_lengths")
        return model.fit(features, truth, lengths)
    kw = {"model__sample_weight": weights} if isinstance(model, Pipeline) else {"sample_weight": weights}
    model.fit(features, truth, **kw)
    return model


def predict(model, features, lengths=None):
    if isinstance(model, GroupedTemporalRegressor):
        if lengths is None:
            raise ValueError("grouped_model_requires_piece_lengths")
        values = model.predict(features, lengths)
    else:
        values = model.predict(features)
    return np.clip(np.asarray(values, dtype=float), -1, 1)


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


def fraction_estimates_inside_human_iqr(piece_results: list[dict]) -> dict:
    """Per-piece balanced coverage of the human central 50% of judgements."""
    totals = {"valence": [], "arousal": []}
    for piece in piece_results:
        for dimension in totals:
            rows = piece["time_series"]
            if rows:
                totals[dimension].append(sum(
                    row[f"{dimension}_q25"] <= row[f"model_{dimension}"] <=
                    row[f"{dimension}_q75"] for row in rows) / len(rows))
    return {key: float(np.mean(values)) if values else None
            for key, values in totals.items()}


def load_original_jsymbolic_index(directory: Path | None) -> dict:
    if directory is None:
        return {}
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    index = {}
    import hashlib
    for batch in manifest["batches"]:
        source = directory / batch["file"]
        if hashlib.sha256(source.read_bytes()).hexdigest() != batch["sha256"]:
            raise ValueError("jsymbolic_batch_sha256_mismatch")
        parsed = read_jsymbolic_ace(source, max_bytes=300_000_000,
                                    nonfinite_as_missing=True)
        for data in parsed["data_sets"]:
            name = Path(data["source_id"]).name
            if name in index:
                raise ValueError("jsymbolic_duplicate_piece")
            index[name] = data
    return index


def run(root: Path, *, academic: bool = True,
        full_fusion: bool = True, jsymbolic_dir: Path | None = None,
        idyom_dir: Path | None = None, feature_cache_dir: Path | None = None,
        split_seed: int = 20261107, model_out: Path | None = None) -> dict:
    originals = load_human_pieces([root / f"vgmidi_raw_{i}.json" for i in (1, 2)])
    accepted = []
    all_features = []
    rejected = []
    engine_counts = Counter()
    original_jsymbolic = load_original_jsymbolic_index(jsymbolic_dir)
    source_status = {}
    midi_parameters = {}
    if feature_cache_dir is not None:
        feature_cache_dir.mkdir(parents=True, exist_ok=True)
    # Code fingerprints protect source-based caches from stale algorithms. All
    # cached rows are computed from MIDI + engines; NEVER from human labels.
    repository = Path(__file__).resolve().parents[1]
    sources_fingerprint = hashlib.sha256(b"".join((repository / p).read_bytes() for p in (
        "anamu/vgmidi_temporal.py", "anamu/theory_features.py",
        "anamu/melody_toolbox.py", "anamu/academic_fusion.py",
        "anamu/tempo_map.py", "anamu/jsymbolic_ace.py",
        "anamu/emotion_pipeline.py"))).hexdigest()
    for i, piece in enumerate(originals, 1):
        source = root / "midi" / piece.filename
        try:
            # Cache only MIDI-derived engines, NOT the external Java output.
            # Adding original jSymbolic must not recompute all costly music21,
            # Partitura and melody-features columns on 200 MIDI files.
            cache_key = hashlib.sha256((piece.filename + "|" + sources_fingerprint + "|" +
                str(academic) + "|" + str(full_fusion) + "|" +
                hashlib.sha256(source.read_bytes()).hexdigest()).encode()).hexdigest()
            cache_file = feature_cache_dir / (cache_key + ".json") if feature_cache_dir else None
            if cache_file and cache_file.is_file():
                cached = json.loads(cache_file.read_text(encoding="utf-8"))
                measures, meta = cached["measures"], cached["meta"]
                source_status[piece.filename] = dict(cached["source_status"])
                engine_counts.update(cached["engine_counts"])
            else:
                counts_before = engine_counts.copy()
                measures, meta, status = extract_academic_rows(
                    source, piece.n_measures, academic=academic, full_fusion=full_fusion)
                source_status[piece.filename] = status
                if academic:
                    engine_counts.update(f"{name}:{status[name]}" for name in ("partitura", "music21")
                                         if name in status)
                if full_fusion:
                    engine_counts.update(["melody-features:" + status["melody_features"]])
                if cache_file:
                    recorded = list((engine_counts - counts_before).elements())
                    cache_file.write_text(json.dumps({"measures": measures, "meta": meta,
                            "source_status": status, "engine_counts": recorded},
                            ensure_ascii=False), encoding="utf-8")
            midi_parameters[piece.filename] = meta
            if full_fusion and piece.filename in original_jsymbolic:
                java = {"data_set_count": 1, "data_sets": [original_jsymbolic[piece.filename]]}
                result = add_jsymbolic_ace(
                    measures, java, MidiTempoMap.from_bytes(source.read_bytes()),
                    meta["beats_per_measure"])
                source_status[piece.filename]["jsymbolic"] = result["status"]
                engine_counts.update(["jSymbolic:" + result["status"]])
            accepted.append(piece)
            all_features.append(measures)
        except (OSError, ValueError, RuntimeError, IndexError, ZeroDivisionError) as exc:
            rejected.append({"midi": piece.filename, "reason": str(exc)[:160]})
        if i % 25 == 0:
            print(f"analyzed {i}/{len(originals)}, accepted {len(accepted)}", flush=True)
    # Test choice sees feature *availability* and musical identity, NEVER the
    # labels or a model result. The ten test pieces are isolated before fitting.
    split = select_splits(accepted, seed=split_seed)
    idyom_import = None
    if idyom_dir is not None:
        idyom_import = import_original_idyom_directory(
            idyom_dir, root, split,
            {piece.filename: measures for piece, measures in zip(accepted, all_features)},
            {name: meta["beats_per_measure"] for name, meta in midi_parameters.items()})
        missing = set(idyom_import["pieces_unavailable"])
        for piece in accepted:
            source_status.setdefault(piece.filename, {})["original_idyom"] = (
                "unavailable:no_source_export" if piece.filename in missing else "ok")
    if full_fusion:
        train_sources = [(root / "midi" / p.filename,
                          midi_parameters[p.filename]["beats_per_measure"], p.n_measures)
                         for p in accepted if split[p.filename] == "train"]
        models = fit_training_expectancies(train_sources)
        for piece, measures in zip(accepted, all_features):
            exp = add_expectancy_observations(root / "midi" / piece.filename, measures,
                                               midi_parameters[piece.filename]["beats_per_measure"], models)
            source_status[piece.filename]["expectancy_baseline"] = exp["status"]
            motion = add_multiscale_motion(measures)
            source_status[piece.filename]["temporal_memory_derivatives"] = (
                motion["original_signals_with_temporal_derivatives"])
    by_split = {}
    for name in ("train", "validation", "test"):
        chosen = [(p, f) for p, f in zip(accepted, all_features) if split[p.filename] == name]
        by_split[name] = ([p for p, _ in chosen], [f for _, f in chosen])
    features = sorted({key for sequence in all_features for row in sequence for key in row})
    datasets = {name: flat_rows(x, p, features) for name, (p, x) in by_split.items()}
    train_x, train_y, train_w = datasets["train"]
    val_x, val_y, val_w = datasets["validation"]
    test_x, test_y, test_w = datasets["test"]
    lengths = {split_name: [len(p.human) for p in by_split[split_name][0]]
               for split_name in ("train", "validation", "test")}
    candidates = {}
    for name in ("constant", "ridge_10", "ridge_100", "forest", "grouped_temporal"):
        model = fit(create_model(name), train_x, train_y, train_w, lengths["train"])
        predictions = predict(model, val_x, lengths["validation"])
        candidates[name] = piece_weighted_mae(val_y, predictions, by_split["validation"][0])
        print(f"validation model {name}: {candidates[name]['both']:.4f}", flush=True)
    # This choice is made on validation only. A constant baseline is a
    # candidate, so if musical signals fail to help, report that explicitly.
    winner = min(candidates, key=lambda k: (candidates[k]["both"], k))
    # Ablation is fitted and scored exclusively on train/validation. It
    # quantifies incremental information without consulting test labels.
    group_prefixes = {
        "partitura": ("partitura_",),
        "music21": ("music21_",),
        "melody_features": ("melody_",),
        "narmour": ("narmour.", "narmour_"),
        "jSymbolic": ("jsym_",),
        "theory_proxies": ("theory_",),
        "statistical_expectancy": ("ngram_",),
        "temporal_memory": ("motion_",),
    }
    ablations = {}
    if full_fusion:
        def validate_subset(keep):
            model = fit(create_model("ridge_100"), train_x[:, keep], train_y, train_w)
            return piece_weighted_mae(val_y, predict(model, val_x[:, keep]),
                                      by_split["validation"][0])
        ablations["all_features"] = validate_subset(list(range(len(features))))
        for group, prefixes in group_prefixes.items():
            selected = [i for i, name in enumerate(features) if not name.startswith(prefixes)]
            if selected and len(selected) != len(features):
                ablations["without_" + group] = validate_subset(selected)
    final = fit(create_model(winner),
                np.concatenate([train_x, val_x]), np.concatenate([train_y, val_y]),
                np.concatenate([train_w, val_w]), lengths["train"] + lengths["validation"])
    deployable = None
    if model_out is not None:
        # Every benchmark candidate remains eligible to win; the deployment
        # format is explicitly Ridge-only, so re-fit it when a forest wins.
        deployment_name = winner if winner.startswith("ridge_") else "ridge_100"
        deployment_model = (final if deployment_name == winner else fit(
            create_model(deployment_name), np.concatenate([train_x, val_x]),
            np.concatenate([train_y, val_y]), np.concatenate([train_w, val_w])))
        deployable = export_ridge_artifact(
            model_out, deployment_model, features, models if full_fusion else {},
            metadata={"training_dataset": "VGMIDI", "selection": "validation only",
                      "calibration_model": deployment_name,
                      "training_pieces": len(by_split["train"][0]) + len(by_split["validation"][0]),
                      "held_out_test_sha256": sorted(hashlib.sha256(
                          (root / "midi" / p.filename).read_bytes()).hexdigest()
                          for p in by_split["test"][0]),
                      "limits": "training MIDI and human annotation labels; not a causal emotional theory"})
        # The JSON artifact must reproduce the fitted sklearn model exactly
        # before it is promoted as a standalone inference pipeline.
        restored = load_ridge_artifact(model_out)
        artifact_predictions = predict_ridge_artifact(
            restored, [row for piece_rows in by_split["test"][1] for row in piece_rows])
        direct_predictions = predict(deployment_model, test_x, lengths["test"])
        max_delta = float(np.max(np.abs(artifact_predictions - direct_predictions)))
        if max_delta > 1e-7:
            raise ValueError(f"exported_ridge_pipeline_changes_predictions:{max_delta}")
        deployable["max_export_roundtrip_delta"] = max_delta
    predictions = predict(final, test_x, lengths["test"])
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
    feature_groups = {
        "original_partitura": [n for n in features if n.startswith("partitura_")],
        "original_music21": [n for n in features if n.startswith("music21_")],
        "original_melody_features": [n for n in features if n.startswith("melody_")],
        "original_narmour": [n for n in features if n.startswith(("narmour_", "narmour."))],
        "original_jsymbolic": [n for n in features if n.startswith("jsym_")],
        "local_theory_proxies": [n for n in features if n.startswith("theory_")],
        "train_only_expectancy": [n for n in features if n.startswith("ngram_")],
        "temporal_memory_transforms": [n for n in features if n.startswith("motion_")],
        "original_midi_baselines": [n for n in features if not n.startswith((
            "partitura_", "music21_", "melody_", "narmour.", "narmour_",
            "jsym_", "theory_", "ngram_", "motion_"))],
    }
    train_piece_count = len(by_split["train"][0])
    return {
        "status": "real_human_vs_model_emotion_estimation_by_measure",
        "dataset": "Ferreira & Whitehead VGMIDI, 200 piano pieces, 2019-2022",
        "source": "https://github.com/lucasnfe/vgmidi",
        "source_commit": "1e62f0af8c866ded8e665cefad06dc02c35cb739",
        "experiment": ("exploratory repeated VGMIDI song-disjoint temporal comparison"
                       if split_seed == 20261107 else
                       "additional preselected VGMIDI song-disjoint temporal holdout") +
                       "; not external EMOPIA proof",
        "seed": split_seed,
        "initial_pieces": len(originals), "eligible_pieces": len(accepted),
        "rejected": rejected,
        "split": {n: {"pieces": len(p), "measure_samples": sum(len(z.human) for z in p)}
                  for n, (p, _) in by_split.items()},
        "algorithm": "supervised V/A regressor on fused real engines and independently tagged theory proxies",
        "model_selection": ("validation-only group-averaged MAE, then refit train+validation; " +
            ("ten test compositions inspected in prior pilot, exploratory" if split_seed == 20261107
             else "new test compositions preselected by filename-only seed")),
        "selected_model": winner,
        "deployable_midi_pipeline": deployable,
        "validation_mae_candidates": candidates,
        "validation_ridge100_leave_one_family_out": ablations,
        "test_mae": piece_weighted_mae(test_y, predictions, by_split["test"][0]),
        "test_constant_baseline_mae": piece_weighted_mae(test_y, baseline_predictions, by_split["test"][0]),
        "feature_names": features, "published_engines": dict(engine_counts),
        "academic_fusion": full_fusion,
        "original_idyom_import": idyom_import,
        "feature_group_counts": {name: len(columns) for name, columns in feature_groups.items()},
        "theory_registry": THEORY_REGISTRY,
        "mechanism_execution_audit": mechanism_execution_audit(source_status),
        "per_piece_source_status": source_status,
        "jsymbolic_original_java_piece_count": sum(
            s.get("jsymbolic") == "ok" for s in source_status.values()),
        "melody_features_original_piece_count": sum(
            s.get("melody_features") == "ok" for s in source_status.values()),
        "notes_about_scope": [
            "jSymbolic/Melody global descriptors remain static across a piece; only window/event features vary",
            "original jSymbolic outputs loaded from SHA256-verified local ACE XML batches",
            "original IDyOM Lisp is not executed; the explicitly distinct ngram baseline uses only training MIDI",
            "theory_M7-M20 are operational probes, not replications of full cognitive models",
            f"train-only expectation prior fitted on {train_piece_count} MIDI pieces",
        ],
        "human_aggregation": "median per musical measure across all valid individual 30-rater V/A series",
        "ten_held_out_pieces": result,
        "temporal_shape": measure_time_shape_diagnostics(result),
        "within_human_interquartile_band": fraction_estimates_inside_human_iqr(result),
        "limitations": [
            "emotion estimates learned from other VGMIDI human ratings: not unsupervised theory-to-emotion",
            "VGMIDI self-reports are subjective; median and quartiles preserve disagreement",
            "MIDI metre and raw annotation measure grids aligned by bar count; invalid files rejected",
            "original IDyOM Lisp unavailable (n-gram baseline is not IDyOM)",
            "jSymbolic original Java features require a verified --jsymbolic-ace directory",
            ("same ten test compositions inspected previously; exploratory only"
             if split_seed == 20261107 else
             "new test split chosen before viewing its human label series; still internal to VGMIDI"),
            "no independent external EMOPIA validation, no causal inference",
            "possible stylistic similarities across different arrangements, despite filename-disjoint pieces",
        ],
    }


def markdown_report(data: dict, *, chart_filename: str = "vgmidi-temporal-ten.svg") -> str:
    parts = [
        "# VGMIDI — émotions humaines vs analyse AnaMu sur 10 thèmes connus",
        "",
        "**Expérience exécutée**, pas un résultat simulé. AnaMu **estime les émotions",
        "exprimées dans une musique déjà composée** à partir de ses MIDI originaux ;",
        "il ne cherche pas à prévoir les notes ou les émotions futures.",
        "Les humains ont évalué valence et activation",
        "à chaque mesure. Les courbes complètes sont dans le JSON associé.",
        "« Jamais vus » signifie exclusivement *absents de l'entraînement du modèle* :",
        "il s'agit de thèmes connus de jeux vidéo, identifiés précisément dans le tableau ci-dessous.",
        ("**Attention :** ces dix thèmes ont déjà été inspectés dans le premier pilote ;"
         if data['seed'] == 20261107 else
         "**Test additionnel :** dix autres œuvres choisies avant examen des annotations humaines ;"),
        ("cette nouvelle comparaison est **exploratoire**, pas une validation indépendante intacte."
         if data['seed'] == 20261107 else
         "ce test interne distinct ne remplace pas une validation externe sur d'autres styles."),
        "",
        f"![Trajectoires : médianes humaines et sorties AnaMu sur dix pièces]({chart_filename})",
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
        f"- Dans les **quartiles humains** à chaque mesure : "
        f"**V {data['within_human_interquartile_band']['valence']:.1%}**, "
        f"**A {data['within_human_interquartile_band']['arousal']:.1%}** "
        "(moyenne équilibrée par pièce ; ce n'est pas un test de causalité).",
        "",
        "## Sources réellement intégrées à cette exécution",
        "",
    ]
    for family, count in data.get("feature_group_counts", {}).items():
        parts.append(f"- `{family}` : **{count} colonnes** effectivement disponibles dans le schéma.")
    if data.get("mechanism_execution_audit"):
        parts.extend(["", "### Couverture des 23 mécanismes recensés", "",
                      "| Mécanisme | Exécution réelle ou approximation | Pièces couvertes |",
                      "|---|---|---:|"])
        for code, audit in data["mechanism_execution_audit"].items():
            parts.append(f"| {code} — {audit['mechanism']} | {audit['status']} : "
                         f"{audit['implementation']} | {audit['pieces_with_engine']}/"
                         f"{audit['eligible_pieces']} |")
    parts += [
        "",
        f"- Pièces traitées par le Java original jSymbolic : "
        f"**{data.get('jsymbolic_original_java_piece_count', 0)}**.",
        f"- Pièces traitées par `melody-features` original : "
        f"**{data.get('melody_features_original_piece_count', 0)}**.",
        "- Les colonnes globales ne donnent **aucune information temporelle locale** ; "
        "la comparaison mesure par mesure est possible grâce aux colonnes vraiment temporelles.",
        "- IDyOM original n'est PAS remplacé par le modèle n-gramme de contrôle. "
        "Les mécanismes cognitifs non exécutables figurent explicitement comme manquants.",
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
        "- **Les outils de théorie musicale ne produisent pas directement des émotions.** "
        "Ils produisent des caractéristiques musicales qui ont ensuite été "
        "reliées aux évaluations des humains par un modèle supervisé.",
        "- Le test est **interne à VGMIDI** ; le corpus EMOPIA est réservé à une future validation externe.",
        "- Les MIDI à mesure/tempo ambigu ont été refusés *avant* le choix des dix pièces.",
        "- Le cas échéant, la baseline constante peut battre le moteur : on le signale, "
        "sans masquer les échecs.",
        "- Les évaluations sont subjectives ; 30 personnes peuvent ne pas être d'accord, "
        "leurs quartiles sont conservés dans le JSON.",
        "- Seules les sorties Java jSymbolic effectivement présentes dans la run sont comptées. "
        "Le Lisp IDyOM original n'a pas été exécuté.",
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
    parser.add_argument("--no-full-fusion", action="store_true",
                        help="legacy 24-feature baseline, without melody, jSymbolic, theory and ngram")
    parser.add_argument("--jsymbolic-ace", type=Path,
                        help="directory of SHA256-verified original Java batches + manifest.json")
    parser.add_argument("--idyom-dat-dir", type=Path,
                        help="optional verified original IDyOM Lisp .dat output manifest directory")
    parser.add_argument("--feature-cache-dir", type=Path,
                        help="optional MIDI-only extraction cache; includes no human emotion labels")
    parser.add_argument("--model-out", type=Path,
                        help="export deployable SAFE JSON Ridge calibration + train-only ngrams")
    parser.add_argument("--split-seed", type=int, default=20261107,
                        help="filename-only split seed; select a fresh seed before viewing labels")
    parser.add_argument("--reformat-existing", action="store_true",
                        help="rebuild report/diagnostics from an already executed JSON, no re-training")
    args = parser.parse_args()
    report = (json.loads(args.json_out.read_text(encoding="utf-8"))
              if args.reformat_existing else run(args.root, academic=not args.no_published_engines,
                    full_fusion=not args.no_full_fusion, jsymbolic_dir=args.jsymbolic_ace,
                    idyom_dir=args.idyom_dat_dir, feature_cache_dir=args.feature_cache_dir,
                    split_seed=args.split_seed, model_out=args.model_out))
    report["status"] = "real_human_vs_model_emotion_estimation_by_measure"
    report["temporal_shape"] = measure_time_shape_diagnostics(report["ten_held_out_pieces"])
    report["within_human_interquartile_band"] = fraction_estimates_inside_human_iqr(
        report["ten_held_out_pieces"])
    args.json_out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.markdown_out.write_text(markdown_report(
        report, chart_filename=args.markdown_out.with_suffix(".svg").name), encoding="utf-8")
    print(f"test={report['split']['test']['pieces']} model={report['selected_model']} "
          f"MAE={report['test_mae']} baseline={report['test_constant_baseline_mae']}")


if __name__ == "__main__":
    main()
