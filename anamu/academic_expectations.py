"""Independent melodic and harmonic expectation features (train-only priors).

Two distinct viewpoints are fit only on the training compositions; they
estimate musical-event uncertainty, *not* emotional forecasts. Unlike IDyOM,
these are explicitly labelled small n-gram control models. The music-theory
event views are hypotheses, especially for polyphonic transcriptions.
"""

from __future__ import annotations

import math
import statistics
from pathlib import Path

from .academic_fusion import _notes
from .expectation import VariableOrderExpectancy


def piece_symbolic_events(path: str | Path, beats_per_measure: float,
                          n_measures: int) -> dict:
    notes, _ = _notes(path)
    if not notes:
        raise ValueError("no_notes_for_expectancy")
    onsets: dict[float, list] = {}
    for n in notes:
        onsets.setdefault(round(n[0], 5), []).append(n)
    # Upper-pitch-onset sequence is a reproducible *candidate* viewpoint,
    # NOT an assertion that the upper note is always the perceived melody.
    upper = [(t, max(group, key=lambda n: (n[2], n[3]))[2])
             for t, group in sorted(onsets.items())]
    melodic = [(t, max(-24, min(24, pitch - upper[i - 1][1])))
               for i, (t, pitch) in enumerate(upper) if i > 0]
    sonorities = []
    for bar in range(n_measures):
        # At each bar onset, use genuinely sounding notes; repeated empty
        # measures have an explicit REST token instead of silent interpolation.
        tick = bar * beats_per_measure + .02
        active = {n[2] % 12 for n in notes if n[0] <= tick < n[1]}
        if not active:
            start = bar * beats_per_measure
            active = {n[2] % 12 for n in notes if start <= n[0] < start + .25}
        label = "pc:" + "-".join(map(str, sorted(active))) if active else "REST"
        sonorities.append((bar, label))
    return {"melodic_interval": melodic, "harmonic_sonority": sonorities}


def fit_training_expectancies(sources: list[tuple[Path, float, int]],
                             *, max_order: int = 3) -> dict:
    """Fit independent priors using ONLY the train split's MIDI bytes."""
    sequences = [piece_symbolic_events(path, beats, measures)
                 for path, beats, measures in sources]
    result = {}
    for label in ("melodic_interval", "harmonic_sonority"):
        result[label] = VariableOrderExpectancy(max_order=max_order, smoothing=2.0).fit(
            [[event for _, event in source[label]] for source in sequences
             if source[label]])
    return result


def add_expectancy_observations(path: Path, rows: list[dict],
                                beats_per_measure: float, models: dict) -> dict:
    sequences = piece_symbolic_events(path, beats_per_measure, len(rows))
    families = {}
    for viewpoint, model in models.items():
        events = sequences[viewpoint]
        analyzed = model.evaluate([token for _, token in events])
        buckets = [[] for _ in rows]
        for (beat, _), expectation in zip(events, analyzed):
            idx = int(beat / beats_per_measure) if viewpoint == "melodic_interval" else beat
            if 0 <= idx < len(rows):
                buckets[idx].append(expectation)
        for row, measure_events in zip(rows, buckets):
            prefix = "ngram_" + viewpoint
            if measure_events:
                surprises = [e.surprisal_bits for e in measure_events]
                entropies = [e.entropy_bits_before for e in measure_events]
                row[prefix + ".surprisal_mean"] = statistics.mean(surprises)
                row[prefix + ".surprisal_max"] = max(surprises)
                row[prefix + ".surprisal_variability"] = (
                    statistics.pstdev(surprises) if len(surprises) > 1 else 0.)
                row[prefix + ".entropy_before_mean"] = statistics.mean(entropies)
                row[prefix + ".entropy_x_surprisal"] = statistics.mean(
                    s * h for s, h in zip(surprises, entropies))
                row[prefix + ".surprise_given_low_entropy"] = statistics.mean(
                    s / (1 + h) for s, h in zip(surprises, entropies))
                row[prefix + ".events"] = len(measure_events)
            else:
                row[prefix + ".events"] = 0
        families[viewpoint] = len(events)
    return {"status": "ok", "engine": "AnaMu variable-order ngram baseline (NOT original IDyOM)",
            "events": families, "fit_data": "train-only; piece-disjoint validation/test",
            "viewpoint_limits": "highest-onset-pitch and sounding pitch-class sets are hypotheses"}
