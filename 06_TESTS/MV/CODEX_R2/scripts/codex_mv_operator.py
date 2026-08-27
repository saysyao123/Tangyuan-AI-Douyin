#!/usr/bin/env python3
"""Codex-local operator for the Tangyuan Canonical MV Runtime.

This is a transport adapter, not a state authority. It reuses the existing
Canonical Runtime and Lean macro controller functions directly from a Codex
checkout so Codex does not need the ChatGPT-Web request/Actions/response loop.

Normal commands:
  preflight
  resume --slot D03-B
  init --slot D03-B
  accept-gate --slot D03-B --gate HG01 --decision '...' --approved path
  run-until --slot D03-B
  advance --slot D03-B --to Sxx_...
  update-context --slot D03-B --key multi_shot --value true --reason '...'
  rollback --slot D03-B --change-type ... --reason '...'

No publish-sync command is exposed intentionally. Publication requires explicit
real-world confirmation and remains a separate high-risk boundary.
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPT = Path(__file__).resolve()
REPO_ROOT = SCRIPT.parents[4]
TOOLS_DIR = REPO_ROOT / "04_HARNESS" / "tools"
RUNTIME_DIR = REPO_ROOT / "04_HARNESS" / "runtime"
CODEX_DIR = SCRIPT.parent.parent
TEST_CONTRACT_PATH = CODEX_DIR / "CODEX_R2_TEST_CONTRACT.json"

sys.path.insert(0, str(TOOLS_DIR))
import mv_runtime_bridge as core  # noqa: E402
import mv_runtime_lean_bridge as lean  # noqa: E402


class CodexOperatorError(RuntimeError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CodexOperatorError(f"invalid JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CodexOperatorError(f"JSON root must be object: {path}")
    return value


def contract() -> dict[str, Any]:
    return load_json(TEST_CONTRACT_PATH)


def run_text(cmd: list[str]) -> tuple[int, str, str]:
    p = subprocess.run(cmd, cwd=REPO_ROOT, text=True, capture_output=True)
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()


def git_branch() -> str:
    code, out, err = run_text(["git", "branch", "--show-current"])
    if code != 0:
        raise CodexOperatorError(f"git branch check failed: {err}")
    return out


def git_head() -> str:
    code, out, err = run_text(["git", "rev-parse", "HEAD"])
    if code != 0:
        raise CodexOperatorError(f"git HEAD check failed: {err}")
    return out


def ensure_branch() -> str:
    cfg = contract()
    expected = str(cfg["branch"])
    actual = git_branch()
    if actual != expected:
        raise CodexOperatorError(
            f"wrong branch: expected={expected!r} actual={actual!r}; do not mutate Runtime truth"
        )
    return actual


def paths(cfg: dict[str, Any]) -> tuple[Path, Path]:
    program_root = REPO_ROOT / str(cfg["program_root"])
    tracker = REPO_ROOT / str(cfg["tracker_path"])
    return program_root, tracker


def lean_contract() -> dict[str, Any]:
    value = lean.load_contract(RUNTIME_DIR)
    lean.validate_contract(value)
    return value


def resume_raw(slot: str) -> dict[str, Any]:
    cfg = contract()
    program_root, tracker = paths(cfg)
    return core.resume_query(REPO_ROOT, RUNTIME_DIR, program_root, tracker, slot)


def resume_enriched(slot: str) -> tuple[dict[str, Any], dict[str, Any]]:
    cfg = contract()
    program_root, tracker = paths(cfg)
    packet = resume_raw(slot)
    enriched = lean.enrich_packet(packet, RUNTIME_DIR, lean_contract())
    guard = core.guard_for_packet(packet, RUNTIME_DIR, program_root, tracker)
    enriched["next_guard"] = guard
    return packet, enriched


def print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False))


def mutation_request(command: str, slot: str, payload: dict[str, Any], guard: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "command": command,
        "slot_id": slot,
        "payload": payload,
        "expected_guard": guard,
        "requested_by": "codex",
        "reason": "Codex R2 local operator command using fresh canonical guard",
    }


def postflight(slot: str, execution: dict[str, Any]) -> dict[str, Any]:
    _raw, enriched = resume_enriched(slot)
    return {"execution": execution, "postflight": enriched}


def command_preflight(_args: argparse.Namespace) -> int:
    cfg = contract()
    expected_branch = str(cfg["branch"])
    actual_branch = git_branch()
    head = git_head()
    program_root, tracker = paths(cfg)
    required = [
        RUNTIME_DIR / "mv_stage_registry.json",
        RUNTIME_DIR / "mv_resume_contract.json",
        RUNTIME_DIR / "mv_stage_executor_registry.json",
        RUNTIME_DIR / "mv_lean_runtime_contract.json",
        TOOLS_DIR / "mv_runtime_state.py",
        TOOLS_DIR / "mv_runtime_bridge.py",
        TOOLS_DIR / "mv_runtime_lean_bridge.py",
        TOOLS_DIR / "mv_audio_timeline" / "package_tool.py",
        TOOLS_DIR / "mv_audio_timeline" / "final_gate.py",
        TOOLS_DIR / "mv_audio_timeline" / "lightweight_align.py",
        tracker,
        program_root,
    ]
    missing = [str(p.relative_to(REPO_ROOT)) for p in required if not p.exists()]

    row = None
    if tracker.is_file():
        with tracker.open("r", encoding="utf-8-sig", newline="") as handle:
            for item in csv.DictReader(handle):
                if item.get("slot_id") == cfg["target_slot"]:
                    row = item
                    break

    tools: dict[str, Any] = {
        "git": shutil.which("git"),
        "python": sys.executable,
        "python_version": platform.python_version(),
        "ffmpeg": shutil.which("ffmpeg"),
        "ffprobe": shutil.which("ffprobe"),
        "faster_whisper_importable": importlib.util.find_spec("faster_whisper") is not None,
    }
    _c, dirty, _e = run_text(["git", "status", "--porcelain"])

    errors: list[str] = []
    warnings: list[str] = []
    if actual_branch != expected_branch:
        errors.append(f"wrong branch: expected {expected_branch}, got {actual_branch or '<detached>'}")
    if missing:
        errors.append(f"missing required repository paths: {missing}")
    if row is None:
        errors.append(f"target slot {cfg['target_slot']} missing from tracker")
    elif row.get("lane") != cfg["target_lane"]:
        errors.append(
            f"target lane mismatch: tracker={row.get('lane')} contract={cfg['target_lane']}"
        )
    if not tools["ffmpeg"] or not tools["ffprobe"]:
        warnings.append("ffmpeg/ffprobe unavailable; media phases will be blocked until environment is prepared")
    if not tools["faster_whisper_importable"]:
        warnings.append("faster-whisper unavailable; P1 cannot run locally, but P0 may still pass and P2 remains conditional")
    if dirty:
        warnings.append("worktree is not clean at preflight")

    status = "BLOCKED" if errors else ("PARTIAL" if warnings else "PASS")
    report = {
        "status": status,
        "branch": {"expected": expected_branch, "actual": actual_branch, "head": head},
        "target": {"slot": cfg["target_slot"], "lane": cfg["target_lane"], "tracker_row": row},
        "required_paths_missing": missing,
        "tools": tools,
        "worktree_dirty": bool(dirty),
        "errors": errors,
        "warnings": warnings,
        "note": "preflight never installs dependencies and never mutates canonical Runtime state",
    }
    print_json(report)
    return 2 if errors else 0


def command_resume(args: argparse.Namespace) -> int:
    ensure_branch()
    _raw, enriched = resume_enriched(args.slot)
    print_json(enriched)
    return 0


def command_init(args: argparse.Namespace) -> int:
    ensure_branch()
    cfg = contract()
    program_root, tracker = paths(cfg)
    preflight, enriched = resume_enriched(args.slot)
    if preflight.get("mode") != "ALLOCATE_NEW_SLOT":
        raise CodexOperatorError(
            f"init requires ALLOCATE_NEW_SLOT; fresh mode={preflight.get('mode')} stage={preflight.get('current_stage')}"
        )
    if preflight.get("slot_id") != args.slot:
        raise CodexOperatorError(f"allocation selected different slot: {preflight.get('slot_id')}")
    guard = enriched["next_guard"]
    payload = {
        "program": cfg["program"],
        "web": bool(cfg["initial_context"]["web"]),
        "multi_shot": bool(cfg["initial_context"]["multi_shot"]),
        "program_30d60": bool(cfg["initial_context"]["program_30d60"]),
    }
    req = mutation_request("INIT_SLOT", args.slot, payload, guard)
    result = core.execute_mutation(req, preflight, RUNTIME_DIR, program_root, tracker)
    print_json(postflight(args.slot, result))
    return 0 if result.get("ok") else 3


def command_accept_gate(args: argparse.Namespace) -> int:
    ensure_branch()
    cfg = contract()
    program_root, _tracker = paths(cfg)
    preflight, enriched = resume_enriched(args.slot)
    if preflight.get("mode") != "RESUME_CANONICAL":
        raise CodexOperatorError(f"accept-gate requires canonical slot; mode={preflight.get('mode')}")
    req = mutation_request(
        "ACCEPT_GATE",
        args.slot,
        {
            "gate": args.gate,
            "user_decision_text": args.decision,
            "approved_artifacts": args.approved,
        },
        enriched["next_guard"],
    )
    result = lean.execute_accept_gate(req, preflight, RUNTIME_DIR, program_root)
    print_json(postflight(args.slot, result))
    return 0 if result.get("ok") else 3


def command_run_until(args: argparse.Namespace) -> int:
    ensure_branch()
    cfg = contract()
    program_root, tracker = paths(cfg)
    preflight, enriched = resume_enriched(args.slot)
    if preflight.get("mode") != "RESUME_CANONICAL":
        raise CodexOperatorError(f"run-until requires canonical slot; mode={preflight.get('mode')}")
    req = mutation_request(
        "RUN_UNTIL_GATE_OR_BLOCK",
        args.slot,
        {"max_steps": args.max_steps},
        enriched["next_guard"],
    )
    result = lean.execute_run_until(
        req, preflight, RUNTIME_DIR, program_root, tracker, lean_contract()
    )
    print_json(postflight(args.slot, result))
    return 0 if result.get("ok") else 3


def command_advance(args: argparse.Namespace) -> int:
    ensure_branch()
    cfg = contract()
    program_root, tracker = paths(cfg)
    preflight, enriched = resume_enriched(args.slot)
    req = mutation_request("ADVANCE", args.slot, {"to": args.to}, enriched["next_guard"])
    result = core.execute_mutation(req, preflight, RUNTIME_DIR, program_root, tracker)
    print_json(postflight(args.slot, result))
    return 0 if result.get("ok") else 3


def parse_bool(value: str) -> bool:
    v = value.strip().lower()
    if v in {"true", "1", "yes", "on"}:
        return True
    if v in {"false", "0", "no", "off"}:
        return False
    raise argparse.ArgumentTypeError("value must be true/false")


def command_update_context(args: argparse.Namespace) -> int:
    ensure_branch()
    cfg = contract()
    program_root, tracker = paths(cfg)
    preflight, enriched = resume_enriched(args.slot)
    req = mutation_request(
        "UPDATE_CONTEXT",
        args.slot,
        {"key": args.key, "value": args.value, "reason": args.reason},
        enriched["next_guard"],
    )
    result = core.execute_mutation(req, preflight, RUNTIME_DIR, program_root, tracker)
    print_json(postflight(args.slot, result))
    return 0 if result.get("ok") else 3


def command_rollback(args: argparse.Namespace) -> int:
    ensure_branch()
    cfg = contract()
    program_root, tracker = paths(cfg)
    preflight, enriched = resume_enriched(args.slot)
    payload: dict[str, Any] = {"change_type": args.change_type, "reason": args.reason}
    if args.authority:
        payload["authority"] = args.authority
    req = mutation_request("ROLLBACK", args.slot, payload, enriched["next_guard"])
    result = core.execute_mutation(req, preflight, RUNTIME_DIR, program_root, tracker)
    print_json(postflight(args.slot, result))
    return 0 if result.get("ok") else 3


def build_parser() -> argparse.ArgumentParser:
    cfg = contract()
    default_slot = str(cfg["target_slot"])
    parser = argparse.ArgumentParser(description="Codex-local facade over Tangyuan Canonical/Lean MV Runtime")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("preflight", help="read-only Codex/environment/runtime preflight")
    p.set_defaults(func=command_preflight)

    p = sub.add_parser("resume", help="read-only canonical resume with resolved executor and fresh guard")
    p.add_argument("--slot", default=default_slot)
    p.set_defaults(func=command_resume)

    p = sub.add_parser("init", help="initialize only after a fresh ALLOCATE_NEW_SLOT result")
    p.add_argument("--slot", default=default_slot)
    p.set_defaults(func=command_init)

    p = sub.add_parser("accept-gate", help="record a real user Human Gate decision and advance transactionally")
    p.add_argument("--slot", default=default_slot)
    p.add_argument("--gate", required=True)
    p.add_argument("--decision", required=True, help="exact current user approval/selection text")
    p.add_argument("--approved", action="append", required=True, help="approved artifact path; repeat as needed")
    p.set_defaults(func=command_accept_gate)

    p = sub.add_parser("run-until", help="advance already-valid machine stages until Human Gate/handoff/block/S16")
    p.add_argument("--slot", default=default_slot)
    p.add_argument("--max-steps", type=int, default=8)
    p.set_defaults(func=command_run_until)

    p = sub.add_parser("advance", help="single canonical advance for debugging/repair; prefer run-until normally")
    p.add_argument("--slot", default=default_slot)
    p.add_argument("--to", required=True)
    p.set_defaults(func=command_advance)

    p = sub.add_parser("update-context", help="update a canonical boolean context flag with receipt")
    p.add_argument("--slot", default=default_slot)
    p.add_argument("--key", required=True)
    p.add_argument("--value", required=True, type=parse_bool)
    p.add_argument("--reason", required=True)
    p.set_defaults(func=command_update_context)

    p = sub.add_parser("rollback", help="invoke canonical revision/rollback controller")
    p.add_argument("--slot", default=default_slot)
    p.add_argument("--change-type", required=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--authority")
    p.set_defaults(func=command_rollback)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except (CodexOperatorError, core.BridgeFatal, lean.LeanFatal) as exc:
        print_json({"ok": False, "error": type(exc).__name__, "message": str(exc)})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
