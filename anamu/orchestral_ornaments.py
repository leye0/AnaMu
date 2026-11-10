"""Conservative notated three-note passing/neighbor figures.

University counterpoint distinguishes a linear figure from an actual
non-chord tone: the latter needs a justified harmonic reduction and
accent/resolution evidence. This module only identifies strict diatonic
stepwise patterns and describes the *other* parts sounding underneath.
It never assigns tonal function, quality, metric accent or note hierarchy.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction

from .orchestral_harmony import ScoreSonorityIndex
from .orchestral_voice_leading import ScoreMoment
from .score_texture import ScoreTextureEvidence, WrittenNote


_DIATONIC = {name: index for index, name in enumerate("CDEFGAB")}


@dataclass(frozen=True)
class OrchestralOrnamentFigure:
    source_sha256: str
    part_id: str
    staff: str | None
    voice: str | None
    kind: str  # diatonic_passing_figure | diatonic_neighbor_figure
    source_note_ids: tuple[str, str, str]
    moments: tuple[ScoreMoment, ScoreMoment, ScoreMoment]
    sounding_pitches: tuple[int, int, int]
    written_pitches: tuple[tuple[str, int, int], ...]  # step, alter, octave
    durations_quarters: tuple[Fraction, Fraction, Fraction]
    other_parts_pitch_classes: tuple[tuple[int, ...], ...]
    accompaniment_unchanged: bool
    anchors_present_in_accompaniment: bool
    middle_absent_from_accompaniment: bool
    status: str = "three_note_linear_figure_not_nonchord_tone_annotation"

    @property
    def stable_accompaniment_support_candidate(self) -> bool:
        """Strict observable backing support, not proof of harmonic function."""
        return (self.accompaniment_unchanged
                and self.anchors_present_in_accompaniment
                and self.middle_absent_from_accompaniment)


def _diatonic_number(note: WrittenNote) -> int:
    return 7 * note.written_octave + _DIATONIC[note.written_step]


def _figure_kind(a: WrittenNote, b: WrittenNote, c: WrittenNote) -> str | None:
    left = _diatonic_number(b) - _diatonic_number(a)
    right = _diatonic_number(c) - _diatonic_number(b)
    chromatic_left = b.sounding_midi_pitch - a.sounding_midi_pitch
    chromatic_right = c.sounding_midi_pitch - b.sounding_midi_pitch
    # Enforce actual semitone/whole-tone steps too: altered written seconds
    # can be augmented, and a generic second alone proves too little.
    if not (abs(left) == abs(right) == 1
            and abs(chromatic_left) in (1, 2)
            and abs(chromatic_right) in (1, 2)):
        return None
    if left == right and chromatic_left * chromatic_right > 0:
        return "diatonic_passing_figure"
    if (left == -right and chromatic_left == -chromatic_right
            and a.written_step == c.written_step
            and a.written_alter == c.written_alter
            and a.written_octave == c.written_octave):
        return "diatonic_neighbor_figure"
    return None


def score_ornamental_figures(evidence: ScoreTextureEvidence, *,
                             max_figures: int = 100_000
                             ) -> tuple[OrchestralOrnamentFigure, ...]:
    """Observe contiguous three-note written gestures in one part/voice.

    Restricted to a single measure: current score evidence does not carry
    robust barline continuity or annotated rests. Chords, simultaneous
    attacks in a part, ties and non-contiguous durations are excluded,
    not quietly joined into imagined melodic lines.
    """
    if max_figures < 1:
        raise ValueError("ornamental_figure_budget_invalid")
    by_part: dict[str, dict[ScoreMoment, list[WrittenNote]]] = defaultdict(
        lambda: defaultdict(list))
    for note in evidence.notes:
        by_part[note.part_id][ScoreMoment(note.measure_index,
                                           note.onset_quarters)].append(note)

    index = ScoreSonorityIndex(evidence)
    part_by_source_id = {n.source_note_id: n.part_id for n in evidence.notes}
    figures: list[OrchestralOrnamentFigure] = []
    for part_id in sorted(by_part):
        groups = sorted(by_part[part_id].items(), key=lambda item: (
            item[0].measure_index, item[0].onset_quarters))
        for i in range(1, len(groups) - 1):
            (t0, g0), (t1, g1), (t2, g2) = groups[i - 1:i + 2]
            if (len(g0) != 1 or len(g1) != 1 or len(g2) != 1
                    or t0.measure_index != t1.measure_index
                    or t1.measure_index != t2.measure_index):
                continue
            a, b, c = g0[0], g1[0], g2[0]
            if (a.tied or b.tied or c.tied
                    or a.staff != b.staff or b.staff != c.staff
                    or a.voice != b.voice or b.voice != c.voice
                    or t0.onset_quarters + a.duration_quarters != t1.onset_quarters
                    or t1.onset_quarters + b.duration_quarters != t2.onset_quarters):
                continue
            kind = _figure_kind(a, b, c)
            if kind is None:
                continue
            background = []
            for moment in (t0, t1, t2):
                vertical = index.at(moment)
                pitches = (pitch for note_id, pitch in zip(
                    vertical.active_source_note_ids,
                    vertical.sounding_midi_pitches)
                    if part_by_source_id[note_id] != part_id)
                background.append(tuple(sorted({pitch % 12 for pitch in pitches})))
            stable = bool(background[0]) and background[0] == background[1] == background[2]
            anchor_supported = (a.sounding_midi_pitch % 12 in background[0]
                                and c.sounding_midi_pitch % 12 in background[2])
            middle_absent = b.sounding_midi_pitch % 12 not in background[1]
            figures.append(OrchestralOrnamentFigure(
                source_sha256=evidence.source_sha256, part_id=part_id,
                staff=a.staff, voice=a.voice, kind=kind,
                source_note_ids=(a.source_note_id, b.source_note_id,
                                 c.source_note_id), moments=(t0, t1, t2),
                sounding_pitches=(a.sounding_midi_pitch, b.sounding_midi_pitch,
                                  c.sounding_midi_pitch),
                written_pitches=((a.written_step, a.written_alter,
                                  a.written_octave),
                                 (b.written_step, b.written_alter,
                                  b.written_octave),
                                 (c.written_step, c.written_alter,
                                  c.written_octave)),
                durations_quarters=(a.duration_quarters, b.duration_quarters,
                                    c.duration_quarters),
                other_parts_pitch_classes=tuple(background),
                accompaniment_unchanged=stable,
                anchors_present_in_accompaniment=anchor_supported,
                middle_absent_from_accompaniment=middle_absent,
            ))
            if len(figures) > max_figures:
                raise ValueError("ornamental_figure_budget_exceeded")
    return tuple(figures)
