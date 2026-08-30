from __future__ import annotations

import functools
import http.server
import json
import shutil
import subprocess
import sys
import threading
from pathlib import Path

import pytest


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return


def test_cli_download_runs_full_local_acceptance_path(tmp_path: Path) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        pytest.skip("ffmpeg is not available")
    source = tmp_path / "source.mp4"
    subprocess.run(
        [ffmpeg, "-y", "-f", "lavfi", "-i", "color=c=blue:s=16x16:d=0.2", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(source)],
        capture_output=True,
        check=True,
    )
    payload = source.read_bytes()
    metadata = {
        "vid": "v186a3gm000cda9gbpfog65jfpbu9q50",
        "video_list": [
            {
                "main_url": "PLACEHOLDER",
                "logo_type": "unwatermarked",
                "original": True,
                "width": 16,
                "height": 16,
                "codec_type": "h264",
            }
        ],
    }
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(QuietHandler, directory=str(tmp_path)))
    metadata["video_list"][0]["main_url"] = f"http://127.0.0.1:{server.server_port}/source.mp4?lr=unwatermarked"
    metadata_path = tmp_path / "response.json"
    metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
    output_path = tmp_path / "output" / "cli.mp4"
    report_path = tmp_path / "output" / "cli.report.json"
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "app.cli",
                "download",
                "--metadata",
                str(metadata_path),
                "--output",
                str(output_path),
                "--report",
                str(report_path),
            ],
            cwd=Path(__file__).parents[1],
            capture_output=True,
            text=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stdout + completed.stderr
        report = json.loads(completed.stdout)
        assert report["status"] == "success"
        assert report["file"]["ftyp_valid"] is True
        assert output_path.read_bytes() == payload
        assert report_path.exists()
    finally:
        server.shutdown()
        thread.join(timeout=5)
