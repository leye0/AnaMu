"""Time-aligned, provenance-preserving fusion of independent music theories.

All values in this module describe *existing music*, not emotional labels.
Original engines are deliberately distinguished from our explicitly named
theory-inspired operationalizations. MIDI remains the authoritative input.
"""

from __future__ import annotations

import io
import math
import statistics
from collections import Counter
from pathlib import Path

from .tempo_map import MidiTempoMap


THEORY_REGISTRY = {
    "M1": "statistical_melodic_expectancy",
    "M2": "narmour_implication_realization",
    "M3": "statistical_harmonic_expectancy",
    "M4": "chew_herremans_tonal_tension",
    "M5": "krumhansl_schmuckler_key",
    "M6": "roman_harmonic_functions",
    "M7": "tonal_pitch_space_proxy_not_lerdahl_original",
    "M8": "cadential_resolution_hypotheses",
    "M9": "melodic_rhythmic_motifs",
    "M10": "phrasing_segmentation_proxies",
    "M11": "metric_accents",
    "M12": "metrical_syncopation_proxies",
    "M13": "jsymbolic_polyphony_texture",
    "M14": "articulation_dynamics",
    "M15": "symbolic_dissonance_not_acoustic_roughness",
    "M16": "voice_leading_hypotheses",
    "M17": "temporal_tension_memory_inspired_by_farbood",
    "M18": "entropy_surprisal_interaction_inspired_by_cheung",
    "M19": "itpra_framework_not_directly_observable",
    "M20": "style_memory_and_local_familiarity",
    "M21": "style_descriptors_from_existing_engines",
    "M22": "supervised_emotion_trajectory",
    "M23": "human_annotator_variation_evaluation_only",
}


def mechanism_execution_audit(piece_statuses: dict) -> dict:
    """Every catalogued research mechanism gets an honest provenance status."""
    count = len(piece_statuses)
    melody = sum(p.get("melody_features") == "ok" for p in piece_statuses.values())
    jsym = sum(p.get("jsymbolic") == "ok" for p in piece_statuses.values())
    partitura = sum(p.get("partitura") == "ok" for p in piece_statuses.values())
    music21 = sum(p.get("music21") == "ok" for p in piece_statuses.values())
    ngram = sum(p.get("expectancy_baseline") == "ok" for p in piece_statuses.values())
    idyom = sum(p.get("original_idyom") == "ok" for p in piece_statuses.values())
    local = sum(p.get("theory_probes") == "ok" for p in piece_statuses.values())
    original = {
        "M2": ("melody-features 1.3.3 / Narmour", melody),
        "M4": ("Partitura / Herremans-Chew", partitura),
        "M5": ("music21 / Krumhansl-Schmuckler", music21),
        "M6": ("music21 / Roman-numeral hypotheses", music21),
        "M9": ("melody-features / melodic motifs", melody),
        "M11": ("jSymbolic 2.2 + melody-features", max(melody, jsym)),
        "M12": ("jSymbolic 2.2 + melody-features", max(melody, jsym)),
        "M13": ("jSymbolic 2.2 original Java", jsym),
        "M14": ("jSymbolic 2.2 original Java", jsym),
        "M21": ("jSymbolic 2.2 + melody-features descriptors", max(melody, jsym)),
    }
    approximations = {
        "M1": ("train-only variable-order ngram, explicitly NOT original IDyOM", ngram),
        "M3": ("train-only sonority ngram, unverified chord tokenization", ngram),
        "M7": ("tonic-chord and fifth-distance proxy, NOT Lerdahl TPS", local),
        "M8": ("tonic-restoration and dominant-to-tonic proxy", local),
        "M10": ("measure-boundary rests and motif grouping proxy", local),
        "M15": ("MIDI vertical interval clash, NOT acoustic roughness", local),
        "M16": ("independent track-direction proxy; voice identity unverified", local),
        "M17": ("multiscale feature memory, NOT fitted Farbood original", local),
        "M18": ("entropy/surprisal interaction on training-only ngrams", ngram),
        "M20": ("within-piece motif repetition and training-only ngram", local),
    }
    audit = {}
    for code, name in THEORY_REGISTRY.items():
        if code == "M1" and idyom:
            engine, available, status = "IDyOM original (audited Lisp .dat output)", idyom, "published_engine_output_imported"
        elif code in original:
            engine, available = original[code]
            status = "published_engine_executed" if available else "unavailable"
        elif code in approximations:
            engine, available = approximations[code]
            status = "theory_inspired_proxy_not_full_replication" if available else "unavailable"
        elif code == "M19":
            engine, available, status = "Huron ITPRA: cognitive framework, not inferred mental states", 0, "framework_only"
        elif code == "M22":
            engine, available, status = "supervised human-valence/arousal regression", count, "evaluated_against_humans"
        elif code == "M23":
            engine, available, status = "median and quartiles of real raters, evaluation side only", count, "human_labels_preserved_not_features"
        else:
            engine, available, status = "not implemented", 0, "unavailable"
        audit[code] = {"mechanism": name, "implementation": engine,
                       "status": status, "pieces_with_engine": available,
                       "eligible_pieces": count}
    return audit


