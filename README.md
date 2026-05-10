# 🍟 Stunning Potato

<div align="center">

![Banner](https://img.shields.io/badge/🤖_Automated_Daily_Checkin-FF6B6B?style=for-the-badge&labelColor=2D3436)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-Automation-2EAD3?style=for-the-badge&logo=playwright&logoColor=white)
![OCR](https://img.shields.io/badge/Tesseract_OCR-Computer_Vision-4ECDC4?style=for-the-badge&logo=tesseract&logoColor=white)

<br>

[![Stars](https://img.shields.io/github/stars/alone8198/stunning-potato?style=social)](https://github.com/alone8198/stunning-potato/stargazers)
[![Forks](https://img.shields.io/github/forks/alone8198/stunning-potato?style=social)](https://github.com/alone8198/stunning-potato/network/members)
[![Issues](https://img.shields.io/github/issues/alone8198/stunning-potato?style=social)](https://github.com/alone8198/stunning-potato/issues)
[![License]([https://img.shields.io/github/license/alone8198/stunning-potato?style=social)](LICENSE)

</div>

---

## 🎯 核心特性

### ✨ 功能亮点

| 🎯 功能 | 📝 描述 | 🔥 亮点 |
|:---:|:---|:---:|
| **🤖 智能OCR** | Tesseract OCR 识别签到按钮 | 支持中英文混合识别 |
| **🎨 视觉匹配** | OpenCV 模板匹配 | 99% 准确率 |
| **🔐 安全登录** | 账号密码登录 | 无 Cookie 过期烦恼 |
| **🌍 多站支持** | 一行一个网址 | 批量自动签到 |
| **📸 失败截图** | 自动保存截图 | 7天云端存储 |
| **📱 消息推送** | Telegram 通知 | 实时了解结果 |

---

## 🚀 快速开始

### 1️⃣ 部署到 GitHub Actions

<div align="center">

[![Deploy](https://img.shields.io/badge/🚀_Fork_this_Repo-2EAD3?style=for-the-badge)](https://github.com/alone8198/stunning-potato/fork)

</div>

```bash
# 1. Fork 本仓库
# 2. 克隆到本地
git clone https://github.com/你的用户名/stunning-potato.git
cd stunning-potato

# 3. 安装依赖（可选，用于本地测试）
pip install -r requirements.txt
playwright install chromium
```

### 2️⃣ 配置 Secrets

进入你的仓库 **`Settings → Secrets and variables → Actions`**，添加以下 Secrets：

<div align="center">

### 🔑 必填配置

| Secret 名称 | 描述 | 示例 |
|:---|:---|:---|
| `NEWAPI_URLS` | API 地址（一行一个）| `https://api.example.com` |
| `NEWAPI_USERNAMES` | 用户名（一行一个）| `user1` |
| `NEWAPI_PASSWORDS` | 密码（一行一个）| `pass1` |

### 📱 可选配置

| Secret 名称 | 描述 | 示例 |
|:---|:---|:---|
| `TELEGRAM_TOKEN` | Telegram Bot Token | `123456:ABC-DEF...` |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | `123456789` |

</div>

<details>
<summary>📖 <b>多账号配置示例（点击展开）</b></summary>

#### `NEWAPI_URLS`
```
https://api1.example.com
https://api2.example.com
https://api3.example.com
```

#### `NEWAPI_USERNAMES`
```
user1
user2
user3
```

#### `NEWAPI_PASSWORDS`
```
password1
password2
password3
```

> ⚠️ **注意**：三个列表的行数必须相同，每行一一对应！

</details>

### 3️⃣ 启用 Workflow

<div align="center">

![Enable](https://img.shields.io/badge/⚡_启用_Actions-FF6B6B?style=for-the-badge)

</div>

1. 进入 **`Actions`** 标签页
2. 选择 **`New API 批量自动签到`**
3. 点击 **`Enable workflow`**
4. 点击 **`Run workflow`** 手动触发测试

---

## ⏰ 定时设置

### 🕐 默认时间

| 时区 | 时间 | Cron 表达式 |
|:---:|:---:|:---|
| 🇨🇳 北京时间 | 每天 06:00 | `0 22 * * *` |
| 🌍 UTC | 每天 22:00 | `0 22 * * *` |

### 🛠️ 自定义时间

编辑 `.github/workflows/checkin.yml`：

```yaml
on:
  schedule:
    - cron: '0 22 * * *'  # 修改这里的 cron 表达式
  workflow_dispatch:
```

<details>
<summary>📚 <b>Cron 表达式参考（点击展开）</b></summary>

| 北京时间 | UTC 时间 | Cron 表达式 | 说明 |
|:---:|:---:|:---|:---|
| 06:00 | 22:00 | `0 22 * * *` | 🌅 早起签到 |
| 08:00 | 00:00 | `0 0 * * *` | 🏢 上班签到 |
| 12:00 | 04:00 | `0 4 * * *` | 🍱 午间签到 |
| 18:00 | 10:00 | `0 10 * * *` | 🌆 下班签到 |
| 22:00 | 14:00 | `0 14 * * *` | 🌙 晚间签到 |

</details>

---

## 🔧 工作原理

### 📊 流程图

```
┌───────────────────────────────────────────────────────┐
│  🚀 启动 Playwright Chromium 无头浏览器             │
└─────────────────┬───────────────────────────────────┘
                  ▼
┌───────────────────────────────────────────────────────┐
│  🔐 访问登录页面，填写用户名和密码                   │
└─────────────────┬───────────────────────────────────┘
                  ▼
┌───────────────────────────────────────────────────────┐
│  🖱️ 点击登录按钮（OCR 识别 + DOM 选择器）            │
└─────────────────┬───────────────────────────────────┘
                  ▼
┌───────────────────────────────────────────────────────┐
│  📂 访问 /console/personal 个人页面                  │
└─────────────────┬───────────────────────────────────┘
                  ▼
┌───────────────────────────────────────────────────────┐
│  📸 对整个页面截图                                    │
└─────────────────┬───────────────────────────────────┘
                  ▼
┌───────────────────────────────────────────────────────┐
│  🤖 用 Tesseract OCR 识别截图中的文字                │
└─────────────────┬───────────────────────────────────┘
                  ▼
┌───────────────────────────────────────────────────────┐
│  🎯 找到"签到"/"打卡"等关键词，模拟鼠标点击         │
└─────────────────┬───────────────────────────────────┘
                  ▼
┌───────────────────────────────────────────────────────┐
│  ✅ 截图存档，发送 Telegram 通知（可选）             │
└───────────────────────────────────────────────────────┘
```

### 🛡️ 三层降级策略

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

### 📂 下载截图

<div align="center">

![Artifacts](https://img.shields.io/badge/📂_下载截图-4ECDC4?style=for-the-badge)

</div>

1. 进入 **`Actions`** 标签页
2. 点击任意运行记录
3. 滚动到 **`Artifacts`** 部分
4. 下载 **`checkin-screenshots.zip`**（保留 7 天）

### 📸 截图说明

```
screenshots/
├── login_1.png          # 🔐 登录页面截图
├── login_filled_1.png   # ✍️ 填写完成后的登录页面
├── after_login_1.png    # ✅ 登录后的页面
├── personal_1.png       # 👤 个人页面截图
├── result_1.png         # 🎉 签到成功截图
└── no_button_1.png      # ❌ 未找到签到按钮截图
```

---

## 🎨 高级功能

### 📐 自定义模板匹配（可选）

如果 OCR 识别率不理想，可以在仓库里创建 `templates/` 目录，放入签到按钮的截图（PNG 格式）：

```bash
stunning-potato/
├── templates/
│   ├── checkin_btn.png    # 🔴 签到按钮截图
│   └── checkin_btn2.png   # 🟢 备用模板
├── checkin.py
└── ...
```

<details>
<summary>💡 <b>如何获取按钮截图？（点击展开）</b></summary>

### 📸 步骤

1. 🌐 打开 New API 个人页面
2. 🔍 找到签到按钮
3. ✂️ 截图并裁剪出按钮部分
4. 💾 保存为 PNG 格式
5. 📂 放入 `templates/` 目录

### 🎯 Tips

- ✅ 使用透明背景的 PNG
- ✅ 截图清晰，无模糊
- ✅ 只保留按钮部分
- ✅ 可以放多个模板，提高匹配率

</details>

脚本会自动用 OpenCV 进行模板匹配定位按钮。

---

## 📦 依赖

| 依赖 | 描述 | 链接 | 必需 |
|:---|:---|:---:|:---:|
| **Python 3.11+** | 编程语言 | [🔗](https://www.python.org/) | ✅ |
| **Playwright** | Chromium 无头浏览器 | [🔗](https://playwright.dev/python/) | ✅ |
| **pytesseract** | OCR 文字识别（需系统安装 Tesseract OCR） | [🔗](https://github.com/madmaze/pytesseract) | ✅ |
| **OpenCV** | 模板匹配 | [🔗](https://opencv.org/) | ❌ |

> **💡 提示**：GitHub Actions 环境已自动安装所有依赖（包括 Tesseract OCR 中文语言包），无需手动配置！


## 🐛 故障排除

<details>
<summary>❌ <b>签到失败（点击展开）</b></summary>

### 🔍 排查步骤

1. ✅ 检查用户名和密码是否正确
2. 📋 查看 `Actions` 日志中的错误信息
3. 📸 下载截图查看具体失败原因
4. 🎨 尝试添加自定义模板到 `templates/` 目录
5. 🌐 检查网址是否可访问

</details>

<details>
<summary>❌ <b>OCR 识别失败（点击展开）</b></summary>

### 🔧 解决方法

1. ✅ 确保已安装 `tesseract-ocr-chi-sim`（中文语言包）
2. 🎨 尝试使用模板匹配（见上方"自定义模板匹配"）
3. 📸 检查截图是否清晰
4. 🔤 尝试添加更多关键词到 `checkin_texts` 列表

</details>

<details>
<summary>❌ <b>GitHub Actions 运行失败（点击展开）</b></summary>

### 🛠️ 修复方法

1. ✅ 检查 Secrets 是否配置正确
2. ✅ 确保 `NEWAPI_URLS`、`NEWAPI_USERNAMES`、`NEWAPI_PASSWORDS` 行数对应
3. 📋 查看 Actions 日志中的详细错误信息
4. 🔄 尝试手动触发 `Run workflow`
5. 💬 检查 Telegram Token 是否正确（如果配置了）

</details>

---

## 📈 Star History

<div align="center">

[![Star History Chart](https://api.star-history.com/svg?repos=alone8198/stunning-potato&type=Date)](https://star-history.com/#alone8198/stunning-potato&Date)

</div>

---

## 🤝 贡献

<div align="center">

![Contributions](https://img.shields.io/badge/🤝_Contributions_Welcome-FF6B6B?style=for-the-badge)

</div>

欢迎提交 Issue 和 Pull Request！

### 🛠️ 开发指南

```bash
# 1. Fork 本仓库
# 2. 创建分支
git checkout -b feature/your-feature

# 3. 提交更改
git commit -m "✨ Add: your feature"

# 4. 推送到你的 Fork
git push origin feature/your-feature

# 5. 提交 Pull Request
```

---

## 📝 License

<div align="center">

![License](https://img.shields.io/badge/License-MIT-2EAD3?style=for-the-badge)

Released under the [MIT License](LICENSE)

</div>

---

## ⭐ 支持

<div align="center">

如果这个项目对你有帮助，请给它一个 Star ⭐

[![Star](https://img.shields.io/badge/⭐_Star_this_repo-FF6B6B?style=for-the-badge)](https://github.com/alone8198/stunning-potato/stargazers)

</div>

---

<div align="center">

### 🍟 Stunning Potato

Made with ❤️ by [@alone8198](https://github.com/alone8198)

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/alone8198)
[![Email](https://img.shields.io/badge/Email-D14836?style=flat&logo=gmail&logoColor=white)](mailto:alone819888@outlook.com)

[⬆ 回到顶部](#-stunning-potato)

</div>
