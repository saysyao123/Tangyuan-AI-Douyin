"""Deterministic S0 vNext evaluator. Standard-library only."""
from __future__ import annotations

from copy import deepcopy

CORE_LANES = {"PRIMARY_CORE", "VERIFIED_CORE", "HISTORICAL_CORE_VERIFIED", "HISTORICAL_VERIFIED_CORE", "CURRENT_CORE_DIRECT"}
REVIEWABLE = {"PLAYABLE_PUBLIC_REFERENCE", "USER_PROVIDED_REFERENCE", "VERIFIED_REFERENCE_MEDIA"}
FORBIDDEN_KEYS = {"exact_source_hash", "full_song_timeline", "production_segment", "locked_final_audio", "segment_start", "segment_end"}


def _contains_forbidden(value):
    if isinstance(value, dict):
        return bool(FORBIDDEN_KEYS.intersection(value)) or any(_contains_forbidden(v) for v in value.values())
    if isinstance(value, list):
        return any(_contains_forbidden(v) for v in value)
    return False


def evaluate_s0(payload):
    data = deepcopy(payload)
    errors, warnings, identity_pending, eligible, ready = [], [], [], [], []
    if _contains_forbidden(data):
        errors.append("S0_BOUNDARY_LEAKAGE")

    seen = set()
    for raw in data.get("candidates", []):
        item = deepcopy(raw)
        family = str(item.get("song_family", "")).strip()
        reasons = []
        if not family:
            reasons.append("MISSING_SONG_FAMILY")
        if family in seen:
            reasons.append("DUPLICATE_SONG_FAMILY")
        seen.add(family)
        if item.get("language_evidence") != "CHINESE":
            reasons.append("CHINESE_LANGUAGE_EVIDENCE_REQUIRED")
        if item.get("song_family_identity_status", "RESOLVED") != "RESOLVED":
            reasons.append("SONG_FAMILY_IDENTITY_UNRESOLVED")
        if item.get("history_policy") not in {"ELIGIBLE", "NO_EXCLUSION_IN_CURRENT_LEDGER"}:
            reasons.append("HISTORY_EXCLUDED")
        lane = item.get("source_lane")
        if lane not in CORE_LANES:
            if lane == "SUPPLEMENTAL_TEST" and data.get("supplemental_enabled"):
                reasons.append("SUPPLEMENTAL_TEST_CANNOT_ENTER_PRODUCTION_CORE")
            else:
                reasons.append("NON_CORE_LANE")
        if not str(item.get("semantic_direction", "")).strip():
            reasons.append("SEMANTIC_DIRECTION_REQUIRED")
        item["direction_eligible"] = not reasons
        item["eligibility_reasons"] = reasons
        if reasons == ["SONG_FAMILY_IDENTITY_UNRESOLVED"]:
            identity_pending.append(item)
        if not item["direction_eligible"]:
            continue
        eligible.append(item)

    eligible = eligible[:3]
    if len(seen) > 3:
        warnings.append("MAX_THREE_DIRECTIONS_APPLIED")

    for item in eligible:
        ref = item.get("reference_review", {})
        ref_ready = bool(ref.get("identity_tied")) and bool(ref.get("user_reviewable")) and ref.get("access") in REVIEWABLE
        item["hg01_ready"] = ref_ready
        item["review_warnings"] = []
        if not ref_ready:
            item["review_warnings"].append("CURRENT_HUMAN_REVIEWABLE_REFERENCE_REQUIRED")
        if ref.get("access") == "HTML_SHELL_ONLY" or (ref.get("http_status") == 200 and not ref.get("user_reviewable")):
            item["review_warnings"].append("HTTP_PAGE_IS_NOT_REVIEWABLE_MEDIA")
        if ref.get("current_freshness") == "NOT_REFRESHED":
            item["review_warnings"].append("REFERENCE_NOT_REFRESHED")
        if ref_ready:
            ready.append(item)

    confirmation = data.get("human_confirmation", {})
    selected = confirmation.get("song_family")
    production_human_pass = (
        confirmation.get("status") == "PASS"
        and confirmation.get("actor") == "USER"
        and confirmation.get("mode") == "PRODUCTION"
        and any(x["song_family"] == selected for x in ready)
    )
    if errors:
        route = "INVALID"
    elif production_human_pass:
        route = "SEALED"
    elif ready:
        route = "READY_FOR_HG01"
    elif eligible:
        route = "REFERENCE_REFRESH_REQUIRED"
    elif identity_pending:
        route = "SONG_IDENTITY_REFRESH_REQUIRED"
    else:
        route = "SONG_POOL_REFRESH_REQUIRED"

    return {
        "validator": "FAIL" if errors else "PASS",
        "errors": errors,
        "warnings": warnings,
        "stage_route": route,
        "direction_candidates": [x["song_family"] for x in eligible],
        "identity_refresh_candidates": [x["song_family"] for x in identity_pending],
        "hg01_ready_candidates": [x["song_family"] for x in ready],
        "candidate_details": eligible,
        "selected_song_family": selected if production_human_pass else None,
        "human_gate": "PASS" if production_human_pass else "PENDING",
        "s0_sealed": production_human_pass,
        "s1_entry_allowed": production_human_pass,
        "s2_entry_allowed": False,
    }
