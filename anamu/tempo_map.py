"""Exact MIDI tick -> performance-second conversion across tempo changes.

Do not treat quarter-note beats as seconds or silently discard tempo maps.
"""

from __future__ import annotations

import bisect
import io
from dataclasses import dataclass


@dataclass(frozen=True)
class TempoSegment:
    tick: int
    seconds: float
    micros_per_quarter: int


@dataclass(frozen=True)
class MidiTempoMap:
    ticks_per_quarter: int
    segments: tuple[TempoSegment, ...]

    @classmethod
    def from_bytes(cls, data: bytes) -> "MidiTempoMap":
        import mido

        midi = mido.MidiFile(file=io.BytesIO(data))
        if midi.type == 2 or midi.ticks_per_beat <= 0:
            raise ValueError("unsupported_midi_time_structure")
        current_tempo = 500_000
        absolute_tick = 0
        elapsed_seconds = 0.0
        result = [TempoSegment(0, 0.0, current_tempo)]
        for message in mido.merge_tracks(midi.tracks):
            delta = message.time
            elapsed_seconds += mido.tick2second(delta, midi.ticks_per_beat, current_tempo)
            absolute_tick += delta
            if message.type == "set_tempo":
                if message.tempo <= 0:
                    raise ValueError("invalid_tempo")
                current_tempo = message.tempo
                segment = TempoSegment(absolute_tick, elapsed_seconds, current_tempo)
                if result[-1].tick == absolute_tick:
                    result[-1] = segment
                else:
                    result.append(segment)
        return cls(ticks_per_quarter=midi.ticks_per_beat, segments=tuple(result))

    def beats_to_seconds(self, beat: float) -> float:
        if beat < 0:
            raise ValueError("negative_beat")
        tick = beat * self.ticks_per_quarter
        positions = [segment.tick for segment in self.segments]
        index = bisect.bisect_right(positions, tick) - 1
        preceding = self.segments[index]
        return preceding.seconds + (tick - preceding.tick) * (
            preceding.micros_per_quarter / 1_000_000 / self.ticks_per_quarter
        )

    def seconds_to_beats(self, seconds: float) -> float:
        """Inverse tempo map, retaining exact historical tempo changes."""
        if seconds < 0:
            raise ValueError("negative_seconds")
        positions = [segment.seconds for segment in self.segments]
        index = bisect.bisect_right(positions, seconds) - 1
        preceding = self.segments[index]
        return (preceding.tick + (seconds - preceding.seconds) *
                1_000_000 * self.ticks_per_quarter / preceding.micros_per_quarter) / self.ticks_per_quarter

    def tempo_changes_seconds(self) -> list[tuple[float, float]]:
        return [(v.seconds, 60_000_000 / v.micros_per_quarter)
                for v in self.segments]
