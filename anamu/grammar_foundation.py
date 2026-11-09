"""AnaMu Grammar G0: lossless-source, conservative MIDI event foundation.

This is *not* a music grammar parser. It is the event evidence layer on which
parallel musical interpretations can be built. Original MIDI bytes, complete
message payloads, track-local order and exact ticks are retained. Only
unambiguously matched key-press spans are interpreted as note instances.

MIDI velocity, CC7/CC11 and key-off do not determine acoustic loudness or
the end of a sustained sound. A set_tempo event does not prove musical rubato.
"""

from __future__ import annotations

import hashlib
import io
from bisect import bisect_right
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


def _frozen_value(value):
    """Preserve message values without leaking mutable lists into the IR."""
    if isinstance(value, (tuple, list)):
        return tuple(_frozen_value(item) for item in value)
    if isinstance(value, bytearray):
        return bytes(value)
    if isinstance(value, (int, float, str, bytes, bool, type(None))):
        return value
    raise ValueError(f"unsupported_midi_message_field:{type(value).__name__}")


@dataclass(frozen=True)
class MidiEvent:
    id: str
    track: int
    index_in_track: int
    tick: int
    delta_ticks: int
    type: str
    is_meta: bool
    fields: tuple[tuple[str, object], ...]

    def field(self, name: str, default=None):
        return next((value for key, value in self.fields if key == name), default)


@dataclass(frozen=True)
class NoteSpan:
    """An unambiguous *key press*, not inferred audio sustain or voice role."""

    onset_event_id: str
    release_event_id: str
    track: int
    channel: int
    pitch: int
    velocity: int
    release_velocity: int
    start_tick: int
    end_tick: int

    def overlaps(self, other: "NoteSpan") -> bool:
        """Half-open key-down spans; exact simultaneity is also overlap."""
        return max(self.start_tick, other.start_tick) < min(self.end_tick,
                                                            other.end_tick)


@dataclass(frozen=True)
class Diagnostic:
    code: str
    source_event_ids: tuple[str, ...]


@dataclass(frozen=True)
class TempoAnchor:
    tick: int
    micros_per_quarter: int
    elapsed_micros: Fraction
    source_event_id: str | None  # None = MIDI 500000-us/quarter default


@dataclass(frozen=True)
class MidiEvidence:
    """All original bytes plus analysis-friendly, immutable MIDI event views."""

    raw_bytes: bytes
    sha256: str
    midi_type: int
    ticks_per_beat: int
    timebase: str
    track_count: int
    events: tuple[MidiEvent, ...]
    notes: tuple[NoteSpan, ...]
    tempo_anchors: tuple[TempoAnchor, ...]
    diagnostics: tuple[Diagnostic, ...]

    def events_of_type(self, *types: str) -> tuple[MidiEvent, ...]:
        return tuple(event for event in self.events if event.type in types)

    def beat_at_tick(self, tick: int) -> Fraction:
        if tick < 0:
            raise ValueError("negative_midi_tick")
        if self.timebase != "ppq":
            raise ValueError("musical_beat_unknown_for_smpte_division")
        return Fraction(tick, self.ticks_per_beat)

    def seconds_at_tick(self, tick: int) -> Fraction:
        """Exact rational playback time under explicit MIDI tempo messages.

        This is *not* a performance-intent inference. If two different tempo
        values occur on independent tracks at one tick, temporal mapping is
        undefined rather than arbitrarily choosing a track's event.
        """
        if tick < 0:
            raise ValueError("negative_midi_tick")
        if self.timebase != "ppq":
            raise ValueError("seconds_conversion_unsupported_for_smpte_division")
        if any(d.code in {"conflicting_tempo_at_tick", "invalid_tempo"}
               for d in self.diagnostics):
            raise ValueError("ambiguous_or_invalid_tempo_map")
        anchors = self.tempo_anchors
        index = bisect_right([point.tick for point in anchors], tick) - 1
        anchor = anchors[index]
        elapsed = (anchor.elapsed_micros +
                   Fraction((tick - anchor.tick) * anchor.micros_per_quarter,
                            self.ticks_per_beat))
        return elapsed / 1_000_000

    def summary(self) -> dict:
        """Small, explicitly *non-lossless* presentation of a raw-preserved IR."""
        return {
            "sha256": self.sha256, "midi_type": self.midi_type,
            "timebase": self.timebase, "ticks_per_beat": self.ticks_per_beat,
            "track_count": self.track_count,
            "event_count": len(self.events), "unambiguous_key_spans": len(self.notes),
            "tempo_anchor_count": len(self.tempo_anchors),
            "diagnostics": [diagnostic.code for diagnostic in self.diagnostics],
            "audio_loudness": None, "sounding_end_after_pedal": None,
            "inferred_instrument": None,
        }


