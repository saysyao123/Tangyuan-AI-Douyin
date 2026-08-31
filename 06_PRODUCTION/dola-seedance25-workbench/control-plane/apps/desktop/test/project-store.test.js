'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const { buildPortableLayout, ensurePortableLayout } = require('../src/core/portable-paths');
const { ProjectStore } = require('../src/core/project-store');

function fixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'dola-project-store-'));
  const layout = buildPortableLayout(root);
  ensurePortableLayout(layout);
  const store = new ProjectStore(layout);
  return { root, layout, store };
}

function cleanup(root) {
  fs.rmSync(root, { recursive: true, force: true });
}

test('project name creates a stable project directory', () => {
  const { root, store } = fixture();
  try {
    const first = store.createProject({ name: 'MV 那封信' });
    const second = store.createProject({ name: 'MV 那封信', id: first.project.id });
    assert.equal(first.created, true);
    assert.equal(second.created, false);
    assert.equal(second.project.id, first.project.id);
    assert.equal(fs.existsSync(store.projectFile(first.project.id)), true);
  } finally { cleanup(root); }
});

test('same project shot revision is strongly idempotent', () => {
  const { root, store } = fixture();
  try {
    const project = store.createProject({ name: 'Idempotency Test' }).project;
    const request = {
      projectId: project.id,
      shotId: 'S01',
      revision: 1,
      mode: 't2v',
      prompt: 'A quiet rainy study.',
      duration: 5,
      ratio: '9:16'
    };
    const first = store.createJob(request);
    const second = store.createJob(request);
    assert.equal(first.created, true);
    assert.equal(second.created, false);
    assert.equal(second.job.id, first.job.id);
  } finally { cleanup(root); }
});

test('changing generation inputs under same revision raises idempotency conflict', () => {
  const { root, store } = fixture();
  try {
    const project = store.createProject({ name: 'Conflict Test' }).project;
    store.createJob({ projectId: project.id, shotId: 'S01', revision: 1, prompt: 'Prompt A', duration: 5 });
    assert.throws(
      () => store.createJob({ projectId: project.id, shotId: 'S01', revision: 1, prompt: 'Prompt B', duration: 5 }),
      (error) => error && error.code === 'IDEMPOTENCY_CONFLICT'
    );
  } finally { cleanup(root); }
});

test('explicit new revision creates a new job identity', () => {
  const { root, store } = fixture();
  try {
    const project = store.createProject({ name: 'Revision Test' }).project;
    const first = store.createJob({ projectId: project.id, shotId: 'S01', prompt: 'v1', duration: 5 }).job;
    const second = store.createNewRevision({ projectId: project.id, shotId: 'S01', prompt: 'v2', duration: 5 }).job;
    assert.equal(first.revision, 1);
    assert.equal(second.revision, 2);
    assert.notEqual(second.id, first.id);
  } finally { cleanup(root); }
});

test('i2v absolute source is staged inside project inputs', () => {
  const { root, store } = fixture();
  try {
    const source = path.join(root, 'source.png');
    fs.writeFileSync(source, Buffer.from([0x89, 0x50, 0x4e, 0x47]));
    const project = store.createProject({ name: 'I2V Test' }).project;
    const job = store.createJob({
      projectId: project.id,
      shotId: 'S01',
      mode: 'i2v',
      prompt: 'Animate this still.',
      duration: 5,
      sourceImagePath: source
    }).job;
    assert.equal(path.isAbsolute(job.stagedImagePath), true);
    assert.equal(fs.existsSync(job.stagedImagePath), true);
    assert.equal(job.stagedImagePath.startsWith(store.projectDir(project.id)), true);
  } finally { cleanup(root); }
});

test('project emits PROJECT_COMPLETE only after every created job succeeds', () => {
  const { root, store } = fixture();
  try {
    const project = store.createProject({ name: 'Completion Test' }).project;
    const a = store.createJob({ projectId: project.id, shotId: 'S01', prompt: 'one', duration: 5 }).job;
    const b = store.createJob({ projectId: project.id, shotId: 'S02', prompt: 'two', duration: 5 }).job;
    store.patchJob(a.id, { state: 'success' });
    assert.equal(store.projectResult(project.id).event, 'PROJECT_STATUS');
    store.patchJob(b.id, { state: 'success' });
    const result = store.projectResult(project.id);
    assert.equal(result.event, 'PROJECT_COMPLETE');
    assert.equal(result.outputs.length, 2);
  } finally { cleanup(root); }
});
