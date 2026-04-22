"""Tests for tools/ingest_plan.py."""
from __future__ import annotations

from pathlib import Path

import pytest

from tools.ingest_plan import (
    INGEST_SCHEMA_VERSION,
    SummarySchemaError,
    aggregate,
    parse_summary,
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
