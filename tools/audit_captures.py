"""Audit raw captures for end-to-end fidelity.

Walks a topic directory (or `raw/` itself) and verifies for every captured
markdown file:

1. Every image ref in the markdown resolves to an existing file (relative to
   the markdown's own location).
2. A source PDF exists alongside (in `pdfs/<slug>.pdf`) when the capture is a
   PDF capture.
3. The markdown size is sane relative to the source PDF page count
   (flags suspiciously thin captures — likely OCR failures or partial extracts).
4. No image filename is referenced by more than one markdown (cross-paper
   overwrite indicator).

Usage:
    poetry run python -m tools.audit_captures <topic-dir>
    poetry run python -m tools.audit_captures raw/research/<topic>

Exit code is 0 if no issues are found, 1 otherwise. The report is printed to
stdout in a structured form so it can be piped into a wiki page or grepped.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

# Markdown image refs that target a local file. Skip http(s):// URLs, absolute
# paths, inline data: URIs (e.g. `data:image/svg+xml;base64,...` UI chrome on
# publisher pages like Nature), and fragment/JS/mail schemes.
_IMAGE_REF_RE = re.compile(r"!\[[^\]]*\]\((?!https?://|data:|javascript:|mailto:|#|/)([^)\s]+)\)")

# Markdown filenames written by capture_pdf are prefixed with a sequence number,
# e.g. `04-B-1-maml-finn.md`. Stripping that prefix recovers the slug.
_NUMERIC_PREFIX_RE = re.compile(r"^\d+-")

# A capture is considered "thin" if its markdown has fewer than this many lines
# per source-PDF page. Marker captures of normal papers run ~30-60 lines/page;
# anything below 10 strongly suggests an OCR failure or truncation.
_MIN_LINES_PER_PAGE = 10


def audit(topic_dir: Path) -> tuple[list[str], list[str], list[str], list[str]]:
    """Return (broken_refs, missing_pdfs, thin_captures, image_collisions)."""
    broken_refs: list[str] = []
    missing_pdfs: list[str] = []
    thin_captures: list[str] = []
    image_owners: dict[str, list[str]] = defaultdict(list)

    md_files = sorted(p for p in topic_dir.glob("*.md") if p.is_file())
    pdfs_dir = topic_dir / "pdfs"

    for md in md_files:
        slug = _NUMERIC_PREFIX_RE.sub("", md.stem)
        body = md.read_text(encoding="utf-8")

        for ref in _IMAGE_REF_RE.findall(body):
            target = (md.parent / ref).resolve()
            if not target.exists():
                broken_refs.append(f"{md.name} -> {ref}")
            else:
                # Use the basename to detect cross-MD collisions even when each
                # MD writes under its own assets/<slug>/ — a real collision
                # would be the same path referenced from two MDs.
                key = str(target.relative_to(topic_dir))
                if md.name not in image_owners[key]:
                    image_owners[key].append(md.name)

        if pdfs_dir.exists():
            paired_pdf = pdfs_dir / f"{slug}.pdf"
            if not paired_pdf.exists():
                missing_pdfs.append(f"{md.name} (expected {paired_pdf.relative_to(topic_dir)})")
            else:
                page_count = _safe_page_count(paired_pdf)
                if page_count:
                    line_count = body.count("\n") + 1
                    if line_count < _MIN_LINES_PER_PAGE * page_count:
                        ratio = line_count / page_count
                        thin_captures.append(
                            f"{md.name}: {line_count} lines for {page_count} pages "
                            f"({ratio:.1f} L/p, threshold {_MIN_LINES_PER_PAGE})"
                        )

    image_collisions = [
        f"{img} -> {', '.join(owners)}"
        for img, owners in sorted(image_owners.items())
        if len(owners) > 1
    ]

    return broken_refs, missing_pdfs, thin_captures, image_collisions


def _safe_page_count(pdf_path: Path) -> int | None:
    try:
        import pymupdf
    except ImportError:
        return None
    try:
        with pymupdf.open(str(pdf_path)) as doc:
            return doc.page_count
    except Exception:
        return None


def _print_section(title: str, items: list[str]) -> None:
    print(f"\n## {title} ({len(items)})")
    if not items:
        print("  (clean)")
        return
    for item in items:
        print(f"  - {item}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Audit raw captures for fidelity.")
    p.add_argument("topic_dir", type=Path, help="Directory containing capture MDs (e.g. raw/research/<topic>).")
    args = p.parse_args(argv)

    topic_dir = args.topic_dir.resolve()
    if not topic_dir.is_dir():
        print(f"audit_captures: not a directory: {topic_dir}", file=sys.stderr)
        return 2

    broken, missing_pdfs, thin, collisions = audit(topic_dir)

    print(f"# Capture audit — {topic_dir}")
    _print_section("Broken image refs (file not found)", broken)
    _print_section("Markdowns without a paired source PDF", missing_pdfs)
    _print_section("Suspiciously thin captures (lines << pages)", thin)
    _print_section("Image-path collisions (same image referenced by >1 MD)", collisions)

    issue_count = len(broken) + len(missing_pdfs) + len(thin) + len(collisions)
    print(f"\n# Total issues: {issue_count}")
    return 0 if issue_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
