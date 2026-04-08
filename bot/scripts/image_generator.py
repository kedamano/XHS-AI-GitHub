#!/usr/bin/env python3
"""
配图自动生成脚本
为小红书内容生成封面图和项目截图展示
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import base64

# 尝试导入 PIL，如果不可用则使用替代方案
try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class ImageGenerator:
    """小红书配图生成器"""

    # 封面图尺寸（小红书推荐 3:4 或 1:1）
    COVER_SIZE = (1080, 1440)  # 3:4 竖版
    THUMBNAIL_SIZE = (600, 400)

    # 配色方案
    COLORS = {
        'primary': '#FF6B6B',      # 珊瑚红
        'secondary': '#4ECDC4',   # 青绿色
        'accent': '#FFE66D',       # 明黄色
        'dark': '#2C3E50',         # 深蓝灰
        'light': '#F8F9FA',        # 浅灰白
        'gradient_start': '#667EEA',  # 渐变起始
        'gradient_end': '#764BA2',    # 渐变结束
    }

    def __init__(self, output_dir: str = 'output', assets_dir: str = 'assets'):
        self.output_dir = Path(output_dir)
        self.assets_dir = Path(assets_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_cover_image(self, title: str, subtitle: str = "",
                          projects: List[Dict] = None) -> str:
        """
        创建封面图

        Args:
            title: 主标题
            subtitle: 副标题
            projects: 项目列表（用于展示）

        Returns:
            生成的图片路径
        """
        if not PIL_AVAILABLE:
            return self._create_placeholder_cover(title, subtitle)

        # 创建画布
        width, height = self.COVER_SIZE
        img = Image.new('RGB', (width, height), self.COLORS['dark'])
        draw = ImageDraw.Draw(img)

        # 绘制渐变背景
        for y in range(height):
            ratio = y / height
            r = int(102 + (118 - 102) * ratio)
            g = int(126 + (74 - 126) * ratio)
            b = int(234 + (162 - 234) * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # 绘制装饰元素
        self._draw_decorative_elements(draw, width, height)

        # 绘制标题
        self._draw_centered_text(draw, title, height // 3,
                                  font_size=80, color='white')

        # 绘制副标题
        if subtitle:
            self._draw_centered_text(draw, subtitle, height // 2,
                                    font_size=40, color=self.COLORS['accent'])

        # 绘制项目预览（如果提供）
        if projects:
            self._draw_projects_preview(draw, projects, height, width)

        # 绘制底部标签
        self._draw_bottom_badge(draw, width, height)

        # 保存
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = self.output_dir / f'cover_{timestamp}.png'
        img.save(output_path, 'PNG', quality=95)

        print(f"✅ 封面图已生成：{output_path}")
        return str(output_path)

    def _draw_decorative_elements(self, draw: ImageDraw, width: int, height: int):
        """绘制装饰元素"""
        # 圆形装饰
        draw.ellipse([width - 200, -100, width + 100, 200],
                    fill=self.COLORS['primary'] + '40')
        draw.ellipse([-50, height - 200, 150, height + 50],
                    fill=self.COLORS['secondary'] + '40')

        # 线条装饰
        for i in range(5):
            y = 100 + i * 30
            draw.line([50, y, 200, y], fill='white', width=2)

    def _draw_centered_text(self, draw: ImageDraw.Draw, text: str,
                           y: int, font_size: int = 60, color: str = 'white'):
        """绘制居中文字"""
        try:
            font = ImageFont.truetype("msyh.ttc", font_size)
        except:
            font = ImageFont.load_default()

        # 计算文字位置使其居中
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (self.COVER_SIZE[0] - text_width) // 2

        # 绘制阴影
        draw.text((x + 3, y + 3), text, font=font, fill='black')
        # 绘制文字
        draw.text((x, y), text, font=font, fill=color)

    def _draw_projects_preview(self, draw: ImageDraw.Draw, projects: List[Dict],
                               height: int, width: int):
        """绘制项目预览"""
        start_y = int(height * 0.55)
        box_height = 100
        padding = 20

        for i, project in enumerate(projects[:3]):
            y = start_y + i * (box_height + padding)

            # 项目卡片背景
            card_color = 'white'
            draw.rounded_rectangle([padding, y, width - padding, y + box_height],
                                 radius=15, fill=card_color + 'E0')

            # 项目名称
            name = project.get('name', '')[:20]
            stars = project.get('stargazers_count', 0)

            try:
                name_font = ImageFont.truetype("msyh.ttc", 28)
                stats_font = ImageFont.truetype("msyh.ttc", 20)
            except:
                name_font = ImageFont.load_default()
                stats_font = name_font

            draw.text((padding + 20, y + 20), name, font=name_font, fill=self.COLORS['dark'])
            draw.text((padding + 20, y + 60), f"⭐ {stars:,} stars",
                     font=stats_font, fill='#666666')

    def _draw_bottom_badge(self, draw: ImageDraw.Draw, width: int, height: int):
        """绘制底部标签"""
        badge_text = "GitHub AI Trending 🔥"

        try:
            font = ImageFont.truetype("msyh.ttc", 24)
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), badge_text, font=font)
        badge_width = bbox[2] - bbox[0] + 40
        badge_height = bbox[3] - bbox[1] + 20

        x = (width - badge_width) // 2
        y = height - badge_height - 60

        # 标签背景
        draw.rounded_rectangle([x, y, x + badge_width, y + badge_height],
                              radius=badge_height // 2, fill=self.COLORS['primary'])

        # 标签文字
        draw.text((x + 20, y + 8), badge_text, font=font, fill='white')

    def create_project_thumbnail(self, project: Dict) -> str:
        """为单个项目创建缩略图"""
        if not PIL_AVAILABLE:
            return self._create_placeholder_thumbnail(project)

        width, height = self.THUMBNAIL_SIZE
        img = Image.new('RGB', (width, height), self.COLORS['dark'])
        draw = ImageDraw.Draw(img)

        # 渐变背景
        for y in range(height):
            ratio = y / height
            r = int(45 + (100 - 45) * ratio)
            g = int(52 + (100 - 52) * ratio)
            b = int(79 + (100 - 79) * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # 项目名称
        name = project.get('name', 'Unknown')[:15]
        try:
            font = ImageFont.truetype("msyh.ttc", 32)
        except:
            font = ImageFont.load_default()

        draw.text((30, 30), name, font=font, fill='white')

        # Stars
        stars = project.get('stargazers_count', 0)
        draw.text((30, 80), f"⭐ {stars:,} stars", font=font, fill=self.COLORS['accent'])

        # 描述
        desc = project.get('description', '')[:40]
        if desc:
            draw.text((30, 150), desc, font=font, fill='white')

        # 语言标签
        lang = project.get('language', 'Unknown')
        draw.text((30, 350), f"💻 {lang}", font=font, fill=self.COLORS['secondary'])

        # 保存
        name_safe = project.get('name', 'unknown').replace('/', '_')
        timestamp = datetime.now().strftime('%Y%m%d')
        output_path = self.output_dir / f'thumb_{name_safe}_{timestamp}.png'
        img.save(output_path, 'PNG', quality=90)

        print(f"✅ 缩略图已生成：{output_path}")
        return str(output_path)

    def create_comparison_grid(self, projects: List[Dict]) -> str:
        """创建项目对比网格图"""
        if not PIL_AVAILABLE or len(projects) < 2:
            return "需要 PIL 库且至少 2 个项目"

        grid_cols = min(3, len(projects))
        grid_rows = (len(projects) + grid_cols - 1) // grid_cols

        cell_width = 400
        cell_height = 300
        width = cell_width * grid_cols
        height = cell_height * grid_rows

        img = Image.new('RGB', (width, height), self.COLORS['light'])
        draw = ImageDraw.Draw(img)

        for i, project in enumerate(projects):
            col = i % grid_cols
            row = i // grid_cols
            x = col * cell_width
            y = row * cell_height

            # 单元格背景
            draw.rectangle([x + 10, y + 10, x + cell_width - 10, y + cell_height - 10],
                         fill='white', outline=self.COLORS['primary'], width=2)

            # 项目名称
            name = project.get('name', '')[:12]
            try:
                name_font = ImageFont.truetype("msyh.ttc", 24)
                stat_font = ImageFont.truetype("msyh.ttc", 18)
            except:
                name_font = ImageFont.load_default()
                stat_font = name_font

            draw.text((x + 25, y + 30), name, font=name_font, fill=self.COLORS['dark'])
            draw.text((x + 25, y + 70), f"⭐ {project.get('stargazers_count', 0):,}",
                     font=stat_font, fill='#FF9500')
            draw.text((x + 25, y + 100), project.get('language', 'Unknown'),
                     font=stat_font, fill=self.COLORS['secondary'])

        # 保存
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = self.output_dir / f'comparison_{timestamp}.png'
        img.save(output_path, 'PNG', quality=90)

        print(f"✅ 对比图已生成：{output_path}")
        return str(output_path)

    def _create_placeholder_cover(self, title: str, subtitle: str) -> str:
        """创建占位封面（无 PIL 时）"""
        content = f"""# 封面图占位符

