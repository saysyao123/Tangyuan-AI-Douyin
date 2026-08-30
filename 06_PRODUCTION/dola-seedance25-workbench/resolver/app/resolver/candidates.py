from __future__ import annotations

import json
import re
from collections.abc import Iterable
from typing import Any

from app.config import (
    CANDIDATE_URL_KEYS,
    ORIGINAL_HINTS,
    UNWATERMARKED_HINTS,
    VIDEO_ID_KEYS,
    WATERMARKED_HINTS,
)
from app.discovery.router_data import walk_json
from app.models import MediaCandidate
from app.resolver.url_decoder import decode_media_urls


def _number(value: Any) -> int | None:
    if isinstance(value, bool) or value is None:
        return None
    try:
        number = int(float(str(value).strip()))
    except (TypeError, ValueError):
        return None
    return number if number >= 0 else None


def _first(parent: dict[str, Any], *keys: str) -> Any:
    lowered = {str(key).lower(): value for key, value in parent.items()}
    for key in keys:
        value = lowered.get(key.lower())
        if value is not None:
            return value
    return None


def _text_without_urls(parent: dict[str, Any]) -> str:
    values = {
        str(key): value
        for key, value in parent.items()
        if str(key).lower() not in set(CANDIDATE_URL_KEYS) | {"fallback_api"}
    }
    return json.dumps(values, ensure_ascii=False, sort_keys=True, default=str).lower()


def is_unwatermarked_candidate(url: str, raw: dict[str, Any] | None = None) -> bool:
    url_text = url.lower()
    metadata_text = _text_without_urls(raw or {})
    combined = f"{url_text}\n{metadata_text}"
    if any(marker in combined for marker in WATERMARKED_HINTS):
        return False
    return any(marker in combined for marker in UNWATERMARKED_HINTS)


def is_original_candidate(raw: dict[str, Any] | None = None) -> bool:
    text = _text_without_urls(raw or {})
    return any(re.search(rf"\b{re.escape(hint)}\b", text) for hint in ORIGINAL_HINTS)


def _codec(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip().lower()
    if text in {"1", "avc", "avc1", "h264", "h.264"}:
        return "h264"
    if text in {"2", "hevc", "h265", "h.265", "hvc1", "bytevc1"}:
        return "h265"
    return text or None


def _vid_from_parent(parent: dict[str, Any]) -> str | None:
    for key in VIDEO_ID_KEYS:
        value = _first(parent, key)
        if isinstance(value, str) and re.match(r"^v[0-9][A-Za-z0-9]{20,}$", value.strip()):
            return value.strip()
    return None


def _make_candidate(
    *,
    source: str,
    url: str,
    parent: dict[str, Any],
    key_seed: str | None,
) -> MediaCandidate:
    return MediaCandidate(
        source=source,
        url=url,
        width=_number(_first(parent, "vwidth", "width", "video_width", "videoWidth")),
        height=_number(_first(parent, "vheight", "height", "video_height", "videoHeight")),
        bitrate=_number(_first(parent, "bitrate", "bit_rate", "bps")),
        real_bitrate=_number(_first(parent, "real_bitrate", "realBitrate")),
        codec=_codec(_first(parent, "codec_type", "codec", "codec_name")),
        definition=str(_first(parent, "definition", "quality") or "") or None,
        gear_name=str(_first(parent, "gear_name", "gearName") or "") or None,
        is_original=is_original_candidate(parent),
        is_unwatermarked=is_unwatermarked_candidate(url, parent),
        raw={**parent, "_key_seed_present": bool(key_seed)},
    )


def discover_candidates(metadata: Any, *, source: str = "direct_metadata") -> list[MediaCandidate]:
    """Find direct media fields anywhere in a Dola response."""
    global_key_seed: str | None = None
    for path, node in walk_json(metadata):
        if isinstance(node, dict):
            value = _first(node, "key_seed", "keySeed")
            if isinstance(value, str) and value.strip():
                global_key_seed = value.strip()
                break

    candidates: list[MediaCandidate] = []
    seen: set[tuple[str, str]] = set()
    url_keys = {key.lower() for key in CANDIDATE_URL_KEYS}
    for path, node in walk_json(metadata):
        if not isinstance(node, dict):
            continue
        local_key_seed = _first(node, "key_seed", "keySeed") or global_key_seed
        path_text = ".".join(str(part) for part in path).lower()
        candidate_source = "fallback_api" if "video_list" in path_text or "videolist" in path_text else source
        for key, raw_value in node.items():
            if str(key).lower() not in url_keys or not isinstance(raw_value, str):
                continue
            for decoded_url in decode_media_urls(raw_value, key_seed=local_key_seed):
                identity = (candidate_source, decoded_url)
                if identity in seen:
                    continue
                seen.add(identity)
                candidates.append(
                    _make_candidate(
                        source=candidate_source,
                        url=decoded_url,
                        parent=node,
                        key_seed=local_key_seed,
                    )
                )
    return candidates


def merge_candidates(*groups: Iterable[MediaCandidate]) -> list[MediaCandidate]:
    result: list[MediaCandidate] = []
    seen: set[str] = set()
    for group in groups:
        for candidate in group:
            if candidate.url in seen:
                continue
            seen.add(candidate.url)
            result.append(candidate)
    return result
