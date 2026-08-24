#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests

BASE = "https://api.bugpk.com/api"
TZ8 = timezone(timedelta(hours=8))
START_DATE = datetime(2026, 8, 10, tzinfo=TZ8)
END_DATE = datetime(2026, 8, 25, tzinfo=TZ8)
BACKOFF_SECONDS = (3, 7, 15)


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
        for value in obj.values():
            yield from walk_work_items(value)


def fetch_json(
    session: requests.Session,
    url: str,
    params: dict[str, Any],
    timeout: int = 30,
):
    last_error: Exception | None = None
    for attempt in range(len(BACKOFF_SECONDS) + 1):
        try:
            response = session.get(url, params=params, timeout=timeout)
            if response.status_code == 429:
                if attempt >= len(BACKOFF_SECONDS):
                    response.raise_for_status()
                wait = BACKOFF_SECONDS[attempt]
                print(f"[RATE_LIMIT] {response.url} -> 429; sleep {wait}s", flush=True)
                time.sleep(wait)
                continue
            response.raise_for_status()
            return response.json(), response.url
        except (requests.RequestException, ValueError) as exc:
            last_error = exc
            if attempt >= len(BACKOFF_SECONDS):
                break
            wait = BACKOFF_SECONDS[attempt]
            print(f"[RETRY] {url} attempt={attempt + 1} error={exc}; sleep {wait}s", flush=True)
            time.sleep(wait)
    raise RuntimeError(f"request failed after retries: {last_error}")


def probe_media_url(session: requests.Session, url: str | None) -> dict[str, Any]:
    if not url:
        return {"ok": False, "status": None, "content_type": "", "bytes": 0, "error": "no_url"}
    try:
        with session.get(
            url,
            headers={"Range": "bytes=0-65535", "Referer": "https://www.douyin.com/"},
            stream=True,
            timeout=30,
            allow_redirects=True,
        ) as response:
            chunk = next(response.iter_content(chunk_size=65536), b"")
            content_type = response.headers.get("content-type", "")
            return {
                "ok": response.status_code in (200, 206) and len(chunk) > 0,
                "status": response.status_code,
                "content_type": content_type,
                "bytes": len(chunk),
                "final_url": response.url,
                "error": "",
            }
    except Exception as exc:
        return {
            "ok": False,
            "status": None,
            "content_type": "",
            "bytes": 0,
            "error": str(exc)[:300],
        }


