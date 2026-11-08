"""MIDI-only *trajectory* of tonal mode/ambiguity over a performed phrase.

Motivation (not reproduction): Xia et al. (AAAI 2026) found that explicitly
injecting mode helps symbolic music emotion recognition. Krumhansl & Kessler
(1982) supply the unchanged perceptual key profiles used here. Our hypothesis
is that the *evolution* of tonal confidence and ambiguity, not simply a
clip-wide major/minor mean, may distinguish difficult piano mood labels.

Equal-duration note-attack windows, 24 rotated key-profile correlations.
No audio; no mood labels; no language-model fitting; no assumption that one
major/minor decision is objectively the correct musical analysis.
"""

from __future__ import annotations

import hashlib
from collections import defaultdict
from pathlib import Path

import mido
import numpy as np

from .piast_research_cues import MAJOR_PROFILE, MINOR_PROFILE


TONAL_MOTION_FEATURE_NAMES = (
    "tonal_motion_minor_evidence_mean",
    "tonal_motion_minor_evidence_std",
    "tonal_motion_minor_evidence_last_first",
    "tonal_motion_minor_evidence_late_early",
    "tonal_motion_minor_persistent_fraction",
    "tonal_motion_confidence_mean",
    "tonal_motion_confidence_std",
    "tonal_motion_mode_ambiguity_mean",
    "tonal_motion_mode_ambiguity_std",
    "tonal_motion_mode_ambiguity_last_first",
    "tonal_motion_tonic_change_fraction",
    "tonal_motion_key_switch_fraction",
    "tonal_motion_minor_to_major_switch_fraction",
    "tonal_motion_chromatic_fraction_mean",
    "tonal_motion_chromatic_fraction_std",
    "tonal_motion_chromatic_fraction_late_early",
    "tonal_motion_chromatic_fraction_peak",
    "tonal_motion_key_path_return_fraction",
)


def _profiles() -> tuple[np.ndarray, np.ndarray]:
    # [24 modes, 12 chroma], mode indices 0..11 major, 12..23 minor.
    profiles = np.asarray([np.roll(profile, tonic)
                           for profile in (MAJOR_PROFILE, MINOR_PROFILE)
                           for tonic in range(12)], dtype=float)
    profiles -= profiles.mean(axis=1, keepdims=True)
    profiles /= np.maximum(np.linalg.norm(profiles, axis=1, keepdims=True), 1e-10)
    masks = np.zeros((24, 12), dtype=float)
    for minor in range(2):
        for tonic in range(12):
            degrees = (0, 2, 3, 5, 7, 8, 10) if minor else (0, 2, 4, 5, 7, 9, 11)
            masks[minor * 12 + tonic, [(tonic + v) % 12 for v in degrees]] = 1.
    return profiles, masks


PROFILES, DIATONIC_MASKS = _profiles()


