"""Make an SVG of AnaMu's inferred trajectories on known classic works.

No human reference lines are drawn: Bach and Chopin in the bundled music21
corpus are not part of the temporally human-annotated VGMIDI benchmark.
"""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("svg", type=Path)
    args = parser.parse_args()
    pieces = json.loads(args.report.read_text(encoding="utf-8"))["analyses"]
    if not pieces:
        raise ValueError("no_known_works_to_plot")
    width, row_height = 1350, 195
    height = 125 + row_height * len(pieces)
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" '
        'aria-label="Analyse des émotions inférées par mesure sur des pièces classiques connues">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<style>text{font-family:Arial,sans-serif;fill:#283340}.heading{font-size:16px;font-weight:bold}'
        '.small{font-size:12px}.axis{stroke:#cad3dc;stroke-width:1}'
        '.valence{fill:none;stroke:#167b75;stroke-width:3}'
        '.arousal{fill:none;stroke:#ad4033;stroke-width:3}</style>',
        '<text x="28" y="36" style="font-size:25px;font-weight:bold">AnaMu — Bach et Chopin : émotions estimées</text>',
        '<text x="28" y="62" class="small">Valence (vert) et activation (rouge), de −1 à +1, par mesure ; '
        'aucune annotation humaine correspondante disponible.</text>',
    ]
    for index, piece in enumerate(pieces):
        rows = piece["emotion_trajectory"]
        top, left, plot_width, plot_height = 86 + index * row_height, 48, 1235, 123
        def position_x(item):
            return round(left + plot_width * (item["measure"] - 1) / max(len(rows) - 1, 1), 1)
        def position_y(value):
            return round(top + 24 + (1 - value) * plot_height / 2, 1)
        def coords(axis):
            return " ".join(f"{position_x(x)},{position_y(x[axis])}" for x in rows)
        caption = html.escape(piece.get("known_composition", piece["source_midi"]))
        out.extend([
            f'<text x="{left}" y="{top+13}" class="heading">{caption} — {len(rows)} mesures</text>',
            f'<line x1="{left}" y1="{position_y(0)}" x2="{left+plot_width}" y2="{position_y(0)}" class="axis"/>',
            f'<polyline class="valence" points="{coords("valence")}"/>',
            f'<polyline class="arousal" points="{coords("arousal")}"/>',
            f'<text x="{left}" y="{top+plot_height+45}" class="small">Mesure 1</text>',
            f'<text x="{left+plot_width-90}" y="{top+plot_height+45}" class="small">Mesure {len(rows)}</text>',
        ])
    out.append('</svg>')
    args.svg.parent.mkdir(parents=True, exist_ok=True)
    args.svg.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"{len(pieces)} known works plotted: {args.svg}")


if __name__ == "__main__":
    main()
