"""Commands for source inventory, inspection and first-piece analysis."""
from __future__ import annotations

import argparse
from collections import Counter
import gzip
import json
from pathlib import Path

from .knowledge import MODULE_ROOT, REPO_ROOT, compile_knowledge, write_coverage


def output_directory(value, repo):
    path = Path(value).resolve()
    if path.is_relative_to(repo.resolve()) and not path.is_relative_to(MODULE_ROOT):
        raise ValueError("Write analysis outputs inside analysis/ or outside the source repository")
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description="AnaMu — volet indépendant de connaissances et d'analyse")
    parser.add_argument("--repo", type=Path, default=REPO_ROOT)
    commands = parser.add_subparsers(dest="command", required=True)
    inventory = commands.add_parser("inventory", help="Index all course text, reconcile curated concepts and expose coverage")
    inventory.add_argument("--out", type=Path, default=MODULE_ROOT / ".cache/inventory")
    inspect = commands.add_parser("inspect", help="Inspect one course and all its source fragments")
    inspect.add_argument("course_id", help="For example berklee:CM-211")
    analyse = commands.add_parser("analyse", help="Produce an evidence-bound first analysis of a MIDI piece")
    analyse.add_argument("midi", type=Path)
    analyse.add_argument("--midi-profile", choices=["unknown", "gm1"], default="unknown")
    analyse.add_argument("--out", type=Path, default=MODULE_ROOT / ".cache/analysis")
    for modality in ["audio", "score", "lyrics", "context"]:
        analyse.add_argument("--" + modality, type=Path, help="Record a supplied input; interpretation adapter is not yet implemented")
    args = parser.parse_args(argv)
    try:
        if args.command == "inventory":
            knowledge = compile_knowledge(args.repo)
            out = output_directory(args.out, args.repo)
            write_json(out / "coverage.json", {"schema_version": 1,
                "source_fingerprint": knowledge["source_fingerprint"], "coverage": knowledge["coverage"],
                "institutions": dict(Counter(c["institution"] for c in knowledge["courses"])),
                "choice_families": knowledge["choice_families"],
                "multiple_documents_per_course": {k: v for k, v in knowledge["course_identity_groups"].items() if len(v) > 1},
                "contract": knowledge["indexing_contract"]})
            write_coverage(knowledge, out / "courses.csv")
            data = json.dumps(knowledge, ensure_ascii=False, separators=(",", ":")).encode()
            (out / "knowledge.json.gz").write_bytes(gzip.compress(data, mtime=0))
            print(json.dumps(knowledge["coverage"], ensure_ascii=False, indent=2))
        elif args.command == "inspect":
            knowledge = compile_knowledge(args.repo)
            courses = [c for c in knowledge["courses"] if c["course_id"] == args.course_id or c["id"] == args.course_id]
            if not courses:
                raise ValueError("Unknown individual course: " + args.course_id)
            course = courses[0]
            register = next(s["data"] for s in knowledge["structured_sources"]
                            if s["path"] == "docs/data/course-material-progress.json")
            record = register["courses"].get(course["institution"], {}).get(course["code"])
            paths = {c["path"] for c in courses}
            concepts = {id for c in courses for id in c["concept_ids"]}
            print(json.dumps({"course_documents": courses, "fragments": [f for f in knowledge["fragments"] if f["document_path"] in paths],
                "source_register_record": record,
                "concepts": [c for c in knowledge["concepts"] if c["id"] in concepts]}, ensure_ascii=False, indent=2))
        else:
            from .engine import analyse as run, markdown_report
            report = run(args.midi, args.midi_profile, args.repo,
                         {m: getattr(args, m) for m in ["audio", "score", "lyrics", "context"]})
            out = output_directory(args.out, args.repo)
            write_json(out / "report.json", report)
            (out / "report.md").write_text(markdown_report(report), encoding="utf-8")
            print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    except (ValueError, OSError, EOFError, KeyError) as exc:
        parser.exit(2, "Analysis stopped: " + str(exc) + "\n")


if __name__ == "__main__":
    main()
