from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

from app.production.account_registry import AccountRegistry
from app.production.consumer_gateway import (
    ConsumerGatewayClient,
    sync_registry_from_consumer_gateway,
    validate_gateway_endpoint,
)


class GatewayHandler(BaseHTTPRequestHandler):
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
        if self.path == "/health":
            return self._send({"status": "ok", "logged_in": True, "accounts": {"total": 1, "ready": 1}})
        if self.path == "/admin/api/accounts":
            return self._send({"accounts": [{"id": "account-02", "name": "136792", "status": "ready", "runtime": {"ready": True, "hot": True}, "quota_status": {"video": {"remaining": 8, "limit": 10}}}]})
        if self.path == "/admin/api/accounts/account-02/status":
            return self._send({"account_id": "account-02", "logged_in": True})
        return self._send({"detail": "not found"}, 404)

    def do_POST(self) -> None:  # noqa: N802
        if self.path.endswith("/probe"):
            return self._send({"status": "healthy", "account_id": "account-02", "ms": 12, "response": "2"})
        if self.path.endswith("/start"):
            return self._send({"status": "ready", "account": {"id": "account-02", "name": "136792", "status": "ready", "runtime": {"ready": True}, "quota_status": {}}})
        if self.path.endswith("/stop"):
            return self._send({"status": "stopped", "account_id": "account-02"})
        return self._send({"detail": "not found"}, 404)


@pytest.fixture()
def gateway_server() -> tuple[ThreadingHTTPServer, str]:
    server = ThreadingHTTPServer(("127.0.0.1", 0), GatewayHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server, f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        thread.join(timeout=5)


def test_gateway_endpoint_is_loopback_only() -> None:
    assert validate_gateway_endpoint("http://127.0.0.1:19090") == "http://127.0.0.1:19090"
    with pytest.raises(ValueError):
        validate_gateway_endpoint("https://example.com:19090")


def test_gateway_client_redacts_account_storage_details(gateway_server: tuple[ThreadingHTTPServer, str]) -> None:
    _, endpoint = gateway_server
    client = ConsumerGatewayClient(endpoint)
    assert client.health()["logged_in"] is True
    account = client.accounts()[0]
    assert account == {
        "host_account_id": "account-02",
        "display_name": "136792",
        "host_status": "ready",
        "runtime_ready": True,
        "runtime_hot": True,
        "needs_captcha": False,
        "video_remaining_local": 8,
        "video_limit_local": 10,
    }
    assert "session_file" not in account
    assert client.status("account-02")["logged_in"] is True
    assert client.start("account-02")["status"] == "ready"
    assert client.probe("account-02")["status"] == "healthy"


def test_gateway_sync_reuses_empty_local_slots_and_marks_live_ready(tmp_path: Path) -> None:
    registry = AccountRegistry(tmp_path / "accounts.json")
    registry.add("A01", display_name="placeholder")
    mapping = sync_registry_from_consumer_gateway(
        registry,
        [{"host_account_id": "account-02", "display_name": "136792", "host_status": "ready", "runtime_ready": True}],
    )
    assert mapping[0]["account_id"] == "A01"
    account = registry.get("A01")
    assert account.session_host == "consumer_gateway"
    assert account.host_account_id == "account-02"
    assert account.status == "READY"
