#!/usr/bin/env python3
"""
GitHub AI Trending 内容创作自动化主脚本
每天自动抓取、评分、生成小红书内容
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# 添加 scripts 目录到路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from fetch_trending import GitHubTrendingFetcher, save_trending_data
from aggregator import XHSAggregator
from image_generator import ImageGenerator


class DailyContentBot:
    """每日内容创作机器人"""

    def __init__(self, base_dir: str = None):
        if base_dir is None:
            base_dir = SCRIPT_DIR.parent

        self.base_dir = Path(base_dir)
        self.data_dir = self.base_dir / 'data'
        self.output_dir = self.base_dir / 'output'
        self.log_dir = self.base_dir / 'logs'

        # 创建目录
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # 初始化组件
        self.fetcher = GitHubTrendingFetcher()
        self.aggregator = XHSAggregator(
            data_dir=str(self.data_dir),
            output_dir=str(self.output_dir)
        )
        self.image_gen = ImageGenerator(output_dir=str(self.output_dir))

        # 日志文件
        self.log_file = self.log_dir / f'run_{datetime.now().strftime("%Y%m%d")}.log'

    def log(self, message: str, level: str = "INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"

        print(log_entry.strip())

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

    def step_1_fetch_trending(self) -> bool:
        """步骤 1: 抓取 GitHub 趋势"""
        self.log("=" * 50)
        self.log("🚀 步骤 1: 抓取 GitHub AI 趋势项目")
        self.log("=" * 50)

        try:
            # 获取 Python 项目
            self.log("📦 抓取 Python AI 项目...")
            python_repos = self.fetcher.fetch_trending_repos(language='python')
            self.log(f"   ✅ 找到 {len(python_repos)} 个 Python AI 项目")

            # 获取 JavaScript 项目
            self.log("📦 抓取 JavaScript AI 项目...")
            js_repos = self.fetcher.fetch_trending_repos(language='javascript')
            self.log(f"   ✅ 找到 {len(js_repos)} 个 JavaScript AI 项目")

            # 获取 Go 项目（可选）
            self.log("📦 抓取 Go AI 项目...")
            go_repos = self.fetcher.fetch_trending_repos(language='go')
            self.log(f"   ✅ 找到 {len(go_repos)} 个 Go AI 项目")

            # 合并并排序
            all_repos = python_repos + js_repos + go_repos
            all_repos.sort(key=lambda x: x['hot_score'], reverse=True)

            # 保存数据
            trending_file = self.data_dir / 'trending.json'
            save_trending_data(all_repos, str(trending_file))

            self.log(f"✅ 共获取 {len(all_repos)} 个 AI 项目")
            self.log(f"📊 Top 1 项目: {all_repos[0]['full_name']} (热度: {all_repos[0]['hot_score']})")

            return True

        except Exception as e:
            self.log(f"❌ 抓取失败: {e}", "ERROR")
            return False

    def step_2_generate_content(self, count: int = 3) -> bool:
        """步骤 2: 生成小红书内容"""
        self.log("=" * 50)
        self.log("✍️ 步骤 2: 生成小红书合集内容")
        self.log("=" * 50)

        try:
            content = self.aggregator.generate_and_save(count=count)

            self.log(f"✅ 内容生成成功")

            # 显示预览
            preview_lines = content.split('\n')[:30]
            self.log("📄 内容预览:")
            for line in preview_lines:
                self.log(f"   {line}")

            return True

        except Exception as e:
            self.log(f"❌ 内容生成失败: {e}", "ERROR")
            return False

    def step_3_generate_images(self, count: int = 3) -> bool:
        """步骤 3: 生成配图"""
        self.log("=" * 50)
        self.log("🖼️ 步骤 3: 生成配图")
        self.log("=" * 50)

        try:
            projects = self.aggregator.load_trending_data()[:count]
            selected = self.aggregator.select_top_projects(projects, count=count)

            if not selected:
                self.log("⚠️ 没有可用的项目数据，跳过配图生成")
                return False

            # 生成封面图
            self.log("📦 生成封面图...")
            titles = self.aggregator.generate_title(selected)
            cover_path = self.image_gen.create_cover_image(
                title=titles[0],
                subtitle="GitHub AI Trending 每日推荐",
                projects=selected
            )
            self.log(f"   ✅ 封面图: {cover_path}")

            # 生成项目缩略图
            self.log("📦 生成项目缩略图...")
            for i, project in enumerate(selected, 1):
                thumb_path = self.image_gen.create_project_thumbnail(project)
                self.log(f"   ✅ 项目 {i} 缩略图: {thumb_path}")

            # 生成对比图
            if len(selected) >= 2:
                self.log("📦 生成对比图...")
                grid_path = self.image_gen.create_comparison_grid(selected)
                self.log(f"   ✅ 对比图: {grid_path}")

            # 生成 AI 绘图提示词
            self.log("📦 生成 AI 绘图提示词...")
            for i, project in enumerate(selected, 1):
                prompt = self.image_gen.generate_image_prompt(project)
                prompt_file = self.output_dir / f'prompt_{project["name"]}.txt'
                with open(prompt_file, 'w', encoding='utf-8') as f:
                    f.write(prompt)
                self.log(f"   ✅ 提示词 {i}: {prompt_file}")

            return True

        except Exception as e:
            self.log(f"❌ 配图生成失败: {e}", "ERROR")
            return False

    def step_4_generate_report(self) -> bool:
        """步骤 4: 生成执行报告"""
        self.log("=" * 50)
        self.log("📊 步骤 4: 生成执行报告")
        self.log("=" * 50)

        try:
            report = {
                'generated_at': datetime.now().isoformat(),
                'status': 'success',
                'output_files': [],
                'next_run': self._get_next_run_time()
            }

            # 收集输出文件
            for ext in ['*.md', '*.json', '*.png', '*.txt']:
                files = list(self.output_dir.glob(ext))
                report['output_files'].extend([str(f) for f in files])

            # 保存报告
            report_file = self.output_dir / f'report_{datetime.now().strftime("%Y%m%d")}.json'
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)

            self.log(f"✅ 报告已生成: {report_file}")
            self.log(f"📁 输出文件数量: {len(report['output_files'])}")

            return True

        except Exception as e:
            self.log(f"❌ 报告生成失败: {e}", "ERROR")
            return False

    def _get_next_run_time(self) -> str:
        """计算下次运行时间"""
        from datetime import timedelta
        next_run = datetime.now() + timedelta(days=1)
        next_run = next_run.replace(hour=9, minute=0, second=0)
        return next_run.isoformat()

    def run_full_pipeline(self, content_count: int = 3,
                         generate_images: bool = True) -> bool:
        """运行完整流水线"""
        self.log("🎯 GitHub AI Trending 内容创作机器人启动")
        self.log(f"⏰ 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log(f"📦 内容数量: {content_count}")
        self.log(f"🖼️ 生成配图: {'是' if generate_images else '否'}")

        success = True

        # 执行各步骤
        if not self.step_1_fetch_trending():
            success = False

        if success and not self.step_2_generate_content(count=content_count):
            success = False

        if success and generate_images:
            if not self.step_3_generate_images(count=content_count):
                self.log("⚠️ 配图生成失败，继续执行...", "WARNING")

        if not self.step_4_generate_report():
            success = False

        # 最终状态
        self.log("=" * 50)
        if success:
            self.log("✅ 全部任务执行成功！")
        else:
            self.log("❌ 部分任务执行失败，请检查日志", "ERROR")
        self.log("=" * 50)

        return success

    def list_recent_outputs(self, limit: int = 10):
        """列出最近的输出文件"""
        self.log("📁 最近的输出文件:")

        files = sorted(self.output_dir.glob('*'), key=lambda x: x.stat().st_mtime, reverse=True)

        for f in files[:limit]:
            size = f.stat().st_size
            size_str = f"{size:,} bytes" if size < 1024 else f"{size/1024:.1f} KB"
            self.log(f"   {f.name} ({size_str})")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='GitHub AI Trending 内容创作机器人')
    parser.add_argument('--count', '-c', type=int, default=3,
                       help='生成的项目数量 (默认: 3)')
    parser.add_argument('--no-image', action='store_true',
                       help='跳过图片生成')
    parser.add_argument('--list', '-l', action='store_true',
                       help='列出最近的输出文件')

    args = parser.parse_args()

    bot = DailyContentBot()

    if args.list:
        bot.list_recent_outputs()
        return

    success = bot.run_full_pipeline(
        content_count=args.count,
        generate_images=not args.no_image
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
