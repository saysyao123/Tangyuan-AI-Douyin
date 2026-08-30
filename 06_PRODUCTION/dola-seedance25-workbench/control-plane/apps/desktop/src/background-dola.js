'use strict';

const { BrowserWindow } = require('electron');
const fs = require('node:fs');
const path = require('node:path');

const DOLA_HOME = 'https://www.dola.com/chat/';
const DOLA_CREATE_IMAGE = 'https://www.dola.com/chat/create-image';
const DOLA_HOSTS = new Set(['dola.com', 'www.dola.com']);
const DEFAULT_WAIT_SECONDS = 180;
const EXECUTE_TIMEOUT_MS = 8000;

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function writeJsonAtomic(filePath, payload) {
  const target = path.resolve(filePath);
  const partial = `${target}.part`;
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(partial, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
  fs.renameSync(partial, target);
}

function redactedUrl(value) {
  try {
    const parsed = new URL(String(value));
    return `${parsed.origin}${parsed.pathname}`;
  } catch (_) {
    return '';
  }
}

function isDolaUrl(value) {
  try {
    const parsed = new URL(String(value));
    return parsed.protocol === 'https:' && DOLA_HOSTS.has(parsed.hostname.toLowerCase());
  } catch (_) {
    return false;
  }
}

function isInterestingResponse(value) {
  if (!isDolaUrl(value)) return false;
  try {
    const pathname = new URL(value).pathname.toLowerCase();
    return pathname.includes('/chat/completion')
      || pathname.includes('/im/')
      || pathname.includes('/samantha/')
      || pathname.includes('/video/')
      || pathname.includes('/media/');
  } catch (_) {
    return false;
  }
}

function identitySummary() {
  return {
    task_id_found: false,
    generation_id_found: false,
    conversation_id_found: false,
    message_id_found: false,
    vid_found: false,
    node_id_found: false,
    media_key_found: false,
    fallback_api_found: false,
    key_seed_found: false,
    video_list_found: false,
    video_list_count: 0,
    original_media_info_found: false,
    media_info_found: false,
    main_url_found: false,
    response_count: 0,
    identity_pass: false,
    response_paths: []
  };
}

function mergeIdentity(target, source) {
  for (const key of [
    'task_id_found', 'generation_id_found', 'conversation_id_found', 'message_id_found',
    'vid_found', 'node_id_found', 'media_key_found', 'fallback_api_found',
    'key_seed_found', 'video_list_found', 'original_media_info_found',
    'media_info_found', 'main_url_found', 'identity_pass'
  ]) {
    target[key] = target[key] || source[key] === true;
  }
  target.video_list_count += Number(source.video_list_count || 0);
  target.response_count += Number(source.response_count || 0);
  for (const item of source.response_paths || []) {
    if (item && !target.response_paths.includes(item)) target.response_paths.push(item);
  }
  return target;
}

function tryParseJsonStrings(value, visit) {
  if (typeof value !== 'string' || value.length > 500000) return;
  const text = value.trim();
  if (!text) return;
  try {
    visit(JSON.parse(text));
    return;
  } catch (_) {}
  for (const line of text.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed.startsWith('data:')) continue;
    const data = trimmed.slice(5).trim();
    if (!data || data === '[DONE]') continue;
    try { visit(JSON.parse(data)); } catch (_) {}
  }
}

function extractIdentity(body, responsePath) {
  const result = identitySummary();
  result.response_count = 1;
  if (responsePath) result.response_paths.push(responsePath);
  const visitedStrings = new Set();

  function scan(value, context = '') {
    if (value === null || value === undefined) return;
    if (typeof value === 'string') {
      const marker = value.slice(0, 500000);
      if (visitedStrings.has(marker)) return;
      visitedStrings.add(marker);
      if (/fallback_api|video_list|original_media_info|media_info|main_url|node_id|key_seed|"vid"/i.test(marker)) {
        tryParseJsonStrings(marker, (parsed) => scan(parsed, context));
      }
      return;
    }
    if (Array.isArray(value)) {
      if (context === 'video_list') {
        result.video_list_found = true;
        result.video_list_count += value.length;
      }
      for (const item of value.slice(0, 200)) scan(item, context);
      return;
    }
    if (typeof value !== 'object') return;

    const keys = Object.keys(value);
    const normalized = new Set(keys.map((key) => key.toLowerCase().replace(/[^a-z0-9]/g, '')));
    const mediaContext = /video|media|play|generation|download|chain|completion/i.test(context)
      || normalized.has('nodeid') || normalized.has('videolist') || normalized.has('mediainfo');

    for (const key of keys) {
      const normalizedKey = key.toLowerCase().replace(/[^a-z0-9]/g, '');
      const child = value[key];
      if (normalizedKey === 'taskid') result.task_id_found = true;
      if (normalizedKey === 'generationid') result.generation_id_found = true;
      if (normalizedKey === 'conversationid') result.conversation_id_found = true;
      if (normalizedKey === 'messageid') result.message_id_found = true;
      if (normalizedKey === 'vid' || normalizedKey === 'videoid') result.vid_found = true;
      if (normalizedKey === 'nodeid') result.node_id_found = true;
      if (normalizedKey === 'key' && mediaContext) result.media_key_found = true;
      if (normalizedKey === 'fallbackapi') result.fallback_api_found = true;
      if (normalizedKey === 'keyseed') result.key_seed_found = true;
      if (normalizedKey === 'videolist') {
        result.video_list_found = true;
        if (Array.isArray(child)) result.video_list_count += child.length;
      }
      if (normalizedKey === 'originalmediainfo') result.original_media_info_found = true;
      if (normalizedKey === 'mediainfo') result.media_info_found = true;
      if (normalizedKey === 'mainurl') result.main_url_found = true;
      scan(child, normalizedKey);
    }
  }

  tryParseJsonStrings(body, (parsed) => scan(parsed, 'response'));
  result.identity_pass = result.vid_found
    || (result.node_id_found && result.media_key_found)
    || result.fallback_api_found
    || result.video_list_found
    || result.original_media_info_found
    || result.main_url_found;
  return result;
}

function findVisibleButtonScript(matcher, exact = false) {
  const matcherLiteral = JSON.stringify(String(matcher));
  return `(() => {
    const target = ${matcherLiteral};
    const exact = ${exact ? 'true' : 'false'};
    const visible = (el) => !!el && !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
    const text = (el) => String(el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
    const buttons = Array.from(document.querySelectorAll('button,[role="button"],a,[tabindex],div,span'))
      .filter((el) => visible(el) && text(el).length <= 100);
    const item = buttons.find((el) => {
      const value = text(el);
      return exact ? value === target : value.includes(target);
    });
    if (!item || item.disabled) return false;
    item.click();
    return true;
  })()`;
}

