'use strict';

const { schedulingReason } = require('./account-registry');

function schedulerError(code, message, statusCode = 409, detail = {}) {
  const error = new Error(message);
  error.code = code;
  error.statusCode = statusCode;
  Object.assign(error, detail);
  return error;
}

function normalizeMaxWorkers(value, fallback = 3) {
  const parsed = Number(value ?? fallback);
  if (!Number.isInteger(parsed) || parsed < 1 || parsed > 20) {
    throw schedulerError('BAD_MAX_WORKERS', 'maxWorkers must be an integer from 1 to 20', 400);
  }
  return parsed;
}

function normalizeIdleMs(value, fallback = 5 * 60 * 1000) {
  const parsed = Number(value ?? fallback);
  if (!Number.isFinite(parsed) || parsed < 1000 || parsed > 24 * 60 * 60 * 1000) {
    throw schedulerError('BAD_IDLE_MS', 'idleMs must be between 1000 and 86400000', 400);
  }
  return Math.round(parsed);
}

class WorkerScheduler {
  constructor(options = {}) {
    this.maxWorkers = normalizeMaxWorkers(options.maxWorkers, 3);
    this.idleMs = normalizeIdleMs(options.idleMs, 5 * 60 * 1000);
    this.now = typeof options.now === 'function' ? options.now : () => Date.now();
    this.onWake = typeof options.onWake === 'function' ? options.onWake : null;
    this.onSleep = typeof options.onSleep === 'function' ? options.onSleep : null;
    this.leasesByAccount = new Map();
    this.leasesByJob = new Map();
    this.workers = new Map();
    this.debugAccountId = null;
  }

  configure(input = {}) {
    if (input.maxWorkers !== undefined) this.maxWorkers = normalizeMaxWorkers(input.maxWorkers, this.maxWorkers);
    if (input.idleMs !== undefined) this.idleMs = normalizeIdleMs(input.idleMs, this.idleMs);
    return this.status();
  }

  activeLeaseCount() {
    return this.leasesByJob.size;
  }

  isLeased(accountId) {
    return this.leasesByAccount.has(String(accountId || ''));
  }

  isJobLeased(jobId) {
    return this.leasesByJob.has(String(jobId || ''));
  }

  _ensureWorker(accountId) {
    const id = String(accountId);
    let worker = this.workers.get(id);
    if (!worker) {
      const now = this.now();
      worker = {
        accountId: id,
        state: 'idle',
        jobId: null,
        awakeAt: now,
        lastActiveAt: now,
        debugVisible: this.debugAccountId === id
      };
      this.workers.set(id, worker);
      if (this.onWake) this.onWake(id, { ...worker });
    }
    return worker;
  }

  _accountIsSelectable(account) {
    return schedulingReason(account) === null && !this.isLeased(account.id);
  }

  _selectAccount(job, accounts) {
    const pool = Array.isArray(accounts) ? accounts : [];
    const requested = String(job?.requestedAccountId || job?.accountId || '').trim();
    if (requested) {
      const account = pool.find((item) => item.id === requested);
      if (!account) throw schedulerError('FORCED_ACCOUNT_NOT_FOUND', 'The requested account does not exist.', 404, { accountId: requested });
      const reason = schedulingReason(account);
      if (reason) throw schedulerError('FORCED_ACCOUNT_UNAVAILABLE', `Requested account is not schedulable: ${reason}`, 409, { accountId: requested, reason });
      if (this.isLeased(account.id)) throw schedulerError('FORCED_ACCOUNT_BUSY', 'Requested account already has an active generation lease.', 409, { accountId: requested });
      return account;
    }

    const candidates = pool
      .filter((account) => this._accountIsSelectable(account))
      .sort((a, b) => {
        const workerA = this.workers.get(a.id);
        const workerB = this.workers.get(b.id);
        if (Boolean(workerA) !== Boolean(workerB)) return workerA ? -1 : 1;
        const priorityDiff = Number(b.priority || 0) - Number(a.priority || 0);
        if (priorityDiff) return priorityDiff;
        const aTime = Number(workerA?.lastActiveAt || a.lastCheckedAt || a.createdAt || 0);
        const bTime = Number(workerB?.lastActiveAt || b.lastCheckedAt || b.createdAt || 0);
        return aTime - bTime;
      });
    if (!candidates.length) throw schedulerError('NO_SCHEDULABLE_ACCOUNT', 'No healthy, enabled account is available for this job.');
    return candidates[0];
  }

