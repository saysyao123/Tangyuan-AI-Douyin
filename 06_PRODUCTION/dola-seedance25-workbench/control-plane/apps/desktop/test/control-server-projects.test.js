'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const { startControlServer } = require('../src/control-server');
const { buildPortableLayout, ensurePortableLayout } = require('../src/core/portable-paths');
const { ProjectStore } = require('../src/core/project-store');

async function jsonRequest(runtime, method, route, body) {
  const response = await fetch(`http://127.0.0.1:${runtime.info.port}${route}`, {
    method,
    headers: {
      authorization: `Bearer ${runtime.info.token}`,
      ...(body === undefined ? {} : { 'content-type': 'application/json' })
    },
    body: body === undefined ? undefined : JSON.stringify(body)
  });
  return { status: response.status, body: await response.json() };
}

test('project routes expose idempotent durable jobs and project result', async () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'dola-control-projects-'));
  const controlRoot = path.join(root, 'control');
  const previousControlDir = process.env.SEEDANCE_STUDIO_CONTROL_DIR;
  process.env.SEEDANCE_STUDIO_CONTROL_DIR = controlRoot;
  const layout = buildPortableLayout(path.join(root, 'portable'));
  ensurePortableLayout(layout);
  const store = new ProjectStore(layout);
  let runtime;
  try {
    runtime = await startControlServer({
      health: async () => ({ ok: true }),
      listProjects: async () => store.listProjects(),
      createProject: async (input) => store.createProject(input),
      getProject: async (id) => store.getProject(id),
      listProjectJobs: async (id) => store.listJobs(id),
      createProjectJob: async (input) => store.createJob(input),
      createProjectJobRevision: async (input) => store.createNewRevision(input),
      getProjectJob: async (id) => store.getJob(id),
      getProjectResult: async (id) => store.projectResult(id)
    });

    const createdProject = await jsonRequest(runtime, 'POST', '/v1/projects', { name: 'API Project' });
    assert.equal(createdProject.status, 201);
    const projectId = createdProject.body.project.id;

    const jobInput = { shotId: 'S01', prompt: 'Rainy room.', duration: 5, ratio: '9:16' };
    const first = await jsonRequest(runtime, 'POST', `/v1/projects/${encodeURIComponent(projectId)}/jobs`, jobInput);
    assert.equal(first.status, 201);
    const duplicate = await jsonRequest(runtime, 'POST', `/v1/projects/${encodeURIComponent(projectId)}/jobs`, jobInput);
    assert.equal(duplicate.status, 200);
    assert.equal(duplicate.body.job.id, first.body.job.id);

    const listed = await jsonRequest(runtime, 'GET', `/v1/projects/${encodeURIComponent(projectId)}/jobs`);
    assert.equal(listed.status, 200);
    assert.equal(listed.body.jobs.length, 1);

    store.patchJob(first.body.job.id, { state: 'success' });
    const result = await jsonRequest(runtime, 'GET', `/v1/projects/${encodeURIComponent(projectId)}/result`);
    assert.equal(result.status, 200);
    assert.equal(result.body.event, 'PROJECT_COMPLETE');
    assert.equal(result.body.outputs.length, 1);
  } finally {
    if (runtime) await runtime.stop();
    if (previousControlDir === undefined) delete process.env.SEEDANCE_STUDIO_CONTROL_DIR;
    else process.env.SEEDANCE_STUDIO_CONTROL_DIR = previousControlDir;
    fs.rmSync(root, { recursive: true, force: true });
  }
});
