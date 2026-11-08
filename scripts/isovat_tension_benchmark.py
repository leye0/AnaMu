"""Exploratory MIDI-only tension-ranking benchmark on the *human* IsoVAT orders.

Primary sources:
  Plut et al. (2022), Table 8, DOI 10.5334/tismir.120.
  Herremans & Chew (2016), Tension Ribbons (three tonal proxies).

This compares *fixed, unfitted observables* on the ten three-piece Tension
sets. It does not train a classifier, estimate a probability of emotion, or
claim that "tension" is identical to the PIAST mood label "Tense".
The ground-truth orders are higher-perceived-tension -> lower, transcribed
from the "Aggregate G-T Order" column (not the composer's H/M/L intent).

The table was known when this diagnostic was designed, so it is exploratory,
not a blinded confirmatory experiment. No tuning on the ten sets is allowed.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import statistics
from collections import defaultdict
from itertools import permutations as all_permutations
from pathlib import Path

import mido

from anamu.theory_features import partitura_tension


# Source: Plut et al., 2022, Table 8, Aggregate G-T Order, Tension rows 1..10.
# Do not replace these with the composer's intended H-M-L sequence.
HUMAN_TENSION_ORDER = {
    1: "HML", 2: "HLM", 3: "HML", 4: "HML", 5: "HML",
    6: "LMH", 7: "MHL", 8: "MLH", 9: "MHL", 10: "HML",
}


def physical_observables(path: Path) -> dict[str, float]:
    """Untrained density, dynamics and vertical dissonance heuristics.

    Rough interval weights are deliberately coarse and *not* a psychoacoustic
    roughness simulation; SoundFont spectrum is unavailable in MIDI alone.
    """
    midi = mido.MidiFile(str(path))
    if midi.type == 2:
        raise ValueError("type_2_midi_unsupported")
    active = defaultdict(list)
    tempo = 500_000
    onset_velocities = []
    intervals: list[tuple[float, float, float, int]] = []
    seconds = 0.0
    n_onsets = 0
    # mido.merge_tracks puts simultaneous events at zero time delta; segment
    # measures use the held active pitches *before* applying later messages.
    for message in mido.merge_tracks(midi.tracks):
        delta = mido.tick2second(message.time, midi.ticks_per_beat, tempo)
        if delta > 0:
            sounding = [p for (_, p), starts in active.items() for _ in starts]
            pitch_classes = sorted({pitch % 12 for pitch in sounding})
            clashes = []
            for i, left in enumerate(pitch_classes):
                for right in pitch_classes[i+1:]:
                    interval = min((right - left) % 12, (left - right) % 12)
                    clashes.append({1: 1.0, 2: .75, 6: .95}.get(interval, 0.0))
            clash = statistics.mean(clashes) if clashes else 0.0
            intervals.append((seconds, seconds + delta, clash, len(sounding)))
            seconds += delta
        if message.type == "set_tempo":
            tempo = message.tempo
        elif message.type in ("note_on", "note_off") and message.channel != 9:
            key = message.channel, message.note
            if message.type == "note_on" and message.velocity > 0:
                active[key].append(message.velocity)
                onset_velocities.append(message.velocity)
                n_onsets += 1
            elif active[key]:
                active[key].pop(0)
    if n_onsets < 4 or seconds <= 0:
        raise ValueError("insufficient_midi_events")
    sounding = [(left, right, clash, voices) for left, right, clash, voices
                in intervals if voices > 0]
    occupied_seconds = sum(right - left for left, right, _, _ in sounding)
    if occupied_seconds <= 0:
        raise ValueError("no_sounding_segments")
    def weighted_in_range(left: float, right: float) -> float:
        occupied = [(max(0.0, min(end, right) - max(start, left)), clash)
                    for start, end, clash, _ in sounding]
        duration = sum(weight for weight, _ in occupied)
        return sum(weight * clash for weight, clash in occupied) / duration if duration else 0.0
    first = weighted_in_range(0.0, seconds * .25)
    last = weighted_in_range(seconds * .75, seconds)
    return {
        "arousal_velocity": statistics.mean(onset_velocities) / 127.0,
        "arousal_onsets_per_second": n_onsets / seconds,
        "harmonic_clash_mean": weighted_in_range(0.0, seconds),
        "harmonic_clash_end": last,
        "harmonic_clash_end_minus_start": last - first,
        "active_duration_fraction": occupied_seconds / seconds,
    }


def ribbon_observables(path: Path) -> dict[str, float]:
    ribbons = partitura_tension(path, window_seconds=1.0, hop_seconds=0.5)["samples"]
    if len(ribbons) < 3:
        raise ValueError("too_few_tension_ribbon_windows")
    result = {}
    for key in ("cloud_diameter", "cloud_momentum", "tensile_strain"):
        values = [row[key] for row in ribbons]
        result[key + "_mean"] = statistics.mean(values)
        result[key + "_end"] = statistics.mean(values[-max(1, len(values) // 4):])
    return result


def score_order(scores: dict[str, float], human: str) -> dict:
    guessed = "".join(sorted(scores, key=lambda level: (-scores[level], level)))
    ties = sum(abs(scores[left] - scores[right]) < 1e-10 for left in "HML"
               for right in "HML" if left < right)
    correct = sum(scores[human[i]] > scores[human[j]] for i in range(3)
                  for j in range(i+1, 3))
    return {"predicted": guessed, "human": human, "pairwise_correct": correct,
            "pairwise_possible": 3, "exact_order": guessed == human and ties == 0,
            "tied_pairs": ties}


def benchmark(directory: Path) -> dict:
    # Hypotheses are defined *before* seeing this experiment's outputs.
    hypotheses = ("arousal_velocity", "arousal_onsets_per_second",
                  "harmonic_clash_mean", "harmonic_clash_end",
                  "harmonic_clash_end_minus_start", "cloud_diameter_mean",
                  "cloud_diameter_end", "cloud_momentum_mean",
                  "cloud_momentum_end", "tensile_strain_mean",
                  "tensile_strain_end")
    examples = {}
    for index in HUMAN_TENSION_ORDER:
        paths = {level: directory / f"T-{index:02d}-{level}.mid" for level in "HML"}
        if any(not path.is_file() for path in paths.values()):
            raise FileNotFoundError(f"missing_isoVAT_tension_triplet_{index}")
        examples[index] = {level: {**physical_observables(path),
                                    **ribbon_observables(path)}
                           for level, path in paths.items()}
    results = {}
    for hypothesis in hypotheses:
        by_set = {}
        for index, values in examples.items():
            scores = {level: values[level][hypothesis] for level in "HML"}
            if any(not math.isfinite(value) for value in scores.values()):
                raise ValueError("nonfinite_hypothesis_score")
            by_set[index] = {**score_order(scores, HUMAN_TENSION_ORDER[index]),
                             "scores": scores}
        results[hypothesis] = {
            "exact_orders": sum(case["exact_order"] for case in by_set.values()),
            "correct_pairs": sum(case["pairwise_correct"] for case in by_set.values()),
            "possible_pairs": 30,
            "tie_pairs": sum(case["tied_pairs"] for case in by_set.values()),
            "by_set": by_set,
        }
    # Acknowledge selection among all eleven hypotheses. We permute the *same*
    # human rank order within each triplet across all feature families and
    # compare the observed best result to the null distribution of the best
    # of eleven. This handles post-hoc best-of-11 selection, not reuse of a
    # pre-existing human table or future independent replication.
    permutations = 20_000
    rng = random.Random(20261108)
    observed_max_exact = max(v["exact_orders"] for v in results.values())
    observed_max_pairs = max(v["correct_pairs"] for v in results.values())
    shuffled_max_exact_extreme = 0
    shuffled_max_pairs_extreme = 0
    orders = ["".join(p) for p in all_permutations("HML")]
    predicted = {
        name: {idx: case["predicted"] for idx, case in item["by_set"].items()}
        for name, item in results.items()
    }
    for _ in range(permutations):
        permuted = {idx: rng.choice(orders) for idx in HUMAN_TENSION_ORDER}
        max_exact = 0
        max_pairs = 0
        for name in hypotheses:
            exact = sum(predicted[name][idx] == gt for idx, gt in permuted.items())
            pair_correct = 0
            for idx, gt in permuted.items():
                order = predicted[name][idx]
                positions = {level: j for j, level in enumerate(order)}
                pair_correct += sum(positions[gt[i]] < positions[gt[j]]
                                    for i in range(3) for j in range(i+1, 3))
            max_exact = max(exact, max_exact)
            max_pairs = max(pair_correct, max_pairs)
        shuffled_max_exact_extreme += max_exact >= observed_max_exact
        shuffled_max_pairs_extreme += max_pairs >= observed_max_pairs
    return {"dataset": "IsoVAT, 30 MIDI clips, 10 tension triplets",
            "human_gt": "Plut et al. (2022), Table 8, aggregate listener orders",
            "method": "zero-shot independent MIDI observables; no fitted weights",
            "limitation": "exploratory after knowing Table 8; no independent held-out data, no significance claim",
            "chance_baseline": "exact order 1/6; expected 1.67/10 sets; each pair 1/2",
            "best_of_11_permutation": {
                "iterations": permutations,
                "max_exact": observed_max_exact,
                "max_correct_pairs": observed_max_pairs,
                "familywise_null_p_max_exact": (shuffled_max_exact_extreme + 1) / (permutations + 1),
                "familywise_null_p_max_pairs": (shuffled_max_pairs_extreme + 1) / (permutations + 1),
                "null_hypothesis": "independently uniform random human rankings in each same-piece triplet",
                "caveat": "exploratory, selection-adjusted within tested feature family, not a fresh-dataset replication",
            },
            "hypotheses": results}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("midi_tension_directory", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    results = benchmark(args.midi_tension_directory)
    summary = {name: (item["exact_orders"], item["correct_pairs"],
                      item["tie_pairs"]) for name, item in results["hypotheses"].items()}
    for name, (exact, pairs, ties) in summary.items():
        print(f"{name:37} {exact}/10 exact; {pairs}/30 pairs; {ties} tied pairs")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(results, indent=2, allow_nan=False) + "\n",
                               encoding="utf-8")


if __name__ == "__main__":
    main()
