"""Independent 48-work check of score-relative expressive MIDI descriptors.

CP-WTC's 288 performer MIDIs are evaluated against HUMAN valence/arousal
ratings, separately from PercePiano where the hypotheses were developed.
Every score's six interpretations stay in the same GroupKFold fold; no audio
is read. music21 parses the provided musicXML score only. Metrics include
hard within-work human judgments (valence >=1, arousal >=10) and centered R².

This is an exploratory transfer experiment, not a validatory test of PIAST's
Dark/Epic/Mysterious categorical labels, nor an original Delta-VA reimplementation.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from music21 import converter
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from anamu.score_aligned_expression import SCORE_FEATURE_NAMES, score_aligned_features
from .cp_wtc_relative_benchmark import (
    FEATURES, cluster_bootstrap_improvement, evaluate_pairs, load_examples,
)
from .percepiano_pulse_hypothesis import center_within_score, shuffled_within_score


def score_first_eight_bars(root: Path, piece: int) -> np.ndarray:
    path = root / "symbolic" / "scores" / f"{piece:02d}.musicxml"
    symbolic = converter.parse(str(path))
    # Each file may contain the full piece; annotations cover FIRST eight bars.
    part = symbolic.parts[0]
    eighth = part.measure(9)
    if eighth is None:
        raise ValueError(f"score_missing_ninth_measure:{piece}")
    cutoff = float(eighth.offset)
    events = []
    for note in symbolic.flatten().notes:
        if float(note.offset) >= cutoff:
            continue
        pitches = note.pitches if note.isChord else [note.pitch]
        for pitch in pitches:
            # Score time in a fixed quarter-note unit, not performance time.
            # Normalize by score/performer duration in the aligner.
            events.append((float(note.offset) * .5, float(pitch.midi),
                           max(float(note.quarterLength) * .5, .005), .5))
    if len(events) < 12:
        raise ValueError(f"score_too_few_notes:{piece}")
    return np.asarray(sorted(events), dtype=float)


def fold_predict(x: np.ndarray, y: np.ndarray, groups: np.ndarray) -> np.ndarray:
    estimated = np.zeros_like(y)
    for train, test in GroupKFold(n_splits=6).split(x, y, groups):
        model = make_pipeline(StandardScaler(), Ridge(alpha=20.0))
        model.fit(x[train], y[train])
        estimated[test] = model.predict(x[test])
    return estimated


def _comparison_with_explicit_reference(y, reference, experiment, groups):
    raw = cluster_bootstrap_improvement(
        y, reference, experiment, groups, repetitions=3_000)
    return {axis: {
        "hard_accuracy_gain_vs_reference": stats["hard_accuracy_gain_vs_tempo"],
        "hard_gain_95pct_cluster_bootstrap": stats["hard_gain_95pct_cluster_bootstrap"],
        "r2_gain_vs_reference": stats["r2_gain_vs_tempo"],
        "r2_gain_95pct_cluster_bootstrap": stats["r2_gain_95pct_cluster_bootstrap"],
    } for axis, stats in raw.items()}


def benchmark(root: Path, cache: Path | None = None) -> dict:
    base, y, score_groups, examples = load_examples(root)
    stems = [f"{ex['performer']}/{int(ex['piece']):02d}" for ex in examples]
    extra = None
    diagnostics, missing_files = [], []
    if cache and cache.is_file():
        saved = json.loads(cache.read_text(encoding="utf-8"))
        if saved.get("stems") == stems and saved.get("features") == list(SCORE_FEATURE_NAMES):
            extra = np.asarray(saved["values"], dtype=float)
            diagnostics = saved.get("diagnostics", [])
            missing_files = saved.get("neutralized", [])
    if extra is None:
        score_cache = {}
        rows = []
        for ex in examples:
            piece = int(ex["piece"])
            player = ex["performer"]
            if piece not in score_cache:
                score_cache[piece] = score_first_eight_bars(root, piece)
            path = root / "symbolic" / "midi" / player / f"{piece:02d}.midi"
            try:
                values = score_aligned_features(path, score_notes=score_cache[piece])
            except ValueError as error:
                if str(error) != "unreliable_alignment_coverage":
                    raise
                missing_files.append(f"{player}/{piece:02d}")
                rows.append([None] * len(SCORE_FEATURE_NAMES))
                continue
            rows.append([values[name] for name in SCORE_FEATURE_NAMES])
            diagnostics.append(values["alignment_diagnostics"])
        extra = np.asarray(rows, dtype=float)
        if cache:
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_text(json.dumps({"stems": stems,
                                         "features": list(SCORE_FEATURE_NAMES),
                                         "values": rows,
                                         "diagnostics": diagnostics,
                                         "neutralized": missing_files},
                                        allow_nan=False) + "\n", encoding="utf-8")
    missing = np.any(~np.isfinite(extra), axis=1)
    if int(np.sum(missing)) != len(missing_files):
        raise ValueError("unexpected_missing_alignment_rows")
    for group in np.unique(score_groups):
        members = score_groups == group
        valid = members & ~missing
        if np.any(members & missing):
            mean = extra[valid].mean(axis=0) if np.any(valid) else np.zeros(
                len(SCORE_FEATURE_NAMES))
            extra[members & missing] = mean
    if not np.isfinite(extra).all():
        raise ValueError("nonfinite_score_features")
    extra = center_within_score(extra, score_groups)
    systems = {
        "original_14_features": base,
        "score_only_14_features": extra,
        "original_plus_score": np.column_stack((base, extra)),
        "shuffled_score_control": np.column_stack((
            base, shuffled_within_score(extra, score_groups, 20261108))),
    }
    predictions = {name: fold_predict(x, y, score_groups) for name, x in systems.items()}
    results = {name: evaluate_pairs(y, predicted, score_groups)
               for name, predicted in predictions.items()}
    improvements = {}
    for arm in ("score_only_14_features", "original_plus_score", "shuffled_score_control"):
        improvements[arm] = _comparison_with_explicit_reference(
            y, predictions["original_14_features"], predictions[arm], score_groups)
    actual_vs_shuffle = _comparison_with_explicit_reference(
        y, predictions["shuffled_score_control"],
        predictions["original_plus_score"], score_groups)
    # Which scores actually cause the difference? Avoid aggregate optimism
    # based on a few unusually easy compositions.
    per_work = {}
    for axis, dimension, threshold in (("arousal", 0, 10.0),
                                       ("valence", 1, 1.0)):
        work_deltas = []
        for group in np.unique(score_groups):
            ids = np.flatnonzero(score_groups == group)
            successes = [0, 0]
            hard = 0
            for i in range(len(ids)):
                for j in range(i + 1, len(ids)):
                    left, right = ids[i], ids[j]
                    truth = y[left, dimension] - y[right, dimension]
                    if abs(truth) < threshold:
                        continue
                    hard += 1
                    for arm, name in enumerate(("original_14_features",
                                                "original_plus_score")):
                        prediction = predictions[name][left, dimension] - predictions[name][right, dimension]
                        successes[arm] += int((truth > 0) == (prediction > 0))
            work_deltas.append({"work": int(group), "hard_pairs": hard,
                                "correct_baseline": successes[0],
                                "correct_augmented": successes[1],
                                "net_correct_gain": successes[1] - successes[0]})
        per_work[axis] = {
            "improved_works": sum(row["net_correct_gain"] > 0 for row in work_deltas),
            "worsened_works": sum(row["net_correct_gain"] < 0 for row in work_deltas),
            "unchanged_works": sum(row["net_correct_gain"] == 0 for row in work_deltas),
            "top_improvements": sorted(work_deltas, key=lambda row: row["net_correct_gain"],
                                       reverse=True)[:5],
            "top_regressions": sorted(work_deltas, key=lambda row: row["net_correct_gain"])[:5],
        }
    return {
        "dataset": "CP-WTC: 288 MIDI performances, 48 works x 6 performers",
        "human_labels": "original listener mean valence and arousal on audio; no audio processed here",
        "cross_validation": "six GroupKFold folds, all interpretations of entire score held out",
        "score_source": "official CP-WTC musicXML, first eight bars only",
        "score_features": list(SCORE_FEATURE_NAMES),
        "alignment_audit": {
            "valid_matches": len(diagnostics), "neutralized": missing_files,
            "median_coverage": float(np.median([d["match_fraction"] for d in diagnostics]))
                               if diagnostics else None,
        },
        "models": results,
        "improvement_vs_existing": improvements,
        "actual_score_vs_shuffled_control": actual_vs_shuffle,
        "per_work_error_attribution": per_work,
        "limitations": [
            "Valence/arousal and not PIAST difficult emotions",
            "Performance MIDI was transcribed from recordings by dataset authors",
            "Score alignment is approximate matched-pitch position, not original pyScoreParser",
            "Score families are all Bach WTC Book I, not an independent genre",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset_directory", type=Path)
    parser.add_argument("--cache", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = benchmark(args.dataset_directory, args.cache)
    print("alignments", report["alignment_audit"], flush=True)
    for name, metrics in report["models"].items():
        print(name, {axis: (round(v["hard_accuracy"], 3),
                            round(v["delta_r2"], 3)) for axis, v in metrics.items()},
              flush=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n",
                               encoding="utf-8")


if __name__ == "__main__":
    main()
