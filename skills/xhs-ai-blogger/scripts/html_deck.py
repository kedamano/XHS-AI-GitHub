#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书 AI 博主 - 单文件 HTML 翻页演示生成器
生成一个自包含的 index.html，支持横向翻页、键盘/滚轮导航、ESC 索引。

用法:
    python html_deck.py --project "名称" --repo "URL" --description "描述" \
                        --features "f1|f2|f3" --output "./output"

核心特性:
    - 单文件 HTML，拖进浏览器即可查看
    - 横向翻页动画（CSS transition + translateX）
    - 6 种科技主题色（蓝黑/紫黑/绿黑/橙黑/青黑/玫红）
    - 键盘 ← → / 滚轮 / 触屏 / 底部圆点导航
    - ESC 索引视图（缩略图网格）
    - B 键低功耗模式（禁用动画）
    - 响应式布局，适配不同屏幕
"""

import os
import sys
import json
import argparse
from datetime import datetime

# ─── 主题色（与 tech_draw.py 同步） ──────────────────────
THEMES = [
    {"name": "蓝黑科技", "bg": "10,14,26",     "panel": "18,24,42",    "accent": "0,180,255",   "accent2": "0,100,200",   "subtitle": "0,200,255",  "text": "200,210,230",  "muted": "100,120,150",  "tag_bg": "0,60,120"},
    {"name": "紫黑极客", "bg": "12,8,20",      "panel": "22,16,36",    "accent": "180,80,255",  "accent2": "100,40,180",  "subtitle": "200,120,255", "text": "210,200,230",  "muted": "120,100,150",  "tag_bg": "60,20,100"},
    {"name": "绿黑终端", "bg": "8,16,10",      "panel": "12,24,14",    "accent": "0,255,120",   "accent2": "0,150,70",    "subtitle": "0,255,130",   "text": "180,230,190",  "muted": "80,130,90",    "tag_bg": "0,60,30"},
    {"name": "橙黑工业", "bg": "18,12,6",      "panel": "28,20,10",    "accent": "255,140,0",   "accent2": "180,80,0",    "subtitle": "255,160,40",  "text": "230,210,180",  "muted": "140,110,70",   "tag_bg": "80,40,0"},
    {"name": "青黑赛博", "bg": "6,16,20",      "panel": "10,26,32",    "accent": "0,230,220",   "accent2": "0,130,140",   "subtitle": "0,240,230",   "text": "180,220,225",  "muted": "80,130,140",   "tag_bg": "0,60,70"},
    {"name": "玫红极简", "bg": "16,8,14",      "panel": "26,14,22",    "accent": "255,60,130",  "accent2": "160,20,80",   "subtitle": "255,80,150",  "text": "230,200,215",  "muted": "140,100,120",  "tag_bg": "80,20,50"},
]

# ─── HTML 模板 ────────────────────────────────────────────
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{deck_title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;500;600;700;900&family=Noto+Sans+SC:wght@300;400;500;700;900&family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=IBM+Plex+Mono:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:100%;height:100%;overflow:hidden;background:#0a0a0b;color:#f1efea;font-family:'Noto Sans SC',sans-serif;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}}

/* ─── Deck 容器 ─── */
#deck{{position:fixed;inset:0;width:10000vw;height:100vh;display:flex;flex-wrap:nowrap;transition:transform .9s cubic-bezier(.77,0,.175,1);z-index:10;will-change:transform}}
.slide{{width:100vw;height:100vh;flex:0 0 100vw;position:relative;padding:6vh 6vw 10vh 6vw;display:flex;flex-direction:column;overflow:hidden;--bg:20,20,22;--panel:30,30,35;--accent:0,180,255;--accent2:0,100,200;--text:220,220,230;--muted:120,120,140;--tag-bg:0,60,120;--subtitle:0,200,255}}
.slide::before{{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;background:rgba(var(--bg),.85);backdrop-filter:blur(2px)}}
.slide .bg-fill{{position:absolute;inset:0;z-index:-2;pointer-events:none;background:rgb(var(--bg))}}

/* ─── 网格背景 ─── */
.slide .grid-bg{{position:absolute;inset:0;z-index:-1;pointer-events:none;opacity:.06;background-image:linear-gradient(rgba(var(--accent),1) 1px,transparent 1px),linear-gradient(90deg,rgba(var(--accent),1) 1px,transparent 1px);background-size:80px 80px}}

/* ─── 四角装饰 ─── */
.slide .corner-tl{{position:absolute;top:0;left:0;width:60px;height:4px;background:rgb(var(--accent))}}
.slide .corner-tl::after{{content:"";position:absolute;top:0;left:0;width:4px;height:60px;background:rgb(var(--accent))}}
.slide .corner-tr{{position:absolute;top:0;right:0;width:60px;height:4px;background:rgb(var(--accent))}}
.slide .corner-tr::after{{content:"";position:absolute;top:0;right:0;width:4px;height:60px;background:rgb(var(--accent))}}
.slide .corner-bl{{position:absolute;bottom:0;left:0;width:60px;height:4px;background:rgb(var(--accent))}}
.slide .corner-bl::after{{content:"";position:absolute;bottom:0;left:0;width:4px;height:60px;background:rgb(var(--accent))}}
.slide .corner-br{{position:absolute;bottom:0;right:0;width:60px;height:4px;background:rgb(var(--accent))}}
.slide .corner-br::after{{content:"";position:absolute;bottom:0;right:0;width:4px;height:60px;background:rgb(var(--accent))}}

/* ─── 页码 ─── */
.slide .page-num{{position:absolute;top:3vh;right:3vw;font-family:'IBM Plex Mono',monospace;font-size:14px;letter-spacing:.14em;color:rgba(var(--muted),1);text-transform:uppercase}}

/* ─── Chrome 顶部栏 ─── */
.chrome{{display:flex;justify-content:space-between;align-items:flex-start;font-family:'IBM Plex Mono',monospace;font-size:12px;letter-spacing:.18em;text-transform:uppercase;opacity:.7;margin-bottom:2vh}}
.chrome .left,.chrome .right{{display:flex;gap:2.4em;align-items:center}}
.chrome .sep{{width:40px;height:1px;background:currentColor;opacity:.4}}

/* ─── Kicker 小标签 ─── */
.kicker{{display:inline-block;font-family:'IBM Plex Mono',monospace;font-size:13px;letter-spacing:.24em;text-transform:uppercase;padding:6px 14px;border:1px solid rgba(var(--accent),.6);color:rgb(var(--accent));margin-bottom:2.5vh;background:rgba(var(--tag-bg),.3);width:fit-content}}

/* ─── 标题 ─── */
h1.title{{font-family:'Noto Serif SC',serif;font-weight:900;font-size:4.2vw;line-height:1.08;letter-spacing:-.005em;color:#fff;margin-bottom:1.5vh}}
h2.subtitle{{font-family:'Noto Serif SC',serif;font-weight:400;font-size:1.8vw;line-height:1.4;letter-spacing:0;color:rgba(var(--subtitle),1);margin-bottom:2vh}}

/* ─── 分隔线 ─── */
.divider{{width:100%;height:2px;background:rgb(var(--accent));margin:2.5vh 0;position:relative}}
.divider::before{{content:"";position:absolute;left:0;top:-2px;width:6px;height:6px;border-radius:50%;background:rgb(var(--accent))}}
.divider::after{{content:"";position:absolute;right:0;top:-2px;width:6px;height:6px;border-radius:50%;background:rgb(var(--accent))}}

/* ─── Label 小标签 ─── */
.label{{display:inline-block;font-family:'IBM Plex Mono',monospace;font-size:13px;letter-spacing:.24em;text-transform:uppercase;padding:5px 12px;background:rgba(var(--accent2),.5);color:#fff;margin-bottom:1.5vh;width:fit-content;font-weight:500}}

/* ─── 文本块 ─── */
.text-block{{font-family:'Noto Sans SC',sans-serif;font-size:1.15vw;line-height:1.75;color:rgba(var(--text),.9);margin-bottom:1.5vh}}
.text-block p{{margin-bottom:.5vh}}

/* ─── Bullet 列表 ─── */
.bullet-list{{list-style:none;margin-bottom:1.5vh}}
.bullet-list li{{font-family:'Noto Sans SC',sans-serif;font-size:1.15vw;line-height:1.7;color:rgba(var(--text),.85);padding-left:1.5em;position:relative;margin-bottom:.6vh}}
.bullet-list li::before{{content:"";position:absolute;left:0;top:.6em;width:6px;height:6px;border-radius:50%;background:rgb(var(--accent))}}

/* ─── KV 键值对 ─── */
.kv-list{{list-style:none;margin-bottom:1.5vh}}
.kv-list li{{font-family:'Noto Sans SC',sans-serif;font-size:1.15vw;line-height:1.7;padding:.8vh 0;border-bottom:1px solid rgba(var(--muted),.2);display:flex;gap:1.5vw}}
.kv-list li:last-child{{border-bottom:none}}
.kv-list .k{{color:rgb(var(--accent));font-weight:600;flex:0 0 12vw;font-size:1vw}}
.kv-list .v{{color:rgba(var(--text),.85);flex:1}}

/* ─── Code 块 ─── */
.code-block{{background:rgba(var(--panel),1);border-left:4px solid rgb(var(--accent));padding:2vh 1.5vw;margin-bottom:1.5vh;font-family:'IBM Plex Mono',monospace;font-size:.95vw;line-height:1.65;color:rgb(var(--accent));overflow-x:auto}}
.code-block .code-header{{background:rgba(var(--accent2),.4);padding:.5vh 1vw;margin:-2vh -1.5vw 1.5vh -1.5vw;font-size:.85vw;color:#fff;letter-spacing:.12em}}
.code-block .code-line{{display:block;white-space:pre}}

/* ─── Footer 底部 ─── */
.foot{{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.14em;text-transform:uppercase;opacity:.55;padding-top:2vh;border-top:1px solid rgba(var(--accent),.3)}}
.foot .title{{font-family:'Noto Serif SC',serif;font-weight:400;letter-spacing:.05em;text-transform:none;opacity:.75;font-size:13px}}

/* ─── 标签 ─── */
.tags{{display:flex;flex-wrap:wrap;gap:.8vw;margin-top:1.5vh}}
.tag{{display:inline-block;font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.2em;text-transform:uppercase;padding:5px 10px;background:rgba(var(--tag-bg),.4);color:rgb(var(--accent));border:1px solid rgba(var(--accent),.3)}}

/* ─── 导航 ─── */
#nav{{position:fixed;left:50%;bottom:2.6vh;transform:translateX(-50%);z-index:30;display:flex;gap:10px;padding:8px 14px;border-radius:999px;background:rgba(0,0,0,.4);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px)}}
#nav .dot{{width:8px;height:8px;border-radius:50%;background:rgba(255,255,255,.3);cursor:pointer;transition:all .3s ease;border:0;padding:0}}
#nav .dot:hover{{background:rgba(255,255,255,.5);transform:scale(1.15)}}
#nav .dot.active{{background:rgba(255,255,255,.95);width:22px;border-radius:999px}}
#hint{{position:fixed;bottom:3vh;right:3vw;z-index:30;font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.2em;text-transform:uppercase;opacity:.4;color:#aaa;mix-blend-mode:difference}}

/* ─── ESC 索引 ─── */
#overview{{position:fixed;inset:0;z-index:100;background:rgba(10,10,11,.94);backdrop-filter:blur(12px);display:none;overflow-y:auto;padding:4vh 4vw}}
#overview .grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:2vh 1.6vw;max-width:90vw;margin:0 auto}}
#overview .card{{cursor:pointer;border-radius:6px;overflow:hidden;border:2px solid rgba(255,255,255,.15);transition:border-color .2s;display:flex;flex-direction:column}}
#overview .card:hover{{border-color:rgba(255,255,255,.5)}}
#overview .card.active{{border-color:rgba(0,180,255,.8)}}
#overview .card .thumb{{width:100%;aspect-ratio:16/10;overflow:hidden;position:relative;background:#111}}
#overview .card .thumb iframe{{width:100vw;height:100vh;transform:scale(.18);transform-origin:top left;position:absolute;top:0;left:0;border:none;pointer-events:none}}
#overview .card .label{{padding:6px 10px;font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#f1efea;opacity:.7;background:#111}}

/* ─── 低功耗模式 ─── */
body.low-power #deck{{transition:none!important}}
body.low-power *,
body.low-power *::before,
body.low-power *::after{{animation:none!important;transition:none!important}}

/* ─── 响应式 ─── */
@media (max-width:900px){{
    h1.title{{font-size:7vw}}
    h2.subtitle{{font-size:3vw}}
    .text-block,.bullet-list li,.kv-list li{{font-size:2.5vw}}
    .kicker,.label{{font-size:2.2vw}}
    #overview .grid{{grid-template-columns:repeat(2,1fr)}}
}}
</style>
</head>
<body>

<div id="deck">
{slides_html}
</div>

<div id="nav"></div>
<div id="hint">← → 翻页 · B 静态 · ESC 索引</div>

<div id="overview"></div>

<script>
const deck=document.getElementById('deck');
const slides=deck.querySelectorAll('.slide');
const nav=document.getElementById('nav');
let idx=0,total=slides.length,lock=false;
deck.style.width=(total*100)+'vw';

slides.forEach((s,i)=>{{
  const b=document.createElement('button');
  b.className='dot';b.dataset.i=i;b.setAttribute('aria-label','Page '+(i+1));
  b.onclick=()=>go(i);
  nav.appendChild(b);
}});

function go(n){{
  if(lock)return;
  idx=Math.max(0,Math.min(total-1,n));
  deck.style.transform=`translateX(${{-idx*100}}vw)`;
  nav.querySelectorAll('.dot').forEach((d,i)=>d.classList.toggle('active',i===idx));
  lock=true;setTimeout(()=>lock=false,700);
}}

/* ESC 索引 */
let overviewOn=false;
const ov=document.getElementById('overview');
function buildOverview(){{
  ov.innerHTML='<div class="grid"></div>';
  const grid=ov.querySelector('.grid');
  slides.forEach((s,i)=>{{
    const card=document.createElement('div');
    card.className='card'+(i===idx?' active':'');
    const thumb=document.createElement('div');
    thumb.className='thumb';
    const clone=s.cloneNode(true);
    clone.style.cssText='width:100vw;height:100vh;transform:scale(.18);transform-origin:top left;position:absolute;top:0;left:0;pointer-events:none';
    thumb.appendChild(clone);
    const label=document.createElement('div');
    label.className='label';
    label.textContent=(i+1)+' / '+total+'  '+s.dataset.kicker;
    card.appendChild(thumb);
    card.appendChild(label);
    card.onclick=()=>{{toggleOverview();go(i)}};
    grid.appendChild(card);
  }});
}}
function toggleOverview(){{
  overviewOn=!overviewOn;
  if({{buildOverview();ov.style.display='block';}}
  else{{ov.style.display='none';}}
}}

/* 键盘 */
addEventListener('keydown',e=>{{
  if(e.key==='Escape'){{e.preventDefault();toggleOverview();return;}}
  if(e.key && e.key.toLowerCase()==='b' && !e.metaKey && !e.ctrlKey && !e.altKey){{
    e.preventDefault();
    document.body.classList.toggle('low-power');
    return;
  }}
  if(overviewOn)return;
  if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' '||e.key==='ArrowDown'){{go(idx+1);return;}}
  if(e.key==='ArrowLeft'||e.key==='PageUp'||e.key==='ArrowUp')go(idx-1);
  if(e.key==='Home')go(0);
  if(e.key==='End')go(total-1);
}});

/* 滚轮 */
let wheelTO=null,wheelAcc=0;
addEventListener('wheel',e=>{{
  wheelAcc+=e.deltaY+e.deltaX;
  if(Math.abs(wheelAcc)>50){{go(idx+(wheelAcc>0?1:-1));wheelAcc=0;}}
  clearTimeout(wheelTO);wheelTO=setTimeout(()=>wheelAcc=0,150);
}},{{passive:true}});

/* 触屏 */
let tx=0,ty=0;
addEventListener('touchstart',e=>{{tx=e.touches[0].clientX;ty=e.touches[0].clientY}},{{passive:true}});
addEventListener('touchend',e=>{{
  const dx=(e.changedTouches[0].clientX-tx);
  const dy=(e.changedTouches[0].clientY-ty);
  if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy))go(idx+(dx<0?1:-1));
}},{{passive:true}});

go(0);
</script>
</body>
</html>
"""


