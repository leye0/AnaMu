"""Adapters for published musical mechanisms; NOT emotion predictors.

Partitura runs the original Herremans/Chew tension-ribbon mathematics. We do
not recode it, rename tension 'sadness', or use EMOPIA labels as features.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path


def partitura_tension(midi_path: str | Path, *, window_seconds: float = 1.0,
                      hop_seconds: float = 0.5) -> dict:
    """Run Partitura's published tonal-tension implementation on a MIDI file.

    Input is a performed piano MIDI. Partitura uses performance seconds,
    estimates missing pitch spelling and key; report these assumptions.
    This adapter intentionally does not pretend to know local modulations.
    """
    if window_seconds <= 0 or hop_seconds <= 0:
        raise ValueError("window_seconds and hop_seconds must be positive")
    try:
        import partitura
        from partitura.musicanalysis import estimate_tonaltension
    except ImportError as exc:
        raise RuntimeError("Install optional dependency: pip install 'partitura>=1.8,<2'") from exc

    note_array = partitura.midi_to_notearray(str(midi_path))
    if not len(note_array):
        raise ValueError("empty_midi_notes")
    if "onset_sec" not in note_array.dtype.names:
        raise ValueError("expected_performance_time_in_seconds")
    # These are independent tonal observations, not perceptual labels.
    result = estimate_tonaltension(note_array, ws=window_seconds, ss=hop_seconds)
    signals = []
    for observation in result:
        sample = {
            "time_seconds": float(observation["onset_sec"]),
            "cloud_diameter": float(observation["cloud_diameter"]),
            "cloud_momentum": float(observation["cloud_momentum"]),
            "tensile_strain": float(observation["tensile_strain"]),
        }
        if any(not math.isfinite(v) for v in sample.values()):
            raise ValueError("nonfinite_partitura_tension")
        signals.append(sample)
    return {
        "engine": "partitura.musicanalysis.estimate_tonaltension",
        "engine_version": partitura.__version__,
        "reference": "Herremans & Chew (2016), Tension Ribbons",
        "axis": "performance_seconds",
        "parameters": {"window_seconds": window_seconds, "hop_seconds": hop_seconds},
        "limitations": ["key_and_spelling_may_be_estimated",
                        "global_key_estimate_does_not_validate_local_modulations",
                        "not_a_direct_emotion_measure"],
        "samples": signals,
    }


def read_idyom_export(
    csv_path: str | Path, *, surprisal_column: str,
    entropy_column: str, onset_column: str | None = None,
) -> dict:
    """Import output of the *real* IDyOM experiment, not our n-gram baseline.

    Column names are explicit to support different IDyOM viewpoint exports.
    Information content and entropy should use IDyOM's native bits.
    Provenance and training configuration are supplied by the experiment log.
    """
    if not surprisal_column or not entropy_column:
        raise ValueError("explicit_idyom_columns_required")
    rows = []
    with Path(csv_path).open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        columns = [surprisal_column, entropy_column]
        if onset_column:
            columns.append(onset_column)
        missing = set(columns) - set(reader.fieldnames or ())
        if missing:
            raise ValueError(f"missing_idyom_columns: {sorted(missing)}")
        for record in reader:
            try:
                sample = {"surprisal_bits": float(record[surprisal_column]),
                          "entropy_bits_before": float(record[entropy_column])}
                if onset_column:
                    sample["onset_native"] = float(record[onset_column])
            except (TypeError, ValueError) as exc:
                raise ValueError("invalid_idyom_numeric_value") from exc
            if any(not math.isfinite(v) for v in sample.values()):
                raise ValueError("nonfinite_idyom_measure")
            if sample["surprisal_bits"] < 0 or sample["entropy_bits_before"] < 0:
                raise ValueError("negative_idyom_information_measure")
            rows.append(sample)
    if not rows:
        raise ValueError("empty_idyom_export")
    return {"engine": "IDyOM (upstream export)",
            "reference": "Pearce, Information Dynamics of Music",
            "columns": {"surprisal": surprisal_column, "entropy": entropy_column,
                        "onset": onset_column},
            "samples": rows,
            "limitations": ["verify_original_idyom_training_and_viewpoint_configuration",
                            "onset_units_are_source_specific",
                            "not_a_direct_emotion_measure"]}


def music21_harmonic_hypotheses(midi_path: str | Path) -> dict:
    """Use music21's existing Krumhansl-Schmuckler and Roman numeral tools.

    A chordified vertical slice is NOT guaranteed to be a functional chord:
    it can contain passing notes, pedal tones, and independent voices.
    Inferred key and roman numerals are *hypotheses*, never ground truth.
    """
    try:
        import music21
        from music21 import chord, converter, roman
    except ImportError as exc:
        raise RuntimeError("Install optional dependency: pip install 'music21>=9,<12'") from exc
    score = converter.parse(str(midi_path))
    if not list(score.recurse().notes):
        raise ValueError("empty_midi_notes")
    estimated_key = score.analyze("key.krumhanslschmuckler")
    sonorities = []
    # flatten() is essential: a chord's .offset inside each measure resets
    # locally, which would create a fake chronology for multi-measure scores.
    for event in score.chordify().flatten().getElementsByClass(chord.Chord):
        pcs = sorted(set(event.pitchClasses))
        roman_hypothesis = None
        roman_scale_degree = None
        roman_inversion = None
        if len(pcs) >= 3:
            try:
                hypothesis = roman.romanNumeralFromChord(event, estimated_key)
                roman_hypothesis = hypothesis.figure
                roman_scale_degree = int(hypothesis.scaleDegree)
                roman_inversion = int(hypothesis.inversion())
            except (ValueError, IndexError, music21.exceptions21.Music21Exception):
                pass  # Unknown is more honest than a fabricated harmonic role.
        sonorities.append({
            "onset_quarter_beats": float(event.offset),
            "duration_quarter_beats": float(event.quarterLength),
            "pitch_classes": pcs,
            "roman_numeral_hypothesis": roman_hypothesis,
            "roman_scale_degree_hypothesis": roman_scale_degree,
            "roman_inversion_hypothesis": roman_inversion,
            "candidate_not_verified_chord": True,
        })
    return {
        "engine": "music21.converter / KrumhanslSchmuckler / romanNumeralFromChord",
        "engine_version": music21.__version__,
        "key_hypothesis": {
            "tonic": estimated_key.tonic.name,
            "mode": estimated_key.mode,
            "correlation_not_probability": float(estimated_key.correlationCoefficient),
        },
        "axis": "estimated_score_quarter_beats",
        "limitations": ["chordification_is_not_functional_harmony_truth",
                        "midi_performance_timing_converted_to_estimated_score_time",
                        "global_key_is_assumed_for_roman_numerals",
                        "correlation_is_not_probability",
                        "not_a_direct_emotion_measure"],
        "sonorities": sonorities,
    }
