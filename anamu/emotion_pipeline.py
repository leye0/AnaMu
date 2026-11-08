"""Reusable MIDI -> academic mechanisms -> calibrated emotion trajectory.

Feature extraction contains NO human labels. A model trained on other works
is required to estimate valence/arousal. The research tools and local theory
proxies remain independently identifiable; missing engines are not fabricated.
"""

from __future__ import annotations

import hashlib
import gzip
import io
import json
import math
import subprocess
import tempfile
from pathlib import Path

import numpy as np

from .academic_expectations import add_expectancy_observations
from .academic_fusion import (add_jsymbolic_ace, add_melody_library,
                              add_multiscale_motion, add_theory_observations)
from .expectation import VariableOrderExpectancy
from .jsymbolic_ace import read_jsymbolic_ace
from .jsymbolic_segments import split_midi_measures
from .tempo_map import MidiTempoMap
from .vgmidi_temporal import enrich_published_mechanisms, extract_midi_measures


SCHEMA = "anamu-symbolic-emotions-ridge-v1"


def execute_original_jsymbolic(path: Path, jar: Path, *,
                               window_seconds: float = 10., timeout_seconds: int = 240,
                               fallback_window_seconds: float | None = 30.,
                               fallback_timeout_seconds: int = 120) -> dict:
    """Execute real jSymbolic 2.2 on a new work and return its ACE windows.

    No network or fabricated substitution. The official tool can fail on
    individual works; callers should record this instead of making up data.
    """
    if not path.is_file() or not jar.is_file() or window_seconds <= 0:
        raise ValueError("missing_midi_or_original_jsymbolic_jar")
    if timeout_seconds <= 0 or fallback_timeout_seconds <= 0:
        raise ValueError("invalid_jsymbolic_timeout")
    if fallback_window_seconds is not None and fallback_window_seconds <= window_seconds:
        raise ValueError("fallback_window_must_be_longer")
    with tempfile.TemporaryDirectory(prefix="anamu-original-jsymbolic-") as tmp:
        xml = Path(tmp) / "features.xml"
        definitions = Path(tmp) / "definitions.xml"
        options = [(window_seconds, timeout_seconds)]
        if fallback_window_seconds is not None:
            options.append((fallback_window_seconds, fallback_timeout_seconds))
        for index, (actual_window, budget) in enumerate(options):
            xml.unlink(missing_ok=True)
            definitions.unlink(missing_ok=True)
            try:
                completed = subprocess.run(
                    ["java", "-Xmx3g", "-jar", str(jar.resolve()), "-csv", "-window",
                     str(path.resolve()), str(xml), str(definitions), str(actual_window), "0"],
                    cwd=jar.resolve().parent, capture_output=True, text=True,
                    timeout=budget)
            except subprocess.TimeoutExpired:
                # Longer windows mean fewer genuine Java sections. This is a
                # documented granularity change, never a synthetic substitute.
                if index + 1 == len(options):
                    raise
                continue
            if completed.returncode:
                raise RuntimeError("original_jsymbolic_failed:" + completed.stderr[-240:])
            break
        if not xml.is_file():
            raise RuntimeError("original_jsymbolic_missing_ace")
        data = read_jsymbolic_ace(xml, max_bytes=200_000_000,
                                  nonfinite_as_missing=True)
        matched = [item for item in data["data_sets"]
                   if Path(item["source_id"]).name == path.name]
        if len(matched) != 1:
            raise RuntimeError("original_jsymbolic_no_unique_matching_source")
        record = matched[0]
        record["anamu_extraction_window_seconds"] = actual_window
        record["anamu_window_fallback_used"] = actual_window != window_seconds
        return record


