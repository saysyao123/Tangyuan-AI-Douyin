'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');
const { startControlServer } = require('../src/control-server');

async function request(runtime, method, route) {
  const response = await fetch(`http://127.0.0.1:${runtime.info.port}${route}`, {
    method,
    headers: { authorization: `Bearer ${runtime.info.token}`, 'content-type': 'application/json' },
    body: method === 'POST' ? '{}' : undefined
  });
  return { status: response.status, body: await response.json() };
}

test('task recovery route can return accepted recoverable state without resubmission', async () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'dola-control-recovery-'));
  const previous = process.env.SEEDANCE_STUDIO_CONTROL_DIR;
  process.env.SEEDANCE_STUDIO_CONTROL_DIR = root;
  let runtime;
  try {
    runtime = await startControlServer({
      health: async () => ({ ok: true }),
      recoverTask: async (id) => ({ ok: false, recoverable: true, state: 'RECOVERY_REQUIRED', taskId: id })
    });
    const result = await request(runtime, 'POST', '/v1/tasks/task_001/recover');
    assert.equal(result.status, 202);
    assert.equal(result.body.recoverable, true);
    assert.equal(result.body.state, 'RECOVERY_REQUIRED');
  } finally {
    if (runtime) await runtime.stop();
    if (previous === undefined) delete process.env.SEEDANCE_STUDIO_CONTROL_DIR;
    else process.env.SEEDANCE_STUDIO_CONTROL_DIR = previous;
    fs.rmSync(root, { recursive: true, force: true });
  }
});
