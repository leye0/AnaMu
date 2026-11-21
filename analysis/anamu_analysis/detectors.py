"""Small, generic observational mechanisms. No phrase/function inference.

Every mechanism has a narrow evidence contract in the concept registry.
"""
from __future__ import annotations

from collections import Counter, defaultdict


def finding(detector, kind, concepts, observed, span=None, candidates=None, limits=None):
    return {"detector": detector, "detector_version": 1, "kind": kind,
        "claim_level": "conditional_structural_candidates" if candidates else "encoded_event_observation",
        "concept_ids": concepts, "span_ticks": span, "observed": observed,
        "candidate_interpretations": candidates or [], "not_established": limits or []}


def event_inventory(features):
    channels = sorted({n["channel"] for n in features["notes"]})
    return [finding("event_inventory", "midi_inventory", ["notation.key_events"], {
        "note_attacks": len(features["notes"]), "paired_releases": sum(n["release_tick"] is not None for n in features["notes"]),
        "tracks": len(features["tracks"]), "channels_zero_based": channels,
        "controls": len(features["controls"]), "text_and_lyric_events": len(features["text_events"]),
        "warnings": len(features["warnings"]), "evidence": "features.notes, tracks, controls and warnings"},
        [0, features["end_tick"]], limits=["musical voice count", "real instrument identity", "sounding note durations"])]


CHORD_TEMPLATES = {
    "major_triad": (0, 4, 7), "minor_triad": (0, 3, 7), "diminished_triad": (0, 3, 6),
    "augmented_triad": (0, 4, 8), "major_minor_seventh_pitch_set": (0, 4, 7, 10),
    "major_seventh": (0, 4, 7, 11), "minor_seventh": (0, 3, 7, 10),
    "half_diminished_seventh": (0, 3, 6, 10), "diminished_seventh": (0, 3, 6, 9),
    "major_sixth": (0, 4, 7, 9), "minor_sixth": (0, 3, 7, 9),
}


def sonority_candidates(features):
    if features["profile_declared"] != "gm1":
        return []
    boundaries = defaultdict(lambda: {"start": [], "end": []})
    for note in features["notes"]:
        if note["channel"] == 9 or note["release_tick"] is None or note["release_tick"] <= note["onset_tick"]:
            continue
        boundaries[note["onset_tick"]]["start"].append(note)
        boundaries[note["release_tick"]]["end"].append(note)
    active = {}
    ticks = sorted(boundaries)
    result = []
    for i, tick in enumerate(ticks[:-1]):
        # Half-open key intervals remove releases before observing the next span.
        for note in boundaries[tick]["end"]: active.pop(note["id"], None)
        for note in boundaries[tick]["start"]: active[note["id"]] = note
        if not active:
            continue
        pitches = sorted({n["midi_key"] for n in active.values()})
        pcs = sorted({pitch % 12 for pitch in pitches})
        candidates = []
        for root in range(12):
            relative = {(pc - root) % 12 for pc in pcs}
            for name, template in CHORD_TEMPLATES.items():
                if relative == set(template):
                    candidates.append({"pitch_set_template": name, "candidate_root_pitch_class": root,
                        "lowest_key_interval_from_candidate_root": (pitches[0] % 12 - root) % 12})
        concepts = ["harmony.sonority", "harmony.lowest_pitch"]
        if any(c["pitch_set_template"] == "augmented_triad" for c in candidates):
            concepts.append("harmony.augmented_symmetry")
        if any(c["pitch_set_template"] == "diminished_seventh" for c in candidates):
            concepts.append("harmony.diminished_symmetry")
        result.append(finding("sonority_candidates", "active_key_sonority", concepts,
            {"active_note_ids": sorted(active), "midi_keys": pitches, "pitch_classes": pcs,
             "lowest_active_key": pitches[0], "profile_assumption": "gm1; channel 9 excluded",
             "time_basis": "key-down intervals; not acoustical sounding intervals"},
            [tick, ticks[i + 1]], candidates=candidates,
            limits=["spelling", "established tonic", "harmonic function", "cadential function", "bass voice assignment", "perceptual fusion"]))
    return result


