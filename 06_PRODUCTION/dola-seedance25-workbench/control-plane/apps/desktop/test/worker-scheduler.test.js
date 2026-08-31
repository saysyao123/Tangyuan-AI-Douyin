'use strict';

const assert = require('node:assert/strict');
const test = require('node:test');

const { WorkerScheduler } = require('../src/core/worker-scheduler');

function account(id, status = 'READY', extra = {}) {
  return {
    id,
    status,
    enabled: true,
    restrictionCode: '',
    health: { loginStatus: status === 'NEEDS_LOGIN' ? 'logged_out' : 'logged_in' },
    capabilities: { quotaStatus: 'AVAILABLE', entitlementStatus: 'AVAILABLE' },
    ...extra
  };
}

test('global active leases never exceed configured worker limit', () => {
  const scheduler = new WorkerScheduler({ maxWorkers: 3 });
  const accounts = [account('acct_001'), account('acct_002'), account('acct_003'), account('acct_004')];
  scheduler.acquire({ id: 'job_1' }, accounts);
  scheduler.acquire({ id: 'job_2' }, accounts);
  scheduler.acquire({ id: 'job_3' }, accounts);
  assert.equal(scheduler.status().activeLeases, 3);
  assert.throws(() => scheduler.acquire({ id: 'job_4' }, accounts), (error) => error.code === 'WORKER_LIMIT_REACHED');
});

test('one account never receives two concurrent generation leases', () => {
  const scheduler = new WorkerScheduler({ maxWorkers: 3 });
  const accounts = [account('acct_001'), account('acct_002')];
  const first = scheduler.acquire({ id: 'job_1', requestedAccountId: 'acct_001' }, accounts);
  assert.equal(first.lease.accountId, 'acct_001');
  assert.throws(
    () => scheduler.acquire({ id: 'job_2', requestedAccountId: 'acct_001' }, accounts),
    (error) => error.code === 'FORCED_ACCOUNT_BUSY'
  );
});

test('forced account is obeyed and unavailable forced account is not silently replaced', () => {
  const scheduler = new WorkerScheduler({ maxWorkers: 3 });
  const accounts = [account('acct_ready'), account('acct_paused', 'PAUSED', { enabled: false })];
  const forced = scheduler.acquire({ id: 'job_forced', requestedAccountId: 'acct_ready' }, accounts);
  assert.equal(forced.lease.accountId, 'acct_ready');
  scheduler.release('job_forced');
  assert.throws(
    () => scheduler.acquire({ id: 'job_blocked', requestedAccountId: 'acct_paused' }, accounts),
    (error) => error.code === 'FORCED_ACCOUNT_UNAVAILABLE' && error.accountId === 'acct_paused'
  );
  assert.equal(scheduler.status().activeLeases, 0);
});

test('auto assignment only chooses healthy schedulable accounts', () => {
  const scheduler = new WorkerScheduler({ maxWorkers: 3 });
  const accounts = [
    account('acct_login', 'NEEDS_LOGIN'),
    account('acct_quota', 'RESTRICTED', { restrictionCode: 'QUOTA_EXHAUSTED' }),
    account('acct_ok')
  ];
  const result = scheduler.acquire({ id: 'job_auto' }, accounts);
  assert.equal(result.lease.accountId, 'acct_ok');
});

test('release makes account reusable while preserving awake worker state', () => {
  const scheduler = new WorkerScheduler({ maxWorkers: 2 });
  const accounts = [account('acct_001')];
  scheduler.acquire({ id: 'job_1' }, accounts);
  const released = scheduler.release('job_1');
  assert.equal(released.released, true);
  assert.equal(scheduler.status().workers[0].state, 'idle');
  const second = scheduler.acquire({ id: 'job_2' }, accounts);
  assert.equal(second.lease.accountId, 'acct_001');
});

test('idle workers are evicted lazily but active and debug workers stay awake', () => {
  let now = 1000;
  const slept = [];
  const scheduler = new WorkerScheduler({
    maxWorkers: 3,
    idleMs: 5000,
    now: () => now,
    onSleep: (id) => slept.push(id)
  });
  const accounts = [account('acct_001'), account('acct_002')];
  scheduler.acquire({ id: 'job_1', requestedAccountId: 'acct_001' }, accounts);
  scheduler.release('job_1');
  scheduler.promoteDebug('acct_002');
  now += 6000;
  const evicted = scheduler.sweepIdle();
  assert.deepEqual(evicted, ['acct_001']);
  assert.deepEqual(slept, ['acct_001']);
  assert.equal(scheduler.status().workers.some((worker) => worker.accountId === 'acct_002'), true);
});

test('same job acquire is idempotent', () => {
  const scheduler = new WorkerScheduler({ maxWorkers: 2 });
  const accounts = [account('acct_001')];
  const first = scheduler.acquire({ id: 'job_same' }, accounts);
  const second = scheduler.acquire({ id: 'job_same' }, accounts);
  assert.equal(first.created, true);
  assert.equal(second.created, false);
  assert.equal(second.lease.accountId, first.lease.accountId);
  assert.equal(scheduler.status().activeLeases, 1);
});
