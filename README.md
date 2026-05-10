# 🍟 Stunning Potato

<div align="center">

### New API 自动签到脚本

使用 Playwright + OCR + OpenCV 视觉识别自动完成每日签到

[![GitHub Stars](https://img.shields.io/github/stars/alone8198/stunning-potato?style=social)](https://github.com/alone8198/stunning-potato)
[![License](https://img.shields.io/github/license/alone8198/stunning-potato?style=flat&color=blue)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-green?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Auto%20Checkin-brightgreen?style=flat&logo=github-actions&logoColor=white)](https://github.com/alone8198/stunning-potato/actions)

</div>

---

## ✨ 功能特点

<div align="center">

| 🎯 功能 | 📝 说明 |
|:---:|:---|
| **🤖 视觉识别签到** | 使用 Tesseract OCR 识别页面文字，自动定位并点击签到按钮 |
| **🎨 模板匹配** | 在 `templates/` 目录放置按钮截图，用 OpenCV 进行模板匹配点击 |
| **🔐 账号密码登录** | 使用用户名和密码自动登录，安全可靠 |
| **🌍 多关键词兼容** | 自动识别"签到"、"打卡"、"Check in"等多种按钮文字 |
| **📸 失败自动截图** | 截图存档保留 7 天，方便调试 |
| **📱 Telegram 通知** | 签到完成后推送消息（可选）|
| **💯 完全免费** | 运行在 GitHub Actions，无需自己的服务器 |

</div>

---

## 🚀 快速开始

### 1️⃣ Fork / Clone 本仓库

```bash
git clone https://github.com/alone8198/stunning-potato.git
cd stunning-potato
```

### 2️⃣ 配置 Secrets

进入仓库 **`Settings → Secrets and variables → Actions → New repository secret`**，添加以下 Secrets：

| Secret 名称 | 说明 | 必填 | 示例 |
|:---|:---|:---:|:---|
| `NEWAPI_URLS` | New API 地址（一行一个）| ✅ | `https://api.example.com` |
| `NEWAPI_USERNAMES` | 账号（一行一个）| ✅ | `user1` |
| `NEWAPI_PASSWORDS` | 密码（一行一个）| ✅ | `pass1` |
| `TELEGRAM_TOKEN` | Telegram Bot Token | ❌ | `123456:ABC-DEF...` |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | ❌ | `123456789` |

<details>
<summary>📖 多账号配置示例（点击展开）</summary>

```
# NEWAPI_URLS（一行一个网址）
https://api1.example.com
https://api2.example.com

# NEWAPI_USERNAMES（行数对应网址）
user1
user2

# NEWAPI_PASSWORDS（行数对应网址）
password1
password2
```

</details>

### 3️⃣ 手动触发测试

进入 **`Actions`** 标签页 → 选择 **`New API 批量自动签到`** → 点击 **`Run workflow`**

---

## ⏰ 定时设置

默认每天 **北京时间 06:00** 自动签到（UTC 22:00）。

修改 `.github/workflows/checkin.yml` 中的 cron 表达式：

```yaml
# 北京时间 06:00（默认）
- cron: '0 22 * * *'

# 北京时间 22:00
# - cron: '0 14 * * *'

# 北京时间 12:00（中午）
# - cron: '0 4 * * *'
```

<details>
<summary>📚 Cron 表达式说明（点击展开）</summary>

| 北京时间 | UTC 时间 | Cron 表达式 |
|:---:|:---:|:---|
| 06:00 | 22:00 (前一天) | `0 22 * * *` |
| 08:00 | 00:00 | `0 0 * * *` |
| 12:00 | 04:00 | `0 4 * * *` |
| 18:00 | 10:00 | `0 10 * * *` |
| 22:00 | 14:00 | `0 14 * * *` |

</details>

---

## 🔧 工作原理

```
┌─────────────────────────────────────────────────────┐
│  1. 启动 Playwright Chromium 无头浏览器          │
└─────────────────┬───────────────────────────────────┘
                  ▼
┌─────────────────────────────────────────────────────┐
│  2. 访问登录页面，填写用户名和密码                │
└─────────────────┬───────────────────────────────────┘
                  ▼
┌─────────────────────────────────────────────────────┐
│  3. 点击登录按钮（OCR 识别 + DOM 选择器）         │
└─────────────────┬───────────────────────────────────┘
                  ▼
┌─────────────────────────────────────────────────────┐
│  4. 访问 /console/personal 个人页面               │
└─────────────────┬───────────────────────────────────┘
                  ▼
┌─────────────────────────────────────────────────────┐
│  5. 对整个页面截图                                 │
└─────────────────┬───────────────────────────────────┘
                  ▼
┌─────────────────────────────────────────────────────┐
│  6. 用 Tesseract OCR 识别截图中的文字             │
└─────────────────┬───────────────────────────────────┘
                  ▼
┌─────────────────────────────────────────────────────┐
│  7. 找到"签到"/"打卡"等关键词，模拟鼠标点击      │
└─────────────────┬───────────────────────────────────┘
                  ▼
┌─────────────────────────────────────────────────────┐
│  8. 截图存档，发送 Telegram 通知（可选）          │
└─────────────────────────────────────────────────────┘
```

### 🛡️ 降级策略

```
OCR 识别失败
    ↓
OpenCV 模板匹配
    ↓
DOM 选择器
    ↓
记录失败并截图
```

---

## 📊 查看运行结果

<div align="center">

| 步骤 | 操作 |
|:---:|:---|
| 1️⃣ | 进入 `Actions` 标签页查看运行日志 |
| 2️⃣ | 点击任意运行记录 → `Artifacts` |
| 3️⃣ | 下载 `checkin-screenshots.zip`（保留 7 天）|

</div>

### 📸 截图文件说明

```
screenshots/
├── login_1.png          # 登录页面截图
├── login_filled_1.png   # 填写完成后的登录页面
├── after_login_1.png    # 登录后的页面
├── personal_1.png       # 个人页面截图
├── result_1.png         # 签到成功截图
└── no_button_1.png      # 未找到签到按钮截图
```

---

## 🎨 自定义模板匹配（可选）

如果 OCR 识别率不理想，可以在仓库里创建 `templates/` 目录，放入签到按钮的截图（PNG 格式）：

```
stunning-potato/
├── templates/
│   ├── checkin_btn.png    # 签到按钮截图
│   └── checkin_btn2.png   # 备用模板
├── checkin.py
└── ...
```

<details>
<summary>💡 如何获取按钮截图？（点击展开）</summary>

1. 打开 New API 个人页面
2. 找到签到按钮
3. 截图并裁剪出按钮部分
4. 保存为 PNG 格式
5. 放入 `templates/` 目录

</details>

脚本会自动用 OpenCV 进行模板匹配定位按钮。

---

## 📦 依赖

<div align="center">

| 依赖 | 说明 | 必需 |
|:---|:---|:---:|
| **Python 3.11+** | 编程语言 | ✅ |
| **[Playwright](https://playwright.dev/python/)** | Chromium 无头浏览器 | ✅ |
| **[pytesseract](https://github.com/madmaze/pytesseract)** | OCR 文字识别 | ✅ |
| **[OpenCV](https://opencv.org/)** | 模板匹配 | ❌ |
| **Tesseract OCR** | `tesseract-ocr` + `tesseract-ocr-chi-sim` | ✅ |

</div>

> **注意**：GitHub Actions 环境已自动安装所有依赖，无需手动配置。

---

## 🐛 故障排除

<details>
<summary>❌ 签到失败（点击展开）</summary>

1. 检查用户名和密码是否正确
2. 查看 `Actions` 日志中的错误信息
3. 下载截图查看具体失败原因
4. 尝试添加自定义模板到 `templates/` 目录

</details>

<details>
<summary>❌ OCR 识别失败（点击展开）</summary>

1. 确保已安装 `tesseract-ocr-chi-sim`（中文语言包）
2. 尝试使用模板匹配（见上方"自定义模板匹配"）
3. 检查截图是否清晰

</details>

<details>
<summary>❌ GitHub Actions 运行失败（点击展开）</summary>

1. 检查 Secrets 是否配置正确
2. 确保 `NEWAPI_URLS`、`NEWAPI_USERNAMES`、`NEWAPI_PASSWORDS` 行数对应
3. 查看 Actions 日志中的详细错误信息

</details>

---

## 📝 License

[MIT License](LICENSE) - 可自由使用、修改和分发

---

## ⭐ Star History

如果你觉得这个项目有用，请给它一个 Star ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=alone8198/stunning-potato&type=Date)](https://star-history.com/#alone8198/stunning-potato&Date)

---

<div align="center">

**🍟 Stunning Potato**

Made with ❤️ by [alone8198](https://github.com/alone8198)

[⬆ 回到顶部](#-stunning-potato)

</div>
