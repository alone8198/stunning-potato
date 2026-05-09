#!/usr/bin/env python3
"""
New API Auto Checkin - Playwright + OCR + OpenCV
使用视觉识别（OCR文字识别 + OpenCV模板匹配）定位并点击按钮
支持账号密码登录和 Cookie 登录两种方式

环境变量：
  NEWAPI_URL            New API 地址（如 https://api.xxx.com）
  NEWAPI_USERNAME       账号（密码登录方式）
  NEWAPI_PASSWORD       密码（密码登录方式）
  NEWAPI_COOKIE         Cookie 字符串（Cookie 登录方式，优先）
  TELEGRAM_TOKEN       Telegram Bot Token（可选）
  TELEGRAM_CHAT_ID     Telegram Chat ID（可选）
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

# ── 可选依赖检测 ──────────────────────────────────────────
HAS_OCR = False
HAS_CV = False

try:
    import pytesseract
    from PIL import Image
    HAS_OCR = True
    print("[OK] pytesseract OCR 可用")
except ImportError:
    print("[WARN] pytesseract 未安装，OCR 功能不可用")

try:
    import cv2
    import numpy as np
    HAS_CV = True
    print("[OK] OpenCV 可用")
except ImportError:
    print("[WARN] opencv-python 未安装，模板匹配功能不可用")


# ── OCR 文字定位 ──────────────────────────────────────────
def ocr_find_text(image_path: str, targets: list) -> list:
    """
    用 OCR 在截图中查找目标文字，返回所有匹配的坐标列表
    每个元素: (x, y, w, h, matched_text)
    """
    if not HAS_OCR:
        return []
    try:
        img = Image.open(image_path)
        data = pytesseract.image_to_data(
            img, lang="chi_sim+eng", output_type=pytesseract.Output.DICT
        )
    except Exception as e:
        print("  [OCR] 识别失败: " + str(e))
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
                print("  [OCR] 找到 「" + text + "」@ (" + str(x) + "," + str(y) + ") " + str(w) + "x" + str(h))
                break
    return results


# ── OpenCV 模板匹配（可选增强）────────────────────────────
def cv_find_template(screenshot_path: str, template_path: str, threshold: float = 0.8) -> list:
    """
    用 OpenCV 模板匹配定位按钮图标，返回匹配坐标列表
    若无模板图片，返回空列表
    """
    if not HAS_CV:
        return []
    try:
        img = cv2.imread(screenshot_path)
        tpl = cv2.imread(template_path)
        if img is None or tpl is None:
            return []
        result = cv2.matchTemplate(img, tpl, cv2.TM_CCOEFF_NORMED)
        locs = []
        while True:
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val < threshold:
                break
            x, y = max_loc
            h, w = tpl.shape[:2]
            locs.append((x, y, w, h, "template_match"))
            # 屏蔽已匹配区域，避免重复
            cv2.rectangle(result, (x, y), (x + w, y + h), 0, -1)
        if locs:
            print("  [CV] 模板匹配到 " + str(len(locs)) + " 个位置")
        return locs
    except Exception as e:
        print("  [CV] 模板匹配失败: " + str(e))
        return []


# ── 主流程 ─────────────────────────────────────────────────
async def main():
    url = os.environ.get("NEWAPI_URL", "https://api.xxx.com").rstrip("/")
    username = os.environ.get("NEWAPI_USERNAME", "")
    password = os.environ.get("NEWAPI_PASSWORD", "")
    ck_raw = os.environ.get("NEWAPI_COOKIE", "")

    print("=" * 50)
    print("  New API 自动签到（OCR + OpenCV 视觉识别）")
    print("  目标: " + url)
    print("  OCR: " + ("可用" if HAS_OCR else "不可用（DOM 降级）"))
    print("  OpenCV: " + ("可用" if HAS_CV else "不可用"))
    print("=" * 50)

    # 登录凭证检查
    use_cookie = bool(ck_raw.strip())
    use_password = bool(username and password)
    if not use_cookie and not use_password:
        print("\n[ERROR] 请设置 NEWAPI_COOKIE 或 NEWAPI_USERNAME+NEWAPI_PASSWORD")
        sys.exit(1)

    async with async_playwright() as p:
        br = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        ctx = await br.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        )
        page = await ctx.new_page()

        # ── Step 1: 登录 ──────────────────────────────────
        if use_cookie:
            # Cookie 登录
            from urllib.parse import urlparse
            domain = urlparse(url).hostname or "localhost"
            cookies = []
            for pair in ck_raw.split(";"):
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
            await ctx.add_cookies(cookies)
            print("\n[登录] 已注入 " + str(len(cookies)) + " 个 Cookie")
        else:
            # 账号密码登录
            print("\n[登录] 使用账号密码登录...")
            login_url = url + "/login"
            print("  打开: " + login_url)
            await page.goto(login_url, timeout=30000, wait_until="networkidle")
            await asyncio.sleep(2)

            sd = Path("screenshots")
            sd.mkdir(exist_ok=True)
            await page.screenshot(path=str(sd / "01_login_page.png"))

            # 填写表单（兼容不同 New API 版本的 input name）
            await page.fill(
                "input[name='username'], input[placeholder*='用户'], input[type='text']",
                username
            )
            await page.fill(
                "input[name='password'], input[placeholder*='密码'], input[type='password']",
                password
            )
            print("  已填写账号密码")
            await asyncio.sleep(1)
            await page.screenshot(path=str(sd / "02_login_filled.png"))

            # 点击登录按钮：优先 OCR，降级 DOM
            clicked = False
            if HAS_OCR:
                await page.screenshot(path="temp_login.png")
                matches = ocr_find_text("temp_login.png", ["登录", "Login", "登錄", "Sign in"])
                if matches:
                    x, y, w, h, _ = matches[0]
                    await page.mouse.click(x + w // 2, y + h // 2)
                    clicked = True
                    print("  [OCR] 已点击登录按钮")

            if not clicked:
                print("  [DOM] 用选择器点击登录按钮")
                for sel in [
                    "button[type='submit']",
                    "button:has-text('登录')",
                    "button:has-text('Login')",
                    "input[type='submit']",
                ]:
                    try:
                        btn = await page.query_selector(sel)
                        if btn:
                            await btn.click()
                            clicked = True
                            print("  [DOM] 已点击: " + sel)
                            break
                    except Exception:
                        continue

            if not clicked:
                print("[ERROR] 找不到登录按钮！")
                await br.close()
                sys.exit(1)

            await asyncio.sleep(3)
            await page.screenshot(path=str(sd / "03_after_login.png"))

        # ── Step 2: 进入个人页面 ─────────────────────────
        personal_url = url + "/console/personal"
        print("\n[签到] 进入个人页面: " + personal_url)
        await page.goto(personal_url, timeout=30000, wait_until="networkidle")
        await asyncio.sleep(2)

        sd = Path("screenshots")
        sd.mkdir(exist_ok=True)
        await page.screenshot(path=str(sd / "04_personal_page.png"))
        print("  截图: 04_personal_page.png")

        # 检查是否登录成功
        pwd_input = await page.query_selector("input[type='password']")
        if pwd_input:
            print("[ERROR] 未登录！Cookie 可能已过期，或账号密码错误")
            await page.screenshot(path=str(sd / "ERROR_not_logged_in.png"))
            await br.close()
            sys.exit(1)

        print("  [OK] 登录状态确认")

        # ── Step 3: OCR 定位签到按钮并点击 ───────────────
        print("\n[签到] 查找签到按钮...")
        await page.screenshot(path="temp_personal.png")

        checkin_texts = ["签到", "打卡", "Check in", "Check-in", "每日签到", "Sign in"]
        clicked = False

        # 方法1: OCR 文字识别
        if HAS_OCR:
            matches = ocr_find_text("temp_personal.png", checkin_texts)
            # 去重：同一行（y 坐标相近）只取第一个
            seen_y = set()
            unique = []
            for (x, y, w, h, t) in matches:
                y_key = y // 20  # 20px 容差
                if y_key not in seen_y:
                    seen_y.add(y_key)
                    unique.append((x, y, w, h, t))
            if unique:
                x, y, w, h, t = unique[0]
                cx = x + w // 2
                cy = y + h // 2
                print("  [OCR] 点击 「" + t + "」@ (" + str(cx) + ", " + str(cy) + ")")
                await page.mouse.click(cx, cy)
                clicked = True

        # 方法2: OpenCV 模板匹配（如已安装且有模板）
        if not clicked and HAS_CV:
            tpl_dir = Path("templates")
            if tpl_dir.exists():
                for tpl_file in tpl_dir.glob("*.png"):
                    matches = cv_find_template("temp_personal.png", str(tpl_file))
                    if matches:
                        x, y, w, h, _ = matches[0]
                        await page.mouse.click(x + w // 2, y + h // 2)
                        clicked = True
                        print("  [CV] 模板匹配点击: " + tpl_file.name)
                        break

        # 方法3: DOM 降级
        if not clicked:
            print("  [DOM] OCR/CV 未找到，降级使用 DOM 选择器")
            for txt in checkin_texts:
                try:
                    btn = await page.query_selector("text=" + txt)
                    if btn:
                        await btn.click()
                        clicked = True
                        print("  [DOM] 已点击: " + txt)
                        break
                except Exception:
                    continue

        if clicked:
            print("  [OK] 签到按钮已点击！")
            await asyncio.sleep(3)
            await page.screenshot(path=str(sd / "05_after_checkin.png"))
        else:
            print("[WARN] 未找到签到按钮！")
            await page.screenshot(path=str(sd / "05_no_button.png"))
            # 列出所有可点击元素供调试
            btns = await page.query_selector_all("button, a[href], [role='button']")
            print("  页面可点击元素（前 15 个）:")
            for i, b in enumerate(btns[:15]):
                try:
                    t = await b.inner_text()
                    if t.strip():
                        print("    #" + str(i) + ": " + t.strip()[:30])
                except Exception:
                    pass

        # 最终截图
        await asyncio.sleep(2)
        await page.screenshot(path=str(sd / "06_result.png"))
        print("\n[完成] 截图已保存至 screenshots/ 目录")
        print("  页面标题: " + await page.title())

        await br.close()

    # ── Telegram 通知（可选）─────────────────────────────
    ttoken = os.environ.get("TELEGRAM_TOKEN", "")
    tchat = os.environ.get("TELEGRAM_CHAT_ID", "")
    if ttoken and tchat:
        try:
            import urllib.request
            import urllib.parse
            tmsg = "New API 签到完成\nURL: " + url
            turl = (
                "https://api.telegram.org/bot" + ttoken + "/sendMessage"
                "?chat_id=" + tchat +
                "&text=" + urllib.parse.quote(tmsg)
            )
            urllib.request.urlopen(turl, timeout=10)
            print("[通知] Telegram 消息已发送")
        except Exception as e:
            print("[通知] Telegram 发送失败: " + str(e))

    # GitHub Actions 输出
    out = os.environ.get("GITHUB_OUTPUT", "/dev/null")
    try:
        with open(out, "a") as f:
            f.write("checkin_result=completed\n")
    except Exception:
        pass


if __name__ == "__main__":
    subprocess.run(["mkdir", "-p", "screenshots"], check=False)
    asyncio.run(main())
