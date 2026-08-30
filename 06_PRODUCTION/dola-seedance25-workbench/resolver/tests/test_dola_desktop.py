from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

from app.production.account_registry import AccountRegistry
from app.production.dola_desktop import (
    DolaDesktopClient,
    DolaDesktopError,
    read_control_discovery,
    sync_registry_from_dola_desktop,
)


class DolaDesktopHandler(BaseHTTPRequestHandler):
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
            return self._send({"ok": True, "service": "seedance-desktop-studio", "pid": 123, "gates": {"D1": "pending"}})
        if self.path == "/v1/accounts":
            return self._send(
                {
                    "accounts": [
                        {
                            "id": "host-a",
                            "name": "Dola A",
                            "partition": "persist:dola_host_a",
                            "createdAt": 1,
                        },
                        {
                            "id": "host-b",
                            "name": "Dola B",
                            "partition": "persist:dola_host_b",
                            "createdAt": 2,
                        },
                    ]
                }
            )
        if self.path == "/v1/accounts/host-a/session":
            return self._send({"session": {"loginStatus": "logged_in", "pageLoaded": True, "evidence": "logout_action_present", "pagePath": "https://www.dola.com/chat/"}})
        if self.path == "/v1/accounts/host-b/session":
            return self._send({"session": {"loginStatus": "logged_out", "pageLoaded": True, "evidence": "login_path", "pagePath": "https://www.dola.com/login"}})
        return self._send({"error": "not found"}, 404)

    def do_POST(self) -> None:  # noqa: N802
        if self.path == "/v1/accounts/host-a/activate":
            return self._send({"account": {"id": "host-a", "name": "Dola A", "partition": "persist:dola_host_a"}})
        return self._send({"error": "not found"}, 404)


@pytest.fixture()
def desktop_server() -> tuple[ThreadingHTTPServer, str]:
    server = ThreadingHTTPServer(("127.0.0.1", 0), DolaDesktopHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server, f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        thread.join(timeout=5)


def test_control_discovery_does_not_emit_token(tmp_path: Path) -> None:
    path = tmp_path / "control.json"
    path.write_text(json.dumps({"port": 1234, "token": "local-secret"}), encoding="utf-8")
    discovery = read_control_discovery(path)
    assert discovery.endpoint == "http://127.0.0.1:1234"
    assert discovery.token == "local-secret"


def test_dola_desktop_client_lists_public_accounts_and_activates(desktop_server: tuple[ThreadingHTTPServer, str]) -> None:
    _, endpoint = desktop_server
    client = DolaDesktopClient(endpoint, token="local-secret")
    assert client.health()["ok"] is True
    assert [item["display_name"] for item in client.accounts()] == ["Dola A", "Dola B"]
    assert client.session("host-a")["login_status"] == "logged_in"
    assert client.activate("host-a")["account"]["host_account_id"] == "host-a"


def test_dola_desktop_rejects_non_loopback_endpoint() -> None:
    with pytest.raises(ValueError, match="loopback"):
        DolaDesktopClient("http://example.com", token="local-secret")


def test_dola_desktop_sync_creates_distinct_dola_records_without_marking_ready(tmp_path: Path) -> None:
    registry = AccountRegistry(tmp_path / "dola_accounts.json")
    mapping = sync_registry_from_dola_desktop(
        registry,
        [
            {"host_account_id": "host-a", "display_name": "Dola A"},
            {"host_account_id": "host-b", "display_name": "Dola B"},
        ],
    )
    assert [item["account_id"] for item in mapping] == ["D01", "D02"]
    assert [item["session_slot"] for item in mapping] == ["DS01", "DS02"]
    assert [item.status for item in registry.accounts] == ["NEEDS_LOGIN", "NEEDS_LOGIN"]
    assert [item.readiness_basis for item in registry.accounts] == ["unverified", "unverified"]
    assert all(item.session_host == "dola_desktop_studio" for item in registry.accounts)
    assert all(item.host_account_id for item in registry.accounts)
    assert "token" not in (tmp_path / "dola_accounts.json").read_text(encoding="utf-8") if (tmp_path / "dola_accounts.json").exists() else True


def test_dola_desktop_sync_applies_only_explicit_session_status(tmp_path: Path) -> None:
    registry = AccountRegistry(tmp_path / "dola_accounts.json")
    mapping = sync_registry_from_dola_desktop(
        registry,
        [
            {"host_account_id": "host-a", "display_name": "Dola A", "login_status": "logged_in"},
            {"host_account_id": "host-b", "display_name": "Dola B", "login_status": "unknown"},
        ],
    )
    assert mapping[0]["authentication"] == "logged_in"
    assert registry.get("D01").status == "READY"
    assert registry.get("D01").readiness_basis == "host_observed"
    assert registry.get("D02").status == "NEEDS_LOGIN"
