'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const { startControlServer } = require('../src/control-server');
const { buildPortableLayout, ensurePortableLayout } = require('../src/core/portable-paths');
const { AccountRegistry } = require('../src/core/account-registry');
const { WorkerScheduler } = require('../src/core/worker-scheduler');
const { WorkerConfigStore } = require('../src/core/worker-config');

async function jsonRequest(runtime, method, route, body) {
  const response = await fetch(`http://127.0.0.1:${runtime.info.port}${route}`, {
    method,
    headers: {
      authorization: `Bearer ${runtime.info.token}`,
      ...(body === undefined ? {} : { 'content-type': 'application/json' })
    },
    body: body === undefined ? undefined : JSON.stringify(body)
  });
  return { status: response.status, body: await response.json() };
}

test('account health, pause/resume and worker settings are available through Control Plane', async () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'dola-control-workers-'));
  const previousControlDir = process.env.SEEDANCE_STUDIO_CONTROL_DIR;
  process.env.SEEDANCE_STUDIO_CONTROL_DIR = path.join(root, 'control');
  const layout = buildPortableLayout(path.join(root, 'portable'));
  ensurePortableLayout(layout);
  const registry = new AccountRegistry(layout);
  const config = new WorkerConfigStore(layout);
  const scheduler = new WorkerScheduler(config.load());
  const a = registry.create({ id: 'acct_001', name: 'A', status: 'READY' });
  registry.recordHealth(a.id, { loginStatus: 'logged_in', pageLoaded: true });
  let runtime;
  try {
    runtime = await startControlServer({
      health: async () => ({ ok: true }),
      listAccounts: async () => registry.list(),
      createAccount: async (name) => registry.create({ name }),
      activateAccount: async (id) => registry.get(id),
      getAccountSession: async (id) => ({ accountId: id, loginStatus: registry.get(id)?.health?.loginStatus || 'unknown' }),
      listProviders: async () => [],
      listTasks: async () => [],
      createTask: async () => ({}),
      getTask: async () => null,
      cancelTask: async () => null,
      dispatchTask: async () => ({ ok: false, statusCode: 409 }),
      accountHealthSummary: async () => registry.healthSummary(),
      pauseAccount: async (id, reason) => registry.pause(id, reason),
      resumeAccount: async (id) => registry.resume(id),
      debugAccount: async (id) => ({ account: registry.get(id), debug: scheduler.promoteDebug(id) }),
      workerStatus: async () => scheduler.status(),
      configureWorkers: async (input) => {
        const saved = config.save(input);
        scheduler.configure(saved);
        return { settings: saved, workers: scheduler.status() };
      },
      sweepWorkers: async () => ({ evicted: scheduler.sweepIdle(), workers: scheduler.status() })
    });

    const health = await jsonRequest(runtime, 'GET', '/v1/accounts/health');
    assert.equal(health.status, 200);
    assert.equal(health.body.schedulable, 1);

    const paused = await jsonRequest(runtime, 'POST', '/v1/accounts/acct_001/pause', { reason: 'test' });
    assert.equal(paused.status, 200);
    assert.equal(paused.body.account.status, 'PAUSED');

    const resumed = await jsonRequest(runtime, 'POST', '/v1/accounts/acct_001/resume', {});
    assert.equal(resumed.status, 200);
    assert.equal(resumed.body.account.status, 'READY');

    const settings = await jsonRequest(runtime, 'POST', '/v1/workers/settings', { maxWorkers: 4, idleMs: 60000 });
    assert.equal(settings.status, 200);
    assert.equal(settings.body.workers.maxWorkers, 4);
    assert.equal(config.load().maxWorkers, 4);

    const debug = await jsonRequest(runtime, 'POST', '/v1/accounts/acct_001/debug', {});
    assert.equal(debug.status, 200);
    assert.equal(debug.body.debug.accountId, 'acct_001');

    const workers = await jsonRequest(runtime, 'GET', '/v1/workers');
    assert.equal(workers.status, 200);
    assert.equal(workers.body.debugAccountId, 'acct_001');
  } finally {
    if (runtime) await runtime.stop();
    if (previousControlDir === undefined) delete process.env.SEEDANCE_STUDIO_CONTROL_DIR;
    else process.env.SEEDANCE_STUDIO_CONTROL_DIR = previousControlDir;
    fs.rmSync(root, { recursive: true, force: true });
  }
});
