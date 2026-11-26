"""Maintain the P1 source edition without collapsing source identity into its path.

This module audits a checkout or synchronizes metadata. It reads all source
documents but never edits the course Markdown, shared sources, or corpus.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from copy import deepcopy
import hashlib
import json
from pathlib import Path
from typing import Any

from .knowledge import REPO_ROOT, compile_knowledge

MANIFEST = Path("analysis/knowledge/source-manifest.json")


def sha1_blob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def discover(repo: Path) -> tuple[list[dict], str, list[dict]]:
    knowledge = compile_knowledge(repo)
    registered = {row["path"] for row in knowledge["courses"]
                  if row["primary_registered_material_file"]}
    found: list[dict] = []
    for doc in knowledge["documents"]:
        path = doc["path"]
        found.append({
            "path": path,
            "kind": "course_markdown" if doc["kind"] == "course"
                    else "shared_markdown",
            "course_id": doc.get("course_id"),
            "registered_course_material": path in registered,
            "git_blob_sha1": doc["git_blob_sha1"],
            "size_bytes": (repo / path).stat().st_size,
            "document_sha256": doc["sha256"],
        })
    for structured in knowledge["structured_sources"]:
        path = structured["path"]
        raw = (repo / path).read_bytes()
        found.append({
            "path": path, "kind": "structured_register_json",
            "course_id": None, "registered_course_material": False,
            "git_blob_sha1": sha1_blob(raw), "size_bytes": len(raw),
            "document_sha256": structured["sha256"],
        })
    paths = [row["path"] for row in found]
    if len(paths) != len(set(paths)):
        raise ValueError("Duplicate source paths")
    return sorted(found, key=lambda row: row["path"]), knowledge["source_fingerprint"], knowledge["excluded_operational_documents"]


def next_id(existing: list[dict]) -> int:
    try:
        return max((int(item["id"].split(":")[-1]) for item in existing),
                   default=0)
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("Malformed existing source ID") from error


def reconcile(previous: dict, fresh: list[dict], fingerprint: str,
              excluded: list[dict]) -> tuple[dict, dict]:
    old = deepcopy(previous.get("sources", []))
    ids = [row["id"] for row in old]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate source IDs in previous manifest")
    seen_paths = [row["path"] for row in old]
    if len(seen_paths) != len(set(seen_paths)):
        raise ValueError("Duplicate paths in previous manifest")
    fresh_paths = {row["path"] for row in fresh}
    previous_by_path = {row["path"]: row for row in old}
    missing_by_blob: dict[str, list[dict]] = defaultdict(list)
    for row in old:
        if row["path"] not in fresh_paths:
            missing_by_blob[row["git_blob_sha1"]].append(row)
    new_blobs: dict[str, int] = defaultdict(int)
    for row in fresh:
        if row["path"] not in previous_by_path:
            new_blobs[row["git_blob_sha1"]] += 1

    counter = next_id(old)
    reconciled: list[dict] = []
    changes = {"unchanged": 0, "changed": [], "added": [],
               "relocated_requires_review": [], "missing_retained": []}
    claimed: set[str] = set()
    for observed in fresh:
        path, blob = observed["path"], observed["git_blob_sha1"]
        previous_row = previous_by_path.get(path)
        relocated = False
        if previous_row is None:
            candidates = missing_by_blob.get(blob, [])
            if len(candidates) == 1 and new_blobs[blob] == 1:
                previous_row = candidates[0]
                relocated = True
        if previous_row is None:
            counter += 1
            record = {
                "id": f"source:{counter:06d}",
                "disposition": "source_frozen_pending_complete_material_review",
                "source_revision": 1, "review_required": True,
                "status_note": "Discovered source, not semantically reviewed."
            }
            changes["added"].append(record["id"])
        else:
            if previous_row["id"] in claimed:
                raise ValueError("A source identity was reused twice: " +
                                 previous_row["id"])
            claimed.add(previous_row["id"])
            record = deepcopy(previous_row)
            previous_blob = record["git_blob_sha1"]
            if previous_blob != blob:
                record["source_revision"] = record.get("source_revision", 1) + 1
                record["review_required"] = True
                record["prior_disposition"] = record.get("disposition")
                record["disposition"] = "source_changed_requires_reinspection"
                record["status_note"] = "Source bytes changed; semantic bindings need review."
                changes["changed"].append(record["id"])
            elif relocated:
                record["review_required"] = True
                record.setdefault("previous_paths", []).append(record["path"])
                record["status_note"] = "Unique byte-identical relocation proposed; verify attribution."
                changes["relocated_requires_review"].append(record["id"])
            else:
                changes["unchanged"] += 1
        record.update(observed)
        record["lifecycle"] = "present"
        reconciled.append(record)

    for previous_row in old:
        if previous_row["id"] not in claimed and \
                previous_row["path"] not in fresh_paths:
            missing = deepcopy(previous_row)
            missing["lifecycle"] = "source_missing_not_deleted"
            missing["review_required"] = True
            missing["status_note"] = "Prior document missing in current edition; identity retained."
            reconciled.append(missing)
            changes["missing_retained"].append(missing["id"])
    reconciled.sort(key=lambda row: int(row["id"].split(":")[-1]))
    if len({row["id"] for row in reconciled}) != len(reconciled):
        raise ValueError("Duplicate source identity after reconciliation")
    counts: dict[str, int] = defaultdict(int)
    for row in reconciled:
        if row["lifecycle"] == "present":
            counts[row["kind"]] += 1
    counts["total_source_documents"] = sum(
        row["lifecycle"] == "present" for row in reconciled)
    counts["operational_documents_excluded"] = len(excluded)
    counts["source_identities_preserved_missing"] = len(changes["missing_retained"])
    new = {
        "schema_version": 1,
        "edition_id": previous.get("edition_id", "anamu-current-sources"),
        "git_snapshot": previous.get("git_snapshot"),
        "working_copy_source_fingerprint": fingerprint,
        "contract": "Git blob identity and sha256 fingerprint source bytes; source inclusion does not mean semantic understanding.",
        "counts": dict(sorted(counts.items())),
        "excluded_operational_sources": [
            {"path": row["path"], "reason": row["reason"]}
            for row in excluded
        ],
        "sources": reconciled,
    }
    return new, changes


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="AnaMu P1 source edition audit")
    parser.add_argument("--repo", type=Path, default=REPO_ROOT)
    parser.add_argument("command", choices=["audit", "sync"])
    args = parser.parse_args(argv)
    try:
        repo = args.repo.resolve()
        path = repo / MANIFEST
        previous = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        fresh, fingerprint, excluded = discover(repo)
        manifest, changes = reconcile(previous, fresh, fingerprint, excluded)
        if args.command == "sync":
            path.parent.mkdir(parents=True, exist_ok=True)
            written = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
            if not path.exists() or path.read_text(encoding="utf-8") != written:
                path.write_text(written, encoding="utf-8")
        print(json.dumps({"mode": args.command, "counts": manifest["counts"],
                          "changes": changes,
                          "warning": "This is a source-file audit, not a semantic or musical validation."},
                         ensure_ascii=False, indent=2))
    except (OSError, ValueError, TypeError, KeyError) as error:
        parser.exit(2, "Source manifest stopped: " + str(error) + "\n")


if __name__ == "__main__":
    main()
