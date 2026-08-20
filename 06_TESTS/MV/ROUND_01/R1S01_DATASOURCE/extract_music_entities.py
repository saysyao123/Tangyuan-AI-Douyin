from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ID_KEYS = ("music_id", "musicId", "id_str", "id")
TITLE_KEYS = ("title", "music_name", "name")
AUTHOR_KEYS = ("author_name", "author", "owner_nickname", "nickname")
URL_KEYS = ("share_url", "play_url", "play_url_lowbr", "audio_url")
COUNT_KEYS = ("use_count", "user_count", "used_count", "shoot_count")


def first_value(d: dict[str, Any], keys: tuple[str, ...]) -> Any:
    for key in keys:
        value = d.get(key)
        if value not in (None, "", [], {}):
            return value
    return None


def scalar_url(value: Any) -> str | None:
    if isinstance(value, str) and value.startswith("http"):
        return value
    if isinstance(value, dict):
        for key in ("url", "uri"):
            v = value.get(key)
            if isinstance(v, str) and v.startswith("http"):
                return v
        urls = value.get("url_list")
        if isinstance(urls, list):
            for v in urls:
                if isinstance(v, str) and v.startswith("http"):
                    return v
    if isinstance(value, list):
        for v in value:
            found = scalar_url(v)
            if found:
                return found
    return None


def walk(value: Any, source_url: str, out: list[dict[str, Any]]) -> None:
    if isinstance(value, dict):
        music_id = first_value(value, ID_KEYS)
        title = first_value(value, TITLE_KEYS)
        joined_keys = " ".join(value.keys()).lower()
        musicish = "music" in joined_keys or any(k in value for k in ("play_url", "audio_url", "use_count"))
        if musicish and (music_id or title):
            urls: dict[str, str] = {}
            for key in URL_KEYS:
                found = scalar_url(value.get(key))
                if found:
                    urls[key] = found
            out.append({
                "music_id": str(music_id) if music_id is not None else None,
                "title": str(title) if title is not None else None,
                "author": first_value(value, AUTHOR_KEYS),
                "use_count": first_value(value, COUNT_KEYS),
                "urls": urls,
                "source_url": source_url,
                "raw_keys": sorted(value.keys()),
            })
        for child in value.values():
            walk(child, source_url, out)
    elif isinstance(value, list):
        for child in value:
            walk(child, source_url, out)


def dedupe(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str, str]] = set()
    result = []
    for row in rows:
        key = (str(row.get("music_id") or ""), str(row.get("title") or ""), str(row.get("author") or ""))
        if key == ("", "", "") or key in seen:
            continue
        seen.add(key)
        result.append(row)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract candidate Douyin music entities from creator panel network dump")
    parser.add_argument("network_json")
    parser.add_argument("--out", default="music_entities.json")
    args = parser.parse_args()

    source = Path(args.network_json)
    payload = json.loads(source.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = []
    if isinstance(payload, list):
        for entry in payload:
            if not isinstance(entry, dict):
                continue
            walk(entry.get("data"), str(entry.get("url") or ""), rows)
    else:
        walk(payload, "", rows)

    rows = dedupe(rows)
    # Prefer rows that have a music_id, direct URLs, and usage signals.
    rows.sort(key=lambda r: (bool(r.get("music_id")), bool(r.get("urls")), r.get("use_count") is not None), reverse=True)
    out = Path(args.out)
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"entities": len(rows), "output": str(out.resolve())}, ensure_ascii=False, indent=2))
    for i, row in enumerate(rows[:20], 1):
        print(f"{i:02d}. music_id={row.get('music_id')} | {row.get('title')} | {row.get('author')} | use={row.get('use_count')}")


if __name__ == "__main__":
    main()
