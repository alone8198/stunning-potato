#!/usr/bin/env python3
"""
New API Auto Checkin - Multi-site batch checkin
Supports one URL per line, username/password aligned by line number.

Env vars:
  NEWAPI_URLS        URLs, one per line
  NEWAPI_USERNAMES   Usernames, one per line (aligned with URLs)
  NEWAPI_PASSWORDS   Passwords, one per line (aligned with URLs)
  TELEGRAM_TOKEN     Telegram Bot Token (optional)
  TELEGRAM_CHAT_ID  Telegram Chat ID (optional)
"""

import os
import sys
import asyncio
import subprocess
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("ERROR: pip install playwright && playwright install chromium")
    sys.exit(1)

# Optional dependencies
HAS_OCR = False
HAS_CV = False

try:
    import pytesseract
    from PIL import Image
    HAS_OCR = True
except ImportError:
    pass

try:
    import cv2
    HAS_CV = True
except ImportError:
    pass


def ocr_find_text(image_path, targets):
    if not HAS_OCR:
        return []
    try:
        img = Image.open(image_path)
        data = pytesseract.image_to_data(
            img, lang="chi_sim+eng", output_type=pytesseract.Output.DICT
        )
    except Exception as e:
        print("  [OCR] Failed: " + str(e))
        return []

    results = []
    n = len(data["text"])
    for i in range(n):
        text = data["text"][i].strip()
        if not text:
            continue
        for t in targets:
            if t in text:
                x = data["left"][i]
                y = data["top"][i]
                w = data["width"][i]
                h = data["height"][i]
                results.append((x, y, w, h, text))
                break
    return results


def parse_lines(env_name):
    val = os.environ.get(env_name, "")
    lines = []
    for line in val.splitlines():
        line = line.strip()
        if line:
            lines.append(line)
    return lines


