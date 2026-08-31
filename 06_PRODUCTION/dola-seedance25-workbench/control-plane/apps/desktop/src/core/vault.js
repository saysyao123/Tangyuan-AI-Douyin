'use strict';

const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const { readJson, writeJsonAtomic, safeSegment } = require('./atomic-json');

const VAULT_VERSION = 1;
const KDF = Object.freeze({ name: 'scrypt', N: 32768, r: 8, p: 1, keyLen: 32, maxmem: 128 * 1024 * 1024 });
const VERIFIER_CONTEXT = Buffer.from('dola-workbench-vault-verifier-v1', 'utf8');
const ACCOUNT_KEY_INFO = Buffer.from('dola-workbench-account-profile-v1', 'utf8');
const MANIFEST_AAD = Buffer.from('dola-workbench-profile-manifest-v1', 'utf8');

function vaultError(code, message, statusCode = 409) {
  const error = new Error(message);
  error.code = code;
  error.statusCode = statusCode;
  return error;
}

function ensurePassword(password) {
  const value = String(password || '');
  if (value.length < 8) throw vaultError('WEAK_VAULT_PASSWORD', 'Vault password must contain at least 8 characters.', 400);
  return value;
}

function deriveMasterKey(password, salt, kdf = KDF) {
  return crypto.scryptSync(ensurePassword(password), salt, Number(kdf.keyLen || 32), {
    N: Number(kdf.N || KDF.N),
    r: Number(kdf.r || KDF.r),
    p: Number(kdf.p || KDF.p),
    maxmem: Number(kdf.maxmem || KDF.maxmem)
  });
}

function verifierForKey(key) {
  return crypto.createHmac('sha256', key).update(VERIFIER_CONTEXT).digest();
}

function accountKey(masterKey, accountId) {
  return Buffer.from(crypto.hkdfSync(
    'sha256',
    masterKey,
    Buffer.from(String(accountId), 'utf8'),
    ACCOUNT_KEY_INFO,
    32
  ));
}

function encryptBuffer(key, plaintext, aad) {
  const iv = crypto.randomBytes(12);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  if (aad) cipher.setAAD(Buffer.from(aad));
  const ciphertext = Buffer.concat([cipher.update(plaintext), cipher.final()]);
  const tag = cipher.getAuthTag();
  return { iv, tag, ciphertext };
}

function decryptBuffer(key, payload, aad) {
  const decipher = crypto.createDecipheriv('aes-256-gcm', key, payload.iv);
  if (aad) decipher.setAAD(Buffer.from(aad));
  decipher.setAuthTag(payload.tag);
  return Buffer.concat([decipher.update(payload.ciphertext), decipher.final()]);
}

function isDirectoryEmpty(dir) {
  try { return fs.readdirSync(dir).length === 0; } catch (_) { return true; }
}

function walkFiles(root) {
  const base = path.resolve(root);
  const files = [];
  function visit(current) {
    for (const entry of fs.readdirSync(current, { withFileTypes: true })) {
      const absolute = path.join(current, entry.name);
      if (entry.isSymbolicLink()) continue;
      if (entry.isDirectory()) visit(absolute);
      else if (entry.isFile()) files.push(absolute);
    }
  }
  if (fs.existsSync(base)) visit(base);
  return files.sort();
}

function relativeSafe(base, absolute) {
  const rel = path.relative(base, absolute);
  if (!rel || rel.startsWith('..') || path.isAbsolute(rel)) throw vaultError('UNSAFE_PROFILE_PATH', 'Profile contains an unsafe path.');
  return rel.split(path.sep).join('/');
}

function targetSafe(base, relativePath) {
  const normalized = String(relativePath || '').split('/').join(path.sep);
  const target = path.resolve(base, normalized);
  const root = `${path.resolve(base)}${path.sep}`;
  if (!target.startsWith(root)) throw vaultError('UNSAFE_PROFILE_PATH', 'Encrypted profile manifest contains an unsafe path.');
  return target;
}

function removeDirectory(dir) {
  fs.rmSync(dir, { recursive: true, force: true });
}

function copyDirectory(source, target) {
  removeDirectory(target);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.cpSync(source, target, { recursive: true, force: true, dereference: false });
}

