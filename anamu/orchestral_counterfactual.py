"""Generative falsification of one narrow orchestral technique: doubling.

Learn an exact unison/octave relation from a short prefix of two notated
parts. Hide the subsequent target part, generate its next notes from the
source part alone, and *only then* compare predictions with the score.
This is an in-piece structural reconstruction test, not musical creativity,
listening quality, style transfer or leave-one-composition-out validation.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations

from .score_texture import ScoreTextureEvidence, WrittenNote


@dataclass(frozen=True)
class GeneratedScoreNote:
    source_note_id: str
    measure_index: int
    onset_quarters: Fraction
    duration_quarters: Fraction
    source_sounding_pitch: int
    predicted_sounding_pitch: int


@dataclass(frozen=True)
class DoublingCompletionTrial:
    score_sha256: str
    source_part: str
    target_part: str
    octave_offset: int
    training_source_note_ids: tuple[str, ...]
    training_target_note_ids: tuple[str, ...]
    generated: tuple[GeneratedScoreNote, ...]
    exact_matches: tuple[bool, ...]
    constant_pitch_baseline_matches: tuple[bool, ...]
    unison_copy_baseline_matches: tuple[bool, ...]
    method: str = "prefix_learned_octave_relation_hidden_target_continuation"


def doubling_reconstruction_trials(
    evidence: ScoreTextureEvidence, *, training_notes: int = 3,
    prediction_notes: int = 3, max_trials: int = 20_000,
) -> tuple[DoublingCompletionTrial, ...]:
    """Predict held-out target notes from a source line and a learned shift.

    Training selection can see target notes ONLY in the prefix. Future target
    notes are consulted at scoring time, after all generated notes exist.
    Source-onset windows are disjoint per source/target pair to limit repeated
    test usage. Chords/ties in the prefix are rejected rather than flattened.
    Every score position is (measure index, fractional quarter offset).
    """
    if training_notes < 2 or prediction_notes < 1 or max_trials < 1:
        raise ValueError("counterfactual_trial_budget_invalid")
    grouped: dict[str, dict[tuple[int, Fraction], list[WrittenNote]]] = defaultdict(
        lambda: defaultdict(list))
    for note in evidence.notes:
        grouped[note.part_id][note.measure_index, note.onset_quarters].append(note)
    positions = {part: {time: grouped[part][time] for time in sorted(grouped[part])}
                 for part in grouped}
    trials: list[DoublingCompletionTrial] = []
    window_size = training_notes + prediction_notes

    for source, target in permutations(sorted(positions), 2):
        source_stream = list(positions[source].items())
        target_notes = positions[target]
        target_indices = {time: index for index, time in enumerate(target_notes)}
        # Non-overlapping source windows; no target future read for selection.
        for start in range(0, len(source_stream) - window_size + 1, window_size):
            prefix = source_stream[start:start + training_notes]
            target_prefix = [target_notes.get(time) for time, _ in prefix]
            if any(len(notes) != 1 or notes[0].tied for _, notes in prefix):
                continue
            if any(other is None or len(other) != 1 or other[0].tied
                   for other in target_prefix):
                continue
            source_prefix = [notes[0] for _, notes in prefix]
            target_prefix_notes = [other[0] for other in target_prefix]
            indices = [target_indices[time] for time, _ in prefix]
            if any(indices[i] != indices[i-1] + 1 for i in range(1, len(indices))):
                continue
            deltas = {b.sounding_midi_pitch - a.sounding_midi_pitch
                      for a, b in zip(source_prefix, target_prefix_notes)}
            if len(deltas) != 1 or next(iter(deltas)) not in (-24, -12, 0, 12, 24):
                continue
            if any(a.duration_quarters != b.duration_quarters
                   for a, b in zip(source_prefix, target_prefix_notes)):
                continue
            shift = next(iter(deltas))

            future = source_stream[start + training_notes:start + window_size]
            if any(len(notes) != 1 or notes[0].tied for _, notes in future):
                continue
            # Generative step: do not inspect the withheld target notes here.
            generated = tuple(GeneratedScoreNote(
                source_note_id=notes[0].source_note_id,
                measure_index=time[0], onset_quarters=time[1],
                duration_quarters=notes[0].duration_quarters,
                source_sounding_pitch=notes[0].sounding_midi_pitch,
                predicted_sounding_pitch=notes[0].sounding_midi_pitch + shift)
                for time, notes in future)

            # Evaluation step: target note values first become visible here.
            matches = []
            baseline = []
            unison_baseline = []
            last_target_pitch = target_prefix_notes[-1].sounding_midi_pitch
            for predicted in generated:
                observed = target_notes.get((predicted.measure_index,
                                             predicted.onset_quarters), [])
                valid = len(observed) == 1 and not observed[0].tied
                matches.append(bool(valid and
                                    observed[0].sounding_midi_pitch ==
                                    predicted.predicted_sounding_pitch and
                                    observed[0].duration_quarters ==
                                    predicted.duration_quarters))
                baseline.append(bool(valid and
                                     observed[0].sounding_midi_pitch ==
                                     last_target_pitch and
                                     observed[0].duration_quarters ==
                                     predicted.duration_quarters))
                unison_baseline.append(bool(valid and
                                            observed[0].sounding_midi_pitch ==
                                            predicted.source_sounding_pitch and
                                            observed[0].duration_quarters ==
                                            predicted.duration_quarters))
            trials.append(DoublingCompletionTrial(
                score_sha256=evidence.source_sha256,
                source_part=source, target_part=target,
                octave_offset=shift // 12,
                training_source_note_ids=tuple(n.source_note_id for n in source_prefix),
                training_target_note_ids=tuple(n.source_note_id
                                               for n in target_prefix_notes),
                generated=generated,
                exact_matches=tuple(matches),
                constant_pitch_baseline_matches=tuple(baseline),
                unison_copy_baseline_matches=tuple(unison_baseline)))
            if len(trials) > max_trials:
                raise ValueError("counterfactual_trial_budget_exceeded")
    return tuple(trials)
