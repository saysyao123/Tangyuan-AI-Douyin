from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Any

from app.download.authenticated import download_stream
from app.capture.local_bridge import serve as serve_capture
from app.capture.cdp_browser import DEFAULT_CDP_ENDPOINT, DEFAULT_TARGET_CHAT, run_dola_cdp
from app.capture.generation_time import resolve_generation_bundle
from app.capture.playwright_browser import run_dola_browser
from app.logger import configure_logging, redact_url
from app.qa.ffprobe import probe_media
from app.qa.report import make_report
from app.production.account_registry import AccountRegistry
from app.production.capacity import capacity_observation
from app.production.consumer_gateway import (
    ConsumerGatewayClient,
    ConsumerGatewayError,
    sync_registry_from_consumer_gateway,
)
from app.production.dola_desktop import (
    DolaDesktopClient,
    DolaDesktopError,
    sync_registry_from_dola_desktop,
)
from app.production.models import JobRecord
from app.production.queue import JobQueue
from app.production.scheduler import HealthAwareRoundRobin, NoReadyAccount
from app.production.xiaochai_bridge import (
    XiaochaiBridgeClient,
    XiaochaiBridgeError,
    latest_capture_body,
    sync_registry_from_xiaochai,
    write_capture_body,
)
from app.resolver.resolver import resolve_metadata


def _load_json(path: str | Path) -> Any:
    source = Path(path)
    with source.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _emit(payload: Any, *, report_path: str | Path | None = None) -> None:
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    print(text)
    if report_path is not None:
        destination = Path(report_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text + "\n", encoding="utf-8")


def _resolve_payload(result: Any) -> dict[str, Any]:
    return make_report(result)


def _cmd_resolve(args: argparse.Namespace) -> int:
    metadata = _load_json(args.metadata)
    result = resolve_metadata(metadata, fetch_fallback=args.fetch_fallback)
    _emit(_resolve_payload(result), report_path=args.report)
    return 0 if result.status == "success" else 2


def _cmd_download(args: argparse.Namespace) -> int:
    metadata = _load_json(args.metadata)
    result = resolve_metadata(metadata, fetch_fallback=args.fetch_fallback)
    if result.status != "success" or result.selected is None:
        _emit(_resolve_payload(result), report_path=args.report)
        return 2
    try:
        media_path = download_stream(result.selected.url, args.output)
        ffprobe = probe_media(media_path)
        report = make_report(result, file_path=media_path, ffprobe=ffprobe)
        _emit(report, report_path=args.report)
        return 0
    except Exception as exc:
        _emit(
            {
                "status": "download_failed",
                "error": str(exc),
                "url": redact_url(result.selected.url),
                "security": {"bypass_attempted": False},
            },
            report_path=args.report,
        )
        return 3


def _cmd_inspect(args: argparse.Namespace) -> int:
    try:
        ffprobe = probe_media(args.input)
        report = {
            "status": "success",
            "file": str(Path(args.input).resolve()),
            "ffprobe": ffprobe,
            "security": {"reencoded": False},
        }
        _emit(report, report_path=args.report)
        return 0
    except Exception as exc:
        _emit({"status": "inspect_failed", "error": str(exc)}, report_path=args.report)
        return 3


def _cmd_dola_browser(args: argparse.Namespace) -> int:
    try:
        summary = asyncio.run(
            run_dola_browser(
                profile=args.profile,
                url=args.url,
                auto_download=args.auto_download,
                headless=args.headless,
                output_dir=args.output_dir,
                timeout_seconds=args.timeout,
                discover_network=args.discover_network,
            )
        )
        _emit(summary)
        return 0 if summary.get("capture_results") else 2
    except Exception as exc:
        _emit({"status": "dola_browser_failed", "error": str(exc), "bypass_attempted": False})
        return 3


def _cmd_dola_cdp(args: argparse.Namespace) -> int:
    try:
        summary = asyncio.run(
            run_dola_cdp(
                endpoint=args.endpoint,
                target_chat=args.target_chat,
                auto_download=args.auto_download,
                discover_network=args.discover_network,
                output_dir=args.output_dir,
                wait_seconds=args.wait_seconds,
            )
        )
        _emit(summary)
        acceptance = summary.get("acceptance") or {}
        return 0 if acceptance.get("CAPTURE_RESPONSE") == "PASS" else 2
    except Exception as exc:
        _emit({"status": "dola_cdp_failed", "error": str(exc), "bypass_attempted": False})
        return 3


