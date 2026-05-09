#!/usr/bin/env python3
"""
New API Auto Checkin - Playwright + Chromium
Env: NEWAPI_URL, NEWAPI_COOKIE, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
"""
import os
import sys
import asyncio
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("ERROR: pip install playwright && playwright install chromium")
    sys.exit(1)


async def main():
    url = os.environ.get("NEWAPI_URL", "").rstrip("/")
    ck = os.environ.get("NEWAPI_COOKIE", "")

    if not url:
        print("ERROR: NEWAPI_URL not set")
        sys.exit(1)
    if not ck:
        print("ERROR: NEWAPI_COOKIE not set")
        sys.exit(1)

    print("New API Auto Checkin")
    print("Target: " + url)

    async with async_playwright() as p:
        br = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        ctx = await br.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )

        # Parse cookies
        from urllib.parse import urlparse
        domain = urlparse(url).hostname or "localhost"
        cookies = []
        for pair in ck.split(";"):
            pair = pair.strip()
            if "=" not in pair:
                continue
            name, _, value = pair.partition("=")
            cookies.append({
                "name": name.strip(),
                "value": value.strip(),
                "domain": domain,
                "path": "/",
            })

        if cookies:
            await ctx.add_cookies(cookies)
            print("Injected " + str(len(cookies)) + " cookies")
        else:
            print("WARNING: no cookies parsed, check NEWAPI_COOKIE format")

        page = await ctx.new_page()

        # Visit page
        target = url + "/"
        print("Visiting: " + target)
        try:
            await page.goto(target, timeout=30000, wait_until="networkidle")
        except Exception as e:
            print("ERROR: page load failed: " + str(e))
            await br.close()
            sys.exit(1)

        # Screenshot
        sd = Path("screenshots")
        sd.mkdir(exist_ok=True)
        await page.screenshot(path=str(sd / "01_homepage.png"))
        print("Screenshot: 01_homepage.png")

        # Check login
        pwd = await page.query_selector("input[type='password']")
        if pwd:
            print("ERROR: not logged in, cookie may be expired")
            await page.screenshot(path=str(sd / "ERROR_not_logged_in.png"))
            await br.close()
            sys.exit(1)

        print("Login confirmed OK")

        # Find and click checkin button
        print("Looking for checkin button...")
        texts = ["签到", "打卡", "Check in", "Check-in", "每日签到", "Sign in"]
        clicked = False
        for txt in texts:
            try:
                btn = await page.query_selector("text=" + txt)
                if btn:
                    print("Found button: " + txt)
                    await btn.click()
                    clicked = True
                    print("Clicked!")
                    await asyncio.sleep(3)
                    await page.screenshot(path=str(sd / "02_after_click.png"))
                    break
            except Exception:
                continue

        if not clicked:
            print("WARNING: checkin button not found, check README for help")
            btns = await page.query_selector_all("button, a[href], [role='button']")
            print("Clickable elements (first 15):")
            for i, b in enumerate(btns[:15]):
                try:
                    t = await b.inner_text()
                    if t.strip():
                        print("  #" + str(i) + ": " + t.strip()[:30])
                except Exception:
                    pass
            await page.screenshot(path=str(sd / "02_no_button.png"))

        # Final screenshot
        await asyncio.sleep(2)
        await page.screenshot(path=str(sd / "03_result.png"))

        title = await page.title()
        print("Page title: " + title)
        print("Done!")

        await br.close()

        # Telegram (optional)
        ttoken = os.environ.get("TELEGRAM_TOKEN", "")
        tchat = os.environ.get("TELEGRAM_CHAT_ID", "")
        if ttoken and tchat:
            try:
                import urllib.request
                import urllib.parse
                tmsg = "New API Checkin Completed\nURL: " + url
                turl = (
                    "https://api.telegram.org/bot" + ttoken + "/sendMessage"
                    "?chat_id=" + tchat +
                    "&text=" + urllib.parse.quote(tmsg)
                )
                urllib.request.urlopen(turl, timeout=10)
                print("Telegram notification sent")
            except Exception as e:
                print("Telegram failed: " + str(e))

        # GitHub Actions output
        out = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with open(out, "a") as f:
            f.write("checkin_result=completed\n")


if __name__ == "__main__":
    asyncio.run(main())
