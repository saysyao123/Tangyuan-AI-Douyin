#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import io
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import requests

BASE = "https://api.bugpk.com/api/dyzy"
WINDOW_START = datetime(2026, 8, 10, 0, 0, 0)
WINDOW_END = datetime(2026, 8, 25, 0, 0, 0)
PAGE_SIZE = 30
MAX_PAGES = 8
BACKOFF = (3, 7, 15, 30)
CASE_ORDER = ["P01", "P02", "P03", "P04", "P05", "P06", "P07", "P09", "P10"]


def parse_dt(value: Any) -> datetime | None:
    try:
        return datetime.strptime(str(value), "%Y-%m-%d %H:%M:%S")
    except Exception:
        return None


def fetch_page(session: requests.Session, sec_uid: str, page: int) -> dict[str, Any]:
    last: Exception | None = None
    for attempt in range(len(BACKOFF) + 1):
        try:
            response = session.get(BASE, params={"id": sec_uid, "page": page, "page_size": PAGE_SIZE}, timeout=45)
            if response.status_code == 429 and attempt < len(BACKOFF):
                time.sleep(BACKOFF[attempt])
                continue
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, dict) or payload.get("code") != 200:
                raise RuntimeError(f"business failure: {payload}")
            return payload
        except Exception as exc:
            last = exc
            if attempt < len(BACKOFF):
                time.sleep(BACKOFF[attempt])
    raise RuntimeError(str(last))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        if rows:
            writer.writerows(rows)