  acquire(job, accounts) {
    const jobId = String(job?.id || '').trim();
    if (!jobId) throw schedulerError('BAD_JOB_ID', 'job.id is required', 400);
    const existing = this.leasesByJob.get(jobId);
    if (existing) return { created: false, lease: { ...existing }, worker: { ...this.workers.get(existing.accountId) } };
    if (this.activeLeaseCount() >= this.maxWorkers) {
      throw schedulerError('WORKER_LIMIT_REACHED', `Global worker limit ${this.maxWorkers} is already active.`);
    }

    const account = this._selectAccount(job, accounts);
    const worker = this._ensureWorker(account.id);
    const now = this.now();
    const lease = {
      jobId,
      accountId: account.id,
      forced: Boolean(job.requestedAccountId || job.accountId),
      acquiredAt: now
    };
    this.leasesByAccount.set(account.id, lease);
    this.leasesByJob.set(jobId, lease);
    worker.state = 'busy';
    worker.jobId = jobId;
    worker.lastActiveAt = now;
    worker.debugVisible = this.debugAccountId === account.id;
    return { created: true, lease: { ...lease }, worker: { ...worker } };
  }

  release(jobId, options = {}) {
    const id = String(jobId || '');
    const lease = this.leasesByJob.get(id);
    if (!lease) return { released: false, lease: null };
    this.leasesByJob.delete(id);
    this.leasesByAccount.delete(lease.accountId);
    const worker = this.workers.get(lease.accountId);
    if (worker) {
      worker.state = 'idle';
      worker.jobId = null;
      worker.lastActiveAt = this.now();
      if (options.sleep === true) this.sleepAccount(lease.accountId, 'explicit-release');
    }
    return { released: true, lease: { ...lease }, worker: worker ? { ...worker } : null };
  }

  sleepAccount(accountId, reason = 'idle') {
    const id = String(accountId || '');
    if (this.isLeased(id)) throw schedulerError('ACCOUNT_LEASE_ACTIVE', 'Cannot sleep an account with an active generation lease.');
    const worker = this.workers.get(id);
    if (!worker) return { slept: false, accountId: id, reason: 'not-awake' };
    this.workers.delete(id);
    if (this.debugAccountId === id) this.debugAccountId = null;
    if (this.onSleep) this.onSleep(id, { ...worker, sleepReason: reason });
    return { slept: true, accountId: id, reason };
  }

  sweepIdle() {
    const now = this.now();
    const evicted = [];
    for (const [accountId, worker] of this.workers.entries()) {
      if (worker.state !== 'idle' || this.isLeased(accountId) || this.debugAccountId === accountId) continue;
      if (now - Number(worker.lastActiveAt || 0) < this.idleMs) continue;
      const result = this.sleepAccount(accountId, 'idle-timeout');
      if (result.slept) evicted.push(accountId);
    }
    return evicted;
  }

  promoteDebug(accountId) {
    const id = String(accountId || '').trim();
    if (!id) throw schedulerError('BAD_ACCOUNT_ID', 'accountId is required', 400);
    if (this.debugAccountId && this.workers.has(this.debugAccountId)) {
      this.workers.get(this.debugAccountId).debugVisible = false;
    }
    this.debugAccountId = id;
    const worker = this._ensureWorker(id);
    worker.debugVisible = true;
    worker.lastActiveAt = this.now();
    return { accountId: id, worker: { ...worker } };
  }

  clearDebug() {
    const id = this.debugAccountId;
    if (id && this.workers.has(id)) this.workers.get(id).debugVisible = false;
    this.debugAccountId = null;
    return { accountId: id };
  }

  status() {
    return {
      maxWorkers: this.maxWorkers,
      idleMs: this.idleMs,
      activeLeases: this.activeLeaseCount(),
      awakeWorkers: this.workers.size,
      debugAccountId: this.debugAccountId,
      leases: Array.from(this.leasesByJob.values()).map((item) => ({ ...item })),
      workers: Array.from(this.workers.values()).map((item) => ({ ...item }))
    };
  }
}

module.exports = {
  WorkerScheduler,
  normalizeMaxWorkers,
  normalizeIdleMs,
  schedulerError
};
