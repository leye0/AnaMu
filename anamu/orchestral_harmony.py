"""Notated vertical sonorities and harmonic context of one note edit.

This is deliberately NOT functional harmony analysis. Exact pitch-class
templates are observational hypotheses only: key, enharmonic spelling,
non-chord tones, cadences and voice roles are not inferred. The purpose is
to expose which actual orchestral notes a counterfactual would affect.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction

from .orchestral_voice_leading import (
    ScoreMoment, VoiceLeadingNoteEdit, VoiceLeadingObservation,
)
from .score_texture import ScoreTextureEvidence, WrittenNote


_TEMPLATES = (
    ("major_triad", (0, 4, 7)),
    ("minor_triad", (0, 3, 7)),
    ("diminished_triad", (0, 3, 6)),
    ("augmented_triad", (0, 4, 8)),
    ("dominant_seventh_shape", (0, 4, 7, 10)),
    ("major_seventh_shape", (0, 4, 7, 11)),
    ("minor_seventh_shape", (0, 3, 7, 10)),
    ("half_diminished_seventh_shape", (0, 3, 6, 10)),
    ("diminished_seventh_shape", (0, 3, 6, 9)),
    ("minor_major_seventh_shape", (0, 3, 7, 11)),
)


@dataclass(frozen=True)
class SonorityTemplate:
    shape: str
    root_pitch_class: int
    bass_chord_member_index: int
    status: str = "pitch_class_template_match_not_functional_harmony"


@dataclass(frozen=True)
class NotatedSonority:
    source_sha256: str
    moment: ScoreMoment
    active_source_note_ids: tuple[str, ...]
    sounding_midi_pitches: tuple[int, ...]
    pitch_classes: tuple[int, ...]
    bass_sounding_pitch: int | None
    matching_templates: tuple[SonorityTemplate, ...]
    status: str = "score_local_vertical_observation"


@dataclass(frozen=True)
class HarmonicEditContext:
    """Descriptive consequence of changing exactly one notated pitch."""

    score_sha256: str
    target_note_id: str
    original: NotatedSonority
    proposed: NotatedSonority
    pitch_classes_added: tuple[int, ...]
    pitch_classes_removed: tuple[int, ...]
    original_target_pitch_class_also_held_by_other_notes: bool
    proposed_target_pitch_class_also_held_by_other_notes: bool
    changes_lowest_sounding_pitch: bool
    status: str = "counterfactual_vertical_effect_not_quality_judgment"


def _templates(pitches: tuple[int, ...]) -> tuple[SonorityTemplate, ...]:
    if not pitches:
        return ()
    observed = {p % 12 for p in pitches}
    bass_class = min(pitches) % 12
    matches = []
    for quality, intervals in _TEMPLATES:
        if len(observed) != len(intervals):
            continue
        for root in range(12):
            if observed != {(root + interval) % 12 for interval in intervals}:
                continue
            bass_interval = (bass_class - root) % 12
            matches.append(SonorityTemplate(
                shape=quality, root_pitch_class=root,
                bass_chord_member_index=intervals.index(bass_interval)))
    return tuple(matches)


def _make_sonority(source_sha: str, moment: ScoreMoment,
                   notes: tuple[WrittenNote, ...],
                   changed_pitch: tuple[str, int] | None = None) -> NotatedSonority:
    pitches = tuple(changed_pitch[1] if changed_pitch and
                    note.source_note_id == changed_pitch[0]
                    else note.sounding_midi_pitch for note in notes)
    return NotatedSonority(
        source_sha256=source_sha, moment=moment,
        active_source_note_ids=tuple(note.source_note_id for note in notes),
        sounding_midi_pitches=pitches,
        pitch_classes=tuple(sorted({p % 12 for p in pitches})),
        bass_sounding_pitch=min(pitches) if pitches else None,
        matching_templates=_templates(pitches))


class ScoreSonorityIndex:
    """Fetch score-local vertical pitch material at exact notated time.

    No repeats are unfolded. Notes reaching over a bar boundary do not
    automatically carry to the next bar: continuity needs a tie-aware pass.
    Sounds are score declarations, not observed acoustic pitches.
    """

    def __init__(self, evidence: ScoreTextureEvidence):
        self.evidence = evidence
        self._by_measure: dict[int, list[WrittenNote]] = defaultdict(list)
        self._by_source_id = {}
        for note in evidence.notes:
            self._by_measure[note.measure_index].append(note)
            if note.source_note_id in self._by_source_id:
                raise ValueError("duplicate_score_note_id")
            self._by_source_id[note.source_note_id] = note
        for notes in self._by_measure.values():
            notes.sort(key=lambda n: (n.onset_quarters, n.sounding_midi_pitch,
                                      n.source_note_id))

    def _active(self, moment: ScoreMoment) -> tuple[WrittenNote, ...]:
        if not (0 <= moment.measure_index < self.evidence.measure_count
                and moment.onset_quarters >= Fraction(0)):
            raise ValueError("sonority_moment_outside_score")
        return tuple(note for note in self._by_measure.get(moment.measure_index, ())
                     if note.onset_quarters <= moment.onset_quarters
                     < note.onset_quarters + note.duration_quarters)

    def at(self, moment: ScoreMoment) -> NotatedSonority:
        return _make_sonority(self.evidence.source_sha256, moment,
                              self._active(moment))

    def context_for_edit(self, observed: VoiceLeadingObservation,
                         edit: VoiceLeadingNoteEdit) -> HarmonicEditContext:
        if (observed.source_sha256 != self.evidence.source_sha256
                or edit.based_on_note_ids != observed.source_note_ids
                or edit.target_note_id != observed.source_note_ids[3]
                or edit.target_part != observed.part_b):
            raise ValueError("counterfactual_source_or_correspondence_mismatch")
        target = self._by_source_id.get(edit.target_note_id)
        if (target is None or target.part_id != observed.part_b
                or target.sounding_midi_pitch != edit.original_sounding_pitch
                or target.measure_index != observed.to_moment.measure_index
                or target.onset_quarters != observed.to_moment.onset_quarters):
            raise ValueError("counterfactual_target_not_in_score")
        active = self._active(observed.to_moment)
        if target not in active:
            raise ValueError("counterfactual_target_not_active")
        original = _make_sonority(self.evidence.source_sha256,
                                  observed.to_moment, active)
        proposed = _make_sonority(self.evidence.source_sha256,
                                  observed.to_moment, active,
                                  (edit.target_note_id, edit.proposed_sounding_pitch))
        other_pcs = {note.sounding_midi_pitch % 12 for note in active if note != target}
        return HarmonicEditContext(
            score_sha256=self.evidence.source_sha256,
            target_note_id=edit.target_note_id,
            original=original, proposed=proposed,
            pitch_classes_added=tuple(sorted(set(proposed.pitch_classes)
                                             - set(original.pitch_classes))),
            pitch_classes_removed=tuple(sorted(set(original.pitch_classes)
                                               - set(proposed.pitch_classes))),
            original_target_pitch_class_also_held_by_other_notes=(
                target.sounding_midi_pitch % 12 in other_pcs),
            proposed_target_pitch_class_also_held_by_other_notes=(
                edit.proposed_sounding_pitch % 12 in other_pcs),
            changes_lowest_sounding_pitch=(
                original.bass_sounding_pitch != proposed.bass_sounding_pitch))
