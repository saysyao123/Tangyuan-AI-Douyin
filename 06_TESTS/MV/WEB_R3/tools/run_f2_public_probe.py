#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import json
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path

from f2.apps.douyin.handler import DouyinHandler

TZ8 = timezone(timedelta(hours=8))
TARGETS = {
    'P04': 'MS4wLjABAAAA_TyjlQm1QDz9oQlS4x7f3MzHvuL-V9IYMQ2Qsc2xWg4',
    'P07': 'MS4wLjABAAAAtxmz8hjhGyax79DGnNe5KojkphdWs1GOojeMcq3H-y4',
    'P09': 'MS4wLjABAAAAa35gEPqHzLItRgy6Jf4T59m0Si3tx7YP2MV5G0TuOwmxxoFVK8M3pBpWZuKH8gfV',
}


def decode_aweme_time(aweme_id: str) -> str:
    try:
        ts = int(str(aweme_id)) >> 32
        return datetime.fromtimestamp(ts, TZ8).isoformat(timespec='seconds')
    except Exception:
        return ''


def listify(v):
    if v is None:
        return []
    if isinstance(v, list):
        return v
    if isinstance(v, tuple):
        return list(v)
    return [v]


async def main_async() -> int:
    root = Path(__file__).resolve().parents[4]
    out = root / '06_TESTS/MV/WEB_R3/_f2_public_probe'
    out.mkdir(parents=True, exist_ok=True)

    cookie = os.environ.get('DOUYIN_COOKIE', '')
    kwargs = {
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
            'Referer': 'https://www.douyin.com/',
        },
        'proxies': {'http://': None, 'https://': None},
        'timeout': 2,
        'cookie': cookie,
    }

    report = []
    for case_id, sec_uid in TARGETS.items():
        rec = {
            'case_id': case_id,
            'sec_uid': sec_uid,
            'cookie_supplied': bool(cookie),
            'pages': [],
            'all_ids': [],
            'newest': '',
            'oldest': '',
            'error': '',
        }
        all_ids = []
        try:
            handler = DouyinHandler(kwargs)
            page_index = 0
            async for page_data in handler.fetch_user_post_videos(
                sec_uid,
                min_cursor=0,
                max_cursor=0,
                page_counts=18,
                max_counts=54,
            ):
                page_index += 1
                raw = page_data._to_raw()
                ids = [str(x) for x in listify(getattr(page_data, 'aweme_id', [])) if x]
                all_ids.extend(ids)
                rec['pages'].append({
                    'page': page_index,
                    'ids': ids,
                    'times': [decode_aweme_time(x) for x in ids],
                    'has_more': getattr(page_data, 'has_more', None),
                    'max_cursor': str(getattr(page_data, 'max_cursor', '') or ''),
                    'raw_type': type(raw).__name__,
                })
                (out / f'{case_id}_page_{page_index}.json').write_text(
                    json.dumps(raw, ensure_ascii=False, indent=2, default=str),
                    encoding='utf-8',
                )
                if page_index >= 3:
                    break
        except Exception as exc:
            rec['error'] = f'{type(exc).__name__}: {exc}'[:1000]

        unique_ids = sorted(set(all_ids), key=int, reverse=True) if all_ids else []
        rec['all_ids'] = unique_ids
        times = [decode_aweme_time(x) for x in unique_ids]
        rec['all_times'] = times
        if times:
            rec['newest'] = max(times)
            rec['oldest'] = min(times)
        report.append(rec)

    (out / 'report.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8'
    )
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(asyncio.run(main_async()))
