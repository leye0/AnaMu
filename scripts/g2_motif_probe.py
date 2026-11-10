"""Reproducible G2 candidate inventory; no theme labels or human validation.

Usage: python -m scripts.g2_motif_probe [MIDI ...] [--top 8] [--output file.json]
No large downloads or paid services. JSON is written only when requested.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from anamu.grammar_foundation import midi_evidence_from_file
from anamu.grammar_motifs import discover_exact_motifs


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MIDI = (
    ROOT / "data/orchestral/beethoven5-movement1.mid",
    ROOT / "data/orchestral/beethoven7-movement2.mid",
)


def inspect(paths: list[Path], *, top: int = 8, min_onsets: int = 3,
            max_onsets: int = 5) -> dict:
    if not 0 <= top <= 200:
        raise ValueError("preview_limit_must_be_between_0_and_200")
    rows = []
    for path in paths:
        evidence = midi_evidence_from_file(path)
        discovered = discover_exact_motifs(evidence, min_onsets=min_onsets,
                                            max_onsets=max_onsets)
        preview = []
        for candidate in discovered.candidates[:top]:
            preview.append({
                "signature_sha256": candidate.signature_sha256,
                "note_count": candidate.note_count,
                "onset_count": candidate.onset_count,
                "occurrence_count": len(candidate.occurrences),
                "occurrences": [{"track": o.track, "channel": o.channel,
                                 "start_tick": o.start_tick, "end_tick": o.end_tick,
                                 "onset_event_ids": o.onset_event_ids}
                                for o in candidate.occurrences],
                "verified_transforms": [{
                    "transposition_semitones": t.transposition_semitones,
                    "time_scale_numerator": t.time_scale.numerator,
                    "time_scale_denominator": t.time_scale.denominator,
                    "source_event_ids": t.source_event_ids}
                    for t in candidate.transforms_from_first],
            })
        rows.append({
            "file": str(path), "source_sha256": evidence.sha256,
            "note_count": len(evidence.notes),
            "candidates_total": len(discovered.candidates),
            "candidates_previewed": len(preview), "preview_only": True,
            "windows_examined": discovered.windows_examined,
            "dense_windows_skipped": discovered.dense_windows_skipped,
            "strands_examined": discovered.strands_examined,
            "percussion_notes_excluded": discovered.percussion_notes_excluded,
            "nonpositive_notes_excluded": discovered.nonpositive_notes_excluded,
            "candidates": preview,
        })
    return {
        "claim": "exact_transposition_and_rhythmic_scaling_candidates_not_confirmed_themes",
        "method": "track_channel_consecutive_onset_windows_not_full_SIATEC",
        "human_reference_compared": False,
        "parameters": {"min_onsets": min_onsets, "max_onsets": max_onsets,
                       "preview_top": top},
        "pieces": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("midi", nargs="*", type=Path,
                        help="MIDI input; default is both pinned Beethoven movements")
    parser.add_argument("--top", type=int, default=8,
                        help="Explicit preview limit; total candidate counts always shown")
    parser.add_argument("--min-onsets", type=int, default=3)
    parser.add_argument("--max-onsets", type=int, default=5)
    parser.add_argument("--output", type=Path,
                        help="Optional JSON path; default prints results only")
    args = parser.parse_args()
    report = inspect(args.midi or list(DEFAULT_MIDI), top=args.top,
                     min_onsets=args.min_onsets, max_onsets=args.max_onsets)
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
        print(f"Written {args.output}")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
