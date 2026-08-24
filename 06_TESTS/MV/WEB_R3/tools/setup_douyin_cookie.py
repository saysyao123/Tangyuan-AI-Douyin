#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import os
from pathlib import Path

from playwright.async_api import async_playwright


def secret_path() -> Path:
    return Path(__file__).resolve().parents[1] / ".secrets" / "douyin_cookie.txt"


def build_cookie_header(cookies: list[dict]) -> str:
    pairs: list[str] = []
    seen: set[str] = set()
    for item in cookies:
        name = str(item.get("name") or "").strip()
        value = str(item.get("value") or "")
        domain = str(item.get("domain") or "")
        if not name or not value:
            continue
        if "douyin.com" not in domain and "iesdouyin.com" not in domain:
            continue
        if name in seen:
            continue
        seen.add(name)
        pairs.append(f"{name}={value}")
    return "; ".join(pairs)


async def capture(force: bool) -> int:
    target = secret_path()
    if target.exists() and target.stat().st_size > 20 and not force:
        print(f"[OK] Existing local Douyin session found: {target}")
        print("Use --force only when the authenticated collector says the session expired.")
        return 0

    target.parent.mkdir(parents=True, exist_ok=True)
    print("A Chromium window will open on Douyin.")
    print("Please log in with your normal Douyin account (QR scan is recommended).")
    print("After the web page clearly shows you are logged in, return to this terminal and press Enter.")
    print("The session value will be written only to the local .secrets directory and will NOT be printed.")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 1440, "height": 960},
            locale="zh-CN",
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
            ),
        )
        page = await context.new_page()
        try:
            await page.goto("https://www.douyin.com/", wait_until="domcontentloaded", timeout=90000)
        except Exception:
            # The user can still finish login if the page partially loads.
            pass

        await asyncio.to_thread(input, "\nLogin complete? Press Enter here to capture the local session... ")
        await page.wait_for_timeout(1500)
        cookies = await context.cookies()
        header = build_cookie_header(cookies)
        await browser.close()

    if len(header) < 20:
        print("[FAIL] No usable Douyin cookies were captured. Nothing was saved.")
        return 2

    tmp = target.with_suffix(".tmp")
    tmp.write_text(header, encoding="utf-8")
    try:
        if os.name != "nt":
            os.chmod(tmp, 0o600)
        tmp.replace(target)
    finally:
        if tmp.exists():
            tmp.unlink(missing_ok=True)

    print(f"[PASS] Local Douyin session captured: {target}")
    print("The Cookie value was intentionally not printed.")
    print("Next step: run the authenticated core-account collector.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="One-time local Douyin QR-login session bootstrap for R3.")
    parser.add_argument("--force", action="store_true", help="replace an existing local session")
    args = parser.parse_args()
    return asyncio.run(capture(args.force))


if __name__ == "__main__":
    raise SystemExit(main())
