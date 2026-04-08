# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, r'C:\Users\lcl13\.workbuddy\skills\小红书配图生成器\scripts')
from image_generator_v6 import generate_multi_page_v6

pages = [
    {
        'title': 'Agentic Loop：流式智能体循环',
        'image_type': 'flowchart',
        'content': {
            'steps': [
                '用户输入：重构用户认证模块',
                '并行加载上下文（Git/CLAUDE.md）',
                'LLM 流式推理，边生成边执行',
                '工具并行调用（Grep/Glob/Read）',
                '结果聚合 -> 继续推理 -> 完成'
            ]
        },
        'explanation': '传统AI助手采用生成-执行串行模式，Claude Code 的创新在于流式推理：当 LLM 生成工具调用时立即执行，无需等待完整响应。这种设计将延迟从完整生成时间+执行时间降低到首 token 时间+增量执行时间，实现真正的交互式编程体验。'
    },
    {
        'title': '多智能体：三层协作架构',
        'image_type': 'architecture',
        'content': {
            'components': [
                {'name': '代码探索者', 'desc': '文件搜索和读取'},
                {'name': '代码架构师', 'desc': '代码分析和设计'},
                {'name': '测试工程师', 'desc': '测试用例生成'},
            ]
        },
        'explanation': 'Claude Code 的多智能体系统通过分叉-并行-合并模式实现高效协作。主实例通过 KV Cache 分叉创建子实例，各实例并行工作，共享主实例的上下文。Git Worktree 技术确保多个智能体不会产生文件冲突，实现真正的并行编程辅助。'
    },
    {
        'title': '工具系统：40+ 工具的编排',
        'image_type': 'tools',
        'content': {
            'steps': [
                '自然语言 -> 意图识别',
                'BashTool（沙箱化执行）',
                'FileWriteTool（差异优化）',
                'Grep/Glob（结构化搜索）',
                'LSP 集成（代码结构）',
                '网络请求（安全沙箱）'
            ]
        },
        'explanation': 'Claude Code 的工具系统采用统一的接口抽象层，通过 MCP 协议动态发现和调用外部工具。工具编排器负责意图识别、参数提取、结果解析。沙箱化的 BashTool 限制文件操作范围，FileWriteTool 采用 diff 算法最小化变更，Grep/Glob 提供结构化的代码搜索能力。'
    },
    {
        'title': '记忆系统：三层持久化架构',
        'image_type': 'memory',
        'content': {
            'points': [
                'MEMORY.md 作为主索引文件',
                '按需加载的主题文件（auth.md/api.md）',
                '完整会话记录，可搜索历史',
                '严格写入纪律，验证后更新'
            ]
        },
        'explanation': 'Claude Code 的记忆系统借鉴了操作系统的内存管理思想：MEMORY.md 如同主索引，按需加载的主题文件如同按页调入的内存，会话记录如同磁盘缓存。这套系统确保 AI 在长程任务中保持上下文连贯，同时避免上下文窗口溢出的问题。'
    },
    {
        'title': '安全机制：五层权限控制',
        'image_type': 'security',
        'content': {
            'left_title': '系统级保护',
            'left_items': [
                'SOC 2 Type 2 认证',
                '管理员强制策略',
                '故障关闭机制',
                '沙箱文件系统隔离'
            ],
            'right_title': '运行时保护',
            'right_items': [
                '默认只读权限',
                '命令黑名单',
                '提示注入检测',
                '网络访问限制'
            ]
        },
        'explanation': 'Claude Code 的安全模型采用最小权限原则：默认状态下只允许读取文件，修改需要显式授权。命令执行在沙箱中进行，危险命令被加入黑名单。提示注入检测机制防止恶意代码利用 AI 传播，安全机制贯穿从系统策略到运行时监控的每个层面。'
    },
    {
        'title': '未发布功能：源码暴露的黑科技',
        'image_type': 'code',
        'content': {
            'title': 'KAIROS / ULTRAPLAN / AUTODREAM',
            'lines': [
                '# KAIROS - 持续运行的后台进程',
                '- 接收周期性 tick 提示',
                '- 订阅 GitHub Webhooks',
                '- 发送推送通知',
                '',
                '# ULTRAPLAN - 远程深度思考',
                '- 卸载到 Opus 4.6 云容器',
                '- 长达 30 分钟深度分析',
                '',
                '# AUTODREAM - 自动化做梦',
                '- 夜间深度探索代码库'
            ]
        },
        'explanation': '源码泄露揭示了 Claude Code 正在开发的多项重磅功能：KAIROS 实现后台持续监控，ULTRAPLAN 将复杂推理卸载到云端 GPU 集群，支持长达 30 分钟的深度思考。AUTODREAM 则让 AI 在夜间主动探索代码库并生成待办事项，这些功能预示着 AI 编程助手的未来形态。'
    }
]

output_dir = r'd:\work\项目\XHS-AI-GitHub-每日创作助手'
paths = generate_multi_page_v6(
    'Claude_Code_Deep',
    '基于 51.2 万行源码的深度技术解析',
    pages,
    output_dir
)
print(f'生成完成！共 {len(paths)} 页')
