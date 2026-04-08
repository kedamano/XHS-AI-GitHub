#!/usr/bin/env python3
"""
GitHub Trending AI 项目抓取脚本
自动抓取 GitHub 趋势中的 AI 相关项目
"""

import json
import time
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re


class GitHubTrendingFetcher:
    """GitHub 趋势项目抓取器"""

    # AI 相关关键词过滤
    AI_KEYWORDS = [
        'ai', 'gpt', 'llm', 'chatgpt', 'openai', 'claude', 'gemini',
        '的人工智能', 'ai-', '-ai', 'machine-learning', 'deep-learning',
        'neural', 'transformer', 'diffusion', 'stable-diffusion',
        'agent', 'rag', 'embedding', 'vector', 'langchain',
        'chatbot', 'conversation', 'nlp', 'nlu', 'text-to',
        'image-generation', 'image gen', 'aigc', 'generative',
        'copilot', 'assistant', 'automation', 'auto-gpt',
        'ollama', 'local-llm', 'llama', 'mistral', 'qwen'
    ]

    # 排除的非 AI 项目关键词
    EXCLUDE_KEYWORDS = [
        'kubernetes', 'k8s', 'docker', 'aws', 'terraform',
        'kubernetes', 'prometheus', 'grafana', 'ansible',
        'ci-cd', 'pipeline', 'monitoring', 'logging',
    ]

    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.session = requests.Session()
        if token:
            self.session.headers.update({'Authorization': f'token {token}'})
        self.session.headers.update({
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-Trending-AI-Fetcher'
        })

    def fetch_trending_repos(self, language: str = 'python',
                             since: str = 'daily') -> List[Dict]:
        """
        获取 GitHub 趋势项目

        Args:
            language: 编程语言 (python, javascript, go, etc.)
            since: 时间范围 (daily, weekly, monthly)

        Returns:
            趋势项目列表
        """
        url = f'https://api.github.com/search/repositories'
        params = {
            'q': f'language:{language} created:>{datetime.now().date() - timedelta(days=30)}',
            'sort': 'stars',
            'order': 'desc',
            'per_page': 100
        }

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            repos = data.get('items', [])

            # 过滤 AI 相关项目
            ai_repos = self._filter_ai_repos(repos)

            # 计算热度评分
            for repo in ai_repos:
                repo['hot_score'] = self._calculate_hot_score(repo)

            # 按热度排序
            ai_repos.sort(key=lambda x: x['hot_score'], reverse=True)

            return ai_repos[:20]  # 返回 Top 20

        except requests.exceptions.RequestException as e:
            print(f"Error fetching trending repos: {e}")
            return []

    def _filter_ai_repos(self, repos: List[Dict]) -> List[Dict]:
        """过滤 AI 相关项目"""
        filtered = []

        for repo in repos:
            name = repo.get('name', '').lower()
            description = repo.get('description', '').lower()
            full_text = f"{name} {description}"

            # 检查是否包含 AI 关键词
            is_ai = any(keyword.lower() in full_text for keyword in self.AI_KEYWORDS)

            # 检查是否应该排除
            is_excluded = any(excl.lower() in full_text for excl in self.EXCLUDE_KEYWORDS)

            if is_ai and not is_excluded:
                # 检查项目是否有实际价值（排除底层库）
                if self._is_user_friendly(repo):
                    filtered.append(repo)

        return filtered

    def _is_user_friendly(self, repo: Dict) -> bool:
        """检查项目是否对普通用户友好"""
        name = repo.get('name', '').lower()
        description = repo.get('description', '') or ''

        # 排除过于技术性的项目
        technical_patterns = [
            r'^torch', r'^tensorflow', r'^jax',
            r'^huggingface', r'^transformers$',
            r'^\w+-core$', r'^\w+-sdk$',
            r'protocol$', r'^wire',
        ]

        for pattern in technical_patterns:
            if re.match(pattern, name):
                return False

        # 检查是否有 README
        has_readme = repo.get('has_wiki', False) or description

        return has_readme and repo.get('stargazers_count', 0) > 10

    def _calculate_hot_score(self, repo: Dict) -> float:
        """
        计算项目热度评分

        评分维度：
        - Stars 数量 (权重 40%)
        - Stars 增长速率 (权重 30%)
        - Issues 活跃度 (权重 15%)
        - Watchers (权重 10%)
        - 最近更新时间 (权重 5%)
        """
        stars = repo.get('stargazers_count', 0)
        watchers = repo.get('watchers_count', 0)
        open_issues = repo.get('open_issues_count', 0)
        forks = repo.get('forks_count', 0)

        # 计算更新时间因子（越新分数越高）
        updated_at = datetime.strptime(repo.get('updated_at', ''), '%Y-%m-%dT%H:%M:%SZ')
        days_since_update = (datetime.now() - updated_at).days
        recency_factor = max(0, 1 - days_since_update / 30)

        # 归一化计算
        score = (
            min(stars / 10000, 1) * 40 +           # Stars 权重
            min(forks / 1000, 1) * 15 +           # Forks 权重
            min(watchers / 1000, 1) * 10 +         # Watchers 权重
            min(open_issues / 100, 1) * 15 +      # Issues 活跃度
            recency_factor * 20                     # 更新频率
        )

        return round(score, 2)

    def fetch_repo_details(self, owner: str, repo: str) -> Optional[Dict]:
        """获取项目详细信息"""
        url = f'https://api.github.com/repos/{owner}/{repo}'

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching repo details: {e}")
            return None

    def search_ai_projects(self, query: str = 'AI tools',
                          per_page: int = 30) -> List[Dict]:
        """搜索 AI 相关项目"""
        url = 'https://api.github.com/search/repositories'
        params = {
            'q': f'{query} language:python language:javascript',
            'sort': 'stars',
            'order': 'desc',
            'per_page': per_page
        }

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json().get('items', [])
        except requests.exceptions.RequestException as e:
            print(f"Error searching repos: {e}")
            return []


def save_trending_data(repos: List[Dict], filepath: str = 'data/trending.json'):
    """保存趋势数据到 JSON 文件"""
    output = {
        'timestamp': datetime.now().isoformat(),
        'count': len(repos),
        'repos': repos
    }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(repos)} repos to {filepath}")


def main():
    """主函数"""
    print("🚀 GitHub Trending AI 项目抓取器")
    print("=" * 50)

    fetcher = GitHubTrendingFetcher()

    # 获取 Python 趋势
    print("\n📦 抓取 Python 趋势项目...")
    python_repos = fetcher.fetch_trending_repos(language='python')
    print(f"   找到 {len(python_repos)} 个 Python AI 项目")

    # 获取 JavaScript 趋势
    print("\n📦 抓取 JavaScript 趋势项目...")
    js_repos = fetcher.fetch_trending_repos(language='javascript')
    print(f"   找到 {len(js_repos)} 个 JavaScript AI 项目")

    # 合并并排序
    all_repos = python_repos + js_repos
    all_repos.sort(key=lambda x: x['hot_score'], reverse=True)

    # 输出 Top 10
    print("\n🏆 Top 10 AI 热门项目：")
    print("-" * 80)
    for i, repo in enumerate(all_repos[:10], 1):
        print(f"{i}. {repo['full_name']}")
        print(f"   ⭐ {repo['stargazers_count']} | 📊 热度: {repo['hot_score']}")
        print(f"   📝 {repo.get('description', 'N/A')[:60]}...")
        print()

    # 保存数据
    save_trending_data(all_repos[:20], 'data/trending.json')

    return all_repos


if __name__ == '__main__':
    main()
