'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { safeSegment } = require('./atomic-json');

function bridgeError(code, message, statusCode = 409) {
  const error = new Error(message);
  error.code = code;
  error.statusCode = statusCode;
  return error;
}

function persistentPartitionName(partition) {
  const raw = String(partition || '').trim();
  if (!raw.startsWith('persist:')) {
    throw bridgeError('NON_PERSISTENT_PARTITION', 'Account partition must use Electron persist: semantics.', 400);
  }
  const name = raw.slice('persist:'.length);
  if (!name) throw bridgeError('BAD_PARTITION', 'Persistent partition name is empty.', 400);
  return safeSegment(name, 'partition');
}

function directoryHasFiles(dir) {
  try { return fs.readdirSync(dir).length > 0; } catch (_) { return false; }
}

function copyTree(source, target) {
  fs.rmSync(target, { recursive: true, force: true });
  fs.mkdirSync(path.dirname(target), { recursive: true });
  if (fs.existsSync(source)) fs.cpSync(source, target, { recursive: true, force: true, dereference: false });
  else fs.mkdirSync(target, { recursive: true });
}

class ElectronProfileBridge {
  constructor(layout, vault) {
    if (!layout?.sessionDataDir || !layout?.vaultWorkingDir) {
      throw new Error('ElectronProfileBridge requires sessionDataDir and vaultWorkingDir.');
    }
    if (!vault) throw new Error('ElectronProfileBridge requires a ProfileVault.');
    this.layout = layout;
    this.vault = vault;
    fs.mkdirSync(layout.sessionDataDir, { recursive: true });
    fs.mkdirSync(layout.vaultWorkingDir, { recursive: true });
  }

  partitionDir(account) {
    if (!account?.id) throw bridgeError('BAD_ACCOUNT_ID', 'Account id is required.', 400);
    const partitionName = persistentPartitionName(account.partition || `persist:dola_${account.id}`);
    return path.join(this.layout.sessionDataDir, 'Partitions', partitionName);
  }

  tempUnsealDir(accountId) {
    return this.vault.workingDir(accountId);
  }

  prepare(account) {
    const id = String(account?.id || '').trim();
    if (!id) throw bridgeError('BAD_ACCOUNT_ID', 'Account id is required.', 400);
    const status = this.vault.status();
    if (!['UNLOCKED', 'RESEAL_REQUIRED'].includes(status.state)) {
      throw bridgeError('VAULT_LOCKED', 'Vault must be unlocked before a Dola account session can be prepared.', 423);
    }

    const target = this.partitionDir(account);
    const dirty = status.dirtyAccounts.includes(id);
    // Crash recovery rule: if this account was dirty and its plaintext runtime
    // partition still exists, preserve that newer runtime state. Never replace
    // it with an older sealed package automatically.
    if (dirty && directoryHasFiles(target)) {
      return { accountId: id, partitionDir: target, recoveredRuntime: true, prepared: true };
    }

    if (directoryHasFiles(target)) {
      throw bridgeError('UNTRACKED_RUNTIME_PROFILE', 'Runtime partition exists but is not tracked as dirty; manual recovery is required.');
    }

    const unsealed = this.vault.unsealProfile(id);
    copyTree(unsealed.workingDir, target);
    fs.rmSync(unsealed.workingDir, { recursive: true, force: true });
    return {
      accountId: id,
      partitionDir: target,
      recoveredRuntime: false,
      createdEmpty: unsealed.createdEmpty === true,
      fileCount: Number(unsealed.fileCount || 0),
      prepared: true
    };
  }

  markDirty(account) {
    const id = String(account?.id || '').trim();
    if (!id) throw bridgeError('BAD_ACCOUNT_ID', 'Account id is required.', 400);
    this.vault.markDirty(id);
    return { accountId: id, partitionDir: this.partitionDir(account) };
  }

  reseal(account) {
    const id = String(account?.id || '').trim();
    if (!id) throw bridgeError('BAD_ACCOUNT_ID', 'Account id is required.', 400);
    const source = this.partitionDir(account);
    if (!fs.existsSync(source)) {
      // An account can exist without ever opening a Dola session in this run.
      // If it is not dirty there is nothing to reseal.
      if (!this.vault.status().dirtyAccounts.includes(id)) {
        return { accountId: id, resealed: false, reason: 'not-dirty' };
      }
      throw bridgeError('RUNTIME_PROFILE_MISSING', 'Dirty account runtime partition is missing; recovery is required.');
    }
    const result = this.vault.sealProfile(id, source, { removeSource: true });
    fs.rmSync(this.tempUnsealDir(id), { recursive: true, force: true });
    return { ...result, resealed: true };
  }

  resealDirty(accounts) {
    const byId = new Map((Array.isArray(accounts) ? accounts : []).map((account) => [String(account.id), account]));
    const results = [];
    for (const id of this.vault.status().dirtyAccounts) {
      const account = byId.get(id);
      if (!account) {
        results.push({ accountId: id, resealed: false, error: 'ACCOUNT_METADATA_MISSING' });
        continue;
      }
      try { results.push(this.reseal(account)); }
      catch (error) { results.push({ accountId: id, resealed: false, error: error.code || error.message }); }
    }
    return results;
  }

  runtimeStatus(accounts) {
    return (Array.isArray(accounts) ? accounts : []).map((account) => {
      const dir = this.partitionDir(account);
      return {
        accountId: account.id,
        partition: account.partition,
        runtimePrepared: directoryHasFiles(dir) || fs.existsSync(dir),
        dirty: this.vault.status().dirtyAccounts.includes(String(account.id))
      };
    });
  }
}

module.exports = {
  ElectronProfileBridge,
  persistentPartitionName,
  bridgeError
};
