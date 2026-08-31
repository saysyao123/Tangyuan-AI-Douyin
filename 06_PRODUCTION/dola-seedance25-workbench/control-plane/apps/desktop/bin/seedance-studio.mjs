#!/usr/bin/env node

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDir = path.dirname(fileURLToPath(import.meta.url));

function portableControlPath(root) {
  return path.join(path.resolve(root), 'runtime', 'control', 'SeedanceDesktopStudio', 'control.json');
}

function discoveryCandidates() {
  const candidates = [];
  if (process.env.SEEDANCE_STUDIO_CONTROL_DIR) {
    candidates.push(path.join(path.resolve(process.env.SEEDANCE_STUDIO_CONTROL_DIR), 'SeedanceDesktopStudio', 'control.json'));
  }
  if (process.env.DOLA_WORKBENCH_ROOT) candidates.push(portableControlPath(process.env.DOLA_WORKBENCH_ROOT));
  if (process.env.PORTABLE_EXECUTABLE_DIR) candidates.push(portableControlPath(process.env.PORTABLE_EXECUTABLE_DIR));

  // Development bootstrap uses apps/desktop/.portable-dev.
  candidates.push(portableControlPath(path.resolve(scriptDir, '..', '.portable-dev')));

  const legacyBase = process.env.LOCALAPPDATA
    || process.env.APPDATA
    || path.join(os.homedir(), '.seedance-desktop-studio');
  candidates.push(path.join(legacyBase, 'SeedanceDesktopStudio', 'control.json'));
  return [...new Set(candidates)];
}

function readDiscovery() {
  const errors = [];
  for (const filePath of discoveryCandidates()) {
    try {
      const parsed = JSON.parse(fs.readFileSync(filePath, 'utf8'));
      if (!parsed.port || !parsed.token) throw new Error('Incomplete control discovery file.');
      return parsed;
    } catch (error) {
      errors.push({ file: filePath, cause: error.message });
    }
  }
  fail('Seedance Desktop Studio is not running or its control file is unavailable.', {
    checked: errors.map((item) => item.file)
  });
}

