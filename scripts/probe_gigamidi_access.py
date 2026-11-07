#!/usr/bin/env python3
"""AnaMu: verify Hugging Face GigaMIDI file access using HEAD only.

No MIDI, Parquet, CSV or ZIP body is downloaded. The token is never printed.
The HEAD redirect is intentionally NOT followed to avoid forwarding secrets.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request


GIGAMIDI_FILE = "https://huggingface.co/datasets/Metacreation/GigaMIDI/resolve/main/v2.0.0/validation/00001.parquet"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def classify_status(status: int | None) -> str:
    if status in (200, 206, 301, 302, 303, 307, 308):
        return "accessible_or_redirected_to_file"
    if status in (401, 403):
        return "access_denied"
    if status == 404:
        return "file_not_found"
    return "inconclusive"


def head_access(token: str | None = None) -> dict:
    headers = {"User-Agent": "AnaMu-AccessProbe/0.1", "Accept": "*/*"}
    if token:
        headers["Authorization"] = "Bearer " + token
    request = urllib.request.Request(GIGAMIDI_FILE, headers=headers, method="HEAD")
    opener = urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(request, timeout=12) as response:
            status = response.status
    except urllib.error.HTTPError as exc:
        status = exc.code
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        return {"classification": "network_error", "error": type(exc).__name__}
    return {"status": status, "classification": classify_status(status)}


def main() -> None:
    token = os.environ.get("HF_TOKEN", "").strip()
    report = {
        "dataset": "Metacreation/GigaMIDI",
        "target": "v2.0.0/validation/00001.parquet",
        "operation": "HEAD, redirects disabled, no payload",
        "anonymous": head_access(),
        "credential_configured": bool(token),
        "authenticated": head_access(token) if token else "not_attempted",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
