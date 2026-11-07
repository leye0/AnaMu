"""Optional entry point to the *original* IDyOM engine via py2lispIDyOM.

    python -m scripts.run_original_idyom --test ./midi-test --pretrain ./midi-train \
        --history ./experiments/idyom --execute

No emulated IDyOM, no implicit download. Requires SBCL + a working IDyOM
installation and py2lispIDyOM; upstream runtime/config may require setup.
This experiment must NEVER use the EMOPIA held-out music in pretraining.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from anamu.idyom_guardrails import audit_idyom_partitions


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--test", required=True, type=Path)
    parser.add_argument("--pretrain", required=True, type=Path)
    parser.add_argument("--history", required=True, type=Path)
    parser.add_argument("--target-viewpoints", default="cpitch,onset")
    parser.add_argument("--source-viewpoints", default="cpitch,onset")
    parser.add_argument("--max-midi-files", type=int, default=500,
                        help="Per-partition bound; avoid unexpected bulk runs")
    parser.add_argument("--allow-emopia-test", action="store_true",
                        help="Explicit opt-in; never use EMOPIA in pretraining")
    parser.add_argument("--execute", action="store_true", help="opt in to original SBCL analysis")
    args = parser.parse_args()
    test = args.test.resolve()
    train = args.pretrain.resolve()
    try:
        audit = audit_idyom_partitions(test, train, max_files=args.max_midi_files,
                                       allow_emopia_test=args.allow_emopia_test)
    except ValueError as exc:
        parser.error(str(exc))

    def digest_manifest(sha_by_path: dict[str, str]) -> str:
        serialized = json.dumps(sha_by_path, sort_keys=True).encode("utf-8")
        return hashlib.sha256(serialized).hexdigest()

    configuration = {
        "engine": "py2lispIDyOM.IDyOMExperiment invoking the original IDyOM",
        "test": str(test), "pretrain": str(train),
        "history": str(args.history.resolve()),
        "target_viewpoints": args.target_viewpoints.split(","),
        "source_viewpoints": args.source_viewpoints.split(","),
        "models": ":both", "detail": 3, "k": 1,
        "partition_audit": {
            "pretrain_files": audit["pretrain_files"],
            "test_files": audit["test_files"],
            "pretrain_manifest_sha256": digest_manifest(audit["pretrain_sha256_by_relative_path"]),
            "test_manifest_sha256": digest_manifest(audit["test_sha256_by_relative_path"]),
            "emopia_test_detected": audit["emopia_test_detected"],
        },
        "execute": args.execute,
        "warnings": audit["warnings"],
    }
    if not args.execute:
        print(json.dumps(configuration, indent=2, ensure_ascii=False))
        return
    if shutil.which("sbcl") is None:
        parser.error("SBCL binary not found; install original IDyOM requirements first")
    try:
        from py2lispIDyOM.run import IDyOMExperiment
    except ImportError:
        parser.error("Install py2lispIDyOM and the original IDyOM first")
    experiment = IDyOMExperiment(
        test_dataset_path=str(test),
        pretrain_dataset_path=str(train),
        experiment_history_folder_path=str(args.history.resolve()),
    )
    experiment.set_parameters(
        target_viewpoints=configuration["target_viewpoints"],
        source_viewpoints=configuration["source_viewpoints"],
        models=":both", k=1, detail=3,
    )
    # This executes the upstream Lisp engine. Runtime/errors belong to its
    # environment; do not claim a valid result merely from process launch.
    experiment.run()


if __name__ == "__main__":
    main()
