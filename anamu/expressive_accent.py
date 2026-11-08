"""MIDI performance gestures: register, accentuation, asynchrony, articulation.

Hu et al. (TISMIR, 2026) reported expressive timing and asynchrony effects
across >600h of piano MIDI; Delle Grazie et al. (2025/26) found intensity
variability matters for emotional expressivity. These features are our own
score-free operationalizations, NOT a reproduction of either study.

In particular, a high pitch is a *proxy* for melody, not identified voice.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import mido
import numpy as np


ACCENT_FEATURE_NAMES = (
    "pitch_velocity_correlation",
    "high_vs_low_velocity",
    "chord_dynamic_contrast",
    "chord_dynamic_irregularity",
    "high_note_lead_ms",
    "high_note_lead_absolute_ms",
    "lead_dynamic_coupling",
    "timing_dynamic_coupling",
    "articulation_ratio_dispersion",
    "articulation_short_fraction",
)


def _correlation(a: np.ndarray, b: np.ndarray) -> float:
    if len(a) < 5 or np.std(a) < 1e-9 or np.std(b) < 1e-9:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def expressive_accent_features(path: str | Path) -> dict[str, float]:
    midi = mido.MidiFile(str(path))
    if midi.type == 2:
        raise ValueError("unsupported_type2")
    tempo, seconds = 500_000, 0.0
    held: dict[tuple[int, int], list[tuple[float, int]]] = defaultdict(list)
    notes: list[tuple[float, int, float, float]] = []
    for msg in mido.merge_tracks(midi.tracks):
        seconds += mido.tick2second(msg.time, midi.ticks_per_beat, tempo)
        if msg.type == "set_tempo":
            tempo = msg.tempo
        elif msg.type in ("note_on", "note_off") and msg.channel != 9:
            key = msg.channel, msg.note
            if msg.type == "note_on" and msg.velocity > 0:
                held[key].append((seconds, msg.velocity))
            elif held[key]:
                start, velocity = held[key].pop(0)
                if seconds > start:
                    notes.append((start, msg.note, velocity / 127., seconds - start))
    if len(notes) < 12:
        raise ValueError(f"insufficient_notes:{path}")
    notes.sort()
    onsets = np.asarray([n[0] for n in notes])
    pitches = np.asarray([n[1] for n in notes], dtype=float)
    velocities = np.asarray([n[2] for n in notes])
    durations = np.asarray([n[3] for n in notes])

    # Group near-simultaneous notes into musical attacks. Limit to 80 ms for
    # piano asynchrony, which includes rolled chords and transcription jitter.
    chords = [[0]]
    for i in range(1, len(notes)):
        if onsets[i] - onsets[chords[-1][0]] <= 0.080:
            chords[-1].append(i)
        else:
            chords.append([i])
    if len(chords) < 8:
        raise ValueError(f"insufficient_distinct_attacks:{path}")
    attack_times = np.array([onsets[group[0]] for group in chords])
    attack_velocity = np.array([float(velocities[group].mean()) for group in chords])
    # Local accent: difference from nearby attacks in the same interpretation.
    contrast = []
    for index, velocity in enumerate(attack_velocity):
        neighboring = attack_velocity[max(0, index - 2):min(len(chords), index + 3)]
        contrast.append(velocity - float(np.median(neighboring)))
    contrast = np.asarray(contrast)

    lead_ms, lead_strength = [], []
    high_minus_low = []
    for group in chords:
        if len(group) < 2:
            continue
        group = np.asarray(group)
        ordering = np.argsort(pitches[group])
        high = group[ordering[-1]]
        low = group[ordering[0]]
        if pitches[high] - pitches[low] < 4:
            continue
        high_minus_low.append(float(velocities[high] - velocities[low]))
        others = group[ordering[:-1]]
        lead_ms.append(1000.0 * float(onsets[high] - np.median(onsets[others])))
        lead_strength.append(float(velocities[high]))

    # Approximate articulation as note duration / distance to next *attack*.
    # Not a replacement for score-aligned legato/staccato measurements.
    idx = np.searchsorted(attack_times, onsets + .081, side="left")
    usable = idx < len(attack_times)
    ratios = np.clip(durations[usable] /
                     np.maximum(attack_times[idx[usable]] - onsets[usable], .05), 0, 4)
    lead_ms_arr = np.asarray(lead_ms)
    return {
        "pitch_velocity_correlation": _correlation(pitches, velocities),
        "high_vs_low_velocity": float(np.mean(high_minus_low)) if high_minus_low else 0.,
        "chord_dynamic_contrast": float(np.std(contrast)),
        "chord_dynamic_irregularity": float(np.mean(np.abs(np.diff(contrast)))),
        "high_note_lead_ms": float(np.mean(lead_ms_arr)) if lead_ms else 0.,
        "high_note_lead_absolute_ms": float(np.mean(np.abs(lead_ms_arr))) if lead_ms else 0.,
        "lead_dynamic_coupling": _correlation(-lead_ms_arr, np.asarray(lead_strength)),
        "timing_dynamic_coupling": _correlation(np.diff(attack_times), attack_velocity[1:]),
        "articulation_ratio_dispersion": float(np.std(ratios)) if len(ratios) else 0.,
        "articulation_short_fraction": float(np.mean(ratios < .6)) if len(ratios) else 0.,
    }
