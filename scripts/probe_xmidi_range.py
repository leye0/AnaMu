#!/usr/bin/env python3
"""Determine whether XMIDI's public Google Drive ZIP supports byte ranges.

The probe sends two suffix-range requests with a hard 64 KiB read limit each.
It prints only HTTP metadata and ZIP footer detection, never file content.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request


FILE_ID = "1qDkSH31x7jN8X-2RyzB9wuxGji4QxYyA"
READ_LIMIT = 65_536
URLS = {
    "drive_uc": f"https://drive.google.com/uc?export=download&id={FILE_ID}",
    "driveusercontent": f"https://drive.usercontent.google.com/download?id={FILE_ID}&export=download&confirm=t",
}


def summarize(status: int, headers: object, body: bytes, final_url: str, label: str) -> dict:
    get = headers.get  # type: ignore[attr-defined]
    content_range = get("Content-Range")
    content_length = get("Content-Length")
    content_type = (get("Content-Type") or "").split(";", 1)[0]
    return {
        "source": label,
        "status": status,
        "final_host": urllib.parse.urlsplit(final_url).hostname,
        "content_type": content_type,
        "content_length_header": content_length,
        "content_range_header": content_range,
        "bytes_examined": len(body),
        "suffix_range_honored": status == 206 and bool(content_range),
        "zip_end_marker_present": b"PK\x05\x06" in body,
    }


def probe(label: str, url: str) -> dict:
    request = urllib.request.Request(url, headers={
        "Range": f"bytes=-{READ_LIMIT}", "User-Agent": "AnaMu-RangeProbe/0.1",
    })
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = response.read(READ_LIMIT)
            return summarize(response.status, response.headers, body, response.url, label)
    except urllib.error.HTTPError as exc:
        return {"source": label, "status": exc.code, "error": "http_error"}
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        return {"source": label, "error": type(exc).__name__}


def main() -> None:
    print(json.dumps({
        "purpose": "XMIDI ZIP access and 64 KiB suffix-range support only",
        "maximum_examined_bytes": READ_LIMIT * len(URLS),
        "results": [probe(label, url) for label, url in URLS.items()],
    }, indent=2))


if __name__ == "__main__":
    main()