def execute_segmented_jsymbolic(path: Path, jar: Path, *,
                                max_measures: int = 16,
                                timeout_per_segment: int = 45) -> dict:
    """Run unchanged original jSymbolic on bounded, exact MIDI bar excerpts.

    Section features retain original seconds coordinates. Whole-piece features
    are intentionally NOT reconstructed from excerpts. Missing segments stay
    missing, with an explicit coverage warning and per-segment provenance.
    """
    if timeout_per_segment <= 0 or max_measures < 2:
        raise ValueError("invalid_segment_timeout")
    path = Path(path)
    total_measures = infer_measure_count(path)
    if total_measures > 256 or (total_measures + max_measures - 1) // max_measures > 16:
        raise ValueError("segmented_original_java_budget_exceeded")
    sections = []
    provenance = []
    with tempfile.TemporaryDirectory(prefix="anamu-jsymbolic-segments-") as tmp:
        excerpts = split_midi_measures(path, Path(tmp), measure_count=total_measures,
                                       max_measures=max_measures)
        for segment in excerpts:
            result = {"first_measure": segment.first_measure,
                      "last_measure": segment.stop_measure_exclusive - 1,
                      "midi_sha256": segment.source_sha256}
            try:
                record = execute_original_jsymbolic(
                    segment.path, jar, timeout_seconds=timeout_per_segment,
                    fallback_window_seconds=None)
                count = 0
                for window in record["windows"]:
                    left = window["start_seconds_if_j_symbolic_windowed"]
                    right = window["stop_seconds_if_j_symbolic_windowed"]
                    if left is None or right is None:
                        continue
                    start = max(segment.start_seconds, segment.start_seconds + left)
                    stop = min(segment.stop_seconds, segment.start_seconds + right)
                    if start >= stop:
                        continue
                    sections.append({**window,
                                     "start_seconds_if_j_symbolic_windowed": start,
                                     "stop_seconds_if_j_symbolic_windowed": stop})
                    count += 1
                result["status"] = "original_java_executed" if count else "no_timed_windows"
                result["window_count"] = count
            except (subprocess.TimeoutExpired, RuntimeError, ValueError, OSError) as exc:
                result["status"] = f"unavailable:{type(exc).__name__}"
                result["window_count"] = 0
            provenance.append(result)
    if not sections:
        raise RuntimeError("original_jsymbolic_no_segment_windows")
    return {
        "source_id": str(path), "whole_piece_features": {},
        "windows": sorted(sections, key=lambda w: w["start_seconds_if_j_symbolic_windowed"]),
        "anamu_segmented_original_java": True,
        "anamu_extraction_window_seconds": 10.,
        "anamu_original_java_segment_provenance": provenance,
        "anamu_original_java_segments_total": len(provenance),
        "anamu_original_java_segments_ok": sum(
            x["status"] == "original_java_executed" for x in provenance),
        "anamu_whole_piece_jsymbolic_features": "unavailable:segmented_not_equivalent",
        "anamu_midi_pairing_adjustments": {
            "discarded_unmatched_note_offs": excerpts[0].source_unmatched_note_off_count,
            "discarded_unclosed_note_ons": excerpts[0].source_unclosed_note_on_count,
        },
    }


def infer_measure_count(path: str | Path) -> int:
    """Derive a bar grid from completed MIDI notes when no human grid exists.

    The last sounding note determines length; arbitrary trailing MIDI silence
    does not. Non-constant metre is rejected rather than silently realigned.
    """
    import mido

    midi = mido.MidiFile(file=io.BytesIO(Path(path).read_bytes()))
    if midi.type == 2 or midi.ticks_per_beat <= 0:
        raise ValueError("unsupported_midi_timing")
    signatures = {(msg.numerator, msg.denominator) for track in midi.tracks
                  for msg in track if msg.type == "time_signature"}
    if len(signatures) > 1:
        raise ValueError("changing_time_signature")
    num, den = next(iter(signatures)) if signatures else (4, 4)
    bar_beats = num * 4 / den
    if not 1 <= bar_beats <= 12:
        raise ValueError("unsupported_meter")
    active: dict[tuple[int, int], list[int]] = {}
    last_end_tick = 0
    tick = 0
    for msg in mido.merge_tracks(midi.tracks):
        tick += msg.time
        if msg.type not in ("note_on", "note_off") or msg.channel == 9:
            continue
        token = (msg.channel, msg.note)
        if msg.type == "note_on" and msg.velocity > 0:
            active.setdefault(token, []).append(tick)
        elif active.get(token):
            start = active[token].pop(0)
            if tick > start:
                last_end_tick = max(last_end_tick, tick)
    if not last_end_tick:
        raise ValueError("empty_or_unterminated_midi")
    measures = math.ceil(last_end_tick / midi.ticks_per_beat / bar_beats - 1e-9)
    if not 1 <= measures <= 512:
        raise ValueError("unsupported_measure_count")
    return measures


