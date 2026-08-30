from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, ClassVar


ACCOUNT_STATUSES = {"DISABLED", "NEEDS_LOGIN", "READY", "BUSY", "COOLDOWN", "ERROR"}
READINESS_BASES = {"unverified", "host_observed", "user_confirmed"}
JOB_TERMINAL_STATUSES = {
    "PASS",
    "FAIL_ACCOUNT",
    "FAIL_SESSION",
    "FAIL_CAPTURE",
    "FAIL_GENERATION",
    "FAIL_IDENTITY",
    "FAIL_RESOLVE",
    "FAIL_DOWNLOAD",
    "FAIL_FFPROBE",
    "FAIL_WATERMARK_QA",
    "FAIL_DURATION",
    "FAIL_TIMEOUT",
    "FAIL_IDENTITY_MISMATCH",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def prompt_sha256(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


@dataclass(slots=True)
class AccountRecord:
    account_id: str
    display_name: str
    enabled: bool = True
    status: str = "NEEDS_LOGIN"
    session_slot: str = ""
    session_host: str = "external_slot"
    host_account_id: str | None = None
    readiness_basis: str = "unverified"
    last_used_at: str | None = None
    last_success_at: str | None = None
    last_failure_at: str | None = None
    success_count: int = 0
    failure_count: int = 0
    last_error: str = ""

    def __post_init__(self) -> None:
        self.account_id = self.account_id.strip()
        self.display_name = self.display_name.strip()
        self.session_slot = self.session_slot.strip()
        self.session_host = self.session_host.strip() or "external_slot"
        if self.host_account_id is not None:
            self.host_account_id = self.host_account_id.strip() or None
        self.readiness_basis = self.readiness_basis.strip() or "unverified"
        if not self.account_id or not self.display_name or not self.session_slot:
            raise ValueError("account_id, display_name and session_slot are required")
        if self.status not in ACCOUNT_STATUSES:
            raise ValueError(f"unsupported account status: {self.status}")
        if self.readiness_basis not in READINESS_BASES:
            raise ValueError(f"unsupported readiness basis: {self.readiness_basis}")

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "AccountRecord":
        allowed = {field for field in cls.__dataclass_fields__}
        unknown = set(payload) - allowed
        if unknown:
            raise ValueError(f"account registry contains unsupported fields: {sorted(unknown)}")
        return cls(**{key: value for key, value in payload.items() if key in allowed})

    def public_dict(self) -> dict[str, Any]:
        return asdict(self)

    def mark_used(self) -> None:
        self.last_used_at = utc_now()

    def mark_success(self) -> None:
        self.status = "READY"
        self.last_success_at = utc_now()
        self.success_count += 1
        self.last_error = ""

    def mark_failure(self, error: str, *, status: str = "ERROR") -> None:
        if status not in ACCOUNT_STATUSES:
            raise ValueError(f"unsupported account status: {status}")
        self.status = status
        self.last_failure_at = utc_now()
        self.failure_count += 1
        self.last_error = error[:500]


@dataclass(slots=True)
class JobRecord:
    job_id: str
    prompt_hash: str
    target_duration: float = 5.0
    account_id: str | None = None
    session_slot: str | None = None
    status: str = "CREATED"
    created_at: str = ""
    started_at: str | None = None
    completed_at: str | None = None
    conversation_id: str | None = None
    message_id: str | None = None
    task_id: str | None = None
    vid: str | None = None
    fallback_api_found: bool = False
    clean_candidate_found: bool = False
    downloaded: bool = False
    qa_passed: bool = False
    failure_code: str | None = None

    _TRANSITIONS: ClassVar[dict[str, set[str]]] = {
        "CREATED": {"ACCOUNT_ASSIGNED", "FAIL_ACCOUNT"},
        "ACCOUNT_ASSIGNED": {"SESSION_READY", "FAIL_SESSION"},
        "SESSION_READY": {"CAPTURE_ARMED", "FAIL_SESSION"},
        "CAPTURE_ARMED": {"GENERATION_SUBMITTED", "FAIL_CAPTURE"},
        "GENERATION_SUBMITTED": {"GENERATION_RUNNING", "FAIL_GENERATION", "FAIL_TIMEOUT"},
        "GENERATION_RUNNING": {"GENERATION_COMPLETED", "FAIL_GENERATION", "FAIL_TIMEOUT"},
        "GENERATION_COMPLETED": {"IDENTITY_FOUND", "FAIL_IDENTITY"},
        "IDENTITY_FOUND": {"RESOLVING", "FAIL_RESOLVE", "FAIL_IDENTITY_MISMATCH"},
        "RESOLVING": {"CLEAN_CANDIDATE_FOUND", "FAIL_RESOLVE"},
        "CLEAN_CANDIDATE_FOUND": {"DOWNLOADING", "FAIL_DOWNLOAD"},
        "DOWNLOADING": {"DOWNLOADED", "FAIL_DOWNLOAD"},
        "DOWNLOADED": {"QA_RUNNING", "FAIL_FFPROBE"},
        "QA_RUNNING": {"PASS", "FAIL_WATERMARK_QA", "FAIL_DURATION", "FAIL_FFPROBE"},
    }

    def __post_init__(self) -> None:
        if not self.created_at:
            self.created_at = utc_now()
        if self.target_duration <= 0:
            raise ValueError("target_duration must be positive")

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "JobRecord":
        allowed = {field for field in cls.__dataclass_fields__}
        unknown = set(payload) - allowed
        if unknown:
            raise ValueError(f"job record contains unsupported fields: {sorted(unknown)}")
        return cls(**{key: value for key, value in payload.items() if key in allowed})

    def public_dict(self) -> dict[str, Any]:
        return asdict(self)

    def bind_account(self, account: AccountRecord) -> None:
        if self.account_id is not None and (
            self.account_id != account.account_id or self.session_slot != account.session_slot
        ):
            raise ValueError("job account binding is sticky and cannot be changed")
        self.account_id = account.account_id
        self.session_slot = account.session_slot

    def assert_binding(self, account_id: str, session_slot: str) -> None:
        if self.account_id != account_id or self.session_slot != session_slot:
            raise ValueError("account/session binding mismatch")

    def transition(self, next_status: str) -> None:
        if self.status in JOB_TERMINAL_STATUSES:
            raise ValueError(f"terminal job cannot transition: {self.status}")
        allowed = self._TRANSITIONS.get(self.status, set())
        if next_status not in allowed:
            raise ValueError(f"invalid job transition {self.status} -> {next_status}")
        self.status = next_status
        if next_status in {"ACCOUNT_ASSIGNED", "SESSION_READY", "CAPTURE_ARMED", "GENERATION_SUBMITTED"}:
            self.started_at = self.started_at or utc_now()
        if next_status in JOB_TERMINAL_STATUSES:
            self.completed_at = utc_now()
            if next_status != "PASS":
                self.failure_code = next_status
