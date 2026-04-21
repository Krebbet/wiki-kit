"""Tests for tools/audit_captures.py."""
from __future__ import annotations

from pathlib import Path

import pytest

from tools.audit_captures import audit


def _write_md(path: Path, body: str) -> None:
    path.write_text(body, encoding="utf-8")


def _write_pdf(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"%PDF-1.4\n%EOF\n")


def test_audit_clean_dir_returns_no_issues(tmp_path):
    md = tmp_path / "01-foo.md"
    img_dir = tmp_path / "assets" / "foo"
    img_dir.mkdir(parents=True)
    (img_dir / "_page_0.jpeg").write_bytes(b"img")
    _write_md(md, "# t\n![](./assets/foo/_page_0.jpeg)\n" + "x\n" * 50)
    _write_pdf(tmp_path / "pdfs" / "foo.pdf")

    broken, missing_pdfs, thin, collisions = audit(tmp_path)
    assert broken == []
    assert missing_pdfs == []
    assert thin == []
    assert collisions == []


def test_audit_flags_broken_image_ref(tmp_path):
    _write_md(tmp_path / "01-foo.md", "# t\n![](./assets/foo/missing.jpeg)\n" + "x\n" * 50)
    _write_pdf(tmp_path / "pdfs" / "foo.pdf")

    broken, *_ = audit(tmp_path)
    assert any("missing.jpeg" in b for b in broken)


def test_audit_flags_missing_paired_pdf(tmp_path):
    _write_md(tmp_path / "01-foo.md", "# t\n" + "x\n" * 50)
    # No pdfs/ dir -> missing_pdfs should still be empty (we only flag if pdfs/ exists)
    _, missing_no_dir, *_ = audit(tmp_path)
    assert missing_no_dir == []

    # With pdfs/ dir present but the matching PDF absent, we flag it.
    (tmp_path / "pdfs").mkdir()
    _, missing_with_dir, *_ = audit(tmp_path)
    assert any("01-foo.md" in m for m in missing_with_dir)


def test_audit_flags_thin_capture(tmp_path):
    _write_md(tmp_path / "01-foo.md", "# t\nshort\n")  # 2 lines for many pages
    pdf = tmp_path / "pdfs" / "foo.pdf"
    _write_pdf(pdf)
    pymupdf = pytest.importorskip("pymupdf")
    # Build a real multi-page PDF so the page-count check has something to read.
    doc = pymupdf.open()
    for _ in range(20):
        doc.new_page()
    pdf.write_bytes(doc.tobytes())
    doc.close()

    *_, thin, _ = audit(tmp_path)
    assert any("01-foo.md" in t for t in thin)


def test_audit_flags_image_collision_across_mds(tmp_path):
    img_dir = tmp_path / "assets"
    img_dir.mkdir()
    (img_dir / "shared.jpeg").write_bytes(b"img")
    _write_md(tmp_path / "01-a.md", "# a\n![](./assets/shared.jpeg)\n" + "x\n" * 50)
    _write_md(tmp_path / "02-b.md", "# b\n![](./assets/shared.jpeg)\n" + "x\n" * 50)
    _write_pdf(tmp_path / "pdfs" / "a.pdf")
    _write_pdf(tmp_path / "pdfs" / "b.pdf")

    *_, collisions = audit(tmp_path)
    assert any("shared.jpeg" in c and "01-a.md" in c and "02-b.md" in c for c in collisions)


def test_audit_skips_url_image_refs(tmp_path):
    _write_md(tmp_path / "01-foo.md", "# t\n![](https://example.com/x.png)\n" + "x\n" * 50)
    _write_pdf(tmp_path / "pdfs" / "foo.pdf")

    broken, *_ = audit(tmp_path)
    assert broken == []
