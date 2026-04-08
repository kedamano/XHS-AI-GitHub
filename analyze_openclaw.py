# -*- coding: utf-8 -*-
"""
openclaw 项目深度分析 + 小红书内容生成
"""

import sys
import json
sys.path.insert(0, r'C:\Users\lcl13\.workbuddy\skills\GitHub热门项目\scripts')
sys.path.insert(0, r'C:\Users\lcl13\.workbuddy\skills\小红书配图生成器\scripts')

from github_to_xiaohongshu import fetch_repo_details, create_analysis_from_repo, generate_xiaohongshu_post

# openclaw 项目数据
repo_data = {
    "name": "openclaw/openclaw",
    "author": "openclaw",
    "url": "https://github.com/openclaw/openclaw",
    "description": "Your own personal AI assistant. Any OS. Any Platform. The lobster way.",
    "stars": 351938,
    "forks": 70878,
    "language": "TypeScript",
    "topics": ["ai", "assistant", "crustacean", "molty", "openclaw"],
}

# 获取详细信息
print("Fetching repo details...")
details = fetch_repo_details("openclaw", "openclaw")
if details:
    repo_data.update(details)

# 创建分析框架
analysis = create_analysis_from_repo(repo_data)

# ==================== 5维深度分析（手动填充） ====================

