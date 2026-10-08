#!/usr/bin/env python3
"""P1 independent media verifier: ffprobe + full decode + exact-frame checks."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

video = Path(sys.argv[1]).resolve()
report = Path(sys.argv[2]).resolve()
preview = Path(sys.argv[3]).resolve()
report.parent.mkdir(parents=True, exist_ok=True)
result = {
    "stage": "P1_WEB_SMOKE",
    "file": video.name,
    "checks": {},
    "status": "FAIL",
    "error": None
}
def cmd(args):
    return subprocess.run(args, capture_output=True, text=True, check=True)

try:
    if not video.is_file() or video.stat().st_size < 10000:
        raise ValueError("Video missing or suspiciously small")
    probe = json.loads(cmd([
        "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(video)
    ]).stdout)
    vids = [s for s in probe["streams"] if s.get("codec_type") == "video"]
    auds = [s for s in probe["streams"] if s.get("codec_type") == "audio"]
    if len(vids) != 1 or len(auds) != 1:
        raise ValueError(f"Expected 1 video and 1 audio stream; got {len(vids)} and {len(auds)}")
    v, a = vids[0], auds[0]
    duration = float(probe["format"]["duration"])
    frames = int(v.get("nb_frames", "0"))
    fps = v.get("avg_frame_rate")
    result.update({
        "duration_s": duration,
        "bytes": video.stat().st_size,
        "sha256": hashlib.sha256(video.read_bytes()).hexdigest(),
        "video": {"codec": v.get("codec_name"), "width": v.get("width"), "height": v.get("height"), "frames": frames, "fps": fps},
        "audio": {"codec": a.get("codec_name"), "sample_rate": a.get("sample_rate"), "channels": a.get("channels")}
    })
    result["checks"]["dimensions_1080x1920"] = (v.get("width"), v.get("height")) == (1080, 1920)
    result["checks"]["exactly_60_frames"] = frames == 60
    result["checks"]["fps_30"] = fps == "30/1"
    result["checks"]["duration_2s"] = abs(duration - 2) < .08
    result["checks"]["audio_aac_stereo"] = a.get("codec_name") == "aac" and a.get("channels") == 2
    decoded = subprocess.run(["ffmpeg","-hide_banner","-v","error","-xerror","-i",str(video),"-f","null","-"],capture_output=True,text=True)
    result["checks"]["full_decode"] = decoded.returncode == 0
    result["decode_errors"] = decoded.stderr[-2000:]
    cmd(["ffmpeg","-hide_banner","-loglevel","error","-y","-ss","1.0","-i",str(video),"-frames:v","1",str(preview)])
    result["checks"]["preview_png"] = preview.exists() and preview.stat().st_size > 1000
    result["status"] = "PASS" if all(result["checks"].values()) else "FAIL"
except Exception as exc:
    result["error"] = f"{type(exc).__name__}: {exc}"
finally:
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
if result["status"] != "PASS":
    sys.exit(1)
