#!/usr/bin/env python3
"""Inspect at most the first 8 KiB of GigaMIDI's gated raw metadata CSV.

Never transfer the entire 1+ GB CSV and never log row values or signed URLs.
The bearer token is only sent to Hugging Face; the signed redirect is fetched
without forwarding any credential.
"""

from __future__ import annotations

import csv
import io
import json
import os
import urllib.error
import urllib.parse
import urllib.request


CSV_URL = "https://huggingface.co/datasets/Metacreation/GigaMIDI/resolve/main/Final-Metadata-Extended-GigaMIDI-Dataset-updated.csv"
MAX_READ = 8192


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


def parse_header(chunk: bytes) -> list[str]:
    line = chunk.split(b"\n", 1)[0]
    return next(csv.reader(io.StringIO(line.decode("utf-8-sig"))))


def discover_url(token: str) -> tuple[str, int]:
    request = urllib.request.Request(CSV_URL, method="HEAD", headers={
        "Authorization": "Bearer " + token, "User-Agent": "AnaMu-CSVHeaderProbe/0.1",
    })
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=20) as response:
            return response.url, response.status
    except urllib.error.HTTPError as exc:
        if exc.code not in (302, 303, 307, 308):
            raise
        url = exc.headers.get("Location", "")
        parsed = urllib.parse.urlsplit(url)
        host = parsed.hostname or ""
        if parsed.scheme != "https" or not (
            host.endswith(".hf.co") or host.endswith(".huggingface.co")
            or host.endswith(".amazonaws.com") or host == "huggingface.co"
        ):
            raise ValueError("untrusted_redirect")
        return url, exc.code


def probe(token: str) -> dict:
    target, redirect_status = discover_url(token)
    request = urllib.request.Request(target, headers={
        "Range": f"bytes=0-{MAX_READ-1}", "User-Agent": "AnaMu-CSVHeaderProbe/0.1",
    })
    with urllib.request.urlopen(request, timeout=20) as response:
        if response.status != 206:
            return {"error": "range_not_honored", "status": response.status,
                    "auth_handshake_status": redirect_status}
        chunk = response.read(MAX_READ + 1)
        if len(chunk) > MAX_READ:
            raise ValueError("csv_header_budget_exceeded")
        names = parse_header(chunk)
        return {
            "auth_handshake_status": redirect_status,
            "range_status": response.status,
            "content_range": response.headers.get("Content-Range"),
            "bytes_examined": len(chunk),
            "column_count": len(names),
            "column_names": names,
        }


def main() -> None:
    token = os.environ.get("HF_TOKEN", "").strip()
    report: dict = {"operation": "GigaMIDI raw CSV header only", "max_bytes": MAX_READ,
                    "credential_configured": bool(token)}
    if token:
        try:
            report["result"] = probe(token)
        except Exception as exc:
            report["error"] = type(exc).__name__  # No signed URL or token in logs.
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
