'use strict';

const http = require('http');
const { URL } = require('url');

const MAX_REQUEST_BYTES = 64 * 1024;
const MAX_CAPTURE_BYTES = 16 * 1024 * 1024;
const SAFE_MEDIA_SUFFIXES = [
  '.dola.com',
  '.ciciai.com',
  '.byteintlapi.com',
  '.ibytedtos.com',
  '.bytecdn.cn',
  '.volces.com',
  '.volcengine.com',
  '.snssdk.com'
];

function clean(value, max = 240) {
  return String(value == null ? '' : value)
    .replace(/[\u0000-\u001f\u007f]/g, '')
    .trim()
    .slice(0, max);
}

function json(res, status, payload) {
  const body = JSON.stringify(payload);
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    'Content-Length': Buffer.byteLength(body)
  });
  res.end(body);
}

function errorCode(error, fallback = 'BRIDGE_ERROR') {
  const code = clean(error && error.code, 80);
  return /^[A-Z0-9_:-]+$/.test(code) ? code : fallback;
}

function isSafeMediaUrl(value) {
  try {
    const parsed = new URL(String(value || '').trim());
    const host = String(parsed.hostname || '').toLowerCase();
    if (parsed.protocol !== 'https:' || parsed.username || parsed.password) return false;
    return SAFE_MEDIA_SUFFIXES.some(suffix => host === suffix.slice(1) || host.endsWith(suffix));
  } catch (_) {
    return false;
  }
}

function readJson(req) {
  return new Promise((resolve, reject) => {
    let total = 0;
    const chunks = [];
    req.on('data', chunk => {
      total += Buffer.byteLength(chunk);
      if (total > MAX_REQUEST_BYTES) {
        reject(Object.assign(new Error('request too large'), { code: 'REQUEST_TOO_LARGE' }));
        try { req.destroy(); } catch (_) {}
        return;
      }
      chunks.push(chunk);
    });
    req.on('end', () => {
      try {
        const raw = Buffer.concat(chunks).toString('utf8');
        resolve(raw ? JSON.parse(raw) : {});
      } catch (_) {
        reject(Object.assign(new Error('invalid json'), { code: 'INVALID_JSON' }));
      }
    });
    req.on('error', reject);
  });
}

