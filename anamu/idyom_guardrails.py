"""Leakage audit for original IDyOM experiments, before launching Lisp.

Hash matching cannot detect different arrangements of the same composition;
that requires a separate metadata/music-identity audit. But exact-byte
duplicates and the labelled EMOPIA benchmark must never silently leak into
the pretraining side of a claimed external evaluation.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from .emopia import parse_emopia_filename


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
                           allow_emopia_test: bool = False) -> dict:
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
    train_emopia = [name for name in train_files
                    if parse_emopia_filename(Path(name).name) is not None]
    if train_emopia:
        raise ValueError(f"emopia_forbidden_in_idyom_pretraining: {train_emopia[:5]}")
    test_emopia = [name for name in test_files
                   if parse_emopia_filename(Path(name).name) is not None]
    if test_emopia and not allow_emopia_test:
        raise ValueError("emopia_external_test_requires_explicit_opt_in")
    intersection = set(train_files.values()) & set(test_files.values())
    if intersection:
        raise ValueError(f"idyom_exact_content_leakage: {len(intersection)} SHA256 matches")
    return {
        "test_files": len(test_files), "pretrain_files": len(train_files),
        "test_sha256_by_relative_path": test_files,
        "pretrain_sha256_by_relative_path": train_files,
        "emopia_test_detected": bool(test_emopia),
        "warnings": ["no_arrangement_or_composition_identity_deduplication",
                     "independent_style_corpus_must_be_verified_for_semantic_overlap",
                     "all_hyperparameters_must_be_locked_before_external_emopia_test"],
    }
