'use strict';

const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const { readJson, writeJsonAtomic } = require('./atomic-json');

const ACCOUNT_STATUSES = new Set([
  'UNKNOWN', 'NEEDS_LOGIN', 'READY', 'BUSY', 'PAUSED', 'ERROR', 'RESTRICTED'
]);
const QUOTA_STATES = new Set(['UNKNOWN', 'AVAILABLE', 'LOW', 'EXHAUSTED']);
const ENTITLEMENT_STATES = new Set(['UNKNOWN', 'AVAILABLE', 'UNAVAILABLE']);

function cleanText(value, fallback = '', max = 160) {
  return String(value ?? fallback).replace(/[\r\n\t]/g, ' ').trim().slice(0, max);
}

function normalizeStatus(value, fallback = 'UNKNOWN') {
  const status = cleanText(value, fallback, 32).toUpperCase();
  return ACCOUNT_STATUSES.has(status) ? status : fallback;
}

function normalizeCapabilityBool(value) {
  return value === true || value === false ? value : 'unknown';
}

function normalizeDurationState(value) {
  const text = cleanText(value, 'unknown', 24).toLowerCase();
  if (['available', 'unavailable', 'experimental', 'unknown'].includes(text)) return text;
  if (value === true) return 'available';
  if (value === false) return 'unavailable';
  return 'unknown';
}

function normalizeHealth(value = {}) {
  const loginStatus = cleanText(value.loginStatus, 'unknown', 32).toLowerCase();
  return {
    loginStatus: ['logged_in', 'logged_out', 'unknown'].includes(loginStatus) ? loginStatus : 'unknown',
    pageLoaded: value.pageLoaded === true,
    evidence: cleanText(value.evidence, '', 160),
    pagePath: cleanText(value.pagePath, '', 500),
    checkedAt: Number(value.checkedAt) || null
  };
}

function normalizeCapabilities(value = {}) {
  const quota = cleanText(value.quotaStatus, 'UNKNOWN', 24).toUpperCase();
  const entitlement = cleanText(value.entitlementStatus, 'UNKNOWN', 24).toUpperCase();
  const durations = value.durationSeconds || value.durations || {};
  const getDuration = (seconds) => {
    if (Array.isArray(durations)) return durations.includes(seconds) ? 'available' : 'unknown';
    return normalizeDurationState(durations?.[seconds] ?? durations?.[String(seconds)]);
  };
  return {
    t2v: normalizeCapabilityBool(value.t2v),
    i2v: normalizeCapabilityBool(value.i2v),
    durations: { 5: getDuration(5), 10: getDuration(10), 30: getDuration(30) },
    quotaStatus: QUOTA_STATES.has(quota) ? quota : 'UNKNOWN',
    entitlementStatus: ENTITLEMENT_STATES.has(entitlement) ? entitlement : 'UNKNOWN',
    lastCheckedAt: Number(value.lastCheckedAt) || null
  };
}

function normalizeAccount(value = {}, previous = null) {
  const id = cleanText(value.id || previous?.id, '', 80);
  if (!/^[a-zA-Z0-9_-]{6,80}$/.test(id)) {
    const error = new Error('account id must contain 6-80 letters, digits, underscore or dash');
    error.code = 'BAD_ACCOUNT_ID';
    throw error;
  }
  const status = normalizeStatus(value.status ?? previous?.status, previous?.status || 'UNKNOWN');
  const enabled = value.enabled === undefined ? (previous?.enabled !== false) : value.enabled === true;
  const pauseReason = cleanText(value.pauseReason ?? previous?.pauseReason, '', 240);
  const restrictionCode = cleanText(value.restrictionCode ?? previous?.restrictionCode, '', 80).toUpperCase();
  const capabilities = normalizeCapabilities({ ...(previous?.capabilities || {}), ...(value.capabilities || {}) });
  const health = normalizeHealth({ ...(previous?.health || {}), ...(value.health || {}) });
  const now = Date.now();
  return {
    id,
    name: cleanText(value.name ?? previous?.name, 'Dola Account', 80) || 'Dola Account',
    partition: cleanText(value.partition ?? previous?.partition, `persist:dola_${id}`, 160) || `persist:dola_${id}`,
    enabled,
    status,
    pauseReason,
    restrictionCode,
    source: cleanText(value.source ?? previous?.source, 'portable', 32) || 'portable',
    capabilities,
    health,
    createdAt: Number(value.createdAt ?? previous?.createdAt) || now,
    updatedAt: now,
    lastError: cleanText(value.lastError ?? previous?.lastError, '', 500),
    lastCheckedAt: Number(value.lastCheckedAt ?? previous?.lastCheckedAt) || null
  };
}

