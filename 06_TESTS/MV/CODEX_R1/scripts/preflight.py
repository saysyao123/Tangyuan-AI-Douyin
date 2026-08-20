#!/usr/bin/env python3
"""CODEX R1 C00 environment preflight.

Creates local runtime directories and a machine-readable env report.
No secrets are read or written.
"""

from __future__ import annotations

import importlib.util
import json
import os
import platform
import shutil
import socket
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
LOCAL = ROOT / "local"
OUTPUTS = LOCAL / "outputs"
REPORTS = OUTPUTS / "reports"
LOGS = OUTPUTS / "logs"

for p in [
    LOCAL / "inputs" / "audio",
    LOCAL / "inputs" / "videos",
    LOCAL / "inputs" / "links",
    OUTPUTS / "audio",
    OUTPUTS / "sources",
    OUTPUTS / "subtitles",
    OUTPUTS / "video",
    OUTPUTS / "final",
    OUTPUTS / "manifests",
    REPORTS,
    LOGS,
]:
    p.mkdir(parents=True, exist_ok=True)


def command_info(name: str) -> dict:
    path = shutil.which(name)
    result = {"found": bool(path), "path": path, "version": None}
    if not path:
        return result
    probes = {
        "git": [name, "--version"],
        "ffmpeg": [name, "-version"],
        "ffprobe": [name, "-version"],
        "whisper": [name, "--help"],
    }
    cmd = probes.get(name, [name, "--version"])
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=12)
        text = (proc.stdout or proc.stderr or "").strip().splitlines()
        result["version"] = text[0][:300] if text else None
    except Exception as exc:
        result["probe_error"] = repr(exc)
    return result


def module_info(name: str) -> dict:
    spec = importlib.util.find_spec(name)
    return {"found": spec is not None, "origin": getattr(spec, "origin", None) if spec else None}


def network_probe(host: str = "github.com", port: int = 443) -> dict:
    try:
        with socket.create_connection((host, port), timeout=5):
            return {"ok": True, "target": f"{host}:{port}"}
    except Exception as exc:
        return {"ok": False, "target": f"{host}:{port}", "error": repr(exc)}


def git_context() -> dict:
    info = {"is_repo": False, "branch": None, "root": None, "error": None}
    try:
        repo_root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True, stderr=subprocess.STDOUT, timeout=10
        ).strip()
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"], text=True, stderr=subprocess.STDOUT, timeout=10
        ).strip()
        info.update({"is_repo": True, "branch": branch, "root": repo_root})
    except Exception as exc:
        info["error"] = repr(exc)
    return info


report = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "platform": platform.platform(),
    "python": {
        "version": sys.version,
        "executable": sys.executable,
        "meets_minimum_3_10": sys.version_info >= (3, 10),
    },
    "commands": {
        "git": command_info("git"),
        "ffmpeg": command_info("ffmpeg"),
        "ffprobe": command_info("ffprobe"),
        "whisper_cli": command_info("whisper"),
    },
    "python_modules": {
        "faster_whisper": module_info("faster_whisper"),
        "openai_whisper": module_info("whisper"),
        "playwright": module_info("playwright"),
    },
    "browsers": {
        "chrome": shutil.which("chrome") or shutil.which("google-chrome") or shutil.which("chrome.exe"),
        "chromium": shutil.which("chromium") or shutil.which("chromium-browser"),
        "edge": shutil.which("msedge") or shutil.which("msedge.exe"),
    },
    "network": network_probe(),
    "git_context": git_context(),
    "runtime_root": str(LOCAL),
}

core = {
    "python": report["python"]["meets_minimum_3_10"],
    "git": report["commands"]["git"]["found"],
    "ffmpeg": report["commands"]["ffmpeg"]["found"],
    "ffprobe": report["commands"]["ffprobe"]["found"],
    "whisper": (
        report["commands"]["whisper_cli"]["found"]
        or report["python_modules"]["faster_whisper"]["found"]
        or report["python_modules"]["openai_whisper"]["found"]
    ),
}
report["core_requirements"] = core

if all(core.values()):
    status = "PASS"
elif core["python"] and core["git"] and core["ffmpeg"] and core["ffprobe"]:
    status = "PARTIAL_WHISPER_MISSING"
else:
    status = "BLOCKED_CORE_DEPENDENCY"

report["status"] = status

report_path = REPORTS / "env_report.json"
report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

log_path = LOGS / "C00_preflight.log"
log_path.write_text(
    "CODEX R1 C00 preflight\n"
    + f"status={status}\n"
    + json.dumps(core, ensure_ascii=False, indent=2)
    + "\n",
    encoding="utf-8",
)

print(json.dumps({"status": status, "report": str(report_path), "core": core}, ensure_ascii=False, indent=2))

# Do not hide partial state from Codex. A nonzero code signals that setup/fix is needed.
if status == "PASS":
    raise SystemExit(0)
elif status.startswith("PARTIAL"):
    raise SystemExit(1)
else:
    raise SystemExit(2)
