#!/usr/bin/env python3
"""Read at most one GigaMIDI *metadata* row through the HF dataset viewer.

Do not print music bytes, lyrics or any dataset row values. Request and response
sizes are bounded. Intended for a quick authentication + schema experiment.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request


MAX_RESPONSE_BYTES = 400_000
VIEWER_ENDPOINT = "https://datasets-server.huggingface.co/rows"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Never send the Hugging Face bearer token to a redirect destination."""

    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


def summarize(payload: dict, transferred_bytes: int) -> dict:
    rows = payload.get("rows") or []
    features = payload.get("features") or []
    return {
        "http_status": 200,
        "response_bytes": transferred_bytes,
        "row_count": len(rows),
        "num_rows_total": payload.get("num_rows_total"),
        "feature_names": [f.get("name") for f in features],
        "first_row_keys": list((rows[0].get("row") or {}).keys()) if rows else [],
        "viewer_partial": payload.get("partial"),
    }


def probe(token: str) -> dict:
    query = urllib.parse.urlencode({
        "dataset": "Metacreation/GigaMIDI",
        "config": "v2.0.0",
        "split": "validation",
        "offset": "0",
        "length": "1",
    })
    request = urllib.request.Request(
        VIEWER_ENDPOINT + "?" + query,
        headers={"Authorization": "Bearer " + token, "User-Agent": "AnaMu-SchemaProbe/0.1"},
    )
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=20) as response:
            body = response.read(MAX_RESPONSE_BYTES + 1)
            if len(body) > MAX_RESPONSE_BYTES:
                return {"error": "response_exceeds_400kB_limit", "maximum_bytes": MAX_RESPONSE_BYTES}
            payload = json.loads(body)
            return summarize(payload, len(body))
    except urllib.error.HTTPError as exc:
        # HTTP status is enough to diagnose; response may contain row values.
        return {"http_status": exc.code, "error": "viewer_http_error"}
    except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        return {"error": type(exc).__name__}


def main() -> None:
    token = os.environ.get("HF_TOKEN", "").strip()
    report = {
        "dataset": "Metacreation/GigaMIDI",
        "operation": "viewer API: exactly 1 row, <=400kB, no row values logged",
        "credential_configured": bool(token),
        "result": probe(token) if token else {"error": "missing_HF_TOKEN_secret"},
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
