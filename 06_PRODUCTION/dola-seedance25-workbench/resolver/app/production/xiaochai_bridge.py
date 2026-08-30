from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from app.production.account_registry import AccountRegistry
from app.production.models import AccountRecord


class XiaochaiBridgeError(RuntimeError):
    """A safe, local-only bridge failure without exposing response secrets."""


def validate_bridge_endpoint(endpoint: str) -> str:
    value = str(endpoint or "").strip().rstrip("/")
    parsed = urllib.parse.urlparse(value)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("bridge endpoint must use http or https")
    if parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("bridge endpoint must be loopback")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("bridge endpoint must not contain credentials or query data")
    if parsed.path not in {"", "/"}:
        raise ValueError("bridge endpoint must not contain a path")
    return value


class XiaochaiBridgeClient:
    def __init__(
        self,
        endpoint: str = "http://127.0.0.1:8766",
        *,
        token: str | None = None,
        timeout: float = 20.0,
    ) -> None:
        self.endpoint = validate_bridge_endpoint(endpoint)
        self.token = token or os.environ.get("XIAOCHAI_DOLA_BRIDGE_TOKEN")
        self.timeout = timeout

    def _request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.endpoint}{path}"
        data = None
        headers = {"Accept": "application/json"}
        if self.token:
            headers["X-Xiaochai-Bridge-Token"] = self.token
        if payload is not None:
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = response.read(32 * 1024 * 1024 + 1)
                if len(body) > 32 * 1024 * 1024:
                    raise XiaochaiBridgeError("bridge response too large")
                parsed = json.loads(body.decode("utf-8"))
        except urllib.error.HTTPError as exc:
            raise XiaochaiBridgeError(f"bridge http error {exc.code}") from None
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise XiaochaiBridgeError(f"bridge unavailable: {type(exc).__name__}") from None
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise XiaochaiBridgeError(f"bridge returned invalid json: {type(exc).__name__}") from None
        if not isinstance(parsed, dict):
            raise XiaochaiBridgeError("bridge response must be an object")
        if parsed.get("ok") is False:
            raise XiaochaiBridgeError(str(parsed.get("error_code") or "bridge request failed"))
        return parsed

    @staticmethod
    def _quoted(value: str) -> str:
        return urllib.parse.quote(str(value), safe="")

    def health(self) -> dict[str, Any]:
        return self._request("GET", "/v1/health")

    def accounts(self) -> list[dict[str, Any]]:
        payload = self._request("GET", "/v1/accounts")
        accounts = payload.get("accounts")
        if not isinstance(accounts, list):
            raise XiaochaiBridgeError("bridge accounts response is invalid")
        return [item for item in accounts if isinstance(item, dict)]

    def session(self, host_account_id: str) -> dict[str, Any]:
        return self._request("GET", f"/v1/accounts/{self._quoted(host_account_id)}/session")

    def activate(self, host_account_id: str) -> dict[str, Any]:
        return self._request("POST", f"/v1/accounts/{self._quoted(host_account_id)}/activate")

    def capture_latest(self, host_account_id: str, *, limit: int = 1) -> list[dict[str, Any]]:
        safe_limit = max(1, min(int(limit), 10))
        payload = self._request(
            "GET",
            f"/v1/accounts/{self._quoted(host_account_id)}/capture/latest?limit={safe_limit}",
        )
        entries = payload.get("captures")
        if not isinstance(entries, list):
            raise XiaochaiBridgeError("bridge capture response is invalid")
        return [item for item in entries if isinstance(item, dict)]

    def download(self, host_account_id: str, url: str, filename: str) -> dict[str, Any]:
        return self._request(
            "POST",
            f"/v1/accounts/{self._quoted(host_account_id)}/download",
            {"url": url, "filename": filename},
        )


def sync_registry_from_xiaochai(
    registry: AccountRegistry,
    host_accounts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    used_ids = {account.account_id for account in registry.accounts}
    results: list[dict[str, Any]] = []
    for host in host_accounts:
        host_id = str(host.get("host_account_id") or host.get("id") or "").strip()
        if not host_id:
            continue
        account = registry.find_by_host_account_id(host_id, session_host="xiaochai")
        if account is None:
            index = 1
            while f"A{index:02d}" in used_ids:
                index += 1
            account = registry.add(
                f"A{index:02d}",
                display_name=str(host.get("profile_name") or host.get("display_name") or f"Xiaochai-{index:02d}"),
                session_host="xiaochai",
                host_account_id=host_id,
                status="NEEDS_LOGIN",
            )
            used_ids.add(account.account_id)
        else:
            account.display_name = str(host.get("profile_name") or host.get("display_name") or account.display_name).strip()
        results.append(
            {
                "account_id": account.account_id,
                "session_slot": account.session_slot,
                "host_account_id": host_id,
                "host_auth_status": str(host.get("auth_status") or "unknown"),
            }
        )
    return results


def latest_capture_body(
    client: XiaochaiBridgeClient,
    account: AccountRecord,
) -> tuple[str, dict[str, Any]]:
    if account.session_host != "xiaochai" or not account.host_account_id:
        raise XiaochaiBridgeError("account is not bound to Xiaochai session host")
    entries = client.capture_latest(account.host_account_id, limit=1)
    if not entries:
        raise XiaochaiBridgeError("no captured Dola response")
    entry = entries[0]
    body = entry.get("body")
    if not isinstance(body, str) or not body.strip():
        raise XiaochaiBridgeError("latest capture has no body")
    return body, entry


def write_capture_body(body: str, output: str | Path) -> Path:
    destination = Path(output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(body, encoding="utf-8")
    return destination
