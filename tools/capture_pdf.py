"""Capture a PDF (URL or local path) as markdown."""
from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Callable

import httpx

from tools._common import (
    next_numbered_filename,
    slugify,
    today_iso,
    write_frontmatter,
)


def capture(src: str, out_dir: Path, slug: str | None, engine: str, max_pages: int | None) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path, source_url, cleanup = _resolve_source(src)
    # Per-paper asset namespace prevents cross-capture image collisions in shared
    # output dirs. Use the supplied slug if available; otherwise fall back to a
    # source-derived hint (refined to the title-derived slug after conversion).
    pre_slug = slug or slugify(_slug_hint(src, pdf_path))
    try:
        page_count = _page_count(pdf_path)
        if page_count > 200:
            print(f"capture_pdf: warning — PDF has {page_count} pages", file=sys.stderr)
        pages = list(range(min(page_count, max_pages))) if max_pages else None
        assets_dir = out_dir / "assets" / pre_slug
        if engine == "marker":
            title, body_md = _convert_marker(pdf_path, assets_dir, pages)
        elif engine == "pymupdf":
            title, body_md = _convert_pymupdf(pdf_path, assets_dir, pages)
        else:
            raise ValueError(f"unknown engine: {engine}")
    finally:
        cleanup()

    effective_slug = slug or slugify(title or source_url or "pdf")
    filename = next_numbered_filename(out_dir, effective_slug)
    assets_rel = f"./assets/{pre_slug}"
    has_assets = assets_dir.exists() and next(assets_dir.iterdir(), None) is not None
    if has_assets:
        body_md = _rewrite_image_refs(body_md, assets_rel)
    fm = write_frontmatter({
        "url": source_url or f"file://{Path(src).resolve()}",
        "title": title or "(untitled)",
        "captured_on": today_iso(),
        "capture_method": "pdf",
        "engine": engine,
        "assets_dir": assets_rel if has_assets else None,
    })
    out_path = out_dir / filename
    out_path.write_text(fm + body_md, encoding="utf-8")
    return out_path


def _slug_hint(src: str, pdf_path: Path) -> str:
    """Derive a short identifier from the source for pre-conversion asset namespacing."""
    if src.startswith(("http://", "https://")):
        tail = src.rstrip("/").rsplit("/", 1)[-1]
        return tail.removesuffix(".pdf") or "pdf"
    return pdf_path.stem


_IMAGE_REF_RE = re.compile(r"(!\[[^\]]*\]\()(?!https?://|/)([^)\s]+)(\))")


def _rewrite_image_refs(markdown: str, assets_rel: str) -> str:
    """Prefix bare-filename image refs with the per-paper asset directory.

    Marker emits `![](foo.jpeg)` with the image alongside the markdown; we move
    images into a slug-namespaced subdir, so the refs need to be rewritten.
    Refs already containing a path separator or a URL are left alone.
    """
    prefix = assets_rel.rstrip("/")

    def repl(m: re.Match[str]) -> str:
        target = m.group(2)
        if "/" in target:
            return m.group(0)
        return f"{m.group(1)}{prefix}/{target}{m.group(3)}"

    return _IMAGE_REF_RE.sub(repl, markdown)


def _resolve_source(src: str) -> tuple[Path, str | None, Callable[[], None]]:
    """Resolve src to (pdf_path, source_url, cleanup_fn).

    For HTTP(S) URLs, downloads to a tempdir and returns a cleanup that removes it.
    For local paths, returns the path with a no-op cleanup.
    """
    if src.startswith(("http://", "https://")):
        tmp_dir = Path(tempfile.mkdtemp(prefix="wk-pdf-"))
        tmp_path = tmp_dir / "source.pdf"
        try:
            with httpx.Client(follow_redirects=True, timeout=60.0) as client:
                r = client.get(src)
                r.raise_for_status()
                tmp_path.write_bytes(r.content)
        except Exception:
            shutil.rmtree(tmp_dir, ignore_errors=True)
            raise
        return tmp_path, src, lambda: shutil.rmtree(tmp_dir, ignore_errors=True)
    path = Path(src).resolve()
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")
    return path, None, lambda: None


def _page_count(pdf_path: Path) -> int:
    import pymupdf
    with pymupdf.open(str(pdf_path)) as doc:
        return doc.page_count


def _convert_marker(pdf_path: Path, assets_dir: Path, pages: list[int] | None) -> tuple[str | None, str]:
    # NOTE: marker-pdf API has changed across versions. If the imports below fail,
    # consult the installed version's docs for the current "PDF -> markdown + images" recipe.
    from marker.converters.pdf import PdfConverter
    from marker.models import create_model_dict
    from marker.output import text_from_rendered

    config = {"page_range": ",".join(str(p) for p in pages)} if pages else {}
    converter = PdfConverter(artifact_dict=create_model_dict(), config=config)
    rendered = converter(str(pdf_path))
    text, _, images = text_from_rendered(rendered)
    _save_images(images, assets_dir)
    title = _first_heading(text)
    return title, text


def _convert_pymupdf(pdf_path: Path, assets_dir: Path, pages: list[int] | None) -> tuple[str | None, str]:
    import pymupdf4llm
    assets_dir.mkdir(parents=True, exist_ok=True)
    kwargs: dict = {"write_images": True, "image_path": str(assets_dir)}
    if pages is not None:
        kwargs["pages"] = pages
    text = pymupdf4llm.to_markdown(str(pdf_path), **kwargs)
    title = _first_heading(text)
    return title, text


def _save_images(images: dict, assets_dir: Path) -> None:
    if not images:
        return
    assets_dir.mkdir(parents=True, exist_ok=True)
    for name, img in images.items():
        path = assets_dir / name
        if not path.suffix:
            path = path.with_suffix(".png")
        if hasattr(img, "save"):
            img.save(path)
        else:
            path.write_bytes(img)


def _first_heading(markdown: str) -> str | None:
    """Return the text of the first `# heading` line, or None if none found."""
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Capture a PDF as markdown.")
    p.add_argument("--src", required=True, help="URL or local path")
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--slug", default=None)
    p.add_argument("--engine", choices=["marker", "pymupdf"], default="marker")
    p.add_argument("--max-pages", type=int, default=None)
    args = p.parse_args(argv)
    try:
        written = capture(args.src, args.out, args.slug, args.engine, args.max_pages)
    except Exception as e:
        print(f"capture_pdf failed: {e}", file=sys.stderr)
        return 1
    print(written)
    return 0


if __name__ == "__main__":
    sys.exit(main())
