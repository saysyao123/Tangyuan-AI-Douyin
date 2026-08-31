'use strict';

const path = require('node:path');
const { readJson, writeJsonAtomic } = require('./atomic-json');
const { normalizeMaxWorkers, normalizeIdleMs } = require('./worker-scheduler');

class WorkerConfigStore {
  constructor(layout) {
    if (!layout?.stateDir) throw new Error('WorkerConfigStore requires layout.stateDir');
    this.file = path.join(layout.stateDir, 'worker-settings.json');
    if (!readJson(this.file, null)) this.save({ maxWorkers: 3, idleMs: 5 * 60 * 1000 });
  }

  load() {
    const raw = readJson(this.file, {}) || {};
    return {
      version: 1,
      maxWorkers: normalizeMaxWorkers(raw.maxWorkers, 3),
      idleMs: normalizeIdleMs(raw.idleMs, 5 * 60 * 1000),
      updatedAt: Number(raw.updatedAt) || null
    };
  }

  save(input = {}) {
    const current = readJson(this.file, {}) || {};
    const next = {
      version: 1,
      maxWorkers: normalizeMaxWorkers(input.maxWorkers, current.maxWorkers ?? 3),
      idleMs: normalizeIdleMs(input.idleMs, current.idleMs ?? 5 * 60 * 1000),
      updatedAt: Date.now()
    };
    writeJsonAtomic(this.file, next);
    return next;
  }
}

module.exports = { WorkerConfigStore };