def tonal_motion_features(notes: np.ndarray, *, windows: int = 8,
                          shuffle: bool = False, seed: int = 20261108) -> dict[str, float]:
    """`notes` rows: [onset_ticks, offset_ticks, MIDI pitch, velocity]."""
    if notes.ndim != 2 or notes.shape[1] != 4 or len(notes) < 12:
        raise ValueError("insufficient_notes_for_tonal_motion")
    if not windows >= 4:
        raise ValueError("too_few_tonal_windows")
    start, end = float(np.min(notes[:, 0])), float(np.max(notes[:, 1]))
    if end <= start:
        raise ValueError("invalid_tonal_duration")
    indices = np.clip(np.floor((notes[:, 0] - start) / (end - start) * windows).astype(int),
                      0, windows - 1)
    duration = np.maximum(notes[:, 1] - notes[:, 0], 1.)
    # Cap sustained notes; this reduces pedal / long-drone dominance.
    weight = np.minimum(duration / (end - start) * windows, 2.)
    chroma = np.zeros((windows, 12), dtype=float)
    for j, pitch, mass in zip(indices, notes[:, 2], weight):
        chroma[int(j), int(pitch) % 12] += mass
    if np.count_nonzero(np.sum(chroma, axis=1) > 0) < windows // 2:
        raise ValueError("too_many_empty_tonal_windows")
    if shuffle:
        chroma = chroma[np.random.default_rng(seed).permutation(windows)]

    evidence = []
    for row in chroma:
        if row.sum() < 1e-10:
            # Missing tonal evidence is explicitly ambiguous, not major.
            evidence.append((0., 0., 0., -1, 0.))
            continue
        z = row - np.mean(row)
        z /= max(float(np.linalg.norm(z)), 1e-10)
        corr = PROFILES @ z
        best_major = int(np.argmax(corr[:12]))
        best_minor = int(np.argmax(corr[12:])) + 12
        winning = int(np.argmax(corr))
        # This is a *rank-relative entropy proxy*; NOT calibrated
        # probability of a musicological key or empirical listener belief.
        centered = (corr - np.max(corr)) / .18
        masses = np.exp(np.clip(centered, -40., 0.))
        probs = masses / masses.sum()
        entropy = -float(np.sum(probs * np.log2(np.maximum(probs, 1e-12)))) / np.log2(24)
        chromatic = float(np.sum(row * (1. - DIATONIC_MASKS[winning])) / row.sum())
        evidence.append((float(corr[best_minor] - corr[best_major]),
                         float(corr[winning]), entropy, winning, chromatic))
    data = np.asarray(evidence, dtype=float)
    mode, confidence, ambiguity, key, chromatic = data.T
    nonempty = key >= 0
    if nonempty.sum() < windows // 2:
        raise ValueError("not_enough_tonal_observations")

    def last_first(a):
        return float(a[-1] - a[0])

    def late_early(a):
        midpoint = len(a) // 2
        return float(np.mean(a[midpoint:]) - np.mean(a[:midpoint]))

    valid_transitions = (key[1:] >= 0) & (key[:-1] >= 0)
    change = (key[1:] != key[:-1]) & valid_transitions
    tonic_change = ((key[1:].astype(int) % 12) != (key[:-1].astype(int) % 12)) & valid_transitions
    switch_minor_major = ((key[1:] >= 12) != (key[:-1] >= 12)) & valid_transitions
    transitions = max(int(np.sum(valid_transitions)), 1)
    # Return to an earlier tonal center after a new center: A-B-A motif.
    returns = np.asarray([int(key[k] >= 0 and key[k] == key[k-2] and key[k] != key[k-1])
                          for k in range(2, len(key))], dtype=float)
    result = {
        "tonal_motion_minor_evidence_mean": float(np.mean(mode)),
        "tonal_motion_minor_evidence_std": float(np.std(mode)),
        "tonal_motion_minor_evidence_last_first": last_first(mode),
        "tonal_motion_minor_evidence_late_early": late_early(mode),
        "tonal_motion_minor_persistent_fraction": float(np.mean(mode > .08)),
        "tonal_motion_confidence_mean": float(np.mean(confidence)),
        "tonal_motion_confidence_std": float(np.std(confidence)),
        "tonal_motion_mode_ambiguity_mean": float(np.mean(ambiguity)),
        "tonal_motion_mode_ambiguity_std": float(np.std(ambiguity)),
        "tonal_motion_mode_ambiguity_last_first": last_first(ambiguity),
        "tonal_motion_tonic_change_fraction": float(tonic_change.sum() / transitions),
        "tonal_motion_key_switch_fraction": float(change.sum() / transitions),
        "tonal_motion_minor_to_major_switch_fraction": float(switch_minor_major.sum() / transitions),
        "tonal_motion_chromatic_fraction_mean": float(np.mean(chromatic)),
        "tonal_motion_chromatic_fraction_std": float(np.std(chromatic)),
        "tonal_motion_chromatic_fraction_late_early": late_early(chromatic),
        "tonal_motion_chromatic_fraction_peak": float(np.max(chromatic)),
        "tonal_motion_key_path_return_fraction": float(np.mean(returns)),
    }
    if set(result) != set(TONAL_MOTION_FEATURE_NAMES) or not all(np.isfinite(list(result.values()))):
        raise ValueError("unexpected_tonal_feature_output")
    return result


def midi_tonal_motion(path: str | Path, *, shuffle: bool = False,
                      seed: int = 20261108) -> dict[str, float]:
    path = Path(path)
    midi = mido.MidiFile(str(path))
    if midi.type == 2 or midi.ticks_per_beat <= 0:
        raise ValueError("unsupported_tonal_midi")
    tick, active, notes = 0, defaultdict(list), []
    for msg in mido.merge_tracks(midi.tracks):
        tick += msg.time
        if msg.type not in ("note_on", "note_off") or msg.channel == 9:
            continue
        key = msg.channel, msg.note
        if msg.type == "note_on" and msg.velocity > 0:
            active[key].append((tick, msg.velocity))
        elif active[key]:
            started, velocity = active[key].pop(0)
            if tick > started:
                notes.append((started, tick, msg.note, velocity))
    digest = hashlib.sha256(path.name.encode("utf-8")).digest()
    return tonal_motion_features(np.asarray(notes, dtype=float), shuffle=shuffle,
                                 seed=seed + int.from_bytes(digest[:4], "little"))