def _cmd_resolve_generation(args: argparse.Namespace) -> int:
    try:
        report = resolve_generation_bundle(args.bundle_dir, fetch_fallback=args.fetch_fallback)
        _emit(report, report_path=args.report)
        return 0 if report.get("GENERATION_MEDIA_IDENTITY_CAPTURE") == "PASS" else 2
    except Exception as exc:
        _emit({"status": "resolve_generation_failed", "error": str(exc), "bypass_attempted": False}, report_path=args.report)
        return 3


def _registry(args: argparse.Namespace) -> AccountRegistry:
    return AccountRegistry.load(args.registry)


def _cmd_account_add(args: argparse.Namespace) -> int:
    registry = _registry(args)
    account = registry.add(
        args.account_id,
        display_name=args.display_name,
        session_slot=args.session_slot,
        status=args.status,
    )
    registry.save()
    _emit({"status": "account_added", "account": account.public_dict(), "credentials_saved": False})
    return 0


def _cmd_account_login(args: argparse.Namespace) -> int:
    registry = _registry(args)
    account = registry.get(args.account_id)
    _emit(
        {
            "status": "manual_login_required",
            "account": account.public_dict(),
            "instructions": [
                f"打开 Dola 并在 session slot {account.session_slot} 中由账号所有者完成登录。",
                "登录后用 account-set-status ... READY 显式确认；本命令不读取密码、Cookie 或验证码。",
            ],
            "marked_ready": False,
        }
    )
    return 2


def _cmd_accounts(args: argparse.Namespace) -> int:
    registry = _registry(args)
    payload = {"accounts": registry.dashboard(), "ready_count": len(registry.ready())}
    if args.json:
        _emit(payload)
        return 0
    print("ACCOUNT  STATUS       SLOT  JOBS  PASS  FAIL  LAST_USED")
    for item in payload["accounts"]:
        print(
            f"{item['account_id']:<8} {item['status']:<12} {item['session_slot']:<5} "
            f"-     {item['success_count']:<4} {item['failure_count']:<4} {item['last_used_at'] or '-'}"
        )
    return 0


def _cmd_account_set_status(args: argparse.Namespace) -> int:
    registry = _registry(args)
    account = registry.set_status(args.account_id, args.status, error=args.error)
    registry.save()
    _emit({"status": "account_status_updated", "account": account.public_dict()})
    return 0


def _cmd_enqueue(args: argparse.Namespace) -> int:
    prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    queue = JobQueue(args.queue)
    job = queue.enqueue(prompt, target_duration=args.duration, job_id=args.job_id)
    _emit(
        {
            "status": "queued",
            "job": job.public_dict(),
            "prompt_file": str(Path(args.queue).parent / "prompts" / f"{job.job_id}.md"),
        }
    )
    return 0


def _cmd_worker(args: argparse.Namespace) -> int:
    registry = _registry(args)
    queue = JobQueue(args.queue)
    pending = queue.pending()
    if not args.dry_run:
        _emit(
            {
                "status": "browser_adapter_required",
                "pending_jobs": len(pending),
                "reason": "Real Dola generation requires an in-app browser session and a user-confirmed submit action; no background credential or quota bypass is performed.",
            }
        )
        return 4
    scheduler = HealthAwareRoundRobin(registry)
    assignments: list[dict[str, str]] = []
    for job in pending[: args.max_jobs]:
        try:
            account = scheduler.bind_job(job)
        except NoReadyAccount as exc:
            _emit({"status": "no_ready_account", "assigned": assignments, "error": str(exc)})
            return 2
        assignments.append(
            {"job_id": job.job_id, "account_id": account.account_id, "session_slot": account.session_slot}
        )
        scheduler.release(account.account_id)
    _emit(
        {
            "status": "dry_run_pass",
            "pending_jobs": len(pending),
            "assigned": assignments,
            "mutated_external_state": False,
        }
    )
    return 0


def _cmd_capacity_report(args: argparse.Namespace) -> int:
    payload = _load_json(args.status_json)
    accounts = payload.get("accounts") if isinstance(payload, dict) else None
    if not isinstance(accounts, list):
        raise ValueError("status JSON must contain an accounts list")
    _emit({"target_duration": args.duration, "accounts": [capacity_observation(item, target_duration=args.duration) for item in accounts]})
    return 0


