"""Human continuation ratings versus MIDI-note expectations (Cuddy/Lunney).

The 1995 experiment reported group-mean ratings for 25 continuation pitches
after each of eight two-note contexts. The 2025 thesis repository reproduces
the published group means (`cudlun95.data`) and reconstructed MIDI stimuli.
It does NOT expose 24 independent participant-level response vectors.

No rating data are used to derive the note features or to pick candidate
continuations. This is an exploratory reanalysis of already published data.
"""

from __future__ import annotations

import re
from pathlib import Path

import mido
import numpy as np


MAJOR = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09,
                  2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MINOR = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53,
                  2.54, 4.75, 3.98, 2.69, 3.34, 3.17])


def load_group_means(path: Path) -> list[dict]:
    """Parse exact 8 x 25 x 2 published aggregate-ratings schema."""
    blocks = []
    current = None
    for line in path.read_text(encoding="utf-8").splitlines():
        value = line.strip()
        if not value or value.lower().startswith("trained"):
            continue
        if value.startswith("#"):
            if current:
                blocks.append(current)
            current = {"name": value[1:].strip(), "trained": [], "untrained": []}
            continue
        if current is None:
            raise ValueError("rating_without_named_context")
        parts = value.split()
        if len(parts) != 2:
            raise ValueError(f"expected_two_group_mean_ratings: {value!r}")
        trained, untrained = map(float, parts)
        if not (1 <= trained <= 7 and 1 <= untrained <= 7):
            raise ValueError("rating_outside_1_to_7")
        current["trained"].append(trained)
        current["untrained"].append(untrained)
    if current:
        blocks.append(current)
    if len(blocks) != 8 or any(len(b["trained"]) != 25 or len(b["untrained"]) != 25
                                for b in blocks):
        raise ValueError("expected_eight_contexts_and_25_probes_per_group")
    if len(set(b["name"] for b in blocks)) != 8:
        raise ValueError("repeated_context_name")
    return blocks


def _midi_onsets(path: Path) -> list[int]:
    midi = mido.MidiFile(str(path))
    if midi.type == 2:
        raise ValueError("unsupported_midi_type_2")
    notes = [msg.note for msg in mido.merge_tracks(midi.tracks)
             if msg.type == "note_on" and msg.velocity > 0]
    if len(notes) != 3 or notes[1] != notes[2]:
        raise ValueError("requires_two_context_notes_plus_repeated_placeholder_probe")
    return notes


def load_contexts(ratings_file: Path, midi_folder: Path) -> list[dict]:
    result = []
    for index, block in enumerate(load_group_means(ratings_file), start=1):
        notes = _midi_onsets(midi_folder / f"cudlun95-{index}_with_probe.mid")
        first, second = notes[:2]
        label = block["name"].lower()
        interval_name = re.match(r"^(m2|m3|m6|m7) (ascending|descending)$", label)
        # M2 (major second) and m3 (minor third); M6 and m7 denote
        # major sixth and minor seventh. The MIDI itself has priority.
        if not interval_name:
            raise ValueError("unrecognized_original_interval_name")
        expected = {"m2": 2, "m3": 3, "m6": 9, "m7": 10}[interval_name[1]]
        sign = 1 if interval_name[2] == "ascending" else -1
        if second - first != sign * expected:
            raise ValueError("midi_context_does_not_match_annotated_interval")
        probes = np.arange(second - 12, second + 13)
        if probes[0] != 54 or probes[-1] != 78:
            raise ValueError("probe_pitch_map_not_54_to_78")
        result.append({**block, "id": index, "first": first,
                       "second": second, "probes": probes})
    return result


def theory_features(first: int, second: int, probes: np.ndarray) -> dict[str, np.ndarray]:
    """Explicit, untrained proxies; no claim to original Narmour equations."""
    change = second - first
    continuation = probes - second
    distance = np.abs(continuation).astype(float)
    small = abs(change) <= 5
    same_direction = np.sign(continuation) == np.sign(change)
    expected_direction = same_direction if small else ~same_direction
    retrace = np.maximum(0, 3 - np.abs(probes - first))
    proximity = np.maximum(0, 6 - distance)
    interval_match = (-np.abs(distance - abs(change))) if small else (-distance)
    height = continuation.astype(float)
    contour = np.column_stack([
        proximity, retrace, expected_direction.astype(float),
        interval_match, height,
    ])
    tonal = np.column_stack([
        np.roll(profile, tonic)[probes % 12]
        for profile in (MAJOR, MINOR)
        for tonic in (first % 12, second % 12)
    ])
    return {
        "proximity": proximity.reshape(-1, 1),
        "narmour_contour_proxy": contour,
        "contour_plus_tonal_hierarchy": np.column_stack([contour, tonal]),
    }


def training_arrays(contexts: list[dict]) -> dict:
    groups = np.repeat(np.arange(len(contexts)), 25)
    labels = np.array([(tr + un) / 2
                       for b in contexts for tr, un in zip(b["trained"], b["untrained"])])
    trained = np.array([n for b in contexts for n in b["trained"]])
    untrained = np.array([n for b in contexts for n in b["untrained"]])
    features = {key: np.vstack([theory_features(b["first"], b["second"], b["probes"])[key]
                                for b in contexts])
                for key in ("proximity", "narmour_contour_proxy", "contour_plus_tonal_hierarchy")}
    return {"groups": groups, "labels": labels, "trained": trained,
            "untrained": untrained, "features": features}
