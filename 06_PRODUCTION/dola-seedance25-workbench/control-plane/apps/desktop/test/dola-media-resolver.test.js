'use strict';

const assert = require('node:assert/strict');
const test = require('node:test');
const { extractMediaCandidates } = require('../src/core/dola-media-resolver');

test('resolver ranks explicit unwatermarked original above preview/watermarked sources', () => {
  const body = JSON.stringify({
    video_list: [
      { preview_url: 'https://media.example.test/preview.mp4?watermarked=1', width: 720, height: 1280 },
      { original_media_info: { main_url: 'https://media.example.test/original.mp4?logo_type=unwatermarked', width: 1080, height: 1920, bitrate: 8000000 } }
    ]
  });
  const candidates = extractMediaCandidates(body);
  assert.equal(candidates.length >= 2, true);
  assert.match(candidates[0].redactedUrl, /original\.mp4$/);
  assert.equal(candidates[0].unwatermarked, true);
  const marked = candidates.find((item) => /preview\.mp4$/.test(item.redactedUrl));
  assert.equal(marked.watermarked, true);
  assert.equal(candidates[0].score > marked.score, true);
});

test('resolver does not treat arbitrary text as a media URL', () => {
  const candidates = extractMediaCandidates(JSON.stringify({ text: 'hello', url: 'https://example.test/page' }));
  assert.equal(candidates.length, 0);
});
