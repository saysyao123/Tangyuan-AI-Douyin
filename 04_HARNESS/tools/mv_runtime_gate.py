#!/usr/bin/env python3
"""Machine-enforced MV Runtime stage/artifact validator.

P0 scope is intentionally read-only:
- registry-check
- artifact-check
- validate-stage (strict cumulative chain)
- audit-slot
- explain-stage

It never advances CURRENT_STATE. A later P0/P1 transition tool may consume its PASS
result, but state mutation must stay separate from evidence validation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable


SCRIPT_PATH = Path(__file__).resolve()
DEFAULT_REGISTRY_DIR = SCRIPT_PATH.parent.parent / "runtime"
STAGE_REGISTRY_NAME = "mv_stage_registry.json"
ARTIFACT_REGISTRY_NAME = "mv_artifact_registry.json"


@dataclass
class ArtifactResult:
    artifact_id: str
    ok: bool
    path: str | None
    source: str | None
    canonical_path: str
    errors: list[str]
    warnings: list[str]


@dataclass
class StageResult:
    stage_id: str
    label: str
    own_ok: bool
    chain_ok: bool
    required_artifacts: list[str]
    failed_artifacts: list[str]
    legacy_artifacts: list[str]


def die(message: str, code: int = 2) -> None:
    print(json.dumps({"ok": False, "error": message}, ensure_ascii=False, indent=2))
    raise SystemExit(code)


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        die(f"missing registry: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        die(f"invalid JSON registry {path}: {exc}")
    if not isinstance(payload, dict):
        die(f"registry root must be an object: {path}")
    return payload


def load_registries(registry_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    stage = load_json(registry_dir / STAGE_REGISTRY_NAME)
    artifact = load_json(registry_dir / ARTIFACT_REGISTRY_NAME)
    return stage, artifact


def index_by_id(items: Iterable[dict[str, Any]], label: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id:
            die(f"{label} item missing string id")
        if item_id in result:
            die(f"duplicate {label} id: {item_id}")
        result[item_id] = item
    return result


def normalize_context(stage_registry: dict[str, Any], args: argparse.Namespace) -> dict[str, bool]:
    defaults = stage_registry.get("default_context") or {}
    context: dict[str, bool] = {}
    for key in ("web", "multi_shot", "program_30d60"):
        value = getattr(args, key, None)
        if value is None:
            value = bool(defaults.get(key, False))
        context[key] = bool(value)
    return context


def bool_arg(value: str) -> bool:
    lowered = value.strip().lower()
    if lowered in {"1", "true", "yes", "y", "on"}:
        return True
    if lowered in {"0", "false", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"expected true/false, got {value!r}")


def condition_matches(condition: dict[str, Any], context: dict[str, bool]) -> bool:
    for key, expected in condition.items():
        if context.get(key) != expected:
            return False
    return True


def effective_stage_artifacts(stage: dict[str, Any], context: dict[str, bool]) -> list[str]:
    artifacts = list(stage.get("required_artifacts") or [])
    for conditional in stage.get("conditional_requirements") or []:
        if condition_matches(conditional.get("when") or {}, context):
            artifacts.extend(conditional.get("required_artifacts") or [])
    # Preserve declared order while deduplicating.
    return list(dict.fromkeys(str(item) for item in artifacts))


def registry_check(stage_registry: dict[str, Any], artifact_registry: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    stages = stage_registry.get("stages")
    artifacts = artifact_registry.get("artifacts")
    if not isinstance(stages, list) or not stages:
        errors.append("stage registry must contain non-empty stages[]")
        stages = []
    if not isinstance(artifacts, list) or not artifacts:
        errors.append("artifact registry must contain non-empty artifacts[]")
        artifacts = []

    try:
        stage_by_id = index_by_id(stages, "stage")
        artifact_by_id = index_by_id(artifacts, "artifact")
    except SystemExit:
        raise

    orders: dict[int, str] = {}
    previous_order: int | None = None
    for stage in sorted(stages, key=lambda item: item.get("order", -1)):
        stage_id = stage.get("id", "<missing>")
        order = stage.get("order")
        if not isinstance(order, int):
            errors.append(f"{stage_id}: order must be int")
            continue
        if order in orders:
            errors.append(f"duplicate stage order {order}: {orders[order]} and {stage_id}")
        orders[order] = stage_id
        if previous_order is not None and order <= previous_order:
            errors.append(f"stage order not strictly increasing near {stage_id}")
        previous_order = order

        refs = list(stage.get("required_artifacts") or [])
        for conditional in stage.get("conditional_requirements") or []:
            refs.extend(conditional.get("required_artifacts") or [])
        for artifact_id in refs:
            if artifact_id not in artifact_by_id:
                errors.append(f"{stage_id}: unknown artifact id {artifact_id}")

    canonical_paths: dict[str, str] = {}
    for artifact_id, artifact in artifact_by_id.items():
        canonical = artifact.get("canonical_path")
        if not isinstance(canonical, str) or not canonical:
            errors.append(f"{artifact_id}: missing canonical_path")
            continue
        if canonical in canonical_paths:
            errors.append(
                f"duplicate canonical path {canonical}: {canonical_paths[canonical]} and {artifact_id}"
            )
        canonical_paths[canonical] = artifact_id
        if canonical.startswith("/") or ".." in Path(canonical).parts:
            errors.append(f"{artifact_id}: unsafe canonical_path {canonical}")

    if stage_registry.get("human_gates") != ["HG01", "HG02", "HG03", "HG04", "HG05"]:
        warnings.append("human_gates differs from current five-gate Golden Runtime")

    return {
        "ok": not errors,
        "stage_count": len(stage_by_id),
        "artifact_count": len(artifact_by_id),
        "errors": errors,
        "warnings": warnings,
    }


def find_artifact_path(slot_root: Path, artifact: dict[str, Any]) -> tuple[Path | None, str | None, list[str]]:
    canonical = slot_root / artifact["canonical_path"]
    warnings: list[str] = []
    if canonical.is_file():
        return canonical, "canonical", warnings

    matches: list[Path] = []
    for pattern in artifact.get("legacy_patterns") or []:
        matches.extend(path for path in slot_root.glob(pattern) if path.is_file())
    # De-duplicate paths and prefer newest lexical version (v2 > v1 in common names).
    unique = sorted({path.resolve() for path in matches}, key=lambda p: str(p), reverse=True)
    if unique:
        chosen = unique[0]
        warnings.append(
            f"legacy alias used: {chosen.relative_to(slot_root.resolve())}; canonical is {artifact['canonical_path']}"
        )
        if len(unique) > 1:
            warnings.append(
                "multiple legacy candidates found: "
                + ", ".join(str(path.relative_to(slot_root.resolve())) for path in unique)
            )
        return chosen, "legacy", warnings
    return None, None, warnings


def run_artifact_checks(path: Path, artifact: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    for check in artifact.get("checks") or []:
        check_type = check.get("type")
        if check_type == "min_size":
            minimum = int(check.get("bytes", 1))
            try:
                size = path.stat().st_size
            except OSError as exc:
                errors.append(f"stat failed: {exc}")
                continue
            if size < minimum:
                errors.append(f"file too small: {size} < {minimum} bytes")
        elif check_type == "json_object":
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                errors.append(f"invalid JSON: {exc}")
                continue
            if not isinstance(payload, dict):
                errors.append("JSON root must be an object")
        elif check_type == "text_regex":
            pattern = check.get("pattern")
            if not isinstance(pattern, str) or not pattern:
                errors.append("text_regex check has empty pattern")
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError as exc:
                errors.append(f"read failed: {exc}")
                continue
            if re.search(pattern, text) is None:
                errors.append(f"required text pattern not found: {pattern}")
        else:
            errors.append(f"unsupported artifact check type: {check_type}")
    return errors, warnings


def check_artifact(slot_root: Path, artifact: dict[str, Any]) -> ArtifactResult:
    path, source, warnings = find_artifact_path(slot_root, artifact)
    if path is None:
        return ArtifactResult(
            artifact_id=artifact["id"],
            ok=False,
            path=None,
            source=None,
            canonical_path=artifact["canonical_path"],
            errors=["artifact not found"],
            warnings=warnings,
        )
    errors, check_warnings = run_artifact_checks(path, artifact)
    warnings.extend(check_warnings)
    return ArtifactResult(
        artifact_id=artifact["id"],
        ok=not errors,
        path=str(path.relative_to(slot_root)),
        source=source,
        canonical_path=artifact["canonical_path"],
        errors=errors,
        warnings=warnings,
    )


def sorted_stages(stage_registry: dict[str, Any]) -> list[dict[str, Any]]:
    return sorted(stage_registry["stages"], key=lambda item: item["order"])


def audit_slot(
    slot_root: Path,
    stage_registry: dict[str, Any],
    artifact_registry: dict[str, Any],
    context: dict[str, bool],
    stop_at: str | None = None,
) -> dict[str, Any]:
    if not slot_root.is_dir():
        die(f"slot root does not exist: {slot_root}")

    artifact_by_id = index_by_id(artifact_registry["artifacts"], "artifact")
    stages = sorted_stages(stage_registry)
    stage_ids = {stage["id"] for stage in stages}
    if stop_at is not None and stop_at not in stage_ids:
        die(f"unknown stage: {stop_at}")

    artifact_cache: dict[str, ArtifactResult] = {}
    stage_results: list[StageResult] = []
    chain_ok = True
    highest_valid_stage: str | None = None

    for stage in stages:
        required = effective_stage_artifacts(stage, context)
        failed: list[str] = []
        legacy: list[str] = []
        for artifact_id in required:
            if artifact_id not in artifact_cache:
                artifact_cache[artifact_id] = check_artifact(slot_root, artifact_by_id[artifact_id])
            result = artifact_cache[artifact_id]
            if not result.ok:
                failed.append(artifact_id)
            if result.source == "legacy":
                legacy.append(artifact_id)

        own_ok = not failed
        chain_ok = chain_ok and own_ok
        if chain_ok:
            highest_valid_stage = stage["id"]
        stage_results.append(
            StageResult(
                stage_id=stage["id"],
                label=stage.get("label", stage["id"]),
                own_ok=own_ok,
                chain_ok=chain_ok,
                required_artifacts=required,
                failed_artifacts=failed,
                legacy_artifacts=legacy,
            )
        )
        if stop_at is not None and stage["id"] == stop_at:
            break

    legacy_count = sum(1 for item in artifact_cache.values() if item.source == "legacy")
    failed_count = sum(1 for item in artifact_cache.values() if not item.ok)
    target_result = stage_results[-1] if stage_results else None

    declared_state: Any = None
    state_result = artifact_cache.get("STATE_LEDGER")
    if state_result and state_result.path:
        state_path = slot_root / state_result.path
        if state_path.suffix.lower() == ".json":
            try:
                state_payload = json.loads(state_path.read_text(encoding="utf-8"))
                declared_state = state_payload.get("status") or state_payload.get("state")
            except Exception:
                declared_state = None

    return {
        "ok": bool(target_result and target_result.chain_ok),
        "slot_root": str(slot_root),
        "context": context,
        "target_stage": stop_at or (stage_results[-1].stage_id if stage_results else None),
        "highest_contiguous_valid_stage": highest_valid_stage,
        "declared_state": declared_state,
        "artifact_summary": {
            "checked": len(artifact_cache),
            "failed": failed_count,
            "legacy_aliases_used": legacy_count,
        },
        "stages": [asdict(item) for item in stage_results],
        "artifacts": {key: asdict(value) for key, value in artifact_cache.items()},
    }


def explain_stage(stage_registry: dict[str, Any], context: dict[str, bool], stage_id: str) -> dict[str, Any]:
    stage_by_id = index_by_id(stage_registry["stages"], "stage")
    if stage_id not in stage_by_id:
        die(f"unknown stage: {stage_id}")
    stage = dict(stage_by_id[stage_id])
    stage["effective_required_artifacts"] = effective_stage_artifacts(stage, context)
    stage["context"] = context
    return {"ok": True, "stage": stage}


def add_context_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--web", type=bool_arg, default=None, help="true/false; default from stage registry")
    parser.add_argument(
        "--multi-shot", dest="multi_shot", type=bool_arg, default=None, help="true/false; default from registry"
    )
    parser.add_argument(
        "--program-30d60", dest="program_30d60", type=bool_arg, default=None, help="true/false; default from registry"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate Tangyuan AI MV Runtime stages and artifacts.")
    parser.add_argument("--registry-dir", type=Path, default=DEFAULT_REGISTRY_DIR)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("registry-check", help="Validate stage/artifact registry integrity.")

    artifact = sub.add_parser("artifact-check", help="Validate one artifact in a slot.")
    artifact.add_argument("--slot-root", required=True, type=Path)
    artifact.add_argument("--artifact", required=True)

    validate = sub.add_parser("validate-stage", help="Validate the entire chain through one target stage.")
    validate.add_argument("--slot-root", required=True, type=Path)
    validate.add_argument("--stage", required=True)
    add_context_args(validate)

    audit = sub.add_parser("audit-slot", help="Audit all stages and report the highest contiguous valid stage.")
    audit.add_argument("--slot-root", required=True, type=Path)
    add_context_args(audit)

    explain = sub.add_parser("explain-stage", help="Show one stage and its effective requirements.")
    explain.add_argument("--stage", required=True)
    add_context_args(explain)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    registry_dir = args.registry_dir.resolve()
    stage_registry, artifact_registry = load_registries(registry_dir)

    integrity = registry_check(stage_registry, artifact_registry)
    if not integrity["ok"]:
        print(json.dumps(integrity, ensure_ascii=False, indent=2))
        return 2

    if args.command == "registry-check":
        print(json.dumps(integrity, ensure_ascii=False, indent=2))
        return 0

    if args.command == "artifact-check":
        artifact_by_id = index_by_id(artifact_registry["artifacts"], "artifact")
        if args.artifact not in artifact_by_id:
            die(f"unknown artifact: {args.artifact}")
        result = check_artifact(args.slot_root.resolve(), artifact_by_id[args.artifact])
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
        return 0 if result.ok else 1

    context = normalize_context(stage_registry, args)

    if args.command == "validate-stage":
        report = audit_slot(
            args.slot_root.resolve(),
            stage_registry,
            artifact_registry,
            context,
            stop_at=args.stage,
        )
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["ok"] else 1

    if args.command == "audit-slot":
        report = audit_slot(
            args.slot_root.resolve(), stage_registry, artifact_registry, context
        )
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["ok"] else 1

    if args.command == "explain-stage":
        report = explain_stage(stage_registry, context, args.stage)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    die(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
