"""Manzara/Witten/Conklin (1992): real-next-note human information content.

The observations are group summaries of human *bets* in bits, not independent
listener votes, probe-tone ratings, emotion, or acoustic-envelope annotations.
The paired modern MIDI reconstructions contain one monophonic realized melody
per chorale; at prediction time the current and later pitches must stay hidden.
"""

from __future__ import annotations

from pathlib import Path

import mido
import numpy as np


CHORALE_LENGTHS = {151: 29, 61: 57}


def human_note_bits(source: Path) -> dict[int, np.ndarray]:
    """Read three documented human-aggregation columns, keyed by chorale."""
    results: dict[int, list[tuple[int, float, float, float]]] = {
        id_: [] for id_ in CHORALE_LENGTHS
    }
    for line in source.read_text(encoding="utf-8").splitlines():
        entry = line.strip()
        if not entry or entry.startswith("#") or entry.lower().startswith("chorale"):
            continue
        columns = entry.split()
        if len(columns) != 5:
            raise ValueError("expected_chorale_note_and_three_human_bits_columns")
        try:
            chorale, index = int(columns[0]), int(columns[1])
            aggregate = tuple(float(x) for x in columns[2:])
        except ValueError as exc:
            raise ValueError("invalid_human_chorale_row") from exc
        if chorale not in results:
            raise ValueError("unexpected_chorale_id")
        if index != len(results[chorale]) + 1:
            raise ValueError("duplicate_out_of_order_or_missing_note_index")
        if any(not np.isfinite(v) or v < 0 for v in aggregate):
            raise ValueError("invalid_human_information_bits")
        results[chorale].append((index, *aggregate))
    if any(len(results[id_]) != length for id_, length in CHORALE_LENGTHS.items()):
        raise ValueError("expected_29_and_57_human_note_rows")
    return {id_: np.asarray(rows, dtype=float) for id_, rows in results.items()}


def reconstructed_chorale_notes(folder: Path) -> dict[int, np.ndarray]:
    """Read only the realized sequential notes, with no human responses."""
    sequences = {}
    for chorale, expected_length in CHORALE_LENGTHS.items():
        midi = mido.MidiFile(str(folder / f"chorale{chorale}.mid"))
        if midi.type == 2:
            raise ValueError("unsupported_type_two_chorale")
        events = list(mido.merge_tracks(midi.tracks))
        notes = np.asarray([msg.note for msg in events
                            if msg.type == "note_on" and msg.velocity > 0], dtype=int)
        if len(notes) != expected_length:
            raise ValueError("midi_note_count_does_not_match_original_chorale")
        if np.any(np.abs(np.diff(notes)) > 12):
            # The Cuddy-trained predictor explicitly has only a +/-12-note
            # candidate window. Never silently drop out-of-window answers.
            raise ValueError("realized_note_outside_frozen_25_pitch_support")
        sequences[chorale] = notes
    return sequences


def softmax_information_bits(scores: np.ndarray, actual_index: int) -> float:
    """Convert frozen *ratings* into a 25-state probability, then -log2(p).

    Softmax temperature is fixed at 1 original rating unit; it is NOT
    calibrated to human gambling probabilities and is not a proper fit to
    another task. The human target is not read by this function.
    """
    values = np.asarray(scores, dtype=float)
    if values.shape != (25,) or not np.isfinite(values).all():
        raise ValueError("expected_25_finite_continuation_scores")
    if actual_index not in range(25):
        raise ValueError("actual_note_outside_cuddy_candidate_support")
    centered = values - float(np.max(values))
    log_denom = float(np.log(np.exp(centered).sum()))
    return float((log_denom - centered[actual_index]) / np.log(2))