def _mean(values):
    valid = [float(x) for x in values if x is not None and math.isfinite(float(x))]
    return statistics.mean(valid) if valid else None


def _std(values):
    valid = [float(x) for x in values if x is not None and math.isfinite(float(x))]
    return statistics.pstdev(valid) if len(valid) > 1 else (0.0 if valid else None)


def _flatten_numeric(value, prefix: str, *, max_dimension: int = 24):
    """Preserve bounded named dimensions; never convert categorical data to numbers."""
    if isinstance(value, bool):
        return {prefix: float(value)}
    if isinstance(value, (int, float)) and math.isfinite(float(value)):
        return {prefix: float(value)}
    if isinstance(value, dict):
        if len(value) > max_dimension:
            return {}
        result = {}
        for key, part in value.items():
            result.update(_flatten_numeric(part, f"{prefix}.{key}"))
        return result
    if isinstance(value, (list, tuple)) and len(value) <= max_dimension:
        result = {}
        for i, part in enumerate(value):
            result.update(_flatten_numeric(part, f"{prefix}.{i}"))
        return result
    return {}


def _melody_numeric_descriptor(value, prefix: str) -> dict[str, float]:
    """Represent published multi-valued melody features in a *fixed* space.

    Free-form dict keys such as motif strings and n-gram fingerprints must
    NOT become new columns for each piece. Preserve bounded, known histogram
    domains when appropriate; summarize all other collections by their shape
    and numeric distribution. The original raw values remain available from
    ``extract_melody_toolbox`` for detailed, lossless inspection.
    """
    if isinstance(value, bool):
        return {prefix: float(value)}
    if isinstance(value, (int, float)):
        return {prefix: float(value)} if math.isfinite(float(value)) else {}
    if not isinstance(value, (dict, list, tuple)):
        return {}
    result = {}
    if isinstance(value, dict):
        # Only explicitly bounded musical domains can be expanded losslessly.
        if "pitch_class_histogram" in prefix.lower() or "pitch_class_distribution" in prefix.lower():
            for pc in range(12):
                v = value.get(str(pc), value.get(pc, 0))
                if isinstance(v, (int, float)) and math.isfinite(float(v)):
                    result[f"{prefix}.pc{pc:02d}"] = float(v)
        elif "basic_pitch_histogram" in prefix.lower():
            for pitch in range(128):
                v = value.get(str(pitch), value.get(pitch, 0))
                if isinstance(v, (int, float)) and math.isfinite(float(v)):
                    result[f"{prefix}.pitch{pitch:03d}"] = float(v)
    # For all arbitrary motif/pattern/category dictionaries and variable-
    # length vectors, the numeric summary has an invariant schema. Null and
    # categorical leaves are excluded, not encoded as zeros.
    numbers = []
    def collect(item):
        if len(numbers) >= 10_000:
            return
        if isinstance(item, (int, float, bool)) and math.isfinite(float(item)):
            numbers.append(float(item))
        elif isinstance(item, dict):
            for part in item.values():
                collect(part)
        elif isinstance(item, (list, tuple)):
            for part in item:
                collect(part)
    collect(value)
    if numbers:
        result.update({
            prefix + ".value_count": len(numbers),
            prefix + ".value_sum": sum(numbers),
            prefix + ".value_mean": statistics.mean(numbers),
            prefix + ".value_std": statistics.pstdev(numbers) if len(numbers) > 1 else 0.,
            prefix + ".value_min": min(numbers),
            prefix + ".value_max": max(numbers),
            prefix + ".value_zero_fraction": sum(x == 0 for x in numbers) / len(numbers),
        })
        if min(numbers) >= 0 and sum(numbers) > 0:
            total = sum(numbers)
            result[prefix + ".distribution_entropy"] = -sum(
                (x / total) * math.log2(x / total) for x in numbers if x > 0)
    return result


