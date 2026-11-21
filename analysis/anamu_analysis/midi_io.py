"""Strict event reading, with no automatic musical voice assignment."""
from __future__ import annotations

from collections import defaultdict, deque
import io
from pathlib import Path

import mido

from .knowledge import sha256


def read_midi(path: Path, profile: str = "unknown") -> dict:
    if profile not in {"unknown", "gm1"}:
        raise ValueError("Supported profiles: unknown or an explicitly declared gm1")
    raw = path.read_bytes()
    midi = mido.MidiFile(file=io.BytesIO(raw), clip=False)
    if midi.type == 2:
        raise ValueError("Type-2 MIDI contains independent sequences; select a sequence before analysing one timeline")
    if midi.ticks_per_beat <= 0:
        raise ValueError("SMPTE division is not implemented; do not interpret it as PPQ")
    notes, controls, programs, tempos, signatures, text_events, tracks, warnings = [], [], [], [], [], [], [], []
    duration = 0
    for ti, track in enumerate(midi.tracks):
        tick = 0
        pending = defaultdict(deque)
        bank = defaultdict(lambda: [None, None])
        program = {}
        channels = set()
        for ei, event in enumerate(track):
            if event.time < 0:
                raise ValueError("Negative event delta")
            tick += event.time
            uid = f"track:{ti}:event:{ei}"
            if hasattr(event, "channel"):
                channels.add(event.channel)
            if event.type == "note_on" and event.velocity > 0:
                key = (event.channel, event.note)
                if pending[key]:
                    warnings.append({"kind": "overlapping_same_key", "event_id": uid,
                                     "meaning": "Note identity ambiguous; FIFO release pairing is an explicit convention"})
                note = {"id": uid, "track": ti, "channel": event.channel, "midi_key": event.note,
                        "onset_tick": tick, "release_tick": None, "key_duration_ticks": None,
                        "velocity": event.velocity, "program_seen_in_source_track_zero_based": program.get(event.channel),
                        "bank_seen_in_source_track": list(bank[event.channel])}
                pending[key].append(note)
                notes.append(note)
            elif event.type == "note_off" or (event.type == "note_on" and event.velocity == 0):
                key = (event.channel, event.note)
                if not pending[key]:
                    warnings.append({"kind": "unmatched_release", "event_id": uid})
                else:
                    note = pending[key].popleft()
                    note.update({"release_tick": tick, "key_duration_ticks": tick - note["onset_tick"],
                                 "release_event_id": uid})
                    if tick == note["onset_tick"]:
                        warnings.append({"kind": "zero_key_duration", "event_id": note["id"]})
            elif event.type == "program_change":
                program[event.channel] = event.program
                programs.append({"event_id": uid, "track": ti, "tick": tick, "channel": event.channel,
                                 "program_zero_based": event.program})
            elif event.type == "control_change":
                controls.append({"event_id": uid, "track": ti, "tick": tick, "channel": event.channel,
                                 "control": event.control, "value": event.value})
                if event.control in (0, 32):
                    bank[event.channel][0 if event.control == 0 else 1] = event.value
                if event.control in (120, 123):
                    warnings.append({"kind": "channel_mode_command_not_simulated", "event_id": uid,
                                     "meaning": "All Sound/Notes Off affects the sounding state; key-release inventory remains literal"})
            elif event.type == "set_tempo":
                tempos.append({"event_id": uid, "track": ti, "tick": tick,
                               "microseconds_per_quarter": event.tempo})
            elif event.type == "time_signature":
                signatures.append({"event_id": uid, "track": ti, "tick": tick,
                    "numerator": event.numerator, "denominator": event.denominator,
                    "clocks_per_click": event.clocks_per_click,
                    "notated_32nd_notes_per_beat": event.notated_32nd_notes_per_beat})
            elif event.type in ("lyrics", "text", "marker", "key_signature"):
                content = event.text if hasattr(event, "text") else event.key
                # Preserve provenance without reproducing a lyric corpus in every report.
                text_events.append({"event_id": uid, "track": ti, "tick": tick, "type": event.type,
                                    "characters": len(content), "content_sha256": sha256(content.encode())})
            elif event.type == "sysex":
                warnings.append({"kind": "sysex_not_interpreted", "event_id": uid,
                                 "meaning": "Device resets or profiles may affect instrument and channel interpretation"})
        for queue in pending.values():
            for note in queue:
                warnings.append({"kind": "unmatched_attack", "event_id": note["id"],
                                 "meaning": "No end-of-track release was invented"})
        duration = max(duration, tick)
        tracks.append({"index": ti, "name": track.name, "event_count": len(track), "end_tick": tick,
                       "channels": sorted(channels)})
    shared = defaultdict(set)
    for track in tracks:
        for channel in track["channels"]:
            shared[channel].add(track["index"])
    for channel, track_indices in shared.items():
        if len(track_indices) > 1:
            warnings.append({"kind": "channel_shared_across_tracks", "channel": channel,
                             "tracks": sorted(track_indices),
                             "meaning": "Cross-track event ordering and channel state require interpretation; no voice merge was inferred"})
    return {"input_path": str(path), "sha256": sha256(raw), "midi_type": midi.type,
        "profile_declared": profile, "ticks_per_quarter": midi.ticks_per_beat,
        "end_tick": duration, "tracks": tracks, "notes": notes, "controls": controls,
        "program_changes": programs, "tempo_events": tempos, "time_signature_events": signatures,
        "text_events": text_events, "warnings": warnings,
        "semantics": {"note_durations": "literal key-release intervals; sustain, acoustical decay and channel mode commands are not simulated",
            "voice_assignment": "none; track/channel is a source partition, not a musical voice",
            "absolute_seconds": "not inferred; event ticks and explicit tempo changes retained",
            "instrument_identity": "program/bank commands do not prove a real instrument",
            "missing_time_signature": "unknown; 4/4 not inferred",
            "percussion": "channel 9 is excluded from pitched sonorities only under the explicit gm1 assumption"}}
