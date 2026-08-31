'use strict';

const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const { readJson, writeJsonAtomic, safeSegment } = require('./atomic-json');

const TERMINAL_STATES = new Set(['success', 'failed', 'cancelled']);

function sha(value, length = 16) {
  return crypto.createHash('sha256').update(String(value)).digest('hex').slice(0, length);
}

function normalizeRevision(value) {
  const revision = Number(value ?? 1);
  if (!Number.isInteger(revision) || revision < 1 || revision > 9999) {
    const error = new Error('revision must be an integer from 1 to 9999');
    error.code = 'BAD_REVISION';
    throw error;
  }
  return revision;
}

function normalizeShotId(value) {
  const shotId = safeSegment(value, 'shot');
  if (!shotId || shotId === 'shot' && !String(value || '').trim()) {
    const error = new Error('shotId is required');
    error.code = 'BAD_SHOT_ID';
    throw error;
  }
  return shotId;
}

function normalizeProjectId(value, name) {
  if (value) return safeSegment(value, `project_${sha(value, 8)}`);
  const base = safeSegment(name, 'project');
  return `${base}_${sha(String(name || base), 8)}`;
}

function normalizeSourceImagePath(value) {
  if (!value) return null;
  const raw = String(value).trim();
  if (!path.isAbsolute(raw)) {
    const error = new Error('sourceImagePath must be an absolute local path');
    error.code = 'BAD_SOURCE_IMAGE';
    throw error;
  }
  return path.normalize(raw);
}

function stableJobFingerprint(input) {
  const normalized = {
    projectId: String(input.projectId),
    shotId: String(input.shotId),
    revision: Number(input.revision),
    provider: String(input.provider || 'dola-web'),
    mode: String(input.mode || 't2v'),
    model: String(input.model || 'seedance-v2.5'),
    duration: Number(input.duration || 10),
    ratio: String(input.ratio || '9:16'),
    prompt: String(input.prompt || ''),
    sourceImagePath: input.sourceImagePath ? path.normalize(String(input.sourceImagePath)) : null,
    requestedAccountId: input.requestedAccountId ? String(input.requestedAccountId) : null
  };
  return crypto.createHash('sha256').update(JSON.stringify(normalized)).digest('hex');
}

class ProjectStore {
  constructor(layout) {
    if (!layout?.projectsDir || !layout?.outputsDir || !layout?.stateDir) {
      throw new Error('ProjectStore requires a portable layout.');
    }
    this.layout = layout;
    this.jobIndexPath = path.join(layout.stateDir, 'job-index.json');
    fs.mkdirSync(layout.projectsDir, { recursive: true });
    fs.mkdirSync(layout.outputsDir, { recursive: true });
    fs.mkdirSync(layout.stateDir, { recursive: true });
  }

  projectDir(projectId) {
    return path.join(this.layout.projectsDir, safeSegment(projectId));
  }

  projectFile(projectId) {
    return path.join(this.projectDir(projectId), 'project.json');
  }

  jobsDir(projectId) {
    return path.join(this.projectDir(projectId), 'jobs');
  }

  inputsDir(projectId, shotId, revision) {
    return path.join(this.projectDir(projectId), 'inputs', safeSegment(shotId), `v${revision}`);
  }

  createProject(input = {}) {
    const name = String(input.name || '').trim();
    if (!name) {
      const error = new Error('project name is required');
      error.code = 'BAD_PROJECT_NAME';
      throw error;
    }
    const id = normalizeProjectId(input.id, name);
    const existing = this.getProject(id);
    if (existing) return { created: false, project: existing };
    const now = Date.now();
    const project = {
      id,
      name: name.slice(0, 160),
      status: 'active',
      createdAt: now,
      updatedAt: now,
      completedAt: null
    };
    fs.mkdirSync(this.jobsDir(id), { recursive: true });
    writeJsonAtomic(this.projectFile(id), project);
    return { created: true, project };
  }

  getProject(projectId) {
    return readJson(this.projectFile(projectId), null);
  }

