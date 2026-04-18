"""Smoke test for tools/capture_url.py — hits example.com."""
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


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
        assert "url: https://example.com" in content
        assert "capture_method: url" in content
        assert "Example Domain" in content
