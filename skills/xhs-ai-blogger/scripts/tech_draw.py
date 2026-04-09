#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
科技简约深色风绘图核心引擎
OASYS 小红书配图生成器 - 通用绘图模块
内置于 xhs-ai-blogger skill
"""

import os
from PIL import Image, ImageFont, ImageDraw

W, H = 1080, 1440

# ─── 主题配色 ────────────────────────────────────────────
THEMES = [
    # 0: 蓝黑科技（封面/项目介绍）
    {
        "bg": (10, 14, 26),
        "panel": (18, 24, 42),
        "accent": (0, 180, 255),
        "accent2": (0, 100, 200),
        "title_fg": (255, 255, 255),
        "subtitle_fg": (0, 200, 255),
        "text_fg": (200, 210, 230),
        "muted": (100, 120, 150),
        "tag_bg": (0, 60, 120),
        "highlight_bg": (0, 50, 100),
    },
    # 1: 紫黑极客（高级功能）
    {
        "bg": (12, 8, 20),
        "panel": (22, 16, 36),
        "accent": (180, 80, 255),
        "accent2": (100, 40, 180),
        "title_fg": (255, 255, 255),
        "subtitle_fg": (200, 120, 255),
        "text_fg": (210, 200, 230),
        "muted": (120, 100, 150),
        "tag_bg": (60, 20, 100),
        "highlight_bg": (50, 20, 80),
    },
    # 2: 绿黑终端（部署/配置）
    {
        "bg": (8, 16, 10),
        "panel": (12, 24, 14),
        "accent": (0, 255, 120),
        "accent2": (0, 150, 70),
        "title_fg": (255, 255, 255),
        "subtitle_fg": (0, 255, 130),
        "text_fg": (180, 230, 190),
        "muted": (80, 130, 90),
        "tag_bg": (0, 60, 30),
        "highlight_bg": (0, 50, 25),
    },
    # 3: 橙黑工业（模块展示）
    {
        "bg": (18, 12, 6),
        "panel": (28, 20, 10),
        "accent": (255, 140, 0),
        "accent2": (180, 80, 0),
        "title_fg": (255, 255, 255),
        "subtitle_fg": (255, 160, 40),
        "text_fg": (230, 210, 180),
        "muted": (140, 110, 70),
        "tag_bg": (80, 40, 0),
        "highlight_bg": (60, 30, 0),
    },
    # 4: 青黑赛博（AI功能）
    {
        "bg": (6, 16, 20),
        "panel": (10, 26, 32),
        "accent": (0, 230, 220),
        "accent2": (0, 130, 140),
        "title_fg": (255, 255, 255),
        "subtitle_fg": (0, 240, 230),
        "text_fg": (180, 220, 225),
        "muted": (80, 130, 140),
        "tag_bg": (0, 60, 70),
        "highlight_bg": (0, 50, 60),
    },
    # 5: 玫红极简（注意事项）
    {
        "bg": (16, 8, 14),
        "panel": (26, 14, 22),
        "accent": (255, 60, 130),
        "accent2": (160, 20, 80),
        "title_fg": (255, 255, 255),
        "subtitle_fg": (255, 80, 150),
        "text_fg": (230, 200, 215),
        "muted": (140, 100, 120),
        "tag_bg": (80, 20, 50),
        "highlight_bg": (60, 15, 40),
    },
]

FONT_PATHS = [
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/msyhbd.ttc", 
    "C:/Windows/Fonts/simhei.ttf",
    "C:/Windows/Fonts/simsun.ttc",
    "C:/Windows/Fonts/Arial.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]

def get_font(size, bold=False):
    if bold:
        for p in ["C:/Windows/Fonts/msyhbd.ttc", "C:/Windows/Fonts/simhei.ttf"]:
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    pass
    for p in FONT_PATHS:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def text_w(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]

def wrap(draw, text, font, max_w):
    lines = []
    for para in text.split('\n'):
        if not para.strip():
            lines.append('')
            continue
        cur = ''
        for ch in para:
            if text_w(draw, cur + ch, font) <= max_w:
                cur += ch
            else:
                if cur:
                    lines.append(cur)
                cur = ch
        if cur:
            lines.append(cur)
    return lines

def hline(draw, x0, y, x1, color, w=2):
    draw.rectangle([x0, y, x1, y + w], fill=color)

def dot(draw, x, y, color, r=5):
    draw.ellipse([x - r, y - r, x + r, y + r], fill=color)

def vline(draw, x, y0, y1, color, w=2):
    draw.rectangle([x, y0, x + w, y1], fill=color)

def draw_background(img, t, show_grid=True):
    draw = ImageDraw.Draw(img)
    if show_grid:
        gc = tuple(min(255, c + 15) for c in t["bg"])
        for gx in range(0, W, 80):
            draw.rectangle([gx, 0, gx + 1, H], fill=gc)
        for gy in range(0, H, 80):
            draw.rectangle([0, gy, W, gy + 1], fill=gc)

def draw_corners(draw, t):
    ac = t["accent"]
    draw.rectangle([0, 0, 60, 4], fill=ac)
    draw.rectangle([0, 0, 4, 60], fill=ac)
    draw.rectangle([W - 60, 0, W, 4], fill=ac)
    draw.rectangle([W - 4, 0, W, 60], fill=ac)
    draw.rectangle([0, H - 4, 60, H], fill=ac)
    draw.rectangle([0, H - 60, 4, H], fill=ac)
    draw.rectangle([W - 60, H - 4, W, H], fill=ac)
    draw.rectangle([W - 4, H - 60, W, H], fill=ac)

def draw_page_number(draw, page, total, t):
    f = get_font(28)
    s = f"[ {page} / {total} ]"
    sw = text_w(draw, s, f)
    draw.text((W - sw - 50, 28), s, fill=t["muted"], font=f)

def draw_kicker(draw, text, x, y, t, f=None):
    if f is None:
        f = get_font(24)
    tw = text_w(draw, text, f) + 28
    draw.rectangle([x, y, x + tw, y + 34], fill=t["highlight_bg"])
    draw.rectangle([x, y, x + 4, y + 34], fill=t["accent"])
    draw.text((x + 14, y + 6), text, fill=t["accent"], font=f)
    return x + tw + 12, y + 38

def draw_title_block(draw, title, x, y, t, size=72, line_h=85):
    tf = get_font(size, bold=True)
    ty = y
    for line in wrap(draw, title, tf, W - 100):
        draw.text((x, ty), line, fill=t["title_fg"], font=tf)
        ty += line_h
    return ty

def draw_subtitle_block(draw, subtitle, x, y, t, size=38):
    sf = get_font(size)
    sy = y
    for line in wrap(draw, subtitle, sf, W - 100):
        draw.text((x, sy), line, fill=t["subtitle_fg"], font=sf)
        sy += 50
    return sy

def draw_divider(draw, y, t, pad=50):
    hline(draw, pad, y, W - pad, t["accent"], 3)
    dot(draw, pad, y + 1, t["accent"], 5)
    dot(draw, W - pad, y + 1, t["accent"], 5)
    return y + 28

def draw_footer(draw, tags, t):
    fy = H - 108
    hline(draw, 0, fy, W, t["accent"], 2)
    draw.rectangle([0, fy + 2, W, H], fill=t["panel"])
    tg_f = get_font(26)
    tx = 50
    for tag in tags.split(' '):
        tag = tag.strip()
        if not tag:
            continue
        tw = text_w(draw, tag, tg_f) + 20
        draw.rectangle([tx, fy + 16, tx + tw, fy + 48], fill=t["highlight_bg"])
        draw.text((tx + 10, fy + 20), tag, fill=t["accent"], font=tg_f)
        tx += tw + 12

def draw_label(draw, text, x, y, t, f=None):
    if f is None:
        f = get_font(26)
    tw = text_w(draw, text, f) + 20
    draw.rectangle([x, y, x + tw, y + 28], fill=t["accent2"])
    draw.text((x + 10, y + 4), text, fill=(255, 255, 255), font=f)
    return y + 38

def draw_code_block(draw, lines, x, y, t, max_w=None, line_h=38):
    if max_w is None:
        max_w = W - 100
    visible = [ln for ln in lines if ln.strip()]
    if not visible:
        return y + 10
    bh = len(visible) * line_h + 24
    draw.rectangle([x, y, x + max_w, y + bh], fill=t["panel"])
    draw.rectangle([x, y, x + 4, y + bh], fill=t["accent"])
    draw.rectangle([x + 4, y, x + max_w, y + 26], fill=t["accent2"])
    hf = get_font(24)
    draw.text((x + 16, y + 5), " CODE", fill=(255, 255, 255), font=hf)
    cf = get_font(28)
    iy = y + 26
    for ln in visible:
        draw.text((x + 16, iy), ln, fill=t["accent"], font=cf)
        iy += line_h
    return iy + 12

def draw_bullet(draw, items, x, y, t, small_f=None, indent=38, bullet_r=6, line_h=42):
    if small_f is None:
        small_f = get_font(32)
    by = y
    for item in items:
        if isinstance(item, (list, tuple)):
            k, v = item[0], item[1] if len(item) > 1 else ""
            dot(draw, x + bullet_r, by + 14, t["accent"], bullet_r)
            kw = text_w(draw, k, small_f)
            draw.text((x + indent, by), k, fill=t["accent"], font=small_f)
            draw.text((x + indent + kw + 14, by), v, fill=t["text_fg"], font=small_f)
            by += line_h + 4
        else:
            dot(draw, x + bullet_r, by + 14, t["accent"], bullet_r)
            sub_lines = wrap(draw, item.strip(), small_f, W - 100 - indent)
            for i, sl in enumerate(sub_lines):
                ix = x + indent if i == 0 else x + indent + 4
                draw.text((ix, by), sl, fill=t["text_fg"], font=small_f)
                by += line_h
    return by + 8

def draw_text_block(draw, lines, x, y, t, f=None, line_h=46):
    if f is None:
        f = get_font(34)
    py = y
    for line in lines:
        if not line.strip():
            py += 16
            continue
        draw.text((x, py), line, fill=t["text_fg"], font=f)
        py += line_h
    return py + 10

def gen_card(cfg, output_path=None):
    """
    通用配图生成函数
    
    cfg = {
        "theme_idx": 0-5,           # 主题色索引
        "page_num": int,            # 当前页码
        "total": int,               # 总页数
        "kicker": str,             # 小标签
        "title": str,              # 主标题
        "subtitle": str,           # 副标题
        "sections": [
            {"type": "text", "lines": [...]},
            {"type": "bullet", "items": [...]},
            {"type": "kv", "items": [(k,v), ...]},
            {"type": "code", "lines": [...]},
            {"type": "label", "text": str},
            {"type": "divider"},
        ],
        "footer_tags": str,         # 底部标签
    }
    """
    t = THEMES[cfg.get("theme_idx", 0)]
    img = Image.new('RGB', (W, H), t["bg"])
    draw = ImageDraw.Draw(img)
    
    draw_background(img, t, show_grid=cfg.get("show_grid", True))
    draw_corners(draw, t)
    draw_page_number(draw, cfg.get("page_num", ""), cfg.get("total", ""), t)
    
    cy = 60
    if cfg.get("kicker"):
        _, cy = draw_kicker(draw, cfg["kicker"], 50, cy, t)
    
    cy = draw_title_block(draw, cfg["title"], 50, cy, t)
    
    if cfg.get("subtitle"):
        cy += 6
        cy = draw_subtitle_block(draw, cfg["subtitle"], 50, cy, t)
    
    cy += 6
    cy = draw_divider(draw, cy, t)
    
    body_f = get_font(34)
    small_f = get_font(30)
    
    for sec in cfg.get("sections", []):
        if cy > H - 200:
            break
        stype = sec.get("type", "text")
        if stype == "text":
            lines = sec.get("lines", [])
            if isinstance(lines, str):
                lines = wrap(draw, lines, body_f, W - 100)
            cy = draw_text_block(draw, lines, 50, cy, t, body_f)
        elif stype == "bullet":
            cy = draw_bullet(draw, sec.get("items", []), 50, cy, t, small_f)
        elif stype == "kv":
            cy = draw_bullet(draw, sec.get("items", []), 50, cy, t, small_f)
        elif stype == "code":
            cy = draw_code_block(draw, sec.get("lines", []), 50, cy, t)
        elif stype == "label":
            cy = draw_label(draw, sec["text"], 50, cy, t)
        elif stype == "divider":
            cy += 16
            hline(draw, 50, cy, W - 50, t["muted"], 1)
            cy += 24
    
    draw_footer(draw, cfg.get("footer_tags", "#AI #GitHub #开源"), t)
    
    if output_path:
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        img.save(output_path, "JPEG", quality=96)
        print(f"[OK] {os.path.basename(output_path)}")
    
    return img