class ProfileVault {
  constructor(layout) {
    if (!layout?.vaultDir || !layout?.unlockedProfilesDir || !layout?.backupsDir) {
      throw new Error('ProfileVault requires vaultDir, unlockedProfilesDir and backupsDir.');
    }
    this.layout = layout;
    this.configFile = path.join(layout.vaultDir, 'vault.json');
    this.indexFile = path.join(layout.vaultDir, 'index.json');
    this.accountsVaultDir = path.join(layout.vaultDir, 'accounts');
    this.sessionMarker = path.join(layout.unlockedProfilesDir, 'vault-session.json');
    fs.mkdirSync(this.accountsVaultDir, { recursive: true });
    fs.mkdirSync(layout.unlockedProfilesDir, { recursive: true });
    fs.mkdirSync(layout.backupsDir, { recursive: true });
    if (!readJson(this.indexFile, null)) writeJsonAtomic(this.indexFile, { version: 1, accounts: {}, updatedAt: Date.now() });

    this._masterKey = null;
    this.state = 'LOCKED';
    this.recoveryRequired = fs.existsSync(this.sessionMarker);
    const previous = readJson(this.sessionMarker, null);
    this.dirtyAccounts = new Set(Array.isArray(previous?.dirtyAccounts) ? previous.dirtyAccounts.map(String) : []);
    if (this.recoveryRequired && this.dirtyAccounts.size) this.state = 'LOCKED';
  }

  isInitialized() {
    return Boolean(readJson(this.configFile, null));
  }

  _requireUnlocked() {
    if (!this._masterKey || !['UNLOCKED', 'RESEAL_REQUIRED'].includes(this.state)) {
      throw vaultError('VAULT_LOCKED', 'Vault is locked.', 423);
    }
  }

  _writeSessionMarker() {
    if (!this._masterKey) return;
    writeJsonAtomic(this.sessionMarker, {
      version: 1,
      pid: process.pid,
      startedAt: Number(readJson(this.sessionMarker, {})?.startedAt) || Date.now(),
      updatedAt: Date.now(),
      dirtyAccounts: [...this.dirtyAccounts].sort(),
      recoveryRequired: this.recoveryRequired
    });
  }

  initialize(password) {
    if (this.isInitialized()) throw vaultError('VAULT_ALREADY_INITIALIZED', 'Vault is already initialized.');
    const salt = crypto.randomBytes(16);
    const key = deriveMasterKey(password, salt, KDF);
    const verifier = verifierForKey(key);
    const now = Date.now();
    writeJsonAtomic(this.configFile, {
      version: VAULT_VERSION,
      kdf: {
        name: KDF.name,
        salt: salt.toString('base64'),
        N: KDF.N,
        r: KDF.r,
        p: KDF.p,
        keyLen: KDF.keyLen,
        maxmem: KDF.maxmem
      },
      verifier: verifier.toString('base64'),
      initializedAt: now,
      updatedAt: now
    });
    key.fill(0);
    return this.unlock(password);
  }

  unlock(password) {
    const config = readJson(this.configFile, null);
    if (!config) throw vaultError('VAULT_NOT_INITIALIZED', 'Vault is not initialized.', 412);
    if (Number(config.version) !== VAULT_VERSION) throw vaultError('VAULT_VERSION_UNSUPPORTED', 'Vault version is not supported.');
    this.state = 'UNLOCKING';
    try {
      const salt = Buffer.from(String(config.kdf?.salt || ''), 'base64');
      const key = deriveMasterKey(password, salt, config.kdf || KDF);
      const actual = verifierForKey(key);
      const expected = Buffer.from(String(config.verifier || ''), 'base64');
      if (actual.length !== expected.length || !crypto.timingSafeEqual(actual, expected)) {
        key.fill(0);
        throw vaultError('VAULT_UNLOCK_FAILED', 'Vault password is incorrect.', 401);
      }
      if (this._masterKey) this._masterKey.fill(0);
      this._masterKey = key;
      this.state = this.dirtyAccounts.size ? 'RESEAL_REQUIRED' : 'UNLOCKED';
      this._writeSessionMarker();
      return this.status();
    } catch (error) {
      this.state = 'LOCKED';
      if (error.code) throw error;
      throw vaultError('VAULT_UNLOCK_FAILED', 'Vault could not be unlocked.', 401);
    }
  }

  accountPackageDir(accountId) {
    return path.join(this.accountsVaultDir, safeSegment(accountId, 'account'));
  }

  workingDir(accountId) {
    return path.join(this.layout.unlockedProfilesDir, safeSegment(accountId, 'account'));
  }

  _readIndex() {
    const index = readJson(this.indexFile, { version: 1, accounts: {} }) || { version: 1, accounts: {} };
    index.accounts ||= {};
    return index;
  }

  _writeIndex(index) {
    index.version = 1;
    index.updatedAt = Date.now();
    writeJsonAtomic(this.indexFile, index);
  }

  _manifestEnvelope(packageDir) {
    const envelope = readJson(path.join(packageDir, 'manifest.enc.json'), null);
    if (!envelope) throw vaultError('SEALED_PROFILE_INVALID', 'Encrypted profile manifest is missing or invalid.');
    return {
      iv: Buffer.from(String(envelope.iv || ''), 'base64'),
      tag: Buffer.from(String(envelope.tag || ''), 'base64'),
      ciphertext: Buffer.from(String(envelope.ciphertext || ''), 'base64')
    };
  }

