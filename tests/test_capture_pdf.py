"""Tests for tools/capture_pdf.py.

Includes a network smoke test (skipped by default) and offline unit tests
for the pure helper `_first_heading`.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from tools.capture_pdf import _first_heading, _resolve_source, capture


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