async function request(method, route, body) {
  const discovery = readDiscovery();
  const response = await fetch(`http://127.0.0.1:${discovery.port}${route}`, {
    method,
    headers: {
      authorization: `Bearer ${discovery.token}`,
      ...(body === undefined ? {} : { 'content-type': 'application/json' })
    },
    body: body === undefined ? undefined : JSON.stringify(body)
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    fail(payload.message || payload.error || `HTTP ${response.status}`, { status: response.status, ...payload });
  }
  return payload;
}

function parseFlags(tokens) {
  const flags = {};
  const positional = [];
  for (let i = 0; i < tokens.length; i += 1) {
    const token = tokens[i];
    if (!token.startsWith('--')) {
      positional.push(token);
      continue;
    }
    const key = token.slice(2);
    const next = tokens[i + 1];
    if (next === undefined || next.startsWith('--')) flags[key] = true;
    else {
      flags[key] = next;
      i += 1;
    }
  }
  return { flags, positional };
}

function print(value) {
  process.stdout.write(`${JSON.stringify(value, null, 2)}\n`);
}

function fail(message, detail = {}) {
  process.stderr.write(`${JSON.stringify({ ok: false, error: message, ...detail }, null, 2)}\n`);
  process.exit(1);
}

function requireFlag(flags, key) {
  const value = flags[key];
  if (value === undefined || value === true || String(value).trim() === '') fail(`Missing --${key}`);
  return String(value);
}

function readPrompt(flags) {
  if (flags['prompt-file'] !== undefined && flags['prompt-file'] !== true) {
    const promptPath = path.resolve(String(flags['prompt-file']));
    return fs.readFileSync(promptPath, 'utf8');
  }
  return requireFlag(flags, 'prompt');
}

async function resolveAccount(value) {
  const { accounts } = await request('GET', '/v1/accounts');
  const exact = accounts.find(item => item.id === value);
  if (exact) return exact;
  const byName = accounts.filter(item => item.name.toLowerCase() === value.toLowerCase());
  if (byName.length === 1) return byName[0];
  if (byName.length > 1) fail('Account name is ambiguous; use the account id.', { matches: byName });
  const ordinal = String(value).toLowerCase().replace(/[^a-z0-9]/g, '').match(/^dola([1-9][0-9]*)$/);
  if (ordinal) {
    const account = accounts[Number(ordinal[1]) - 1];
    if (account) return account;
  }
  fail('Account not found.', { account: value });
}

async function resolveOptionalAccount(flags) {
  if (flags.account === undefined || flags.account === true || !String(flags.account).trim()) return null;
  return resolveAccount(String(flags.account));
}

async function watchTask(id, intervalMs) {
  const terminal = new Set(['success', 'failed', 'cancelled']);
  while (true) {
    const payload = await request('GET', `/v1/tasks/${encodeURIComponent(id)}`);
    print(payload);
    if (terminal.has(payload.task.state)) return;
    await new Promise(resolve => setTimeout(resolve, intervalMs));
  }
}

function projectJobBody(flags, account) {
  const body = {
    shotId: requireFlag(flags, 'shot'),
    provider: String(flags.provider || 'dola-web'),
    mode: String(flags.mode || 't2v'),
    model: String(flags.model || 'seedance-v2.5'),
    duration: Number(flags.duration || 10),
    ratio: String(flags.ratio || '9:16'),
    prompt: readPrompt(flags)
  };
  if (flags.revision !== undefined && flags.revision !== true) body.revision = Number(flags.revision);
  if (flags.image !== undefined && flags.image !== true) body.sourceImagePath = String(flags.image);
  if (account) body.requestedAccountId = account.id;
  return body;
}

async function main() {
  const args = process.argv.slice(2);
  const [group, action, ...rest] = args;
  const { flags, positional } = parseFlags(rest);

  if (group === 'health') return print(await request('GET', '/health'));
  if (group === 'providers' && action === 'list') return print(await request('GET', '/v1/providers'));

  if (group === 'accounts' && action === 'list') return print(await request('GET', '/v1/accounts'));
  if (group === 'accounts' && action === 'add') {
    const name = flags.name === undefined ? positional.join(' ') : String(flags.name);
    if (!name.trim()) fail('Usage: accounts add --name "Dola A"');
    return print(await request('POST', '/v1/accounts', { name }));
  }
  if (group === 'accounts' && action === 'open') {
    const selector = String(flags.account || positional[0] || '').trim();
    if (!selector) fail('Usage: accounts open --account <id-or-name>');
    const account = await resolveAccount(selector);
    return print(await request('POST', `/v1/accounts/${encodeURIComponent(account.id)}/activate`, {}));
  }

  // Legacy POC task commands remain available during migration.
  if (group === 'tasks' && action === 'list') return print(await request('GET', '/v1/tasks'));
  if (group === 'tasks' && action === 'get') {
    const id = String(flags.id || positional[0] || '').trim();
    if (!id) fail('Usage: tasks get --id <task-id>');
    return print(await request('GET', `/v1/tasks/${encodeURIComponent(id)}`));
  }
  if (group === 'tasks' && action === 'create') {
    const selector = requireFlag(flags, 'account');
    const account = await resolveAccount(selector);
    const body = {
      accountId: account.id,
      provider: String(flags.provider || 'dola-web'),
      mode: String(flags.mode || 't2v'),
      model: String(flags.model || 'seedance-v2.5'),
      duration: Number(flags.duration || 10),
      ratio: String(flags.ratio || '9:16'),
      prompt: readPrompt(flags)
    };
    if (flags.image !== undefined && flags.image !== true) body.imagePath = String(flags.image);
    return print(await request('POST', '/v1/tasks', body));
  }
  if (group === 'tasks' && action === 'dispatch') {
    const id = String(flags.id || positional[0] || '').trim();
    if (!id) fail('Usage: tasks dispatch --id <task-id>');
    return print(await request('POST', `/v1/tasks/${encodeURIComponent(id)}/dispatch`, {}));
  }
  if (group === 'tasks' && action === 'cancel') {
    const id = String(flags.id || positional[0] || '').trim();
    if (!id) fail('Usage: tasks cancel --id <task-id>');
    return print(await request('POST', `/v1/tasks/${encodeURIComponent(id)}/cancel`, {}));
  }
  if (group === 'tasks' && action === 'watch') {
    const id = String(flags.id || positional[0] || '').trim();
    if (!id) fail('Usage: tasks watch --id <task-id> [--interval 5000]');
    const interval = Math.max(1000, Number(flags.interval || 5000));
    return watchTask(id, interval);
  }

  // Portable V1 project/job commands. They create durable, idempotent work
  // records but do not bypass provider Gates or submit directly to Dola.
  if (group === 'projects' && action === 'list') return print(await request('GET', '/v1/projects'));
  if (group === 'projects' && action === 'create') {
    const name = flags.name === undefined ? positional.join(' ') : String(flags.name);
    if (!name.trim()) fail('Usage: projects create --name "MV Project"');
    const body = { name };
    if (flags.id !== undefined && flags.id !== true) body.id = String(flags.id);
    return print(await request('POST', '/v1/projects', body));
  }
  if (group === 'projects' && action === 'get') {
    const id = String(flags.id || positional[0] || '').trim();
    if (!id) fail('Usage: projects get --id <project-id>');
    return print(await request('GET', `/v1/projects/${encodeURIComponent(id)}`));
  }
  if (group === 'projects' && action === 'jobs') {
    const id = String(flags.id || flags.project || positional[0] || '').trim();
    if (!id) fail('Usage: projects jobs --id <project-id>');
    return print(await request('GET', `/v1/projects/${encodeURIComponent(id)}/jobs`));
  }
  if (group === 'projects' && action === 'result') {
    const id = String(flags.id || flags.project || positional[0] || '').trim();
    if (!id) fail('Usage: projects result --id <project-id>');
    return print(await request('GET', `/v1/projects/${encodeURIComponent(id)}/result`));
  }

  if (group === 'jobs' && action === 'get') {
    const id = String(flags.id || positional[0] || '').trim();
    if (!id) fail('Usage: jobs get --id <job-id>');
    return print(await request('GET', `/v1/jobs/${encodeURIComponent(id)}`));
  }
  if (group === 'jobs' && action === 'create') {
    const projectId = requireFlag(flags, 'project');
    const account = await resolveOptionalAccount(flags);
    const body = projectJobBody(flags, account);
    return print(await request('POST', `/v1/projects/${encodeURIComponent(projectId)}/jobs`, body));
  }
  if (group === 'jobs' && (action === 'revise' || action === 'new-revision')) {
    const projectId = requireFlag(flags, 'project');
    const account = await resolveOptionalAccount(flags);
    const body = projectJobBody({ ...flags, revision: undefined }, account);
    return print(await request('POST', `/v1/projects/${encodeURIComponent(projectId)}/revisions`, body));
  }

  fail('Unknown command.', {
    commands: [
      'health',
      'providers list',
      'accounts list',
      'accounts add --name "Dola A"',
      'accounts open --account "Dola A"',
      'projects list',
      'projects create --name "MV Project"',
      'projects get --id <project-id>',
      'projects jobs --id <project-id>',
      'projects result --id <project-id>',
      'jobs create --project <project-id> --shot S01 --duration 5 --ratio 9:16 --prompt "..."',
      'jobs create --project <project-id> --shot S01 --mode i2v --image "C:\\path\\first-frame.png" --duration 5 --ratio 9:16 --prompt-file "C:\\path\\S01.md"',
      'jobs revise --project <project-id> --shot S01 --duration 5 --prompt "..."',
      'jobs get --id <job-id>',
      'tasks list',
      'tasks create --account "Dola A" --duration 5 --ratio 9:16 --prompt "..."',
      'tasks get --id <task-id>',
      'tasks dispatch --id <task-id>',
      'tasks cancel --id <task-id>',
      'tasks watch --id <task-id>'
    ]
  });
}

main().catch(error => fail(error.message || String(error), { stack: error.stack }));
