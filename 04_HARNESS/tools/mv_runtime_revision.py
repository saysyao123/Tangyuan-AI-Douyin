#!/usr/bin/env python3
"""Controlled rollback/revision controller for canonical MV Runtime slots.

Rollback is not deletion. The controller:
1. verifies the current canonical state/hash chain;
2. maps an explicit change_type to one minimal upstream target;
3. archives downstream canonical artifacts, transition receipts and context events;
4. writes an immutable rollback receipt with SHA-256 archive inventory;
5. resets CURRENT_STATE to the still-valid target stage;
6. re-verifies active state and independent revision history.

Published states S17/S18 are intentionally not reversible by this tool.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
from pathlib import Path
from typing import Any

import mv_runtime_state as statectl

SCRIPT_PATH = Path(__file__).resolve()
RUNTIME_DIR = SCRIPT_PATH.parent.parent / "runtime"
REVISION_CONTRACT_NAME = "mv_revision_contract.json"


def emit(payload: dict[str, Any], code: int = 0) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(code)


def fail(message: str, details: Any = None, code: int = 1) -> None:
    payload: dict[str, Any] = {"ok": False, "error": message}
    if details is not None:
        payload["details"] = details
    emit(payload, code)


def load_contract(registry_dir: Path) -> dict[str, Any]:
    return statectl.load_json(registry_dir / REVISION_CONTRACT_NAME)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stage_list(runtime: dict[str, Any]) -> list[dict[str, Any]]:
    return statectl.stages(runtime)


def stage_indexes(runtime: dict[str, Any]) -> dict[str, int]:
    return {stage["id"]: index for index, stage in enumerate(stage_list(runtime))}


def artifact_stage_index(runtime: dict[str, Any]) -> dict[str, int]:
    mapping: dict[str, int] = {}
    for index, stage in enumerate(stage_list(runtime)):
        ids = list(stage.get("required_artifacts") or [])
        for conditional in stage.get("conditional_requirements") or []:
            ids.extend(conditional.get("required_artifacts") or [])
        for artifact_id in ids:
            if artifact_id not in mapping or index < mapping[artifact_id]:
                mapping[artifact_id] = index
    return mapping


def revision_root(slot_root: Path, contract: dict[str, Any]) -> Path:
    return slot_root / contract["revision_directory"]


def revision_dirs(slot_root: Path, contract: dict[str, Any]) -> list[Path]:
    root = revision_root(slot_root, contract)
    if not root.is_dir():
        return []
    values = [p for p in root.iterdir() if p.is_dir() and re.match(r"^R\d{3}_", p.name)]
    return sorted(values, key=lambda p: p.name)


def next_revision_identity(slot_root: Path, contract: dict[str, Any], change_type: str) -> tuple[int, Path]:
    dirs = revision_dirs(slot_root, contract)
    sequence = len(dirs) + 1
    target = revision_root(slot_root, contract) / f"R{sequence:03d}_{change_type}"
    if target.exists():
        fail("next revision directory already exists", str(target))
    return sequence, target


def receipt_path(directory: Path, contract: dict[str, Any]) -> Path:
    return directory / contract["receipt_name"]


def validate_revision_chain_internal(slot_root: Path, runtime: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    statectl.verify_state_internal(slot_root, runtime)
    state = statectl.load_canonical_state(slot_root, runtime)
    dirs = revision_dirs(slot_root, contract)
    previous_hash: str | None = None
    previous_rel: str | None = None
    errors: list[str] = []
    checked: list[str] = []
    for expected_sequence, directory in enumerate(dirs, start=1):
        path = receipt_path(directory, contract)
        if not path.is_file():
            errors.append(f"{directory.name}: rollback receipt missing")
            continue
        receipt = statectl.load_json(path)
        rel = str(path.relative_to(slot_root))
        if receipt.get("revision_sequence") != expected_sequence:
            errors.append(f"{rel}: revision_sequence mismatch")
        if receipt.get("previous_revision_receipt") != previous_rel:
            errors.append(f"{rel}: previous revision receipt pointer mismatch")
        if receipt.get("previous_revision_receipt_sha256") != previous_hash:
            errors.append(f"{rel}: revision receipt hash chain mismatch")
        for item in receipt.get("archived_files") or []:
            archive_rel = item.get("archive_path")
            expected_sha = item.get("sha256")
            if not isinstance(archive_rel, str) or not isinstance(expected_sha, str):
                errors.append(f"{rel}: malformed archive inventory item")
                continue
            archive_path = slot_root / archive_rel
            if not archive_path.is_file():
                errors.append(f"{rel}: archived file missing: {archive_rel}")
                continue
            if statectl.sha256_file(archive_path) != expected_sha:
                errors.append(f"{rel}: archived file hash changed: {archive_rel}")
        previous_hash = statectl.sha256_file(path)
        previous_rel = rel
        checked.append(rel)

    state_revision = int(state.get("revision_sequence", 0) or 0)
    if state_revision != len(dirs):
        errors.append(f"CURRENT_STATE revision_sequence {state_revision} != archive count {len(dirs)}")
    if dirs:
        if state.get("last_revision_receipt") != previous_rel:
            errors.append("CURRENT_STATE last_revision_receipt mismatch")
        if state.get("last_revision_receipt_sha256") != previous_hash:
            errors.append("CURRENT_STATE last_revision_receipt_sha256 mismatch")
    else:
        if state.get("last_revision_receipt") not in {None, ""}:
            errors.append("CURRENT_STATE has revision pointer but no revision archive exists")

    # Active transition directory must contain exactly the chain through current stage.
    indexes = stage_indexes(runtime)
    current_index = indexes[state["current_stage"]]
    expected_active: set[str] = set()
    stages = stage_list(runtime)
    for sequence in range(current_index + 1):
        to_stage = stages[sequence]["id"]
        from_stage = None if sequence == 0 else stages[sequence - 1]["id"]
        expected_active.add(statectl.transition_receipt_relpath(sequence, from_stage, to_stage, runtime))
    transition_dir = slot_root / runtime["transition_contract"]["receipt_directory"]
    actual_active = {
        str(path.relative_to(slot_root))
        for path in transition_dir.glob("*.json")
        if path.is_file()
    } if transition_dir.is_dir() else set()
    extras = sorted(actual_active - expected_active)
    missing = sorted(expected_active - actual_active)
    if extras:
        errors.append("unexpected active downstream transition receipts: " + ", ".join(extras))
    if missing:
        errors.append("active transition receipts missing: " + ", ".join(missing))

    return {
        "ok": not errors,
        "slot_id": state["slot_id"],
        "current_stage": state["current_stage"],
        "revision_sequence": len(dirs),
        "checked_revision_receipts": checked,
        "errors": errors,
    }


def validate_revision_chain(slot_root: Path, runtime: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    report = validate_revision_chain_internal(slot_root, runtime, contract)
    if not report["ok"]:
        fail("revision history validation failed", report)
    return report


def context_events_to_archive(slot_root: Path, runtime: dict[str, Any], target_index: int) -> list[Path]:
    directory = slot_root / runtime["context_contract"]["receipt_directory"]
    if not directory.is_dir():
        return []
    indexes = stage_indexes(runtime)
    result: list[Path] = []
    for path in sorted(directory.glob("*.json")):
        receipt = statectl.load_json(path)
        event_stage = receipt.get("current_stage")
        if event_stage not in indexes:
            fail("context event references unknown stage", str(path))
        if indexes[event_stage] > target_index:
            result.append(path)
    return result


def rebuild_context_after_archive(slot_root: Path, runtime: dict[str, Any]) -> dict[str, Any]:
    manifest = statectl.load_json(statectl.manifest_path(slot_root, runtime))
    derived = dict(manifest.get("context") or {})
    directory = slot_root / runtime["context_contract"]["receipt_directory"]
    paths = sorted(directory.glob("*.json")) if directory.is_dir() else []
    previous_hash: str | None = None
    previous_rel: str | None = None
    for expected_revision, path in enumerate(paths, start=1):
        receipt = statectl.load_json(path)
        rel = str(path.relative_to(slot_root))
        if receipt.get("revision") != expected_revision:
            fail("remaining context event revision sequence is not contiguous", rel)
        if receipt.get("previous_context_receipt_sha256") != previous_hash:
            fail("remaining context event hash chain is broken", rel)
        key = receipt.get("key")
        if derived.get(key) != receipt.get("from"):
            fail("remaining context event old value disagrees with derived context", rel)
        derived[key] = receipt.get("to")
        previous_hash = statectl.sha256_file(path)
        previous_rel = rel
    return {
        "context": derived,
        "context_revision": len(paths),
        "last_context_receipt": previous_rel,
        "last_context_receipt_sha256": previous_hash,
    }


def build_plan(slot_root: Path, runtime: dict[str, Any], contract: dict[str, Any], change_type: str) -> dict[str, Any]:
    validate_revision_chain(slot_root, runtime, contract)
    state = statectl.load_canonical_state(slot_root, runtime)
    if state["current_stage"] in set(contract.get("forbidden_current_stages") or []):
        fail("published/post-publish states cannot use generic rollback", state["current_stage"])
    change_defs = contract.get("change_types") or {}
    if change_type not in change_defs:
        fail("unknown rollback change_type", {"change_type": change_type, "allowed": sorted(change_defs)})
    definition = change_defs[change_type]
    indexes = stage_indexes(runtime)
    target_stage = definition["target_stage"]
    current_index = indexes[state["current_stage"]]
    target_index = indexes[target_stage]
    if target_index >= current_index:
        fail(
            "requested revision does not move backward from current stage",
            {"current_stage": state["current_stage"], "change_type": change_type, "target_stage": target_stage},
        )

    artifact_defs = statectl.artifacts(runtime)
    artifact_origins = artifact_stage_index(runtime)
    artifacts_to_archive: list[dict[str, str]] = []
    for artifact_id, origin_index in sorted(artifact_origins.items(), key=lambda item: (item[1], item[0])):
        if not (target_index < origin_index <= current_index):
            continue
        definition_artifact = artifact_defs[artifact_id]
        path = slot_root / definition_artifact["canonical_path"]
        if path.is_file():
            artifacts_to_archive.append({
                "kind": "artifact",
                "artifact_id": artifact_id,
                "active_path": str(path.relative_to(slot_root)),
            })

    transitions: list[dict[str, str]] = []
    stages = stage_list(runtime)
    for sequence in range(target_index + 1, current_index + 1):
        to_stage = stages[sequence]["id"]
        from_stage = stages[sequence - 1]["id"]
        rel = statectl.transition_receipt_relpath(sequence, from_stage, to_stage, runtime)
        path = slot_root / rel
        if not path.is_file():
            fail("downstream transition receipt missing before rollback", rel)
        transitions.append({"kind": "transition", "active_path": rel})

    contexts = [
        {"kind": "context_event", "active_path": str(path.relative_to(slot_root))}
        for path in context_events_to_archive(slot_root, runtime, target_index)
    ]

    return {
        "ok": True,
        "slot_id": state["slot_id"],
        "change_type": change_type,
        "current_stage": state["current_stage"],
        "target_stage": target_stage,
        "current_index": current_index,
        "target_index": target_index,
        "state": state,
        "files_to_archive": artifacts_to_archive + transitions + contexts,
        "artifacts_to_archive": artifacts_to_archive,
        "transitions_to_archive": transitions,
        "context_events_to_archive": contexts,
    }


def plan(args: argparse.Namespace, runtime: dict[str, Any], contract: dict[str, Any]) -> None:
    result = build_plan(args.slot_root.resolve(), runtime, contract, args.change_type)
    emit({key: value for key, value in result.items() if key != "state"})


def move_to_archive(slot_root: Path, revision_dir: Path, item: dict[str, str]) -> tuple[Path, Path, dict[str, Any]]:
    source = slot_root / item["active_path"]
    if not source.is_file():
        fail("planned rollback source disappeared before archive", item)
    destination = revision_dir / "ARCHIVE" / item["active_path"]
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        fail("revision archive destination already exists", str(destination))
    original_sha = statectl.sha256_file(source)
    os.replace(source, destination)
    inventory = dict(item)
    inventory.update({
        "archive_path": str(destination.relative_to(slot_root)),
        "sha256": original_sha,
        "bytes": destination.stat().st_size,
    })
    return source, destination, inventory


def rollback(args: argparse.Namespace, runtime: dict[str, Any], contract: dict[str, Any]) -> None:
    if not args.reason.strip():
        fail("rollback requires a non-empty reason")
    slot_root = args.slot_root.resolve()
    result = build_plan(slot_root, runtime, contract, args.change_type)
    state_file = statectl.state_path(slot_root, runtime)
    state_before_bytes = state_file.read_bytes()
    state_before_sha = sha256_bytes(state_before_bytes)
    sequence, revision_dir = next_revision_identity(slot_root, contract, args.change_type)
    revision_dir.mkdir(parents=True, exist_ok=False)
    moved: list[tuple[Path, Path]] = []
    inventory: list[dict[str, Any]] = []
    receipt: Path | None = None
    try:
        for item in result["files_to_archive"]:
            source, destination, record = move_to_archive(slot_root, revision_dir, item)
            moved.append((source, destination))
            inventory.append(record)

        context_state = rebuild_context_after_archive(slot_root, runtime)
        stages = stage_list(runtime)
        target_index = result["target_index"]
        target = stages[target_index]
        target_from = None if target_index == 0 else stages[target_index - 1]["id"]
        target_transition_rel = statectl.transition_receipt_relpath(target_index, target_from, target["id"], runtime)
        target_transition = slot_root / target_transition_rel
        if not target_transition.is_file():
            fail("target transition receipt missing after rollback archive", target_transition_rel)

        old_revision_sequence = int(result["state"].get("revision_sequence", 0) or 0)
        if old_revision_sequence != sequence - 1:
            fail("CURRENT_STATE revision sequence disagrees with revision archive count")
        previous_revision_rel = result["state"].get("last_revision_receipt")
        previous_revision_sha = result["state"].get("last_revision_receipt_sha256")
        receipt = receipt_path(revision_dir, contract)
        receipt_payload = {
            "receipt_version": "1.0",
            "revision_sequence": sequence,
            "slot_id": result["slot_id"],
            "change_type": args.change_type,
            "reason": args.reason.strip(),
            "authority": args.authority,
            "from_stage": result["current_stage"],
            "to_stage": result["target_stage"],
            "state_before_sha256": state_before_sha,
            "previous_revision_receipt": previous_revision_rel,
            "previous_revision_receipt_sha256": previous_revision_sha,
            "archived_files": inventory,
            "created_at": statectl.now_iso(),
        }
        statectl.atomic_json(receipt, receipt_payload)
        receipt_sha = statectl.sha256_file(receipt)

        new_state = dict(result["state"])
        new_state.update({
            "current_stage": target["id"],
            "current_state_token": target["state_token"],
            "status": target["state_token"],
            "transition_sequence": target_index,
            "last_transition_receipt": target_transition_rel,
            "last_transition_receipt_sha256": statectl.sha256_file(target_transition),
            "context": context_state["context"],
            "context_revision": context_state["context_revision"],
            "last_context_receipt": context_state["last_context_receipt"],
            "last_context_receipt_sha256": context_state["last_context_receipt_sha256"],
            "revision_sequence": sequence,
            "last_revision_receipt": str(receipt.relative_to(slot_root)),
            "last_revision_receipt_sha256": receipt_sha,
            "updated_at": statectl.now_iso(),
        })
        statectl.atomic_json(state_file, new_state)
        state_verified = statectl.verify_state_internal(slot_root, runtime)
        revision_verified = validate_revision_chain_internal(slot_root, runtime, contract)
        if not revision_verified["ok"]:
            fail("post-rollback revision history verification failed", revision_verified)
    except SystemExit:
        state_file.write_bytes(state_before_bytes)
        for source, destination in reversed(moved):
            if destination.exists():
                source.parent.mkdir(parents=True, exist_ok=True)
                os.replace(destination, source)
        shutil.rmtree(revision_dir, ignore_errors=True)
        raise
    except Exception as exc:
        state_file.write_bytes(state_before_bytes)
        for source, destination in reversed(moved):
            if destination.exists():
                source.parent.mkdir(parents=True, exist_ok=True)
                os.replace(destination, source)
        shutil.rmtree(revision_dir, ignore_errors=True)
        fail("unexpected rollback failure; active evidence restored", repr(exc))

    emit({
        "ok": True,
        "mode": "rollback",
        "revision_sequence": sequence,
        "change_type": args.change_type,
        "from_stage": result["current_stage"],
        "to_stage": result["target_stage"],
        "archived_file_count": len(inventory),
        "revision_receipt": str(receipt.relative_to(slot_root)) if receipt else None,
        "state_verified": state_verified,
        "revision_history_verified": revision_verified,
    })


def verify_history(args: argparse.Namespace, runtime: dict[str, Any], contract: dict[str, Any]) -> None:
    report = validate_revision_chain_internal(args.slot_root.resolve(), runtime, contract)
    emit(report, 0 if report["ok"] else 1)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Controlled revision/rollback for canonical MV Runtime slots.")
    p.add_argument("--registry-dir", type=Path, default=RUNTIME_DIR)
    sub = p.add_subparsers(dest="command", required=True)

    dry = sub.add_parser("plan")
    dry.add_argument("--slot-root", required=True, type=Path)
    dry.add_argument("--change-type", required=True)

    rb = sub.add_parser("rollback")
    rb.add_argument("--slot-root", required=True, type=Path)
    rb.add_argument("--change-type", required=True)
    rb.add_argument("--reason", required=True)
    rb.add_argument("--authority", default="human_or_runtime_decision")

    verify = sub.add_parser("verify-history")
    verify.add_argument("--slot-root", required=True, type=Path)
    return p


def main() -> None:
    args = parser().parse_args()
    runtime = statectl.load_runtime(args.registry_dir.resolve())
    contract = load_contract(args.registry_dir.resolve())
    if args.command == "plan":
        plan(args, runtime, contract)
    elif args.command == "rollback":
        rollback(args, runtime, contract)
    elif args.command == "verify-history":
        verify_history(args, runtime, contract)
    else:
        fail("unknown command", args.command, 2)


if __name__ == "__main__":
    main()
