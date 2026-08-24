#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import csv
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict

TZ8 = timezone(timedelta(hours=8))
START_DATE = "2026-08-10"
END_DATE = "2026-08-24"


def safe_int(v: Any) -> int:
    try:
        return int(v or 0)
    except Exception:
        return 0


def normalize_work(item: Dict[str, Any], case_id: str, input_link: str, sec_uid: str) -> Dict[str, Any]:
    author = item.get("author") or {}
    music = item.get("music") or {}
    stats = item.get("statistics") or item.get("stats") or {}
    ts = safe_int(item.get("create_time"))
    dt = datetime.fromtimestamp(ts, TZ8) if ts else None
    aweme_id = str(item.get("aweme_id") or "")
    share = item.get("share_info") or {}
    share_url = share.get("share_url") or ""
    if not isinstance(share_url, str) or not share_url.startswith("http"):
        share_url = f"https://www.douyin.com/video/{aweme_id}" if aweme_id else ""
    effective_sec_uid = author.get("sec_uid") or sec_uid
    return {
        "case_id": case_id,
        "input_profile_short_url": input_link,
        "aweme_id": aweme_id,
        "publish_time": dt.isoformat(timespec="seconds") if dt else "",
        "publish_date": dt.date().isoformat() if dt else "",
        "author_nickname": author.get("nickname") or "",
        "author_unique_id": author.get("unique_id") or "",
        "author_short_id": author.get("short_id") or "",
        "author_sec_uid": effective_sec_uid,
        "author_url": f"https://www.douyin.com/user/{effective_sec_uid}" if effective_sec_uid else "",
        "desc": (item.get("desc") or "").replace("\n", " ").strip(),
        "music_id": music.get("id_str") or music.get("id") or "",
        "music_title": music.get("title") or "",
        "music_author": music.get("author") or music.get("author_name") or "",
        "digg_count": safe_int(stats.get("digg_count")),
        "comment_count": safe_int(stats.get("comment_count")),
        "share_count": safe_int(stats.get("share_count")),
        "collect_count": safe_int(stats.get("collect_count")),
        "play_count": safe_int(stats.get("play_count")),
        "work_url": share_url,
        "aweme_type": item.get("aweme_type") if item.get("aweme_type") is not None else "",
    }


async def main_async() -> int:
    repo_root = Path(__file__).resolve().parents[4]
    backend = repo_root / ".tmp_douyin_downloader"
    sys.path.insert(0, str(backend))

    from core import DouyinAPIClient, URLParser
    from utils.validators import normalize_short_url

    links = json.loads((repo_root / "06_TESTS/MV/WEB_R3/core_profile_links_input.json").read_text(encoding="utf-8"))
    out_root = repo_root / "06_TESTS/MV/WEB_R3/_browser_probe_output"
    out_root.mkdir(parents=True, exist_ok=True)

    statuses = []
    all_works = []

    for idx, link in enumerate(links, 1):
        case_id = f"P{idx:02d}"
        status: Dict[str, Any] = {
            "case_id": case_id,
            "input_link": link,
            "resolved_url": "",
            "sec_uid": "",
            "browser_ids": 0,
            "captured_post_items": 0,
            "works_15d": 0,
            "browser_stats": {},
            "error": "",
        }
        try:
            async with DouyinAPIClient({}) as api_client:
                resolved = await api_client.resolve_short_url(normalize_short_url(link))
                status["resolved_url"] = resolved or ""
                parsed = URLParser.parse(resolved or "") if resolved else None
                sec_uid = str((parsed or {}).get("sec_uid") or "")
                status["sec_uid"] = sec_uid
                if not sec_uid:
                    raise RuntimeError("short URL resolved but no sec_uid found")

                ids = await api_client.collect_user_post_ids_via_browser(
                    sec_uid,
                    expected_count=0,
                    headless=True,
                    max_scrolls=24,
                    idle_rounds=4,
                    wait_timeout_seconds=60,
                )
                items = api_client.pop_browser_post_aweme_items()
                stats = api_client.pop_browser_post_stats()
                status["browser_ids"] = len(ids)
                status["captured_post_items"] = len(items)
                status["browser_stats"] = stats

                seen = set()
                for aweme_id in ids:
                    item = items.get(str(aweme_id))
                    if not isinstance(item, dict):
                        continue
                    if str(aweme_id) in seen:
                        continue
                    seen.add(str(aweme_id))
                    row = normalize_work(item, case_id, link, sec_uid)
                    if row["publish_date"] and START_DATE <= row["publish_date"] <= END_DATE:
                        all_works.append(row)
                        status["works_15d"] += 1
        except Exception as exc:
            status["error"] = " ".join(str(exc).split())[:500]
        statuses.append(status)

    fieldnames = [
        "case_id","input_profile_short_url","aweme_id","publish_time","publish_date",
        "author_nickname","author_unique_id","author_short_id","author_sec_uid","author_url",
        "desc","music_id","music_title","music_author","digg_count","comment_count",
        "share_count","collect_count","play_count","work_url","aweme_type"
    ]
    with (out_root / "core_15d_works.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader(); w.writerows(sorted(all_works, key=lambda r: r["publish_time"], reverse=True))

    (out_root / "core_15d_works.json").write_text(json.dumps(all_works, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_root / "probe_status.json").write_text(json.dumps(statuses, ensure_ascii=False, indent=2), encoding="utf-8")

    profile_rows = []
    for status in statuses:
        rows = [r for r in all_works if r["case_id"] == status["case_id"]]
        first = rows[0] if rows else {}
        profile_rows.append({
            "case_id": status["case_id"],
            "input_link": status["input_link"],
            "resolved_url": status["resolved_url"],
            "sec_uid": status["sec_uid"],
            "author_nickname": first.get("author_nickname", ""),
            "author_unique_id": first.get("author_unique_id", ""),
            "author_url": first.get("author_url", f"https://www.douyin.com/user/{status['sec_uid']}" if status["sec_uid"] else ""),
            "browser_ids": status["browser_ids"],
            "captured_post_items": status["captured_post_items"],
            "works_15d": status["works_15d"],
            "error": status["error"],
        })
    with (out_root / "profile_resolution.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(profile_rows[0].keys()))
        w.writeheader(); w.writerows(profile_rows)

    print(json.dumps({"profiles": len(links), "works_15d": len(all_works), "output": str(out_root)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main_async()))
