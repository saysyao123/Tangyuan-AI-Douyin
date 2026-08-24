#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests

BASE = "https://api.bugpk.com/api"
TZ8 = timezone(timedelta(hours=8))
START_DATE = datetime(2026, 8, 10, tzinfo=TZ8)
END_DATE = datetime(2026, 8, 25, tzinfo=TZ8)


def parse_dt(value: Any):
    if not value:
        return None
    text = str(value).strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt).replace(tzinfo=TZ8)
        except ValueError:
            pass
    return None


def walk_work_items(obj: Any):
    if isinstance(obj, list):
        for item in obj:
            if isinstance(item, dict) and item.get("aweme_id"):
                yield item
            else:
                yield from walk_work_items(item)
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from walk_work_items(v)


def fetch_json(session: requests.Session, url: str, params: dict[str, Any], timeout: int = 30):
    r = session.get(url, params=params, timeout=timeout)
    r.raise_for_status()
    return r.json(), r.url


def probe_media_url(session: requests.Session, url: str | None) -> dict[str, Any]:
    if not url:
        return {"ok": False, "status": None, "content_type": "", "bytes": 0, "error": "no_url"}
    try:
        with session.get(url, headers={"Range": "bytes=0-65535", "Referer": "https://www.douyin.com/"}, stream=True, timeout=30, allow_redirects=True) as r:
            chunk = next(r.iter_content(chunk_size=65536), b"")
            return {
                "ok": r.status_code in (200, 206) and len(chunk) > 0,
                "status": r.status_code,
                "content_type": r.headers.get("content-type", ""),
                "bytes": len(chunk),
                "final_url": r.url,
                "error": "",
            }
    except Exception as exc:
        return {"ok": False, "status": None, "content_type": "", "bytes": 0, "error": str(exc)[:300]}


def main() -> int:
    repo_root = Path(__file__).resolve().parents[4]
    links = json.loads((repo_root / "06_TESTS/MV/WEB_R3/core_profile_links_input.json").read_text(encoding="utf-8"))
    out = repo_root / "06_TESTS/MV/WEB_R3/_bugpk_probe_output"
    raw_dir = out / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 R3-BugPk-Probe/1.0"})

    statuses: list[dict[str, Any]] = []
    works_15d: list[dict[str, Any]] = []
    single_probes: list[dict[str, Any]] = []

    for idx, link in enumerate(links, 1):
        case_id = f"P{idx:02d}"
        status = {
            "case_id": case_id,
            "input_link": link,
            "profile_code": None,
            "profile_msg": "",
            "total_items": 0,
            "items_15d": 0,
            "unique_sec_uid": "",
            "author": "",
            "error": "",
        }
        try:
            payload, request_url = fetch_json(
                session,
                f"{BASE}/dyzy",
                {"url": link, "page": 1, "page_size": 50},
            )
            (raw_dir / f"{case_id}_profile.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            status["request_url"] = request_url
            status["profile_code"] = payload.get("code") if isinstance(payload, dict) else None
            status["profile_msg"] = payload.get("msg") or payload.get("mag") or "" if isinstance(payload, dict) else ""
            items = list(walk_work_items((payload or {}).get("data") if isinstance(payload, dict) else payload))
            status["total_items"] = len(items)
            for item in items:
                dt = parse_dt(item.get("create_time"))
                if not dt or not (START_DATE <= dt < END_DATE):
                    continue
                stats = item.get("statistics") or {}
                row = {
                    "case_id": case_id,
                    "input_profile_short_url": link,
                    "aweme_id": str(item.get("aweme_id") or ""),
                    "create_time": item.get("create_time") or "",
                    "author": item.get("author") or "",
                    "author_uid": str(item.get("author_uid") or ""),
                    "author_sec_uid": item.get("author_sec_uid") or "",
                    "desc": item.get("desc") or "",
                    "share_url": item.get("share_url") or "",
                    "type": item.get("type") or "",
                    "duration": item.get("duration") or "",
                    "music_title": item.get("music_title") or "",
                    "music_author": item.get("music_author") or "",
                    "music_url": item.get("music_url") or "",
                    "video_url": item.get("url") or "",
                    "digg_count": stats.get("digg_count", 0),
                    "comment_count": stats.get("comment_count", 0),
                    "share_count": stats.get("share_count", 0),
                    "collect_count": stats.get("collect_count", 0),
                    "play_count": stats.get("play_count", 0),
                    "hashtags": "|".join(item.get("hashtags") or []),
                }
                works_15d.append(row)
                status["items_15d"] += 1
                if not status["unique_sec_uid"]:
                    status["unique_sec_uid"] = row["author_sec_uid"]
                    status["author"] = row["author"]

            # Test one real work per profile against the single-video endpoint.
            first = next((x for x in works_15d if x["case_id"] == case_id and x["share_url"]), None)
            if first:
                detail, detail_url = fetch_json(session, f"{BASE}/douyin", {"url": first["share_url"]})
                (raw_dir / f"{case_id}_single.json").write_text(json.dumps(detail, ensure_ascii=False, indent=2), encoding="utf-8")
                data = detail.get("data") or {} if isinstance(detail, dict) else {}
                video_url = data.get("url") if isinstance(data, dict) else ""
                backup = data.get("video_backup") if isinstance(data, dict) else None
                if not video_url and isinstance(backup, list) and backup:
                    cand = backup[0]
                    video_url = cand.get("url") if isinstance(cand, dict) else str(cand)
                media_probe = probe_media_url(session, video_url)
                single_probes.append({
                    "case_id": case_id,
                    "aweme_id": first["aweme_id"],
                    "share_url": first["share_url"],
                    "detail_code": detail.get("code") if isinstance(detail, dict) else None,
                    "detail_msg": detail.get("msg") if isinstance(detail, dict) else "",
                    "detail_type": data.get("type") if isinstance(data, dict) else "",
                    "detail_title": data.get("title") if isinstance(data, dict) else "",
                    "resolved_video_url": video_url or "",
                    "media_ok": media_probe.get("ok"),
                    "media_status": media_probe.get("status"),
                    "media_content_type": media_probe.get("content_type"),
                    "media_bytes": media_probe.get("bytes"),
                    "media_error": media_probe.get("error"),
                    "detail_request_url": detail_url,
                })
        except Exception as exc:
            status["error"] = str(exc)[:500]
        statuses.append(status)

    out.mkdir(parents=True, exist_ok=True)
    (out / "profile_status.json").write_text(json.dumps(statuses, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "works_15d.json").write_text(json.dumps(works_15d, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "single_video_probes.json").write_text(json.dumps(single_probes, ensure_ascii=False, indent=2), encoding="utf-8")

    if works_15d:
        with (out / "works_15d.csv").open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(works_15d[0].keys()))
            w.writeheader(); w.writerows(works_15d)
    if statuses:
        with (out / "profile_status.csv").open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(statuses[0].keys()))
            w.writeheader(); w.writerows(statuses)
    if single_probes:
        with (out / "single_video_probes.csv").open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(single_probes[0].keys()))
            w.writeheader(); w.writerows(single_probes)

    summary = {
        "profiles": len(links),
        "profile_success": sum(1 for s in statuses if s.get("profile_code") == 200 and s.get("total_items", 0) > 0),
        "works_15d": len(works_15d),
        "single_detail_tests": len(single_probes),
        "download_probe_success": sum(1 for p in single_probes if p.get("media_ok")),
    }
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if summary["profile_success"] > 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
