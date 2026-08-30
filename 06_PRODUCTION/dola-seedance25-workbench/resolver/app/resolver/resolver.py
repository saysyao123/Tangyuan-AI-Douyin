from __future__ import annotations

from typing import Any

from app.config import FALLBACK_API_KEYS
from app.discovery.metadata_scan import scan_metadata
from app.models import MediaCandidate, ResolveResult
from app.resolver.candidates import discover_candidates, merge_candidates
from app.resolver.fallback_api import fetch_fallback_metadata, parse_fallback_candidates


def _rank_key(candidate: MediaCandidate) -> tuple[int, int, int, int, int]:
    """Prefer clean/original media, then native-looking quality signals."""
    codec_score = {"h264": 2, "h265": 1}.get(candidate.codec or "", 0)
    return (
        int(candidate.is_unwatermarked),
        int(candidate.is_original),
        candidate.pixel_area,
        candidate.effective_bitrate,
        codec_score,
    )


def rank_candidates(candidates: list[MediaCandidate]) -> list[MediaCandidate]:
    return sorted(candidates, key=_rank_key, reverse=True)


def resolve_metadata(metadata: Any, *, fetch_fallback: bool = False) -> ResolveResult:
    scan = scan_metadata(metadata)
    candidates = discover_candidates(metadata)
    fetched_groups: list[list[MediaCandidate]] = []
    if fetch_fallback:
        for fallback_api in scan.fallback_apis:
            try:
                payload = fetch_fallback_metadata(fallback_api)
                fetched_groups.append(parse_fallback_candidates(payload))
            except Exception:
                # A 403 or malformed fallback response is evidence that the
                # candidate is not currently usable, not a reason to bypass it.
                continue

    candidates = merge_candidates(candidates, *fetched_groups)
    ranked = rank_candidates(candidates)
    clean = [candidate for candidate in ranked if candidate.is_unwatermarked]
    selected = clean[0] if clean else (ranked[0] if ranked else None)
    if selected is None:
        status = "no_candidates"
    elif selected.is_unwatermarked:
        status = "success"
    else:
        status = "clean_source_not_available"

    video_ids = scan.vids
    source_metadata = {
        "candidate_count": len(ranked),
        "clean_candidate_count": len(clean),
        "fallback_api_count": len(scan.fallback_apis),
        "fetched_fallback_count": len(fetched_groups),
        "key_seed_present": bool(scan.key_seeds),
        "video_model_count": len(scan.video_models),
        "video_list_count": len(scan.video_lists),
    }
    return ResolveResult(
        vid=video_ids[0] if video_ids else None,
        candidates=ranked,
        selected=selected,
        source_metadata=source_metadata,
        status=status,
    )