function findVisibleTargetRectScript(matcher, exact = false) {
  const matcherLiteral = JSON.stringify(String(matcher));
  return `(() => {
    const target = ${matcherLiteral};
    const exact = ${exact ? 'true' : 'false'};
    const visible = (el) => !!el && !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
    const text = (el) => String(el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
    const nodes = Array.from(document.querySelectorAll('button,[role="button"],a,[tabindex],div,span'))
      .filter((el) => visible(el) && text(el).length <= 100);
    const item = nodes.find((el) => {
      const value = text(el);
      return exact ? value === target : value.includes(target);
    });
    if (!item) return null;
    const rect = item.getBoundingClientRect();
    return { x: rect.left + rect.width / 2, y: rect.top + rect.height / 2, width: rect.width, height: rect.height };
  })()`;
}

function findVisibleButtonRectScript(matcher, exact = false) {
  const matcherLiteral = JSON.stringify(String(matcher));
  return `(() => {
    const target = ${matcherLiteral};
    const exact = ${exact ? 'true' : 'false'};
    const visible = (el) => !!el && !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
    const text = (el) => String(el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
    // Prefer the actual interactive element. Some Dola sessions also expose
    // the same label on ancestor div/span wrappers, so a broad DOM scan must
    // only be used when no semantic candidate exists.
    const semantic = Array.from(document.querySelectorAll('button,[role="button"],a,[tabindex]'))
      .filter((el) => visible(el) && text(el).length <= 100);
    const nodes = (semantic.length ? semantic : Array.from(document.querySelectorAll('div,span')))
      .filter((el) => visible(el) && text(el).length <= 100);
    const item = nodes.find((el) => {
      const value = text(el);
      return exact ? value === target : value.includes(target);
    });
    if (!item || item.disabled || item.getAttribute('aria-disabled') === 'true') return null;
    const rect = item.getBoundingClientRect();
    return { x: rect.left + rect.width / 2, y: rect.top + rect.height / 2, width: rect.width, height: rect.height, text: text(item) };
  })()`;
}

function clickVisibleButtonScript(matcher, exact = false) {
  const matcherLiteral = JSON.stringify(String(matcher));
  return `(() => {
    const target = ${matcherLiteral};
    const exact = ${exact ? 'true' : 'false'};
    const visible = (el) => !!el && !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
    const text = (el) => String(el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
    const nodes = Array.from(document.querySelectorAll('button,[role="button"],a'))
      .filter((el) => visible(el) && text(el).length <= 100);
    const item = nodes.find((el) => {
      const value = text(el);
      return exact ? value === target : value.includes(target);
    });
    if (!item || item.disabled || item.getAttribute('aria-disabled') === 'true') return false;
    item.click();
    return true;
  })()`;
}

function focusVisibleButtonScript(matcher, exact = false) {
  const matcherLiteral = JSON.stringify(String(matcher));
  return `(() => {
    const target = ${matcherLiteral};
    const exact = ${exact ? 'true' : 'false'};
    const visible = (el) => !!el && !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
    const text = (el) => String(el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
    const item = Array.from(document.querySelectorAll('button,[role="button"],a'))
      .filter((el) => visible(el) && text(el).length <= 100)
      .find((el) => exact ? text(el) === target : text(el).includes(target));
    if (!item || item.disabled || item.getAttribute('aria-disabled') === 'true') return false;
    item.focus();
    return true;
  })()`;
}

function clickMenuItemScript(value, contains = false) {
  const literal = JSON.stringify(String(value));
  return `(() => {
    const target = ${literal};
    const contains = ${contains ? 'true' : 'false'};
    const visible = (el) => !!el && !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
    const text = (el) => String(el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
    const normalize = (value) => String(value || '').replace(/\\s+/g, '').replace(/[：]/g, ':');
    const nodes = Array.from(document.querySelectorAll('[role="menuitem"],button,[role="option"],[role="menuitemradio"],[role="radio"],li,[data-value],[data-radix-collection-item],div,span'))
      .filter((el) => visible(el) && text(el).length <= 40);
    const matches = nodes.filter((el) => {
      const value = text(el);
      return contains
        ? value.includes(target) || normalize(value).includes(normalize(target))
        : value === target || normalize(value) === normalize(target);
    });
    const item = matches.sort((a, b) => {
      const aText = text(a); const bText = text(b);
      const aExact = aText === target || normalize(aText) === normalize(target);
      const bExact = bText === target || normalize(bText) === normalize(target);
      if (aExact !== bExact) return aExact ? -1 : 1;
      return aText.length - bText.length;
    })[0];
    if (!item || item.disabled) return false;
    item.click();
    return true;
  })()`;
}

function findVisibleMenuItemRectScript(value, contains = false) {
  const literal = JSON.stringify(String(value));
  return `(() => {
    const target = ${literal};
    const contains = ${contains ? 'true' : 'false'};
    const visible = (el) => !!el && !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
    const text = (el) => String(el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
    const normalize = (value) => String(value || '').replace(/\\s+/g, '').replace(/[：]/g, ':');
    const nodes = Array.from(document.querySelectorAll('[role="menuitem"],button,[role="option"],[role="menuitemradio"],[role="radio"],li,[data-value],[data-radix-collection-item],div,span'))
      .filter((el) => visible(el) && text(el).length <= 60);
    const matches = nodes.filter((el) => {
      const value = text(el);
      return contains
        ? value.includes(target) || normalize(value).includes(normalize(target))
        : value === target || normalize(value) === normalize(target);
    }).sort((a, b) => {
      const aText = text(a); const bText = text(b);
      const aExact = aText === target || normalize(aText) === normalize(target);
      const bExact = bText === target || normalize(bText) === normalize(target);
      if (aExact !== bExact) return aExact ? -1 : 1;
      return aText.length - bText.length;
    });
    const item = matches[0];
    if (!item || item.disabled || item.getAttribute('aria-disabled') === 'true') return null;
    const rect = item.getBoundingClientRect();
    return { x: rect.left + rect.width / 2, y: rect.top + rect.height / 2, text: text(item) };
  })()`;
}

function chooseDurationScript(value) {
  const literal = JSON.stringify(String(value));
  return `(() => {
    const target = ${literal};
    const visible = (el) => !!el && !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
    const text = (el) => String(el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
    const nodes = Array.from(document.querySelectorAll('button,[role="button"],[role="option"]')).filter(visible);
    const item = nodes.find((el) => text(el) === target || text(el).replace(/\\s+/g, '') === target.replace(/\\s+/g, ''));
    if (!item || item.disabled) return false;
    item.click();
    return true;
  })()`;
}

