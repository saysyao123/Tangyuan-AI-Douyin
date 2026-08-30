from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from app.config import (
    CANDIDATE_URL_KEYS,
    FALLBACK_API_KEYS,
    KEY_SEED_KEYS,
    VIDEO_ID_KEYS,
    VIDEO_LIST_KEYS,
    VIDEO_MODEL_KEYS,
)
from app.discovery.router_data import walk_json


VID_PATTERN = re.compile(r"^v[0-9][A-Za-z0-9]{20,}$")


@dataclass(slots=True)
class FieldHit:
    key: str
    path: tuple[str | int, ...]
    value: Any
    parent: dict[str, Any]


@dataclass(slots=True)
class MetadataScan:
    fields: dict[str, list[FieldHit]] = field(default_factory=dict)

    def hits(self, *keys: str) -> list[FieldHit]:
        wanted = {key.lower() for key in keys}
        return [hit for key, values in self.fields.items() if key.lower() in wanted for hit in values]

    def values(self, *keys: str) -> list[Any]:
        return [hit.value for hit in self.hits(*keys)]

    @property
    def vids(self) -> list[str]:
        result: list[str] = []
        for value in self.values(*VIDEO_ID_KEYS):
            if isinstance(value, str) and VID_PATTERN.match(value.strip()):
                if value.strip() not in result:
                    result.append(value.strip())
        return result

    @property
    def fallback_apis(self) -> list[str]:
        return _unique_strings(self.values(*FALLBACK_API_KEYS))

    @property
    def key_seeds(self) -> list[str]:
        return _unique_strings(self.values(*KEY_SEED_KEYS))

    @property
    def video_models(self) -> list[Any]:
        return self.values(*VIDEO_MODEL_KEYS)

    @property
    def video_lists(self) -> list[Any]:
        return self.values(*VIDEO_LIST_KEYS)


def _unique_strings(values: list[Any]) -> list[str]:
    result: list[str] = []
    for value in values:
        if isinstance(value, str) and value and value not in result:
            result.append(value)
    return result


def scan_metadata(metadata: Any) -> MetadataScan:
    scan = MetadataScan()
    for path, node in walk_json(metadata):
        if not isinstance(node, dict):
            continue
        for key, value in node.items():
            normalized = str(key).lower()
            interesting = {
                *(item.lower() for item in CANDIDATE_URL_KEYS),
                *(item.lower() for item in FALLBACK_API_KEYS),
                *(item.lower() for item in KEY_SEED_KEYS),
                *(item.lower() for item in VIDEO_ID_KEYS),
                *(item.lower() for item in VIDEO_LIST_KEYS),
                *(item.lower() for item in VIDEO_MODEL_KEYS),
            }
            if normalized in interesting:
                scan.fields.setdefault(normalized, []).append(FieldHit(str(key), path + (str(key),), value, node))
    return scan
