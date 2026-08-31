'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const { buildPortableLayout, ensurePortableLayout } = require('../src/core/portable-paths');
const { ProfileVault } = require('../src/core/vault');

const PASSWORD = 'correct horse battery staple';

function fixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'dola-vault-'));
  const layout = buildPortableLayout(root);
  ensurePortableLayout(layout);
  return { root, layout, vault: new ProfileVault(layout) };
}

function cleanup(root) {
  fs.rmSync(root, { recursive: true, force: true });
}

function writeProfile(dir) {
  fs.mkdirSync(path.join(dir, 'Default', 'Network'), { recursive: true });
  fs.writeFileSync(path.join(dir, 'Default', 'Preferences'), '{"theme":"dark","secretLike":"example-only"}', 'utf8');
  fs.writeFileSync(path.join(dir, 'Default', 'Network', 'Cookies'), Buffer.from([0, 1, 2, 3, 254, 255]));
}

test('vault initializes locked storage and rejects a wrong password', () => {
  const { root, vault } = fixture();
  try {
    const status = vault.initialize(PASSWORD);
    assert.equal(status.initialized, true);
    assert.equal(status.state, 'UNLOCKED');
    vault.lock();
    assert.throws(() => vault.unlock('incorrect password'), (error) => error.code === 'VAULT_UNLOCK_FAILED');
    assert.equal(vault.status().state, 'LOCKED');
    assert.equal(vault.status().secretsExposed, false);
  } finally { cleanup(root); }
});

test('profile files round-trip through per-account authenticated encryption', () => {
  const { root, layout, vault } = fixture();
  try {
    vault.initialize(PASSWORD);
    const source = path.join(root, 'profile-source');
    writeProfile(source);
    const sealed = vault.sealProfile('acct_001', source);
    assert.equal(sealed.fileCount, 2);
    assert.equal(vault.status().sealedAccounts.includes('acct_001'), true);

    const packageDir = vault.accountPackageDir('acct_001');
    const manifestEnvelope = fs.readFileSync(path.join(packageDir, 'manifest.enc.json'), 'utf8');
    assert.equal(manifestEnvelope.includes('Preferences'), false);
    assert.equal(manifestEnvelope.includes('example-only'), false);
    const blobText = fs.readFileSync(path.join(packageDir, 'files', '00000000.bin'));
    assert.equal(blobText.includes(Buffer.from('example-only')), false);

    removeSource(source);
    const unsealed = vault.unsealProfile('acct_001');
    assert.equal(unsealed.createdEmpty, false);
    assert.equal(fs.readFileSync(path.join(unsealed.workingDir, 'Default', 'Preferences'), 'utf8').includes('example-only'), true);
    assert.deepEqual([...fs.readFileSync(path.join(unsealed.workingDir, 'Default', 'Network', 'Cookies'))], [0, 1, 2, 3, 254, 255]);
    assert.equal(vault.status().state, 'RESEAL_REQUIRED');
    assert.throws(() => vault.lock(), (error) => error.code === 'RESEAL_REQUIRED');

    fs.writeFileSync(path.join(unsealed.workingDir, 'Default', 'Preferences'), '{"changed":true}', 'utf8');
    vault.resealProfile('acct_001');
    assert.equal(fs.existsSync(unsealed.workingDir), false);
    assert.equal(vault.status().state, 'UNLOCKED');
    vault.lock();
    assert.equal(vault.status().state, 'LOCKED');
    assert.equal(fs.existsSync(path.join(layout.unlockedProfilesDir, 'vault-session.json')), false);
  } finally { cleanup(root); }
});

function removeSource(dir) {
  fs.rmSync(dir, { recursive: true, force: true });
}

test('first-time account gets an empty controlled working profile and must be resealed', () => {
  const { root, vault } = fixture();
  try {
    vault.initialize(PASSWORD);
    const result = vault.unsealProfile('acct_new');
    assert.equal(result.createdEmpty, true);
    assert.equal(fs.existsSync(result.workingDir), true);
    assert.equal(vault.status().dirtyAccounts.includes('acct_new'), true);
    fs.writeFileSync(path.join(result.workingDir, 'hello.txt'), 'hello', 'utf8');
    vault.resealProfile('acct_new');
    assert.equal(vault.status().sealedAccounts.includes('acct_new'), true);
  } finally { cleanup(root); }
});

test('abnormal shutdown marker is detected by the next vault instance', () => {
  const { root, layout, vault } = fixture();
  try {
    vault.initialize(PASSWORD);
    vault.unsealProfile('acct_crash');
    assert.equal(fs.existsSync(path.join(layout.unlockedProfilesDir, 'vault-session.json')), true);

    // Simulate a new process starting after the previous process disappeared
    // without a clean reseal/lock. No secret key is reused by the new object.
    const restarted = new ProfileVault(layout);
    const status = restarted.status();
    assert.equal(status.state, 'LOCKED');
    assert.equal(status.recoveryRequired, true);
    assert.equal(status.dirtyAccounts.includes('acct_crash'), true);
    assert.throws(() => restarted.resealProfile('acct_crash'), (error) => error.code === 'VAULT_LOCKED');
    restarted.unlock(PASSWORD);
    restarted.resealProfile('acct_crash');
    restarted.lock();
    assert.equal(restarted.status().recoveryRequired, false);
  } finally { cleanup(root); }
});

test('sealed account package can be backed up without unlocking secrets into the backup tree', () => {
  const { root, vault } = fixture();
  try {
    vault.initialize(PASSWORD);
    const source = path.join(root, 'source');
    writeProfile(source);
    vault.sealProfile('acct_backup', source);
    vault.lock();
    const backup = vault.backupSealedProfile('acct_backup');
    assert.equal(fs.existsSync(path.join(backup.backupDir, 'manifest.enc.json')), true);
    const envelope = fs.readFileSync(path.join(backup.backupDir, 'manifest.enc.json'), 'utf8');
    assert.equal(envelope.includes('example-only'), false);
  } finally { cleanup(root); }
});
