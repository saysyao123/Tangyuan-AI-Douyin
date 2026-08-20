from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Cut a short BGM preview with ffmpeg")
    parser.add_argument("audio", help="source audio file")
    parser.add_argument("--start", type=float, default=0.0, help="start seconds")
    parser.add_argument("--duration", type=float, default=24.0, help="preview duration seconds")
    parser.add_argument("--out", default="bgm_preview.m4a")
    args = parser.parse_args()

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("未找到 ffmpeg。请先安装 ffmpeg，并确认 ffmpeg -version 可运行。")

    source = Path(args.audio).expanduser().resolve()
    if not source.is_file():
        raise SystemExit(f"音频文件不存在：{source}")
    if args.start < 0 or args.duration <= 0:
        raise SystemExit("--start 必须 >=0，--duration 必须 >0")

    out = Path(args.out).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        ffmpeg,
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-ss",
        str(args.start),
        "-i",
        str(source),
        "-t",
        str(args.duration),
        "-vn",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        str(out),
    ]
    subprocess.run(cmd, check=True)
    result = {
        "source": str(source),
        "start_sec": args.start,
        "duration_sec": args.duration,
        "preview": str(out),
        "bytes": out.stat().st_size,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
