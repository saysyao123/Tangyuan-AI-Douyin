'use strict';

let runtime = null;

function installPortableRuntime(value) {
  if (!value || typeof value !== 'object') throw new Error('Portable runtime object is required.');
  if (runtime) throw new Error('Portable runtime is already installed.');
  runtime = value;
  return runtime;
}

function getPortableRuntime() {
  return runtime;
}

function requirePortableRuntime() {
  if (!runtime) {
    const error = new Error('Portable runtime is not installed.');
    error.code = 'PORTABLE_RUNTIME_UNAVAILABLE';
    throw error;
  }
  return runtime;
}

module.exports = { installPortableRuntime, getPortableRuntime, requirePortableRuntime };
