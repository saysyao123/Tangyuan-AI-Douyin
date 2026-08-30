from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from app.production.models import ACCOUNT_STATUSES, AccountRecord


SENSITIVE_KEYS = {
    "password",
    "passwd",
    "cookie",
    "cookies",
    "authorization",
    "oauth",
    "oauthtoken",
    "token",
    "accesstoken",
    "refreshtoken",
    "verificationcode",
    "passkey",
    "secret",
}


def _normal_key(value: object) -> str:
    return "".join(ch for ch in str(value).lower() if ch.isalnum())


def assert_non_sensitive_registry(payload: Any) -> None:
    """Reject credential-like fields before parsing or writing a registry."""

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if _normal_key(key) in SENSITIVE_KEYS:
                    raise ValueError(f"sensitive account field is forbidden: {key}")
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(payload)


def _write_json_atomic(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_name(path.name + ".part")
    try:
        partial.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(partial, path)
    finally:
        if partial.exists():
            partial.unlink()


class AccountRegistry:
    def __init__(self, path: str | Path = "runtime/accounts/accounts.json") -> None:
        self.path = Path(path)
        self.accounts: list[AccountRecord] = []

    @classmethod
    def load(cls, path: str | Path = "runtime/accounts/accounts.json") -> "AccountRegistry":
        registry = cls(path)
        if not registry.path.exists():
            return registry
        payload = json.loads(registry.path.read_text(encoding="utf-8"))
        assert_non_sensitive_registry(payload)
        if not isinstance(payload, dict) or not isinstance(payload.get("accounts"), list):
            raise ValueError("account registry must contain an accounts list")
        registry.accounts = [AccountRecord.from_dict(item) for item in payload["accounts"]]
        registry._validate_unique()
        return registry

    def _validate_unique(self) -> None:
        account_ids = [account.account_id for account in self.accounts]
        session_slots = [account.session_slot for account in self.accounts]
        if len(account_ids) != len(set(account_ids)):
            raise ValueError("duplicate account_id in registry")
        if len(session_slots) != len(set(session_slots)):
            raise ValueError("duplicate session_slot in registry")

    def save(self) -> None:
        payload = {"accounts": [account.public_dict() for account in self.accounts]}
        assert_non_sensitive_registry(payload)
        self._validate_unique()
        _write_json_atomic(self.path, payload)

    def add(
        self,
        account_id: str,
        *,
        display_name: str | None = None,
        session_slot: str | None = None,
        status: str = "NEEDS_LOGIN",
        session_host: str = "external_slot",
        host_account_id: str | None = None,
        readiness_basis: str = "unverified",
    ) -> AccountRecord:
        if any(item.account_id == account_id for item in self.accounts):
            raise ValueError(f"account already exists: {account_id}")
        if status not in ACCOUNT_STATUSES:
            raise ValueError(f"unsupported account status: {status}")
        slot = session_slot or self._default_slot(account_id)
        account = AccountRecord(
            account_id=account_id,
            display_name=display_name or account_id,
            session_slot=slot,
            status=status,
            session_host=session_host,
            host_account_id=host_account_id,
            readiness_basis=readiness_basis,
        )
        self.accounts.append(account)
        self._validate_unique()
        return account

    def _default_slot(self, account_id: str) -> str:
        digits = "".join(ch for ch in account_id if ch.isdigit())
        return f"S{int(digits):02d}" if digits else f"S{len(self.accounts) + 1:02d}"

    def get(self, account_id: str) -> AccountRecord:
        for account in self.accounts:
            if account.account_id == account_id:
                return account
        raise KeyError(account_id)

    def find_by_host_account_id(
        self,
        host_account_id: str,
        *,
        session_host: str | None = None,
    ) -> AccountRecord | None:
        target = str(host_account_id or "").strip()
        if not target:
            return None
        for account in self.accounts:
            if account.host_account_id != target:
                continue
            if session_host is not None and account.session_host != session_host:
                continue
            return account
        return None

    def set_status(self, account_id: str, status: str, *, error: str = "") -> AccountRecord:
        if status not in ACCOUNT_STATUSES:
            raise ValueError(f"unsupported account status: {status}")
        account = self.get(account_id)
        account.status = status
        if error:
            account.last_error = error[:500]
        elif status in {"READY", "NEEDS_LOGIN", "BUSY"}:
            account.last_error = ""
        return account

    def ready(self) -> list[AccountRecord]:
        return [account for account in self.accounts if account.enabled and account.status == "READY"]

    def dashboard(self) -> list[dict[str, Any]]:
        return [
            {
                "account_id": account.account_id,
                "display_name": account.display_name,
                "status": account.status,
                "session_slot": account.session_slot,
                "session_host": account.session_host,
                "host_account_id": account.host_account_id,
                "readiness_basis": account.readiness_basis,
                "success_count": account.success_count,
                "failure_count": account.failure_count,
                "last_used_at": account.last_used_at,
            }
            for account in self.accounts
        ]
