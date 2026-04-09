---
name: oasys-redbook
description: 基于 OASYS OA 办公自动化系统的科技简约风小红书配图生成器。使用深色科技风格，自动生成涵盖项目介绍、快速开始、AI助手、核心模块、技术架构、配置说明等6个主题的系列配图。
---

# OASYS 小红书配图生成器

基于 OASYS 智能 OA 办公自动化系统，生成**科技简约深色风**小红书配图。

## 使用方法

### 方式一：批量生成（推荐）

运行批量脚本，一次生成 **6 张核心配图**：

```bash
cd skills/oasys-redbook/scripts
python batch_oasys.py
```

**输出文件**（保存到 `scripts/output/`）：

| 文件 | 主题色 | 内容 |
|------|--------|------|
| 01_intro.jpg | 蓝黑科技 | OASYS 是什么 + 核心亮点 |
| 02_quickstart.jpg | 紫黑极客 | 环境要求 + 部署5步骤 |
| 03_ai.jpg | 青黑赛博 | AI助手功能详解 |
| 04_modules.jpg | 橙黑工业 | 10大核心模块 |
| 05_architecture.jpg | 绿黑终端 | 技术架构图 |
| 06_config.jpg | 玫红极简 | 配置说明 |

### 方式二：自定义单图

```bash
python generate_cover.py --title "标题" --subtitle "副标题" --content "正文内容" --theme 0 --output my.jpg
```

**参数说明**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--title` | 是 | 主标题 |
| `--subtitle` | 否 | 副标题 |
| `--content` | 否 | 正文，多行用 `\|` 分隔 |
| `--theme` | 否 | 主题色 0-5，默认随机 |
| `--output` | 否 | 输出文件名，默认 `oasys_cover.jpg` |

### 方式三：使用内置模板

```bash
# 生成 AI 助手主题图
python batch_oasys.py --template ai

# 生成技术架构主题图
python batch_oasys.py --template arch
```

## 主题色说明

| 序号 | 主题 | 配色风格 | 适用场景 |
|------|------|---------|---------|
| 0 | 蓝黑科技 | 深蓝+青色 | 封面、项目介绍 |
| 1 | 紫黑极客 | 深紫+粉色 | 高级功能、技术细节 |
| 2 | 绿黑终端 | 深绿+翠绿 | 部署、环境配置 |
| 3 | 橙黑工业 | 深橙+金黄 | 模块功能、分类展示 |
| 4 | 青黑赛博 | 深青+亮青 | AI功能、创新特性 |
| 5 | 玫红极简 | 深红+玫粉 | 快捷操作、注意事项 |

## OASYS 项目简介

OASYS（OASYS - Office Automation System）是集成智谱AI的智能OA办公自动化系统。

**技术栈**：Spring Boot 1.5.6 + Java 8 + MySQL 8.0 + 智谱AI GLM-4

**核心模块**：用户管理、考勤管理、流程管理、任务管理、邮件管理、日程管理、通讯录、文件管理、讨论区、公告通知、AI助手

**仓库地址**：https://github.com/kedamano/oasys

## 输出规格

- 尺寸：1080 x 1440（小红书标准竖图）
- 格式：JPEG
- 质量：96%
- 风格：科技简约深色风（深色背景 + 网格线 + 代码块 + 标签栏）

## 依赖

```bash
pip install Pillow
```

已在 scripts/requirements.txt 中声明。

## 文件结构

```
oasys-redbook/
├── SKILL.md                  # 本文件
├── _meta.json                # Skill 元数据
├── _skillhub_meta.json       # SkillHub 配置
├── README.md                 # 详细文档
├── scripts/
│   ├── generate_cover.py     # 单图生成器（科技风）
│   ├── batch_oasys.py        # 批量生成器（6张核心图）
│   ├── tech_draw.py          # 科技风绘图核心引擎
│   ├── requirements.txt     # Python 依赖
│   └── output/               # 生成图片输出目录
└── references/
    ├── overview.md           # 项目概览
    ├── modules.md            # 核心模块详解
    ├── ai_assistant.md       # AI助手功能说明
    ├── tech_stack.md         # 技术栈详解
    └── config_guide.md       # 配置指南
```
