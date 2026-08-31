'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { readJson, writeJsonAtomic, safeSegment } = require('./atomic-json');

const PROVIDER_STATES = new Set([
  'PREPARING', 'SUBMITTING', 'SUBMITTED', 'ACKNOWLEDGED', 'GENERATING',
  'RESULT_OBSERVED', 'RESOLVING', 'SUCCESS', 'LOGIN_REQUIRED',
  'PROVIDER_REJECTED', 'OBSERVATION_WAIT', 'RECOVERY_REQUIRED', 'FAILED', 'CANCELLED'
]);

function normalizeState(value) {
  const state = String(value || '').trim().toUpperCase();
  if (!PROVIDER_STATES.has(state)) {
    const error = new Error(`Unsupported provider lifecycle state: ${state}`);
    error.code = 'BAD_PROVIDER_STATE';
    throw error;
  }
  return state;
}

class ProviderLifecycleStore {
  constructor(layoutOrStateDir) {
    const stateDir = typeof layoutOrStateDir === 'string'
      ? layoutOrStateDir
      : layoutOrStateDir?.stateDir;
    if (!stateDir) throw new Error('ProviderLifecycleStore requires stateDir.');
    this.dir = path.join(path.resolve(stateDir), 'provider-lifecycle');
    fs.mkdirSync(this.dir, { recursive: true });
  }

  file(taskId) {
    return path.join(this.dir, `${safeSegment(taskId, 'task')}.json`);
  }

  get(taskId) {
    return readJson(this.file(taskId), null);
  }

  begin(task, account) {
    const now = Date.now();
    const existing = this.get(task.id);
    if (existing) return existing;
    const record = {
      version: 1,
      taskId: String(task.id),
      accountId: String(account?.id || task.accountId || ''),
      provider: String(task.provider || 'dola-web-background'),
      state: 'PREPARING',
      submittedAt: null,
      lastObservedAt: null,
      conversationId: null,
      messageId: null,
      generationId: null,
      mediaObserved: false,
      outputPath: null,
      error: null,
      createdAt: now,
      updatedAt: now,
      history: [{ state: 'PREPARING', at: now, detail: 'lifecycle-created' }]
    };
    writeJsonAtomic(this.file(task.id), record);
    return record;
  }

  transition(taskId, stateValue, patch = {}, detail = '') {
    const state = normalizeState(stateValue);
    const current = this.get(taskId);
    if (!current) {
      const error = new Error('Provider lifecycle record not found.');
      error.code = 'LIFECYCLE_NOT_FOUND';
      error.statusCode = 404;
      throw error;
    }
    const now = Date.now();
    const next = {
      ...current,
      ...patch,
      state,
      updatedAt: now,
      history: [
        ...(Array.isArray(current.history) ? current.history : []),
        { state, at: now, ...(detail ? { detail: String(detail).slice(0, 240) } : {}) }
      ].slice(-200)
    };
    writeJsonAtomic(this.file(taskId), next);
    return next;
  }

  markSubmitted(taskId, patch = {}) {
    return this.transition(taskId, 'SUBMITTED', { submittedAt: Date.now(), ...patch }, 'provider-submit-clicked');
  }

  markObservationWait(taskId, patch = {}) {
    return this.transition(taskId, 'OBSERVATION_WAIT', {
      lastObservedAt: Date.now(),
      ...patch,
      error: null
    }, 'observation-window-ended-without-resubmission');
  }

  recoverable(taskId) {
    const record = this.get(taskId);
    if (!record) return false;
    return ['SUBMITTED', 'ACKNOWLEDGED', 'GENERATING', 'OBSERVATION_WAIT', 'RECOVERY_REQUIRED', 'RESULT_OBSERVED', 'RESOLVING'].includes(record.state);
  }

  list() {
    const items = [];
    for (const entry of fs.readdirSync(this.dir, { withFileTypes: true })) {
      if (!entry.isFile() || !entry.name.endsWith('.json')) continue;
      const value = readJson(path.join(this.dir, entry.name), null);
      if (value) items.push(value);
    }
    return items.sort((a, b) => Number(b.updatedAt || 0) - Number(a.updatedAt || 0));
  }
}

module.exports = { ProviderLifecycleStore, PROVIDER_STATES, normalizeState };