async def checkin_one(page, url, username, password, idx):
    prefix = "[#" + str(idx) + "] "
    print("\n" + "=" * 50)
    print(prefix + "URL: " + url)
    print("=" * 50)

    if not username or not password:
        print(prefix + "[ERROR] Username or password is empty, skipping")
        return False

    # Login with username and password
    login_url = url.rstrip("/") + "/login"
    print(prefix + "[Login] Opening: " + login_url)
    await page.goto(login_url, timeout=30000, wait_until="networkidle")
    await asyncio.sleep(2)

    sd = Path("screenshots")
    await page.screenshot(path=str(sd / ("login_" + str(idx) + ".png")))

    try:
        await page.fill("input[name='username'], input[placeholder*='user'], input[type='text']:visible", username, timeout=5000)
        await page.fill("input[name='password'], input[placeholder*='pass'], input[type='password']:visible", password, timeout=5000)
        print(prefix + "[Login] Form filled")
    except Exception as e:
        print(prefix + "[ERROR] Fill form failed: " + str(e))
        return False

    await asyncio.sleep(1)
    await page.screenshot(path=str(sd / ("login_filled_" + str(idx) + ".png")))

    # Click login button: OCR -> DOM
    clicked = False
    if HAS_OCR:
        await page.screenshot(path="temp_login.png")
        matches = ocr_find_text("temp_login.png", ["Login", "Sign in", "Sign in", "Login"])
        if matches:
            x, y, w, h, _ = matches[0]
            await page.mouse.click(x + w // 2, y + h // 2)
            clicked = True
            print(prefix + "[Login] [OCR] Clicked login button")

    if not clicked:
        for sel in ["button[type='submit']", "button:has-text('Login')", "button:has-text('Sign in')", "input[type='submit']"]:
            try:
                btn = await page.query_selector(sel)
                if btn:
                    await btn.click()
                    clicked = True
                    print(prefix + "[Login] [DOM] Clicked: " + sel)
                    break
            except Exception:
                continue

    if not clicked:
        print(prefix + "[ERROR] Cannot find login button")
        return False

    await asyncio.sleep(3)
    await page.screenshot(path=str(sd / ("after_login_" + str(idx) + ".png")))

    # Go to personal page
    personal_url = url.rstrip("/") + "/console/personal"
    print(prefix + "[Checkin] Going to: " + personal_url)
    await page.goto(personal_url, timeout=30000, wait_until="networkidle")
    await asyncio.sleep(2)

    sd = Path("screenshots")
    sd.mkdir(exist_ok=True)
    await page.screenshot(path=str(sd / ("personal_" + str(idx) + ".png")))

    # Check login status
    pwd_input = await page.query_selector("input[type='password']")
    if pwd_input:
        print(prefix + "[ERROR] Not logged in! Login failed.")
        await page.screenshot(path=str(sd / ("error_not_logged_in_" + str(idx) + ".png")))
        return False

    print(prefix + "[OK] Login confirmed")

    # Find and click checkin button
    await page.screenshot(path="temp_personal.png")

    checkin_texts = ["Sign in", "Check in", "Check-in", "Daily sign in", "Sign in"]
    clicked = False

    if HAS_OCR:
        matches = ocr_find_text("temp_personal.png", checkin_texts)
        seen_y = set()
        unique = []
        for (x, y, w, h, t) in matches:
            y_key = y // 20
            if y_key not in seen_y:
                seen_y.add(y_key)
                unique.append((x, y, w, h, t))
        if unique:
            x, y, w, h, t = unique[0]
            await page.mouse.click(x + w // 2, y + h // 2)
            clicked = True
            print(prefix + "[Checkin] [OCR] Clicked [" + t + "]")

    if not clicked and HAS_CV:
        tpl_dir = Path("templates")
        if tpl_dir.exists():
            for tpl_file in tpl_dir.glob("*.png"):
                try:
                    import numpy as np
                    img = cv2.imread("temp_personal.png")
                    tpl = cv2.imread(str(tpl_file))
                    result = cv2.matchTemplate(img, tpl, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, max_loc = cv2.minMaxLoc(result)
                    if max_val > 0.8:
                        h, w = tpl.shape[:2]
                        await page.mouse.click(max_loc[0] + w // 2, max_loc[1] + h // 2)
                        clicked = True
                        print(prefix + "[Checkin] [CV] Template matched: " + tpl_file.name)
                        break
                except Exception:
                    continue

    if not clicked:
        print(prefix + "[Checkin] OCR/CV failed, falling back to DOM")
        for txt in checkin_texts:
            try:
                btn = await page.query_selector("text=" + txt)
                if btn:
                    await btn.click()
                    clicked = True
                    print(prefix + "[Checkin] [DOM] Clicked: " + txt)
                    break
            except Exception:
                continue

    if clicked:
        print(prefix + "[OK] Checkin successful!")
        await asyncio.sleep(3)
        await page.screenshot(path=str(sd / ("result_" + str(idx) + ".png")))
        return True
    else:
        print(prefix + "[WARN] Checkin button not found")
        await page.screenshot(path=str(sd / ("no_button_" + str(idx) + ".png")))
        return False


async def main():
    urls = parse_lines("NEWAPI_URLS")
    usernames = parse_lines("NEWAPI_USERNAMES")
    passwords = parse_lines("NEWAPI_PASSWORDS")

    total = len(urls)
    if total == 0:
        print("[ERROR] NEWAPI_URLS not set (one URL per line)")
        sys.exit(1)

    # Align lists to same length
    def align(lst, n):
        while len(lst) < n:
            lst.append("")
        return lst

    usernames = align(usernames, total)
    passwords = align(passwords, total)

    print("=" * 60)
    print("  New API Batch Auto Checkin (OCR + OpenCV)")
    print("  Total accounts: " + str(total))
    print("  OCR: " + ("Available" if HAS_OCR else "Unavailable (DOM fallback)"))
    print("  OpenCV: " + ("Available" if HAS_CV else "Unavailable"))
    print("=" * 60)

    results = []

    async with async_playwright() as p:
        br = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )

        for i in range(total):
            ctx = await br.new_context(
                viewport={"width": 1280, "height": 800},
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
            )
            page = await ctx.new_page()
            Path("screenshots").mkdir(exist_ok=True)

            ok = await checkin_one(page, urls[i], usernames[i], passwords[i], i + 1)
            results.append((i + 1, urls[i], ok))

            await ctx.close()

        await br.close()

    # Summary
    print("\n" + "=" * 60)
    print("  Checkin Summary")
    print("=" * 60)
    success = 0
    for idx, url, ok in results:
        status = "SUCCESS" if ok else "FAILED"
        print("  #" + str(idx) + " " + url + " -> " + status)
        if ok:
            success += 1
    print("\n  Total: " + str(success) + "/" + str(total) + " success")
    print("=" * 60)

    # Telegram notification
    ttoken = os.environ.get("TELEGRAM_TOKEN", "")
    tchat = os.environ.get("TELEGRAM_CHAT_ID", "")
    if ttoken and tchat:
        try:
            import urllib.request
            import urllib.parse
            lines = ["New API Batch Checkin (" + str(success) + "/" + str(total) + ")"]
            for idx, url, ok in results:
                lines.append("  #" + str(idx) + " " + ("OK" if ok else "FAIL") + " " + url)
            tmsg = "\n".join(lines)
            turl = (
                "https://api.telegram.org/bot" + ttoken + "/sendMessage"
                "?chat_id=" + tchat +
                "&text=" + urllib.parse.quote(tmsg)
            )
            urllib.request.urlopen(turl, timeout=10)
            print("[Notify] Telegram sent")
        except Exception as e:
            print("[Notify] Telegram failed: " + str(e))

    # GitHub Actions output
    out = os.environ.get("GITHUB_OUTPUT", "/dev/null")
    try:
        with open(out, "a") as f:
            f.write("checkin_result=" + str(success) + "/" + str(total) + "\n")
    except Exception:
        pass


if __name__ == "__main__":
    subprocess.run(["mkdir", "-p", "screenshots"], check=False)
    asyncio.run(main())
