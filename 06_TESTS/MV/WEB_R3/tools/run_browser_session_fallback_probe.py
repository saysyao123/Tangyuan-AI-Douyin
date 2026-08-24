#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import urlencode

import requests
from playwright.async_api import async_playwright

TZ8 = timezone(timedelta(hours=8))
TARGETS = {
    'P04': 'MS4wLjABAAAA_TyjlQm1QDz9oQlS4x7f3MzHvuL-V9IYMQ2Qsc2xWg4',
    'P07': 'MS4wLjABAAAAtxmz8hjhGyax79DGnNe5KojkphdWs1GOojeMcq3H-y4',
    'P09': 'MS4wLjABAAAAa35gEPqHzLItRgy6Jf4T59m0Si3tx7YP2MV5G0TuOwmxxoFVK8M3pBpWZuKH8gfV',
}
VIDEO_RE = re.compile(r'/video/(\d{16,22})')


def aweme_time(aweme_id: str) -> str:
    try:
        ts = int(aweme_id) >> 32
        return datetime.fromtimestamp(ts, TZ8).isoformat(timespec='seconds')
    except Exception:
        return ''


def direct_post_request(sec_uid: str, cookies: list[dict], max_cursor: str = '0') -> dict:
    cookie_header = '; '.join(f"{c['name']}={c['value']}" for c in cookies if c.get('name') and c.get('value'))
    params = {
        'device_platform':'webapp','aid':'6383','channel':'channel_pc_web',
        'sec_user_id':sec_uid,'max_cursor':max_cursor,'count':'18',
        'publish_video_strategy_type':'2','pc_client_type':'1','version_code':'170400','version_name':'17.4.0',
        'cookie_enabled':'true','screen_width':'1920','screen_height':'1080','browser_language':'zh-CN',
        'browser_platform':'Win32','browser_name':'Chrome','browser_version':'139.0.0.0','browser_online':'true',
        'engine_name':'Blink','engine_version':'139.0.0.0','os_name':'Windows','os_version':'10','cpu_core_num':'16',
        'device_memory':'8','platform':'PC','downlink':'10','effective_type':'4g','round_trip_time':'50',
    }
    url = 'https://www.douyin.com/aweme/v1/web/aweme/post/?' + urlencode(params)
    s = requests.Session()
    r = s.get(url, headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        'Accept':'application/json, text/plain, */*',
        'Referer':f'https://www.douyin.com/user/{sec_uid}',
        'Cookie':cookie_header,
    }, timeout=40)
    rec = {'http_status':r.status_code,'url':r.url,'body_prefix':r.text[:500]}
    try:
        data = r.json()
        items = data.get('aweme_list') or []
        rec.update({
            'status_code':data.get('status_code'),
            'status_msg':data.get('status_msg'),
            'items':len(items) if isinstance(items,list) else 0,
            'has_more':data.get('has_more'),
            'max_cursor':str(data.get('max_cursor') or ''),
            'ids':[str(x.get('aweme_id')) for x in items if isinstance(x,dict) and x.get('aweme_id')],
        })
    except Exception as exc:
        rec['json_error']=str(exc)
    return rec


async def main_async() -> int:
    root = Path(__file__).resolve().parents[4]
    out = root / '06_TESTS/MV/WEB_R3/_browser_session_fallback'
    out.mkdir(parents=True, exist_ok=True)
    report=[]
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--disable-blink-features=AutomationControlled'])
        for case_id, sec_uid in TARGETS.items():
            context = await browser.new_context(
                viewport={'width':1440,'height':1000},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
                locale='zh-CN',
            )
            page = await context.new_page()
            network=[]
            page.on('response', lambda resp: network.append(resp.url) if ('aweme' in resp.url or '/post/' in resp.url or 'user' in resp.url) else None)
            rec={'case_id':case_id,'sec_uid':sec_uid,'page_url':'','dom_ids':[],'dom_times':[],'network_urls':[]}
            try:
                await page.goto(f'https://www.douyin.com/user/{sec_uid}', wait_until='domcontentloaded', timeout=60000)
                await page.wait_for_timeout(5000)
                found=set()
                for _ in range(8):
                    hrefs = await page.locator('a[href]').evaluate_all("els => els.map(e => e.getAttribute('href'))")
                    for href in hrefs:
                        if not href: continue
                        m=VIDEO_RE.search(href)
                        if m: found.add(m.group(1))
                    await page.mouse.wheel(0, 1800)
                    await page.wait_for_timeout(1200)
                ids=sorted(found, key=int, reverse=True)
                rec['page_url']=page.url
                rec['dom_ids']=ids
                rec['dom_times']=[aweme_time(x) for x in ids]
                rec['network_urls']=network[-100:]
                cookies=await context.cookies()
                rec['cookie_names']=sorted({c['name'] for c in cookies})
                first=direct_post_request(sec_uid,cookies,'0')
                rec['direct_page1']=first
                if first.get('max_cursor'):
                    rec['direct_page2']=direct_post_request(sec_uid,cookies,first['max_cursor'])
            except Exception as exc:
                rec['error']=str(exc)[:1000]
            finally:
                await context.close()
            report.append(rec)
        await browser.close()
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps([{k:v for k,v in r.items() if k in ('case_id','dom_ids','dom_times','cookie_names','direct_page1','direct_page2','error')} for r in report],ensure_ascii=False))
    return 0

if __name__=='__main__':
    raise SystemExit(asyncio.run(main_async()))
