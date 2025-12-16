"""Convert exported Mailchimp HTML files into Jekyll Markdown posts.
- Title from <title> or first <h1>
- Date from filename prefix if present, else file mtime
- Converts HTML to Markdown
- Finds <img> src and rewrites to /assets/images/<filename>
"""

import sys, re, os, shutil, datetime
from pathlib import Path
from bs4 import BeautifulSoup
from markdownify import markdownify as md

SRC = Path(sys.argv[1])
DST = Path(sys.argv[2])
IMG_DIR = Path("assets/images")
IMG_DIR.mkdir(parents=True, exist_ok=True)
DST.mkdir(parents=True, exist_ok=True)

for html_file in SRC.glob("**/*.html"):
    raw = html_file.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(raw, "html.parser")

    # Pull title - skip Mailchimp template variables
    title = ""
    # Try H2 first (often the main heading in Mailchimp emails)
    h2 = soup.find("h2")
    if h2:
        title = h2.get_text(strip=True)
    # Fall back to H1
    if not title:
        h1 = soup.find("h1")
        if h1:
            title = h1.get_text(strip=True)
    # Fall back to HTML title (but skip template variables)
    if not title and soup.title:
        title = soup.title.string or ""
        if "*|MC:" in title or "*|" in title:
            title = ""
    # Last resort: derive from filename
    if not title:
        # Remove numeric prefix and clean up filename
        stem = html_file.stem
        # Remove leading numbers and underscores
        stem = re.sub(r"^\d+_?-?", "", stem)
        # Replace underscores and dashes with spaces, capitalize
        title = re.sub(r"[_-]+", " ", stem).strip()
        # Capitalize first letter of each word
        title = " ".join(word.capitalize() for word in title.split())
    title = re.sub(r"\s+", " ", title).strip()

    # Extract content from text blocks and images in order
    # Mailchimp uses .mceText divs for text and .mceImageBlockContainer for images
    content_parts = []

    # Find the main content section (mceSectionBody)
    body_section = soup.find(class_="mceSectionBody")
    if not body_section:
        body_section = soup.find("body")

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
            # Get position in document
            try:
                pos = list(body_section.descendants).index(block)
                content_elements.append((pos, "text", block))
            except (ValueError, AttributeError):
                content_elements.append((999999, "text", block))  # Fallback position

        # Find image containers (can be divs or tds with that class)
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
                            filename = os.path.basename(src.split("?")[0])
                            filename = re.sub(r"[^a-zA-Z0-9._-]", "_", filename)

                        alt_text = img.get("alt", "") or filename
                        content_parts.append(
                            f"![{alt_text}](/assets/images/{filename})"
                        )
                        content_parts.append("")
                        processed_images.add(img)

    # Fallback: if no body section found, use the old method but with proper image handling
    if not content_parts:
        # Collect all content elements (text and images) in document order
        processed_images = set()
        processed_text_blocks = set()
        content_elements = []
        
        # Find text blocks
        text_blocks = soup.find_all("div", class_="mceText", recursive=True)
        for block in text_blocks:
            # Skip footer blocks
            if block.find_parent(class_="mceSectionFooter"):
                continue
            # Skip header blocks with "View this email" links
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
                # Check if this image is already processed
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
                            filename = os.path.basename(src.split("?")[0])
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
                            filename = os.path.basename(src.split("?")[0])
                            filename = re.sub(r"[^a-zA-Z0-9._-]", "_", filename)
                        
                        alt_text = img.get("alt", "") or filename
                        content_parts.append(f"![{alt_text}](/assets/images/{filename})")
                        content_parts.append("")
                        processed_images.add(img)

    # If still no content, try a more comprehensive search
    if not content_parts:
        # Remove unwanted elements first
        for sel in [
            ".mcnTextContentFooter",
            "#footer",
            ".footer",
            'center[style*="powered"]',
            ".mceSectionFooter",
            'a[href*="ARCHIVE"]',
            'a[href*="SUBSCRIBE"]',
            'a[href*="UNSUB"]',
        ]:
            for n in soup.select(sel):
                n.decompose()

        # Try to extract just the body content
        body = soup.find("body")
        if body:
            # Remove script and style tags
            for tag in body.find_all(["script", "style"]):
                tag.decompose()
            body_html = str(body)
            body_md = md(body_html, heading_style="ATX")
            # Clean up template variables
            body_md = re.sub(r"\*\|[A-Z_:]+\|\*", "", body_md)
            body_md = re.sub(r"\n{3,}", "\n\n", body_md)
            content_parts.append(body_md.strip())

    body_md = "\n\n".join(content_parts)

    # Date
    # Try to discover a date in filename like 2023-06-12-Subject.html
    m = re.search(r"(20\d{2}-\d{2}-\d{2})", html_file.name)
    if m:
        date = datetime.datetime.fromisoformat(m.group(1))
    else:
        date = datetime.datetime.fromtimestamp(html_file.stat().st_mtime)

    # Slug - use original filename (minus numeric prefix) instead of title
    # Original filename format: 14174234_sagevoice-update-shifting-our-target-not-a-pivot-.html
    stem = html_file.stem
    # Remove leading numbers and underscores/dashes
    stem = re.sub(r"^\d+[_-]?", "", stem)
    # Remove trailing dashes/underscores
    stem = re.sub(r"[_-]+$", "", stem)
    # Convert to slug format
    slug = re.sub(r"[^a-z0-9-]+", "-", stem.lower()).strip("-")
    # Ensure slug is not empty
    if not slug:
        slug = re.sub(r"[^a-z0-9-]+", "-", title.lower()).strip("-") or html_file.stem

    out = DST / f"{date.strftime('%Y-%m-%d')}-{slug}.md"
    fm = (
        f"---\n"
        f'title: "{title}"\n'
        f"date: {date.strftime('%Y-%m-%d %H:%M:%S %z')}\n"
        f"categories: [newsletter]\n"
        f"tags: [mailchimp]\n"
        f"---\n\n"
    )
    out.write_text(fm + body_md, encoding="utf-8")
    print("Wrote", out)