  sealProfile(accountId, sourceDir, options = {}) {
    this._requireUnlocked();
    const id = String(accountId || '').trim();
    if (!id) throw vaultError('BAD_ACCOUNT_ID', 'accountId is required.', 400);
    const source = path.resolve(String(sourceDir || ''));
    if (!fs.existsSync(source) || !fs.statSync(source).isDirectory()) {
      throw vaultError('PROFILE_SOURCE_MISSING', 'Profile source directory does not exist.', 400);
    }
    const key = accountKey(this._masterKey, id);
    const target = this.accountPackageDir(id);
    const next = `${target}.next-${crypto.randomUUID()}`;
    const blobsDir = path.join(next, 'files');
    fs.mkdirSync(blobsDir, { recursive: true });
    let totalBytes = 0;
    const manifest = { version: 1, accountId: id, files: [], sealedAt: Date.now() };
    try {
      const files = walkFiles(source);
      files.forEach((absolute, index) => {
        const relativePath = relativeSafe(source, absolute);
        const stat = fs.statSync(absolute);
        const plaintext = fs.readFileSync(absolute);
        totalBytes += plaintext.length;
        const aad = Buffer.from(`${id}\0${relativePath}`, 'utf8');
        const encrypted = encryptBuffer(key, plaintext, aad);
        plaintext.fill(0);
        const blobName = `${String(index).padStart(8, '0')}.bin`;
        fs.writeFileSync(path.join(blobsDir, blobName), encrypted.ciphertext);
        manifest.files.push({
          path: relativePath,
          blob: blobName,
          iv: encrypted.iv.toString('base64'),
          tag: encrypted.tag.toString('base64'),
          size: stat.size,
          mtimeMs: Math.round(stat.mtimeMs),
          mode: stat.mode
        });
      });
      const manifestBytes = Buffer.from(JSON.stringify(manifest), 'utf8');
      const encryptedManifest = encryptBuffer(key, manifestBytes, MANIFEST_AAD);
      manifestBytes.fill(0);
      writeJsonAtomic(path.join(next, 'manifest.enc.json'), {
        version: 1,
        algorithm: 'aes-256-gcm',
        iv: encryptedManifest.iv.toString('base64'),
        tag: encryptedManifest.tag.toString('base64'),
        ciphertext: encryptedManifest.ciphertext.toString('base64')
      });

      const old = `${target}.old-${crypto.randomUUID()}`;
      if (fs.existsSync(target)) fs.renameSync(target, old);
      try {
        fs.renameSync(next, target);
        removeDirectory(old);
      } catch (error) {
        if (!fs.existsSync(target) && fs.existsSync(old)) fs.renameSync(old, target);
        throw error;
      }

      const index = this._readIndex();
      index.accounts[id] = {
        accountId: id,
        sealedAt: manifest.sealedAt,
        fileCount: manifest.files.length,
        totalBytes,
        package: path.relative(this.layout.vaultDir, target).split(path.sep).join('/')
      };
      this._writeIndex(index);
      this.dirtyAccounts.delete(id);
      this.state = this.dirtyAccounts.size ? 'RESEAL_REQUIRED' : 'UNLOCKED';
      this.recoveryRequired = this.dirtyAccounts.size > 0;
      this._writeSessionMarker();
      if (options.removeSource === true) removeDirectory(source);
      return { accountId: id, fileCount: manifest.files.length, totalBytes, sealedAt: manifest.sealedAt };
    } finally {
      key.fill(0);
      removeDirectory(next);
    }
  }

