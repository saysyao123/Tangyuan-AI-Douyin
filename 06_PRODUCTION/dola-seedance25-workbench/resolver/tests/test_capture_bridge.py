from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import requests

from app.capture.local_bridge import CaptureStore, create_server


CHAIN_URL = "https://www.dola.com/im/chain/single?conversation_id=fixture"


def envelope(media_url: str, *, request_url: str = CHAIN_URL) -> dict:
    return {
        "captured_at": "2026-08-30T12:00:00Z",
        "page_url": "https://www.dola.com/chat/fixture?secret=redact-me",
        "request_url": request_url,
        "response_status": 200,
        "raw_body": json.dumps(
            {
                "vid": "v186a3gm000cda9gbpfog65jfpbu9q50",
                "video_list": [
                    {
                        "main_url": media_url,
                        "logo_type": "unwatermarked",
                        "width": 1280,
                        "height": 720,
                        "bitrate": 6000000,
                        "codec_type": "h264",
                    }
                ],
            }
        ),
    }


class QuietHandler(BaseHTTPRequestHandler):
    status = 200

    def do_GET(self) -> None:
        self.send_response(self.status)
        self.end_headers()

    def log_message(self, format: str, *args: object) -> None:
        return


def run_server(handler: type[BaseHTTPRequestHandler]) -> tuple[ThreadingHTTPServer, threading.Thread]:
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def test_bridge_health_and_post_capture(tmp_path: Path) -> None:
    server = create_server(port=0, out_dir=tmp_path / "captures", fetch_fallback=False)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        base = f"http://127.0.0.1:{server.server_port}"
        health = requests.get(base + "/health", timeout=5)
        assert health.status_code == 200
        assert health.json() == {"ok": True}
        response = requests.post(base + "/capture", json=envelope("https://cdn.example.test/clean.mp4?lr=unwatermarked"), timeout=5)
        body = response.json()
        assert response.status_code == 200
        assert body["ok"] is True
        assert Path(body["raw_path"]).exists()
        assert Path(body["meta_path"]).exists()
        assert Path(body["resolve_report_path"]).exists()
        assert body["acceptance"]["FOUND_CLEAN_CANDIDATE"] == "YES"
        assert "secret=redact-me" not in Path(body["meta_path"]).read_text(encoding="utf-8")
    finally:
        server.shutdown()
        thread.join(timeout=5)


def test_invalid_host_and_endpoint_rejected(tmp_path: Path) -> None:
    server = create_server(port=0, out_dir=tmp_path, fetch_fallback=False)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        base = f"http://127.0.0.1:{server.server_port}"
        bad_host = requests.post(base + "/capture", json=envelope("https://cdn.example.test/x.mp4", request_url="https://evil.example/im/chain/single"), timeout=5)
        bad_endpoint = requests.post(base + "/capture", json=envelope("https://cdn.example.test/x.mp4", request_url="https://www.dola.com/api/im/chain/single-extra"), timeout=5)
        assert bad_host.status_code == 400
        assert bad_endpoint.status_code == 400
        assert not list(tmp_path.glob("*.json"))
    finally:
        server.shutdown()
        thread.join(timeout=5)


def test_auto_resolve_and_no_clean_candidate(tmp_path: Path) -> None:
    server = create_server(port=0, out_dir=tmp_path / "auto", auto_download=True, fetch_fallback=False)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        base = f"http://127.0.0.1:{server.server_port}"
        clean = requests.post(base + "/capture", json=envelope(base + "/unavailable.mp4?lr=unwatermarked"), timeout=5)
        clean_body = clean.json()
        assert clean_body["acceptance"]["FOUND_CLEAN_CANDIDATE"] == "YES"
        assert clean_body["acceptance"]["DOWNLOAD_CLEAN_SOURCE"] == "FAIL"

        watermarked = envelope("https://cdn.example.test/preview.mp4?lr=video_gen_watermark_dyn")
        water_body = requests.post(base + "/capture", json=watermarked, timeout=5).json()
        assert water_body["acceptance"]["FOUND_CLEAN_CANDIDATE"] == "NO"
        assert water_body["acceptance"]["DOWNLOAD_CLEAN_SOURCE"] == "NOT_AVAILABLE"
    finally:
        server.shutdown()
        thread.join(timeout=5)


def test_403_fails_closed(tmp_path: Path) -> None:
    class ForbiddenHandler(QuietHandler):
        status = 403

    media_server, media_thread = run_server(ForbiddenHandler)
    bridge = create_server(port=0, out_dir=tmp_path / "forbidden", auto_download=True, fetch_fallback=False)
    bridge_thread = threading.Thread(target=bridge.serve_forever, daemon=True)
    bridge_thread.start()
    try:
        media_url = f"http://127.0.0.1:{media_server.server_port}/source.mp4?lr=unwatermarked"
        base = f"http://127.0.0.1:{bridge.server_port}"
        response = requests.post(base + "/capture", json=envelope(media_url), timeout=5)
        body = response.json()
        assert response.status_code == 200
        assert body["acceptance"]["DOWNLOAD_CLEAN_SOURCE"] == "FAIL"
        report = json.loads(Path(body["resolve_report_path"]).read_text(encoding="utf-8"))
        assert "403" in report["download"]["error"]
        assert report["download"]["bypass_attempted"] is False
        assert not list((tmp_path / "forbidden" / "downloads").glob("*.part"))
    finally:
        bridge.shutdown()
        bridge_thread.join(timeout=5)
        media_server.shutdown()
        media_thread.join(timeout=5)
