"""Tests for tools/capture_url.py."""
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import httpx
import pytest

from tools.capture_url import _rewrite_images


@pytest.mark.network
def test_capture_url_smoke():
    with tempfile.TemporaryDirectory() as d:
        result = subprocess.run(
            [sys.executable, "-m", "tools.capture_url", "--url", "https://example.com",
             "--out", d, "--slug", "example"],
            capture_output=True, text=True, timeout=60,
        )
        assert result.returncode == 0, result.stderr
        out_path = Path(result.stdout.strip())
        assert out_path.exists()
        content = out_path.read_text()
        assert content.startswith("---\n")
        assert 'url: "https://example.com"' in content
        assert 'capture_method: "url"' in content
        assert "Example Domain" in content


def _fake_png_client() -> MagicMock:
    client = MagicMock(spec=httpx.Client)
    response = MagicMock()
    response.content = b"png-content"
    response.headers = {"content-type": "image/png"}
    response.raise_for_status = MagicMock()
    client.get.return_value = response
    return client


def test_rewrite_images_resolves_protocol_relative_url(monkeypatch, tmp_path):
    """Protocol-relative image URLs (//host/path) must resolve against the page URL."""
    called_urls: list[str] = []

    def fake_download(url, assets_dir, *, client=None):
        called_urls.append(url)
        return "abc123.png"

    monkeypatch.setattr("tools.capture_url.download_asset", fake_download)
    # Stub out httpx.Client entirely — _rewrite_images opens one even when not used.
    monkeypatch.setattr("tools.capture_url.httpx.Client", lambda **kwargs: MagicMock(
        __enter__=lambda s: s, __exit__=lambda *a: False
    ))

    body = "![pic](//upload.wikimedia.org/foo.jpg)\n"
    out = _rewrite_images(body, tmp_path / "assets", "https://en.wikipedia.org/wiki/X")
    assert called_urls == ["https://upload.wikimedia.org/foo.jpg"]
    assert "./assets/abc123.png" in out


def test_rewrite_images_resolves_root_relative_url(monkeypatch, tmp_path):
    """Root-relative image URLs (/path) must resolve against the page URL."""
    called_urls: list[str] = []

    def fake_download(url, assets_dir, *, client=None):
        called_urls.append(url)
        return "xyz.png"

    monkeypatch.setattr("tools.capture_url.download_asset", fake_download)
    monkeypatch.setattr("tools.capture_url.httpx.Client", lambda **kwargs: MagicMock(
        __enter__=lambda s: s, __exit__=lambda *a: False
    ))

    body = "![](/static/hero.png)\n"
    _rewrite_images(body, tmp_path / "assets", "https://blog.example.com/post/42")
    assert called_urls == ["https://blog.example.com/static/hero.png"]


def test_rewrite_images_preserves_absolute_url(monkeypatch, tmp_path):
    """Already-absolute URLs pass through urljoin unchanged."""
    called_urls: list[str] = []

    def fake_download(url, assets_dir, *, client=None):
        called_urls.append(url)
        return "a.png"

    monkeypatch.setattr("tools.capture_url.download_asset", fake_download)
    monkeypatch.setattr("tools.capture_url.httpx.Client", lambda **kwargs: MagicMock(
        __enter__=lambda s: s, __exit__=lambda *a: False
    ))

    body = "![](https://other.example.com/i.png)\n"
    _rewrite_images(body, tmp_path / "assets", "https://page.example.org/x")
    assert called_urls == ["https://other.example.com/i.png"]


def test_rewrite_images_skips_data_and_relative_refs(monkeypatch, tmp_path):
    """data: URIs and already-localised `./` refs are left alone."""
    download_mock = MagicMock()
    monkeypatch.setattr("tools.capture_url.download_asset", download_mock)
    monkeypatch.setattr("tools.capture_url.httpx.Client", lambda **kwargs: MagicMock(
        __enter__=lambda s: s, __exit__=lambda *a: False
    ))

    body = (
        "![](data:image/png;base64,AAA)\n"
        "![](./assets/local.png)\n"
    )
    out = _rewrite_images(body, tmp_path / "assets", "https://page.example.org/x")
    assert out == body  # unchanged
    download_mock.assert_not_called()
