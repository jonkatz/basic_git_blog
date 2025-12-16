#!/usr/bin/env python3
"""
Script to download all images (.png, .gif, .jpeg, .jpg) from HTML files
in the campaigns_content folder and save them to assets/images.
"""

import os
import re
import urllib.request
import urllib.parse
from pathlib import Path
from html.parser import HTMLParser
from collections import defaultdict

class ImageExtractor(HTMLParser):
    """HTML parser to extract image URLs from src attributes."""
    
    def __init__(self):
        super().__init__()
        self.image_urls = []
    
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for attr_name, attr_value in attrs:
                if attr_name == 'src' and attr_value:
                    self.image_urls.append(attr_value)

def extract_image_urls(html_file_path):
    """Extract all image URLs from an HTML file."""
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    parser = ImageExtractor()
    parser.feed(html_content)
    return parser.image_urls

def get_filename_from_url(url):
    """Extract filename from URL, handling query parameters."""
    # Parse URL and get the path
    parsed = urllib.parse.urlparse(url)
    path = parsed.path
    
    # Get the last part of the path (filename)
    filename = os.path.basename(path)
    
    # Remove query parameters if any
    if '?' in filename:
        filename = filename.split('?')[0]
    
    return filename

def is_image_url(url):
    """Check if URL points to an image file."""
    image_extensions = ['.png', '.gif', '.jpeg', '.jpg']
    filename = get_filename_from_url(url)
    return any(filename.lower().endswith(ext) for ext in image_extensions)

def download_image(url, output_path):
    """Download an image from URL to output path."""
    try:
        # Create a request with a user agent to avoid blocking
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        with urllib.request.urlopen(req) as response:
            with open(output_path, 'wb') as out_file:
                out_file.write(response.read())
        return True
    except Exception as e:
        print(f"  Error downloading {url}: {e}")
        return False

def main():
    # Set up paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    campaigns_dir = project_root / '_posts' / 'campaigns_content'
    images_dir = project_root / 'assets' / 'images'
    
    # Ensure images directory exists
    images_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all HTML files
    html_files = list(campaigns_dir.glob('*.html'))
    
    if not html_files:
        print(f"No HTML files found in {campaigns_dir}")
        return
    
    print(f"Found {len(html_files)} HTML files")
    
    # Collect all unique image URLs
    all_image_urls = set()
    url_to_files = defaultdict(list)
    
    for html_file in html_files:
        print(f"Processing {html_file.name}...")
        image_urls = extract_image_urls(html_file)
        
        for url in image_urls:
            if is_image_url(url):
                all_image_urls.add(url)
                url_to_files[url].append(html_file.name)
    
    print(f"\nFound {len(all_image_urls)} unique image URLs")
    
    # Download images
    downloaded = 0
    skipped = 0
    failed = 0
    
    for url in sorted(all_image_urls):
        filename = get_filename_from_url(url)
        output_path = images_dir / filename
        
        # Skip if already exists
        if output_path.exists():
            print(f"Skipping {filename} (already exists)")
            skipped += 1
            continue
        
        print(f"Downloading {filename}...")
        if download_image(url, output_path):
            downloaded += 1
            print(f"  ✓ Saved to {output_path}")
        else:
            failed += 1
    
    print(f"\nSummary:")
    print(f"  Downloaded: {downloaded}")
    print(f"  Skipped (already exists): {skipped}")
    print(f"  Failed: {failed}")
    print(f"  Total: {len(all_image_urls)}")

if __name__ == '__main__':
    main()

