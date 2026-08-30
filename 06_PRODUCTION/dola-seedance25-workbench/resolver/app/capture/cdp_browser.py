from __future__ import annotations

import asyncio
import json
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from playwright.async_api import Browser, BrowserContext, Page, async_playwright

from app.capture.local_bridge import CaptureStore
from app.capture.response_capture import ResponseCapture, is_dola_response_url, score_response_metadata
from app.download.authenticated import download_stream_with_playwright_fallback
from app.qa.ffprobe import probe_media


DEFAULT_CDP_ENDPOINT = "http://127.0.0.1:9222"
DEFAULT_TARGET_CHAT = "https://www.dola.com/chat/00000000000000000"
LOGIN_URL_MARKERS = ("/login", "/signin", "/sign-in", "accounts.google.com")


def validate_cdp_endpoint(endpoint: str) -> str:
    parts = urlsplit(endpoint)
    host = (parts.hostname or "").lower().rstrip(".")
    if parts.scheme not in {"http", "https"} or host not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("CDP endpoint must be an HTTP(S) loopback URL")
    if parts.username or parts.password or parts.query or parts.fragment:
        raise ValueError("CDP endpoint must not contain credentials, query parameters, or fragments")
    return endpoint.rstrip("/")


def validate_target_chat(url: str) -> str:
    if not is_dola_response_url(url):
        raise ValueError("target chat must be an HTTPS dola.com URL")
    parts = urlsplit(url)
    if not parts.path.startswith("/chat/"):
        raise ValueError("target chat must use a /chat/ path")
    return url


def _is_dola_chat_url(url: str) -> bool:
    try:
        parts = urlsplit(url)
    except ValueError:
        return False
    return is_dola_response_url(url) and parts.path.startswith("/chat/")


def _is_target_chat_url(url: str, target_chat: str | None) -> bool:
    if not target_chat:
        return _is_dola_chat_url(url)
    current = urlsplit(url)
    target = urlsplit(target_chat)
    return current.hostname == target.hostname and current.path == target.path


async def _visible_count(page: Page, selector: str) -> int:
    try:
        count = await page.locator(selector).count()
        visible = 0
        for index in range(min(count, 5)):
            try:
                if await page.locator(selector).nth(index).is_visible(timeout=250):
                    visible += 1
            except Exception:
                continue
        return visible
    except Exception:
        return 0


async def login_session_status(page: Page) -> str:
    """Return a conservative status without reading passwords, cookies, or page text."""
    current = page.url.lower()
    if any(marker in current for marker in LOGIN_URL_MARKERS):
        return "MANUAL_REQUIRED"
    if await _visible_count(page, "input[type='password']"):
        return "MANUAL_REQUIRED"
    if await _visible_count(page, "a[href*='accounts.google.com']"):
        return "MANUAL_REQUIRED"
    return "PASS"


def _target_page(context: BrowserContext, target_chat: str | None) -> Page | None:
    pages = list(context.pages)
    if target_chat:
        target_parts = urlsplit(target_chat)
        for page in pages:
            current = urlsplit(page.url)
            if current.hostname == target_parts.hostname and current.path == target_parts.path:
                return page
    for page in pages:
        if _is_dola_chat_url(page.url):
            return page
    for page in pages:
        try:
            if is_dola_response_url(page.url):
                return page
        except Exception:
            continue
    return pages[0] if pages else None


async def _wait_until_logged_in(page: Page, timeout_seconds: float) -> str:
    deadline = time.monotonic() + max(timeout_seconds, 0)
    status = await login_session_status(page)
    while status == "MANUAL_REQUIRED" and time.monotonic() < deadline:
        await asyncio.sleep(1)
        status = await login_session_status(page)
    return status


async def _router_or_hydration(page: Page) -> tuple[Any, str] | None:
    try:
        router = await page.evaluate("() => window._ROUTER_DATA || null")
    except Exception:
        router = None
    if router is not None:
        try:
            text = json.dumps(router, ensure_ascii=False)
            if score_response_metadata(text)[0] >= 8:
                return router, "window._ROUTER_DATA"
        except (TypeError, ValueError):
            pass

    try:
        scripts = page.locator("script[type='application/json']")
        count = await scripts.count()
    except Exception:
        return None
    for index in range(min(count, 100)):
        try:
            text = await scripts.nth(index).text_content()
            parsed = json.loads(text or "")
            if score_response_metadata(json.dumps(parsed, ensure_ascii=False))[0] >= 8:
                return parsed, "script[type=application/json]"
        except (Exception, json.JSONDecodeError):
            continue
    return None


