'use strict';

const http = require('http');
const fs = require('fs');
const os = require('os');
const path = require('path');
const crypto = require('crypto');

function controlDiscoveryPath() {
  const base = process.env.SEEDANCE_STUDIO_CONTROL_DIR
    || process.env.LOCALAPPDATA
    || process.env.APPDATA
    || path.join(os.homedir(), '.seedance-desktop-studio');
  return path.join(base, 'SeedanceDesktopStudio', 'control.json');
}

function writeJson(res, statusCode, payload) {
  const body = JSON.stringify(payload, null, 2);
  res.writeHead(statusCode, {
    'content-type': 'application/json; charset=utf-8',
    'content-length': Buffer.byteLength(body),
    'cache-control': 'no-store'
  });
  res.end(body);
}

function readJson(req, limit = 1024 * 1024) {
  return new Promise((resolve, reject) => {
    let size = 0;
    const chunks = [];
    req.on('data', (chunk) => {
      size += chunk.length;
      if (size > limit) {
        reject(Object.assign(new Error('Request body too large'), { statusCode: 413 }));
        req.destroy();
        return;
      }
      chunks.push(chunk);
    });
    req.on('end', () => {
      if (chunks.length === 0) return resolve({});
      try { resolve(JSON.parse(Buffer.concat(chunks).toString('utf8'))); }
      catch (_) { reject(Object.assign(new Error('Invalid JSON body'), { statusCode: 400 })); }
    });
    req.on('error', reject);
  });
}

function routeParts(url) {
  const parsed = new URL(url, 'http://127.0.0.1');
  return parsed.pathname.split('/').filter(Boolean).map(decodeURIComponent);
}

function requireHandler(handlers, name) {
  if (typeof handlers[name] !== 'function') {
    throw Object.assign(new Error(`Control capability is not available: ${name}`), { statusCode: 501, code: 'capability_not_available' });
  }
  return handlers[name];
}

