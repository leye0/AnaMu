"""Existing multi-framework melody features on *reliable monophonic* MIDI.

Uses the published `melody-features` library rather than recreating 200+
melody descriptors. We preserve hypotheses and refuse ambiguous polyphony.
"""

from __future__ import annotations

import math
from collections import Counter
from importlib.metadata import version
from pathlib import Path

from .midi_views import extract_monophonic_candidates
from .tempo_map import MidiTempoMap


def _json_value(value):
    """Convert numpy/pandas scalars and missing values without inventing data."""
    if hasattr(value, "item") and not isinstance(value, (dict, list, tuple)):
        try:
            value = value.item()
        except (ValueError, TypeError):
            pass
    if hasattr(value, "tolist") and not isinstance(value, (dict, list, tuple, str)):
        try:
            value = value.tolist()
        except (ValueError, TypeError):
            pass
    if isinstance(value, dict):
        return {str(k): _json_value(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [_json_value(v) for v in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    # Preserve unsupported objects as unresolved, never as made-up numbers.
    return None


def extract_melody_toolbox(midi_path: str | Path, *, minimum_notes: int = 6) -> dict:
    """Run external source-comparison features for strictly monophonic parts.

    The library's default reference corpus may be used by corpus-statistical
    descriptors; it must be logged, independently audited for overlap, and
    never confused with EMOPIA human labels. Original IDyOM is separately
    integrated; this path deliberately excludes it.
    """
    try:
        import melody_features as mf
        from melody_features.core.representations import Melody
        from melody_features.features import get_narmour_features
    except ImportError as exc:
        raise RuntimeError("Install optional package: pip install 'melody-features==1.3.3'") from exc
    package_version = version("melody-features")
    if package_version != "1.3.3":
        raise RuntimeError(f"melody_features_version_not_pinned: {package_version}")

    source = Path(midi_path)
    contents = source.read_bytes()
    timing = MidiTempoMap.from_bytes(contents)
    selection = extract_monophonic_candidates(contents, min_notes=minimum_notes)
    accepted = selection["candidates"]
    if not accepted:
        return {"engine": "melody-features", "status": "no_reliable_monophonic_part",
                "candidate_count": 0, "rejected_parts": selection["rejected_parts"],
                "limitations": ["polyphonic_piano_cannot_be_assumed_to_have_extractable_melody"]}

    melodies = []
    tempo_changes = timing.tempo_changes_seconds()
    for part in accepted:
        pitches = [n["pitch"] for n in part["notes"]]
        starts = [timing.beats_to_seconds(n["start_beats"]) for n in part["notes"]]
        ends = [timing.beats_to_seconds(n["end_beats"]) for n in part["notes"]]
        melodies.append(Melody.from_notes(
            pitches, starts, ends, melody_id=f'track{part["track"]}_channel{part["channel"]}',
            tempo=tempo_changes[0][1],
            tempo_changes=tempo_changes,
        ))

    # A single batch avoids repeated reference-corpus computation. No
    # IDyOM launch: it is an independent experiment requiring SBCL and proper
    # training partitions.
    frame = mf.get_all_features(input=melodies, skip_idyom=True, log_level=40)
    records = []
    if len(frame) != len(melodies):
        raise RuntimeError("unexpected_melody_feature_row_count")
    for (_, row), part, melody in zip(frame.iterrows(), accepted, melodies):
        if row["melody_id"] != melody.id:
            raise RuntimeError("melody_feature_rows_not_in_input_order")
        features = {str(key): _json_value(value) for key, value in row.to_dict().items()
                    if str(key) not in ("melody_num", "melody_id")}
        family_counts = dict(sorted(Counter(
            name.split(".", 1)[0] for name in features).items()))
        # The original published Narmour measures are calculated over each
        # three-note realization, so their *temporal* evolution remains
        # visible rather than being reduced to a single whole-piece mean.
        # These scores are retrospective observations at the third note,
        # NOT probabilities predicted before that note.
        narmour_events = []
        notes = part["notes"]
        for offset in range(2, len(notes)):
            fragment = notes[offset - 2:offset + 1]
            fragment_melody = Melody.from_notes(
                [note["pitch"] for note in fragment],
                [timing.beats_to_seconds(note["start_beats"]) for note in fragment],
                [timing.beats_to_seconds(note["end_beats"]) for note in fragment],
            )
            narmour_events.append({
                "time_seconds": timing.beats_to_seconds(notes[offset]["start_beats"]),
                "scores": _json_value(get_narmour_features(fragment_melody)),
            })
        records.append({"track": part["track"], "channel": part["channel"],
                        "notes_count": len(part["notes"]),
                        "start_seconds": timing.beats_to_seconds(part["notes"][0]["start_beats"]),
                        "end_seconds": timing.beats_to_seconds(part["notes"][-1]["end_beats"]),
                        "features": features,
                        "feature_families": family_counts,
                        "missing_feature_count": sum(v is None for v in features.values()),
                        "narmour_triplet_realizations": narmour_events})
    return {"engine": "melody-features (published multi-framework library)",
            "status": "features_extracted",
            "engine_version": package_version, "version_pinned": "1.3.3",
            "included_original_idyom": False,
            "default_reference_corpus": "melody-features/pearce_default_idyom (903 melodies; verify overlap)",
            "time_unit": "performance_seconds_derived_from_midi_tempo_map",
            "candidates_are_verified_melodies": False,
            "candidate_count": len(records), "parts": records,
            "rejected_parts": selection["rejected_parts"],
            "limitations": ["no_voice_separation_of_ambiguous_polyphony",
                            "candidate_track_not_verified_primary_melody",
                            "feature_computations_are_not_direct_emotional_labels"]}