function composerReadyScript() {
  return `(() => {
    const body = String(document.body?.innerText || '');
    const visible = (el) => !!el && !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
    const text = (el) => String(el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
    const promptEditors = Array.from(document.querySelectorAll('textarea:not([disabled]),[contenteditable],[role="textbox"],[aria-label="doc_editor"]'));
    const promptEditor = promptEditors.some((el) => {
      const marker = [
        el.getAttribute('placeholder'), el.getAttribute('data-placeholder'),
        el.getAttribute('aria-placeholder'), el.getAttribute('aria-label')
      ].filter(Boolean).join(' ');
      return marker.includes('描述你想要的视频') || marker.includes('视频')
        || (el.getAttribute('role') === 'textbox' && !el.getAttribute('aria-disabled'))
        || el.matches('textarea,[contenteditable],[role="textbox"],[aria-label="doc_editor"]');
    });
    const visibleModel = Array.from(document.querySelectorAll('button,[role="button"]'))
      .filter(visible)
      .map((el) => text(el))
      .find((value) => value.includes('模型')) || '';
    const hasVideoMode = /seedance|2\.5/i.test(visibleModel);
    // The creator's doc_editor can be mounted through a custom/shadow-backed
    // renderer and is not always enumerable from the page document. The
    // subsequent fill step has its own strict editor confirmation, so the
    // current visible Seedance model is the reliable mode gate here.
    return hasVideoMode;
  })()`;
}

function fillPromptScript(prompt) {
  const literal = JSON.stringify(String(prompt));
  return `(() => {
    const value = ${literal};
    const visible = (el) => !!el && !el.disabled && !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
    const marker = (el) => [
      el.getAttribute('placeholder'), el.getAttribute('data-placeholder'),
      el.getAttribute('aria-placeholder'), el.getAttribute('aria-label')
    ].filter(Boolean).join(' ');
    const candidates = Array.from(document.querySelectorAll('textarea:not([disabled]),[contenteditable],[role="textbox"],[aria-label="doc_editor"],input:not([disabled])'))
      .filter(visible)
      .sort((a, b) => {
        const score = (el) => (marker(el).includes('视频') || marker(el).includes('描述') ? 100 : 0)
          + (el.matches('[contenteditable="true"]') ? 30 : 0)
          + (el.getAttribute('role') === 'textbox' ? 20 : 0)
          + (el.tagName === 'TEXTAREA' ? 10 : 0);
        return score(b) - score(a);
      });
    const editor = candidates[0];
    if (!editor) return { ok: false, reason: 'prompt_editor_not_found' };
    editor.focus();
    if (editor.matches('[contenteditable],[role="textbox"],[aria-label="doc_editor"]') && editor.tagName !== 'TEXTAREA') {
      const range = document.createRange();
      range.selectNodeContents(editor);
      const selection = window.getSelection();
      selection?.removeAllRanges();
      selection?.addRange(range);
      const inserted = document.execCommand('insertText', false, value);
      if (!inserted) editor.textContent = value;
    } else {
      const setter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value')?.set;
      if (setter) setter.call(editor, value); else editor.value = value;
    }
    editor.dispatchEvent(new InputEvent('input', { bubbles: true, inputType: 'insertText', data: value }));
    editor.dispatchEvent(new Event('change', { bubbles: true }));
    return { ok: true, tag: editor.tagName.toLowerCase(), role: editor.getAttribute('role') || '', marker: marker(editor) };
  })()`;
}

function promptEditorStateScript() {
  return `(() => {
    const visible = (el) => !!el && !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
    const marker = (el) => [
      el.getAttribute('placeholder'), el.getAttribute('data-placeholder'),
      el.getAttribute('aria-placeholder'), el.getAttribute('aria-label')
    ].filter(Boolean).join(' ');
    return Array.from(document.querySelectorAll('textarea,[contenteditable],[role="textbox"],[aria-label="doc_editor"],input'))
      .filter(visible)
      .map((el) => {
        const r = el.getBoundingClientRect();
        return {
          tag: el.tagName.toLowerCase(), role: el.getAttribute('role') || '', marker: marker(el),
          value: String(el.value || '').slice(0, 300), text: String(el.innerText || el.textContent || '').slice(0, 300),
          rect: { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) },
          html: String(el.outerHTML || '').slice(0, 500)
        };
      });
  })()`;
}

function focusPromptEditorScript() {
  return `(() => {
    const visible = (el) => !!el && !el.disabled && !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
    const marker = (el) => [
      el.getAttribute('placeholder'), el.getAttribute('data-placeholder'),
      el.getAttribute('aria-placeholder'), el.getAttribute('aria-label')
    ].filter(Boolean).join(' ');
    const candidates = Array.from(document.querySelectorAll('textarea:not([disabled]),[contenteditable],[role="textbox"],[aria-label="doc_editor"]'))
      .filter(visible)
      .sort((a, b) => {
        const score = (el) => (marker(el).includes('视频') || marker(el).includes('描述') ? 100 : 0)
          + (el.matches('[contenteditable="true"]') ? 30 : 0)
          + (el.getAttribute('role') === 'textbox' ? 20 : 0)
          + (el.tagName === 'TEXTAREA' ? 10 : 0);
        return score(b) - score(a);
      });
    const editor = candidates[0];
    if (!editor) return false;
    editor.focus();
    if (editor.tagName !== 'TEXTAREA') {
      const range = document.createRange();
      range.selectNodeContents(editor);
      const selection = window.getSelection();
      selection?.removeAllRanges();
      selection?.addRange(range);
    } else {
      editor.select();
    }
    return true;
  })()`;
}

function submitScript() {
  return `(() => {
    const visible = (el) => !!el && !el.disabled && el.getAttribute('aria-disabled') !== 'true'
      && !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
    const text = (el) => String(el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
    const label = (el) => [text(el), el.getAttribute('aria-label') || '', el.getAttribute('title') || '', el.getAttribute('data-testid') || ''].join(' ');
    const buttons = Array.from(document.querySelectorAll('button,[role="button"]')).filter(visible);
    const preferred = buttons.find((el) => /^(生成|生成视频|发送|提交)$/.test(text(el))
      || /(生成视频|发送消息|send|submit|generate)/i.test(label(el)));
    const fallback = buttons
      .map((el) => ({ el, rect: el.getBoundingClientRect(), label: label(el) }))
      .filter(({ rect, label: value }) => !value.trim()
        && rect.width >= 28 && rect.width <= 48 && rect.height >= 28 && rect.height <= 48
        // The creator composer is centered vertically on /chat/create-image;
        // its unlabeled send arrow is right-aligned inside the composer, not
        // necessarily at the bottom of the viewport.
        && rect.x > window.innerWidth * 0.86)
      .sort((a, b) => (b.rect.x + b.rect.y) - (a.rect.x + a.rect.y))[0]?.el;
    const target = preferred || fallback;
    if (!target) return {
      clicked: false,
      reason: 'submit_button_not_found',
      buttons: buttons.map((el) => {
        const rect = el.getBoundingClientRect();
        return {
          label: label(el).slice(0, 120),
          disabled: Boolean(el.disabled) || el.getAttribute('aria-disabled') === 'true',
          rect: { x: Math.round(rect.x), y: Math.round(rect.y), w: Math.round(rect.width), h: Math.round(rect.height) }
        };
      }).slice(-40)
    };
    const button = target;
    button.click();
    return { clicked: true, button: label(button).slice(0, 120), buttonCount: buttons.length };
  })()`;
}

