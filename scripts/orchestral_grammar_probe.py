"""Deterministic G0/G1 audit of explicitly licensed, *symbolic* orchestral MIDI.

No instrument recognition, sounding loudness, phrase, chord, motif, or
orchestration correctness is inferred. Runs on the bundled binary files.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from anamu.grammar_foundation import MidiEvidence, midi_evidence_from_file  # noqa: E402
from anamu.grammar_relations import NoteRelationIndex  # noqa: E402


def _counts(counter: Counter) -> dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter)}


def _max_key_down_concurrency(evidence: MidiEvidence) -> int:
    """Exact maximum simultaneous *key-down* spans, not sounding voices."""
    boundaries: Counter[int] = Counter()
    for note in evidence.notes:
        if note.end_tick <= note.start_tick:
            continue
        boundaries[note.start_tick] += 1
        boundaries[note.end_tick] -= 1
    active = peak = 0
    for tick in sorted(boundaries):
        active += boundaries[tick]
        if active < 0:
            raise ValueError("invalid_note_span_concurrency")
        peak = max(peak, active)
    return peak


def audit(evidence: MidiEvidence, *, max_adjacent_pairs: int = 5000) -> dict:
    """Measure complete G0 observations and a deliberately bounded G1 sample.

    G1 pair sample = first N adjacent *distinct* positive-duration notes,
    sorted (start_tick, track, onset_id); NOT the distribution of all pairs.
    """
    if max_adjacent_pairs < 0:
        raise ValueError("negative_pair_budget")
    event_types = Counter(event.type for event in evidence.events)
    diagnostics = Counter(item.code for item in evidence.diagnostics)
    named_tracks: dict[int, dict] = {
        track: {"track": track, "track_names": [], "instrument_names": [],
                "program_changes": [], "key_spans": 0}
        for track in range(evidence.track_count)
    }
    controls = Counter()
    for event in evidence.events:
        row = named_tracks[event.track]
        if event.type == "track_name":
            row["track_names"].append(event.field("name"))
        elif event.type == "instrument_name":
            row["instrument_names"].append(event.field("name"))
        elif event.type == "program_change":
            row["program_changes"].append({
                "tick": event.tick, "channel": event.field("channel"),
                "program_zero_based": event.field("program")})
        elif event.type == "control_change":
            controls[event.field("control")] += 1

    onsets = Counter()
    for note in evidence.notes:
        named_tracks[note.track]["key_spans"] += 1
        onsets[note.start_tick] += 1
    sorted_notes = sorted((note for note in evidence.notes
                           if note.end_tick > note.start_tick),
                          key=lambda note: (note.start_tick, note.track,
                                            note.onset_event_id))
    relation_index = NoteRelationIndex(evidence)
    allen = Counter()
    operators = Counter()
    pair_budget = min(max_adjacent_pairs, max(0, len(sorted_notes) - 1))
    for left, right in zip(sorted_notes[:pair_budget],
                           sorted_notes[1:pair_budget + 1]):
        relation = relation_index.compare(left.onset_event_id,
                                          right.onset_event_id)
        allen[relation.allen_relation.value] += 1
        operators[relation.operator] += 1

    tempos = evidence.events_of_type("set_tempo")
    return {
        "g0": {
            **evidence.summary(),
            "event_types": _counts(event_types),
            "diagnostic_counts": _counts(diagnostics),
            "track_observations": [named_tracks[i] for i in sorted(named_tracks)],
            "control_change_numbers": _counts(controls),
            "explicit_set_tempo_events": len(tempos),
            "distinct_explicit_tempo_values_micros_per_quarter":
                sorted({event.field("tempo") for event in tempos}),
            "onset_ticks_with_two_or_more_key_spans":
                sum(1 for count in onsets.values() if count >= 2),
            "largest_simultaneous_key_span_onset": max(onsets.values(), default=0),
            "max_simultaneous_key_down_spans": _max_key_down_concurrency(evidence),
            "end_tick_of_observed_events": max((e.tick for e in evidence.events), default=0),
        },
        "g1_adjacent_note_probe": {
            "sampling": "first N adjacent positive-duration key spans in (onset_tick, track, onset_id) order; not all note pairs",
            "budget": max_adjacent_pairs,
            "evaluated_pairs": pair_budget,
            "operators": _counts(operators),
            "allen_relations": _counts(allen),
        },
        "not_inferred": ["sounding_loudness", "instrument_timbre",
                         "true_orchestral_instrument", "human_rubato",
                         "phrase", "chord_function", "musical_motif",
                         "score_fidelity"],
    }


def run_manifest(manifest_path: Path, *, pair_budget: int = 5000) -> dict:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("version") != 1:
        raise ValueError("unsupported_orchestral_manifest_version")
    results = []
    for piece in manifest["pieces"]:
        path = (ROOT / piece["file"]).resolve()
        if not path.is_relative_to((ROOT / "data" / "orchestral").resolve()):
            raise ValueError("orchestral_file_outside_data_directory")
        evidence = midi_evidence_from_file(path)
        if evidence.sha256 != piece["sha256"]:
            raise ValueError(f"source_checksum_mismatch:{piece['id']}")
        results.append({"source": piece, "observations": audit(
            evidence, max_adjacent_pairs=pair_budget)})
    return {
        "schema_version": 1,
        "method": "G0 lossless MIDI evidence; bounded adjacent-note G1 temporal relation probe",
        "corpus_is_annotated_ground_truth": False,
        "pieces": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path,
                        default=ROOT / "data/orchestral/SOURCES.json")
    parser.add_argument("--output", type=Path,
                        default=ROOT / "reports/orchestral-grammar-probe-2026-11-09.json")
    parser.add_argument("--max-adjacent-pairs", type=int, default=5000)
    args = parser.parse_args()
    report = run_manifest(args.manifest, pair_budget=args.max_adjacent_pairs)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2,
                                      sort_keys=True) + "\n", encoding="utf-8")
    for row in report["pieces"]:
        g0 = row["observations"]["g0"]
        print(f"{row['source']['id']}: {g0['track_count']} tracks, "
              f"{g0['unambiguous_key_spans']} key spans, "
              f"{g0['max_simultaneous_key_down_spans']} peak key-down")


if __name__ == "__main__":
    main()
