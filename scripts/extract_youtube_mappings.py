#!/usr/bin/env python3
"""
Extract YouTube video IDs and thumbnail mappings from HTML files.
"""

import re
from pathlib import Path
from collections import defaultdict

def extract_video_id(url):
    match = re.search(r'youtu\.be/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    match = re.search(r'youtube\.com/watch\?v=([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    return None

def extract_thumbnail_filename(img_src):
    match = re.search(r'/([^/]+\.(png|jpg|jpeg|gif))', img_src)
    if match:
        return match.group(1)
    return None

campaigns_dir = Path('_posts/campaigns_content')
mappings = defaultdict(list)

for html_file in campaigns_dir.glob('*.html'):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    youtube_pattern = r'href=["\'](https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]+))["\']'
    
    for match in re.finditer(youtube_pattern, content):
        video_id = match.group(2)
        start_pos = match.start()
        a_tag_start = content.rfind('<a', max(0, start_pos - 500), start_pos)
        if a_tag_start != -1:
            a_tag_end = content.find('</a>', start_pos, start_pos + 2000)
            if a_tag_end == -1:
                a_tag_end = start_pos + 2000
            a_tag_content = content[a_tag_start:a_tag_end]
            img_match = re.search(r'<img[^>]*src=["\']([^"\']+)["\']', a_tag_content)
            if img_match:
                img_src = img_match.group(1)
                thumb = extract_thumbnail_filename(img_src)
                if thumb:
                    key = f"{html_file.name}|{video_id}"
                    if thumb not in mappings[key]:
                        mappings[key].append(thumb)

# Print mappings
for key, thumbs in mappings.items():
    html_name, video_id = key.split('|')
    print(f"\n{html_name}")
    print(f"  Video ID: {video_id}")
    for thumb in thumbs:
        print(f"  Thumbnail: {thumb}")

