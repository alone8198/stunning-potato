# Stunning Potato

New API 自动签到脚本 —— 使用 Playwright + OCR + OpenCV 视觉识别自动完成每日签到。

## 功能特点

- **视觉识别签到**：使用 Tesseract OCR 识别页面文字，自动定位并点击签到按钮
- **模板匹配**（可选）：在 `templates/` 目录下放置按钮截图，用 OpenCV 进行模板匹配点击
- **账号密码登录**：使用用户名和密码自动登录
- **多关键词兼容**：自动识别"签到"、"打卡"、"Check in"等多种按钮文字
- **失败自动截图**：截图存档保留 7 天，方便调试
- **Telegram 通知**（可选）：签到完成后推送消息
- **完全免费**：运行在 GitHub Actions，无需自己的服务器

---

## 快速开始

### 1. Fork / Clone 本仓库

### 2. 配置 Secrets

进入仓库 `Settings → Secrets and variables → Actions → New repository secret`，添加以下 Secrets：

| Secret 名称 | 说明 | 必填 |
|---|---|---|
| `NEWAPI_URLS` | New API 地址，一行一个 | ✅ |
| `NEWAPI_USERNAMES` | 账号，一行一个，行数对应 URL | ✅ |
| `NEWAPI_PASSWORDS` | 密码，一行一个，行数对应 URL | ✅ |
| `TELEGRAM_TOKEN` | Telegram Bot Token | ❌ |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | ❌ |

### 3. 手动触发测试

进入 `Actions` 标签页 → 选择 `New API 批量自动签到` → `Run workflow`

---

## 定时设置

默认每天 **北京时间 06:00** 自动签到（UTC 22:00）。

修改 `.github/workflows/checkin.yml` 中的 cron 表达式：

```yaml
# 北京时间 06:00（默认）
- cron: '0 22 * * *'

# 北京时间 22:00
# - cron: '0 14 * * *'
```

---

## 工作原理

```
1. 启动 Playwright Chromium 无头浏览器
2. 访问登录页面，填写用户名和密码
3. 点击登录按钮（OCR 识别 + DOM 选择器）
4. 访问 /console/personal 个人页面
5. 对整个页面截图
6. 用 Tesseract OCR 识别截图中的文字
7. 找到"签到"/"打卡"等关键词的坐标，模拟鼠标点击
8. 截图存档，发送 Telegram 通知（可选）
```

**降级策略**：OCR 失败 → OpenCV 模板匹配 → DOM 选择器，三层保障。

---

## 查看运行结果

- 进入 `Actions` 标签页查看运行日志
- 点击任意运行记录 → `Artifacts` → 下载 `checkin-screenshots.zip`（保留 7 天）
- 截图文件：`login_1.png`、`personal_1.png`、`result_1.png` 等，方便排查问题

---

## 自定义模板匹配（可选）

如果 OCR 识别率不理想，可以在仓库里创建 `templates/` 目录，放入签到按钮的截图（PNG 格式）：

```
stunning-potato/
├── templates/
│   ├── checkin_btn.png    # 签到按钮截图
│   └── checkin_btn2.png   # 备用模板
├── checkin.py
└── ...
```

脚本会自动用 OpenCV 进行模板匹配定位按钮。

---

## 依赖

- Python 3.11+
- [Playwright](https://playwright.dev/python/)（Chromium 无头浏览器）
- [pytesseract](https://github.com/madmaze/pytesseract)（OCR 文字识别）
- [OpenCV](https://opencv.org/)（模板匹配，可选）
- Tesseract OCR（`tesseract-ocr` + `tesseract-ocr-chi-sim`）

GitHub Actions 环境已自动安装所有依赖，无需手动配置。

---

## License

MIT
