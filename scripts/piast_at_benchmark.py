"""Reproducible, held-out MIDI-only PIAST-AT emotion/mood benchmark.

Run after ``python -m scripts.fetch_piast_at /tmp/piast-at --limit 240``:
  python -m scripts.piast_at_benchmark /tmp/piast-at \
    --json-out /tmp/piast-results.json --markdown-out /tmp/piast-results.md

This predicts **human majority-tagged piano moods**, not an objective
listener's felt emotions. No labels are passed to feature extraction.
Validation and test examples are grouped by original video identity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
import time
from collections import Counter
from pathlib import Path

import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, f1_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from anamu.emotion_pipeline import extract_academic_rows, infer_measure_count
from anamu.piast_research_cues import midi_emotion_cues
from anamu.piast_at import (MOOD_LABELS, assigned_split, available_annotations,
                            load_annotations, tag_popularity)


def summarize_measures(rows: list[dict]) -> dict[str, float]:
    """Whole-clip summaries of physical MIDI observables, with no labels."""
    features = {"n_measures": float(len(rows))}
    for key in sorted({key for row in rows for key in row}):
        vals = [(i, float(row[key])) for i, row in enumerate(rows)
                if isinstance(row.get(key), (int, float))
                and math.isfinite(float(row[key]))]
        if not vals:
            continue
        values = [value for _, value in vals]
        features[key + "__mean"] = statistics.mean(values)
        features[key + "__std"] = statistics.pstdev(values)
        features[key + "__min"] = min(values)
        features[key + "__max"] = max(values)
        if len(vals) >= 2:
            features[key + "__last_minus_first"] = vals[-1][1] - vals[0][1]
        features[key + "__observed_fraction"] = len(vals) / len(rows)
    return features


def make_matrix(records: list[tuple], features: list[str]) -> np.ndarray:
    return np.asarray([[data.get(feature, np.nan) for feature in features]
                       for _, data in records], dtype=float)


def score_labels(train: list[tuple], subset: list[tuple], features: list[str]) -> dict:
    """One fixed, class-balanced linear model per mood, with prevalence baseline."""
    if not train or not subset:
        raise ValueError("train_and_evaluation_splits_required")
    train_x = make_matrix(train, features)
    test_x = make_matrix(subset, features)
    results = {}
    for label in MOOD_LABELS:
        train_y = np.asarray([int(label in clip.mood_tags()) for clip, _ in train], dtype=int)
        test_y = np.asarray([int(label in clip.mood_tags()) for clip, _ in subset], dtype=int)
        baseline = float(train_y.mean())
        if not 0 < baseline < 1:
            predictions = np.full(len(subset), baseline, dtype=float)
            model_status = "not_trainable_single_class"
        else:
            model = Pipeline([
                ("missing", SimpleImputer(strategy="median", keep_empty_features=True,
                                           add_indicator=True)),
                ("scale", StandardScaler()),
                ("classifier", LogisticRegression(C=0.5, class_weight="balanced",
                                                   max_iter=1200, random_state=20261108)),
            ])
            model.fit(train_x, train_y)
            predictions = model.predict_proba(test_x)[:, 1]
            model_status = "trained"
        positives = int(test_y.sum())
        eligible = model_status == "trained" and 3 <= positives < len(subset)
        results[label] = {
            "status": model_status,
            "train_positives": int(train_y.sum()),
            "evaluated_positives": positives,
            "evaluated_total": len(subset),
            "train_prevalence": baseline,
            "observed_prevalence": float(test_y.mean()),
            "average_precision": float(average_precision_score(test_y, predictions))
                if eligible else None,
            "prevalence_baseline_ap": float(test_y.mean()) if eligible else None,
            "f1_fixed_threshold_0_5": float(f1_score(test_y, predictions >= 0.5,
                                                       zero_division=0)) if eligible else None,
            "eligible": eligible,
        }
    scored = [row for row in results.values() if row["eligible"]]
    # 'Emotional' is exceptionally broad, so do not count it as a named emotion.
    named = [row for label, row in results.items() if label != "Emotional" and row["eligible"]]
    def macro(items):
        return {
            "labels": len(items),
            "mean_average_precision": float(statistics.mean(x["average_precision"] for x in items))
                if items else None,
            "mean_prevalence_baseline": float(statistics.mean(x["prevalence_baseline_ap"] for x in items))
                if items else None,
        }
    return {"named_moods": macro(named), "all_moods": macro(scored), "per_mood": results}


def run(root: Path, *, feature_set: str = "basic", cache_dir: Path | None = None,
        seed: int = 20261108, limit: int = 0, fresh_after: int = 0) -> dict:
    if feature_set not in {"basic", "academic", "full",
                           "research_cues", "research_interactions"}:
        raise ValueError("unsupported_feature_set")
    if limit < 0 or fresh_after < 0:
        raise ValueError("invalid_limit")
    clips = load_annotations(root / "at_text.csv")
    available = available_annotations(clips, {p.name for p in (root / "midi").glob("*.mid")})
    available = sorted(available, key=lambda c: hashlib.sha256(
        f"{seed}|{c.clip_id}".encode()).hexdigest())
    if limit:
        available = available[:limit]
    previously_examined_groups = {clip.song_group for clip in available[:fresh_after]}
    rejected = []
    extracted = []
    academic = feature_set in ("academic", "full")
    full_fusion = feature_set == "full"
    start = time.monotonic()
    if cache_dir:
        cache_dir.mkdir(parents=True, exist_ok=True)
    for index, clip in enumerate(available, 1):
        path = root / "midi" / clip.midi_name
        key = hashlib.sha256(("piast-v1|" + feature_set + "|" +
                              hashlib.sha256(path.read_bytes()).hexdigest()).encode()).hexdigest()
        cache_file = cache_dir / (key + ".json") if cache_dir else None
        try:
            if cache_file and cache_file.exists():
                features = json.loads(cache_file.read_text(encoding="utf-8"))
            else:
                n = infer_measure_count(path)
                rows, _, _ = extract_academic_rows(path, n,
                                                    academic=academic, full_fusion=full_fusion)
                features = summarize_measures(rows)
                if feature_set in {"research_cues", "research_interactions"}:
                    features.update(midi_emotion_cues(
                        path, interactions=(feature_set == "research_interactions")))
                if cache_file:
                    cache_file.write_text(json.dumps(features, allow_nan=False),
                                          encoding="utf-8")
            extracted.append((clip, features))
        except (OSError, ValueError, RuntimeError, IndexError, ZeroDivisionError,
                TypeError) as exc:
            rejected.append({"clip": clip.clip_id, "reason": str(exc)[:140]})
        if index % 30 == 0 or index == len(available):
            print(f"PIAST extraction {index}/{len(available)}, accepted {len(extracted)}, "
                  f"rejected {len(rejected)}", flush=True)
    splits = {name: [(clip, row) for clip, row in extracted
                     if assigned_split(clip, seed=seed) == name]
              for name in ("train", "validation", "test")}
    for name, records in splits.items():
        if not records:
            raise ValueError(f"empty_{name}_split")
    feature_names = sorted({key for _, row in splits["train"] for key in row})
    validation = score_labels(splits["train"], splits["validation"], feature_names)
    # No algorithm, features, threshold or hyperparameter is tuned on test.
    test = score_labels(splits["train"], splits["test"], feature_names)
    fresh_records = [(clip, data) for clip, data in splits["test"]
                     if clip.song_group not in previously_examined_groups]
    fresh_test = score_labels(splits["train"], fresh_records, feature_names) \
        if fresh_after and fresh_records else None
    split_groups = {name: {clip.song_group for clip, _ in records}
                    for name, records in splits.items()}
    assert all(split_groups[a].isdisjoint(split_groups[b]) for a, b in
               (("train", "validation"), ("train", "test"), ("validation", "test")))
    return {
        "dataset": "PIAST-AT", "source": "Hayeonbang/PIAST",
        "annotation_kind": "piano mood descriptors, not listeners' felt emotions",
        "input": "symbolic MIDI only, no recorded audio",
        "consensus": "at least two of three expert annotators",
        "feature_set": feature_set,
        "model": "fixed class-balanced logistic regression per tag (C=0.5)",
        "fixed_decision_threshold": 0.5,
        "split_policy": "deterministic source-video-disjoint 70/15/15; no label stratification",
        "annotated": len(clips), "local_matched_midis": len(available),
        "requested_analysis_limit": limit,
        "previously_examined_pilot_count": fresh_after,
        "fresh_heldout_test_size": len(fresh_records) if fresh_after else None,
        "accepted": len(extracted), "rejected": rejected,
        "split_sizes": {key: len(records) for key, records in splits.items()},
        "split_source_groups": {key: len(groups) for key, groups in split_groups.items()},
        "feature_count": len(feature_names), "feature_names": feature_names,
        "mood_popularity": tag_popularity(clips),
        "validation": validation, "test": test, "fresh_test": fresh_test,
        "elapsed_seconds": round(time.monotonic() - start, 2),
        "limitations": [
            "Échantillon prélevé par hachage ; certaines humeurs rares ont trop peu d'exemples dans le test.",
            "Associations musique/humeur, pas preuve d'émotion réellement ressentie ou causée.",
            "Domaine limité au piano solo ; aucun audio analysé, transfert à d'autres styles non démontré.",
            "Les MIDI de structure irrégulière peuvent être refusés ; refus et couverture sont déclarés.",
            "Le terme générique 'Emotional' est exclu de la moyenne des humeurs nommées.",
            "Validation et test restent séparés ; aucune sélection ni réglage sur les labels de test.",
        ],
    }


def as_markdown(result: dict) -> str:
    result_lines = [
        "# PIAST-AT — premier banc MIDI → humeurs humaines",
        "",
        f"- Corpus : {result['annotated']} extraits annotés ; "
        f"{result['local_matched_midis']} MIDI locaux ; "
        f"{result['accepted']} analysés, {len(result['rejected'])} rejetés.",
        "- Cibles : **humeurs/traits de perception**, pas émotions ressenties ; "
        "accord de **2 experts sur 3**.",
        "- Entrée : uniquement MIDI. Classes genre/style exclues des cibles.",
        f"- Découpage : {result['split_sizes']} ; sans chanson/vidéo partagée.",
        f"- Observations : {result['feature_count']} résumés MIDI ; "
        f"variante `{result['feature_set']}`.",
        "",
        "## Validation et test séparés",
        "",
        "| Échantillon | Humeurs évaluables | AP moyenne du classement | Référence de fréquence |",
        "|---|---:|---:|---:|",
    ]
    for split in ("validation", "test", "fresh_test"):
        if result[split] is None:
            continue
        for kind in ("named_moods", "all_moods"):
            row = result[split][kind]
            fmt = lambda v: "—" if v is None else f"{v:.3f}"
            result_lines.append(f"| {split} / {kind} | {row['labels']} | "
                                f"{fmt(row['mean_average_precision'])} | "
                                f"{fmt(row['mean_prevalence_baseline'])} |")
    result_lines.extend([
        "", "## Détail du test (majorité des experts)", "",
        "| Terme | Exemples positifs test | AP modèle | AP hasard | F1 (seuil 0,5) |",
        "|---|---:|---:|---:|---:|",
    ])
    for label, row in sorted(result["test"]["per_mood"].items()):
        fmt = lambda v: "—" if v is None else f"{v:.3f}"
        result_lines.append(f"| {label} | {row['evaluated_positives']} | "
                            f"{fmt(row['average_precision'])} | "
                            f"{fmt(row['prevalence_baseline_ap'])} | "
                            f"{fmt(row['f1_fixed_threshold_0_5'])} |")
    result_lines.extend([
        "", "## Popularité des humeurs dans les 2 023 annotations", "",
        "| Terme | Cité par ≥1 expert | Accord ≥2 experts |",
        "|---|---:|---:|",
    ])
    for row in result["mood_popularity"][:10]:
        result_lines.append(f"| {row['tag']} | {row['clips_with_tag']} | "
                            f"{row['majority_clips']} |")
    result_lines.extend([
        "", "## Limites", "",
        *[f"- {item}" for item in result["limitations"]],
        "", f"Extraction et mesures : {result['elapsed_seconds']} s.", "",
    ])
    return "\n".join(result_lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--feature-set", choices=("basic", "academic", "full",
                                                   "research_cues", "research_interactions"),
                        default="basic")
    parser.add_argument("--cache-dir", type=Path)
    parser.add_argument("--seed", type=int, default=20261108)
    parser.add_argument("--limit", type=int, default=0,
                        help="Analyze only first N deterministically sampled available MIDIs")
    parser.add_argument("--fresh-after", type=int, default=0,
                        help="Report a separate test score excluding first N earlier-examined clips")
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--markdown-out", type=Path)
    args = parser.parse_args()
    outcome = run(args.directory, feature_set=args.feature_set,
                  cache_dir=args.cache_dir, seed=args.seed, limit=args.limit,
                  fresh_after=args.fresh_after)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(outcome, indent=2, ensure_ascii=False,
                                            allow_nan=False) + "\n", encoding="utf-8")
    if args.markdown_out:
        args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_out.write_text(as_markdown(outcome), encoding="utf-8")
    print(as_markdown(outcome))


if __name__ == "__main__":
    main()
