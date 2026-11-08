"""Hard, MIDI-only CP-WTC benchmark of *performance-induced* emotional shifts.

Uses the six interpretations of each of 48 identical Bach compositions. Each
of the 288 clips has human-perceived valence/arousal annotations, rather than
inferred emotion labels. The MIDI was automatically transcribed from commercial
recordings by the dataset's authors; this script never loads or analyzes audio.

Ching & Widmer (2026), Delta-VA, motivates within-composition centering.
The descriptors below are our deliberately small *score-free approximation*,
NOT their score-aligned Performance Codec or a claimed replication of Delta-VA.

CV blocks entire, previously unseen compositions. At evaluation, all six
performances of a held-out composition may be compared, so centering features
across the six is allowed; **held-out labels are never used to train**. All
comparison thresholds and model families are fixed before running this study.

Primary: directional correctness for within-composition performance pairs
whose annotated differences are substantial, and held-out delta R².
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path

import mido
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


PERFORMERS = ("Gould", "Gulda", "Hewitt", "Richter", "Schiff", "Tureck")
FEATURES = (
    "velocity_mean", "velocity_sd", "velocity_slope", "velocity_arc",
    "onset_density", "ioi_cv", "ioi_slope", "ioi_q90_q10",
    "note_duration_mean", "note_duration_cv", "duration_slope",
    "chord_spread_mean", "chord_spread_p90", "chord_spread_fraction",
)
MODELS = {
    "tempo_only": ("onset_density",),
    "dynamics_only": ("velocity_mean", "velocity_sd", "velocity_slope", "velocity_arc"),
    "expressivity_all": FEATURES,
}


def _coefficient_variation(values: np.ndarray) -> float:
    mean = float(np.mean(values)) if len(values) else 0.0
    return float(np.std(values) / mean) if mean > 1e-8 else 0.0


def _slope(values: np.ndarray) -> float:
    """End-versus-start mean: stable when event count differs by recording."""
    if len(values) < 4:
        return 0.0
    width = max(1, len(values) // 4)
    return float(np.mean(values[-width:]) - np.mean(values[:width]))


def midi_expression(path: Path) -> dict[str, float]:
    """MIDI-only expressive descriptors; no composer identity, pitches or mode."""
    midi = mido.MidiFile(str(path))
    if midi.type == 2:
        raise ValueError("midi_type_2_not_supported")
    tempo = 500_000
    seconds = 0.0
    held = defaultdict(list)
    notes = []
    # Work in real time, accounting for tempo metadata in any MIDI track.
    for msg in mido.merge_tracks(midi.tracks):
        seconds += mido.tick2second(msg.time, midi.ticks_per_beat, tempo)
        if msg.type == "set_tempo":
            tempo = msg.tempo
        elif msg.type in ("note_on", "note_off") and msg.channel != 9:
            key = msg.channel, msg.note
            if msg.type == "note_on" and msg.velocity > 0:
                held[key].append((seconds, msg.velocity))
            elif held[key]:
                onset, velocity = held[key].pop(0)
                if seconds > onset:
                    notes.append((onset, seconds - onset, velocity))
    if len(notes) < 10 or seconds < 2:
        raise ValueError(f"too_few_valid_notes:{path}")
    notes.sort()
    onsets = np.array([note[0] for note in notes], dtype=float)
    durations = np.array([note[1] for note in notes], dtype=float)
    velocities = np.array([note[2] for note in notes], dtype=float) / 127.0
    # Simultaneous notes are a single musical onset; transcription jitter
    # under 35ms is grouped as one chord, with intra-chord spread measured.
    chord_groups = [[float(onsets[0])]]
    for onset in onsets[1:]:
        if onset - chord_groups[-1][0] <= 0.035:
            chord_groups[-1].append(float(onset))
        else:
            chord_groups.append([float(onset)])
    chord_times = np.array([g[0] for g in chord_groups], dtype=float)
    ioi = np.diff(chord_times)
    if len(ioi) < 4:
        raise ValueError(f"too_few_unique_chord_onsets:{path}")
    spreads = np.array([max(g) - min(g) for g in chord_groups], dtype=float)
    quarter = max(1, len(velocities) // 4)
    return {
        "velocity_mean": float(np.mean(velocities)),
        "velocity_sd": float(np.std(velocities)),
        "velocity_slope": _slope(velocities),
        "velocity_arc": float(np.mean(velocities[quarter:-quarter]) - np.mean(
            np.r_[velocities[:quarter], velocities[-quarter:]]))
            if len(velocities) > 2 * quarter else 0.0,
        "onset_density": float(len(chord_times) / seconds),
        "ioi_cv": _coefficient_variation(ioi),
        "ioi_slope": _slope(ioi),
        "ioi_q90_q10": float(np.quantile(ioi, .9) - np.quantile(ioi, .1)),
        "note_duration_mean": float(np.mean(durations)),
        "note_duration_cv": _coefficient_variation(durations),
        "duration_slope": _slope(durations),
        "chord_spread_mean": float(np.mean(spreads)),
        "chord_spread_p90": float(np.quantile(spreads, .9)),
        "chord_spread_fraction": float(np.mean(spreads > .010)),
    }


def load_examples(root: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[dict]]:
    metadata_path = root / "metadata" / "metadata_annotations.csv"
    with metadata_path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 288:
        raise ValueError("expected_exactly_288_human_annotated_performances")
    seen = set()
    examples = []
    for row in rows:
        player = str(row["pianist_name"])
        piece = int(row["short_name"])
        if player not in PERFORMERS or not 1 <= piece <= 48:
            raise ValueError(f"unexpected_performer_or_piece:{player}:{piece}")
        if (player, piece) in seen:
            raise ValueError("duplicate_performance")
        seen.add((player, piece))
        path = root / "symbolic" / "midi" / player / f"{piece:02d}.midi"
        if not path.is_file():
            raise FileNotFoundError(path)
        values = midi_expression(path)
        examples.append({"piece": piece, "performer": player,
                         "mean_A": float(row["mean_A"]), "mean_V": float(row["mean_V"]),
                         **values})
    if len(seen) != 288 or len({x["piece"] for x in examples}) != 48:
        raise ValueError("incomplete_six_performers_per_composition")
    groups = np.array([x["piece"] for x in examples], dtype=int)
    x = np.array([[v[name] for name in FEATURES] for v in examples], dtype=float)
    y = np.array([[v["mean_A"], v["mean_V"]] for v in examples], dtype=float)
    if not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ValueError("nonfinite_features_or_labels")
    # Compute reference from *all six MIDI interpretations* of same piece.
    # y is centered only as target/evaluation, never used as a test predictor.
    for piece in np.unique(groups):
        mask = groups == piece
        x[mask] -= x[mask].mean(axis=0)
        y[mask] -= y[mask].mean(axis=0)
    return x, y, groups, examples


def predict_out_of_fold(x: np.ndarray, y: np.ndarray, groups: np.ndarray,
                        features: tuple[str, ...]) -> np.ndarray:
    columns = [FEATURES.index(name) for name in features]
    pred = np.zeros_like(y)
    for train, test in GroupKFold(n_splits=6).split(x, y, groups):
        assert not (set(groups[train]) & set(groups[test]))
        pipeline = make_pipeline(StandardScaler(), Ridge(alpha=20.0))
        pipeline.fit(x[train][:, columns], y[train])
        pred[test] = pipeline.predict(x[test][:, columns])
    return pred


def evaluate_pairs(y: np.ndarray, pred: np.ndarray, groups: np.ndarray) -> dict:
    # Intentionally discard near-identical annotation means: easy cases
    # and ambiguous pairwise human-label noise must not drive progress.
    dimension_specs = ((0, "arousal", 10.0), (1, "valence", 1.0))
    results = {}
    for dim, label, hard_threshold in dimension_specs:
        total = 0
        correct = 0
        total_hard = 0
        correct_hard = 0
        for piece in np.unique(groups):
            index = np.flatnonzero(groups == piece)
            for left, right in combinations(index, 2):
                difference = y[left, dim] - y[right, dim]
                estimated = pred[left, dim] - pred[right, dim]
                if difference == 0 or estimated == 0:
                    continue
                total += 1
                correct += (difference > 0) == (estimated > 0)
                if abs(difference) >= hard_threshold:
                    total_hard += 1
                    correct_hard += (difference > 0) == (estimated > 0)
        sq = float(np.sum((y[:, dim] - pred[:, dim]) ** 2))
        baseline = float(np.sum(y[:, dim] ** 2))
        results[label] = {
            "delta_r2": 1.0 - sq / baseline,
            "pair_direction_correct": int(correct),
            "pair_direction_evaluable": int(total),
            "pair_accuracy": float(correct / total) if total else None,
            "hard_minimum_absolute_difference": hard_threshold,
            "hard_direction_correct": int(correct_hard),
            "hard_direction_evaluable": int(total_hard),
            "hard_accuracy": float(correct_hard / total_hard)
                             if total_hard else None,
        }
    return results


def cluster_bootstrap_improvement(y: np.ndarray, reference: np.ndarray,
                                  experiment: np.ndarray, groups: np.ndarray,
                                  *, repetitions: int = 5_000) -> dict:
    """Resample 48 *compositions*, not correlated performance pairs."""
    rng = np.random.default_rng(20261108)
    group_ids = np.unique(groups)
    summaries = {}
    for dim, label, threshold in ((0, "arousal", 10.0), (1, "valence", 1.0)):
        # Per work: hard pair totals + correct for each model, plus squared
        # target and model errors (for centered R² improvement).
        units = np.zeros((len(group_ids), 6), dtype=float)
        for k, group in enumerate(group_ids):
            index = np.flatnonzero(groups == group)
            target = y[index, dim]
            units[k, 3] = np.sum(target ** 2)
            units[k, 4] = np.sum((target - reference[index, dim]) ** 2)
            units[k, 5] = np.sum((target - experiment[index, dim]) ** 2)
            for i, j in combinations(index, 2):
                gap = y[i, dim] - y[j, dim]
                if abs(gap) < threshold:
                    continue
                units[k, 0] += 1
                ref_gap = reference[i, dim] - reference[j, dim]
                exp_gap = experiment[i, dim] - experiment[j, dim]
                units[k, 1] += (gap > 0) == (ref_gap > 0)
                units[k, 2] += (gap > 0) == (exp_gap > 0)
        draws = rng.integers(0, len(group_ids), size=(repetitions, len(group_ids)))
        sums = units[draws].sum(axis=1)
        pair_delta = (sums[:, 2] - sums[:, 1]) / sums[:, 0]
        r2_delta = (sums[:, 4] - sums[:, 5]) / sums[:, 3]
        summaries[label] = {
            "hard_accuracy_gain_vs_tempo": float((units[:, 2].sum() - units[:, 1].sum()) /
                                                  units[:, 0].sum()),
            "hard_gain_95pct_cluster_bootstrap": [float(v) for v in np.quantile(pair_delta, [.025, .975])],
            "r2_gain_vs_tempo": float((units[:, 4].sum() - units[:, 5].sum()) /
                                       units[:, 3].sum()),
            "r2_gain_95pct_cluster_bootstrap": [float(v) for v in np.quantile(r2_delta, [.025, .975])],
        }
    return summaries


def benchmark(root: Path) -> dict:
    x, y, groups, samples = load_examples(root)
    results = {}
    predictions = {}
    for name, selection in MODELS.items():
        pred = predict_out_of_fold(x, y, groups, selection)
        predictions[name] = pred
        results[name] = {"features": selection, "evaluation": evaluate_pairs(y, pred, groups)}
    # Human pairwise disagreement makes absolute performance effects uncertain;
    # no inference that shifts are causal, or transferable to pop-music tags.
    return {
        "dataset": "CP-WTC 2026, 288 transcribed MIDI from 48 Bach pieces x 6 pianists",
        "reference": "Ching and Widmer (2026), Delta-VA (inspiration, not reproduction)",
        "human_annotations": "7652 human listener ratings; means provided by CP-WTC",
        "task": "predict relative affect of different performances of the SAME composition",
        "split": "6-fold, group by 48 compositions; each test composition unseen",
        "centering": "six-performance feature and label means computed per piece; test labels never train",
        "midi_caveat": "machine-transcribed commercial audio; transcription artifacts may influence performance cues",
        "no_easy_mood_credit": "no calm/genre class or composition mode in predictors; hard pair thresholds A>=10, V>=1",
        "performers": list(PERFORMERS),
        "composition_count": len(np.unique(groups)),
        "samples": len(samples),
        "models": results,
        "expressivity_vs_tempo_cluster_bootstrap": cluster_bootstrap_improvement(
            y, predictions["tempo_only"], predictions["expressivity_all"], groups),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset_directory", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = benchmark(args.dataset_directory)
    for name, value in report["models"].items():
        print(name)
        for label, metrics in value["evaluation"].items():
            print(" ", label, "R2", round(metrics["delta_r2"], 3),
                  "hard", metrics["hard_direction_correct"], "/",
                  metrics["hard_direction_evaluable"], "=",
                  round(metrics["hard_accuracy"], 3))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n",
                               encoding="utf-8")


if __name__ == "__main__":
    main()
