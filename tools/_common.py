"""Shared helpers for capture tools."""
from __future__ import annotations

import hashlib
import re
from datetime import date
from pathlib import Path
from typing import Any

import httpx


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
    """Download a binary asset to assets_dir, dedupe by content hash, return relative filename or None on failure."""
    assets_dir.mkdir(parents=True, exist_ok=True)
    own_client = client is None
    client = client or httpx.Client(follow_redirects=True, timeout=20.0)
    try:
        r = client.get(url)
        r.raise_for_status()
        data = r.content
        digest = hashlib.sha256(data).hexdigest()[:16]
        ext = _guess_ext(url, r.headers.get("content-type", ""))
        filename = f"{digest}{ext}"
        target = assets_dir / filename
        if not target.exists():
            target.write_bytes(data)
        return filename
    except Exception:
        return None
    finally:
        if own_client:
            client.close()


def _guess_ext(url: str, content_type: str) -> str:
    """Guess file extension from URL path or content-type header."""
    m = re.search(r"\.([a-zA-Z0-9]{2,4})(?:\?|$)", url)
    if m:
        return f".{m.group(1).lower()}"
    if "png" in content_type: return ".png"
    if "jpeg" in content_type or "jpg" in content_type: return ".jpg"
    if "gif" in content_type: return ".gif"
    if "webp" in content_type: return ".webp"
    if "svg" in content_type: return ".svg"
    return ".bin"


def today_iso() -> str:
    return date.today().isoformat()
