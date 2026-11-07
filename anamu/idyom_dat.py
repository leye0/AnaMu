"""Read real, whitespace-delimited IDyOM / py2lispIDyOM ``.dat`` output.

The upstream format contains one row per musical event, often several
melodies in the same file. ``information.content`` and ``entropy`` are the
joint prediction, while e.g. ``cpitch.information.content`` and
``cpitch.entropy`` are a distinct source viewpoint. Missing ``NA`` values
stay missing. The reader never invents emotions or seconds timestamps.

Format and column names are verified against the actual output fixture in
the official xinyiguan/py2lispIDyOM repository (tests/experiment_history).
"""

from __future__ import annotations

import hashlib
import math
import shlex
from pathlib import Path


_NA = frozenset(("NA", ""))
_INFO = "information.content"
_ENTROPY = "entropy"


def _number(raw: str, field: str, *, nonnegative: bool = False) -> float | None:
    if raw in _NA:
        return None
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(f"idyom_invalid_number: {field}") from exc
    if not math.isfinite(value):
        raise ValueError(f"idyom_nonfinite_number: {field}")
    if nonnegative and value < 0:
        raise ValueError(f"idyom_negative_measure: {field}")
    return value


def _positive_id(raw: str, field: str) -> int:
    try:
        result = int(raw)
    except ValueError as exc:
        raise ValueError(f"idyom_invalid_event_id: {field}") from exc
    if result <= 0:
        raise ValueError(f"idyom_nonpositive_event_id: {field}")
    return result


def _viewpoint_columns(columns: list[str]) -> dict[str, dict[str, str]]:
    """Discover all pairs of information-content and entropy outputs."""
    available = set(columns)
    pairs = {}
    for name in columns:
        if name == _INFO:
            prefix, entropy_column = "joint", _ENTROPY
        elif name.endswith("." + _INFO):
            prefix = name[: -len("." + _INFO)]
            entropy_column = prefix + "." + _ENTROPY
        else:
            continue
        if entropy_column not in available:
            raise ValueError(f"idyom_missing_entropy_column: {name}")
        probability = "probability" if prefix == "joint" else prefix + ".probability"
        pairs[prefix] = {"information_content": name, "entropy": entropy_column,
                         "probability": probability if probability in available else ""}
    if not pairs:
        raise ValueError("idyom_no_information_entropy_pairs")
    return pairs


