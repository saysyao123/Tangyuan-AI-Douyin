from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.production.account_registry import AccountRegistry, assert_non_sensitive_registry
from app.production.capacity import capacity_observation
from app.production.job_store import JobStore
from app.production.ledger import DurableCaptureSink
from app.production.models import JobRecord, prompt_sha256
from app.production.scheduler import HealthAwareRoundRobin, NoReadyAccount
from app.qa.production_gate import evaluate_5s_gate


def make_registry(tmp_path: Path, statuses: tuple[str, ...] = ("READY", "READY", "READY")) -> AccountRegistry:
    registry = AccountRegistry(tmp_path / "accounts.json")
    for index, status in enumerate(statuses, 1):
        registry.add(f"A{index:02d}", display_name=f"Dola-{index:02d}", status=status)
    registry.save()
    return AccountRegistry.load(registry.path)


def test_registry_has_unique_slots_and_rejects_credentials(tmp_path: Path) -> None:
    registry = make_registry(tmp_path)
    assert [account.session_slot for account in registry.accounts] == ["S01", "S02", "S03"]
    with pytest.raises(ValueError, match="sensitive"):
        assert_non_sensitive_registry({"accounts": [{"account_id": "A01", "cookie": "secret"}]})


def test_health_aware_round_robin_skips_unready_accounts(tmp_path: Path) -> None:
    registry = make_registry(tmp_path, ("READY", "NEEDS_LOGIN", "READY"))
    scheduler = HealthAwareRoundRobin(registry)
    assignments = scheduler.simulate(5)
    assert [item["account_id"] for item in assignments] == ["A01", "A03", "A01", "A03", "A01"]


def test_scheduler_sticky_binding_and_no_ready_fail_closed(tmp_path: Path) -> None:
    registry = make_registry(tmp_path, ("READY", "READY"))
    scheduler = HealthAwareRoundRobin(registry)
    job = JobRecord("job-1", prompt_sha256("x"))
    account = scheduler.bind_job(job)
    assert job.account_id == account.account_id
    with pytest.raises(ValueError, match="sticky"):
        job.bind_account(registry.get("A02"))
    scheduler.release(account.account_id)

    empty = make_registry(tmp_path / "empty", ("NEEDS_LOGIN", "ERROR"))
    with pytest.raises(NoReadyAccount):
        HealthAwareRoundRobin(empty).reserve_next()


def test_durable_capture_appends_safe_identity_immediately(tmp_path: Path) -> None:
    sink = DurableCaptureSink(tmp_path / "events.jsonl")
    sink.append_identity_event(
        event="IDENTITY_FOUND",
        account_id="A02",
        session_slot="S02",
        job_id="job-2",
        identity={
            "conversation_id": "conv-2",
            "message_id": "msg-2",
            "vid": "v186abc123456789012345678",
            "fallback_api": "https://dola.example/api?token=secret",
            "key_seed": "do-not-write",
            "video_list": [{"main_url": "https://cdn.example/a.mp4?sig=secret"}],
        },
    )
    rows = [json.loads(line) for line in (tmp_path / "events.jsonl").read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 1
    row = rows[0]
    assert row["account_id"] == "A02"
    assert row["session_slot"] == "S02"
    assert row["job_id"] == "job-2"
    assert row["key_seed_found"] is True
    assert "secret" not in json.dumps(row)


def test_job_store_resume_preserves_binding(tmp_path: Path) -> None:
    store = JobStore(tmp_path / "jobs")
    job = store.create(JobRecord("job-3", prompt_sha256("prompt")))
    job.bind_account(make_registry(tmp_path / "registry").get("A01"))
    store.transition(job, "ACCOUNT_ASSIGNED")
    loaded = store.load("job-3")
    assert loaded.account_id == "A01"
    assert loaded.session_slot == "S01"
    assert loaded.status == "ACCOUNT_ASSIGNED"


@pytest.mark.parametrize(
    ("duration", "expected"),
    [(5.05, "PASS"), (4.0, "PASS"), (6.5, "PASS"), (10.08, "FAIL"), (3.9, "FAIL")],
)
def test_5s_gate_is_file_level(duration: float, expected: str) -> None:
    report = evaluate_5s_gate(
        {"duration": duration, "width": 1280, "height": 720},
        visible_watermark="NO",
    )
    assert report["status"] == expected


def test_5s_gate_rejects_unknown_watermark_or_small_media() -> None:
    report = evaluate_5s_gate(
        {"duration": 5.0, "width": 720, "height": 1280},
        visible_watermark="UNVERIFIED",
    )
    assert report["status"] == "FAIL"
    assert "FAIL_RESOLUTION" in report["failure_codes"]
    assert "FAIL_WATERMARK_QA" in report["failure_codes"]


def test_capacity_does_not_claim_from_local_counter() -> None:
    result = capacity_observation(
        {
            "id": "account-04",
            "quota": {"local_remaining": 10, "provider_remaining": None, "provider_source": ""},
        }
    )
    assert result["local_remaining_observed"] == 10
    assert result["capacity_known"] is False
    assert result["max_jobs"] is None
    assert result["provider_quota_state"] == "unverified"
