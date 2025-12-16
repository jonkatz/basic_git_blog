#!/usr/bin/env python3
"""
Script to find YouTube embeds in campaigns_content HTML files and replace
corresponding image placeholders in markdown files with YouTube embeds.
"""

import re
import os
from pathlib import Path
from typing import List, Tuple, Dict

def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from URL."""
    # Handle youtu.be/VIDEO_ID
    match = re.search(r'youtu\.be/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    
    # Handle youtube.com/watch?v=VIDEO_ID
    match = re.search(r'youtube\.com/watch\?v=([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    
    return None

def extract_thumbnail_filename(img_src: str) -> str:
    """Extract thumbnail filename from image src URL."""
    # Extract filename from URLs like:
    # https://mcusercontent.com/.../video_thumbnails_new/FILENAME.png
    # https://mcusercontent.com/.../images/FILENAME.png
    match = re.search(r'/([^/]+\.(png|jpg|jpeg|gif))', img_src)
    if match:
        return match.group(1)
    return None

def find_youtube_embeds_in_html(html_file: Path) -> List[Tuple[str, str]]:
    """
    Find YouTube embeds in HTML file.
    Returns list of (video_id, thumbnail_filename) tuples.
    """
    results = []
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all YouTube URLs first
    youtube_url_pattern = r'href=["\'](https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]+))["\']'
    
    for url_match in re.finditer(youtube_url_pattern, content):
        video_url = url_match.group(1)
        video_id = url_match.group(2)
        
        # Find the <a> tag that contains this href
        start_pos = url_match.start()
        # Look backwards for the opening <a> tag
        a_tag_start = content.rfind('<a', max(0, start_pos - 500), start_pos)
        if a_tag_start == -1:
            continue
        
        # Find the closing </a> tag
        a_tag_end = content.find('</a>', start_pos, start_pos + 2000)
        if a_tag_end == -1:
            # Try to find it in a larger range or look for self-closing pattern
            a_tag_end = start_pos + 2000
        
        # Extract the content between <a> and </a>
        a_tag_content = content[a_tag_start:a_tag_end]
        
        # Find image src within this <a> tag content
        img_pattern = r'<img[^>]*src=["\']([^"\']+)["\']'
        img_match = re.search(img_pattern, a_tag_content)
        
        if img_match:
            img_src = img_match.group(1)
            thumbnail_filename = extract_thumbnail_filename(img_src)
            if thumbnail_filename:
                if (video_id, thumbnail_filename) not in results:
                    results.append((video_id, thumbnail_filename))
    
    return results

def find_corresponding_markdown(html_file: Path, posts_dir: Path) -> Path:
    """Find the corresponding markdown file for an HTML file."""
    # Extract the base name (e.g., "14175582_sagevoice-update-prolly-winding-down-")
    html_name = html_file.stem
    
    # Extract key words from HTML filename
    # Pattern: ID_description
    # Examples: 
    #   14175582_sagevoice-update-prolly-winding-down- -> prolly-winding-down
    #   14176398_sagevoice-post-mortem-1-of-2-what-went-wrong- -> post-mortem-1-of-2-what-went-wrong
    
    # Remove the ID prefix
    match = re.search(r'_\d+_(.+)', html_name)
    if match:
        descriptive_part = match.group(1).rstrip('-').lower()
        
        # Get key words (last few words are usually most unique)
        words = descriptive_part.split('-')
        # Use last 4-6 words as key identifier (more words = more unique)
        key_words = '-'.join(words[-6:]) if len(words) > 6 else descriptive_part
        
        # Search for matching markdown files
        # Try multiple matching strategies
        for md_file in posts_dir.glob('*.md'):
            md_name = md_file.stem.lower()
            # Remove date prefix (YYYY-MM-DD-)
            md_name_clean = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', md_name)
            
            # Strategy 1: Check if key words appear in markdown filename (either way)
            if key_words in md_name_clean or md_name_clean in key_words:
                return md_file
            
            # Strategy 2: Check if descriptive part (without sagevoice/update prefixes) matches
            # Remove common prefixes from both for comparison
            desc_clean = re.sub(r'^sagevoice-', '', descriptive_part)
            desc_clean = re.sub(r'^update-', '', desc_clean)
            md_clean_no_prefix = re.sub(r'^sagevoice-', '', md_name_clean)
            md_clean_no_prefix = re.sub(r'^update-', '', md_clean_no_prefix)
            
            if desc_clean in md_clean_no_prefix or md_clean_no_prefix in desc_clean:
                return md_file
            
            # Strategy 3: Check if most of the key words match
            key_word_list = [w for w in key_words.split('-') if len(w) > 2]  # Ignore short words
            if len(key_word_list) >= 2:
                # Check if at least 60% of key words match
                matches = sum(1 for word in key_word_list if word in md_name_clean)
                if matches >= max(2, len(key_word_list) * 0.6):
                    return md_file
    
    return None

def replace_image_with_youtube_embed(md_file: Path, thumbnail_filename: str, video_id: str) -> bool:
    """Replace image placeholder with YouTube embed in markdown file."""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match image tags with the thumbnail filename
    # Match: <img src="{{ site.baseurl }}/assets/images/THUMBNAIL.png" alt="...">
    pattern = rf'<img\s+src=["\']{{{{\s*site\.baseurl\s*}}}}/assets/images/{re.escape(thumbnail_filename)}["\']\s+alt=["\'][^"\']*["\']\s*>'
    
    youtube_embed = f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    
    if re.search(pattern, content):
        new_content = re.sub(pattern, youtube_embed, content)
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    
    return False

def main():
    campaigns_dir = Path('_posts/campaigns_content')
    posts_dir = Path('_posts')
    
    if not campaigns_dir.exists():
        print(f"Error: {campaigns_dir} does not exist")
        return
    
    if not posts_dir.exists():
        print(f"Error: {posts_dir} does not exist")
        return
    
    # Process all HTML files
    html_files = list(campaigns_dir.glob('*.html'))
    
    replacements_made = []
    
    for html_file in html_files:
        print(f"\nProcessing {html_file.name}...")
        
        # Find YouTube embeds
        youtube_embeds = find_youtube_embeds_in_html(html_file)
        
        if not youtube_embeds:
            print(f"  No YouTube embeds found")
            continue
        
        print(f"  Found {len(youtube_embeds)} YouTube embed(s)")
        
        # Find corresponding markdown file
        md_file = find_corresponding_markdown(html_file, posts_dir)
        
        if not md_file:
            print(f"  Could not find corresponding markdown file")
            continue
        
        print(f"  Found markdown file: {md_file.name}")
        
        # Replace images with YouTube embeds
        for video_id, thumbnail_filename in youtube_embeds:
            print(f"    Looking for thumbnail: {thumbnail_filename} (video: {video_id})")
            if replace_image_with_youtube_embed(md_file, thumbnail_filename, video_id):
                print(f"    ✓ Replaced image with YouTube embed")
                replacements_made.append((md_file.name, thumbnail_filename, video_id))
            else:
                print(f"    ✗ Image not found in markdown file")
    
    print(f"\n\nSummary:")
    print(f"Total replacements made: {len(replacements_made)}")
    for md_name, thumb, vid_id in replacements_made:
        print(f"  - {md_name}: {thumb} -> {vid_id}")

if __name__ == '__main__':
    main()

