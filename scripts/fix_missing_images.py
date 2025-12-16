#!/usr/bin/env python3
"""
Re-convert HTML files that are missing images, preserving existing front matter.
"""
import sys
from pathlib import Path
import re
from bs4 import BeautifulSoup
from markdownify import markdownify as md

def extract_front_matter(md_file):
    """Extract front matter from existing markdown file."""
    if not md_file.exists():
        return None
    
    content = md_file.read_text(encoding='utf-8', errors='ignore')
    front_matter_match = re.search(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if front_matter_match:
        return front_matter_match.group(1)
    return None

def convert_html_to_markdown(html_file, output_dir):
    """Convert HTML to markdown, extracting content only."""
    raw = html_file.read_text(encoding='utf-8', errors='ignore')
    soup = BeautifulSoup(raw, 'html.parser')
    
    content_parts = []
    
    # Try to find body section first
    body_section = soup.find(class_="mceSectionBody")
    
    if body_section:
        # Collect all content elements with their document positions
        processed_images = set()
        processed_text_blocks = set()
        content_elements = []

        # Find text blocks
        text_blocks = body_section.find_all("div", class_="mceText", recursive=True)
        for block in text_blocks:
            if block.find_parent(class_="mceSectionFooter"):
                continue
            if block.find("a", href=lambda x: x and "*|ARCHIVE|*" in str(x)):
                continue
            try:
                pos = list(body_section.descendants).index(block)
                content_elements.append((pos, "text", block))
            except (ValueError, AttributeError):
                content_elements.append((999999, "text", block))

        # Find image containers
        image_containers = body_section.find_all(
            ["div", "td"], class_="mceImageBlockContainer", recursive=True
        )
        for container in image_containers:
            if container.find_parent(class_="mceSectionFooter"):
                continue
            if container.find("img", class_="mceLogo"):
                continue
            try:
                pos = list(body_section.descendants).index(container)
                content_elements.append((pos, "image_container", container))
            except (ValueError, AttributeError):
                content_elements.append((999999, "image_container", container))

        # Sort by document position
        content_elements.sort(key=lambda x: x[0])

        # Process in order
        for pos, elem_type, elem in content_elements:
            if elem_type == "text":
                if elem in processed_text_blocks:
                    continue

                block_html = str(elem)
                block_md = md(block_html, heading_style="ATX")
                block_md = re.sub(r"\*\|[A-Z_:]+\|\*", "", block_md)
                block_md = re.sub(r"\n{3,}", "\n\n", block_md)

                if block_md.strip():
                    content_parts.append(block_md.strip())
                    processed_text_blocks.add(elem)

            elif elem_type == "image_container":
                img = elem.find("img")
                if img and img not in processed_images:
                    if "mceLogo" in img.get("class", []):
                        continue

                    src = img.get("src", "")
                    if src and "mcusercontent.com" in src:
                        filename_match = re.search(
                            r"/([^/]+\.(jpg|jpeg|png|gif|webp))", src, re.IGNORECASE
                        )
                        if filename_match:
                            filename = filename_match.group(1)
                        else:
                            filename = Path(src.split("?")[0]).name
                            filename = re.sub(r"[^a-zA-Z0-9._-]", "_", filename)

                        alt_text = img.get("alt", "") or filename
                        content_parts.append(
                            f"![{alt_text}](/assets/images/{filename})"
                        )
                        content_parts.append("")
                        processed_images.add(img)

    # Fallback: if no body section found
    if not content_parts:
        processed_images = set()
        processed_text_blocks = set()
        content_elements = []
        
        # Find text blocks
        text_blocks = soup.find_all("div", class_="mceText", recursive=True)
        for block in text_blocks:
            if block.find_parent(class_="mceSectionFooter"):
                continue
            if block.find("a", href=lambda x: x and "*|ARCHIVE|*" in str(x)):
                continue
            
            try:
                pos = list(soup.descendants).index(block)
                content_elements.append((pos, "text", block))
            except (ValueError, AttributeError):
                content_elements.append((999999, "text", block))
        
        # Find images in mceImageBlockContainer
        image_containers = soup.find_all(["div", "td"], class_="mceImageBlockContainer", recursive=True)
        for container in image_containers:
            if container.find_parent(class_="mceSectionFooter"):
                continue
            if container.find("img", class_="mceLogo"):
                continue
            try:
                pos = list(soup.descendants).index(container)
                content_elements.append((pos, "image_container", container))
            except (ValueError, AttributeError):
                content_elements.append((999999, "image_container", container))
        
        # Find images in mceBlockContainer (older Mailchimp format)
        block_containers = soup.find_all(["div", "td"], class_="mceBlockContainer", recursive=True)
        for container in block_containers:
            if container.find_parent(class_="mceSectionFooter"):
                continue
            img = container.find("img")
            if img and "mceLogo" not in img.get("class", []):
                if img not in processed_images:
                    try:
                        pos = list(soup.descendants).index(container)
                        content_elements.append((pos, "image_block", container))
                    except (ValueError, AttributeError):
                        content_elements.append((999999, "image_block", container))
        
        # Sort by document position
        content_elements.sort(key=lambda x: x[0])
        
        # Process in order
        for pos, elem_type, elem in content_elements:
            if elem_type == "text":
                if elem in processed_text_blocks:
                    continue
                
                block_html = str(elem)
                block_md = md(block_html, heading_style="ATX")
                block_md = re.sub(r"\*\|[A-Z_:]+\|\*", "", block_md)
                block_md = re.sub(r"\n{3,}", "\n\n", block_md)
                
                if block_md.strip():
                    content_parts.append(block_md.strip())
                    processed_text_blocks.add(elem)
            
            elif elem_type == "image_container":
                img = elem.find("img")
                if img and img not in processed_images:
                    src = img.get("src", "")
                    if src and "mcusercontent.com" in src:
                        filename_match = re.search(
                            r"/([^/]+\.(jpg|jpeg|png|gif|webp))", src, re.IGNORECASE
                        )
                        if filename_match:
                            filename = filename_match.group(1)
                        else:
                            filename = Path(src.split("?")[0]).name
                            filename = re.sub(r"[^a-zA-Z0-9._-]", "_", filename)
                        
                        alt_text = img.get("alt", "") or filename
                        content_parts.append(f"![{alt_text}](/assets/images/{filename})")
                        content_parts.append("")
                        processed_images.add(img)
            
            elif elem_type == "image_block":
                img = elem.find("img")
                if img and img not in processed_images:
                    src = img.get("src", "")
                    if src and "mcusercontent.com" in src:
                        filename_match = re.search(
                            r"/([^/]+\.(jpg|jpeg|png|gif|webp))", src, re.IGNORECASE
                        )
                        if filename_match:
                            filename = filename_match.group(1)
                        else:
                            filename = Path(src.split("?")[0]).name
                            filename = re.sub(r"[^a-zA-Z0-9._-]", "_", filename)
                        
                        alt_text = img.get("alt", "") or filename
                        content_parts.append(f"![{alt_text}](/assets/images/{filename})")
                        content_parts.append("")
                        processed_images.add(img)
    
    return "\n\n".join(content_parts)

def main():
    html_dir = Path("_posts/campaigns_content")
    output_dir = Path("_posts")
    
    # Find HTML files that need fixing (those without mceSectionBody)
    html_files = list(html_dir.glob("*.html"))
    files_to_fix = []
    
    for html_file in html_files:
        content = html_file.read_text(encoding='utf-8', errors='ignore')
        if 'mceSectionBody' not in content and 'mceBlockContainer' in content:
            files_to_fix.append(html_file)
    
    print(f"Found {len(files_to_fix)} files to fix")
    
    for html_file in files_to_fix:
        print(f"\nProcessing {html_file.name}...")
        
        # Find corresponding markdown file
        stem = html_file.stem
        # Remove numeric prefix
        stem = re.sub(r'^\d+_?-?', '', stem)
        slug = re.sub(r'[^a-z0-9-]+', '-', stem.lower()).strip('-')
        
        # Find matching markdown file
        md_files = list(output_dir.glob(f"*-{slug}.md"))
        if not md_files:
            # Try to find by partial match
            md_files = [f for f in output_dir.glob("*.md") if slug in f.stem]
        
        if not md_files:
            print(f"  Warning: No matching markdown file found for {html_file.name}")
            continue
        
        md_file = md_files[0]
        print(f"  Found: {md_file.name}")
        
        # Extract existing front matter
        existing_front_matter = extract_front_matter(md_file)
        if not existing_front_matter:
            print(f"  Warning: No front matter found in {md_file.name}, skipping")
            continue
        
        # Convert HTML to markdown content
        new_content = convert_html_to_markdown(html_file, output_dir)
        
        # Write with preserved front matter
        output = f"---\n{existing_front_matter}\n---\n\n{new_content}\n"
        md_file.write_text(output, encoding='utf-8')
        
        image_count = new_content.count("![")
        print(f"  ✓ Updated with {image_count} images")

if __name__ == "__main__":
    main()

