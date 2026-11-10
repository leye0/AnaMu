"""G2 exploratory discovery of exact pitch/time-scale motif candidates.

Inspired by geometric repetition discovery (Meredith, Lemström & Wiggins,
2002), but this is NOT SIA/SIATEC: windows use consecutive MIDI onsets in
each (track, channel) strand. Neither MIDI strands nor repeated structures
are asserted to be voices, themes, phrases or perceptually salient motifs.

No human labels, learned weights, style rules or floating-point quantization.
"""

from __future__ import annotations

import hashlib
from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from math import gcd

from .grammar_foundation import MidiEvidence, NoteSpan
from .grammar_relations import ExactPatternTransform, ExactPatternTransformIndex


@dataclass(frozen=True)
class MotifOccurrence:
    """A source-backed contiguous-onset window, not an inferred phrase."""

    track: int
    channel: int
    start_tick: int
    end_tick: int
    onset_event_ids: tuple[str, ...]
    release_event_ids: tuple[str, ...]
    notes: tuple[NoteSpan, ...]


@dataclass(frozen=True)
class MotifCandidate:
    """At least two non-overlapping occurrences of one exact structure."""

    operator: str  # GROUP candidate, with verified TRANSFORM edges
    status: str  # structural_candidate, never human-confirmed_theme
    source_sha256: str
    signature_sha256: str
    onset_count: int
    note_count: int
    occurrences: tuple[MotifOccurrence, ...]
    transforms_from_first: tuple[ExactPatternTransform, ...]


@dataclass(frozen=True)
class MotifDiscovery:
    source_sha256: str
    candidates: tuple[MotifCandidate, ...]
    strands_examined: int
    windows_examined: int
    dense_windows_skipped: int
    percussion_notes_excluded: int
    nonpositive_notes_excluded: int
    method: str = "consecutive_midi_onset_windows_exact_pitch_shift_and_time_scale"


def _fingerprint(notes: tuple[NoteSpan, ...]) -> tuple[tuple[int, int, int], ...]:
    """Normalize translation in pitch, time origin and uniform time scale."""
    start = min(note.start_tick for note in notes)
    base_pitch = min(note.pitch for note in notes if note.start_tick == start)
    offsets_and_durations = [x for note in notes
                             for x in (note.start_tick - start,
                                       note.end_tick - note.start_tick)]
    quantum = reduce(gcd, offsets_and_durations)
    if quantum <= 0:
        raise ValueError("nonpositive_motif_time_quantum")
    return tuple(((note.start_tick - start) // quantum,
                  note.pitch - base_pitch,
                  (note.end_tick - note.start_tick) // quantum)
                 for note in notes)


def discover_exact_motifs(
    evidence: MidiEvidence, *, min_onsets: int = 3, max_onsets: int = 5,
    max_notes_per_window: int = 32, max_windows: int = 100_000,
    max_candidates: int = 5_000,
) -> MotifDiscovery:
    """Discover candidate repetitions without claiming themes or voices.

    Onsets are grouped *only* within source (track, channel) strands. Each
    window contains all valid pitched notes from consecutive distinct onset
    ticks. Canonical integer signatures preserve polyphonic chord membership
    and durations, while permitting uniform pitch shifts, positive rhythmic
    scaling and time translation. Cross-strand matches are permitted, but
    simultaneous occurrences are not counted as repeated-in-time evidence.

    Dense windows are explicitly counted as excluded; exceeding global
    search/output budgets fails rather than silently returning a top-K list.
    """
    if not (2 <= min_onsets <= max_onsets <= 8):
        raise ValueError("motif_onset_range_invalid")
    if not (2 <= max_notes_per_window <= 256):
        raise ValueError("motif_window_note_budget_invalid")
    if max_windows < 1 or max_candidates < 1:
        raise ValueError("motif_search_budget_invalid")

    strands: dict[tuple[int, int], dict[int, list[NoteSpan]]] = defaultdict(
        lambda: defaultdict(list))
    percussion = nonpositive = 0
    for note in evidence.notes:
        if note.channel == 9:
            percussion += 1
        elif note.end_tick <= note.start_tick:
            nonpositive += 1
        else:
            strands[note.track, note.channel][note.start_tick].append(note)

    buckets: dict[tuple[tuple[int, int, int], ...], list[MotifOccurrence]] = defaultdict(list)
    examined = dense = 0
    for (track, channel), by_tick in sorted(strands.items()):
        ticks = sorted(by_tick)
        groups = [tuple(sorted(by_tick[tick], key=lambda n: (
            n.pitch, n.end_tick, n.onset_event_id))) for tick in ticks]
        for start_index in range(len(groups)):
            combined: list[NoteSpan] = []
            for end_index in range(start_index, min(len(groups), start_index + max_onsets)):
                combined.extend(groups[end_index])
                onset_count = end_index - start_index + 1
                if onset_count < min_onsets:
                    continue
                examined += 1
                if examined > max_windows:
                    raise ValueError("motif_window_budget_exceeded")
                if len(combined) > max_notes_per_window:
                    dense += 1
                    continue
                ordered = tuple(sorted(combined, key=lambda n: (
                    n.start_tick, n.pitch, n.end_tick, n.onset_event_id)))
                occurrence = MotifOccurrence(
                    track=track, channel=channel,
                    start_tick=ticks[start_index],
                    end_tick=max(note.end_tick for note in ordered),
                    onset_event_ids=tuple(n.onset_event_id for n in ordered),
                    release_event_ids=tuple(n.release_event_id for n in ordered),
                    notes=ordered)
                buckets[_fingerprint(ordered)].append(occurrence)

    candidates = []
    verifier = ExactPatternTransformIndex(evidence)
    for signature, occurrences in buckets.items():
        if len(occurrences) < 2:
            continue
        # Use an interval-scheduling witness. A repeated occurrence must not
        # merely be an overlapping subwindow of the same passage.
        chosen: list[MotifOccurrence] = []
        last_end = -1
        for item in sorted(occurrences, key=lambda o: (
            o.end_tick, o.start_tick, o.track, o.channel, o.onset_event_ids)):
            if item.start_tick >= last_end:
                chosen.append(item)
                last_end = item.end_tick
        if len(chosen) < 2:
            continue
        chosen.sort(key=lambda o: (o.start_tick, o.track, o.channel))
        transforms = []
        for occurrence in chosen[1:]:
            proof = verifier.prove(chosen[0].notes, occurrence.notes)
            if proof is None:
                raise AssertionError("identical_signature_failed_exact_transform_proof")
            transforms.append(proof)
        candidates.append(MotifCandidate(
            operator="GROUP", status="structural_candidate",
            source_sha256=evidence.sha256,
            signature_sha256=hashlib.sha256(repr(signature).encode("ascii")).hexdigest(),
            onset_count=len({note.start_tick for note in chosen[0].notes}),
            note_count=len(chosen[0].notes), occurrences=tuple(chosen),
            transforms_from_first=tuple(transforms)))
        if len(candidates) > max_candidates:
            raise ValueError("motif_candidate_budget_exceeded")

    candidates.sort(key=lambda c: (-c.note_count, -c.onset_count,
                                    -len(c.occurrences), c.signature_sha256))
    return MotifDiscovery(
        source_sha256=evidence.sha256, candidates=tuple(candidates),
        strands_examined=len(strands), windows_examined=examined,
        dense_windows_skipped=dense, percussion_notes_excluded=percussion,
        nonpositive_notes_excluded=nonpositive)