def _tempo_anchors(events: tuple[MidiEvent, ...], ticks_per_beat: int,
                   diagnostics: list[Diagnostic]) -> tuple[TempoAnchor, ...]:
    """MIDI default 120 BPM, then source-explicit tempo changes at ticks."""
    if ticks_per_beat <= 0:
        return ()
    tempos: dict[int, list[MidiEvent]] = {}
    for event in events:
        if event.type != "set_tempo":
            continue
        value = event.field("tempo")
        if not isinstance(value, int) or not 1 <= value <= 0xFFFFFF:
            diagnostics.append(Diagnostic("invalid_tempo", (event.id,)))
            continue
        tempos.setdefault(event.tick, []).append(event)

    anchors = [TempoAnchor(0, 500_000, Fraction(0), None)]
    current_tick, current_tempo, elapsed_micros = 0, 500_000, Fraction(0)
    for tick, batch in sorted(tempos.items()):
        # Within one track, event order is specified even for identical ticks.
        # Across tracks, there is no authoritative ordering: contradictory
        # simultaneous tempo assignments must remain unresolved.
        last_per_track: dict[int, MidiEvent] = {}
        for event in batch:
            last_per_track[event.track] = event
        values = {event.field("tempo") for event in last_per_track.values()}
        if len(values) != 1:
            diagnostics.append(Diagnostic("conflicting_tempo_at_tick",
                                          tuple(event.id for event in last_per_track.values())))
            continue
        elapsed_micros += Fraction((tick - current_tick) * current_tempo,
                                   ticks_per_beat)
        current_tick, current_tempo = tick, values.pop()
        anchor = TempoAnchor(tick, current_tempo, elapsed_micros,
                             next(reversed(last_per_track.values())).id)
        if anchors[-1].tick == tick:
            anchors[-1] = anchor
        else:
            anchors.append(anchor)
    return tuple(anchors)


def midi_evidence(data: bytes | bytearray) -> MidiEvidence:
    """Ingest MIDI format 0/1; do not merge notes or assume a principal voice.

    Format 2 tracks are asynchronous and are rejected pending a dedicated
    format-2 alignment model. SMPTE divisions are retained as tick evidence,
    but never mapped to invented quarter-note beats.
    """
    import mido

    original = bytes(data)
    midi = mido.MidiFile(file=io.BytesIO(original))
    if midi.type not in (0, 1):
        raise ValueError("unrelated_format_two_tracks_not_supported")
    if midi.ticks_per_beat == 0:
        raise ValueError("zero_midi_time_division")

    events: list[MidiEvent] = []
    diagnostics: list[Diagnostic] = []
    notes: list[NoteSpan] = []
    for track_index, track in enumerate(midi.tracks):
        tick = 0
        # Repeated same-pitch key-downs are genuinely ambiguous in SMF;
        # never silently impose LIFO/FIFO pairing or voice separation.
        pending: dict[tuple[int, int], list[MidiEvent]] = {}
        for message_index, message in enumerate(track):
            delta = message.time
            if not isinstance(delta, int) or delta < 0:
                raise ValueError("invalid_midi_delta_ticks")
            tick += delta
            payload = tuple(sorted((key, _frozen_value(value))
                                   for key, value in message.dict().items()))
            event = MidiEvent(
                id=f"t{track_index}:e{message_index}", track=track_index,
                index_in_track=message_index, tick=tick, delta_ticks=delta,
                type=message.type, is_meta=message.is_meta, fields=payload)
            events.append(event)

            if message.type not in ("note_on", "note_off"):
                continue
            key = (message.channel, message.note)
            if message.type == "note_on" and message.velocity > 0:
                if pending.get(key):
                    diagnostics.append(Diagnostic(
                        "same_pitch_retrigger_ambiguous",
                        tuple(v.id for v in pending[key]) + (event.id,)))
                pending.setdefault(key, []).append(event)
                continue
            active = pending.get(key, [])
            if not active:
                diagnostics.append(Diagnostic("unmatched_key_release", (event.id,)))
            elif len(active) > 1:
                diagnostics.append(Diagnostic(
                    "ambiguous_key_release",
                    tuple(v.id for v in active) + (event.id,)))
            else:
                started = active.pop()
                notes.append(NoteSpan(
                    onset_event_id=started.id, release_event_id=event.id,
                    track=track_index, channel=message.channel, pitch=message.note,
                    velocity=started.field("velocity"),
                    release_velocity=message.velocity, start_tick=started.tick,
                    end_tick=event.tick))
                if started.tick == event.tick:
                    diagnostics.append(Diagnostic(
                        "zero_duration_key_span", (started.id, event.id)))
        for opened in pending.values():
            for event in opened:
                diagnostics.append(Diagnostic("unclosed_key_press", (event.id,)))

    # Track order is only a deterministic tie breaker. Equal-tick events on
    # different tracks have no inferred causal ordering.
    ordered = tuple(sorted(events, key=lambda event: (
        event.tick, event.track, event.index_in_track)))
    spans = tuple(sorted(notes, key=lambda note: (
        note.start_tick, note.track, note.onset_event_id)))
    anchors = _tempo_anchors(ordered, midi.ticks_per_beat, diagnostics)
    return MidiEvidence(
        raw_bytes=original, sha256=hashlib.sha256(original).hexdigest(),
        midi_type=midi.type, ticks_per_beat=midi.ticks_per_beat,
        timebase="ppq" if midi.ticks_per_beat > 0 else "smpte",
        track_count=len(midi.tracks), events=ordered, notes=spans,
        tempo_anchors=anchors, diagnostics=tuple(diagnostics))


def midi_evidence_from_file(path: str | Path) -> MidiEvidence:
    return midi_evidence(Path(path).read_bytes())