function pageStatusScript() {
  return `(() => {
    const text = String(document.body?.innerText || '').slice(0, 80000);
    const lower = text.toLowerCase();
    const pathname = String(location.pathname || '');
    const visible = (el) => !!el && !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
    const hasPromptEditor = Array.from(document.querySelectorAll('textarea:not([disabled]),[contenteditable],[role="textbox"],[aria-label="doc_editor"]'))
      .some((el) => {
        const marker = [
          el.getAttribute('placeholder'), el.getAttribute('data-placeholder'),
          el.getAttribute('aria-placeholder'), el.getAttribute('aria-label')
        ].filter(Boolean).join(' ');
        return marker.includes('描述你想要的视频') || marker.includes('视频')
          || (el.getAttribute('role') === 'textbox' && !el.getAttribute('aria-disabled'))
          || el.matches('textarea,[contenteditable],[role="textbox"],[aria-label="doc_editor"]');
      });
    const visibleModel = Array.from(document.querySelectorAll('button,[role="button"]'))
      .filter(visible)
      .map((el) => String(el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim())
      .find((value) => value.includes('模型')) || '';
    const hasComposer = hasPromptEditor && /seedance|2\.5/i.test(visibleModel)
      && (text.includes('比例') || text.includes('10s') || text.includes('5s'));
    const hasEditor = !!document.querySelector('textarea:not([disabled]),[contenteditable],[role="textbox"],[aria-label="doc_editor"]');
    const logoutSignal = /(退出登录|退出账号|log out|logout|sign out|signout)/i.test(lower);
    const loginSignal = /(登录|log in|signin|sign in)/i.test(lower);
    const errorMarkers = [
      '出于肖像保护考虑', '未认证人脸暂不支持', 'country restricted',
      'quota', 'rate limit', '登录已过期', '请先登录'
    ];
    const error = errorMarkers.find((marker) => lower.includes(marker.toLowerCase())) || null;
    const loggedIn = hasComposer || hasEditor || logoutSignal;
    const loggedOut = !loggedIn && (/\\/(login|signin|sign-in)(\\/|$)/i.test(pathname)
      || !!document.querySelector('input[type="password"]')
      || loginSignal);
    const controls = Array.from(document.querySelectorAll('button,[role="button"],input,textarea,[contenteditable="true"],[aria-label],[title],[data-testid],[role]'))
      .filter(visible).map((el) => ({
        tag: el.tagName.toLowerCase(),
        text: String(el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim().slice(0, 80),
        aria: String(el.getAttribute('aria-label') || '').slice(0, 80),
        title: String(el.getAttribute('title') || '').slice(0, 80),
        placeholder: String(el.getAttribute('placeholder') || '').slice(0, 80),
        testid: String(el.getAttribute('data-testid') || '').slice(0, 80)
      })).filter((item) => item.text || item.aria || item.title || item.placeholder || item.testid).slice(0, 80);
    return { pathname, loggedIn, loggedOut, error, hasComposer, hasEditor, hasVideo: document.querySelectorAll('video').length > 0, controls };
  })()`;
}

function visibleUiDiagnosticScript() {
  return `(() => {
    const visible = (el) => !!el && !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
    const text = (el) => String(el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
    const nodes = Array.from(document.querySelectorAll('button,[role="button"],[role="menu"],[role="menuitem"],[role="option"],[role="radio"],li,[data-value],[data-radix-collection-item],input,textarea,[contenteditable="true"],[role="textbox"],div,span'))
      .filter((el) => visible(el) && text(el).length > 0 && text(el).length <= 100)
      .map((el) => ({
        tag: el.tagName.toLowerCase(), role: el.getAttribute('role') || '', text: text(el).slice(0, 100),
        aria: el.getAttribute('aria-label') || '', title: el.getAttribute('title') || '',
        value: el.getAttribute('data-value') || '',
        rect: (() => { const r = el.getBoundingClientRect(); return { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) }; })()
      }));
    return { pathname: location.pathname, bodyTail: String(document.body?.innerText || '').slice(-5000), nodes: nodes.slice(-160) };
  })()`;
}

class DolaBackgroundRunner {
  constructor({ outputRoot, getAccount, updateTask, updateAccount, waitSeconds = DEFAULT_WAIT_SECONDS }) {
    this.outputRoot = path.resolve(outputRoot);
    this.getAccount = getAccount;
    this.updateTask = updateTask;
    this.updateAccount = updateAccount;
    this.waitSeconds = waitSeconds;
    this.slots = new Map();
    this.queueTail = Promise.resolve();
  }

  async ensureSlot(account) {
    const existing = this.slots.get(account.id);
    if (existing && !existing.window.isDestroyed()) {
      if (!existing.page || existing.page.isDestroyed()) existing.page = existing.window.webContents;
      const currentUrl = existing.page.getURL();
      if (!currentUrl || !isDolaUrl(currentUrl)) {
        existing.page.loadURL(DOLA_HOME).catch(() => {});
      }
      await this.waitForDolaPage(existing, 30000);
      return existing;
    }
    const window = new BrowserWindow({
      show: false,
      skipTaskbar: true,
      width: 1280,
      height: 900,
      webPreferences: {
        partition: account.partition,
        contextIsolation: true,
        nodeIntegration: false,
        sandbox: false
      }
    });
    window.webContents.setAudioMuted(true);
    const slot = { accountId: account.id, window, page: window.webContents, childWindows: [], debugger: null, capture: null };
    this.slots.set(account.id, slot);
    window.webContents.on('did-create-window', (childWindow) => {
      try { childWindow.hide(); } catch (_) {}
      try { childWindow.webContents.setAudioMuted(true); } catch (_) {}
      slot.childWindows.push(childWindow);
      slot.page = childWindow.webContents;
      childWindow.on('closed', () => {
        slot.childWindows = slot.childWindows.filter(item => item !== childWindow);
        if (slot.page === childWindow.webContents) slot.page = window.webContents;
      });
    });
    window.on('closed', () => {
      if (this.slots.get(account.id) === slot) this.slots.delete(account.id);
    });
    // Do not await did-finish-load here: an authenticated SPA may keep
    // navigation open while service workers/network requests settle. The
    // control plane must stay responsive while the hidden page continues
    // loading in its account slot.
    window.loadURL(DOLA_HOME).catch(() => {});
    await this.waitForDolaPage(slot, 30000);
    return slot;
  }

