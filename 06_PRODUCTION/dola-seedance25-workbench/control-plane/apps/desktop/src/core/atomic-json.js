'use strict';

const fs = require('node:fs');
const path = require('node:path');

function readJson(filePath, fallback = null) {
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (_) {
    return fallback;
  }
}

function writeJsonAtomic(filePath, payload) {
  const target = path.resolve(filePath);
  const partial = `${target}.part-${process.pid}-${Date.now()}`;
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(partial, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
  fs.renameSync(partial, target);
  return target;
}

function safeSegment(value, fallback = 'item') {
  const raw = String(value || '').trim();
  const cleaned = raw
    .replace(/[<>:"/\\|?*\x00-\x1f]/g, '-')
    .replace(/[. ]+$/g, '')
    .replace(/\s+/g, '_')
    .replace(/-+/g, '-')
    .slice(0, 96);
  const reserved = /^(con|prn|aux|nul|com[1-9]|lpt[1-9])$/i;
  if (!cleaned || reserved.test(cleaned)) return fallback;
  return cleaned;
}

module.exports = { readJson, writeJsonAtomic, safeSegment };
