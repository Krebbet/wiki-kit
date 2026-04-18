"""Tests for tools/capture_pdf.py.

Includes a network smoke test (skipped by default) and offline unit tests
for the pure helper `_first_heading`.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from tools.capture_pdf import _first_heading


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
