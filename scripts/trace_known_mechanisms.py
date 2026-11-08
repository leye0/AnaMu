"""Attach original MIDI-theory measurements to existing emotion trajectories.

The trace is observational, not a causal attribution of emotion. It uses the
same academic feature extractor, but never reuses listener ratings as inputs.
For timing and identity integrity, the MIDI SHA must exactly match the report.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
from pathlib import Path

from anamu.emotion_pipeline import extract_academic_rows, load_ridge_artifact
from anamu.expectation import VariableOrderExpectancy


# Selected interpretable views; the calibrated model itself still receives
# ALL 1,198 features. The names are genuine extractor keys, not re-creations.
MECHANISMS = {
    "tension.tensile_strain": ("partitura_tensile_strain", "original_partitura"),
    "tension.cloud_diameter": ("partitura_cloud_diameter", "original_partitura"),
    "tension.cloud_momentum": ("partitura_cloud_momentum", "original_partitura"),
    "harmony.key_correlation_not_probability": ("music21_key_correlation", "original_music21"),
    "harmony.roman_function_changes": ("music21_roman_changes", "original_music21"),
    "harmony.dominant_to_tonic": ("music21_dominant_to_tonic_hypotheses", "original_music21"),
    "melody.narmour_closure": ("narmour.closure_mean", "original_melody_features"),
    "melody.narmour_proximity": ("narmour.proximity_mean", "original_melody_features"),
    "melody.narmour_registral_return": ("narmour.registral_return_mean", "original_melody_features"),
    "expectancy.melodic_surprisal": ("ngram_melodic_interval.surprisal_mean", "trained_ngram_proxy"),
    "expectancy.melodic_entropy": ("ngram_melodic_interval.entropy_before_mean", "trained_ngram_proxy"),
    "expectancy.harmonic_surprisal": ("ngram_harmonic_sonority.surprisal_mean", "trained_ngram_proxy"),
    "rhythm.syncopated_sustains": ("theory_syncopated_sustains", "local_theory_proxy"),
    "texture.note_density": ("note_density", "midi_observation"),
    "texture.mean_velocity": ("mean_velocity", "midi_observation"),
    "texture.vertical_interval_clash_proxy": ("vertical_interval_clash", "symbolic_interval_proxy"),
    "resolution.symbolic_dissonance_release": ("theory_symbolic_dissonance_release", "local_theory_proxy"),
    "repetition.melodic_motif_familiarity": ("theory_melodic_motif_previous_appearances", "local_theory_proxy"),
}


def build_trace(report_path: Path, model_path: Path) -> dict:
    report = json.loads(report_path.read_text(encoding="utf-8"))
    model_bytes = model_path.read_bytes()
    if model_path.suffix == ".gz":
        model_bytes = gzip.decompress(model_bytes)
    if report.get("calibrated_artifact_sha256") != hashlib.sha256(model_bytes).hexdigest():
        raise ValueError("emotion_report_and_mechanism_model_do_not_match")
    artifact = load_ridge_artifact(model_path)
    models = {name: VariableOrderExpectancy.from_state(state)
              for name, state in artifact["expectancy_models"].items()}
    pieces = []
    for analysis in report["analyses"]:
        path = report_path.parent / analysis["source_midi"]
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != analysis["source_sha256"]:
            raise ValueError(f"source_midi_missing_or_checksum_changed:{analysis['source_midi']}")
        rows, _, engines = extract_academic_rows(path, analysis["measure_count"],
                                                  expectancy_models=models)
        emotion_rows = analysis["emotion_trajectory"]
        if len(rows) != len(emotion_rows):
            raise ValueError(f"unaligned_emotion_and_mechanism_bars:{path.name}")
        trajectory = []
        for i, (row, emotion) in enumerate(zip(rows, emotion_rows)):
            if emotion["measure"] != i + 1:
                raise ValueError(f"incorrect_measure_order:{path.name}")
            values = {}
            for label, (key, _) in MECHANISMS.items():
                value = row.get(key)
                values[label] = (float(value) if isinstance(value, (int, float))
                                 and math.isfinite(float(value)) else None)
            trajectory.append({"measure": i + 1,
                               "emotion_estimate": {"valence": emotion["valence"],
                                                    "arousal": emotion["arousal"]},
                               "observed_mechanisms": values})
        pieces.append({"composition": analysis.get("known_composition", path.name),
                       "source_sha256": analysis["source_sha256"],
                       "engine_status_without_java": engines,
                       "trajectory": trajectory})
    return {
        "scope": "same MIDI and measures as emotional analysis; mechanism observations are not human emotion labels",
        "causality": "no causal claims: juxtaposition does not establish that a mechanism caused the reported emotion",
        "java_note": "original Java output cannot be reconstructed from this trace; jSymbolic contributions stay in the emotion report only",
        "selected_mechanisms": {k: {"source_feature": v[0], "origin": v[1]}
                                for k, v in MECHANISMS.items()},
        "pieces": pieces,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--model", type=Path,
                        default=Path("models/vgmidi-piano-ridge.json.gz"))
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    traced = build_trace(args.report, args.model)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(traced, separators=(",", ":"),
                                   ensure_ascii=False, allow_nan=False)
                        + "\n", encoding="utf-8")
    print(f"Mechanism timelines on {len(traced['pieces'])} known works: {args.out}")


if __name__ == "__main__":
    main()
