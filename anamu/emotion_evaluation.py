"""Strict held-out evaluation of externally supplied emotion predictions.

Predictions are intentionally a separate input: a feature extractor cannot
look at the EMOPIA quadrant field to construct its features or predictions.
"""

from __future__ import annotations

from collections import Counter, defaultdict

from .emopia import EmopiaClip, assert_song_disjoint


def majority_class_baseline(train: list[EmopiaClip], held_out: list[EmopiaClip]) -> dict[str, int]:
    """Simple control, trained only on *train* labels; no musical explanation."""
    if not train or any(c.split != "train" for c in train):
        raise ValueError("baseline_requires_training_only")
    if any(c.split == "train" for c in held_out):
        raise ValueError("baseline_target_is_not_held_out")
    assert_song_disjoint(train + held_out)
    counts = Counter(c.quadrant for c in train)
    winner = min(range(1, 5), key=lambda q: (-counts[q], q))
    return {clip.clip_id: winner for clip in held_out}


def evaluate_quadrants(clips: list[EmopiaClip], predictions: dict[str, int],
                       *, split: str = "test") -> dict:
    """Macro-F1, coverage, abstentions, confusion and song-level accuracy.

    Each withheld clip counts: missing predictions are abstentions and reduce
    recall. Macro-F1 uses the four fixed quadrants including absent classes;
    report support so an empty class is not silently declared successful.
    """
    if split not in ("validation", "test"):
        raise ValueError("evaluation_must_be_held_out")
    assert_song_disjoint(clips)
    selected = [c for c in clips if c.split == split]
    if not selected:
        raise ValueError("no_held_out_clips")
    if len({c.clip_id for c in selected}) != len(selected):
        raise ValueError("duplicate_clip_ids")
    if any(not isinstance(v, int) or isinstance(v, bool) or v not in (1, 2, 3, 4)
           for v in predictions.values()):
        raise ValueError("predictions_must_be_quadrants_1_to_4")
    true_support = Counter(c.quadrant for c in selected)
    predicted_counts = Counter()
    tp = Counter()
    confusion = {str(q): {str(p): 0 for p in (*range(1, 5), "abstain")}
                 for q in range(1, 5)}
    song_results: dict[str, list[int]] = defaultdict(list)
    n_predicted = 0
    n_correct = 0
    for clip in selected:
        prediction = predictions.get(clip.clip_id)
        confusion[str(clip.quadrant)][str(prediction) if prediction is not None else "abstain"] += 1
        is_correct = int(prediction == clip.quadrant)
        song_results[clip.song_id].append(is_correct)
        n_correct += is_correct
        if prediction is not None:
            n_predicted += 1
            predicted_counts[prediction] += 1
            tp[clip.quadrant] += is_correct

    def f1_for(q: int) -> float:
        denominator = true_support[q] + predicted_counts[q]
        return 2 * tp[q] / denominator if denominator else 0.0

    return {
        "split": split,
        "total_clips": len(selected),
        "songs": len(song_results),
        "class_support": {str(q): true_support[q] for q in range(1, 5)},
        "coverage": n_predicted / len(selected),
        "clip_accuracy_including_abstentions": n_correct / len(selected),
        "mean_song_accuracy": sum(sum(values) / len(values) for values in song_results.values())
                              / len(song_results),
        "macro_f1_fixed_four_classes": sum(f1_for(q) for q in range(1, 5)) / 4,
        "per_class_f1": {str(q): f1_for(q) for q in range(1, 5)},
        "confusion": confusion,
        "warning": "Clip labels are not moment-by-moment emotions; MIDI is a transcription."
    }
