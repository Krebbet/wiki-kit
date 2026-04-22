"""Tests for tools/ingest_plan.py."""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

import pytest

from tools.ingest_plan import (
    INGEST_SCHEMA_VERSION,
    SummarySchemaError,
    aggregate,
    compute_dispatch_list,
    load_run_state,
    parse_summary,
    save_run_state,
)

FIXTURES = Path(__file__).parent / "fixtures" / "ingest"


def test_schema_version_is_one():
    assert INGEST_SCHEMA_VERSION == 1


def test_parse_summary_well_formed():
    s = parse_summary(FIXTURES / "01-foo.summary.md")
    assert s["frontmatter"]["slug"] == "01-foo"
    assert s["frontmatter"]["schema_version"] == 1
    assert "two-stage training recipe" in s["one_line"]
    assert "Method" in s["takeaway_sections"]
    assert "Results" in s["takeaway_sections"]
    assert s["cross_ref_candidates"] == [
        {"page": "rlhf", "reason": "extends with outcome-based variant"},
        {"page": "sft", "reason": "first stage is standard SFT"},
    ]
    assert s["conflict_flags"] == []
    assert s["proposed_page_shape"]["kind"] == "new"
    assert s["proposed_page_shape"]["title"] == "foo-method"


def test_parse_summary_missing_frontmatter_raises():
    with pytest.raises(SummarySchemaError, match="frontmatter"):
        parse_summary(FIXTURES / "malformed-no-frontmatter.md")


def test_parse_summary_missing_required_sections_raises():
    with pytest.raises(SummarySchemaError, match="required section"):
        parse_summary(FIXTURES / "malformed-missing-sections.md")


def test_parse_summary_captures_conflict_flags():
    s = parse_summary(FIXTURES / "03-baz.summary.md")
    assert len(s["conflict_flags"]) == 1
    flag = s["conflict_flags"][0]
    assert "72.1" in flag["claim"]
    assert flag["contradicts_page"] == "dpo"


def test_aggregate_flags_merge_candidate_when_two_new_pages_share_concepts():
    plan = aggregate([
        FIXTURES / "01-foo.summary.md",
        FIXTURES / "02-bar.summary.md",
        FIXTURES / "03-baz.summary.md",
    ])
    # 02-bar and 03-baz both NEW pages, both name dpo + preference optimization
    assert len(plan.merge_candidates) == 1
    mc = plan.merge_candidates[0]
    assert set(mc.slugs) == {"02-bar", "03-baz"}


def test_aggregate_cross_refs_union_and_strength():
    plan = aggregate([
        FIXTURES / "01-foo.summary.md",
        FIXTURES / "02-bar.summary.md",
        FIXTURES / "03-baz.summary.md",
    ])
    by_page = {x.page: x for x in plan.cross_refs}
    # dpo named by both 02-bar and 03-baz → strong
    assert by_page["dpo"].strong is True
    # rlhf named by 01-foo and 03-baz → strong
    assert by_page["rlhf"].strong is True
    # sft named by 01-foo only → not strong
    assert by_page["sft"].strong is False


def test_aggregate_surfaces_conflicts_verbatim():
    plan = aggregate([FIXTURES / "03-baz.summary.md"])
    assert len(plan.conflicts) == 1
    assert plan.conflicts[0]["contradicts_page"] == "dpo"


def test_aggregate_page_plan_has_one_new_per_non_merged_summary():
    plan = aggregate([FIXTURES / "01-foo.summary.md"])
    assert len(plan.page_plan) == 1
    assert plan.page_plan[0].kind == "new"
    assert plan.page_plan[0].title == "foo-method"
    assert plan.page_plan[0].sources == ["01-foo"]


def test_parse_summary_accepts_quoted_schema_version(tmp_path):
    """A subagent that quotes the int should still be accepted."""
    p = tmp_path / "quoted.summary.md"
    p.write_text(
        '---\n'
        'source: "src.md"\n'
        'slug: "quoted"\n'
        'summarized_on: "2026-04-21"\n'
        'schema_version: "1"\n'
        '---\n\n'
        '# Quoted\n\n## One-line\nq\n\n## Method\nx\n\n'
        '## Cross-ref candidates\n(none)\n\n'
        '## Conflict flags\n(none)\n\n'
        '## Proposed page shape\n- New page: quoted\n',
        encoding="utf-8",
    )
    s = parse_summary(p)
    assert s["frontmatter"]["schema_version"] == 1


def test_parse_summary_accepts_bullet_style_conflict(tmp_path):
    """Bullet-form conflict block (each line `- Xxx:`) should parse."""
    p = tmp_path / "bullet.summary.md"
    p.write_text(
        '---\n'
        'source: "src.md"\n'
        'slug: "bullet"\n'
        'summarized_on: "2026-04-21"\n'
        'schema_version: 1\n'
        '---\n\n'
        '# Bullet\n\n## One-line\nb\n\n## Method\nm\n\n'
        '## Cross-ref candidates\n- [[dpo]] — refines\n\n'
        '## Conflict flags\n'
        '- Claim: Bullet reports 90.0 on X.\n'
        '- Contradicts: [[dpo]] which says 80.0\n'
        '- Basis: Table 1\n\n'
        '## Proposed page shape\n- New page: bullet-method\n',
        encoding="utf-8",
    )
    s = parse_summary(p)
    assert len(s["conflict_flags"]) == 1
    cf = s["conflict_flags"][0]
    assert cf["contradicts_page"] == "dpo"
    assert cf["basis"] == "Table 1"


