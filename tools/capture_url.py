"""Capture a URL as markdown with local images. Writes to <out>/NN-<slug>.md."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

import httpx
import trafilatura
from markdownify import markdownify as md

from tools._common import (
    USER_AGENT,
    download_asset,
    next_numbered_filename,
    slugify,
    today_iso,
    write_frontmatter,
)


MIN_CONTENT_CHARS = 500

# Heuristic — if the extracted body is short AND contains any of these
# signatures, treat as a bot-wall / block page rather than a successful
# capture. Silent-success on tiny "Access Denied" pages was the easiest
# failure mode to miss until you read the file by hand.
_BOT_WALL_BODY_MAX = 3000
_BOT_WALL_SIGNATURES = (
    "access denied",
    "cloudflare_error",
    "edgesuite.net",
    "there was a problem providing the content you requested",
    "please enable cookies",
    "unusual traffic from your computer",
    "you don't have permission to access",
    "request blocked",
    "attention required!",
)


def capture(url: str, out_dir: Path, slug: str | None, force_js: bool) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    title, body_md = _extract(url, force_js=force_js)
    if _looks_like_bot_wall(title, body_md):
        raise RuntimeError(
            f"capture appears to be a bot-wall / block page (title={title!r}, "
            f"body={len(body_md)} chars). Try --js, a direct PDF URL, or a "
            f"manual PDF drop into the output directory."
        )
    effective_slug = slug or slugify(title or url)
    filename = next_numbered_filename(out_dir, effective_slug)
    assets_dir = out_dir / "assets"
    body_md = _rewrite_images(body_md, assets_dir, source_url=url)

    fm = write_frontmatter({
        "url": url,
        "title": title or "(untitled)",
        "captured_on": today_iso(),
        "capture_method": "url",
        "assets_dir": "./assets" if assets_dir.exists() and any(assets_dir.iterdir()) else None,
    })
    out_path = out_dir / filename
    out_path.write_text(fm + body_md, encoding="utf-8")
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
    title = title or None
    return title, body_md


def _main_content_html(html: str) -> str:
    """Extract the outermost <article> or <main> element. Falls back to full HTML."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    for tag_name in ("article", "main"):
        el = soup.find(tag_name)
        if el:
            return str(el)
    return html


def _rewrite_images(body: str, assets_dir: Path, *, source_url: str) -> str:
    """Replace markdown image URLs with local asset paths.

    Normalises protocol-relative (`//host/path`) and plain-relative
    (`fig01.png`, `img/logo.png`) asset URLs against `source_url` before
    fetching — many publisher pages (Nature, arXiv HTML renderings) use
    those forms and would otherwise fail at the httpx layer with "Request
    URL is missing an http/https protocol".
    """
    with httpx.Client(
        follow_redirects=True, timeout=20.0, headers={"User-Agent": USER_AGENT}
    ) as client:
        def _replace(m: re.Match) -> str:
            alt, url = m.group(1), m.group(2)
            if url.startswith("data:") or url.startswith("./"):
                return m.group(0)
            fetchable = _normalize_asset_url(source_url, url)
            if fetchable is None:
                return m.group(0)
            filename = download_asset(fetchable, assets_dir, client=client)
            if filename is None:
                return m.group(0)
            return f"![{alt}](./assets/{filename})"
        return re.sub(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)', _replace, body)


def _looks_like_bot_wall(title: str | None, body: str) -> bool:
    """Return True if the captured content looks like a bot-wall / block page.

    Short bodies are treated as strong evidence; long bodies that happen to
    contain a signature string in a legitimate context (e.g. a paper
    discussing Cloudflare) are left alone.
    """
    if len(body) > _BOT_WALL_BODY_MAX:
        return False
    haystack = f"{title or ''}\n{body}".lower()
    return any(sig in haystack for sig in _BOT_WALL_SIGNATURES)


def _normalize_asset_url(source_url: str, asset_url: str) -> str | None:
    """Return a fetchable absolute URL for an asset found in source_url.

    Handles three cases:
    - Already absolute (`http://` / `https://`) — returned unchanged.
    - Protocol-relative (`//host/path`) — prefixed with `https:`.
    - Relative (`fig01.png`, `img/logo.png`, `../x.png`) — joined against
      `source_url`, appending a trailing `/` to the base when the last
      segment looks like a page rather than a file (no extension), so that
      arXiv HTML URLs like `https://arxiv.org/html/2509.21556v1` resolve
      figures under that article and not the `/html/` parent.

    Returns None if the URL is too malformed to normalise.
    """
    if not asset_url:
        return None
    if asset_url.startswith("http://") or asset_url.startswith("https://"):
        return asset_url
    if asset_url.startswith("//"):
        return "https:" + asset_url
    base = source_url
    if not base.endswith("/"):
        parsed = urlparse(base)
        last_segment = parsed.path.rsplit("/", 1)[-1]
        # Only treat the last segment as a file (no trailing slash) if it
        # ends in a known page extension. arXiv article IDs like
        # "2509.21556v1" and journal DOIs like "s41538-025-00441-8" contain
        # dots but are not files — they are article-directory pages whose
        # figures live *under* that path.
        if not _looks_like_page_file(last_segment):
            base = base + "/"
    try:
        return urljoin(base, asset_url)
    except ValueError:
        return None


_PAGE_EXTENSIONS = (".html", ".htm", ".php", ".aspx", ".jsp", ".pdf", ".xml")


def _looks_like_page_file(segment: str) -> bool:
    return segment.lower().endswith(_PAGE_EXTENSIONS)


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
