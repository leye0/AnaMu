"""Per-measure symbolic observations; no emotion corpus or labels required."""

from __future__ import annotations

import hashlib
import io
import math
import statistics
from collections import Counter
from pathlib import Path


def extract_midi_measures(path: str | Path, n_measures: int) -> tuple[list[dict], dict]:
    """Descriptive per-measure MIDI features; no ground-truth annotations required.

    The requested grid is per *measure*, not per second. Require a
    constant meter and an alignment-compatible number of MIDI measures.
    Irregular examples abstain rather than being silently time-warped.
    """
    import mido
    from .tempo_map import MidiTempoMap

    data = Path(path).read_bytes()
    score = mido.MidiFile(file=io.BytesIO(data))
    if score.type == 2 or score.ticks_per_beat <= 0:
        raise ValueError("unsupported_midi_timing")
    signatures = {(msg.numerator, msg.denominator) for track in score.tracks for msg in track
                  if msg.type == "time_signature"}
    if len(signatures) > 1:
        raise ValueError("changing_time_signature")
    num, den = next(iter(signatures)) if signatures else (4, 4)
    beats_per_measure = num * 4 / den
    if not 1 <= beats_per_measure <= 12:
        raise ValueError("unsupported_meter")
    duration_beats = n_measures * beats_per_measure
    timing = MidiTempoMap.from_bytes(data)
    start_map: dict[tuple[int, int], list[tuple[int, int]]] = {}
    notes: list[tuple[float, float, int, int, int]] = []
    tick = 0
    for message in mido.merge_tracks(score.tracks):
        tick += message.time
        if message.type not in ("note_on", "note_off") or message.channel == 9:
            continue
        key = (message.channel, message.note)
        if message.type == "note_on" and message.velocity > 0:
            start_map.setdefault(key, []).append((tick, message.velocity))
        elif start_map.get(key):
            beginning, velocity = start_map[key].pop(0)
            if tick > beginning:
                notes.append((beginning / score.ticks_per_beat,
                              tick / score.ticks_per_beat, message.note, velocity,
                              message.channel))
    if not notes:
        raise ValueError("empty_midi")
    actual_end = max(note[1] for note in notes)
    if abs(actual_end - duration_beats) > max(beats_per_measure * 1.5, duration_beats * 0.12):
        raise ValueError(f"measure_alignment_not_confirmed: {actual_end:.2f} vs {duration_beats:.2f}")

    # No global key/tempo shortcut: windowed shape, interval movements,
    # dissonance (symbolic), counterpoint texture and metric positions.
    groups: list[list[tuple[float, float, int, int, int]]] = [[] for _ in range(n_measures)]
    for note in notes:
        index = min(max(int(note[0] / beats_per_measure), 0), n_measures - 1)
        groups[index].append(note)
    result = []
    for i, group in enumerate(groups):
        left = i * beats_per_measure
        active = [n for n in notes if n[0] < left + beats_per_measure and n[1] > left]
        pitches = [n[2] for n in group]
        durations = [n[1] - n[0] for n in group]
        velocities = [n[3] for n in group]
        onsets = sorted(set(round(n[0], 4) for n in group))
        pcs = Counter(p % 12 for p in pitches)
        total = max(len(pitches), 1)
        pc_entropy = -sum((v / total) * math.log2(v / total) for v in pcs.values())
        # Weighted roughness proxy (not psychoacoustic roughness): intervals
        # between simultaneous notes at regularly sampled points.
        clash, concurrency = 0.0, 0.0
        for step in range(16):
            beat = left + (step + 0.5) * beats_per_measure / 16
            sounding = sorted(set(n[2] for n in active if n[0] <= beat < n[1]))
            concurrency += len(sounding) / 16
            intervals = [(b - a) % 12 for j, a in enumerate(sounding) for b in sounding[j + 1:]]
            if intervals:
                clash += (sum(v in (1, 2, 6, 10, 11) for v in intervals)
                          / len(intervals)) / 16
        sequence = sorted(group, key=lambda n: (n[0], n[2]))
        movements = [b[2] - a[2] for a, b in zip(sequence, sequence[1:])]
        result.append({
            "note_density": len(group) / beats_per_measure,
            "onset_density": len(onsets) / beats_per_measure,
            "mean_pitch": statistics.mean(pitches) if pitches else None,
            "pitch_range": max(pitches) - min(pitches) if pitches else None,
            "pc_entropy": pc_entropy,
            "mean_velocity": statistics.mean(velocities) if velocities else None,
            "velocity_variation": statistics.pstdev(velocities) if len(velocities) > 1 else 0.0,
            "mean_duration_beats": statistics.mean(durations) if durations else None,
            "mean_polyphony": concurrency,
            "vertical_interval_clash": clash,
            "mean_abs_melodic_leap": statistics.mean(map(abs, movements)) if movements else None,
            "melodic_direction_bias": statistics.mean((1 if x > 0 else -1 if x < 0 else 0)
                                                        for x in movements) if movements else None,
            "weak_beat_onset_fraction": sum(abs((n[0] - left) % 1) > 0.2 for n in group) / total,
            "end_of_measure_density": sum(n[0] - left >= beats_per_measure * .75 for n in group) / total,
            "fraction_low_register": sum(p < 48 for p in pitches) / total,
            "fraction_high_register": sum(p >= 72 for p in pitches) / total,
        })
    return result, {
        "source_sha256": hashlib.sha256(data).hexdigest(),
        "features": "MIDI note/interval/rhythm/texture/dynamics/vertical pitch-class heuristics",
        "beats_per_measure": beats_per_measure,
        "midi_duration_seconds": timing.beats_to_seconds(actual_end),
        "limitations": ["sounding intervals approximate dissonance, not perceived roughness",
                        "global orchestration and production timbre absent from MIDI",
                        "repeated-note and pedal interpretation approximate"],
    }
