# Stunning Potato 🥔

个人工具仓库，包含 New API 自动签到脚本和任务看板。

## 项目结构

```
stunning-potato/
├── checkin.py              # New API 自动签到脚本
├── requirements.txt        # Python 依赖
├── .github/workflows/      # GitHub Actions 自动签到
├── tasks/                  # 任务看板（HTML + Markdown）
│   ├── index.html
│   └── TASKS.md
└── newapi-README.md        # New API 签到详细说明
```

## New API 自动签到

通过 GitHub Actions 定时执行，使用 Playwright + Chromium 模拟浏览器操作，携带 Cookie 自动完成签到。

### 功能特点

- ✅ 支持 Cookie 注入登录，无需账号密码
- ✅ 多关键词兼容（`签到`/`打卡`/`Check in` 等）
- ✅ 签到失败自动截图存档（保留 7 天）
- ✅ 可选 Telegram 通知推送
- ✅ 完全免费，运行在 GitHub Actions

### 配置步骤

1. **Fork 或克隆本仓库**

2. **配置 GitHub Secrets**（`Settings → Secrets and variables → Actions → New repository secret`）：

| Secret 名称 | 说明 | 必填 |
|---|---|---|
| `NEWAPI_URL` | New API 部署地址（如 `https://api.example.com`） | ✅ |
| `NEWAPI_COOKIE` | 浏览器中复制的完整 Cookie 字符串 | ✅ |
| `TELEGRAM_TOKEN` | Telegram Bot Token（可选） | ❌ |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID（可选） | ❌ |

3. **获取 Cookie 方法**：
   - 浏览器打开 New API 页面并登录
   - 按 `F12` 打开开发者工具 → `Application` → `Cookies`
   - 复制所有 Cookie（格式：`name1=value1; name2=value2; ...`）

4. **手动触发测试**：`Actions` → `New API 自动签到` → `Run workflow`

### 定时设置

默认每天 **北京时间 06:00** 自动签到（UTC 22:00）。

修改 `.github/workflows/checkin.yml` 中的 cron 表达式调整时间：

```yaml
# 北京时间 06:00（默认）
cron: '0 22 * * *'

# 北京时间 22:00
# cron: '0 14 * * *'
```

### 查看运行结果

- 进入 `Actions` 标签页查看运行日志
- 截图在 `Artifacts` 里下载（保留 7 天）

详细说明见 [newapi-README.md](newapi-README.md)。

## 任务看板

仓库内置一个可视化任务看板，可直接在浏览器查看。

### 本地预览

```bash
cd tasks
python -m http.server 8080
# 浏览器访问 http://localhost:8080
```

或使用任意静态服务器托管 `tasks/` 目录。

### 任务文件

- `tasks/index.html` — 可视化 Kanban 看板（支持筛选、搜索、弹窗详情）
- `tasks/TASKS.md` — Markdown 任务文档，可直接放入 Issues 或 Project

## 许可证

MIT
