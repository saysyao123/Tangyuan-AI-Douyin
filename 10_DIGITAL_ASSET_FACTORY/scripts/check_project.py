#!/usr/bin/env python3
"""Check shared-project continuity. Does not verify business or financial evidence."""
import json
import re
from pathlib import Path

PROJECT_ID = "AI_DIGITAL_ASSET_FACTORY"
REQUIRED_DOCS = (
    "START_HERE.md", "PROJECT_CONTRACT.md", "PROJECT_STATE.json", "AGENTS.md",
    "ASSET_REGISTRY.md", "DECISIONS.md", "DESIGN_QUALITY_GATE.md",
    "research/CYCLE06_PLATFORM_RULES_AUDIT.md",
    "research/CYCLE06_OPEN_SOURCE_REVIEW.md", "CYCLE06_EXECUTION_RECEIPT.md",
    "third_party/qiaomu-design-MIT.txt",
)
STATUSES = {"PASS", "UNKNOWN", "BLOCKED"}


def local_path(root, value):
    """Resolve only repository-relative public evidence paths."""
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ValueError("evidence path must be relative")
    target = (root / value).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError("evidence path leaves project root")
    return target


def validate_state(root, state):
    errors = []
    expected = {
        "project_id": PROJECT_ID,
        "repository": "saysyao123/Tangyuan-AI-Douyin",
        "branch": "main",
        "project_root": "10_DIGITAL_ASSET_FACTORY/",
        "mode_policy": "one_project_shared_by_web_codex_work",
    }
    for key, value in expected.items():
        if state.get(key) != value:
            errors.append(f"{key}: unexpected project identity or mode fork")
    if type(state.get("revision")) is not int or state["revision"] < 1:
        errors.append("revision must be a positive integer")
    stages = state.get("stages", {})
    if set(stages) != {f"R{i}" for i in range(6)}:
        errors.append("all six R0-R5 stages must be present")
    for name, stage in stages.items():
        if stage.get("status") not in STATUSES or not stage.get("scope"):
            errors.append(f"{name}: status and scope are required")
        if not stage.get("evidence"):
            errors.append(f"{name}: evidence or blocker report is required")
        for item in stage.get("evidence", []):
            try:
                if not local_path(root, item.get("path")).is_file():
                    errors.append(f"{name}: missing evidence file")
            except (ValueError, TypeError):
                errors.append(f"{name}: unsafe evidence path")
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", item.get("checked_on", "")):
                errors.append(f"{name}: evidence check date is required")
    if not state.get("next_task", {}).get("id") or not state.get("next_task", {}).get("action"):
        errors.append("one named next task is required")
    if state.get("new_cash_spent") != 0:
        errors.append("new cash violates current zero-spend contract; record an authorized contract change first")
    for candidate in state.get("platform_candidates", []):
        if candidate.get("decision") == "approved_for_full_production":
            if any(stages.get(name, {}).get("status") != "PASS" for name in ("R1", "R2")):
                errors.append(f"{candidate.get('id')}: production approval requires platform and demand stages to pass")
            fields = (
                "public_ai_admission", "public_nonexclusive_sales_mechanism",
                "personal_paid_upload_permission", "buyer_intended_use_license",
                "final_personal_payout",
            )
            if any(candidate.get(field) != "PASS" for field in fields):
                errors.append(f"{candidate.get('id')}: production approval skips an unknown or blocked gate")
    if state.get("full_viable_channel_found"):
        if not any(p.get("decision") == "approved_for_full_production"
                   for p in state.get("platform_candidates", [])):
            errors.append("viable-channel claim requires a fully gated candidate")
    amounts = state.get("verified_net_revenue", {})
    if not amounts or any(type(v) not in (int, float) or v < 0 for v in amounts.values()):
        errors.append("verified revenue must contain nonnegative numeric evidence totals")
    if any(type(v) in (int, float) and v > 0 for v in amounts.values()):
        if stages.get("R5", {}).get("status") != "PASS" or not state.get("revenue_verification_summary"):
            errors.append("positive verified revenue requires R5 PASS and a sanitized verification summary")
    return errors


def check(root):
    errors = []
    for name in REQUIRED_DOCS:
        if not (root / name).is_file():
            errors.append(f"missing required file: {name}")
    if not (root / "PROJECT_STATE.json").is_file():
        return errors
    try:
        state = json.loads((root / "PROJECT_STATE.json").read_text())
    except (ValueError, OSError) as exc:
        return errors + [f"invalid PROJECT_STATE.json: {type(exc).__name__}"]
    errors.extend(validate_state(root, state))
    for name in REQUIRED_DOCS:
        source = root / name
        if not source.is_file():
            continue
        content = source.read_text()
        if re.search(r"libfile_[0-9a-f]+|0x[0-9a-fA-F]{40}\b|BEGIN [A-Z ]*PRIVATE KEY", content):
            errors.append(f"{name}: possible private locator, wallet or secret in public material")
        if source.suffix != ".md":
            continue
        for dest in re.findall(r"\]\(([^)]+)\)", content):
            dest = dest.split("#", 1)[0]
            if not dest or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", dest):
                continue
            try:
                rel = (source.parent / dest).resolve().relative_to(root.resolve())
                if not local_path(root, str(rel)).is_file():
                    errors.append(f"{name}: broken local link {dest}")
            except ValueError:
                errors.append(f"{name}: local link leaves project root")
    return errors


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    errors = check(root)
    print(json.dumps({
        "status": "FAIL" if errors else "PASS",
        "checks": "project identity, scoped links, evidence references and unsupported claims",
        "errors": errors,
        "limits": "Not verification of platform policies, licenses, visual quality, transactions or payouts.",
    }, ensure_ascii=False, indent=2))
    raise SystemExit(1 if errors else 0)