def extract_academic_rows(path: str | Path, n_measures: int, *,
                          academic: bool = True, full_fusion: bool = True,
                          jsymbolic_record: dict | None = None,
                          expectancy_models: dict | None = None) -> tuple[list[dict], dict, dict]:
    """Single shared extraction path for benchmark training AND new music."""
    path = Path(path)
    rows, meta = extract_midi_measures(path, n_measures)
    status = {}
    if academic:
        status.update(enrich_published_mechanisms(path, rows, meta["beats_per_measure"]))
    if full_fusion:
        local = add_theory_observations(path, rows, meta["beats_per_measure"])
        status["theory_probes"] = local["status"]
        try:
            melody = add_melody_library(path, rows, meta["beats_per_measure"],
                                        allow_skyline=True)
            status["melody_features"] = melody["status"]
            status["melody_method"] = melody.get("extraction_methods", [])
        except (ValueError, RuntimeError, IndexError, ZeroDivisionError,
                TypeError, KeyError) as exc:
            status["melody_features"] = f"unavailable:{type(exc).__name__}"
        if jsymbolic_record is not None:
            ace = {"data_set_count": 1, "data_sets": [jsymbolic_record]}
            aligned = add_jsymbolic_ace(rows, ace, MidiTempoMap.from_bytes(path.read_bytes()),
                                        meta["beats_per_measure"])
            status["jsymbolic"] = aligned["status"]
        else:
            status["jsymbolic"] = "unavailable:no_original_java_output"
        if expectancy_models is not None:
            exp = add_expectancy_observations(path, rows, meta["beats_per_measure"],
                                              expectancy_models)
            status["expectancy_baseline"] = exp["status"]
            motion = add_multiscale_motion(rows)
            status["temporal_memory_derivatives"] = motion[
                "original_signals_with_temporal_derivatives"]
    return rows, meta, status


def export_ridge_artifact(path: Path, model, feature_names: list[str],
                          expectancy_models: dict, *, metadata: dict) -> dict:
    """Save a safe JSON model: no pickle, no remote code on load.

    Includes trained n-gram statistics, imputation, scaling and Ridge weights,
    so new pieces use the EXACT feature order and model semantics.
    """
    from sklearn.linear_model import Ridge
    from sklearn.pipeline import Pipeline

    if not isinstance(model, Pipeline) or not isinstance(model.named_steps.get("model"), Ridge):
        raise ValueError("only_fitted_ridge_models_are_exportable")
    imputer = model.named_steps["missing"]
    scale = model.named_steps["scale"]
    linear = model.named_steps["model"]
    artifact = {
        "schema": SCHEMA,
        "feature_names": feature_names,
        "numeric_model": {
            "imputation_medians": imputer.statistics_.tolist(),
            "missing_indicator_indices": imputer.indicator_.features_.tolist(),
            "scale_means": scale.mean_.tolist(),
            "scale_factors": scale.scale_.tolist(),
            "coefficients": linear.coef_.tolist(),
            "intercepts": linear.intercept_.tolist(),
        },
        "expectancy_models": {name: model.to_state()
                              for name, model in expectancy_models.items()},
        "metadata": metadata,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(artifact, ensure_ascii=False, allow_nan=False,
                               separators=(",", ":")) + "\n", encoding="utf-8")
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size, "format": SCHEMA}


def load_ridge_artifact(path: str | Path) -> dict:
    path = Path(path)
    # A checked-in, gzip-compressed numerical artifact avoids retraining on
    # each analysis. Plain JSON research outputs remain supported.
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8") as stream:
            artifact = json.load(stream)
    else:
        artifact = json.loads(path.read_text(encoding="utf-8"))
    if artifact.get("schema") != SCHEMA or not artifact.get("feature_names"):
        raise ValueError("unsupported_emotion_model_artifact")
    required = ("imputation_medians", "missing_indicator_indices", "scale_means",
                "scale_factors", "coefficients", "intercepts")
    numeric = artifact["numeric_model"]
    if any(key not in numeric for key in required):
        raise ValueError("incomplete_emotion_model_artifact")
    n_features = len(artifact["feature_names"])
    expected = n_features + len(numeric["missing_indicator_indices"])
    if (len(numeric["imputation_medians"]) != n_features or
        len(numeric["scale_means"]) != expected or
        len(numeric["scale_factors"]) != expected or
        len(numeric["coefficients"]) != 2 or
        any(len(coef) != expected for coef in numeric["coefficients"]) or
        len(numeric["intercepts"]) != 2 or
        any(not 0 <= int(index) < n_features for index in numeric["missing_indicator_indices"])):
        raise ValueError("emotion_model_dimensions_mismatch")
    return artifact


