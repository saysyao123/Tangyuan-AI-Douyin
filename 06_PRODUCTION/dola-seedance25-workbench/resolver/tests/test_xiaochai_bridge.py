from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

from app.cli import build_parser
from app.production.account_registry import AccountRegistry
from app.production.xiaochai_bridge import (
    XiaochaiBridgeClient,
    latest_capture_body,
    sync_registry_from_xiaochai,
    validate_bridge_endpoint,
)


class BridgeHandler(BaseHTTPRequestHandler):
    last_headers: dict[str, str] = {}
    last_body: dict[str, object] = {}

    def log_message(self, format: str, *args: object) -> None:
        return

    def _send(self, payload: dict[str, object], status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        self.__class__.last_headers = {key.lower(): value for key, value in self.headers.items()}
        if self.path == "/v1/health":
            return self._send({"ok": True, "bridge_version": "1"})
        if self.path == "/v1/accounts":
            return self._send({"ok": True, "accounts": [{"host_account_id": "host-1", "display_name": "A"}]})
        if self.path.startswith("/v1/accounts/host-1/capture/latest"):
            return self._send({"ok": True, "captures": [{"source_key": "network:1", "body": '{"video_list": []}'}]})
        return self._send({"ok": False, "error_code": "NOT_FOUND"}, 404)

    def do_POST(self) -> None:  # noqa: N802
        self.__class__.last_headers = {key.lower(): value for key, value in self.headers.items()}
        length = int(self.headers.get("Content-Length", "0"))
        self.__class__.last_body = json.loads(self.rfile.read(length).decode("utf-8"))
        return self._send({"ok": True, "path": "/download", "bytes": 12})


@pytest.fixture()
def bridge_server() -> tuple[ThreadingHTTPServer, str]:
    server = ThreadingHTTPServer(("127.0.0.1", 0), BridgeHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server, f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        thread.join(timeout=5)


def test_bridge_endpoint_is_loopback_only() -> None:
    assert validate_bridge_endpoint("http://127.0.0.1:8766") == "http://127.0.0.1:8766"
    with pytest.raises(ValueError):
        validate_bridge_endpoint("https://example.com:8766")
    with pytest.raises(ValueError):
        validate_bridge_endpoint("http://127.0.0.1:8766/?token=secret")


def test_bridge_client_has_public_account_and_capture_operations(bridge_server: tuple[ThreadingHTTPServer, str]) -> None:
    _, endpoint = bridge_server
    client = XiaochaiBridgeClient(endpoint, token="local-test-token")
    assert client.health()["ok"] is True
    assert client.accounts()[0]["host_account_id"] == "host-1"
    captures = client.capture_latest("host-1")
    assert captures[0]["source_key"] == "network:1"
    assert "cookie" not in BridgeHandler.last_headers
    result = client.download("host-1", "https://cdn.dola.com/video.mp4?sig=abc", "video.mp4")
    assert result["bytes"] == 12
    assert BridgeHandler.last_body["filename"] == "video.mp4"
    assert "cookie" not in BridgeHandler.last_headers


def test_registry_sync_binds_host_without_marking_ready(tmp_path: Path) -> None:
    registry = AccountRegistry(tmp_path / "accounts.json")
    registry.add("A01", display_name="existing", status="READY")
    mapping = sync_registry_from_xiaochai(
        registry,
        [
            {"host_account_id": "host-1", "profile_name": "new account", "auth_status": "authenticated"},
            {"host_account_id": "host-2", "display_name": "second", "auth_status": "logged_out"},
        ],
    )
    assert [item["account_id"] for item in mapping] == ["A02", "A03"]
    assert [account.status for account in registry.accounts] == ["READY", "NEEDS_LOGIN", "NEEDS_LOGIN"]
    assert registry.get("A02").session_host == "xiaochai"
    assert registry.get("A02").host_account_id == "host-1"


def test_latest_capture_requires_xiaochai_mapping(bridge_server: tuple[ThreadingHTTPServer, str], tmp_path: Path) -> None:
    _, endpoint = bridge_server
    client = XiaochaiBridgeClient(endpoint)
    registry = AccountRegistry(tmp_path / "accounts.json")
    account = registry.add("A01", display_name="x", session_host="xiaochai", host_account_id="host-1")
    body, entry = latest_capture_body(client, account)
    assert json.loads(body) == {"video_list": []}
    assert entry["source_key"] == "network:1"


def test_cli_exposes_xiaochai_bridge_commands() -> None:
    args = build_parser().parse_args(["xiaochai-bridge", "health"])
    assert args.command == "xiaochai-bridge"
    assert args.bridge_command == "health"
