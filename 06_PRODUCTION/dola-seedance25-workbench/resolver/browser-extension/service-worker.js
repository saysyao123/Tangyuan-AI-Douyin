const DEBUGGER_VERSION = "1.3";
const BRIDGE_URL = "http://127.0.0.1:8765/capture";
const TARGET_PATH = "/im/chain/single";

const attachedTabs = new Set();
const fetchPatterns = [
  { urlPattern: "*://*.dola.com/im/chain/single*", requestStage: "Response" }
];

function isDolaUrl(url) {
  try {
    const parsed = new URL(url);
    return /^https?:$/i.test(parsed.protocol) &&
      /(^|\.)dola\.com$/i.test(parsed.hostname);
  } catch {
    return false;
  }
}

function isTargetRequest(url) {
  try {
    const parsed = new URL(url);
    return parsed.protocol === "https:" &&
      /(^|\.)dola\.com$/i.test(parsed.hostname) &&
      parsed.pathname === TARGET_PATH;
  } catch {
    return false;
  }
}

async function safeGetTab(tabId) {
  try { return await chrome.tabs.get(tabId); } catch { return null; }
}

function sendCommand(tabId, method, params = {}) {
  return new Promise((resolve, reject) => {
    chrome.debugger.sendCommand({ tabId }, method, params, result => {
      const err = chrome.runtime.lastError;
      if (err) reject(new Error(err.message));
      else resolve(result);
    });
  });
}

function attachDebugger(tabId) {
  return new Promise((resolve, reject) => {
    chrome.debugger.attach({ tabId }, DEBUGGER_VERSION, () => {
      const err = chrome.runtime.lastError;
      if (err) reject(new Error(err.message));
      else resolve();
    });
  });
}

async function ensureAttached(tabId) {
  if (attachedTabs.has(tabId)) return;
  const tab = await safeGetTab(tabId);
  if (!tab || !isDolaUrl(tab.url)) return;
  try { await attachDebugger(tabId); } catch (_) { /* already attached is okay */ }
  try {
    await sendCommand(tabId, "Fetch.enable", { patterns: fetchPatterns });
    attachedTabs.add(tabId);
    await chrome.action.setBadgeText({ tabId, text: "ON" });
    await chrome.action.setBadgeBackgroundColor({ tabId, color: "#137333" });
  } catch (e) {
    console.warn("[DolaCapture] attach failed:", e.message || e);
  }
}

async function attachExistingTabs() {
  const tabs = await chrome.tabs.query({});
  for (const tab of tabs) {
    if (tab.id && isDolaUrl(tab.url)) await ensureAttached(tab.id);
  }
}

async function getResponseBody(tabId, requestId) {
  const result = await sendCommand(tabId, "Fetch.getResponseBody", { requestId });
  if (!result) return "";
  if (!result.base64Encoded) return result.body || "";
  try {
    const binary = atob(result.body || "");
    const bytes = Uint8Array.from(binary, char => char.charCodeAt(0));
    return new TextDecoder("utf-8").decode(bytes);
  } catch {
    return "";
  }
}

function looksRelevant(body) {
  if (!body) return false;
  return [
    "fallback_api", "video_model", "main_url", "man_url", "download_url",
    "video_list", "key_seed", '"vid"', '"video_id"'
  ].some(key => body.includes(key));
}

async function postToLocalBridge(payload) {
  try {
    const response = await fetch(BRIDGE_URL, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (!response.ok) throw new Error(`bridge HTTP ${response.status}`);
    return true;
  } catch (e) {
    console.warn("[DolaCapture] local bridge unavailable:", e.message || e);
    return false;
  }
}

async function continuePausedResponse(tabId, requestId) {
  try {
    await sendCommand(tabId, "Fetch.continueResponse", { requestId });
  } catch (_) {
    try { await sendCommand(tabId, "Fetch.continueRequest", { requestId }); } catch (_) {}
  }
}

chrome.debugger.onEvent.addListener(async (source, method, params) => {
  if (method !== "Fetch.requestPaused" || !source.tabId || !params) return;
  const tabId = source.tabId;
  const requestId = params.requestId;
  const requestUrl = params.request?.url || "";
  if (!isTargetRequest(requestUrl)) {
    await continuePausedResponse(tabId, requestId);
    return;
  }
  try {
    const body = await getResponseBody(tabId, requestId);
    if (looksRelevant(body)) {
      const tab = await safeGetTab(tabId);
      await postToLocalBridge({
        captured_at: new Date().toISOString(),
        page_url: tab?.url || "",
        request_url: requestUrl,
        response_status: params.responseStatusCode || null,
        raw_body: body
      });
      await chrome.action.setBadgeText({ tabId, text: "CAP" });
      setTimeout(() => chrome.action.setBadgeText({ tabId, text: "ON" }).catch(() => {}), 1500);
    }
  } catch (e) {
    console.warn("[DolaCapture] capture failed:", e.message || e);
  } finally {
    await continuePausedResponse(tabId, requestId);
  }
});

chrome.debugger.onDetach.addListener(source => {
  if (source.tabId) {
    attachedTabs.delete(source.tabId);
    chrome.action.setBadgeText({ tabId: source.tabId, text: "" }).catch(() => {});
  }
});
chrome.tabs.onActivated.addListener(async ({ tabId }) => ensureAttached(tabId));
chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
  if (isDolaUrl(changeInfo.url || tab.url || "")) await ensureAttached(tabId);
});
chrome.tabs.onRemoved.addListener(tabId => attachedTabs.delete(tabId));
chrome.runtime.onInstalled.addListener(attachExistingTabs);
chrome.runtime.onStartup.addListener(attachExistingTabs);
chrome.action.onClicked.addListener(async tab => {
  if (tab?.id) await ensureAttached(tab.id);
});

attachExistingTabs();
