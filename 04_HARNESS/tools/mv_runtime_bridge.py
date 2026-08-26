#!/usr/bin/env python3
"""GitHub-backed execution bridge for the canonical MV Runtime.

The bridge is a narrow control plane for clients (including ChatGPT web) that
can read/write GitHub but cannot execute repository Python directly.

It never accepts shell fragments or repository paths from a request. Mutating
requests must carry an exact optimistic-concurrency guard obtained from a prior
bridge response. Existing Runtime controllers remain the only mutation
authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import mv_runtime_state as statectl

SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[2]
RUNTIME_DIR = SCRIPT_PATH.parent.parent / "runtime"
CONTRACT_NAME = "mv_runtime_bridge_contract.json"

STATE_TOOL = SCRIPT_PATH.parent / "mv_runtime_state.py"
RESUME_TOOL = SCRIPT_PATH.parent / "mv_runtime_resume.py"
REVISION_TOOL = SCRIPT_PATH.parent / "mv_runtime_revision.py"
PUBLISH_TOOL = SCRIPT_PATH.parent / "mv_runtime_publish.py"


class BridgeFatal(RuntimeError):
    pass


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise BridgeFatal(f"invalid or missing JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise BridgeFatal(f"JSON root must be object: {path}")
    return value


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temp, path)


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


def validate_contract(contract: dict[str, Any]) -> None:
    commands = contract.get("commands")
    if not isinstance(commands, dict) or not commands:
        raise BridgeFatal("bridge contract commands must be a non-empty object")
    expected = {
        "RESUME",
        "INIT_SLOT",
        "RECORD_HUMAN_GATE",
        "ADVANCE",
        "UPDATE_CONTEXT",
        "ROLLBACK",
        "PUBLISH_SYNC",
    }
    if set(commands) != expected:
        raise BridgeFatal(
            f"bridge command whitelist mismatch: expected={sorted(expected)} actual={sorted(commands)}"
        )
    if not isinstance(contract.get("request_id_pattern"), str):
        raise BridgeFatal("bridge request_id_pattern missing")
    for name, definition in commands.items():
        if not isinstance(definition, dict):
            raise BridgeFatal(f"{name}: command definition must be object")
        for key in ("mutation", "slot_id_required", "expected_guard_required"):
            if not isinstance(definition.get(key), bool):
                raise BridgeFatal(f"{name}: {key} must be boolean")
        for key in ("payload_required", "payload_allowed"):
            value = definition.get(key)
            if not isinstance(value, list) or any(not isinstance(x, str) for x in value):
                raise BridgeFatal(f"{name}: {key} must be string array")
        if not set(definition["payload_required"]).issubset(
            set(definition["payload_allowed"])
        ):
            raise BridgeFatal(f"{name}: required payload keys must be allowed")


def run_json(command: list[str]) -> tuple[int, dict[str, Any], str, str]:
    result = subprocess.run(command, text=True, capture_output=True)
    stdout = result.stdout.strip()
    stderr = result.stderr.strip()
    try:
        parsed = json.loads(stdout) if stdout else {}
        payload = parsed if isinstance(parsed, dict) else {"raw_stdout": stdout}
    except json.JSONDecodeError:
        payload = {"raw_stdout": stdout}
    return result.returncode, payload, stdout, stderr


def tool_command(tool: Path, registry_dir: Path, *args: str) -> list[str]:
    return [
        sys.executable,
        str(tool.resolve()),
        "--registry-dir",
        str(registry_dir.resolve()),
        *args,
    ]


def resume_query(
    repo_root: Path,
    registry_dir: Path,
    program_root: Path,
    tracker: Path,
    slot_id: str | None,
) -> dict[str, Any]:
    command = tool_command(
        RESUME_TOOL,
        registry_dir,
        "--repo-root",
        str(repo_root),
        "--program-root",
        str(program_root),
        "--tracker",
        str(tracker),
    )
    if slot_id:
        command.extend(["--slot-id", slot_id])
    code, payload, _stdout, stderr = run_json(command)
    if code != 0:
        raise BridgeFatal(
            f"resume controller rejected repository truth: code={code} payload={payload} stderr={stderr}"
        )
    if payload.get("ok") is not True:
        raise BridgeFatal(f"resume controller returned non-PASS payload: {payload}")
    return payload


def slot_fingerprint(slot_root: Path) -> str:
    if not slot_root.is_dir():
        raise BridgeFatal(f"slot root is missing for fingerprint: {slot_root}")
    rows: list[str] = []
    for path in sorted(p for p in slot_root.rglob("*") if p.is_file()):
        if path.name.endswith(".tmp"):
            continue
        rel = path.relative_to(slot_root).as_posix()
        rows.append(f"{rel}\0{path.stat().st_size}\0{sha256_file(path)}")
    return hashlib.sha256("\n".join(rows).encode("utf-8")).hexdigest()


def canonical_guard(slot_root: Path, registry_dir: Path) -> dict[str, Any]:
    verify = tool_command(
        STATE_TOOL, registry_dir, "verify-state", "--slot-root", str(slot_root)
    )
    code, payload, _stdout, stderr = run_json(verify)
    if code != 0 or payload.get("ok") is not True:
        raise BridgeFatal(
            f"canonical state verification failed before guard snapshot: {payload} {stderr}"
        )
    runtime = statectl.load_runtime(registry_dir.resolve())
    state_file = statectl.state_path(slot_root, runtime)
    state = load_json(state_file)
    return {
        "kind": "CANONICAL",
        "state_sha256": sha256_file(state_file),
        "slot_fingerprint_sha256": slot_fingerprint(slot_root),
        "current_stage": state.get("current_stage"),
        "current_state_token": state.get("current_state_token"),
        "transition_sequence": state.get("transition_sequence"),
        "last_transition_receipt_sha256": state.get("last_transition_receipt_sha256"),
        "context_revision": int(state.get("context_revision", 0) or 0),
        "last_context_receipt_sha256": state.get("last_context_receipt_sha256"),
        "revision_sequence": int(state.get("revision_sequence", 0) or 0),
        "last_revision_receipt_sha256": state.get("last_revision_receipt_sha256"),
    }


def allocation_guard(packet: dict[str, Any], tracker: Path) -> dict[str, Any]:
    return {
        "kind": "ALLOCATION",
        "tracker_sha256": sha256_file(tracker),
        "mode": packet.get("mode"),
        "slot_id": packet.get("slot_id"),
        "lane": packet.get("lane"),
    }


def guard_for_packet(
    packet: dict[str, Any],
    registry_dir: Path,
    program_root: Path,
    tracker: Path,
) -> dict[str, Any] | None:
    mode = packet.get("mode")
    if mode == "RESUME_CANONICAL":
        slot_id = packet.get("slot_id")
        if not isinstance(slot_id, str) or not slot_id:
            raise BridgeFatal("canonical resume packet is missing slot_id")
        return canonical_guard(program_root / slot_id, registry_dir)
    if mode == "ALLOCATE_NEW_SLOT":
        return allocation_guard(packet, tracker)
    return None


def validate_request(
    request_path: Path,
    request: dict[str, Any],
    contract: dict[str, Any],
) -> dict[str, Any]:
    missing = [
        key
        for key in contract.get("required_request_fields") or []
        if key not in request
    ]
    if missing:
        raise BridgeFatal(f"request missing required fields: {missing}")
    if request.get("schema_version") != contract.get("schema_version"):
        raise BridgeFatal("request schema_version does not match bridge contract")
    request_id = request.get("request_id")
    if not isinstance(request_id, str) or re.fullmatch(
        contract["request_id_pattern"], request_id
    ) is None:
        raise BridgeFatal(f"invalid request_id: {request_id!r}")
    if request_path.name != contract["request_filename_template"].format(
        request_id=request_id
    ):
        raise BridgeFatal("request filename does not match request_id")
    command = request.get("command")
    commands = contract["commands"]
    if command not in commands:
        raise BridgeFatal(f"command is not whitelisted: {command!r}")
    definition = commands[command]
    slot_id = request.get("slot_id")
    if definition["slot_id_required"] and (
        not isinstance(slot_id, str) or not slot_id.strip()
    ):
        raise BridgeFatal(f"{command}: non-empty slot_id is required")
    if slot_id is not None and (
        not isinstance(slot_id, str)
        or re.fullmatch(r"^D[0-9]+-[A-Za-z]$", slot_id) is None
    ):
        raise BridgeFatal(f"invalid slot_id: {slot_id!r}")
    payload = request.get("payload")
    if not isinstance(payload, dict):
        raise BridgeFatal("request payload must be object")
    allowed = set(definition["payload_allowed"])
    extra = sorted(set(payload) - allowed)
    if extra:
        raise BridgeFatal(f"{command}: payload contains forbidden keys: {extra}")
    required = [key for key in definition["payload_required"] if key not in payload]
    if required:
        raise BridgeFatal(f"{command}: payload missing required keys: {required}")
    requested_by = request.get("requested_by")
    if requested_by not in set(contract.get("allowed_requested_by") or []):
        raise BridgeFatal(f"requested_by is not allowed: {requested_by!r}")
    reason = request.get("reason")
    if not isinstance(reason, str) or not reason.strip():
        raise BridgeFatal("request reason must be non-empty")
    expected_guard = request.get("expected_guard")
    if definition["expected_guard_required"]:
        if not isinstance(expected_guard, dict):
            raise BridgeFatal(f"{command}: expected_guard is required")
        expected_kind = definition.get("expected_guard_kind")
        if expected_guard.get("kind") != expected_kind:
            raise BridgeFatal(f"{command}: expected_guard.kind must be {expected_kind}")
        fields_key = (
            "canonical_guard_fields"
            if expected_kind == "CANONICAL"
            else "allocation_guard_fields"
        )
        required_guard_fields = set(contract.get(fields_key) or [])
        missing_guard = sorted(required_guard_fields - set(expected_guard))
        extra_guard = sorted(set(expected_guard) - required_guard_fields)
        if missing_guard or extra_guard:
            raise BridgeFatal(
                f"{command}: guard fields mismatch missing={missing_guard} extra={extra_guard}"
            )
    elif expected_guard is not None:
        raise BridgeFatal(f"{command}: expected_guard is not accepted")
    return definition


def compare_guard(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    if expected != actual:
        diff = {
            key: {"expected": expected.get(key), "actual": actual.get(key)}
            for key in sorted(set(expected) | set(actual))
            if expected.get(key) != actual.get(key)
        }
        raise BridgeFatal(f"stale optimistic-concurrency guard: {diff}")


def controller_failure(
    command: str,
    code: int,
    payload: dict[str, Any],
    stderr: str,
) -> dict[str, Any]:
    return {
        "ok": False,
        "command": command,
        "returncode": code,
        "controller_payload": payload,
        "stderr": stderr,
    }


def controller_success(command: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "ok": True,
        "command": command,
        "returncode": 0,
        "controller_payload": payload,
    }


def execute_mutation(
    request: dict[str, Any],
    preflight: dict[str, Any],
    registry_dir: Path,
    program_root: Path,
    tracker: Path,
) -> dict[str, Any]:
    command_name = request["command"]
    slot_id = request["slot_id"]
    payload = request["payload"]
    slot_root = program_root / slot_id

    if command_name == "INIT_SLOT":
        if preflight.get("mode") != "ALLOCATE_NEW_SLOT":
            raise BridgeFatal(
                f"INIT_SLOT requires ALLOCATE_NEW_SLOT preflight, got {preflight.get('mode')}"
            )
        if preflight.get("slot_id") != slot_id:
            raise BridgeFatal("INIT_SLOT preflight selected a different slot")
        compare_guard(request["expected_guard"], allocation_guard(preflight, tracker))
        program = str(payload.get("program", "30D_60")).strip()
        if not program:
            raise BridgeFatal("INIT_SLOT payload.program cannot be blank")
        bool_values = {
            "web": payload.get("web", True),
            "multi_shot": payload.get("multi_shot", False),
            "program_30d60": payload.get("program_30d60", True),
        }
        if any(not isinstance(value, bool) for value in bool_values.values()):
            raise BridgeFatal("INIT_SLOT context flags must be booleans")
        args = [
            "init-slot",
            "--slot-root",
            str(slot_root),
            "--slot-id",
            slot_id,
            "--program",
            program,
            "--lane",
            str(preflight.get("lane", "")),
            "--web",
            str(bool_values["web"]).lower(),
            "--multi-shot",
            str(bool_values["multi_shot"]).lower(),
            "--program-30d60",
            str(bool_values["program_30d60"]).lower(),
        ]
        tool = STATE_TOOL
    else:
        if preflight.get("mode") != "RESUME_CANONICAL":
            raise BridgeFatal(
                f"{command_name} requires RESUME_CANONICAL preflight, got {preflight.get('mode')}"
            )
        compare_guard(
            request["expected_guard"], canonical_guard(slot_root, registry_dir)
        )

        if command_name == "RECORD_HUMAN_GATE":
            gate = payload["gate"]
            text = payload["user_decision_text"]
            approved = payload["approved_artifacts"]
            if not isinstance(gate, str) or not gate.strip():
                raise BridgeFatal("RECORD_HUMAN_GATE payload.gate must be non-empty")
            if not isinstance(text, str) or not text.strip():
                raise BridgeFatal(
                    "RECORD_HUMAN_GATE payload.user_decision_text must be non-empty"
                )
            if (
                not isinstance(approved, list)
                or not approved
                or any(not isinstance(item, str) or not item.strip() for item in approved)
            ):
                raise BridgeFatal(
                    "RECORD_HUMAN_GATE payload.approved_artifacts must be a non-empty string array"
                )
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
            tool = STATE_TOOL
        elif command_name == "ADVANCE":
            target = payload["to"]
            if not isinstance(target, str) or not target.strip():
                raise BridgeFatal("ADVANCE payload.to must be non-empty")
            args = ["advance", "--slot-root", str(slot_root), "--to", target]
            tool = STATE_TOOL
        elif command_name == "UPDATE_CONTEXT":
            key = payload["key"]
            value = payload["value"]
            reason = payload["reason"]
            if not isinstance(key, str) or not key.strip():
                raise BridgeFatal("UPDATE_CONTEXT payload.key must be non-empty")
            if not isinstance(value, bool):
                raise BridgeFatal("UPDATE_CONTEXT payload.value must be boolean")
            if not isinstance(reason, str) or not reason.strip():
                raise BridgeFatal("UPDATE_CONTEXT payload.reason must be non-empty")
            args = [
                "update-context",
                "--slot-root",
                str(slot_root),
                "--key",
                key,
                "--value",
                str(value).lower(),
                "--reason",
                reason,
            ]
            tool = STATE_TOOL
        elif command_name == "ROLLBACK":
            change_type = payload["change_type"]
            reason = payload["reason"]
            authority = payload.get("authority", request["requested_by"])
            if not isinstance(change_type, str) or not change_type.strip():
                raise BridgeFatal("ROLLBACK payload.change_type must be non-empty")
            if not isinstance(reason, str) or not reason.strip():
                raise BridgeFatal("ROLLBACK payload.reason must be non-empty")
            if not isinstance(authority, str) or not authority.strip():
                raise BridgeFatal("ROLLBACK payload.authority must be non-empty")
            args = [
                "rollback",
                "--slot-root",
                str(slot_root),
                "--change-type",
                change_type,
                "--reason",
                reason,
                "--authority",
                authority,
            ]
            tool = REVISION_TOOL
        elif command_name == "PUBLISH_SYNC":
            for key in ("song_family", "audio_asset", "confirmation_source"):
                if not isinstance(payload[key], str) or not payload[key].strip():
                    raise BridgeFatal(f"PUBLISH_SYNC payload.{key} must be non-empty")
            args = [
                "sync",
                "--slot-root",
                str(slot_root),
                "--tracker",
                str(tracker),
                "--song-family",
                payload["song_family"],
                "--audio-asset",
                payload["audio_asset"],
                "--confirmation-source",
                payload["confirmation_source"],
            ]
            for request_key, flag in (
                ("packaging", "--packaging"),
                ("publish_time", "--publish-time"),
            ):
                value = payload.get(request_key)
                if value is not None:
                    if not isinstance(value, str) or not value.strip():
                        raise BridgeFatal(
                            f"PUBLISH_SYNC payload.{request_key} must be non-empty when supplied"
                        )
                    args.extend([flag, value])
            tool = PUBLISH_TOOL
        else:
            raise BridgeFatal(f"unsupported mutation command: {command_name}")

    code, controller_payload, _stdout, stderr = run_json(
        tool_command(tool, registry_dir, *args)
    )
    if code != 0 or controller_payload.get("ok") is not True:
        return controller_failure(command_name, code, controller_payload, stderr)
    return controller_success(command_name, controller_payload)


def response_path_for(
    request_id: str, response_dir: Path, contract: dict[str, Any]
) -> Path:
    return response_dir / contract["response_filename_template"].format(
        request_id=request_id
    )


def write_response(
    response_path: Path,
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
    payload: dict[str, Any] = {
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
    atomic_json(response_path, payload)
    payload["response_path"] = rel_to_repo(repo_root, response_path)
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
        stem = request_path.stem
        if re.fullmatch(contract["request_id_pattern"], stem):
            request_id = stem
            request["request_id"] = stem
        else:
            raise BridgeFatal(
                f"malformed request has no recoverable request_id: {request_path}"
            )

    response_path = response_path_for(request_id, response_dir, contract)
    if response_path.exists():
        existing = load_json(response_path)
        if existing.get("request_sha256") != request_sha:
            raise BridgeFatal(
                f"request was modified after immutable response: {request_path}"
            )
        return {
            "request_id": request_id,
            "status": "ALREADY_RESPONDED",
            "response_path": rel_to_repo(repo_root, response_path),
        }

    preflight: dict[str, Any] | None = None
    execution: dict[str, Any] | None = None
    postflight: dict[str, Any] | None = None
    next_guard: dict[str, Any] | None = None

    try:
        definition = validate_request(request_path, request, contract)
        slot_id = request.get("slot_id")
        preflight = resume_query(
            repo_root, registry_dir, program_root, tracker, slot_id
        )

        if request["command"] == "RESUME":
            next_guard = guard_for_packet(
                preflight, registry_dir, program_root, tracker
            )
            return write_response(
                response_path,
                request=request,
                request_sha=request_sha,
                status="EXECUTED",
                preflight=preflight,
                execution={
                    "ok": True,
                    "command": "RESUME",
                    "returncode": 0,
                    "controller_payload": preflight,
                },
                postflight=preflight,
                next_guard=next_guard,
                error=None,
                repo_root=repo_root,
            )

        if definition["mutation"] is not True:
            raise BridgeFatal(
                f"contract marks non-RESUME command as non-mutating: {request['command']}"
            )
        execution = execute_mutation(
            request,
            preflight,
            registry_dir,
            program_root,
            tracker,
        )
        if execution.get("ok") is not True:
            try:
                postflight = resume_query(
                    repo_root, registry_dir, program_root, tracker, slot_id
                )
                next_guard = guard_for_packet(
                    postflight, registry_dir, program_root, tracker
                )
            except BridgeFatal:
                postflight = None
                next_guard = None
            return write_response(
                response_path,
                request=request,
                request_sha=request_sha,
                status="REJECTED",
                preflight=preflight,
                execution=execution,
                postflight=postflight,
                next_guard=next_guard,
                error="authoritative Runtime controller rejected the request",
                repo_root=repo_root,
            )

        postflight = resume_query(
            repo_root, registry_dir, program_root, tracker, slot_id
        )
        next_guard = guard_for_packet(
            postflight, registry_dir, program_root, tracker
        )
        return write_response(
            response_path,
            request=request,
            request_sha=request_sha,
            status="EXECUTED",
            preflight=preflight,
            execution=execution,
            postflight=postflight,
            next_guard=next_guard,
            error=None,
            repo_root=repo_root,
        )
    except BridgeFatal as exc:
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


def request_paths(request_dir: Path) -> list[Path]:
    if not request_dir.is_dir():
        return []
    return sorted(path for path in request_dir.glob("*.json") if path.is_file())


def process_pending(args: argparse.Namespace) -> None:
    repo_root = args.repo_root.resolve()
    registry_dir = args.registry_dir.resolve()
    contract = load_contract(registry_dir)
    validate_contract(contract)

    program_root = resolve_repo_path(
        repo_root, args.program_root or contract["program_root"]
    )
    tracker = resolve_repo_path(repo_root, args.tracker or contract["tracker_path"])
    request_dir = resolve_repo_path(
        repo_root, args.request_dir or contract["request_directory"]
    )
    response_dir = resolve_repo_path(
        repo_root, args.response_dir or contract["response_directory"]
    )
    if not tracker.is_file():
        raise BridgeFatal(f"tracker is missing: {tracker}")

    results: list[dict[str, Any]] = []
    for path in request_paths(request_dir):
        results.append(
            process_one(
                path,
                response_dir,
                contract,
                repo_root,
                registry_dir,
                program_root,
                tracker,
            )
        )
    print(
        json.dumps(
            {
                "ok": True,
                "mode": "process-pending",
                "request_count": len(results),
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="GitHub request/response execution bridge for canonical MV Runtime."
    )
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
    except BridgeFatal as exc:
        print(
            json.dumps(
                {"ok": False, "error": str(exc)},
                ensure_ascii=False,
                indent=2,
            )
        )
        raise SystemExit(1)


if __name__ == "__main__":
    main()
