#!/usr/bin/env python3
# ============================================================
# generate.py — 将日报内容写入 index.html 并部署
# 由 CatDesk Automation 每日调用
# 用法: python3 generate.py --date "2026-03-21" --content content.json
# ============================================================

import json
import sys
import os
import subprocess
import argparse
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(SCRIPT_DIR, "template.html")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "public", "index.html")
ARCHIVE_DIR = os.path.join(SCRIPT_DIR, "archive")
ARCHIVE_INDEX = os.path.join(SCRIPT_DIR, "public", "archive.json")

WEEKDAYS = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]


def format_date(date_str):
    """将 2026-03-21 转为 2026年3月21日 · 星期五"""
    d = datetime.strptime(date_str, "%Y-%m-%d")
    wd = WEEKDAYS[d.weekday()]
    return f"{d.year}年{d.month}月{d.day}日 · {wd}"


def build_track_a_cards(items):
    html = ""
    for i, item in enumerate(items, 1):
        html += f"""
    <div class="card">
      <div class="card-header">
        <span class="card-num a">{i:02d}</span>
        <span class="card-title">{item['title']}</span>
      </div>
      <div class="card-body">{item['desc']}</div>
      <div class="insight a">
        <div class="insight-label a">⚡ 闪购迁移洞察</div>
        <div class="insight-text">{item['insight']}</div>
      </div>
      <div class="card-source">
        <span class="source-dot a"></span>
        <a href="{item['url']}" target="_blank" rel="noopener">{item['url_display']}</a>
      </div>
    </div>"""
    return html


def build_track_b_cards(items):
    html = ""
    for i, item in enumerate(items, 1):
        html += f"""
    <div class="card">
      <div class="card-header">
        <span class="card-num b">{i:02d}</span>
        <span class="card-title">{item['title']}</span>
      </div>
      <div class="card-body">{item['desc']}</div>
      <div class="insight b">
        <div class="insight-label b">📌 核心结论</div>
        <div class="insight-text">{item['insight']}</div>
      </div>
      <div class="card-source">
        <span class="source-dot b"></span>
        <a href="{item['url']}" target="_blank" rel="noopener">{item['url_display']}</a>
      </div>
    </div>"""
    return html


def build_judgment_items(items):
    html = ""
    nums = ["01", "02", "03", "04"]
    for i, item in enumerate(items):
        html += f"""
    <div class="judgment-item">
      <span class="judgment-num">{nums[i]}</span>
      <div class="judgment-text"><strong>{item['headline']}</strong>{item['body']}</div>
    </div>"""
    return html


def build_archive_links(archive_list, current_date):
    html = f'<a class="archive-item" href="#">{current_date}（当前）</a>\n'
    for entry in reversed(archive_list[-30:]):  # 最多显示最近30天
        d = entry['date']
        html += f'<a class="archive-item" href="archive/{d}.html">{d}</a>\n'
    return html


def build_sources_text(track_a, track_b):
    sources = set()
    for item in track_a + track_b:
        sources.add(item.get('source_name', ''))
    return ' · '.join(s for s in sources if s)


def generate(date_str, content):
    date_display = format_date(date_str)

    track_a_html = build_track_a_cards(content['track_a'])
    track_b_html = build_track_b_cards(content['track_b'])
    judgment_html = build_judgment_items(content['judgment'])

    # 读取历史归档列表
    archive_list = []
    if os.path.exists(ARCHIVE_INDEX):
        with open(ARCHIVE_INDEX, 'r') as f:
            archive_list = json.load(f)

    archive_html = build_archive_links(archive_list, date_str)
    sources_text = build_sources_text(content['track_a'], content['track_b'])

    # 读取模板
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template = f.read()

    # 替换占位符
    html = template
    html = html.replace("{{DATE_DISPLAY}}", date_display)
    html = html.replace("{{DATE_STR}}", date_str)
    html = html.replace("{{TRACK_A_CARDS}}", track_a_html)
    html = html.replace("{{TRACK_B_CARDS}}", track_b_html)
    html = html.replace("{{JUDGMENT_ITEMS}}", judgment_html)
    html = html.replace("{{ARCHIVE_LINKS}}", archive_html)
    html = html.replace("{{SOURCES_TEXT}}", sources_text)

    # 保存当前 index.html
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(html)

    # 同时保存到 archive/
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    archive_html_path = os.path.join(SCRIPT_DIR, "public", "archive", f"{date_str}.html")
    os.makedirs(os.path.dirname(archive_html_path), exist_ok=True)
    with open(archive_html_path, 'w', encoding='utf-8') as f:
        f.write(html)

    # 更新归档索引
    if not any(e['date'] == date_str for e in archive_list):
        archive_list.append({'date': date_str})
        with open(ARCHIVE_INDEX, 'w') as f:
            json.dump(archive_list, f)

    print(f"✅ 已生成 {date_str} 日报 → {OUTPUT_PATH}")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="日期，格式 YYYY-MM-DD")
    parser.add_argument("--content", required=True, help="内容JSON文件路径")
    args = parser.parse_args()

    with open(args.content, 'r', encoding='utf-8') as f:
        content = json.load(f)

    generate(args.date, content)
