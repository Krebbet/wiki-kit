"""Tests for tools/capture_pdf.py.

Includes a network smoke test (skipped by default) and offline unit tests
for the pure helper `_first_heading`.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from tools.capture_pdf import (
    _first_heading,
    _resolve_source,
    _rewrite_image_refs,
    _slug_hint,
    capture,
)


SMALL_PDF_URL = "https://arxiv.org/pdf/1706.03762v7"  # Attention is All You Need, ~2.1MB


@pytest.mark.network
@pytest.mark.slow
def test_capture_pdf_pymupdf():
    with tempfile.TemporaryDirectory() as d:
        result = subprocess.run(
            [sys.executable, "-m", "tools.capture_pdf", "--src", SMALL_PDF_URL,
             "--out", d, "--slug", "attention", "--engine", "pymupdf"],
            capture_output=True, text=True, timeout=120,
        )
        assert result.returncode == 0, result.stderr
        out_path = Path(result.stdout.strip())
        assert out_path.exists()
        content = out_path.read_text()
        assert 'capture_method: "pdf"' in content
        assert 'engine: "pymupdf"' in content


def test_first_heading_returns_first_h1():
    md = "Some intro text\n# Real Title\nbody\n# Another Title\n"
    assert _first_heading(md) == "Real Title"


def test_first_heading_returns_none_when_absent():
    md = "Just a paragraph.\nNo headings here.\n"
    assert _first_heading(md) is None


def test_first_heading_skips_h2():
    md = "## Sub Heading\nbody\n# Top Heading\n"
    assert _first_heading(md) == "Top Heading"


def test_resolve_source_local_existing_pdf(tmp_path):
    pdf = tmp_path / "sample.pdf"
    pdf.write_bytes(b"%PDF-1.4\n%EOF\n")
    resolved_path, source_url, cleanup = _resolve_source(str(pdf))
    assert resolved_path == pdf.resolve()
    assert source_url is None
    assert callable(cleanup)
    cleanup()
    assert pdf.exists()


def test_resolve_source_missing_local_path_raises():
    with pytest.raises(FileNotFoundError):
        _resolve_source("/nonexistent/path/foo.pdf")


def test_capture_with_stubbed_convert_pymupdf(tmp_path, monkeypatch):
    local_pdf = tmp_path / "input.pdf"
    local_pdf.write_bytes(b"%PDF-1.4\n%EOF\n")

    def fake_convert(pdf_path, assets_dir, pages):
        return ("Stub Title", "# Stub Title\n\nbody text")

    monkeypatch.setattr("tools.capture_pdf._convert_pymupdf", fake_convert)
    monkeypatch.setattr("tools.capture_pdf._page_count", lambda p: 1)

    out_path = capture(
        src=str(local_pdf),
        out_dir=tmp_path,
        slug=None,
        engine="pymupdf",
        max_pages=None,
    )
    assert out_path == tmp_path / "01-stub-title.md"
    content = out_path.read_text(encoding="utf-8")
    assert content.startswith("---\n")
    assert 'engine: "pymupdf"' in content
    assert 'capture_method: "pdf"' in content
    assert "body text" in content
    assert "assets_dir" not in content


def test_rewrite_image_refs_prefixes_bare_filenames():
    md = "intro\n![](_page_1.jpeg)\n![alt](pic.png)\nend"
    out = _rewrite_image_refs(md, "./assets/my-paper")
    assert "![](./assets/my-paper/_page_1.jpeg)" in out
    assert "![alt](./assets/my-paper/pic.png)" in out


def test_rewrite_image_refs_skips_urls_and_absolute_paths():
    md = (
        "![](https://example.com/foo.png)\n"
        "![](http://x/y.jpeg)\n"
        "![](/abs/path.png)\n"
    )
    out = _rewrite_image_refs(md, "./assets/p")
    assert out == md  # unchanged


def test_rewrite_image_refs_skips_already_pathed_refs():
    md = "![](assets/p/foo.png)\n![](sub/dir/x.jpeg)\n"
    out = _rewrite_image_refs(md, "./assets/p")
    assert out == md  # contains '/' so left alone


def test_slug_hint_from_url():
    assert _slug_hint("https://arxiv.org/pdf/2504.20571", Path("/tmp/dummy.pdf")) == "2504.20571"
    assert _slug_hint("https://arxiv.org/pdf/2504.20571.pdf", Path("/tmp/dummy.pdf")) == "2504.20571"


def test_slug_hint_from_local_path():
    assert _slug_hint("/tmp/some-paper.pdf", Path("/tmp/some-paper.pdf")) == "some-paper"


def test_capture_namespaces_assets_per_slug(tmp_path, monkeypatch):
    """Two captures into the same out_dir must not share the assets/ namespace."""
    local_pdf = tmp_path / "input.pdf"
    local_pdf.write_bytes(b"%PDF-1.4\n%EOF\n")

    def fake_convert(pdf_path, assets_dir, pages):
        # Simulate marker writing one image and emitting a bare-filename ref.
        assets_dir.mkdir(parents=True, exist_ok=True)
        (assets_dir / "_page_0.jpeg").write_bytes(b"fake-image-bytes")
        return ("Paper Title", "# Paper Title\n\n![](_page_0.jpeg)\n")

    monkeypatch.setattr("tools.capture_pdf._convert_pymupdf", fake_convert)
    monkeypatch.setattr("tools.capture_pdf._page_count", lambda p: 1)

    capture(str(local_pdf), tmp_path, slug="paper-a", engine="pymupdf", max_pages=None)
    capture(str(local_pdf), tmp_path, slug="paper-b", engine="pymupdf", max_pages=None)

    # Each paper has its own asset subdir.
    assert (tmp_path / "assets" / "paper-a" / "_page_0.jpeg").exists()
    assert (tmp_path / "assets" / "paper-b" / "_page_0.jpeg").exists()

    # Markdown refs are rewritten to the per-paper namespace.
    md_a = (tmp_path / "01-paper-a.md").read_text()
    md_b = (tmp_path / "02-paper-b.md").read_text()
    assert "![](./assets/paper-a/_page_0.jpeg)" in md_a
    assert "![](./assets/paper-b/_page_0.jpeg)" in md_b
    # Frontmatter points to the per-paper dir.
    assert 'assets_dir: "./assets/paper-a"' in md_a
    assert 'assets_dir: "./assets/paper-b"' in md_b
