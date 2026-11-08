"""Human-labelled piano MIDI clips from the PIAST-AT research corpus.

The paper separates emotion/mood, genre and style. Only the first family is
used as the target of the emotion benchmark; generic ``Emotional`` remains
explicitly labelled a mood descriptor, not a discrete felt emotion.

The source contains *aggregated* 3/2/1-annotator agreements, not raw votes.
No label, agreement or caption is ever passed to MIDI feature extraction.
"""

from __future__ import annotations

import csv
import hashlib
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


REVISION = "f391794c63b24ec30f558274c075ae2890ba028c"
REPOSITORY = "Hayeonbang/PIAST"

# PIAST's piano-specific emotion/mood vocabulary, not a list of felt emotions.
MOOD_LABELS = (
    "Happy", "Bright", "Playful", "Cute", "Relaxing/Calm", "Emotional",
    "Dreamy", "Mysterious", "Sad", "Dark", "Tense", "Epic",
    "Intense/Grand", "Passionate", "Powerful", "Upbeat/Energetic",
)
GENRE_LABELS = (
    "Blues", "Ragtime", "Classical", "New-age", "Latin", "Funk", "Ballad",
    "Pop-Piano Cover", "Jazz", "Swing", "Bossa Nova",
)
STYLE_LABELS = ("Difficult/Advanced", "Laid-back", "Easy", "Speedy")
ALL_LABELS = frozenset(MOOD_LABELS + GENRE_LABELS + STYLE_LABELS)
assert len(ALL_LABELS) == 31


@dataclass(frozen=True)
class PIASTClip:
    clip_id: str
    midi_name: str
    song_group: str
    agreement_3: frozenset[str]
    agreement_2: frozenset[str]
    agreement_1: frozenset[str]

    def mood_tags(self, min_agreement: int = 2) -> frozenset[str]:
        if min_agreement not in (1, 2, 3):
            raise ValueError("min_agreement_must_be_1_2_or_3")
        tags = set(self.agreement_3)
        if min_agreement <= 2:
            tags.update(self.agreement_2)
        if min_agreement <= 1:
            tags.update(self.agreement_1)
        return frozenset(tags.intersection(MOOD_LABELS))


def load_annotations(path: str | Path) -> list[PIASTClip]:
    """Read the actual 2023-line CSV; reject malformed or ambiguous records."""
    clips = []
    seen = set()
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        expected = {"AudioFile", "Agreements_3", "Agreements_2", "Agreements_1"}
        if set(reader.fieldnames or []) != expected:
            raise ValueError("invalid_piast_annotation_columns")
        for row in reader:
            # The published CSV has occasional inserted spaces in video IDs,
            # whereas the released MIDI filenames omit them.
            identifier = re.sub(r"\s+", "", row["AudioFile"] or "")
            if not re.fullmatch(r"[A-Za-z0-9_-]{6,80}", identifier) or ".." in identifier:
                raise ValueError("unsafe_piast_audio_id")
            if identifier in seen:
                raise ValueError("duplicate_piast_audio_id")
            seen.add(identifier)
            levels = []
            for number in (3, 2, 1):
                tags = (row[f"Agreements_{number}"] or "").split(",")
                labels = frozenset(v.strip() for v in tags if v.strip())
                unknown = labels.difference(ALL_LABELS)
                if unknown:
                    raise ValueError(f"unknown_piast_tags:{sorted(unknown)}")
                levels.append(labels)
            if levels[0] & levels[1] or levels[0] & levels[2] or levels[1] & levels[2]:
                raise ValueError("conflicting_piast_agreement_levels")
            # '_part_N' means multiple excerpts of one underlying video.
            group = re.sub(r"_part_\d+$", "", identifier)
            clips.append(PIASTClip(identifier, identifier + ".mid", group, *levels))
    return clips


def available_annotations(clips: list[PIASTClip], names: set[str]) -> list[PIASTClip]:
    return [clip for clip in clips if clip.midi_name in names]


def assigned_split(clip: PIASTClip, *, seed: int = 20261108) -> str:
    """Stable song/video-disjoint 70/15/15 split; labels are never consulted."""
    # Independent salt: sampling uses a separate hash, so a downloaded prefix
    # cannot accidentally contain only training clips.
    digest = hashlib.sha256(f"split-v1|{seed}|{clip.song_group}".encode()).digest()
    fraction = int.from_bytes(digest[:8], "big") / 2**64
    return "train" if fraction < .7 else "validation" if fraction < .85 else "test"


def tag_popularity(clips: list[PIASTClip], *, moods_only: bool = True) -> list[dict]:
    allowed = set(MOOD_LABELS) if moods_only else ALL_LABELS
    clips_with_tag = Counter()
    human_votes = Counter()
    majority = Counter()
    for clip in clips:
        for count, labels in ((3, clip.agreement_3), (2, clip.agreement_2),
                              (1, clip.agreement_1)):
            for tag in labels.intersection(allowed):
                clips_with_tag[tag] += 1
                human_votes[tag] += count
                if count >= 2:
                    majority[tag] += 1
    return [{"tag": label, "clips_with_tag": clips_with_tag[label],
             "human_votes": human_votes[label], "majority_clips": majority[label]}
            for label in sorted(allowed, key=lambda k: (-clips_with_tag[k], k))]
