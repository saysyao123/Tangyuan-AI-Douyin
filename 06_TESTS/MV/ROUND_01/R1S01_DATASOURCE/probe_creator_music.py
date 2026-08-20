from __future__ import annotations

import argparse
import asyncio
import json
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from playwright.async_api import async_playwright

CREATOR_UPLOAD_URL = "https://creator.douyin.com/creator-micro/content/upload?default-tab=3"

MUSIC_OPEN_SELECTORS = (
    "span.action-Q1y01k",
    ".container-right-uW7Pj",
    ".container-JngpiB",
)
MUSIC_OPEN_TEXTS = ("选择音乐", "添加音乐")
MUSIC_PANEL_SELECTOR = ".semi-portal"
MUSIC_PANEL_MARKERS = ("选择音乐", "热门榜")


def _safe_json(value: Any) -> str:
    try:
        return json.dumps(value, ensure_ascii=False)
    except Exception:
        return "{}"


def _strip_query(url: str) -> str:
    """Keep endpoint identity but never persist query tokens from Creator Center requests."""
    try:
        parts = urlsplit(url)
        return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))
    except Exception:
        return ""


async def _wait_for_user_login(page, timeout_s: int) -> None:
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        text = await page.locator("body").inner_text(timeout=5000)
        if "选择音乐" in text or "添加音乐" in text or "发布视频" in text or "发布作品" in text:
            return
        print("[WAIT] 请在打开的浏览器中完成抖音创作者中心登录；检测到发布页后会自动继续。")
        await asyncio.sleep(2)
    raise TimeoutError("等待抖音创作者中心登录超时")


async def _open_music_panel(page) -> None:
    for selector in MUSIC_OPEN_SELECTORS:
        loc = page.locator(selector)
        if await loc.count():
            try:
                await loc.first.click(timeout=3000)
                break
            except Exception:
                pass
    else:
        clicked = await page.evaluate(
            """
            (texts) => {
              const nodes = Array.from(document.querySelectorAll('button,[role="button"],span,div'));
              const target = nodes.find(el => texts.includes((el.innerText || '').trim()));
              if (!target) return false;
              target.click();
              return true;
            }
            """,
            list(MUSIC_OPEN_TEXTS),
        )
        if not clicked:
            raise RuntimeError("未找到“选择音乐/添加音乐”入口")

    await page.wait_for_function(
        """
        ({selector, markers}) => Array.from(document.querySelectorAll(selector)).some(el => {
          const text = el.innerText || '';
          return markers.every(m => text.includes(m));
        })
        """,
        arg={"selector": MUSIC_PANEL_SELECTOR, "markers": list(MUSIC_PANEL_MARKERS)},
        timeout=20000,
    )


async def _scrape_panel(page, topn: int) -> dict[str, Any]:
    return await page.evaluate(
        """
        ({selector, markers, topn}) => {
          const portal = Array.from(document.querySelectorAll(selector)).find(el => {
            const text = el.innerText || '';
            return markers.every(m => text.includes(m));
          });
          if (!portal) return {success:false, reason:'no-panel'};

          const text = portal.innerText || '';
          const buttons = Array.from(portal.querySelectorAll('button'));
          const useButtons = buttons.filter(btn => (btn.innerText || '').trim() === '使用');
          const rows = [];
          const seen = new Set();

          for (const btn of useButtons) {
            let row = btn;
            for (let i = 0; i < 8 && row; i++) {
              const t = (row.innerText || '').trim();
              const useCount = row.querySelectorAll ? Array.from(row.querySelectorAll('button')).filter(b => (b.innerText || '').trim() === '使用').length : 0;
              if (t && useCount === 1 && t.length < 500) break;
              row = row.parentElement;
            }
            if (!row) continue;
            const rowText = (row.innerText || '').trim();
            if (!rowText || seen.has(rowText)) continue;
            seen.add(rowText);
            const links = Array.from(row.querySelectorAll('a[href]')).map(a => a.href).filter(Boolean);
            const audios = Array.from(row.querySelectorAll('audio')).map(a => a.currentSrc || a.src).filter(Boolean);
            const data = {};
            for (const el of [row, ...Array.from(row.querySelectorAll('*'))]) {
              for (const attr of Array.from(el.attributes || [])) {
                const name = attr.name || '';
                if (/music|song|audio|item|id/i.test(name)) data[name] = attr.value;
              }
            }
            const lines = rowText.split('\n').map(x => x.trim()).filter(Boolean).filter(x => x !== '使用');
            rows.push({
              lines,
              text: rowText,
              links,
              audio_src: audios,
              data_attrs: data,
              html: row.outerHTML.slice(0, 12000),
            });
            if (rows.length >= topn) break;
          }
          return {
            success:true,
            rows,
            panel_text: text.slice(0, 20000),
            use_button_count: useButtons.length,
          };
        }
        """,
        {"selector": MUSIC_PANEL_SELECTOR, "markers": list(MUSIC_PANEL_MARKERS), "topn": topn},
    )