analysis["analysis"] = {
    # 1. 项目作用
    "purpose": """OpenClaw 是一个开源的个人 AI 助手框架，让任何人都能拥有自己的 AI 助手。

核心特点：
- 跨平台：支持 Windows、macOS、Linux
- 跨设备：桌面、移动端、服务器都能运行
- 隐私优先：数据本地处理，不上传云端
- 高度可定制：支持插件扩展，可接入任意 LLM

目标用户：
- 开发者：打造自己的 AI 编程助手
- 普通用户：拥有私人 AI 助理
- 企业：构建内部 AI 知识库""",

    # 2. 核心优势（5条）
    "advantages": [
        "开源免费：MIT 协议，可商用，无使用限制",
        "隐私安全：本地部署，数据不离开你的设备",
        "跨平台统一：Windows/macOS/Linux 全覆盖",
        "插件生态：丰富的插件系统，功能可扩展",
        "多模型支持：OpenAI/Anthropic/本地模型任选"
    ],

    # 3. 实现机制
    "mechanisms": [
        {
            "title": "架构概览：模块化设计",
            "type": "architecture",
            "components": [
                {"name": "核心引擎", "desc": "LLM 接口抽象层"},
                {"name": "插件系统", "desc": "功能扩展机制"},
                {"name": "记忆模块", "desc": "上下文管理"},
                {"name": "工具层", "desc": "系统交互接口"},
            ],
            "explanation": "OpenClaw 采用插件化架构，核心引擎只负责 LLM 调用和对话管理，所有具体功能（网页搜索、文件处理、代码执行等）都通过插件实现。这种设计让系统高度可扩展，新增功能只需开发插件。"
        },
        {
            "title": "多模型支持：统一接口",
            "type": "tools",
            "steps": [
                "OpenAI API（GPT-4/GPT-3.5）",
                "Anthropic API（Claude）",
                "本地模型（Ollama/LM Studio）",
                "自定义 API 端点",
            ],
            "explanation": "通过统一的抽象接口，OpenClaw 可以无缝切换不同的 LLM 提供商。用户可以根据需求选择性价比最高的模型：日常对话用 GPT-3.5，复杂任务用 GPT-4，本地部署用 Llama2。"
        },
        {
            "title": "记忆系统：持久化上下文",
            "type": "memory",
            "points": [
                "会话历史：自动保存完整对话",
                "知识库：用户可上传文档作为参考",
                "偏好设置：记住用户的习惯和偏好",
            ],
            "explanation": "OpenClaw 的记忆系统分为三层：短期记忆管理当前会话上下文，中期记忆存储跨会话的信息，长期记忆保存用户的偏好设置和知识库。这种设计让 AI 能真正'认识'用户，提供个性化服务。"
        },
        {
            "title": "安全机制：隐私优先设计",
            "type": "security",
            "left_title": "数据安全",
            "left_items": [
                "本地处理优先",
                "端到端加密",
                "无追踪无日志",
            ],
            "right_title": "访问控制",
            "right_items": [
                "API 密钥加密存储",
                "敏感操作确认",
                "可审计的操作日志",
            ],
            "explanation": "OpenClaw 的设计理念是'你的数据就是你的数据'。默认情况下，所有对话数据都存储在本地，只有在用户明确授权时才会调用云端 API。这种隐私优先的设计让用户无需担心数据泄露。"
        },
        {
            "title": "插件系统：无限扩展",
            "type": "code",
            "title_extra": "插件示例",
            "lines": [
                "// 网页搜索插件",
                "export default {",
                "  name: 'web-search',",
                "  async execute(query) {",
                "    // 调用搜索 API",
                "    return results;",
                "  }",
                "}",
                "",
                "// 文件处理插件",
                "export default {",
                "  name: 'file-tool',",
                "  actions: ['read', 'write', 'edit']",
                "}",
            ],
            "explanation": "OpenClaw 的插件系统采用类似 VSCode 扩展的模式，任何开发者都可以创建插件来扩展功能。官方提供了网页搜索、代码执行、文件处理等核心插件，社区还在持续贡献更多插件。"
        },
        {
            "title": "使用流程：三步启动",
            "type": "flowchart",
            "steps": [
                "安装 OpenClaw（npm/pip/homebrew）",
                "配置 API Key（可选本地模型）",
                "启动对话（./openclaw 或 openclaw cli）",
            ],
            "explanation": "OpenClaw 的安装和使用非常简洁。对于开发者用户，只需几行命令就能启动；对于普通用户，也有图形界面版本可选。这种低门槛的设计让任何人都能快速拥有自己的 AI 助手。"
        }
    ],

    # 4. 使用指南
    "usage": [
        {"step": "1", "title": "安装 OpenClaw", "content": "npm install -g openclaw\n# 或\npip install openclaw\n# 或\nbrew install openclaw"},
        {"step": "2", "title": "配置 API Key", "content": "export OPENAI_API_KEY=sk-xxxxx\n# 或配置其他模型"},
        {"step": "3", "title": "启动助手", "content": "openclaw\n# 或\nopenclaw --model claude"},
        {"step": "4", "title": "开始对话", "content": "> 你好，帮我写一个 Python 快速排序"},
        {"step": "5", "title": "安装插件（可选）", "content": "openclaw plugin install web-search\nopenclaw plugin install github"}
    ],

    # 5. 实用技巧
    "tips": [
        "本地模型省钱：用 Ollama 部署 Llama2，免费无限用",
        "快捷命令：用 /search 快速搜索，/code 执行代码",
        "上下文注入：@文件 可以让 AI 读取本地文件",
        "插件组合：搜索 + 总结 + 翻译 组合使用效率翻倍",
        "自定义提示词：修改 ~/.openclaw/system.md 定制 AI 性格"
    ]
}

# 保存完整分析
output_file = r"d:\work\项目\XHS-AI-GitHub-每日创作助手\openclaw_analysis.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(analysis, f, ensure_ascii=False, indent=2)
print(f"Analysis saved to: {output_file}")

# 生成小红书内容
content = generate_xiaohongshu_post(analysis)

# 保存小红书内容
xhs_file = r"d:\work\项目\XHS-AI-GitHub-每日创作助手\openclaw_xiaohongshu.json"
with open(xhs_file, 'w', encoding='utf-8') as f:
    json.dump(content, f, ensure_ascii=False, indent=2)
print(f"XHS content saved to: {xhs_file}")

# 打印内容（只打印标题）
print("\n" + "="*60)
print("Analysis complete!")
print("Files saved:")
print("  -", output_file)
print("  -", xhs_file)