def load_existing_metrics(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main() -> int:
    data_dir = Path(__file__).resolve().parent
    r3_dir = data_dir.parent
    profiles = json.loads((r3_dir / "core_profile_resolution_v1.json").read_text(encoding="utf-8"))
    profiles = {p["case_id"]: p for p in profiles if not p.get("duplicate_of")}
    roles = json.loads((data_dir / "account_roles_v1.json").read_text(encoding="utf-8"))
    observed_at = datetime.now(ZoneInfo("Asia/Manila")).isoformat(timespec="seconds")
    stamp = datetime.now(ZoneInfo("Asia/Manila")).strftime("%Y%m%d_%H%M%S")

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/139 Safari/537.36",
        "Accept": "application/json,text/plain,*/*",
    })

    accounts: list[dict[str, Any]] = []
    works: list[dict[str, Any]] = []
    new_metrics: list[dict[str, Any]] = []
    runs: list[dict[str, Any]] = []

    for index, case_id in enumerate(CASE_ORDER, 1):
        profile = profiles[case_id]
        sec_uid = profile["sec_uid"]
        role = roles[case_id]
        account_id = f"DYCORE{index:02d}"
        fetched: list[dict[str, Any]] = []
        seen: set[str] = set()
        nickname = ""
        complete = False
        stop_reason = ""
        terminal_has_more = True
        error = ""
        pages_fetched = 0

        try:
            for page in range(1, MAX_PAGES + 1):
                payload = fetch_page(session, sec_uid, page)
                pages_fetched = page
                items = payload.get("data") or []
                if not isinstance(items, list):
                    items = []
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    if not nickname:
                        nickname = item.get("author") or ""
                    aweme_id = str(item.get("aweme_id") or "")
                    if aweme_id and aweme_id not in seen:
                        seen.add(aweme_id)
                        fetched.append(item)
                dates = [parse_dt(item.get("create_time")) for item in fetched]
                dates = [dt for dt in dates if dt]
                oldest = min(dates) if dates else None
                terminal_has_more = bool((payload.get("pagination") or {}).get("has_more"))
                if oldest and oldest < WINDOW_START:
                    complete = True
                    stop_reason = "OLDEST_BEFORE_WINDOW_START"
                    break
                if not terminal_has_more:
                    complete = True
                    stop_reason = "HAS_MORE_FALSE"
                    break
                if not items:
                    stop_reason = "EMPTY_PAGE_WITH_HAS_MORE"
                    break
                time.sleep(2.5)
            else:
                stop_reason = "MAX_PAGES_REACHED"
        except Exception as exc:
            error = str(exc)[:500]
            stop_reason = "COLLECTOR_ERROR"

        dates = [parse_dt(item.get("create_time")) for item in fetched]
        dates = [dt for dt in dates if dt]
        oldest = min(dates) if dates else None
        newest = max(dates) if dates else None
        in_window = [item for item in fetched if (dt := parse_dt(item.get("create_time"))) and WINDOW_START <= dt < WINDOW_END]

        accounts.append({
            "account_id": account_id,
            "case_id": case_id,
            "sec_uid": sec_uid,
            "douyin_id": role["douyin_id"],
            "current_nickname": nickname,
            "profile_short_url": profile["input_link"],
            "role": role["role"],
            "role_category": role["role_category"],
            "trend_weight": role["trend_weight"],
            "visual_weight": role["visual_weight"],
            "packaging_weight": role["packaging_weight"],
            "registry_source": role["registry_source"],
            "r3_test_core": 1,
            "active": 1,
            "last_verified_at": observed_at,
            "window_15d_complete": 1 if complete else 0,
            "notes": "nickname mutable; sec_uid is the stable external key",
        })

        for item in in_window:
            stats = item.get("statistics") or {}
            aweme_id = str(item.get("aweme_id") or "")
            works.append({
                "aweme_id": aweme_id,
                "account_id": account_id,
                "create_time": item.get("create_time") or "",
                "work_url": item.get("share_url") or f"https://www.douyin.com/video/{aweme_id}",
                "caption": item.get("desc") or "",
                "type": item.get("type") or "",
                "duration_s": item.get("duration") or "",
                "music_title_raw": item.get("music_title") or "",
                "music_author_raw": item.get("music_author") or "",
                "hashtags": "|".join(item.get("hashtags") or []),
                "first_observed_at": observed_at,
            })
            new_metrics.append({
                "aweme_id": aweme_id,
                "observed_at": observed_at,
                "digg_count": stats.get("digg_count", 0),
                "comment_count": stats.get("comment_count", 0),
                "share_count": stats.get("share_count", 0),
                "collect_count": stats.get("collect_count", 0),
                "play_count": stats.get("play_count", 0),
            })

        runs.append({
            "run_id": f"R3A3_{stamp}_{case_id}",
            "account_id": account_id,
            "window_start": WINDOW_START.strftime("%Y-%m-%d %H:%M:%S"),
            "window_end_exclusive": WINDOW_END.strftime("%Y-%m-%d %H:%M:%S"),
            "pages_fetched": pages_fetched,
            "items_fetched": len(fetched),
            "items_in_window": len(in_window),
            "oldest_fetched": oldest.strftime("%Y-%m-%d %H:%M:%S") if oldest else "",
            "newest_fetched": newest.strftime("%Y-%m-%d %H:%M:%S") if newest else "",
            "terminal_has_more": 1 if terminal_has_more else 0,
            "window_complete": 1 if complete else 0,
            "stop_reason": stop_reason,
            "error": error,
            "collector": "BUGPK_DYZY_PUBLIC_API",
            "observed_at": observed_at,
        })
        time.sleep(2.5)

    works.sort(key=lambda row: (row["create_time"], row["account_id"]), reverse=True)
    write_csv(data_dir / "accounts.csv", accounts)
    write_csv(data_dir / "works.csv", works)

    metrics_path = data_dir / "work_metrics.csv"
    existing_metrics = load_existing_metrics(metrics_path)
    metric_keys = {(r.get("aweme_id", ""), r.get("observed_at", "")) for r in existing_metrics}
    merged_metrics = existing_metrics + [r for r in new_metrics if (r["aweme_id"], r["observed_at"]) not in metric_keys]
    write_csv(metrics_path, merged_metrics, fieldnames=["aweme_id","observed_at","digg_count","comment_count","share_count","collect_count","play_count"])

    runs_path = data_dir / "ingestion_runs.csv"
    old_runs: list[dict[str, str]] = []
    if runs_path.exists():
        with runs_path.open("r", encoding="utf-8-sig", newline="") as f:
            old_runs = list(csv.DictReader(f))
    write_csv(runs_path, old_runs + runs)

    normalization = data_dir / "song_normalization.csv"
    if not normalization.exists():
        normalization.write_text("song_key,music_title_raw,music_author_raw,song_family,audio_version,normalization_status,confidence,reviewed_at,notes\n", encoding="utf-8")

    manifest = {
        "observed_at": observed_at,
        "accounts": len(accounts),
        "works_in_window": len(works),
        "complete_accounts": sum(int(a["window_15d_complete"]) for a in accounts),
        "incomplete_accounts": [a["current_nickname"] or a["case_id"] for a in accounts if not a["window_15d_complete"]],
        "window_start": WINDOW_START.isoformat(),
        "window_end_exclusive": WINDOW_END.isoformat(),
    }
    (data_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
