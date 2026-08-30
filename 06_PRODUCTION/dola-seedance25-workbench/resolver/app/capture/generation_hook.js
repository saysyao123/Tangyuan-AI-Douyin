(() => {
  const SINGLE_LIMIT = 2 * 1024 * 1024;
  const TOTAL_LIMIT = 64 * 1024 * 1024;
  const now = () => new Date().toISOString();
  const safeUrl = (value) => {
    try {
      const parsed = new URL(String(value || ""), location.href);
      return { host: parsed.hostname, path: parsed.pathname };
    } catch (_) {
      return { host: "", path: "" };
    }
  };
  const state = window.__DOLA_GEN_CAPTURE__ || {
    version: "1.0",
    armed_at: now(),
    fetch: [],
    xhr: [],
    sse_chunks: [],
    websocket: [],
    hits: [],
    total_body_bytes: 0,
    body_buffer_exhausted: false,
  };
  state.armed_at = now();
  state.fetch = [];
  state.xhr = [];
  state.sse_chunks = [];
  state.websocket = [];
  state.hits = [];
  state.total_body_bytes = 0;
  state.body_buffer_exhausted = false;

  const scores = {
    fallback_api: 15,
    original_media_info: 15,
    video_list: 15,
    key_seed: 12,
    main_url: 10,
    play_infos: 10,
    node_id: 8,
    video_id: 8,
    vid: 8,
    media_info: 6,
    task_id: 5,
    generation_id: 5,
    video_model: 1,
  };
  const scan = (value, path, fields) => {
    if (Array.isArray(value)) {
      value.slice(0, 500).forEach((child, index) => scan(child, path.concat(index), fields));
      return;
    }
    if (!value || typeof value !== "object") return;
    Object.keys(value).forEach((key) => {
      const normalized = key.toLowerCase();
      if (Object.prototype.hasOwnProperty.call(scores, normalized)) fields.add(normalized);
      scan(value[key], path.concat(key), fields);
    });
  };
  const reserve = (text) => {
    if (typeof text !== "string") return { text: "", truncated: false };
    if (text.length > SINGLE_LIMIT || state.total_body_bytes + text.length > TOTAL_LIMIT) {
      state.body_buffer_exhausted = true;
      return { text: text.slice(0, SINGLE_LIMIT), truncated: true };
    }
    state.total_body_bytes += text.length;
    return { text, truncated: false };
  };
  const meta = (kind, info) => {
    const locationInfo = safeUrl(info.url || info.responseURL || "");
    return {
      captured_at: now(),
      kind,
      host: locationInfo.host,
      path: locationInfo.path,
      method: info.method || "",
      status: Number(info.status || 0),
      mime_type: info.mime_type || info.content_type || "",
    };
  };
  const record = (kind, info, text, extra) => {
    const entry = Object.assign(meta(kind, info), extra || {});
    if (typeof text === "string") {
      const reserved = reserve(text);
      entry.body = reserved.text;
      entry.body_truncated = reserved.truncated;
      const fields = new Set();
      try { scan(JSON.parse(text), [], fields); } catch (_) { scan(text, [], fields); }
      entry.score = [...fields].reduce((sum, field) => sum + (scores[field] || 0), 0);
      entry.matched_fields = [...fields];
      if (entry.score >= 8) {
        state.hits.push({ captured_at: entry.captured_at, kind, host: entry.host, path: entry.path, score: entry.score, matched_fields: entry.matched_fields });
      }
    }
    if (Array.isArray(state[kind])) state[kind].push(entry);
    else state[kind] = [entry];
  };
  const recordSseChunk = (info, text) => {
    const reserved = reserve(text);
    const entry = Object.assign(meta("sse", info), { chunk: reserved.text, body_truncated: reserved.truncated });
    state.sse_chunks.push(entry);
    const fields = new Set();
    text.split(/\r?\n/).forEach((line) => {
      if (!line.startsWith("data:")) return;
      const data = line.slice(5).trim();
      if (!data || data === "[DONE]") return;
      try { scan(JSON.parse(data), ["data"], fields); } catch (_) { scan(data, ["data"], fields); }
    });
    entry.score = [...fields].reduce((sum, field) => sum + (scores[field] || 0), 0);
    entry.matched_fields = [...fields];
    if (entry.score >= 8) state.hits.push({ captured_at: entry.captured_at, kind: "sse", host: entry.host, path: entry.path, score: entry.score, matched_fields: entry.matched_fields });
  };

  if (!state.__fetch_installed) {
    const originalFetch = window.fetch;
    window.fetch = function (...args) {
      const input = args[0];
      const init = args[1] || {};
      const requestUrl = typeof input === "string" ? input : (input && input.url) || "";
      const method = init.method || (input && input.method) || "GET";
      return originalFetch.apply(this, args).then((response) => {
        const info = { url: response.url || requestUrl, method, status: response.status, content_type: response.headers.get("content-type") || "" };
        const type = info.content_type.toLowerCase();
        if (type.includes("text/event-stream")) {
          record("fetch", info, "", { streaming: true });
          const clone = response.clone();
          Promise.resolve().then(async () => {
            try {
              const reader = clone.body && clone.body.getReader();
              if (!reader) return;
              const decoder = new TextDecoder();
              while (true) {
                const part = await reader.read();
                if (part.done) break;
                if (part.value) recordSseChunk(info, decoder.decode(part.value, { stream: true }));
              }
            } catch (_) {}
          });
        } else {
          const clone = response.clone();
          Promise.resolve().then(async () => {
            try { record("fetch", info, await clone.text()); } catch (_) { record("fetch", info, "", { body_unavailable: true }); }
          });
        }
        return response;
      }, (error) => {
        record("fetch", { url: requestUrl, method, status: 0 }, "", { error: String(error).slice(0, 200) });
        throw error;
      });
    };
    state.__fetch_installed = true;
  }

  if (!state.__xhr_installed) {
    const open = XMLHttpRequest.prototype.open;
    const send = XMLHttpRequest.prototype.send;
    XMLHttpRequest.prototype.open = function (method, url, ...rest) {
      this.__dolaGenMethod = method;
      this.__dolaGenUrl = url;
      return open.call(this, method, url, ...rest);
    };
    XMLHttpRequest.prototype.send = function (...args) {
      if (!this.__dolaGenCaptureBound) {
        this.__dolaGenCaptureBound = true;
        this.addEventListener("loadend", () => {
          const type = this.getResponseHeader("content-type") || "";
          const info = { url: this.responseURL || this.__dolaGenUrl || "", method: this.__dolaGenMethod || "GET", status: this.status, content_type: type };
          if (!this.responseType || this.responseType === "text") {
            let text = "";
            try { text = this.responseText || ""; } catch (_) {}
            record("xhr", info, text);
          } else if (this.responseType === "json") {
            try { record("xhr", info, JSON.stringify(this.response)); } catch (_) { record("xhr", info, "", { body_unavailable: true }); }
          } else {
            record("xhr", info, "", { response_type: this.responseType, body_unavailable: true });
          }
        });
      }
      return send.apply(this, args);
    };
    state.__xhr_installed = true;
  }

  if (!state.__websocket_installed && window.WebSocket) {
    const OriginalWebSocket = window.WebSocket;
    const WrappedWebSocket = function (...args) {
      const socket = new OriginalWebSocket(...args);
      const info = { url: args[0] || "", method: "WEBSOCKET", status: 101, content_type: "" };
      socket.addEventListener("message", (event) => {
        if (typeof event.data === "string") record("websocket", info, event.data);
        else if (event.data instanceof ArrayBuffer) record("websocket", info, "", {data_type: "ArrayBuffer", data_size: event.data.byteLength});
        else if (event.data instanceof Blob) record("websocket", info, "", {data_type: "Blob", data_size: event.data.size});
        else record("websocket", info, "", {data_type: typeof event.data});
      });
      return socket;
    };
    WrappedWebSocket.prototype = OriginalWebSocket.prototype;
    try { Object.setPrototypeOf(WrappedWebSocket, OriginalWebSocket); } catch (_) {}
    window.WebSocket = WrappedWebSocket;
    state.__websocket_installed = true;
  }
  state.__installed = true;
  window.__DOLA_GEN_CAPTURE__ = state;
  return JSON.stringify({ armed: true, armed_at: state.armed_at, installed: true });
})()
