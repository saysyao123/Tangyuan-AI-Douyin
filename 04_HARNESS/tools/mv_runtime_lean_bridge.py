#!/usr/bin/env python3
"""Lean orchestration layer for the canonical MV Runtime.

This is NOT a second state authority. It delegates every mutation to the existing
canonical Runtime controllers while compressing external Web/GitHub round-trips.

Lean-only macros:
- ACCEPT_GATE: durable record-human-gate + internal fresh verification + advance.
- RUN_UNTIL_GATE_OR_BLOCK: repeatedly invokes canonical ADVANCE through already-
  valid machine stages, stopping before a Human Gate, at an external generation
  handoff, at Release Ready, or on a real validator BLOCK.

The macro never creates stage artifacts and never bypasses stage validators.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import mv_runtime_bridge as core
import mv_runtime_state as statectl

SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[2]
RUNTIME_DIR = SCRIPT_PATH.parent.parent / "runtime"
CONTRACT_NAME = "mv_lean_runtime_contract.json"
EXECUTOR_REGISTRY_NAME = "mv_stage_executor_registry.json"


class LeanFatal(RuntimeError):
    pass


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LeanFatal(f"invalid or missing JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise LeanFatal(f"JSON root must be object: {path}")
    return value


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve_repo_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    return path.resolve() if path.is_absolute() else (repo_root / path).resolve()


def rel_to_repo(repo_root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        return str(path.resolve())


def load_contract(registry_dir: Path) -> dict[str, Any]:
    return load_json(registry_dir / CONTRACT_NAME)


def load_executor_registry(registry_dir: Path) -> dict[str, Any]:
    return load_json(registry_dir / EXECUTOR_REGISTRY_NAME)


def validate_contract(contract: dict[str, Any]) -> None:
    commands = contract.get("commands")
    if not isinstance(commands, dict) or not commands:
        raise LeanFatal("lean contract commands must be a non-empty object")
    required = {"RESUME", "INIT_SLOT", "ACCEPT_GATE", "RUN_UNTIL_GATE_OR_BLOCK"}
    if not required.issubset(commands):
        raise LeanFatal(f"lean contract missing required commands: {sorted(required - set(commands))}")
    if not isinstance(contract.get("request_id_pattern"), str):
        raise LeanFatal("request_id_pattern missing")


def validate_request(path: Path, request: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    for key in contract.get("required_request_fields") or []:
        if key not in request:
            raise LeanFatal(f"request missing required field: {key}")
    if request.get("schema_version") != contract.get("schema_version"):
        raise LeanFatal("request schema_version does not match lean contract")
    request_id = request.get("request_id")
    if not isinstance(request_id, str) or re.fullmatch(contract["request_id_pattern"], request_id) is None:
        raise LeanFatal(f"invalid request_id: {request_id!r}")
    expected_name = contract["request_filename_template"].format(request_id=request_id)
    if path.name != expected_name:
        raise LeanFatal("request filename does not match request_id")
    command = request.get("command")
    definition = (contract.get("commands") or {}).get(command)
    if not isinstance(definition, dict):
        raise LeanFatal(f"command is not whitelisted: {command!r}")
    slot_id = request.get("slot_id")
    if definition.get("slot_id_required") and (not isinstance(slot_id, str) or not slot_id.strip()):
        raise LeanFatal(f"{command}: non-empty slot_id is required")
    if slot_id is not None and (not isinstance(slot_id, str) or re.fullmatch(r"^D[0-9]+-[A-Za-z]$", slot_id) is None):
        raise LeanFatal(f"invalid slot_id: {slot_id!r}")
    if request.get("requested_by") not in set(contract.get("allowed_requested_by") or []):
        raise LeanFatal("requested_by is not allowed")
    if not isinstance(request.get("reason"), str) or not request["reason"].strip():
        raise LeanFatal("request reason must be non-empty")
    payload = request.get("payload")
    if not isinstance(payload, dict):
        raise LeanFatal("request payload must be object")
    allowed = set(definition.get("payload_allowed") or [])
    extra = sorted(set(payload) - allowed)
    if extra:
        raise LeanFatal(f"{command}: forbidden payload keys: {extra}")
    missing = [key for key in definition.get("payload_required") or [] if key not in payload]
    if missing:
        raise LeanFatal(f"{command}: missing payload keys: {missing}")
    expected_guard = request.get("expected_guard")
    if definition.get("expected_guard_required"):
        if not isinstance(expected_guard, dict):
            raise LeanFatal(f"{command}: expected_guard is required")
        kind = definition.get("expected_guard_kind")
        if expected_guard.get("kind") != kind:
            raise LeanFatal(f"{command}: expected_guard.kind must be {kind}")
        fields_key = "canonical_guard_fields" if kind == "CANONICAL" else "allocation_guard_fields"
        fields = set(contract.get(fields_key) or [])
        if set(expected_guard) != fields:
            raise LeanFatal(f"{command}: expected_guard fields must exactly match {sorted(fields)}")
    elif expected_guard is not None:
        raise LeanFatal(f"{command}: expected_guard is not accepted")
    if command == "RUN_UNTIL_GATE_OR_BLOCK" and "max_steps" in payload:
        value = payload["max_steps"]
        max_allowed = int((contract.get("lean_policy") or {}).get("max_max_steps", 16))
        if not isinstance(value, int) or isinstance(value, bool) or value < 1 or value > max_allowed:
            raise LeanFatal(f"max_steps must be integer 1..{max_allowed}")
    return definition


def stage_items(registry_dir: Path) -> list[dict[str, Any]]:
    runtime = statectl.load_runtime(registry_dir.resolve())
    return statectl.stages(runtime)


def stage_index(stages: list[dict[str, Any]], stage_id: str) -> int:
    for i, item in enumerate(stages):
        if item.get("id") == stage_id:
            return i
    raise LeanFatal(f"current stage is absent from stage registry: {stage_id}")


def enrich_packet(packet: dict[str, Any], registry_dir: Path, contract: dict[str, Any]) -> dict[str, Any]:
    value = json.loads(json.dumps(packet, ensure_ascii=False))
    executors = (load_executor_registry(registry_dir).get("stage_executors") or {})
    if value.get("mode") == "RESUME_CANONICAL":
        stage_id = value.get("current_stage")
    elif value.get("mode") == "ALLOCATE_NEW_SLOT":
        stage_id = "S00_SLOT_CREATED"
    else:
        stage_id = None
    if isinstance(stage_id, str):
        executor = executors.get(stage_id)
        if isinstance(executor, dict):
            value["resolved_executor"] = executor
    value["lean_runtime"] = {
        "enabled": True,
        "macro_commands": ["ACCEPT_GATE", "RUN_UNTIL_GATE_OR_BLOCK"],
        "principle": "fine-grained canonical evidence, coarse-grained external execution",
        "external_handoff_stop_after_stages": (contract.get("lean_policy") or {}).get("external_handoff_stop_after_stages") or [],
    }
    return value


def execute_old_mutation(
    request: dict[str, Any],
    preflight: dict[str, Any],
    registry_dir: Path,
    program_root: Path,
    tracker: Path,
) -> dict[str, Any]:
    try:
        result = core.execute_mutation(request, preflight, registry_dir, program_root, tracker)
    except core.BridgeFatal as exc:
        raise LeanFatal(str(exc)) from exc
    return result


def execute_accept_gate(
    request: dict[str, Any],
    preflight: dict[str, Any],
    registry_dir: Path,
    program_root: Path,
) -> dict[str, Any]:
    if preflight.get("mode") != "RESUME_CANONICAL":
        raise LeanFatal("ACCEPT_GATE requires RESUME_CANONICAL preflight")
    slot_id = request["slot_id"]
    slot_root = program_root / slot_id
    core.compare_guard(request["expected_guard"], core.canonical_guard(slot_root, registry_dir))
    stages = stage_items(registry_dir)
    current = preflight.get("current_stage")
    index = stage_index(stages, str(current))
    if index + 1 >= len(stages):
        raise LeanFatal("terminal stage has no Human Gate to accept")
    next_item = stages[index + 1]
    expected_gate = next_item.get("human_gate")
    payload = request["payload"]
    gate = payload.get("gate")
    if expected_gate is None or gate != expected_gate:
        raise LeanFatal(f"ACCEPT_GATE gate mismatch: expected={expected_gate!r} supplied={gate!r}")
    text = payload.get("user_decision_text")
    approved = payload.get("approved_artifacts")
    if not isinstance(text, str) or not text.strip():
        raise LeanFatal("user_decision_text must be non-empty")
    if not isinstance(approved, list) or not approved or any(not isinstance(x, str) or not x.strip() for x in approved):
        raise LeanFatal("approved_artifacts must be a non-empty string array")

    record_args = [
        "record-human-gate", "--slot-root", str(slot_root), "--gate", str(gate),
        "--user-decision-text", text,
    ]
    for artifact in approved:
        record_args.extend(["--approved-artifact", artifact])
    code, record_payload, _stdout, stderr = core.run_json(core.tool_command(core.STATE_TOOL, registry_dir, *record_args))
    if code != 0 or record_payload.get("ok") is not True:
        return {
            "ok": False,
            "outcome": "GATE_RECORD_REJECTED",
            "record": core.controller_failure("RECORD_HUMAN_GATE", code, record_payload, stderr),
            "transitions_advanced": 0,
        }

    # Re-verify state/fingerprint inside the same serialized workflow before advance.
    fresh_guard = core.canonical_guard(slot_root, registry_dir)
    if fresh_guard.get("current_stage") != current:
        return {
            "ok": False,
            "outcome": "GATE_RECORDED_STATE_DRIFT",
            "record": core.controller_success("RECORD_HUMAN_GATE", record_payload),
            "fresh_guard": fresh_guard,
            "transitions_advanced": 0,
        }

    target = str(next_item["id"])
    advance_args = ["advance", "--slot-root", str(slot_root), "--to", target]
    code, advance_payload, _stdout, stderr = core.run_json(core.tool_command(core.STATE_TOOL, registry_dir, *advance_args))
    if code != 0 or advance_payload.get("ok") is not True:
        return {
            "ok": False,
            "outcome": "GATE_RECORDED_ADVANCE_BLOCKED",
            "record": core.controller_success("RECORD_HUMAN_GATE", record_payload),
            "advance": core.controller_failure("ADVANCE", code, advance_payload, stderr),
            "transitions_advanced": 0,
        }
    return {
        "ok": True,
        "outcome": "GATE_ACCEPTED_AND_ADVANCED",
        "gate": gate,
        "from_stage": current,
        "to_stage": target,
        "record": core.controller_success("RECORD_HUMAN_GATE", record_payload),
        "advance": core.controller_success("ADVANCE", advance_payload),
        "transitions_advanced": 1,
    }


def execute_run_until(
    request: dict[str, Any],
    preflight: dict[str, Any],
    registry_dir: Path,
    program_root: Path,
    tracker: Path,
    contract: dict[str, Any],
) -> dict[str, Any]:
    if preflight.get("mode") != "RESUME_CANONICAL":
        raise LeanFatal("RUN_UNTIL_GATE_OR_BLOCK requires RESUME_CANONICAL preflight")
    slot_id = request["slot_id"]
    slot_root = program_root / slot_id
    core.compare_guard(request["expected_guard"], core.canonical_guard(slot_root, registry_dir))
    stages = stage_items(registry_dir)
    policy = contract.get("lean_policy") or {}
    external_stops = set(policy.get("external_handoff_stop_after_stages") or [])
    release_stops = set(policy.get("release_stop_after_stages") or [])
    max_steps = int(request.get("payload", {}).get("max_steps", policy.get("default_max_steps", 8)))
    packet = preflight
    advanced: list[dict[str, Any]] = []

    for _ in range(max_steps):
        current = str(packet.get("current_stage"))
        if current in external_stops:
            return {"ok": True, "outcome": "EXTERNAL_HANDOFF", "stop_stage": current, "transitions_advanced": len(advanced), "steps": advanced}
        if current in release_stops:
            return {"ok": True, "outcome": "RELEASE_READY", "stop_stage": current, "transitions_advanced": len(advanced), "steps": advanced}
        index = stage_index(stages, current)
        if index + 1 >= len(stages):
            return {"ok": True, "outcome": "TERMINAL", "stop_stage": current, "transitions_advanced": len(advanced), "steps": advanced}
        next_item = stages[index + 1]
        next_stage = str(next_item["id"])
        if next_item.get("human_gate"):
            return {
                "ok": True,
                "outcome": "HUMAN_GATE",
                "stop_stage": current,
                "human_gate": next_item.get("human_gate"),
                "next_stage": next_stage,
                "transitions_advanced": len(advanced),
                "steps": advanced,
            }

        args = ["advance", "--slot-root", str(slot_root), "--to", next_stage]
        code, payload, _stdout, stderr = core.run_json(core.tool_command(core.STATE_TOOL, registry_dir, *args))
        if code != 0 or payload.get("ok") is not True:
            return {
                "ok": True,
                "outcome": "BLOCKED",
                "stop_stage": current,
                "attempted_next_stage": next_stage,
                "block": core.controller_failure("ADVANCE", code, payload, stderr),
                "transitions_advanced": len(advanced),
                "steps": advanced,
            }
        advanced.append({"from_stage": current, "to_stage": next_stage, "controller_payload": payload})
        packet = core.resume_query(REPO_ROOT, registry_dir, program_root, tracker, slot_id)

    return {
        "ok": True,
        "outcome": "MAX_STEPS",
        "stop_stage": packet.get("current_stage"),
        "transitions_advanced": len(advanced),
        "steps": advanced,
    }


def response_path_for(request_id: str, response_dir: Path, contract: dict[str, Any]) -> Path:
    return response_dir / contract["response_filename_template"].format(request_id=request_id)


def write_response(
    path: Path,
    *,
    request: dict[str, Any],
    request_sha: str,
    status: str,
    preflight: dict[str, Any] | None,
    execution: dict[str, Any] | None,
    postflight: dict[str, Any] | None,
    next_guard: dict[str, Any] | None,
    error: str | None,
    repo_root: Path,
) -> dict[str, Any]:
    payload = {
        "schema_version": "1.0",
        "request_id": request.get("request_id"),
        "request_sha256": request_sha,
        "command": request.get("command"),
        "slot_id": request.get("slot_id"),
        "status": status,
        "preflight": preflight,
        "execution": execution,
        "postflight": postflight,
        "next_guard": next_guard,
        "error": error,
        "runner": {
            "github_run_id": os.getenv("GITHUB_RUN_ID"),
            "github_run_attempt": os.getenv("GITHUB_RUN_ATTEMPT"),
            "github_source_sha": os.getenv("GITHUB_SHA"),
            "github_ref_name": os.getenv("GITHUB_REF_NAME"),
        },
        "completed_at": now_iso(),
    }
    core.atomic_json(path, payload)
    payload["response_path"] = rel_to_repo(repo_root, path)
    return payload


def process_one(
    request_path: Path,
    response_dir: Path,
    contract: dict[str, Any],
    repo_root: Path,
    registry_dir: Path,
    program_root: Path,
    tracker: Path,
) -> dict[str, Any]:
    request_sha = sha256_file(request_path)
    request = load_json(request_path)
    request_id = request.get("request_id")
    if not isinstance(request_id, str):
        raise LeanFatal("request_id missing")
    response_path = response_path_for(request_id, response_dir, contract)
    if response_path.exists():
        existing = load_json(response_path)
        if existing.get("request_sha256") != request_sha:
            raise LeanFatal("request was modified after immutable response")
        return {"request_id": request_id, "status": "ALREADY_RESPONDED", "response_path": rel_to_repo(repo_root, response_path)}

    preflight = execution = postflight = next_guard = None
    try:
        definition = validate_request(request_path, request, contract)
        slot_id = request.get("slot_id")
        preflight_raw = core.resume_query(repo_root, registry_dir, program_root, tracker, slot_id)
        preflight = enrich_packet(preflight_raw, registry_dir, contract)
        command = request["command"]

        if command == "RESUME":
            next_guard = core.guard_for_packet(preflight_raw, registry_dir, program_root, tracker)
            execution = {"ok": True, "outcome": "RESUMED", "transitions_advanced": 0}
        elif command == "ACCEPT_GATE":
            execution = execute_accept_gate(request, preflight_raw, registry_dir, program_root)
        elif command == "RUN_UNTIL_GATE_OR_BLOCK":
            execution = execute_run_until(request, preflight_raw, registry_dir, program_root, tracker, contract)
        else:
            execution = execute_old_mutation(request, preflight_raw, registry_dir, program_root, tracker)

        if command != "RESUME":
            try:
                postflight_raw = core.resume_query(repo_root, registry_dir, program_root, tracker, slot_id)
                postflight = enrich_packet(postflight_raw, registry_dir, contract)
                next_guard = core.guard_for_packet(postflight_raw, registry_dir, program_root, tracker)
            except (core.BridgeFatal, LeanFatal):
                postflight = None
                next_guard = None

        ok = isinstance(execution, dict) and execution.get("ok") is True
        status = "EXECUTED" if ok else "REJECTED"
        return write_response(
            response_path,
            request=request,
            request_sha=request_sha,
            status=status,
            preflight=preflight,
            execution=execution,
            postflight=postflight if postflight is not None else preflight,
            next_guard=next_guard,
            error=None if ok else "lean macro or canonical controller rejected the request",
            repo_root=repo_root,
        )
    except (LeanFatal, core.BridgeFatal) as exc:
        return write_response(
            response_path,
            request=request,
            request_sha=request_sha,
            status="REJECTED",
            preflight=preflight,
            execution=execution,
            postflight=postflight,
            next_guard=next_guard,
            error=str(exc),
            repo_root=repo_root,
        )


def request_paths(directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []
    return sorted(p for p in directory.glob("*.json") if p.is_file())


def process_pending(args: argparse.Namespace) -> None:
    repo_root = args.repo_root.resolve()
    registry_dir = args.registry_dir.resolve()
    contract = load_contract(registry_dir)
    validate_contract(contract)
    program_root = resolve_repo_path(repo_root, args.program_root or contract["program_root"])
    tracker = resolve_repo_path(repo_root, args.tracker or contract["tracker_path"])
    request_dir = resolve_repo_path(repo_root, args.request_dir or contract["request_directory"])
    response_dir = resolve_repo_path(repo_root, args.response_dir or contract["response_directory"])
    if not tracker.is_file():
        raise LeanFatal(f"tracker is missing: {tracker}")
    results = [process_one(p, response_dir, contract, repo_root, registry_dir, program_root, tracker) for p in request_paths(request_dir)]
    print(json.dumps({"ok": True, "mode": "lean-process-pending", "request_count": len(results), "results": results}, ensure_ascii=False, indent=2))


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Lean macro bridge over the canonical MV Runtime")
    p.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    p.add_argument("--registry-dir", type=Path, default=RUNTIME_DIR)
    p.add_argument("--program-root")
    p.add_argument("--tracker")
    p.add_argument("--request-dir")
    p.add_argument("--response-dir")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("process-pending")
    return p


def main() -> None:
    args = parser().parse_args()
    try:
        process_pending(args)
    except LeanFatal as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
