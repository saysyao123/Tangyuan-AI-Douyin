#!/usr/bin/env python3
"""Zero-context startup/resume controller for canonical MV Runtime.

The controller is deliberately read-only. It turns repository truth into one
machine-readable startup decision:
- RESUME_CANONICAL
- MIGRATION_REQUIRED
- ALLOCATE_NEW_SLOT

It never advances a stage, never records a Human Gate and never mutates the
Tracker. Invalid or ambiguous repository state blocks startup instead of being
resolved from chat memory.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any

import mv_asset_manifest as assetctl
import mv_runtime_revision as revisionctl
import mv_runtime_state as statectl

SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[2]
RUNTIME_DIR = SCRIPT_PATH.parent.parent / "runtime"
CONTRACT_NAME = "mv_resume_contract.json"


def emit(payload: dict[str, Any], code: int = 0) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(code)


def fail(message: str, details: Any = None, code: int = 1) -> None:
    payload: dict[str, Any] = {"ok": False, "error": message}
    if details is not None:
        payload["details"] = details
    emit(payload, code)


def load_contract(registry_dir: Path) -> dict[str, Any]:
    return statectl.load_json(registry_dir / CONTRACT_NAME)


def resolve_repo_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    return path.resolve() if path.is_absolute() else (repo_root / path).resolve()


def relative_to_repo(repo_root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        return str(path.resolve())


def read_tracker(path: Path, contract: dict[str, Any]) -> tuple[list[str], list[dict[str, str]], dict[str, dict[str, str]]]:
    if not path.is_file():
        fail("tracker file missing", str(path))
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = [{key: (value or "") for key, value in row.items()} for row in reader]
    except (OSError, UnicodeDecodeError, csv.Error) as exc:
        fail("tracker is unreadable", {"path": str(path), "error": str(exc)})
    missing = [key for key in contract.get("tracker_required_columns") or [] if key not in fieldnames]
    if missing:
        fail("tracker missing required columns", missing)
    by_slot: dict[str, dict[str, str]] = {}
    duplicates: list[str] = []
    for row in rows:
        slot_id = row.get("slot_id", "").strip()
        if not slot_id:
            fail("tracker contains blank slot_id")
        if slot_id in by_slot:
            duplicates.append(slot_id)
        by_slot[slot_id] = row
    if duplicates:
        fail("tracker slot_id must be unique", sorted(set(duplicates)))
    return fieldnames, rows, by_slot


def validate_resume_contract(repo_root: Path, runtime: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    stages = statectl.stages(runtime)
    stage_ids = [item["id"] for item in stages]
    actions = contract.get("stage_actions") or {}
    errors: list[str] = []
    warnings: list[str] = []
    if set(actions) != set(stage_ids):
        missing = sorted(set(stage_ids) - set(actions))
        extra = sorted(set(actions) - set(stage_ids))
        if missing:
            errors.append("resume contract missing stage actions: " + ", ".join(missing))
        if extra:
            errors.append("resume contract has unknown stage actions: " + ", ".join(extra))
    for index, stage in enumerate(stages):
        stage_id = stage["id"]
        action = actions.get(stage_id) or {}
        expected_next = None if index == len(stages) - 1 else stages[index + 1]["id"]
        if action.get("next_stage") != expected_next:
            errors.append(f"{stage_id}: next_stage must be {expected_next!r}")
        expected_gate = None
        if expected_next is not None:
            expected_gate = stages[index + 1].get("human_gate")
        if action.get("human_gate") != expected_gate:
            errors.append(f"{stage_id}: human_gate must match immediate next stage ({expected_gate!r})")
        if not isinstance(action.get("action_id"), str) or not action.get("action_id", "").strip():
            errors.append(f"{stage_id}: action_id missing")
        if not isinstance(action.get("summary"), str) or not action.get("summary", "").strip():
            errors.append(f"{stage_id}: summary missing")
        for rel in action.get("jit_reads") or []:
            if not (repo_root / rel).is_file():
                errors.append(f"{stage_id}: JIT read path missing: {rel}")
    for rel in contract.get("startup_required_reads") or []:
        if not (repo_root / rel).is_file():
            errors.append(f"startup required read path missing: {rel}")
    allocation = contract.get("allocation") or {}
    if allocation.get("human_gate") != "HG01":
        errors.append("allocation must stop at HG01")
    for rel in allocation.get("jit_reads") or []:
        if not (repo_root / rel).is_file():
            errors.append(f"allocation JIT read path missing: {rel}")
    return {"ok": not errors, "errors": errors, "warnings": warnings, "stage_count": len(stages)}


def stage_range(runtime: dict[str, Any], contract: dict[str, Any]) -> tuple[set[str], set[str], set[str]]:
    stages = statectl.stages(runtime)
    indexes = {item["id"]: index for index, item in enumerate(stages)}
    bounds = contract["production_stage_range"]
    start = indexes[bounds["from"]]
    end = indexes[bounds["through"]]
    production = {item["id"] for item in stages[start : end + 1]}
    post_publish = set(contract.get("post_publish_active_stages") or [])
    terminal = set(contract.get("terminal_stages") or [])
    return production, post_publish, terminal


def parse_slot_identity(slot_id: str) -> tuple[str | None, str | None]:
    match = re.fullmatch(r"D(\d+)-([A-Za-z])", slot_id)
    if match is None:
        return None, None
    return str(int(match.group(1))), match.group(2).upper()


def tracker_projection(row: dict[str, str]) -> dict[str, str]:
    keys = ("slot_id", "day", "slot", "lane", "song_family", "audio_asset", "status", "packaging", "publish_time")
    return {key: row.get(key, "") for key in keys}


def validate_tracker_slot_consistency(
    slot_root: Path,
    state: dict[str, Any],
    row: dict[str, str],
    contract: dict[str, Any],
    production: set[str],
    post_publish: set[str],
    terminal: set[str],
) -> list[str]:
    errors: list[str] = []
    slot_id = state["slot_id"]
    if slot_root.name != slot_id:
        errors.append(f"slot directory {slot_root.name!r} does not equal state slot_id {slot_id!r}")
    if row.get("slot_id", "").strip() != slot_id:
        errors.append("tracker slot_id disagrees with canonical state")
    if row.get("lane", "").strip() != str(state.get("lane", "")):
        errors.append("tracker lane disagrees with canonical state")
    expected_day, expected_slot = parse_slot_identity(slot_id)
    if expected_day is not None and row.get("day", "").strip() != expected_day:
        errors.append("tracker day disagrees with slot_id")
    if expected_slot is not None and row.get("slot", "").strip().upper() != expected_slot:
        errors.append("tracker slot letter disagrees with slot_id")
    current = state["current_stage"]
    tracker_status = row.get("status", "").strip()
    published = contract["tracker_published_status"]
    if current in post_publish or current in terminal:
        if tracker_status != published:
            errors.append("published/post-publish canonical state requires tracker status PUBLISHED")
    elif current in production:
        if tracker_status == published:
            errors.append("pre-publish canonical state cannot have tracker status PUBLISHED")
    else:
        errors.append("canonical state is outside registered resume stage classes")
    return errors


def discover_canonical_slots(program_root: Path, runtime: dict[str, Any], contract: dict[str, Any], tracker_by_slot: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    production, post_publish, terminal = stage_range(runtime, contract)
    asset_contract, asset_stage_registry = assetctl.load_runtime(RUNTIME_DIR)
    revision_contract = revisionctl.load_contract(RUNTIME_DIR)
    discovered: list[dict[str, Any]] = []
    state_rel = Path(contract["canonical_state_relative_path"])
    pattern = f"*/{state_rel.as_posix()}"
    for state_path in sorted(program_root.glob(pattern)) if program_root.is_dir() else []:
        slot_root = state_path.parent.parent
        state = statectl.load_canonical_state(slot_root, runtime)
        slot_id = state["slot_id"]
        if slot_id not in tracker_by_slot:
            fail("canonical slot has no tracker row", {"slot_id": slot_id, "slot_root": str(slot_root)})
        state_report = statectl.verify_state_internal(slot_root, runtime)
        revision_report = revisionctl.validate_revision_chain_internal(slot_root, runtime, revision_contract)
        if not revision_report.get("ok"):
            fail("canonical slot revision history is invalid", revision_report)
        asset_report = assetctl.verify_all_internal(slot_root, asset_contract, asset_stage_registry)
        if not asset_report.get("ok"):
            fail("canonical slot media asset identity is invalid", {"slot_id": slot_id, "asset_report": asset_report})
        row = tracker_by_slot[slot_id]
        consistency_errors = validate_tracker_slot_consistency(slot_root, state, row, contract, production, post_publish, terminal)
        if consistency_errors:
            fail("tracker/canonical slot consistency check failed", {"slot_id": slot_id, "errors": consistency_errors})
        current = state["current_stage"]
        if current in production:
            stage_class = "production"
        elif current in post_publish:
            stage_class = "post_publish"
        else:
            stage_class = "terminal"
        discovered.append({
            "slot_id": slot_id,
            "slot_root": slot_root,
            "state": state,
            "state_report": state_report,
            "revision_report": revision_report,
            "asset_report": asset_report,
            "tracker_row": row,
            "stage_class": stage_class,
        })
    return discovered


def discover_legacy_prepublish_slots(program_root: Path, tracker_by_slot: dict[str, dict[str, str]], contract: dict[str, Any], canonical_slot_ids: set[str]) -> list[dict[str, str]]:
    values: list[dict[str, str]] = []
    published = contract["tracker_published_status"]
    if not program_root.is_dir():
        return values
    for path in sorted(program_root.glob("*/CURRENT_STATE.json")):
        slot_root = path.parent
        slot_id = slot_root.name
        if slot_id in canonical_slot_ids or slot_id not in tracker_by_slot:
            continue
        row = tracker_by_slot[slot_id]
        if row.get("status", "").strip() == published:
            continue
        values.append({"slot_id": slot_id, "slot_root": str(slot_root), "legacy_state": str(path)})
    return values


def allocation_candidate(rows: list[dict[str, str]], contract: dict[str, Any], unavailable: set[str]) -> dict[str, str] | None:
    allowed = set(contract.get("tracker_allocation_statuses") or [])
    for row in rows:
        slot_id = row.get("slot_id", "").strip()
        if slot_id in unavailable:
            continue
        if row.get("status", "").strip() not in allowed:
            continue
        if row.get("song_family", "").strip() or row.get("audio_asset", "").strip():
            continue
        return row
    return None


def resume_packet(slot: dict[str, Any], contract: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    state = slot["state"]
    current = state["current_stage"]
    action = contract["stage_actions"][current]
    revision_sequence = int(state.get("revision_sequence", 0) or 0)
    return {
        "ok": True,
        "mode": "RESUME_CANONICAL",
        "slot_id": state["slot_id"],
        "slot_root": relative_to_repo(repo_root, slot["slot_root"]),
        "lane": state["lane"],
        "current_stage": current,
        "current_state_token": state["current_state_token"],
        "active_attempt": revision_sequence + 1,
        "revision_sequence": revision_sequence,
        "last_revision_receipt": state.get("last_revision_receipt"),
        "context": state.get("context"),
        "tracker_row": tracker_projection(slot["tracker_row"]),
        "asset_record_count": slot["asset_report"].get("record_count", 0),
        "next_action": action,
        "startup_required_reads": contract.get("startup_required_reads") or [],
        "jit_reads": action.get("jit_reads") or [],
        "verification": {
            "state": True,
            "revision_history": True,
            "asset_identity": True,
            "tracker_consistency": True,
        },
    }


def migration_packet(legacy: dict[str, str], tracker_row: dict[str, str], contract: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    return {
        "ok": True,
        "mode": "MIGRATION_REQUIRED",
        "blocked_for_production": True,
        "slot_id": legacy["slot_id"],
        "slot_root": relative_to_repo(repo_root, Path(legacy["slot_root"])),
        "tracker_row": tracker_projection(tracker_row),
        "reason": "A pre-publish legacy root-level CURRENT_STATE exists, but canonical_v2 nested state does not. Do not infer progress from chat memory and do not allocate over this directory.",
        "next_action": {
            "action_id": "PLAN_CONTROLLED_LEGACY_MIGRATION",
            "summary": "Audit legacy evidence with mv_runtime_migrate.py and migrate explicitly before canonical resume.",
            "human_gate": null,
            "jit_reads": ["04_HARNESS/runtime/MV_RUNTIME_V2_MIGRATION_PLAN.md"]
        },
        "startup_required_reads": contract.get("startup_required_reads") or [],
    }


def allocation_packet(row: dict[str, str], contract: dict[str, Any], repo_root: Path, program_root: Path) -> dict[str, Any]:
    slot_id = row["slot_id"].strip()
    slot_root = program_root / slot_id
    return {
        "ok": True,
        "mode": "ALLOCATE_NEW_SLOT",
        "slot_id": slot_id,
        "slot_root": relative_to_repo(repo_root, slot_root),
        "lane": row.get("lane", "").strip(),
        "tracker_row": tracker_projection(row),
        "next_action": contract["allocation"],
        "startup_required_reads": contract.get("startup_required_reads") or [],
        "jit_reads": contract["allocation"].get("jit_reads") or [],
        "init_command": f"python 04_HARNESS/tools/mv_runtime_state.py init-slot --slot-root {relative_to_repo(repo_root, slot_root)} --slot-id {slot_id} --program 30D_60 --lane {row.get('lane','').strip()}",
    }


def startup(args: argparse.Namespace, runtime: dict[str, Any], contract: dict[str, Any]) -> None:
    repo_root = args.repo_root.resolve()
    program_root = resolve_repo_path(repo_root, args.program_root or contract["program_root"])
    tracker_path = resolve_repo_path(repo_root, args.tracker or contract["tracker_path"])
    contract_report = validate_resume_contract(repo_root, runtime, contract)
    if not contract_report["ok"]:
        fail("resume contract validation failed", contract_report)
    _, rows, tracker_by_slot = read_tracker(tracker_path, contract)
    canonical = discover_canonical_slots(program_root, runtime, contract, tracker_by_slot)
    canonical_by_id = {item["slot_id"]: item for item in canonical}
    legacy = discover_legacy_prepublish_slots(program_root, tracker_by_slot, contract, set(canonical_by_id))
    legacy_by_id = {item["slot_id"]: item for item in legacy}
    post_publish = [item["slot_id"] for item in canonical if item["stage_class"] == "post_publish"]
    terminal = [item["slot_id"] for item in canonical if item["stage_class"] == "terminal"]

    if args.slot_id:
        if args.slot_id not in tracker_by_slot:
            fail("requested slot_id is absent from tracker", args.slot_id)
        if args.slot_id in canonical_by_id:
            packet = resume_packet(canonical_by_id[args.slot_id], contract, repo_root)
        elif args.slot_id in legacy_by_id:
            packet = migration_packet(legacy_by_id[args.slot_id], tracker_by_slot[args.slot_id], contract, repo_root)
        else:
            candidate = allocation_candidate([tracker_by_slot[args.slot_id]], contract, set())
            if candidate is None:
                fail("requested slot is neither canonical-resumable nor eligible for fresh allocation", tracker_projection(tracker_by_slot[args.slot_id]))
            packet = allocation_packet(candidate, contract, repo_root, program_root)
    else:
        production_slots = [item for item in canonical if item["stage_class"] == "production"]
        if len(production_slots) > 1:
            fail("multiple pre-publish canonical slots are active; explicit --slot-id is required", [item["slot_id"] for item in production_slots])
        if len(production_slots) == 1:
            packet = resume_packet(production_slots[0], contract, repo_root)
        elif legacy:
            if len(legacy) > 1:
                fail("multiple pre-publish legacy slots require migration; explicit --slot-id is required", [item["slot_id"] for item in legacy])
            packet = migration_packet(legacy[0], tracker_by_slot[legacy[0]["slot_id"]], contract, repo_root)
        else:
            unavailable = set(canonical_by_id) | set(legacy_by_id)
            candidate = allocation_candidate(rows, contract, unavailable)
            if candidate is None:
                fail("no resumable canonical slot and no eligible tracker row for allocation")
            packet = allocation_packet(candidate, contract, repo_root, program_root)

    packet["program_root"] = relative_to_repo(repo_root, program_root)
    packet["tracker"] = relative_to_repo(repo_root, tracker_path)
    packet["post_publish_slots"] = post_publish
    packet["terminal_slots"] = terminal
    packet["contract_validation"] = contract_report
    emit(packet)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Read-only zero-context startup controller for canonical MV Runtime.")
    p.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    p.add_argument("--registry-dir", type=Path, default=RUNTIME_DIR)
    p.add_argument("--program-root")
    p.add_argument("--tracker")
    p.add_argument("--slot-id")
    return p


def main() -> None:
    args = parser().parse_args()
    runtime = statectl.load_runtime(args.registry_dir.resolve())
    contract = load_contract(args.registry_dir.resolve())
    startup(args, runtime, contract)


if __name__ == "__main__":
    main()