function createXiaochaiBridge(options = {}) {
  const port = Number(options.port || process.env.XIAOCHAI_DOLA_BRIDGE_PORT || 8766);
  const host = '127.0.0.1';
  const token = clean(options.token || process.env.XIAOCHAI_DOLA_BRIDGE_TOKEN, 512);
  const getAccounts = typeof options.getAccounts === 'function' ? options.getAccounts : () => [];
  const findAccount = typeof options.findAccount === 'function'
    ? options.findAccount
    : hostId => getAccounts().find(account => String(account.id) === String(hostId));
  const verifyAccount = typeof options.verifyAccount === 'function' ? options.verifyAccount : async () => null;
  const activateAccount = typeof options.activateAccount === 'function' ? options.activateAccount : async () => false;
  const getChainCache = typeof options.getChainCache === 'function' ? options.getChainCache : () => [];
  const downloadForAccount = typeof options.downloadForAccount === 'function' ? options.downloadForAccount : async () => {
    throw Object.assign(new Error('download callback unavailable'), { code: 'DOWNLOAD_UNAVAILABLE' });
  };
  const appVersion = typeof options.appVersion === 'function' ? options.appVersion : () => '';

  function authorized(req) {
    return !token || String(req.headers['x-xiaochai-bridge-token'] || '') === token;
  }

  function publicAccounts() {
    return getAccounts().map((account, index) => ({
      host_account_id: clean(account.id, 120),
      display_name: clean(account.name, 160),
      profile_name: clean(account.profileName, 160),
      auth_status: clean(account.authStatus || 'unknown', 80),
      site: clean(account.site || 'dola', 40),
      index
    })).filter(account => account.host_account_id && account.site === 'dola');
  }

  function findHostAccount(hostId) {
    const account = findAccount(hostId);
    if (!account || String(account.site || 'dola') !== 'dola') {
      throw Object.assign(new Error('account not found'), { code: 'ACCOUNT_NOT_FOUND' });
    }
    return account;
  }

  function captureEntries(account, limit) {
    const requested = Math.max(1, Math.min(Number(limit) || 1, 10));
    const cache = Array.isArray(getChainCache(account)) ? getChainCache(account) : [];
    return cache.slice(-requested).reverse().map(item => {
      const body = String(item && item.body || '');
      if (!body || Buffer.byteLength(body, 'utf8') > MAX_CAPTURE_BYTES) return null;
      return {
        source_key: clean(item && (item.sourceKey || item.source_key), 240),
        body
      };
    }).filter(Boolean);
  }

  async function route(req, res) {
    if (!authorized(req)) return json(res, 401, { ok: false, error_code: 'UNAUTHORIZED' });
    const parsed = new URL(req.url || '/', `http://${host}:${port}`);
    const parts = parsed.pathname.split('/').filter(Boolean);
    if (req.method === 'GET' && parsed.pathname === '/v1/health') {
      return json(res, 200, { ok: true, bridge_version: '1', pid: process.pid, app_version: clean(appVersion(), 80) });
    }
    if (req.method === 'GET' && parsed.pathname === '/v1/accounts') {
      return json(res, 200, { ok: true, accounts: publicAccounts() });
    }
    if (parts.length < 3 || parts[0] !== 'v1' || parts[1] !== 'accounts') {
      return json(res, 404, { ok: false, error_code: 'NOT_FOUND' });
    }
    const hostId = decodeURIComponent(parts[2]);
    let account;
    try { account = findHostAccount(hostId); } catch (error) { return json(res, 404, { ok: false, error_code: errorCode(error, 'ACCOUNT_NOT_FOUND') }); }

    if (req.method === 'GET' && parts[3] === 'session') {
      try {
        const authenticated = await verifyAccount(account);
        return json(res, 200, { ok: true, authenticated: authenticated === true, verification: authenticated === null ? 'unknown' : 'checked' });
      } catch (error) {
        return json(res, 502, { ok: false, error_code: errorCode(error, 'SESSION_CHECK_FAILED') });
      }
    }
    if (req.method === 'POST' && parts[3] === 'activate') {
      try {
        const activated = await activateAccount(account);
        return json(res, 200, { ok: activated !== false, activated: activated !== false });
      } catch (error) {
        return json(res, 502, { ok: false, error_code: errorCode(error, 'ACTIVATE_FAILED') });
      }
    }
    if (req.method === 'GET' && parts[3] === 'capture' && parts[4] === 'latest') {
      return json(res, 200, { ok: true, captures: captureEntries(account, parsed.searchParams.get('limit')) });
    }
    if (req.method === 'POST' && parts[3] === 'download') {
      try {
        const payload = await readJson(req);
        const url = String(payload && payload.url || '').trim();
        const filename = clean(payload && payload.filename || 'dola-video.mp4', 120);
        if (!isSafeMediaUrl(url)) return json(res, 400, { ok: false, error_code: 'UNSAFE_MEDIA_URL' });
        if (!filename || filename.includes('..') || /[\\/]/.test(filename)) return json(res, 400, { ok: false, error_code: 'UNSAFE_FILENAME' });
        const result = await downloadForAccount(account, { url, filename });
        return json(res, 200, { ok: true, path: clean(result && result.path, 1000), bytes: Number(result && result.bytes) || 0 });
      } catch (error) {
        return json(res, 502, { ok: false, error_code: errorCode(error, 'DOWNLOAD_FAILED') });
      }
    }
    return json(res, 404, { ok: false, error_code: 'NOT_FOUND' });
  }

  const server = http.createServer((req, res) => {
    route(req, res).catch(() => json(res, 500, { ok: false, error_code: 'BRIDGE_ERROR' }));
  });
  server.on('error', () => {});
  return {
    host,
    port,
    server,
    start() { server.listen(port, host); return server; },
    stop() { return new Promise(resolve => server.close(() => resolve())); }
  };
}

module.exports = { createXiaochaiBridge, isSafeMediaUrl };
