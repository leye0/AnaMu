"""Conservative orchestral voice-leading observations and note-edit proposals.

Based on classical motion terminology (contrary, similar, parallel, oblique)
and on notated *sounding* pitches in two declared MusicXML score parts.
Part identity is not a proof of a perceptually separated musical voice;
parallel perfect intervals are not automatically forbidden in orchestration.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations

from .score_texture import ScoreTextureEvidence, WrittenNote


@dataclass(frozen=True)
class ScoreMoment:
    measure_index: int
    onset_quarters: Fraction


@dataclass(frozen=True)
class VoiceLeadingObservation:
    source_sha256: str
    part_a: str
    part_b: str
    source_note_ids: tuple[str, str, str, str]  # A0, A1, B0, B1
    from_moment: ScoreMoment
    to_moment: ScoreMoment
    pitches: tuple[int, int, int, int]  # sounding A0, A1, B0, B1
    motion_a: int
    motion_b: int
    interval_before: int  # B0 - A0
    interval_after: int  # B1 - A1
    motion_type: str  # contrary, oblique, parallel, similar, static
    parallel_perfect_class: str | None  # unison_or_octave, fifth; not "error"
    crossing: bool
    status: str = "exact_two_part_notation_observation"


@dataclass(frozen=True)
class VoiceLeadingNoteEdit:
    """One hypothetical new pitch, not a claim of score or audio evidence."""

    based_on_note_ids: tuple[str, str, str, str]
    target_part: str
    target_note_id: str
    original_sounding_pitch: int
    proposed_sounding_pitch: int
    requested_motion_type: str
    resulting_motion_type: str
    interval_after: int
    causes_parallel_perfect: str | None
    changes_voice_crossing: bool
    status: str = "counterfactual_note_edit_not_validated_arrangement"


def _classify(a_delta: int, b_delta: int, before: int,
              after: int) -> tuple[str, str | None, bool]:
    if a_delta == b_delta == 0:
        motion = "static"
    elif a_delta == 0 or b_delta == 0:
        motion = "oblique"
    elif (a_delta > 0) != (b_delta > 0):
        motion = "contrary"
    elif before == after:
        motion = "parallel"
    else:
        motion = "similar"

    # Two perfect classes are structural descriptions, not a prohibition.
    perfect = None
    if motion == "parallel":
        if abs(before) % 12 == 0:
            perfect = "unison_or_octave"
        elif abs(before) % 12 == 7:
            perfect = "fifth"
    crossing = before * after < 0  # touching/unison is not a strict crossing
    return motion, perfect, crossing


def score_voice_leading(evidence: ScoreTextureEvidence, *,
                        max_observations: int = 250_000
                        ) -> tuple[VoiceLeadingObservation, ...]:
    """Observe consecutive synchronized attacks in two notated score parts.

    The method deliberately makes no correspondence across unsynchronized
    attacks, tied fragments or chords: such passages need a richer voice
    separation/alignment model. A notated part can change its musical role.
    """
    if max_observations < 1:
        raise ValueError("voice_leading_budget_invalid")
    by_part: dict[str, dict[ScoreMoment, list[WrittenNote]]] = defaultdict(
        lambda: defaultdict(list))
    for note in evidence.notes:
        time = ScoreMoment(note.measure_index, note.onset_quarters)
        by_part[note.part_id][time].append(note)

    indexed = {}
    for part, groups in by_part.items():
        indexed[part] = {moment: (index, notes)
                         for index, (moment, notes) in enumerate(
                             sorted(groups.items(), key=lambda x: (
                                 x[0].measure_index, x[0].onset_quarters)))}
    observations = []
    for part_a, part_b in combinations(sorted(indexed), 2):
        a, b = indexed[part_a], indexed[part_b]
        previous: tuple[ScoreMoment, int, int, WrittenNote, WrittenNote] | None = None
        for moment in sorted(a.keys() & b.keys(),
                             key=lambda x: (x.measure_index, x.onset_quarters)):
            ia, aa = a[moment]
            ib, bb = b[moment]
            if (len(aa) != 1 or len(bb) != 1
                    or aa[0].tied or bb[0].tied):
                previous = None
                continue
            note_a, note_b = aa[0], bb[0]
            if previous is not None:
                earlier, prev_ia, prev_ib, prev_a, prev_b = previous
                # Each part must have NO intervening attack of its own.
                if (ia == prev_ia + 1 and ib == prev_ib + 1
                        and moment.measure_index - earlier.measure_index <= 1
                        and prev_a.voice == note_a.voice
                        and prev_b.voice == note_b.voice
                        and prev_a.staff == note_a.staff
                        and prev_b.staff == note_b.staff):
                    a_delta = note_a.sounding_midi_pitch - prev_a.sounding_midi_pitch
                    b_delta = note_b.sounding_midi_pitch - prev_b.sounding_midi_pitch
                    before = prev_b.sounding_midi_pitch - prev_a.sounding_midi_pitch
                    after = note_b.sounding_midi_pitch - note_a.sounding_midi_pitch
                    motion, perfect, crossing = _classify(
                        a_delta, b_delta, before, after)
                    observations.append(VoiceLeadingObservation(
                        source_sha256=evidence.source_sha256,
                        part_a=part_a, part_b=part_b,
                        source_note_ids=(prev_a.source_note_id, note_a.source_note_id,
                                         prev_b.source_note_id, note_b.source_note_id),
                        from_moment=earlier, to_moment=moment,
                        pitches=(prev_a.sounding_midi_pitch,
                                 note_a.sounding_midi_pitch,
                                 prev_b.sounding_midi_pitch,
                                 note_b.sounding_midi_pitch),
                        motion_a=a_delta, motion_b=b_delta,
                        interval_before=before, interval_after=after,
                        motion_type=motion,
                        parallel_perfect_class=perfect, crossing=crossing))
                    if len(observations) > max_observations:
                        raise ValueError("voice_leading_budget_exceeded")
            previous = (moment, ia, ib, note_a, note_b)
    return tuple(observations)


def propose_voice_motion_edit(observation: VoiceLeadingObservation,
                              desired: str) -> VoiceLeadingNoteEdit:
    """Sketch an alternate B1 pitch, preserving A's motion and B0.

    Constructive 'what if', NOT a harmonic, instrumental, perceptual or
    voice-leading quality recommendation. The new note must be later
    voiced, harmonized and rendered before any listening judgment.
    """
    if desired not in ("parallel", "contrary", "oblique"):
        raise ValueError("unsupported_motion_edit")
    a0, a1, b0, b1 = observation.pitches
    a_delta = a1 - a0
    if a_delta == 0 and desired != "oblique":
        raise ValueError("stationary_source_cannot_define_requested_motion")
    target_delta = {
        "parallel": a_delta, "contrary": -a_delta, "oblique": 0,
    }[desired]
    proposed_pitch = b0 + target_delta
    if not 0 <= proposed_pitch <= 127:
        raise ValueError("hypothetical_pitch_outside_midi_range")
    after = proposed_pitch - a1
    motion, perfect, crossing = _classify(
        a_delta, target_delta, observation.interval_before, after)
    if motion != desired:
        raise AssertionError("constructed_motion_does_not_match_request")
    return VoiceLeadingNoteEdit(
        based_on_note_ids=observation.source_note_ids,
        target_part=observation.part_b,
        target_note_id=observation.source_note_ids[3],
        original_sounding_pitch=b1,
        proposed_sounding_pitch=proposed_pitch,
        requested_motion_type=desired, resulting_motion_type=motion,
        interval_after=after, causes_parallel_perfect=perfect,
        changes_voice_crossing=(crossing != observation.crossing))
