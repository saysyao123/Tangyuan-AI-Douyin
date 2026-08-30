from __future__ import annotations

from collections.abc import Iterable

from app.resolver.qaab import QAABDecodeError, decode_qaab, loose_b64decode


def _url_from_bytes(value: bytes) -> str | None:
    try:
        decoded = value.decode("utf-8").strip()
    except UnicodeDecodeError:
        return None
    if decoded.startswith(("http://", "https://")):
        return decoded
    return None


def decode_media_urls(value: str, *, key_seed: str | None = None) -> list[str]:
    """Return validated URL candidates without accepting arbitrary decoded text."""
    if not isinstance(value, str) or not value.strip():
        return []
    token = value.strip()
    if token.startswith(("http://", "https://")):
        return [token]
    if token.startswith("qAAB"):
        if not key_seed:
            return []
        try:
            return [decode_qaab(token, key_seed)]
        except QAABDecodeError:
            return []

    results: list[str] = []
    variants: Iterable[str] = (
        token,
        token.replace("$", "+").replace("@", "/").replace("#", "="),
    )
    for variant in variants:
        try:
            decoded = _url_from_bytes(loose_b64decode(variant))
        except QAABDecodeError:
            decoded = None
        if decoded and decoded not in results:
            results.append(decoded)
    return results
