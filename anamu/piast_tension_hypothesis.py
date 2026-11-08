"""Temporal tension *hypothesis* based on Farbood (2012), MIDI only.

Source: M. M. Farbood, "A Parametric, Temporal Model of Musical Tension",
Music Perception 29(4), 387-428 (2012), doi:10.1525/mp.2012.29.4.387.

The paper supports multiple musical cues, a moving attentional window and
preceding memory/trend salience. Here we test a *simplified* implementation:
equal, untrained cue weights, fixed two- and four-measure windows and a
simple trend reinforcement. These are our hypotheses, NOT original weights,
original time-domain windows or a reproduction of the published algorithm.

All observations come from pre-existing MIDI measure rows, without labels.
"""

from __future__ import annotations

import hashlib
import math
import random
import statistics


_CUES = ("vertical_interval_clash", "mean_velocity", "onset_density",
         "weak_beat_onset_fraction", "pitch_range")


def _unit(value: float, cue: str) -> float:
    """Fixed physical scale, never a dataset- or label-fitted scale."""
    x = max(0., float(value))
    if cue == "mean_velocity":
        return min(1., x / 127.)
    if cue == "pitch_range":
        return min(1., x / 48.)
    if cue == "weak_beat_onset_fraction":
        return min(1., x)
    return x / (1 + x)


def _slope(values: list[float]) -> float:
    n = len(values)
    if n < 2:
        return 0.
    center = (n - 1) / 2
    denominator = sum((i - center) ** 2 for i in range(n))
    return sum((i - center) * value for i, value in enumerate(values)) / denominator


def _longest_run(values: list[float], *, positive: bool) -> int:
    best = current = 0
    for value in values:
        if value > 1e-5 if positive else value < -1e-5:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def _trend_at(rows: list[dict], window: int) -> dict[str, float]:
    n = len(rows)
    normalized = {}
    for cue in _CUES:
        observed = []
        missing = []
        for row in rows:
            value = row.get(cue)
            if isinstance(value, (int, float)) and math.isfinite(value):
                observed.append(_unit(value, cue))
                missing.append(False)
            else:
                observed.append(0.)
                missing.append(True)
        # Missing is *not* evidence of quietness, low dissonance or a pause.
        # A cue with <3 valid measures is omitted from the temporal average.
        if sum(not item for item in missing) < 3:
            continue
        for i, absent in enumerate(missing):
            if absent:
                observed[i] = observed[i-1] if i else next(
                    (x for x, absent2 in zip(observed, missing) if not absent2), 0.)
        normalized[cue] = observed

    trends = [0.] * n
    memory_matches = 0
    weighted_windows = 0
    if normalized:
        for i in range(2 * window - 1, n):
            now = statistics.mean(
                _slope(v[i - window + 1:i + 1]) for v in normalized.values())
            before = statistics.mean(
                _slope(v[i - 2 * window + 1:i - window + 1])
                for v in normalized.values())
            aligned = abs(now) > 1e-5 and abs(before) > 1e-5 and now * before > 0
            if aligned:
                memory_matches += 1
            weighted_windows += 1
            # The *direction* and the size of change both matter. Prior trend
            # salience amplifies sustained movement, never uses emotion votes.
            trends[i] = now * (1.5 if aligned else 1.)
    cumulative = [0.]
    for trend in trends:
        cumulative.append(cumulative[-1] + trend)
    values = cumulative[1:]
    reversals = sum(a * b < -1e-10 for a, b in zip(trends, trends[1:]))
    high = -float("inf")
    drawdown = 0.
    for value in values:
        high = max(high, value)
        drawdown = max(drawdown, high - value)
    name = f"farbood_w{window}_"
    return {
        name + "rise_total_per_bar": sum(max(0., t) for t in trends) / n,
        name + "fall_total_per_bar": sum(max(0., -t) for t in trends) / n,
        name + "max_rise": max(trends),
        name + "max_fall": max(-t for t in trends),
        name + "longest_rise_fraction": _longest_run(trends, positive=True) / n,
        name + "longest_fall_fraction": _longest_run(trends, positive=False) / n,
        name + "reversal_fraction": reversals / max(1, n - 1),
        name + "memory_alignment_fraction": memory_matches / max(1, weighted_windows),
        name + "cumulative_excursion": max(values) - min(values),
        name + "peak_to_end_release": max(values) - values[-1],
        name + "max_drawdown": drawdown,
    }


def tension_trend_features(rows: list[dict], *, shuffle: bool = False,
                           group: str = "", seed: int = 20261108) -> dict[str, float]:
    """Score observed chronology or a fixed, whole-measure order control."""
    if not rows:
        raise ValueError("empty_tension_measures")
    if shuffle:
        rows = list(rows)
        digest = hashlib.sha256(f"tension-shuffle-v1|{seed}|{group}".encode()).digest()
        random.Random(int.from_bytes(digest, "big")).shuffle(rows)
    result = {}
    for window in (2, 4):
        result.update(_trend_at(rows, window))
    assert all(math.isfinite(value) for value in result.values())
    return result
