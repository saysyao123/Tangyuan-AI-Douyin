'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');
const { ProviderLifecycleStore } = require('../src/core/provider-lifecycle-store');

test('observation timeout remains recoverable and does not imply resubmit', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'dola-lifecycle-'));
  try {
    const store = new ProviderLifecycleStore(root);
    store.begin({ id: 'task_001', accountId: 'acct_001', provider: 'dola-web-background' }, { id: 'acct_001' });
    store.transition('task_001', 'SUBMITTING');
    store.markSubmitted('task_001', { conversationId: 'conv-observed' });
    store.transition('task_001', 'GENERATING');
    const wait = store.markObservationWait('task_001', { lastKnownPage: '/chat/abc' });
    assert.equal(wait.state, 'OBSERVATION_WAIT');
    assert.equal(store.recoverable('task_001'), true);
    assert.equal(wait.submittedAt > 0, true);
    assert.equal(wait.error, null);
    assert.equal(wait.history.filter((item) => item.state === 'SUBMITTED').length, 1);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});
