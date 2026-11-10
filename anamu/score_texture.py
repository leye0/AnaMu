"""Source-backed MusicXML note evidence and exact orchestral line doublings.

An orchestration *fact* is a written note, part, duration or transpose rule;
an exact doubling is a structural candidate for an arrangement technique.
No claim of melody hierarchy, auditory blend, quality or causal intent.
Measures are in score order (repeats are not unfolded); ties remain fragments.
"""

from __future__ import annotations

import hashlib
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations

from .score_inventory import (
    _child, _children, _tag, _text, instrument_family, musicxml_root_from_mxl,
)

_STEPS = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


@dataclass(frozen=True)
class ScorePart:
    id: str
    label: str
    instrument_family: str


@dataclass(frozen=True)
class WrittenNote:
    source_note_id: str
    part_id: str
    measure_index: int  # 0-based score order, NOT playback order
    measure_number: str  # original printed label
    onset_quarters: Fraction  # within this measure, not seconds
    duration_quarters: Fraction
    written_midi_pitch: int
    sounding_midi_pitch: int  # score <transpose> is applied, when present
    staff: str | None
    voice: str | None
    tied: bool  # score fragments, not reconstructed sustained notes


@dataclass(frozen=True)
class ScoreTextureEvidence:
    source_sha256: str
    parts: tuple[ScorePart, ...]
    notes: tuple[WrittenNote, ...]
    measure_count: int
    grace_notes_excluded: int
    cue_notes_excluded: int
    unpitched_notes_excluded: int
    method: str = "musicxml_written_score_order_no_repeat_unfolding"


@dataclass(frozen=True)
class OctaveDoublingCandidate:
    """Consecutive synchronized, equal-duration pitches in two score parts."""

    source_sha256: str
    part_a: str
    part_b: str
    octave_offset: int  # sounding pitch of B minus A, in octaves
    source_note_pairs: tuple[tuple[str, str], ...]
    start_measure_index: int
    end_measure_index: int
    status: str = "exact_notational_doubling_candidate"


def _required_int(value: str | None, issue: str) -> int:
    if value is None:
        raise ValueError(issue)
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(issue) from exc


def _pitch_midi(pitch) -> int:
    step = _text(pitch, "step")
    if step not in _STEPS:
        raise ValueError("unsupported_musicxml_pitch_step")
    octave = _required_int(_text(pitch, "octave"), "missing_musicxml_octave")
    # Explicitly reject microtones instead of rounding them to MIDI semitones.
    alteration = Fraction(_text(pitch, "alter") or "0")
    if alteration.denominator != 1:
        raise ValueError("microtonal_musicxml_pitch_not_supported")
    return (octave + 1) * 12 + _STEPS[step] + int(alteration)


def _chromatic_transposition(transpose) -> int:
    chromatic = Fraction(_text(transpose, "chromatic") or "0")
    if chromatic.denominator != 1:
        raise ValueError("microtonal_musicxml_transposition_not_supported")
    return int(chromatic) + 12 * int(_text(transpose, "octave-change") or "0")


