#!/usr/bin/env python3
"""Immutable media-asset identity registry for canonical MV Runtime slots.

The tool does not store large media in Git. It stores durable identity records:
SHA-256, byte size, role, stage of origin, locator, provenance and lineage.
Stage-scoped manifests then bind immutable asset IDs to production meaning.

Commands:
- register-local
- register-external
- verify-record
- verify-all
- create-manifest
- verify-manifest
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

SCRIPT_PATH = Path(__file__).resolve()
RUNTIME_DIR = SCRIPT_PATH.parent.parent / "runtime"
CONTRACT_NAME = "mv_media_asset_contract.json"
STAGE_REGISTRY_NAME = "mv_stage_registry.json"


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


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail("invalid or missing JSON", {"path": str(path), "error": str(exc)}, 2)
    if not isinstance(payload, dict):
        fail("JSON root must be object", str(path), 2)
    return payload


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temp, path)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_runtime(registry_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    contract = load_json(registry_dir / CONTRACT_NAME)
    stage_registry = load_json(registry_dir / STAGE_REGISTRY_NAME)
    return contract, stage_registry


def stage_ids(stage_registry: dict[str, Any]) -> set[str]:
    values = set()
    for item in stage_registry.get("stages") or []:
        stage_id = item.get("id")
        if isinstance(stage_id, str):
            values.add(stage_id)
    return values


def validate_asset_id(asset_id: str, contract: dict[str, Any]) -> None:
    if re.fullmatch(contract["asset_id_pattern"], asset_id) is None:
        fail("asset_id violates contract", {"asset_id": asset_id, "pattern": contract["asset_id_pattern"]})


def record_dir(slot_root: Path, contract: dict[str, Any]) -> Path:
    return slot_root / contract["record_directory"]


def record_path(slot_root: Path, contract: dict[str, Any], asset_id: str) -> Path:
    validate_asset_id(asset_id, contract)
    return record_dir(slot_root, contract) / f"{asset_id}{contract['record_extension']}"


def validate_sha(value: str, contract: dict[str, Any]) -> None:
    if re.fullmatch(contract["sha256_pattern"], value) is None:
        fail("invalid SHA-256 identity", value)


def normalize_parents(values: list[str] | None) -> list[str]:
    result: list[str] = []
    for value in values or []:
        value = value.strip()
        if value and value not in result:
            result.append(value)
    return result


def load_parent_records(slot_root: Path, contract: dict[str, Any], asset_id: str, parents: list[str]) -> list[dict[str, Any]]:
    loaded: list[dict[str, Any]] = []
    for parent in parents:
        if parent == asset_id:
            fail("asset cannot name itself as parent", asset_id)
        path = record_path(slot_root, contract, parent)
        if not path.is_file():
            fail("parent asset record must already exist", {"asset_id": asset_id, "parent": parent})
        loaded.append(load_json(path))
    return loaded


def local_locator_value(slot_root: Path, source: Path) -> str:
    source = source.resolve()
    slot_root = slot_root.resolve()
    try:
        return str(source.relative_to(slot_root))
    except ValueError:
        return str(source)


def validate_record_payload(
    slot_root: Path,
    payload: dict[str, Any],
    contract: dict[str, Any],
    stage_registry: dict[str, Any],
    *,
    verify_local_bytes: bool,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    missing = [key for key in contract["required_record_fields"] if key not in payload]
    if missing:
        errors.append("missing record fields: " + ", ".join(missing))

    asset_id = payload.get("asset_id")
    if not isinstance(asset_id, str) or re.fullmatch(contract["asset_id_pattern"], asset_id) is None:
        errors.append("invalid asset_id")
    if payload.get("media_type") not in set(contract["media_types"]):
        errors.append("invalid media_type")
    if not isinstance(payload.get("role"), str) or not payload.get("role", "").strip():
        errors.append("role must be non-empty string")
    if payload.get("stage_origin") not in stage_ids(stage_registry):
        errors.append("stage_origin is not registered")

    content = payload.get("content")
    if not isinstance(content, dict):
        errors.append("content must be object")
        content = {}
    else:
        for key in contract["content_required_fields"]:
            if key not in content:
                errors.append(f"content missing {key}")
    sha = content.get("sha256")
    if not isinstance(sha, str) or re.fullmatch(contract["sha256_pattern"], sha) is None:
        errors.append("content.sha256 invalid")
    byte_count = content.get("bytes")
    if not isinstance(byte_count, int) or byte_count < 0:
        errors.append("content.bytes must be non-negative integer")

    locator = payload.get("locator")
    if not isinstance(locator, dict):
        errors.append("locator must be object")
        locator = {}
    else:
        for key in contract["locator_required_fields"]:
            if key not in locator:
                errors.append(f"locator missing {key}")
    locator_kind = locator.get("kind")
    if locator_kind not in set(contract["locator_kinds"]):
        errors.append("locator.kind invalid")
    if not isinstance(locator.get("value"), str) or not locator.get("value", "").strip():
        errors.append("locator.value must be non-empty string")

    provenance = payload.get("provenance")
    if not isinstance(provenance, dict):
        errors.append("provenance must be object")
        provenance = {}
    else:
        for key in contract["provenance_required_fields"]:
            if key not in provenance:
                errors.append(f"provenance missing {key}")
    if provenance.get("kind") not in set(contract["provenance_kinds"]):
        errors.append("provenance.kind invalid")
    if not isinstance(provenance.get("description"), str) or not provenance.get("description", "").strip():
        errors.append("provenance.description must be non-empty string")

    parents = payload.get("parents")
    if not isinstance(parents, list) or any(not isinstance(item, str) for item in parents):
        errors.append("parents must be string array")
        parents = []
    if len(set(parents)) != len(parents):
        errors.append("parents contains duplicates")
    if asset_id in parents:
        errors.append("self-parent is forbidden")
    for parent in parents:
        parent_path = record_path(slot_root, contract, parent)
        if not parent_path.is_file():
            errors.append(f"parent record missing: {parent}")

    if not isinstance(payload.get("metadata"), dict):
        errors.append("metadata must be object")
    if not isinstance(payload.get("registered_at"), str) or not payload.get("registered_at", "").strip():
        errors.append("registered_at must be non-empty string")

    local_verified = False
    if locator_kind == "workspace_path" and verify_local_bytes and not errors:
        raw_value = Path(locator["value"])
        local_path = raw_value if raw_value.is_absolute() else slot_root / raw_value
        if local_path.is_file():
            actual_sha = sha256_file(local_path)
            actual_bytes = local_path.stat().st_size
            if actual_sha != sha:
                errors.append("workspace media SHA-256 no longer matches asset record")
            if actual_bytes != byte_count:
                errors.append("workspace media byte size no longer matches asset record")
            local_verified = not errors
        else:
            warnings.append("workspace media bytes are currently unavailable; durable SHA identity remains recorded")

    return {
        "ok": not errors,
        "asset_id": asset_id,
        "errors": errors,
        "warnings": warnings,
        "local_bytes_verified": local_verified,
    }


def base_record(
    args: argparse.Namespace,
    contract: dict[str, Any],
    *,
    sha256: str,
    byte_count: int,
    locator_kind: str,
    locator_value: str,
) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    for item in args.meta or []:
        if "=" not in item:
            fail("--meta must use key=value", item)
        key, value = item.split("=", 1)
        key = key.strip()
        if not key:
            fail("--meta key cannot be empty", item)
        metadata[key] = value.strip()
    return {
        "schema_version": "1.0",
        "asset_id": args.asset_id,
        "media_type": args.media_type,
        "role": args.role.strip(),
        "stage_origin": args.stage_origin,
        "content": {"sha256": sha256, "bytes": byte_count},
        "locator": {"kind": locator_kind, "value": locator_value},
        "provenance": {"kind": args.provenance_kind, "description": args.provenance_description.strip()},
        "parents": normalize_parents(args.parent),
        "metadata": metadata,
        "registered_at": now_iso(),
    }


def register_local(args: argparse.Namespace, contract: dict[str, Any], stage_registry: dict[str, Any]) -> None:
    slot_root = args.slot_root.resolve()
    source = args.file.resolve()
    if not source.is_file():
        fail("local media file missing", str(source))
    validate_asset_id(args.asset_id, contract)
    if args.stage_origin not in stage_ids(stage_registry):
        fail("stage_origin is not registered", args.stage_origin)
    if args.media_type not in contract["media_types"]:
        fail("invalid media_type", args.media_type)
    if args.provenance_kind not in contract["provenance_kinds"]:
        fail("invalid provenance_kind", args.provenance_kind)
    target = record_path(slot_root, contract, args.asset_id)
    if target.exists():
        fail("asset record already exists and is immutable", str(target))
    parents = normalize_parents(args.parent)
    load_parent_records(slot_root, contract, args.asset_id, parents)
    payload = base_record(
        args,
        contract,
        sha256=sha256_file(source),
        byte_count=source.stat().st_size,
        locator_kind="workspace_path",
        locator_value=local_locator_value(slot_root, source),
    )
    result = validate_record_payload(slot_root, payload, contract, stage_registry, verify_local_bytes=True)
    if not result["ok"]:
        fail("generated local asset record failed contract", result)
    atomic_json(target, payload)
    emit({"ok": True, "mode": "register-local", "record": str(target.relative_to(slot_root)), "asset": payload, "verification": result})


def register_external(args: argparse.Namespace, contract: dict[str, Any], stage_registry: dict[str, Any]) -> None:
    slot_root = args.slot_root.resolve()
    validate_asset_id(args.asset_id, contract)
    validate_sha(args.sha256.lower(), contract)
    if args.bytes < 0:
        fail("--bytes must be non-negative")
    if args.stage_origin not in stage_ids(stage_registry):
        fail("stage_origin is not registered", args.stage_origin)
    if args.locator_kind == "workspace_path":
        fail("register-external cannot use workspace_path; use register-local")
    if args.locator_kind not in contract["locator_kinds"]:
        fail("invalid locator_kind", args.locator_kind)
    if args.media_type not in contract["media_types"]:
        fail("invalid media_type", args.media_type)
    if args.provenance_kind not in contract["provenance_kinds"]:
        fail("invalid provenance_kind", args.provenance_kind)
    target = record_path(slot_root, contract, args.asset_id)
    if target.exists():
        fail("asset record already exists and is immutable", str(target))
    parents = normalize_parents(args.parent)
    load_parent_records(slot_root, contract, args.asset_id, parents)
    payload = base_record(
        args,
        contract,
        sha256=args.sha256.lower(),
        byte_count=args.bytes,
        locator_kind=args.locator_kind,
        locator_value=args.locator,
    )
    result = validate_record_payload(slot_root, payload, contract, stage_registry, verify_local_bytes=False)
    if not result["ok"]:
        fail("generated external asset record failed contract", result)
    atomic_json(target, payload)
    emit({"ok": True, "mode": "register-external", "record": str(target.relative_to(slot_root)), "asset": payload, "verification": result})


def verify_record(args: argparse.Namespace, contract: dict[str, Any], stage_registry: dict[str, Any]) -> None:
    slot_root = args.slot_root.resolve()
    path = record_path(slot_root, contract, args.asset_id)
    payload = load_json(path)
    if payload.get("asset_id") != args.asset_id:
        fail("asset record filename/id mismatch", {"filename_id": args.asset_id, "payload_id": payload.get("asset_id")})
    result = validate_record_payload(slot_root, payload, contract, stage_registry, verify_local_bytes=True)
    emit({"ok": result["ok"], "mode": "verify-record", "record": str(path.relative_to(slot_root)), **result}, 0 if result["ok"] else 1)


def verify_all_internal(slot_root: Path, contract: dict[str, Any], stage_registry: dict[str, Any]) -> dict[str, Any]:
    directory = record_dir(slot_root, contract)
    paths = sorted(directory.glob(f"*{contract['record_extension']}")) if directory.is_dir() else []
    records: dict[str, Any] = {}
    errors: list[str] = []
    for path in paths:
        payload = load_json(path)
        asset_id = payload.get("asset_id")
        if not isinstance(asset_id, str):
            errors.append(f"{path.name}: missing asset_id")
            continue
        if path.name != f"{asset_id}{contract['record_extension']}":
            errors.append(f"{path.name}: filename/id mismatch")
        result = validate_record_payload(slot_root, payload, contract, stage_registry, verify_local_bytes=True)
        records[asset_id] = {"path": str(path.relative_to(slot_root)), **result}
        if not result["ok"]:
            errors.append(f"{asset_id}: invalid record")
    return {"ok": not errors, "record_count": len(paths), "records": records, "errors": errors}


def verify_all(args: argparse.Namespace, contract: dict[str, Any], stage_registry: dict[str, Any]) -> None:
    report = verify_all_internal(args.slot_root.resolve(), contract, stage_registry)
    emit(report, 0 if report["ok"] else 1)


def parse_binding(value: str) -> dict[str, str]:
    # asset_id or asset_id|shot_id|use
    parts = value.split("|")
    if len(parts) > 3:
        fail("--asset binding must be asset_id or asset_id|shot_id|use", value)
    binding = {"asset_id": parts[0].strip()}
    if len(parts) >= 2 and parts[1].strip():
        binding["shot_id"] = parts[1].strip()
    if len(parts) == 3 and parts[2].strip():
        binding["use"] = parts[2].strip()
    return binding


def validate_manifest_payload(slot_root: Path, payload: dict[str, Any], contract: dict[str, Any], stage_registry: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    schema = contract["manifest_schema"]
    missing = [key for key in schema["required_fields"] if key not in payload]
    if missing:
        errors.append("missing manifest fields: " + ", ".join(missing))
    if payload.get("stage_id") not in stage_ids(stage_registry):
        errors.append("manifest stage_id is not registered")
    if not isinstance(payload.get("manifest_id"), str) or not payload.get("manifest_id", "").strip():
        errors.append("manifest_id must be non-empty string")
    assets = payload.get("assets")
    if not isinstance(assets, list) or not assets:
        errors.append("manifest assets must be a non-empty array")
        assets = []
    seen: set[str] = set()
    asset_results: dict[str, Any] = {}
    for index, binding in enumerate(assets):
        if not isinstance(binding, dict):
            errors.append(f"assets[{index}] must be object")
            continue
        for key in schema["asset_binding_required_fields"]:
            if key not in binding:
                errors.append(f"assets[{index}] missing {key}")
        asset_id = binding.get("asset_id")
        if not isinstance(asset_id, str):
            continue
        if asset_id in seen:
            errors.append(f"duplicate asset binding: {asset_id}")
            continue
        seen.add(asset_id)
        path = record_path(slot_root, contract, asset_id)
        if not path.is_file():
            errors.append(f"asset record missing: {asset_id}")
            continue
        record = load_json(path)
        result = validate_record_payload(slot_root, record, contract, stage_registry, verify_local_bytes=True)
        asset_results[asset_id] = result
        if not result["ok"]:
            errors.append(f"asset record invalid: {asset_id}")
        warnings.extend(f"{asset_id}: {item}" for item in result["warnings"])
    return {"ok": not errors, "manifest_id": payload.get("manifest_id"), "asset_count": len(assets), "asset_results": asset_results, "errors": errors, "warnings": warnings}


def create_manifest(args: argparse.Namespace, contract: dict[str, Any], stage_registry: dict[str, Any]) -> None:
    slot_root = args.slot_root.resolve()
    if args.stage_id not in stage_ids(stage_registry):
        fail("manifest stage_id is not registered", args.stage_id)
    target = args.manifest.resolve() if args.manifest.is_absolute() else slot_root / args.manifest
    if target.exists():
        fail("stage asset manifest already exists and is immutable", str(target))
    bindings = [parse_binding(value) for value in args.asset]
    payload = {
        "schema_version": "1.0",
        "manifest_id": args.manifest_id,
        "stage_id": args.stage_id,
        "assets": bindings,
        "created_at": now_iso(),
    }
    result = validate_manifest_payload(slot_root, payload, contract, stage_registry)
    if not result["ok"]:
        fail("generated stage asset manifest failed validation", result)
    atomic_json(target, payload)
    emit({"ok": True, "mode": "create-manifest", "manifest": str(target), "validation": result})


def verify_manifest(args: argparse.Namespace, contract: dict[str, Any], stage_registry: dict[str, Any]) -> None:
    slot_root = args.slot_root.resolve()
    target = args.manifest.resolve() if args.manifest.is_absolute() else slot_root / args.manifest
    payload = load_json(target)
    result = validate_manifest_payload(slot_root, payload, contract, stage_registry)
    emit({"ok": result["ok"], "mode": "verify-manifest", "manifest": str(target), **result}, 0 if result["ok"] else 1)


def add_record_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--slot-root", required=True, type=Path)
    parser.add_argument("--asset-id", required=True)
    parser.add_argument("--media-type", required=True)
    parser.add_argument("--role", required=True)
    parser.add_argument("--stage-origin", required=True)
    parser.add_argument("--provenance-kind", required=True)
    parser.add_argument("--provenance-description", required=True)
    parser.add_argument("--parent", action="append", default=[])
    parser.add_argument("--meta", action="append", default=[])


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Immutable media identity and stage asset manifest tool for MV Runtime.")
    p.add_argument("--registry-dir", type=Path, default=RUNTIME_DIR)
    sub = p.add_subparsers(dest="command", required=True)

    local = sub.add_parser("register-local")
    add_record_args(local)
    local.add_argument("--file", required=True, type=Path)

    external = sub.add_parser("register-external")
    add_record_args(external)
    external.add_argument("--sha256", required=True)
    external.add_argument("--bytes", required=True, type=int)
    external.add_argument("--locator-kind", required=True)
    external.add_argument("--locator", required=True)

    one = sub.add_parser("verify-record")
    one.add_argument("--slot-root", required=True, type=Path)
    one.add_argument("--asset-id", required=True)

    all_parser = sub.add_parser("verify-all")
    all_parser.add_argument("--slot-root", required=True, type=Path)

    manifest = sub.add_parser("create-manifest")
    manifest.add_argument("--slot-root", required=True, type=Path)
    manifest.add_argument("--manifest", required=True, type=Path)
    manifest.add_argument("--manifest-id", required=True)
    manifest.add_argument("--stage-id", required=True)
    manifest.add_argument("--asset", action="append", required=True)

    check_manifest = sub.add_parser("verify-manifest")
    check_manifest.add_argument("--slot-root", required=True, type=Path)
    check_manifest.add_argument("--manifest", required=True, type=Path)
    return p


def main() -> None:
    args = parser().parse_args()
    contract, stage_registry = load_runtime(args.registry_dir.resolve())
    if args.command == "register-local":
        register_local(args, contract, stage_registry)
    elif args.command == "register-external":
        register_external(args, contract, stage_registry)
    elif args.command == "verify-record":
        verify_record(args, contract, stage_registry)
    elif args.command == "verify-all":
        verify_all(args, contract, stage_registry)
    elif args.command == "create-manifest":
        create_manifest(args, contract, stage_registry)
    elif args.command == "verify-manifest":
        verify_manifest(args, contract, stage_registry)
    else:
        fail("unknown command", args.command, 2)


if __name__ == "__main__":
    main()
