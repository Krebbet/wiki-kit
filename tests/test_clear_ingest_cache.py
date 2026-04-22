"""Tests for tools/clear_ingest_cache.py."""
from __future__ import annotations

from pathlib import Path

import pytest

from tools.clear_ingest_cache import clear, main


def test_clear_removes_existing_ingest_dir(tmp_path):
    ingest = tmp_path / ".ingest"
    ingest.mkdir()
    (ingest / "run.json").write_text("{}")
    (ingest / "01-foo.summary.md").write_text("x")
    assert clear(tmp_path) is True
    assert not ingest.exists()


def test_clear_returns_false_when_absent(tmp_path):
    assert clear(tmp_path) is False


def test_clear_refuses_non_ingest_target(tmp_path, monkeypatch):
    # Simulate an attempt to clear a topic_dir whose .ingest path somehow
    # resolves elsewhere — constructively: pass a topic_dir that has a
    # symlinked .ingest pointing at a non-.ingest directory.
    target = tmp_path / "real"
    target.mkdir()
    (target / "important.txt").write_text("do not delete")
    bad_topic = tmp_path / "topic"
    bad_topic.mkdir()
    (bad_topic / ".ingest").symlink_to(target)
    with pytest.raises(ValueError, match="not a .ingest"):
        clear(bad_topic)
    assert (target / "important.txt").exists()


def test_main_exits_zero_on_success(tmp_path):
    (tmp_path / ".ingest").mkdir()
    assert main([str(tmp_path)]) == 0


def test_main_exits_two_on_bad_path(tmp_path):
    missing = tmp_path / "nope"
    assert main([str(missing)]) == 2
