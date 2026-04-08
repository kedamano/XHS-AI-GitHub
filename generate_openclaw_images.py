# -*- coding: utf-8 -*-
"""为 openclaw 项目生成配图"""

import sys
sys.path.insert(0, r'C:\Users\lcl13\.workbuddy\skills\小红书配图生成器\scripts')

from image_generator_v6 import generate_multi_page_v6, generate_cover_v6
import os

output_dir = r"d:\work\项目\XHS-AI-GitHub-每日创作助手"

# 封面
print("Generating cover...")
generate_cover_v6(
    "openclaw\n深度解析",
    "Your own personal AI assistant",
    os.path.join(output_dir, "openclaw_cover.png")
)

# 内容页数据
pages = [
    {
        "title": "架构概览：模块化设计",
        "image_type": "architecture",
        "content": {
            "components": [
                {"name": "核心引擎", "desc": "LLM 接口抽象层"},
                {"name": "插件系统", "desc": "功能扩展机制"},
                {"name": "记忆模块", "desc": "上下文管理"},
                {"name": "工具层", "desc": "系统交互接口"},
            ]
        },
        "explanation": "OpenClaw 采用插件化架构，核心引擎只负责 LLM 调用和对话管理，所有具体功能都通过插件实现。这种设计让系统高度可扩展，新增功能只需开发插件。"
    },
    {
        "title": "多模型支持：统一接口",
        "image_type": "tools",
        "content": {
            "steps": [
                "OpenAI API (GPT-4/GPT-3.5)",
                "Anthropic API (Claude)",
                "本地模型 (Ollama/LM Studio)",
                "自定义 API 端点",
            ]
        },
        "explanation": "通过统一的抽象接口，OpenClaw 可以无缝切换不同的 LLM 提供商。用户可以根据需求选择性价比最高的模型：日常对话用 GPT-3.5，复杂任务用 GPT-4，本地部署用 Llama2。"
    },
    {
        "title": "记忆系统：持久化上下文",
        "image_type": "memory",
        "content": {
            "points": [
                "会话历史：自动保存完整对话",
                "知识库：用户可上传文档作为参考",
                "偏好设置：记住用户的习惯和偏好",
            ]
        },
        "explanation": "OpenClaw 的记忆系统分为三层：短期记忆管理当前会话上下文，中期记忆存储跨会话的信息，长期记忆保存用户的偏好设置和知识库。这种设计让 AI 能真正'认识'用户。"
    },
    {
        "title": "安全机制：隐私优先设计",
        "image_type": "security",
        "content": {
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
            ]
        },
        "explanation": "OpenClaw 的设计理念是'你的数据就是你的数据'。默认情况下，所有对话数据都存储在本地，只有在用户明确授权时才会调用云端 API。"
    },
    {
        "title": "插件系统：无限扩展",
        "image_type": "code",
        "content": {
            "title": "插件开发示例",
            "lines": [
                "// 网页搜索插件",
                "export default {",
                "  name: 'web-search',",
                "  async execute(query) {",
                "    return results;",
                "  }",
                "}",
                "",
                "// 文件处理插件",
                "export default {",
                "  name: 'file-tool',",
                "  actions: ['read','write','edit']",
                "}",
            ]
        },
        "explanation": "OpenClaw 的插件系统采用类似 VSCode 扩展的模式，任何开发者都可以创建插件来扩展功能。官方提供了核心插件，社区还在持续贡献更多。"
    },
    {
        "title": "使用流程：三步启动",
        "image_type": "flowchart",
        "content": {
            "steps": [
                "安装 OpenClaw (npm/pip/homebrew)",
                "配置 API Key (可选本地模型)",
                "启动对话 (openclaw cli)",
            ]
        },
        "explanation": "OpenClaw 的安装和使用非常简洁。对于开发者用户，只需几行命令就能启动；对于普通用户，也有图形界面版本可选。这种低门槛的设计让任何人都能快速拥有自己的 AI 助手。"
    }
]

print("Generating 6 pages...")
paths = generate_multi_page_v6(
    "openclaw",
    "Your own personal AI assistant",
    pages,
    output_dir
)

print(f"\nDone! Generated {len(paths)} images:")
for p in paths:
    print(f"  - {p}")
