from __future__ import annotations

import hashlib
import os
import asyncio
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import requests

from app.config import DOLA_REFERER, DOLA_TIMEOUT_SECONDS


def download_stream(
    url: str,
    output: str | Path,
    *,
    headers: dict[str, str] | None = None,
    timeout: float = DOLA_TIMEOUT_SECONDS,
    chunk_size: int = 1024 * 1024,
) -> Path:
    """Download an already-authorized source without re-encoding it."""
    parts = urlsplit(url)
    if parts.scheme not in {"http", "https"} or not parts.netloc:
        raise ValueError("media URL must be an absolute HTTP(S) URL")

    destination = Path(output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    partial = destination.with_name(destination.name + ".part")
    request_headers = {"Accept": "video/*,application/octet-stream", "Referer": DOLA_REFERER}
    if headers:
        request_headers.update(headers)

    try:
        with requests.get(url, headers=request_headers, timeout=timeout, stream=True) as response:
            if response.status_code == 403:
                raise PermissionError("HTTP 403: authenticated access required; no bypass attempted")
            response.raise_for_status()
            expected = response.headers.get("Content-Length")
            expected_bytes = int(expected) if expected and expected.isdigit() else None
            written = 0
            with partial.open("wb") as handle:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if not chunk:
                        continue
                    handle.write(chunk)
                    written += len(chunk)
                handle.flush()
                os.fsync(handle.fileno())
            if expected_bytes is not None and written != expected_bytes:
                raise IOError(f"Content-Length mismatch: expected {expected_bytes}, got {written}")
        os.replace(partial, destination)
        return destination
    except Exception:
        # A partial file is never presented as a completed source.
        if partial.exists():
            partial.unlink()
        raise


def sha256_file(path: str | Path, *, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


async def download_stream_with_playwright_fallback(
    url: str,
    context: object,
    output: str | Path,
    *,
    timeout: float = DOLA_TIMEOUT_SECONDS,
) -> tuple[Path, str]:
    """Use normal HTTP first, then the current Playwright context on 403 only."""
    try:
        return await asyncio.to_thread(download_stream, url, output, timeout=timeout), "HTTP"
    except PermissionError as normal_error:
        request_context = getattr(context, "request", None)
        if request_context is None:
            raise normal_error
        response = await request_context.get(
            url,
            headers={"Accept": "video/*,application/octet-stream", "Referer": DOLA_REFERER},
            timeout=int(timeout * 1000),
        )
        if response.status == 403:
            raise PermissionError("HTTP 403: Playwright authenticated context also denied access; no bypass attempted")
        if not 200 <= response.status < 300:
            raise IOError(f"Playwright context download failed with HTTP {response.status}")
        body = await response.body()
        expected = None
        try:
            headers = await response.all_headers()
            expected_text = headers.get("content-length")
            expected = int(expected_text) if expected_text and expected_text.isdigit() else None
        except (AttributeError, ValueError):
            expected = None
        if expected is not None and len(body) != expected:
            raise IOError(f"Content-Length mismatch: expected {expected}, got {len(body)}")
        destination = Path(output)
        destination.parent.mkdir(parents=True, exist_ok=True)
        partial = destination.with_name(destination.name + ".part")
        try:
            partial.write_bytes(body)
            os.replace(partial, destination)
        except Exception:
            if partial.exists():
                partial.unlink()
            raise
        return destination, "PLAYWRIGHT_CONTEXT"