  async waitForDolaPage(slot, timeoutMs = 30000) {
    const deadline = Date.now() + timeoutMs;
    while (Date.now() < deadline) {
      try {
        const url = slot.page?.getURL?.() || '';
        if (isDolaUrl(url) && !slot.page.isLoading()) return true;
      } catch (_) {}
      await sleep(500);
    }
    return false;
  }

  async execute(slot, script, timeoutMs = EXECUTE_TIMEOUT_MS) {
    if (!slot || slot.window.isDestroyed()) throw new Error('background Dola session is unavailable');
    let timer = null;
    const timeout = new Promise((_, reject) => {
      timer = setTimeout(() => reject(new Error('background Dola page script timed out')), timeoutMs);
    });
    try {
      return await Promise.race([
        slot.page.executeJavaScript(script, true),
        timeout
      ]);
    } finally {
      if (timer) clearTimeout(timer);
    }
  }

  async capturePage(slot, jobDir, name) {
    try {
      const image = await slot.page.capturePage();
      fs.writeFileSync(path.join(jobDir, name), image.toPNG());
    } catch (_) {}
  }

  async sessionStatus(account) {
    try {
      const slot = await this.ensureSlot(account);
      let status;
      try {
        status = await this.execute(slot, pageStatusScript());
      } catch (_) {
        // A hidden Chromium renderer can finish navigation while its first
        // executeJavaScript call is still attached to the old document. Reload
        // the same account partition once before declaring the session bad.
        try {
          try { slot.page.reload(); } catch (_) {}
          await this.waitForDolaPage(slot, 30000);
          status = await this.execute(slot, pageStatusScript());
        } catch (retryError) {
          return {
            loginStatus: 'unknown',
            pageLoaded: false,
            evidence: String(retryError.message || retryError).slice(0, 120),
            pagePath: ''
          };
        }
      }
      return {
        loginStatus: status.loggedIn ? 'logged_in' : status.loggedOut ? 'logged_out' : 'unknown',
        pageLoaded: true,
        evidence: status.loggedIn ? (status.hasComposer ? 'composer_present' : status.hasEditor ? 'editor_present' : 'logout_action_present') : status.loggedOut ? 'login_marker_present' : 'background_page_loaded',
        pagePath: `https://www.dola.com${status.pathname || '/chat/'}`,
        controls: Array.isArray(status.controls) ? status.controls : []
      };
    } catch (error) {
      return { loginStatus: 'unknown', pageLoaded: false, evidence: String(error.message || error).slice(0, 120), pagePath: '' };
    }
  }

  async click(slot, text, exact = false) {
    await this.clickRetry(slot, text, exact);
  }

  async clickButtonRetry(slot, text, exact = false, timeoutMs = 15000) {
    const deadline = Date.now() + timeoutMs;
    while (Date.now() < deadline) {
      try {
        const rect = await this.execute(slot, findVisibleButtonRectScript(text, exact));
        if (rect && Number.isFinite(rect.x) && Number.isFinite(rect.y)) {
          const dbg = slot.page.debugger;
          if (!dbg.isAttached()) dbg.attach('1.3');
          slot.debugger = dbg;
          await dbg.sendCommand('Input.dispatchMouseEvent', {
            type: 'mouseMoved', x: rect.x, y: rect.y
          });
          await dbg.sendCommand('Input.dispatchMouseEvent', {
            type: 'mousePressed', button: 'left', clickCount: 1, buttons: 1, x: rect.x, y: rect.y
          });
          await dbg.sendCommand('Input.dispatchMouseEvent', {
            type: 'mouseReleased', button: 'left', clickCount: 1, buttons: 0, x: rect.x, y: rect.y
          });
          await sleep(500);
          return rect;
        }
      } catch (_) {}
      await sleep(500);
    }
    throw new Error(`Dola button not found after waiting: ${text}`);
  }

  async clickButtonDomRetry(slot, text, exact = false, timeoutMs = 10000) {
    const deadline = Date.now() + timeoutMs;
    while (Date.now() < deadline) {
      try {
        if (await this.execute(slot, clickVisibleButtonScript(text, exact))) {
          await sleep(400);
          return true;
        }
      } catch (_) {}
      await sleep(500);
    }
    return false;
  }

  async pressButtonEnter(slot, text, exact = false, timeoutMs = 5000) {
    const deadline = Date.now() + timeoutMs;
    while (Date.now() < deadline) {
      try {
        if (await this.execute(slot, focusVisibleButtonScript(text, exact))) {
          const dbg = slot.page.debugger;
          if (!dbg.isAttached()) dbg.attach('1.3');
          slot.debugger = dbg;
          await dbg.sendCommand('Input.dispatchKeyEvent', {
            type: 'keyDown', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13, nativeVirtualKeyCode: 13
          });
          await dbg.sendCommand('Input.dispatchKeyEvent', {
            type: 'keyUp', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13, nativeVirtualKeyCode: 13
          });
          await sleep(500);
          return true;
        }
      } catch (_) {}
      await sleep(500);
    }
    return false;
  }

  async clickRetry(slot, text, exact = false, timeoutMs = 20000) {
    const deadline = Date.now() + timeoutMs;
    while (Date.now() < deadline) {
      try {
        const rect = await this.execute(slot, findVisibleTargetRectScript(text, exact));
        if (rect && Number.isFinite(rect.x) && Number.isFinite(rect.y)) {
          const dbg = slot.page.debugger;
          if (!dbg.isAttached()) dbg.attach('1.3');
          slot.debugger = dbg;
          await dbg.sendCommand('Input.dispatchMouseEvent', {
            type: 'mousePressed', button: 'left', clickCount: 1, x: rect.x, y: rect.y
          });
          await dbg.sendCommand('Input.dispatchMouseEvent', {
            type: 'mouseReleased', button: 'left', clickCount: 1, x: rect.x, y: rect.y
          });
          await sleep(500);
          return;
        }
      } catch (_) {}
      await sleep(700);
    }
    throw new Error(`Dola control not found after waiting: ${text}`);
  }

  async waitForAnyControl(slot, matchers, timeoutMs = 15000) {
    const values = Array.isArray(matchers) ? matchers : [matchers];
    const deadline = Date.now() + timeoutMs;
    while (Date.now() < deadline) {
      for (const matcher of values) {
        try {
          const current = await this.execute(slot, `(() => {
            const target = ${JSON.stringify(String(matcher))};
            const visible = (el) => !!el && !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
            const text = (el) => String(el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
            const button = Array.from(document.querySelectorAll('button,[role="button"]')).find((el) => visible(el) && text(el).includes(target));
            return button ? text(button) : '';
          })()`);
          if (current) return { matcher, current: String(current) };
        } catch (_) {}
      }
      await sleep(700);
    }
    return null;
  }

