from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from app.production.ledger import AccountJobLedgers
from app.production.models import JobRecord


def _write_json_atomic(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_name(path.name + ".part")
    try:
        partial.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(partial, path)
    finally:
        if partial.exists():
            partial.unlink()


class JobStore:
    def __init__(self, root: str | Path = "runtime/jobs") -> None:
        self.root = Path(root)
        self.ledgers = AccountJobLedgers(self.root.parent)

    def path_for(self, job_id: str) -> Path:
        return self.root / job_id / "job.json"

    def create(self, job: JobRecord) -> JobRecord:
        if self.path_for(job.job_id).exists():
            raise ValueError(f"job already exists: {job.job_id}")
        self.save(job)
        self.ledgers.append_job_event(
            "JOB_CREATED",
            job_id=job.job_id,
            account_id=job.account_id,
            session_slot=job.session_slot,
            prompt_hash=job.prompt_hash,
            target_duration=job.target_duration,
        )
        return job

    def load(self, job_id: str) -> JobRecord:
        path = self.path_for(job_id)
        if not path.is_file():
            raise FileNotFoundError(path)
        return JobRecord.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def save(self, job: JobRecord) -> None:
        _write_json_atomic(self.path_for(job.job_id), job.public_dict())

    def transition(self, job: JobRecord, next_status: str, **updates: Any) -> JobRecord:
        job.transition(next_status)
        for key, value in updates.items():
            if not hasattr(job, key):
                raise ValueError(f"unsupported job update: {key}")
            setattr(job, key, value)
        self.save(job)
        self.ledgers.append_job_event(
            f"JOB_{next_status}",
            job_id=job.job_id,
            account_id=job.account_id,
            session_slot=job.session_slot,
            prompt_hash=job.prompt_hash,
            conversation_id=job.conversation_id,
            message_id=job.message_id,
            task_id=job.task_id,
            vid=job.vid,
            result="PASS" if next_status == "PASS" else None,
            failure_code=job.failure_code,
        )
        return job
