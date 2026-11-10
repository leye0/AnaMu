"""AnaMu Grammar G1: source-backed temporal and exact-transform relations.

Temporal classification uses the 13 mutually exclusive relations of Allen's
interval algebra (Allen, CACM 1983, DOI 10.1145/182.358434). No chord, voice,
phrase, instrument role or acoustic meaning is inferred by these facts.

This is a *partial* G1: SEQUENCE, PARALLEL and exact TRANSFORM have executable
contracts. ALIGN, GROUP and DEPEND need separate evidence/annotation models.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Sequence

from .grammar_foundation import MidiEvidence, NoteSpan


class AllenRelation(str, Enum):
    BEFORE = "before"
    MEETS = "meets"
    OVERLAPS = "overlaps"
    STARTS = "starts"
    DURING = "during"
    FINISHES = "finishes"
    EQUALS = "equals"
    AFTER = "after"
    MET_BY = "met_by"
    OVERLAPPED_BY = "overlapped_by"
    STARTED_BY = "started_by"
    CONTAINS = "contains"
    FINISHED_BY = "finished_by"


def interval_relation(a_start: int, a_end: int,
                      b_start: int, b_end: int) -> AllenRelation:
    """Classify two positive, half-open time intervals without tolerance."""
    if a_start < 0 or b_start < 0 or a_start >= a_end or b_start >= b_end:
        raise ValueError("allen_requires_positive_length_intervals")
    if a_end < b_start:
        return AllenRelation.BEFORE
    if a_end == b_start:
        return AllenRelation.MEETS
    if b_end < a_start:
        return AllenRelation.AFTER
    if b_end == a_start:
        return AllenRelation.MET_BY
    if a_start == b_start:
        if a_end == b_end:
            return AllenRelation.EQUALS
        return AllenRelation.STARTS if a_end < b_end else AllenRelation.STARTED_BY
    if a_end == b_end:
        return AllenRelation.FINISHES if a_start > b_start else AllenRelation.FINISHED_BY
    if a_start < b_start:
        return AllenRelation.OVERLAPS if a_end < b_end else AllenRelation.CONTAINS
    return AllenRelation.OVERLAPPED_BY if a_end > b_end else AllenRelation.DURING


_DISJOINT = {AllenRelation.BEFORE, AllenRelation.MEETS,
             AllenRelation.AFTER, AllenRelation.MET_BY}


@dataclass(frozen=True)
class ObservedNoteRelation:
    """Exact G1 pair fact, not an inferred chord, motif or voice relation."""

    operator: str  # SEQUENCE (disjoint) or PARALLEL (time-intersecting)
    source_sha256: str
    allen_relation: AllenRelation
    left_onset_id: str
    right_onset_id: str
    source_event_ids: tuple[str, str, str, str]
    start_delta_ticks: int
    overlap_ticks: int
    start_delta_beats: Fraction | None  # Unknown on SMPTE divisions
    pitch_delta_semitones: int | None  # Unknown for MIDI percussion channel


def _compare_known_spans(evidence: MidiEvidence, left: NoteSpan,
                         right: NoteSpan) -> ObservedNoteRelation:
    if left == right:
        raise ValueError("self_relation_is_not_a_pair")
    topology = interval_relation(left.start_tick, left.end_tick,
                                 right.start_tick, right.end_tick)
    overlap = max(0, min(left.end_tick, right.end_tick) -
                  max(left.start_tick, right.start_tick))
    delta = right.start_tick - left.start_tick
    beats = Fraction(delta, evidence.ticks_per_beat) if evidence.timebase == "ppq" else None
    pitch = (None if 9 in (left.channel, right.channel)
             else right.pitch - left.pitch)
    return ObservedNoteRelation(
        operator="SEQUENCE" if topology in _DISJOINT else "PARALLEL",
        source_sha256=evidence.sha256,
        allen_relation=topology,
        left_onset_id=left.onset_event_id,
        right_onset_id=right.onset_event_id,
        source_event_ids=(left.onset_event_id, left.release_event_id,
                          right.onset_event_id, right.release_event_id),
        start_delta_ticks=delta, overlap_ticks=overlap,
        start_delta_beats=beats, pitch_delta_semitones=pitch)


def compare_note_spans(evidence: MidiEvidence, left: NoteSpan,
                       right: NoteSpan) -> ObservedNoteRelation:
    """Compare two note key-down spans *from this evidence* with provenance."""
    if left not in evidence.notes or right not in evidence.notes:
        raise ValueError("note_span_not_present_in_evidence")
    return _compare_known_spans(evidence, left, right)


class NoteRelationIndex:
    """Indexed pairwise queries; no quadratic orchestral all-pairs expansion."""

    def __init__(self, evidence: MidiEvidence):
        self.evidence = evidence
        self._by_onset_id = {note.onset_event_id: note for note in evidence.notes}
        if len(self._by_onset_id) != len(evidence.notes):
            raise ValueError("duplicate_note_onset_id_in_evidence")

    def compare(self, left_onset_id: str, right_onset_id: str) -> ObservedNoteRelation:
        try:
            left = self._by_onset_id[left_onset_id]
            right = self._by_onset_id[right_onset_id]
        except KeyError as exc:
            raise ValueError("unknown_note_onset_id") from exc
        return _compare_known_spans(self.evidence, left, right)


@dataclass(frozen=True)
class ExactPatternTransform:
    """Verified 1:1 correspondence, not a claim of perceived motif identity."""

    operator: str  # TRANSFORM
    source_sha256: str
    source_onset_ids: tuple[str, ...]
    target_onset_ids: tuple[str, ...]
    transposition_semitones: int
    time_scale: Fraction
    temporal_shift_ticks: int
    source_event_ids: tuple[str, ...]


def exact_pattern_transform(evidence: MidiEvidence,
                            source: Sequence[NoteSpan],
                            target: Sequence[NoteSpan]) -> ExactPatternTransform | None:
    """Prove exact transposition + uniform temporal scale for an explicit match.

    The caller supplies *ordered correspondence*: this routine does not match
    parts, decide voices or search motifs. At least two notes and positive
    durations are required; MIDI percussion is excluded from pitched claims.
    One-to-one matches with a zero temporal scale are rejected.
    """
    return _exact_pattern_transform(evidence, source, target, frozenset(evidence.notes))


def _exact_pattern_transform(evidence: MidiEvidence,
                             source: Sequence[NoteSpan],
                             target: Sequence[NoteSpan],
                             known_notes: frozenset[NoteSpan]) -> ExactPatternTransform | None:
    if len(source) < 2 or len(source) != len(target):
        raise ValueError("transform_requires_equal_patterns_of_at_least_two_notes")
    if any(note not in known_notes for note in (*source, *target)):
        raise ValueError("transform_span_not_present_in_evidence")
    if any(note.channel == 9 or note.end_tick <= note.start_tick
           for note in (*source, *target)):
        return None
    if len({note.onset_event_id for note in source}) != len(source):
        raise ValueError("duplicate_source_note_in_correspondence")
    if len({note.onset_event_id for note in target}) != len(target):
        raise ValueError("duplicate_target_note_in_correspondence")

    semitones = target[0].pitch - source[0].pitch
    time_scale = Fraction(target[0].end_tick - target[0].start_tick,
                          source[0].end_tick - source[0].start_tick)
    shift = target[0].start_tick
    base = source[0].start_tick
    for a, b in zip(source, target):
        if b.pitch - a.pitch != semitones:
            return None
        if Fraction(b.start_tick - shift) != time_scale * (a.start_tick - base):
            return None
        if Fraction(b.end_tick - b.start_tick) != time_scale * (a.end_tick - a.start_tick):
            return None
    refs = tuple(event_id for note in (*source, *target)
                 for event_id in (note.onset_event_id, note.release_event_id))
    return ExactPatternTransform(
        operator="TRANSFORM",
        source_sha256=evidence.sha256,
        source_onset_ids=tuple(note.onset_event_id for note in source),
        target_onset_ids=tuple(note.onset_event_id for note in target),
        transposition_semitones=semitones, time_scale=time_scale,
        temporal_shift_ticks=shift - base, source_event_ids=refs)


class ExactPatternTransformIndex:
    """Repeated G1 proofs using one source-membership index per MIDI file.

    This is a pure performance optimization: it has the same validity
    conditions and result as :func:`exact_pattern_transform`.
    """

    def __init__(self, evidence: MidiEvidence):
        self.evidence = evidence
        self._known_notes = frozenset(evidence.notes)

    def prove(self, source: Sequence[NoteSpan],
              target: Sequence[NoteSpan]) -> ExactPatternTransform | None:
        return _exact_pattern_transform(self.evidence, source, target, self._known_notes)