  async waitForButton(slot, matcher, exact = false, timeoutMs = 15000) {
    const deadline = Date.now() + timeoutMs;
    while (Date.now() < deadline) {
      try {
        const rect = await this.execute(slot, findVisibleButtonRectScript(matcher, exact));
        if (rect) return rect;
      } catch (_) {}
      await sleep(600);
    }
    return null;
  }

  async waitForComposer(slot, timeoutMs = 15000) {
    const deadline = Date.now() + timeoutMs;
    while (Date.now() < deadline) {
      try {
        if (await this.execute(slot, composerReadyScript())) return true;
      } catch (_) {}
      await sleep(600);
    }
    return false;
  }

  async clickMenuItemRetry(slot, value, contains = false, timeoutMs = 12000) {
    const deadline = Date.now() + timeoutMs;
    while (Date.now() < deadline) {
      try {
        const rect = await this.execute(slot, findVisibleMenuItemRectScript(value, contains));
        if (rect && Number.isFinite(rect.x) && Number.isFinite(rect.y)) {
          const dbg = slot.page.debugger;
          if (!dbg.isAttached()) dbg.attach('1.3');
          slot.debugger = dbg;
          await dbg.sendCommand('Input.dispatchMouseEvent', {
            type: 'mousePressed', button: 'left', clickCount: 1, x: rect.x, y: rect.y
          });
          await dbg.sendCommand('Input.dispatchMouseEvent', {
            type: 'mouseReleased', button: 'left', clickCount: 1, x: rect.x, y: rect.y
          });
          await sleep(500);
          return true;
        }
      } catch (_) {}
      await sleep(400);
    }
    return false;
  }

  async choose(slot, currentMatcher, value, exactCurrent = true) {
    const current = await this.execute(slot, `(() => {
      const visible = (el) => !!el && !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
      const text = (el) => String(el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
      const button = Array.from(document.querySelectorAll('button')).find((el) => visible(el) && text(el).includes(${JSON.stringify(currentMatcher)}));
      return button ? text(button) : '';
    })()`);
    if (String(current || '').includes(value)) return;
    await this.click(slot, currentMatcher, false);
    const selected = await this.execute(slot, clickMenuItemScript(value));
    if (!selected) throw new Error(`Dola option not found: ${value}`);
    await sleep(500);
  }

  async chooseAny(slot, currentMatchers, value, containsOption = false) {
    const matchers = Array.isArray(currentMatchers) ? currentMatchers : [currentMatchers];
    const control = await this.waitForAnyControl(slot, matchers);
    if (control && control.current.includes(String(value))) return;
    if (control) {
      const opened = await this.clickButtonDomRetry(slot, control.matcher, false);
      if (!opened) await this.clickButtonRetry(slot, control.matcher, false);
      if (await this.clickMenuItemRetry(slot, value, containsOption)) return;
      await this.pressButtonEnter(slot, control.matcher, false);
      if (await this.clickMenuItemRetry(slot, value, containsOption)) return;
    }
    throw new Error(`Dola option control not found for ${String(value)}`);
  }

  async chooseDuration(slot, value) {
    const findDuration = () => this.execute(slot, `(() => {
      const visible = (el) => !!el && !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
      const text = (el) => String(el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
      const button = Array.from(document.querySelectorAll('button,[role="button"]')).find((el) => visible(el) && /^\\d+\\s*(s|秒)$/.test(text(el)));
      return button ? text(button) : '';
    })()`);
    let current = '';
    const deadline = Date.now() + 15000;
    while (Date.now() < deadline && !current) {
      try { current = String(await findDuration() || ''); } catch (_) {}
      if (!current) await sleep(700);
    }
    if (String(current || '').replace(/\\s+/g, '') === String(value).replace(/\\s+/g, '')) return;
    const opened = await this.execute(slot, `(() => {
      const visible = (el) => !!el && !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
      const text = (el) => String(el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
      const button = Array.from(document.querySelectorAll('button,[role="button"]')).find((el) => visible(el) && /^\\d+\\s*(s|秒)$/.test(text(el)));
      if (!button || button.disabled) return false;
      return true;
    })()`);
    if (!opened) throw new Error('Dola duration control not found');
    await this.clickButtonRetry(slot, current, true);
    await sleep(300);
    let selected = await this.execute(slot, chooseDurationScript(value));
    if (!selected) {
      const normalized = String(value).replace(/\\s+/g, '').replace(/s$/i, '秒');
      const aliases = [normalized, normalized.replace(/秒$/, ''), String(value).replace(/s$/i, '秒')];
      for (const alias of aliases) {
        if (await this.clickMenuItemRetry(slot, alias, true)) return;
      }
    }
    if (!selected) throw new Error(`Dola duration option not found: ${value}`);
    await sleep(500);
  }

  async upload(slot, filePath) {
    const absolute = path.resolve(filePath);
    if (!fs.existsSync(absolute)) throw new Error(`image file does not exist: ${absolute}`);
    const dbg = slot.debugger || slot.page.debugger;
    if (!dbg) throw new Error('Dola browser debugger is not ready for image upload');
    if (!dbg.isAttached()) dbg.attach('1.3');
    await dbg.sendCommand('DOM.enable');
    const documentNode = await dbg.sendCommand('DOM.getDocument', { depth: -1 });
    const query = await dbg.sendCommand('DOM.querySelector', {
      nodeId: documentNode.root.nodeId,
      selector: 'input[type="file"]'
    });
    if (!query.nodeId) throw new Error('Dola image input was not found');
    await dbg.sendCommand('DOM.setFileInputFiles', { nodeId: query.nodeId, files: [absolute] });
    // Electron's DOM.setFileInputFiles already emits the file-input change
    // event. Dispatching a second change duplicates the same reference image
    // in Dola's attachment list (observed as image_attachment_num=2).
    await sleep(1200);
  }

