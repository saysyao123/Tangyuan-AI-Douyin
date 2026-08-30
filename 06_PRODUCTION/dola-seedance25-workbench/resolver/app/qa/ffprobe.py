from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


def find_ffprobe() -> str | None:
    return shutil.which("ffprobe")


def probe_media(path: str | Path) -> dict[str, Any]:
    ffprobe = find_ffprobe()
    if not ffprobe:
        raise RuntimeError("ffprobe is not available on PATH")
    command = [
        ffprobe,
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=codec_name,width,height,bit_rate,r_frame_rate",
        "-show_entries",
        "format=duration,size,bit_rate",
        "-of",
        "json",
        str(Path(path)),
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=True)
    payload = json.loads(completed.stdout)
    stream = (payload.get("streams") or [{}])[0]
    fmt = payload.get("format") or {}
    return {
        "codec_name": stream.get("codec_name"),
        "width": stream.get("width"),
        "height": stream.get("height"),
        "bit_rate": stream.get("bit_rate"),
        "r_frame_rate": stream.get("r_frame_rate"),
        "duration": fmt.get("duration"),
        "size": fmt.get("size"),
        "format_bit_rate": fmt.get("bit_rate"),
    }