def read_idyom_dat(path: str | Path, *, max_bytes: int = 50_000_000,
                   max_events: int = 200_000,
                   keep_original_fields: bool = False) -> dict:
    """Import real IDyOM event-level surprise/entropy without semantic guesses.

    ``onset`` is expressed in IDyOM's native units (24 units per quarter
    note). It is **not** performance seconds. Use the source MIDI tempo map
    after verifying melody alignment for accurate performance-time conversion.
    ``NA`` means unknown, never zero. Different songs and viewpoint models
    remain distinct in the resulting records. ``keep_original_fields``
    preserves every original column as a string (or None) for auditing and
    research without guessing units, at the cost of larger JSON files.
    """
    source = Path(path)
    if source.stat().st_size > max_bytes:
        raise ValueError("idyom_dat_over_size_limit")
    if max_events <= 0:
        raise ValueError("idyom_invalid_event_limit")
    raw = source.read_bytes()
    try:
        lines = raw.decode("utf-8-sig").splitlines()
    except UnicodeDecodeError as exc:
        raise ValueError("idyom_dat_not_utf8") from exc
    if not lines:
        raise ValueError("idyom_dat_empty")
    columns = lines[0].split()
    if len(set(columns)) != len(columns):
        raise ValueError("idyom_duplicate_columns")
    required = {"dataset.id", "melody.id", "note.id", "melody.name", "onset"}
    if not required.issubset(columns):
        raise ValueError(f"idyom_missing_columns: {sorted(required - set(columns))}")
    pairs = _viewpoint_columns(columns)
    support_columns = {}
    for viewpoint in pairs:
        if viewpoint == "joint":
            continue
        prefix = viewpoint + "."
        support_columns[viewpoint] = {
            name[len(prefix):]: name for name in columns
            if name.startswith(prefix) and name[len(prefix):].lstrip("-").isdigit()
        }

    collections: dict[tuple[str, str], dict] = {}
    seen_ids: dict[tuple[str, str], set[int]] = {}
    count = 0
    for line_number, line in enumerate(lines[1:], start=2):
        if not line.strip():
            continue
        count += 1
        if count > max_events:
            raise ValueError("idyom_dat_over_event_limit")
        try:
            parts = shlex.split(line, comments=False, posix=True)
        except ValueError as exc:
            raise ValueError(f"idyom_invalid_quoted_fields_line_{line_number}") from exc
        if len(parts) != len(columns):
            raise ValueError(f"idyom_field_count_mismatch_line_{line_number}")
        record = dict(zip(columns, parts))
        identity = (record["dataset.id"], record["melody.id"])
        if not all(identity):
            raise ValueError("idyom_missing_melody_identity")
        if identity not in collections:
            collections[identity] = {"dataset_id": identity[0],
                                     "melody_id": identity[1],
                                     "melody_name": record["melody.name"],
                                     "events": []}
            seen_ids[identity] = set()
        melody = collections[identity]
        if record["melody.name"] != melody["melody_name"]:
            raise ValueError("idyom_inconsistent_melody_name")
        note_id = _positive_id(record["note.id"], "note.id")
        if note_id in seen_ids[identity]:
            raise ValueError("idyom_duplicate_note_id")
        seen_ids[identity].add(note_id)
        onset = _number(record["onset"], "onset")
        if onset is None:
            raise ValueError("idyom_onset_missing")
        previous = melody["events"][-1] if melody["events"] else None
        if previous and onset < previous["onset_idyom_units"]:
            raise ValueError("idyom_nonmonotonic_onsets")
        viewpoints = {}
        predictions = {}
        for viewpoint, names in pairs.items():
            probability = (_number(record[names["probability"]], names["probability"],
                                   nonnegative=True) if names["probability"] else None)
            if probability is not None and probability > 1:
                raise ValueError(f"idyom_probability_exceeds_one: {viewpoint}")
            viewpoints[viewpoint] = {
                "surprisal_bits": _number(record[names["information_content"]],
                                           names["information_content"], nonnegative=True),
                "entropy_bits_before": _number(record[names["entropy"]],
                                                names["entropy"], nonnegative=True),
                "event_probability": probability,
            }
            if viewpoint in support_columns:
                predictions[viewpoint] = {}
                for symbol, column in support_columns[viewpoint].items():
                    measure = _number(record[column], column, nonnegative=True)
                    if measure is not None and measure > 1:
                        raise ValueError(f"idyom_probability_exceeds_one: {column}")
                    predictions[viewpoint][symbol] = measure
        tempo = (_number(record["tempo"], "tempo", nonnegative=True)
                 if "tempo" in record else None)
        if tempo == 0:
            raise ValueError("idyom_invalid_zero_tempo")
        event = {
            "note_id": note_id,
            "onset_idyom_units": onset,
            "onset_quarter_beats": onset / 24,
            "tempo_microseconds_per_quarter_if_reported": tempo,
            "viewpoints": viewpoints,
            "information_gain_native_if_reported": (
                _number(record["information.gain"], "information.gain")
                if "information.gain" in record else None),
            "predicted_event_probabilities": predictions,
        }
        if keep_original_fields:
            event["original_fields"] = {
                column: None if value in _NA else value for column, value in record.items()
            }
        melody["events"].append(event)
    if not count:
        raise ValueError("idyom_dat_no_events")
    return {
        "engine": "IDyOM original (imported native .dat)",
        "source_file": str(source),
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "time_axis": "idyom_native_onset_24_units_per_quarter_not_seconds",
        "viewpoint_columns": pairs,
        "prediction_support_columns": {
            name: list(choices) for name, choices in support_columns.items()
        },
        "native_columns_available": columns,
        "original_fields_preserved": keep_original_fields,
        "melody_count": len(collections), "event_count": count,
        "melodies": list(collections.values()),
        "limitations": ["requires_audited_original_idyom_training_and_configuration",
                        "missing_NA_is_unknown_not_zero",
                        "tempo_changes_not_integrated_without_validated_MIDI_alignment",
                        "native_information_gain_units_and_meaning_not_normalized",
                        "information_content_entropy_are_not_direct_emotion_labels"],
    }