## 主标题
{title}

## 副标题
{subtitle}

---
请安装 Pillow 以生成实际图片:
pip install pillow
"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = self.output_dir / f'cover_placeholder_{timestamp}.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return str(output_path)

    def _create_placeholder_thumbnail(self, project: Dict) -> str:
        """创建占位缩略图"""
        content = f"""# 项目缩略图占位符

## {project.get('name', 'Unknown')}
- Stars: {project.get('stargazers_count', 0):,}
- Language: {project.get('language', 'Unknown')}
- Description: {project.get('description', 'N/A')}

---
请安装 Pillow 以生成实际图片
"""
        name_safe = project.get('name', 'unknown').replace('/', '_')
        output_path = self.output_dir / f'thumb_{name_safe}_placeholder.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return str(output_path)

    def generate_image_prompt(self, project: Dict) -> str:
        """
        生成用于 AI 绘图的提示词
        用于生成更具吸引力的封面图
        """
        name = project.get('name', '')
        desc = project.get('description', '')
        stars = project.get('stargazers_count', 0)

        prompt = f"""Create a vibrant social media cover image for a GitHub AI project:

Project: {name}
Description: {desc}
Stars: {stars:,}

Style requirements:
- Modern, eye-catching design
- Tech/AI theme with gradient background
- Chinese social media aesthetic (Xiaohongshu style)
- Include stars badge and GitHub branding elements
- Clean, minimalist layout with bold typography space

Colors: Coral red (#FF6B6B), Teal (#4ECDC4), Yellow (#FFE66D)
Size: 1080x1440 pixels (3:4 vertical format)
"""

        return prompt


def main():
    """测试函数"""
    print("🖼️ 小红书配图生成器")
    print("=" * 50)

    generator = ImageGenerator()

    # 测试封面图
    print("\n📦 生成测试封面图...")
    cover_path = generator.create_cover_image(
        title="GitHub AI 神器合集",
        subtitle="这 3 个项目，让我效率翻倍 ⚡️"
    )
    print(f"封面图路径: {cover_path}")

    # 测试项目缩略图
    print("\n📦 生成测试缩略图...")
    test_project = {
        'name': 'AutoGPT',
        'full_name': 'Significant-Gravitas/AutoGPT',
        'description': 'An experimental open-source attempt to make GPT-4 fully autonomous',
        'stargazers_count': 154000,
        'language': 'Python',
        'html_url': 'https://github.com/Significant-Gravitas/AutoGPT'
    }
    thumb_path = generator.create_project_thumbnail(test_project)
    print(f"缩略图路径: {thumb_path}")

    # 生成 AI 绘图提示词
    print("\n🎨 AI 绘图提示词：")
    print(generator.generate_image_prompt(test_project))


if __name__ == '__main__':
    main()