def _notes(midi_path):
    import mido

    contents = Path(midi_path).read_bytes()
    midi = mido.MidiFile(file=io.BytesIO(contents))
    if midi.type == 2 or midi.ticks_per_beat <= 0:
        raise ValueError("unsupported_polyphonic_midi_clock")
    tracks = []
    for track_idx, track in enumerate(midi.tracks):
        pos = 0
        active = {}
        for message in track:
            pos += message.time
            if message.type not in ("note_on", "note_off") or message.channel == 9:
                continue
            key = (message.channel, message.note)
            if message.type == "note_on" and message.velocity > 0:
                active.setdefault(key, []).append((pos, message.velocity))
            elif active.get(key):
                start, velocity = active[key].pop(0)
                if pos > start:
                    tracks.append((start / midi.ticks_per_beat,
                                   pos / midi.ticks_per_beat,
                                   message.note, velocity, track_idx, message.channel))
    return sorted(tracks, key=lambda n: (n[0], n[2])), contents


def _signature(group, *, rhythmic=False):
    events = sorted(group, key=lambda n: (n[0], n[2]))
    if len(events) < 3:
        return None
    # Intervals are transposition-invariant; quantized distances and durations
    # are robust to mild expressive timing (but not tempo-invariant).
    events = events[:8]
    if rhythmic:
        gaps = [b[0] - a[0] for a, b in zip(events, events[1:])]
        unit = max(statistics.median(gaps), .0625)
        return tuple(round(g / unit * 2) / 2 for g in gaps)
    return tuple(b[2] - a[2] for a, b in zip(events, events[1:]))


