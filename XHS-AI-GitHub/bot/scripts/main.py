#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub AI Trending - 小红书内容生成 Pipeline
一键抓取 GitHub Trending AI 项目，生成小红书爆款内容 + 科技风配图

用法:
    python bot/scripts/main.py [--top N] [--output ./output]

示例:
    python bot/scripts/main.py --top 3 --output ./output
"""

import os
import sys
import json
import re
import time
import random
import argparse
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime

# ─── 路径设置（硬编码确保正确） ─────────────────────────
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(_SCRIPT_DIR))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")

# tech_draw.py 的确定路径（基于已知文件结构）
_SKILL_SCRIPTS = os.path.join(PROJECT_ROOT, "..", "skills", "xhs-ai-blogger", "scripts")
_SKILL_SCRIPTS = os.path.normpath(_SKILL_SCRIPTS)
SKILL_DIR = _SKILL_SCRIPTS

# 确保 skill 路径在 sys.path 中
if SKILL_DIR not in sys.path:
    sys.path.insert(0, SKILL_DIR)

# ─── 配置 ───────────────────────────────────────────────
GITHUB_TRENDING_URL = "https://github.com/trending?since=daily"
GITHUB_API_SEARCH = "https://api.github.com/search/repositories"

DEFAULT_TOP_N = 3
DEFAULT_OUTPUT = os.path.join(PROJECT_ROOT, "output")

# 小红书标签 / 话题
DEFAULT_TAGS = "#AI #人工智能 #AI工具 #GitHub #开源 #效率工具 #学习必备 #ChatGPT #AI助手 #黑科技"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
]


def get_random_ua():
    return random.choice(USER_AGENTS)


def fetch_url(url, headers=None, timeout=15):
    """安全地获取 URL 内容"""
    import ssl
    if headers is None:
        headers = {"User-Agent": get_random_ua(), "Accept": "application/json, text/html"}
    req = urllib.request.Request(url, headers=headers)
    
    # 跳过 SSL 证书验证（某些环境需要）
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  请求失败: {url} -> {e}")
        return None


# ─── 第一步：抓取 GitHub Trending ────────────────────────
def fetch_github_trending():
    """从 GitHub Trending 页面抓取今日热门项目"""
    print("\n[1/6] 抓取 GitHub Trending 热门项目...")
    
    html = fetch_url(GITHUB_TRENDING_URL)
    if html:
        repos = parse_trending_html(html)
        if repos:
            print(f"  成功抓取 {len(repos)} 个热门项目")
            return repos
        print("  HTML 解析失败，尝试其他方式...")
    
    # 尝试 GitHub API
    api_repos = fetch_github_api_trending()
    if api_repos:
        return api_repos
    
    # 回退到缓存数据
    cached = load_cached_trending()
    if cached:
        print(f"  使用缓存数据: {len(cached)} 个项目")
        return cached
    
    print("  ❌ 所有方式都失败，无法获取数据")
    return []


def load_cached_trending():
    """加载缓存的 trending 数据"""
    cache_path = os.path.join(PROJECT_ROOT, "..", "github_trending.json")
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            repos = data.get("repos", [])
            # 补充 topics 字段
            for r in repos:
                if "topics" not in r:
                    r["topics"] = []
            return repos
        except Exception:
            pass
    
    # 内嵌备用数据（2026-07-07 GitHub Trending Top 15）
    return [
        {"name": "asgeirtj/system_prompts_leaks", "url": "https://github.com/asgeirtj/system_prompts_leaks", "description": "Extracted system prompts from Anthropic - Claude Fable 5, Opus 4.8, Claude Code, Claude Design. OpenAI - ChatGPT 5.5 Thinking, GPT 5.5 Instant, Codex. Google - Gemini 3.5 Flash, 3.1 Pro.", "stars": 51524, "forks": 8395, "language": "JavaScript", "topics": ["ai", "llm", "prompts"]},
        {"name": "addyosmani/agent-skills", "url": "https://github.com/addyosmani/agent-skills", "description": "Production-grade engineering skills for AI coding agents.", "stars": 70809, "forks": 7676, "language": "Shell", "topics": ["ai", "agents", "coding"]},
        {"name": "ruvnet/RuView", "url": "https://github.com/ruvnet/RuView", "description": "RuView turns commodity WiFi signals into real-time spatial intelligence, vital sign monitoring, and presence detection — all without a single pixel of video.", "stars": 77513, "forks": 10408, "language": "Rust", "topics": ["wifi", "spatial", "ai"]},
        {"name": "Leonxlnx/taste-skill", "url": "https://github.com/Leonxlnx/taste-skill", "description": "Taste-Skill - gives your AI good taste. stops the AI from generating boring, generic slop", "stars": 58926, "forks": 4014, "language": "JavaScript", "topics": ["ai", "quality", "coding"]},
        {"name": "Zackriya-Solutions/meetily", "url": "https://github.com/Zackriya-Solutions/meetily", "description": "Privacy first, AI meeting assistant with 4x faster Parakeet/Whisper live transcription, speaker diarization, and Ollama summarization built on Rust.", "stars": 19377, "forks": 1965, "language": "Rust", "topics": ["ai", "meeting", "transcription"]},
        {"name": "alirezarezvani/claude-skills", "url": "https://github.com/alirezarezvani/claude-skills", "description": "345 Claude Code skills & agent skills & plugins for Claude Code, Codex, Gemini CLI, Cursor, and 8 more coding agents.", "stars": 21150, "forks": 2842, "language": "Python", "topics": ["ai", "agents", "skills"]},
        {"name": "openai/codex-plugin-cc", "url": "https://github.com/openai/codex-plugin-cc", "description": "Use Codex from Claude Code to review code or delegate tasks.", "stars": 26275, "forks": 1573, "language": "JavaScript", "topics": ["ai", "coding", "codex"]},
        {"name": "mvanhorn/last30days-skill", "url": "https://github.com/mvanhorn/last30days-skill", "description": "AI agent skill that researches any topic across Reddit, X, YouTube, HN, Polymarket, and the web.", "stars": 49747, "forks": 4145, "language": "Python", "topics": ["ai", "research", "agents"]},
        {"name": "ogulcancelik/herdr", "url": "https://github.com/ogulcancelik/herdr", "description": "Agent multiplexer that lives in your terminal.", "stars": 12867, "forks": 747, "language": "Rust", "topics": ["ai", "agents", "terminal"]},
        {"name": "bradautomates/claude-video", "url": "https://github.com/bradautomates/claude-video", "description": "Give Claude the ability to watch any video. Downloads, extracts frames, transcribes, hands it all to Claude.", "stars": 4230, "forks": 603, "language": "Python", "topics": ["ai", "video", "claude"]},
        {"name": "karakeep-app/karakeep", "url": "https://github.com/karakeep-app/karakeep", "description": "A self-hostable bookmark-everything app with AI-based automatic tagging and full text search.", "stars": 26892, "forks": 1319, "language": "TypeScript", "topics": ["ai", "bookmarks", "self-hosted"]},
        {"name": "firecrawl/firecrawl", "url": "https://github.com/firecrawl/firecrawl", "description": "The API to search, scrape, and interact with the web at scale.", "stars": 146249, "forks": 8412, "language": "TypeScript", "topics": ["ai", "web", "scraping"]},
        {"name": "steipete/CodexBar", "url": "https://github.com/steipete/CodexBar", "description": "Show usage stats for OpenAI Codex and Claude Code, without having to login.", "stars": 16734, "forks": 1375, "language": "Swift", "topics": ["ai", "coding", "stats"]},
        {"name": "alibaba/zvec", "url": "https://github.com/alibaba/zvec", "description": "A lightweight, lightning-fast, in-process vector database.", "stars": 13502, "forks": 823, "language": "C++", "topics": ["ai", "vector", "database"]},
        {"name": "gastownhall/gastown", "url": "https://github.com/gastownhall/gastown", "description": "Gas Town - multi-agent workspace manager.", "stars": 16692, "forks": 1539, "language": "Go", "topics": ["ai", "agents", "workspace"]},
    ]


def parse_trending_html(html):
    """解析 GitHub Trending 页面 HTML（简化版）"""
    repos = []
    
    # 尝试从 HTML 中提取仓库信息
    # 匹配 h2 > a 结构
    blocks = re.findall(
        r'<h2[^>]*>.*?<a href="(/[^"]+)"[^>]*>\s*(.*?)\s*</a>.*?</h2>'
        r'(.*?)<div\s+class="f6',
        html, re.DOTALL
    )
    
    if not blocks:
        # 备用：更宽松的匹配
        blocks = re.findall(
            r'<a href="(/[^"]+)"[^>]*>\s*\n?\s*(.*?)\s*</a>'
            r'.*?<p[^>]*>(.*?)</p>',
            html, re.DOTALL
        )
        for path, name, desc in blocks[:25]:
            if path.count("/") == 1:
                repos.append({
                    "name": path.strip("/"),
                    "url": f"https://github.com{path}",
                    "description": clean_html(desc),
                    "stars": 0,
                    "forks": 0,
                    "language": "",
                    "topics": [],
                })
    else:
        for path, name, block in blocks[:25]:
            if path.count("/") != 1:
                continue
            
            desc_match = re.search(r'<p[^>]*>(.*?)</p>', block, re.DOTALL)
            desc = clean_html(desc_match.group(1)) if desc_match else ""
            
            lang_match = re.search(r'itemprop="programmingLanguage">([^<]+)</span>', block)
            lang = lang_match.group(1).strip() if lang_match else ""
            
            stars_match = re.findall(r'([\d,]+)\s*(?:stars|forks)', block)
            
            repos.append({
                "name": path.strip("/"),
                "url": f"https://github.com{path}",
                "description": desc,
                "stars": parse_number(stars_match[0]) if stars_match else 0,
                "forks": parse_number(stars_match[1]) if len(stars_match) > 1 else 0,
                "language": lang,
                "topics": [],
            })
    
    # 去重
    seen = set()
    unique = []
    for r in repos:
        if r["name"] not in seen and r["name"].count("/") == 1:
            seen.add(r["name"])
            unique.append(r)
    
    return unique[:25]


def fetch_github_api_trending():
    """通过 GitHub API 获取热门 AI 仓库"""
    print("  通过 GitHub API 获取热门 AI 仓库...")
    
    query_params = urllib.parse.urlencode({
        "q": "topic:artificial-intelligence+topic:machine-learning+topic:deep-learning+topic:llm",
        "sort": "stars",
        "order": "desc",
        "per_page": 30,
    })
    url = f"{GITHUB_API_SEARCH}?{query_params}"
    
    data = fetch_url(url)
    if not data:
        return []
    
    try:
        result = json.loads(data)
        items = result.get("items", [])
    except json.JSONDecodeError:
        return []
    
    repos = []
    for item in items:
        repos.append({
            "name": item.get("full_name", ""),
            "url": item.get("html_url", ""),
            "description": clean_html(item.get("description") or ""),
            "stars": item.get("stargazers_count", 0),
            "forks": item.get("forks_count", 0),
            "language": item.get("language") or "",
            "topics": item.get("topics", []),
        })
    
    print(f"  API 返回 {len(repos)} 个热门仓库")
    return repos


def clean_html(text):
    """清除 HTML 标签"""
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def parse_number(text):
    """解析数字字符串（含千分位）"""
    if not text:
        return 0
    try:
        return int(text.replace(",", "").strip())
    except (ValueError, AttributeError):
        return 0


# ─── 第二步：热度评分 ────────────────────────────────────
def score_repos(repos):
    """5维热度评分系统"""
    print("\n[2/6] 计算热度评分...")
    
    scored = []
    for repo in repos:
        score = 0.0
        breakdown = {}
        
        # 维度1：Star 数量（权重 30%）
        stars = repo.get("stars", 0)
        star_score = min(100.0, stars / 50000 * 100)
        breakdown["stars"] = round(star_score, 1)
        score += star_score * 0.30
        
        # 维度2：Fork 数量（权重 20%）
        forks = repo.get("forks", 0)
        fork_score = min(100.0, forks / 20000 * 100)
        breakdown["forks"] = round(fork_score, 1)
        score += fork_score * 0.20
        
        # 维度3：描述丰富度（权重 15%）
        desc = repo.get("description", "")
        desc_score = min(100.0, len(desc) / 100 * 100) if desc else 30.0
        breakdown["description"] = round(desc_score, 1)
        score += desc_score * 0.15
        
        # 维度4：话题标签（权重 15%）
        topics = repo.get("topics", [])
        topic_score = min(100.0, len(topics) / 5 * 100) if topics else 20.0
        breakdown["topics"] = round(topic_score, 1)
        score += topic_score * 0.15
        
        # 维度5：AI 关键词匹配（权重 20%）
        ai_keywords = ["ai", "llm", "gpt", "ml", "deep learning", "neural", "transformer",
                       "agent", "rag", "diffusion", "model", "inference", "chatbot",
                       "openai", "anthropic", "claude", "gemini", "stable diffusion",
                       "machine learning", "artificial intelligence", "copilot"]
        text = f"{repo.get('name', '')} {repo.get('description', '')} {' '.join(topics)}".lower()
        keyword_matches = sum(1 for kw in ai_keywords if kw in text)
        keyword_score = min(100.0, keyword_matches / 5 * 100)
        breakdown["ai_keywords"] = round(keyword_score, 1)
        score += keyword_score * 0.20
        
        repo["score"] = round(score, 2)
        repo["score_breakdown"] = breakdown
        scored.append(repo)
    
    # 按分数排序
    scored.sort(key=lambda x: x["score"], reverse=True)
    
    print(f"  评分完成，最高分: {scored[0]['score'] if scored else 0}")
    return scored


# ─── 第三步：筛选 Top N ──────────────────────────────────
def select_top_n(scored_repos, n=3):
    """选择 Top N 项目"""
    print(f"\n[3/6] 筛选 Top {n} 项目...")
    
    top = scored_repos[:n]
    
    for i, repo in enumerate(top, 1):
        print(f"  #{i} {repo['name']} (热度: {repo['score']})")
        print(f"     Stars: {repo['stars']:,} | Forks: {repo['forks']:,} | Lang: {repo['language']}")
        print(f"     {repo.get('description', '')[:80]}...")
    
    return top


# ─── 第四步：生成小红书内容 ──────────────────────────────
def generate_xhs_content(repo):
    """为单个项目生成小红书风格内容"""
    name = repo.get("name", "").split("/")[-1] if "/" in repo.get("name", "") else repo.get("name", "")
    description = repo.get("description", "")
    stars = repo.get("stars", 0)
    language = repo.get("language", "")
    topics = repo.get("topics", [])
    url = repo.get("url", "")
    
    # 生成标题（5个备选）
    titles = generate_titles(name, description, stars)
    
    # 生成正文
    body = generate_body(name, description, stars, language, topics, url)
    
    # 生成标签
    tags = generate_tags(name, language, topics)
    
    return {
        "project_name": name,
        "titles": titles,
        "body": body,
        "tags": tags,
        "repo_url": url,
        "stars": stars,
        "language": language,
    }


def generate_titles(name, description, stars):
    """生成爆款标题"""
    star_text = f"{stars // 1000}k+" if stars >= 1000 else str(stars)
    
    templates = [
        f"{name}深度解析 | 这才是真正的AI神器",
        f"救命！{name}也太好用了吧",
        f"用了{name}，效率直接翻倍",
        f"GitHub爆款！{name}让我彻底戒不掉",
        f"{name}深度测评 | 真的绝绝子",
        f"发现宝藏！{star_text} star 的 {name} 绝了",
        f"这个 {name} 项目，让我直接跪了",
        f"GitHub 热榜第1！{name}到底有多强",
    ]
    return templates


def generate_body(name, description, stars, language, topics, url):
    """生成小红书正文"""
    star_text = f"{stars // 1000}k" if stars >= 1000 else str(stars)
    
    # 提取核心功能点
    features = extract_features(name, description, topics)
    
    feature_lines = "\n".join([f"- {f}" for f in features[:5]])
    topic_tags = " ".join([f"#{t}" for t in topics[:5]]) if topics else ""
    
    body = f"""姐妹们！我最近发现了一个超级炸裂的项目，必须跟你们分享！