def main() -> int:
    repo_root = Path(__file__).resolve().parents[4]
    resolved_profiles = json.loads(
        (repo_root / "06_TESTS/MV/WEB_R3/core_profile_resolution_v1.json").read_text(encoding="utf-8")
    )
    out = repo_root / "06_TESTS/MV/WEB_R3/_bugpk_probe_output"
    raw_dir = out / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/139 Safari/537.36",
            "Accept": "application/json,text/plain,*/*",
        }
    )

    statuses: list[dict[str, Any]] = []
    works_15d: list[dict[str, Any]] = []
    single_probes: list[dict[str, Any]] = []

    # P08 is the same account as P03; keep its identity record but do not burn API quota twice.
    unique_profiles = [profile for profile in resolved_profiles if not profile.get("duplicate_of")]

    for index, profile in enumerate(unique_profiles, 1):
        case_id = profile["case_id"]
        link = profile["input_link"]
        sec_uid = profile["sec_uid"]
        status = {
            "case_id": case_id,
            "input_link": link,
            "sec_uid_requested": sec_uid,
            "profile_code": None,
            "profile_msg": "",
            "total_items": 0,
            "items_15d": 0,
            "author_sec_uid": "",
            "author": "",
            "error": "",
        }
        try:
            payload, request_url = fetch_json(
                session,
                f"{BASE}/dyzy",
                {"id": sec_uid, "page": 1, "page_size": 30},
            )
            (raw_dir / f"{case_id}_profile.json").write_text(
                json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            status["request_url"] = request_url
            status["profile_code"] = payload.get("code") if isinstance(payload, dict) else None
            status["profile_msg"] = (
                (payload.get("msg") or payload.get("mag") or "") if isinstance(payload, dict) else ""
            )
            items = list(
                walk_work_items((payload or {}).get("data") if isinstance(payload, dict) else payload)
            )
            status["total_items"] = len(items)

            for item in items:
                dt = parse_dt(item.get("create_time"))
                if not dt or not (START_DATE <= dt < END_DATE):
                    continue
                statistics = item.get("statistics") or {}
                row = {
                    "case_id": case_id,
                    "input_profile_short_url": link,
                    "aweme_id": str(item.get("aweme_id") or ""),
                    "create_time": item.get("create_time") or "",
                    "author": item.get("author") or "",
                    "author_uid": str(item.get("author_uid") or ""),
                    "author_sec_uid": item.get("author_sec_uid") or sec_uid,
                    "desc": item.get("desc") or "",
                    "share_url": item.get("share_url") or "",
                    "type": item.get("type") or "",
                    "duration": item.get("duration") or "",
                    "music_title": item.get("music_title") or "",
                    "music_author": item.get("music_author") or "",
                    "music_url": item.get("music_url") or "",
                    "video_url": item.get("url") or "",
                    "digg_count": statistics.get("digg_count", 0),
                    "comment_count": statistics.get("comment_count", 0),
                    "share_count": statistics.get("share_count", 0),
                    "collect_count": statistics.get("collect_count", 0),
                    "play_count": statistics.get("play_count", 0),
                    "hashtags": "|".join(item.get("hashtags") or []),
                }
                works_15d.append(row)
                status["items_15d"] += 1
                if not status["author_sec_uid"]:
                    status["author_sec_uid"] = row["author_sec_uid"]
                    status["author"] = row["author"]

            first = next(
                (
                    work
                    for work in works_15d
                    if work["case_id"] == case_id and work["share_url"]
                ),
                None,
            )
            if first:
                # Avoid immediately hitting the free endpoint after the profile call.
                time.sleep(2.0)
                detail, detail_url = fetch_json(
                    session, f"{BASE}/douyin", {"url": first["share_url"]}
                )
                (raw_dir / f"{case_id}_single.json").write_text(
                    json.dumps(detail, ensure_ascii=False, indent=2), encoding="utf-8"
                )
                data = detail.get("data") or {} if isinstance(detail, dict) else {}
                video_url = data.get("url") if isinstance(data, dict) else ""
                backup = data.get("video_backup") if isinstance(data, dict) else None
                if not video_url and isinstance(backup, list) and backup:
                    candidate = backup[0]
                    video_url = candidate.get("url") if isinstance(candidate, dict) else str(candidate)
                media_probe = probe_media_url(session, video_url)
                single_probes.append(
                    {
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
                    }
                )
        except Exception as exc:
            status["error"] = str(exc)[:500]
        statuses.append(status)

        if index < len(unique_profiles):
            time.sleep(2.5)

    # Preserve duplicate identity explicitly without fetching the same account twice.
    by_case = {status["case_id"]: status for status in statuses}
    for profile in resolved_profiles:
        duplicate_of = profile.get("duplicate_of")
        if not duplicate_of:
            continue
        source = by_case.get(duplicate_of, {})
        statuses.append(
            {
                "case_id": profile["case_id"],
                "input_link": profile["input_link"],
                "sec_uid_requested": profile["sec_uid"],
                "profile_code": source.get("profile_code"),
                "profile_msg": "DUPLICATE_PROFILE_REUSED",
                "total_items": source.get("total_items", 0),
                "items_15d": source.get("items_15d", 0),
                "author_sec_uid": source.get("author_sec_uid", profile["sec_uid"]),
                "author": source.get("author", ""),
                "duplicate_of": duplicate_of,
                "error": source.get("error", ""),
            }
        )

    out.mkdir(parents=True, exist_ok=True)
    (out / "profile_status.json").write_text(
        json.dumps(statuses, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out / "works_15d.json").write_text(
        json.dumps(works_15d, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out / "single_video_probes.json").write_text(
        json.dumps(single_probes, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    if works_15d:
        with (out / "works_15d.csv").open("w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=list(works_15d[0].keys()))
            writer.writeheader()
            writer.writerows(works_15d)
    if statuses:
        fields = sorted({key for row in statuses for key in row.keys()})
        with (out / "profile_status.csv").open("w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(statuses)
    if single_probes:
        with (out / "single_video_probes.csv").open("w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=list(single_probes[0].keys()))
            writer.writeheader()
            writer.writerows(single_probes)

    summary = {
        "input_links": len(resolved_profiles),
        "unique_profiles": len(unique_profiles),
        "profile_success": sum(
            1
            for status in statuses
            if not status.get("duplicate_of")
            and status.get("profile_code") == 200
            and status.get("total_items", 0) > 0
        ),
        "works_15d": len(works_15d),
        "single_detail_tests": len(single_probes),
        "single_detail_success": sum(
            1 for probe in single_probes if probe.get("detail_code") == 200
        ),
        "download_probe_success": sum(
            1 for probe in single_probes if probe.get("media_ok")
        ),
    }
    (out / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False), flush=True)
    return 0 if summary["profile_success"] > 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