def add_theory_observations(path: str | Path, rows: list[dict], beats_per_measure: float) -> dict:
    """Distinct theoretical proxy families with explicit assumptions.

    These quantities are retrospective musical observations; the Farbood and
    Cheung interactions below are operational hypotheses, not replications of
    those authors' original fitted perceptual experiments.
    """
    notes, _ = _notes(path)
    if not rows or not notes or beats_per_measure <= 0:
        raise ValueError("invalid_symbolic_theory_input")
    groups = [[] for _ in rows]
    for event in notes:
        idx = int(event[0] / beats_per_measure)
        if 0 <= idx < len(rows):
            groups[idx].append(event)
    motifs = Counter()
    rhythms = Counter()
    prev_pcs = None
    prev_density = None
    prev_velocity = None
    prev_clash = None
    prev_tonic = None
    prev_dominant = None
    recent_energy = []
    recent_contour = []
    for i, (row, notes_in_bar) in enumerate(zip(rows, groups)):
        left = i * beats_per_measure
        pitches = [n[2] for n in notes_in_bar]
        onset_beats = [n[0] - left for n in notes_in_bar]
        total = len(notes_in_bar)
        onsets = sorted({round(t, 4) for t in onset_beats})
        durations = [n[1] - n[0] for n in notes_in_bar]
        long_notes = [n for n in notes_in_bar if n[1] - n[0] >= .75]
        # Metric weight: 1 on the bar, 1/2 on beat, 1/4 on half beat, etc.
        def metric_strength(beat):
            if abs(beat) < .09:
                return 1.0
            if abs(beat - round(beat)) < .09:
                return .65
            if abs(beat * 2 - round(beat * 2)) < .1:
                return .4
            return .18
        weights = [metric_strength(t) for t in onset_beats]
        weighted_offbeat = sum((1 - w) * n[3] / 127 for w, n in zip(weights, notes_in_bar))
        # Long accented notes on weak subdivisions are a metric-displacement
        # proxy, not a published Longuet-Higgins/Lee score reproduction.
        syn = sum((1 - w) * n[3] / 127 for w, n in zip(weights, notes_in_bar)
                  if n[1] - n[0] >= .5) / max(total, 1)
        pcs = Counter(p % 12 for p in pitches)
        pc_vec = tuple(pcs.get(x, 0) / max(total, 1) for x in range(12))
        tonic = row.get("music21_tonic_pc")
        mode_minor = row.get("music21_key_is_minor")
        if tonic is not None:
            tonic = int(tonic)
            triad = {(tonic + step) % 12 for step in (
                0, 3 if mode_minor else 4, 7)}
            tonic_weight = pc_vec[tonic]
            dominant_weight = pc_vec[(tonic + 7) % 12]
            triad_weight = sum(pc_vec[pc] for pc in triad)
            fifth_distance = _mean([min((pc - tonic) * 7 % 12,
                                        (tonic - pc) * 7 % 12)
                                    for pc in pitches])
        else:
            tonic_weight = dominant_weight = triad_weight = fifth_distance = None
        change = (sum(abs(a - b) for a, b in zip(pc_vec, prev_pcs)) / 2
                  if prev_pcs is not None else None)
        sig = _signature(notes_in_bar)
        rhysig = _signature(notes_in_bar, rhythmic=True)
        motif_familiarity = motifs.get(sig, 0) if sig is not None else None
        rhythm_familiarity = rhythms.get(rhysig, 0) if rhysig is not None else None
        if sig is not None:
            motifs[sig] += 1
        if rhysig is not None:
            rhythms[rhysig] += 1
        intervals = [b[2] - a[2] for a, b in zip(notes_in_bar, notes_in_bar[1:])]
        # Adjacent pitch arrivals are NOT verified voice-leading. Report only
        # average contrary motion among simultaneous track-local sequences.
        per_part = {}
        for event in notes_in_bar:
            per_part.setdefault((event[4], event[5]), []).append(event)
        part_steps = [part[-1][2] - part[0][2] for part in per_part.values()
                      if len(part) >= 2]
        contrary = (sum(a * b < 0 for j, a in enumerate(part_steps)
                        for b in part_steps[j + 1:]) /
                    max(len(part_steps) * (len(part_steps) - 1) / 2, 1))
        velocity = row.get("mean_velocity")
        density = row.get("note_density")
        clash = row.get("vertical_interval_clash")
        onset_span = (max(onsets) - min(onsets)) if len(onsets) > 1 else None
        row.update({
            "theory_beat_accent_strength": _mean(weights),
            "theory_velocity_weighted_displacement": weighted_offbeat / max(total, 1),
            "theory_syncopated_sustains": syn,
            "theory_onset_span_beats": onset_span,
            "theory_long_note_fraction": len(long_notes) / max(total, 1),
            "theory_articulation_ratio": _mean([min(n[1] - n[0], beats_per_measure) /
                                                  max(beats_per_measure, .1) for n in notes_in_bar]),
            "theory_accented_attack_velocity": _mean([n[3] for n, w in zip(notes_in_bar, weights) if w >= .65]),
            "theory_offbeat_attack_velocity": _mean([n[3] for n, w in zip(notes_in_bar, weights) if w < .65]),
            "theory_local_pitch_class_change": change,
            "theory_key_triad_pitch_fraction": triad_weight,
            "theory_circle_of_fifths_distance_proxy": fifth_distance,
            "theory_dominant_to_tonic_proxy": (
                prev_dominant * tonic_weight if prev_dominant is not None and tonic_weight is not None
                else None),
            "theory_tonic_restoration_proxy": (
                max(tonic_weight - prev_tonic, 0) if tonic_weight is not None and prev_tonic is not None
                else None),
            "theory_melodic_motif_previous_appearances": motif_familiarity,
            "theory_rhythmic_motif_previous_appearances": rhythm_familiarity,
            "theory_melodic_contour_repeated": int(sig in recent_contour) if sig is not None else None,
            "theory_melodic_large_leap_fraction": (sum(abs(x) >= 7 for x in intervals) /
                                                   len(intervals)) if intervals else None,
            "theory_contrary_track_movement_proxy": contrary if len(part_steps) > 1 else None,
            "theory_dynamics_change": velocity - prev_velocity if velocity is not None and prev_velocity is not None else None,
            "theory_density_change": density - prev_density if density is not None and prev_density is not None else None,
            "theory_dissonance_change": clash - prev_clash if clash is not None and prev_clash is not None else None,
            "theory_symbolic_dissonance_release": max(prev_clash - clash, 0) if clash is not None and prev_clash is not None else None,
            "theory_phrase_boundary_rest_fraction": (max(0., beats_per_measure -
                                                  (max(n[1] for n in notes_in_bar) - left)) /
                                                  beats_per_measure if notes_in_bar else 1.0),
        })
        # Simple temporal-memory probes at multiple scales. These are not the
        # Farbood calibrated perceptual weights; calibrate with humans later.
        energy = (_mean([density, row.get("mean_polyphony"),
                        (velocity / 127 if velocity is not None else None), clash]) or 0)
        recent_energy.append(energy)
        for width in (2, 4, 8):
            previous = recent_energy[max(0, len(recent_energy) - width):]
            row[f"theory_memory_energy_{width}bars"] = _mean(previous)
            row[f"theory_memory_energy_volatility_{width}bars"] = _std(previous)
        row["theory_memory_energy_growth_4bars"] = (energy - recent_energy[-4]
            if len(recent_energy) >= 4 else None)
        if sig is not None:
            recent_contour.append(sig)
            recent_contour = recent_contour[-8:]
        prev_pcs, prev_density, prev_velocity, prev_clash = pc_vec, density, velocity, clash
        prev_tonic, prev_dominant = tonic_weight, dominant_weight
    return {"source": "M7-M20 distinct theory-inspired symbolic probes",
            "status": "ok", "origin": "local approximations, not original calibrated theory implementations",
            "families": ["M7", "M8", "M9", "M10", "M11", "M12", "M14", "M15", "M16", "M17", "M20"]}


