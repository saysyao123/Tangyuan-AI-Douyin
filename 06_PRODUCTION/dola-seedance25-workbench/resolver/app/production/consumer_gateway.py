from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from app.production.account_registry import AccountRegistry


class ConsumerGatewayError(RuntimeError):
    """Local consumer-gateway integration error without credential disclosure."""


def validate_gateway_endpoint(endpoint: str) -> str:
    value = str(endpoint or "").strip().rstrip("/")
    parsed = urllib.parse.urlparse(value)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("gateway endpoint must use http or https")
    if parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("gateway endpoint must be loopback")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("gateway endpoint must not contain credentials or query data")
    if parsed.path not in {"", "/"}:
        raise ValueError("gateway endpoint must not contain a path")
    return value


def public_gateway_account(payload: dict[str, Any]) -> dict[str, Any]:
    runtime = payload.get("runtime") if isinstance(payload.get("runtime"), dict) else {}
    quota = payload.get("quota_status") if isinstance(payload.get("quota_status"), dict) else {}
    video_quota = quota.get("video") if isinstance(quota.get("video"), dict) else {}
    return {
        "host_account_id": str(payload.get("id") or "").strip(),
        "display_name": str(payload.get("name") or payload.get("id") or "").strip(),
        "host_status": str(payload.get("status") or "unknown").strip(),
        "runtime_ready": bool(runtime.get("ready")),
        "runtime_hot": bool(runtime.get("hot")),
        "needs_captcha": bool(runtime.get("needs_captcha")),
        "video_remaining_local": video_quota.get("remaining"),
        "video_limit_local": video_quota.get("limit"),
    }


class ConsumerGatewayClient:
    def __init__(
        self,
        endpoint: str = "http://127.0.0.1:19090",
        *,
        timeout: float = 20.0,
    ) -> None:
        self.endpoint = validate_gateway_endpoint(endpoint)
        self.timeout = timeout

    def _request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        data = None
        headers = {"Accept": "application/json"}
        if payload is not None:
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(f"{self.endpoint}{path}", data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = response.read(32 * 1024 * 1024 + 1)
                if len(body) > 32 * 1024 * 1024:
                    raise ConsumerGatewayError("gateway response too large")
                result = json.loads(body.decode("utf-8"))
        except urllib.error.HTTPError as exc:
            raise ConsumerGatewayError(f"gateway http error {exc.code}") from None
        except (urllib.error.URLError, TimeoutError, OSError):
            raise ConsumerGatewayError("consumer gateway unavailable") from None
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ConsumerGatewayError(f"gateway returned invalid json: {type(exc).__name__}") from None
        if not isinstance(result, dict):
            raise ConsumerGatewayError("gateway response must be an object")
        return result

    @staticmethod
    def _quote(value: str) -> str:
        return urllib.parse.quote(str(value), safe="")

    def health(self) -> dict[str, Any]:
        payload = self._request("GET", "/health")
        return {
            "status": payload.get("status"),
            "logged_in": payload.get("logged_in"),
            "accounts": payload.get("accounts"),
            "video_tasks": payload.get("video_tasks"),
        }

    def accounts(self) -> list[dict[str, Any]]:
        payload = self._request("GET", "/admin/api/accounts")
        rows = payload.get("accounts")
        if not isinstance(rows, list):
            raise ConsumerGatewayError("gateway accounts response is invalid")
        return [public_gateway_account(item) for item in rows if isinstance(item, dict)]

    def status(self, host_account_id: str) -> dict[str, Any]:
        payload = self._request("GET", f"/admin/api/accounts/{self._quote(host_account_id)}/status")
        return {
            "account_id": str(payload.get("account_id") or host_account_id),
            "logged_in": payload.get("logged_in"),
            "browser": payload.get("browser"),
            "ready": payload.get("ready"),
            "status": payload.get("status"),
        }

    def start(self, host_account_id: str) -> dict[str, Any]:
        payload = self._request("POST", f"/admin/api/accounts/{self._quote(host_account_id)}/start")
        account = payload.get("account") if isinstance(payload.get("account"), dict) else {}
        return {"status": payload.get("status"), "account": public_gateway_account(account)}

    def stop(self, host_account_id: str) -> dict[str, Any]:
        return self._request("POST", f"/admin/api/accounts/{self._quote(host_account_id)}/stop")

    def probe(self, host_account_id: str) -> dict[str, Any]:
        payload = self._request("POST", f"/admin/api/accounts/{self._quote(host_account_id)}/probe")
        return {
            "status": payload.get("status"),
            "account_id": payload.get("account_id") or host_account_id,
            "ms": payload.get("ms"),
            "response_present": bool(payload.get("response")),
            "message": str(payload.get("message") or "")[:300],
        }


def sync_registry_from_consumer_gateway(
    registry: AccountRegistry,
    host_accounts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Bind public gateway IDs to local slots; never import browser state."""

    used_ids = {account.account_id for account in registry.accounts}
    results: list[dict[str, Any]] = []
    for host in host_accounts:
        host_id = str(host.get("host_account_id") or "").strip()
        if not host_id:
            continue
        account = registry.find_by_host_account_id(host_id, session_host="consumer_gateway")
        if account is None:
            reusable = next(
                (
                    item
                    for item in registry.accounts
                    if item.session_host == "external_slot"
                    and item.host_account_id is None
                    and item.status == "NEEDS_LOGIN"
                    and item.account_id not in {value["account_id"] for value in results}
                ),
                None,
            )
            if reusable is not None:
                account = reusable
                account.session_host = "consumer_gateway"
                account.host_account_id = host_id
            else:
                index = 1
                while f"A{index:02d}" in used_ids:
                    index += 1
                account = registry.add(
                    f"A{index:02d}",
                    display_name=str(host.get("display_name") or f"Doubao-{index:02d}"),
                    session_host="consumer_gateway",
                    host_account_id=host_id,
                    status="NEEDS_LOGIN",
                )
                used_ids.add(account.account_id)
        if host.get("display_name"):
            account.display_name = str(host["display_name"]).strip() or account.display_name
        remote_ready = bool(host.get("runtime_ready")) and not bool(host.get("needs_captcha"))
        if remote_ready:
            account.status = "READY"
        elif account.status == "READY":
            account.status = "NEEDS_LOGIN"
        results.append(
            {
                "account_id": account.account_id,
                "session_slot": account.session_slot,
                "session_host": account.session_host,
                "host_account_id": host_id,
                "host_status": host.get("host_status") or "unknown",
                "runtime_ready": remote_ready,
                "video_remaining_local": host.get("video_remaining_local"),
            }
        )
    return results
