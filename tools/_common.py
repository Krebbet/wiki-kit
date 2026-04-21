"""Shared helpers for capture tools."""
from __future__ import annotations

import hashlib
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

import httpx


# Browser-like User-Agent. Many government, academic, and enterprise sites
# (ftc.gov behind Akamai, Wikimedia upload endpoints) return 403 to the default
# httpx User-Agent; a browser UA keeps them unblocked for routine captures.
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) wiki-kit/0.1 Chrome/120.0.0.0 Safari/537.36"
)


_SLUG_CLEAN_RE = re.compile(r"[^a-z0-9]+")
_NUMBERED_FILE_RE = re.compile(r"^(\d+)-.+\.md$")


def slugify(text: str, max_len: int = 60) -> str:
    """Convert text to a URL-safe slug."""
    s = _SLUG_CLEAN_RE.sub("-", text.lower()).strip("-")
    return s[:max_len].rstrip("-")


def next_numbered_filename(out_dir: Path, slug: str) -> str:
    """Return `NN-<slug>.md` with NN one higher than the max existing numbered file."""
    existing = [
        int(m.group(1))
        for f in out_dir.iterdir()
        if f.is_file() and (m := _NUMBERED_FILE_RE.match(f.name))
    ] if out_dir.exists() else []
    nn = (max(existing) + 1) if existing else 1
    return f"{nn:02d}-{slug}.md"


def write_frontmatter(fields: dict[str, Any]) -> str:
    """Render a YAML frontmatter block (trailing blank line included).

    String values are double-quoted with `"` and `\\` escaped so that values
    containing `:` or `"` produce valid YAML. None values are skipped.
    Non-string values pass through unmodified.
    """
    lines = ["---"]
    for k, v in fields.items():
        if v is None:
            continue
        if isinstance(v, str):
            escaped = v.replace("\\", "\\\\").replace('"', '\\"')
            lines.append(f'{k}: "{escaped}"')
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines) + "\n"


def download_asset(url: str, assets_dir: Path, *, client: httpx.Client | None = None) -> str | None:
    """Download a binary asset to assets_dir, dedupe by content hash, return relative filename or None on failure.

    Defers mkdir until after a successful fetch so all-failed captures leave no empty assets/ dir.
    """
    own_client = client is None
    client = client or httpx.Client(
        follow_redirects=True, timeout=20.0, headers={"User-Agent": USER_AGENT}
    )
    try:
        r = client.get(url)
        r.raise_for_status()
        data = r.content
        digest = hashlib.sha256(data).hexdigest()[:16]
        ext = _guess_ext(url, r.headers.get("content-type", ""))
        filename = f"{digest}{ext}"
        assets_dir.mkdir(parents=True, exist_ok=True)
        target = assets_dir / filename
        if not target.exists():
            target.write_bytes(data)
        return filename
    except Exception as e:
        print(f"download_asset failed for {url}: {e}", file=sys.stderr)
        return None
    finally:
        if own_client:
            client.close()


_CONTENT_TYPE_EXTS: list[tuple[str, str]] = [
    ("png", ".png"),
    ("jpeg", ".jpg"),
    ("jpg", ".jpg"),
    ("gif", ".gif"),
    ("webp", ".webp"),
    ("svg", ".svg"),
]


def _guess_ext(url: str, content_type: str) -> str:
    """Guess file extension from URL path or content-type header."""
    m = re.search(r"\.([a-zA-Z0-9]{2,4})(?:\?|$)", url)
    if m:
        return f".{m.group(1).lower()}"
    for token, ext in _CONTENT_TYPE_EXTS:
        if token in content_type:
            return ext
    return ".bin"


def today_iso() -> str:
    return date.today().isoformat()
