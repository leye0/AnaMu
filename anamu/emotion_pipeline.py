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
from .tempo_map import MidiTempoMap
from .vgmidi_temporal import enrich_published_mechanisms, extract_midi_measures


SCHEMA = "anamu-symbolic-emotions-ridge-v1"


def execute_original_jsymbolic(path: Path, jar: Path, *,
                               window_seconds: float = 10., timeout_seconds: int = 240) -> dict:
    """Execute real jSymbolic 2.2 on a new work and return its ACE windows.

    No network or fabricated substitution. The official tool can fail on
    individual works; callers should record this instead of making up data.
    """
    if not path.is_file() or not jar.is_file() or window_seconds <= 0:
        raise ValueError("missing_midi_or_original_jsymbolic_jar")
    with tempfile.TemporaryDirectory(prefix="anamu-original-jsymbolic-") as tmp:
        xml = Path(tmp) / "features.xml"
        definitions = Path(tmp) / "definitions.xml"
        completed = subprocess.run(
            ["java", "-Xmx3g", "-jar", str(jar.resolve()), "-csv", "-window",
             str(path.resolve()), str(xml), str(definitions), str(window_seconds), "0"],
            cwd=jar.resolve().parent, capture_output=True, text=True,
            timeout=timeout_seconds)
        if completed.returncode:
            raise RuntimeError("original_jsymbolic_failed:" + completed.stderr[-240:])
        if not xml.is_file():
            raise RuntimeError("original_jsymbolic_missing_ace")
        data = read_jsymbolic_ace(xml, max_bytes=200_000_000,
                                  nonfinite_as_missing=True)
        matched = [item for item in data["data_sets"]
                   if Path(item["source_id"]).name == path.name]
        if len(matched) != 1:
            raise RuntimeError("original_jsymbolic_no_unique_matching_source")
        return matched[0]


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
    estimates = predict_ridge_artifact(artifact, rows)
    names = artifact["feature_names"]
    used = sum(any(row.get(name) is not None and
                   isinstance(row[name], (int, float)) and math.isfinite(row[name])
                   for row in rows) for name in names)
    warnings = []
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
