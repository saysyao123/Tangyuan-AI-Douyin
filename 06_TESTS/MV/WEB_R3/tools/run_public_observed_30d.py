#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import requests

BASE = "https://api.bugpk.com/api/dyzy"
PAGE_SIZE = 30
BACKOFF = (3, 7, 15)


def parse_dt(value: Any) -> datetime | None:
    try:
        return datetime.strptime(str(value), "%Y-%m-%d %H:%M:%S")
    except Exception:
        return None


def request_profile(session: requests.Session, sec_uid: str) -> dict[str, Any]:
    last: Exception | None = None
    for attempt in range(len(BACKOFF) + 1):
        try:
            r = session.get(BASE, params={"id": sec_uid, "page": 1, "page_size": PAGE_SIZE}, timeout=45)
            if r.status_code == 429 and attempt < len(BACKOFF):
                time.sleep(BACKOFF[attempt]); continue
            r.raise_for_status()
            payload = r.json()
            if not isinstance(payload, dict) or payload.get("code") != 200:
                raise RuntimeError(f"business failure: {payload}")
            return payload
        except Exception as exc:
            last = exc
            if attempt < len(BACKOFF):
                time.sleep(BACKOFF[attempt])
    raise RuntimeError(str(last))


def main() -> int:
    root = Path(__file__).resolve().parents[4]
    profiles = json.loads((root / "06_TESTS/MV/WEB_R3/core_profile_resolution_v1.json").read_text(encoding="utf-8"))
    profiles = [p for p in profiles if not p.get("duplicate_of")]
    accounts_csv = root / "06_TESTS/MV/WEB_R3/database/accounts.csv"
    with accounts_csv.open("r", encoding="utf-8-sig", newline="") as f:
        accounts = list(csv.DictReader(f))
    account_by_case = {a["case_id"]: a for a in accounts}

    session = requests.Session()
    session.headers.update({"User-Agent":"Mozilla/5.0","Accept":"application/json,text/plain,*/*"})
    all_items: list[dict[str, Any]] = []
    coverage: list[dict[str, Any]] = []

    for idx, p in enumerate(profiles, 1):
        case_id = p["case_id"]
        account = account_by_case[case_id]
        rec = {"case_id":case_id,"account_id":account["account_id"],"nickname":account["current_nickname"],"returned":0,"newest":"","oldest":"","has_more":"","error":""}
        try:
            payload = request_profile(session, p["sec_uid"])
            items = payload.get("data") or []
            if not isinstance(items, list): items = []
            dates = []
            for item in items:
                if not isinstance(item, dict) or not item.get("aweme_id"): continue
                dt = parse_dt(item.get("create_time"))
                if dt: dates.append(dt)
                stats = item.get("statistics") or {}
                all_items.append({
                    "case_id":case_id,"account_id":account["account_id"],"nickname":account["current_nickname"],
                    "aweme_id":str(item.get("aweme_id") or ""),"create_time":item.get("create_time") or "",
                    "work_url":item.get("share_url") or f"https://www.douyin.com/video/{item.get('aweme_id')}",
                    "caption":item.get("desc") or "","music_title_raw":item.get("music_title") or "",
                    "music_author_raw":item.get("music_author") or "","hashtags":"|".join(item.get("hashtags") or []),
                    "digg_count":stats.get("digg_count",0),"comment_count":stats.get("comment_count",0),
                    "share_count":stats.get("share_count",0),"collect_count":stats.get("collect_count",0),"play_count":stats.get("play_count",0),
                })
            rec["returned"] = len(items)
            rec["newest"] = max(dates).strftime("%Y-%m-%d %H:%M:%S") if dates else ""
            rec["oldest"] = min(dates).strftime("%Y-%m-%d %H:%M:%S") if dates else ""
            rec["has_more"] = (payload.get("pagination") or {}).get("has_more", "")
        except Exception as exc:
            rec["error"] = str(exc)[:300]
        coverage.append(rec)
        if idx < len(profiles): time.sleep(2.5)

    valid_dates = [parse_dt(x["create_time"]) for x in all_items if parse_dt(x["create_time"])]
    if not valid_dates:
        raise RuntimeError("no observable public works")
    anchor = max(valid_dates)
    end_exclusive = (anchor + timedelta(days=1)).replace(hour=0,minute=0,second=0,microsecond=0)
    start = end_exclusive - timedelta(days=30)
    observed = [x for x in all_items if (dt:=parse_dt(x["create_time"])) and start <= dt < end_exclusive]
    observed.sort(key=lambda x:(x["create_time"],x["account_id"]), reverse=True)

    out = root / "06_TESTS/MV/WEB_R3/database/public_observed_30d"
    out.mkdir(parents=True, exist_ok=True)
    fields = list(observed[0].keys()) if observed else list(all_items[0].keys())
    with (out / "works_observed_30d.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n"); w.writeheader(); w.writerows(observed)
    with (out / "coverage.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(coverage[0].keys()),lineterminator="\n"); w.writeheader(); w.writerows(coverage)
    summary={
        "mode":"PUBLIC_OBSERVED_30D","anchor_latest_observed":anchor.strftime("%Y-%m-%d %H:%M:%S"),
        "window_start":start.strftime("%Y-%m-%d %H:%M:%S"),"window_end_exclusive":end_exclusive.strftime("%Y-%m-%d %H:%M:%S"),
        "unique_accounts":len(profiles),"observable_rows":len(observed),"source":"BUGPK_DYZY_PUBLIC_PAGE1",
        "semantics":"positive evidence only; absence is UNKNOWN, never NO_WORK; refresh every 15 days and merge by aweme_id"
    }
    (out / "summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
