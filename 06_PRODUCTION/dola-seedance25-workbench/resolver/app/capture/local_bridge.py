from __future__ import annotations

import argparse
import hashlib
import json
import os
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from app.download.authenticated import download_stream
from app.logger import redact_url
from app.qa.ffprobe import probe_media
from app.qa.report import make_report
from app.resolver.resolver import resolve_metadata


MAX_BODY = 32 * 1024 * 1024
CAPTURE_PATH = "/im/chain/single"
DISCOVERY_CAPTURE_PATH = "/capture-discovered"


def _is_dola_chain_single(value: str) -> bool:
    try:
        parts = urlsplit(value)
    except ValueError:
        return False
    host = (parts.hostname or "").lower().rstrip(".")
    return (
        parts.scheme == "https"
        and (host == "dola.com" or host.endswith(".dola.com"))
        and parts.path == CAPTURE_PATH
    )


def _write_text_atomic(path: Path, text: str) -> None:
    partial = path.with_name(path.name + ".part")
    try:
        partial.write_text(text, encoding="utf-8")
        os.replace(partial, path)
    except Exception:
        if partial.exists():
            partial.unlink()
        raise


def _write_json_atomic(path: Path, payload: Any) -> None:
    _write_text_atomic(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _yes_no(value: bool) -> str:
    return "YES" if value else "NO"


class CaptureStore:
    def __init__(
        self,
        out_dir: Path,
        *,
        auto_download: bool = False,
        fetch_fallback: bool = True,
    ) -> None:
        self.out_dir = out_dir.resolve()
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.auto_download = auto_download
        self.fetch_fallback = fetch_fallback
        self._lock = threading.Lock()

    def _acceptance(self, result: Any, *, capture_pass: str, download_state: str = "NOT_AVAILABLE") -> dict[str, str]:
        selected = result.selected
        if selected and selected.width and selected.height:
            resolution = f"{selected.width}x{selected.height}"
        elif result.candidates:
            best = max(result.candidates, key=lambda item: item.pixel_area)
            resolution = f"{best.width}x{best.height}" if best.width and best.height else "UNKNOWN"
        else:
            resolution = "UNKNOWN"
        return {
            "CAPTURE_CHAIN_SINGLE": capture_pass,
            "FOUND_FALLBACK_API": _yes_no(bool(result.source_metadata.get("fallback_api_count"))),
            "FOUND_VIDEO_LIST": _yes_no(bool(result.source_metadata.get("video_list_count"))),
            "FOUND_QAAB": _yes_no(bool(result.source_metadata.get("key_seed_present"))),
            "FOUND_CLEAN_CANDIDATE": _yes_no(bool(result.clean_candidates)),
            "HIGHEST_NATIVE_RESOLUTION": resolution,
            "DOWNLOAD_CLEAN_SOURCE": download_state,
            "VISIBLE_DOLA_WATERMARK": "UNVERIFIED",
        }

    def _save_parsed(
        self,
        *,
        raw_body: str,
        parsed: Any,
        captured_at: Any,
        page_url: str,
        request_url: str,
        response_status: Any,
        prefix: str,
        include_internal: bool = False,
    ) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        digest = hashlib.sha256(raw_body.encode("utf-8")).hexdigest()[:12]
        stem = f"{prefix}_{now.strftime('%Y%m%d_%H%M%S_%f')}_{digest}"
        raw_path = self.out_dir / f"{stem}.json"
        meta_path = self.out_dir / f"{stem}.capture.json"
        resolve_path = self.out_dir / f"{stem}.resolve.report.json"

        # Keep the original response body available to the P0 resolver. It is
        # local capture data, not a log; safe metadata and reports are redacted.
        with self._lock:
            _write_text_atomic(raw_path, raw_body)
            safe_meta = {
                "captured_at": captured_at,
                "page_url": redact_url(page_url),
                "request_url": redact_url(request_url) if request_url.startswith("http") else request_url,
                "response_status": response_status,
                "sha256": hashlib.sha256(raw_body.encode("utf-8")).hexdigest(),
                "raw_path": str(raw_path),
            }
            _write_json_atomic(meta_path, safe_meta)

        result = resolve_metadata(parsed, fetch_fallback=self.fetch_fallback)
        report = make_report(result)
        report["acceptance"] = self._acceptance(result, capture_pass="PASS")
        report["capture"] = {
            "request_url": redact_url(request_url),
            "raw_path": str(raw_path),
            "capture_metadata_path": str(meta_path),
        }
        download_state = "NOT_AVAILABLE"

        if self.auto_download and result.status == "success" and result.selected is not None:
            download_dir = self.out_dir / "downloads"
            output_path = download_dir / f"{stem}.mp4"
            try:
                download_stream(result.selected.url, output_path)
                ffprobe = probe_media(output_path)
                report = make_report(result, file_path=output_path, ffprobe=ffprobe)
                download_state = "PASS"
                report["download"] = {"path": str(output_path), "method": "authorized_stream"}
            except Exception as exc:
                download_state = "FAIL"
                report["download"] = {
                    "status": "failed",
                    "error": str(exc),
                    "url": redact_url(result.selected.url),
                    "bypass_attempted": False,
                }

        report["acceptance"] = self._acceptance(result, capture_pass="PASS", download_state=download_state)
        report["capture"] = {
            "request_url": redact_url(request_url) if request_url.startswith("http") else request_url,
            "raw_path": str(raw_path),
            "capture_metadata_path": str(meta_path),
        }
        with self._lock:
            _write_json_atomic(resolve_path, report)

        payload: dict[str, Any] = {
            "ok": True,
            "raw_path": str(raw_path),
            "meta_path": str(meta_path),
            "resolve_report_path": str(resolve_path),
            "request_url": redact_url(request_url) if request_url.startswith("http") else request_url,
            "status": result.status,
            "acceptance": report["acceptance"],
        }
        if include_internal:
            payload["_resolve_result"] = result
        return payload

    def save(self, envelope: dict[str, Any], *, include_internal: bool = False) -> dict[str, Any]:
        if not isinstance(envelope, dict):
            raise ValueError("capture envelope must be a JSON object")
        raw_body = envelope.get("raw_body", "")
        if not isinstance(raw_body, str) or not raw_body.strip():
            raise ValueError("raw_body must be a non-empty string")
        try:
            parsed = json.loads(raw_body)
        except json.JSONDecodeError as exc:
            raise ValueError(f"raw_body is not valid JSON: {exc}") from exc

        request_url = envelope.get("request_url")
        if not isinstance(request_url, str) or not _is_dola_chain_single(request_url):
            raise ValueError("request_url must be an HTTPS dola.com /im/chain/single URL")
        return self._save_parsed(
            raw_body=raw_body,
            parsed=parsed,
            captured_at=envelope.get("captured_at"),
            page_url=str(envelope.get("page_url", "")),
            request_url=request_url,
            response_status=envelope.get("response_status"),
            prefix="dola_chain",
            include_internal=include_internal,
        )

    def save_router_data(self, parsed: Any, *, page_url: str = "", include_internal: bool = False) -> dict[str, Any]:
        raw_body = json.dumps(parsed, ensure_ascii=False, separators=(",", ":"))
        return self._save_parsed(
            raw_body=raw_body,
            parsed=parsed,
            captured_at=datetime.now(timezone.utc).isoformat(),
            page_url=page_url,
            request_url="<window._ROUTER_DATA>",
            response_status=None,
            prefix="dola_router",
            include_internal=include_internal,
        )

    def save_discovered_response(
        self,
        envelope: dict[str, Any],
        *,
        include_internal: bool = False,
    ) -> dict[str, Any]:
        """Resolve a high-relevance response found by network discovery."""
        if not isinstance(envelope, dict):
            raise ValueError("capture envelope must be a JSON object")
        raw_body = envelope.get("raw_body", "")
        if not isinstance(raw_body, str) or not raw_body.strip():
            raise ValueError("raw_body must be a non-empty string")
        try:
            parsed = json.loads(raw_body)
        except json.JSONDecodeError as exc:
            raise ValueError(f"raw_body is not valid JSON: {exc}") from exc
        request_url = envelope.get("request_url")
        if not isinstance(request_url, str):
            raise ValueError("request_url must be a string")
        return self._save_parsed(
            raw_body=raw_body,
            parsed=parsed,
            captured_at=envelope.get("captured_at"),
            page_url=str(envelope.get("page_url", "")),
            request_url=request_url,
            response_status=envelope.get("response_status"),
            prefix="dola_discovery",
            include_internal=include_internal,
        )

    def finalize_playwright_download(
        self,
        capture_result: dict[str, Any],
        resolve_result: Any,
        *,
        output_path: Path,
        ffprobe: dict[str, Any] | None = None,
        method: str = "PLAYWRIGHT_CONTEXT",
        error: Exception | None = None,
    ) -> dict[str, Any]:
        if error is None:
            report = make_report(resolve_result, file_path=output_path, ffprobe=ffprobe)
            report["download"] = {"status": "success", "path": str(output_path), "method": method}
            state = "PASS"
        else:
            report = make_report(resolve_result)
            report["download"] = {
                "status": "failed",
                "error": str(error),
                "url": redact_url(resolve_result.selected.url) if resolve_result.selected else None,
                "bypass_attempted": False,
            }
            state = "FAIL"
        report["acceptance"] = self._acceptance(resolve_result, capture_pass="PASS", download_state=state)
        report["capture"] = {
            "request_url": capture_result.get("request_url", "<captured>"),
            "raw_path": capture_result.get("raw_path"),
            "capture_metadata_path": capture_result.get("meta_path"),
        }
        with self._lock:
            _write_json_atomic(Path(capture_result["resolve_report_path"]), report)
        return report


def make_handler(store: CaptureStore):
    class Handler(BaseHTTPRequestHandler):
        server_version = "DolaCaptureBridge/1.1"

        def _cors(self) -> None:
            # The extension has a chrome-extension:// origin. The bridge is
            # loopback-only and never accepts credentials, so wildcard CORS
            # is safe here and avoids an origin mismatch.
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Headers", "content-type")
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS, GET")

        def _send_json(self, status: int, payload: dict[str, Any]) -> None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self._cors()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_OPTIONS(self) -> None:
            self.send_response(204)
            self._cors()
            self.end_headers()

        def do_GET(self) -> None:
            if urlsplit(self.path).path != "/health":
                self._send_json(404, {"ok": False, "error": "not found"})
                return
            self._send_json(200, {"ok": True})

        def do_POST(self) -> None:
            path = urlsplit(self.path).path
            if path not in {"/capture", DISCOVERY_CAPTURE_PATH}:
                self._send_json(404, {"ok": False, "error": "not found"})
                return
            try:
                length_text = self.headers.get("content-length", "0")
                length = int(length_text)
                if length <= 0 or length > MAX_BODY:
                    raise ValueError("invalid content length")
                data = self.rfile.read(length)
                envelope = json.loads(data.decode("utf-8"))
                result = store.save(envelope) if path == "/capture" else store.save_discovered_response(envelope)
                self._send_json(200, result)
            except Exception as exc:
                self._send_json(400, {"ok": False, "error": str(exc)})

        def log_message(self, fmt: str, *args: object) -> None:
            # Never log request bodies, query strings, tokens, or key_seed.
            print("[bridge] " + fmt.split(" ")[0])

    return Handler


def create_server(
    *,
    host: str = "127.0.0.1",
    port: int = 8765,
    out_dir: str | Path = "captures",
    auto_download: bool = False,
    fetch_fallback: bool = True,
) -> ThreadingHTTPServer:
    if host not in {"127.0.0.1", "localhost"}:
        raise ValueError("capture bridge must bind to loopback")
    store = CaptureStore(Path(out_dir), auto_download=auto_download, fetch_fallback=fetch_fallback)
    server = ThreadingHTTPServer((host, port), make_handler(store))
    server.capture_store = store  # type: ignore[attr-defined]
    return server


def serve(args: argparse.Namespace) -> None:
    server = create_server(
        host=args.host,
        port=args.port,
        out_dir=args.out,
        auto_download=args.auto_download,
        fetch_fallback=not args.no_fetch_fallback,
    )
    store = server.capture_store  # type: ignore[attr-defined]
    print(f"[bridge] listening on http://{args.host}:{args.port}")
    print(f"[bridge] captures -> {store.out_dir}")
    print(f"[bridge] auto-resolve -> enabled; fallback fetch -> {store.fetch_fallback}")
    print(f"[bridge] auto-download -> {store.auto_download}")
    print("[bridge] Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Loopback bridge for authenticated Dola chain/single captures")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--out", default="captures")
    parser.add_argument("--auto-download", action="store_true")
    parser.add_argument("--no-fetch-fallback", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    serve(args)


if __name__ == "__main__":
    main()
