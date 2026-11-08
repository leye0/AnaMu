"""Score-free MIDI pulse/expectancy probes, not a ground-truth meter decoder.

Research motivation: hierarchical temporal expectation affects perceived
tension (Cognitive Neurodynamics, 2024). Since some performance MIDI files
contain default 4/4 metadata even for 3/4 scores, we infer approximate pulse
strength from note onsets. No false claims of beat/downbeat identification.
"""

from __future__ import annotations

import math
from collections import Counter
from pathlib import Path

import mido
import numpy as np


PULSE_FEATURE_NAMES = (
    "accent_autocorr_1", "accent_autocorr_2", "accent_autocorr_3",
    "pulse_phase_concentration", "pulse_phase_entropy",
    "event_accent_lag1", "event_accent_lag2",
    "ioi_transition_entropy", "ioi_high_surprisal",
)


def _corr(values: np.ndarray, lag: int) -> float:
    if len(values) <= lag + 2 or np.std(values) < 1e-9:
        return 0.0
    a = values[:-lag]
    b = values[lag:]
    if np.std(a) < 1e-9 or np.std(b) < 1e-9:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def _entropy(counts: np.ndarray) -> float:
    s = float(np.sum(counts))
    if s <= 0:
        return 0.0
    p = counts[counts > 0] / s
    return float(-np.sum(p * np.log2(p)))


def expressive_pulse_features(midi_path: str | Path) -> dict[str, float]:
    """Extract beat-period *proxies* from actual MIDI performance timing.

    Tempo changes are handled in seconds; time-signature meta-events are
    deliberately ignored because they can be incorrect in PercePiano.
    """
    midi = mido.MidiFile(str(midi_path))
    if midi.type == 2:
        raise ValueError("unsupported_type_2")
    now = 0.0
    tempo = 500_000
    attacks = []
    for msg in mido.merge_tracks(midi.tracks):
        now += mido.tick2second(msg.time, midi.ticks_per_beat, tempo)
        if msg.type == "set_tempo":
            tempo = msg.tempo
        elif msg.type == "note_on" and msg.velocity > 0 and msg.channel != 9:
            attacks.append((now, msg.velocity / 127.0))
    if len(attacks) < 12 or now < 2:
        raise ValueError(f"insufficient_rhythmic_events:{midi_path}")
    attacks.sort()
    grouped = [[attacks[0]]]
    for onset, intensity in attacks[1:]:
        if onset - grouped[-1][0][0] < 0.035:
            grouped[-1].append((onset, intensity))
        else:
            grouped.append([(onset, intensity)])
    if len(grouped) < 7:
        raise ValueError(f"too_few_chord_attacks:{midi_path}")
    onsets = np.array([g[0][0] for g in grouped])
    strengths = np.array([np.mean([v for _, v in g]) for g in grouped])

    # Use 50ms bins, but avoid O(N²) correlation for longer excerpts.
    step = 0.05
    n = min(16000, int(now / step) + 2)
    signal = np.zeros(n, dtype=float)
    indices = np.clip((onsets / step).astype(int), 0, n - 1)
    np.add.at(signal, indices, strengths)
    signal -= float(np.mean(signal))
    fft_length = 1 << ((2 * n - 1).bit_length())
    spectrum = np.fft.rfft(signal, n=fft_length)
    autocorr = np.fft.irfft(spectrum * np.conjugate(spectrum), n=fft_length)[:n]
    denom = float(autocorr[0])
    if denom <= 1e-9:
        raise ValueError("flat_onset_signal")
    autocorr /= denom
    # Physically plausible pulse: 0.30..1.10 seconds. This is NOT proof of
    # the true score's beat period; accompaniment subdivisions may dominate.
    left = 6
    right = min(n - 1, 22)
    if left > right:
        raise ValueError("clip_shorter_than_pulse_window")
    lag = int(left + np.argmax(autocorr[left:right + 1]))
    pulse_seconds = lag * step

    phase = ((onsets - onsets[0]) / pulse_seconds) % 1
    bins = np.floor(phase * 8).astype(int) % 8
    phase_weights = np.bincount(bins, weights=strengths, minlength=8).astype(float)
    concentration = abs(np.sum(strengths * np.exp(2j * np.pi * phase))) / np.sum(strengths)
    phase_entropy = _entropy(phase_weights) / math.log2(8)

    ioi = np.diff(onsets)
    # Coarse proportional rhythm categories, scaled to dominant pulse. These
    # are within-piece transitions, not IDyOM trained on a human repertoire.
    classes = np.clip(np.rint(ioi / pulse_seconds * 4).astype(int), 1, 24)
    unigram = Counter(int(v) for v in classes)
    pairs = Counter((int(a), int(b)) for a, b in zip(classes[:-1], classes[1:]))
    possibilities = len(unigram)
    outgoing = Counter(int(v) for v in classes[:-1])
    entropy_terms = []
    surprisals = []
    for previous, following in zip(classes[:-1], classes[1:]):
        previous, following = int(previous), int(following)
        count = outgoing[previous]
        probs = [(pairs[(previous, candidate)] + 1) / (count + possibilities)
                 for candidate in unigram]
        # Laplace-smoothed conditional information: self-fit, so treat as
        # local-regularity diagnostic, NEVER as actual listener expectation.
        entropy_terms.append(_entropy(np.array(probs, dtype=float)))
        surprisal = -math.log2((pairs[(previous, following)] + 1) /
                                 (count + possibilities))
        surprisals.append(surprisal)

    return {
        "accent_autocorr_1": float(autocorr[lag]),
        "accent_autocorr_2": float(autocorr[lag * 2]) if lag * 2 < n else 0.0,
        "accent_autocorr_3": float(autocorr[lag * 3]) if lag * 3 < n else 0.0,
        "pulse_phase_concentration": float(concentration),
        "pulse_phase_entropy": phase_entropy,
        "event_accent_lag1": _corr(strengths, 1),
        "event_accent_lag2": _corr(strengths, 2),
        "ioi_transition_entropy": float(np.mean(entropy_terms)) if entropy_terms else 0.0,
        "ioi_high_surprisal": float(np.quantile(surprisals, .9)) if surprisals else 0.0,
    }
