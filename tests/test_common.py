"""Tests for tools/_common.py — pure-function helpers."""
from pathlib import Path
import tempfile

from tools._common import (
    next_numbered_filename,
    slugify,
    write_frontmatter,
)


def test_slugify_basic():
    assert slugify("Hello World") == "hello-world"


def test_slugify_strips_nonalnum():
    assert slugify("Foo: Bar & Baz!") == "foo-bar-baz"


def test_slugify_collapses_dashes():
    assert slugify("a---b") == "a-b"


def test_next_numbered_filename_empty_dir():
    with tempfile.TemporaryDirectory() as d:
        assert next_numbered_filename(Path(d), "test") == "01-test.md"


def test_next_numbered_filename_increments():
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "01-foo.md").touch()
        (Path(d) / "02-bar.md").touch()
        assert next_numbered_filename(Path(d), "baz") == "03-baz.md"


def test_next_numbered_filename_ignores_non_numbered():
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "README.md").touch()
        (Path(d) / "01-foo.md").touch()
        assert next_numbered_filename(Path(d), "bar") == "02-bar.md"


def test_write_frontmatter_basic():
    fm = write_frontmatter({"url": "https://x.y", "title": "Hi", "captured_on": "2026-04-17"})
    assert fm.startswith("---\n")
    assert "url: https://x.y" in fm
    assert "title: Hi" in fm
    assert fm.endswith("---\n\n")
