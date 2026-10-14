#!/usr/bin/env python3
"""Plus-only task preflight/QA controller. Requires no model API, key or third-party package.

ChatGPT Plus operates *outside* this script: the assistant researches and authors the
verified episode JSON in chat. This code verifies a handoff, invokes the existing free
cloud rendering workflow, and reports evidence rather than pretending to be an LLM.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
STATUS_PATH = HERE / "runs" / "latest_status.json"
SAFE_ID = re.compile(r"^[a-zA-Z0-9_-]{1,80}$")


class GateError(ValueError):
    pass


def within_repo(value: str) -> Path:
    if not isinstance(value, str) or not value:
        raise GateError("episode_path must be a nonempty repository-relative path")
    candidate = (REPO / value).resolve()
    if not candidate.is_relative_to(REPO.resolve()):
        raise GateError("episode_path escapes repository")
    if not candidate.is_file():
        raise GateError(f"episode not found: {value}")
    if candidate.suffix != ".json":
        raise GateError("episode_path must be JSON")
    return candidate


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise GateError(f"cannot read JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise GateError("root JSON must be an object")
    return value


def digest(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1048576), b""):
            sha.update(block)
    return sha.hexdigest()


def verify(task_path: Path) -> dict[str, Any]:
    task = load_json(task_path)
    if task.get("schema_version") != 1 or task.get("task_type") != "gossip_video":
        raise GateError("only gossip_video task schema_version=1 is supported in v0")
    task_id = task.get("task_id")
    if not isinstance(task_id, str) or SAFE_ID.fullmatch(task_id) is None:
        raise GateError("task_id must be 1-80 safe letters, digits, - or _")
    episode_path = within_repo(task.get("episode_path"))
    episode = load_json(episode_path)
    if episode.get("language") != "zh":
        raise GateError("Chinese only; episode.language must be zh")
    eid = episode.get("id")
    if not isinstance(eid, str) or SAFE_ID.fullmatch(eid) is None:
        raise GateError("episode.id must be safe and nonempty")
    if not episode.get("direction") or not episode.get("rows"):
        raise GateError("missing direction or scene rows")
    if episode["rows"][0].get("type") != "cover" or episode["rows"][-1].get("type") != "end":
        raise GateError("invalid shot bookends")
    demo = episode.get("technical_demo") is True
    if demo:
        if task.get("intent") != "technical_demo":
            raise GateError("technical_demo episode may only run with intent=technical_demo")
    else:
        if task.get("intent") != "editorial":
            raise GateError("real videos require intent=editorial")
        if not episode.get("editorial_review_complete"):
            raise GateError("editorial source review not completed")
        # Do not confuse public online availability with legal re-use permission.
        if not task.get("source_rights_review_complete"):
            raise GateError("source rights review is required before rendering a real episode")
        # Rights claims need a traceable evidence URL or permission record. Neither
        # a status flag nor this machine check proves that the claim is legally true.
        assets = episode.get("assets", {})
        for name, asset in assets.items():
            if asset.get("generate") == "testsrc2":
                raise GateError(f"technical fixture forbidden in editorial video: {name}")
            evidence = asset.get("license_evidence_url") or asset.get("permission_record")
            if not isinstance(evidence, str) or not evidence.strip():
                raise GateError(f"missing licensing evidence for {name}")
    return {
        "schema_version": 1,
        "task_id": task_id,
        "task_type": "gossip_video",
        "intent": task["intent"],
        "episode_id": eid,
        "episode_path": str(episode_path.relative_to(REPO)),
        "episode_sha256": digest(episode_path),
        "status": "ready_to_render",
        "model_api_used": False,
        "rights_status": "not_applicable_demo" if demo else "evidence_declared_unverified",
        "editorial_validation": "technical_demo" if demo else "declaration_only",
        "notes": "This validation does not prove source truth, licensing, visual quality, or voice naturalness.",
    }


def inspect(status: dict[str, Any]) -> dict[str, Any]:
    run = REPO / "gossip_video_workflow" / "runs" / status["episode_id"]
    state_path = run / "state.json"
    qa_path = run / "output" / "qa.json"
    video_path = run / "output" / "final_1080p.mp4"
    status = dict(status)
    if not all(x.is_file() for x in (state_path, qa_path, video_path)):
        status["status"] = "not_exported"
        status["missing"] = [str(x.relative_to(REPO)) for x in (state_path, qa_path, video_path) if not x.is_file()]
        return status
    state, qa = load_json(state_path), load_json(qa_path)
    # A previous successful export must never validate a newly edited episode.
    episode = load_json(REPO / status["episode_path"])
    expected_hash = hashlib.sha256(json.dumps(episode, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    if state.get("episodeHash") != expected_hash:
        status["status"] = "stale_output"
        status["reason"] = "render state belongs to a different episode revision"
        return status
    if state.get("stage") != "exported_awaiting_review":
        status["status"] = "needs_investigation"
        status["reason"] = f"unexpected render stage {state.get('stage')}"
        return status
    if qa.get("sha256") != digest(video_path) or state.get("videoSha256") != digest(video_path):
        status["status"] = "integrity_failure"
        status["reason"] = "encoded video SHA256 not consistent with reports"
        return status
    if qa.get("automaticTechnicalChecks") not in ("passed", "passed_with_visual_warnings"):
        status["status"] = "needs_investigation"
        status["reason"] = "no successful automatic technical QA"
        return status
    status["status"] = "exported_awaiting_review"
    status["encoded_file"] = str(video_path.relative_to(REPO))
    status["encoded_sha256"] = digest(video_path)
    status["technical_qa"] = qa["automaticTechnicalChecks"]
    status["stt"] = qa.get("stt", "pending")
    status["visual_review"] = qa.get("visualReview", "pending")
    status["listening_review"] = qa.get("humanListening", "pending")
    return status


def save(status: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(status, ensure_ascii=False, indent=2))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="No-paid-API video task controller")
    parser.add_argument("command", choices=("preflight", "render", "inspect"))
    parser.add_argument("--task", required=True, type=Path)
    parser.add_argument("--status", default=STATUS_PATH, type=Path)
    args = parser.parse_args(argv)
    try:
        status = verify(args.task.resolve())
        if args.command == "render":
            runner = REPO / "gossip_video_workflow" / "run.py"
            if not runner.is_file():
                raise GateError("missing original gossip_video_workflow/run.py")
            status["status"] = "rendering"
            save(status, args.status)
            # Never interpolate task text through a shell.
            subprocess.run([sys.executable, str(runner), "--episode", str(REPO / status["episode_path"]), "--stt"], cwd=REPO, check=True)
            status = inspect(status)
            if status["status"] != "exported_awaiting_review":
                raise GateError(f"render lacked complete verified files: {status['status']}")
        elif args.command == "inspect":
            status = inspect(status)
        save(status, args.status)
        return 0
    except (GateError, subprocess.CalledProcessError) as exc:
        save({"status": "failed", "reason": str(exc), "task_path": str(args.task)}, args.status)
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