  listProjects() {
    let entries = [];
    try { entries = fs.readdirSync(this.layout.projectsDir, { withFileTypes: true }); } catch (_) {}
    return entries
      .filter((entry) => entry.isDirectory())
      .map((entry) => this.getProject(entry.name))
      .filter(Boolean)
      .sort((a, b) => Number(b.updatedAt || 0) - Number(a.updatedAt || 0));
  }

  stageSourceImage(projectId, shotId, revision, sourceImagePath) {
    if (!sourceImagePath) return null;
    const absolute = normalizeSourceImagePath(sourceImagePath);
    if (!fs.existsSync(absolute) || !fs.statSync(absolute).isFile()) {
      const error = new Error('sourceImagePath must reference an existing absolute local file');
      error.code = 'BAD_SOURCE_IMAGE';
      throw error;
    }
    const dir = this.inputsDir(projectId, shotId, revision);
    fs.mkdirSync(dir, { recursive: true });
    const ext = path.extname(absolute).slice(0, 16);
    const base = safeSegment(path.basename(absolute, ext), 'input');
    const target = path.join(dir, `${base}${ext}`);
    fs.copyFileSync(absolute, target);
    return target;
  }

  outputPath(projectId, shotId, revision) {
    const dir = path.join(this.layout.outputsDir, safeSegment(projectId), safeSegment(shotId));
    return path.join(dir, `v${revision}.mp4`);
  }

  createJob(input = {}) {
    const project = this.getProject(input.projectId);
    if (!project) {
      const error = new Error('Unknown projectId');
      error.code = 'PROJECT_NOT_FOUND';
      throw error;
    }
    const shotId = normalizeShotId(input.shotId);
    const revision = normalizeRevision(input.revision);
    const idempotencyKey = `${project.id}:${shotId}:v${revision}`;
    const jobId = `job_${sha(idempotencyKey, 20)}`;
    const existing = this.getJob(jobId);

    const normalized = {
      projectId: project.id,
      shotId,
      revision,
      provider: String(input.provider || 'dola-web'),
      mode: String(input.mode || 't2v'),
      model: String(input.model || 'seedance-v2.5'),
      duration: Number(input.duration || 10),
      ratio: String(input.ratio || '9:16'),
      prompt: String(input.prompt || '').trim(),
      sourceImagePath: normalizeSourceImagePath(input.sourceImagePath),
      requestedAccountId: input.requestedAccountId ? String(input.requestedAccountId) : null
    };
    if (!normalized.prompt) {
      const error = new Error('prompt is required');
      error.code = 'BAD_PROMPT';
      throw error;
    }
    if (!['t2v', 'i2v'].includes(normalized.mode)) {
      const error = new Error('mode must be t2v or i2v');
      error.code = 'BAD_MODE';
      throw error;
    }
    if (normalized.mode === 'i2v' && !normalized.sourceImagePath) {
      const error = new Error('sourceImagePath is required for i2v');
      error.code = 'BAD_SOURCE_IMAGE';
      throw error;
    }

    const fingerprint = stableJobFingerprint({ ...normalized, projectId: project.id, shotId, revision });
    if (existing) {
      if (existing.requestFingerprint !== fingerprint) {
        const error = new Error('The same project/shot/revision already exists with different generation inputs. Create a new revision.');
        error.code = 'IDEMPOTENCY_CONFLICT';
        error.existingJobId = existing.id;
        throw error;
      }
      return { created: false, job: existing };
    }

    const stagedImagePath = this.stageSourceImage(project.id, shotId, revision, normalized.sourceImagePath);
    const now = Date.now();
    const job = {
      id: jobId,
      idempotencyKey,
      requestFingerprint: fingerprint,
      projectId: project.id,
      shotId,
      revision,
      provider: normalized.provider,
      mode: normalized.mode,
      model: normalized.model,
      duration: normalized.duration,
      ratio: normalized.ratio,
      prompt: normalized.prompt,
      requestedAccountId: normalized.requestedAccountId,
      assignedAccountId: null,
      sourceImagePath: normalized.sourceImagePath,
      stagedImagePath,
      outputPath: this.outputPath(project.id, shotId, revision),
      state: 'queued',
      error: null,
      recoveryCount: 0,
      createdAt: now,
      updatedAt: now,
      completedAt: null
    };

    fs.mkdirSync(this.jobsDir(project.id), { recursive: true });
    writeJsonAtomic(path.join(this.jobsDir(project.id), `${job.id}.json`), job);
    this.indexJob(job);
    this.touchProject(project.id);
    return { created: true, job };
  }

