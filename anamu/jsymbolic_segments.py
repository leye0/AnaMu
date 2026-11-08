"""Bounded, note-preserving MIDI segments for running original jSymbolic.

Only section/window features may be reassembled across segments. Original
whole-piece jSymbolic features cannot be reconstructed from excerpts.
"""

from __future__ import annotations

import hashlib
import io
from dataclasses import dataclass
from pathlib import Path

from .tempo_map import MidiTempoMap


@dataclass(frozen=True)
class MidiSegment:
    path: Path
    source_sha256: str
    first_measure: int
    stop_measure_exclusive: int
    start_seconds: float
    stop_seconds: float
    source_unmatched_note_off_count: int
    source_unclosed_note_on_count: int


def split_midi_measures(source: Path, destination: Path, *,
                        measure_count: int, max_measures: int = 16) -> list[MidiSegment]:
    """Split at written bar boundaries; clip and re-start crossing notes.

    Retains each original track, channel, program and tempo history. Does not
    transpose, concatenate measures, or infer a changed metre. Synthetic note
    boundaries are required for independently executable excerpts, and are
    explicitly disclosed to downstream consumers.
    """
    import mido

    if max_measures < 2 or measure_count <= 0:
        raise ValueError("invalid_segment_measure_budget")
    raw = source.read_bytes()
    midi = mido.MidiFile(file=io.BytesIO(raw))
    if midi.type == 2 or midi.ticks_per_beat <= 0:
        raise ValueError("unsupported_segment_midi_type")
    signatures = {(msg.numerator, msg.denominator)
                  for track in midi.tracks for msg in track if msg.type == "time_signature"}
    if len(signatures) > 1:
        raise ValueError("cannot_segment_changing_metre")
    numerator, denominator = next(iter(signatures)) if signatures else (4, 4)
    ticks_per_bar = midi.ticks_per_beat * numerator * 4 / denominator
    if not ticks_per_bar.is_integer():
        raise ValueError("non_integer_measure_tick_boundary")
    ticks_per_bar = int(ticks_per_bar)
    timeline = MidiTempoMap.from_bytes(raw)

    # Parse absolute notes once, with strict note pairing. Keep original track
    # identities and channel metadata for instrument/polyphony features.
    track_content = []
    unmatched_off = unclosed_on = note_on_count = 0
    for track in midi.tracks:
        position = 0
        open_notes = {}
        notes = []
        other = []
        for message in track:
            position += message.time
            if message.type in ("note_on", "note_off"):
                token = (message.channel, message.note)
                if message.type == "note_on" and message.velocity > 0:
                    note_on_count += 1
                    open_notes.setdefault(token, []).append((position, message.velocity))
                elif open_notes.get(token):
                    start, velocity = open_notes[token].pop(0)
                    if position > start:
                        notes.append((start, position, message.channel, message.note, velocity))
                else:
                    # Some known music21 source MIDI encodes inconsistent
                    # note-off pitches. Those invalid events have no provable
                    # sounding-note correspondence; account for their loss.
                    unmatched_off += 1
            elif message.type != "end_of_track":
                other.append((position, message))
        unclosed_on += sum(map(len, open_notes.values()))
        track_content.append((notes, other))
    if not note_on_count or (unmatched_off + unclosed_on) / note_on_count > .1:
        raise ValueError("excessive_unpaired_midi_notes_for_segmentation")

    destination.mkdir(parents=True, exist_ok=True)
    slices = []
    for first in range(0, measure_count, max_measures):
        stop = min(first + max_measures, measure_count)
        left, right = first * ticks_per_bar, stop * ticks_per_bar
        excerpt = mido.MidiFile(type=midi.type, ticks_per_beat=midi.ticks_per_beat)
        for notes, metadata in track_content:
            events = []
            # Independent files need the state that preceded this excerpt.
            initial = {}
            for tick, msg in metadata:
                if tick > left:
                    break
                if msg.type in ("set_tempo", "time_signature", "key_signature",
                                "track_name", "instrument_name"):
                    initial[(msg.type, None)] = msg
                elif msg.type in ("program_change", "control_change"):
                    key = (msg.type, msg.channel,
                           msg.control if msg.type == "control_change" else None)
                    initial[key] = msg
            for msg in initial.values():
                events.append((0, 0, msg))
            for tick, msg in metadata:
                if left < tick < right:
                    events.append((tick - left, 0, msg))
            for on, off, channel, pitch, velocity in notes:
                if off <= left or on >= right:
                    continue
                start = max(left, on) - left
                end = min(right, off) - left
                events.append((start, 2, mido.Message("note_on", channel=channel,
                                                       note=pitch, velocity=velocity)))
                events.append((end, 1, mido.Message("note_off", channel=channel,
                                                     note=pitch, velocity=0)))
            events.sort(key=lambda item: (item[0], item[1]))
            result_track = mido.MidiTrack()
            last = 0
            for tick, _, message in events:
                result_track.append(message.copy(time=tick - last))
                last = tick
            result_track.append(mido.MetaMessage("end_of_track", time=right - left - last))
            excerpt.tracks.append(result_track)
        path = destination / f"segment-{first + 1:04d}-{stop:04d}.mid"
        excerpt.save(path)
        slices.append(MidiSegment(path=path,
                                  source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                                  first_measure=first + 1,
                                  stop_measure_exclusive=stop + 1,
                                  start_seconds=timeline.beats_to_seconds(first * ticks_per_bar /
                                                                          midi.ticks_per_beat),
                                  stop_seconds=timeline.beats_to_seconds(stop * ticks_per_bar /
                                                                         midi.ticks_per_beat),
                                  source_unmatched_note_off_count=unmatched_off,
                                  source_unclosed_note_on_count=unclosed_on))
    return slices
