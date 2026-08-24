#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import requests

BASE = "https://api.bugpk.com/api/dyzy"
WINDOW_START = datetime(2026, 8, 10, 0, 0, 0)
WINDOW_END = datetime(2026, 8, 25, 0, 0, 0)
PAGE_SIZE = 30
MAX_PAGES = 8
BACKOFF = (3, 7, 15, 30)


def parse_dt(value: Any) -> datetime | None:
    try:
        return datetime.strptime(str(value), "%Y-%m-%d %H:%M:%S")
    except Exception:
        return None


def request_page(session: requests.Session, sec_uid: str, page: int) -> dict[str, Any]:
    last: Exception | None = None
    for attempt in range(len(BACKOFF) + 1):
        try:
            response = session.get(
                BASE,
                params={"id": sec_uid, "page": page, "page_size": PAGE_SIZE},
                timeout=45,
            )
            if response.status_code == 429 and attempt < len(BACKOFF):
                wait = BACKOFF[attempt]
                print(f"[429] page={page} wait={wait}s", flush=True)
                time.sleep(wait)
                continue
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict) or data.get("code") != 200:
                raise RuntimeError(f"business failure: {data}")
            return data
        except Exception as exc:
            last = exc
            if attempt < len(BACKOFF):
                wait = BACKOFF[attempt]
                print(f"[RETRY] page={page} wait={wait}s error={exc}", flush=True)
                time.sleep(wait)
    raise RuntimeError(str(last))


def stable_row(case_id: str, item: dict[str, Any]) -> dict[str, Any]:
    stats = item.get("statistics") or {}
    return {
        "case_id": case_id,
        "account": item.get("author") or "",
        "author_sec_uid": item.get("author_sec_uid") or "",
        "aweme_id": str(item.get("aweme_id") or ""),
        "create_time": item.get("create_time") or "",
        "work_url": item.get("share_url") or "",
        "caption": item.get("desc") or "",
        "type": item.get("type") or "",
        "duration_s": item.get("duration") or "",
        "music_title_raw": item.get("music_title") or "",
        "music_author_raw": item.get("music_author") or "",
        "digg_count": stats.get("digg_count", 0),
        "comment_count": stats.get("comment_count", 0),
        "share_count": stats.get("share_count", 0),
        "collect_count": stats.get("collect_count", 0),
        "play_count": stats.get("play_count", 0),
        "hashtags": "|".join(item.get("hashtags") or []),
    }


def main() -> int:
    repo_root = Path(__file__).resolve().parents[4]
    profiles = json.loads(
        (repo_root / "06_TESTS/MV/WEB_R3/core_profile_resolution_v1.json").read_text(encoding="utf-8")
    )
    profiles = [p for p in profiles if not p.get("duplicate_of")]
    out = repo_root / "06_TESTS/MV/WEB_R3/_complete_15d_probe"
    raw = out / "raw"
    raw.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/139 Safari/537.36",
        "Accept": "application/json,text/plain,*/*",
    })

    all_rows: list[dict[str, Any]] = []
    account_reports: list[dict[str, Any]] = []

    for profile_index, profile in enumerate(profiles):
        case_id = profile["case_id"]
        sec_uid = profile["sec_uid"]
        seen: set[str] = set()
        fetched: list[dict[str, Any]] = []
        report: dict[str, Any] = {
            "case_id": case_id,
            "sec_uid": sec_uid,
            "pages_fetched": 0,
            "items_fetched": 0,
            "items_15d": 0,
            "oldest_fetched": "",
            "newest_fetched": "",
            "terminal_has_more": None,
            "complete_15d": False,
            "stop_reason": "",
            "error": "",
        }
        try:
            for page in range(1, MAX_PAGES + 1):
                payload = request_page(session, sec_uid, page)
                (raw / f"{case_id}_page_{page}.json").write_text(
                    json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
                )
                report["pages_fetched"] = page
                items = payload.get("data") or []
                if not isinstance(items, list):
                    items = []
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    aweme_id = str(item.get("aweme_id") or "")
                    if not aweme_id or aweme_id in seen:
                        continue
                    seen.add(aweme_id)
                    fetched.append(item)

                dates = [parse_dt(item.get("create_time")) for item in fetched]
                dates = [dt for dt in dates if dt]
                oldest = min(dates) if dates else None
                newest = max(dates) if dates else None
                pagination = payload.get("pagination") or {}
                has_more = bool(pagination.get("has_more"))
                report["terminal_has_more"] = has_more
                report["oldest_fetched"] = oldest.strftime("%Y-%m-%d %H:%M:%S") if oldest else ""
                report["newest_fetched"] = newest.strftime("%Y-%m-%d %H:%M:%S") if newest else ""

                if oldest and oldest < WINDOW_START:
                    report["complete_15d"] = True
                    report["stop_reason"] = "OLDEST_BEFORE_WINDOW_START"
                    break
                if not has_more:
                    report["complete_15d"] = True
                    report["stop_reason"] = "HAS_MORE_FALSE"
                    break
                if not items:
                    report["stop_reason"] = "EMPTY_PAGE_WITH_HAS_MORE"
                    break
                time.sleep(2.5)
            else:
                report["stop_reason"] = "MAX_PAGES_REACHED"

            report["items_fetched"] = len(fetched)
            for item in fetched:
                dt = parse_dt(item.get("create_time"))
                if dt and WINDOW_START <= dt < WINDOW_END:
                    all_rows.append(stable_row(case_id, item))
                    report["items_15d"] += 1
        except Exception as exc:
            report["error"] = str(exc)[:500]
        account_reports.append(report)
        if profile_index < len(profiles) - 1:
            time.sleep(2.5)

    all_rows.sort(key=lambda row: (row["create_time"], row["case_id"]), reverse=True)
    out.mkdir(parents=True, exist_ok=True)
    (out / "account_completeness.json").write_text(
        json.dumps(account_reports, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out / "stable_15d_works.json").write_text(
        json.dumps(all_rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    if all_rows:
        with (out / "stable_15d_works.csv").open("w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=list(all_rows[0].keys()))
            writer.writeheader()
            writer.writerows(all_rows)

    complete = sum(1 for report in account_reports if report["complete_15d"])
    summary = {
        "unique_profiles": len(profiles),
        "profiles_complete_15d": complete,
        "all_profiles_complete_15d": complete == len(profiles),
        "works_15d": len(all_rows),
        "reports": account_reports,
    }
    (out / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps({
        "unique_profiles": len(profiles),
        "profiles_complete_15d": complete,
        "all_profiles_complete_15d": summary["all_profiles_complete_15d"],
        "works_15d": len(all_rows),
    }, ensure_ascii=False), flush=True)
    return 0 if summary["all_profiles_complete_15d"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
