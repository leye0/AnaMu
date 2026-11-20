#!/usr/bin/env python3
"""Export original MIDI lyric timestamps; this does not infer sung text from notes.

Requires mido 1.3.3. Library functions are used by the acquisition notebook/script.
CLI: python export_embedded_lyrics.py SCORE.mid OUTPUT_DIRECTORY
The CLI exports timestamps without assuming a correspondence to a vocal track.
"""
import argparse
import csv
import json
from pathlib import Path
import mido


def read_midi(path):
    """Prefer UTF-8 lyrics used by LilyPond; preserve older Latin-1 files."""
    try:
        return mido.MidiFile(path, charset="utf-8")
    except UnicodeDecodeError:
        return mido.MidiFile(path, charset="latin1")


def streams(midi):
    notes, lyrics = {}, {}
    for index, track in enumerate(midi.tracks):
        tick, onsets, syllables = 0, {}, []
        for msg in track:
            tick += msg.time
            if msg.type == "note_on" and msg.velocity > 0:
                onsets.setdefault(tick, []).append(msg.note)
            elif msg.type == "lyrics" and msg.text.strip():
                syllables.append((tick, msg.text))
        if onsets:
            notes[index] = onsets
        if syllables:
            lyrics[index] = syllables
    return notes, lyrics


def export_lyrics(midi, destination, mapping=None):
    """mapping is explicit {original lyric track: original note track}.

    A matched tick is a structural consistency observation, not an independent
    validation of which voice sings the syllable. Unmapped tracks stay unmapped.
    """
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    mapping = mapping or {}
    notes, lyrics = streams(midi)
    summary = []
    with (destination / "lyrics-timed.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["lyric_track", "tick", "quarter_offset", "syllable", "note_track", "pitches_at_onset"])
        for index, syllables in lyrics.items():
            selected = mapping.get(index)
            matching = 0
            for tick, text in syllables:
                pitches = notes.get(selected, {}).get(tick, [])
                matching += bool(pitches)
                writer.writerow([index, tick, format(tick / midi.ticks_per_beat, ".12g"), text,
                                 selected if selected is not None else "", ",".join(map(str, pitches))])
            summary.append({"lyric_track_zero_based": index, "note_track_zero_based": selected,
                            "syllables": len(syllables), "matching_note_onsets": matching})
    # Preserve source syllabification; joining with spaces does not reconstruct words.
    text = "\n\n".join(f"[Piste de paroles source {i}]\n" + " ".join(t for _, t in syllables)
                       for i, syllables in lyrics.items())
    (destination / "lyrics-syllables.txt").write_text(text + "\n", encoding="utf-8")
    return {"ticks_per_beat": midi.ticks_per_beat, "streams": summary,
            "syllables": sum(len(s) for s in lyrics.values()),
            "status": "source_timestamps_exported_not_independently_score_validated"}


def export_vocal(midi, destination, selected, lyric_tracks=()):
    """Copy original voice/lyric streams and global timing, without changing notes."""
    result = mido.MidiFile(type=1, ticks_per_beat=midi.ticks_per_beat, charset=midi.charset)
    events = {}
    for track in midi.tracks:
        tick = 0
        for msg in track:
            tick += msg.time
            if msg.type in {"set_tempo", "time_signature", "key_signature", "smpte_offset"}:
                events[(tick, str(msg.copy(time=0)))] = msg.copy(time=0)
    conductor, last = mido.MidiTrack(), 0
    for (tick, _), msg in sorted(events.items()):
        conductor.append(msg.copy(time=tick-last))
        last = tick
    result.tracks.append(conductor)
    for index in dict.fromkeys([*selected, *lyric_tracks]):
        result.tracks.append(mido.MidiTrack(msg.copy() for msg in midi.tracks[index]))
    result.save(destination)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("midi")
    parser.add_argument("output_directory")
    args = parser.parse_args()
    print(json.dumps(export_lyrics(read_midi(args.midi), args.output_directory), ensure_ascii=False, indent=2))
