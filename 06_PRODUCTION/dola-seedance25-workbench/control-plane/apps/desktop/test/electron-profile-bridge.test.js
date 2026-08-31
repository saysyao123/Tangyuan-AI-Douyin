'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const { buildPortableLayout, ensurePortableLayout } = require('../src/core/portable-paths');
const { ProfileVault } = require('../src/core/vault');
const { ElectronProfileBridge, persistentPartitionName } = require('../src/core/electron-profile-bridge');

const PASSWORD = 'portable vault bridge password';

function fixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'dola-electron-profile-'));
  const layout = buildPortableLayout(root);
  ensurePortableLayout(layout);
  const vault = new ProfileVault(layout);
  const bridge = new ElectronProfileBridge(layout, vault);
  return { root, layout, vault, bridge };
}

function cleanup(root) {
  fs.rmSync(root, { recursive: true, force: true });
}

test('persistent partition names preserve existing dola_<id> convention', () => {
  assert.equal(persistentPartitionName('persist:dola_abc123'), 'dola_abc123');
  assert.throws(() => persistentPartitionName('temporary'), (error) => error.code === 'NON_PERSISTENT_PARTITION');
});

test('sealed account profile is prepared into ephemeral Electron sessionData and resealed with changes', () => {
  const { root, layout, vault, bridge } = fixture();
  try {
    vault.initialize(PASSWORD);
    const source = path.join(root, 'source');
    fs.mkdirSync(path.join(source, 'Default'), { recursive: true });
    fs.writeFileSync(path.join(source, 'Default', 'Cookies'), 'cookie-v1', 'utf8');
    vault.sealProfile('acct_001', source);

    const account = { id: 'acct_001', partition: 'persist:dola_acct_001' };
    const prepared = bridge.prepare(account);
    assert.equal(prepared.partitionDir, path.join(layout.sessionDataDir, 'Partitions', 'dola_acct_001'));
    assert.equal(fs.readFileSync(path.join(prepared.partitionDir, 'Default', 'Cookies'), 'utf8'), 'cookie-v1');
    assert.equal(vault.status().state, 'RESEAL_REQUIRED');

    fs.writeFileSync(path.join(prepared.partitionDir, 'Default', 'Cookies'), 'cookie-v2', 'utf8');
    const resealed = bridge.reseal(account);
    assert.equal(resealed.resealed, true);
    assert.equal(fs.existsSync(prepared.partitionDir), false);
    vault.lock();

    ensurePortableLayout(layout);
    vault.unlock(PASSWORD);
    const second = bridge.prepare(account);
    assert.equal(fs.readFileSync(path.join(second.partitionDir, 'Default', 'Cookies'), 'utf8'), 'cookie-v2');
  } finally { cleanup(root); }
});

test('crash recovery preserves dirty runtime partition instead of replacing it with older sealed data', () => {
  const { root, layout, vault, bridge } = fixture();
  try {
    vault.initialize(PASSWORD);
    const source = path.join(root, 'source');
    fs.mkdirSync(source, { recursive: true });
    fs.writeFileSync(path.join(source, 'state.txt'), 'sealed-old', 'utf8');
    vault.sealProfile('acct_crash', source);
    const account = { id: 'acct_crash', partition: 'persist:dola_acct_crash' };
    const prepared = bridge.prepare(account);
    fs.writeFileSync(path.join(prepared.partitionDir, 'state.txt'), 'runtime-new', 'utf8');

    const restartedVault = new ProfileVault(layout);
    const restartedBridge = new ElectronProfileBridge(layout, restartedVault);
    assert.equal(restartedVault.status().recoveryRequired, true);
    restartedVault.unlock(PASSWORD);
    const recovered = restartedBridge.prepare(account);
    assert.equal(recovered.recoveredRuntime, true);
    assert.equal(fs.readFileSync(path.join(recovered.partitionDir, 'state.txt'), 'utf8'), 'runtime-new');
    restartedBridge.reseal(account);
    restartedVault.lock();

    ensurePortableLayout(layout);
    restartedVault.unlock(PASSWORD);
    const final = restartedBridge.prepare(account);
    assert.equal(fs.readFileSync(path.join(final.partitionDir, 'state.txt'), 'utf8'), 'runtime-new');
  } finally { cleanup(root); }
});

test('first-time account prepares an empty Electron partition and becomes dirty', () => {
  const { root, vault, bridge } = fixture();
  try {
    vault.initialize(PASSWORD);
    const account = { id: 'acct_new', partition: 'persist:dola_acct_new' };
    const result = bridge.prepare(account);
    assert.equal(result.createdEmpty, true);
    assert.equal(fs.existsSync(result.partitionDir), true);
    assert.equal(vault.status().dirtyAccounts.includes('acct_new'), true);
  } finally { cleanup(root); }
});
