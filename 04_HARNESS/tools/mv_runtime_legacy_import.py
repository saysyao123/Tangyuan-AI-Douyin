#!/usr/bin/env python3
"""Controlled legacy-slot import into canonical MV Runtime.

This tool does not trust a legacy CURRENT_STATE declaration. It only imports the
explicit source evidence required by a registered profile, reconstructs the
minimum canonical machine packages with provenance, and then delegates every
forward stage transition to mv_runtime_state.py.

Current profile boundary:
  LEGACY_PRE_DIRECTOR_S04 -> S04_NATURAL_BEAT_LOCKED

S05+ and real-world publication are deliberately not inferred.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import mv_runtime_state as statectl

SCRIPT_PATH = Path(__file__).resolve()
RUNTIME_DIR = SCRIPT_PATH.parent.parent / "runtime"
CONTRACT_NAME = "mv_legacy_import_contract.json"
STATE_TOOL = SCRIPT_PATH.parent / "mv_runtime_state.py"
IMPORT_RECEIPT = "00_STATE/LEGACY_IMPORT_RECEIPT.json"


class ImportFatal(RuntimeError):
    pass


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
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_contract(registry_dir: Path) -> dict[str, Any]:
    return statectl.load_json(registry_dir / CONTRACT_NAME)


def parse_source_bindings(items: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise ImportFatal(f"--source must use KIND=relative/path syntax: {item!r}")
        kind, value = item.split("=", 1)
        kind = kind.strip()
        value = value.strip()
        if not kind or not value:
            raise ImportFatal(f"invalid --source binding: {item!r}")
        if kind in result:
            raise ImportFatal(f"duplicate --source binding for {kind}")
        result[kind] = value
    return result


def resolve_inside(slot_root: Path, rel: str) -> Path:
    path = (slot_root / rel).resolve()
    try:
        path.relative_to(slot_root.resolve())
    except ValueError as exc:
        raise ImportFatal(f"source escapes slot root: {rel}") from exc
    return path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise ImportFatal(f"unreadable UTF-8 source: {path}") from exc


def load_json_file(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        raise ImportFatal(f"invalid JSON source: {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ImportFatal(f"JSON source root must be object: {path}")
    return payload


def extract_hg01_song(text: str) -> str:
    patterns = [
        r"Selected\s+`?SONG_FAMILY`?\s*:\s*\n+\s*`([^`]+)`",
        r"Selected\s+SONG_FAMILY\s*:\s*([^\n]+)",
        r"song[_ ]family\s*[:=]\s*`?([^`\n]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1).strip().strip("`")
    raise ImportFatal("HG01 selected song family could not be extracted")


def extract_markdown_field(text: str, label: str) -> str | None:
    match = re.search(
        rf"^\s*(?:[-*]\s*)?{re.escape(label)}\s*:\s*`?([^`\n]+)",
        text,
        flags=re.IGNORECASE | re.MULTILINE,
    )
    return match.group(1).strip() if match else None


def extract_sha(text: str, label: str) -> str | None:
    match = re.search(
        rf"{re.escape(label)}[^\n]*?([a-f0-9]{{64}})",
        text,
        flags=re.IGNORECASE,
    )
    return match.group(1).lower() if match else None


def extract_candidates(text: str) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    for match in re.finditer(
        r"^##\s+Candidate\s+([A-Z])(?:｜|\|)\s*([^\n]+)",
        text,
        flags=re.MULTILINE,
    ):
        found.append({"candidate_id": match.group(1), "song_family": match.group(2).strip()})
    return found


def directory_inventory(directory: Path, slot_root: Path) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    for path in sorted(p for p in directory.rglob("*") if p.is_file()):
        values.append(
            {
                "path": str(path.relative_to(slot_root)),
                "sha256": sha256_file(path),
                "bytes": path.stat().st_size,
            }
        )
    return values


def source_inventory(
    slot_root: Path,
    bindings: dict[str, str],
    contract: dict[str, Any],
    profile: dict[str, Any],
) -> tuple[dict[str, Path], list[dict[str, Any]]]:
    required = profile["required_sources"]
    missing = [kind for kind in required if kind not in bindings]
    extra = sorted(set(bindings) - set(contract["source_kinds"]))
    if missing:
        raise ImportFatal("missing required source bindings: " + ", ".join(missing))
    if extra:
        raise ImportFatal("unknown source kinds: " + ", ".join(extra))
    resolved: dict[str, Path] = {}
    inventory: list[dict[str, Any]] = []
    for kind in required:
        path = resolve_inside(slot_root, bindings[kind])
        expected = contract["source_kinds"][kind]
        if expected == "file" and not path.is_file():
            raise ImportFatal(f"{kind} must be a file: {bindings[kind]}")
        if expected == "directory" and not path.is_dir():
            raise ImportFatal(f"{kind} must be a directory: {bindings[kind]}")
        resolved[kind] = path
        if expected == "file":
            inventory.append(
                {
                    "kind": kind,
                    "path": bindings[kind],
                    "type": "file",
                    "sha256": sha256_file(path),
                    "bytes": path.stat().st_size,
                }
            )
        else:
            files = directory_inventory(path, slot_root)
            if not files:
                raise ImportFatal(f"{kind} directory contains no files")
            inventory.append(
                {
                    "kind": kind,
                    "path": bindings[kind],
                    "type": "directory",
                    "files": files,
                    "tree_fingerprint_sha256": sha256_bytes(
                        json.dumps(files, sort_keys=True, ensure_ascii=False).encode("utf-8")
                    ),
                }
            )
    return resolved, inventory


def validate_evidence(
    slot_root: Path,
    resolved: dict[str, Path],
    inventory: list[dict[str, Any]],
    profile_name: str,
    profile: dict[str, Any],
) -> dict[str, Any]:
    legacy_state = load_json_file(resolved["LEGACY_STATE"])
    hg01_pack = read_text(resolved["HG01_CANDIDATE_EVIDENCE"])
    hg01_receipt = read_text(resolved["HG01_SELECTION_RECEIPT"])
    hg02_pack = read_text(resolved["HG02_LISTENING_PACK"])
    hg02_receipt = read_text(resolved["HG02_LOCK_RECEIPT"])
    natural_beat = read_text(resolved["NATURAL_BEAT"])

    if legacy_state.get("slot_id") != slot_root.name:
        raise ImportFatal("legacy state slot_id does not match slot directory")
    lane = str(legacy_state.get("lane") or "").strip()
    song = str(legacy_state.get("song_family") or "").strip()
    if not lane or not song:
        raise ImportFatal("legacy state must contain non-empty lane and song_family")

    if not re.search(r"\bPASS\b", hg01_receipt, flags=re.IGNORECASE):
        raise ImportFatal("legacy HG01 receipt does not contain explicit PASS evidence")
    selected_song = extract_hg01_song(hg01_receipt)
    if selected_song != song:
        raise ImportFatal(
            f"HG01 selected song disagrees with legacy state: {selected_song!r} != {song!r}"
        )
    if song not in hg01_pack:
        raise ImportFatal("selected song is absent from HG01 candidate evidence pack")
    candidates = extract_candidates(hg01_pack)
    if not candidates:
        raise ImportFatal("HG01 candidate evidence pack contains no parseable formal candidates")
    if song not in {item["song_family"] for item in candidates}:
        raise ImportFatal("selected song is not one of the parsed HG01 formal candidates")

    if not re.search(r"(HG02_PASS|BGM_LOCKED|\bPASS\b)", hg02_receipt, flags=re.IGNORECASE):
        raise ImportFatal("legacy HG02 receipt does not contain explicit PASS/LOCK evidence")
    if song not in hg02_pack or song not in hg02_receipt:
        raise ImportFatal("HG02 pack/receipt song family disagrees with HG01/legacy state")

    source_sha = extract_sha(hg02_receipt, "Source direct-asset SHA256")
    rendered_sha = extract_sha(hg02_receipt, "Locked rendered-file SHA256")
    if not source_sha or not rendered_sha:
        raise ImportFatal("HG02 lock receipt is missing locked source/rendered SHA256")
    if source_sha not in hg02_pack.lower():
        raise ImportFatal("HG02 listening pack does not contain the locked source SHA256")
    selected_option_match = re.search(
        r"(?:selected|explicitly selected)\s+\*{0,2}Option\s+([A-Z])",
        hg02_receipt,
        flags=re.IGNORECASE,
    )
    selected_option = selected_option_match.group(1).upper() if selected_option_match else None
    if selected_option is None:
        legacy_audio = legacy_state.get("audio_lock") or {}
        selected_option = str(legacy_audio.get("selected_option") or "").strip().upper() or None
    if not selected_option:
        raise ImportFatal("HG02 selected option could not be established")

    audio_dir = resolved["AUDIO_TIMELINE_DIR"]
    manifest_path = audio_dir / "package_manifest.json"
    qa_path = audio_dir / "alignment_qa_report.md"
    if not manifest_path.is_file() or not qa_path.is_file():
        raise ImportFatal("Audio Timeline directory must contain package_manifest.json and alignment_qa_report.md")
    manifest = load_json_file(manifest_path)
    qa_text = read_text(qa_path)
    if str(manifest.get("slot_id")) != slot_root.name:
        raise ImportFatal("Audio Timeline manifest slot_id mismatch")
    if manifest.get("song_family") != song:
        raise ImportFatal("Audio Timeline manifest song_family mismatch")
    if str(manifest.get("status", "")).upper() != "LOCKED":
        raise ImportFatal("Audio Timeline manifest is not LOCKED")
    if str(manifest.get("audio_source_sha256", "")).lower() != source_sha:
        raise ImportFatal("Audio Timeline source SHA does not match HG02 lock")
    if str(manifest.get("locked_rendered_audio_sha256", "")).lower() != rendered_sha:
        raise ImportFatal("Audio Timeline rendered SHA does not match HG02 lock")
    if (manifest.get("qa") or {}).get("decision") != "PASS":
        raise ImportFatal("Audio Timeline manifest QA decision is not PASS")
    if not re.search(r"(Status:\s*`?PASS|AUDIO_TIMELINE_PACKAGE\s*=\s*PASS)", qa_text, re.IGNORECASE):
        raise ImportFatal("Audio Timeline QA report does not contain PASS evidence")

    if not re.search(r"Status:\s*`?LOCKED", natural_beat, flags=re.IGNORECASE):
        raise ImportFatal("Natural Beat is not explicitly LOCKED")
    nb_song = extract_markdown_field(natural_beat, "Song")
    nb_lane = extract_markdown_field(natural_beat, "Lane")
    if nb_song and nb_song != song:
        raise ImportFatal("Natural Beat song mismatch")
    if nb_lane and nb_lane != lane:
        raise ImportFatal("Natural Beat lane mismatch")

    legacy_audio = legacy_state.get("audio_lock") or {}
    legacy_source_sha = str(legacy_audio.get("source_sha256") or "").lower()
    legacy_rendered_sha = str(legacy_audio.get("locked_file_sha256") or "").lower()
    if legacy_source_sha and legacy_source_sha != source_sha:
        raise ImportFatal("legacy state audio source SHA disagrees with HG02/Timeline")
    if legacy_rendered_sha and legacy_rendered_sha != rendered_sha:
        raise ImportFatal("legacy state rendered audio SHA disagrees with HG02/Timeline")

    return {
        "profile": profile_name,
        "slot_id": slot_root.name,
        "lane": lane,
        "song_family": song,
        "selected_hg01_song_family": selected_song,
        "hg01_candidates": candidates,
        "hg02_selected_option": selected_option,
        "audio_source_sha256": source_sha,
        "locked_rendered_audio_sha256": rendered_sha,
        "audio_timeline_status": manifest.get("status"),
        "audio_timeline_qa": (manifest.get("qa") or {}).get("decision"),
        "target_stage": profile["target_stage"],
        "downstream_not_proven_from_stage": profile["downstream_not_proven_from_stage"],
        "source_inventory": inventory,
    }


def plan_internal(
    slot_root: Path,
    registry_dir: Path,
    profile_name: str,
    bindings: dict[str, str],
) -> dict[str, Any]:
    contract = load_contract(registry_dir)
    if profile_name not in contract.get("profiles", {}):
        raise ImportFatal(f"unknown legacy import profile: {profile_name}")
    profile = contract["profiles"][profile_name]
    runtime = statectl.load_runtime(registry_dir)

    canonical_state = statectl.state_path(slot_root, runtime)
    if canonical_state.exists():
        raise ImportFatal("canonical CURRENT_STATE already exists; import will not overwrite it")

    resolved, inventory = source_inventory(slot_root, bindings, contract, profile)
    evidence = validate_evidence(slot_root, resolved, inventory, profile_name, profile)

    canonical_outputs = contract.get("canonical_outputs") or {}
    collisions: list[str] = []
    for rel in canonical_outputs.values():
        target = slot_root / rel
        if target.is_file():
            collisions.append(rel)
    if (slot_root / IMPORT_RECEIPT).exists():
        collisions.append(IMPORT_RECEIPT)
    if collisions:
        raise ImportFatal("canonical import outputs already exist: " + ", ".join(sorted(collisions)))

    plan_core = {
        "schema_version": contract["schema_version"],
        "profile": profile_name,
        "slot_id": evidence["slot_id"],
        "lane": evidence["lane"],
        "song_family": evidence["song_family"],
        "target_stage": evidence["target_stage"],
        "downstream_not_proven_from_stage": evidence["downstream_not_proven_from_stage"],
        "audio_source_sha256": evidence["audio_source_sha256"],
        "locked_rendered_audio_sha256": evidence["locked_rendered_audio_sha256"],
        "hg02_selected_option": evidence["hg02_selected_option"],
        "source_bindings": {kind: bindings[kind] for kind in profile["required_sources"]},
        "source_inventory": evidence["source_inventory"],
    }
    plan_sha = sha256_bytes(
        json.dumps(plan_core, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    )
    return {
        "ok": True,
        "mode": "PLAN",
        "plan_sha256": plan_sha,
        "plan": plan_core,
        "evidence": {
            "hg01_candidates": evidence["hg01_candidates"],
            "audio_timeline_status": evidence["audio_timeline_status"],
            "audio_timeline_qa": evidence["audio_timeline_qa"],
        },
    }


def run_controller(command: list[str]) -> dict[str, Any]:
    result = subprocess.run(command, text=True, capture_output=True)
    text = result.stdout.strip()
    payload: dict[str, Any] | None = None
    if text:
        try:
            parsed = json.loads(text)
            if isinstance(parsed, dict):
                payload = parsed
        except json.JSONDecodeError:
            payload = None
    if result.returncode != 0:
        raise ImportFatal(
            "authoritative state controller refused operation: "
            + json.dumps(
                {
                    "command": command[2:] if len(command) > 2 else command,
                    "returncode": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                },
                ensure_ascii=False,
            )
        )
    if payload is None:
        raise ImportFatal("state controller returned non-JSON output")
    return payload


def snapshot_canonical_paths(slot_root: Path, runtime: dict[str, Any]) -> set[str]:
    roots = {Path(rel).parts[0] for rel in runtime["scaffold"]["directories"]}
    existing: set[str] = set()
    for root_name in roots:
        root = slot_root / root_name
        if root.exists():
            existing.add(str(root.relative_to(slot_root)))
            if root.is_dir():
                for path in root.rglob("*"):
                    existing.add(str(path.relative_to(slot_root)))
    return existing


def rollback_new_canonical_paths(slot_root: Path, before: set[str], runtime: dict[str, Any]) -> None:
    roots = {Path(rel).parts[0] for rel in runtime["scaffold"]["directories"]}
    candidates: list[Path] = []
    for root_name in roots:
        root = slot_root / root_name
        if root.exists():
            candidates.append(root)
            if root.is_dir():
                candidates.extend(root.rglob("*"))
    for path in sorted(candidates, key=lambda p: len(p.parts), reverse=True):
        rel = str(path.relative_to(slot_root))
        if rel in before:
            continue
        if path.is_file() or path.is_symlink():
            path.unlink(missing_ok=True)
        elif path.is_dir():
            try:
                path.rmdir()
            except OSError:
                pass


def materialize_init_state(
    slot_root: Path,
    runtime: dict[str, Any],
    registry_dir: Path,
    slot_id: str,
    lane: str,
) -> None:
    with tempfile.TemporaryDirectory(prefix="mv-legacy-import-init-") as temp:
        temp_root = Path(temp) / slot_id
        run_controller(
            [
                sys.executable,
                str(STATE_TOOL),
                "--registry-dir",
                str(registry_dir),
                "init-slot",
                "--slot-root",
                str(temp_root),
                "--slot-id",
                slot_id,
                "--program",
                "30D_60",
                "--lane",
                lane,
            ]
        )
        source_state_root = temp_root / "00_STATE"
        target_state_root = slot_root / "00_STATE"
        if target_state_root.exists() and any(target_state_root.iterdir()):
            raise ImportFatal("00_STATE already exists and is non-empty")
        if target_state_root.exists():
            target_state_root.rmdir()
        shutil.copytree(source_state_root, target_state_root)

    for rel in runtime["scaffold"]["directories"]:
        (slot_root / rel).mkdir(parents=True, exist_ok=True)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    if path.exists():
        raise ImportFatal(f"refusing to overwrite canonical file: {path}")
    statectl.atomic_json(path, payload)


def copy_file_preserved(source: Path, target: Path) -> None:
    if target.exists():
        raise ImportFatal(f"refusing to overwrite canonical file: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(source.read_bytes())
    if sha256_file(source) != sha256_file(target):
        raise ImportFatal(f"byte-preserved copy hash mismatch: {source} -> {target}")


def copy_directory_preserved(source: Path, target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    if any(target.iterdir()):
        raise ImportFatal(f"canonical directory must be empty before preserved copy: {target}")
    for path in sorted(source.rglob("*")):
        rel = path.relative_to(source)
        destination = target / rel
        if path.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
        elif path.is_file():
            copy_file_preserved(path, destination)


def legacy_source_sha(plan: dict[str, Any], kind: str) -> str:
    for item in plan["source_inventory"]:
        if item["kind"] == kind:
            if item["type"] == "file":
                return item["sha256"]
            return item["tree_fingerprint_sha256"]
    raise ImportFatal(f"source inventory missing {kind}")


def import_slot(
    slot_root: Path,
    registry_dir: Path,
    profile_name: str,
    bindings: dict[str, str],
    expected_plan_sha: str,
    selected_by: str,
    reason: str,
) -> dict[str, Any]:
    if not selected_by.strip() or not reason.strip():
        raise ImportFatal("import requires non-empty selected_by and reason")
    plan_result = plan_internal(slot_root, registry_dir, profile_name, bindings)
    if plan_result["plan_sha256"] != expected_plan_sha:
        raise ImportFatal(
            f"plan hash mismatch; repository truth changed: expected {expected_plan_sha}, "
            f"actual {plan_result['plan_sha256']}"
        )

    runtime = statectl.load_runtime(registry_dir)
    plan = plan_result["plan"]
    before = snapshot_canonical_paths(slot_root, runtime)
    resolved = {kind: resolve_inside(slot_root, rel) for kind, rel in bindings.items()}

    try:
        materialize_init_state(slot_root, runtime, registry_dir, plan["slot_id"], plan["lane"])

        song_package = {
            "schema_version": "1.0",
            "status": "LEGACY_IMPORT_RECONSTRUCTED_MACHINE_PREFLIGHT",
            "slot_id": plan["slot_id"],
            "lane": plan["lane"],
            "formal_candidates": plan_result["evidence"]["hg01_candidates"],
            "selected_song_family": plan["song_family"],
            "provenance": {
                "candidate_evidence_source": bindings["HG01_CANDIDATE_EVIDENCE"],
                "candidate_evidence_sha256": legacy_source_sha(plan, "HG01_CANDIDATE_EVIDENCE"),
                "legacy_selection_receipt": bindings["HG01_SELECTION_RECEIPT"],
                "legacy_selection_receipt_sha256": legacy_source_sha(plan, "HG01_SELECTION_RECEIPT"),
                "import_plan_sha256": expected_plan_sha,
            },
        }
        write_json(slot_root / "01_SONG/SONG_CANDIDATE_SET.json", song_package)
        run_controller([
            sys.executable, str(STATE_TOOL), "--registry-dir", str(registry_dir),
            "record-human-gate", "--slot-root", str(slot_root), "--gate", "HG01",
            "--user-decision-text",
            "Legacy evidence import; original HG01 explicitly PASS selected "
            f"SONG_FAMILY={plan['song_family']}; source={bindings['HG01_SELECTION_RECEIPT']}; "
            f"sha256={legacy_source_sha(plan, 'HG01_SELECTION_RECEIPT')}",
            "--approved-artifact", bindings["HG01_SELECTION_RECEIPT"],
        ])
        run_controller([
            sys.executable, str(STATE_TOOL), "--registry-dir", str(registry_dir),
            "advance", "--slot-root", str(slot_root), "--to", "S01_HG01_SONG_LOCKED",
        ])

        bgm_package = {
            "schema_version": "1.0",
            "status": "LEGACY_IMPORT_RECONSTRUCTED_MACHINE_PREFLIGHT",
            "slot_id": plan["slot_id"],
            "song_family": plan["song_family"],
            "selected_option": plan["hg02_selected_option"],
            "audio_source_sha256": plan["audio_source_sha256"],
            "locked_rendered_audio_sha256": plan["locked_rendered_audio_sha256"],
            "provenance": {
                "listening_pack_source": bindings["HG02_LISTENING_PACK"],
                "listening_pack_sha256": legacy_source_sha(plan, "HG02_LISTENING_PACK"),
                "legacy_lock_receipt": bindings["HG02_LOCK_RECEIPT"],
                "legacy_lock_receipt_sha256": legacy_source_sha(plan, "HG02_LOCK_RECEIPT"),
                "import_plan_sha256": expected_plan_sha,
            },
        }
        write_json(slot_root / "02_BGM/BGM_CANDIDATE_PACKAGE.json", bgm_package)
        run_controller([
            sys.executable, str(STATE_TOOL), "--registry-dir", str(registry_dir),
            "record-human-gate", "--slot-root", str(slot_root), "--gate", "HG02",
            "--user-decision-text",
            "Legacy evidence import; original HG02 explicitly PASS selected "
            f"Option {plan['hg02_selected_option']}; audio_source_sha256={plan['audio_source_sha256']}; "
            f"source={bindings['HG02_LOCK_RECEIPT']}; sha256={legacy_source_sha(plan, 'HG02_LOCK_RECEIPT')}",
            "--approved-artifact", bindings["HG02_LOCK_RECEIPT"],
        ])
        run_controller([
            sys.executable, str(STATE_TOOL), "--registry-dir", str(registry_dir),
            "advance", "--slot-root", str(slot_root), "--to", "S02_HG02_BGM_LOCKED",
        ])

        copy_directory_preserved(resolved["AUDIO_TIMELINE_DIR"], slot_root / "03_AUDIO_TIMELINE")
        run_controller([
            sys.executable, str(STATE_TOOL), "--registry-dir", str(registry_dir),
            "advance", "--slot-root", str(slot_root), "--to", "S03_AUDIO_TIMELINE_LOCKED",
        ])

        copy_file_preserved(resolved["NATURAL_BEAT"], slot_root / "04_BEATS/NATURAL_BEAT.md")
        verified = run_controller([
            sys.executable, str(STATE_TOOL), "--registry-dir", str(registry_dir),
            "advance", "--slot-root", str(slot_root), "--to", "S04_NATURAL_BEAT_LOCKED",
        ])

        receipt_payload = {
            "receipt_version": "1.0",
            "status": "PASS",
            "profile": profile_name,
            "slot_id": plan["slot_id"],
            "imported_through_stage": "S04_NATURAL_BEAT_LOCKED",
            "downstream_not_proven_from_stage": plan["downstream_not_proven_from_stage"],
            "plan_sha256": expected_plan_sha,
            "selected_by": selected_by.strip(),
            "reason": reason.strip(),
            "legacy_sources": plan["source_inventory"],
            "canonical_state": {"current_stage": verified.get("to_stage"), "state_token": verified.get("state_token")},
            "safety_assertions": {
                "legacy_files_modified": false,
                "S05_and_later_imported": false,
                "S17_published_inferred": false
            } if False else {
                "legacy_files_modified": False,
                "S05_and_later_imported": False,
                "S17_published_inferred": False,
            },
            "created_at": statectl.now_iso(),
        }
        write_json(slot_root / IMPORT_RECEIPT, receipt_payload)
        final_state = run_controller([
            sys.executable, str(STATE_TOOL), "--registry-dir", str(registry_dir),
            "verify-state", "--slot-root", str(slot_root),
        ])
        return {
            "ok": True,
            "mode": "IMPORT",
            "profile": profile_name,
            "plan_sha256": expected_plan_sha,
            "import_receipt": IMPORT_RECEIPT,
            "state": final_state,
            "downstream_not_proven_from_stage": plan["downstream_not_proven_from_stage"],
        }
    except Exception:
        rollback_new_canonical_paths(slot_root, before, runtime)
        raise


def verify_import(slot_root: Path, registry_dir: Path) -> dict[str, Any]:
    receipt_path = slot_root / IMPORT_RECEIPT
    if not receipt_path.is_file():
        raise ImportFatal("legacy import receipt missing")
    receipt = load_json_file(receipt_path)
    if receipt.get("status") != "PASS":
        raise ImportFatal("legacy import receipt is not PASS")
    if receipt.get("imported_through_stage") != "S04_NATURAL_BEAT_LOCKED":
        raise ImportFatal("legacy import receipt exceeds or disagrees with the registered S04 boundary")
    if receipt.get("downstream_not_proven_from_stage") != "S05_DIRECTOR_PLAN_LOCKED":
        raise ImportFatal("legacy import receipt has invalid downstream proof boundary")
    safety = receipt.get("safety_assertions") or {}
    if safety.get("S05_and_later_imported") is not False or safety.get("S17_published_inferred") is not False:
        raise ImportFatal("legacy import safety assertions are invalid")

    failures: list[str] = []
    for source in receipt.get("legacy_sources") or []:
        kind = source.get("kind")
        rel = source.get("path")
        if not isinstance(rel, str):
            failures.append(f"{kind}: malformed source path")
            continue
        path = resolve_inside(slot_root, rel)
        if source.get("type") == "file":
            if not path.is_file() or sha256_file(path) != source.get("sha256"):
                failures.append(f"{kind}: legacy source missing or hash changed")
        elif source.get("type") == "directory":
            if not path.is_dir():
                failures.append(f"{kind}: legacy source directory missing")
                continue
            current = directory_inventory(path, slot_root)
            fingerprint = sha256_bytes(json.dumps(current, sort_keys=True, ensure_ascii=False).encode("utf-8"))
            if fingerprint != source.get("tree_fingerprint_sha256"):
                failures.append(f"{kind}: legacy source directory fingerprint changed")
        else:
            failures.append(f"{kind}: malformed source type")
    if failures:
        raise ImportFatal("legacy import provenance verification failed: " + "; ".join(failures))

    runtime = statectl.load_runtime(registry_dir)
    state = statectl.verify_state_internal(slot_root, runtime)
    indexes = statectl.stage_index(runtime)
    if indexes[state.get("current_stage")] < indexes["S04_NATURAL_BEAT_LOCKED"]:
        raise ImportFatal("active canonical state is earlier than the imported S04 evidence boundary")
    return {
        "ok": True,
        "mode": "VERIFY",
        "slot_id": receipt.get("slot_id"),
        "imported_through_stage": receipt.get("imported_through_stage"),
        "downstream_not_proven_from_stage": receipt.get("downstream_not_proven_from_stage"),
        "legacy_source_provenance": "PASS",
        "canonical_state": state,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Controlled legacy slot -> canonical_v2 import up to registered evidence boundary.")
    parser.add_argument("--registry-dir", type=Path, default=RUNTIME_DIR)
    sub = parser.add_subparsers(dest="command", required=True)

    pl = sub.add_parser("plan")
    pl.add_argument("--slot-root", required=True, type=Path)
    pl.add_argument("--profile", default="LEGACY_PRE_DIRECTOR_S04")
    pl.add_argument("--source", action="append", default=[], required=True)

    imp = sub.add_parser("import")
    imp.add_argument("--slot-root", required=True, type=Path)
    imp.add_argument("--profile", default="LEGACY_PRE_DIRECTOR_S04")
    imp.add_argument("--source", action="append", default=[], required=True)
    imp.add_argument("--plan-sha256", required=True)
    imp.add_argument("--selected-by", required=True)
    imp.add_argument("--reason", required=True)

    ver = sub.add_parser("verify")
    ver.add_argument("--slot-root", required=True, type=Path)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    registry_dir = args.registry_dir.resolve()
    try:
        if args.command in {"plan", "import"}:
            slot_root = args.slot_root.resolve()
            bindings = parse_source_bindings(args.source)
            if args.command == "plan":
                emit(plan_internal(slot_root, registry_dir, args.profile, bindings))
            else:
                emit(import_slot(slot_root, registry_dir, args.profile, bindings, args.plan_sha256, args.selected_by, args.reason))
        elif args.command == "verify":
            emit(verify_import(args.slot_root.resolve(), registry_dir))
        else:
            fail("unknown command", args.command, 2)
    except ImportFatal as exc:
        fail(str(exc))


if __name__ == "__main__":
    main()
