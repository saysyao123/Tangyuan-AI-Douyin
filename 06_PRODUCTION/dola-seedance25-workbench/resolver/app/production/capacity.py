from __future__ import annotations

from typing import Any


def capacity_observation(account: dict[str, Any], *, target_duration: float = 5.0) -> dict[str, Any]:
    """Report observable quota facts without turning stale/local counters into capacity."""

    quota = account.get("quota") if isinstance(account.get("quota"), dict) else {}
    provider_remaining = quota.get("provider_remaining")
    provider_source = quota.get("provider_source") or ""
    provider_stale = bool(quota.get("provider_stale"))
    provider_verified = isinstance(provider_remaining, (int, float)) and not provider_stale and bool(provider_source)
    return {
        "account_id": account.get("id") or account.get("account_id"),
        "target_duration": target_duration,
        "local_remaining_observed": quota.get("local_remaining"),
        "provider_remaining_observed": provider_remaining,
        "provider_quota_state": "verified" if provider_verified else "unverified",
        "capacity_known": False,
        "max_jobs": None,
        "reason": "A 5-second job cost and provider quota must be confirmed by a real provider response; local counters are not proof.",
    }
