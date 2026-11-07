"""Convert an *original* IDyOM .dat file into faithful, event-level JSON.

    python -m scripts.import_idyom_dat ./results.dat --json-out ./results.json

No training, guessed labels, smoothing, or fabricated timestamps occur here.
The source experiment must be audited separately for training leakage.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from anamu.idyom_dat import read_idyom_dat


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dat_file", type=Path)
    parser.add_argument("--json-out", type=Path, required=True)
    parser.add_argument("--max-events", type=int, default=200_000)
    parser.add_argument("--keep-original-fields", action="store_true",
                        help="Also export every native column as its original text; larger JSON")
    args = parser.parse_args()
    target = args.json_out.resolve()
    source = args.dat_file.resolve()
    if source == target:
        parser.error("output_must_not_replace_original_dat")
    result = read_idyom_dat(source, max_events=args.max_events,
                            keep_original_fields=args.keep_original_fields)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                      encoding="utf-8")
    print(json.dumps({"status": "original_idyom_dat_imported",
                      "input_sha256": result["input_sha256"],
                      "melodies": result["melody_count"],
                      "events": result["event_count"],
                      "viewpoints": list(result["viewpoint_columns"]),
                      "json_file": str(target)}, indent=2))


if __name__ == "__main__":
    main()
