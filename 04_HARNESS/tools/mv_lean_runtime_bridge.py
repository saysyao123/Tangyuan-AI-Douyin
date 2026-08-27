#!/usr/bin/env python3
"""Lean external bridge over the canonical MV Runtime.

Lean R1 compresses transport, not evidence. Existing canonical controllers remain
the mutation authority. Two macro commands are added:
- ACCEPT_GATE: record Human Gate receipt then advance in one external request.
- RUN_UNTIL_GATE_OR_BLOCK: advance consecutive already-ready machine stages,
  preserving normal per-stage validation/receipts, and stop at a Human Gate,
  external generation handoff, Release Ready, terminal state, or first block.

The macro never fabricates missing artifacts and never executes arbitrary shell.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import mv_runtime_bridge as core

SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[2]
RUNTIME_DIR = SCRIPT_PATH.parent.parent / "runtime"
CONTRACT_NAME = "mv_lean_runtime_contract.json"


class LeanFatal(RuntimeError):
    pass


def load_contract(registry_dir: Path) -> dict[str, Any]:
    return core.load_json(registry_dir / CONTRACT_NAME)


def validate_contract(contract: dict[str, Any]) -> None:
    commands = contract.get("commands")
    expected = {
        "RESUME",
        "INIT_SLOT",
        "ACCEPT_GATE",
        "RUN_UNTIL_GATE_OR_BLOCK",
        "ADVANCE",
        "UPDATE_CONTEXT",
        "ROLLBACK",
        "PUBLISH_SYNC",
    }
    if not isinstance(commands, dict) or set(commands) != expected:
        raise LeanFatal(
            f"lean command whitelist mismatch expected={sorted(expected)} actual={sorted(commands or {})}"
        )
    policy = contract.get("lean_policy")
    if not isinstance(policy, dict):
        raise LeanFatal("lean_policy missing")
    if policy.get("machine_stage_receipts_are_not_skipped") is not True:
        raise LeanFatal("Lean Runtime may not skip machine stage receipts")
    if not isinstance(contract.get("request_id_pattern"), str):
        raise LeanFatal("request_id_pattern missing")


def load_executor_registry(registry_dir: Path, contract: dict[str, Any]) -> dict[str, Any]:
    rel = contract.get("executor_registry_path")
    if not isinstance(rel, str) or not rel:
        raise LeanFatal("executor_registry_path missing")
    path = (REPO_ROOT / rel).resolve()
    payload = core.load_json(path)
    stages = payload.get("stage_executors")
    if not isinstance(stages, dict) or not stages:
        raise LeanFatal("stage executor registry is empty")
    return payload


def enrich_packet(packet: dict[str, Any], executor_registry: dict[str, Any]) -> dict[str, Any]:
    result = dict(packet)
    stage = packet.get("current_stage")
    entry = (executor_registry.get("stage_executors") or {}).get(stage)
    if isinstance(entry, dict):
        result["resolved_executor"] = entry
        result["jit_reads"] = entry.get("jit_reads") or packet.get("jit_reads") or []
    elif packet.get("mode") == "ALLOCATE_NEW_SLOT":
        result["resolved_executor"] = {
            "executor_id": "HG01_CORE_DATABASE_ORCHESTRATION",
            "execution_class": "DATA_ORCHESTRATION",
            "dependency_policy": "NO_NEW_DEPENDENCY",
        }
    return result


def state_call(registry_dir: Path, *args: str) -> tuple[int, dict[str, Any], str]:
    code, payload, _stdout, stderr = core.run_json(
        core.tool_command(core.STATE_TOOL, registry_dir, *args)
    )
    return code, payload, stderr


def record_gate(
    slot_root: Path,
    payload: dict[str, Any],
    registry_dir: Path,
) -> dict[str, Any]:
    gate = payload.get("gate")
    text = payload.get("user_decision_text")
    approved = payload.get("approved_artifacts")
    if not isinstance(gate, str) or not gate.strip():
        raise LeanFatal("ACCEPT_GATE payload.gate must be non-empty")
    if not isinstance(text, str) or not text.strip():
        raise LeanFatal("ACCEPT_GATE payload.user_decision_text must be non-empty")
    if (
        not isinstance(approved, list)
        or not approved
        or any(not isinstance(x, str) or not x.strip() for x in approved)
    ):
        raise LeanFatal("ACCEPT_GATE approved_artifacts must be a non-empty string array")
    args = [
        "record-human-gate",
        "--slot-root",
        str(slot_root),
        "--gate",
        gate,
        "--user-decision-text",
        text,
    ]
    for item in approved:
        args.extend(["--approved-artifact", item])
    code, result, stderr = state_call(registry_dir, *args)
    return {"ok": code == 0 and result.get("ok") is True, "payload": result, "stderr": stderr}


def advance_once(slot_root: Path, target: str, registry_dir: Path) -> dict[str, Any]:
    code, payload, stderr = state_call(
        registry_dir, "advance", "--slot-root", str(slot_root), "--to", target
    )
    return {"ok": code == 0 and payload.get("ok") is True, "payload": payload, "stderr": stderr}


def execute_accept_gate(
    request: dict[str, Any],
    preflight: dict[str, Any],
    registry_dir: Path,
    program_root: Path,
    tracker: Path,
) -> dict[str, Any]:
    slot_id = request["slot_id"]
    slot_root = program_root / slot_id
    if preflight.get("mode") != "RESUME_CANONICAL":
        raise LeanFatal("ACCEPT_GATE requires RESUME_CANONICAL")
    core.compare_guard(request["expected_guard"], core.canonical_guard(slot_root, registry_dir))

    expected_gate = ((preflight.get("next_action") or {}).get("human_gate"))
    supplied_gate = (request.get("payload") or {}).get("gate")
    if expected_gate != supplied_gate or expected_gate is None:
        raise LeanFatal(
            f"ACCEPT_GATE gate mismatch current expected={expected_gate!r} supplied={supplied_gate!r}"
        )
    target = (preflight.get("next_action") or {}).get("next_stage")
    if not isinstance(target, str) or not target:
        raise LeanFatal("ACCEPT_GATE current action has no next_stage")

    phase1 = record_gate(slot_root, request["payload"], registry_dir)
    if phase1["ok"] is not True:
        return {
            "ok": False,
            "command": "ACCEPT_GATE",
            "phase": "RECORD_HUMAN_GATE",
            "phase1": phase1,
        }

    after_receipt = core.resume_query(REPO_ROOT, registry_dir, program_root, tracker, slot_id)
    phase2 = advance_once(slot_root, target, registry_dir)
    if phase2["ok"] is not True:
        return {
            "ok": False,
            "command": "ACCEPT_GATE",
            "phase": "ADVANCE_AFTER_RECEIPT",
            "phase1": phase1,
            "after_receipt": after_receipt,
            "phase2": phase2,
            "recovery": "Human Gate receipt is durable; patch the blocking prerequisite and ADVANCE with a fresh guard. Do not record the gate twice.",
        }
    return {
        "ok": True,
        "command": "ACCEPT_GATE",
        "phase1": phase1,
        "after_receipt": after_receipt,
        "phase2": phase2,
        "target_stage": target,
    }


def execute_run_until(
    request: dict[str, Any],
    preflight: dict[str, Any],
    contract: dict[str, Any],
    registry_dir: Path,
    program_root: Path,
    tracker: Path,
) -> dict[str, Any]:
    slot_id = request["slot_id"]
    slot_root = program_root / slot_id
    if preflight.get("mode") != "RESUME_CANONICAL":
        raise LeanFatal("RUN_UNTIL_GATE_OR_BLOCK requires RESUME_CANONICAL")
    core.compare_guard(request["expected_guard"], core.canonical_guard(slot_root, registry_dir))

    policy = contract["lean_policy"]
    requested_max = (request.get("payload") or {}).get("max_steps", policy["default_max_steps"])
    if not isinstance(requested_max, int) or isinstance(requested_max, bool):
        raise LeanFatal("max_steps must be integer")
    if requested_max < 1 or requested_max > int(policy["max_max_steps"]):
        raise LeanFatal("max_steps outside Lean Runtime limits")

    external_stops = set(policy.get("external_handoff_stop_after_stages") or [])
    release_stops = set(policy.get("release_stop_after_stages") or [])
    packet = preflight
    transitions: list[dict[str, Any]] = []
    stop_reason = "MAX_STEPS"
    blocking: dict[str, Any] | None = None

    for _ in range(requested_max):
        current = packet.get("current_stage")
        action = packet.get("next_action") or {}
        human_gate = action.get("human_gate")
        if human_gate:
            stop_reason = "HUMAN_GATE"
            break
        if current in external_stops:
            stop_reason = "EXTERNAL_HANDOFF"
            break
        if current in release_stops:
            stop_reason = "RELEASE_READY"
            break
        target = action.get("next_stage")
        if target is None:
            stop_reason = "TERMINAL"
            break
        if not isinstance(target, str) or not target:
            stop_reason = "INVALID_NEXT_STAGE"
            blocking = {"action": action}
            break

        result = advance_once(slot_root, target, registry_dir)
        if result["ok"] is not True:
            stop_reason = "BLOCKED"
            blocking = result
            break
        transitions.append(
            {
                "from": current,
                "to": target,
                "controller_payload": result["payload"],
            }
        )
        packet = core.resume_query(REPO_ROOT, registry_dir, program_root, tracker, slot_id)

    return {
        "ok": True,
        "command": "RUN_UNTIL_GATE_OR_BLOCK",
        "macro_status": stop_reason,
        "transition_count": len(transitions),
        "transitions": transitions,
        "blocking": blocking,
        "final_packet": packet,
    }


def response_path_for(request_id: str, response_dir: Path, contract: dict[str, Any]) -> Path:
    return response_dir / contract["response_filename_template"].format(request_id=request_id)


def process_one(
    request_path: Path,
    response_dir: Path,
    contract: dict[str, Any],
    executor_registry: dict[str, Any],
    repo_root: Path,
    registry_dir: Path,
    program_root: Path,
    tracker: Path,
) -> dict[str, Any]:
    request_sha = core.sha256_file(request_path)
    request = core.load_json(request_path)
    request_id = request.get("request_id")
    if not isinstance(request_id, str):
        raise LeanFatal("request_id missing")
    response_path = response_path_for(request_id, response_dir, contract)
    if response_path.exists():
        existing = core.load_json(response_path)
        if existing.get("request_sha256") != request_sha:
            raise LeanFatal("request modified after immutable response")
        return {"request_id": request_id, "status": "ALREADY_RESPONDED"}

    preflight = None
    execution = None
    postflight = None
    next_guard = None
    try:
        definition = core.validate_request(request_path, request, contract)
        slot_id = request.get("slot_id")
        preflight = core.resume_query(repo_root, registry_dir, program_root, tracker, slot_id)
        preflight = enrich_packet(preflight, executor_registry)

        if request["command"] == "RESUME":
            next_guard = core.guard_for_packet(preflight, registry_dir, program_root, tracker)
            return core.write_response(
                response_path,
                request=request,
                request_sha=request_sha,
                status="EXECUTED",
                preflight=preflight,
                execution={"ok": True, "command": "RESUME", "controller_payload": preflight},
                postflight=preflight,
                next_guard=next_guard,
                error=None,
                repo_root=repo_root,
            )

        if definition["mutation"] is not True:
            raise LeanFatal("non-RESUME Lean command must be mutating")

        if request["command"] == "ACCEPT_GATE":
            execution = execute_accept_gate(request, preflight, registry_dir, program_root, tracker)
        elif request["command"] == "RUN_UNTIL_GATE_OR_BLOCK":
            execution = execute_run_until(
                request, preflight, contract, registry_dir, program_root, tracker
            )
        else:
            execution = core.execute_mutation(
                request, preflight, registry_dir, program_root, tracker
            )

        postflight = core.resume_query(repo_root, registry_dir, program_root, tracker, slot_id)
        postflight = enrich_packet(postflight, executor_registry)
        next_guard = core.guard_for_packet(postflight, registry_dir, program_root, tracker)
        status = "EXECUTED" if execution.get("ok") is True else "REJECTED"
        error = None if execution.get("ok") is True else "Lean or canonical controller rejected the request"
        return core.write_response(
            response_path,
            request=request,
            request_sha=request_sha,
            status=status,
            preflight=preflight,
            execution=execution,
            postflight=postflight,
            next_guard=next_guard,
            error=error,
            repo_root=repo_root,
        )
    except (core.BridgeFatal, LeanFatal) as exc:
        return core.write_response(
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


def process_pending(args: argparse.Namespace) -> None:
    repo_root = args.repo_root.resolve()
    registry_dir = args.registry_dir.resolve()
    contract = load_contract(registry_dir)
    validate_contract(contract)
    executor_registry = load_executor_registry(registry_dir, contract)
    program_root = core.resolve_repo_path(repo_root, args.program_root or contract["program_root"])
    tracker = core.resolve_repo_path(repo_root, args.tracker or contract["tracker_path"])
    request_dir = core.resolve_repo_path(repo_root, args.request_dir or contract["request_directory"])
    response_dir = core.resolve_repo_path(repo_root, args.response_dir or contract["response_directory"])
    if not tracker.is_file():
        raise LeanFatal(f"tracker missing: {tracker}")

    results = []
    for path in sorted(p for p in request_dir.glob("*.json") if p.is_file()) if request_dir.is_dir() else []:
        results.append(
            process_one(
                path,
                response_dir,
                contract,
                executor_registry,
                repo_root,
                registry_dir,
                program_root,
                tracker,
            )
        )
    print(json.dumps({"ok": True, "mode": "process-pending", "results": results}, ensure_ascii=False, indent=2))


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Lean macro bridge for canonical MV Runtime")
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
    except (core.BridgeFatal, LeanFatal) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
