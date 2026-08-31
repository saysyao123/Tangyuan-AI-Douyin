#!/usr/bin/env node

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));

function discoveryCandidates() {
  const roots = [];
  if (process.env.DOLA_WORKBENCH_ROOT) roots.push(path.resolve(process.env.DOLA_WORKBENCH_ROOT));
  if (process.env.PORTABLE_EXECUTABLE_DIR) roots.push(path.resolve(process.env.PORTABLE_EXECUTABLE_DIR));
  roots.push(path.resolve(here, '..', '.portable-dev'));
  const files = roots.map((root) => path.join(root, 'runtime', 'control', 'SeedanceDesktopStudio', 'control.json'));
  const legacy = process.env.LOCALAPPDATA || process.env.APPDATA || path.join(os.homedir(), '.seedance-desktop-studio');
  files.push(path.join(legacy, 'SeedanceDesktopStudio', 'control.json'));
  return [...new Set(files)];
}

function discovery() {
  for (const file of discoveryCandidates()) {
    try {
      const value = JSON.parse(fs.readFileSync(file, 'utf8'));
      if (value.port && value.token) return value;
    } catch (_) {}
  }
  throw new Error('Dola Seedance Workbench is not running or its control file is unavailable.');
}

async function request(method, route, body) {
  const value = discovery();
  const response = await fetch(`http://127.0.0.1:${value.port}${route}`, {
    method,
    headers: {
      authorization: `Bearer ${value.token}`,
      ...(body === undefined ? {} : { 'content-type': 'application/json' })
    },
    body: body === undefined ? undefined : JSON.stringify(body)
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok && response.status !== 202) {
    const error = new Error(payload.message || payload.error || `HTTP ${response.status}`);
    error.payload = payload;
    throw error;
  }
  return payload;
}

function flags(tokens) {
  const out = { _: [] };
  for (let i = 0; i < tokens.length; i += 1) {
    const token = tokens[i];
    if (!token.startsWith('--')) { out._.push(token); continue; }
    const key = token.slice(2);
    const next = tokens[i + 1];
    if (next === undefined || next.startsWith('--')) out[key] = true;
    else { out[key] = next; i += 1; }
  }
  return out;
}

function required(value, name) {
  if (value === undefined || value === true || String(value).trim() === '') throw new Error(`Missing --${name}`);
  return String(value);
}

function print(value) { process.stdout.write(`${JSON.stringify(value, null, 2)}\n`); }

async function main() {
  const [group, action, ...rest] = process.argv.slice(2);
  const f = flags(rest);
  if (group === 'health') return print(await request('GET', '/health'));
  if (group === 'accounts' && action === 'list') return print(await request('GET', '/v1/accounts'));
  if (group === 'accounts' && action === 'health') return print(await request('GET', '/v1/accounts/health'));
  if (group === 'workers' && action === 'status') return print(await request('GET', '/v1/workers'));
  if (group === 'workers' && action === 'configure') {
    const body = {};
    if (f.max !== undefined && f.max !== true) body.maxWorkers = Number(f.max);
    if (f['idle-ms'] !== undefined && f['idle-ms'] !== true) body.idleMs = Number(f['idle-ms']);
    return print(await request('POST', '/v1/workers/settings', body));
  }
  if (group === 'tasks' && action === 'list') return print(await request('GET', '/v1/tasks'));
  if (group === 'tasks' && action === 'get') {
    const id = required(f.id || f._[0], 'id');
    return print(await request('GET', `/v1/tasks/${encodeURIComponent(id)}`));
  }
  if (group === 'tasks' && action === 'create') {
    const accountId = required(f.account, 'account');
    const prompt = f['prompt-file'] && f['prompt-file'] !== true
      ? fs.readFileSync(path.resolve(String(f['prompt-file'])), 'utf8')
      : required(f.prompt, 'prompt');
    const body = {
      accountId,
      provider: String(f.provider || 'dola-web'),
      mode: String(f.mode || (f.image ? 'i2v' : 't2v')),
      model: String(f.model || 'seedance-v2.5'),
      duration: Number(f.duration || 10),
      ratio: String(f.ratio || '9:16'),
      prompt
    };
    if (f.image && f.image !== true) body.imagePath = path.resolve(String(f.image));
    return print(await request('POST', '/v1/tasks', body));
  }
  if (group === 'tasks' && action === 'dispatch') {
    const id = required(f.id || f._[0], 'id');
    return print(await request('POST', `/v1/tasks/${encodeURIComponent(id)}/dispatch`, {}));
  }
  if (group === 'tasks' && action === 'recover') {
    const id = required(f.id || f._[0], 'id');
    return print(await request('POST', `/v1/tasks/${encodeURIComponent(id)}/recover`, {}));
  }
  if (group === 'outputs' && action === 'get') {
    const id = required(f.task || f.id || f._[0], 'task');
    const payload = await request('GET', `/v1/tasks/${encodeURIComponent(id)}`);
    return print({ taskId: id, state: payload.task?.state, outputPath: payload.task?.outputPath || null, outputBytes: payload.task?.outputBytes || null, outputSha256: payload.task?.outputSha256 || null });
  }
  throw new Error('Unknown command. Try: health | accounts list/health | workers status/configure | tasks list/get/create/dispatch/recover | outputs get');
}

main().catch((error) => {
  process.stderr.write(`${JSON.stringify({ ok: false, error: error.message, ...(error.payload || {}) }, null, 2)}\n`);
  process.exit(1);
});
