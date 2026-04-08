# XHS-AI-GitHub 每日创作助手

> 🤖 AI 时代的内容创作神器！将 GitHub 上的优质 AI 项目转化为小红书爆款种草内容

[English](./README_EN.md) | 简体中文

## 🎯 项目简介

这是一个专注于 **AI 内容创作** 的自动化工具集：

| 模块 | 功能 |
|------|------|
| 🤖 **Bot 自动化** | 每日自动抓取 GitHub 趋势 AI 项目 |
| 📊 **热度评分** | 智能评分系统，筛选最优质项目 |
| ✍️ **内容生成** | 自动生成小红书风格的爆款内容 |
| 🖼️ **配图生成** | 自动生成封面图和项目缩略图 |
| ⏰ **定时任务** | 支持每日自动执行 |
| 📦 **多项目合集** | 支持生成 Top 3/5/10 合集 |

## 📦 快速开始

### 方式一：使用 WorkBuddy Skill

在 WorkBuddy 中直接说：
```
帮我写一篇小红书推荐 XX 项目
生成 AI 项目的种草内容
```

### 方式二：运行自动化 Bot

```bash
# 克隆仓库
git clone https://github.com/kedamano/XHS-AI-GitHub.git
cd XHS-AI-GitHub

# 安装依赖
pip install -r bot/requirements.txt

# 运行一次测试
python bot/scripts/main.py

# 设置每日定时任务
python bot/scripts/setup_scheduler.py
```

## 📁 项目结构

```
XHS-AI-GitHub/
├── README.md              # 本文档
├── LICENSE                # MIT 许可证
│
├── skills/
│   └── xhs-ai-blogger/    # WorkBuddy Skill
│       └── SKILL.md       # 小红书 AI 博主技能
│
└── bot/                   # 自动化 Bot
    ├── scripts/
    │   ├── main.py              # 主运行脚本
    │   ├── fetch_trending.py    # GitHub 趋势抓取
    │   ├── aggregator.py        # 多项目合集生成器
    │   ├── image_generator.py   # 配图生成器
    │   └── setup_scheduler.py   # 定时任务设置
    ├── data/                    # 数据存储
    ├── output/                  # 输出目录
    ├── logs/                    # 日志目录
    ├── requirements.txt         # Python 依赖
    └── README.md                # Bot 使用文档
```

## 🔥 功能详情

### 1. GitHub 趋势抓取

自动从 GitHub 抓取 AI 相关项目，支持：
- 多语言筛选 (Python, JavaScript, Go, etc.)
- AI 关键词智能过滤
- 自动排除底层技术库

### 2. 热度评分系统

智能评分基于：
| 维度 | 权重 | 说明 |
|------|------|------|
| Stars | 40% | 绝对受欢迎程度 |
| Forks | 15% | 社区参与度 |
| Watchers | 10% | 关注度 |
| Issues | 15% | 开发活跃度 |
| 更新频率 | 20% | 最近更新时间 |

### 3. 小红书内容生成

自动生成完整的小红书图文内容：

- 📌 **5 个爆款标题**（情绪型、数字型、对比型、FOMO型）
- 📣 **封面文案**（短而有冲击力）
- 📝 **完整正文**（钩子→功能→理由→人群→评价→互动）
- 🏷️ **10-15 个热门标签**

### 4. 配图自动生成

- 🖼️ **封面图** (1080x1440)
- 📦 **项目缩略图** (600x400)
- 📊 **对比网格图**
- 🎨 **AI 绘图提示词**

## ⏰ 定时任务设置

### Windows

```powershell
schtasks /create /tn "GitHubAITrendingBot" /tr "python D:\path\to\main.py" /sc daily /st 09:00
```

### macOS/Linux

```bash
# 编辑 crontab
crontab -e

# 添加行
0 9 * * * cd /path/to/XHS-AI-GitHub && python3 bot/scripts/main.py
```

### WorkBuddy 自动化

在 WorkBuddy 中创建每日自动化任务：
- 触发：每天 09:00
- 执行：`python /path/to/bot/scripts/main.py`

## 💡 使用示例

### 输入

```
帮我写一篇小红书推荐 https://github.com/xxx/yyy 项目
```

### 输出

```markdown
📌 爆款标题（5 选 1）：
1. 救命！这个 AI 工具也太好用了吧😭
2. 5 分钟搞定 XX，GitHub 10k+ star 神器绝了
...

📣 封面文案：
用了再也回不去的 AI 神器 ⚡️

📝 完整正文：
[小红书图文内容]

🏷️ 热门标签：
#AI #人工智能 #GitHub #效率工具 ...
```

## 🔧 配置

### GitHub Token（可选）

设置环境变量避免 API 限流：

```bash
# Linux/macOS
export GITHUB_TOKEN="your_github_token"

# Windows
set GITHUB_TOKEN=your_github_token
```

### 自定义参数

编辑 `bot/scripts/main.py`：
- `content_count`: 生成的项目数量（默认 3）
- `generate_images`: 是否生成配图（默认 True）

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 PR！

## ⭐ 支持

如果这个项目对你有帮助，请 star 支持一下！

---

Made with ❤️ for AI content creators
