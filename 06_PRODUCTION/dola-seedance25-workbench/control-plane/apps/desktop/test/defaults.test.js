'use strict';

const assert = require('node:assert/strict');
const test = require('node:test');
const { DEFAULT_INITIAL_VAULT_PASSWORD } = require('../src/core/defaults');

test('first-run default vault password is explicit and non-empty', () => {
  assert.equal(typeof DEFAULT_INITIAL_VAULT_PASSWORD, 'string');
  assert.equal(DEFAULT_INITIAL_VAULT_PASSWORD.length >= 12, true);
});
