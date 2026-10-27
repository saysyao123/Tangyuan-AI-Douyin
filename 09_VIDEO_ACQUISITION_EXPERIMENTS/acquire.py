#!/usr/bin/env python3
"""Controlled video acquisition and QA. Uses yt-dlp + ffprobe/ffmpeg.

No platform login bypass, no DRM decryption, no automatic publication.
The caller is responsible for access rights and downstream reuse permissions.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import uuid
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

ERROR_PATTERNS = (
    ("SESSION_NEEDED", (r"fresh cookies", r"sign in to confirm", r"login required", r"sign in to view")),
    ("HTTP_412", (r"\b412\b", r"precondition failed")),
    ("HTTP_403", (r"\b403\b", r"forbidden")),
    ("HTTP_429", (r"\b429\b", r"too many requests")),
    ("GEO_RESTRICTED", (r"not available in your country", r"geo.?restricted", r"not available in your region")),
    ("DRM_PROTECTED", (r"\bdrm\b", r"protected by")),
    ("UNAVAILABLE", (r"video unavailable", r"not available", r"private video", r"removed")),
    ("NO_FORMATS", (r"requested format is not available", r"no video formats found")),
    ("UNSUPPORTED", (r"unsupported url",)),
    ("TIMEOUT", (r"timed out",)),
)

def classify_error(message: str) -> str:
    s = message.lower()
    for category, patterns in ERROR_PATTERNS:
        if any(re.search(pattern, s) for pattern in patterns):
            return category
    return "OTHER"

def safe_source_url(url: str) -> str:
    p = urlsplit(url)
    # Never persist source URLs with arbitrary access keys or signed query parameters.
    keep = [(key, value) for key, value in parse_qsl(p.query, keep_blank_values=True)
            if key == "v" and (p.hostname or "").lower().endswith("youtube.com")
            and re.fullmatch(r"[-_A-Za-z0-9]{1,20}", value)]
    return urlunsplit((p.scheme, p.netloc, p.path, urlencode(keep), ""))

def platform_of(url: str) -> str:
    host = (urlsplit(url).hostname or "").lower()
    for name, suffixes in {
        "douyin": ("douyin.com", "v.douyin.com"),
        "bilibili": ("bilibili.com", "b23.tv"),
        "youtube": ("youtube.com", "youtu.be"),
        "hongguo_related_web": ("hongguoduanju.com",),
        "w3c_media_control": ("media.w3.org",),
    }.items():
        if any(host == suffix or host.endswith("." + suffix) for suffix in suffixes):
            return name
    return "generic_web"

def tool_run(args: list[str], timeout: int, redact: str = "") -> dict:
    started = time.monotonic()
    try:
        p = subprocess.run(args, capture_output=True, text=True, errors="replace", timeout=timeout)
        outcome = {"rc": p.returncode, "stdout": p.stdout, "stderr": p.stderr}
    except subprocess.TimeoutExpired:
        outcome = {"rc": None, "stdout": "", "stderr": f"Timed out after {timeout}s"}
    except OSError as e:
        outcome = {"rc": None, "stdout": "", "stderr": f"{type(e).__name__}: {e}"}
    outcome["seconds"] = round(time.monotonic() - started, 2)
    if redact:
        # Redact credentials embedded in the original URL, if any.
        outcome["stderr"] = outcome["stderr"].replace(redact, safe_source_url(redact))
    return outcome

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def summarize_error(o: dict, url: str) -> tuple[str, str]:
    msg = (o.get("stderr") or o.get("stdout") or "").replace(url, safe_source_url(url))
    lines = [x.strip() for x in msg.splitlines() if x.strip()]
    interesting = [x for x in lines if "error" in x.lower()] or lines
    short = (interesting[-1] if interesting else "Unknown failure")[:650]
    return classify_error(msg), short

def ffprobe_file(path: Path) -> dict:
    result = tool_run(["ffprobe", "-v", "error", "-show_entries",
                       "format=duration,size:stream=codec_type,codec_name,width,height",
                       "-of", "json", str(path)], 30)
    if result["rc"] != 0:
        raise RuntimeError("ffprobe failed: " + result["stderr"][-300:])
    obj = json.loads(result["stdout"])
    streams = obj.get("streams") or []
    video = [v for v in streams if v.get("codec_type") == "video"]
    audio = [v for v in streams if v.get("codec_type") == "audio"]
    if not video:
        raise RuntimeError("No video stream")
    sec = float(obj.get("format", {}).get("duration") or 0)
    if sec <= 0:
        raise RuntimeError("Video duration not positive")
    decode = tool_run(["ffmpeg", "-v", "error", "-i", str(path),
                       "-t", str(min(2, sec)), "-f", "null", "-"], 45)
    if decode["rc"] != 0:
        raise RuntimeError("Decode failed: " + decode["stderr"][-350:])
    return {"duration_seconds": round(sec, 3), "width": video[0].get("width"),
            "height": video[0].get("height"), "video_codec": video[0].get("codec_name"),
            "audio_codecs": [a.get("codec_name") for a in audio],
            "bytes": path.stat().st_size, "sha256": sha256_file(path),
            "decode_passed": True}

def execute(url: str, mode: str, root: Path, clip_seconds: float,
            max_size_mb: int, browser: str | None, rights_basis: str) -> tuple[int, dict]:
    src = urlsplit(url)
    if src.scheme not in ("https", "http") or not src.hostname or src.username or src.password:
        raise ValueError("Only valid public HTTP(S) video-page URLs accepted")
    if browser and os.environ.get("GITHUB_ACTIONS"):
        raise ValueError("Browser-cookie access is forbidden in hosted CI")
    if mode == "full" and rights_basis not in ("owner", "licensed", "platform_permitted"):
        raise ValueError("Full download requires --rights-basis owner|licensed|platform_permitted")
    if mode == "clip" and rights_basis == "unspecified":
        raise ValueError("Clip tests require explicit --rights-basis (internal_evaluation permitted)")
    if not 1 <= clip_seconds <= 10:
        raise ValueError("Clip duration must be 1..10 seconds")
    if not 1 <= max_size_mb <= 2000:
        raise ValueError("Max size must be 1..2000 MB")
    slug = platform_of(url)
    uid = hashlib.sha256(url.encode()).hexdigest()[:12]
    dirname = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = root / f"{slug}-{uid}-{dirname}-{uuid.uuid4().hex[:8]}"
    run_dir.mkdir(parents=True, exist_ok=True)
    report: dict = {
        "schema_version": 1, "source_url": safe_source_url(url), "platform": slug,
        "verified_official_source": False if slug == "hongguo_related_web" else None,
        "mode": mode, "rights_basis": rights_basis,
        "created_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "metadata_ok": False, "download_attempted": False,
        "file_verified": False, "ready_for_editor_review": False,
        "error_code": None, "error_detail": None,
        "media": None,
    }
    manifest = run_dir / "asset_manifest.json"
    try:
        common = ["yt-dlp", "--ignore-config", "--no-playlist", "--no-warnings",
                  "--socket-timeout", "12", "--retries", "1", "--fragment-retries", "1"]
        if browser:
            common += ["--cookies-from-browser", browser]
        probe = tool_run([*common, "--dump-single-json", "--skip-download", url],
                         timeout=85, redact=url)
        report["probe_seconds"] = probe["seconds"]
        if probe["rc"] != 0:
            report["error_code"], report["error_detail"] = summarize_error(probe, url)
            report["status"] = "ACCESS_BLOCKED_OR_EXTRACTION_FAILED"
            return 2, report
        try:
            info = json.loads(probe["stdout"])
        except Exception:
            report.update(error_code="BAD_METADATA", error_detail="Invalid yt-dlp JSON",
                          status="EXTRACTION_FAILED")
            return 2, report
        report.update(metadata_ok=True, title=str(info.get("title") or "")[:150],
                      extractor=info.get("extractor_key"), video_id=str(info.get("id", ""))[:100],
                      original_duration=info.get("duration"), format_count=len(info.get("formats") or []),
                      availability=info.get("availability"))
        if info.get("has_drm") is True or info.get("is_live"):
            report.update(status="RESTRICTED_MEDIA", error_code="DRM_OR_LIVE",
                          error_detail="No DRM-protected media or live streams downloaded")
            return 3, report
        if mode == "probe":
            report["status"] = "METADATA_ONLY"
            return 0, report
        report["download_attempted"] = True
        # Private, isolated folder prevents stale-file false positives.
        out_template = str(run_dir / "%(id).80s.%(ext)s")
        fmt = "b[height<=480]/bv*[height<=480]+ba/worst" if mode == "clip" else "bv*+ba/b"
        cmd = [*common, "-f", fmt, "--merge-output-format", "mp4",
               "--max-filesize", f"{max_size_mb}M", "--no-overwrites",
               "--no-progress", "-o", out_template]
        if mode == "clip":
            cmd += ["--download-sections", f"*0-{clip_seconds:g}"]
        cmd.append(url)
        got = tool_run(cmd, timeout=110 if mode == "clip" else 1800, redact=url)
        report["download_seconds"] = got["seconds"]
        candidates = [f for f in run_dir.iterdir()
                      if f.is_file() and f.name != manifest.name
                      and not (f.name.endswith((".part", ".ytdl", ".json", ".temp", ".aria2")))]
        if got["rc"] != 0 or not candidates:
            report["error_code"], report["error_detail"] = summarize_error(got, url)
            if got["rc"] == 0 and not candidates:
                report["error_code"], report["error_detail"] = "NO_OUTPUT", "No final media file was generated"
            report["status"] = "DOWNLOAD_FAILED"
            return 4, report
        candidate = max(candidates, key=lambda x: x.stat().st_size)
        try:
            media = ffprobe_file(candidate)
        except Exception as e:
            report.update(error_code="MEDIA_QA_FAILED", error_detail=str(e)[:450],
                          status="MEDIA_QA_FAILED")
            return 5, report
        report.update(media=media, file_verified=True,
                      status="VERIFIED_CLIP_TEMPORARY" if mode == "clip" else "FILE_VERIFIED")
        if mode == "full":
            report["media"]["local_file"] = str(candidate.resolve())
            report["ready_for_editor_review"] = True
            report["editorial_review_required"] = True
        return 0, report
    finally:
        # No recorded media samples survive a clip smoke test.
        if mode == "clip":
            for file in run_dir.iterdir():
                if file.is_file() and file != manifest:
                    file.unlink(missing_ok=True)
        manifest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Video acquisition with explicit QA and rights gate")
    p.add_argument("--url", required=True)
    p.add_argument("--mode", choices=("probe", "clip", "full"), default="probe")
    p.add_argument("--output-dir", type=Path, default=Path("acquisition_runs"))
    p.add_argument("--clip-seconds", type=float, default=3.0)
    p.add_argument("--max-size-mb", type=int, default=50)
    p.add_argument("--rights-basis", choices=("unspecified", "internal_evaluation", "owner", "licensed",
                                               "platform_permitted"), default="unspecified")
    p.add_argument("--browser", choices=("chrome", "edge", "firefox"), default=None,
                   help="EXPLICIT local consent only. Never use on CI or share browser profile.")
    args = p.parse_args(argv)
    try:
        rc, result = execute(args.url, args.mode, args.output_dir, args.clip_seconds,
                             args.max_size_mb, args.browser, args.rights_basis)
    except Exception as e:
        rc, result = 6, {"status": "SETUP_OR_POLICY_ERROR", "error_code": type(e).__name__,
                         "error_detail": str(e)[:450]}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True), flush=True)
    return rc

if __name__ == "__main__":
    sys.exit(main())
