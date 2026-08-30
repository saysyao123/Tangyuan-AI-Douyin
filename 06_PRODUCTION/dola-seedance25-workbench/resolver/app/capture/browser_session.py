from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

from playwright.async_api import BrowserContext, Error as PlaywrightError, Page, async_playwright

from app.capture.local_bridge import CaptureStore
from app.capture.response_capture import ResponseCapture, _relevant_fields
from app.download.authenticated import download_stream_with_playwright_fallback
from app.qa.ffprobe import probe_media


DEFAULT_PROFILE = Path("runtime") / "dola-browser-profile"
DEFAULT_URL = "https://www.dola.com/"


def _is_relevant_json(value: Any) -> bool:
    try:
        import json

        text = json.dumps(value, ensure_ascii=False)
    except (TypeError, ValueError):
        return False
    return bool(_relevant_fields(text))


async def _router_data(page: Page) -> Any:
    try:
        return await page.evaluate("() => window._ROUTER_DATA || null")
    except Exception:
        return None


async def run_dola_browser(
    *,
    profile: str | Path = DEFAULT_PROFILE,
    url: str = DEFAULT_URL,
    auto_download: bool = False,
    headless: bool = False,
    output_dir: str | Path = "captures",
    timeout_seconds: float = 300,
    discover_network: bool = False,
) -> dict[str, Any]:
    profile_dir = Path(profile).resolve()
    output_path = Path(output_dir).resolve()
    if headless and not profile_dir.exists():
        raise ValueError("--headless requires an existing persistent profile; run headed once for manual login")
    profile_dir.mkdir(parents=True, exist_ok=True)
    output_path.mkdir(parents=True, exist_ok=True)

    store = CaptureStore(output_path, auto_download=False, fetch_fallback=True)
    capture = ResponseCapture(store, discover_network=discover_network)
    summary: dict[str, Any] = {
        "profile": str(profile_dir),
        "url": url,
        "headless": headless,
        "capture_results": [],
        "router_data_fallback": False,
        "raw_bytes_debug": [],
    }

    async with async_playwright() as playwright:
        try:
            context: BrowserContext = await playwright.chromium.launch_persistent_context(
                user_data_dir=str(profile_dir),
                headless=headless,
            )
        except PlaywrightError as exc:
            message = str(exc)
            lowered = message.lower()
            if (
                "already running" in lowered
                or "processsingleton" in lowered
                or "user data directory" in lowered
                or "already in use" in lowered
            ):
                raise RuntimeError("persistent profile is already in use; close the other Dola browser first") from exc
            raise RuntimeError(f"could not launch persistent Chromium: {message}") from exc

        try:
            capture.attach(context, discovery_path=output_path / "network-discovery.json")
            page = context.pages[0] if context.pages else await context.new_page()
            print(f"[dola-browser] {'headed' if not headless else 'headless'} browser opened; complete Dola login manually if needed")
            print("[dola-browser] open your own completed video conversation and refresh it")
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=int(timeout_seconds * 1000))
            except Exception as exc:
                summary["navigation_error"] = str(exc)
            captured = await capture.wait_for_capture(timeout_seconds)

            if not captured:
                router = await _router_data(page)
                if router is not None and _is_relevant_json(router):
                    result = await asyncio.to_thread(store.save_router_data, router, page_url=page.url, include_internal=True)
                    capture.capture_results.append(result)
                    capture._captured.set()
                    summary["router_data_fallback"] = True
                    captured = True

            if discover_network and capture.discovery is not None:
                capture.discovery.save()
            summary["capture_results"] = [{key: value for key, value in item.items() if not key.startswith("_")} for item in capture.capture_results]
            summary["raw_bytes_debug"] = [str(path) for path in capture.raw_bytes_debug]

            if auto_download:
                for capture_result in capture.capture_results:
                    internal_result = capture_result.get("_resolve_result")
                    if internal_result is None or internal_result.status != "success" or internal_result.selected is None:
                        continue
                    output_file = output_path / "downloads" / (Path(capture_result["raw_path"]).stem + ".mp4")
                    try:
                        downloaded, method = await download_stream_with_playwright_fallback(
                            internal_result.selected.url,
                            context,
                            output_file,
                        )
                        ffprobe = await asyncio.to_thread(probe_media, downloaded)
                        store.finalize_playwright_download(
                            capture_result,
                            internal_result,
                            output_path=downloaded,
                            ffprobe=ffprobe,
                            method=method,
                        )
                    except Exception as exc:
                        store.finalize_playwright_download(
                            capture_result,
                            internal_result,
                            output_path=output_file,
                            method="NONE",
                            error=exc,
                        )
            return summary
        finally:
            capture.detach(context)
            await context.close()
