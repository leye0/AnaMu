"""Conservative symbolic melody candidates extracted directly from MIDI bytes.

The output is deliberately *not* labelled as the true melody: MIDI tracks
often contain harmony, accompaniment, multiple voices, or transcriptions.
Only unambiguous monophonic track/channel parts are exposed to the initial
melodic-expectation experiment. No audio preprocessing is required.
"""

from __future__ import annotations

import io
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Note:
    pitch: int
    start_beats: float
    end_beats: float
    velocity: int


@dataclass(frozen=True)
class MelodyCandidate:
    track: int
    channel: int
    notes: tuple[Note, ...]
    intervals: tuple[int, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def extract_monophonic_candidates(midi: bytes, min_notes: int = 3) -> dict:
    """Return conservatively eligible part sequences plus explicit rejections.

    All times are musical *quarter-note beats*, not seconds. SMPTE division,
    format-2 asynchronous tracks, ambiguous retriggers and overlapping notes
    are rejected instead of inventing voice separation.
    """
    import mido

    if min_notes < 2:
        raise ValueError("min_notes must be at least 2")
    score = mido.MidiFile(file=io.BytesIO(midi))
    if score.type == 2 or score.ticks_per_beat <= 0:
        raise ValueError("unsupported_midi_time_structure")
    candidates = []
    rejected = []
    for track_index, track in enumerate(score.tracks):
        # Tracks can share channels. We deliberately do not merge them into
        # a supposed voice: it would falsely fuse independent instruments.
        active: dict[tuple[int, int], list[tuple[int, int]]] = {}
        notes: dict[int, list[tuple[int, int, int, int]]] = {}
        issues: dict[int, set[str]] = {}
        tick = 0
        for message in track:
            tick += message.time
            if message.type not in ("note_on", "note_off") or message.channel == 9:
                continue
            channel = message.channel
            key = (channel, message.note)
            if message.type == "note_on" and message.velocity > 0:
                if active.get(key):
                    issues.setdefault(channel, set()).add("same_pitch_retrigger")
                active.setdefault(key, []).append((tick, message.velocity))
                notes.setdefault(channel, [])
            else:
                if not active.get(key):
                    issues.setdefault(channel, set()).add("unmatched_note_off")
                    continue
                started, velocity = active[key].pop()
                if tick <= started:
                    issues.setdefault(channel, set()).add("zero_duration_note")
                    continue
                notes.setdefault(channel, []).append((started, tick, message.note, velocity))
        for (channel, _), pending in active.items():
            if pending:
                issues.setdefault(channel, set()).add("unclosed_note")
        for channel in sorted(set(notes) | set(issues)):
            raw = sorted(notes.get(channel, []), key=lambda note: (note[0], note[2]))
            reasons = set(issues.get(channel, set()))
            if len(raw) < min_notes:
                reasons.add("too_few_notes")
            if any(next_note[0] < previous_note[1]
                   for previous_note, next_note in zip(raw, raw[1:])):
                reasons.add("polyphonic_or_overlapping_notes")
            if reasons:
                rejected.append({"track": track_index, "channel": channel,
                                 "reasons": sorted(reasons), "notes_observed": len(raw)})
                continue
            events = tuple(Note(pitch=pitch, start_beats=start / score.ticks_per_beat,
                                end_beats=end / score.ticks_per_beat, velocity=velocity)
                           for start, end, pitch, velocity in raw)
            candidates.append(MelodyCandidate(
                track=track_index, channel=channel, notes=events,
                intervals=tuple(b.pitch - a.pitch for a, b in zip(events, events[1:])),
            ).to_dict())
    return {
        "midi_type": score.type,
        "ticks_per_beat": score.ticks_per_beat,
        "time_unit": "quarter_note_beats",
        "candidates_are_verified_melodies": False,
        "candidates": candidates,
        "rejected_parts": rejected,
    }
