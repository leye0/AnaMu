"""Human temporal V/A annotation reader and MIDI-only, theory-informed features.

VGMIDI annotators supplied one valence and arousal value per musical measure.
This module keeps the full human disagreement and never passes any annotation
to the feature extractor. Features are observations, not emotion judgements.
"""

from __future__ import annotations

import hashlib
import io
import math
import statistics
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class HumanPiece:
    filename: str
    title: str
    n_measures: int
    duration_audio_seconds: float
    human: tuple[dict, ...]

    @property
    def group(self) -> str:
        # One recording/arrangement and all its repeated excerpts must remain
        # together. The original full MIDI filename is the identity here.
        return self.filename.casefold()


def load_human_pieces(files: list[str | Path]) -> list[HumanPiece]:
    import json

    pieces: dict[str, HumanPiece] = {}
    for file in files:
        source = json.loads(Path(file).read_text(encoding="utf-8"))
        if not isinstance(source.get("pieces"), dict) or not isinstance(source.get("annotations"), dict):
            raise ValueError("bad_vgmidi_raw_schema")
        participants: dict[str, list[dict]] = {}
        for key, annotation in source["annotations"].items():
            piece_id = key.rsplit("_", 1)[0]
            participants.setdefault(piece_id, []).append(annotation)
        for piece_id, meta in source["pieces"].items():
            filename = Path(meta["midi"]).name
            if not filename.endswith(".mid") or "/" in meta["midi"] or "\\" in meta["midi"]:
                raise ValueError("untrusted_vgmidi_midi_name")
            if filename in pieces:
                raise ValueError("duplicate_vgmidi_piece")
            n_measures = int(meta["measures"])
            if not 4 <= n_measures <= 512:
                raise ValueError("invalid_vgmidi_measures")
            human = []
            valid_people = []
            for response in participants.get(piece_id, []):
                valence, arousal = response.get("valence"), response.get("arousal")
                if (isinstance(valence, list) and isinstance(arousal, list)
                    and len(valence) == len(arousal) == n_measures
                    and all(isinstance(v, (int, float)) and math.isfinite(v) and -1 <= v <= 1
                            for v in valence + arousal)):
                    valid_people.append(response)
            if len(valid_people) < 10:
                raise ValueError(f"insufficient_vgmidi_annotators: {filename}")
            for measure in range(n_measures):
                vals = sorted(p["valence"][measure] for p in valid_people)
                arous = sorted(p["arousal"][measure] for p in valid_people)
                def percentile(values: list[float], fraction: float) -> float:
                    return float(values[round((len(values) - 1) * fraction)])
                human.append({
                    "measure": measure + 1,
                    "valence_median": float(statistics.median(vals)),
                    "valence_q25": percentile(vals, 0.25),
                    "valence_q75": percentile(vals, 0.75),
                    "arousal_median": float(statistics.median(arous)),
                    "arousal_q25": percentile(arous, 0.25),
                    "arousal_q75": percentile(arous, 0.75),
                    "annotators": len(valid_people),
                })
            pieces[filename] = HumanPiece(
                filename=filename, title=meta["name"], n_measures=n_measures,
                duration_audio_seconds=float(meta["duration"]), human=tuple(human))
    return sorted(pieces.values(), key=lambda item: item.filename)


def select_splits(pieces: list[HumanPiece], *, seed: int = 20261107,
                  n_test: int = 10, n_validation: int = 20) -> dict[str, str]:
    """Predefine held-out piece identities WITHOUT reading emotional ratings."""
    if n_test < 1 or n_validation < 1 or len(pieces) <= n_test + n_validation:
        raise ValueError("insufficient_pieces_for_group_split")
    if len({p.group for p in pieces}) != len(pieces):
        raise ValueError("duplicate_piece_group")
    order = sorted(pieces, key=lambda p: hashlib.sha256(
        f"{seed}|{p.group}".encode()).hexdigest())
    return {p.filename: ("test" if i < n_test else
                         "validation" if i < n_test + n_validation else "train")
            for i, p in enumerate(order)}


def extract_midi_measures(path: str | Path, n_measures: int) -> tuple[list[dict], dict]:
    """Music-theory features from the actual MIDI, never from emotion labels.

    The annotation grid is per *measure*, not per second. Strictly require a
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
        "audio_reference_duration_seconds_not_used_for_alignment": None,
        "limitations": ["sounding intervals approximate dissonance, not perceived roughness",
                        "global orchestration and production timbre absent from MIDI",
                        "repeated-note and pedal interpretation approximate"],
    }


def enrich_published_mechanisms(path: str | Path, rows: list[dict],
                                beats_per_measure: float) -> dict:
    """Original academic tool outputs on the same measure axis.

    Failures stay missing/observable. Never substitute arbitrary emotional
    scores when a scholarly engine fails on a particular MIDI.
    """
    import warnings
    from .theory_features import music21_harmonic_hypotheses, partitura_tension
    from .tempo_map import MidiTempoMap

    source = Path(path)
    timing = MidiTempoMap.from_bytes(source.read_bytes())
    sources = {}
    # M4 original published Herremans/Chew implementation via Partitura.
    for row in rows:
        for key in ("cloud_diameter", "cloud_momentum", "tensile_strain"):
            row[f"partitura_{key}"] = None
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            tension = partitura_tension(source, window_seconds=2.0, hop_seconds=1.0)
        sources["partitura"] = "ok"
        for index, row in enumerate(rows):
            left = timing.beats_to_seconds(index * beats_per_measure)
            right = timing.beats_to_seconds((index + 1) * beats_per_measure)
            samples = [s for s in tension["samples"] if left <= s["time_seconds"] < right]
            for key in ("cloud_diameter", "cloud_momentum", "tensile_strain"):
                if samples:
                    row[f"partitura_{key}"] = statistics.mean(s[key] for s in samples)
    except (ValueError, RuntimeError, IndexError, ZeroDivisionError) as exc:
        sources["partitura"] = f"unavailable:{type(exc).__name__}"

    # M5/M6 original music21 tonal/harmonic tools; chordified observations
    # remain hypotheses (passing tones are not magically functional chords).
    for row in rows:
        row["music21_chordified_sonorities"] = None
        row["music21_roman_changes"] = None
        row["music21_pitch_class_spread"] = None
        row["music21_key_correlation"] = None
        row["music21_key_is_minor"] = None
    try:
        harmony = music21_harmonic_hypotheses(source)
        sources["music21"] = "ok"
        previous_roman = None
        at_measure: list[list[dict]] = [[] for _ in rows]
        for sonority in harmony["sonorities"]:
            idx = int(sonority["onset_quarter_beats"] / beats_per_measure)
            if 0 <= idx < len(rows):
                at_measure[idx].append(sonority)
        for row, events in zip(rows, at_measure):
            row["music21_chordified_sonorities"] = len(events)
            row["music21_pitch_class_spread"] = (statistics.mean(len(e["pitch_classes"])
                for e in events) if events else None)
            changes = 0
            for event in events:
                rn = event["roman_numeral_hypothesis"]
                if rn is not None and previous_roman is not None and rn != previous_roman:
                    changes += 1
                if rn is not None:
                    previous_roman = rn
            row["music21_roman_changes"] = changes
            row["music21_key_correlation"] = harmony["key_hypothesis"]["correlation_not_probability"]
            row["music21_key_is_minor"] = int(harmony["key_hypothesis"]["mode"] == "minor")
    except (ValueError, RuntimeError, IndexError, ZeroDivisionError) as exc:
        sources["music21"] = f"unavailable:{type(exc).__name__}"
    return sources