def exact_recurrence(features, window_size=3):
    groups = defaultdict(lambda: defaultdict(list))
    for note in features["notes"]:
        if note["key_duration_ticks"] is not None:
            groups[(note["track"], note["channel"])][note["onset_tick"]].append(note)
    result = []
    for (track, channel), by_tick in sorted(groups.items()):
        onsets = sorted(by_tick)
        modes = ["exact_keys_and_notated_rhythm"]
        if features["profile_declared"] == "gm1" and channel != 9:
            modes.append("constant_pitch_transposition_and_same_notated_rhythm")
        for mode in modes:
            patterns = defaultdict(list)
            for i in range(len(onsets) - window_size + 1):
                window = onsets[i:i + window_size]
                first_pitch = min(n["midi_key"] for n in by_tick[window[0]])
                shift = first_pitch if mode.startswith("constant") else 0
                signature = tuple((tick - window[0], tuple(sorted(
                    (n["midi_key"] - shift, n["key_duration_ticks"]) for n in by_tick[tick]))) for tick in window)
                patterns[signature].append({"start_tick": window[0], "last_attack_tick": window[-1],
                    "end_tick": max(n["release_tick"] for tick in window for n in by_tick[tick]),
                    "reference_key": first_pitch, "note_ids": [n["id"] for tick in window for n in by_tick[tick]]})
            for signature, occurrences in patterns.items():
                if len(occurrences) < 2:
                    continue
                # Exact matches already have their own record; transposition mode
                # only adds a claim when at least one nonzero shift occurs.
                if mode.startswith("constant") and len({o["reference_key"] for o in occurrences}) == 1:
                    continue
                result.append(finding("exact_recurrence", "source_partition_recurrence", ["motif.exact_recurrence"],
                    {"track": track, "channel_zero_based": channel, "mode": mode,
                     "window_attack_groups": window_size, "signature": signature, "occurrences": occurrences,
                     "overlapping_windows_allowed": True,
                     "excluded_parameters": ["velocity", "controllers", "timbre", "articulation", "phrase role"]},
                    [min(o["start_tick"] for o in occurrences), max(o["end_tick"] for o in occurrences)],
                    limits=["musical motif identity", "imitative voice assignment", "formal return", "perceived similarity"]))
    return result


def notated_timing(features):
    conflicts = []
    for name, rows, fields in [
        ("tempo", features["tempo_events"], ("microseconds_per_quarter",)),
        ("meter", features["time_signature_events"], ("numerator", "denominator")),
    ]:
        at_tick = defaultdict(set)
        for row in rows: at_tick[row["tick"]].add(tuple(row[k] for k in fields))
        conflicts.extend({"type": name, "tick": tick, "values": sorted(values)} for tick, values in at_tick.items() if len(values) > 1)
    return [finding("notated_timing", "declared_timing", ["rhythm.notated_grid"], {
        "ticks_per_quarter": features["ticks_per_quarter"], "tempo_events": features["tempo_events"],
        "time_signature_events": features["time_signature_events"], "simultaneous_conflicts": conflicts,
        "missing_time_signature_policy": "unknown; not a declaration of 4/4",
        "missing_tempo_policy": "SMF playback default 500000 us/quarter is a convention, not evidence of expressive intent"},
        [0, features["end_tick"]], limits=["perceived pulse", "accent grouping", "anacrusis", "hypermetric phrase boundaries"])]


def velocity_commands(features):
    by_channel = defaultdict(list)
    for note in features["notes"]: by_channel[(note["track"], note["channel"])].append(note["velocity"])
    return [finding("velocity_commands", "encoded_velocity_distribution", ["sound.velocity"], {
        "partitions": [{"track": t, "channel_zero_based": c, "counts": dict(sorted(Counter(values).items())),
                        "minimum": min(values), "maximum": max(values)} for (t, c), values in sorted(by_channel.items())]},
        [0, features["end_tick"]], limits=["acoustic loudness", "perceived accent", "performer effort", "dynamic marking"])]


def sustain_commands(features):
    return [finding("sustain_commands", "literal_sustain_commands", ["sound.sustain"], {
        "events": [e for e in features["controls"] if e["control"] in (64, 66, 67)],
        "duration_model": "key releases only; damper/sostenuto/soft pedal not rendered"},
        [0, features["end_tick"]], limits=["actual pedal gesture", "sounding duration", "acoustical decay", "mallet damping"])]


DETECTORS = {
    "event_inventory": event_inventory, "sonority_candidates": sonority_candidates,
    "exact_recurrence": exact_recurrence, "notated_timing": notated_timing,
    "velocity_commands": velocity_commands, "sustain_commands": sustain_commands,
}


def run_detectors(features):
    result, execution = [], []
    for name, fn in DETECTORS.items():
        ambiguous_notes = {w["kind"] for w in features["warnings"]} & {
            "unmatched_attack", "unmatched_release", "overlapping_same_key"}
        if name in {"sonority_candidates", "exact_recurrence"} and ambiguous_notes:
            execution.append({"id": name, "status": "blocked",
                "reason": "Incomplete or ambiguous note pairing: " + ", ".join(sorted(ambiguous_notes))})
            continue
        if name == "sonority_candidates" and features["profile_declared"] != "gm1":
            execution.append({"id": name, "status": "blocked", "reason": "pitched/percussive channel semantics not declared"})
            continue
        observations = fn(features)
        for item in observations:
            item["id"] = f"observation:{len(result):06d}"
            result.append(item)
        execution.append({"id": name, "status": "executed", "observation_count": len(observations),
                          "empty_result_means": "no observation under this limited mechanism, not absence of the musical concept"})
    return result, execution
