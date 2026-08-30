from __future__ import annotations

from app.production.account_registry import AccountRegistry
from app.production.models import AccountRecord, JobRecord


class NoReadyAccount(RuntimeError):
    pass


class HealthAwareRoundRobin:
    """Single-worker round robin over READY accounts with sticky reservations."""

    def __init__(self, registry: AccountRegistry) -> None:
        self.registry = registry
        self._cursor = 0

    def reserve_next(self) -> AccountRecord:
        accounts = self.registry.accounts
        if not accounts:
            raise NoReadyAccount("account registry is empty")
        for offset in range(len(accounts)):
            index = (self._cursor + offset) % len(accounts)
            account = accounts[index]
            if account.enabled and account.status == "READY":
                self._cursor = (index + 1) % len(accounts)
                account.status = "BUSY"
                account.mark_used()
                return account
        raise NoReadyAccount("no enabled READY account is available")

    def bind_job(self, job: JobRecord) -> AccountRecord:
        account = self.reserve_next()
        try:
            job.bind_account(account)
            job.transition("ACCOUNT_ASSIGNED")
        except Exception:
            account.status = "READY"
            raise
        return account

    def release(self, account_id: str, *, success: bool | None = None, error: str = "") -> AccountRecord:
        account = self.registry.get(account_id)
        if success is True:
            account.mark_success()
        elif success is False:
            account.mark_failure(error or "job failed")
        elif account.status == "BUSY":
            account.status = "READY"
        return account

    @staticmethod
    def assert_job_account(job: JobRecord, account: AccountRecord) -> None:
        job.assert_binding(account.account_id, account.session_slot)

    def simulate(self, count: int) -> list[dict[str, str]]:
        assignments: list[dict[str, str]] = []
        for index in range(count):
            job = JobRecord(job_id=f"SIM-{index + 1:03d}", prompt_hash="simulation")
            account = self.bind_job(job)
            assignments.append(
                {
                    "job_id": job.job_id,
                    "account_id": account.account_id,
                    "session_slot": account.session_slot,
                }
            )
            self.release(account.account_id)
        return assignments
