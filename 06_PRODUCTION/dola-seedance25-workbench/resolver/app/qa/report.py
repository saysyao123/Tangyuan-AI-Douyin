from __future__ import annotations

from pathlib import Path
from typing import Any

from app.download.validator import validate_download
from app.logger import redact_url
from app.models import MediaCandidate, ResolveResult


def _candidate_report(candidate: MediaCandidate) -> dict[str, Any]:
    return candidate.public_dict(redacted_url=redact_url(candidate.url))


def make_report(
    result: ResolveResult,
    *,
    file_path: str | Path | None = None,
    ffprobe: dict[str, Any] | None = None,
) -> dict[str, Any]:
    report: dict[str, Any] = {
        "status": result.status,
        "vid": result.vid,
        "source_metadata": result.source_metadata,
        "candidates": [_candidate_report(candidate) for candidate in result.candidates],
        "selected": _candidate_report(result.selected) if result.selected else None,
        "security": {
            "url_tokens_redacted": True,
            "key_seed_emitted": False,
            "cookies_emitted": False,
            "reencoded": False,
        },
    }
    if file_path is not None:
        report["file"] = validate_download(file_path)
    if ffprobe is not None:
        report["ffprobe"] = ffprobe
        width = ffprobe.get("width")
        height = ffprobe.get("height")
        report["quality_claim"] = {
            "native_resolution": f"{width}x{height}" if width and height else None,
            "upscaled": False,
            "basis": "ffprobe",
        }
    return report
