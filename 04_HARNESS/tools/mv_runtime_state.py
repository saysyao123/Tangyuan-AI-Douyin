#!/usr/bin/env python3
"""Canonical MV Runtime state controller.

This tool mutates state only for canonical_v2 slots. Validation stays delegated to
mv_runtime_gate.py. Historical R1/R2/R3 slots remain read-only audit fixtures.

Commands:
- init-slot
- record-human-gate
- advance
- verify-state
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import mv_runtime_gate as gate


SCRIPT_PATH = Path(__file__).resolve()
RUNTIME_DIR = SCRIPT_PATH.parent.parent / "runtime"
HUMAN_GATE_REGISTRY = "mv_human_gate_registry.json"
TRANSITION_CONTRACT = "mv_transition_contract.json"
SCAFFOLD_REGISTRY = "mv_slot_scaffold.json"


def out(payload: dict[str, Any], code: int = 0) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(code)


def fail(message: str, details: Any = None, code: int = 1) -> None:
    payload: dict[str, Any] = {"ok": False, "error": message}
    if details is not None:
        payload["details"] = details
    out(payload, code)


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
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"invalid or missing JSON: {path}", str(exc), 2)
    if not isinstance(payload, dict):
        fail(f"JSON root must be object: {path}", code=2)
    return payload


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temp, path)


def load_runtime(registry_dir: Path) -> dict[str, Any]:
    stage_registry, artifact_registry = gate.load_registries(registry_dir)
    return {
        "stage_registry": stage_registry,
        "artifact_registry": artifact_registry,
        "human_gate_registry": load_json(registry_dir / HUMAN_GATE_REGISTRY),
        "transition_contract": load_json(registry_dir / TRANSITION_CONTRACT),
        "scaffold": load_json(registry_dir / SCAFFOLD_REGISTRY),
    }


def stages(runtime: dict[str, Any]) -> list[dict[str, Any]]:
    return gate.sorted_stages(runtime["stage_registry"])


def stage_index(runtime: dict[str, Any]) -> dict[str, int]:
    return {item["id"]: index for index, item in enumerate(stages(runtime))}


def artifacts(runtime: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return gate.index_by_id(runtime["artifact_registry"]["artifacts"], "artifact")


def human_gates(runtime: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return gate.index_by_id(runtime["human_gate_registry"]["gates"], "human gate")


def state_path(slot_root: Path, runtime: dict[str, Any]) -> Path:
    return slot_root / runtime["scaffold"]["state_path"]


def manifest_path(slot_root: Path, runtime: dict[str, Any]) -> Path:
    return slot_root / runtime["scaffold"]["slot_manifest_path"]


def load_canonical_state(slot_root: Path, runtime: dict[str, Any]) -> dict[str, Any]:
    path = state_path(slot_root, runtime)
    state = load_json(path)
    required = runtime["transition_contract"].get("state_required_fields") or []
    missing = [key for key in required if key not in state]
    if missing:
        fail("canonical state missing required fields", missing)
    if state.get("runtime_mode") != "canonical_v2":
        fail("state mutation is allowed only for canonical_v2 slots")
    context = state.get("context")
    if not isinstance(context, dict) or context.get("canonical_v2") is not True:
        fail("canonical_v2 state must carry context.canonical_v2=true")
    return state


def canonical_audit(
    slot_root: Path,
    runtime: dict[str, Any],
    context: dict[str, bool],
    target_stage: str,
) -> dict[str, Any]:
    report = gate.audit_slot(
        slot_root,
        runtime["stage_registry"],
        runtime["artifact_registry"],
        context,
        stop_at=target_stage,
    )
    legacy = {
        artifact_id: item
        for artifact_id, item in report.get("artifacts", {}).items()
        if item.get("source") == "legacy"
    }
    if legacy:
        report["ok"] = False
        report["canonical_v2_error"] = "legacy artifact aliases are not accepted in canonical_v2 state transitions"
        report["legacy_artifacts"] = legacy
    return report


def evidence_snapshot(slot_root: Path, report: dict[str, Any]) -> list[dict[str, str]]:
    snapshot: list[dict[str, str]] = []
    for artifact_id, item in sorted(report.get("artifacts", {}).items()):
        if not item.get("ok") or not item.get("path"):
            continue
        path = slot_root / item["path"]
        snapshot.append(
            {
                "artifact_id": artifact_id,
                "path": item["path"],
                "sha256": sha256_file(path),
            }
        )
    return snapshot


def receipt_relpath(sequence: int, from_stage: str | None, to_stage: str, runtime: dict[str, Any]) -> str:
    directory = runtime["transition_contract"]["receipt_directory"]
    if sequence == 0:
        return f"{directory}/{runtime['transition_contract']['initial_receipt_name']}"
    return f"{directory}/{sequence:03d}_{from_stage}__{to_stage}.json"


def init_slot(args: argparse.Namespace, runtime: dict[str, Any]) -> None:
    slot_root = args.slot_root.resolve()
    if slot_root.exists() and any(slot_root.iterdir()):
        fail("slot root already exists and is not empty", str(slot_root))
    slot_root.mkdir(parents=True, exist_ok=True)
    for rel in runtime["scaffold"]["directories"]:
        (slot_root / rel).mkdir(parents=True, exist_ok=True)

    context = dict(runtime["scaffold"]["defaults"])
    context.update(
        {
            "web": args.web,
            "multi_shot": args.multi_shot,
            "program_30d60": args.program_30d60,
            "canonical_v2": True,
        }
    )
    created = now_iso()
    manifest = {
        "schema_version": "1.0",
        "runtime_schema_version": runtime["scaffold"]["runtime_schema_version"],
        "runtime_mode": "canonical_v2",
        "slot_id": args.slot_id,
        "program": args.program,
        "lane": args.lane,
        "context": context,
        "created_at": created,
    }
    mpath = manifest_path(slot_root, runtime)
    atomic_json(mpath, manifest)

    initial_stage = runtime["scaffold"]["initial_stage"]
    initial_token = runtime["scaffold"]["initial_state_token"]
    initial_rel = receipt_relpath(0, None, initial_stage, runtime)
    initial_path = slot_root / initial_rel
    initial_receipt = {
        "receipt_version": "1.0",
        "sequence": 0,
        "slot_id": args.slot_id,
        "from_stage": None,
        "to_stage": initial_stage,
        "to_state_token": initial_token,
        "previous_receipt_sha256": None,
        "state_before_sha256": None,
        "evidence_validation": {"ok": True, "mode": "slot_init"},
        "evidence_snapshot": [
            {
                "artifact_id": "SLOT_MANIFEST",
                "path": str(mpath.relative_to(slot_root)),
                "sha256": sha256_file(mpath),
            }
        ],
        "created_at": created,
    }
    atomic_json(initial_path, initial_receipt)
    initial_hash = sha256_file(initial_path)

    state = {
        "runtime_schema_version": runtime["scaffold"]["runtime_schema_version"],
        "runtime_mode": "canonical_v2",
        "slot_id": args.slot_id,
        "program": args.program,
        "lane": args.lane,
        "current_stage": initial_stage,
        "current_state_token": initial_token,
        "status": initial_token,
        "transition_sequence": 0,
        "last_transition_receipt": initial_rel,
        "last_transition_receipt_sha256": initial_hash,
        "context": context,
        "created_at": created,
        "updated_at": created,
    }
    atomic_json(state_path(slot_root, runtime), state)

    report = canonical_audit(slot_root, runtime, context, initial_stage)
    if not report.get("ok"):
        fail("initialized slot failed S00 validation", report)
    out(
        {
            "ok": True,
            "slot_root": str(slot_root),
            "slot_id": args.slot_id,
            "stage": initial_stage,
            "state_token": initial_token,
            "transition_receipt": initial_rel,
        }
    )


def verify_state_internal(slot_root: Path, runtime: dict[str, Any]) -> dict[str, Any]:
    state = load_canonical_state(slot_root, runtime)
    stage_list = stages(runtime)
    indexes = stage_index(runtime)
    current_stage = state["current_stage"]
    if current_stage not in indexes:
        fail("state references unknown current_stage", current_stage)
    expected_sequence = indexes[current_stage]
    if state.get("transition_sequence") != expected_sequence:
        fail(
            "transition_sequence does not match current stage index",
            {"expected": expected_sequence, "actual": state.get("transition_sequence")},
        )

    previous_hash: str | None = None
    last_rel: str | None = None
    checked_receipts: list[str] = []
    for sequence in range(expected_sequence + 1):
        to_stage = stage_list[sequence]["id"]
        from_stage = None if sequence == 0 else stage_list[sequence - 1]["id"]
        rel = receipt_relpath(sequence, from_stage, to_stage, runtime)
        path = slot_root / rel
        receipt = load_json(path)
        if receipt.get("sequence") != sequence:
            fail("transition receipt sequence mismatch", rel)
        if receipt.get("from_stage") != from_stage or receipt.get("to_stage") != to_stage:
            fail("transition receipt stage mismatch", rel)
        if receipt.get("previous_receipt_sha256") != previous_hash:
            fail("transition receipt hash chain mismatch", rel)
        if receipt.get("evidence_validation", {}).get("ok") is not True:
            fail("transition receipt does not contain PASS evidence validation", rel)
        for item in receipt.get("evidence_snapshot") or []:
            evidence_path = slot_root / item.get("path", "")
            if not evidence_path.is_file():
                fail("transition evidence file missing", {"receipt": rel, "path": item.get("path")})
            if sha256_file(evidence_path) != item.get("sha256"):
                fail("transition evidence hash changed after lock", {"receipt": rel, "path": item.get("path")})
        previous_hash = sha256_file(path)
        last_rel = rel
        checked_receipts.append(rel)

    if state.get("last_transition_receipt") != last_rel:
        fail("state last_transition_receipt mismatch")
    if state.get("last_transition_receipt_sha256") != previous_hash:
        fail("state last_transition_receipt_sha256 mismatch")
    expected_token = stage_list[expected_sequence]["state_token"]
    if state.get("current_state_token") != expected_token or state.get("status") != expected_token:
        fail("state token/status does not match canonical stage")

    context = dict(state["context"])
    report = canonical_audit(slot_root, runtime, context, current_stage)
    if not report.get("ok"):
        fail("current canonical evidence chain does not validate", report)

    return {
        "ok": True,
        "slot_id": state["slot_id"],
        "current_stage": current_stage,
        "current_state_token": expected_token,
        "transition_sequence": expected_sequence,
        "checked_transition_receipts": checked_receipts,
        "highest_contiguous_valid_stage": report.get("highest_contiguous_valid_stage"),
    }


def verify_state(args: argparse.Namespace, runtime: dict[str, Any]) -> None:
    out(verify_state_internal(args.slot_root.resolve(), runtime))


def record_human_gate(args: argparse.Namespace, runtime: dict[str, Any]) -> None:
    slot_root = args.slot_root.resolve()
    verify_state_internal(slot_root, runtime)
    state = load_canonical_state(slot_root, runtime)
    gate_defs = human_gates(runtime)
    if args.gate not in gate_defs:
        fail("unknown human gate", args.gate, 2)
    definition = gate_defs[args.gate]
    target_stage = definition["stage_id"]
    stage_list = stages(runtime)
    indexes = stage_index(runtime)
    target_index = indexes[target_stage]
    if target_index == 0:
        fail("human gate cannot target S00", code=2)
    expected_from = stage_list[target_index - 1]["id"]
    if state["current_stage"] != expected_from:
        fail(
            "human gate can only be recorded when its immediate upstream stage is current",
            {"current_stage": state["current_stage"], "expected": expected_from, "gate": args.gate},
        )
    if args.decision != "PASS":
        fail("only PASS receipts unlock a canonical stage; rejected options remain discussion evidence")
    if not args.user_decision_text.strip():
        fail("user_decision_text must be non-empty")
    if not args.approved_artifact:
        fail("at least one --approved-artifact is required")

    context = dict(state["context"])
    upstream = canonical_audit(slot_root, runtime, context, expected_from)
    if not upstream.get("ok"):
        fail("human gate upstream chain is not machine-valid", upstream)

    artifact_defs = artifacts(runtime)
    machine_evidence: list[dict[str, str]] = []
    for artifact_id in definition.get("machine_preflight_artifacts") or []:
        result = gate.check_artifact(slot_root, artifact_defs[artifact_id])
        if not result.ok or result.source != "canonical" or not result.path:
            fail(
                "human gate machine preflight artifact missing or non-canonical",
                {"gate": args.gate, "artifact": artifact_id, "result": result.__dict__},
            )
        path = slot_root / result.path
        machine_evidence.append(
            {"artifact_id": artifact_id, "path": result.path, "sha256": sha256_file(path)}
        )

    receipt_artifact_id = definition["receipt_artifact_id"]
    receipt_def = artifact_defs[receipt_artifact_id]
    receipt_path = slot_root / receipt_def["canonical_path"]
    if receipt_path.exists():
        fail("canonical human gate receipt already exists and is immutable", str(receipt_path))

    payload = {
        "receipt_version": "1.0",
        "gate_id": args.gate,
        "stage_id": target_stage,
        "decision": "PASS",
        "user_decision_text": args.user_decision_text,
        "approved_artifacts": args.approved_artifact,
        "machine_evidence": machine_evidence,
        "state_stage_before": expected_from,
        "created_at": now_iso(),
    }
    atomic_json(receipt_path, payload)
    result = gate.check_artifact(slot_root, receipt_def)
    if not result.ok or result.source != "canonical":
        receipt_path.unlink(missing_ok=True)
        fail("generated human gate receipt failed artifact validation", result.__dict__)
    out(
        {
            "ok": True,
            "gate": args.gate,
            "stage_id": target_stage,
            "receipt": str(receipt_path.relative_to(slot_root)),
            "state_advanced": False,
            "next_action": f"advance --to {target_stage}",
        }
    )


def advance(args: argparse.Namespace, runtime: dict[str, Any]) -> None:
    slot_root = args.slot_root.resolve()
    verify_state_internal(slot_root, runtime)
    state_file = state_path(slot_root, runtime)
    state_before_bytes = state_file.read_bytes()
    state_before_hash = hashlib.sha256(state_before_bytes).hexdigest()
    state = load_canonical_state(slot_root, runtime)
    stage_list = stages(runtime)
    indexes = stage_index(runtime)
    current_index = indexes[state["current_stage"]]
    if current_index >= len(stage_list) - 1:
        fail("slot is already at the final registered stage")
    target = stage_list[current_index + 1]
    if args.to is not None and args.to != target["id"]:
        fail(
            "stage skipping is forbidden; only the immediate next stage may advance",
            {"current": state["current_stage"], "allowed_next": target["id"], "requested": args.to},
        )

    context = dict(state["context"])
    report = canonical_audit(slot_root, runtime, context, target["id"])
    if not report.get("ok"):
        fail("target stage evidence validation failed; state not advanced", report)

    sequence = current_index + 1
    previous_rel = state["last_transition_receipt"]
    previous_hash = state["last_transition_receipt_sha256"]
    rel = receipt_relpath(sequence, state["current_stage"], target["id"], runtime)
    receipt_path = slot_root / rel
    if receipt_path.exists():
        fail("transition receipt path already exists; revisions require a future controlled rollback/attempt flow", rel)

    transition = {
        "receipt_version": "1.0",
        "sequence": sequence,
        "slot_id": state["slot_id"],
        "from_stage": state["current_stage"],
        "to_stage": target["id"],
        "to_state_token": target["state_token"],
        "previous_receipt": previous_rel,
        "previous_receipt_sha256": previous_hash,
        "state_before_sha256": state_before_hash,
        "evidence_validation": {
            "ok": True,
            "target_stage": target["id"],
            "highest_contiguous_valid_stage": report.get("highest_contiguous_valid_stage"),
            "canonical_v2": True,
        },
        "evidence_snapshot": evidence_snapshot(slot_root, report),
        "created_at": now_iso(),
    }
    atomic_json(receipt_path, transition)
    transition_hash = sha256_file(receipt_path)

    new_state = dict(state)
    new_state.update(
        {
            "current_stage": target["id"],
            "current_state_token": target["state_token"],
            "status": target["state_token"],
            "transition_sequence": sequence,
            "last_transition_receipt": rel,
            "last_transition_receipt_sha256": transition_hash,
            "updated_at": now_iso(),
        }
    )
    atomic_json(state_file, new_state)
    try:
        verified = verify_state_internal(slot_root, runtime)
    except SystemExit:
        state_file.write_bytes(state_before_bytes)
        receipt_path.unlink(missing_ok=True)
        raise
    out(
        {
            "ok": True,
            "from_stage": state["current_stage"],
            "to_stage": target["id"],
            "state_token": target["state_token"],
            "transition_receipt": rel,
            "verified": verified,
        }
    )


def bool_arg(value: str) -> bool:
    value = value.lower().strip()
    if value in {"true", "1", "yes", "y"}:
        return True
    if value in {"false", "0", "no", "n"}:
        return False
    raise argparse.ArgumentTypeError("expected true/false")


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Machine-controlled state transitions for canonical MV Runtime slots.")
    p.add_argument("--registry-dir", type=Path, default=RUNTIME_DIR)
    sub = p.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init-slot")
    init.add_argument("--slot-root", required=True, type=Path)
    init.add_argument("--slot-id", required=True)
    init.add_argument("--program", required=True)
    init.add_argument("--lane", required=True)
    init.add_argument("--web", type=bool_arg, default=True)
    init.add_argument("--multi-shot", type=bool_arg, default=False)
    init.add_argument("--program-30d60", type=bool_arg, default=True)

    receipt = sub.add_parser("record-human-gate")
    receipt.add_argument("--slot-root", required=True, type=Path)
    receipt.add_argument("--gate", required=True)
    receipt.add_argument("--decision", default="PASS", choices=["PASS"])
    receipt.add_argument("--user-decision-text", required=True)
    receipt.add_argument("--approved-artifact", action="append", default=[])

    advance_parser = sub.add_parser("advance")
    advance_parser.add_argument("--slot-root", required=True, type=Path)
    advance_parser.add_argument("--to")

    verify = sub.add_parser("verify-state")
    verify.add_argument("--slot-root", required=True, type=Path)

    return p


def main() -> None:
    args = parser().parse_args()
    runtime = load_runtime(args.registry_dir.resolve())
    if args.command == "init-slot":
        init_slot(args, runtime)
    elif args.command == "record-human-gate":
        record_human_gate(args, runtime)
    elif args.command == "advance":
        advance(args, runtime)
    elif args.command == "verify-state":
        verify_state(args, runtime)
    else:
        fail("unknown command", args.command, 2)


if __name__ == "__main__":
    main()
