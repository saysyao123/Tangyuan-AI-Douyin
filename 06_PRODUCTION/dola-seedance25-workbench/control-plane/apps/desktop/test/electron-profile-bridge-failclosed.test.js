'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const { buildPortableLayout, ensurePortableLayout } = require('../src/core/portable-paths');
const { ProfileVault } = require('../src/core/vault');
const { ElectronProfileBridge } = require('../src/core/electron-profile-bridge');

const PASSWORD = 'portable test password';

function fixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'dola-bridge-failclosed-'));
  const layout = buildPortableLayout(root);
  ensurePortableLayout(layout);
  const vault = new ProfileVault(layout);
  vault.initialize(PASSWORD);
  return { root, layout, vault, bridge: new ElectronProfileBridge(layout, vault) };
}

function account(id = 'acct_failclosed') {
  return { id, partition: `persist:dola_${id}` };
}

test('reseal removes plaintext runtime and clears dirty only after cleanup', () => {
  const { root, vault, bridge } = fixture();
  try {
    const acct = account();
    const prepared = bridge.prepare(acct);
    fs.mkdirSync(path.join(prepared.partitionDir, 'Default'), { recursive: true });
    fs.writeFileSync(path.join(prepared.partitionDir, 'Default', 'Preferences'), '{"ok":true}', 'utf8');
    bridge.markDirty(acct);
    assert.equal(vault.status().dirtyAccounts.includes(acct.id), true);

    const result = bridge.reseal(acct);
    assert.equal(result.resealed, true);
    assert.equal(result.plaintextRemoved, true);
    assert.equal(fs.existsSync(prepared.partitionDir), false);
    assert.equal(vault.status().dirtyAccounts.includes(acct.id), false);
    assert.equal(vault.status().sealedAccounts.includes(acct.id), true);
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});
