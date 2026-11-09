"""Compare score part-list families with observed source MIDI track labels."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from anamu.grammar_foundation import midi_evidence_from_file  # noqa: E402
from anamu.score_inventory import (compare_score_to_midi,  # noqa: E402
                                   score_part_inventory)


def run(manifest: Path) -> dict:
    sources = json.loads(manifest.read_text(encoding="utf-8"))
    comparisons = []
    for piece in sources["pieces"]:
        ref = piece["score_reference"]
        for relative in (piece["file"], ref["file"]):
            if not (ROOT / relative).resolve().is_relative_to(
                    (ROOT / "data/orchestral").resolve()):
                raise ValueError("source_outside_corpus_directory")
        midi = midi_evidence_from_file(ROOT / piece["file"])
        score = score_part_inventory((ROOT / ref["file"]).read_bytes())
        if midi.sha256 != piece["sha256"] or score["sha256"] != ref["sha256"]:
            raise ValueError(f"source_checksum_mismatch:{piece['id']}")
        comparisons.append({"id": piece["id"], "work": piece["work"],
                            "score_source": ref["source"],
                            "score_inventory": score,
                            "midi_score_comparison": compare_score_to_midi(score, midi)})
    return {"schema_version": 1,
            "scope": "instrument labels and written score part-counts only",
            "no_audio_or_midi_note_alignment_inference": True,
            "pieces": comparisons}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path,
                        default=ROOT / "data/orchestral/SOURCES.json")
    parser.add_argument("--output", type=Path,
                        default=ROOT / "reports/orchestral-score-inventory-2026-11-09.json")
    args = parser.parse_args()
    result = run(args.manifest)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False,
                                      sort_keys=True) + "\n", encoding="utf-8")
    for row in result["pieces"]:
        c = row["midi_score_comparison"]
        print(f"{row['id']}: score={c['score_part_count']} parts, "
              f"MIDI={c['midi_active_track_count']} active tracks, "
              f"score-only={c['families_declared_only_in_score']}, "
              f"MIDI-only={c['families_declared_only_in_midi']}")


if __name__ == "__main__":
    main()