def _make_source(topic: Path, slug: str, body: str = "x") -> Path:
    src = topic / f"{slug}.md"
    src.write_text(body, encoding="utf-8")
    return src


def _make_summary(topic: Path, slug: str, schema_version: int = 1) -> Path:
    ingest = topic / ".ingest"
    ingest.mkdir(exist_ok=True)
    summary = ingest / f"{slug}.summary.md"
    summary.write_text(
        f"---\nsource: \"{slug}.md\"\nslug: \"{slug}\"\n"
        f"summarized_on: \"2026-04-21\"\nschema_version: {schema_version}\n---\n"
        "# Stub\n\n## One-line\nstub\n\n## Method\nstub\n\n"
        "## Cross-ref candidates\n(none)\n\n## Conflict flags\n(none)\n\n"
        "## Proposed page shape\n- New page: stub\n",
        encoding="utf-8",
    )
    return summary


def test_load_run_state_absent_returns_default(tmp_path):
    state = load_run_state(tmp_path)
    assert state["schema_version"] == 1
    assert state["sources"] == {}
    assert state["started_at"] is not None


def test_save_run_state_writes_atomically(tmp_path):
    (tmp_path / ".ingest").mkdir()
    state = {"schema_version": 1, "sources": {"01-foo": {"status": "ok"}}}
    save_run_state(tmp_path, state)
    loaded = json.loads((tmp_path / ".ingest" / "run.json").read_text())
    assert loaded["sources"]["01-foo"]["status"] == "ok"
    assert "last_updated" in loaded


def test_compute_dispatch_list_no_cache_dispatches_all(tmp_path):
    s1 = _make_source(tmp_path, "01-foo")
    s2 = _make_source(tmp_path, "02-bar")
    to_dispatch, cached = compute_dispatch_list(tmp_path, [s1, s2])
    assert sorted(p.name for p in to_dispatch) == ["01-foo.md", "02-bar.md"]
    assert cached == []


def test_compute_dispatch_list_skips_cached_ok(tmp_path):
    s1 = _make_source(tmp_path, "01-foo")
    s2 = _make_source(tmp_path, "02-bar")
    _make_summary(tmp_path, "01-foo")
    save_run_state(tmp_path, {
        "schema_version": 1,
        "sources": {"01-foo": {"status": "ok", "summary": "01-foo.summary.md"}},
    })
    to_dispatch, cached = compute_dispatch_list(tmp_path, [s1, s2])
    assert [p.name for p in to_dispatch] == ["02-bar.md"]
    assert [p.name for p in cached] == ["01-foo.summary.md"]


def test_compute_dispatch_list_redispatches_failed(tmp_path):
    s1 = _make_source(tmp_path, "01-foo")
    save_run_state(tmp_path, {
        "schema_version": 1,
        "sources": {"01-foo": {"status": "failed", "error": "timeout"}},
    })
    to_dispatch, cached = compute_dispatch_list(tmp_path, [s1])
    assert [p.name for p in to_dispatch] == ["01-foo.md"]
    assert cached == []


def test_compute_dispatch_list_redispatches_stale_mtime(tmp_path, monkeypatch):
    s1 = _make_source(tmp_path, "01-foo")
    summary = _make_summary(tmp_path, "01-foo")
    save_run_state(tmp_path, {
        "schema_version": 1,
        "sources": {"01-foo": {"status": "ok", "summary": "01-foo.summary.md"}},
    })
    # touch source newer than summary
    newer = time.time() + 5
    os.utime(s1, (newer, newer))
    to_dispatch, _ = compute_dispatch_list(tmp_path, [s1])
    assert [p.name for p in to_dispatch] == ["01-foo.md"]


def test_compute_dispatch_list_redispatches_wrong_schema_version(tmp_path):
    s1 = _make_source(tmp_path, "01-foo")
    _make_summary(tmp_path, "01-foo", schema_version=0)
    save_run_state(tmp_path, {
        "schema_version": 1,
        "sources": {"01-foo": {"status": "ok", "summary": "01-foo.summary.md"}},
    })
    to_dispatch, cached = compute_dispatch_list(tmp_path, [s1])
    assert [p.name for p in to_dispatch] == ["01-foo.md"]
    assert cached == []


def test_compute_dispatch_list_force_redispatches_all(tmp_path):
    s1 = _make_source(tmp_path, "01-foo")
    _make_summary(tmp_path, "01-foo")
    save_run_state(tmp_path, {
        "schema_version": 1,
        "sources": {"01-foo": {"status": "ok", "summary": "01-foo.summary.md"}},
    })
    to_dispatch, cached = compute_dispatch_list(tmp_path, [s1], force=True)
    assert [p.name for p in to_dispatch] == ["01-foo.md"]
    assert cached == []
