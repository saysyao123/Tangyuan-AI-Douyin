'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const { buildPortableLayout, ensurePortableLayout } = require('../src/core/portable-paths');
const { AccountRegistry } = require('../src/core/account-registry');

function fixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'dola-account-registry-'));
  const layout = buildPortableLayout(root);
  ensurePortableLayout(layout);
  return { root, registry: new AccountRegistry(layout) };
}

function cleanup(root) {
  fs.rmSync(root, { recursive: true, force: true });
}

test('legacy accounts import dynamically without hard-coded account names', () => {
  const { root, registry } = fixture();
  try {
    const legacy = Array.from({ length: 20 }, (_, index) => ({
      id: `acct_${String(index + 1).padStart(3, '0')}`,
      name: `Workspace ${index + 1}`,
      partition: `persist:dola_acct_${index + 1}`,
      status: 'READY'
    }));
    registry.syncLegacy(legacy);
    const accounts = registry.list();
    assert.equal(accounts.length, 20);
    assert.equal(accounts.every((item) => item.source === 'legacy-poc'), true);
    assert.equal(accounts.every((item) => item.schedulable), true);
  } finally { cleanup(root); }
});

test('pause prevents scheduling but keeps account metadata available', () => {
  const { root, registry } = fixture();
  try {
    const account = registry.create({ name: 'Dola A', status: 'READY' });
    const paused = registry.pause(account.id, 'manual maintenance');
    assert.equal(paused.enabled, false);
    assert.equal(paused.status, 'PAUSED');
    assert.equal(paused.schedulable, false);
    assert.equal(paused.schedulingReason, 'ACCOUNT_DISABLED');
    assert.equal(registry.get(account.id).name, 'Dola A');
  } finally { cleanup(root); }
});

test('login health transitions ready account to needs-login and back', () => {
  const { root, registry } = fixture();
  try {
    const account = registry.create({ name: 'Health', status: 'READY' });
    const out = registry.recordHealth(account.id, { loginStatus: 'logged_out', pageLoaded: true });
    assert.equal(out.status, 'NEEDS_LOGIN');
    assert.equal(out.schedulingReason, 'LOGIN_REQUIRED');
    const inside = registry.recordHealth(account.id, { loginStatus: 'logged_in', pageLoaded: true });
    assert.equal(inside.status, 'READY');
    assert.equal(inside.schedulable, true);
  } finally { cleanup(root); }
});

test('quota and entitlement restrictions are exposed and block scheduling', () => {
  const { root, registry } = fixture();
  try {
    const account = registry.create({ name: 'Capacity', status: 'READY' });
    registry.recordHealth(account.id, { loginStatus: 'logged_in', pageLoaded: true });
    const exhausted = registry.recordCapabilities(account.id, {
      t2v: true,
      i2v: true,
      durationSeconds: { 5: 'available', 10: 'available', 30: 'experimental' },
      quotaStatus: 'EXHAUSTED',
      entitlementStatus: 'AVAILABLE'
    });
    assert.equal(exhausted.status, 'RESTRICTED');
    assert.equal(exhausted.schedulingReason, 'QUOTA_EXHAUSTED');
    const restored = registry.recordCapabilities(account.id, {
      quotaStatus: 'AVAILABLE',
      entitlementStatus: 'AVAILABLE'
    });
    assert.equal(restored.status, 'READY');
    assert.equal(restored.capabilities.durations[30], 'experimental');
    assert.equal(restored.schedulable, true);
  } finally { cleanup(root); }
});

test('health summary is Codex-friendly and counts schedulable accounts', () => {
  const { root, registry } = fixture();
  try {
    const ready = registry.create({ name: 'Ready', status: 'READY' });
    const login = registry.create({ name: 'Login', status: 'NEEDS_LOGIN' });
    registry.recordHealth(ready.id, { loginStatus: 'logged_in' });
    registry.recordHealth(login.id, { loginStatus: 'logged_out' });
    const summary = registry.healthSummary();
    assert.equal(summary.total, 2);
    assert.equal(summary.schedulable, 1);
    assert.equal(summary.counts.READY, 1);
    assert.equal(summary.counts.NEEDS_LOGIN, 1);
  } finally { cleanup(root); }
});
