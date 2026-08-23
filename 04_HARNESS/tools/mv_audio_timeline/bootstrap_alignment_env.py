#!/usr/bin/env python3
"""Create/check a pinned local MV lyric-alignment environment.

No silent fallback: installation/model-preheat failures exit non-zero.
Default mode is `doctor`; use `install` explicitly to mutate the environment.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOCK = HERE / "alignment_runtime.lock.json"


def load_lock() -> dict:
    return json.loads(LOCK.read_text(encoding="utf-8"))


def run(cmd: list[str], *, env=None, check=True) -> subprocess.CompletedProcess:
    print("+", " ".join(cmd), flush=True)
    return subprocess.run(cmd, text=True, env=env, check=check)


def venv_python(venv: Path) -> Path:
    return venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def venv_bin(venv: Path, name: str) -> Path:
    suffix = ".exe" if os.name == "nt" else ""
    return venv / ("Scripts" if os.name == "nt" else "bin") / f"{name}{suffix}"


def ensure_python(lock: dict) -> None:
    if not (sys.version_info.major == 3 and 11 <= sys.version_info.minor < 14):
        raise RuntimeError(f"Primary aligner requires Python >=3.11,<3.14; current={platform.python_version()}")


def cmd_install(args) -> int:
    lock = load_lock(); ensure_python(lock)
    venv = Path(args.venv).resolve()
    if not venv.exists(): run([sys.executable, "-m", "venv", str(venv)])
    py = venv_python(venv)
    run([str(py), "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
    p = lock["primary"]
    primary_url = f"git+{p['repository']}@{p['git_commit']}#egg={p['name']}[{p['install_extra']}]"
    run([str(py), "-m", "pip", "install", primary_url])
    if args.with_secondary:
        s = lock["secondary"]; extras = ",".join(s["install_extras"])
        secondary_url = f"git+{s['repository']}@{s['git_commit']}#egg={s['name']}[{extras}]"
        run([str(py), "-m", "pip", "install", secondary_url])
    env = os.environ.copy()
    if args.hf_home:
        hf = str(Path(args.hf_home).resolve()); Path(hf).mkdir(parents=True, exist_ok=True)
        env["HF_HOME"] = hf; env["HUGGINGFACE_HUB_CACHE"] = str(Path(hf) / "hub")
    xingyu = venv_bin(venv, p["cli"])
    run([str(xingyu), "doctor"], env=env)
    if args.preheat:
        run([str(xingyu), "models", "pull", "--language", p["language"], "--device", args.device], env=env)
    write_env_manifest(venv, env, lock)
    print(json.dumps({"success": True, "venv": str(venv), "preheated": bool(args.preheat)}, ensure_ascii=False))
    return 0


def capture(cmd: list[str], env=None) -> str:
    p = subprocess.run(cmd, text=True, capture_output=True, env=env)
    return ((p.stdout or "") + (p.stderr or "")).strip()


def write_env_manifest(venv: Path, env: dict, lock: dict) -> Path:
    py = venv_python(venv); p = lock["primary"]; s = lock["secondary"]
    manifest = {
        "schema_version": "1.0",
        "python": capture([str(py), "--version"]),
        "platform": platform.platform(),
        "ffmpeg": capture(["ffmpeg", "-version"]).splitlines()[0] if shutil.which("ffmpeg") else None,
        "primary_expected": p,
        "primary_actual_version": capture([str(venv_bin(venv, p['cli'])), "--version"]),
        "secondary_expected": s,
        "secondary_actual_version": capture([str(venv_bin(venv, s['cli'])), "--version"]) if venv_bin(venv, s['cli']).exists() else None,
        "hf_home": env.get("HF_HOME"),
    }
    out = venv / "mv_audio_alignment_environment.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


def cmd_doctor(args) -> int:
    lock = load_lock(); venv = Path(args.venv).resolve(); errors=[]; notes=[]
    if not venv_python(venv).exists(): errors.append("venv python missing")
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"): errors.append("ffmpeg/ffprobe missing")
    p = lock["primary"]; x = venv_bin(venv, p["cli"])
    if not x.exists(): errors.append("primary xingyu-align missing")
    else:
        ver = capture([str(x), "--version"]); notes.append(f"primary={ver}")
        if p["version"] not in ver: errors.append(f"primary version drift: expected {p['version']}, got {ver}")
        d = subprocess.run([str(x), "doctor"], text=True, capture_output=True)
        if d.returncode != 0: errors.append("xingyu-align doctor failed")
    s = lock["secondary"]; y = venv_bin(venv, s["cli"])
    if y.exists():
        ver = capture([str(y), "--version"]); notes.append(f"secondary={ver}")
        if s["version"] not in ver: errors.append(f"secondary version drift: expected {s['version']}, got {ver}")
    else: notes.append("secondary not installed (allowed unless cross-check requested)")
    result={"pass": not errors, "errors": errors, "notes": notes, "venv": str(venv)}
    print(json.dumps(result, ensure_ascii=False, indent=2)); return 0 if not errors else 2


def main() -> int:
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest="cmd", required=True)
    a=sub.add_parser("install"); a.add_argument("--venv", default=".mv-audio-align-venv"); a.add_argument("--hf-home"); a.add_argument("--device", default="cpu"); a.add_argument("--preheat", action="store_true"); a.add_argument("--with-secondary", action="store_true"); a.set_defaults(func=cmd_install)
    a=sub.add_parser("doctor"); a.add_argument("--venv", default=".mv-audio-align-venv"); a.set_defaults(func=cmd_doctor)
    args=ap.parse_args()
    try: return args.func(args)
    except Exception as e:
        print(json.dumps({"success": False, "state": "AUDIO_ALIGNMENT_RUNTIME_BLOCKED", "error": type(e).__name__, "message": str(e)}, ensure_ascii=False), file=sys.stderr); return 3

if __name__ == "__main__": raise SystemExit(main())
