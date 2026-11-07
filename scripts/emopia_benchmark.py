"""Auditable EMOPIA manifest, deterministic partition, and held-out scoring.

    python -m scripts.emopia_benchmark /path/to/EMOPIA --seed 2026
    python -m scripts.emopia_benchmark /path/to/EMOPIA --predictions predictions.jsonl

The optional prediction file has one row per clip:
    {"clip_id": "0vLPYiPN7qY_0", "quadrant": 2}

No dataset download or algorithm training is performed here.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from anamu.emopia import (assign_song_splits, hold_out_entire_emopia,
                          inventory_emopia, split_summary)
from anamu.emotion_evaluation import evaluate_quadrants, majority_class_baseline


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--protocol", choices=("external", "internal"),
                        default="external", help="external: all EMOPIA is held out")
    parser.add_argument("--predictions", type=Path, help="JSONL predictions on held-out clips")
    parser.add_argument("--manifest-out", type=Path, help="write an explicit reproducible JSON manifest")
    args = parser.parse_args()

    inventory = inventory_emopia(args.root)
    clips = (hold_out_entire_emopia(inventory["clips"])
             if args.protocol == "external"
             else assign_song_splits(inventory["clips"], seed=args.seed))
    if args.manifest_out:
        args.manifest_out.write_text(
            "\n".join(json.dumps(clip.to_dict(), ensure_ascii=False) for clip in clips) + "\n",
            encoding="utf-8",
        )
    report = {
        "dataset": "EMOPIA", "protocol": args.protocol,
        "split_seed": args.seed if args.protocol == "internal" else None,
        "counts": split_summary(clips), "rejections": inventory["rejected"],
        "research_status": "No independent emotional predictive validation without predictions",
    }
    if args.protocol == "internal":
        train = [c for c in clips if c.split == "train"]
        held_out = [c for c in clips if c.split == "test"]
        baseline = majority_class_baseline(train, held_out)
        report["baseline_majority_train_only"] = evaluate_quadrants(clips, baseline)
    else:
        report["strict_external_requirement"] = (
            "Model and all decisions must be frozen without any EMOPIA labels, "
            "MIDI or overlapping song arrangements used in training.")
    if args.predictions:
        predictions: dict[str, int] = {}
        with args.predictions.open(encoding="utf-8") as stream:
            for line in stream:
                if not line.strip():
                    continue
                row = json.loads(line)
                key = row["clip_id"]
                if key in predictions:
                    raise ValueError(f"duplicate_prediction: {key}")
                predictions[key] = row["quadrant"]
        report["model"] = evaluate_quadrants(clips, predictions)
        report["research_status"] = "Scoring complete; inspect provenance, overlap and leakage"
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
