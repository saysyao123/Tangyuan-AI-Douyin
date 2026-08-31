'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { ProfileVault } = require('./vault');

function rekeyError(code, message, statusCode = 409) {
  const error = new Error(message);
  error.code = code;
  error.statusCode = statusCode;
  return error;
}

function timestamp() {
  return new Date().toISOString().replace(/[:.]/g, '-');
}

function copyDir(source, target) {
  fs.rmSync(target, { recursive: true, force: true });
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.cpSync(source, target, { recursive: true, force: true, dereference: false });
}

function clearWorking(layout) {
  try {
    for (const entry of fs.readdirSync(layout.vaultWorkingDir, { withFileTypes: true })) {
      fs.rmSync(path.join(layout.vaultWorkingDir, entry.name), { recursive: true, force: true });
    }
  } catch (_) {}
  try { fs.unlinkSync(path.join(layout.unlockedProfilesDir, 'vault-session.json')); } catch (_) {}
}

function replaceVaultObject(target, source) {
  for (const key of Object.keys(target)) delete target[key];
  Object.assign(target, source);
  return target;
}

/**
 * Change the vault password without changing account IDs.
 *
 * Preconditions: no live/dirty Chromium account session. The caller should
 * close visible Dola WebViews, flush storage and reseal dirty profiles first.
 * The operation keeps an encrypted backup of the old vault and rolls back on
 * failure. It never exposes the password to the loopback Control Plane.
 */
function rekeyVaultPassword(vault, layout, currentPassword, nextPassword) {
  const current = String(currentPassword || '');
  const next = String(nextPassword || '');
  if (next.length < 8) throw rekeyError('WEAK_VAULT_PASSWORD', 'New vault password must contain at least 8 characters.', 400);
  if (current === next) throw rekeyError('PASSWORD_UNCHANGED', 'New vault password must differ from the current password.', 400);

  vault.unlock(current);
  const initial = vault.status();
  if (initial.dirtyAccounts.length) {
    throw rekeyError('REKEY_REQUIRES_CLEAN_VAULT', 'All account sessions must be resealed before changing the vault password.');
  }

  const sealedAccounts = [...initial.sealedAccounts];
  const backupDir = path.join(layout.backupsDir, 'vault-rekey', `${timestamp()}-old-vault`);
  copyDir(layout.vaultDir, backupDir);
  const plaintextDirs = [];

  try {
    for (const accountId of sealedAccounts) {
      const result = vault.unsealProfile(accountId, { force: true });
      plaintextDirs.push({ accountId, workingDir: result.workingDir });
    }

    // Clear the old key before replacing the encrypted vault tree. force=true
    // is intentional here because the plaintext copies are the controlled
    // rekey workspace, not active Chromium runtime partitions.
    vault.lock({ force: true });
    try { fs.unlinkSync(path.join(layout.unlockedProfilesDir, 'vault-session.json')); } catch (_) {}
    fs.rmSync(layout.vaultDir, { recursive: true, force: true });
    fs.mkdirSync(layout.vaultDir, { recursive: true });

    const fresh = new ProfileVault(layout);
    fresh.initialize(next);
    for (const item of plaintextDirs) {
      fresh.sealProfile(item.accountId, item.workingDir, { removeSource: true });
    }
    fresh.lock();
    fresh.unlock(next);
    replaceVaultObject(vault, fresh);

    return {
      changed: true,
      sealedAccounts: sealedAccounts.length,
      backupDir,
      vault: vault.status()
    };
  } catch (error) {
    clearWorking(layout);
    try {
      fs.rmSync(layout.vaultDir, { recursive: true, force: true });
      copyDir(backupDir, layout.vaultDir);
      const restored = new ProfileVault(layout);
      restored.unlock(current);
      replaceVaultObject(vault, restored);
    } catch (_) {}
    if (error.code) throw error;
    throw rekeyError('VAULT_REKEY_FAILED', `Vault password change failed and rollback was attempted: ${error.message || error}`);
  } finally {
    for (const item of plaintextDirs) {
      try { fs.rmSync(item.workingDir, { recursive: true, force: true }); } catch (_) {}
    }
  }
}

module.exports = { rekeyVaultPassword, rekeyError };
