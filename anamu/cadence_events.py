"""MIDI-compatible note events vs *independently annotated* DCML cadences.

Only the public `notes/*.notes.tsv` tables contribute input features. The
`harmonies/*.harmonies.tsv` tables are opened strictly to obtain cadence
targets; not even their expert global/local keys enter the model. These are
symbolic scores rather than recordings or performance MIDI transcriptions.

This is an exploratory *musicological* benchmark, NOT an emotion benchmark.
"""

from __future__ import annotations

import csv
import math
import re
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

import numpy as np


MAJOR = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09,
                  2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MINOR = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53,
                  2.54, 4.75, 3.98, 2.69, 3.34, 3.17])


def _position(s: str) -> float:
    return float(Fraction(s))


def _rows(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _tonic(pitches: list[tuple[int, float]]) -> tuple[int, bool, float]:
    """Global key hypothesis from note pitch/durations, never expert keys."""
    chroma = np.zeros(12)
    for pitch, duration in pitches:
        chroma[pitch % 12] += min(4.0, duration)
    if chroma.sum() == 0:
        raise ValueError("empty_pitch_distribution")
    chroma /= chroma.sum()
    hypotheses = []
    for minor, profile in [(False, MAJOR), (True, MINOR)]:
        for pitch in range(12):
            hypotheses.append((float(np.corrcoef(chroma, np.roll(profile, pitch))[0, 1]),
                               pitch, minor))
    hypotheses.sort(reverse=True)
    best, second = hypotheses[:2]
    return best[1], best[2], best[0] - second[0]


def _chroma(pitches: list[int], tonic: int) -> np.ndarray:
    output = np.zeros(12)
    for pitch in pitches:
        output[(pitch - tonic) % 12] += 1
    if output.sum():
        output /= output.sum()
    return output


def _triad(chroma: np.ndarray, pcs: tuple[int, ...]) -> float:
    return float(sum(chroma[pc] for pc in pcs))


def build_piece(notes_file: Path, harmony_file: Path) -> dict:
    """Return label-aligned candidate events; no annotated harmony inputs."""
    note_rows = _rows(notes_file)
    harmony_rows = _rows(harmony_file)
    if not note_rows or not harmony_rows:
        raise ValueError("empty_notes_or_harmonies")
    candidates: dict[float, list[tuple[int, float, float]]] = defaultdict(list)
    pitch_durations = []
    for row in note_rows:
        if not row.get("midi") or not row.get("quarterbeats"):
            continue
        pitch = int(row["midi"])
        duration = _position(row["duration_qb"])
        if not 0 <= pitch <= 127 or duration <= 0:
            continue
        pos = _position(row["quarterbeats"])
        beat = 4 * _position(row["mc_onset"])
        candidates[pos].append((pitch, duration, beat))
        pitch_durations.append((pitch, duration))
    if len(candidates) < 8:
        raise ValueError("insufficient_note_onsets")
    annotations = {
        _position(row["quarterbeats"])
        for row in harmony_rows if row.get("cadence", "").strip()
        and row.get("quarterbeats")
    }
    tonic, minor, confidence = _tonic(pitch_durations)
    tonic_third = 3 if minor else 4
    tonic_pcs = (0, tonic_third, 7)
    dominant_pcs = (7, 11, 2)
    times = sorted(candidates)
    rhythm: list[list[float]] = []
    harmony: list[list[float]] = []
    labels: list[int] = []
    prior_events: list[tuple[float, list[int]]] = []
    last_attack = []
    last_pos = None
    for t in times:
        attacks = candidates[t]
        pitches = [p for p, _, _ in attacks]
        durations = [d for _, d, _ in attacks]
        beat = attacks[0][2]
        prev_pos = last_pos
        gap = min(8.0, t - prev_pos) if prev_pos is not None else 0.0
        # Offline known score notes, but no labelled harmonic segmentation.
        rhythm.append([
            float(len(pitches)), float(max(pitches) - min(pitches)),
            float(np.mean(durations)), float(max(durations)),
            math.sin(2 * math.pi * beat), math.cos(2 * math.pi * beat),
            float(abs(beat) < 1e-9), gap,
        ])
        immediate = [p for time, ps in prior_events if t - time <= 1.0 for p in ps]
        context = [p for time, ps in prior_events if t - time <= 5.0 for p in ps]
        current_pc = _chroma(immediate + pitches, tonic)
        previous_pc = _chroma(context, tonic)
        delta_pc = current_pc - previous_pc
        bass = (min(pitches) - tonic) % 12
        prev_bass = (min(last_attack) - tonic) % 12 if last_attack else -1
        tonic_now = _triad(current_pc, tonic_pcs)
        tonic_prev = _triad(previous_pc, tonic_pcs)
        dominant_now = _triad(current_pc, dominant_pcs)
        dominant_prev = _triad(previous_pc, dominant_pcs)
        harmony.append([
            *current_pc, *previous_pc, *delta_pc,
            *[float(bass == pc) for pc in range(12)],
            *[float(prev_bass == pc) for pc in range(12)],
            tonic_now, tonic_prev, dominant_now, dominant_prev,
            tonic_now - tonic_prev, dominant_prev - dominant_now,
            float(prev_bass == 7 and bass == 0),
            float(prev_bass == 11 and bass == 0),
            confidence,
        ])
        labels.append(int(t in annotations))
        prior_events.append((t, pitches))
        prior_events = [(time, ps) for time, ps in prior_events if t - time <= 5.0]
        last_attack = pitches
        last_pos = t
    matched = len(annotations.intersection(candidates))
    return {
        "rhythm": rhythm, "harmony": harmony, "labels": labels,
        "n_annotated_cadences": len(annotations), "n_matched_cadences": matched,
        "n_onsets": len(times), "tonic_pc_estimate": tonic,
        "tonic_mode_estimate": "minor" if minor else "major",
    }


def load_corpora(roots: dict[str, Path]) -> dict:
    """Skip missing pairs explicitly, retaining per-composer / work grouping."""
    pieces = []
    skipped = []
    for name, root in sorted(roots.items()):
        for harmonies in sorted((root / "harmonies").glob("*.harmonies.tsv")):
            stem = harmonies.name.removesuffix(".harmonies.tsv")
            notes = root / "notes" / (stem + ".notes.tsv")
            if not notes.is_file():
                skipped.append(f"{name}/{stem}:no_notes")
                continue
            try:
                features = build_piece(notes, harmonies)
            except (ValueError, KeyError) as error:
                skipped.append(f"{name}/{stem}:{error}")
                continue
            features["piece"] = f"{name}/{stem}"
            features["composer"] = name
            # Multiple movements of the SAME sonata/suite share thematic,
            # tonal and editorial conventions. Never split those siblings
            # across train and test folds merely because their files differ.
            family = re.match(r"^(K\d+|BWV\d+)(?:[-_]|$)", stem)
            features["parent_work"] = f"{name}/{family.group(1) if family else stem}"
            pieces.append(features)
    return {"pieces": pieces, "skipped": skipped}
