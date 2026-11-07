"""Run 200+ published melody-feature descriptors on eligible MIDI parts.

    python -m scripts.extract_melody_features example.mid > melody-features.json

Will explicitly refuse ambiguous polyphonic parts. The source reference
corpus is the library's published default; see docs/emotion-engine.md.
"""

import argparse
import json

from anamu.melody_toolbox import extract_melody_toolbox


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("midi_path")
    parser.add_argument("--minimum-notes", type=int, default=6)
    args = parser.parse_args()
    print(json.dumps(extract_melody_toolbox(args.midi_path,
                                           minimum_notes=args.minimum_notes),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
