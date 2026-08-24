#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import urlparse, parse_qs

from playwright.async_api import async_playwright

TZ8 = timezone(timedelta(hours=8))
WINDOW_START = datetime(2026, 8, 10, 0, 0, 0, tzinfo=TZ8)
TARGETS = {
    'P04': 'MS4wLjABAAAA_TyjlQm1QDz9oQlS4x7f3MzHvuL-V9IYMQ2Qsc2xWg4',
    'P07': 'MS4wLjABAAAAtxmz8hjhGyax79DGnNe5KojkphdWs1GOojeMcq3H-y4',
    'P09': 'MS4wLjABAAAAa35gEPqHzLItRgy6Jf4T59m0Si3tx7YP2MV5G0TuOwmxxoFVK8M3pBpWZuKH8gfV',
}
VIDEO_RE = re.compile(r'/video/(\d{16,22})')


def aweme_dt(aweme_id: str) -> datetime | None:
    try:
        ts = int(aweme_id) >> 32
        return datetime.fromtimestamp(ts, TZ8)
    except Exception:
        return None


def aweme_time(aweme_id: str) -> str:
    dt = aweme_dt(aweme_id)
    return dt.isoformat(timespec='seconds') if dt else ''


def summarize_payload(url: str, payload: dict) -> dict:
    items = payload.get('aweme_list') or []
    if not isinstance(items, list):
        items = []
    ids = [str(x.get('aweme_id')) for x in items if isinstance(x, dict) and x.get('aweme_id')]
    q = parse_qs(urlparse(url).query)
    return {
        'request_max_cursor': (q.get('max_cursor') or [''])[0],
        'request_count': (q.get('count') or [''])[0],
        'status_code': payload.get('status_code'),
        'status_msg': payload.get('status_msg'),
        'has_more': payload.get('has_more'),
        'response_max_cursor': str(payload.get('max_cursor') or ''),
        'items': len(items),
        'ids': ids,
        'times': [aweme_time(x) for x in ids],
    }


