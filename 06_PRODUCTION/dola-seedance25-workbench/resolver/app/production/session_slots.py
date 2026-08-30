from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ACCOUNT_PATTERN = re.compile(r"^A(?P<number>[0-9]{2})$")


@dataclass(frozen=True, slots=True)
class SessionSlotConfig:
    account_id: str
    session_slot: str
    port: int
    profile_dir: Path

    @property
    def endpoint(self) -> str:
        return f"http://127.0.0.1:{self.port}"


def session_slot_for(account_id: str, *, project_root: str | Path = ".", base_port: int = 9330) -> SessionSlotConfig:
    match = ACCOUNT_PATTERN.fullmatch(account_id.strip().upper())
    if not match:
        raise ValueError("account_id must use the A01/A02 format")
    number = int(match.group("number"))
    if number <= 0:
        raise ValueError("account_id number must be greater than zero")
    root = Path(project_root).resolve()
    return SessionSlotConfig(
        account_id=f"A{number:02d}",
        session_slot=f"S{number:02d}",
        port=base_port + number,
        profile_dir=root / "runtime" / "dola-accounts" / f"A{number:02d}",
    )


def safe_slot_manifest(account_ids: list[str], *, project_root: str | Path = ".") -> list[dict[str, str | int]]:
    """Return launcher metadata without cookies, profile contents, or credentials."""

    return [
        {
            "account_id": config.account_id,
            "session_slot": config.session_slot,
            "port": config.port,
            "profile_dir": str(config.profile_dir),
            "endpoint": config.endpoint,
        }
        for config in (session_slot_for(account_id, project_root=project_root) for account_id in account_ids)
    ]
