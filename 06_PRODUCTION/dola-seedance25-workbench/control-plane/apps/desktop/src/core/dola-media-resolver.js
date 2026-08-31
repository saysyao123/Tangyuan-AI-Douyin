'use strict';

const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { writeJsonAtomic, safeSegment } = require('./atomic-json');

function redactUrl(value) {
  try {
    const url = new URL(String(value));
    return `${url.origin}${url.pathname}`;
  } catch (_) { return ''; }
}

function looksLikeMediaUrl(value) {
  if (typeof value !== 'string' || value.length < 12 || value.length > 12000) return false;
  let url;
  try { url = new URL(value); } catch (_) { return false; }
  if (!['http:', 'https:'].includes(url.protocol)) return false;
  const marker = `${url.pathname} ${url.search}`.toLowerCase();
  return /\.(mp4|mov|m4v)(?:$|[/?#])/i.test(url.pathname)
    || /video|media|play|download|stream|main_url|mainurl|vid/i.test(marker);
}

function evidenceFromContext(context, url) {
  const text = `${context} ${url}`.toLowerCase();
  const unwatermarked = /unwatermarked|no[_-]?watermark|without[_-]?watermark|logo[_-]?type[=:]?(?:unwatermarked|0)|无水印/.test(text);
  const watermarked = !unwatermarked && /watermarked|with[_-]?watermark|logo[_-]?type[=:]?(?:watermarked|1)|水印/.test(text);
  const original = /original|origin|source|main[_-]?url|master/.test(text);
  const preview = /preview|thumbnail|poster|cover/.test(text);
  return { unwatermarked, watermarked, original, preview };
}

function numberNear(object, names) {
  if (!object || typeof object !== 'object') return null;
  for (const [key, value] of Object.entries(object)) {
    const normalized = key.toLowerCase().replace(/[^a-z0-9]/g, '');
    if (!names.includes(normalized)) continue;
    const number = Number(value);
    if (Number.isFinite(number) && number > 0) return number;
  }
  return null;
}

function parseNestedString(value, visit) {
  if (typeof value !== 'string' || value.length > 2_000_000) return;
  const text = value.trim();
  if (!text) return;
  try { visit(JSON.parse(text)); } catch (_) {}
  for (const line of text.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed.startsWith('data:')) continue;
    const payload = trimmed.slice(5).trim();
    if (!payload || payload === '[DONE]') continue;
    try { visit(JSON.parse(payload)); } catch (_) {}
  }
}

function extractMediaCandidates(body) {
  const candidates = new Map();
  const seenObjects = new Set();
  const seenStrings = new Set();

  function add(url, context, owner) {
    if (!looksLikeMediaUrl(url)) return;
    const key = String(url);
    const evidence = evidenceFromContext(context, key);
    const width = numberNear(owner, ['width', 'videowidth', 'w']);
    const height = numberNear(owner, ['height', 'videoheight', 'h']);
    const bitrate = numberNear(owner, ['bitrate', 'bitratebps', 'bandwidth']);
    const previous = candidates.get(key);
    const value = {
      url: key,
      redactedUrl: redactUrl(key),
      contexts: [...new Set([...(previous?.contexts || []), String(context || '').slice(0, 300)])].filter(Boolean),
      unwatermarked: previous?.unwatermarked || evidence.unwatermarked,
      watermarked: previous?.watermarked || evidence.watermarked,
      original: previous?.original || evidence.original,
      preview: previous?.preview || evidence.preview,
      width: Math.max(Number(previous?.width || 0), Number(width || 0)) || null,
      height: Math.max(Number(previous?.height || 0), Number(height || 0)) || null,
      bitrate: Math.max(Number(previous?.bitrate || 0), Number(bitrate || 0)) || null
    };
    candidates.set(key, value);
  }

  function scan(value, context = '', owner = null) {
    if (value === null || value === undefined) return;
    if (typeof value === 'string') {
      if (seenStrings.has(value)) return;
      seenStrings.add(value);
      add(value, context, owner);
      const urlRegex = /https?:\/\/[^\s"'<>\\]+/g;
      for (const match of value.match(urlRegex) || []) add(match.replace(/[),.;]+$/, ''), context, owner);
      parseNestedString(value, (parsed) => scan(parsed, context, owner));
      return;
    }
    if (Array.isArray(value)) {
      for (const item of value.slice(0, 1000)) scan(item, context, owner);
      return;
    }
    if (typeof value !== 'object' || seenObjects.has(value)) return;
    seenObjects.add(value);
    for (const [key, child] of Object.entries(value)) {
      const nextContext = context ? `${context}.${key}` : key;
      if (typeof child === 'string') add(child, nextContext, value);
      scan(child, nextContext, value);
    }
  }

  parseNestedString(String(body || ''), (parsed) => scan(parsed, 'response', parsed));
  scan(body, 'raw', null);
  return [...candidates.values()].map((candidate) => ({ ...candidate, score: scoreCandidate(candidate) }))
    .sort((a, b) => b.score - a.score);
}

function scoreCandidate(candidate) {
  // Fail-closed ranking: explicit watermark evidence dominates everything.
  let score = 0;
  if (candidate.watermarked) score -= 1_000_000;
  if (candidate.unwatermarked) score += 500_000;
  if (candidate.original) score += 50_000;
  if (candidate.preview) score -= 25_000;
  const area = Number(candidate.width || 0) * Number(candidate.height || 0);
  score += Math.min(30_000, Math.floor(area / 100));
  score += Math.min(20_000, Math.floor(Number(candidate.bitrate || 0) / 1000));
  if (/\.mp4(?:$|[?#])/i.test(candidate.url)) score += 5_000;
  return score;
}

function candidateReport(candidates) {
  return candidates.map((item, index) => ({
    rank: index + 1,
    redactedUrl: item.redactedUrl,
    score: item.score,
    unwatermarked: item.unwatermarked,
    watermarked: item.watermarked,
    original: item.original,
    preview: item.preview,
    width: item.width,
    height: item.height,
    bitrate: item.bitrate,
    contexts: item.contexts
  }));
}

function collectCandidatesFromJob(jobDir) {
  const rawDir = path.join(jobDir, 'raw-responses');
  const all = [];
  if (!fs.existsSync(rawDir)) return all;
  for (const name of fs.readdirSync(rawDir).filter((item) => item.endsWith('.json')).sort()) {
    try {
      const payload = JSON.parse(fs.readFileSync(path.join(rawDir, name), 'utf8'));
      const body = payload?.body;
      for (const candidate of extractMediaCandidates(body)) {
        candidate.sourceFile = name;
        all.push(candidate);
      }
    } catch (_) {}
  }
  const merged = new Map();
  for (const candidate of all) {
    const previous = merged.get(candidate.url);
    if (!previous || candidate.score > previous.score) merged.set(candidate.url, candidate);
  }
  return [...merged.values()].sort((a, b) => b.score - a.score);
}

function validateMp4(filePath) {
  const stat = fs.statSync(filePath);
  const head = Buffer.alloc(Math.min(64, stat.size));
  const fd = fs.openSync(filePath, 'r');
  try { fs.readSync(fd, head, 0, head.length, 0); } finally { fs.closeSync(fd); }
  const ftyp = head.includes(Buffer.from('ftyp'));
  const hash = crypto.createHash('sha256');
  const data = fs.readFileSync(filePath);
  hash.update(data);
  return { validMedia: ftyp && stat.size > 1024, ftyp, bytes: stat.size, sha256: hash.digest('hex') };
}

async function downloadCandidate(candidate, outputPath) {
  const target = path.resolve(outputPath);
  const partial = `${target}.part`;
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.rmSync(partial, { force: true });
  const response = await fetch(candidate.url, { redirect: 'follow' });
  if (!response.ok) {
    const error = new Error(`Media download HTTP ${response.status}`);
    error.code = response.status === 403 ? 'MEDIA_FORBIDDEN' : 'MEDIA_DOWNLOAD_FAILED';
    error.statusCode = response.status;
    throw error;
  }
  const expected = Number(response.headers.get('content-length') || 0);
  const buffer = Buffer.from(await response.arrayBuffer());
  if (expected && buffer.length !== expected) {
    const error = new Error(`Media Content-Length mismatch: expected ${expected}, received ${buffer.length}`);
    error.code = 'MEDIA_LENGTH_MISMATCH';
    throw error;
  }
  fs.writeFileSync(partial, buffer);
  const validation = validateMp4(partial);
  if (!validation.validMedia) {
    fs.rmSync(partial, { force: true });
    const error = new Error('Downloaded media did not pass lightweight MP4 validation.');
    error.code = 'MEDIA_VALIDATION_FAILED';
    throw error;
  }
  fs.renameSync(partial, target);
  return { path: target, ...validation };
}

async function resolveJobMedia(jobDir, outputRoot, taskId) {
  const candidates = collectCandidatesFromJob(jobDir);
  writeJsonAtomic(path.join(jobDir, 'media-candidates.json'), candidateReport(candidates));
  const acceptable = candidates.filter((item) => !item.watermarked);
  const attempts = [];
  for (const candidate of acceptable) {
    const outputPath = path.join(outputRoot, `${safeSegment(taskId, 'task')}.mp4`);
    try {
      const download = await downloadCandidate(candidate, outputPath);
      const result = {
        ok: true,
        output: download,
        selected: { redactedUrl: candidate.redactedUrl, score: candidate.score, unwatermarked: candidate.unwatermarked, original: candidate.original },
        attempts
      };
      writeJsonAtomic(path.join(jobDir, 'media-resolution.json'), result);
      return result;
    } catch (error) {
      attempts.push({ redactedUrl: candidate.redactedUrl, error: error.code || error.message, statusCode: error.statusCode || null });
    }
  }
  const result = {
    ok: false,
    error: candidates.length ? 'NO_ACCESSIBLE_ACCEPTABLE_MEDIA' : 'NO_MEDIA_CANDIDATES',
    candidateCount: candidates.length,
    attempts
  };
  writeJsonAtomic(path.join(jobDir, 'media-resolution.json'), result);
  return result;
}

module.exports = {
  redactUrl,
  looksLikeMediaUrl,
  extractMediaCandidates,
  scoreCandidate,
  collectCandidatesFromJob,
  validateMp4,
  downloadCandidate,
  resolveJobMedia
};