def _capture_acceptance(capture_results: list[dict[str, Any]], *, ffprobe: dict[str, Any] | None = None) -> dict[str, Any]:
    if not capture_results:
        return {
            "CAPTURE_RESPONSE": "FAIL",
            "FOUND_FALLBACK_API": "NO",
            "FOUND_VIDEO_LIST": "NO",
            "FOUND_QAAB": "NO",
            "FOUND_CLEAN_CANDIDATE": "NO",
            "HIGHEST_NATIVE_RESOLUTION": "UNKNOWN",
            "HIGHEST_BITRATE": "UNKNOWN",
            "DOWNLOAD_CLEAN_SOURCE": "NOT_AVAILABLE",
            "DOWNLOAD_METHOD": "NONE",
            "FFPROBE": "NOT_RUN",
            "VISIBLE_DOLA_WATERMARK": "UNVERIFIED",
        }
    first = capture_results[0]
    acceptance = dict(first.get("acceptance") or {})
    resolution = acceptance.get("HIGHEST_NATIVE_RESOLUTION", "UNKNOWN")
    bitrate = "UNKNOWN"
    report_path = first.get("resolve_report_path")
    if report_path:
        try:
            report = json.loads(Path(report_path).read_text(encoding="utf-8"))
            source_metadata = report.get("source_metadata") or {}
            acceptance.setdefault("FOUND_QAAB", "YES" if source_metadata.get("key_seed_present") else "NO")
            candidates = report.get("candidates") or []
            values = [item.get("bitrate") or item.get("real_bitrate") for item in candidates if isinstance(item, dict)]
            values = [int(value) for value in values if isinstance(value, (int, float)) or str(value).isdigit()]
            if values:
                bitrate = max(values)
            selected = report.get("selected") or {}
            if selected.get("width") and selected.get("height"):
                resolution = f"{selected['width']}x{selected['height']}"
            download = report.get("download") or {}
            acceptance.setdefault("DOWNLOAD_METHOD", download.get("method", "NONE"))
            acceptance.setdefault("DOWNLOAD_CLEAN_SOURCE", "PASS" if download.get("status") == "success" else acceptance.get("DOWNLOAD_CLEAN_SOURCE", "NOT_AVAILABLE"))
            acceptance.setdefault("FFPROBE", "PASS" if report.get("ffprobe") else "NOT_RUN")
        except (OSError, TypeError, ValueError):
            pass
    acceptance.setdefault("CAPTURE_RESPONSE", "PASS")
    acceptance.setdefault("FOUND_QAAB", "NO")
    acceptance.setdefault("HIGHEST_BITRATE", bitrate)
    acceptance.setdefault("DOWNLOAD_METHOD", "NONE")
    acceptance.setdefault("FFPROBE", "PASS" if ffprobe else "NOT_RUN")
    acceptance.setdefault("VISIBLE_DOLA_WATERMARK", "UNVERIFIED")
    acceptance["HIGHEST_NATIVE_RESOLUTION"] = resolution
    acceptance["HIGHEST_BITRATE"] = bitrate if bitrate != "UNKNOWN" else acceptance.get("HIGHEST_BITRATE", "UNKNOWN")
    return acceptance