  createNewRevision(input = {}) {
    const jobs = this.listJobs(input.projectId).filter((job) => job.shotId === normalizeShotId(input.shotId));
    const nextRevision = jobs.reduce((max, job) => Math.max(max, Number(job.revision) || 0), 0) + 1;
    return this.createJob({ ...input, revision: nextRevision });
  }

  indexJob(job) {
    const index = readJson(this.jobIndexPath, { jobs: {} }) || { jobs: {} };
    index.jobs ||= {};
    index.jobs[job.id] = { projectId: job.projectId, file: path.join(this.jobsDir(job.projectId), `${job.id}.json`) };
    writeJsonAtomic(this.jobIndexPath, index);
  }

  getJob(jobId) {
    const index = readJson(this.jobIndexPath, { jobs: {} });
    const record = index?.jobs?.[String(jobId)];
    if (!record?.file) return null;
    return readJson(record.file, null);
  }

  listJobs(projectId) {
    const dir = this.jobsDir(projectId);
    let files = [];
    try { files = fs.readdirSync(dir); } catch (_) {}
    return files
      .filter((name) => name.endsWith('.json'))
      .map((name) => readJson(path.join(dir, name), null))
      .filter(Boolean)
      .sort((a, b) => Number(a.createdAt || 0) - Number(b.createdAt || 0));
  }

  patchJob(jobId, patch = {}) {
    const index = readJson(this.jobIndexPath, { jobs: {} });
    const record = index?.jobs?.[String(jobId)];
    if (!record?.file) {
      const error = new Error('Unknown jobId');
      error.code = 'JOB_NOT_FOUND';
      throw error;
    }
    const current = readJson(record.file, null);
    if (!current) {
      const error = new Error('Job file is missing');
      error.code = 'JOB_FILE_MISSING';
      throw error;
    }
    const now = Date.now();
    const next = { ...current, ...patch, id: current.id, idempotencyKey: current.idempotencyKey, projectId: current.projectId, shotId: current.shotId, revision: current.revision, updatedAt: now };
    if (TERMINAL_STATES.has(next.state) && !next.completedAt) next.completedAt = now;
    writeJsonAtomic(record.file, next);
    const project = this.refreshProject(next.projectId);
    return { job: next, project, projectComplete: project.status === 'complete' };
  }

  touchProject(projectId) {
    const project = this.getProject(projectId);
    if (!project) return null;
    const next = { ...project, updatedAt: Date.now() };
    writeJsonAtomic(this.projectFile(projectId), next);
    return next;
  }

  refreshProject(projectId) {
    const project = this.getProject(projectId);
    if (!project) return null;
    const jobs = this.listJobs(projectId);
    let status = 'active';
    let completedAt = null;
    if (jobs.length > 0 && jobs.every((job) => job.state === 'success')) {
      status = 'complete';
      completedAt = Date.now();
    } else if (jobs.length > 0 && jobs.every((job) => TERMINAL_STATES.has(job.state))) {
      status = 'terminal_with_errors';
      completedAt = Date.now();
    } else if (jobs.some((job) => !['queued', 'cancelled'].includes(job.state))) {
      status = 'running';
    }
    const next = { ...project, status, completedAt, updatedAt: Date.now() };
    writeJsonAtomic(this.projectFile(projectId), next);
    return next;
  }

  projectResult(projectId) {
    const project = this.refreshProject(projectId);
    if (!project) return null;
    const jobs = this.listJobs(projectId);
    return {
      event: project.status === 'complete' ? 'PROJECT_COMPLETE' : 'PROJECT_STATUS',
      project,
      jobs,
      outputs: jobs.filter((job) => job.state === 'success').map((job) => ({ jobId: job.id, shotId: job.shotId, revision: job.revision, outputPath: job.outputPath }))
    };
  }
}

module.exports = {
  ProjectStore,
  TERMINAL_STATES,
  stableJobFingerprint,
  normalizeRevision,
  normalizeShotId,
  normalizeSourceImagePath
};
