#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书 AI 博主 Pipeline - 融合版
xhs-ai-blogger + oasys-redbook 配图生成
一次运行生成：内容.md + 配图.jpg

用法:
    python xhs_blogger_pipeline.py --project "项目名称" --repo "GitHub仓库URL" 
                                   --description "项目描述" --features "功能1|功能2|功能3"
                                   --output "输出目录"

示例:
    python xhs_blogger_pipeline.py --project "ColaOS" --repo "https://github.com/xxx/ColaOS"
        --description "人类第一个有灵魂的操作系统" 
        --features "直接操控电脑|原生记忆|主动服务|多模态生成"
        --output "./output"
"""

import os
import sys
import json
import argparse
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tech_draw import gen_card, THEMES

# ─── 配置 ────────────────────────────────────────────
DEFAULT_TAGS = "#AI #人工智能 #AI工具 #GitHub #开源 #效率工具 #学习必备 #ChatGPT #AI助手 #黑科技"


def generate_title(project_name, description):
    """生成爆款标题（无 emoji 版本）"""
    templates = [
        f"{project_name}深度解析 | 这才是真正的AI神器",
        f"救命！{project_name}也太好用了吧",
        f"用了{project_name}，效率直接翻倍",
        f"GitHub爆款！{project_name}让我彻底戒不掉",
        f"{project_name}深度测评 | 真的绝绝子",
    ]
    return templates


def generate_content(project_name, repo_url, description, features, tags=None):
    """生成小红书内容（无 emoji 版本）"""
    if tags is None:
        tags = DEFAULT_TAGS
    
    feature_list = [f.strip() for f in features.split('|') if f.strip()]
    
    # 生成核心功能部分（无 emoji）
    core_features = []
    for i, feat in enumerate(feature_list[:5]):
        core_features.append(f"- {feat}")
    
    content = f"""姐妹们！我最近发现了一个超级炸裂的项目，必须跟你们分享！

这就是 **{project_name}** —— {description}

【核心功能】
{chr(10).join(core_features)}

【为什么选择它】
- 开源免费，社区活跃
- 简单易用，快速上手
- 功能强大，满足多种场景

GitHub: {repo_url}

用了 {project_name}，你会发现效率提升不是一点点！

你们有没有用过类似的 AI 工具？
评论区告诉我，一起交流！

