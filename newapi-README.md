# 🎯 New API 自动签到工具

使用 **Python + Playwright（Chromium）** 在 GitHub Actions 上实现每日自动签到。

---

## ✨ 功能特点

- ✅ 全自动：每天定时运行，无需人工干预
- ✅ 真实浏览器：使用 Chromium 内核，模拟真实用户行为
- ✅ Cookie 登录：无需账号密码，安全便捷
- ✅ 截图存档：每次运行自动截图，签到结果一目了然
- ✅ 多通知渠道：支持 Telegram 通知（可扩展钉钉/企业微信）
- ✅ 免费托管：完全基于 GitHub Actions 免费额度

---

## 🚀 快速开始

### 第一步：获取 New API 的 Cookie

1. 用浏览器打开您的 New API 地址并**登录**
2. 按 `F12` 打开开发者工具 → 切换到 **Network（网络）** 标签
3. 刷新页面（F5）
4. 点击第一个请求（通常是页面本身）
5. 在右侧找到 **Request Headers（请求头）**
6. 找到 `Cookie:` 这一行，**复制整个 Cookie 值**

```
示例 Cookie 内容：
token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...; refresh_token=xxx; session=yyy
```

> ⚠️ **注意：** Cookie 包含登录凭证，请勿分享给他人！

---

### 第二步：Fork / 创建仓库

将本仓库（包含所有文件）上传到您自己的 GitHub 仓库。

推荐目录结构：
```
your-repo/
├── .github/
│   └── workflows/
│       └── checkin.yml      ← GitHub Actions 配置
├── checkin.py               ← 签到脚本
├── requirements.txt         ← Python 依赖
└── README.md
```

---

### 第三步：配置 GitHub Secrets

进入您的仓库 → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

添加以下 Secrets：

| Secret 名称 | 必填 | 说明 |
|-------------|------|------|
| `NEWAPI_URL` | ✅ 必填 | New API 地址，如 `https://api.example.com` |
| `NEWAPI_COOKIE` | ✅ 必填 | 第一步中获取的完整 Cookie 字符串 |
| `TELEGRAM_TOKEN` | 可选 | Telegram Bot Token（用于推送签到结果） |
| `TELEGRAM_CHAT_ID` | 可选 | Telegram Chat ID |

---

### 第四步：修改签到时间（可选）

编辑 `.github/workflows/checkin.yml`，找到 `schedule` 部分：

```yaml
schedule:
  - cron: '0 22 * * *'   # UTC 22:00 = 北京时间 06:00
```

**Cron 时间对照表（UTC → 北京时间 UTC+8）：**

| 北京时间 | Cron 表达式（UTC） |
|---------|-------------------|
| 06:00   | `0 22 * * *` |
| 08:00   | `0 0 * * *` |
| 09:00   | `0 1 * * *` |
| 12:00   | `0 4 * * *` |
| 22:00   | `0 14 * * *` |

---

### 第五步：测试运行

1. 进入仓库 → **Actions** 标签
2. 选择 **New API 自动签到** workflow
3. 点击 **Run workflow** → 选择 `main` 分支 → **Run workflow**
4. 等待运行完成（约 1-2 分钟）
5. 查看 **Artifacts** 中的 `checkin-screenshots` 截图

---

## 🔧 本地测试

在本地调试脚本（需要先安装依赖）：

```bash
# 安装依赖
pip install -r requirements.txt
playwright install chromium

# 设置环境变量并运行
export NEWAPI_URL="https://your-api-url.com"
export NEWAPI_COOKIE="your_cookie_here"
python checkin.py
```

Windows（PowerShell）：
```powershell
$env:NEWAPI_URL="https://your-api-url.com"
$env:NEWAPI_COOKIE="your_cookie_here"
python checkin.py
```

---

## 🔄 Cookie 过期处理

Cookie 通常有效期为 **7~30 天**，过期后签到会失败。

**判断 Cookie 是否过期：**
- GitHub Actions 运行失败
- 截图显示登录页面（而非个人页面）
- 通知提示「Cookie 已过期」

**重新获取 Cookie：**
1. 重新登录 New API
2. 按第一步的方法获取新 Cookie
3. 更新 `NEWAPI_COOKIE` Secret
4. 重新运行 workflow

---

## 📸 截图说明

每次运行后，GitHub Actions 会自动上传截图到 **Artifacts**（保留 7 天）：

| 截图文件名 | 说明 |
|-----------|------|
| `01_homepage.png` | 访问个人页面后的截图 |
| `02_after_click.png` | 点击签到按钮后的截图（如找到按钮） |
| `02_no_button_found.png` | 未找到签到按钮时的截图 |
| `03_result.png` | 最终页面截图 |

查看方式：**Actions** → 选择某次运行 → 右侧 **Artifacts** → 下载 `checkin-screenshots`

---

## 🔍 签到按钮找不到怎么办？

不同 New API 版本页面结构不同，脚本内置了多种选择器。如果找不到：

1. 下载 Artifacts 中的截图，确认页面是否正常加载
2. 打开浏览器 F12，找到签到按钮的 **CSS 选择器**
3. 将选择器添加到 `checkin.py` 的 `checkin_selectors` 列表中
4. 提交更新，重新运行

**欢迎提交 PR 补充更多 New API 版本的签到选择器！** 🙏

---

## 📢 通知配置（可选）

### Telegram 通知

1. 找 [@BotFather](https://t.me/botfather) 创建 Bot，获取 `Token`
2. 给 Bot 发一条消息，然后访问：
   `https://api.telegram.org/bot<TOKEN>/getUpdates`
3. 在返回 JSON 中找到 `"chat":{"id":...}`，即为 `Chat ID`
4. 将 `TELEGRAM_TOKEN` 和 `TELEGRAM_CHAT_ID` 添加到 Secrets

---

## 🛠️ 故障排查

| 问题 | 解决方法 |
|------|---------|
| `NEWAPI_URL 未设置` | 在 Secrets 中添加 `NEWAPI_URL` |
| `NEWAPI_COOKIE 未设置` | 在 Secrets 中添加 `NEWAPI_COOKIE` |
| Cookie 已过期 | 重新登录获取新 Cookie 并更新 Secret |
| 签到按钮找不到 | 查看截图，手动查找按钮选择器并更新脚本 |
| Playwright 安装失败 | 检查 `playwright install chromium` 是否执行成功 |

---

## 📄 文件说明

```
newapi-checkin/
├── .github/workflows/checkin.yml   # GitHub Actions 自动运行配置
├── checkin.py                      # 主签到脚本（Playwright + Chromium）
├── requirements.txt                # Python 依赖列表
└── README.md                      # 本文件
```

---

## ⚖️ 免责声明

本工具仅供学习交流使用，请遵守您使用的 New API 服务的使用条款。
因使用本工具导致的任何后果，作者概不负责。

---

Made with ❤️ by WorkBuddy
