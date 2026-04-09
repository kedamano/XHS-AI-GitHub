---
name: xhs-ai-blogger
description: 将 GitHub AI 项目转化为小红书爆款种草内容 + 科技风配图。当用户要求生成小红书帖子、推荐 GitHub AI 项目、写 AI 种草内容时使用此技能。一键生成：内容.md + 配图.jpg。
---

# 小红书 AI 博主技能（融合版）

## 概述

这是一个**一体化**小红书内容创作 Pipeline，整合了：
- **xhs-ai-blogger**: 爆款内容生成
- **oasys-redbook**: 科技简约风配图生成（6种主题色）

**一次运行，同时输出：**
- 📄 `项目名_内容.md` - 完整小红书内容文档
- 🖼️ `项目名_page_01~06.jpg` - 6张科技风配图

## 触发条件

当用户说以下内容时使用此技能：
- "帮我写一篇小红书"
- "生成 AI 项目种草内容"
- "推荐一个 GitHub AI 项目"
- "写一个 AI 工具分享笔记"
- 任何涉及 GitHub AI 项目 + 小红书内容的请求

## 快速使用

### 命令行方式

```bash
python C:/Users/lcl13/.workbuddy/skills/xhs-ai-blogger/scripts/xhs_blogger_pipeline.py \
    --project "项目名称" \
    --repo "https://github.com/xxx/repo" \
    --description "项目一句话描述" \
    --features "功能1|功能2|功能3|功能4|功能5" \
    --tags "#AI #开源 #效率工具" \
    --output "./output"
```

### 示例

```bash
python C:/Users/lcl13/.workbuddy/skills/xhs-ai-blogger/scripts/xhs_blogger_pipeline.py ^
    --project "ColaOS" ^
    --repo "https://github.com/xxx/ColaOS" ^
    --description "人类第一个有灵魂的操作系统" ^
    --features "直接操控电脑|原生记忆|主动服务|多模态生成|灵魂共鸣" ^
    --output "./ColaOS_output"
```

## 配图主题色

| 主题 | 配色 | 用途 |
|:---:|:---:|:---:|
| 0 | 蓝黑科技 | 封面/项目介绍 |
| 1 | 紫黑极客 | 快速开始/部署 |
| 2 | 绿黑终端 | 使用体验/终端 |
| 3 | 橙黑工业 | 功能模块 |
| 4 | 青黑赛博 | AI功能/核心能力 |
| 5 | 玫红极简 | 注意事项/结尾 |

## 内容生成规范

### 爆款标题公式

**情绪型：**
- "救命！这个 AI 工具也太好用了吧😭"
- "姐妹们！这个让我效率翻倍的 AI 神器必须知道"

**数字型：**
- "5 分钟搞定 XX，这个 GitHub 10k+ star 的 AI 项目绝了"

**FOMO 型：**
- "全网都在找的 AI 工具，我给你们扒到了"

### 正文结构

```
【开头钩子】- 提出痛点或场景
【项目介绍】- 口语化介绍
【核心功能】- 3-5条，用 emoji 标记
【推荐理由】- 为什么选这个
【互动引导】- 引导评论
```

### 标签策略

**核心标签（必选）：**
- #AI #人工智能 #AI工具 #GitHub #开源

**领域标签（根据项目）：**
- #ChatGPT #AI助手 #AI效率 #AI办公

**趋势标签：**
- #2025AI #黑科技 #神器推荐

## 质量检查

- [ ] 标题有情绪/数字/对比
- [ ] 封面文案短而有冲击力
- [ ] 正文口语化，朗读顺口
- [ ] 功能介绍对普通人有价值
- [ ] 有个人体验/评价
- [ ] 有互动引导
- [ ] 标签覆盖核心关键词
