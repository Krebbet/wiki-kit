"""Capture a URL as markdown with local images. Writes to <out>/NN-<slug>.md."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import httpx
import trafilatura
from markdownify import markdownify as md

from tools._common import (
    download_asset,
    next_numbered_filename,
    slugify,
    today_iso,
    write_frontmatter,
)


MIN_CONTENT_CHARS = 500


def capture(url: str, out_dir: Path, slug: str | None, force_js: bool) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    title, body_md = _extract(url, force_js=force_js)
    effective_slug = slug or slugify(title or url)
    filename = next_numbered_filename(out_dir, effective_slug)
    assets_dir = out_dir / "assets"
    body_md = _rewrite_images(body_md, assets_dir)

    fm = write_frontmatter({
        "url": url,
        "title": title or "(untitled)",
        "captured_on": today_iso(),
        "capture_method": "url",
        "assets_dir": "./assets" if assets_dir.exists() else None,
    })
    out_path = out_dir / filename
    out_path.write_text(fm + body_md)
    return out_path


def _extract(url: str, force_js: bool) -> tuple[str | None, str]:
    """Return (title, markdown body). Falls back to Playwright if trafilatura yields too little."""
    if not force_js:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            extracted = trafilatura.extract(
                downloaded, output_format="markdown", include_images=True, include_links=True
            )
            if extracted and len(extracted) >= MIN_CONTENT_CHARS:
                meta = trafilatura.extract_metadata(downloaded)
                title = meta.title if meta else None
                return title, extracted
    return _extract_with_playwright(url)


def _extract_with_playwright(url: str) -> tuple[str | None, str]:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle", timeout=30_000)
        title = page.title()
        html = page.content()
        browser.close()
    body_html = _main_content_html(html)
    body_md = md(body_html, heading_style="ATX", strip=["script", "style"])
    return title, body_md


def _main_content_html(html: str) -> str:
    for tag in ("<article", "<main", '<div role="main"'):
        m = re.search(rf"{tag}[^>]*>", html)
        if m:
            start = m.start()
            end_tag = tag[1:].split()[0].rstrip(">")
            close_m = re.search(rf"</{end_tag}\s*>", html[start:])
            if close_m:
                return html[start : start + close_m.end()]
    return html


def _rewrite_images(body: str, assets_dir: Path) -> str:
    """Replace markdown image URLs with local asset paths."""
    with httpx.Client(follow_redirects=True, timeout=20.0) as client:
        def _replace(m: re.Match) -> str:
            alt, url = m.group(1), m.group(2)
            if url.startswith("data:") or url.startswith("./"):
                return m.group(0)
            filename = download_asset(url, assets_dir, client=client)
            if filename is None:
                return m.group(0)
            return f"![{alt}](./assets/{filename})"
        return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", _replace, body)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Capture a URL as markdown.")
    p.add_argument("--url", required=True)
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--slug", default=None)
    p.add_argument("--js", action="store_true", help="Force Playwright fallback")
    args = p.parse_args(argv)
    try:
        written = capture(args.url, args.out, args.slug, args.js)
    except Exception as e:
        print(f"capture_url failed: {e}", file=sys.stderr)
        return 1
    print(written)
    return 0


if __name__ == "__main__":
    sys.exit(main())
