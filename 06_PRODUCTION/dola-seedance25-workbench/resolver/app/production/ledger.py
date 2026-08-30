from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from app.logger import redact_url


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_value(key: str, value: Any) -> Any:
    normalized = "".join(ch for ch in key.lower() if ch.isalnum())
    if normalized in {"keyseed", "authorization", "cookie", "token", "password", "secret"}:
        return "<REDACTED>"
    if normalized in {"url", "mainurl", "fallbackapi", "downloadurl", "playurl"} and isinstance(value, str):
        return redact_url(value)
    if isinstance(value, str):
        return value[:500]
    if isinstance(value, (int, float, bool)) or value is None:
        return value
    return "<PRESENT>"


class JsonlLedger:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def append(self, event: str, payload: dict[str, Any]) -> dict[str, Any]:
        safe = {"ts": _now(), "event": event}
        safe.update({key: _safe_value(key, value) for key, value in payload.items()})
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(safe, ensure_ascii=False, separators=(",", ":")) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        return safe


class DurableCaptureSink:
    """Append identity facts as soon as they are observed.

    Raw response bodies and signed URLs are intentionally not persisted here;
    the existing generation bundle can store separately redacted evidence.
    """

    def __init__(self, path: str | Path = "runtime/events.jsonl") -> None:
        self.ledger = JsonlLedger(path)

    def append_identity_event(
        self,
        *,
        event: str,
        account_id: str,
        session_slot: str,
        job_id: str,
        identity: dict[str, Any],
    ) -> dict[str, Any]:
        if not account_id or not session_slot or not job_id:
            raise ValueError("account_id, session_slot and job_id are required")
        video_list = identity.get("video_list")
        payload = {
            "account_id": account_id,
            "session_slot": session_slot,
            "job_id": job_id,
            "conversation_id": identity.get("conversation_id"),
            "message_id": identity.get("message_id"),
            "task_id": identity.get("task_id"),
            "vid": identity.get("vid"),
            "fallback_api": identity.get("fallback_api"),
            "key_seed_found": bool(identity.get("key_seed")),
            "video_list_count": len(video_list) if isinstance(video_list, list) else int(bool(video_list)),
            "source": identity.get("source", "generation_capture"),
        }
        return self.ledger.append(event, payload)


class AccountJobLedgers:
    def __init__(self, root: str | Path = "runtime") -> None:
        root_path = Path(root)
        self.account = JsonlLedger(root_path / "accounts" / "account-ledger.jsonl")
        self.job = JsonlLedger(root_path / "jobs" / "job-ledger.jsonl")

    def append_account_event(self, event: str, **payload: Any) -> dict[str, Any]:
        return self.account.append(event, payload)

    def append_job_event(self, event: str, **payload: Any) -> dict[str, Any]:
        return self.job.append(event, payload)