def add_melody_library(path: str | Path, rows: list[dict], beats_per_measure: float,
                       *, allow_skyline: bool = False) -> dict:
    """Use original melody-features library; show monophony coverage honestly.

    Optional skyline extraction is a declared *hypothesis*, never a detected
    ground-truth melody. By default only proven monophonic track/channels pass.
    """
    from .melody_toolbox import extract_melody_toolbox

    output = extract_melody_toolbox(path, fallback_skyline=allow_skyline)
    if output["status"] != "features_extracted":
        return {"status": output["status"], "monophonic_parts": 0,
                "missing_reason": "no_sufficient_melodic_candidate"}
    timing = MidiTempoMap.from_bytes(Path(path).read_bytes())
    parts = output["parts"]
    numeric_features = {}
    for part in parts:
        for name, value in part["features"].items():
            for full_name, number in _melody_numeric_descriptor(value, f"melody_{name}").items():
                numeric_features.setdefault(full_name, []).append(number)
    for row in rows:
        for key, values in numeric_features.items():
            row[key] = _mean(values)
    # Narmour events arrive in performance seconds and are assigned by true
    # MIDI tempo map; a late event is never shifted into another bar.
    by_measure = [[] for _ in rows]
    for part in parts:
        for event in part["narmour_triplet_realizations"]:
            beat = timing.seconds_to_beats(event["time_seconds"])
            idx = int(beat / beats_per_measure)
            if 0 <= idx < len(rows):
                by_measure[idx].append(event["scores"])
    for idx, events in enumerate(by_measure):
        per_score = {}
        for event in events:
            for key, value in _flatten_numeric(event, "narmour").items():
                per_score.setdefault(key, []).append(value)
        for key, values in per_score.items():
            rows[idx][f"{key}_mean"] = _mean(values)
            rows[idx][f"{key}_std"] = _std(values)
        rows[idx]["narmour_triplet_count"] = len(events)
    return {"status": "ok", "engine": output["engine"],
            "version": output["engine_version"], "monophonic_parts": len(parts),
            "global_numeric_columns": len(numeric_features),
            "narmour_events": sum(map(len, by_measure)),
            "candidate_melody_not_verified": True,
            "extraction_methods": sorted({p["extraction_method"] for p in parts})}


def add_jsymbolic_ace(rows: list[dict], ace: dict, timing: MidiTempoMap,
                      beats_per_measure: float, *, prefix: str = "jsym") -> dict:
    """Project *actual original Java* jSymbolic seconds windows onto MIDI bars.

    Weighted by intersection duration, with missing values left missing.
    Global features are tagged separately so they cannot be mistaken for a
    changing emotion along the piece.
    """
    if ace["data_set_count"] != 1:
        raise ValueError("jsymbolic_requires_single_midi_ace")
    data = ace["data_sets"][0]
    globals_ = {}
    for name, value in data["whole_piece_features"].items():
        globals_.update(_flatten_numeric(value, f"{prefix}_global.{name}"))
    windows = []
    for window in data["windows"]:
        start, stop = window["start_seconds_if_j_symbolic_windowed"], window["stop_seconds_if_j_symbolic_windowed"]
        if start is None or stop is None:
            continue
        values = {}
        for name, value in window["features"].items():
            values.update(_flatten_numeric(value, f"{prefix}_window.{name}"))
        windows.append((start, stop, values))
    for index, row in enumerate(rows):
        row.update(globals_)
        left = timing.beats_to_seconds(index * beats_per_measure)
        right = timing.beats_to_seconds((index + 1) * beats_per_measure)
        overlaps = [(max(0, min(right, stop) - max(left, start)), value)
                    for start, stop, value in windows if start < right and stop > left]
        buckets = {}
        for weight, values in overlaps:
            for key, value in values.items():
                buckets.setdefault(key, []).append((weight, value))
        for key, values in buckets.items():
            total = sum(weight for weight, _ in values)
            if total:
                row[key] = sum(weight * number for weight, number in values) / total
        row[f"{prefix}_window_coverage_seconds"] = sum(weight for weight, _ in overlaps)
    return {"status": "ok" if windows else "no_timed_windows",
            "engine": "original jSymbolic Java ACE XML", "window_count": len(windows),
            "global_numeric_columns": len(globals_),
            "temporal_numeric_columns": len({k for _, _, row in windows for k in row}),
            "time_alignment": "overlap_weighted_performance_seconds"}


