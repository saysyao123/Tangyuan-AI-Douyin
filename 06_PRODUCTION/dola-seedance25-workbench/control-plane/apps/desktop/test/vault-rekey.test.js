'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const { buildPortableLayout, ensurePortableLayout } = require('../src/core/portable-paths');
const { ProfileVault } = require('../src/core/vault');
const { rekeyVaultPassword } = require('../src/core/vault-rekey');

const OLD = 'Tangyuan-Portable-2026!';
const NEXT = 'private replacement password 2026';

test('vault password can be changed while preserving sealed account profile', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'dola-vault-rekey-'));
  try {
    const layout = buildPortableLayout(root);
    ensurePortableLayout(layout);
    const vault = new ProfileVault(layout);
    vault.initialize(OLD);

    const source = path.join(root, 'source-profile');
    fs.mkdirSync(path.join(source, 'Default'), { recursive: true });
    fs.writeFileSync(path.join(source, 'Default', 'Preferences'), '{"session":"preserved"}', 'utf8');
    vault.sealProfile('acct_rekey', source, { removeSource: true });
    assert.equal(vault.status().dirtyAccounts.length, 0);

    const changed = rekeyVaultPassword(vault, layout, OLD, NEXT);
    assert.equal(changed.changed, true);
    assert.equal(vault.status().state, 'UNLOCKED');
    assert.equal(vault.status().sealedAccounts.includes('acct_rekey'), true);
    vault.lock();
    assert.throws(() => vault.unlock(OLD), (error) => error.code === 'VAULT_UNLOCK_FAILED');
    vault.unlock(NEXT);
    const restored = vault.unsealProfile('acct_rekey');
    assert.equal(fs.readFileSync(path.join(restored.workingDir, 'Default', 'Preferences'), 'utf8'), '{"session":"preserved"}');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});
