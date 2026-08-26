#!/usr/bin/env python3
"""Controlled legacy-to-canonical artifact migration for MV Runtime.

Historical evidence is never overwritten and ambiguous revisions are never guessed.
A maintainer explicitly selects a legacy source, the tool validates it, materializes
an identical canonical copy, and records provenance in a migration map.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import mv_runtime_gate as gate

SCRIPT_PATH = Path(__file__).resolve()
RUNTIME_DIR = SCRIPT_PATH.parent.parent / "runtime"
MIGRATION_MAP = "00_STATE/LEGACY_MIGRATION_MAP.json"


def emit(payload: dict[str, Any], code: int = 0) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(code)


def fail(message: str, details: Any = None, code: int = 1) -> None:
    payload: dict[str, Any] = {"ok": False, "error": message}
    if details is not None:
        payload["details"] = details
    emit(payload, code)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temp, path)


def bool_arg(value: str) -> bool:
    lowered = value.strip().lower()
    if lowered in {"1", "true", "yes", "y", "on"}:
        return True
    if lowered in {"0", "false", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError("expected true/false")


def context(args: argparse.Namespace) -> dict[str, bool]:
    return {"web": args.web, "multi_shot": args.multi_shot, "program_30d60": args.program_30d60, "canonical_v2": False}


def load_map(slot_root: Path) -> dict[str, Any]:
    path = slot_root / MIGRATION_MAP
    if not path.is_file():
        return {"schema_version": "1.0", "status": "LEGACY_MIGRATION", "entries": {}}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail("invalid migration map", str(exc), 2)
    if not isinstance(payload, dict) or not isinstance(payload.get("entries"), dict):
        fail("migration map must contain entries object", code=2)
    return payload


def plan(args: argparse.Namespace, stage_registry: dict[str, Any], artifact_registry: dict[str, Any]) -> None:
    slot_root = args.slot_root.resolve()
    report = gate.audit_slot(slot_root, stage_registry, artifact_registry, context(args), stop_at=args.stop_at)
    ambiguous = {}
    missing = {}
    legacy = {}
    for artifact_id, item in report.get("artifacts", {}).items():
        if item.get("source") == "ambiguous":
            ambiguous[artifact_id] = item
        elif not item.get("ok") and item.get("path") is None:
            missing[artifact_id] = item
        elif item.get("source") == "legacy":
            legacy[artifact_id] = item
    emit({
        "ok": True,
        "slot_root": str(slot_root),
        "highest_contiguous_valid_stage": report.get("highest_contiguous_valid_stage"),
        "declared_state": report.get("declared_state"),
        "ambiguous_artifacts": ambiguous,
        "missing_artifacts": missing,
        "legacy_artifacts": legacy,
        "rule": "Ambiguous artifacts require explicit --source selection; no automatic latest-version choice is allowed."
    })


def promote(args: argparse.Namespace, artifact_registry: dict[str, Any]) -> None:
    slot_root = args.slot_root.resolve()
    artifact_defs = gate.index_by_id(artifact_registry["artifacts"], "artifact")
    if args.artifact not in artifact_defs:
        fail("unknown artifact", args.artifact, 2)
    definition = artifact_defs[args.artifact]
    source = (slot_root / args.source).resolve()
    try:
        source.relative_to(slot_root)
    except ValueError:
        fail("source must stay inside slot root")
    if not source.is_file():
        fail("selected legacy source does not exist", args.source)

    allowed: set[Path] = set()
    for pattern in definition.get("legacy_patterns") or []:
        allowed.update(path.resolve() for path in slot_root.glob(pattern) if path.is_file())
    if source not in allowed:
        fail("selected source does not match this artifact's registered legacy aliases", {"artifact": args.artifact, "source": args.source})

    target = (slot_root / definition["canonical_path"]).resolve()
    try:
        target.relative_to(slot_root)
    except ValueError:
        fail("unsafe canonical target", definition["canonical_path"], 2)
    if target.exists():
        fail("canonical artifact already exists; migration will not overwrite it", definition["canonical_path"])
    if source.suffix.lower() != target.suffix.lower():
        fail("legacy source and canonical target use different formats; explicit conversion is required", {"source": source.suffix, "target": target.suffix})

    errors = gate.run_artifact_checks(source, definition)
    if errors:
        fail("selected legacy source fails artifact validation", {"errors": errors})

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(source.read_bytes())
    canonical_result = gate.check_artifact(slot_root, definition)
    if not canonical_result.ok or canonical_result.source != "canonical":
        target.unlink(missing_ok=True)
        fail("materialized canonical artifact failed validation", canonical_result.__dict__)

    migration = load_map(slot_root)
    entries = migration["entries"]
    if args.artifact in entries:
        target.unlink(missing_ok=True)
        fail("artifact already has a migration provenance entry; revisions require a separate controlled flow", args.artifact)
    entry = {
        "artifact_id": args.artifact,
        "mode": "materialized_copy",
        "source_path": str(source.relative_to(slot_root)),
        "source_sha256": sha256_file(source),
        "canonical_path": str(target.relative_to(slot_root)),
        "canonical_sha256": sha256_file(target),
        "selected_by": args.selected_by,
        "selection_reason": args.reason,
        "migrated_at": now_iso()
    }
    entries[args.artifact] = entry
    atomic_json(slot_root / MIGRATION_MAP, migration)
    emit({"ok": True, "migration": entry, "migration_map": MIGRATION_MAP})


def verify(args: argparse.Namespace, artifact_registry: dict[str, Any]) -> None:
    slot_root = args.slot_root.resolve()
    artifact_defs = gate.index_by_id(artifact_registry["artifacts"], "artifact")
    migration = load_map(slot_root)
    failures = []
    checked = []
    for artifact_id, entry in migration["entries"].items():
        if artifact_id not in artifact_defs:
            failures.append({"artifact_id": artifact_id, "error": "unknown artifact id"})
            continue
        source = slot_root / entry["source_path"]
        target = slot_root / entry["canonical_path"]
        problems = []
        if not source.is_file() or sha256_file(source) != entry.get("source_sha256"):
            problems.append("legacy source missing or hash changed")
        if not target.is_file() or sha256_file(target) != entry.get("canonical_sha256"):
            problems.append("canonical copy missing or hash changed")
        result = gate.check_artifact(slot_root, artifact_defs[artifact_id])
        if not result.ok or result.source != "canonical":
            problems.append("canonical artifact no longer validates")
        if problems:
            failures.append({"artifact_id": artifact_id, "problems": problems})
        else:
            checked.append(artifact_id)
    emit({"ok": not failures, "checked": checked, "failures": failures}, 0 if not failures else 1)


def add_context(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--web", type=bool_arg, default=True)
    parser.add_argument("--multi-shot", type=bool_arg, default=False)
    parser.add_argument("--program-30d60", type=bool_arg, default=True)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Controlled legacy artifact migration for MV Runtime.")
    p.add_argument("--registry-dir", type=Path, default=RUNTIME_DIR)
    sub = p.add_subparsers(dest="command", required=True)
    pl = sub.add_parser("plan")
    pl.add_argument("--slot-root", type=Path, required=True)
    pl.add_argument("--stop-at")
    add_context(pl)
    pr = sub.add_parser("promote")
    pr.add_argument("--slot-root", type=Path, required=True)
    pr.add_argument("--artifact", required=True)
    pr.add_argument("--source", required=True)
    pr.add_argument("--selected-by", required=True)
    pr.add_argument("--reason", required=True)
    ve = sub.add_parser("verify")
    ve.add_argument("--slot-root", type=Path, required=True)
    return p


def main() -> None:
    args = build_parser().parse_args()
    stage_registry, artifact_registry = gate.load_registries(args.registry_dir.resolve())
    if args.command == "plan":
        plan(args, stage_registry, artifact_registry)
    elif args.command == "promote":
        promote(args, artifact_registry)
    elif args.command == "verify":
        verify(args, artifact_registry)
    else:
        fail("unknown command", args.command, 2)


if __name__ == "__main__":
    main()