  unsealProfile(accountId, options = {}) {
    this._requireUnlocked();
    const id = String(accountId || '').trim();
    if (!id) throw vaultError('BAD_ACCOUNT_ID', 'accountId is required.', 400);
    const working = this.workingDir(id);
    if (fs.existsSync(working) && !isDirectoryEmpty(working) && options.force !== true) {
      throw vaultError('UNSEALED_PROFILE_EXISTS', 'Unlocked profile working directory already exists. Recovery or reseal is required.');
    }
    removeDirectory(working);
    fs.mkdirSync(working, { recursive: true });
    const packageDir = this.accountPackageDir(id);
    if (!fs.existsSync(packageDir)) {
      this.markDirty(id);
      return { accountId: id, workingDir: working, createdEmpty: true, fileCount: 0 };
    }

    const key = accountKey(this._masterKey, id);
    try {
      const manifestBytes = decryptBuffer(key, this._manifestEnvelope(packageDir), MANIFEST_AAD);
      let manifest;
      try { manifest = JSON.parse(manifestBytes.toString('utf8')); } finally { manifestBytes.fill(0); }
      if (manifest.accountId !== id || !Array.isArray(manifest.files)) throw vaultError('SEALED_PROFILE_INVALID', 'Encrypted profile manifest does not match the requested account.');
      for (const entry of manifest.files) {
        const target = targetSafe(working, entry.path);
        const blobPath = targetSafe(path.join(packageDir, 'files'), entry.blob);
        const encrypted = fs.readFileSync(blobPath);
        const aad = Buffer.from(`${id}\0${entry.path}`, 'utf8');
        const plaintext = decryptBuffer(key, {
          iv: Buffer.from(String(entry.iv || ''), 'base64'),
          tag: Buffer.from(String(entry.tag || ''), 'base64'),
          ciphertext: encrypted
        }, aad);
        fs.mkdirSync(path.dirname(target), { recursive: true });
        fs.writeFileSync(target, plaintext, { mode: Number(entry.mode) || undefined });
        plaintext.fill(0);
        if (Number.isFinite(Number(entry.mtimeMs))) {
          const when = new Date(Number(entry.mtimeMs));
          try { fs.utimesSync(target, when, when); } catch (_) {}
        }
      }
      this.markDirty(id);
      return { accountId: id, workingDir: working, createdEmpty: false, fileCount: manifest.files.length };
    } catch (error) {
      removeDirectory(working);
      if (error.code) throw error;
      throw vaultError('SEALED_PROFILE_DECRYPT_FAILED', 'Encrypted profile could not be decrypted.', 422);
    } finally {
      key.fill(0);
    }
  }

  markDirty(accountId) {
    this._requireUnlocked();
    const id = String(accountId || '').trim();
    if (!id) throw vaultError('BAD_ACCOUNT_ID', 'accountId is required.', 400);
    this.dirtyAccounts.add(id);
    this.state = 'RESEAL_REQUIRED';
    this.recoveryRequired = true;
    this._writeSessionMarker();
    return this.status();
  }

  resealProfile(accountId) {
    this._requireUnlocked();
    const id = String(accountId || '').trim();
    const working = this.workingDir(id);
    if (!fs.existsSync(working)) throw vaultError('UNSEALED_PROFILE_MISSING', 'Unlocked profile working directory is missing.');
    return this.sealProfile(id, working, { removeSource: true });
  }

  backupSealedProfile(accountId) {
    const id = String(accountId || '').trim();
    const source = this.accountPackageDir(id);
    if (!fs.existsSync(source)) throw vaultError('SEALED_PROFILE_MISSING', 'No sealed profile package exists for this account.', 404);
    const stamp = new Date().toISOString().replace(/[:.]/g, '-');
    const target = path.join(this.layout.backupsDir, 'vault', `${stamp}-${safeSegment(id, 'account')}`);
    copyDirectory(source, target);
    return { accountId: id, backupDir: target };
  }

  lock(options = {}) {
    if (this.dirtyAccounts.size && options.force !== true) {
      throw vaultError('RESEAL_REQUIRED', 'One or more unlocked profiles must be resealed before locking.');
    }
    if (this._masterKey) this._masterKey.fill(0);
    this._masterKey = null;
    if (!this.dirtyAccounts.size) {
      for (const entry of fs.readdirSync(this.layout.unlockedProfilesDir, { withFileTypes: true })) {
        if (entry.name === path.basename(this.sessionMarker)) continue;
        removeDirectory(path.join(this.layout.unlockedProfilesDir, entry.name));
      }
      try { fs.unlinkSync(this.sessionMarker); } catch (_) {}
      this.recoveryRequired = false;
    } else {
      this.recoveryRequired = true;
    }
    this.state = 'LOCKED';
    return this.status();
  }

  status() {
    const index = this._readIndex();
    const unlockedDirs = [];
    try {
      for (const entry of fs.readdirSync(this.layout.unlockedProfilesDir, { withFileTypes: true })) {
        if (entry.isDirectory()) unlockedDirs.push(entry.name);
      }
    } catch (_) {}
    return {
      initialized: this.isInitialized(),
      state: this.state,
      recoveryRequired: this.recoveryRequired,
      dirtyAccounts: [...this.dirtyAccounts].sort(),
      sealedAccounts: Object.keys(index.accounts || {}).sort(),
      unlockedProfileDirs: unlockedDirs.sort(),
      algorithm: 'AES-256-GCM',
      kdf: 'scrypt',
      secretsExposed: false
    };
  }
}

module.exports = {
  ProfileVault,
  VAULT_VERSION,
  KDF,
  deriveMasterKey,
  encryptBuffer,
  decryptBuffer,
  vaultError
};
