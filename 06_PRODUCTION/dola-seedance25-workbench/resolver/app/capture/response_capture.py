from __future__ import annotations

import asyncio
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from app.capture.local_bridge import CaptureStore
from app.discovery.router_data import walk_json


FIELD_SCORES = {
    "fallback_api": 10,
    "video_list": 10,
    "original_media_info": 10,
    "main_url": 8,
    "man_url": 8,
    "play_url": 8,
    "download_url": 8,
    "key_seed": 7,
    "video_info": 5,
    "vid": 3,
    "video_id": 3,
    "video_model": 1,
    "media": 4,
}
RELEVANT_FIELDS = tuple(FIELD_SCORES)
DISCOVERY_HOSTS = ("dola.com", "byteintlapi.com")


def _allowed_host(host: str, suffix: str) -> bool:
    value = host.lower().rstrip(".")
    return value == suffix or value.endswith("." + suffix)


def is_dola_response_url(url: str) -> bool:
    try:
        parts = urlsplit(url)
    except ValueError:
        return False
    return parts.scheme == "https" and _allowed_host(parts.hostname or "", "dola.com")


def is_chain_single_url(url: str) -> bool:
    try:
        parts = urlsplit(url)
    except ValueError:
        return False
    return is_dola_response_url(url) and "/im/chain/single" in parts.path


def is_discovery_host(url: str) -> bool:
    try:
        parts = urlsplit(url)
    except ValueError:
        return False
    host = parts.hostname or ""
    return parts.scheme == "https" and any(_allowed_host(host, suffix) for suffix in DISCOVERY_HOSTS)


def _decode_body(body: bytes, content_type: str) -> tuple[str | None, str]:
    charset = "utf-8"
    lowered = content_type.lower()
    marker = "charset="
    if marker in lowered:
        charset = lowered.split(marker, 1)[1].split(";", 1)[0].strip() or charset
    try:
        return body.decode(charset), charset
    except (LookupError, UnicodeDecodeError):
        try:
            return body.decode("utf-8"), "utf-8"
        except UnicodeDecodeError:
            return None, "raw-bytes"


def _relevant_fields(text: str) -> list[str]:
    lowered = text.lower()
    return [field for field in RELEVANT_FIELDS if re.search(rf"[\"']{re.escape(field)}[\"']\s*:", lowered)]


def score_response_metadata(text: str) -> tuple[int, list[str]]:
    """Score JSON/text responses without treating video_model alone as media metadata."""
    fields = set(_relevant_fields(text))
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        parsed = None
    if parsed is not None:
        for _, node in walk_json(parsed):
            if isinstance(node, dict):
                for key in node:
                    normalized = str(key).lower()
                    if normalized in FIELD_SCORES:
                        fields.add(normalized)
    ordered = [field for field in RELEVANT_FIELDS if field in fields]
    return sum(FIELD_SCORES[field] for field in ordered), ordered


async def _headers(response: Any) -> dict[str, str]:
    try:
        return {str(key).lower(): str(value) for key, value in (await response.all_headers()).items()}
    except AttributeError:
        return {str(key).lower(): str(value) for key, value in (response.headers or {}).items()}


class NetworkDiscovery:
    def __init__(self, output_path: Path, *, capture_dir: Path | None = None, minimum_score: int = 8) -> None:
        self.output_path = output_path
        self.capture_dir = capture_dir or output_path.parent / "cdp"
        self.minimum_score = minimum_score
        self.entries: list[dict[str, Any]] = []
        self._seen: set[tuple[str, int, tuple[str, ...]]] = set()

    async def observe(self, response: Any, body: bytes | None = None, headers: dict[str, str] | None = None) -> None:
        url = str(response.url)
        if not is_discovery_host(url):
            return
        headers = headers or await _headers(response)
        content_type = headers.get("content-type", "").lower()
        if "json" not in content_type and body is None:
            return
        try:
            if body is None:
                # Response.body() waits for the response body. Calling
                # response.finished() first leaves Playwright's internal
                # waiter alive when a timed-out context is closed.
                body = await response.body()
        except Exception:
            return
        text, _ = _decode_body(body, content_type)
        if text is None:
            return
        score, hits_list = score_response_metadata(text)
        hits = tuple(hits_list)
        if score < self.minimum_score:
            return
        parts = urlsplit(url)
        key = (url, int(response.status), hits)
        if key in self._seen:
            return
        self._seen.add(key)
        digest = hashlib.sha256(body).hexdigest()[:12]
        slug = re.sub(r"[^A-Za-z0-9._-]+", "_", parts.path.strip("/") or "root").strip("_") or "root"
        capture_path = self.capture_dir / f"dola_{parts.hostname}_{slug}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')}_{digest}.json"
        capture_path.parent.mkdir(parents=True, exist_ok=True)
        partial = capture_path.with_name(capture_path.name + ".part")
        try:
            partial.write_text(text, encoding="utf-8")
            partial.replace(capture_path)
        finally:
            if partial.exists():
                partial.unlink()
        self.entries.append(
            {
                "captured_at": datetime.now(timezone.utc).isoformat(),
                "method": str(response.request.method),
                "host": parts.hostname,
                "path": parts.path,
                "status": int(response.status),
                "content_type": content_type,
                "score": score,
                "matched_fields": list(hits),
                "capture_path": str(capture_path),
            }
        )

    def save(self) -> Path:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"entries": self.entries}
        self.output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return self.output_path


