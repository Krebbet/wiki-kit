"""Tests for tools/fetch_transcript.py.

Includes a network smoke test (skipped by default) and offline unit tests
for the pure helper `_vtt_to_markdown`.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from tools.fetch_transcript import _vtt_to_markdown


# "Me at the zoo" — first YouTube video, has auto-captions
VIDEO_URL = "https://www.youtube.com/watch?v=jNQXAC9IVRw"


@pytest.mark.network
def test_fetch_transcript_smoke():
    with tempfile.TemporaryDirectory() as d:
        result = subprocess.run(
            [sys.executable, "-m", "tools.fetch_transcript", "--url", VIDEO_URL,
             "--out", d, "--slug", "zoo"],
            capture_output=True, text=True, timeout=60,
        )
        assert result.returncode == 0, result.stderr
        out_path = Path(result.stdout.strip())
        assert out_path.exists()
        content = out_path.read_text()
        assert 'capture_method: "youtube"' in content
        assert "channel:" in content


def _write_vtt(tmp_path: Path, body: str) -> Path:
    p = tmp_path / "subs.vtt"
    p.write_text(body, encoding="utf-8")
    return p


def test_vtt_to_markdown_basic(tmp_path):
    vtt = (
        "WEBVTT\n"
        "\n"
        "00:00:00.000 --> 00:00:05.000\n"
        "Hello world\n"
        "\n"
        "00:00:30.000 --> 00:00:35.000\n"
        "Second cue\n"
        "\n"
        "00:01:00.000 --> 00:01:05.000\n"
        "Third cue\n"
    )
    out = _vtt_to_markdown(_write_vtt(tmp_path, vtt), 30)
    assert "**[00:00:00]**" in out
    assert "**[00:00:30]**" in out
    assert "**[00:01:00]**" in out
    assert "Hello world" in out
    assert "Second cue" in out
    assert "Third cue" in out
    assert "<" not in out


def test_vtt_to_markdown_skips_html_tags(tmp_path):
    vtt = (
        "WEBVTT\n"
        "\n"
        "00:00:00.000 --> 00:00:05.000\n"
        "this is <c>highlighted</c> text\n"
    )
    out = _vtt_to_markdown(_write_vtt(tmp_path, vtt), 30)
    assert "highlighted" in out
    assert "<c>" not in out
    assert "</c>" not in out
    assert "<" not in out


def test_vtt_to_markdown_groups_under_threshold(tmp_path):
    vtt = (
        "WEBVTT\n"
        "\n"
        "00:00:00.000 --> 00:00:05.000\n"
        "first line\n"
        "\n"
        "00:00:10.000 --> 00:00:15.000\n"
        "second line\n"
        "\n"
        "00:00:20.000 --> 00:00:25.000\n"
        "third line\n"
    )
    out = _vtt_to_markdown(_write_vtt(tmp_path, vtt), 30)
    # Only the first cue gets a timestamp prefix
    assert out.count("**[") == 1
    assert "**[00:00:00]**" in out
    assert "**[00:00:10]**" not in out
    assert "**[00:00:20]**" not in out
    assert "first line" in out
    assert "second line" in out
    assert "third line" in out


def test_vtt_to_markdown_skips_empty_cues(tmp_path):
    vtt = (
        "WEBVTT\n"
        "\n"
        "00:00:00.000 --> 00:00:05.000\n"
        "\n"
        "00:00:30.000 --> 00:00:35.000\n"
        "real text\n"
    )
    out = _vtt_to_markdown(_write_vtt(tmp_path, vtt), 30)
    # Empty cue at 0:00 should be skipped — no timestamp emitted for it
    assert "**[00:00:00]**" not in out
    assert "**[00:00:30]**" in out
    assert "real text" in out


def test_vtt_to_markdown_handles_webvtt_header(tmp_path):
    vtt = (
        "WEBVTT\n"
        "Kind: captions\n"
        "Language: en\n"
        "\n"
        "00:00:00.000 --> 00:00:05.000\n"
        "first cue text\n"
    )
    out = _vtt_to_markdown(_write_vtt(tmp_path, vtt), 30)
    assert "**[00:00:00]**" in out
    assert "first cue text" in out
    assert "WEBVTT" not in out
    assert "Kind:" not in out
    assert "Language:" not in out
