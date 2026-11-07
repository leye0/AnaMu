#!/usr/bin/env python3
"""AnaMu P0: inspect *metadata only*, never fetch MIDI or audio payloads.

Uses only Python's standard library. The response budget bounds unexpectedly large
API documents; the request list is deliberately fixed and auditable.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MAX_RESPONSE_BYTES = 2_000_000
USER_AGENT = "AnaMu-SourceAudit/0.1 (research metadata probe; contact via GitHub leye0/AnaMu)"


def request_json(url: str) -> tuple[dict[str, Any] | list[Any] | None, dict[str, Any]]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            length = response.headers.get("Content-Length")
            if length and int(length) > MAX_RESPONSE_BYTES:
                return None, {"status": response.status, "error": "metadata document exceeds response budget"}
            payload = response.read(MAX_RESPONSE_BYTES + 1)
            if len(payload) > MAX_RESPONSE_BYTES:
                return None, {"status": response.status, "error": "metadata response exceeds response budget"}
            return json.loads(payload), {"status": response.status, "bytes": len(payload)}
    except urllib.error.HTTPError as exc:
        return None, {"status": exc.code, "error": "HTTP error"}
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ValueError) as exc:
        return None, {"error": type(exc).__name__}


def request_head(url: str) -> dict[str, Any]:
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return {
                "status": response.status,
                "content_type": response.headers.get("Content-Type"),
                "content_length": response.headers.get("Content-Length"),
                # We intentionally do NOT record redirected URLs (may contain tokens).
            }
    except urllib.error.HTTPError as exc:
        return {"status": exc.code, "error": "HTTP error"}
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        return {"error": type(exc).__name__}


def summarize_hf(payload: dict[str, Any]) -> dict[str, Any]:
    siblings = payload.get("siblings") or []
    return {
        "id": payload.get("id"),
        "gated": payload.get("gated", False),
        "private": payload.get("private"),
        "license": (payload.get("cardData") or {}).get("license"),
        "listed_file_count": len(siblings),
        "file_samples": [row.get("rfilename") for row in siblings[:12]],
        "has_parquet": any(str(row.get("rfilename", "")).endswith(".parquet") for row in siblings),
    }


def summarize_zenodo(payload: dict[str, Any]) -> dict[str, Any]:
    files = payload.get("files") or []
    return {
        "id": payload.get("id"),
        "access": payload.get("access"),
        "files": [{"name": row.get("key"), "size": row.get("size")} for row in files[:20]],
        "listed_file_count": len(files),
    }


def collect() -> dict[str, Any]:
    result: dict[str, Any] = {
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "method": "public API metadata and one HTTP HEAD; no corpus file downloaded",
        "probes": {},
    }
    probes = result["probes"]

    endpoints = {
        "xmidi_github_contents": "https://api.github.com/repos/xmusic-project/XMIDI_Dataset/contents",
        "metamidi_zenodo": "https://zenodo.org/api/records/5142664",
        "gigamidi_hf": "https://huggingface.co/api/datasets/Metacreation/GigaMIDI",
        "discover_midi_hf": "https://huggingface.co/api/datasets/projectlosangeles/Discover-MIDI-Dataset",
        "emopia_zenodo": "https://zenodo.org/api/records/5090631",
    }
    for key, url in endpoints.items():
        payload, transport = request_json(url)
        probe: dict[str, Any] = {"url": url, "transport": transport}
        if isinstance(payload, dict):
            if key.endswith("_hf"):
                probe["metadata"] = summarize_hf(payload)
            elif key.endswith("_zenodo"):
                probe["metadata"] = summarize_zenodo(payload)
        elif key == "xmidi_github_contents" and isinstance(payload, list):
            probe["metadata"] = {"repository_files": [row.get("name") for row in payload]}
        probes[key] = probe

    # HEAD only: downloading from the corresponding Google Drive archive is forbidden by this tool.
    probes["xmidi_google_drive_head"] = {
        "url": "https://drive.google.com/file/d/1qDkSH31x7jN8X-2RyzB9wuxGji4QxYyA/view",
        "transport": request_head("https://drive.google.com/uc?export=download&id=1qDkSH31x7jN8X-2RyzB9wuxGji4QxYyA"),
        "caveat": "HEAD cannot establish individual-file or range extraction from a ZIP",
    }
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write compact JSON evidence to this path")
    args = parser.parse_args(argv)
    result = collect()
    body = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    print(body)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(body, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