async def main_async() -> int:
    root = Path(__file__).resolve().parents[4]
    out = root / '06_TESTS/MV/WEB_R3/_browser_session_fallback'
    out.mkdir(parents=True, exist_ok=True)
    report = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled'],
        )
        for case_id, sec_uid in TARGETS.items():
            context = await browser.new_context(
                viewport={'width': 1440, 'height': 1000},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
                locale='zh-CN',
            )
            page = await context.new_page()
            post_responses: list[dict] = []
            capture_tasks: list[asyncio.Task] = []

            async def capture_response(resp):
                if '/aweme/v1/web/aweme/post/' not in resp.url:
                    return
                rec = {'url': resp.url, 'http_status': resp.status}
                try:
                    payload = await resp.json()
                    if isinstance(payload, dict):
                        rec.update(summarize_payload(resp.url, payload))
                        rec['aweme_list'] = payload.get('aweme_list') or []
                    else:
                        rec['json_error'] = f'non-dict payload: {type(payload).__name__}'
                except Exception as exc:
                    rec['json_error'] = str(exc)[:500]
                post_responses.append(rec)

            def on_response(resp):
                if '/aweme/v1/web/aweme/post/' in resp.url:
                    capture_tasks.append(asyncio.create_task(capture_response(resp)))

            page.on('response', on_response)
            rec = {
                'case_id': case_id,
                'sec_uid': sec_uid,
                'page_url': '',
                'dom_ids': [],
                'dom_times': [],
                'post_response_count': 0,
                'post_response_summaries': [],
                'captured_ids': [],
                'captured_times': [],
                'newest_captured': '',
                'oldest_captured': '',
                'freshness_age_hours': None,
                'freshness_72h': False,
                'complete_15d': False,
                'complete_reason': '',
            }
            try:
                await page.goto(
                    f'https://www.douyin.com/user/{sec_uid}',
                    wait_until='domcontentloaded',
                    timeout=60000,
                )
                await page.wait_for_timeout(6000)

                found = set()
                for scroll_round in range(18):
                    hrefs = await page.locator('a[href]').evaluate_all(
                        "els => els.map(e => e.getAttribute('href'))"
                    )
                    for href in hrefs:
                        if not href:
                            continue
                        m = VIDEO_RE.search(href)
                        if m:
                            found.add(m.group(1))

                    # Scroll the real page to trigger signed cursor requests.
                    await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                    await page.wait_for_timeout(1600)

                    # If captured network data already crosses the target window, stop early.
                    all_ids = set()
                    for pr in post_responses:
                        all_ids.update(pr.get('ids') or [])
                    dts = [aweme_dt(x) for x in all_ids]
                    dts = [x for x in dts if x]
                    if dts and min(dts) < WINDOW_START:
                        break

                if capture_tasks:
                    await asyncio.gather(*capture_tasks, return_exceptions=True)

                # One final DOM pass after scrolling.
                hrefs = await page.locator('a[href]').evaluate_all(
                    "els => els.map(e => e.getAttribute('href'))"
                )
                for href in hrefs:
                    if not href:
                        continue
                    m = VIDEO_RE.search(href)
                    if m:
                        found.add(m.group(1))

                ids = sorted(found, key=int, reverse=True)
                rec['page_url'] = page.url
                rec['dom_ids'] = ids
                rec['dom_times'] = [aweme_time(x) for x in ids]

                captured: dict[str, dict] = {}
                summaries = []
                for pr in post_responses:
                    summaries.append({k: v for k, v in pr.items() if k != 'aweme_list' and k != 'url'})
                    for item in pr.get('aweme_list') or []:
                        if not isinstance(item, dict):
                            continue
                        aid = str(item.get('aweme_id') or '')
                        if aid:
                            captured[aid] = item

                captured_ids = sorted(captured, key=int, reverse=True)
                captured_dts = [aweme_dt(x) for x in captured_ids]
                captured_dts = [x for x in captured_dts if x]
                rec['post_response_count'] = len(post_responses)
                rec['post_response_summaries'] = summaries
                rec['captured_ids'] = captured_ids
                rec['captured_times'] = [aweme_time(x) for x in captured_ids]
                if captured_dts:
                    newest = max(captured_dts)
                    oldest = min(captured_dts)
                    now = datetime.now(TZ8)
                    age_h = (now - newest).total_seconds() / 3600
                    rec['newest_captured'] = newest.isoformat(timespec='seconds')
                    rec['oldest_captured'] = oldest.isoformat(timespec='seconds')
                    rec['freshness_age_hours'] = round(age_h, 2)
                    rec['freshness_72h'] = age_h <= 72
                    if oldest < WINDOW_START:
                        rec['complete_15d'] = True
                        rec['complete_reason'] = 'CAPTURED_OLDER_THAN_WINDOW_START'

                # If the last successfully parsed signed response says no more, that also closes history.
                good = [x for x in post_responses if 'has_more' in x]
                if good and good[-1].get('has_more') in (0, False):
                    rec['complete_15d'] = True
                    rec['complete_reason'] = 'SIGNED_RESPONSE_HAS_MORE_FALSE'

                # Persist captured raw work JSON separately for ingestion experiments.
                (out / f'{case_id}_captured_aweme.json').write_text(
                    json.dumps(list(captured.values()), ensure_ascii=False, indent=2),
                    encoding='utf-8',
                )
            except Exception as exc:
                rec['error'] = str(exc)[:1000]
            finally:
                await context.close()
            report.append(rec)
        await browser.close()

    (out / 'report.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8'
    )
    compact = [
        {
            k: r.get(k)
            for k in (
                'case_id', 'post_response_count', 'captured_ids', 'newest_captured',
                'oldest_captured', 'freshness_age_hours', 'freshness_72h',
                'complete_15d', 'complete_reason', 'error'
            )
        }
        for r in report
    ]
    print(json.dumps(compact, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(asyncio.run(main_async()))
