from __future__ import annotations

import functools
import http.server
import threading
from pathlib import Path

from app.download.authenticated import download_stream
from app.download.validator import validate_download
from app.qa.ffprobe import find_ffprobe, probe_media


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return


def test_stream_download_and_mp4_signature(tmp_path: Path) -> None:
    payload = b"\x00\x00\x00\x18ftypisom\x00\x00\x02\x00fixture-mp4"
    served = tmp_path / "source.mp4"
    served.write_bytes(payload)
    handler = functools.partial(QuietHandler, directory=str(tmp_path))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        destination = tmp_path / "nested" / "download.mp4"
        download_stream(f"http://127.0.0.1:{server.server_port}/source.mp4", destination)
        report = validate_download(destination)
        assert report["ftyp_valid"] is True
        assert destination.read_bytes() == payload
        assert not destination.with_name(destination.name + ".part").exists()
    finally:
        server.shutdown()
        thread.join(timeout=5)


def test_ffprobe_is_available_and_probes_existing_evidence() -> None:
    source = Path(r"LOCAL_DOLA_PROJECT_ROOT\outputs\seedance25-fight-30s-segment-01-0-15s-watermarked.mp4")
    if not source.exists() or not find_ffprobe():
        return
    result = probe_media(source)
    assert result["width"] == 720
    assert result["height"] == 1280
    assert result["duration"] is not None
