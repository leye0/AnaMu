"""Read jSymbolic's original ACE XML 1.1 output, without recomputing features.

The original jSymbolic writes one data_set per input file and separates
whole-piece features from features computed over overlapping time sections.
Do not infer missing values, or fabricate temporal coordinates for files
where the exporter omitted section stamps.
"""

from __future__ import annotations

import hashlib
import math
import xml.etree.ElementTree as ET
from pathlib import Path


# Published ACE XML 1.1 feature-values files from the upstream DDMAL/jSymbolic2
# repository include this exact *internal schema declaration*. We remove it
# after an exact normalized-content whitelist check, so the XML parser never
# processes a DTD or an entity definition. Arbitrary DOCTYPE remains forbidden.
_OFFICIAL_ACE_VALUES_DTD = b"""<!DOCTYPE feature_vector_file [
   <!ELEMENT feature_vector_file (comments, data_set+)>
   <!ELEMENT comments (#PCDATA)>
   <!ELEMENT data_set (data_set_id, section*, feature*)>
   <!ELEMENT data_set_id (#PCDATA)>
   <!ELEMENT section (feature+)>
   <!ATTLIST section start CDATA ""
                     stop CDATA "">
   <!ELEMENT feature (name, v+)>
   <!ELEMENT name (#PCDATA)>
   <!ELEMENT v (#PCDATA)>
]>"""


def _without_known_ace_dtd(raw: bytes) -> bytes:
    upper = raw.upper()
    if b"<!ENTITY" in upper:
        raise ValueError("ace_external_or_inline_entity_not_allowed")
    start = upper.find(b"<!DOCTYPE")
    if start < 0:
        return raw
    if upper.count(b"<!DOCTYPE") != 1:
        raise ValueError("ace_multiple_doctypes_not_allowed")
    end = raw.find(b"]>", start)
    if end < 0 or end - start > 4096:
        raise ValueError("ace_unknown_or_oversized_doctype")
    declaration = raw[start:end + 2]
    if b" ".join(declaration.split()) != b" ".join(_OFFICIAL_ACE_VALUES_DTD.split()):
        raise ValueError("ace_unrecognized_doctype_not_allowed")
    return raw[:start] + raw[end + 2:]


def _feature_values(parent: ET.Element) -> dict[str, list[float]]:
    result: dict[str, list[float]] = {}
    for element in parent.findall("feature"):
        label = element.findtext("name")
        if not label or not label.strip():
            raise ValueError("ace_feature_name_missing")
        if label in result:
            raise ValueError(f"ace_duplicate_feature_name: {label}")
        values: list[float] = []
        for node in element.findall("v"):
            try:
                parsed = float(node.text or "")
            except ValueError as exc:
                raise ValueError(f"ace_invalid_feature_value: {label}") from exc
            if not math.isfinite(parsed):
                raise ValueError(f"ace_nonfinite_feature_value: {label}")
            values.append(parsed)
        if not values:
            raise ValueError(f"ace_feature_empty: {label}")
        result[label] = values
    return result


def read_jsymbolic_ace(path: str | Path, *, max_bytes: int = 25_000_000) -> dict:
    """Parse published ACE 1.1 feature vectors for a bounded, local XML file.

    The jSymbolic CLI creates *seconds*-based windows when given ``-window``.
    Section timestamps are preserved from XML, not reconstructed from a
    requested window size. Missing stamps are null, not inferred indices.
    """
    source = Path(path)
    if source.stat().st_size > max_bytes:
        raise ValueError("ace_file_over_size_limit")
    raw = source.read_bytes()
    try:
        root = ET.fromstring(_without_known_ace_dtd(raw))
    except ET.ParseError as exc:
        raise ValueError("invalid_ace_xml") from exc
    if root.tag != "feature_vector_file":
        raise ValueError("unsupported_ace_root")
    datasets = []
    for dataset in root.findall("data_set"):
        identifier = dataset.findtext("data_set_id")
        if not identifier:
            raise ValueError("ace_data_set_id_missing")
        windows = []
        for section in dataset.findall("section"):
            a, b = section.get("start"), section.get("stop")
            if (a is None) != (b is None):
                raise ValueError("ace_incomplete_section_timing")
            if a in (None, "") and b in (None, ""):
                start = stop = None
            else:
                try:
                    start, stop = float(a), float(b)
                except (ValueError, TypeError) as exc:
                    raise ValueError("ace_invalid_section_timing") from exc
                if not (math.isfinite(start) and math.isfinite(stop) and 0 <= start < stop):
                    raise ValueError("ace_invalid_section_interval")
            windows.append({"start_seconds_if_j_symbolic_windowed": start,
                            "stop_seconds_if_j_symbolic_windowed": stop,
                            "features": _feature_values(section)})
        datasets.append({"source_id": identifier, "whole_piece_features":
                         _feature_values(dataset), "windows": windows})
    if not datasets:
        raise ValueError("ace_no_data_sets")
    return {"engine": "jSymbolic original (imported ACE XML 1.1)",
            "input_sha256": hashlib.sha256(raw).hexdigest(),
            "source_file": str(source), "data_set_count": len(datasets),
            "window_count": sum(len(x["windows"]) for x in datasets),
            "time_axis": "performance_seconds_if_exported_by_jsymbolic_window_cli",
            "limitations": ["jSymbolic_feature_values_are_not_emotion_labels",
                            "timestamps_are_only_valid_when_produced_with_-window",
                            "preserve_missing_features_and_multidimensional_vectors"],
            "data_sets": datasets}