def generate_slide_html(page_cfg, page_num, total):
    """将单个 page_cfg 转换为 slide HTML"""
    theme = THEMES[page_cfg.get("theme_idx", 0)]
    
    # CSS 变量
    css_vars = (
        f"--bg:{theme['bg']};"
        f"--panel:{theme['panel']};"
        f"--accent:{theme['accent']};"
        f"--accent2:{theme['accent2']};"
        f"--text:{theme['text']};"
        f"--muted:{theme['muted']};"
        f"--tag-bg:{theme['tag_bg']};"
        f"--subtitle:{theme['subtitle']}"
    )
    
    parts = []
    parts.append(f'<section class="slide" style="{css_vars}" data-kicker="{_esc(page_cfg.get("kicker",""))}">')
    parts.append(f'<div class="bg-fill"></div>')
    parts.append(f'<div class="grid-bg"></div>')
    parts.append(f'<div class="corner-tl"></div><div class="corner-tr"></div><div class="corner-bl"></div><div class="corner-br"></div>')
    parts.append(f'<div class="page-num">[ {page_num} / {total} ]</div>')
    
    # Chrome 顶部栏
    parts.append('<div class="chrome"><div class="left"><span>GitHub Trending</span><span class="sep"></span><span>AI Project</span></div><div class="right"><span>#AI #OpenSource</span></div></div>')
    
    # Kicker
    if page_cfg.get("kicker"):
        parts.append(f'<div class="kicker">{_esc(page_cfg["kicker"])}</div>')
    
    # Title
    title = page_cfg.get("title", "")
    if title:
        parts.append(f'<h1 class="title">{_esc(title)}</h1>')
    
    # Subtitle
    if page_cfg.get("subtitle"):
        parts.append(f'<h2 class="subtitle">{_esc(page_cfg["subtitle"])}</h2>')
    
    # Divider
    parts.append('<div class="divider"></div>')
    
    # Sections
    for sec in page_cfg.get("sections", []):
        stype = sec.get("type", "text")
        
        if stype == "label":
            parts.append(f'<div class="label">{_esc(sec.get("text",""))}</div>')
        
        elif stype == "text":
            lines = sec.get("lines", [])
            if isinstance(lines, str):
                lines = [lines]
            parts.append('<div class="text-block">')
            for line in lines:
                parts.append(f'<p>{_esc(line)}</p>')
            parts.append('</div>')
        
        elif stype == "bullet":
            items = sec.get("items", [])
            parts.append('<ul class="bullet-list">')
            for item in items:
                if isinstance(item, (list, tuple)):
                    k, v = item[0], item[1] if len(item) > 1 else ""
                    parts.append(f'<li><strong style="color:rgb(var(--accent))">{_esc(k)}</strong> {_esc(v)}</li>')
                else:
                    parts.append(f'<li>{_esc(str(item))}</li>')
            parts.append('</ul>')
        
        elif stype == "kv":
            items = sec.get("items", [])
            parts.append('<ul class="kv-list">')
            for item in items:
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    parts.append(f'<li><span class="k">{_esc(str(item[0]))}</span><span class="v">{_esc(str(item[1]))}</span></li>')
            parts.append('</ul>')
        
        elif stype == "code":
            lines = sec.get("lines", [])
            if isinstance(lines, str):
                lines = [lines]
            parts.append('<div class="code-block">')
            parts.append('<div class="code-header"> CODE</div>')
            for line in lines:
                parts.append(f'<span class="code-line">{_esc(line)}</span>')
            parts.append('</div>')
        
        elif stype == "divider":
            parts.append('<div class="divider"></div>')
    
    # Footer tags
    tags_str = page_cfg.get("footer_tags", "")
    if tags_str:
        tags = tags_str.split()
        parts.append('<div class="tags">')
        for tag in tags:
            tag = tag.strip()
            if tag:
                parts.append(f'<span class="tag">{_esc(tag)}</span>')
        parts.append('</div>')
    
    # Footer
    parts.append(f'<div class="foot"><div class="title">{_esc(page_cfg.get("project_name","GitHub AI"))}</div><div>{datetime.now().strftime("%Y-%m-%d")}</div></div>')
    
    parts.append('</section>')
    return "\n".join(parts)


