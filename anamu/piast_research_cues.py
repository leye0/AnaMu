"""Testable MIDI-only musical-cue hypothesis for perceived emotion.

Research rationale (NOT a reproduction of published classifier coefficients):

Micallef Grimaud & Eerola (2022), PLOS ONE 17(12), e0279605, experimentally varied
mode (major/minor), tempo, articulation (legato/staccato), pitch and dynamics
and observed distinct patterns of perceived musical expression. We turn
these candidate mechanisms into *observables* from real performance MIDI.

Only the MIDI is read; absolutely no emotion label influences these features.
Our automatic tonal and articulation proxies are hypotheses with possible
failure modes, not the manipulated ground-truth settings of their study.
PIAST-AT is observational and cannot establish causation from classifier lift.
"""

from __future__ import annotations

import io
import math
import statistics
from collections import defaultdict
from pathlib import Path

import mido
import numpy as np


# Krumhansl & Kessler (1982) probe-tone tonal hierarchy, rotated across roots.
# Values are published perceptual key profiles, NOT fitted to PIAST labels.
MAJOR_PROFILE = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09,
                          2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MINOR_PROFILE = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53,
                          2.54, 4.75, 3.98, 2.69, 3.34, 3.17])


def tonal_mode_evidence(notes: list[tuple[int, int, int, int]],
                        ticks_per_beat: int) -> dict[str, float]:
    """Duration-weighted chroma against published major/minor profiles."""
    chroma = np.zeros(12, dtype=float)
    for start, end, pitch, velocity in notes:
        chroma[pitch % 12] += min((end - start) / ticks_per_beat, 4.0)
    if np.sum(chroma) <= 0:
        raise ValueError("no_pitch_class_evidence")
    def corr(x, y):
        a, b = x - np.mean(x), y - np.mean(y)
        divisor = float(np.linalg.norm(a) * np.linalg.norm(b))
        return float(np.dot(a, b) / divisor) if divisor else 0.0
    major = max(corr(chroma, np.roll(MAJOR_PROFILE, k)) for k in range(12))
    minor = max(corr(chroma, np.roll(MINOR_PROFILE, k)) for k in range(12))
    return {
        "cue_major_profile_fit": major,
        "cue_minor_profile_fit": minor,
        "cue_minor_minus_major_fit": minor - major,
        "cue_mode_fit_strength": max(major, minor),
    }


def midi_emotion_cues(path: str | Path, *, interactions: bool = False) -> dict[str, float]:
    """Compute interpretable mode/tempo/articulation/dynamics cues from MIDI."""
    midi = mido.MidiFile(file=io.BytesIO(Path(path).read_bytes()))
    if midi.type == 2 or midi.ticks_per_beat <= 0:
        raise ValueError("unsupported_midi_for_emotion_cues")
    tpb = midi.ticks_per_beat
    tempo_changes = [(0, 500_000)]
    active = defaultdict(list)
    notes: list[tuple[int, int, int, int]] = []
    tick = 0
    for msg in mido.merge_tracks(midi.tracks):
        tick += msg.time
        if msg.type == "set_tempo":
            if msg.tempo <= 0:
                raise ValueError("invalid_tempo")
            tempo_changes.append((tick, msg.tempo))
        if msg.type not in ("note_on", "note_off") or msg.channel == 9:
            continue
        key = msg.channel, msg.note
        if msg.type == "note_on" and msg.velocity > 0:
            active[key].append((tick, msg.velocity))
        elif active[key]:
            start, velocity = active[key].pop(0)
            if start < tick:
                notes.append((start, tick, msg.note, velocity))
    if len(notes) < 4:
        raise ValueError("too_few_notes_for_emotion_cues")
    end_tick = max(end for _, end, _, _ in notes)

    # Time-weighted performed tempo: tempo messages, not density of onsets.
    # A repeated tempo message at one tick replaces the previous message.
    tempo_by_tick = {position: value for position, value in tempo_changes}
    positions = sorted(x for x in tempo_by_tick if x < end_tick) + [end_tick]
    elapsed = 0.0
    bpm_values = []
    weights = []
    for left, right in zip(positions, positions[1:]):
        beats = (right - left) / tpb
        if beats <= 0:
            continue
        tempo = tempo_by_tick[left]
        seconds = beats * tempo / 1_000_000
        elapsed += seconds
        bpm_values.append(60_000_000 / tempo)
        weights.append(seconds)
    if elapsed <= 0 or not bpm_values:
        raise ValueError("invalid_midi_tempo_timeline")
    bpm = 60 * end_tick / tpb / elapsed
    weighted_log_mean = sum(math.log(v) * w for v, w in zip(bpm_values, weights)) / elapsed
    tempo_log_std = math.sqrt(sum(w * (math.log(v) - weighted_log_mean) ** 2
                                   for v, w in zip(bpm_values, weights)) / elapsed)

    # Upper-onset voice is a heuristic. Polyphonic overlap and sustain pedal
    # may make it an unreliable estimate of true staccato/legato articulation.
    at_onset: dict[int, list[tuple[int, int, int, int]]] = defaultdict(list)
    for note in notes:
        at_onset[note[0]].append(note)
    melody = [max(at_onset[start], key=lambda n: n[2]) for start in sorted(at_onset)]
    ratios = []
    for note, following in zip(melody, melody[1:]):
        ioi = following[0] - note[0]
        if 0 < ioi <= 4 * tpb:
            ratios.append(min(2.0, (note[1] - note[0]) / ioi))
    if not ratios:
        raise ValueError("no_articulation_observations")
    length = len(ratios)
    articulation_median = statistics.median(ratios)
    detached = sum(r < .65 for r in ratios) / length
    legato = sum(r > .95 for r in ratios) / length

    velocity_average = statistics.mean(n[3] for n in notes)
    midpoint = end_tick / 2
    before = [n[3] for n in notes if n[0] < midpoint]
    after = [n[3] for n in notes if n[0] >= midpoint]
    dynamics_arc = statistics.mean(after) - statistics.mean(before) if before and after else 0.
    features = {
        **tonal_mode_evidence(notes, tpb),
        "cue_performed_bpm": float(bpm),
        "cue_tempo_log_variation": float(tempo_log_std),
        "cue_articulation_median_ratio": float(articulation_median),
        "cue_detached_fraction": float(detached),
        "cue_legato_fraction": float(legato),
        "cue_dynamic_second_half_minus_first": float(dynamics_arc),
    }
    if interactions:
        # The research motivates combinations, but not THESE numerical
        # coefficients. These are fixed, falsifiable cross-products and are
        # never chosen by looking at PIAST annotations.
        mode = features["cue_minor_minus_major_fit"]
        pace = bpm / 120.0
        attack = detached
        features.update({
            "cue_x_mode_tempo": mode * pace,
            "cue_x_mode_detachment": mode * attack,
            "cue_x_tempo_detachment": pace * attack,
            "cue_x_mode_dynamic": mode * velocity_average / 127,
            "cue_x_tempo_dynamic": pace * velocity_average / 127,
            "cue_x_mode_rubato": mode * tempo_log_std,
        })
    return features