async function startControlServer(handlers) {
  const token = crypto.randomBytes(32).toString('hex');
  const discoveryFile = controlDiscoveryPath();

  const server = http.createServer(async (req, res) => {
    const pathname = new URL(req.url || '/', 'http://127.0.0.1').pathname;
    if (pathname === '/health') return writeJson(res, 200, await handlers.health());

    const auth = String(req.headers.authorization || '');
    if (auth !== `Bearer ${token}`) return writeJson(res, 401, { error: 'unauthorized' });

    try {
      const parts = routeParts(req.url || '/');
      if (req.method === 'GET' && parts.join('/') === 'v1/accounts') {
        return writeJson(res, 200, { accounts: await handlers.listAccounts() });
      }
      if (req.method === 'POST' && parts.join('/') === 'v1/accounts') {
        const body = await readJson(req);
        return writeJson(res, 201, { account: await handlers.createAccount(body.name) });
      }
      if (req.method === 'GET' && parts.join('/') === 'v1/accounts/health') {
        return writeJson(res, 200, await requireHandler(handlers, 'accountHealthSummary')());
      }
      if (req.method === 'POST' && parts.length === 4 && parts[0] === 'v1' && parts[1] === 'accounts' && parts[3] === 'pause') {
        const body = await readJson(req);
        return writeJson(res, 200, { account: await requireHandler(handlers, 'pauseAccount')(parts[2], body.reason) });
      }
      if (req.method === 'POST' && parts.length === 4 && parts[0] === 'v1' && parts[1] === 'accounts' && parts[3] === 'resume') {
        return writeJson(res, 200, { account: await requireHandler(handlers, 'resumeAccount')(parts[2]) });
      }
      if (req.method === 'POST' && parts.length === 4 && parts[0] === 'v1' && parts[1] === 'accounts' && parts[3] === 'debug') {
        return writeJson(res, 200, await requireHandler(handlers, 'debugAccount')(parts[2]));
      }
      if (req.method === 'POST' && parts.length === 4 && parts[0] === 'v1' && parts[1] === 'accounts' && parts[3] === 'activate') {
        return writeJson(res, 200, { account: await handlers.activateAccount(parts[2]) });
      }
      if (req.method === 'GET' && parts.length === 4 && parts[0] === 'v1' && parts[1] === 'accounts' && parts[3] === 'session') {
        return writeJson(res, 200, { session: await handlers.getAccountSession(parts[2]) });
      }
      if (req.method === 'GET' && parts.join('/') === 'v1/workers') {
        return writeJson(res, 200, await requireHandler(handlers, 'workerStatus')());
      }
      if (req.method === 'POST' && parts.join('/') === 'v1/workers/settings') {
        const body = await readJson(req);
        return writeJson(res, 200, await requireHandler(handlers, 'configureWorkers')(body));
      }
      if (req.method === 'POST' && parts.join('/') === 'v1/workers/sweep') {
        return writeJson(res, 200, await requireHandler(handlers, 'sweepWorkers')());
      }
      if (req.method === 'GET' && parts.join('/') === 'v1/providers') {
        return writeJson(res, 200, { providers: await handlers.listProviders() });
      }

      if (req.method === 'GET' && parts.join('/') === 'v1/tasks') {
        return writeJson(res, 200, { tasks: await handlers.listTasks() });
      }
      if (req.method === 'POST' && parts.join('/') === 'v1/tasks') {
        const body = await readJson(req);
        return writeJson(res, 201, { task: await handlers.createTask(body) });
      }
      if (parts.length === 3 && parts[0] === 'v1' && parts[1] === 'tasks' && req.method === 'GET') {
        const task = await handlers.getTask(parts[2]);
        if (!task) return writeJson(res, 404, { error: 'task_not_found' });
        return writeJson(res, 200, { task });
      }
      if (parts.length === 4 && parts[0] === 'v1' && parts[1] === 'tasks' && parts[3] === 'cancel' && req.method === 'POST') {
        const task = await handlers.cancelTask(parts[2]);
        if (!task) return writeJson(res, 404, { error: 'task_not_found' });
        return writeJson(res, 200, { task });
      }
      if (parts.length === 4 && parts[0] === 'v1' && parts[1] === 'tasks' && parts[3] === 'dispatch' && req.method === 'POST') {
        const result = await handlers.dispatchTask(parts[2]);
        return writeJson(res, result.ok ? 200 : (result.statusCode || 409), result);
      }
      if (parts.length === 4 && parts[0] === 'v1' && parts[1] === 'tasks' && parts[3] === 'recover' && req.method === 'POST') {
        const result = await requireHandler(handlers, 'recoverTask')(parts[2]);
        return writeJson(res, result.ok ? 200 : (result.statusCode || (result.recoverable ? 202 : 409)), result);
      }

      if (req.method === 'GET' && parts.join('/') === 'v1/projects') {
        return writeJson(res, 200, { projects: await requireHandler(handlers, 'listProjects')() });
      }
      if (req.method === 'POST' && parts.join('/') === 'v1/projects') {
        const body = await readJson(req);
        const result = await requireHandler(handlers, 'createProject')(body);
        return writeJson(res, result.created ? 201 : 200, result);
      }
      if (parts.length === 3 && parts[0] === 'v1' && parts[1] === 'projects' && req.method === 'GET') {
        const project = await requireHandler(handlers, 'getProject')(parts[2]);
        if (!project) return writeJson(res, 404, { error: 'project_not_found' });
        return writeJson(res, 200, { project });
      }
      if (parts.length === 4 && parts[0] === 'v1' && parts[1] === 'projects' && parts[3] === 'jobs' && req.method === 'GET') {
        const project = await requireHandler(handlers, 'getProject')(parts[2]);
        if (!project) return writeJson(res, 404, { error: 'project_not_found' });
        return writeJson(res, 200, { project, jobs: await requireHandler(handlers, 'listProjectJobs')(parts[2]) });
      }
      if (parts.length === 4 && parts[0] === 'v1' && parts[1] === 'projects' && parts[3] === 'jobs' && req.method === 'POST') {
        const body = await readJson(req);
        const result = await requireHandler(handlers, 'createProjectJob')({ ...body, projectId: parts[2] });
        return writeJson(res, result.created ? 201 : 200, result);
      }
      if (parts.length === 4 && parts[0] === 'v1' && parts[1] === 'projects' && parts[3] === 'revisions' && req.method === 'POST') {
        const body = await readJson(req);
        const result = await requireHandler(handlers, 'createProjectJobRevision')({ ...body, projectId: parts[2] });
        return writeJson(res, 201, result);
      }
      if (parts.length === 4 && parts[0] === 'v1' && parts[1] === 'projects' && parts[3] === 'result' && req.method === 'GET') {
        const result = await requireHandler(handlers, 'getProjectResult')(parts[2]);
        if (!result) return writeJson(res, 404, { error: 'project_not_found' });
        return writeJson(res, 200, result);
      }
      if (parts.length === 3 && parts[0] === 'v1' && parts[1] === 'jobs' && req.method === 'GET') {
        const job = await requireHandler(handlers, 'getProjectJob')(parts[2]);
        if (!job) return writeJson(res, 404, { error: 'job_not_found' });
        return writeJson(res, 200, { job });
      }

      return writeJson(res, 404, { error: 'not_found' });
    } catch (error) {
      return writeJson(res, Number(error.statusCode) || 500, {
        error: error.code || 'control_error',
        message: error.message || String(error),
        ...(error.existingJobId ? { existingJobId: error.existingJobId } : {}),
        ...(error.accountId ? { accountId: error.accountId } : {}),
        ...(error.reason ? { reason: error.reason } : {})
      });
    }
  });

  await new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', resolve);
  });

  const address = server.address();
  const info = { host: '127.0.0.1', port: address.port, token, pid: process.pid, version: 1, startedAt: Date.now() };
  fs.mkdirSync(path.dirname(discoveryFile), { recursive: true });
  fs.writeFileSync(discoveryFile, JSON.stringify(info, null, 2), { encoding: 'utf8', mode: 0o600 });

  function stop() {
    try {
      const current = JSON.parse(fs.readFileSync(discoveryFile, 'utf8'));
      if (Number(current.pid) === process.pid) fs.unlinkSync(discoveryFile);
    } catch (_) {}
    return new Promise((resolve) => server.close(resolve));
  }

  return { server, info, discoveryFile, stop };
}

module.exports = { startControlServer, controlDiscoveryPath };