  async prepare(slot, task) {
    let ready = false;
    try { ready = await this.execute(slot, composerReadyScript()); } catch (_) {}
    if (!ready) {
      let state = null;
      try { state = await this.execute(slot, pageStatusScript()); } catch (_) {}
    const pathname = String(state?.pathname || '');
      // Dola's home page exposes a “视频生成” quick action. It then opens
      // /chat/create-image, where the actual Seedance composer is the exact
      // “视频” tab. Wait for each UI state instead of assuming a fixed SPA
      // transition delay.
      ready = await this.waitForComposer(slot, 5000);
      let videoTab = await this.waitForButton(slot, '视频', true, 2500);
      if (!ready && !videoTab && !pathname.includes('/create-image')) {
        // The home quick-action may leave an already-selected chat mounted
        // instead of switching the SPA route. Navigate within the same
        // authenticated account partition to the observed creator route,
        // then let the page expose its own controls.
        try {
          await Promise.race([
            slot.page.loadURL(DOLA_CREATE_IMAGE).catch(() => {}),
            sleep(3000)
          ]);
        } catch (_) {}
        ready = await this.waitForComposer(slot, 20000);
        if (!ready) videoTab = await this.waitForButton(slot, '视频', true, 10000);
      }
      if (!ready && !videoTab) {
        let videoQuick = await this.waitForButton(slot, '视频生成', false, 3500);
        if (!videoQuick) {
          const quick = await this.waitForButton(slot, '快速', true, 2500);
          if (quick) {
            await this.clickButtonRetry(slot, '快速', true);
            videoQuick = await this.waitForButton(slot, '视频生成', false, 7000);
          }
        }
        if (!videoQuick && !pathname.includes('/create-image')) {
          await this.clickRetry(slot, 'AI 创作', true);
          videoQuick = await this.waitForButton(slot, '视频生成', false, 15000);
        }
        if (videoQuick) {
          // Prefer the page's own React click path for the home quick action;
          // fall back to trusted CDP coordinates only if the DOM event does
          // not transition the SPA.
          const domClicked = await this.clickButtonDomRetry(slot, '视频生成', false, 5000);
          if (!domClicked) await this.clickButtonRetry(slot, '视频生成', false);
          ready = await this.waitForComposer(slot, 20000);
          if (!ready) videoTab = await this.waitForButton(slot, '视频', true, 10000);
        }
      }
      if (!ready && !videoTab) {
        if (task.artifactDir) await this.capturePage(slot, task.artifactDir, 'after-ai-create-entry.png');
        if (task.artifactDir) {
          try { writeJsonAtomic(path.join(task.artifactDir, 'prepare-page-status-failure.json'), await this.execute(slot, pageStatusScript())); } catch (_) {}
          try { writeJsonAtomic(path.join(task.artifactDir, 'prepare-ui-diagnostic.json'), await this.execute(slot, visibleUiDiagnosticScript())); } catch (_) {}
        }
        throw new Error('Dola video entry did not expose 视频 or 视频生成 after waiting');
      }
      // Dola currently opens AI 创作 on the image tab. The actual video
      // composer is the exact “视频” tab inside /chat/create-image.
      if (!ready) {
        const domClicked = await this.clickButtonDomRetry(slot, '视频', true, 5000);
        if (domClicked) ready = await this.waitForComposer(slot, 4000);
        if (!ready) {
          // A few Dola builds report the DOM click but update the tab only on
          // a trusted pointer sequence. Retry the same visible tab by CDP.
          await this.clickButtonRetry(slot, '视频', true);
          ready = await this.waitForComposer(slot, 20000);
        }
      }
      if (!ready) {
        if (task.artifactDir) {
          await this.capturePage(slot, task.artifactDir, 'video-tab-selection-failure.png');
          try { writeJsonAtomic(path.join(task.artifactDir, 'video-tab-selection-diagnostic.json'), await this.execute(slot, visibleUiDiagnosticScript())); } catch (_) {}
        }
        throw new Error('Dola video composer did not become ready after selecting 视频');
      }
    }
    if (task.artifactDir) await this.capturePage(slot, task.artifactDir, 'after-video-entry.png');
    try {
      const pageState = await this.execute(slot, pageStatusScript());
      if (task.artifactDir) {
        writeJsonAtomic(path.join(task.artifactDir, 'prepare-page-status.json'), {
          pathname: pageState.pathname || '',
          logged_in: pageState.loggedIn === true,
          has_composer: pageState.hasComposer === true,
          has_editor: pageState.hasEditor === true,
          controls: Array.isArray(pageState.controls) ? pageState.controls : []
        });
      }
    } catch (_) {}
    await this.chooseAny(slot, ['模型', 'Seedance', '2.5'], '2.5', true);
    await this.chooseDuration(slot, `${task.duration}s`);
    try {
      await this.chooseAny(slot, ['比例', task.ratio], task.ratio, true);
    } catch (error) {
      if (task.artifactDir) {
        await this.capturePage(slot, task.artifactDir, 'ratio-selection-failure.png');
        try { writeJsonAtomic(path.join(task.artifactDir, 'ratio-selection-diagnostic.json'), await this.execute(slot, visibleUiDiagnosticScript())); } catch (_) {}
      }
      throw error;
    }
    if (task.imagePath) await this.upload(slot, task.imagePath);
    const filled = await this.execute(slot, fillPromptScript(task.prompt));
    if (!filled?.ok) throw new Error(filled?.reason || 'Dola prompt editor was not found');
    await sleep(800);
    let promptState = [];
    try { promptState = await this.execute(slot, promptEditorStateScript()); } catch (_) {}
    const hasPromptText = Array.isArray(promptState)
      && promptState.some((entry) => String(entry.value || entry.text || '').trim().length > 0);
    if (!hasPromptText) {
      const dbg = slot.debugger || slot.page.debugger;
      if (!dbg.isAttached()) dbg.attach('1.3');
      slot.debugger = dbg;
      await this.execute(slot, focusPromptEditorScript());
      await dbg.sendCommand('Input.insertText', { text: String(task.prompt) });
      await sleep(800);
      try { promptState = await this.execute(slot, promptEditorStateScript()); } catch (_) {}
    }
    const promptConfirmed = Array.isArray(promptState)
      && promptState.some((entry) => String(entry.value || entry.text || '').trim().length > 0);
    if (!promptConfirmed) {
      if (task.artifactDir) writeJsonAtomic(path.join(task.artifactDir, 'prompt-editor-state-final.json'), promptState);
      throw new Error('Dola prompt text was not confirmed in the visible editor');
    }
  }

