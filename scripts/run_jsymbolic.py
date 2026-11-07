"""Adapter to jSymbolic's *existing* Java MIDI feature extractor.

Install the upstream jSymbolic2.jar and its lib directory yourself.
No imitation of its 246 features; the original tool is run unmodified.

    python -m scripts.run_jsymbolic piano.mid --jar /opt/jSymbolic/jSymbolic2.jar \
        --out ./reports --window-seconds 5 --overlap 0.5 --execute

Creates ACE XML and CSV outputs when explicitly executed. The documented
jSymbolic -csv -window CLI is used with fixed arrays, never shell commands.
Its feature-definition XML path is generated automatically by jSymbolic
from the sole feature-values XML path (suffix ``_FeatDefs.xml``).
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

from anamu.jsymbolic_ace import read_jsymbolic_ace


def build_jsymbolic_command(jar: Path, midi: Path, values: Path,
                            window_seconds: float, overlap: float,
                            heap_gb: int = 2) -> list[str]:
    if window_seconds <= 0 or not (0 <= overlap < 1):
        raise ValueError("window_seconds must be > 0 and overlap in [0, 1)")
    if not 1 <= heap_gb <= 16:
        raise ValueError("heap_gb must be between 1 and 16")
    for path in (jar, midi):
        if not path.is_file():
            raise ValueError(f"missing_input_file: {path}")
    if midi.suffix.lower() not in (".mid", ".midi", ".mei"):
        raise ValueError("unsupported_symbolic_format")
    return ["java", f"-Xmx{heap_gb}g", "-jar", str(jar.resolve()),
            "-csv", "-window", str(midi.resolve()),
            str(values.resolve()),
            str(window_seconds), str(overlap)]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("midi_path", type=Path)
    parser.add_argument("--jar", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--window-seconds", type=float, default=5.0)
    parser.add_argument("--overlap", type=float, default=0.5)
    parser.add_argument("--heap-gb", type=int, default=2)
    parser.add_argument("--max-minutes", type=int, default=10)
    parser.add_argument("--json-out", type=Path,
                        help="Optional parsed ACE 1.1 JSON output (explicit path)")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    output = args.out.resolve()
    values = output / "features.xml"
    definitions = output / "features_FeatDefs.xml"
    command = build_jsymbolic_command(args.jar, args.midi_path, values,
                                       args.window_seconds, args.overlap, args.heap_gb)
    if not args.execute:
        print(json.dumps({"status": "dry_run", "command": command,
                          "expected_csv": str(values.with_suffix(".csv"))}, indent=2))
        return
    if shutil.which("java") is None:
        parser.error("Java runtime unavailable")
    if args.max_minutes <= 0:
        parser.error("--max-minutes must be positive")
    output.mkdir(parents=True, exist_ok=True)
    # jSymbolic resolves paths relative to the jar directory. All paths above
    # are absolute, so this cwd is only for finding upstream lib/ dependencies.
    completed = subprocess.run(command, cwd=args.jar.resolve().parent,
                               capture_output=True, text=True,
                               timeout=args.max_minutes * 60)
    if completed.returncode:
        raise RuntimeError("jSymbolic_original_java_failed: "
                           f"exit={completed.returncode}; "
                           f"stdout_tail={completed.stdout[-3000:]!r}; "
                           f"stderr_tail={completed.stderr[-3000:]!r}")
    if not values.is_file():
        raise RuntimeError("jSymbolic_returned_without_ace_values: "
                           f"{values}; stdout_tail={completed.stdout[-3000:]!r}; "
                           f"stderr_tail={completed.stderr[-3000:]!r}")
    if not definitions.is_file() or not values.with_suffix(".csv").is_file():
        raise RuntimeError("jSymbolic_missing_requested_feature_outputs: "
                           f"stdout_tail={completed.stdout[-3000:]!r}; "
                           f"stderr_tail={completed.stderr[-3000:]!r}")
    imported = read_jsymbolic_ace(values)
    if imported["data_set_count"] != 1 or imported["window_count"] < 1:
        raise RuntimeError("jSymbolic_did_not_return_windowed_features_for_one_midi")
    if args.json_out:
        target = args.json_out.resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(imported, indent=2, ensure_ascii=False) + "\n",
                          encoding="utf-8")
    print(json.dumps({"status": "completed", "stdout": completed.stdout[-2000:],
                      "csv": str(values.with_suffix(".csv")),
                      "values_xml": str(values), "definitions_xml": str(definitions),
                      "data_set_count": imported["data_set_count"],
                      "window_count": imported["window_count"],
                      "feature_values_sha256": imported["input_sha256"],
                      "parsed_json": str(args.json_out.resolve()) if args.json_out else None},
                     indent=2))


if __name__ == "__main__":
    main()
