"""Create a compact, standalone SVG of the ten real human-vs-model curves.

python -m scripts.plot_vgmidi_temporal report.json comparison.svg
No external chart dependency and no original MIDI included in the artifact.
"""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding="utf-8"))
    pieces = report["ten_held_out_pieces"]
    if len(pieces) != 10:
        raise ValueError("expected_exactly_ten_heldout_pieces")

    width, height = 1540, 1900
    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" '
        'aria-label="Valence et activation par mesure sur 10 pièces; humains versus AnaMu">',
        '<style>text{font-family:Arial,sans-serif;fill:#29333d} .small{font-size:13px} '
        '.heading{font-size:16px;font-weight:bold} .axis{stroke:#becbd2;stroke-width:1} '
        '.human{stroke:#168477;stroke-width:2.5;fill:none} '
        '.model{stroke:#c34432;stroke-width:2.5;fill:none;stroke-dasharray:7 4} '
        '.iqr{fill:#168477;fill-opacity:.13;stroke:none}</style>',
        f'<rect width="{width}" height="{height}" fill="white"/>',
        '<text x="40" y="45" style="font-size:27px;font-weight:bold">'
        'VGMIDI — humains vs AnaMu : dix thèmes connus, réservés au test</text>',
        '<text x="40" y="72" class="small">'
        'Courbes en fonction de la mesure; ligne verte = médiane de 28 à 32 auditeurs, '
        'zone verte = quartiles, pointillés rouges = estimation émotionnelle AnaMu</text>',
    ]
    for index, piece in enumerate(pieces):
        samples = piece["time_series"]
        top = 105 + index * 177
        for column, (name, label) in enumerate((("valence", "Valence"),
                                                ("arousal", "Activation"))):
            left = 42 + 760 * column
            plot_x, plot_y, plot_w, plot_h = left + 32, top + 30, 664, 101
            count = len(samples)
            def x_coord(measure):
                return round(plot_x + (measure - 1) * plot_w / max(count - 1, 1), 1)
            def y_coord(value):
                return round(plot_y + (1 - value) * plot_h / 2, 1)
            def points(key: str, descending: bool = False) -> str:
                seq = reversed(samples) if descending else samples
                return " ".join(f"{x_coord(s['measure'])},{y_coord(s[key])}" for s in seq)
            caption = html.escape(piece["piece"])
            elements.extend([
                f'<text x="{left+32}" y="{top+16}" class="heading">{caption} — {label}</text>',
                f'<line x1="{plot_x}" y1="{plot_y+plot_h/2}" '
                f'x2="{plot_x+plot_w}" y2="{plot_y+plot_h/2}" class="axis"/>',
                f'<text x="{left+3}" y="{plot_y+9}" class="small">+1</text>',
                f'<text x="{left+12}" y="{plot_y+plot_h/2+4}" class="small">0</text>',
                f'<text x="{left+5}" y="{plot_y+plot_h+4}" class="small">−1</text>',
                f'<polygon class="iqr" points="{points(name+"_q25")} '
                f'{points(name+"_q75", True)}"/>',
                f'<polyline class="human" points="{points(name+"_median")}"/>',
                f'<polyline class="model" points="{points("model_"+name)}"/>',
                f'<text x="{plot_x}" y="{plot_y+plot_h+20}" class="small">Mesure 1</text>',
                f'<text x="{plot_x+plot_w-105}" y="{plot_y+plot_h+20}" class="small">'
                f'Mesure {count}</text>',
            ])
    elements += [
        '<text x="40" y="1885" class="small">Source : Ferreira &amp; Whitehead, VGMIDI ; '
        'ensemble de test réservé avant apprentissage. Corrélation temporelle modeste.</text>',
        '</svg>',
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(elements) + "\n", encoding="utf-8")
    print(f"{len(pieces)} real time-series pairs: {args.output}")


if __name__ == "__main__":
    main()
