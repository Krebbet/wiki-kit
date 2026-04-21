"""Tests for tools/_common.py — pure-function helpers."""
from pathlib import Path
import tempfile
from unittest.mock import MagicMock

import httpx
import pytest

from tools._common import (
    USER_AGENT,
    _guess_ext,
    download_asset,
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


def test_slugify_max_len_truncates_no_trailing_dash():
    # 'a' * 10 + '-' + 'b' * 60 → after truncation to max_len=10, no trailing dash.
    # Construct input where truncation would land on a dash, then ensure it's stripped.
    text = "aaaaaaaaa b c d e f g h"  # spaces become dashes
    result = slugify(text, max_len=10)
    assert len(result) <= 10
    assert not result.endswith("-")


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
    assert 'url: "https://x.y"' in fm
    assert 'title: "Hi"' in fm
    assert fm.endswith("---\n\n")


def test_write_frontmatter_skips_none():
    fm = write_frontmatter({"title": "Hi", "assets_dir": None})
    assert 'title: "Hi"' in fm
    assert "assets_dir" not in fm


def test_write_frontmatter_yaml_escapes_quotes_and_colons():
    fm = write_frontmatter({"title": 'He said "hi": yes'})
    assert 'title: "He said \\"hi\\": yes"' in fm


def test_write_frontmatter_yaml_escapes_backslashes():
    fm = write_frontmatter({"title": "back\\slash"})
    assert 'title: "back\\\\slash"' in fm


def _make_mock_client(content: bytes, content_type: str = "image/png") -> MagicMock:
    client = MagicMock(spec=httpx.Client)
    response = MagicMock()
    response.content = content
    response.headers = {"content-type": content_type}
    response.raise_for_status = MagicMock()
    client.get.return_value = response
    return client


def test_download_asset_happy_path_writes_file():
    with tempfile.TemporaryDirectory() as d:
        assets_dir = Path(d) / "assets"
        client = _make_mock_client(b"png-content", "image/png")
        result = download_asset("https://example.com/foo.png", assets_dir, client=client)
        assert result is not None
        assert result.endswith(".png")
        target = assets_dir / result
        assert target.exists()
        assert target.read_bytes() == b"png-content"
        client.get.assert_called_once_with("https://example.com/foo.png")


def test_download_asset_dedupes_same_content():
    with tempfile.TemporaryDirectory() as d:
        assets_dir = Path(d) / "assets"
        client = _make_mock_client(b"image-bytes-here", "image/png")
        f1 = download_asset("https://example.com/a.png", assets_dir, client=client)
        f2 = download_asset("https://example.com/b.png", assets_dir, client=client)
        assert f1 is not None
        assert f1 == f2  # same hash → same filename
        files = list(assets_dir.iterdir())
        assert len(files) == 1
        assert files[0].read_bytes() == b"image-bytes-here"
        # Both calls hit the network (dedupe is content-hash based, not URL based).
        # The dedupe property under test is "no second write," which we verify by
        # asserting only one file exists in the assets dir.
        assert client.get.call_count == 2
        target = assets_dir / f1
        assert target.exists()


def test_download_asset_returns_none_on_http_failure():
    with tempfile.TemporaryDirectory() as d:
        assets_dir = Path(d) / "assets"
        client = MagicMock(spec=httpx.Client)
        response = MagicMock()
        response.raise_for_status = MagicMock(
            side_effect=httpx.HTTPStatusError("404", request=MagicMock(), response=MagicMock())
        )
        client.get.return_value = response
        result = download_asset("https://example.com/missing.png", assets_dir, client=client)
        assert result is None
        # mkdir is deferred until after successful fetch, so failures leave no dir.
        assert not assets_dir.exists()


def test_guess_ext_from_url_extension():
    assert _guess_ext("https://example.com/foo.png", "") == ".png"
    assert _guess_ext("https://example.com/foo.PNG?v=1", "") == ".png"


def test_guess_ext_from_content_type_png():
    assert _guess_ext("https://example.com/image", "image/png") == ".png"


def test_guess_ext_from_content_type_jpeg():
    assert _guess_ext("https://example.com/image", "image/jpeg") == ".jpg"


def test_guess_ext_from_content_type_jpg():
    assert _guess_ext("https://example.com/image", "image/jpg") == ".jpg"


def test_guess_ext_from_content_type_gif():
    assert _guess_ext("https://example.com/image", "image/gif") == ".gif"


def test_guess_ext_from_content_type_webp():
    assert _guess_ext("https://example.com/image", "image/webp") == ".webp"


def test_guess_ext_from_content_type_svg():
    assert _guess_ext("https://example.com/image", "image/svg+xml") == ".svg"


def test_guess_ext_unknown_returns_bin():
    assert _guess_ext("https://example.com/blob", "application/octet-stream") == ".bin"


def test_user_agent_is_browser_like():
    """The UA must look like a browser to avoid 403 on Akamai-fronted sources."""
    assert "Mozilla/5.0" in USER_AGENT
    assert "AppleWebKit" in USER_AGENT


def test_download_asset_own_client_sends_user_agent(monkeypatch):
    """When download_asset creates its own httpx.Client, it must pass the UA header."""
    captured_kwargs: dict = {}

    class FakeClient:
        def __init__(self, **kwargs):
            captured_kwargs.update(kwargs)
        def __enter__(self):
            return self
        def __exit__(self, *a):
            return False
        def get(self, url):
            response = MagicMock()
            response.content = b"data"
            response.headers = {"content-type": "image/png"}
            response.raise_for_status = MagicMock()
            return response
        def close(self):
            pass

    monkeypatch.setattr("tools._common.httpx.Client", FakeClient)
    with tempfile.TemporaryDirectory() as d:
        download_asset("https://example.com/foo.png", Path(d) / "assets")
    assert captured_kwargs.get("headers", {}).get("User-Agent") == USER_AGENT
