"""Summarize an actual known-MIDI run, preserving missing-engine warnings.

The trajectories are AnaMu estimates, NOT listener annotations for these works.
"""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path


def summarize(report: dict) -> str:
    lines = [
        "# AnaMu — analyse de compositions connues",
        "",
        "**Estimations algorithmiques uniquement.** Ces deux œuvres n'ont pas",
        "d'annotations humaines temporelles associées dans VGMIDI ; ce rapport",
        "ne mesure donc **pas** leur justesse émotionnelle. Le modèle est calibré",
        "sur d'autres pièces annotées par des humains.",
        "",
        f"Modèle SHA-256 : `{report.get('calibrated_artifact_sha256', 'inconnu')}`.",
        "",
        "| Composition | Mesures | Valence moyenne | Activation moyenne | Variables observées / apprises | jSymbolic original |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for piece in report["analyses"]:
        rows = piece["emotion_trajectory"]
        if not rows:
            continue
        v = statistics.mean(point["valence"] for point in rows)
        a = statistics.mean(point["arousal"] for point in rows)
        status = piece.get("engine_status", {}).get("jsymbolic", "non rapporté")
        lines.append(
            f"| {piece.get('known_composition', piece['source_midi'])} | {len(rows)} | "
            f"{v:+.3f} | {a:+.3f} | "
            f"{piece['available_feature_columns']}/{piece['trained_feature_columns']} | "
            f"{status} |"
        )
    lines += ["", "## Provenance et limites des moteurs", ""]
    for piece in report["analyses"]:
        lines += [f"### {piece.get('known_composition', piece['source_midi'])}", ""]
        for name, state in piece.get("engine_status", {}).items():
            lines.append(f"- `{name}` : `{state}`")
        for warning in piece.get("warnings", []):
            lines.append(f"- **Limite** : {warning}")
        lines.append("")
    lines += [
        "## Lecture",
        "",
        "Chaque point du graphique correspond à une mesure MIDI, et les valeurs",
        "vont de −1 à +1. L'analyse peut refléter des régularités apprises sur",
        "VGMIDI, mais ni le transfert au répertoire classique ni les émotions de",
        "ses auditeurs n'ont été validés sur Bach ou Chopin.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("markdown", type=Path)
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding="utf-8"))
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.markdown.write_text(summarize(report), encoding="utf-8")
    print(f"Résumé des {len(report['analyses'])} pièces : {args.markdown}")


if __name__ == "__main__":
    main()
