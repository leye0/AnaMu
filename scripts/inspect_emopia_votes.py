"""Inspect official EMOPIA 2.2 annotation schemas without exporting source MIDI.

The output is only aggregate ZIP metadata and a tiny schema preview, never
copyrighted MIDI, audio, or complete individual annotation tables. Download
is pinned to the published Zenodo record and a conservative 40-MB limit.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path


RECORD = "5257995"
EXPECTED_ZIP = "EMOPIA_2.2.zip"
MAX_ARCHIVE_BYTES = 40_000_000


def inspect_archive(payload: bytes) -> dict:
    if len(payload) > MAX_ARCHIVE_BYTES:
        raise ValueError("emopia_zip_over_budget")
    archive = zipfile.ZipFile(io.BytesIO(payload))
    members = [item for item in archive.infolist() if not item.is_dir()]
    if len(members) > 30_000 or sum(item.file_size for item in members) > 250_000_000:
        raise ValueError("unsafe_archive_size")
    names = [item.filename for item in members]
    tagging = [item for item in members if "/tagging_lists/" in "/" + item.filename and
               item.filename.lower().endswith((".csv", ".txt", ".json", ".tsv"))]
    midis = [item for item in members if item.filename.lower().endswith((".mid", ".midi"))]
    labels = [item for item in members if item.filename.endswith("label.csv")]
    if not tagging or not midis or not labels:
        raise AssertionError("missing_raw_tags_midis_or_label_csv")
    preview = []
    # Limit to a few *schema* examples; no full annotator data released here.
    for item in tagging[:5] + labels[:1]:
        if item.file_size > 2_000_000:
            continue
        content = archive.read(item).decode("utf-8-sig", errors="replace")
        preview.append({"kind": "label_csv" if item in labels else "raw_tagging",
                        "suffix": Path(item.filename).suffix,
                        "bytes": item.file_size,
                        "first_line": content.splitlines()[0][:180] if content.splitlines() else "",
                        "second_line_shape": [len(line.split(",")) for line in content.splitlines()[1:2]]})
    folders = Counter(item.filename.split("/")[0] for item in members)
    return {"record": RECORD, "zip": EXPECTED_ZIP,
            "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest(),
            "all_files": len(members), "midi_files": len(midis),
            "raw_tag_files": len(tagging), "label_csv_files": len(labels),
            "raw_tag_extensions": dict(Counter(Path(f.filename).suffix for f in tagging)),
            "root_paths": dict(folders), "schema_previews": preview,
            "scope": "metadata and schemas only; no MIDI or audio uploaded"}


def download_official_zip() -> bytes:
    # Pin an immutable Zenodo version; redirect is managed by official source.
    url = f"https://zenodo.org/records/{RECORD}/files/{EXPECTED_ZIP}?download=1"
    with urllib.request.urlopen(url, timeout=100) as response:
        data = response.read(MAX_ARCHIVE_BYTES + 1)
    if len(data) > MAX_ARCHIVE_BYTES:
        raise ValueError("emopia_zip_over_budget")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = inspect_archive(download_official_zip())
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
