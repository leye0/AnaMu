"""Exploratory PIAST-AT tonal-trajectory ablation, MIDI only.

IMPORTANT: all 1900 precisely paired PIAST MIDI have been evaluated in prior
work. Results on any of their existing split(s) are hypothesis-generating,
NOT a newly held-out confirmation. Separate test tags from train fitting.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from anamu.research_contracts import check_registered_experiment

from .piast_at_benchmark import run
from .piast_tension_experiment import HARD_MOODS, NONCALM_MOODS, focus_stats


ARMS = {
    "research_cues": "H1: published mode profiles, tempo and articulation",
    "research_tonal_motion": "H1 + temporal local-key/mode uncertainty hypothesis",
    "research_tonal_motion_shuffled": "H1 + same local-key windows in random order",
}


def validation_only_selection(scores: dict, moods: tuple[str, ...] = HARD_MOODS) -> dict:
    """Choose each mood's arm exclusively from validation average precision.

    The chosen arm may then be evaluated on test *without* touching test tags
    during selection. Macro comparisons are reported without pooling easy Calm.
    """
    chosen = {}
    for mood in moods:
        arm = max(ARMS, key=lambda name:
                  scores[name]["validation"]["hard_five"]["ap_by_mood"][mood])
        chosen[mood] = {
            "arm_selected_by_validation": arm,
            "validation_ap": scores[arm]["validation"]["hard_five"]["ap_by_mood"][mood],
            "test_ap": scores[arm]["test"]["hard_five"]["ap_by_mood"][mood],
            "former_subset_ap": scores[arm]["fresh_test"]["hard_five"]["ap_by_mood"][mood],
        }
    return {
        "choices": chosen,
        "test_macro_average_precision": sum(v["test_ap"] for v in chosen.values()) / len(chosen),
        "test_reference_macro_average_precision": sum(
            scores["research_cues"]["test"]["hard_five"]["ap_by_mood"][m]
            for m in moods) / len(moods),
        "former_subset_macro_average_precision": sum(
            v["former_subset_ap"] for v in chosen.values()) / len(chosen),
        "former_subset_reference_macro_average_precision": sum(
            scores["research_cues"]["fresh_test"]["hard_five"]["ap_by_mood"][m]
            for m in moods) / len(moods),
        "selection_does_not_use_test_labels": True,
        "warning": "selection is unbiased per run but researcher has already examined this test in prior runs",
    }


def experiment(root: Path, output: Path, *, limit: int = 1900) -> dict:
    if limit != 1900:
        raise ValueError("requires_identical_1900_previously_examined_cohort")
    output.mkdir(parents=True, exist_ok=True)
    results = {}
    for arm in ARMS:
        print("start", arm, flush=True)
        item = run(root, feature_set=arm, cache_dir=output / "cache", limit=limit,
                   fresh_after=1400)
        (output / (arm + ".json")).write_text(
            json.dumps(item, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
            encoding="utf-8")
        results[arm] = item
    base = results["research_cues"]
    if base["local_matched_midis"] != limit:
        raise ValueError("incomplete_piast_dataset")
    for name, item in results.items():
        if (item["split_sizes"] != base["split_sizes"] or
                item["split_source_groups"] != base["split_source_groups"] or
                item["accepted"] != limit or item["rejected"]):
            raise AssertionError(f"unfair_or_incomplete_comparison:{name}")
    scores = {name: {split: {
        "hard_five": focus_stats(item[split], HARD_MOODS),
        "noncalm_fourteen": focus_stats(item[split], NONCALM_MOODS),
        "all_named_diagnostic": item[split]["named_moods"],
    } for split in ("validation", "test", "fresh_test")}
        for name, item in results.items()}
    summary = {
        "study": "Tonal trajectory and key ambiguity, inspired by Xia et al. AAAI 2026",
        "not_authors_algorithm": "NOT MoFi, no MIDIBERT nor published neural weights",
        "inputs": "MIDI only, human expert PIAST mood labels used only for training/evaluation",
        "cohort": "1900/1900 matched MIDI, ALL previously seen in earlier experiments",
        "independent_new_test": False,
        "arms": ARMS,
        "split_sizes": base["split_sizes"],
        "old_fresh_group_split": "former 78 examples outside initial 1400, but ALREADY EXAMINED",
        "hypothesis": "Mode/tonic/entropy movement contains emotion information beyond clip-mean mode fit",
        "negative_control": "reorder eight tonal windows, preserving each clip's tonal distribution",
        "priority_moods": list(HARD_MOODS),
        "scores": scores,
        "validation_only_arm_selection": validation_only_selection(scores),
        "caveats": [
            "Exploratory, post-existing-test; no hypothesis can be accepted as externally confirmed",
            "Tonal key profiles based on 1982 perceptual hierarchy, not actual composer key labels",
            "Local key entropy is a proxy from correlations, not listener uncertainty",
            "Time division is eight equal clip windows, not scored measures or analyst voices",
            "Negative control retains distributional tonal information and tests only temporal order",
            "No audio is processed; labels reflect expert tag-majority, not felt emotion",
        ],
    }
    (output / "tonal-motion-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8")
    lines = ["# Mode et tonalité dans le temps : résultats exploratoires",
             "", "**Attention : 1900 MIDI déjà examinés. Aucune cohorte neuve.**", "",
             "| Variante | Hard 5 validation | Hard 5 ancien test (295) | Hard 5 ancien sous-test (78) | Noncalm 14 ancien test |",
             "|---|---:|---:|---:|---:|"]
    def fmt(n):
        return f"{n:.3f}" if n is not None else "—"
    for arm, description in ARMS.items():
        v = scores[arm]
        lines.append("| " + description + " | " + " | ".join(fmt(x) for x in (
            v["validation"]["hard_five"]["mean_ap"],
            v["test"]["hard_five"]["mean_ap"],
            v["fresh_test"]["hard_five"]["mean_ap"],
            v["test"]["noncalm_fourteen"]["mean_ap"],
        )) + " |")
    lines += ["", "## Détails : cinq faiblesses sur l'ancien test (295)", "",
              "| Humeur | Positifs | Référence AP | Tonalité séquentielle AP | Fenêtres mélangées AP |",
              "|---|---:|---:|---:|---:|"]
    for mood in HARD_MOODS:
        lines.append("| " + mood + " | " + str(scores["research_cues"]["test"]
                     ["hard_five"]["positive_counts"][mood]) + " | " + " | ".join(
                         fmt(scores[arm]["test"]["hard_five"]["ap_by_mood"][mood])
                         for arm in ARMS) + " |")
    selection = summary["validation_only_arm_selection"]
    lines += ["", "## Sélection exclusivement par la validation", "",
              "| Humeur | Variante choisie | AP sur le test |",
              "|---|---|---:|"]
    for mood, row in selection["choices"].items():
        lines.append(f"| {mood} | {row['arm_selected_by_validation']} | {row['test_ap']:.3f} |")
    lines += ["", f"**Macro cinq humeurs sur l'ancien test : référence "
              f"{selection['test_reference_macro_average_precision']:.3f} "
              f"→ sélection validation {selection['test_macro_average_precision']:.3f}.**",
              "", "Les résultats ne valident ni l'équation ni les modèles de l'article AAAI.",
              "Un gain sans autre corpus ou nouvel échantillon n'est pas une découverte confirmée.", ""]
    (output / "tonal-motion-summary.md").write_text("\n".join(lines), encoding="utf-8")
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    check_registered_experiment("piast_tonal_motion")
    result = experiment(args.directory, args.out)
    print((args.out / "tonal-motion-summary.md").read_text(), flush=True)
    print("split_sizes", result["split_sizes"], flush=True)


if __name__ == "__main__":
    main()
