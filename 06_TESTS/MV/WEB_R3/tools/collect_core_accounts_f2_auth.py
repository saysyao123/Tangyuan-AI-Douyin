#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import csv
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from f2.apps.douyin.handler import DouyinHandler

TZ = ZoneInfo("Asia/Manila")
CASE_ORDER = ["P01", "P02", "P03", "P04", "P05", "P06", "P07", "P09", "P10"]
ACCOUNT_FIELDS = [
    "account_id","case_id","sec_uid","douyin_id","current_nickname","profile_short_url",
    "role","role_category","trend_weight","visual_weight","packaging_weight","registry_source",
    "r3_test_core","active","last_verified_at","window_15d_complete","notes",
]
WORK_FIELDS = [
    "aweme_id","account_id","create_time","work_url","caption","type","duration_s",
    "music_title_raw","music_author_raw","hashtags","first_observed_at",
]
METRIC_FIELDS = [
    "aweme_id","observed_at","digg_count","comment_count","share_count","collect_count","play_count",
]
RUN_FIELDS = [
    "run_id","account_id","window_start","window_end_exclusive","pages_fetched","items_fetched",
    "items_in_window","oldest_fetched","newest_fetched","terminal_has_more","window_complete",
    "stop_reason","error","collector","observed_at","profile_auth_pass","first_page_auth_pass",
    "latest_ownership_pass","window_closure_pass","profile_aweme_count","latest_verified_aweme_id",
]


def r3_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def data_dir() -> Path:
    return r3_dir() / "database"


def cookie_path() -> Path:
    return r3_dir() / ".secrets" / "douyin_cookie.txt"


def raw_root() -> Path:
    return r3_dir() / ".local_raw"


def read_cookie() -> str:
    value = os.environ.get("DOUYIN_COOKIE", "").strip()
    if value:
        return value
    path = cookie_path()
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow({field: row.get(field, "") for field in fields})


def parse_dt(value: Any) -> datetime | None:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        try:
            return datetime.fromtimestamp(float(value), TZ)
        except Exception:
            return None
    text = str(value).strip()
    if text.isdigit():
        try:
            return datetime.fromtimestamp(int(text), TZ)
        except Exception:
            pass
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(text, fmt)
            return dt.replace(tzinfo=TZ) if dt.tzinfo is None else dt.astimezone(TZ)
        except ValueError:
            pass
    return None


def iso_db(dt: datetime | None) -> str:
    return dt.astimezone(TZ).strftime("%Y-%m-%d %H:%M:%S") if dt else ""


def normalize_duration_ms(value: Any) -> str:
    try:
        v = float(value or 0)
        if v <= 0:
            return ""
        return f"{v / 1000.0:.3f}" if v > 1000 else f"{v:.3f}"
    except Exception:
        return ""


def get_hashtags(item: dict[str, Any]) -> list[str]:
    tags: list[str] = []
    for extra in item.get("text_extra") or []:
        if not isinstance(extra, dict):
            continue
        name = str(extra.get("hashtag_name") or "").strip()
        if name and name not in tags:
            tags.append(name)
    return tags


def work_type(item: dict[str, Any]) -> str:
    if isinstance(item.get("images"), list) and item.get("images"):
        return "image"
    return "video"


def stable_work(item: dict[str, Any], account_id: str, observed_at: str, existing_first: str = "") -> dict[str, Any]:
    aweme_id = str(item.get("aweme_id") or "")
    music = item.get("music") or {}
    author_name = music.get("author") or music.get("author_name") or ""
    return {
        "aweme_id": aweme_id,
        "account_id": account_id,
        "create_time": iso_db(parse_dt(item.get("create_time"))),
        "work_url": f"https://www.douyin.com/video/{aweme_id}",
        "caption": str(item.get("desc") or "").replace("\n", " ").strip(),
        "type": work_type(item),
        "duration_s": normalize_duration_ms((item.get("video") or {}).get("duration")),
        "music_title_raw": str(music.get("title") or "").strip(),
        "music_author_raw": str(author_name).strip(),
        "hashtags": "|".join(get_hashtags(item)),
        "first_observed_at": existing_first or observed_at,
    }