async def main() -> None:
    parser = argparse.ArgumentParser(description="R1S01: probe Douyin Creator Center hot-music panel")
    parser.add_argument("--out", default="./r1s01_probe_output", help="output directory (private local evidence; do not commit)")
    parser.add_argument("--profile", default="./.douyin_creator_profile", help="persistent browser profile directory (private; do not commit)")
    parser.add_argument("--topn", type=int, default=30, help="max music rows to capture")
    parser.add_argument("--login-timeout", type=int, default=300, help="seconds to wait for first login")
    args = parser.parse_args()

    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    profile = Path(args.profile).resolve()
    profile.mkdir(parents=True, exist_ok=True)

    network_rows: list[dict[str, Any]] = []

    async with async_playwright() as pw:
        context = await pw.chromium.launch_persistent_context(
            str(profile),
            headless=False,
            locale="zh-CN",
            viewport={"width": 1600, "height": 950},
        )
        page = context.pages[0] if context.pages else await context.new_page()

        async def on_response(response):
            url = response.url or ""
            low = url.lower()
            if not any(k in low for k in ("music", "song", "billboard", "hot")):
                return
            try:
                ctype = (response.headers or {}).get("content-type", "")
                if "json" not in ctype.lower():
                    return
                data = await response.json()
                payload = _safe_json(data)
                if len(payload) > 500000:
                    payload = payload[:500000]
                network_rows.append({
                    "endpoint": _strip_query(url),
                    "status": response.status,
                    "data": json.loads(payload) if payload.endswith(("}", "]")) else payload,
                })
            except Exception:
                return

        page.on("response", on_response)
        print(f"[OPEN] {CREATOR_UPLOAD_URL}")
        await page.goto(CREATOR_UPLOAD_URL, wait_until="domcontentloaded", timeout=60000)
        await _wait_for_user_login(page, args.login_timeout)
        await _open_music_panel(page)
        await asyncio.sleep(3)

        result = await _scrape_panel(page, max(1, args.topn))
        (out / "creator_music_panel.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        await page.screenshot(path=str(out / "creator_music_panel.png"), full_page=False)
        (out / "creator_music_network.json").write_text(json.dumps(network_rows, ensure_ascii=False, indent=2), encoding="utf-8")

        summary = {
            "success": bool(result.get("success")),
            "captured_rows": len(result.get("rows") or []),
            "use_button_count": result.get("use_button_count", 0),
            "network_music_responses": len(network_rows),
            "output_dir": str(out),
            "privacy_note": "Output is local test evidence and is gitignored; do not commit browser profile or raw probe output.",
        }
        (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        print("[DONE] 请把 summary.json、creator_music_panel.json、creator_music_network.json 和截图发到当前 ChatGPT 对话，不要提交到公开 GitHub。")
        await context.close()


if __name__ == "__main__":
    asyncio.run(main())