def add_idyom_dat(rows: list[dict], export: dict, beats_per_measure: float,
                  *, melody_name: str | None = None) -> dict:
    """Project *original Lisp* IDyOM native events on the quarter-note grid.

    Caller must verify MIDI source correspondence and training provenance;
    matching by identical filenames alone does not prove correct alignment.
    """
    melodies = export["melodies"]
    if melody_name is not None:
        melodies = [melody for melody in melodies if melody["melody_name"] == melody_name]
    if len(melodies) != 1:
        raise ValueError("idyom_requires_unambiguous_source_melody")
    grouped = [[] for _ in rows]
    for event in melodies[0]["events"]:
        idx = int(event["onset_quarter_beats"] / beats_per_measure)
        if 0 <= idx < len(rows):
            grouped[idx].append(event)
    for row, events in zip(rows, grouped):
        by_name = {}
        for event in events:
            for viewpoint, numbers in event["viewpoints"].items():
                for metric in ("surprisal_bits", "entropy_bits_before", "event_probability"):
                    value = numbers.get(metric)
                    if value is not None:
                        by_name.setdefault(f"idyom_{viewpoint}.{metric}", []).append(value)
                entropy = numbers.get("entropy_bits_before")
                surprisal = numbers.get("surprisal_bits")
                if entropy is not None and surprisal is not None:
                    by_name.setdefault(f"idyom_{viewpoint}.entropy_x_surprisal", []).append(entropy * surprisal)
        for key, values in by_name.items():
            row[key] = _mean(values)
            row[key + ".std"] = _std(values)
        row["idyom_event_count"] = len(events)
    return {"status": "ok", "engine": "original IDyOM Lisp .dat",
            "events_mapped": sum(len(x) for x in grouped),
            "viewpoints": list(export["viewpoint_columns"]),
            "requires_training_and_alignment_audit": True}


def add_multiscale_motion(rows: list[dict]) -> dict:
    """Temporal gradients and memory of complementary, *changing* signals.

    The transforms add no new claims of distinct musical mechanisms; they
    expose change/accumulation (Farbood-inspired) in original tonal tension,
    Narmour events, jSymbolic texture and train-only expectation measures.
    Excludes static whole-piece descriptors and human evaluations.
    """
    candidates = sorted({key for row in rows for key in row if (
        key.startswith("partitura_") or
        key.startswith("narmour.") and key.endswith("_mean") or
        key.startswith("ngram_") and (key.endswith("surprisal_mean") or
                                         key.endswith("entropy_before_mean") or
                                         key.endswith("entropy_x_surprisal")) or
        key.startswith("jsym_window.") and any(term in key.lower() for term in (
            "note density", "dynamic", "articulation", "register", "rhythm", "tempo",
            "melodic", "polyphony", "texture", "dissonance", "pitch class diversity"))
    )})
    for key in candidates:
        observations = [row.get(key) for row in rows]
        for index, row in enumerate(rows):
            value = observations[index]
            previous = observations[index - 1] if index else None
            row[f"motion_delta.{key}"] = (value - previous
                if value is not None and previous is not None else None)
            recent = [x for x in observations[max(0, index - 3):index + 1]
                      if x is not None]
            row[f"motion_memory4.{key}"] = statistics.mean(recent) if recent else None
    return {"status": "ok", "original_signals_with_temporal_derivatives": len(candidates),
            "window": "causal 4-measure memory; not original Farbood perceptual parameters"}