def _esc(text):
    """HTML 转义"""
    if not text:
        return ""
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;"))


def generate_pages_data(project_name, repo_url, description, features, tags=None, github_path=None):
    """生成 6 页 slide 数据（与 xhs_blogger_pipeline.py 同步）"""
    if tags is None:
        tags = "#AI #人工智能 #AI工具 #GitHub #开源 #效率工具 #学习必备 #ChatGPT #AI助手 #黑科技"
    
    feature_list = [f.strip() for f in features.split("|") if f.strip()]
    if not github_path:
        github_path = repo_url.split("github.com/")[-1] if "github.com/" in repo_url else repo_url
    
    star_text = "[ Star 支持开源 ]"
    
    return [
        {
            "theme_idx": 0,
            "kicker": "GitHub 开源项目",
            "title": project_name,
            "subtitle": description,
            "project_name": project_name,
            "sections": [
                {"type": "label", "text": " 核心亮点"},
                {"type": "bullet", "items": feature_list[:5]},
                {"type": "divider"},
                {"type": "text", "lines": [f"GitHub: {github_path}"]},
            ],
            "footer_tags": tags,
        },
        {
            "theme_idx": 1,
            "kicker": "快速上手",
            "title": f"快速部署\n{project_name}",
            "project_name": project_name,
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
            "footer_tags": tags,
        },
        {
            "theme_idx": 4,
            "kicker": "核心能力",
            "title": "核心能力\n全景一览",
            "project_name": project_name,
            "sections": [
                {"type": "bullet", "items": feature_list[:5]},
                {"type": "divider"},
                {"type": "label", "text": " 技术特点"},
                {"type": "text", "lines": ["支持多平台", "简单易用", "持续更新"]},
            ],
            "footer_tags": tags,
        },
        {
            "theme_idx": 3,
            "kicker": "功能详解",
            "title": "功能模块\n深度解析",
            "project_name": project_name,
            "sections": [
                {"type": "label", "text": " 详细功能"},
                {"type": "bullet", "items": feature_list[:5]},
            ],
            "footer_tags": tags,
        },
        {
            "theme_idx": 2,
            "kicker": "使用体验",
            "title": "真实体验\n用户视角",
            "project_name": project_name,
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
            "footer_tags": tags,
        },
        {
            "theme_idx": 5,
            "kicker": "赶紧试试",
            "title": f"{project_name}\n等你来探索",
            "project_name": project_name,
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
            "footer_tags": tags,
        },
    ]