def _xiaochai_client(args: argparse.Namespace) -> XiaochaiBridgeClient:
    return XiaochaiBridgeClient(args.endpoint, token=args.token, timeout=args.timeout)


def _xiaochai_account(args: argparse.Namespace) -> tuple[AccountRegistry, Any]:
    registry = _registry(args)
    account = registry.get(args.account_id)
    if account.session_host != "xiaochai" or not account.host_account_id:
        raise XiaochaiBridgeError(
            f"account {account.account_id} is not mapped to the Xiaochai session host; run xiaochai-bridge accounts --sync first"
        )
    return registry, account


def _cmd_xiaochai_bridge(args: argparse.Namespace) -> int:
    try:
        client = _xiaochai_client(args)
        if args.bridge_command == "health":
            _emit(client.health())
            return 0
        if args.bridge_command == "accounts":
            host_accounts = client.accounts()
            if not args.sync:
                _emit({"status": "ok", "accounts": host_accounts, "registry_mutated": False})
                return 0
            registry = _registry(args)
            mapping = sync_registry_from_xiaochai(registry, host_accounts)
            registry.save()
            _emit({"status": "account_sync_pass", "mapping": mapping, "registry": str(registry.path.resolve())})
            return 0
        if args.bridge_command in {"session", "activate", "capture", "resolve-latest", "download"}:
            _, account = _xiaochai_account(args)
            host_id = account.host_account_id
            assert host_id is not None
            if args.bridge_command == "session":
                payload = client.session(host_id)
                _emit({"status": "session_checked", "account": account.public_dict(), "bridge": payload})
                return 0 if payload.get("authenticated") is True else 2
            if args.bridge_command == "activate":
                _emit(client.activate(host_id))
                return 0
            if args.bridge_command == "download":
                payload = client.download(host_id, args.url, Path(args.output).name)
                _emit({"status": "download_pass", "account_id": account.account_id, "bridge": payload})
                return 0

            body, entry = latest_capture_body(client, account)
            if args.bridge_command == "capture":
                destination = write_capture_body(body, args.output)
                _emit(
                    {
                        "status": "capture_pass",
                        "account_id": account.account_id,
                        "source_key": entry.get("source_key"),
                        "output": str(destination.resolve()),
                        "body_emitted": False,
                    }
                )
                return 0

            metadata = json.loads(body)
            result = resolve_metadata(metadata, fetch_fallback=args.fetch_fallback)
            if result.status != "success" or result.selected is None:
                _emit(_resolve_payload(result), report_path=args.report)
                return 2
            if not args.auto_download:
                _emit(_resolve_payload(result), report_path=args.report)
                return 0
            source_key = str(entry.get("source_key") or "latest")
            safe_key = "".join(char if char.isalnum() or char in "._-" else "_" for char in source_key)[-80:] or "latest"
            filename = f"{account.account_id}_{safe_key}.mp4"
            bridge_result = client.download(host_id, result.selected.url, filename)
            media_path = bridge_result.get("path")
            if not isinstance(media_path, str) or not media_path:
                raise XiaochaiBridgeError("bridge download returned no path")
            ffprobe = probe_media(media_path)
            report = make_report(result, file_path=media_path, ffprobe=ffprobe)
            report["bridge"] = {
                "account_id": account.account_id,
                "host_account_id": host_id,
                "source_key": entry.get("source_key"),
                "download": {key: value for key, value in bridge_result.items() if key != "path"},
            }
            _emit(report, report_path=args.report)
            return 0
        raise XiaochaiBridgeError(f"unsupported bridge command: {args.bridge_command}")
    except (XiaochaiBridgeError, KeyError, ValueError, json.JSONDecodeError, OSError) as exc:
        _emit({"status": "xiaochai_bridge_failed", "error": str(exc), "cookies_emitted": False})
        return 3


def _consumer_gateway_account(args: argparse.Namespace) -> tuple[AccountRegistry, Any]:
    registry = _registry(args)
    account = registry.get(args.account_id)
    if account.session_host != "consumer_gateway" or not account.host_account_id:
        raise ConsumerGatewayError(
            f"account {account.account_id} is not mapped to the consumer gateway; run consumer-gateway accounts --sync first"
        )
    return registry, account


