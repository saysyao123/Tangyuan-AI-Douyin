'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { DolaBackgroundRunner } = require('./background-dola');
const { ProviderLifecycleStore } = require('./core/provider-lifecycle-store');
const { resolveJobMedia } = require('./core/dola-media-resolver');
const { writeJsonAtomic } = require('./core/atomic-json');
const { getPortableRuntime } = require('./core/portable-runtime');

function sleep(ms) { return new Promise((resolve) => setTimeout(resolve, ms)); }
function text(value) { return String(value || '').slice(0, 500); }
function isObservationTimeout(value) { return /timed out before media identity|observation.*timed out/i.test(String(value || '')); }
function isLoginError(value) { return /logged out|login required|登录|请先登录|登录已过期/i.test(String(value || '')); }
function isProviderReject(value) { return /provider rejected|肖像保护|未认证人脸|country restricted|quota|rate limit|entitlement|permission/i.test(String(value || '')); }

function domMediaSnapshotScript() {
  return `(() => {
    const urls = new Set();
    const add = (value) => {
      if (typeof value !== 'string' || !/^https?:\\/\\//i.test(value)) return;
      if (/video|media|play|download|\\.mp4|\\.mov/i.test(value)) urls.add(value);
    };
    for (const el of document.querySelectorAll('video,source,a,[src],[href],[data-src],[data-url]')) {
      for (const name of ['src','href','data-src','data-url']) add(el.getAttribute?.(name));
      try { add(el.src); } catch (_) {}
      try { add(el.href); } catch (_) {}
    }
    const body = String(document.body?.innerText || '').slice(0, 120000);
    for (const match of body.match(/https?:\\/\\/[^\\s"'<>]+/g) || []) add(match);
    const pathname = String(location.pathname || '');
    return {
      pathname,
      title: String(document.title || '').slice(0, 200),
      urls: [...urls].slice(0, 200),
      generating: /(生成中|正在生成|generating|processing)/i.test(body),
      failed: /(生成失败|failed to generate|generation failed)/i.test(body)
    };
  })()`;
}

class PortableDolaBackgroundRunner extends DolaBackgroundRunner {
  constructor(options = {}) {
    const updateTask = options.updateTask;
    const updateAccount = options.updateAccount;
    const stateRoot = process.env.DOLA_WORKBENCH_STATE_ROOT || path.join(options.outputRoot || process.cwd(), 'portable-state');
    const lifecycle = new ProviderLifecycleStore(stateRoot);
    const lifecycleUpdateTask = async (taskId, patch = {}) => {
      const next = { ...patch };
      const errorText = text(next.error);
      try {
        if (next.state === 'capture_armed') lifecycle.transition(taskId, 'ACKNOWLEDGED', {}, 'network-capture-armed');
        if (next.state === 'generation_running') {
          const record = lifecycle.get(taskId);
          if (record?.state !== 'SUBMITTED') lifecycle.markSubmitted(taskId);
          lifecycle.transition(taskId, 'GENERATING', {}, 'provider-generation-observed');
        }
        if (next.state === 'success') {
          next.state = 'result_observed';
          lifecycle.transition(taskId, 'RESULT_OBSERVED', { mediaObserved: true }, 'media-identity-observed');
        }
        if (next.state === 'failed' && isObservationTimeout(errorText)) {
          next.state = 'observation_wait';
          next.error = null;
          next.blockedReason = 'OBSERVATION_WAIT';
          lifecycle.markObservationWait(taskId, { lastError: null });
        } else if (next.state === 'failed' && isLoginError(errorText)) {
          lifecycle.transition(taskId, 'LOGIN_REQUIRED', { error: errorText }, 'login-required');
        } else if (next.state === 'failed' && isProviderReject(errorText)) {
          lifecycle.transition(taskId, 'PROVIDER_REJECTED', { error: errorText }, 'provider-rejected-request');
        } else if (next.state === 'failed') {
          lifecycle.transition(taskId, 'FAILED', { error: errorText }, 'provider-run-failed');
        }
      } catch (_) {}
      return updateTask(taskId, next);
    };

    const lifecycleUpdateAccount = async (accountId, patch = {}) => {
      const next = { ...patch };
      if (next.status === 'ERROR' && isObservationTimeout(next.lastError)) {
        next.status = 'READY';
        next.lastError = '';
      }
      return updateAccount(accountId, next);
    };

    super({ ...options, updateTask: lifecycleUpdateTask, updateAccount: lifecycleUpdateAccount });
    this.directUpdateTask = updateTask;
    this.directUpdateAccount = updateAccount;
    this.lifecycleStore = lifecycle;
    this.mediaOutputRoot = path.resolve(process.env.DOLA_WORKBENCH_OUTPUT_ROOT || path.join(options.outputRoot || process.cwd(), 'resolved-media'));
    fs.mkdirSync(this.mediaOutputRoot, { recursive: true });
    try {
      const runtime = getPortableRuntime();
      if (runtime) runtime.backgroundRunner = this;
    } catch (_) {}
  }