async def run_dola_cdp(
    *,
    endpoint: str = DEFAULT_CDP_ENDPOINT,
    target_chat: str | None = DEFAULT_TARGET_CHAT,
    auto_download: bool = False,
    discover_network: bool = False,
    output_dir: str | Path = "captures",
    wait_seconds: float = 120,
) -> dict[str, Any]:
    endpoint = validate_cdp_endpoint(endpoint)
    if target_chat:
        target_chat = validate_target_chat(target_chat)
    output_path = Path(output_dir).resolve()
    output_path.mkdir(parents=True, exist_ok=True)
    store = CaptureStore(output_path, auto_download=False, fetch_fallback=True)
    capture = ResponseCapture(store, discover_network=discover_network)
    summary: dict[str, Any] = {
        "EXTERNAL_BROWSER_LAUNCH": "MANUAL_GATE",
        "CDP_READY": "NO",
        "PLAYWRIGHT_CDP_CONNECT": "NO",
        "DOLA_LOGIN_SESSION": "MANUAL_REQUIRED",
        "TARGET_CHAT_LOADED": "FAIL",
        "endpoint": endpoint,
        "capture_results": [],
        "router_data_fallback": False,
    }

    async with async_playwright() as playwright:
        try:
            browser: Browser = await playwright.chromium.connect_over_cdp(endpoint)
        except Exception as exc:
            summary["error"] = f"CDP connect failed: {exc}"
            summary.update(_capture_acceptance([]))
            return summary
        summary["EXTERNAL_BROWSER_LAUNCH"] = "PASS"
        summary["CDP_READY"] = "PASS"
        summary["PLAYWRIGHT_CDP_CONNECT"] = "PASS"
        if not browser.contexts:
            summary["error"] = "CDP browser has no existing browser context"
            summary.update(_capture_acceptance([]))
            return summary
        context = browser.contexts[0]
        capture.attach(context, discovery_path=output_path / "network-discovery.json")
        try:
            page = _target_page(context, target_chat)
            if page is None:
                page = await context.new_page()
            if target_chat and not _is_target_chat_url(page.url, target_chat):
                try:
                    await page.goto(target_chat, wait_until="domcontentloaded", timeout=int(wait_seconds * 1000))
                except Exception as exc:
                    summary["navigation_error"] = str(exc)

            status = await login_session_status(page)
            if status == "MANUAL_REQUIRED":
                print("DOLA_LOGIN_SESSION: MANUAL_REQUIRED")
                print("[dola-cdp] 在外部 Chrome/Edge 中完成本人 Dola 登录；不要提供密码给程序。")
                status = await _wait_until_logged_in(page, wait_seconds)
            summary["DOLA_LOGIN_SESSION"] = status
            if status != "PASS":
                summary["error"] = "Dola login was not completed in the external browser"
                summary.update(_capture_acceptance([]))
                return summary

            if target_chat and not _is_target_chat_url(page.url, target_chat):
                await page.goto(target_chat, wait_until="domcontentloaded", timeout=int(wait_seconds * 1000))
            summary["TARGET_CHAT_LOADED"] = "PASS" if _is_dola_chat_url(page.url) else "FAIL"
            print("CDP_READY: YES")
            print("PLAYWRIGHT_CDP_CONNECT: PASS")
            print("[dola-cdp] listener attached; refreshing the target chat once")
            try:
                await page.reload(wait_until="domcontentloaded", timeout=int(wait_seconds * 1000))
            except Exception as exc:
                summary["reload_error"] = str(exc)

            captured = await capture.wait_for_capture(wait_seconds)
            if not captured:
                fallback = await _router_or_hydration(page)
                if fallback is not None:
                    parsed, source = fallback
                    result = await asyncio.to_thread(store.save_router_data, parsed, page_url=page.url, include_internal=True)
                    result["capture_source"] = source
                    capture.capture_results.append(result)
                    summary["router_data_fallback"] = True

            if capture.discovery is not None:
                capture.discovery.save()
            summary["capture_results"] = [{key: value for key, value in item.items() if not key.startswith("_")} for item in capture.capture_results]

            if auto_download:
                for item in capture.capture_results:
                    internal = item.get("_resolve_result")
                    if internal is None or internal.status != "success" or internal.selected is None:
                        continue
                    output_file = output_path / "downloads" / (Path(item["raw_path"]).stem + ".mp4")
                    try:
                        downloaded, method = await download_stream_with_playwright_fallback(internal.selected.url, context, output_file)
                        ffprobe = await asyncio.to_thread(probe_media, downloaded)
                        store.finalize_playwright_download(item, internal, output_path=downloaded, ffprobe=ffprobe, method=method)
                    except Exception as exc:
                        store.finalize_playwright_download(item, internal, output_path=output_file, method="NONE", error=exc)

            summary["acceptance"] = _capture_acceptance(capture.capture_results)
            summary.update(summary["acceptance"])
            if capture.capture_results:
                first = capture.capture_results[0]
                raw_path = first.get("raw_path")
                if raw_path:
                    try:
                        raw_text = Path(raw_path).read_text(encoding="utf-8")
                        _, matched = score_response_metadata(raw_text)
                        summary["matched_fields"] = matched
                        summary["capture_endpoint"] = first.get("request_url", "UNKNOWN")
                    except OSError:
                        pass
            return summary
        finally:
            capture.detach(context)
            # Do not call browser.close() or context.close(): the external
            # Chrome/Edge process and its logged-in profile belong to the user.


__all__ = [
    "DEFAULT_CDP_ENDPOINT",
    "DEFAULT_TARGET_CHAT",
    "login_session_status",
    "run_dola_cdp",
    "validate_cdp_endpoint",
    "validate_target_chat",
]
