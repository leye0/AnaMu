#!/usr/bin/env python3
"""Test whether Hugging Face exposes a *fast* indexed GigaMIDI MD5 lookup.

Uses one known MD5 obtained from one GigaMIDI row; never outputs that MD5,
music contents, song titles, or the bearer token.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request


HOST = "https://datasets-server.huggingface.co"
DATASET = "Metacreation/GigaMIDI"
MAX_BODY = 400_000
TIMEOUT = 12


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


def get(token: str, endpoint: str, params: dict) -> dict:
    request = urllib.request.Request(
        HOST + endpoint + "?" + urllib.parse.urlencode(params),
        headers={"Authorization": "Bearer " + token, "User-Agent": "AnaMu-LookupProbe/0.1"},
    )
    with urllib.request.build_opener(NoRedirect()).open(request, timeout=TIMEOUT) as response:
        body = response.read(MAX_BODY + 1)
        if len(body) > MAX_BODY:
            raise ValueError("response_budget_exceeded")
        return json.loads(body)


def classify_error(exc: BaseException) -> str:
    return f"http_{exc.code}" if isinstance(exc, urllib.error.HTTPError) else type(exc).__name__


def main() -> None:
    token = os.environ.get("HF_TOKEN", "").strip()
    result: dict = {"dataset": DATASET, "credential_configured": bool(token),
                    "operation": "is-valid + one known MD5 search, max 400kB per response"}
    if token:
        try:
            flags = get(token, "/is-valid", {"dataset": DATASET})
            result["capabilities"] = {k: flags.get(k) for k in
                                      ("valid", "viewer", "filter", "search", "preview")}
        except (urllib.error.HTTPError, urllib.error.URLError, ValueError, TimeoutError) as exc:
            result["capabilities_error"] = classify_error(exc)
        try:
            first = get(token, "/rows", {
                "dataset": DATASET, "config": "v2.0.0", "split": "validation", "offset": 0, "length": 1,
            })
            md5 = first["rows"][0]["row"]["md5"]
            search = get(token, "/search", {
                "dataset": DATASET, "config": "v2.0.0", "split": "validation",
                "query": md5, "offset": 0, "length": 1,
            })
            rows = search.get("rows") or []
            result["search"] = {
                "responded": True, "rows_returned": len(rows),
                "known_md5_found": any((r.get("row") or {}).get("md5") == md5 for r in rows),
            }
        except (urllib.error.HTTPError, urllib.error.URLError, ValueError, TimeoutError,
                KeyError, IndexError) as exc:
            result["search_error"] = classify_error(exc)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
