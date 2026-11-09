"""Schellenberg (1996): independent listener expectations and reconstructed MIDI.

The eight real melodic fragments contain an extra, *artificial* probe note in
the 2025 thesis' MIDI reconstructions. Exclude that note from all predictors.
The published 15 diatonic candidates span one octave below and above the
final context tone. The thesis' `schell96.data` entries run high-to-low;
the thesis' own scripts reverse each block to obtain ascending pitch order.
"""

from __future__ import annotations

import re
from pathlib import Path

import mido
import numpy as np


SCALE_DEGREES = (0, 2, 4, 5, 7, 9, 11)
KEY_PC = {"C": 0, "Db": 1, "C#": 1, "D": 2, "Eb": 3, "D#": 3,
          "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "Ab": 8,
          "G#": 8, "A": 9, "Bb": 10, "A#": 10, "B": 11}


def schellenberg_midi_stimuli(folder: Path) -> list[dict]:
    """Recover only context notes and probe *candidate set*, before labels."""
    contexts = []
    for index in range(1, 9):
        source = folder / f"schell96-{index}_with_probe.mid"
        midi = mido.MidiFile(str(source))
        if midi.type == 2:
            raise ValueError("unsupported_type_two_midi")
        messages = list(mido.merge_tracks(midi.tracks))
        notes = [int(msg.note) for msg in messages
                 if msg.type == "note_on" and msg.velocity > 0]
        keys = [msg.key for msg in messages if msg.type == "key_signature"]
        if len(notes) < 4 or notes[-1] != 84:
            raise ValueError("missing_reconstructed_probe_placeholder")
        if len(keys) != 1 or keys[0] not in KEY_PC:
            raise ValueError("missing_supported_major_key_signature")
        context = notes[:-1]
        first, second = context[-2:]
        if abs(second - first) not in (2, 3, 9, 10):
            raise ValueError("unexpected_original_implicative_interval")
        tonic = KEY_PC[keys[0]]
        allowed = {(tonic + deg) % 12 for deg in SCALE_DEGREES}
        candidates = np.array([note for note in range(second - 12, second + 13)
                               if note % 12 in allowed], dtype=int)
        if len(candidates) != 15 or second not in candidates:
            raise ValueError("expected_15_diatonic_continuations")
        contexts.append({"id": index, "key_signature": keys[0],
                         "context_note_count": len(context),
                         "last_two": [first, second],
                         "candidates": candidates})
    if sorted(set(abs(c["last_two"][1] - c["last_two"][0])
                  for c in contexts)) != [2, 3, 9, 10]:
        raise ValueError("unexpected_original_interval_families")
    return contexts


def schellenberg_human_means(path: Path) -> list[np.ndarray]:
    """Load eight 15-probe *aggregate* means, each ascending after reversal."""
    blocks: list[list[float]] = []
    for row in path.read_text(encoding="utf-8").splitlines():
        value = row.strip()
        if not value or value.lower() == "rating":
            continue
        if value.startswith("#"):
            if not re.fullmatch(r"#fragment[1-8]", value):
                raise ValueError("unexpected_schell_fragment_label")
            expected = f"#fragment{len(blocks) + 1}"
            if value != expected:
                raise ValueError("fragment_order_mismatch")
            blocks.append([])
            continue
        if not blocks:
            raise ValueError("ratings_without_fragment")
        val = float(value)
        if not np.isfinite(val) or not 1 <= val <= 7:
            raise ValueError("ratings_outside_1_to_7")
        blocks[-1].append(val)
    if len(blocks) != 8 or any(len(block) != 15 for block in blocks):
        raise ValueError("expected_eight_fragments_with_15_ratings")
    return [np.asarray(block[::-1], dtype=float) for block in blocks]
