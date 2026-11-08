"""Test the *hypothesis* that MIDI melodic expectancy informs perceived mood.

Egermann et al. (2013), doi:10.3758/s13415-013-0161-y, links musical
expectation violations with emotional responses in concert listeners.
Cheung et al. (2019), doi:10.1016/j.cub.2019.09.067, examines the joint
relationship of musical surprise and uncertainty with pleasure.

Those studies do not claim that this n-gram algorithm predicts PIAST moods.
This is a deliberately small, falsifiable IDyOM-*inspired* approximation,
not IDyOM or a reproduction of any paper's trained model. It uses only MIDI.
The highest note at each onset is a *melody candidate*, not ground truth.

Training-piece observations are always out-of-fold, never evaluated with a
prior learned on their own song/video group. Validation/test use a prior fit
only on all training groups. No emotion label enters feature calculation.
"""

from __future__ import annotations

import hashlib
import io
import math
import random
import statistics
from collections import defaultdict
from pathlib import Path

import mido

from .expectation import VariableOrderExpectancy


def melodic_intervals(path: str | Path) -> tuple[int, ...]:
    """Clip-independent pitch intervals of the highest note at each onset."""
    midi = mido.MidiFile(file=io.BytesIO(Path(path).read_bytes()))
    if midi.type == 2 or midi.ticks_per_beat <= 0:
        raise ValueError("unsupported_midi_for_expectancy")
    onsets: dict[int, list[int]] = defaultdict(list)
    tick = 0
    for event in mido.merge_tracks(midi.tracks):
        tick += event.time
        if event.type == "note_on" and event.velocity > 0 and event.channel != 9:
            onsets[tick].append(event.note)
    highest = [max(onsets[t]) for t in sorted(onsets)]
    if len(highest) < 5:
        raise ValueError("too_few_onsets_for_expectancy")
    return tuple(max(-24, min(24, b - a)) for a, b in zip(highest, highest[1:]))


def _digest(value: str) -> int:
    return int(hashlib.sha256(value.encode()).hexdigest(), 16)


def shuffled_events(events: tuple[int, ...], group: str, seed: int) -> tuple[int, ...]:
    """Deterministic within-clip order control; original token counts intact."""
    shuffled = list(events)
    random.Random(_digest(f"piast-shuffle|{seed}|{group}")).shuffle(shuffled)
    return tuple(shuffled)


def surprise_observations(model: VariableOrderExpectancy,
                          events: tuple[int, ...]) -> dict[str, float]:
    """Uncertainty before event, surprise after event; fixed summary features."""
    surprisal = []
    entropy = []
    entropy_cache: dict[tuple[int, ...], float] = {}
    for i, event in enumerate(events):
        context = events[max(0, i - model.max_order):i] if model.max_order else ()
        if context not in entropy_cache:
            entropy_cache[context] = model.entropy(context)
        entropy.append(entropy_cache[context])
        surprisal.append(-math.log2(model.probability(event, context)))
    if not surprisal:
        raise ValueError("no_events_for_expectancy")
    mean_s = statistics.mean(surprisal)
    mean_e = statistics.mean(entropy)
    ordered = sorted(surprisal)
    n = len(surprisal)
    # Tension/release proxies: positive jumps vs drops in informational surprise.
    changes = [next_ - prev for prev, next_ in zip(surprisal, surprisal[1:])]
    third = max(1, n // 3)
    return {
        "surprise_ic_mean": mean_s,
        "surprise_ic_std": statistics.pstdev(surprisal),
        "surprise_ic_p90": ordered[math.ceil(.9 * n) - 1],
        "surprise_ic_max": max(surprisal),
        "surprise_entropy_before_mean": mean_e,
        "surprise_entropy_before_std": statistics.pstdev(entropy),
        "surprise_entropy_x_ic": statistics.mean(a * b for a, b in zip(entropy, surprisal)),
        "surprise_ic_given_low_entropy": statistics.mean(
            s / (1 + e) for s, e in zip(surprisal, entropy)),
        "surprise_ic_end_minus_start": (statistics.mean(surprisal[-third:])
                                          - statistics.mean(surprisal[:third])),
        "surprise_ic_positive_jump_mean": statistics.mean(max(0., d) for d in changes)
            if changes else 0.,
        "surprise_ic_negative_jump_mean": statistics.mean(max(0., -d) for d in changes)
            if changes else 0.,
        "surprise_event_count": float(n),
    }


def add_out_of_fold_expectancy(splits: dict[str, list[tuple]], root: Path, *,
                               order: int, shuffle: bool = False,
                               seed: int = 20261108, folds: int = 5) -> dict:
    """Mutate feature dicts in place; fit only training MIDI, by source group.

    Every training clip is evaluated on a prior excluding *every* clip from
    its song_group, including same-song transcriptions and excerpts.
    """
    if folds < 2 or order < 0:
        raise ValueError("invalid_expectancy_experiment")
    sequences = {}
    groups = {}
    for records in splits.values():
        for clip, _ in records:
            sequences[clip.clip_id] = melodic_intervals(root / "midi" / clip.midi_name)
            groups[clip.clip_id] = str(clip.song_group)
    train = splits["train"]
    if not train:
        raise ValueError("empty_expectancy_training")

    fold_id = {clip.clip_id: _digest(f"piast-fold|{seed}|{clip.song_group}") % folds
               for clip, _ in train}
    fold_counts = {}
    for current in sorted(set(fold_id.values())):
        held_out = [(clip, features) for clip, features in train
                    if fold_id[clip.clip_id] == current]
        prior_sequences = [sequences[clip.clip_id] for clip, _ in train
                           if fold_id[clip.clip_id] != current]
        if not prior_sequences:
            raise ValueError("not_enough_training_folds")
        model = VariableOrderExpectancy(max_order=order, smoothing=2.0).fit(prior_sequences)
        for clip, features in held_out:
            events = sequences[clip.clip_id]
            if shuffle:
                events = shuffled_events(events, groups[clip.clip_id], seed)
            features.update(surprise_observations(model, events))
        fold_counts[str(current)] = len(held_out)

    full_prior = VariableOrderExpectancy(max_order=order, smoothing=2.0).fit(
        [sequences[clip.clip_id] for clip, _ in train])
    for split in ("validation", "test"):
        for clip, features in splits[split]:
            events = sequences[clip.clip_id]
            if shuffle:
                events = shuffled_events(events, groups[clip.clip_id], seed)
            features.update(surprise_observations(full_prior, events))
    return {
        "model": "smoothed variable-order interval n-gram; not original IDyOM",
        "prior_max_order": order, "smoothing": 2.0, "shuffled_event_order": shuffle,
        "training_prior": "out-of-fold, source-group-exclusive",
        "validation_test_prior": "all train groups only",
        "training_fold_sizes": fold_counts,
        "melody_viewpoint": "upper-pitch-onset candidate, interval clipped to +/-24 semitones",
    }
