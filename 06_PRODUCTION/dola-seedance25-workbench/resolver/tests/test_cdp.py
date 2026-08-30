from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from app.capture import cdp_browser
from app.capture.local_bridge import CaptureStore
from app.capture.response_capture import NetworkDiscovery, ResponseCapture, score_response_metadata
from tools.check_cdp import main as check_cdp_main, read_cdp_version


class FakeRequest:
    method = "POST"


class FakeFrame:
    url = "https://www.dola.com/chat/fixture"


class FakeResponse:
    def __init__(self, url: str, body: bytes, *, content_type: str = "application/json") -> None:
        self.url = url
        self.status = 200
        self.request = FakeRequest()
        self.frame = FakeFrame()
        self._body = body
        self._headers = {"content-type": content_type}

    async def body(self) -> bytes:
        return self._body

    async def all_headers(self) -> dict[str, str]:
        return self._headers


def test_cdp_endpoint_and_target_validation() -> None:
    assert cdp_browser.validate_cdp_endpoint("http://127.0.0.1:9222") == "http://127.0.0.1:9222"
    assert cdp_browser.validate_target_chat("https://www.dola.com/chat/00000000000000000").endswith("00000000000000000")
    with pytest.raises(ValueError):
        cdp_browser.validate_cdp_endpoint("https://example.com:9222")
    with pytest.raises(ValueError):
        cdp_browser.validate_cdp_endpoint("http://127.0.0.1:9222/?token=secret")
    with pytest.raises(ValueError):
        cdp_browser.validate_target_chat("https://evil.example/chat/1")


def test_cdp_endpoint_health_reader(monkeypatch: pytest.MonkeyPatch) -> None:
    class _Response:
        def __enter__(self) -> "_Response":
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def read(self) -> bytes:
            return b'{"Browser":"Chrome/136","Protocol-Version":"1.3","webSocketDebuggerUrl":"ws://127.0.0.1/devtools/browser/id"}'

    monkeypatch.setattr("tools.check_cdp.urlopen", lambda *args, **kwargs: _Response())
    payload = read_cdp_version()
    assert payload["Browser"] == "Chrome/136"
    assert payload["Protocol-Version"] == "1.3"
    assert payload["webSocketDebuggerUrl"].startswith("ws://127.0.0.1/")

    assert check_cdp_main(["http://127.0.0.1:9332"]) == 0


def test_response_relevance_score_rejects_video_model_only() -> None:
    assert score_response_metadata('{"video_model":"seedance"}') == (1, ["video_model"])
    assert score_response_metadata('{"video_model":"seedance","video_list":[]}')[0] >= 8
    nested = '{"media":"{\\"vid\\":\\"v186a3gm000cda9gbpfog65jfpbu9q50\\",\\"video_list\\":[]}"}'
    assert score_response_metadata(nested)[0] >= 13


def test_video_model_only_is_not_saved_as_media_discovery(tmp_path: Path) -> None:
    async def run() -> Path:
        discovery = NetworkDiscovery(tmp_path / "network-discovery.json")
        response = FakeResponse("https://www.dola.com/samantha/user/ab/get", b'{"video_model":"seedance"}')
        await discovery.observe(response)
        return discovery.save()

    saved = asyncio.run(run())
    assert '"entries": []' in saved.read_text(encoding="utf-8")


def test_high_score_discovery_saves_capture_and_redacted_index(tmp_path: Path) -> None:
    async def run() -> list[dict]:
        store = CaptureStore(tmp_path / "captures", fetch_fallback=False)
        capture = ResponseCapture(store, discover_network=True)
        capture.attach(_Context(), discovery_path=tmp_path / "captures" / "network-discovery.json")
        response = FakeResponse(
            "https://api.byteintlapi.com/v1/media?token=secret",
            b'{"vid":"v186a3gm000cda9gbpfog65jfpbu9q50","video_list":[{"main_url":"https://cdn.example/clean.mp4?sig=secret","logo_type":"unwatermarked","width":720,"height":1280}]}',
        )
        await capture._handle_response(response)
        assert capture.discovery is not None
        index = capture.discovery.save()
        assert "token=secret" not in index.read_text(encoding="utf-8")
        assert capture.capture_results
        return capture.capture_results

    results = asyncio.run(run())
    assert Path(results[0]["raw_path"]).exists()
    assert results[0]["acceptance"]["FOUND_CLEAN_CANDIDATE"] == "YES"


class _EmptyLocator:
    async def count(self) -> int:
        return 0


class _Page:
    url = "https://www.dola.com/chat/00000000000000000"

    def locator(self, selector: str) -> _EmptyLocator:
        return _EmptyLocator()

    async def reload(self, **kwargs: object) -> None:
        return None

    async def evaluate(self, expression: str) -> None:
        return None


class _RouterPage(_Page):
    async def evaluate(self, expression: str) -> dict:
        return {
            "vid": "v186a3gm000cda9gbpfog65jfpbu9q50",
            "video_list": [{"main_url": "https://cdn.example/clean.mp4", "logo_type": "unwatermarked"}],
        }


def test_router_data_fallback_reader() -> None:
    source, name = asyncio.run(cdp_browser._router_or_hydration(_RouterPage()))
    assert name == "window._ROUTER_DATA"
    assert source["video_list"]


class _Context:
    def __init__(self) -> None:
        self.pages = [_Page()]
        self.listeners: dict[str, object] = {}
        self.close_called = False

    def on(self, event: str, callback: object) -> None:
        self.listeners[event] = callback

    def remove_listener(self, event: str, callback: object) -> None:
        self.listeners.pop(event, None)


class _Browser:
    def __init__(self) -> None:
        self.context = _Context()
        self.contexts = [self.context]
        self.close_called = False

    async def close(self) -> None:
        self.close_called = True


class _FakePlaywright:
    def __init__(self, browser: _Browser) -> None:
        self.chromium = self
        self.browser = browser

    async def connect_over_cdp(self, endpoint: str) -> _Browser:
        return self.browser


class _FakePlaywrightManager:
    def __init__(self, playwright: _FakePlaywright) -> None:
        self.playwright = playwright

    async def __aenter__(self) -> _FakePlaywright:
        return self.playwright

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
        return None


def test_external_cdp_does_not_close_user_browser(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    browser = _Browser()
    monkeypatch.setattr(cdp_browser, "async_playwright", lambda: _FakePlaywrightManager(_FakePlaywright(browser)))
    summary = asyncio.run(
        cdp_browser.run_dola_cdp(
            endpoint="http://127.0.0.1:9222",
            target_chat="https://www.dola.com/chat/00000000000000000",
            output_dir=tmp_path / "run",
            wait_seconds=0,
        )
    )
    assert summary["PLAYWRIGHT_CDP_CONNECT"] == "PASS"
    assert summary["CAPTURE_RESPONSE"] == "FAIL"
    assert browser.close_called is False
    assert browser.context.close_called is False
