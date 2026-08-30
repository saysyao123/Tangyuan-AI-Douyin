from __future__ import annotations

import json
from pathlib import Path

from app.resolver.candidates import discover_candidates
from app.resolver.fallback_api import build_unwatermarked_url
from app.resolver.resolver import resolve_metadata


ROOT = Path(__file__).parents[1]


def load_fixture(name: str) -> dict:
    return json.loads((ROOT / "fixtures" / name).read_text(encoding="utf-8"))


def test_fallback_fixture_discovers_and_ranks_clean_original() -> None:
    metadata = load_fixture("fallback_api_sample.json")
    candidates = discover_candidates(metadata)
    assert len(candidates) == 4
    result = resolve_metadata(metadata)
    assert result.status == "success"
    assert result.selected is not None
    assert result.selected.is_unwatermarked is True
    assert result.selected.is_original is True
    assert (result.selected.width, result.selected.height) == (1920, 1080)
    assert result.selected.source == "fallback_api"


def test_watermark_evidence_cannot_be_outvoted_by_bitrate() -> None:
    metadata = {
        "video_list": [
            {"url": "https://cdn.example.test/high.mp4?lr=video_gen_watermark_dyn", "width": 3840, "height": 2160, "bitrate": 99999999},
            {"url": "https://cdn.example.test/clean.mp4?lr=video_gen_no_watermark", "width": 1280, "height": 720, "bitrate": 1000000},
        ]
    }
    result = resolve_metadata(metadata)
    assert result.selected is not None
    assert result.selected.url.endswith("clean.mp4?lr=video_gen_no_watermark")


def test_fallback_url_contract() -> None:
    built = build_unwatermarked_url("https://api.example.test/x?vid=abc&channel=yes")
    assert "channel=no" in built
    assert "codec_type=8" in built
    assert "logo_type=unwatermarked" in built
