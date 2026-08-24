#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

TZ8 = timezone(timedelta(hours=8))
START_DATE = "2026-08-10"
END_DATE_EXCLUSIVE = "2026-08-25"


def q(v: str) -> str:
    return json.dumps(v, ensure_ascii=False)


def write_config(path: Path, link: str, out_dir: Path) -> None:
    text = f'''link:\n  - {link}\npath: {out_dir.as_posix()}\nvideo: false\nmusic: false\ncover: false\navatar: false\njson: true\nstart_time: "{START_DATE}"\nend_time: "{END_DATE_EXCLUSIVE}"\ndownload_pinned: true\nhomepage_screenshot: false\nmode:\n  - post\nnumber:\n  post: 0\n  like: 0\n  mix: 0\n  allmix: 0\n  music: 0\nincrease:\n  post: false\nthread: 2\nretry_times: 2\nrate_limit: 1\nproxy: ""\ndatabase: false\nprogress:\n  quiet_logs: false\nbrowser_fallback:\n  enabled: false\ncookies: {{}}\n'''
    path.write_text(text, encoding="utf-8")


def walk_awemes(obj):
    if isinstance(obj, dict):
        if obj.get("aweme_id") and ("desc" in obj or "create_time" in obj):
            yield obj
        for v in obj.values():
            yield from walk_awemes(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk_awemes(v)


def safe_int(v):
    try:
        return int(v or 0)
    except Exception:
        return 0


def normalize_work(item: dict, case_id: str, input_link: str) -> dict:
    author = item.get("author") or {}
    music = item.get("music") or {}
    stats = item.get("statistics") or item.get("stats") or {}
    ts = safe_int(item.get("create_time"))
    dt = datetime.fromtimestamp(ts, TZ8) if ts else None
    aweme_id = str(item.get("aweme_id") or "")
    share = item.get("share_info") or {}
    share_url = share.get("share_url") or share.get("share_link_desc") or ""
    if not isinstance(share_url, str) or not share_url.startswith("http"):
        share_url = f"https://www.douyin.com/video/{aweme_id}" if aweme_id else ""
    return {
        "case_id": case_id,
        "input_profile_short_url": input_link,
        "aweme_id": aweme_id,
        "publish_time": dt.isoformat(timespec="seconds") if dt else "",
        "publish_date": dt.date().isoformat() if dt else "",
        "author_nickname": author.get("nickname") or "",
        "author_unique_id": author.get("unique_id") or "",
        "author_short_id": author.get("short_id") or "",
        "author_sec_uid": author.get("sec_uid") or "",
        "author_url": f"https://www.douyin.com/user/{author.get('sec_uid')}" if author.get("sec_uid") else "",
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


def main() -> int:
    repo_root = Path(__file__).resolve().parents[4]
    links_file = repo_root / "06_TESTS/MV/WEB_R3/core_profile_links_input.json"
    backend = repo_root / ".tmp_douyin_downloader"
    out_root = repo_root / "06_TESTS/MV/WEB_R3/_probe_output"
    out_root.mkdir(parents=True, exist_ok=True)

    links = json.loads(links_file.read_text(encoding="utf-8"))
    statuses = []
    all_works = []

    for idx, link in enumerate(links, 1):
        case_id = f"P{idx:02d}"
        case_root = out_root / case_id
        case_root.mkdir(parents=True, exist_ok=True)
        config = case_root / "config.yml"
        data_dir = case_root / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        write_config(config, link, data_dir)
        log_path = case_root / "run.log"
        cmd = [sys.executable, "run.py", "-c", str(config), "-v", "--show-warnings"]
        with log_path.open("w", encoding="utf-8") as log:
            p = subprocess.run(cmd, cwd=backend, stdout=log, stderr=subprocess.STDOUT, text=True)
        statuses.append({"case_id": case_id, "input_link": link, "returncode": p.returncode})

        seen = set()
        for fp in data_dir.rglob("*.json"):
            try:
                obj = json.loads(fp.read_text(encoding="utf-8"))
            except Exception:
                continue
            for item in walk_awemes(obj):
                aweme_id = str(item.get("aweme_id") or "")
                if not aweme_id or aweme_id in seen:
                    continue
                seen.add(aweme_id)
                row = normalize_work(item, case_id, link)
                if row["publish_date"] and START_DATE <= row["publish_date"] <= "2026-08-24":
                    all_works.append(row)

    fieldnames = [
        "case_id","input_profile_short_url","aweme_id","publish_time","publish_date",
        "author_nickname","author_unique_id","author_short_id","author_sec_uid","author_url",
        "desc","music_id","music_title","music_author","digg_count","comment_count",
        "share_count","collect_count","play_count","work_url","aweme_type"
    ]
    csv_path = out_root / "core_15d_works.csv"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(sorted(all_works, key=lambda r: r["publish_time"], reverse=True))

    (out_root / "core_15d_works.json").write_text(
        json.dumps(all_works, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "probe_status.json").write_text(
        json.dumps(statuses, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Compact profile resolution from harvested works.
    profile_rows = []
    for idx, link in enumerate(links, 1):
        case_id = f"P{idx:02d}"
        rows = [r for r in all_works if r["case_id"] == case_id]
        first = rows[0] if rows else {}
        profile_rows.append({
            "case_id": case_id,
            "input_link": link,
            "author_nickname": first.get("author_nickname", ""),
            "author_unique_id": first.get("author_unique_id", ""),
            "author_sec_uid": first.get("author_sec_uid", ""),
            "author_url": first.get("author_url", ""),
            "works_15d": len(rows),
        })
    with (out_root / "profile_resolution.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(profile_rows[0].keys()))
        w.writeheader(); w.writerows(profile_rows)

    print(json.dumps({"profiles": len(links), "works_15d": len(all_works), "output": str(out_root)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
