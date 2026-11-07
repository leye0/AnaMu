"""Audited import of *original executed* IDyOM outputs into existing MIDI bars.

The Lisp engine is not bundled here. Only externally produced, checksum-
verified native .dat exports with an explicit training-set declaration can
enter emotional analysis. A .dat fixture is not evidence Lisp ran on VGMIDI.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .academic_fusion import add_idyom_dat
from .idyom_dat import read_idyom_dat


def _hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def import_original_idyom_directory(directory: Path, root: Path,
                                     split: dict[str, str],
                                     musical_rows: dict[str, list[dict]],
                                     beats_by_piece: dict[str, float]) -> dict:
    """Requires filename/MIDI/IDyOM export checksums and source split guard.

    Expected `manifest.json`:
      engine: 'original_idyom_lisp'
      training_midi_sha256: [sha256 ...]
      outputs: [{midi_filename, midi_sha256, dat_file, dat_sha256,
                 melody_name (optional)}]
    The list of original training MIDI SHA values MUST exclude validation and
    test pieces. The producer must independently attest how IDyOM was fit.
    """
    directory = directory.resolve()
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("engine") != "original_idyom_lisp":
        raise ValueError("not_original_idyom_manifest")
    trained = manifest.get("training_midi_sha256")
    if not isinstance(trained, list) or not trained or any(
            not isinstance(x, str) or len(x) != 64 for x in trained):
        raise ValueError("idyom_training_provenance_required")
    # Exact-hash guard is necessary but not sufficient: arrangements,
    # transpositions and published-model reference corpora need separate audit.
    forbidden = {_hash(root / "midi" / name) for name, category in split.items()
                 if category != "train"}
    if forbidden.intersection(trained):
        raise ValueError("idyom_training_overlaps_validation_or_test_midi")
    outputs = manifest.get("outputs")
    if not isinstance(outputs, list):
        raise ValueError("idyom_outputs_must_be_list")
    result = {"status": "verified_export_import_only", "pieces_mapped": 0,
              "pieces_unavailable": [], "engine": "original IDyOM Lisp, not ngram baseline"}
    seen = set()
    for record in outputs:
        midi_name = record["midi_filename"]
        if midi_name not in musical_rows or midi_name in seen:
            raise ValueError("idyom_duplicate_or_unknown_midi")
        seen.add(midi_name)
        if _hash(root / "midi" / midi_name) != record["midi_sha256"]:
            raise ValueError("idyom_midi_hash_mismatch")
        file = (directory / record["dat_file"]).resolve()
        if not file.is_relative_to(directory) or file.suffix.lower() != ".dat":
            raise ValueError("idyom_untrusted_dat_path")
        if _hash(file) != record["dat_sha256"]:
            raise ValueError("idyom_dat_hash_mismatch")
        export = read_idyom_dat(file)
        add_idyom_dat(musical_rows[midi_name], export, beats_by_piece[midi_name],
                      melody_name=record.get("melody_name"))
        result["pieces_mapped"] += 1
    result["pieces_unavailable"] = sorted(set(musical_rows) - seen)
    result["limitations"] = ["source and training exact SHA matched but composition overlap needs separate audit",
                              "the imported original tool is not executed by this code"]
    return result
