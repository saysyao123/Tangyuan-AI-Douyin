'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '..');
const appJs = fs.readFileSync(path.join(ROOT, 'src', 'renderer', 'app.js'), 'utf8');
const portableActions = fs.readFileSync(path.join(ROOT, 'src', 'renderer', 'portable-actions.js'), 'utf8');
const html = fs.readFileSync(path.join(ROOT, 'src', 'renderer', 'index.html'), 'utf8');
const preload = fs.readFileSync(path.join(ROOT, 'src', 'preload.js'), 'utf8');
const portableMain = fs.readFileSync(path.join(ROOT, 'src', 'portable-main.js'), 'utf8');
const portableIpc = fs.readFileSync(path.join(ROOT, 'src', 'portable-ipc.js'), 'utf8');

test('renderer does not depend on unsupported browser prompt dialogs', () => {
  assert.equal(/window\.(prompt|alert|confirm)\s*\(/.test(appJs), false);
  assert.equal(/vault-settings\.js/.test(html), false);
});

test('account creation and password change use dedicated in-app forms', () => {
  for (const id of ['addAccountModal', 'addAccountForm', 'accountNameInput', 'passwordModal', 'passwordForm', 'newVaultPassword']) {
    assert.match(html, new RegExp(`id=["']${id}["']`));
  }
  assert.match(appJs, /bridge\.addAccount\(name\)/);
  assert.match(appJs, /bridge\.changeVaultPassword\(current, next\)/);
});

test('i2v image picker is wired through preload and portable main', () => {
  assert.match(html, /id="pickImage"/);
  assert.match(preload, /portable:pick-image/);
  assert.match(portableMain, /registerPortableDialogIpc/);
  assert.match(appJs, /bridge\.pickImage\(\)/);
});

test('task form defaults to the Dola portable provider path', () => {
  assert.match(appJs, /provider:\s*'dola-web'/);
  assert.match(appJs, /model:\s*'seedance-v2\.5'/);
});

test('desktop dispatch prefers the currently visible Dola webview', () => {
  assert.match(portableIpc, /getAllWebContents\(\)/);
  assert.match(portableIpc, /item\.getType\(\) === 'webview'/);
  assert.match(portableIpc, /executionSurface:\s*'visible-webview'/);
  assert.match(portableIpc, /dispatchVisibleTask\(runtime, id\)/);
  assert.match(portableIpc, /VISIBLE_DOLA_VIEW_NOT_READY/);
  assert.match(portableIpc, /localControlRequest\(runtime, 'POST', `\/v1\/tasks\/\$\{encodeURIComponent/);
});

test('right studio exposes a full-height vertical scroll path and task failure detail', () => {
  assert.match(portableActions, /overflow-y:\s*scroll\s*!important/);
  assert.match(portableActions, /scrollbar-gutter:\s*stable/);
  assert.match(portableActions, /失败原因：\$\{failure\}/);
  assert.match(portableActions, /执行位置：中间可见 Dola 网页/);
});
