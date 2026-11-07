"""Apply existing music21 key, chordify and Roman numeral hypothesis tools.

    python -m scripts.extract_harmony piano.mid > harmony.json
"""

import argparse
import json

from anamu.theory_features import music21_harmonic_hypotheses


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("midi_path")
    args = parser.parse_args()
    print(json.dumps(music21_harmonic_hypotheses(args.midi_path),
                     indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
