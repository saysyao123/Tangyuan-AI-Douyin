from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.production.account_registry import AccountRegistry


class DolaDesktopError(RuntimeError):
    """Safe local Dola Desktop control-plane failure."""


def default_control_path() -> Path:
    base = (
        os.environ.get("SEEDANCE_STUDIO_CONTROL_DIR")
        or os.environ.get("LOCALAPPDATA")
        or os.environ.get("APPDATA")
        or (Path.home() / ".seedance-desktop-studio")
    )
    return Path(base) / "SeedanceDesktopStudio" / "control.json"


def _validate_loopback_host(host: str | None) -> None:
    if host not in {"127.0.0.1", "localhost", "::1"}:
        raise DolaDesktopError("Dola Desktop control plane must be loopback-only")


@dataclass(frozen=True, slots=True)
class ControlDiscovery:
    endpoint: str
    token: str


def read_control_discovery(path: str | Path | None = None) -> ControlDiscovery:
    discovery_path = Path(path) if path is not None else default_control_path()
    try:
        payload = json.loads(discovery_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise DolaDesktopError("Dola Desktop Studio is not running or its control file is unavailable") from None
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        raise DolaDesktopError("Dola Desktop Studio control file is invalid") from None
    if not isinstance(payload, dict):
        raise DolaDesktopError("Dola Desktop control discovery must be an object")
    try:
        port = int(payload.get("port"))
    except (TypeError, ValueError):
        raise DolaDesktopError("Dola Desktop control discovery has no valid port") from None
    if not 1 <= port <= 65535:
        raise DolaDesktopError("Dola Desktop control discovery port is out of range")
    token = str(payload.get("token") or "").strip()
    if not token:
        raise DolaDesktopError("Dola Desktop control discovery has no control token")
    endpoint = f"http://127.0.0.1:{port}"
    return ControlDiscovery(endpoint=endpoint, token=token)


def public_dola_account(payload: dict[str, Any]) -> dict[str, Any]:
    host_id = str(payload.get("id") or "").strip()
    name = str(payload.get("name") or host_id or "Dola account").strip()
    if not host_id:
        return {}
    return {
        "host_account_id": host_id,
        "display_name": name[:80] or "Dola account",
        "partition": str(payload.get("partition") or "").strip(),
        "created_at": payload.get("createdAt"),
    }


class DolaDesktopClient:
    """Client for the user's local Dola Desktop control plane.

    The control token is consumed only in memory for loopback authentication.
    It is never included in returned payloads, logs, or registry records.
    """

    def __init__(
        self,
        endpoint: str | None = None,
        *,
        token: str | None = None,
        control_path: str | Path | None = None,
        timeout: float = 10.0,
    ) -> None:
        if endpoint is None or token is None:
            discovery = read_control_discovery(control_path)
            endpoint = endpoint or discovery.endpoint
            token = token or discovery.token
        value = str(endpoint or "").strip().rstrip("/")
        parsed = urllib.parse.urlparse(value)
        if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
            raise ValueError("Dola Desktop endpoint must be an http loopback URL")
        if parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path not in {"", "/"}:
            raise ValueError("Dola Desktop endpoint must not contain credentials, query data, or a path")
        if not str(token or "").strip():
            raise ValueError("Dola Desktop control token is required")
        self.endpoint = value
        self._token = str(token).strip()
        self.timeout = timeout

    def _request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        data = None
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self._token}",
        }
        if payload is not None:
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(f"{self.endpoint}{path}", data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = response.read(2 * 1024 * 1024 + 1)
                if len(body) > 2 * 1024 * 1024:
                    raise DolaDesktopError("Dola Desktop response too large")
                parsed = json.loads(body.decode("utf-8"))
        except urllib.error.HTTPError as exc:
            raise DolaDesktopError(f"Dola Desktop control http error {exc.code}") from None
        except (urllib.error.URLError, TimeoutError, OSError):
            raise DolaDesktopError("Dola Desktop control plane unavailable") from None
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise DolaDesktopError("Dola Desktop control returned invalid json") from None
        if not isinstance(parsed, dict):
            raise DolaDesktopError("Dola Desktop control response must be an object")
        return parsed

    @staticmethod
    def _quote(value: str) -> str:
        return urllib.parse.quote(str(value), safe="")

    def health(self) -> dict[str, Any]:
        payload = self._request("GET", "/health")
        return {
            "ok": payload.get("ok"),
            "service": payload.get("service"),
            "version": payload.get("version"),
            "pid": payload.get("pid"),
            "gates": payload.get("gates") if isinstance(payload.get("gates"), dict) else {},
        }

    def accounts(self) -> list[dict[str, Any]]:
        payload = self._request("GET", "/v1/accounts")
        rows = payload.get("accounts")
        if not isinstance(rows, list):
            raise DolaDesktopError("Dola Desktop accounts response is invalid")
        return [item for item in (public_dola_account(row) for row in rows if isinstance(row, dict)) if item]

    def activate(self, host_account_id: str) -> dict[str, Any]:
        payload = self._request(
            "POST",
            f"/v1/accounts/{self._quote(host_account_id)}/activate",
            {},
        )
        account = payload.get("account") if isinstance(payload.get("account"), dict) else {}
        return {"account": public_dola_account(account)}

    def session(self, host_account_id: str) -> dict[str, Any]:
        payload = self._request(
            "GET",
            f"/v1/accounts/{self._quote(host_account_id)}/session",
        )
        session = payload.get("session") if isinstance(payload.get("session"), dict) else {}
        login_status = str(session.get("loginStatus") or "unknown")
        if login_status not in {"logged_in", "logged_out", "unknown"}:
            login_status = "unknown"
        return {
            "host_account_id": host_account_id,
            "login_status": login_status,
            "page_loaded": session.get("pageLoaded") is True,
            "evidence": str(session.get("evidence") or "unknown")[:80],
            "page_path": str(session.get("pagePath") or "")[:500],
            "checked_at": session.get("checkedAt"),
        }


def sync_registry_from_dola_desktop(
    registry: AccountRegistry,
    host_accounts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Bind Dola Desktop's public account IDs to isolated local Dola records.

    Syncing account metadata never proves authentication. New or unchanged
    records therefore remain NEEDS_LOGIN until a separate session check or
    explicit user verification marks them READY.
    """

    used_ids = {account.account_id for account in registry.accounts}
    results: list[dict[str, Any]] = []
    for host in host_accounts:
        host_id = str(host.get("host_account_id") or "").strip()
        if not host_id:
            continue
        account = registry.find_by_host_account_id(host_id, session_host="dola_desktop_studio")
        if account is None:
            index = 1
            while f"D{index:02d}" in used_ids:
                index += 1
            account = registry.add(
                f"D{index:02d}",
                display_name=str(host.get("display_name") or f"Dola-{index:02d}"),
                session_slot=f"DS{index:02d}",
                session_host="dola_desktop_studio",
                host_account_id=host_id,
                status="NEEDS_LOGIN",
                readiness_basis="unverified",
            )
            used_ids.add(account.account_id)
        if host.get("display_name"):
            account.display_name = str(host["display_name"]).strip() or account.display_name
        login_status = str(host.get("login_status") or "unknown")
        if login_status == "logged_in":
            account.status = "READY"
            account.readiness_basis = "host_observed"
        elif login_status == "logged_out":
            account.status = "NEEDS_LOGIN"
            account.readiness_basis = "host_observed"
        results.append(
            {
                "account_id": account.account_id,
                "display_name": account.display_name,
                "session_slot": account.session_slot,
                "session_host": account.session_host,
                "host_account_id": host_id,
                "status": account.status,
                "authentication": login_status,
            }
        )
    registry._validate_unique()
    return results