def predict_ridge_artifact(artifact: dict, rows: list[dict]) -> np.ndarray:
    """Perform exactly the saved sklearn impute → scale → ridge transform."""
    numeric = artifact["numeric_model"]
    names = artifact["feature_names"]
    matrix = np.asarray([[float(row[name]) if row.get(name) is not None and
                          math.isfinite(float(row[name])) else np.nan for name in names]
                         for row in rows], dtype=float)
    unknown = np.isnan(matrix)
    medians = np.asarray(numeric["imputation_medians"], dtype=float)
    matrix = np.where(unknown, medians, matrix)
    missing = numeric["missing_indicator_indices"]
    if missing:
        matrix = np.column_stack((matrix, unknown[:, missing].astype(float)))
    center = np.asarray(numeric["scale_means"], dtype=float)
    scale = np.asarray(numeric["scale_factors"], dtype=float)
    weights = np.asarray(numeric["coefficients"], dtype=float)
    offsets = np.asarray(numeric["intercepts"], dtype=float)
    return np.clip(((matrix - center) / scale) @ weights.T + offsets, -1, 1)


def analyze_known_midi(path: str | Path, artifact: dict, *,
                       jsymbolic_record: dict | None = None,
                       n_measures: int | None = None) -> dict:
    """Analyze existing music with trained human calibration, no ground truth."""
    path = Path(path)
    if n_measures is None:
        n_measures = infer_measure_count(path)
    models = {name: VariableOrderExpectancy.from_state(state)
              for name, state in artifact["expectancy_models"].items()}
    rows, metadata, engines = extract_academic_rows(
        path, n_measures, jsymbolic_record=jsymbolic_record, expectancy_models=models)
    if jsymbolic_record is not None and "anamu_extraction_window_seconds" in jsymbolic_record:
        engines["jsymbolic_original_window_seconds"] = jsymbolic_record[
            "anamu_extraction_window_seconds"]
    if jsymbolic_record is not None and jsymbolic_record.get("anamu_segmented_original_java"):
        engines["jsymbolic_original_segments_ok"] = jsymbolic_record[
            "anamu_original_java_segments_ok"]
        engines["jsymbolic_original_segments_total"] = jsymbolic_record[
            "anamu_original_java_segments_total"]
        engines["jsymbolic_original_whole_piece_features"] = "unavailable:segmented"
        engines["jsymbolic_original_segment_provenance"] = jsymbolic_record[
            "anamu_original_java_segment_provenance"]
        engines["jsymbolic_segment_midi_pairing_adjustments"] = jsymbolic_record[
            "anamu_midi_pairing_adjustments"]
    estimates = predict_ridge_artifact(artifact, rows)
    names = artifact["feature_names"]
    used = sum(any(row.get(name) is not None and
                   isinstance(row[name], (int, float)) and math.isfinite(row[name])
                   for row in rows) for name in names)
    warnings = []
    if jsymbolic_record is not None and jsymbolic_record.get("anamu_window_fallback_used"):
        warnings.append("original jSymbolic used longer windows after timeout; "
                        "temporal resolution differs from 10-second training windows")
    if jsymbolic_record is not None and jsymbolic_record.get("anamu_segmented_original_java"):
        warnings.append("original jSymbolic executed on bounded MIDI segments, "
                        "with note clipping at artificial boundaries; global original "
                        "features unavailable and imputed")
        if any(jsymbolic_record["anamu_midi_pairing_adjustments"].values()):
            warnings.append("source MIDI contained malformed unmatched note events; "
                            "unpaired note events excluded from Java excerpts, quantified "
                            "in engine_status")
        if (jsymbolic_record["anamu_original_java_segments_ok"] !=
                jsymbolic_record["anamu_original_java_segments_total"]):
            warnings.append("original jSymbolic only covered some MIDI segments; "
                            "uncovered windows imputed")
    if engines.get("jsymbolic") != "ok" and any(name.startswith("jsym_") for name in names):
        warnings.append("original jSymbolic unavailable: model imputes its features")
    if any(name.startswith("idyom_") for name in names):
        warnings.append("original IDyOM features not included in this standalone pipeline")
    warnings.append("estimated human-perceived valence/arousal, NOT measured human emotions")
    warnings.append("VGMIDI piano calibration may not generalize to other eras, styles or instrumentation")
    return {
        "source_midi": path.name,
        "source_sha256": metadata["source_sha256"],
        "measure_count": n_measures,
        "model_schema": artifact["schema"],
        "engine_status": engines,
        "available_feature_columns": used,
        "trained_feature_columns": len(names),
        "warnings": warnings,
        "emotion_trajectory": [{"measure": i + 1,
                                "valence": float(pair[0]), "arousal": float(pair[1])}
                               for i, pair in enumerate(estimates)],
    }