function schedulingReason(account) {
  if (!account) return 'ACCOUNT_NOT_FOUND';
  if (account.status === 'PAUSED') return 'ACCOUNT_PAUSED';
  if (account.enabled !== true) return 'ACCOUNT_DISABLED';
  if (account.status === 'RESTRICTED' || account.restrictionCode) return account.restrictionCode || 'ACCOUNT_RESTRICTED';
  if (account.capabilities?.quotaStatus === 'EXHAUSTED') return 'QUOTA_EXHAUSTED';
  if (account.capabilities?.entitlementStatus === 'UNAVAILABLE') return 'ENTITLEMENT_UNAVAILABLE';
  if (account.health?.loginStatus === 'logged_out' || account.status === 'NEEDS_LOGIN') return 'LOGIN_REQUIRED';
  if (account.status !== 'READY') return `ACCOUNT_${account.status || 'UNKNOWN'}`;
  return null;
}

function publicAccount(account) {
  const reason = schedulingReason(account);
  return { ...account, schedulable: reason === null, schedulingReason: reason };
}

class AccountRegistry {
  constructor(layout) {
    if (!layout?.accountsDir) throw new Error('AccountRegistry requires layout.accountsDir');
    this.layout = layout;
    this.registryFile = path.join(layout.accountsDir, 'registry.json');
    fs.mkdirSync(layout.accountsDir, { recursive: true });
    if (!readJson(this.registryFile, null)) {
      writeJsonAtomic(this.registryFile, { version: 1, accounts: [], updatedAt: Date.now() });
    }
  }

  _read() {
    const parsed = readJson(this.registryFile, { version: 1, accounts: [] }) || { version: 1, accounts: [] };
    return { version: 1, accounts: Array.isArray(parsed.accounts) ? parsed.accounts : [], updatedAt: Number(parsed.updatedAt) || null };
  }

  _write(accounts) {
    const payload = { version: 1, accounts, updatedAt: Date.now() };
    writeJsonAtomic(this.registryFile, payload);
    return payload;
  }

  list() {
    return this._read().accounts.map(publicAccount);
  }

  get(id) {
    const account = this._read().accounts.find((item) => item.id === String(id || '')) || null;
    return account ? publicAccount(account) : null;
  }

  create(input = {}) {
    const id = cleanText(input.id, '', 80) || crypto.randomUUID().replace(/-/g, '');
    if (this.get(id)) {
      const error = new Error('Account already exists');
      error.code = 'ACCOUNT_EXISTS';
      throw error;
    }
    const account = normalizeAccount({ ...input, id, source: input.source || 'portable', status: input.status || 'NEEDS_LOGIN' });
    const state = this._read();
    state.accounts.push(account);
    this._write(state.accounts);
    return publicAccount(account);
  }

  upsert(input = {}) {
    const id = cleanText(input.id, '', 80);
    if (!id) {
      const error = new Error('account id is required');
      error.code = 'BAD_ACCOUNT_ID';
      throw error;
    }
    const state = this._read();
    const index = state.accounts.findIndex((item) => item.id === id);
    const previous = index >= 0 ? state.accounts[index] : null;
    const account = normalizeAccount({ ...input, id }, previous);
    if (index >= 0) state.accounts[index] = account;
    else state.accounts.push(account);
    this._write(state.accounts);
    return publicAccount(account);
  }

  syncLegacy(accounts = []) {
    for (const legacy of Array.isArray(accounts) ? accounts : []) {
      if (!legacy?.id) continue;
      const current = this.get(legacy.id);
      const preserveLocalState = current && ['PAUSED', 'RESTRICTED'].includes(current.status);
      this.upsert({
        id: legacy.id,
        name: legacy.name,
        partition: legacy.partition,
        createdAt: legacy.createdAt,
        source: current?.source || 'legacy-poc',
        status: preserveLocalState ? current.status : (legacy.status || current?.status || 'UNKNOWN'),
        lastError: legacy.lastError ?? current?.lastError,
        lastCheckedAt: legacy.lastCheckedAt ?? current?.lastCheckedAt,
        enabled: current?.enabled !== false,
        pauseReason: current?.pauseReason || '',
        restrictionCode: current?.restrictionCode || '',
        capabilities: current?.capabilities || {},
        health: current?.health || {}
      });
    }
    return this.list();
  }