def score_texture_from_mxl(mxl_bytes: bytes) -> ScoreTextureEvidence:
    """Extract score-notated attacks, not actual performance/sounding durations.

    Each part has its own measure cursor, including <backup>/<forward>
    polyphonic positioning and <chord> shared attacks. Fractional quarter
    units avoid implicit quantization when divisions change. Source measure
    order is retained; absent transpose means concert pitch in MusicXML.
    """
    root = musicxml_root_from_mxl(mxl_bytes)
    part_list = _child(root, "part-list")
    if part_list is None:
        raise ValueError("missing_musicxml_part_list")
    parts = []
    for p in _children(part_list, "score-part"):
        part_id = p.get("id")
        if not part_id:
            raise ValueError("musicxml_part_without_id")
        names = [_text(x, "instrument-name") for x in _children(p, "score-instrument")]
        label = next((n for n in names if n), None) or _text(p, "part-name") or "unknown"
        parts.append(ScorePart(part_id, label, instrument_family(label)))
    declared = {p.id for p in parts}
    if len(declared) != len(parts):
        raise ValueError("duplicate_musicxml_part_id")

    notes: list[WrittenNote] = []
    grace = cue = unpitched = 0
    measure_counts = set()
    for part in _children(root, "part"):
        part_id = part.get("id")
        if part_id not in declared:
            raise ValueError("undeclared_musicxml_part")
        measures = _children(part, "measure")
        measure_counts.add(len(measures))
        divisions = 0
        transposition = 0
        for measure_index, measure in enumerate(measures):
            cursor = Fraction(0)
            chord_anchor: Fraction | None = None
            for note_index, element in enumerate(measure):
                name = _tag(element.tag)
                if name == "attributes":
                    new_divisions = _text(element, "divisions")
                    if new_divisions is not None:
                        divisions = _required_int(new_divisions, "invalid_musicxml_divisions")
                        if divisions <= 0:
                            raise ValueError("invalid_musicxml_divisions")
                    transposes = _children(element, "transpose")
                    if len(transposes) > 1 or any(t.get("number") is not None
                                                      for t in transposes):
                        raise ValueError("staff_specific_transpose_not_supported")
                    if transposes:
                        transposition = _chromatic_transposition(transposes[0])
                elif name in ("backup", "forward"):
                    if divisions <= 0:
                        raise ValueError("missing_musicxml_divisions")
                    duration = _required_int(_text(element, "duration"),
                                             "missing_musicxml_move_duration")
                    if duration < 0:
                        raise ValueError("negative_musicxml_move_duration")
                    cursor += Fraction(duration if name == "forward" else -duration,
                                       divisions)
                    if cursor < 0:
                        raise ValueError("musicxml_backup_before_measure_start")
                    chord_anchor = None
                elif name == "note":
                    if divisions <= 0:
                        raise ValueError("missing_musicxml_divisions")
                    if _child(element, "grace") is not None:
                        # Grace chords may be encoded without a normal cursor
                        # anchor; none participate in this strict model.
                        grace += 1
                        continue
                    is_chord = _child(element, "chord") is not None
                    if is_chord and chord_anchor is None:
                        raise ValueError("musicxml_chord_without_anchor")
                    onset = chord_anchor if is_chord else cursor
                    duration_raw = _required_int(_text(element, "duration"),
                                                 "missing_musicxml_note_duration")
                    if duration_raw <= 0:
                        raise ValueError("nonpositive_musicxml_note_duration")
                    duration = Fraction(duration_raw, divisions)
                    if not is_chord:
                        chord_anchor = onset
                        cursor += duration
                    if _child(element, "cue") is not None:
                        cue += 1
                        continue
                    pitch = _child(element, "pitch")
                    if pitch is None:
                        if _child(element, "rest") is None:
                            unpitched += 1
                        continue
                    written = _pitch_midi(pitch)
                    notes.append(WrittenNote(
                        source_note_id=f"{part_id}:{measure_index}:{note_index}",
                        part_id=part_id, measure_index=measure_index,
                        measure_number=measure.get("number", ""),
                        onset_quarters=onset, duration_quarters=duration,
                        written_midi_pitch=written,
                        sounding_midi_pitch=written + transposition,
                        staff=_text(element, "staff"), voice=_text(element, "voice"),
                        tied=bool(_children(element, "tie")),
                    ))
    if len(measure_counts) > 1:
        raise ValueError("score_parts_have_different_measure_counts")
    if len({n.source_note_id for n in notes}) != len(notes):
        raise AssertionError("score_note_id_collision")
    return ScoreTextureEvidence(
        source_sha256=hashlib.sha256(mxl_bytes).hexdigest(),
        parts=tuple(parts), notes=tuple(notes),
        measure_count=next(iter(measure_counts), 0),
        grace_notes_excluded=grace, cue_notes_excluded=cue,
        unpitched_notes_excluded=unpitched)


def discover_exact_octave_doublings(evidence: ScoreTextureEvidence, *,
                                    min_notes: int = 3,
                                    max_candidates: int = 20_000
                                    ) -> tuple[OctaveDoublingCandidate, ...]:
    """Find strict notation-level unison/octave support, not auditory blend.

    Every matching line pair must retain consecutive source onsets in both
    entire parts, equal note durations, and constant sounding pitch shift of
    0, ±12 or ±24 semitones. Chord attacks and tied fragments are NOT matched.
    """
    if min_notes < 2 or max_candidates < 1:
        raise ValueError("doubling_search_budget_invalid")
    by_part: dict[str, dict[tuple[int, Fraction], list[WrittenNote]]] = defaultdict(
        lambda: defaultdict(list))
    for note in evidence.notes:
        by_part[note.part_id][note.measure_index, note.onset_quarters].append(note)
    by_position = {}
    for part_id, notes_at in by_part.items():
        by_position[part_id] = {
            position: (index, notes_at[position])
            for index, position in enumerate(sorted(notes_at))
        }

    found: list[OctaveDoublingCandidate] = []
    for left, right in combinations(sorted(by_position), 2):
        left_positions, right_positions = by_position[left], by_position[right]
        run: list[tuple[WrittenNote, WrittenNote]] = []
        previous_indices: tuple[int, int] | None = None
        previous_interval: int | None = None

        def flush() -> None:
            if len(run) >= min_notes:
                found.append(OctaveDoublingCandidate(
                    source_sha256=evidence.source_sha256,
                    part_a=left, part_b=right,
                    octave_offset=previous_interval // 12,
                    source_note_pairs=tuple((a.source_note_id, b.source_note_id)
                                            for a, b in run),
                    start_measure_index=run[0][0].measure_index,
                    end_measure_index=run[-1][0].measure_index))
                if len(found) > max_candidates:
                    raise ValueError("doubling_candidate_budget_exceeded")
            run.clear()

        for position in sorted(left_positions.keys() & right_positions.keys()):
            index_a, notes_a = left_positions[position]
            index_b, notes_b = right_positions[position]
            if (len(notes_a) != 1 or len(notes_b) != 1 or notes_a[0].tied
                    or notes_b[0].tied or
                    notes_a[0].duration_quarters != notes_b[0].duration_quarters):
                flush()
                previous_indices = previous_interval = None
                continue
            a, b = notes_a[0], notes_b[0]
            interval = b.sounding_midi_pitch - a.sounding_midi_pitch
            if interval not in (-24, -12, 0, 12, 24):
                flush()
                previous_indices = previous_interval = None
                continue
            if run and (previous_indices != (index_a - 1, index_b - 1)
                        or interval != previous_interval):
                flush()
            run.append((a, b))
            previous_indices = (index_a, index_b)
            previous_interval = interval
        flush()
    found.sort(key=lambda x: (-len(x.source_note_pairs), x.start_measure_index,
                              x.part_a, x.part_b, x.octave_offset))
    return tuple(found)
