'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const {
  LAYOUT_VERSION,
  resolvePortableRoot,
  buildPortableLayout,
  ensurePortableLayout
} = require('../src/core/portable-paths');

test('explicit DOLA_WORKBENCH_ROOT wins', () => {
  const root = resolvePortableRoot({
    env: { DOLA_WORKBENCH_ROOT: 'C:\\Portable\\DolaWorkbench', PORTABLE_EXECUTABLE_DIR: 'C:\\Other' },
    execPath: 'C:\\App\\DolaWorkbench.exe',
    isPackaged: true,
    moduleDir: __dirname
  });
  assert.equal(root, path.resolve('C:\\Portable\\DolaWorkbench'));
});

test('PORTABLE_EXECUTABLE_DIR is used for portable packaged builds', () => {
  const root = resolvePortableRoot({
    env: { PORTABLE_EXECUTABLE_DIR: 'D:\\Tools\\DolaWorkbench' },
    execPath: 'C:\\Temp\\unpacked\\DolaWorkbench.exe',
    isPackaged: true,
    moduleDir: __dirname
  });
  assert.equal(root, path.resolve('D:\\Tools\\DolaWorkbench'));
});

test('development root stays under apps/desktop/.portable-dev', () => {
  const fakeModuleDir = path.join('C:\\repo', 'control-plane', 'apps', 'desktop', 'src', 'core');
  const root = resolvePortableRoot({ env: {}, execPath: 'C:\\node\\node.exe', isPackaged: false, moduleDir: fakeModuleDir });
  assert.equal(root, path.resolve(fakeModuleDir, '..', '..', '.portable-dev'));
});

test('layout separates runtime, browser sessionData and durable data roots', () => {
  const layout = buildPortableLayout(path.join(os.tmpdir(), 'dola-layout-example'));
  assert.equal(path.dirname(layout.controlDir), layout.runtimeDir);
  assert.equal(path.dirname(layout.vaultDir), layout.dataDir);
  assert.equal(path.dirname(layout.projectsDir), layout.dataDir);
  assert.equal(path.dirname(layout.outputsDir), layout.dataDir);
  assert.notEqual(layout.runtimeDir, layout.dataDir);
  assert.equal(layout.sessionDataDir.startsWith(layout.runtimeDir), true);
  assert.equal(layout.electronUserData.startsWith(layout.dataDir), true);
  assert.equal(layout.sessionDataDir.startsWith(layout.electronUserData), false);
});

test('ensurePortableLayout creates versioned marker and required directories', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'dola-portable-test-'));
  try {
    const layout = buildPortableLayout(root);
    const marker = ensurePortableLayout(layout);
    assert.equal(marker.version, LAYOUT_VERSION);
    for (const dir of [
      layout.controlDir,
      layout.sessionDataDir,
      layout.vaultWorkingDir,
      layout.electronUserData,
      layout.vaultDir,
      layout.projectsDir,
      layout.outputsDir,
      layout.stateDir,
      layout.backupsDir
    ]) {
      assert.equal(fs.statSync(dir).isDirectory(), true, dir);
    }
    const persisted = JSON.parse(fs.readFileSync(layout.layoutMarker, 'utf8'));
    assert.equal(persisted.version, LAYOUT_VERSION);
    assert.equal(persisted.rootKind, 'dola-workbench-portable');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});
