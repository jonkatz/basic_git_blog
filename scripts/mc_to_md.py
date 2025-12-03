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

    # Pull title
    title = (soup.title.string if soup.title else "") or ""
    if not title:
        h1 = soup.find(["h1", "h2"])
        title = h1.get_text(strip=True) if h1 else html_file.stem
    title = re.sub(r"\s+", " ", title).strip()

    # Rewrite images → /assets/images
    for img in soup.find_all("img"):
        src = img.get("src")
        if not src:
            continue
        filename = os.path.basename(src.split("?")[0])
        # Best-effort download: copy from export bundle if present
        local = SRC / filename
        if local.exists():
            shutil.copy(local, IMG_DIR / filename)
        img["src"] = f"/assets/images/{filename}"

    # Heuristic: strip Mailchimp footers/tracking
    for sel in [
        ".mcnTextContentFooter",
        "#footer",
        ".footer",
        'center[style*="powered"]',
    ]:
        for n in soup.select(sel):
            n.decompose()

    body_html = str(soup.body or soup)
    body_md = md(body_html)

    # Date
    # Try to discover a date in filename like 2023-06-12-Subject.html
    m = re.search(r"(20\d{2}-\d{2}-\d{2})", html_file.name)
    if m:
        date = datetime.datetime.fromisoformat(m.group(1))
    else:
        date = datetime.datetime.fromtimestamp(html_file.stat().st_mtime)

    # Slug
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
