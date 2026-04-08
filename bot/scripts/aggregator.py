#!/usr/bin/env python3
"""
多项目合集生成器
将多个 GitHub AI 项目整合成一篇完整的合集内容
"""

import json
import random
from datetime import datetime
from typing import List, Dict
from pathlib import Path


class XHSAggregator:
    """小红书多项目合集生成器"""

    # 爆款标题模板
    TITLE_TEMPLATES = [
        "救命！挖到 {count} 个 GitHub 神器，每一个都巨好用 😭",
        "全网找疯了的 AI 工具，我给你们扒来了！",
        "这 {count} 个 GitHub 项目，让我效率翻倍 ⚡️",
        "博主亲测！这 {count} 个 AI 工具真的绝 💯",
        "GitHub 上这些 AI 项目，好用到想哭 ✨",
        "不允许你们不知道！{count} 个 GitHub 爆款 AI ✊",
        "这 {count} 款 AI 工具，让我彻底离不开电脑 🤩",
    ]

    # 封面文案模板
    COVER_TEMPLATES = [
        "GitHub AI 神器合集 🎯",
        "效率翻倍的秘密武器 ⚡",
        "这也太香了吧 😭",
        "AI 工具 yyds",
        "宝藏 GitHub 项目合集",
    ]

    def __init__(self, data_dir: str = 'data', output_dir: str = 'output'):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_trending_data(self) -> List[Dict]:
        """加载趋势数据"""
        trending_file = self.data_dir / 'trending.json'

        if not trending_file.exists():
            print("❌ No trending data found. Run fetch_trending.py first!")
            return []

        with open(trending_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data.get('repos', [])

    def select_top_projects(self, repos: List[Dict],
                           count: int = 3,
                           diversity: bool = True) -> List[Dict]:
        """选择优质项目，保证多样性"""
        if not repos:
            return []

        sorted_repos = sorted(repos, key=lambda x: x.get('hot_score', 0), reverse=True)

        if not diversity:
            return sorted_repos[:count]

        selected = []
        used_languages = set()

        for repo in sorted_repos:
            if len(selected) >= count:
                break

            language = repo.get('language', 'Unknown')
            if language not in used_languages or len(selected) < count:
                selected.append(repo)
                used_languages.add(language)

        return selected

    def generate_title(self, projects: List[Dict]) -> List[str]:
        """生成 5 个爆款标题"""
        count = len(projects)
        return [template.format(count=count) for template in self.TITLE_TEMPLATES[:5]]

    def generate_cover(self) -> str:
        """生成封面文案"""
        return random.choice(self.COVER_TEMPLATES)

    def generate_aggregated_content(self, projects: List[Dict]) -> str:
        """生成完整合集内容"""
        if not projects:
            return "没有找到合适的项目"

        titles = self.generate_title(projects)
        cover = self.generate_cover()

        content = f"""
{'='*50}
📌 爆款标题（5 选 1）：
{'='*50}
"""
        for i, title in enumerate(titles, 1):
            content += f"{i}. {title}\n"

        content += f"""
{'='*50}
📣 封面文案：
{'='*50}
{cover}

{'='*50}
📝 完整正文：
{'='*50}

"""

        content += self._generate_hook(len(projects))

        for i, project in enumerate(projects, 1):
            content += self._generate_project_section(i, project)

        content += self._generate_ending(len(projects))
        content += self._generate_tags(projects)

        return content

    def _generate_hook(self, count: int) -> str:
        """生成开头钩子"""
        hooks = [
            f"姐妹们！我又来给你们挖掘宝藏了！🎉\n\n今天分享的这 {count} 个 GitHub AI 项目，是我最近每天都在用的神器！\n\n真的，用了再也回不去那种 😭",
            f"答应我，今天的内容一定要看完！👀\n\n因为我给你们整理了 {count} 个超好用的 GitHub AI 项目，每一个都是同领域的 Top 级存在。\n\n错过真的会后悔那种！",
            f"宝子们，我来交作业了！📝\n\n上次答应你们整理的 GitHub AI 神器，我花了一周实测筛选，终于搞定！\n\n这 {count} 个，每一个都值得收藏 ⭐",
        ]
        return random.choice(hooks) + "\n\n---\n\n"

    def _generate_project_section(self, index: int, project: Dict) -> str:
        """生成单个项目的介绍"""
        name = project.get('name', 'Unknown')
        full_name = project.get('full_name', '')
        description = project.get('description', '') or '暂无描述'
        stars = project.get('stargazers_count', 0)
        language = project.get('language', 'Unknown')
        hot_score = project.get('hot_score', 0)
        url = project.get('html_url', '')

        section = f"""
✨ 项目 {index}：{name}

📍 GitHub：{full_name}
⭐ Stars：{stars:,}
🔥 热度评分：{hot_score}
💻 语言：{language}

📝 项目简介：
{description}

🔗 传送门：{url}

"""

        if stars > 5000:
            section += "💡 推荐理由：全网 {stars:,}+ star，品质绝对有保障！\n\n".format(stars=stars)
        elif hot_score > 50:
            section += "💡 推荐理由：近期增长超猛，说明大家都觉得好用！\n\n"
        else:
            section += "💡 推荐理由：小众但超好用，用了绝对不亏！\n\n"

        section += "---\n\n"
        return section

    def _generate_ending(self, count: int) -> str:
        """生成结尾"""
        endings = [
            f"""
🏷️ 博主有话说：

这 {count} 个项目我全部亲自测试过才来推荐的！✅

说实话，现在 AI 工具真的太多了，但好用的真的不多。\n能让我坚持用的，就这几个。

你们最想了解哪一个？评论区告诉我 👇

#GitHub #AI工具 #人工智能 #效率神器 #AI副业 #打工人必备 #学生党必备 #黑科技 #神器推荐 #2025AI
""",
            f"""
🏷️ 使用建议：

1️⃣ 先收藏再往下看，防止迷路
2️⃣ 每个工具都去实际用一下
3️⃣ 找到最适合自己的那一款

⚠️ 踩坑提醒：
不要一次性装太多，选 1-2 个坚持用才是王道！

评论区聊聊：
👉 你用过几个？
👉 最想尝试哪个？

抽 3 个宝子送详细教程 👀

#AI #人工智能 #GitHub #开源 #效率工具 #AI助手 #学习必备 #宝藏工具
""",
        ]
        return random.choice(endings)

    def _generate_tags(self, projects: List[Dict]) -> str:
        """生成标签"""
        base_tags = [
            "#AI #人工智能 #AI工具 #GitHub #开源",
            "#效率神器 #学习必备 #学生党 #打工人",
            "#AI副业 #黑科技 #宝藏发现 #神器推荐"
        ]

        languages = set(p.get('language', '') for p in projects)
        language_tags = {
            'Python': "#Python #Python爱好者",
            'JavaScript': "#JavaScript #前端开发",
            'TypeScript': "#TypeScript #前端开发",
            'Go': "#Golang #Go语言",
            'Rust': "#Rust #系统编程"
        }

        extra_tags = [language_tags.get(lang, '') for lang in languages if lang in language_tags]
        return '\n'.join(base_tags) + '\n' + ' '.join(extra_tags)

    def generate_and_save(self, count: int = 3) -> str:
        """生成合集内容并保存"""
        repos = self.load_trending_data()

        if not repos:
            return "❌ 没有可用的项目数据"

        projects = self.select_top_projects(repos, count=count)
        content = self.generate_aggregated_content(projects)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = self.output_dir / f'xhs_aggregated_{timestamp}.md'

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ 内容已保存到：{output_file}")

        json_file = self.output_dir / f'xhs_data_{timestamp}.json'
        output_data = {
            'generated_at': datetime.now().isoformat(),
            'projects': projects,
            'titles': self.generate_title(projects),
            'cover': self.generate_cover()
        }

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        return content


def main():
    """主函数"""
    print("🚀 小红书 AI 项目合集生成器")
    print("=" * 50)

    aggregator = XHSAggregator()
    content = aggregator.generate_and_save(count=3)

    print("\n" + "=" * 50)
    print("📄 生成的内容预览：")
    print("=" * 50)
    print(content[:2000])

    return content


if __name__ == '__main__':
    main()