  async finalizeMedia(task, account, result) {
    const jobDir = result?.artifactDir || task.artifactDir || path.join(this.outputRoot, 'jobs', task.id);
    try { this.lifecycleStore.transition(task.id, 'RESOLVING', {}, 'rank-and-download-media-candidates'); } catch (_) {}
    const media = await resolveJobMedia(jobDir, this.mediaOutputRoot, task.id);
    if (media.ok) {
      await this.directUpdateTask(task.id, {
        state: 'success',
        blockedReason: null,
        outputPath: media.output.path,
        outputBytes: media.output.bytes,
        outputSha256: media.output.sha256,
        mediaResolution: media.selected,
        error: null,
        updatedAt: Date.now()
      });
      try {
        this.lifecycleStore.transition(task.id, 'SUCCESS', {
          mediaObserved: true,
          outputPath: media.output.path,
          error: null
        }, 'highest-ranked-accessible-media-downloaded');
      } catch (_) {}
      await this.directUpdateAccount(account.id, { status: 'READY', lastError: '' });
      return { ...result, ok: true, media };
    }

    await this.directUpdateTask(task.id, {
      state: 'observation_wait',
      blockedReason: media.error,
      error: null,
      updatedAt: Date.now()
    });
    try { this.lifecycleStore.markObservationWait(task.id, { mediaObserved: false, resolutionError: media.error }); } catch (_) {}
    await this.directUpdateAccount(account.id, { status: 'READY', lastError: '' });
    return { ...result, ok: false, recoverable: true, media };
  }

  run(task, account) {
    this.lifecycleStore.begin(task, account);
    try { this.lifecycleStore.transition(task.id, 'PREPARING', {}, 'portable-runner-start'); } catch (_) {}
    // Portable V1 concurrency is controlled by WorkerScheduler. Calling _run
    // directly here permits independent account partitions to run concurrently
    // while the scheduler still guarantees one lease per account and the
    // configured global cap (default 3). The legacy runner's queueTail remains
    // intact for legacy call sites.
    return this._run(task, account).then(async (result) => {
      if (result?.ok) return this.finalizeMedia(task, account, result);
      if (isObservationTimeout(result?.error)) {
        return { ...result, recoverable: true, state: 'OBSERVATION_WAIT' };
      }
      return result;
    });
  }

  async recover(task, account, options = {}) {
    const jobDir = task.artifactDir || path.join(this.outputRoot, 'jobs', task.id);
    fs.mkdirSync(path.join(jobDir, 'raw-responses'), { recursive: true });
    if (!this.lifecycleStore.get(task.id)) this.lifecycleStore.begin(task, account);
    try { this.lifecycleStore.transition(task.id, 'RECOVERY_REQUIRED', {}, 'explicit-recovery-without-resubmit'); } catch (_) {}

    const existing = await resolveJobMedia(jobDir, this.mediaOutputRoot, task.id);
    if (existing.ok) return this._finishRecovered(task, account, existing);

    const slot = await this.ensureSlot(account);
    const sessionState = await this.sessionStatus(account);
    if (sessionState.loginStatus === 'logged_out') {
      await this.directUpdateTask(task.id, { state: 'login_required', blockedReason: 'LOGIN_REQUIRED', error: null, updatedAt: Date.now() });
      this.lifecycleStore.transition(task.id, 'LOGIN_REQUIRED', {}, 'recovery-session-logged-out');
      return { ok: false, recoverable: true, loginRequired: true };
    }

    const waitMs = Math.max(5_000, Math.min(120_000, Number(options.waitMs || 60_000)));
    const deadline = Date.now() + waitMs;
    let counter = 0;
    while (Date.now() < deadline) {
      const snapshot = await this.execute(slot, domMediaSnapshotScript()).catch(() => ({ urls: [] }));
      writeJsonAtomic(path.join(jobDir, 'recovery-page.json'), snapshot);
      if (Array.isArray(snapshot.urls) && snapshot.urls.length) {
        writeJsonAtomic(path.join(jobDir, 'raw-responses', `recovery-${String(counter++).padStart(4, '0')}.json`), {
          request: { url: `https://www.dola.com${snapshot.pathname || '/chat/'}`, status: 200, mime_type: 'application/json', source: 'recovery-dom' },
          body: JSON.stringify({ video_list: snapshot.urls.map((url) => ({ main_url: url })) })
        });
        const media = await resolveJobMedia(jobDir, this.mediaOutputRoot, task.id);
        if (media.ok) return this._finishRecovered(task, account, media);
      }
      if (snapshot.failed) {
        this.lifecycleStore.transition(task.id, 'PROVIDER_REJECTED', { error: 'Generation page reports failure.' }, 'recovery-page-failure');
        await this.directUpdateTask(task.id, { state: 'failed', error: 'Generation page reports failure.', updatedAt: Date.now() });
        return { ok: false, recoverable: false, error: 'Generation page reports failure.' };
      }
      await sleep(1500);
    }

    this.lifecycleStore.markObservationWait(task.id, { lastObservedAt: Date.now() });
    await this.directUpdateTask(task.id, { state: 'observation_wait', blockedReason: 'OBSERVATION_WAIT', error: null, updatedAt: Date.now() });
    return { ok: false, recoverable: true, state: 'OBSERVATION_WAIT' };
  }

  async _finishRecovered(task, account, media) {
    await this.directUpdateTask(task.id, {
      state: 'success',
      blockedReason: null,
      outputPath: media.output.path,
      outputBytes: media.output.bytes,
      outputSha256: media.output.sha256,
      mediaResolution: media.selected,
      error: null,
      updatedAt: Date.now()
    });
    this.lifecycleStore.transition(task.id, 'SUCCESS', { mediaObserved: true, outputPath: media.output.path, error: null }, 'recovered-without-resubmit');
    await this.directUpdateAccount(account.id, { status: 'READY', lastError: '' });
    return { ok: true, recovered: true, media };
  }
}

module.exports = { PortableDolaBackgroundRunner, domMediaSnapshotScript, isObservationTimeout };