这就是 **{name}** —— {description}

【核心功能】
{feature_lines}

【为什么选择它】
- 开源免费，社区活跃
- {star_text} star 认证，GitHub 热门项目
- 简单易用，快速上手
- 功能强大，满足多种场景

GitHub: {url}

用了 {name}，你会发现效率提升不是一点点！

你们有没有用过类似的 AI 工具？
评论区告诉我，一起交流！

{topic_tags}
"""
    return body.strip()


def extract_features(name, description, topics):
    """从描述中提取核心功能"""
    features = []
    
    # 从描述中提取
    if description:
        # 按逗号/句号分割
        parts = re.split(r'[,，.。;；]', description)
        for p in parts[:3]:
            p = p.strip()
            if 4 <= len(p) <= 30:
                features.append(p)
    
    # 从 topics 补充
    for t in topics[:3]:
        features.append(f"支持 {t}")
    
    # 默认功能
    defaults = [
        "智能分析与推理",
        "多场景适配",
        "开箱即用体验",
        "持续迭代更新",
        "社区生态丰富",
    ]
    
    while len(features) < 5:
        d = defaults[len(features) % len(defaults)]
        if d not in features:
            features.append(d)
        else:
            break
    
    return features[:5]


def generate_tags(name, language, topics):
    """生成话题标签"""
    tags = ["#AI", "#人工智能", "#AI工具", "#GitHub", "#开源", "#效率工具"]
    
    if language:
        tags.append(f"#{language}")
    
    for t in topics[:3]:
        clean = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]', '', t)
        if clean:
            tags.append(f"#{clean}")
    
    tags.extend(["#学习必备", "#ChatGPT", "#AI助手", "#黑科技"])
    
    return " ".join(tags[:10])


# ─── 第五步：生成配图 ────────────────────────────────────
def _load_tech_draw():
    """动态加载 tech_draw 模块，fallback 到 sys.path"""
    # 方法1：直接 import（如果 SKILL_DIR 已在 sys.path 中）
    try:
        import tech_draw
        return tech_draw
    except ImportError:
        pass
    
    # 方法2：逐个检查可能的路径
    candidates = [
        SKILL_DIR,
        os.path.join(PROJECT_ROOT, "skills", "xhs-ai-blogger", "scripts"),
        os.path.normpath(os.path.join(PROJECT_ROOT, "..", "skills", "xhs-ai-blogger", "scripts")),
        os.path.normpath(os.path.join(os.path.expanduser("~"), ".workbuddy", "plugins",
                                     "marketplaces", "codebuddy-plugins-official",
                                     "skills", "xhs-ai-blogger", "scripts")),
    ]
    
    for c in candidates:
        tech_draw_path = os.path.join(c, "tech_draw.py")
        if not os.path.exists(tech_draw_path):
            continue
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("tech_draw", tech_draw_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            print(f"  ✓ 加载 tech_draw: {tech_draw_path}")
            return mod
        except Exception as e:
            print(f"  ✗ 加载 {tech_draw_path} 失败: {e}")
    
    return None


def generate_images(repo_data, output_dir):
    """为项目生成科技风配图"""
    print("\n[5/6] 生成科技风配图...")
    
    mod = _load_tech_draw()
    if mod is None:
        print("  警告: 无法加载 tech_draw 模块，跳过配图生成")
        return []
    
    gen_card = mod.gen_card
    
    name = repo_data["project_name"]
    description = repo_data.get("body", "").split("\n")[0] if repo_data.get("body") else ""
    url = repo_data.get("repo_url", "")
    stars = repo_data.get("stars", 0)
    language = repo_data.get("language", "")
    tags = repo_data.get("tags", "")
    
    # 提取 GitHub 路径
    github_path = url.split("github.com/")[-1] if "github.com/" in url else url
    
    # 6页配图数据
    pages_data = [
        {
            "theme_idx": 0,
            "kicker": "GitHub 开源项目",
            "title": name,
            "subtitle": description[:60] if description else "AI 热门项目",
            "sections": [
                {"type": "label", "text": " 核心亮点"},
                {"type": "bullet", "items": extract_features(name, description, [])},
                {"type": "divider"},
                {"type": "text", "lines": [f"GitHub: {github_path}"]},
            ],
            "footer_tags": tags.replace(" ", " #") if isinstance(tags, str) else tags,
        },
        {
            "theme_idx": 1,
            "kicker": "快速上手",
            "title": f"快速部署\n{name}",
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
            "footer_tags": tags.replace(" ", " #") if isinstance(tags, str) else tags,
        },
        {
            "theme_idx": 4,
            "kicker": "核心能力",
            "title": "核心能力\n全景一览",
            "sections": [
                {"type": "bullet", "items": extract_features(name, description, [])},
                {"type": "divider"},
                {"type": "label", "text": " 技术特点"},
                {"type": "text", "lines": ["支持多平台", "简单易用", "持续更新"]},
            ],
            "footer_tags": tags.replace(" ", " #") if isinstance(tags, str) else tags,
        },
        {
            "theme_idx": 3,
            "kicker": "功能详解",
            "title": "功能模块\n深度解析",
            "sections": [
                {"type": "label", "text": " 详细功能"},
                {"type": "bullet", "items": extract_features(name, description, [])},
            ],
            "footer_tags": tags.replace(" ", " #") if isinstance(tags, str) else tags,
        },
        {
            "theme_idx": 2,
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
                {"type": "text", "lines": ["[ Star 支持开源 ]"]},
            ],
            "footer_tags": tags.replace(" ", " #") if isinstance(tags, str) else tags,
        },
        {
            "theme_idx": 5,
            "kicker": "赶紧试试",
            "title": f"{name}\n等你来探索",
            "sections": [
                {"type": "label", "text": " 立即体验"},
                {"type": "code", "lines": [
                    github_path,
                    "",
                    "[ Star 支持开源 ]",
                ]},
                {"type": "divider"},
                {"type": "text", "lines": [
                    "觉得有用就点个 Star 吧！",
                    "你们的支持是我更新的动力",
                ]},
            ],
            "footer_tags": tags.replace(" ", " #") if isinstance(tags, str) else tags,
        },
    ]
    
    generated = []
    total = len(pages_data)
    
    for i, page_cfg in enumerate(pages_data, 1):
        page_cfg["page_num"] = i
        page_cfg["total"] = total
        
        output_path = os.path.join(output_dir, f"{name}_page_{i:02d}.jpg")
        try:
            gen_card(page_cfg, output_path)
            generated.append(output_path)
            print(f"  ✓ 生成配图 {i}/{total}: {os.path.basename(output_path)}")
        except Exception as e:
            print(f"  ✗ 配图 {i} 生成失败: {e}")
    
    return generated


# ─── 第六步：保存文件 ────────────────────────────────────
def save_outputs(repo_data, image_paths, output_dir):
    """保存所有内容到 output 目录"""
    print("\n[6/6] 保存输出文件...")
    
    name = repo_data["project_name"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 保存 Markdown 内容
    md_content = f"""# {repo_data['titles'][0] if repo_data['titles'] else name}