class ResponseCapture:
    def __init__(self, store: CaptureStore, *, discover_network: bool = False) -> None:
        self.store = store
        self.discover_network = discover_network
        self.discovery: NetworkDiscovery | None = None
        self.capture_results: list[dict[str, Any]] = []
        self.raw_bytes_debug: list[Path] = []
        self._tasks: set[asyncio.Task[Any]] = set()
        self._captured = asyncio.Event()

    def attach(self, context: Any, *, discovery_path: Path | None = None) -> None:
        if self.discover_network:
            if discovery_path is None:
                discovery_path = self.store.out_dir / "network-discovery.json"
            self.discovery = NetworkDiscovery(discovery_path)
        context.on("response", self._on_response)

    def detach(self, context: Any) -> None:
        context.remove_listener("response", self._on_response)

    def _on_response(self, response: Any) -> None:
        task = asyncio.create_task(self._handle_response(response))
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)

    async def _handle_response(self, response: Any) -> None:
        url = str(response.url)
        target = is_chain_single_url(url)
        discovery_target = self.discover_network and is_discovery_host(url)
        if not target and not discovery_target:
            return
        try:
            # Playwright's response.body() waits until the body is complete.
            # It is safer than leaving response.finished()'s internal waiter
            # alive when a timed-out persistent context is closed.
            body = await response.body()
        except Exception:
            return
        headers = await _headers(response)
        if self.discovery is not None:
            await self.discovery.observe(response, body=body, headers=headers)
        text, encoding = _decode_body(body, headers.get("content-type", ""))
        if text is None:
            if target:
                debug_path = self.store.out_dir / "debug" / f"response_{len(self.raw_bytes_debug) + 1}.bin"
                debug_path.parent.mkdir(parents=True, exist_ok=True)
                debug_path.write_bytes(body)
                self.raw_bytes_debug.append(debug_path)
            return
        if not target:
            if score_response_metadata(text)[0] < 8:
                return
            page_url = ""
            try:
                page_url = str(response.frame.url)
            except Exception:
                pass
            envelope = {
                "captured_at": datetime.now(timezone.utc).isoformat(),
                "page_url": page_url,
                "request_url": url,
                "response_status": int(response.status),
                "raw_body": text,
            }
            try:
                result = await asyncio.to_thread(self.store.save_discovered_response, envelope, include_internal=True)
            except Exception:
                return
            self.capture_results.append(result)
            self._captured.set()
            return
        if score_response_metadata(text)[0] < 8:
            return
        try:
            json.loads(text)
        except json.JSONDecodeError:
            return
        page_url = ""
        try:
            page_url = str(response.frame.url)
        except Exception:
            pass
        envelope = {
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "page_url": page_url,
            "request_url": url,
            "response_status": int(response.status),
            "raw_body": text,
        }
        try:
            result = await asyncio.to_thread(self.store.save, envelope, include_internal=True)
        except Exception:
            return
        self.capture_results.append(result)
        self._captured.set()

    async def wait_for_capture(self, timeout_seconds: float) -> bool:
        captured = False
        try:
            await asyncio.wait_for(self._captured.wait(), timeout=timeout_seconds)
            await asyncio.sleep(0.5)
            captured = True
            return captured
        except asyncio.TimeoutError:
            return False
        finally:
            if self._tasks:
                tasks = list(self._tasks)
                if captured:
                    await asyncio.wait(tasks, timeout=1)
                for task in tasks:
                    if not task.done():
                        task.cancel()
                await asyncio.gather(*tasks, return_exceptions=True)
                self._tasks.clear()
            if self.discovery is not None:
                self.discovery.save()
