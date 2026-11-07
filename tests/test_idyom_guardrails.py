"""Prevent exact training/test leakage before launching the original engine."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from anamu.idyom_guardrails import audit_idyom_partitions


class IdyomGuardrailTests(unittest.TestCase):
    def test_reject_exact_content_duplicates_even_when_filenames_differ(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            test, train = root / "test", root / "train"
            test.mkdir()
            train.mkdir()
            (test / "one.mid").write_bytes(b"exactly-the-same-contents")
            (train / "other.mid").write_bytes(b"exactly-the-same-contents")
            with self.assertRaisesRegex(ValueError, "idyom_exact_content_leakage"):
                audit_idyom_partitions(test, train)

    def test_annotated_emopia_cannot_be_used_for_pretraining(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            test, train = root / "test", root / "train"
            test.mkdir()
            train.mkdir()
            (test / "neutral.mid").write_bytes(b"different")
            (train / "Q1_0vLPYiPN7qY_0.mid").write_bytes(b"emopia")
            with self.assertRaisesRegex(ValueError, "emopia_forbidden_in_idyom_pretraining"):
                audit_idyom_partitions(test, train)

    def test_emopia_test_requires_explicit_opt_in_and_does_not_enter_training(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            test, train = root / "test", root / "train"
            test.mkdir()
            train.mkdir()
            (test / "Q4_0vLPYiPN7qY_9.mid").write_bytes(b"test")
            (train / "reference.mid").write_bytes(b"train")
            with self.assertRaisesRegex(ValueError, "emopia_external_test_requires_explicit"):
                audit_idyom_partitions(test, train)
            audited = audit_idyom_partitions(test, train, allow_emopia_test=True)
            self.assertTrue(audited["emopia_test_detected"])
            self.assertEqual(audited["pretrain_files"], 1)

    def test_bounded_inputs_and_non_nested_dirs(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            test, train = root / "test", root / "train"
            test.mkdir()
            train.mkdir()
            (test / "first.mid").write_bytes(b"first")
            (test / "second.mid").write_bytes(b"second")
            (train / "third.mid").write_bytes(b"third")
            with self.assertRaisesRegex(ValueError, "idyom_file_budget_exceeded"):
                audit_idyom_partitions(test, train, max_files=1)
            with self.assertRaisesRegex(ValueError, "idyom_test_pretrain_directory_nesting"):
                audit_idyom_partitions(test, root)

    def test_original_runner_dry_run_reports_partition_fingerprints(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            test, train = root / "test", root / "train"
            test.mkdir()
            train.mkdir()
            (test / "first.mid").write_bytes(b"first")
            (train / "second.mid").write_bytes(b"second")
            proc = subprocess.run(
                [sys.executable, "-m", "scripts.run_original_idyom", "--test", str(test),
                 "--pretrain", str(train), "--history", str(root / "history")],
                capture_output=True, check=True, text=True,
            )
            import json
            parsed = json.loads(proc.stdout)
            self.assertFalse(parsed["execute"])
            self.assertEqual(parsed["partition_audit"]["pretrain_files"], 1)
            self.assertEqual(len(parsed["partition_audit"]["test_manifest_sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