def metric_row(item: dict[str, Any], observed_at: str) -> dict[str, Any]:
    stats = item.get("statistics") or {}
    return {
        "aweme_id": str(item.get("aweme_id") or ""),
        "observed_at": observed_at,
        "digg_count": stats.get("digg_count", 0),
        "comment_count": stats.get("comment_count", 0),
        "share_count": stats.get("share_count", 0),
        "collect_count": stats.get("collect_count", 0),
        "play_count": stats.get("play_count", 0),
    }


def find_owned_aweme(obj: Any, aweme_id: str) -> dict[str, Any] | None:
    if isinstance(obj, dict):
        if str(obj.get("aweme_id") or "") == aweme_id and isinstance(obj.get("author"), dict):
            return obj
        for value in obj.values():
            found = find_owned_aweme(value, aweme_id)
            if found:
                return found
    elif isinstance(obj, list):
        for value in obj:
            found = find_owned_aweme(value, aweme_id)
            if found:
                return found
    return None


def valid_first_page(raw: Any, profile_aweme_count: int | None) -> bool:
    if not isinstance(raw, dict):
        return False
    if raw.get("status_code") not in (0, None):
        return False
    if "aweme_list" not in raw:
        return False
    items = raw.get("aweme_list")
    if not isinstance(items, list):
        return False
    if items:
        return True
    return profile_aweme_count == 0


def make_kwargs(cookie: str) -> dict[str, Any]:
    return {
        "headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
            ),
            "Referer": "https://www.douyin.com/",
        },
        "proxies": {"http://": None, "https://": None},
        "timeout": 2,
        "cookie": cookie,
    }


