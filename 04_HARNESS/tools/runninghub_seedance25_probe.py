#!/usr/bin/env python3
"""Minimal direct Seedance 2.5 probe via RunningHub public API.

Security boundary:
- reads RUNNINGHUB_API_KEY from environment only;
- never writes credentials to disk or GitHub;
- designed for one user-owned account/key;
- no account rotation, quota bypass or cookie/session automation.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError as exc:
    raise SystemExit("Missing dependency: pip install requests") from exc

BASE = "https://www.runninghub.ai"
UPLOAD = f"{BASE}/openapi/v2/media/upload/binary"
CREATE = f"{BASE}/openapi/v2/bytedance/seedance-2.5-global-token/multimodal-video"
QUERY = f"{BASE}/openapi/v2/query"


def auth_headers(api_key: str, json_content: bool = False) -> dict[str, str]:
    h = {"Authorization": f"Bearer {api_key}"}
    if json_content:
        h["Content-Type"] = "application/json"
    return h


def upload_image(api_key: str, image: Path) -> str:
    with image.open("rb") as fh:
        r = requests.post(
            UPLOAD,
            headers=auth_headers(api_key),
            files={"file": (image.name, fh)},
            timeout=120,
        )
    r.raise_for_status()
    data = r.json()
    if data.get("code") not in (0, "0"):
        raise RuntimeError(f"upload failed: {data}")
    payload = data.get("data") or {}
    url = payload.get("download_url") or payload.get("url")
    if not url:
        raise RuntimeError(f"upload response missing download_url: {data}")
    return str(url)


def create_task(
    api_key: str,
    *,
    prompt: str,
    image_url: str,
    duration: int,
    ratio: str,
    generate_audio: bool,
    seed: int,
) -> str:
    body: dict[str, Any] = {
        "prompt": prompt,
        "resolution": "720p",
        "duration": str(duration),
        "imageUrls": [image_url],
        "videoUrls": [],
        "audioUrls": [],
        "generateAudio": generate_audio,
        "ratio": ratio,
        "realPersonMode": False,
        "conversionSlots": [],
        "returnLastFrame": False,
        "bitrateMode": "standard",
        "seed": seed,
        "outputFormat": "mp4",
        "omniReferenceTaskType": "reference",
    }
    r = requests.post(
        CREATE,
        headers=auth_headers(api_key, json_content=True),
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        timeout=120,
    )
    r.raise_for_status()
    data = r.json()
    task_id = data.get("taskId") or data.get("task_id")
    if not task_id:
        raise RuntimeError(f"create response missing taskId: {data}")
    print(json.dumps({"create_response": data}, ensure_ascii=False, indent=2))
    return str(task_id)


def query_task(api_key: str, task_id: str) -> dict[str, Any]:
    r = requests.post(
        QUERY,
        headers=auth_headers(api_key, json_content=True),
        json={"taskId": task_id},
        timeout=120,
    )
    r.raise_for_status()
    return r.json()


def wait_for_result(api_key: str, task_id: str, timeout_s: int, poll_s: int) -> str:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        data = query_task(api_key, task_id)
        status = str(data.get("status") or "").upper()
        print(f"status={status or 'UNKNOWN'}")
        if status == "SUCCESS":
            for item in data.get("results") or []:
                if str(item.get("outputType") or "").lower() in {"mp4", "mov"} and item.get("url"):
                    return str(item["url"])
            raise RuntimeError(f"SUCCESS but no video URL: {data}")
        if status == "FAILED":
            raise RuntimeError(
                "task failed: "
                + json.dumps(
                    {
                        "errorCode": data.get("errorCode"),
                        "errorMessage": data.get("errorMessage"),
                        "failedReason": data.get("failedReason"),
                    },
                    ensure_ascii=False,
                )
            )
        time.sleep(poll_s)
    raise TimeoutError(f"task did not finish within {timeout_s}s: {task_id}")


def download(url: str, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=180) as r:
        r.raise_for_status()
        with output.open("wb") as fh:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    fh.write(chunk)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--image", required=True, type=Path)
    p.add_argument("--prompt-file", required=True, type=Path)
    p.add_argument("--duration", type=int, default=5, choices=list(range(4, 31)))
    p.add_argument("--ratio", default="9:16", choices=["adaptive", "16:9", "4:3", "1:1", "3:4", "9:16", "21:9"])
    p.add_argument("--audio", action="store_true", help="Enable model-generated audio")
    p.add_argument("--seed", type=int, default=-1)
    p.add_argument("--timeout", type=int, default=1200)
    p.add_argument("--poll", type=int, default=10)
    p.add_argument("--output", required=True, type=Path)
    args = p.parse_args()

    api_key = os.getenv("RUNNINGHUB_API_KEY", "").strip()
    if not api_key:
        print("RUNNINGHUB_API_KEY is not set", file=sys.stderr)
        return 2
    if not args.image.is_file():
        print(f"image not found: {args.image}", file=sys.stderr)
        return 2
    if not args.prompt_file.is_file():
        print(f"prompt file not found: {args.prompt_file}", file=sys.stderr)
        return 2

    prompt = args.prompt_file.read_text(encoding="utf-8").strip()
    if not prompt:
        print("prompt is empty", file=sys.stderr)
        return 2

    print("uploading image...")
    image_url = upload_image(api_key, args.image)
    print(f"uploaded={image_url}")

    print("creating Seedance 2.5 task...")
    task_id = create_task(
        api_key,
        prompt=prompt,
        image_url=image_url,
        duration=args.duration,
        ratio=args.ratio,
        generate_audio=args.audio,
        seed=args.seed,
    )
    print(f"task_id={task_id}")

    video_url = wait_for_result(api_key, task_id, args.timeout, args.poll)
    print(f"video_url={video_url}")
    download(video_url, args.output)
    print(f"saved={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