def _cmd_consumer_gateway(args: argparse.Namespace) -> int:
    try:
        client = ConsumerGatewayClient(args.endpoint, timeout=args.timeout)
        if args.gateway_command == "health":
            _emit(client.health())
            return 0
        if args.gateway_command == "accounts":
            host_accounts = client.accounts()
            if not args.sync:
                _emit({"status": "ok", "accounts": host_accounts, "registry_mutated": False})
                return 0
            registry = _registry(args)
            mapping = sync_registry_from_consumer_gateway(registry, host_accounts)
            registry.save()
            _emit({"status": "account_sync_pass", "mapping": mapping, "registry": str(registry.path.resolve())})
            return 0
        registry, account = _consumer_gateway_account(args)
        host_id = account.host_account_id
        assert host_id is not None
        if args.gateway_command == "status":
            payload = client.status(host_id)
            if payload.get("logged_in") is True:
                registry.set_status(account.account_id, "READY")
                registry.save()
            elif payload.get("logged_in") is False:
                registry.set_status(account.account_id, "NEEDS_LOGIN")
                registry.save()
            _emit({"status": "session_checked", "account": account.public_dict(), "gateway": payload})
            return 0 if payload.get("logged_in") is True or payload.get("ready") is True else 2
        if args.gateway_command == "start":
            payload = client.start(host_id)
            if payload.get("status") == "ready":
                registry.set_status(account.account_id, "READY")
                registry.save()
            _emit({"status": "gateway_account_started", "account_id": account.account_id, "gateway": payload})
            return 0 if payload.get("status") == "ready" else 2
        if args.gateway_command == "stop":
            payload = client.stop(host_id)
            registry.set_status(account.account_id, "NEEDS_LOGIN")
            registry.save()
            _emit({"status": "gateway_account_stopped", "account_id": account.account_id, "gateway": payload})
            return 0
        if args.gateway_command == "probe":
            payload = client.probe(host_id)
            _emit({"status": "gateway_probe", "account_id": account.account_id, "gateway": payload})
            return 0 if payload.get("status") == "healthy" else 2
        raise ConsumerGatewayError(f"unsupported gateway command: {args.gateway_command}")
    except (ConsumerGatewayError, KeyError, ValueError, OSError) as exc:
        _emit({"status": "consumer_gateway_failed", "error": str(exc), "credentials_emitted": False})
        return 3


def _dola_desktop_client(args: argparse.Namespace) -> DolaDesktopClient:
    return DolaDesktopClient(
        endpoint=args.endpoint,
        control_path=args.control_path,
        timeout=args.timeout,
    )


def _dola_desktop_account(args: argparse.Namespace) -> tuple[AccountRegistry, Any]:
    registry = _registry(args)
    account = registry.get(args.account_id)
    if account.session_host != "dola_desktop_studio" or not account.host_account_id:
        raise DolaDesktopError(
            f"account {account.account_id} is not mapped to Dola Desktop; run dola-desktop accounts --sync first"
        )
    return registry, account


