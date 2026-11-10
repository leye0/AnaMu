"""Dataset partition guardrails for original IDyOM experiments.

Exact-byte matching cannot detect different arrangements of the same
composition: a separate musical-identity audit remains necessary. Exclusions
are explicit and dataset-agnostic; no emotion corpus is privileged here.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

def _inventory(directory: Path, *, max_files: int) -> dict[str, str]:
    result: dict[str, str] = {}
    candidates = sorted(p for p in directory.rglob("*")
                        if p.is_file() and p.suffix.lower() in (".mid", ".midi"))
    if not candidates:
        raise ValueError(f"empty_idyom_midi_directory: {directory}")
    if len(candidates) > max_files:
        raise ValueError(f"idyom_file_budget_exceeded: {len(candidates)} > {max_files}")
    for path in candidates:
        checksum = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                checksum.update(chunk)
        result[str(path.relative_to(directory))] = checksum.hexdigest()
    return result


def audit_idyom_partitions(test: Path, pretrain: Path, *, max_files: int = 500,
                           excluded_pretrain_names: tuple[str, ...] = ()) -> dict:
    test = test.resolve()
    pretrain = pretrain.resolve()
    if max_files <= 0:
        raise ValueError("max_files_must_be_positive")
    if not test.is_dir() or not pretrain.is_dir() or test == pretrain:
        raise ValueError("idyom_test_pretrain_must_be_distinct_directories")
    if test in pretrain.parents or pretrain in test.parents:
        raise ValueError("idyom_test_pretrain_directory_nesting")
    train_files = _inventory(pretrain, max_files=max_files)
    test_files = _inventory(test, max_files=max_files)
    forbidden = {name.casefold() for name in excluded_pretrain_names}
    excluded = [name for name in train_files
                if Path(name).name.casefold() in forbidden]
    if excluded:
        raise ValueError(f"excluded_pretrain_files: {excluded[:5]}")
    intersection = set(train_files.values()) & set(test_files.values())
    if intersection:
        raise ValueError(f"idyom_exact_content_leakage: {len(intersection)} SHA256 matches")
    return {
        "test_files": len(test_files), "pretrain_files": len(train_files),
        "test_sha256_by_relative_path": test_files,
        "pretrain_sha256_by_relative_path": train_files,
        "excluded_pretrain_names": sorted(forbidden),
        "warnings": ["no_arrangement_or_composition_identity_deduplication",
                     "independent_style_corpus_must_be_verified_for_semantic_overlap",
                     "all_hyperparameters_must_be_locked_before_external_evaluation"],
    }
