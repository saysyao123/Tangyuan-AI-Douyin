from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest
from playwright.async_api import async_playwright

from app.capture.browser_session import DEFAULT_PROFILE
from app.capture.local_bridge import CaptureStore
from app.capture.response_capture import (
    NetworkDiscovery,
    ResponseCapture,
    _decode_body,
    _relevant_fields,
    is_chain_single_url,
    is_discovery_host,
    is_dola_response_url,
)
from app.download import authenticated


class FakeRequest:
    method = "GET"


class FakeFrame:
    url = "https://www.dola.com/chat/fixture"


class FakeResponse:
    def __init__(self, url: str, body: bytes, *, status: int = 200, content_type: str = "application/json") -> None:
        self.url = url
        self.status = status
        self.request = FakeRequest()
        self.frame = FakeFrame()
        self._body = body
        self._headers = {"content-type": content_type}

    async def finished(self) -> None:
        return None

    async def body(self) -> bytes:
        return self._body

    async def all_headers(self) -> dict[str, str]:
        return self._headers


def test_persistent_profile_path(tmp_path: Path) -> None:
    assert DEFAULT_PROFILE.as_posix().endswith("runtime/dola-browser-profile")
    assert "Google" not in str(DEFAULT_PROFILE)

    async def launch() -> None:
        async with async_playwright() as playwright:
            context = await playwright.chromium.launch_persistent_context(
                user_data_dir=str(tmp_path / "profile"),
                headless=True,
            )
            assert context.pages is not None
            await context.close()

    asyncio.run(launch())


def test_dola_response_match() -> None:
    assert is_dola_response_url("https://www.dola.com/im/chain/single?x=1")
    assert is_chain_single_url("https://sub.dola.com/api/im/chain/single/v2")


def test_non_dola_reject() -> None:
    assert not is_dola_response_url("https://dola.com.evil.example/im/chain/single")
    assert not is_chain_single_url("https://evil.dola.com.example/im/chain/single")
    assert not is_chain_single_url("https://www.dola.com/chat")


def test_relevant_response_filter() -> None:
    assert "fallback_api" in _relevant_fields('{"fallback_api":"x"}')
    assert _relevant_fields('{"message":"hello"}') == []


def test_capture_body_utf8() -> None:
    text, encoding = _decode_body('{"说明":"雨夜"}'.encode("utf-8"), "application/json; charset=utf-8")
    assert text == '{"说明":"雨夜"}'
    assert encoding == "utf-8"


def test_capture_save_and_auto_resolve(tmp_path: Path) -> None:
    async def capture_one() -> dict:
        store = CaptureStore(tmp_path / "captures", auto_download=False, fetch_fallback=False)
        capture = ResponseCapture(store)
        response = FakeResponse(
            "https://www.dola.com/im/chain/single?secret=redacted",
            json.dumps(
                {
                    "vid": "v186a3gm000cda9gbpfog65jfpbu9q50",
                    "video_list": [
                        {
                            "main_url": "https://cdn.example.test/clean.mp4?lr=unwatermarked",
                            "logo_type": "unwatermarked",
                            "width": 1280,
                            "height": 720,
                            "codec_type": "h264",
                        }
                    ],
                },
                ensure_ascii=False,
            ).encode("utf-8"),
        )
        await capture._handle_response(response)
        return capture.capture_results[0]

    result = asyncio.run(capture_one())
    assert Path(result["raw_path"]).exists()
    assert Path(result["resolve_report_path"]).exists()
    assert result["acceptance"]["FOUND_CLEAN_CANDIDATE"] == "YES"
    assert "secret=redacted" not in Path(result["resolve_report_path"]).read_text(encoding="utf-8")


def test_network_discovery_redaction(tmp_path: Path) -> None:
    async def discover_one() -> Path:
        output = tmp_path / "network-discovery.json"
        discovery = NetworkDiscovery(output)
        response = FakeResponse(
            "https://api.byteintlapi.com/private?token=do-not-log",
            b'{"fallback_api":"https://cdn.example.test/x?sig=secret"}',
        )
        await discovery.observe(response)
        return discovery.save()

    path = asyncio.run(discover_one())
    saved = path.read_text(encoding="utf-8")
    assert "byteintlapi.com" in saved
    assert "do-not-log" not in saved
    assert "sig=secret" not in saved


def test_authenticated_download_fallback_mock(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    payload = b"\x00\x00\x00\x18ftypisom\x00\x00\x02\x00playwright"

    def denied(*args, **kwargs):
        raise PermissionError("HTTP 403: authenticated access required; no bypass attempted")

    class FakeAPIResponse:
        status = 200

        async def body(self) -> bytes:
            return payload

        async def all_headers(self) -> dict[str, str]:
            return {"content-length": str(len(payload))}

    class FakeAPIRequest:
        async def get(self, url: str, **kwargs) -> FakeAPIResponse:
            return FakeAPIResponse()

    class FakeContext:
        request = FakeAPIRequest()

    monkeypatch.setattr(authenticated, "download_stream", denied)
    output, method = asyncio.run(
        authenticated.download_stream_with_playwright_fallback(
            "https://cdn.example.test/clean.mp4?lr=unwatermarked",
            FakeContext(),
            tmp_path / "fallback.mp4",
        )
    )
    assert output.read_bytes() == payload
    assert method == "PLAYWRIGHT_CONTEXT"


def test_context_fallback_403_fails_closed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def denied(*args, **kwargs):
        raise PermissionError("HTTP 403: authenticated access required; no bypass attempted")

    class FakeAPIResponse:
        status = 403

    class FakeAPIRequest:
        async def get(self, url: str, **kwargs) -> FakeAPIResponse:
            return FakeAPIResponse()

    class FakeContext:
        request = FakeAPIRequest()

    monkeypatch.setattr(authenticated, "download_stream", denied)
    with pytest.raises(PermissionError, match="no bypass attempted"):
        asyncio.run(
            authenticated.download_stream_with_playwright_fallback(
                "https://cdn.example.test/clean.mp4?lr=unwatermarked",
                FakeContext(),
                tmp_path / "forbidden.mp4",
            )
        )


def test_discovery_host_allowlist() -> None:
    assert is_discovery_host("https://www.dola.com/im/chain/single")
    assert is_discovery_host("https://api.byteintlapi.com/v1/data")
    assert not is_discovery_host("https://byteintlapi.com.evil.example/v1/data")