def _cmd_dola_desktop(args: argparse.Namespace) -> int:
    try:
        if args.desktop_command == "confirm-login":
            registry, account = _dola_desktop_account(args)
            account.status = "READY"
            account.readiness_basis = "user_confirmed"
            account.last_error = ""
            registry.save()
            _emit(
                {
                    "status": "dola_desktop_login_confirmed",
                    "account": account.public_dict(),
                    "confirmation": "user_asserted",
                    "computer_use": False,
                }
            )
            return 0
        client = _dola_desktop_client(args)
        if args.desktop_command == "health":
            payload = client.health()
            _emit({"status": "dola_desktop_health", "control": payload})
            return 0 if payload.get("ok") is True else 2
        if args.desktop_command == "accounts":
            host_accounts = client.accounts()
            if args.check_session:
                for host_account in host_accounts:
                    host_id = host_account.get("host_account_id")
                    if host_id:
                        host_account.update(client.session(host_id))
            if not args.sync:
                _emit({"status": "ok", "accounts": host_accounts, "registry_mutated": False, "authentication_checked": args.check_session})
                return 0
            registry = _registry(args)
            mapping = sync_registry_from_dola_desktop(registry, host_accounts)
            registry.save()
            _emit(
                {
                    "status": "dola_desktop_account_sync_pass",
                    "mapping": mapping,
                    "registry": str(registry.path.resolve()),
                    "authentication_checked": args.check_session,
                }
            )
            return 0
        registry, account = _dola_desktop_account(args)
        if args.desktop_command == "activate":
            assert account.host_account_id is not None
            payload = client.activate(account.host_account_id)
            _emit(
                {
                    "status": "dola_desktop_account_activated",
                    "account": account.public_dict(),
                    "host": payload,
                    "computer_use": False,
                }
            )
            return 0
        raise DolaDesktopError(f"unsupported Dola Desktop command: {args.desktop_command}")
    except (DolaDesktopError, KeyError, ValueError, OSError) as exc:
        _emit({"status": "dola_desktop_failed", "error": str(exc), "credentials_emitted": False})
        return 3


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Resolve and validate authorized Dola video sources")
    subparsers = parser.add_subparsers(dest="command", required=True)

    resolve = subparsers.add_parser("resolve", help="parse metadata and rank candidate URLs")
    resolve.add_argument("--metadata", required=True, help="path to captured JSON metadata")
    resolve.add_argument("--fetch-fallback", action="store_true", help="request discovered fallback_api URLs")
    resolve.add_argument("--report", help="optional JSON report path")
    resolve.set_defaults(handler=_cmd_resolve)

    download = subparsers.add_parser("download", help="download the selected clean candidate")
    download.add_argument("--metadata", required=True, help="path to captured JSON metadata")
    download.add_argument("--output", required=True, help="final MP4 path")
    download.add_argument("--fetch-fallback", action="store_true", help="request discovered fallback_api URLs")
    download.add_argument("--report", help="optional JSON report path")
    download.set_defaults(handler=_cmd_download)

    inspect = subparsers.add_parser("inspect", help="run ffprobe on a local media file")
    inspect.add_argument("input", help="local MP4 path")
    inspect.add_argument("--report", help="optional JSON report path")
    inspect.set_defaults(handler=_cmd_inspect)

    capture = subparsers.add_parser("capture-server", help="receive local Dola chain/single captures")
    capture.add_argument("--host", default="127.0.0.1")
    capture.add_argument("--port", type=int, default=8765)
    capture.add_argument("--out", default="captures")
    capture.add_argument("--auto-download", action="store_true", help="download and ffprobe a selected clean candidate")
    capture.add_argument("--no-fetch-fallback", action="store_true", help="do not request discovered fallback_api URLs")
    capture.set_defaults(handler=serve_capture)

    browser = subparsers.add_parser("dola-browser", help="launch a persistent Playwright Dola capture browser")
    browser.add_argument("--profile", default="runtime/dola-browser-profile")
    browser.add_argument("--url", default="https://www.dola.com/")
    browser.add_argument("--auto-download", action="store_true")
    browser.add_argument("--headless", action="store_true", help="only use after a headed login has created the profile")
    browser.add_argument("--output-dir", default="captures")
    browser.add_argument("--timeout", type=float, default=300)
    browser.add_argument("--discover-network", action="store_true")
    browser.set_defaults(handler=_cmd_dola_browser)

    cdp = subparsers.add_parser("dola-cdp", help="connect to an externally launched Chrome/Edge over CDP")
    cdp.add_argument("--endpoint", default=DEFAULT_CDP_ENDPOINT)
    cdp.add_argument("--auto-download", action="store_true")
    cdp.add_argument("--discover-network", action="store_true")
    cdp.add_argument("--output-dir", default="captures")
    cdp.add_argument("--target-chat", default=DEFAULT_TARGET_CHAT)
    cdp.add_argument("--wait-seconds", type=float, default=120)
    cdp.set_defaults(handler=_cmd_dola_cdp)

    generation = subparsers.add_parser("resolve-generation", help="aggregate a generation-time capture bundle")
    generation.add_argument("bundle_dir", help="captures/generation/YYYYMMDD_HHMMSS directory")
    generation.add_argument("--fetch-fallback", action="store_true", help="request captured fallback_api URLs")
    generation.add_argument("--report", help="optional JSON report path")
    generation.set_defaults(handler=_cmd_resolve_generation)

    account_add = subparsers.add_parser("account-add", help="add a non-sensitive account/session slot record")
    account_add.add_argument("account_id")
    account_add.add_argument("--display-name")
    account_add.add_argument("--session-slot")
    account_add.add_argument("--status", choices=["DISABLED", "NEEDS_LOGIN", "READY", "COOLDOWN", "ERROR"], default="NEEDS_LOGIN")
    account_add.add_argument("--registry", default="runtime/accounts/accounts.json")
    account_add.set_defaults(handler=_cmd_account_add)

    account_login = subparsers.add_parser("account-login", help="print the manual login gate for an account")
    account_login.add_argument("account_id")
    account_login.add_argument("--registry", default="runtime/accounts/accounts.json")
    account_login.set_defaults(handler=_cmd_account_login)

    accounts = subparsers.add_parser("accounts", help="show the account dashboard")
    accounts.add_argument("--json", action="store_true")
    accounts.add_argument("--registry", default="runtime/accounts/accounts.json")
    accounts.set_defaults(handler=_cmd_accounts)

    account_status = subparsers.add_parser("account-set-status", help="explicitly update a manually verified account status")
    account_status.add_argument("account_id")
    account_status.add_argument("status", choices=["DISABLED", "NEEDS_LOGIN", "READY", "COOLDOWN", "ERROR"])
    account_status.add_argument("--error", default="")
    account_status.add_argument("--registry", default="runtime/accounts/accounts.json")
    account_status.set_defaults(handler=_cmd_account_set_status)

    enqueue = subparsers.add_parser("enqueue", help="enqueue a prompt without submitting it")
    enqueue.add_argument("--prompt-file", required=True)
    enqueue.add_argument("--duration", type=float, default=5.0)
    enqueue.add_argument("--job-id")
    enqueue.add_argument("--queue", default="runtime/queue/jobs.jsonl")
    enqueue.set_defaults(handler=_cmd_enqueue)

    worker = subparsers.add_parser("worker", help="run or dry-run the single-worker scheduler")
    worker.add_argument("--dry-run", action="store_true", help="assign pending jobs locally without browser submission")
    worker.add_argument("--max-jobs", type=int, default=100)
    worker.add_argument("--queue", default="runtime/queue/jobs.jsonl")
    worker.add_argument("--registry", default="runtime/accounts/accounts.json")
    worker.set_defaults(handler=_cmd_worker)

    capacity = subparsers.add_parser("capacity-report", help="report observed quota without claiming provider capacity")
    capacity.add_argument("--status-json", required=True)
    capacity.add_argument("--duration", type=float, default=5.0)
    capacity.set_defaults(handler=_cmd_capacity_report)

    xiaochai = subparsers.add_parser("xiaochai-bridge", help="use the isolated Xiaochai app as a local Dola session host")
    xiaochai_sub = xiaochai.add_subparsers(dest="bridge_command", required=True)

    bridge_common = argparse.ArgumentParser(add_help=False)
    bridge_common.add_argument("--endpoint", default="http://127.0.0.1:8766")
    bridge_common.add_argument("--token")
    bridge_common.add_argument("--timeout", type=float, default=20.0)

    health = xiaochai_sub.add_parser("health", parents=[bridge_common], help="check the local Xiaochai bridge")
    health.set_defaults(handler=_cmd_xiaochai_bridge)

    host_accounts = xiaochai_sub.add_parser("accounts", parents=[bridge_common], help="list or sync public host-account mappings")
    host_accounts.add_argument("--sync", action="store_true")
    host_accounts.add_argument("--registry", default="runtime/accounts/accounts.json")
    host_accounts.set_defaults(handler=_cmd_xiaochai_bridge)

    for bridge_command in ("session", "activate"):
        command = xiaochai_sub.add_parser(bridge_command, parents=[bridge_common])
        command.add_argument("account_id")
        command.add_argument("--registry", default="runtime/accounts/accounts.json")
        command.set_defaults(handler=_cmd_xiaochai_bridge)

    capture_latest = xiaochai_sub.add_parser("capture", parents=[bridge_common], help="save the latest captured Dola response")
    capture_latest.add_argument("account_id")
    capture_latest.add_argument("--output", required=True)
    capture_latest.add_argument("--registry", default="runtime/accounts/accounts.json")
    capture_latest.set_defaults(handler=_cmd_xiaochai_bridge)

    resolve_latest = xiaochai_sub.add_parser("resolve-latest", parents=[bridge_common], help="resolve and optionally download the latest capture")
    resolve_latest.add_argument("account_id")
    resolve_latest.add_argument("--auto-download", action="store_true")
    resolve_latest.add_argument("--fetch-fallback", action="store_true")
    resolve_latest.add_argument("--output-dir", default="captures/legacy-host")
    resolve_latest.add_argument("--report")
    resolve_latest.add_argument("--registry", default="runtime/accounts/accounts.json")
    resolve_latest.set_defaults(handler=_cmd_xiaochai_bridge)

    host_download = xiaochai_sub.add_parser("download", parents=[bridge_common], help="download one selected media URL through the host partition")
    host_download.add_argument("account_id")
    host_download.add_argument("--url", required=True)
    host_download.add_argument("--output", required=True, help="output filename inside the host bridge output directory")
    host_download.add_argument("--registry", default="runtime/accounts/accounts.json")
    host_download.set_defaults(handler=_cmd_xiaochai_bridge)

    gateway = subparsers.add_parser("consumer-gateway", help="connect account management to the existing local Doubao consumer gateway")
    gateway_sub = gateway.add_subparsers(dest="gateway_command", required=True)
    gateway_common = argparse.ArgumentParser(add_help=False)
    gateway_common.add_argument("--endpoint", default="http://127.0.0.1:19090")
    gateway_common.add_argument("--timeout", type=float, default=20.0)

    gateway_health = gateway_sub.add_parser("health", parents=[gateway_common], help="check the existing local gateway")
    gateway_health.set_defaults(handler=_cmd_consumer_gateway)

    gateway_accounts = gateway_sub.add_parser("accounts", parents=[gateway_common], help="list or sync gateway account IDs")
    gateway_accounts.add_argument("--sync", action="store_true")
    gateway_accounts.add_argument("--registry", default="runtime/accounts/accounts.json")
    gateway_accounts.set_defaults(handler=_cmd_consumer_gateway)

    for gateway_command in ("status", "start", "stop", "probe"):
        command = gateway_sub.add_parser(gateway_command, parents=[gateway_common])
        command.add_argument("account_id")
        command.add_argument("--registry", default="runtime/accounts/accounts.json")
        command.set_defaults(handler=_cmd_consumer_gateway)

    dola_desktop = subparsers.add_parser(
        "dola-desktop",
        help="connect the backend to the user's local Dola Desktop multi-account host",
    )
    dola_desktop_sub = dola_desktop.add_subparsers(dest="desktop_command", required=True)
    desktop_common = argparse.ArgumentParser(add_help=False)
    desktop_common.add_argument("--endpoint", default=None, help="optional loopback control endpoint")
    desktop_common.add_argument("--control-path", default=None, help="optional local control discovery file")
    desktop_common.add_argument("--timeout", type=float, default=10.0)

    desktop_health = dola_desktop_sub.add_parser("health", parents=[desktop_common], help="check Dola Desktop")
    desktop_health.set_defaults(handler=_cmd_dola_desktop)

    desktop_accounts = dola_desktop_sub.add_parser("accounts", parents=[desktop_common], help="list or sync Dola accounts")
    desktop_accounts.add_argument("--sync", action="store_true")
    desktop_accounts.add_argument("--check-session", action="store_true", help="ask the host for a boolean login-status check")
    desktop_accounts.add_argument("--registry", default="runtime/accounts/dola_accounts.json")
    desktop_accounts.set_defaults(handler=_cmd_dola_desktop)

    desktop_activate = dola_desktop_sub.add_parser("activate", parents=[desktop_common], help="activate one mapped Dola account")
    desktop_activate.add_argument("account_id")
    desktop_activate.add_argument("--registry", default="runtime/accounts/dola_accounts.json")
    desktop_activate.set_defaults(handler=_cmd_dola_desktop)

    desktop_confirm = dola_desktop_sub.add_parser("confirm-login", parents=[desktop_common], help="record the user's explicit login confirmation")
    desktop_confirm.add_argument("account_id")
    desktop_confirm.add_argument("--registry", default="runtime/accounts/dola_accounts.json")
    desktop_confirm.set_defaults(handler=_cmd_dola_desktop)
    return parser


def main(argv: list[str] | None = None) -> int:
    configure_logging()
    parser = build_parser()
    args = parser.parse_args(argv)
    result = args.handler(args)
    return 0 if result is None else int(result)


if __name__ == "__main__":
    sys.exit(main())