## 项目信息

- 项目名称: {name}
- GitHub: {repo_data.get('repo_url', '')}
- Stars: {repo_data.get('stars', 0):,}
- 语言: {repo_data.get('language', 'N/A')}

---

## 备选标题

"""
    for i, title in enumerate(repo_data.get('titles', []), 1):
        md_content += f"{i}. {title}\n"
    
    md_content += f"""

---

## 正文内容

{repo_data.get('body', '')}

---

## 标签

{repo_data.get('tags', '')}

---

## 配图

| 页码 | 文件 |
|:---:|:---:|
"""
    for i, path in enumerate(image_paths, 1):
        md_content += f"| 第{i}页 | {os.path.basename(path)} |\n"
    
    md_content += f"""

---

*由 GitHub AI Trending Pipeline 生成 | {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
    
    md_path = os.path.join(output_dir, f"{name}_内容_{timestamp}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"  ✓ 内容文档: {os.path.basename(md_path)}")
    
    # 保存 JSON 数据
    json_data = {
        "timestamp": timestamp,
        "project_name": name,
        "repo_url": repo_data.get("repo_url", ""),
        "stars": repo_data.get("stars", 0),
        "language": repo_data.get("language", ""),
        "titles": repo_data.get("titles", []),
        "body": repo_data.get("body", ""),
        "tags": repo_data.get("tags", ""),
        "images": [os.path.basename(p) for p in image_paths],
    }
    
    json_path = os.path.join(output_dir, f"{name}_data_{timestamp}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ 数据文件: {os.path.basename(json_path)}")
    
    return md_path, json_path


# ─── 主流程 ──────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="GitHub AI Trending - 小红书内容生成 Pipeline")
    parser.add_argument("--top", type=int, default=DEFAULT_TOP_N, help=f"选择 Top N 项目 (默认: {DEFAULT_TOP_N})")
    parser.add_argument("--output", type=str, default=DEFAULT_OUTPUT, help="输出目录")
    parser.add_argument("--no-images", action="store_true", help="跳过配图生成")
    args = parser.parse_args()
    
    print("=" * 60)
    print("🚀 GitHub AI Trending - 小红书内容生成 Pipeline")
    print("=" * 60)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Top N: {args.top}")
    print(f"输出: {args.output}")
    
    # 创建输出目录
    os.makedirs(args.output, exist_ok=True)
    
    # 第一步：抓取
    repos = fetch_github_trending()
    if not repos:
        print("\n❌ 未能获取任何项目，请检查网络连接")
        sys.exit(1)
    
    print(f"\n📊 共抓取 {len(repos)} 个热门项目")
    
    # 第二步：评分
    scored = score_repos(repos)
    
    # 第三步：筛选
    top_repos = select_top_n(scored, args.top)
    
    # 第四、五、六步：为每个项目生成内容 + 配图 + 保存
    all_outputs = []
    
    for i, repo in enumerate(top_repos, 1):
        print(f"\n{'─' * 50}")
        print(f"📱 处理项目 {i}/{len(top_repos)}: {repo['name']}")
        print(f"{'─' * 50}")
        
        # 生成内容
        content = generate_xhs_content(repo)
        
        # 生成配图
        image_paths = []
        if not args.no_images:
            # 为每个项目创建子目录
            project_dir = os.path.join(args.output, content["project_name"])
            os.makedirs(project_dir, exist_ok=True)
            image_paths = generate_images(content, project_dir)
        else:
            project_dir = args.output
        
        # 保存文件
        md_path, json_path = save_outputs(content, image_paths, project_dir)
        
        all_outputs.append({
            "project": content["project_name"],
            "md": md_path,
            "json": json_path,
            "images": image_paths,
        })
    
    # ─── 完成报告 ───
    print("\n" + "=" * 60)
    print("✅ 执行完成！")
    print("=" * 60)
    print(f"\n📊 执行报告:")
    print(f"  - 抓取项目数: {len(repos)}")
    print(f"  - 评分项目数: {len(scored)}")
    print(f"  - 生成内容数: {len(all_outputs)}")
    print(f"  - 生成配图数: {sum(len(o['images']) for o in all_outputs)}")
    
    print(f"\n📁 输出文件:")
    for out in all_outputs:
        print(f"\n  [{out['project']}]")
        print(f"    内容: {os.path.basename(out['md'])}")
        print(f"    数据: {os.path.basename(out['json'])}")
        for img in out['images']:
            print(f"    配图: {os.path.basename(img)}")
    
    print(f"\n📂 输出目录: {args.output}")
    print(f"⏰ 完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return all_outputs


if __name__ == "__main__":
    main()