def generate_deck(project_name, repo_url, description, features, tags=None, output_dir="./output"):
    """生成完整的单文件 HTML 翻页演示"""
    os.makedirs(output_dir, exist_ok=True)
    
    pages = generate_pages_data(project_name, repo_url, description, features, tags)
    total = len(pages)
    
    slides_html = []
    for i, page in enumerate(pages, 1):
        slide_html = generate_slide_html(page, i, total)
        slides_html.append(slide_html)
    
    deck_title = f"{project_name} | GitHub AI Trending"
    html = HTML_TEMPLATE.format(
        deck_title=_esc(deck_title),
        slides_html="\n".join(slides_html),
    )
    
    output_path = os.path.join(output_dir, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    return output_path


def parse_args():
    parser = argparse.ArgumentParser(description="生成单文件 HTML 翻页演示")
    parser.add_argument("--project", "-p", required=True, help="项目名称")
    parser.add_argument("--repo", "-r", required=True, help="GitHub 仓库 URL")
    parser.add_argument("--description", "-d", required=True, help="项目描述")
    parser.add_argument("--features", "-f", required=True, help="核心功能，用 | 分隔")
    parser.add_argument("--tags", "-t", default=None, help="话题标签，用空格分隔")
    parser.add_argument("--output", "-o", default="./output", help="输出目录")
    return parser.parse_args()


def main():
    args = parse_args()
    output_path = generate_deck(
        project_name=args.project,
        repo_url=args.repo,
        description=args.description,
        features=args.features,
        tags=args.tags,
        output_dir=args.output,
    )
    print(f"✅ 生成完成: {output_path}")
    return output_path


if __name__ == "__main__":
    main()
