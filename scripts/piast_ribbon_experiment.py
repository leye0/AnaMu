"""Exploratory PIAST test of original Herremans--Chew spiral-array tension.

The 1900 expert-annotated PIAST pieces were already studied repeatedly: these
5 source-video-separated folds are diagnostic, not independent confirmation.
All extracted signals come from symbolic MIDI; no audio or labels enter them.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np

from anamu.theory_features import partitura_tension
from anamu.tonal_motion import TONAL_DISTRIBUTION_FEATURE_NAMES, TONAL_MOTION_FEATURE_NAMES
from .piast_at_benchmark import run
from .piast_tonal_cv import SEED, evaluate_arms, group_bootstrap
from .piast_tension_experiment import HARD_MOODS


FIELDS = ("cloud_diameter", "cloud_momentum", "tensile_strain")
METRICS = ("mean", "std", "p90")
RIBBON_FEATURES = tuple(f"ribbon_{field}_{metric}" for field in FIELDS for metric in METRICS)
ARMS = ("baseline", "distribution", "cloud_diameter", "full_ribbons", "sham_ribbons")
WINDOW_SECONDS = 1.0
HOP_SECONDS = 0.5


def ribbon_features_from_samples(samples: list[dict]) -> dict[str, float]:
    """Fixed aggregate summaries of the *published* geometry, not mood tags."""
    if not samples:
        raise ValueError("empty_ribbon_samples")
    result = {}
    for field in FIELDS:
        signal = np.asarray([sample[field] for sample in samples], dtype=float)
        if not np.isfinite(signal).all():
            raise ValueError(f"nonfinite_ribbon:{field}")
        result[f"ribbon_{field}_mean"] = float(np.mean(signal))
        result[f"ribbon_{field}_std"] = float(np.std(signal))
        result[f"ribbon_{field}_p90"] = float(np.quantile(signal, .9))
    if set(result) != set(RIBBON_FEATURES):
        raise AssertionError("incorrect_ribbon_fields")
    return result


def build_arms(records: list[tuple], ribbons: list[dict[str, float] | None]) -> dict:
    """Same examples/order across arms; shuffle signal ownership for placebo."""
    if len(records) != len(ribbons):
        raise ValueError("unequal_ribbon_count")
    output = {arm: [] for arm in ARMS}
    distribution_names = frozenset(TONAL_DISTRIBUTION_FEATURE_NAMES)
    all_tonal_names = frozenset(TONAL_MOTION_FEATURE_NAMES)
    shuffled_indices = np.random.default_rng(SEED + 120).permutation(len(records))
    for i, (clip, features) in enumerate(records):
        base = {k: v for k, v in features.items() if k not in all_tonal_names}
        static = {k: features[k] for k in distribution_names}
        geometric = ribbons[i] if ribbons[i] is not None else {}
        sham = ribbons[int(shuffled_indices[i])]
        placebo = sham if sham is not None else {}
        output["baseline"].append((clip, base))
        output["distribution"].append((clip, {**base, **static}))
        output["cloud_diameter"].append((clip, {**base, **static, **{
            k: v for k, v in geometric.items() if k.startswith("ribbon_cloud_diameter_")}}))
        output["full_ribbons"].append((clip, {**base, **static, **geometric}))
        output["sham_ribbons"].append((clip, {**base, **static, **placebo}))
    return output


def experiment(root: Path, out: Path, *, limit: int = 1900,
               bootstrap_repetitions: int = 500) -> dict:
    if limit != 1900:
        raise ValueError("requires_exact_previously_seen_1900")
    out.mkdir(parents=True, exist_ok=True)
    source = run(root, feature_set="research_tonal_motion", cache_dir=out / "h1-cache",
                 limit=limit, extract_only=True)
    records = source["records"]
    if source["matched"] != limit or len(records) != limit or source["rejected"]:
        raise AssertionError("incomplete_piast_cohort")

    cache = out / "ribbon-cache"
    cache.mkdir(exist_ok=True)
    ribbons: list[dict[str, float] | None] = []
    failures: Counter[str] = Counter()
    example_failures = []
    engine_version = None
    for index, (clip, _) in enumerate(records, 1):
        path = cache / f"{clip.midi_name}.json"
        try:
            if path.is_file():
                record = json.loads(path.read_text(encoding="utf-8"))
            else:
                raw = partitura_tension(root / "midi" / clip.midi_name,
                                       window_seconds=WINDOW_SECONDS,
                                       hop_seconds=HOP_SECONDS)
                engine_version = raw["engine_version"]
                record = ribbon_features_from_samples(raw["samples"])
                path.write_text(json.dumps(record, allow_nan=False) + "\n", encoding="utf-8")
            if set(record) != set(RIBBON_FEATURES) or not all(
                    isinstance(v, (int, float)) and math.isfinite(v) for v in record.values()):
                raise ValueError("bad_cached_ribbon")
            ribbons.append(record)
        except (OSError, ValueError, RuntimeError, IndexError, ZeroDivisionError,
                TypeError, KeyError) as exc:
            code = type(exc).__name__ + ":" + str(exc)[:100]
            failures[code] += 1
            if len(example_failures) < 12:
                example_failures.append({"clip": clip.clip_id, "reason": code})
            ribbons.append(None)
        if index % 100 == 0:
            print(f"Partitura original geometry {index}/{limit}; missing {sum(failures.values())}",
                  flush=True)

    rows = build_arms(records, ribbons)
    evaluated, oof = evaluate_arms(rows, arms=ARMS, negative_control_arm="full_ribbons")
    bootstrap = group_bootstrap(oof, repetitions=bootstrap_repetitions,
                                baseline_arm="distribution", arms=ARMS)
    status = {
        "research_status": "exploratory; no fresh held-out labels; model and arms pre-fixed before this run",
        "new_external_confirmation": False,
        "dataset": "PIAST-AT 1900/1900 matched annotated MIDI; source videos isolated by five GroupKFold folds",
        "human_annotation": "two-of-three expert consensus descriptive mood tags; not listeners' felt emotions",
        "modality": "symbolic MIDI only, no audio",
        "mechanism": "Herremans & Chew (2016) tonal tension geometry via original Partitura implementation",
        "implementation": "partitura.musicanalysis.estimate_tonaltension",
        "engine_version": engine_version,
        "assumptions": "performance seconds; Partitura may infer global key and pitch spelling",
        "window_seconds": WINDOW_SECONDS,
        "hop_seconds": HOP_SECONDS,
        "feature_names": list(RIBBON_FEATURES),
        "feature_definitions": "per-axis mean, population standard deviation, 90th percentile of 1-s overlapping frames",
        "sham": "ribbon features assigned to unrelated clips by label-blind fixed random permutation",
        "matched": len(records),
        "ribbon_success": sum(r is not None for r in ribbons),
        "ribbon_missing": sum(r is None for r in ribbons),
        "failure_reasons": dict(failures),
        "sample_failures": example_failures,
        "arms": list(ARMS),
        "oof": evaluated["scores"],
        "diagnostics": evaluated["diagnostics"],
        "paired_video_bootstrap_delta_ap_vs_distribution": bootstrap,
        "caveats": [
            "All 1900 human tags were previously inspected; CV is not independent validation.",
            "Comparison with literature and IsoVAT 24/30 also informed post-hoc selection.",
            "Cluster bootstrap is conditional on fitted out-of-fold predictions and feature search.",
            "The performance-MIDI global-key/spelling approximation is unverified for PIAST.",
            "Missing ribbons are median-imputed, with identical song cohorts per arm.",
            "Prevalence-sensitive average precision is ranking, not accuracy or human agreement.",
        ],
    }
    (out / "ribbon-summary.json").write_text(json.dumps(
        status, ensure_ascii=False, allow_nan=False, indent=2) + "\n", encoding="utf-8")

    def fmt(value):
        return "—" if value is None else f"{value:.3f}"

    def contrast(arm, metric):
        key = "hard5_macro_ap" if metric == "hard5_macro" else "noncalm14_macro_ap"
        value = status["oof"][arm]["by_mood"]["Dark"] - status["oof"]["distribution"]["by_mood"]["Dark"] \
            if metric == "Dark" else status["oof"][arm][key] - status["oof"]["distribution"][key]
        ci = bootstrap[arm][metric]
        return f"{value:+.3f} [{fmt(ci['ci_95_low'])}, {fmt(ci['ci_95_high'])}]"

    caption = {"baseline": "H1 historique", "distribution": "H1 + distribution tonale (comparateur fort)",
               "cloud_diameter": "+ diamètre du nuage tonal", "full_ribbons": "+ trois rubans originaux",
               "sham_ribbons": "+ rubans attribués à d'autres morceaux (placebo)"}
    lines = ["# Rubans de tension originaux sur les émotions MIDI difficiles", "",
             "**Exploration post-hoc, pas une nouvelle découverte validée** : les 1 900 étiquettes PIAST ont déjà été vues.",
             "", f"MIDI traité : {len(records)}/1900 ; rubans calculés : {status['ribbon_success']}/1900 ; "
             f"manquants : {status['ribbon_missing']} ; Partitura {engine_version}.",
             "", "## Mesure réelle, au-delà de la distribution tonale", "",
             "| Variante | Tense AP | Dark AP | Mysterious AP | Epic AP | Happy AP | Hard5 mAP | Noncalm14 mAP |",
             "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for arm in ARMS:
        s = status["oof"][arm]
        lines.append("| " + caption[arm] + " | " + " | ".join(
            [fmt(s["by_mood"][m]) for m in ("Tense", "Dark", "Mysterious", "Epic", "Happy")]
            + [fmt(s["hard5_macro_ap"]), fmt(s["noncalm14_macro_ap"])]) + " |")
    lines += ["", "## Incertitude par vidéo : gains contre la distribution tonale, pas H1", "",
              "| Variante | Dark ΔAP et IC95% | Hard5 ΔmAP et IC95% | Noncalm14 ΔmAP et IC95% |",
              "|---|---:|---:|---:|"]
    for arm in ARMS:
        if arm != "distribution":
            lines.append(f"| {caption[arm]} | " + " | ".join(
                contrast(arm, metric) for metric in ("Dark", "hard5_macro", "noncalm14_macro")) + " |")
    lines += ["", "Contrôle négatif : étiquettes *Dark* mélangées à l'entraînement, "
              f"AP hors pli {fmt(status['diagnostics']['negative_control']['train_label_permutation_dark_ap'])}.",
              "", "**Interprétation** : le placebo vérifie que l'amélioration n'est pas due au seul nombre "
              "de variables. Les IC sont conditionnels aux prédictions hors pli ; un corpus humain indépendant "
              "reste indispensable avant de parler de progrès généralisable.",
              "", "Source méthodologique : Herremans & Chew, *Tension Ribbons* (2016), et "
              "Partitura `estimate_tonaltension` (mêmes axes et fenêtres que notre test IsoVAT).", ""]
    (out / "ribbon-summary.md").write_text("\n".join(lines), encoding="utf-8")
    return status


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    experiment(args.directory, args.out)
    print((args.out / "ribbon-summary.md").read_text(encoding="utf-8"), flush=True)


if __name__ == "__main__":
    main()