  patch(id, patch = {}) {
    const current = this.get(id);
    if (!current) {
      const error = new Error('Account not found');
      error.code = 'ACCOUNT_NOT_FOUND';
      error.statusCode = 404;
      throw error;
    }
    return this.upsert({ ...current, ...patch, id: current.id, createdAt: current.createdAt });
  }

  pause(id, reason = 'MANUAL_PAUSE') {
    return this.patch(id, { enabled: false, status: 'PAUSED', pauseReason: cleanText(reason, 'MANUAL_PAUSE', 240) || 'MANUAL_PAUSE' });
  }

  resume(id) {
    const current = this.get(id);
    if (!current) {
      const error = new Error('Account not found');
      error.code = 'ACCOUNT_NOT_FOUND';
      error.statusCode = 404;
      throw error;
    }
    let status = current.health?.loginStatus === 'logged_out' ? 'NEEDS_LOGIN' : 'READY';
    if (current.restrictionCode || current.capabilities?.quotaStatus === 'EXHAUSTED' || current.capabilities?.entitlementStatus === 'UNAVAILABLE') status = 'RESTRICTED';
    return this.patch(id, { enabled: true, status, pauseReason: '' });
  }

  recordHealth(id, health = {}) {
    const current = this.get(id);
    if (!current) {
      const error = new Error('Account not found');
      error.code = 'ACCOUNT_NOT_FOUND';
      error.statusCode = 404;
      throw error;
    }
    const mergedHealth = normalizeHealth({ ...current.health, ...health, checkedAt: health.checkedAt || Date.now() });
    let status = current.status;
    if (current.status !== 'PAUSED' && current.status !== 'RESTRICTED') {
      if (mergedHealth.loginStatus === 'logged_in') status = current.status === 'BUSY' ? 'BUSY' : 'READY';
      if (mergedHealth.loginStatus === 'logged_out') status = 'NEEDS_LOGIN';
    }
    return this.patch(id, { health: mergedHealth, status, lastCheckedAt: mergedHealth.checkedAt });
  }

  recordCapabilities(id, capabilities = {}) {
    const current = this.get(id);
    if (!current) {
      const error = new Error('Account not found');
      error.code = 'ACCOUNT_NOT_FOUND';
      error.statusCode = 404;
      throw error;
    }
    const normalized = normalizeCapabilities({ ...current.capabilities, ...capabilities, lastCheckedAt: capabilities.lastCheckedAt || Date.now() });
    let restrictionCode = current.restrictionCode;
    let status = current.status;
    if (normalized.quotaStatus === 'EXHAUSTED') restrictionCode = 'QUOTA_EXHAUSTED';
    else if (normalized.entitlementStatus === 'UNAVAILABLE') restrictionCode = 'ENTITLEMENT_UNAVAILABLE';
    else if (['QUOTA_EXHAUSTED', 'ENTITLEMENT_UNAVAILABLE'].includes(restrictionCode)) restrictionCode = '';
    if (restrictionCode && status !== 'PAUSED') status = 'RESTRICTED';
    else if (!restrictionCode && status === 'RESTRICTED') status = current.health?.loginStatus === 'logged_out' ? 'NEEDS_LOGIN' : 'READY';
    return this.patch(id, { capabilities: normalized, restrictionCode, status });
  }

  healthSummary() {
    const accounts = this.list();
    const counts = {};
    for (const account of accounts) counts[account.status] = (counts[account.status] || 0) + 1;
    return {
      total: accounts.length,
      schedulable: accounts.filter((item) => item.schedulable).length,
      enabled: accounts.filter((item) => item.enabled).length,
      counts,
      accounts
    };
  }
}

module.exports = { AccountRegistry, ACCOUNT_STATUSES, normalizeAccount, normalizeCapabilities, normalizeHealth, schedulingReason, publicAccount };
