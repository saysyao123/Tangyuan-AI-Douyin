from __future__ import annotations

from typing import Any


def _number(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _integer(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def evaluate_5s_gate(
    ffprobe: dict[str, Any],
    *,
    visible_watermark: str,
    duration_min: float = 4.0,
    duration_max: float = 6.5,
    minimum_width: int = 1280,
    minimum_height: int = 720,
) -> dict[str, Any]:
    duration = _number(ffprobe.get("duration"))
    width = _integer(ffprobe.get("width"))
    height = _integer(ffprobe.get("height"))
    duration_pass = duration is not None and duration_min <= duration <= duration_max
    resolution_pass = width is not None and height is not None and width >= minimum_width and height >= minimum_height
    watermark_pass = visible_watermark.strip().upper() == "NO"
    failures: list[str] = []
    if not duration_pass:
        failures.append("FAIL_DURATION")
    if not resolution_pass:
        failures.append("FAIL_RESOLUTION")
    if not watermark_pass:
        failures.append("FAIL_WATERMARK_QA")
    return {
        "target_duration": 5.0,
        "duration": duration,
        "duration_gate": "PASS" if duration_pass else "FAIL",
        "resolution": f"{width}x{height}" if width and height else "UNKNOWN",
        "resolution_gate": "PASS" if resolution_pass else "FAIL",
        "visible_watermark": visible_watermark.upper(),
        "watermark_gate": "PASS" if watermark_pass else "FAIL",
        "status": "PASS" if not failures else "FAIL",
        "failure_codes": failures,
        "basis": "ffprobe + human_visual_review",
    }
