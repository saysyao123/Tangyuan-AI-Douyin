#!/usr/bin/env python3
"""Transactional publish/tracker sync for canonical MV Runtime slots.

This controller is intentionally narrow:
- it never creates a publish event from inference;
- it only operates on canonical_v2 slots at S16_RELEASE_PACKAGE_READY;
- it validates one unique 30D/60 tracker row before writing;
- it writes durable publish/tracker receipts before delegating S16 -> S17 to
  mv_runtime_state.py, which remains the only state-transition authority;
- if the final state advance fails, tracker and receipt writes are rolled back.

Commands: preflight, sync, verify.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
from io import StringIO
from pathlib import Path
from typing import Any

import mv_runtime_gate as gate
import mv_runtime_state as statectl

SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[2]
RUNTIME_DIR = SCRIPT_PATH.parent.parent / "runtime"
DEFAULT_TRACKER = REPO_ROOT / "05_IP_ASSETS" / "MV_30D_60_TRACKER.csv"
PENDING_TIME = "timestamp_pending_backfill"
S16 = "S16_RELEASE_PACKAGE_READY"
S17 = "S17_PUBLISHED_DATA_COLLECTION_ACTIVE"

REQUIRED_TRACKER_COLUMNS = [
    "slot_id", "day", "slot", "lane", "song_family", "audio_asset", "status",
    "packaging", "publish_time", "views_1h", "views_3h", "views_24h",
    "likes_24h", "comments_24h", "favorites_24h", "shares_24h",
    "new_follows_24h", "completion_24h", "avg_watch_24h", "notes",
]
PUBLISH_CRITICAL_FIELDS = [
    "slot_id", "day", "slot", "lane", "song_family", "audio_asset",
    "status", "packaging", "publish_time",
]


def emit(payload: dict[str, Any], code: int = 0) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(code)


def fail(message: str, details: Any = None, code: int = 1) -> None:
    payload: dict[str, Any] = {"ok": False, "error": message}
    if details is not None:
        payload["details"] = details
    emit(payload, code)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return statectl.sha256_file(path)


def atomic_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    temp.write_bytes(data)
    os.replace(temp, path)


def atomic_text(path: Path, text: str) -> None:
    atomic_bytes(path, text.encode("utf-8"))


def receipt_markdown(title: str, payload: dict[str, Any]) -> str:
    body = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
    return f"# {title}\n\n```json\n{body}\n```\n"


def parse_receipt(path: Path) -> dict[str, Any]:
    if not path.is_file():
        fail("publish receipt missing", str(path))
    text = path.read_text(encoding="utf-8")
    match = re.search(r"```json\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    if match is None:
        fail("publish receipt has no machine-readable JSON payload", str(path))
    try:
        payload = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        fail("publish receipt JSON payload is invalid", {"path": str(path), "error": str(exc)})
    if not isinstance(payload, dict):
        fail("publish receipt JSON payload must be an object", str(path))
    return payload


def parse_slot_identity(slot_id: str) -> tuple[str, str]:
    match = re.fullmatch(r"D(\d{2})-([A-Z])", slot_id)
    if match is None:
        fail(
            "30D/60 publish sync requires slot_id shaped like DNN-X",
            {"slot_id": slot_id, "example": "D02-A"},
        )
    return str(int(match.group(1))), match.group(2)


def normalize_cell(value: Any) -> str:
    return "" if value is None else str(value).strip()


def load_tracker(path: Path) -> tuple[list[str], list[dict[str, str]], bytes]:
    if not path.is_file():
        fail("tracker file missing", str(path))
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        fail("tracker must be UTF-8/UTF-8-BOM CSV", str(exc))
    reader = csv.DictReader(StringIO(text))
    fieldnames = reader.fieldnames or []
    missing = [name for name in REQUIRED_TRACKER_COLUMNS if name not in fieldnames]
    if missing:
        fail("tracker schema missing required columns", missing)
    rows: list[dict[str, str]] = []
    for raw_row in reader:
        rows.append({name: normalize_cell(raw_row.get(name, "")) for name in fieldnames})
    return fieldnames, rows, raw


def serialize_tracker(fieldnames: list[str], rows: list[dict[str, str]]) -> bytes:
    stream = StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def unique_tracker_row(rows: list[dict[str, str]], slot_id: str) -> tuple[int, dict[str, str]]:
    matches = [(index, row) for index, row in enumerate(rows) if row.get("slot_id") == slot_id]
    if len(matches) != 1:
        fail(
            "tracker must contain exactly one row for slot_id",
            {"slot_id": slot_id, "matches": len(matches)},
        )
    return matches[0]


def critical_snapshot(row: dict[str, str]) -> dict[str, str]:
    return {key: normalize_cell(row.get(key, "")) for key in PUBLISH_CRITICAL_FIELDS}


def conflict(field: str, existing: str, requested: str) -> None:
    if existing and requested and existing != requested:
        fail(
            "tracker contains conflicting nonblank publish identity",
            {"field": field, "tracker": existing, "requested": requested},
        )


def append_note(existing: str, addition: str) -> str:
    existing = existing.strip()
    if addition in existing:
        return existing
    return addition if not existing else existing + "；" + addition


def artifact_path(runtime: dict[str, Any], slot_root: Path, artifact_id: str) -> Path:
    definitions = statectl.artifacts(runtime)
    if artifact_id not in definitions:
        fail("artifact registry missing publish artifact", artifact_id, 2)
    return slot_root / definitions[artifact_id]["canonical_path"]


def require_canonical_artifact(runtime: dict[str, Any], slot_root: Path, artifact_id: str) -> Path:
    definition = statectl.artifacts(runtime)[artifact_id]
    result = gate.check_artifact(slot_root, definition)
    if not result.ok or result.source != "canonical" or not result.path:
        fail(
            "required publish artifact is missing or non-canonical",
            {"artifact_id": artifact_id, "result": result.__dict__},
        )
    return slot_root / result.path


def publish_time_value(value: str | None) -> str:
    if value is None or not value.strip():
        return PENDING_TIME
    value = value.strip()
    if value.lower() in {"unknown", "pending", "tbd", "n/a", "na"}:
        return PENDING_TIME
    return value


def preflight_internal(args: argparse.Namespace, runtime: dict[str, Any]) -> dict[str, Any]:
    slot_root = args.slot_root.resolve()
    tracker = args.tracker.resolve()
    verified = statectl.verify_state_internal(slot_root, runtime)
    state = statectl.load_canonical_state(slot_root, runtime)
    if state["current_stage"] != S16:
        fail(
            "publish sync is allowed only from S16_RELEASE_PACKAGE_READY",
            {"current_stage": state["current_stage"], "required": S16},
        )
    if state.get("context", {}).get("program_30d60") is not True:
        fail("this controller currently handles program_30d60=true publish transactions only")

    manifest_path = statectl.manifest_path(slot_root, runtime)
    manifest = statectl.load_json(manifest_path)
    if manifest.get("slot_id") != state.get("slot_id"):
        fail("SLOT_MANIFEST slot_id disagrees with CURRENT_STATE")
    if manifest.get("lane") != state.get("lane"):
        fail("SLOT_MANIFEST lane disagrees with CURRENT_STATE")

    slot_id = state["slot_id"]
    expected_day, expected_slot = parse_slot_identity(slot_id)
    fieldnames, rows, tracker_before = load_tracker(tracker)
    row_index, row = unique_tracker_row(rows, slot_id)

    if normalize_cell(row.get("day")) != expected_day:
        fail("tracker day does not match slot_id", {"tracker": row.get("day"), "expected": expected_day})
    if normalize_cell(row.get("slot")) != expected_slot:
        fail("tracker slot letter does not match slot_id", {"tracker": row.get("slot"), "expected": expected_slot})
    if normalize_cell(row.get("lane")) != normalize_cell(state.get("lane")):
        fail("tracker lane does not match canonical slot lane", {"tracker": row.get("lane"), "slot": state.get("lane")})

    song_family = args.song_family.strip()
    audio_asset = args.audio_asset.strip()
    if not song_family or not audio_asset:
        fail("song_family and audio_asset must be explicit non-empty publish identities")
    conflict("song_family", normalize_cell(row.get("song_family")), song_family)
    conflict("audio_asset", normalize_cell(row.get("audio_asset")), audio_asset)

    packaging = normalize_cell(args.packaging) if args.packaging is not None else normalize_cell(row.get("packaging"))
    if args.packaging is not None:
        conflict("packaging", normalize_cell(row.get("packaging")), packaging)

    desired_time = publish_time_value(args.publish_time)
    current_time = normalize_cell(row.get("publish_time"))
    if current_time and current_time != PENDING_TIME and desired_time != PENDING_TIME and current_time != desired_time:
        fail("tracker contains conflicting exact publish_time", {"tracker": current_time, "requested": desired_time})
    if current_time and current_time != PENDING_TIME and desired_time == PENDING_TIME:
        desired_time = current_time

    current_status = normalize_cell(row.get("status"))
    if current_status and current_status not in {"PLANNED", "READY", "RELEASE_READY", "PUBLISHED"}:
        fail("tracker status is not eligible for canonical publish sync", current_status)

    release_package = require_canonical_artifact(runtime, slot_root, "RELEASE_PACKAGE")
    post_receipt = artifact_path(runtime, slot_root, "POST_PUBLISH_SYNC_RECEIPT")
    tracker_receipt = artifact_path(runtime, slot_root, "TRACKER_SYNC_RECEIPT")
    if post_receipt.exists() or tracker_receipt.exists():
        fail(
            "canonical publish receipts already exist; use verify instead of creating a second publish event",
            {"post_receipt": post_receipt.exists(), "tracker_receipt": tracker_receipt.exists()},
        )

    planned = dict(row)
    planned["song_family"] = song_family
    planned["audio_asset"] = audio_asset
    planned["status"] = "PUBLISHED"
    if packaging:
        planned["packaging"] = packaging
    planned["publish_time"] = desired_time
    note = "publish sync confirmed"
    if desired_time == PENDING_TIME:
        note += "; exact publish timestamp pending backfill"
    planned["notes"] = append_note(normalize_cell(planned.get("notes")), note)

    return {
        "ok": True,
        "slot_root": str(slot_root),
        "tracker": str(tracker),
        "slot_id": slot_id,
        "state_before": state,
        "state_verification": verified,
        "manifest_path": str(manifest_path),
        "manifest_sha256": sha256_file(manifest_path),
        "release_package_path": str(release_package),
        "release_package_sha256": sha256_file(release_package),
        "fieldnames": fieldnames,
        "rows": rows,
        "row_index": row_index,
        "row_before": dict(row),
        "row_after": planned,
        "tracker_before_bytes": tracker_before,
        "tracker_before_sha256": sha256_bytes(tracker_before),
        "publish_time": desired_time,
        "post_receipt_path": str(post_receipt),
        "tracker_receipt_path": str(tracker_receipt),
    }


def preflight(args: argparse.Namespace, runtime: dict[str, Any]) -> None:
    plan = preflight_internal(args, runtime)
    emit({
        "ok": True,
        "mode": "preflight",
        "slot_id": plan["slot_id"],
        "current_stage": plan["state_before"]["current_stage"],
        "tracker": plan["tracker"],
        "tracker_row_before": critical_snapshot(plan["row_before"]),
        "tracker_row_after": critical_snapshot(plan["row_after"]),
        "tracker_before_sha256": plan["tracker_before_sha256"],
        "publish_time": plan["publish_time"],
        "writes_performed": False,
    })


def write_receipts(args: argparse.Namespace, runtime: dict[str, Any], plan: dict[str, Any], tracker_after_sha: str) -> tuple[Path, Path]:
    slot_root = Path(plan["slot_root"])
    tracker_receipt = Path(plan["tracker_receipt_path"])
    post_receipt = Path(plan["post_receipt_path"])
    created_at = statectl.now_iso()
    tracker_payload = {
        "receipt_version": "1.0",
        "receipt_type": "TRACKER_SYNC",
        "status": "PASS",
        "slot_id": plan["slot_id"],
        "tracker_path": plan["tracker"],
        "tracker_before_sha256": plan["tracker_before_sha256"],
        "tracker_after_sha256": tracker_after_sha,
        "row_index_zero_based": plan["row_index"],
        "row_before_critical": critical_snapshot(plan["row_before"]),
        "row_after_critical": critical_snapshot(plan["row_after"]),
        "metrics_preserved": {key: plan["row_after"].get(key, "") for key in REQUIRED_TRACKER_COLUMNS if key not in PUBLISH_CRITICAL_FIELDS and key != "notes"},
        "created_at": created_at,
    }
    atomic_text(tracker_receipt, receipt_markdown("TRACKER_SYNC_RECEIPT", tracker_payload))
    tracker_receipt_sha = sha256_file(tracker_receipt)
    post_payload = {
        "receipt_version": "1.0",
        "receipt_type": "POST_PUBLISH_SYNC",
        "status": "PASS",
        "slot_id": plan["slot_id"],
        "publish_confirmation_source": args.confirmation_source.strip(),
        "publish_time": plan["publish_time"],
        "publish_time_pending_backfill": plan["publish_time"] == PENDING_TIME,
        "state_before_stage": plan["state_before"]["current_stage"],
        "state_before_token": plan["state_before"]["current_state_token"],
        "slot_manifest_sha256": plan["manifest_sha256"],
        "release_package_sha256": plan["release_package_sha256"],
        "tracker_receipt_path": str(tracker_receipt.relative_to(slot_root)),
        "tracker_receipt_sha256": tracker_receipt_sha,
        "tracker_after_sha256": tracker_after_sha,
        "row_after_critical": critical_snapshot(plan["row_after"]),
        "created_at": created_at,
    }
    atomic_text(post_receipt, receipt_markdown("POST_PUBLISH_SYNC_RECEIPT", post_payload))
    return tracker_receipt, post_receipt


def rollback_publish_writes(plan: dict[str, Any], receipt_paths: list[Path]) -> None:
    atomic_bytes(Path(plan["tracker"]), plan["tracker_before_bytes"])
    for path in receipt_paths:
        path.unlink(missing_ok=True)


def validate_publish_artifacts(runtime: dict[str, Any], slot_root: Path) -> dict[str, Any]:
    results: dict[str, Any] = {}
    for artifact_id in ("TRACKER_SYNC_RECEIPT", "POST_PUBLISH_SYNC_RECEIPT"):
        definition = statectl.artifacts(runtime)[artifact_id]
        result = gate.check_artifact(slot_root, definition)
        results[artifact_id] = result.__dict__
        if not result.ok or result.source != "canonical":
            fail("generated publish receipt failed canonical artifact validation", results)
    return results


def sync(args: argparse.Namespace, runtime: dict[str, Any]) -> None:
    if not args.confirmation_source.strip():
        fail("sync requires a non-empty real-world publish confirmation source")
    plan = preflight_internal(args, runtime)
    tracker_path = Path(plan["tracker"])
    rows = list(plan["rows"])
    rows[plan["row_index"]] = dict(plan["row_after"])
    tracker_after_bytes = serialize_tracker(plan["fieldnames"], rows)
    tracker_after_sha = sha256_bytes(tracker_after_bytes)
    receipt_paths: list[Path] = []
    try:
        atomic_bytes(tracker_path, tracker_after_bytes)
        tracker_receipt, post_receipt = write_receipts(args, runtime, plan, tracker_after_sha)
        receipt_paths = [tracker_receipt, post_receipt]
        receipt_validation = validate_publish_artifacts(runtime, Path(plan["slot_root"]))
        report = statectl.canonical_audit(
            Path(plan["slot_root"]), runtime, dict(plan["state_before"]["context"]), S17
        )
        if not report.get("ok"):
            fail("S17 evidence chain does not validate after publish sync", report)

        command = [
            sys.executable,
            str(Path(statectl.__file__).resolve()),
            "--registry-dir", str(args.registry_dir.resolve()),
            "advance",
            "--slot-root", str(Path(plan["slot_root"])),
            "--to", S17,
        ]
        result = subprocess.run(command, text=True, capture_output=True)
        if result.returncode != 0:
            fail(
                "state controller refused S16 -> S17; publish transaction rolled back",
                {"returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr},
            )
        verified = statectl.verify_state_internal(Path(plan["slot_root"]), runtime)
    except SystemExit:
        rollback_publish_writes(plan, receipt_paths)
        raise
    except Exception as exc:
        rollback_publish_writes(plan, receipt_paths)
        fail("unexpected publish transaction failure; writes rolled back", repr(exc))

    emit({
        "ok": True,
        "mode": "sync",
        "slot_id": plan["slot_id"],
        "tracker": plan["tracker"],
        "tracker_before_sha256": plan["tracker_before_sha256"],
        "tracker_after_sha256": tracker_after_sha,
        "tracker_row_after": critical_snapshot(plan["row_after"]),
        "receipts": [str(path.relative_to(Path(plan["slot_root"]))) for path in receipt_paths],
        "receipt_validation": receipt_validation,
        "state": verified,
    })


def verify(args: argparse.Namespace, runtime: dict[str, Any]) -> None:
    slot_root = args.slot_root.resolve()
    tracker = args.tracker.resolve()
    state_verified = statectl.verify_state_internal(slot_root, runtime)
    state = statectl.load_canonical_state(slot_root, runtime)
    stage_ids = [item["id"] for item in statectl.stages(runtime)]
    if stage_ids.index(state["current_stage"]) < stage_ids.index(S17):
        fail("publish verification requires state at S17 or later", state["current_stage"])

    tracker_receipt_path = artifact_path(runtime, slot_root, "TRACKER_SYNC_RECEIPT")
    post_receipt_path = artifact_path(runtime, slot_root, "POST_PUBLISH_SYNC_RECEIPT")
    tracker_receipt = parse_receipt(tracker_receipt_path)
    post_receipt = parse_receipt(post_receipt_path)
    for label, payload in (("tracker", tracker_receipt), ("post_publish", post_receipt)):
        if payload.get("status") != "PASS" or payload.get("slot_id") != state["slot_id"]:
            fail("publish receipt status/slot mismatch", {"receipt": label, "payload": payload})
    if post_receipt.get("tracker_receipt_sha256") != sha256_file(tracker_receipt_path):
        fail("POST_PUBLISH receipt no longer points to the current TRACKER_SYNC receipt")

    fieldnames, rows, tracker_bytes = load_tracker(tracker)
    del fieldnames
    _, row = unique_tracker_row(rows, state["slot_id"])
    expected = tracker_receipt.get("row_after_critical")
    actual = critical_snapshot(row)
    if not isinstance(expected, dict) or actual != expected:
        fail("tracker publish-critical fields diverged from locked publish receipt", {"expected": expected, "actual": actual})

    manifest = statectl.manifest_path(slot_root, runtime)
    release = require_canonical_artifact(runtime, slot_root, "RELEASE_PACKAGE")
    if post_receipt.get("slot_manifest_sha256") != sha256_file(manifest):
        fail("slot manifest changed after publish receipt")
    if post_receipt.get("release_package_sha256") != sha256_file(release):
        fail("release package changed after publish receipt")

    current_tracker_sha = sha256_bytes(tracker_bytes)
    exact_tracker_file_match = current_tracker_sha == tracker_receipt.get("tracker_after_sha256")
    warnings: list[str] = []
    if not exact_tracker_file_match:
        warnings.append(
            "tracker file hash changed after publish sync, but publish-critical row fields still match; "
            "this is expected when post-publish metrics/notes are appended"
        )
    emit({
        "ok": True,
        "mode": "verify",
        "slot_id": state["slot_id"],
        "current_stage": state["current_stage"],
        "state_verified": state_verified,
        "tracker_publish_critical_match": True,
        "tracker_exact_file_hash_match": exact_tracker_file_match,
        "warnings": warnings,
    })


def add_common_publish_args(parser: argparse.ArgumentParser, *, confirmation: bool) -> None:
    parser.add_argument("--slot-root", required=True, type=Path)
    parser.add_argument("--tracker", type=Path, default=DEFAULT_TRACKER)
    parser.add_argument("--song-family", required=True)
    parser.add_argument("--audio-asset", required=True)
    parser.add_argument("--packaging")
    parser.add_argument("--publish-time")
    if confirmation:
        parser.add_argument("--confirmation-source", required=True)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Transactional publish/30D60 tracker sync for canonical MV Runtime.")
    p.add_argument("--registry-dir", type=Path, default=RUNTIME_DIR)
    sub = p.add_subparsers(dest="command", required=True)
    pre = sub.add_parser("preflight")
    add_common_publish_args(pre, confirmation=False)
    syn = sub.add_parser("sync")
    add_common_publish_args(syn, confirmation=True)
    ver = sub.add_parser("verify")
    ver.add_argument("--slot-root", required=True, type=Path)
    ver.add_argument("--tracker", type=Path, default=DEFAULT_TRACKER)
    return p


def main() -> None:
    args = parser().parse_args()
    runtime = statectl.load_runtime(args.registry_dir.resolve())
    if args.command == "preflight":
        preflight(args, runtime)
    elif args.command == "sync":
        sync(args, runtime)
    elif args.command == "verify":
        verify(args, runtime)
    else:
        fail("unknown command", args.command, 2)


if __name__ == "__main__":
    main()