async def collect_one(
    case_id: str,
    profile_spec: dict[str, Any],
    account_row: dict[str, str],
    cookie: str,
    window_start: datetime,
    window_end: datetime,
    observed_at: str,
    raw_run_dir: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    sec_uid = profile_spec["sec_uid"]
    account_id = account_row["account_id"]
    handler = DouyinHandler(make_kwargs(cookie))

    profile_auth = False
    first_page_auth = False
    latest_owner_pass = False
    closure_pass = False
    profile_aweme_count: int | None = None
    nickname = account_row.get("current_nickname", "")
    douyin_id = account_row.get("douyin_id", "")
    error = ""
    stop_reason = ""
    pages = 0
    terminal_has_more: bool | None = None
    response_cursor: int | None = None
    fetched_by_id: dict[str, dict[str, Any]] = {}
    latest_verified_id = ""

    case_raw = raw_run_dir / case_id
    case_raw.mkdir(parents=True, exist_ok=True)

    try:
        profile = await handler.fetch_user_profile(sec_uid)
        returned_sec_uid = str(getattr(profile, "sec_user_id", "") or "")
        profile_auth = returned_sec_uid == sec_uid
        nickname = str(getattr(profile, "nickname_raw", "") or nickname)
        douyin_id = str(getattr(profile, "unique_id", "") or douyin_id)
        try:
            profile_aweme_count = int(getattr(profile, "aweme_count", 0) or 0)
        except Exception:
            profile_aweme_count = None
        (case_raw / "profile.json").write_text(
            json.dumps(profile._to_raw(), ensure_ascii=False, indent=2, default=str), encoding="utf-8"
        )
        if not profile_auth:
            raise RuntimeError("PROFILE_AUTH_MISMATCH")

        start_ts = int(window_start.timestamp())
        end_ts = int(window_end.timestamp())
        page_index = 0
        async for page_data in handler.fetch_user_post_videos(
            sec_uid,
            min_cursor=start_ts,
            max_cursor=end_ts,
            page_counts=18,
            max_counts=300,
        ):
            page_index += 1
            pages = page_index
            raw = page_data._to_raw()
            (case_raw / f"post_page_{page_index:02d}.json").write_text(
                json.dumps(raw, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
            )
            if page_index == 1:
                first_page_auth = valid_first_page(raw, profile_aweme_count)
                if not first_page_auth:
                    raise RuntimeError("FIRST_PAGE_AUTH_INVALID_OR_DEGRADED")

            items = raw.get("aweme_list") or [] if isinstance(raw, dict) else []
            if isinstance(items, list):
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    aid = str(item.get("aweme_id") or "")
                    if aid:
                        fetched_by_id[aid] = item

            terminal_has_more = bool(getattr(page_data, "has_more", False))
            raw_cursor = getattr(page_data, "max_cursor", None)
            try:
                response_cursor = int(raw_cursor) if raw_cursor not in (None, "") else None
            except Exception:
                response_cursor = None

        if not first_page_auth:
            raise RuntimeError("NO_VALID_FIRST_PAGE")

        # A valid authenticated no-work response is complete only when profile itself reports zero works.
        if not fetched_by_id:
            if profile_aweme_count == 0 and terminal_has_more is False:
                closure_pass = True
                latest_owner_pass = True
                stop_reason = "AUTHENTICATED_ACCOUNT_HAS_ZERO_WORKS"
            else:
                raise RuntimeError("AUTHENTICATED_POST_LIST_EMPTY_BUT_PROFILE_HAS_WORKS_OR_UNKNOWN")
        else:
            fetched_items = list(fetched_by_id.values())
            dated = [(parse_dt(x.get("create_time")), x) for x in fetched_items]
            dated = [(dt, x) for dt, x in dated if dt]
            if not dated:
                raise RuntimeError("FETCHED_WORKS_HAVE_NO_VALID_TIMESTAMPS")

            latest_dt, latest_item = max(dated, key=lambda pair: pair[0])
            latest_verified_id = str(latest_item.get("aweme_id") or "")
            detail = await handler.fetch_one_video(latest_verified_id)
            detail_raw = detail._to_raw()
            (case_raw / f"latest_detail_{latest_verified_id}.json").write_text(
                json.dumps(detail_raw, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
            )
            owned = find_owned_aweme(detail_raw, latest_verified_id)
            latest_owner_pass = bool(
                owned and str((owned.get("author") or {}).get("sec_uid") or "") == sec_uid
            )
            if not latest_owner_pass:
                raise RuntimeError("LATEST_WORK_AUTHOR_SEC_UID_MISMATCH")

            oldest_dt = min(dt for dt, _ in dated)
            cursor_crossed = response_cursor is not None and response_cursor < int(window_start.timestamp())
            no_more = terminal_has_more is False
            closure_pass = bool(cursor_crossed or no_more or oldest_dt < window_start)
            if cursor_crossed:
                stop_reason = "AUTH_CURSOR_CROSSED_WINDOW_START"
            elif no_more:
                stop_reason = "AUTH_HAS_MORE_FALSE"
            elif oldest_dt < window_start:
                # Extra guard. With authenticated native pagination this is acceptable only after all yielded pages.
                stop_reason = "AUTH_FETCHED_OLDER_THAN_WINDOW_START"
            else:
                stop_reason = "AUTH_WINDOW_NOT_CLOSED"

    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"[:1000]
        if not stop_reason:
            stop_reason = "AUTH_COLLECTOR_ERROR"

    fetched_items = list(fetched_by_id.values())
    dated_all = [(parse_dt(x.get("create_time")), x) for x in fetched_items]
    dated_all = [(dt, x) for dt, x in dated_all if dt]
    in_window_items = [x for dt, x in dated_all if window_start <= dt < window_end]
    oldest = min((dt for dt, _ in dated_all), default=None)
    newest = max((dt for dt, _ in dated_all), default=None)
    window_complete = bool(profile_auth and first_page_auth and latest_owner_pass and closure_pass and not error)

    account_update = dict(account_row)
    account_update.update({
        "current_nickname": nickname,
        "douyin_id": douyin_id,
        "last_verified_at": observed_at,
        "window_15d_complete": 1 if window_complete else 0,
        "notes": "authenticated F2 live verification; sec_uid is stable external key",
    })

    run = {
        "run_id": f"R3AUTH_{datetime.now(TZ).strftime('%Y%m%d_%H%M%S')}_{case_id}",
        "account_id": account_id,
        "window_start": iso_db(window_start),
        "window_end_exclusive": iso_db(window_end),
        "pages_fetched": pages,
        "items_fetched": len(fetched_items),
        "items_in_window": len(in_window_items),
        "oldest_fetched": iso_db(oldest),
        "newest_fetched": iso_db(newest),
        "terminal_has_more": "" if terminal_has_more is None else (1 if terminal_has_more else 0),
        "window_complete": 1 if window_complete else 0,
        "stop_reason": stop_reason,
        "error": error,
        "collector": "F2_AUTHENTICATED_LOCAL",
        "observed_at": observed_at,
        "profile_auth_pass": 1 if profile_auth else 0,
        "first_page_auth_pass": 1 if first_page_auth else 0,
        "latest_ownership_pass": 1 if latest_owner_pass else 0,
        "window_closure_pass": 1 if closure_pass else 0,
        "profile_aweme_count": "" if profile_aweme_count is None else profile_aweme_count,
        "latest_verified_aweme_id": latest_verified_id,
    }
    metrics = [metric_row(item, observed_at) for item in in_window_items]
    return account_update, in_window_items, metrics, run


async def main_async(args: argparse.Namespace) -> int:
    cookie = read_cookie()
    if len(cookie) < 20:
        print("[BLOCKED] No local Douyin authenticated session found.")
        print(f"Run: python {r3_dir() / 'tools' / 'setup_douyin_cookie.py'}")
        return 3

    window_start = datetime.strptime(args.start, "%Y-%m-%d").replace(tzinfo=TZ)
    window_end = datetime.strptime(args.end, "%Y-%m-%d").replace(tzinfo=TZ)
    if window_end <= window_start:
        raise SystemExit("--end must be later than --start")

    observed_at = datetime.now(TZ).isoformat(timespec="seconds")
    run_stamp = datetime.now(TZ).strftime("%Y%m%d_%H%M%S")
    run_raw = raw_root() / run_stamp
    run_raw.mkdir(parents=True, exist_ok=True)

    profiles_list = json.loads((r3_dir() / "core_profile_resolution_v1.json").read_text(encoding="utf-8"))
    profiles = {x["case_id"]: x for x in profiles_list if not x.get("duplicate_of")}
    accounts_existing = read_csv(data_dir() / "accounts.csv")
    accounts_by_case = {x["case_id"]: x for x in accounts_existing}
    works_existing = read_csv(data_dir() / "works.csv")
    works_by_id = {x["aweme_id"]: x for x in works_existing}
    metrics_existing = read_csv(data_dir() / "work_metrics.csv")
    runs_existing = read_csv(data_dir() / "ingestion_runs.csv")

    updated_accounts: list[dict[str, Any]] = []
    new_metrics: list[dict[str, Any]] = []
    new_runs: list[dict[str, Any]] = []
    result_summary = []

    for idx, case_id in enumerate(CASE_ORDER, 1):
        if case_id not in profiles:
            raise RuntimeError(f"missing profile spec for {case_id}")
        account_row = accounts_by_case.get(case_id)
        if not account_row:
            raise RuntimeError(f"database/accounts.csv missing {case_id}; bootstrap database first")

        print(f"[{idx}/{len(CASE_ORDER)}] authenticated collect {case_id} / {account_row.get('current_nickname') or account_row.get('douyin_id')}")
        account_update, items, metrics, run = await collect_one(
            case_id, profiles[case_id], account_row, cookie,
            window_start, window_end, observed_at, run_raw,
        )
        updated_accounts.append(account_update)
        new_runs.append(run)
        new_metrics.extend(metrics)

        for item in items:
            aid = str(item.get("aweme_id") or "")
            if not aid:
                continue
            existing = works_by_id.get(aid, {})
            works_by_id[aid] = stable_work(
                item,
                account_row["account_id"],
                observed_at,
                existing_first=existing.get("first_observed_at", ""),
            )

        result_summary.append({
            "case_id": case_id,
            "account_id": account_row["account_id"],
            "nickname": account_update.get("current_nickname", ""),
            "items_in_window": run["items_in_window"],
            "profile_auth_pass": run["profile_auth_pass"],
            "first_page_auth_pass": run["first_page_auth_pass"],
            "latest_ownership_pass": run["latest_ownership_pass"],
            "window_closure_pass": run["window_closure_pass"],
            "window_complete": run["window_complete"],
            "stop_reason": run["stop_reason"],
            "error": run["error"],
        })

    # Preserve only works inside the R3 requested window for the current core DB snapshot.
    snapshot_works = []
    for row in works_by_id.values():
        dt = parse_dt(row.get("create_time"))
        if dt and window_start <= dt < window_end:
            snapshot_works.append(row)
    snapshot_works.sort(key=lambda x: (x.get("create_time", ""), x.get("account_id", "")), reverse=True)

    metric_keys = {(x.get("aweme_id", ""), x.get("observed_at", "")) for x in metrics_existing}
    metrics_merged = metrics_existing + [
        x for x in new_metrics if (x["aweme_id"], x["observed_at"]) not in metric_keys
    ]
    runs_merged = runs_existing + new_runs
    updated_accounts.sort(key=lambda x: x["account_id"])

    write_csv(data_dir() / "accounts.csv", updated_accounts, ACCOUNT_FIELDS)
    write_csv(data_dir() / "works.csv", snapshot_works, WORK_FIELDS)
    write_csv(data_dir() / "work_metrics.csv", metrics_merged, METRIC_FIELDS)
    write_csv(data_dir() / "ingestion_runs.csv", runs_merged, RUN_FIELDS)

    complete_count = sum(int(x.get("window_15d_complete", 0) or 0) for x in updated_accounts)
    incomplete = [x.get("current_nickname") or x["case_id"] for x in updated_accounts if not int(x.get("window_15d_complete", 0) or 0)]
    manifest = {
        "observed_at": observed_at,
        "collector": "F2_AUTHENTICATED_LOCAL",
        "accounts": len(updated_accounts),
        "works_in_window": len(snapshot_works),
        "complete_accounts": complete_count,
        "incomplete_accounts": incomplete,
        "window_start": window_start.isoformat(),
        "window_end_exclusive": window_end.isoformat(),
        "authenticated_gate_pass": complete_count == len(updated_accounts),
    }
    (data_dir() / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (run_raw / "collection_summary.json").write_text(
        json.dumps({"manifest": manifest, "accounts": result_summary}, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    if manifest["authenticated_gate_pass"]:
        print("[PASS] All 9 core accounts passed authenticated window closure.")
        return 0

    print("[BLOCKED] One or more core accounts failed authenticated completeness. HG01 remains closed.")
    return 2


def main() -> int:
    parser = argparse.ArgumentParser(description="Authenticated F2 collector for the locked 9-account R3 Douyin database.")
    parser.add_argument("--start", default="2026-08-10", help="inclusive local date, YYYY-MM-DD")
    parser.add_argument("--end", default="2026-08-25", help="exclusive local date, YYYY-MM-DD")
    args = parser.parse_args()
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    raise SystemExit(main())
