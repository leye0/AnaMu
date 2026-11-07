#!/usr/bin/env python3
"""Check GigaMIDI MD5 semantics on three bounded Dataset Viewer rows.

Never emit or store a MIDI, title, artist, hash, URL, or the secret. The viewer
can return embedded MIDI bytes in its JSON representation; this probe hashes
them in memory only, if and only if the representation is unambiguous.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request


DATASET = "Metacreation/GigaMIDI"
ENDPOINT = "https://datasets-server.huggingface.co/rows"
MAX_RESPONSE_BYTES = 400_000
OFFSETS = (0, 1000, 10000)
MD5_PATTERN = re.compile(r"[0-9a-f]{32}", re.IGNORECASE)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


def embedded_midi(value: object) -> tuple[bytes | None, str]:
    """Accept only explicit base64 data whose decoded content is a MIDI file."""
    if isinstance(value, dict):
        raw = value.get("bytes")
        label = "music_object"
    elif isinstance(value, str):
        raw = value
        label = "music_string"
    else:
        return None, type(value).__name__

    if not isinstance(raw, str):
        return None, label + "_without_embedded_base64"

    try:
        decoded = base64.b64decode(raw, validate=True)
    except (ValueError, base64.binascii.Error):
        return None, label + "_not_base64"
    if decoded.startswith(b"MThd"):
        return decoded, label + "_decoded_midi"
    return None, label + "_not_midi"


def summarize_row(payload: dict, response_bytes: int, offset: int) -> dict:
    rows = payload.get("rows") or []
    if len(rows) != 1 or not isinstance(rows[0].get("row"), dict):
        return {"offset": offset, "error": "unexpected_row_count", "response_bytes": response_bytes}

    row = rows[0]["row"]
    midi, encoding = embedded_midi(row.get("music"))
    md5 = row.get("md5")
    md5_valid = isinstance(md5, str) and bool(MD5_PATTERN.fullmatch(md5))
    return {
        "offset": offset,
        "response_bytes": response_bytes,
        "music_encoding": encoding,
        "embedded_midi_bytes": len(midi) if midi is not None else None,
        "md5_format_valid": md5_valid,
        "hash_matches_embedded_midi": (
            hashlib.md5(midi).hexdigest() == md5.lower()
            if midi is not None and md5_valid else None
        ),
    }


def probe_row(token: str, offset: int) -> dict:
    query = urllib.parse.urlencode({
        "dataset": DATASET, "config": "v2.0.0", "split": "validation",
        "offset": offset, "length": 1,
    })
    request = urllib.request.Request(
        ENDPOINT + "?" + query,
        headers={"Authorization": "Bearer " + token, "User-Agent": "AnaMu-MD5-Probe/0.1"},
    )
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=20) as response:
            body = response.read(MAX_RESPONSE_BYTES + 1)
            if len(body) > MAX_RESPONSE_BYTES:
                return {"offset": offset, "error": "response_limit_exceeded", "cap_bytes": MAX_RESPONSE_BYTES}
            return summarize_row(json.loads(body), len(body), offset)
    except urllib.error.HTTPError as exc:
        return {"offset": offset, "error": "http_error", "http_status": exc.code}
    except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        return {"offset": offset, "error": type(exc).__name__}


def main() -> None:
    token = os.environ.get("HF_TOKEN", "").strip()
    result = {
        "dataset": DATASET,
        "operation": "3 bounded one-row requests; report only hash parity and sizes",
        "credential_configured": bool(token),
        "samples": [probe_row(token, i) for i in OFFSETS] if token else [],
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
