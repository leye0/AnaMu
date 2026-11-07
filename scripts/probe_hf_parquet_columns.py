#!/usr/bin/env python3
"""Probe one GigaMIDI Parquet row group's md5 *column only* via HF ranges.

This is an alternative to the viewer's failing /filter and /search endpoints.
It uses Arrow column projection and a strict cap on logical remote reads.
No MIDI bytes are requested and no MD5, file URL or row value is printed.
"""

from __future__ import annotations

import io
import json
import os
import urllib.error


MAX_READ_BYTES = 24_000_000
PATH = "hf://datasets/Metacreation/GigaMIDI/v2.0.0/validation/00001.parquet"


class BudgetFile:
    """File-like wrapper that aborts on excessive reads from its remote file."""

    def __init__(self, stream, limit: int = MAX_READ_BYTES):
        self.stream = stream
        self.limit = limit
        self.read_bytes = 0

    def read(self, n: int = -1) -> bytes:
        if n < 0 or n + self.read_bytes > self.limit:
            raise ValueError("parquet_read_budget_exceeded")
        data = self.stream.read(n)
        self.read_bytes += len(data)
        return data

    def seek(self, offset: int, whence: int = io.SEEK_SET) -> int:
        return self.stream.seek(offset, whence)

    def tell(self) -> int:
        return self.stream.tell()

    def seekable(self) -> bool:
        return True

    def readable(self) -> bool:
        return True


def inspect(token: str) -> dict:
    import pyarrow.parquet as pq
    from huggingface_hub import HfFileSystem

    fs = HfFileSystem(token=token)
    with fs.open(PATH, "rb", block_size=0, cache_type="none") as stream:
        bounded = BudgetFile(stream)
        parquet = pq.ParquetFile(bounded, pre_buffer=False)
        names = parquet.schema_arrow.names
        if "md5" not in names:
            return {"error": "missing_md5_column", "fields_count": len(names)}
        if not parquet.num_row_groups:
            return {"error": "empty_parquet_shard"}
        md5_position = names.index("md5")
        group = parquet.metadata.row_group(0)
        column_info = group.column(md5_position)
        table = parquet.read_row_group(0, columns=["md5"], use_threads=False)
        hashes = table.column("md5").to_pylist()
        return {
            "rows_in_shard": parquet.metadata.num_rows,
            "row_groups_in_shard": parquet.num_row_groups,
            "first_group_rows": group.num_rows,
            "md5_column_compressed_bytes": column_info.total_compressed_size,
            "md5_values_read": len(hashes),
            "valid_hashes": sum(isinstance(h, str) and len(h) == 32 for h in hashes),
            "logical_bytes_requested": bounded.read_bytes,
            "under_budget": bounded.read_bytes <= MAX_READ_BYTES,
        }


def main() -> None:
    token = os.environ.get("HF_TOKEN", "").strip()
    result: dict = {
        "operation": "Parquet column projection, validation shard 00001, first row group only",
        "max_logical_remote_read_bytes": MAX_READ_BYTES,
        "credential_configured": bool(token),
    }
    if token:
        try:
            result["inspection"] = inspect(token)
        except Exception as exc:
            # Never print arbitrary exception messages: some contain signed URLs.
            result["error"] = type(exc).__name__
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
