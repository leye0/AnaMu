"""Conservative orchestral score (MusicXML) / MIDI instrumentation audit.

Only self-declared score and MIDI instrument identities are compared here.
This is not a transcription validator or an audio instrument recognizer.
"""

from __future__ import annotations

import hashlib
import io
import zipfile
from collections import Counter
from xml.etree import ElementTree

from .grammar_foundation import MidiEvidence


def _tag(name: str) -> str:
    return name.rsplit("}", 1)[-1]


def _child(parent, name: str):
    return next((node for node in parent if _tag(node.tag) == name), None)


def _children(parent, name: str):
    return [node for node in parent if _tag(node.tag) == name]


def _text(parent, name: str) -> str | None:
    node = _child(parent, name)
    return (node.text or "").strip() if node is not None else None


def instrument_family(label: str | None) -> str:
    """Transparent spelling normalization, not a learned timbre classifier."""
    name = (label or "").casefold()
    for literal, family in (
        ("english horn", "english_horn"), ("cor anglais", "english_horn"),
        ("violoncello", "cello"), ("cello", "cello"),
        ("contrabass", "contrabass"), ("double bass", "contrabass"),
        ("timpani", "timpani"), ("flute", "flute"), ("oboe", "oboe"),
        ("clarinet", "clarinet"), ("bassoon", "bassoon"),
        ("trumpet", "trumpet"), ("horn", "horn"),
        ("violin", "violin"), ("viola", "viola")
    ):
        if literal in name:
            return family
    return "unknown"


def musicxml_root_from_mxl(mxl_bytes: bytes) -> ElementTree.Element:
    """Read one bounded, partwise MusicXML root from a compressed score."""
    if not zipfile.is_zipfile(io.BytesIO(mxl_bytes)):
        raise ValueError("not_a_compressed_musicxml_zip")
    with zipfile.ZipFile(io.BytesIO(mxl_bytes)) as archive:
        xml_members = [info for info in archive.infolist()
                       if info.filename.endswith(".xml") and
                       not info.filename.startswith("META-INF/")]
        if len(xml_members) != 1 or xml_members[0].file_size > 25_000_000:
            raise ValueError("unsupported_mxl_rootfile_layout_or_size")
        root = ElementTree.fromstring(archive.read(xml_members[0]))
    if _tag(root.tag) != "score-partwise":
        raise ValueError("unsupported_musicxml_score_type")
    return root


def score_part_inventory(mxl_bytes: bytes) -> dict:
    """Read compressed MusicXML's score-part declarations; do not unfold repeats.

    Score pitched-note elements are notation occurrences, not sounding events:
    ties, grace notes, transposition and repetition are not reconstructed.
    """
    root = musicxml_root_from_mxl(mxl_bytes)
    part_list = _child(root, "part-list")
    if part_list is None:
        raise ValueError("missing_musicxml_part_list")
    parts = []
    for score_part in _children(part_list, "score-part"):
        label = _text(score_part, "part-name")
        instruments = [_text(node, "instrument-name")
                       for node in _children(score_part, "score-instrument")]
        instrument = next((name for name in instruments if name), None)
        declared_label = instrument or label
        parts.append({
            "id": score_part.get("id"), "part_name": label,
            "instrument_name": instrument,
            "declared_family": instrument_family(declared_label),
            "pitched_note_elements": 0,
        })
    by_id = {row["id"]: row for row in parts}
    for part in _children(root, "part"):
        if part.get("id") not in by_id:
            raise ValueError("undeclared_musicxml_part")
        pitched = sum(1 for note in part.iter()
                      if _tag(note.tag) == "note" and
                      _child(note, "pitch") is not None)
        by_id[part.get("id")]["pitched_note_elements"] = pitched
    return {"sha256": hashlib.sha256(mxl_bytes).hexdigest(),
            "score_parts": parts, "score_part_count": len(parts),
            "pitched_note_elements": sum(row["pitched_note_elements"]
                                         for row in parts),
            "interpretation": "notated pitched note elements, not unfolded/sounding notes"}


def compare_score_to_midi(score: dict, midi: MidiEvidence) -> dict:
    score_families = Counter(row["declared_family"] for row in score["score_parts"])
    midi_rows = []
    for track in range(midi.track_count):
        events = [event for event in midi.events
                  if event.track == track and event.type == "instrument_name"]
        names = sorted({str(event.field("name")) for event in events})
        # Empty control track is NOT a missing instrument.
        note_count = sum(1 for note in midi.notes if note.track == track)
        if note_count == 0:
            continue
        family = instrument_family(names[0]) if len(names) == 1 else "unknown"
        midi_rows.append({"track": track, "instrument_names": names,
                          "declared_family": family,
                          "key_spans": note_count})
    midi_families = Counter(row["declared_family"] for row in midi_rows)
    keys = sorted(set(score_families) | set(midi_families))
    return {
        "score_sha256": score["sha256"], "midi_sha256": midi.sha256,
        "score_part_count": score["score_part_count"],
        "midi_active_track_count": len(midi_rows),
        "declared_family_comparison": [
            {"family": family, "score_parts": score_families[family],
             "midi_active_tracks": midi_families[family]}
            for family in keys],
        "families_declared_only_in_score": sorted(set(score_families) -
                                                  set(midi_families)),
        "families_declared_only_in_midi": sorted(set(midi_families) -
                                                 set(score_families)),
        "midi_tracks": midi_rows,
        "conclusion": "Declared instrument-family inventory differs; does not establish whether note content matches the score",
    }