  async armCapture(slot, jobDir) {
    const dbg = slot.page.debugger;
    if (!dbg.isAttached()) dbg.attach('1.3');
    slot.debugger = dbg;
    await dbg.sendCommand('Network.enable');
    await dbg.sendCommand('Runtime.enable');
    const state = {
      jobDir,
      responses: new Map(),
      identity: identitySummary(),
      capturePromises: [],
      counter: 0,
      error: null
    };
    const handleMessage = (_event, method, params) => {
      if (method === 'Network.responseReceived') {
        const response = params?.response;
        if (!response || !isInterestingResponse(response.url)) return;
        state.responses.set(params.requestId, {
          requestId: params.requestId,
          url: response.url,
          status: response.status,
          mimeType: response.mimeType
        });
      }
      if (method === 'Network.loadingFinished' && state.responses.has(params.requestId)) {
        const pending = this.captureBody(slot, state, params.requestId);
        state.capturePromises.push(pending);
      }
    };
    dbg.on('message', handleMessage);
    state.detach = async () => {
      dbg.removeListener('message', handleMessage);
      await Promise.allSettled(state.capturePromises);
      try { await dbg.sendCommand('Network.disable'); } catch (_) {}
      try { await dbg.sendCommand('Runtime.disable'); } catch (_) {}
      try { if (dbg.isAttached()) dbg.detach(); } catch (_) {}
    };
    slot.capture = state;
    writeJsonAtomic(path.join(jobDir, 'capture-status.json'), {
      capture_armed_before_generation: true,
      protocol: 'electron-webcontents-debugger-network',
      security: { cookies_emitted: false, authorization_emitted: false, raw_shared_ledger: false }
    });
    return state;
  }

  async captureBody(slot, state, requestId) {
    const response = state.responses.get(requestId);
    if (!response) return;
    try {
      const payload = await slot.debugger.sendCommand('Network.getResponseBody', { requestId });
      const body = String(payload?.body || '');
      const responsePath = redactedUrl(response.url);
      const identity = extractIdentity(body, responsePath);
      mergeIdentity(state.identity, identity);
      const index = String(state.counter++).padStart(4, '0');
      writeJsonAtomic(path.join(state.jobDir, 'raw-responses', `${index}.json`), {
        request: { url: responsePath, status: response.status, mime_type: response.mimeType },
        body
      });
      writeJsonAtomic(path.join(state.jobDir, 'identity-summary.json'), state.identity);
      if (/未认证人脸暂不支持|出于肖像保护考虑|country restricted|quota|rate limit/i.test(body)) {
        state.error = 'Dola provider rejected the generation request';
      }
    } catch (_) {
      // Some streaming responses are not body-readable; the page/other responses remain usable evidence.
    }
  }

  async waitForGeneration(slot, state) {
    const deadline = Date.now() + this.waitSeconds * 1000;
    while (Date.now() < deadline) {
      await Promise.allSettled(state.capturePromises);
      if (state.identity.identity_pass) return { ok: true, identity: state.identity };
      const status = await this.execute(slot, pageStatusScript()).catch(() => ({ loggedOut: false }));
      if (status.error) return { ok: false, error: status.error, identity: state.identity };
      if (state.error) return { ok: false, error: state.error, identity: state.identity };
      await sleep(1500);
    }
    await Promise.allSettled(state.capturePromises);
    return state.identity.identity_pass
      ? { ok: true, identity: state.identity }
      : { ok: false, error: 'background generation timed out before media identity was captured', identity: state.identity };
  }

  run(task, account) {
    // A single worker is intentional for the first production-safe slice:
    // account/task bindings stay sticky and two submissions cannot race
    // through the same provider UI. Different partitions remain isolated.
    const next = this.queueTail.then(() => this._run(task, account));
    this.queueTail = next.catch(() => {});
    return next;
  }

  async _run(task, account) {
    const jobDir = path.join(this.outputRoot, 'jobs', task.id);
    task.artifactDir = jobDir;
    fs.mkdirSync(jobDir, { recursive: true });
    writeJsonAtomic(path.join(jobDir, 'task.json'), {
      task_id: task.id,
      account_id: account.id,
      session_slot: account.partition,
      mode: task.mode,
      model: task.model,
      duration: task.duration,
      ratio: task.ratio,
      prompt_present: Boolean(task.prompt),
      image_present: Boolean(task.imagePath)
    });
    let capture = null;
    try {
      await this.updateAccount(account.id, { status: 'BUSY' });
      const slot = await this.ensureSlot(account);
      const session = await this.sessionStatus(account);
      if (session.loginStatus === 'logged_out') {
        throw new Error('Dola session is logged out; complete one manual login in this account slot first');
      }
      await this.prepare(slot, task);
      capture = await this.armCapture(slot, jobDir);
      await this.updateTask(task.id, {
        state: 'capture_armed',
        captureArmedBeforeGeneration: true,
        artifactDir: jobDir,
        updatedAt: Date.now()
      });
      try {
        const promptState = await this.execute(slot, promptEditorStateScript());
        writeJsonAtomic(path.join(jobDir, 'prompt-editor-state.json'), promptState);
      } catch (_) {}
      await this.capturePage(slot, jobDir, 'before-submit.png');
      const submit = await this.execute(slot, submitScript());
      if (!submit?.clicked) {
        writeJsonAtomic(path.join(jobDir, 'submit-diagnostic.json'), submit || { reason: 'empty-submit-result' });
        throw new Error(submit?.reason || 'Dola submit control was not clicked');
      }
      await this.updateTask(task.id, {
        state: 'generation_running',
        generationSubmitted: true,
        updatedAt: Date.now()
      });
      const result = await this.waitForGeneration(slot, capture);
      writeJsonAtomic(path.join(jobDir, 'generation-result.json'), result);
      if (!result.ok) throw new Error(result.error);
      await this.updateTask(task.id, {
        state: 'success',
        generationIdentity: result.identity,
        artifactDir: jobDir,
        updatedAt: Date.now(),
        error: null
      });
      await this.updateAccount(account.id, { status: 'READY', lastError: '' });
      return { ok: true, taskId: task.id, artifactDir: jobDir, identity: result.identity };
    } catch (error) {
      const message = String(error.message || error).slice(0, 500);
      writeJsonAtomic(path.join(jobDir, 'generation-result.json'), { ok: false, error: message });
      await this.updateTask(task.id, { state: 'failed', error: message, artifactDir: jobDir, updatedAt: Date.now() });
      await this.updateAccount(account.id, {
        status: /logged out|login|登录/i.test(message)
          ? 'NEEDS_LOGIN'
          : /出于肖像保护|未认证人脸暂不支持/i.test(message) ? 'READY' : 'ERROR',
        lastError: message
      });
      return { ok: false, taskId: task.id, artifactDir: jobDir, error: message };
    } finally {
      if (capture?.detach) await capture.detach();
      const slot = this.slots.get(account.id);
      if (slot) slot.capture = null;
    }
  }

  async close() {
    for (const slot of this.slots.values()) {
      try { if (slot.capture?.detach) await slot.capture.detach(); } catch (_) {}
      for (const childWindow of slot.childWindows || []) {
        try { if (!childWindow.isDestroyed()) childWindow.destroy(); } catch (_) {}
      }
      try { if (!slot.window.isDestroyed()) slot.window.destroy(); } catch (_) {}
    }
    this.slots.clear();
  }
}

module.exports = {
  DOLA_HOME,
  DolaBackgroundRunner,
  extractIdentity,
  isInterestingResponse,
  redactedUrl
};
