"""Run the published Partitura tonal-tension algorithm on a local piano MIDI.

    python -m scripts.extract_tonal_tension piano.mid > tension.json
"""

from __future__ import annotations

import argparse
import json

from anamu.theory_features import partitura_tension


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("midi_path")
    parser.add_argument("--window-seconds", type=float, default=1.0)
    parser.add_argument("--hop-seconds", type=float, default=0.5)
    args = parser.parse_args()
    print(json.dumps(partitura_tension(args.midi_path,
                                       window_seconds=args.window_seconds,
                                       hop_seconds=args.hop_seconds),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
