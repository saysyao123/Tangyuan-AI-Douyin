from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlsplit

from app.discovery.router_data import walk_json
from app.logger import redact_url
from app.qa.report import make_report
from app.resolver.resolver import resolve_metadata


GENERATION_FIELD_SCORES = {
    "fallback_api": 15,
    "original_media_info": 15,
    "video_list": 15,
    "key_seed": 12,
    "main_url": 10,
    "play_infos": 10,
    "node_id": 8,
    "video_id": 8,
    "vid": 8,
    "media_info": 6,
    "task_id": 5,
    "generation_id": 5,
    "video_model": 1,
}

VID_PATTERN = re.compile(r"^v[0-9][A-Za-z0-9]{20,}$")
GENERATION_FILES = (
    "network-index.json",
    "fetch-events.jsonl",
    "xhr-events.jsonl",
    "sse-events.jsonl",
    "websocket-events.jsonl",
    "raw-responses.jsonl",
    "media-hits.json",
)
DERIVED_FILES = {"identity-chain.json", "resolver-input.json"}
REQUEST_PATH_HINTS = (
    "chat",
    "completion",
    "generate",
    "generation",
    "task",
    "message",
    "chain",
    "video",
    "media",
    "play",
)


def _write_json_atomic(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_name(path.name + ".part")
    try:
        partial.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(partial, path)
    finally:
        if partial.exists():
            partial.unlink()


def _normal_key(value: Any) -> str:
    return re.sub(r"[^a-z0-9]", "", str(value).lower())


def _string(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(value)
    return None


def _valid_vid(value: Any) -> str | None:
    text = _string(value)
    return text if text and VID_PATTERN.match(text) else None


def _unique(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        if value and value not in result:
            result.append(value)
    return result


def _is_url_field(field: str) -> bool:
    return _normal_key(field) in {
        "mainurl",
        "manurl",
        "playurl",
        "downloadurl",
        "url",
    }


def _safe_evidence_value(field: str, value: Any) -> Any:
    text = _string(value)
    if text is None:
        return "<present>" if value is not None else None
    if _is_url_field(field):
        return redact_url(text)
    if _normal_key(field) in {"keyseed", "authorization", "cookie", "token"}:
        return "<REDACTED>"
    return text[:256]


def _media_context(path: tuple[str | int, ...], parent: dict[str, Any]) -> bool:
    path_text = ".".join(str(part).lower() for part in path)
    normalized = {_normal_key(key) for key in parent}
    return (
        any(marker in path_text for marker in ("video", "media", "play", "generation", "download"))
        or bool(normalized & {"nodeid", "mediainfo", "videolist", "playinfos", "originalmediainfo"})
    )


def scan_generation_identity(payloads: Any) -> dict[str, Any]:
    """Extract generation identity with explicit-field and media-context rules."""

    values: dict[str, list[str]] = {
        "task_ids": [],
        "generation_ids": [],
        "message_ids": [],
        "conversation_ids": [],
        "vids": [],
        "node_ids": [],
        "media_keys": [],
        "fallback_apis": [],
    }
    flags = {
        "key_seed_found": False,
        "video_list_found": False,
        "original_media_info_found": False,
        "media_info_found": False,
        "main_url_found": False,
        "play_infos_found": False,
        "generation_request_captured": False,
    }
    evidence: list[dict[str, Any]] = []
    seen_evidence: set[tuple[str, str, str]] = set()

    def add(field: str, value: Any, path: tuple[str | int, ...], *, valid: bool = True) -> None:
        if not valid:
            return
        safe_value = _safe_evidence_value(field, value)
        identity = (field, ".".join(str(part) for part in path), str(safe_value))
        if identity in seen_evidence:
            return
        seen_evidence.add(identity)
        evidence.append({"field": field, "path": list(path), "value": safe_value})

    for path, node in walk_json(payloads):
        if not isinstance(node, dict):
            continue
        media_context = _media_context(path, node)
        normalized_parent = {_normal_key(key): value for key, value in node.items()}
        has_node_id = bool(_string(normalized_parent.get("nodeid")))
        for raw_key, raw_value in node.items():
            field = str(raw_key)
            key = _normal_key(field)
            text = _string(raw_value)
            if key in {"taskid"} and text:
                values["task_ids"].append(text)
                add(field, raw_value, path + (field,))
            elif key in {"generationid"} and text:
                values["generation_ids"].append(text)
                add(field, raw_value, path + (field,))
            elif key in {"messageid"} and text:
                values["message_ids"].append(text)
                add(field, raw_value, path + (field,))
            elif key in {"conversationid"} and text:
                values["conversation_ids"].append(text)
                add(field, raw_value, path + (field,))
            elif key in {"vid", "videoid"}:
                valid_vid = _valid_vid(raw_value)
                if valid_vid:
                    values["vids"].append(valid_vid)
                    add(field, valid_vid, path + (field,), valid=True)
            elif key == "nodeid" and text:
                values["node_ids"].append(text)
                add(field, raw_value, path + (field,))
            elif key == "key" and text and (media_context or has_node_id):
                values["media_keys"].append(text)
                add(field, raw_value, path + (field,))
            elif key == "fallbackapi" and text:
                values["fallback_apis"].append(text)
                flags["generation_request_captured"] = True
                add(field, raw_value, path + (field,))
            elif key == "keyseed" and text:
                flags["key_seed_found"] = True
                add(field, raw_value, path + (field,))
            elif key == "videolist":
                flags["video_list_found"] = True
                add(field, raw_value, path + (field,))
            elif key == "originalmediainfo":
                flags["original_media_info_found"] = True
                add(field, raw_value, path + (field,))
            elif key == "mediainfo":
                flags["media_info_found"] = True
                add(field, raw_value, path + (field,))
            elif key == "mainurl":
                flags["main_url_found"] = True
                add(field, raw_value, path + (field,))
            elif key == "playinfos":
                flags["play_infos_found"] = True
                add(field, raw_value, path + (field,))

    for item in evidence:
        path_text = ".".join(str(part).lower() for part in item["path"])
        if any(hint in path_text for hint in REQUEST_PATH_HINTS):
            flags["generation_request_captured"] = True
            break

    for key in values:
        values[key] = _unique(values[key])
    identity_pass = bool(values["vids"] or (values["node_ids"] and values["media_keys"]) or values["fallback_apis"])
    return {
        "flags": flags,
        "values": values,
        "evidence": evidence,
        "identity_pass": identity_pass,
        "security": {
            "cookies_emitted": False,
            "authorization_emitted": False,
            "signed_query_emitted": False,
            "key_seed_emitted": False,
        },
    }


def _load_bundle_payloads(bundle_dir: Path) -> tuple[list[Any], list[str]]:
    payloads: list[Any] = []
    sources: list[str] = []

    def add_embedded_json(value: Any) -> None:
        """Recover JSON objects wrapped in SSE/data or other text envelopes."""
        if not isinstance(value, str):
            return
        candidates = [value]
        candidates.extend(
            line.split(":", 1)[1].strip()
            for line in value.splitlines()
            if line.lstrip().lower().startswith("data:") and ":" in line
        )
        for candidate in candidates:
            try:
                embedded = json.loads(candidate)
            except json.JSONDecodeError:
                continue
            if isinstance(embedded, (dict, list)):
                payloads.append(embedded)

    for name in GENERATION_FILES:
        path = bundle_dir / name
        if not path.is_file():
            continue
        sources.append(name)
        if path.suffix == ".jsonl":
            with path.open("r", encoding="utf-8") as handle:
                for line in handle:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        row = json.loads(line)
                        payloads.append(row)
                        if isinstance(row, dict):
                            for key in ("body", "chunk", "text", "payload"):
                                add_embedded_json(row.get(key))
                    except json.JSONDecodeError:
                        payloads.append({"text": line})
                        add_embedded_json(line)
        else:
            try:
                row = json.loads(path.read_text(encoding="utf-8"))
                payloads.append(row)
                if isinstance(row, dict):
                    for key in ("body", "chunk", "text", "payload"):
                        add_embedded_json(row.get(key))
            except json.JSONDecodeError:
                continue
    return payloads, sources


def _all_text(payloads: Any) -> str:
    chunks: list[str] = []
    for _, node in walk_json(payloads):
        if isinstance(node, str):
            chunks.append(node)
    return "\n".join(chunks)


def _protocol(sources: list[str], payloads: Any) -> str:
    text = _all_text(payloads).lower()
    names = {name.lower() for name in sources}
    if "sse-events.jsonl" in names and "event-stream" in text:
        return "FETCH_SSE"
    if "websocket-events.jsonl" in names:
        return "WEBSOCKET"
    if "xhr-events.jsonl" in names:
        return "XHR"
    if "fetch-events.jsonl" in names:
        return "FETCH"
    return "JSON" if payloads else "OTHER"


def _bundle_flag(bundle_dir: Path, key: str) -> str:
    path = bundle_dir / "network-index.json"
    if not path.is_file():
        return "FAIL"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return "FAIL"
    value = data.get(key) if isinstance(data, dict) else None
    if isinstance(value, bool):
        return "PASS" if value else "FAIL"
    if isinstance(value, str):
        upper = value.upper()
        if upper in {"PASS", "YES", "TRUE"}:
            return "PASS"
        if upper in {"FAIL", "NO", "FALSE"}:
            return "FAIL"
    return "FAIL"


def _path_text(payloads: Any) -> str:
    paths: list[str] = []
    for _, node in walk_json(payloads):
        if not isinstance(node, dict):
            continue
        for key in ("path", "url", "request_url", "response_url"):
            value = node.get(key)
            if isinstance(value, str):
                try:
                    parsed = urlsplit(value)
                    paths.append(parsed.path.lower())
                except ValueError:
                    paths.append(value.lower())
    return "\n".join(paths)


def _resolution(result: Any) -> str:
    candidates = result.candidates or []
    candidate = result.selected or (candidates[0] if candidates else None)
    if candidate and candidate.width and candidate.height:
        return f"{candidate.width}x{candidate.height}"
    return "UNKNOWN"


def _bitrate(result: Any) -> int | str:
    values = [candidate.effective_bitrate for candidate in result.candidates if candidate.effective_bitrate]
    return max(values) if values else "UNKNOWN"


def resolve_generation_bundle(
    bundle_dir: str | Path,
    *,
    fetch_fallback: bool = False,
) -> dict[str, Any]:
    bundle = Path(bundle_dir).resolve()
    if not bundle.is_dir():
        raise ValueError(f"generation bundle does not exist: {bundle}")
    payloads, sources = _load_bundle_payloads(bundle)
    identity = scan_generation_identity(payloads)
    result = resolve_metadata(payloads, fetch_fallback=fetch_fallback)
    paths = _path_text(payloads)
    report = make_report(result)
    report.update(
        {
            "bundle_dir": str(bundle),
            "sources": sources,
            "FULL_CDP": _bundle_flag(bundle, "full_cdp"),
            "CAPTURE_ARMED_BEFORE_GENERATION": _bundle_flag(bundle, "capture_armed_before_generation"),
            "GENERATION_REQUEST_CAPTURED": "YES" if identity["flags"]["generation_request_captured"] else "NO",
            "STREAMING_PROTOCOL": _protocol(sources, payloads),
            "TASK_ID_FOUND": "YES" if identity["values"]["task_ids"] else "NO",
            "MESSAGE_ID_FOUND": "YES" if identity["values"]["message_ids"] else "NO",
            "VID_FOUND": "YES" if identity["values"]["vids"] else "NO",
            "NODE_ID_FOUND": "YES" if identity["values"]["node_ids"] else "NO",
            "MEDIA_KEY_FOUND": "YES" if identity["values"]["media_keys"] else "NO",
            "FALLBACK_API_FOUND": "YES" if identity["values"]["fallback_apis"] else "NO",
            "KEY_SEED_FOUND": "YES" if identity["flags"]["key_seed_found"] else "NO",
            "VIDEO_LIST_FOUND": "YES" if identity["flags"]["video_list_found"] else "NO",
            "ORIGINAL_MEDIA_INFO_FOUND": "YES" if identity["flags"]["original_media_info_found"] else "NO",
            "GET_PLAY_INFO_CALLED": "PASS" if "/samantha/video/get_play_info" in paths else "NOT_AVAILABLE",
            "GENERATION_MEDIA_IDENTITY_CAPTURE": "PASS" if identity["identity_pass"] else "FAIL",
            "FOUND_CLEAN_CANDIDATE": "YES" if result.clean_candidates else "NO",
            "HIGHEST_NATIVE_RESOLUTION": _resolution(result),
            "HIGHEST_BITRATE": _bitrate(result),
            "DOWNLOAD": "NOT_AVAILABLE",
            "FFPROBE": "NOT_RUN",
            "VISIBLE_DOLA_WATERMARK": "UNVERIFIED",
            "identity": {
                "task_ids": identity["values"]["task_ids"],
                "generation_ids": identity["values"]["generation_ids"],
                "message_ids": identity["values"]["message_ids"],
                "conversation_ids": identity["values"]["conversation_ids"],
                "vids": identity["values"]["vids"],
                "node_ids": identity["values"]["node_ids"],
                "media_keys": identity["values"]["media_keys"],
                "fallback_api_count": len(identity["values"]["fallback_apis"]),
            },
        }
    )

    _write_json_atomic(
        bundle / "identity-chain.json",
        {
            "flags": identity["flags"],
            "values": identity["values"],
            "evidence": identity["evidence"],
            "identity_pass": identity["identity_pass"],
            "security": identity["security"],
        },
    )
    _write_json_atomic(
        bundle / "media-hits.json",
        {
            "identity_pass": identity["identity_pass"],
            "flags": identity["flags"],
            "evidence": identity["evidence"],
            "security": identity["security"],
        },
    )
    _write_json_atomic(
        bundle / "resolver-input.json",
        {"sources": sources, "payloads": payloads, "security": identity["security"]},
    )
    _write_json_atomic(bundle / "generation-report.json", report)
    return report


__all__ = ["GENERATION_FIELD_SCORES", "resolve_generation_bundle", "scan_generation_identity"]
