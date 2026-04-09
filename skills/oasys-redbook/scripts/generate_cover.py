#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OASYS 小红书配图 - 单图生成器
用法: python generate_cover.py --title "标题" --subtitle "副标题" --content "正文" --theme 0 --output xxx.jpg
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tech_draw import gen_card, wrap, get_font, W, H
from PIL import Image, ImageDraw

DEFAULT_OUTPUT = "oasys_cover.jpg"


def parse_args():
    parser = argparse.ArgumentParser(description="OASYS 小红书配图生成器")
    parser.add_argument("--title", "-t", required=True, help="主标题")
    parser.add_argument("--subtitle", "-s", default="", help="副标题")
    parser.add_argument("--content", "-c", default="", help="正文内容，多行用 | 分隔")
    parser.add_argument("--theme", default=None, type=int, choices=range(6),
                        help="主题色 0-5（0蓝黑 1紫黑 2绿黑 3橙黑 4青黑 5玫红）")
    parser.add_argument("--output", "-o", default=DEFAULT_OUTPUT,
                        help=f"输出文件名，默认 {DEFAULT_OUTPUT}")
    parser.add_argument("--page", "-p", type=int, default=0,
                        help="页码")
    parser.add_argument("--total", type=int, default=1,
                        help="总页数")
    parser.add_argument("--kicker", "-k", default="",
                        help="小标签")
    parser.add_argument("--tags", default="#OASYS  #OA办公自动化",
                        help="底部标签，多个用空格分隔")
    return parser.parse_args()


def main():
    args = parse_args()

    # 解析正文
    content_lines = []
    if args.content:
        for part in args.content.split('|'):
            stripped = part.strip()
            if stripped:
                content_lines.append(stripped)

    # 构建配置
    cfg = {
        "theme_idx": args.theme if args.theme is not None else 0,
        "page_num": args.page or 1,
        "total": args.total or 1,
        "kicker": args.kicker or None,
        "title": args.title,
        "subtitle": args.subtitle or None,
        "sections": [],
        "footer_tags": '  '.join(args.tags.split()),
    }

    # 添加正文
    if content_lines:
        cfg["sections"].append({"type": "text", "lines": content_lines})

    # 输出路径
    output = os.path.abspath(args.output)
    os.makedirs(os.path.dirname(output) or '.', exist_ok=True)

    gen_card(cfg, output)
    print(f"\n[Path] {output}")


if __name__ == "__main__":
    main()
