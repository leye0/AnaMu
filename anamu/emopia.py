"""EMOPIA clip manifest and song-disjoint research partitions.

The released EMOPIA MIDI basename encodes Q{1..4}, YouTube video ID and
segment number (as parsed by the upstream MusPy EMOPIA reader).  The label
is *ground truth* and must never be passed to a feature extractor.
"""

from __future__ import annotations

import hashlib
import random
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path


_NAME = re.compile(r"^Q([1-4])_([a-zA-Z0-9_-]{11})_([0-9]+)\.mid$", re.IGNORECASE)


@dataclass(frozen=True)
class EmopiaClip:
    clip_id: str
    song_id: str
    segment_index: int
    quadrant: int
    path: str
    sha256: str
    split: str = "unassigned"

    def to_dict(self) -> dict:
        return asdict(self)


def parse_emopia_filename(filename: str) -> tuple[str, int, int] | None:
    """Return (song ID, segment index, quadrant), or None for other names."""
    match = _NAME.fullmatch(Path(filename).name)
    if not match:
        return None
    quadrant, song_id, segment = match.groups()
    return song_id, int(segment), int(quadrant)


def inventory_emopia(root: str | Path) -> dict:
    """Inventory local files without downloading or modifying the corpus.

    Do not silently exclude malformed .mid names; expose them for audit.
    """
    root = Path(root)
    if not root.is_dir():
        raise ValueError(f"EMOPIA directory does not exist: {root}")
    rows: list[EmopiaClip] = []
    rejects: list[dict] = []
    identities: dict[tuple[str, int], int] = {}
    content_hashes: set[str] = set()
    for file in sorted(root.rglob("*")):
        if not file.is_file() or file.suffix.lower() not in (".mid", ".midi"):
            continue
        relative = file.relative_to(root).as_posix()
        if "__MACOSX" in file.parts or file.name.startswith("._"):
            continue
        parsed = parse_emopia_filename(file.name)
        if parsed is None:
            rejects.append({"path": relative, "reason": "unrecognized_emopia_filename"})
            continue
        song_id, segment_index, quadrant = parsed
        identity = (song_id, segment_index)
        if identity in identities:
            rejects.append({"path": relative, "reason": "duplicate_song_segment"})
            continue
        identities[identity] = quadrant
        checksum = hashlib.sha256(file.read_bytes()).hexdigest()
        if checksum in content_hashes:
            rejects.append({"path": relative, "reason": "duplicate_midi_content"})
            continue
        content_hashes.add(checksum)
        rows.append(EmopiaClip(
            clip_id=f"{song_id}_{segment_index}", song_id=song_id,
            segment_index=segment_index, quadrant=quadrant, path=relative,
            sha256=checksum,
        ))
    return {"clips": rows, "rejected": rejects}


def assign_song_splits(
    clips: list[EmopiaClip], seed: int = 2026,
    train_fraction: float = 0.6, validation_fraction: float = 0.2,
) -> list[EmopiaClip]:
    """Deterministic partitions; all clips of one YouTube song stay together.

    No stratification is assumed. Report per-split counts and class imbalance
    before using the result. Verify other arrangements/remakes separately.
    """
    if train_fraction <= 0 or validation_fraction <= 0 or train_fraction + validation_fraction >= 1:
        raise ValueError("invalid_split_fractions")
    groups = sorted({c.song_id for c in clips})
    if len(groups) < 5:
        raise ValueError("at_least_five_distinct_songs_required")
    random.Random(seed).shuffle(groups)
    n_train = max(1, round(len(groups) * train_fraction))
    n_val = max(1, round(len(groups) * validation_fraction))
    if n_train + n_val >= len(groups):
        n_val = len(groups) - n_train - 1
    split = {song: ("train" if i < n_train else
                    "validation" if i < n_train + n_val else "test")
             for i, song in enumerate(groups)}
    result = [EmopiaClip(**{**c.to_dict(), "split": split[c.song_id]}) for c in clips]
    assert_song_disjoint(result)
    return result


def hold_out_entire_emopia(clips: list[EmopiaClip]) -> list[EmopiaClip]:
    """Preferred protocol: train on independent sources, evaluate all EMOPIA.

    This is only an external test if no EMOPIA labels/MIDI (or versions of its
    songs) were used during model selection, training or pretraining.
    """
    return [EmopiaClip(**{**clip.to_dict(), "split": "test"}) for clip in clips]


def assert_song_disjoint(clips: list[EmopiaClip]) -> None:
    allocation: dict[str, str] = {}
    for clip in clips:
        if clip.split not in ("train", "validation", "test"):
            raise ValueError(f"invalid_split: {clip.split}")
        previous = allocation.setdefault(clip.song_id, clip.split)
        if previous != clip.split:
            raise ValueError(f"song_leakage: {clip.song_id}")


def split_summary(clips: list[EmopiaClip]) -> dict:
    assert_song_disjoint(clips)
    return {name: {
        "clips": sum(c.split == name for c in clips),
        "songs": len({c.song_id for c in clips if c.split == name}),
        "quadrants": {str(q): count for q, count in sorted(Counter(
            c.quadrant for c in clips if c.split == name).items())},
    } for name in ("train", "validation", "test")}