{tags}
"""
    return content.strip()


def extract_github_path(repo_url):
    """从 GitHub URL 提取简洁的仓库路径"""
    if not repo_url:
        return ""
    # 处理各种 GitHub URL 格式
    if "github.com/" in repo_url:
        parts = repo_url.split("github.com/")[-1].rstrip('/')
        # 去掉 .git 后缀
        parts = parts.replace('.git', '')
        return parts
    return repo_url


def generate_pages_data(project_name, description, features, tags=None, repo_url=None):
    """生成6页配图数据"""
    if tags is None:
        tags = DEFAULT_TAGS.replace(' ', ' #')
    
    feature_list = [f.strip() for f in features.split('|') if f.strip()]
    github_path = extract_github_path(repo_url)
    
    # 使用 Star 文字替代 emoji，避免字体问题
    star_text = "[ Star 支持开源 ]"
    
    return [
        {
            "theme_idx": 0,  # 蓝黑科技
            "kicker": "GitHub 开源项目",
            "title": project_name,
            "subtitle": description,
            "sections": [
                {"type": "label", "text": " 核心亮点"},
                {"type": "bullet", "items": feature_list[:5]},
                {"type": "divider"},
                {"type": "text", "lines": [f"GitHub: {github_path}"]},
            ],
            "footer_tags": tags.replace(' ', ' #') if isinstance(tags, str) else " ".join([f"#{t.strip('#')}" for t in tags.split()])
        },
        {
            "theme_idx": 1,  # 紫黑极客
            "kicker": "快速上手",
            "title": f"快速部署\n{project_name}",
            "sections": [
                {"type": "label", "text": " 部署步骤"},
                {"type": "kv", "items": [
                    ["Step 1 ", "访问 GitHub 仓库"],
                    ["Step 2 ", "查看 README 文档"],
                    ["Step 3 ", "开始使用"],
                ]},
                {"type": "divider"},
                {"type": "label", "text": " 项目地址"},
                {"type": "code", "lines": [github_path]},
            ],
            "footer_tags": tags.replace(' ', ' #') if isinstance(tags, str) else " ".join([f"#{t.strip('#')}" for t in tags.split()])
        },
        {
            "theme_idx": 4,  # 青黑赛博
            "kicker": "核心能力",
            "title": "核心能力\n全景一览",
            "sections": [
                {"type": "bullet", "items": feature_list[:5]},
                {"type": "divider"},
                {"type": "label", "text": " 技术特点"},
                {"type": "text", "lines": ["支持多平台", "简单易用", "持续更新"]},
            ],
            "footer_tags": tags.replace(' ', ' #') if isinstance(tags, str) else " ".join([f"#{t.strip('#')}" for t in tags.split()])
        },
        {
            "theme_idx": 3,  # 橙黑工业
            "kicker": "功能详解",
            "title": "功能模块\n深度解析",
            "sections": [
                {"type": "label", "text": " 详细功能"},
                {"type": "bullet", "items": feature_list[:5]},
            ],
            "footer_tags": tags.replace(' ', ' #') if isinstance(tags, str) else " ".join([f"#{t.strip('#')}" for t in tags.split()])
        },
        {
            "theme_idx": 2,  # 绿黑终端
            "kicker": "使用体验",
            "title": "真实体验\n用户视角",
            "sections": [
                {"type": "text", "lines": [
                    "用了 3 个月，彻底离不开",
                    "效率提升不是一点点",
                    "真的绝绝子！",
                ]},
                {"type": "divider"},
                {"type": "label", "text": " 用户评价"},
                {"type": "text", "lines": [star_text]},
            ],
            "footer_tags": tags.replace(' ', ' #') if isinstance(tags, str) else " ".join([f"#{t.strip('#')}" for t in tags.split()])
        },
        {
            "theme_idx": 5,  # 玫红极简
            "kicker": "赶紧试试",
            "title": f"{project_name}\n等你来探索",
            "sections": [
                {"type": "label", "text": " 立即体验"},
                {"type": "code", "lines": [
                    github_path,
                    "",
                    star_text,
                ]},
                {"type": "divider"},
                {"type": "text", "lines": [
                    "觉得有用就点个 Star 吧！",
                    "你们的支持是我更新的动力",
                ]},
            ],
            "footer_tags": tags.replace(' ', ' #') if isinstance(tags, str) else " ".join([f"#{t.strip('#')}" for t in tags.split()])
        },
    ]


def parse_args():
    parser = argparse.ArgumentParser(description="小红书 AI 博主 Pipeline - 融合版")
    parser.add_argument("--project", "-p", required=True, help="项目名称")
    parser.add_argument("--repo", "-r", required=True, help="GitHub 仓库 URL")
    parser.add_argument("--description", "-d", required=True, help="项目描述")
    parser.add_argument("--features", "-f", required=True, help="核心功能，用 | 分隔")
    parser.add_argument("--tags", "-t", default=DEFAULT_TAGS, help="话题标签，用空格分隔")
    parser.add_argument("--output", "-o", default="./xhs_output", help="输出目录")
    return parser.parse_args()


def main():
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    args = parse_args()
    
    # 创建输出目录
    output_dir = os.path.abspath(args.output)
    os.makedirs(output_dir, exist_ok=True)
    
    project_name = args.project
    
    print("=" * 60)
    print(f"📱 {project_name} 小红书内容生成")
    print("=" * 60)
    
    # ─── 第一步：生成标题 ───
    print("\n[1/4] 生成爆款标题...")
    titles = generate_title(project_name, args.description)
    print(f"生成 {len(titles)} 个备选标题:")
    for i, title in enumerate(titles, 1):
        print(f"  {i}. {title}")
    
    # ─── 第二步：生成正文 ───
    print("\n[2/4] 生成正文内容...")
    content = generate_content(
        project_name, 
        args.repo, 
        args.description, 
        args.features,
        args.tags
    )
    
    # ─── 第三步：保存内容文件 ───
    print("\n[3/4] 保存内容文档...")
    content_file = os.path.join(output_dir, f"{project_name}_内容.md")
    
    # 构建完整的 Markdown 文件
    main_title = titles[0]
    md_content = f"""# {main_title}

## 项目信息

- 项目名称: {project_name}
- GitHub: {args.repo}
- 描述: {args.description}

---

## 正文内容

{content}

---

## 配图预览

| 页码 | 主题 |
|:---:|:---:|
| 第1页 | 项目介绍（蓝黑科技） |
| 第2页 | 快速开始（紫黑极客） |
| 第3页 | 核心能力（青黑赛博） |
| 第4页 | 功能详解（橙黑工业） |
| 第5页 | 使用体验（绿黑终端） |
| 第6页 | 结尾引导（玫红极简） |

---

*由 xhs-ai-blogger Pipeline 生成 | {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
    
    with open(content_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"[OK] {content_file}")
    
    # ─── 第四步：生成配图 ───
    print("\n[4/4] 生成科技风配图...")
    pages_data = generate_pages_data(
        project_name,
        args.description,
        args.features,
        args.tags,
        args.repo  # 传入 repo URL
    )
    
    # 生成6张配图
    total = len(pages_data)
    for i, page_cfg in enumerate(pages_data, 1):
        page_cfg["page_num"] = i
        page_cfg["total"] = total
        
        output_path = os.path.join(output_dir, f"{project_name}_page_{i:02d}.jpg")
        gen_card(page_cfg, output_path)
    
    # ─── 完成 ───
    print("\n" + "=" * 60)
    print(f"✅ 生成完成！")
    print("=" * 60)
    print(f"\n📁 输出目录: {output_dir}")
    print(f"\n📄 内容文档: {project_name}_内容.md")
    print(f"🖼️ 配图文件:")
    for i in range(1, total + 1):
        print(f"   - {project_name}_page_{i:02d}.jpg")
    print()


if __name__ == "__main__":
    main()
