from __future__ import annotations

from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import requests

from app.config import DOLA_REFERER, DOLA_TIMEOUT_SECONDS
from app.resolver.candidates import discover_candidates


def build_unwatermarked_url(fallback_api: str) -> str:
    """Build only the documented media-rendition request variant."""
    parts = urlsplit(fallback_api)
    if parts.scheme not in {"http", "https"} or not parts.netloc:
        raise ValueError("fallback_api must be an absolute HTTP(S) URL")
    params = dict(parse_qsl(parts.query, keep_blank_values=True))
    params["channel"] = "no"
    params["codec_type"] = "8"
    params["logo_type"] = "unwatermarked"
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(params), parts.fragment))


def fetch_fallback_metadata(fallback_api: str, *, timeout: float = DOLA_TIMEOUT_SECONDS) -> dict[str, Any]:
    url = build_unwatermarked_url(fallback_api)
    response = requests.get(url, headers={"Accept": "application/json", "Referer": DOLA_REFERER}, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise ValueError("fallback_api returned a non-object JSON payload")
    return payload


def parse_fallback_candidates(payload: Any) -> list:
    return discover_candidates(payload, source="fallback_api")
