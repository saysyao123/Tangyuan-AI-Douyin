from __future__ import annotations

import json
import uuid
from pathlib import Path

from app.production.job_store import JobStore
from app.production.models import JobRecord, prompt_sha256


class JobQueue:
    def __init__(self, path: str | Path = "runtime/queue/jobs.jsonl", *, store: JobStore | None = None) -> None:
        self.path = Path(path)
        self.store = store or JobStore(self.path.parent.parent / "jobs")

    def enqueue(self, prompt: str, *, target_duration: float = 5.0, job_id: str | None = None) -> JobRecord:
        if not prompt.strip():
            raise ValueError("prompt cannot be empty")
        job = JobRecord(
            job_id=job_id or f"{uuid.uuid4().hex[:8]}",
            prompt_hash=prompt_sha256(prompt),
            target_duration=target_duration,
        )
        prompt_path = self.path.parent / "prompts" / f"{job.job_id}.md"
        prompt_path.parent.mkdir(parents=True, exist_ok=True)
        prompt_path.write_text(prompt, encoding="utf-8")
        self.store.create(job)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps({"job_id": job.job_id, "status": "QUEUED"}, ensure_ascii=False) + "\n")
        return job

    def pending(self) -> list[JobRecord]:
        if not self.path.is_file():
            return []
        result: list[JobRecord] = []
        seen: set[str] = set()
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            job_id = row.get("job_id")
            if not job_id or job_id in seen:
                continue
            seen.add(job_id)
            job = self.store.load(job_id)
            if job.status == "CREATED":
                result.append(job)
        return result
