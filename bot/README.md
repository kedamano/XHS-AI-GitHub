# GitHub AI Trending 内容创作自动化

> 🤖 自动抓取 GitHub 趋势 AI 项目，生成小红书爆款内容

## 功能特点

| 功能 | 说明 |
|------|------|
| 🔍 自动抓取 | 每日自动抓取 GitHub 趋势 AI 项目 |
| 📊 热度评分 | 智能评分系统，筛选最优质项目 |
| ✍️ 内容生成 | 自动生成小红书风格的爆款内容 |
| 🖼️ 配图生成 | 自动生成封面图和项目缩略图 |
| ⏰ 定时任务 | 支持每日自动执行 |
| 📦 多项目合集 | 支持生成 Top 3/5/10 合集 |

## 项目结构

```
github-trending-bot/
├── scripts/
│   ├── main.py              # 主运行脚本
│   ├── fetch_trending.py    # GitHub 趋势抓取
│   ├── aggregator.py        # 多项目合集生成器
│   └── image_generator.py   # 配图生成器
├── data/                    # 数据存储
├── output/                  # 输出目录
├── logs/                    # 日志目录
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
pip install requests pillow
```

### 2. 运行一次测试

```bash
cd scripts
python main.py
```

### 3. 设置定时任务

#### Windows (任务计划程序)

```powershell
# 创建每日 9:00 执行的任务
schtasks /create /tn "GitHub AI Trending Bot" /tr "python D:\path\to\scripts\main.py" /sc daily /st 09:00
```

#### macOS/Linux (crontab)

```bash
# 编辑 crontab
crontab -e

# 添加每日 9:00 执行的任务
0 9 * * * cd /path/to/github-trending-bot && python3 scripts/main.py >> logs/cron.log 2>&1
```

## 使用方法

### 基本用法

```bash
# 生成 Top 3 合集
python main.py

# 生成 Top 5 合集
python main.py --count 5

# 跳过图片生成
python main.py --no-image

# 查看最近的输出
python main.py --list
```

### 单独使用各模块

```python
# 抓取趋势
from fetch_trending import GitHubTrendingFetcher
fetcher = GitHubTrendingFetcher()
repos = fetcher.fetch_trending_repos(language='python')

# 生成合集
from aggregator import XHSAggregator
agg = XHSAggregator()
content = agg.generate_aggregated_content(repos[:3])

# 生成配图
from image_generator import ImageGenerator
img_gen = ImageGenerator()
img_gen.create_cover_image("标题", "副标题")
```

## 热度评分系统

项目热度评分基于以下维度：

| 维度 | 权重 | 说明 |
|------|------|------|
| Stars 数量 | 40% | 绝对受欢迎程度 |
| Forks 数量 | 15% | 社区参与度 |
| Watchers | 10% | 关注度 |
| Issues 活跃度 | 15% | 开发活跃度 |
| 更新频率 | 20% | 最近更新时间 |

### 评分公式

```
hot_score = min(stars/10000, 1) * 40
          + min(forks/1000, 1) * 15
          + min(watchers/1000, 1) * 10
          + min(issues/100, 1) * 15
          + recency_factor * 20
```

## AI 项目筛选标准

### 包含关键词

- AI 相关：ai, gpt, llm, chatgpt, agent, rag
- 工具类：copilot, assistant, automation
- 生成式：aigc, generative, diffusion

### 排除关键词

- 基础设施：kubernetes, docker, aws
- 监控运维：prometheus, grafana, monitoring
- CI/CD：ci-cd, pipeline

## 输出示例

### 生成的内容结构

```
📌 爆款标题（5 选 1）
1. 救命！挖到 3 个 GitHub 神器，每一个都巨好用 😭
2. ...

📣 封面文案
GitHub AI 神器合集 🎯

📝 完整正文
[小红书风格正文，包含：]
- 开头钩子
- 项目介绍（3 个）
- 推荐理由
- 使用建议
- 互动引导

🏷️ 热门标签
#AI #人工智能 #GitHub #效率神器 ...
```

### 生成的配图

- `cover_YYYYMMDD_HHMMSS.png` - 封面图 (1080x1440)
- `thumb_project-name_YYYYMMDD.png` - 项目缩略图 (600x400)
- `comparison_YYYYMMDD_HHMMSS.png` - 对比网格图

## 自定义配置

### 修改评分权重

编辑 `scripts/fetch_trending.py` 中的 `_calculate_hot_score` 方法：

```python
def _calculate_hot_score(self, repo: Dict) -> float:
    score = (
        min(stars / 10000, 1) * 50,      # 调整 Stars 权重
        min(forks / 1000, 1) * 20,       # 调整 Forks 权重
        # ...
    )
```

### 修改标题模板

编辑 `scripts/aggregator.py` 中的 `TITLE_TEMPLATES`：

```python
TITLE_TEMPLATES = [
    "你的新模板 {count} ...",
    # ...
]
```

## 工作流程

```
┌─────────────┐
│  定时触发    │  (每天 9:00)
└──────┬──────┘
       ▼
┌─────────────┐
│ 1. 抓取趋势  │  GitHub API
└──────┬──────┘
       ▼
┌─────────────┐
│ 2. AI 评分   │  热度计算
└──────┬──────┘
       ▼
┌─────────────┐
│ 3. 筛选 Top3 │  多样性保证
└──────┬──────┘
       ▼
┌─────────────┐
│ 4. 生成内容  │  小红书风格
└──────┬──────┘
       ▼
┌─────────────┐
│ 5. 生成配图  │  封面+缩略图
└──────┬──────┘
       ▼
┌─────────────┐
│ 6. 输出报告  │  保存文件
└─────────────┘
```

## 常见问题

### Q: GitHub API 限流怎么办？

A: 设置 `GITHUB_TOKEN` 环境变量：
```bash
export GITHUB_TOKEN="your_token_here"
```

### Q: 生成的图片显示中文乱码？

A: 确保系统安装了中文字体，Windows 通常自带 `msyh.ttc`

### Q: 如何修改生成内容的风格？

A: 编辑 `scripts/aggregator.py` 中的各个 `_generate_*` 方法

## 许可证

MIT License

## 作者

Created with ❤️ for AI content creators
