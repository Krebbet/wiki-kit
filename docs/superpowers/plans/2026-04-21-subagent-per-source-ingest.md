# Subagent-per-Source `/ingest` — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers-extended-cc:subagent-driven-development (recommended) or superpowers-extended-cc:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn `/ingest <path>` into an orchestrator that dispatches one subagent per raw source, aggregates structured summaries, and writes wiki pages from the orchestrator after a single human review gate — keeping raw source bodies out of the main context.

**Architecture:** Two complementary halves. (1) A pure-Python support module `tools/ingest_plan.py` that parses subagent-produced summary files, computes the dispatch list against `.ingest/run.json`, and aggregates summaries into a review packet — all unit-testable. (2) Updated prose in `.claude/commands/ingest.md` that drives the orchestrator flow: dispatch subagents in parallel, wait for all, call the support module for aggregation, present the review packet, then write wiki pages. Kit-scope; DOMAIN-SLOT boundary preserved.

**Tech Stack:** Python 3.10+, pytest, Poetry. No new dependencies. Reuses `tools/_common.py` helpers (`write_frontmatter`, `today_iso`).

**Spec:** `docs/superpowers/specs/2026-04-21-subagent-per-source-ingest-design.md`

---

## File Structure

**New files:**
- `tools/ingest_plan.py` — pure-function module with five public entry points:
  - `parse_summary(path)` → dict (frontmatter + named sections)
  - `aggregate(summary_paths)` → `IngestPlan` (page plan, cross-refs, conflicts, low-value, merge candidates)
  - `load_run_state(topic_dir)` → dict from `.ingest/run.json` (empty if absent)
  - `save_run_state(topic_dir, state)` — atomic write
  - `compute_dispatch_list(topic_dir, source_paths)` → `(to_dispatch, cached)` tuple respecting cache + mtime + schema_version
- `tools/clear_ingest_cache.py` — CLI to `rm -rf <topic>/.ingest/` with safety check
- `tests/test_ingest_plan.py`
- `tests/test_clear_ingest_cache.py`
- `tests/fixtures/ingest/` — golden summary fixtures for `aggregate()` and `parse_summary()`
- `tests/fixtures/ingest-smoke/` — 2-source end-to-end fixture with a pre-known conflict

**Modified files:**
- `.claude/commands/ingest.md` — complete rewrite; DOMAIN-SLOT for takeaway-prompts preserved
- `.claude/commands/research.md` — wording update in step 6 only
- `wiki/CLAUDE.md` — one note under "Raw Sources" + one manual QA pointer

**Constants/schema:**
- `INGEST_SCHEMA_VERSION = 1` — exported from `tools/ingest_plan.py`; referenced by orchestrator prose
- `.ingest/run.json` schema per spec (sources map, `review_completed_at`, `pages_written`)
- Summary frontmatter per spec (`source`, `slug`, `summarized_on`, `schema_version`)

---

### Task 1: Summary parser + aggregation in `tools/ingest_plan.py`

**Goal:** Ship the pure-function core that reads a subagent-produced summary file and aggregates N summaries into a structured `IngestPlan`. Includes golden-input fixtures.

**Files:**
- Create: `tools/ingest_plan.py`
- Create: `tests/test_ingest_plan.py`
- Create: `tests/fixtures/ingest/01-foo.summary.md`
- Create: `tests/fixtures/ingest/02-bar.summary.md`
- Create: `tests/fixtures/ingest/03-baz.summary.md`
- Create: `tests/fixtures/ingest/malformed-no-frontmatter.md`
- Create: `tests/fixtures/ingest/malformed-missing-sections.md`

**Acceptance Criteria:**
- [ ] `parse_summary(path)` returns a dict with keys `frontmatter`, `one_line`, `takeaway_sections`, `cross_ref_candidates`, `conflict_flags`, `proposed_page_shape`.
- [ ] `parse_summary` raises `SummarySchemaError` on missing frontmatter, missing required sections, or wrong `schema_version`.
- [ ] `aggregate(summary_paths)` returns an `IngestPlan` dataclass with `page_plan`, `cross_refs`, `conflicts`, `low_value`, `merge_candidates`.
- [ ] Merge candidates are flagged when ≥2 NEW page proposals share ≥2 named concepts.
- [ ] Cross-refs from ≥2 summaries are marked `strong=True`; others `strong=False`.
- [ ] Low-value flag appears when a summary's cross-ref candidates are all "extends [[X]]" with no new method/results.
- [ ] `INGEST_SCHEMA_VERSION = 1` exported at module top.

**Verify:** `poetry run pytest tests/test_ingest_plan.py -v` → all tests pass.

**Steps:**

- [ ] **Step 1: Create the three well-formed fixture summaries**

Write `tests/fixtures/ingest/01-foo.summary.md`:

```markdown
---
source: "raw/research/demo/01-foo.md"
slug: "01-foo"
summarized_on: "2026-04-21"
schema_version: 1
---

# Foo: A Novel Method

## One-line
Foo introduces a two-stage training recipe combining SFT with outcome-based RL.

## Method
Two-stage: SFT on curated reasoning traces, then outcome-based RL with a learned reward model. Derives from InstructGPT.

## Results
Table 3: +4.2 pp on MMLU over the SFT-only baseline; matches GPT-4-level Arena scores at 70B.

## Applicability
Requires RL infra and a reward model. Base-model agnostic above 7B.

## Novelty
Novel combination; neither stage alone is new but the staging is.

## Reproducibility
Code released; weights on HF; no paperswithcode entry yet.

## Adoption
Cited by 3 follow-ups within 4 months.

## Conflicts
None with current wiki.

## Cross-ref candidates
- [[rlhf]] — extends with outcome-based variant
- [[sft]] — first stage is standard SFT

## Conflict flags
(none)

## Proposed page shape
- New page: foo-method — Foo is distinct enough from RLHF to warrant its own page
```

Write `tests/fixtures/ingest/02-bar.summary.md` (a NEW page that *overlaps with 03-baz* to exercise merge detection):

```markdown
---
source: "raw/research/demo/02-bar.md"
slug: "02-bar"
summarized_on: "2026-04-21"
schema_version: 1
---

# Bar: Preference Optimization

## One-line
Bar is a reference-free preference optimization objective.

## Method
Closed-form preference loss; no reference model; derives from DPO.

## Results
Matches DPO on AlpacaEval at half the memory.

## Applicability
Direct DPO replacement for memory-constrained setups.

## Novelty
Refinement of DPO (reference-free variant).

## Reproducibility
Code released.

## Adoption
Used in two open-weights releases.

## Conflicts
None.

## Cross-ref candidates
- [[dpo]] — derives from; reference-free variant

## Conflict flags
(none)

## Proposed page shape
- New page: bar-optimization
```

Write `tests/fixtures/ingest/03-baz.summary.md` (overlaps 02-bar on "preference optimization" + "DPO"):

```markdown
---
source: "raw/research/demo/03-baz.md"
slug: "03-baz"
summarized_on: "2026-04-21"
schema_version: 1
---

# Baz: Another Preference Method

## One-line
Baz is another preference-optimization objective with a DPO-like structure.

## Method
Preference optimization via a modified DPO loss with margin term.

## Results
Small gains over DPO on three benchmarks.

## Applicability
Drop-in DPO replacement.

## Novelty
Refinement of DPO.

## Reproducibility
Code pending; weights released.

## Adoption
Single-lab result so far.

## Conflicts
Claims AlpacaEval score higher than what Bar reports on the same setup.

## Cross-ref candidates
- [[dpo]] — derives from
- [[rlhf]] — background

## Conflict flags
- Claim: Baz reports 72.1 on AlpacaEval under standard settings.
  Contradicts: [[dpo]] which cites 70.8 for the same eval.
  Basis: Table 2, page 6.

## Proposed page shape
- New page: baz-preference-method
```

Write `tests/fixtures/ingest/malformed-no-frontmatter.md`:

```markdown
# Missing frontmatter

## One-line
This file has no frontmatter.
```

Write `tests/fixtures/ingest/malformed-missing-sections.md`:

```markdown
---
source: "raw/research/demo/missing.md"
slug: "missing"
summarized_on: "2026-04-21"
schema_version: 1
---

# Missing Sections

## One-line
Only has the one-line section.
```

- [ ] **Step 2: Write the failing tests**

Create `tests/test_ingest_plan.py`:

```python
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
```

- [ ] **Step 3: Run tests, confirm they fail**

Run: `poetry run pytest tests/test_ingest_plan.py -v`
Expected: ImportError or ModuleNotFoundError on `from tools.ingest_plan import ...`.

- [ ] **Step 4: Implement `tools/ingest_plan.py`**

Create `tools/ingest_plan.py`:

```python
"""Pure-function aggregator for /ingest subagent-produced summaries.

Parses per-source summary markdown files produced by subagents during
/ingest fan-out, and aggregates a batch of them into a structured
IngestPlan used by the orchestrator to build the human review packet.

No side effects, no wiki writes, no file creation outside explicit
save_run_state calls. Unit-testable under tests/test_ingest_plan.py.

See docs/superpowers/specs/2026-04-21-subagent-per-source-ingest-design.md
for the summary schema and review-packet contract.
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


INGEST_SCHEMA_VERSION = 1


class SummarySchemaError(ValueError):
    """Raised when a summary file violates the expected schema."""


_FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
_SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_CROSS_REF_LINE_RE = re.compile(r"^-\s*\[\[([^\]]+)\]\]\s*(?:—|--|-)?\s*(.*)$")
_CONFLICT_CLAIM_RE = re.compile(r"^-\s*Claim:\s*(.+?)$", re.MULTILINE)
_CONFLICT_CONTRADICTS_RE = re.compile(
    r"^\s*Contradicts:\s*\[\[([^\]]+)\]\]\s*(?:which says)?\s*(.*)$",
    re.MULTILINE,
)
_CONFLICT_BASIS_RE = re.compile(r"^\s*Basis:\s*(.+?)$", re.MULTILINE)
_PAGE_SHAPE_NEW_RE = re.compile(r"^-\s*New page:\s*([^—\-]+?)(?:\s*—\s*(.+))?$", re.MULTILINE)
_PAGE_SHAPE_EXTEND_RE = re.compile(
    r"^-\s*(?:OR:\s*)?extend\s*\[\[([^\]]+)\]\]\s*with section\s*\"([^\"]+)\"",
    re.MULTILINE | re.IGNORECASE,
)

_REQUIRED_SECTIONS = ("One-line", "Cross-ref candidates", "Conflict flags", "Proposed page shape")
_TAKEAWAY_EXCLUDED = {"One-line", "Cross-ref candidates", "Conflict flags", "Proposed page shape"}


@dataclass
class PagePlanEntry:
    kind: str  # "new" or "extend"
    title: str  # new page title, or existing page name
    section: str | None  # for extend, the section name; None for new
    sources: list[str]


@dataclass
class CrossRef:
    page: str
    reasons: list[str]
    source_slugs: list[str]
    strong: bool


@dataclass
class MergeCandidate:
    slugs: list[str]
    shared_concepts: list[str]
    reason: str


@dataclass
class IngestPlan:
    page_plan: list[PagePlanEntry] = field(default_factory=list)
    cross_refs: list[CrossRef] = field(default_factory=list)
    conflicts: list[dict[str, str]] = field(default_factory=list)
    low_value: list[str] = field(default_factory=list)  # slugs suggested as skip
    merge_candidates: list[MergeCandidate] = field(default_factory=list)


def parse_summary(path: Path) -> dict[str, Any]:
    """Parse a subagent-produced summary file into a structured dict.

    Raises SummarySchemaError if the file lacks frontmatter, the required
    sections, or carries the wrong schema_version.
    """
    text = path.read_text(encoding="utf-8")

    m = _FRONTMATTER_RE.match(text)
    if not m:
        raise SummarySchemaError(f"{path}: missing frontmatter")
    frontmatter = _parse_simple_yaml(m.group(1))
    if frontmatter.get("schema_version") != INGEST_SCHEMA_VERSION:
        raise SummarySchemaError(
            f"{path}: schema_version={frontmatter.get('schema_version')} "
            f"(expected {INGEST_SCHEMA_VERSION})"
        )
    body = text[m.end():]

    sections = _split_sections(body)
    for required in _REQUIRED_SECTIONS:
        if required not in sections:
            raise SummarySchemaError(f"{path}: missing required section '## {required}'")

    takeaway_sections = {name: sections[name] for name in sections if name not in _TAKEAWAY_EXCLUDED}

    return {
        "frontmatter": frontmatter,
        "one_line": sections["One-line"].strip(),
        "takeaway_sections": takeaway_sections,
        "cross_ref_candidates": _parse_cross_refs(sections["Cross-ref candidates"]),
        "conflict_flags": _parse_conflicts(sections["Conflict flags"]),
        "proposed_page_shape": _parse_page_shape(sections["Proposed page shape"]),
    }


def aggregate(summary_paths: list[Path]) -> IngestPlan:
    """Aggregate parsed summaries into a single IngestPlan.

    page_plan: one entry per summary's proposed_page_shape, except entries
    that are part of a merge_candidate (those stay in page_plan individually
    — user decides whether to merge).
    cross_refs: union across summaries; strong=True when named by ≥2.
    conflicts: every conflict_flag verbatim, tagged with source slug.
    merge_candidates: ≥2 NEW page proposals that share ≥2 named cross-ref
    pages.
    low_value: slugs whose cross_ref_candidates are all "extends" style with
    no other signal — flagged as skip candidates.
    """
    parsed = [(p, parse_summary(p)) for p in summary_paths]

    plan = IngestPlan()
    _populate_page_plan(plan, parsed)
    _populate_cross_refs(plan, parsed)
    _populate_conflicts(plan, parsed)
    _populate_merge_candidates(plan, parsed)
    _populate_low_value(plan, parsed)
    return plan


# ---------- internal helpers ----------

def _parse_simple_yaml(block: str) -> dict[str, Any]:
    """Minimal key: value parser; handles quoted strings and bare ints.

    Good enough for summary frontmatter (flat, no nesting, no lists).
    """
    out: dict[str, Any] = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, _, raw = line.partition(":")
        key = key.strip()
        raw = raw.strip()
        if raw.startswith('"') and raw.endswith('"'):
            out[key] = raw[1:-1].replace('\\"', '"').replace("\\\\", "\\")
        elif raw.isdigit() or (raw.startswith("-") and raw[1:].isdigit()):
            out[key] = int(raw)
        else:
            out[key] = raw
    return out


def _split_sections(body: str) -> dict[str, str]:
    """Split body into {section_name: content} by '## Heading' markers.

    Content is the text from after the heading line up to the next heading
    (or end of body). Leading/trailing whitespace preserved per-section.
    """
    matches = list(_SECTION_RE.finditer(body))
    sections: dict[str, str] = {}
    for i, m in enumerate(matches):
        name = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        sections[name] = body[start:end]
    return sections


def _parse_cross_refs(block: str) -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    for line in block.splitlines():
        line = line.strip()
        if not line or line.lower().startswith("(none"):
            continue
        m = _CROSS_REF_LINE_RE.match(line)
        if m:
            refs.append({"page": m.group(1).strip(), "reason": m.group(2).strip()})
    return refs


def _parse_conflicts(block: str) -> list[dict[str, str]]:
    if "(none" in block.lower():
        return []
    conflicts: list[dict[str, str]] = []
    claim_matches = list(_CONFLICT_CLAIM_RE.finditer(block))
    for i, cm in enumerate(claim_matches):
        chunk_end = claim_matches[i + 1].start() if i + 1 < len(claim_matches) else len(block)
        chunk = block[cm.start():chunk_end]
        contradicts_m = _CONFLICT_CONTRADICTS_RE.search(chunk)
        basis_m = _CONFLICT_BASIS_RE.search(chunk)
        conflicts.append(
            {
                "claim": cm.group(1).strip(),
                "contradicts_page": contradicts_m.group(1).strip() if contradicts_m else "",
                "contradicts_text": contradicts_m.group(2).strip() if contradicts_m else "",
                "basis": basis_m.group(1).strip() if basis_m else "",
            }
        )
    return conflicts


def _parse_page_shape(block: str) -> dict[str, Any]:
    new_m = _PAGE_SHAPE_NEW_RE.search(block)
    if new_m:
        return {
            "kind": "new",
            "title": new_m.group(1).strip(),
            "section": None,
            "justification": (new_m.group(2) or "").strip(),
        }
    extend_m = _PAGE_SHAPE_EXTEND_RE.search(block)
    if extend_m:
        return {
            "kind": "extend",
            "title": extend_m.group(1).strip(),
            "section": extend_m.group(2).strip(),
            "justification": "",
        }
    return {"kind": "unknown", "title": "", "section": None, "justification": block.strip()}


def _populate_page_plan(plan: IngestPlan, parsed: list[tuple[Path, dict[str, Any]]]) -> None:
    for _path, s in parsed:
        shape = s["proposed_page_shape"]
        plan.page_plan.append(
            PagePlanEntry(
                kind=shape["kind"],
                title=shape["title"],
                section=shape.get("section"),
                sources=[s["frontmatter"]["slug"]],
            )
        )


def _populate_cross_refs(plan: IngestPlan, parsed: list[tuple[Path, dict[str, Any]]]) -> None:
    by_page: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"reasons": [], "source_slugs": []}
    )
    for _path, s in parsed:
        slug = s["frontmatter"]["slug"]
        for ref in s["cross_ref_candidates"]:
            entry = by_page[ref["page"]]
            entry["reasons"].append(ref["reason"])
            entry["source_slugs"].append(slug)
    for page, entry in by_page.items():
        plan.cross_refs.append(
            CrossRef(
                page=page,
                reasons=entry["reasons"],
                source_slugs=entry["source_slugs"],
                strong=len(set(entry["source_slugs"])) >= 2,
            )
        )


def _populate_conflicts(plan: IngestPlan, parsed: list[tuple[Path, dict[str, Any]]]) -> None:
    for _path, s in parsed:
        slug = s["frontmatter"]["slug"]
        for cf in s["conflict_flags"]:
            plan.conflicts.append({"source_slug": slug, **cf})


def _populate_merge_candidates(plan: IngestPlan, parsed: list[tuple[Path, dict[str, Any]]]) -> None:
    new_proposals = [
        (s["frontmatter"]["slug"], {r["page"] for r in s["cross_ref_candidates"]})
        for _path, s in parsed
        if s["proposed_page_shape"]["kind"] == "new"
    ]
    seen: set[frozenset[str]] = set()
    for i in range(len(new_proposals)):
        for j in range(i + 1, len(new_proposals)):
            slug_i, pages_i = new_proposals[i]
            slug_j, pages_j = new_proposals[j]
            shared = pages_i & pages_j
            if len(shared) >= 2:
                key = frozenset({slug_i, slug_j})
                if key in seen:
                    continue
                seen.add(key)
                plan.merge_candidates.append(
                    MergeCandidate(
                        slugs=sorted([slug_i, slug_j]),
                        shared_concepts=sorted(shared),
                        reason=f"both propose NEW pages and share {len(shared)} cross-ref pages",
                    )
                )


def _populate_low_value(plan: IngestPlan, parsed: list[tuple[Path, dict[str, Any]]]) -> None:
    for _path, s in parsed:
        refs = s["cross_ref_candidates"]
        if not refs:
            continue
        all_extends = all("extend" in r["reason"].lower() for r in refs)
        shape = s["proposed_page_shape"]
        if all_extends and shape["kind"] == "extend":
            plan.low_value.append(s["frontmatter"]["slug"])
```

- [ ] **Step 5: Run tests, confirm all pass**

Run: `poetry run pytest tests/test_ingest_plan.py -v`
Expected: all 8 tests pass.

- [ ] **Step 6: Commit**

```bash
git add tools/ingest_plan.py tests/test_ingest_plan.py tests/fixtures/ingest/
git commit -m "$(cat <<'EOF'
feat(ingest): add ingest_plan module — summary parser + aggregation

Pure-function core for the new subagent-per-source /ingest pipeline:
parse a subagent-produced .summary.md, aggregate N of them into a
structured IngestPlan (page plan, cross-refs with strength, conflicts,
merge candidates, low-value flags).

Unit-tested against golden fixtures in tests/fixtures/ingest/.
No side effects, no wiki writes — used by the orchestrator to build
the review packet.

See docs/superpowers/specs/2026-04-21-subagent-per-source-ingest-design.md

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 2: `run.json` state + `compute_dispatch_list()`

**Goal:** Add the cache/resume layer to `tools/ingest_plan.py`: read/write `.ingest/run.json`, and compute which source slugs need a fresh subagent dispatch versus reusing an existing summary.

**Files:**
- Modify: `tools/ingest_plan.py` (append new functions + dataclass)
- Modify: `tests/test_ingest_plan.py` (add tests)

**Acceptance Criteria:**
- [ ] `load_run_state(topic_dir)` returns the parsed `run.json` dict, or an empty default state (with today's `started_at`) if absent.
- [ ] `save_run_state(topic_dir, state)` writes `run.json` atomically (temp file + rename) and updates `last_updated`.
- [ ] `compute_dispatch_list(topic_dir, source_paths)` returns `(to_dispatch, cached)` — `to_dispatch` is the list of source paths needing a fresh subagent run; `cached` is the list of existing summary paths that can be reused.
- [ ] A source whose `mtime > summary.mtime` ends up in `to_dispatch`.
- [ ] A source whose run.json entry has `status: failed` ends up in `to_dispatch`.
- [ ] A summary with wrong `schema_version` ends up in `to_dispatch`, with its source.
- [ ] `--force` (callable flag on `compute_dispatch_list`) puts all sources in `to_dispatch`.

**Verify:** `poetry run pytest tests/test_ingest_plan.py -v` → all tests pass (existing 8 + 7 new).

**Steps:**

- [ ] **Step 1: Write failing tests**

Append to `tests/test_ingest_plan.py`:

```python
import json

from tools.ingest_plan import (
    compute_dispatch_list,
    load_run_state,
    save_run_state,
)


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
    import os
    import time
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
```

- [ ] **Step 2: Run tests, confirm failures**

Run: `poetry run pytest tests/test_ingest_plan.py -v`
Expected: ImportError on the new symbols.

- [ ] **Step 3: Implement the new functions**

Append to `tools/ingest_plan.py`:

```python
import os
from datetime import datetime, timezone


def _run_json_path(topic_dir: Path) -> Path:
    return topic_dir / ".ingest" / "run.json"


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def load_run_state(topic_dir: Path) -> dict[str, Any]:
    """Return the .ingest/run.json contents, or a fresh default if absent.

    Default state carries today's started_at and an empty sources map.
    """
    p = _run_json_path(topic_dir)
    if not p.exists():
        return {
            "schema_version": INGEST_SCHEMA_VERSION,
            "started_at": _iso_now(),
            "last_updated": _iso_now(),
            "sources": {},
            "review_completed_at": None,
            "pages_written": [],
        }
    return json.loads(p.read_text(encoding="utf-8"))


def save_run_state(topic_dir: Path, state: dict[str, Any]) -> None:
    """Write run.json atomically. Updates last_updated; creates .ingest/ if absent."""
    ingest = topic_dir / ".ingest"
    ingest.mkdir(exist_ok=True)
    state["last_updated"] = _iso_now()
    state.setdefault("schema_version", INGEST_SCHEMA_VERSION)
    state.setdefault("started_at", _iso_now())
    target = _run_json_path(topic_dir)
    tmp = target.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, target)


def compute_dispatch_list(
    topic_dir: Path,
    source_paths: list[Path],
    *,
    force: bool = False,
) -> tuple[list[Path], list[Path]]:
    """Partition source_paths into (to_dispatch, cached_summary_paths).

    A source needs re-dispatch when any of:
      - force=True
      - no run.json entry (never processed)
      - run.json entry status != "ok"
      - summary file missing on disk despite status=ok
      - source mtime newer than summary mtime (re-captured)
      - summary schema_version != INGEST_SCHEMA_VERSION
    """
    state = load_run_state(topic_dir)
    sources_map: dict[str, dict[str, Any]] = state.get("sources", {})
    to_dispatch: list[Path] = []
    cached: list[Path] = []

    for src in source_paths:
        slug = src.stem
        if force:
            to_dispatch.append(src)
            continue
        entry = sources_map.get(slug)
        if not entry or entry.get("status") != "ok":
            to_dispatch.append(src)
            continue
        summary_name = entry.get("summary")
        if not summary_name:
            to_dispatch.append(src)
            continue
        summary_path = topic_dir / ".ingest" / summary_name
        if not summary_path.exists():
            to_dispatch.append(src)
            continue
        if src.stat().st_mtime > summary_path.stat().st_mtime:
            to_dispatch.append(src)
            continue
        if not _summary_schema_ok(summary_path):
            to_dispatch.append(src)
            continue
        cached.append(summary_path)

    return to_dispatch, cached


def _summary_schema_ok(summary_path: Path) -> bool:
    """Return True if the summary's frontmatter declares the current schema_version."""
    text = summary_path.read_text(encoding="utf-8")
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return False
    fm = _parse_simple_yaml(m.group(1))
    return fm.get("schema_version") == INGEST_SCHEMA_VERSION
```

- [ ] **Step 4: Run tests, confirm all pass**

Run: `poetry run pytest tests/test_ingest_plan.py -v`
Expected: all 15 tests pass.

- [ ] **Step 5: Commit**

```bash
git add tools/ingest_plan.py tests/test_ingest_plan.py
git commit -m "$(cat <<'EOF'
feat(ingest): add run.json cache + dispatch-list computation

Completes the ingest_plan module with resume/cache support. Orchestrator
reads run.json to skip already-processed sources and re-dispatches the
failed, missing, stale, and schema-mismatched ones. Atomic writes via
temp-file-rename.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 3: `tools/clear_ingest_cache.py`

**Goal:** Trivial companion CLI for wiping a topic's `.ingest/` cache, with a safety check that the target path actually ends in `/.ingest/` before deletion.

**Files:**
- Create: `tools/clear_ingest_cache.py`
- Create: `tests/test_clear_ingest_cache.py`

**Acceptance Criteria:**
- [ ] `clear(topic_dir)` removes `topic_dir/.ingest/` recursively and returns `True` if it existed, `False` otherwise.
- [ ] Refuses to operate on a path whose resolved target is not named `.ingest` (defense against arg mistakes).
- [ ] CLI `poetry run python -m tools.clear_ingest_cache <topic-dir>` exits 0 on success (cleared or already absent), 2 on bad path.

**Verify:** `poetry run pytest tests/test_clear_ingest_cache.py -v` → all tests pass.

**Steps:**

- [ ] **Step 1: Write failing tests**

Create `tests/test_clear_ingest_cache.py`:

```python
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
```

- [ ] **Step 2: Run tests, confirm failures**

Run: `poetry run pytest tests/test_clear_ingest_cache.py -v`
Expected: ImportError.

- [ ] **Step 3: Implement `tools/clear_ingest_cache.py`**

Create `tools/clear_ingest_cache.py`:

```python
"""Clear a topic's /.ingest/ cache directory.

Removes all per-source summaries and run.json for a topic, forcing the
next /ingest run over the same dir to re-dispatch every source from
scratch.

Usage:
    poetry run python -m tools.clear_ingest_cache <topic-dir>
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def clear(topic_dir: Path) -> bool:
    """Remove <topic_dir>/.ingest/ if it exists. Return True if something was removed."""
    ingest = topic_dir / ".ingest"
    if not ingest.exists() and not ingest.is_symlink():
        return False
    # Safety: the path we're about to delete must itself be named `.ingest`,
    # even after symlink resolution. Guards against a symlinked `.ingest`
    # pointing at some other directory the user cares about.
    resolved = ingest.resolve()
    if resolved.name != ".ingest":
        raise ValueError(
            f"{ingest} resolves to {resolved}, which is not a .ingest directory; refusing to delete"
        )
    shutil.rmtree(ingest)
    return True


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Clear a topic's .ingest/ cache.")
    p.add_argument("topic_dir", type=Path, help="Directory containing an .ingest/ cache.")
    args = p.parse_args(argv)

    topic = args.topic_dir
    if not topic.is_dir():
        print(f"clear_ingest_cache: not a directory: {topic}", file=sys.stderr)
        return 2
    removed = clear(topic)
    print(f"cleared {topic}/.ingest/" if removed else f"{topic}/.ingest/ already absent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests, confirm all pass**

Run: `poetry run pytest tests/test_clear_ingest_cache.py -v`
Expected: all 5 tests pass.

- [ ] **Step 5: Commit**

```bash
git add tools/clear_ingest_cache.py tests/test_clear_ingest_cache.py
git commit -m "$(cat <<'EOF'
feat(ingest): add clear_ingest_cache.py companion CLI

Trivial tool to wipe a topic's .ingest/ cache when the user wants
/ingest to re-dispatch every source from scratch. Safety check refuses
to delete if the target isn't actually named .ingest (guards against
symlink shenanigans or wrong args).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 4: Rewrite `.claude/commands/ingest.md`

**Goal:** Replace the current `/ingest` prose with the orchestrator-plus-subagent flow. DOMAIN-SLOT for `takeaway-prompts` is preserved verbatim — everything else is generic kit.

**Files:**
- Modify: `.claude/commands/ingest.md` (complete rewrite)

**Acceptance Criteria:**
- [ ] File starts with `# Ingest a New Source` heading and has an `## Arguments` section supporting both file and directory paths.
- [ ] Describes the 7-step pipeline from the spec: resolve inputs → dispatch → wait for all → aggregate → human gate → write → track.
- [ ] Includes a literal subagent prompt template with the read-two/write-one hard rules and the output schema (frontmatter + One-line + DOMAIN-SLOT takeaway sections + Cross-ref candidates + Conflict flags + Proposed page shape).
- [ ] The takeaway-prompts DOMAIN-SLOT block is preserved verbatim from the current file (methods/results/applicability/novelty/repro/adoption/conflicts for this wiki).
- [ ] Documents that orchestrator runs `poetry run python -m tools.ingest_plan ...` style Bash for dispatch-list computation and aggregation (exact invocations shown inline).
- [ ] Review packet format from the spec is reproduced as a fenced markdown block so the orchestrator knows exactly what to render.
- [ ] Error-handling table from the spec is included.
- [ ] Explicit statement: "Main agent MUST NOT read raw source bodies; only subagents read sources."

**Verify:**
- Run: `poetry run pytest -q` → existing test suite still green (this task adds no code).
- Visual diff: `git diff .claude/commands/ingest.md` shows the new structure; the `<!-- DOMAIN-SLOT: takeaway-prompts -->` markers bracket the exact same content as before.

**Steps:**

- [ ] **Step 1: Read current ingest.md to confirm the DOMAIN-SLOT block content**

Run: `poetry run cat .claude/commands/ingest.md` (or Read tool) and copy the block between `<!-- DOMAIN-SLOT: takeaway-prompts -->` and `<!-- /DOMAIN-SLOT -->` verbatim. It must round-trip unchanged.

- [ ] **Step 2: Write the new ingest.md**

Replace `.claude/commands/ingest.md` with the following (the DOMAIN-SLOT block is the exact content you captured in Step 1):

```markdown
# Ingest a New Source

Process raw source documents into the wiki by dispatching one subagent per source, aggregating structured summaries, and writing wiki pages from a single human review gate. Main context never reads raw source bodies.

## Arguments

$ARGUMENTS — a file path or a directory path. If a directory, every `*.md` file in it (non-recursive) is treated as a source.

## Critical rules

- **Main agent MUST NOT read raw source bodies.** Only subagents read `raw/**/*.md` source content. Main agent reads only `.ingest/*.summary.md` (small, structured) and the specific existing wiki pages that the review plan touches.
- **Subagents write only `.ingest/<slug>.summary.md`.** No other files. No wiki writes.
- **All wiki writes happen in the orchestrator, after the human gate.**

## Pipeline

### 1. Resolve inputs

Normalise `$ARGUMENTS` to a topic directory and a list of source files:
- If `$ARGUMENTS` is a directory: enumerate `*.md` at the top level.
- If `$ARGUMENTS` is a file: topic_dir = parent dir; sources = [that file].

Read `wiki/index.md` once. Keep its contents in your working memory — subagents will each need the path to it.

### 2. Compute dispatch list

Run:

```bash
poetry run python -c "
from pathlib import Path
from tools.ingest_plan import compute_dispatch_list
import json, sys

topic = Path(sys.argv[1])
sources = sorted(topic.glob('*.md'))
to_dispatch, cached = compute_dispatch_list(topic, sources)
print(json.dumps({
    'to_dispatch': [str(p) for p in to_dispatch],
    'cached': [str(p) for p in cached],
}))
" <topic-dir>
```

Report to the user: `N sources total, K cached, (N-K) to dispatch`.

### 3. Dispatch subagents in parallel

For every source in `to_dispatch`, spawn a `general-purpose` Agent with the prompt template below. **Send all Agent tool calls in a single message** so they execute in parallel.

Subagent prompt template (substitute `<SOURCE_PATH>`, `<TOPIC_DIR>`, `<SLUG>`):

```
You are ingesting ONE raw source into a structured summary file. Your output is consumed by an orchestrator that aggregates many such summaries into a wiki update plan.

Read only these two paths:
- <SOURCE_PATH>            (the one raw source you own)
- <TOPIC_DIR>/../../wiki/index.md   (the wiki catalog — for cross-ref candidate naming)

Do NOT read:
- Other raw sources
- Sibling summaries in .ingest/
- Any other wiki pages

Write exactly ONE file:
- <TOPIC_DIR>/.ingest/<SLUG>.summary.md

Use this schema EXACTLY:

---
source: "<relative path to source from repo root>"
slug: "<SLUG>"
summarized_on: "<today's date, YYYY-MM-DD>"
schema_version: 1
---

# <source title>

## One-line
<single sentence: what is this source, what does it claim>

<!-- DOMAIN-SLOT: takeaway-prompts -->
## Method
<the technique in precise terms: architecture, training objective, data recipe, RL reward, fine-tuning protocol, etc. Name prior work it derives from.>

## Results
<concrete numbers: benchmarks hit, scale (params / tokens / compute), baselines beaten and by how much. Cite the specific table or figure.>

## Applicability
<what kind of project could use this? Prerequisites (compute budget, data scale, base-model availability, RL infrastructure).>

## Novelty
<genuinely new / refinement / recombination? Closest prior work and what changed?>

## Reproducibility
<code? paperswithcode entry? released weights? independent reproduction?>

## Adoption
<picked up by other labs? cited widely? climbing a leaderboard? community discussion?>

## Conflicts
<contradicts existing wiki claim? (see index.md)>
<!-- /DOMAIN-SLOT -->

## Cross-ref candidates
- [[existing-page-name]] — <why this source touches it: extends / contradicts / parallels>
- ...

## Conflict flags
- Claim: <precise statement from this source>
  Contradicts: [[existing-page]] which says <precise existing statement>
  Basis: <quote or tight paraphrase, with which section of the source>
(or `(none)` if no conflicts)

## Proposed page shape
- New page: <title> — <one-line justification>
- OR: extend [[existing-page]] with section "<section name>"
- OR: split into N pages: ...

Return value: a single line confirming the file was written, plus any warnings (e.g., "source appears truncated at line X").
```

### 4. Wait for all subagents; update run.json

As each subagent completes:
- If it wrote `.ingest/<slug>.summary.md` successfully: record `{"status": "ok", "summary": "<slug>.summary.md"}` in `run.json`.
- If it errored or failed schema validation: record `{"status": "failed", "error": "<reason>"}`.

Persist via:

```bash
poetry run python -c "
from pathlib import Path
from tools.ingest_plan import load_run_state, save_run_state
import json, sys
topic = Path(sys.argv[1])
state = load_run_state(topic)
state['sources'].update(json.loads(sys.argv[2]))
save_run_state(topic, state)
" <topic-dir> '<json-blob-of-updates>'
```

Block on all siblings before moving to aggregation.

### 5. Aggregate

Run:

```bash
poetry run python -c "
from pathlib import Path
from tools.ingest_plan import aggregate
from dataclasses import asdict
import json
topic = Path('<topic-dir>')
summaries = sorted((topic / '.ingest').glob('*.summary.md'))
plan = aggregate(summaries)
print(json.dumps({
    'page_plan': [asdict(x) for x in plan.page_plan],
    'cross_refs': [asdict(x) for x in plan.cross_refs],
    'conflicts': plan.conflicts,
    'merge_candidates': [asdict(x) for x in plan.merge_candidates],
    'low_value': plan.low_value,
}, indent=2))
"
```

### 6. Human gate — render the review packet

Present this block to the user, filled in from the aggregation output:

```markdown
# Ingest Review — <topic>

## Sources processed
| Slug | Title | Status | Summary path |
|---|---|---|---|
| <slug> | <title> | ok | .ingest/<slug>.summary.md |
| <slug> | — | FAILED (retry?) | — |

## Page plan (proposed)
- NEW: wiki/<topic>/<page-title>.md — sources: [<slugs>]
- EXTEND: wiki/<existing>.md with new section "<name>" — sources: [<slugs>]
- MERGE CANDIDATE: [<slugs>] both propose NEW pages but share N cross-ref pages — suggest single page, confirm?

## Cross-references to add
- [[new-page]] ↔ [[existing-page]] — strong/weak, justification
- ...

## Conflict flags (require ruling)
- <source-slug>: claim X; [[existing-page]] says Y. Basis: ...
  → options: (a) resolve in favour of new source, (b) keep existing, (c) open wiki/conflicts/<slug>.md

## Novelty / adoption highlights
- ...

## Low-value candidates (suggest skip)
- ...

## Awaiting your direction
- Accept page plan as-is?
- Any emphasis / de-emphasis per source?
- Conflict rulings?
- Retry failed summaries?
```

Wait for user input. Accept their page plan edits, skip lists, conflict rulings, and retry list verbatim. No "convince the user" loop.

### 7. Write + track

For each approved page-plan entry:
- **NEW**: create `wiki/<topic>/<title>.md` with frontmatter-free page format: `# Title`, one-paragraph summary, takeaway content drawn from the relevant summaries, `## Source` (listing raw files), `## Related` (cross-refs from the plan).
- **EXTEND**: read the existing page, add the new section, update `## Related` if new cross-refs apply.

Append each written page to `state['pages_written']` and `save_run_state` after each write, so a crash mid-write is resumable.

After all writes:
- `wiki/index.md` — add/update entries for created or modified pages.
- `wiki/revisions.md` — add a row per logical change.
- `wiki/log.md` — append a dated ingest entry: `## [YYYY-MM-DD] ingest | Source Title or Topic`.
- `run.json` — set `review_completed_at` to now.

## Error handling

| Failure | Detection | Response |
|---|---|---|
| Subagent errors out (API, timeout) | Agent tool returns non-zero | `run.json` → `failed` with error. Continue waiting for siblings. Report in review packet. User decides retry or skip. |
| Schema-invalid summary | `parse_summary()` raises `SummarySchemaError` when orchestrator tries to aggregate | Treat as `failed`; offer retry with an extra-strict prompt. |
| Subagent wrote outside `.ingest/` | Orchestrator post-check lists files under the topic dir written in the run window | Treat as `failed`; flag loudly — contract breach. |
| Empty / near-empty summary | Size < 500 bytes heuristic | Warn in review packet, don't block. |

## Resume

Re-running `/ingest <same-path>` reads existing `run.json` and skips sources already marked `ok` with a valid summary on disk. Use `poetry run python -m tools.clear_ingest_cache <topic-dir>` to force full re-dispatch.

## Report

At the end, print:
- Pages created/modified.
- Conflicts opened under `wiki/conflicts/`.
- Failed/skipped sources, if any.
- Tracking files touched.
```

- [ ] **Step 3: Sanity-check DOMAIN-SLOT preservation**

Run: `Grep` for `<!-- DOMAIN-SLOT: takeaway-prompts -->` and `<!-- /DOMAIN-SLOT -->` in the new file. Both markers must be present exactly once. The content between them must match what was there before.

- [ ] **Step 4: Smoke-check the Bash snippets parse**

Run: `poetry run python -c "from tools.ingest_plan import compute_dispatch_list, load_run_state, save_run_state, aggregate; print('ok')"`
Expected: `ok`.

- [ ] **Step 5: Commit**

```bash
git add .claude/commands/ingest.md
git commit -m "$(cat <<'EOF'
feat(ingest): rewrite /ingest as orchestrator + per-source subagents

Per docs/superpowers/specs/2026-04-21-subagent-per-source-ingest-design.md.

Main agent now dispatches one subagent per raw source in parallel, waits
for all, aggregates summaries via tools.ingest_plan, presents a single
human review packet, then writes wiki pages. Raw source bodies never
enter the main context.

DOMAIN-SLOT for takeaway-prompts preserved verbatim; everything else
is generic kit (harvestable).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 5: Update `.claude/commands/research.md` step 6

**Goal:** Reflect the new `/ingest` behavior in the `/research` tail — one subagent per captured source, single consolidated review packet.

**Files:**
- Modify: `.claude/commands/research.md` (step 6 block only)

**Acceptance Criteria:**
- [ ] Step 6 wording names the new behavior: "dispatches one subagent per captured source" and "presents a single consolidated review packet".
- [ ] Rest of the file is unchanged.
- [ ] DOMAIN-SLOTs for `authoritative-sources` and `source-type-notes` untouched.

**Verify:** `git diff .claude/commands/research.md` shows only step 6 changed; existing DOMAIN-SLOT markers still bracket the original content.

**Steps:**

- [ ] **Step 1: Edit step 6**

Replace the current step 6 text:

```
6. **Integrate via `/ingest`** — Invoke `/ingest raw/research/<topic-slug>` on the topic directory. `/ingest` reads the raw files, discusses takeaways, writes wiki pages with source-traceable claims, and updates tracking files.
```

with:

```
6. **Integrate via `/ingest`** — Invoke `/ingest raw/research/<topic-slug>` on the topic directory. `/ingest` dispatches one subagent per captured source (so raw source bodies stay out of the main context), aggregates their structured summaries, and presents a single consolidated review packet covering page plan, cross-references, conflicts, and low-value candidates. Wait for the user's rulings on the packet, then the orchestrator writes wiki pages with source-traceable claims and updates tracking files.
```

- [ ] **Step 2: Confirm only step 6 changed**

Run: `git diff .claude/commands/research.md`
Expected: one hunk, touching step 6 lines only.

- [ ] **Step 3: Commit**

```bash
git add .claude/commands/research.md
git commit -m "$(cat <<'EOF'
docs(/research): reflect new per-source-subagent /ingest in step 6

/ingest now fans out per source; /research's step 6 now names that
behavior so users know the tail of a /research run ends in a single
consolidated review packet rather than per-source discussion.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 6: `wiki/CLAUDE.md` — `.ingest/` exception + manual QA pointer

**Goal:** Document the one exception to the raw/ immutability rule (so future sessions know `.ingest/` is written by `/ingest`, not a mistake) and add a pointer to the manual QA step.

**Files:**
- Modify: `wiki/CLAUDE.md`

**Acceptance Criteria:**
- [ ] Under "Raw Sources", a new line names `raw/<topic>/.ingest/` as the one exception, and clarifies source files themselves stay immutable.
- [ ] A new "Manual QA" subsection (or pointer under "Available Commands") names `tests/fixtures/ingest-smoke/` as the canonical smoke target for `/ingest`.
- [ ] Existing bootstrap placeholders (`{{domain}}`, `{{goal}}`, etc.) are untouched.

**Verify:** `git diff wiki/CLAUDE.md` shows the two additions only; no other edits.

**Steps:**

- [ ] **Step 1: Add the `.ingest/` exception**

In `wiki/CLAUDE.md`, under the "Raw Sources" section, after the two existing bullets (`../raw/research/...`, `../raw/<other>/...`), add:

```
- `../raw/<topic>/.ingest/` is the **one exception** to the immutability rule — it holds derived summaries written by `/ingest`'s subagents. Raw source files themselves are never modified.
```

- [ ] **Step 2: Add a Manual QA subsection**

Append after "Available Commands":

```
## Manual QA for `/ingest`

A minimal smoke fixture lives at `tests/fixtures/ingest-smoke/`: two sources with a pre-known conflict. To validate any change to `/ingest`, run it on that fixture and eyeball the review packet + any pages the orchestrator would write. Document regressions in `master_notes.md` (Scope: kit).
```

- [ ] **Step 3: Commit**

```bash
git add wiki/CLAUDE.md
git commit -m "$(cat <<'EOF'
docs(CLAUDE): note .ingest/ exception + /ingest manual QA pointer

/ingest writes derived summaries into raw/<topic>/.ingest/; that is the
one allowed write-path inside raw/. Document it so future sessions
don't treat a present .ingest/ dir as contamination.

Also points at tests/fixtures/ingest-smoke/ as the canonical smoke
target for validating changes to /ingest.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 7: Integration smoke fixture at `tests/fixtures/ingest-smoke/`

**Goal:** Ship a minimal 2-source fixture directory that serves as the canonical smoke target for validating changes to `/ingest`.

**Files:**
- Create: `tests/fixtures/ingest-smoke/01-method-a.md`
- Create: `tests/fixtures/ingest-smoke/02-method-b.md`
- Create: `tests/fixtures/ingest-smoke/README.md`

**Acceptance Criteria:**
- [ ] Both source files are short (under 30 lines each), plain markdown, with distinct titles and one visible content conflict between them that the subagent should flag.
- [ ] The README explains: this is a manual QA fixture for `/ingest`; expected behaviors on success; how to re-run.
- [ ] Running `/ingest tests/fixtures/ingest-smoke/` in a dev session would produce two `.summary.md` files and surface the conflict in the review packet. (Not asserted by automated tests; documented as manual step.)

**Verify:** Visual inspection of the files; both parse as plain markdown; the conflict is clear to a human reader.

**Steps:**

- [ ] **Step 1: Create `tests/fixtures/ingest-smoke/01-method-a.md`**

```markdown
# Method A: Direct Preference Optimization variant (fixture)

Method A trains a policy model directly on preference pairs, removing
the separate reward-model stage from classic RLHF. Closed-form loss
based on log-odds of preferred vs. dispreferred responses.

## Results (fixture)
On AlpacaEval, Method A reports a length-controlled win rate of 50.2%
against the SFT baseline, matching or slightly exceeding an RLHF
pipeline at half the compute.

## Note
This is a FIXTURE file for /ingest smoke testing. It is not a real
paper; don't cite it.
```

- [ ] **Step 2: Create `tests/fixtures/ingest-smoke/02-method-b.md`**

```markdown
# Method B: Margin-augmented preference optimization (fixture)

Method B extends the Method A objective with an explicit margin term,
aiming to separate preferred and dispreferred log-likelihoods by a
fixed amount rather than just preferring one over the other.

## Results (fixture)
On AlpacaEval with identical settings, Method B reports a
length-controlled win rate of 62.1% against the SFT baseline — a 12 pp
gap over Method A on the same eval.

## Note
This is a FIXTURE file for /ingest smoke testing. It is not a real
paper; don't cite it. The 12 pp claimed gap over Method A is the
deliberate conflict a subagent should flag under "Conflict flags" when
summarising 02-method-b against Method A's 50.2% report.
```

- [ ] **Step 3: Create `tests/fixtures/ingest-smoke/README.md`**

```markdown
# `/ingest` smoke fixture

Two synthetic source files used to validate changes to `.claude/commands/ingest.md` and `tools/ingest_plan.py`.

## What to expect when you run `/ingest tests/fixtures/ingest-smoke/`

1. Two subagents dispatched in parallel.
2. `tests/fixtures/ingest-smoke/.ingest/` created with:
   - `01-method-a.summary.md`
   - `02-method-b.summary.md`
   - `run.json` listing both as `status: ok`.
3. Review packet includes a **Conflict flags** entry because 02-method-b's 62.1% claim on AlpacaEval contradicts 01-method-a's 50.2%.
4. **Merge candidate** entry (optional, depending on how the subagent wrote cross-ref candidates): both summaries likely name the same prior-art pages and both propose NEW pages.

## Clean up

```bash
poetry run python -m tools.clear_ingest_cache tests/fixtures/ingest-smoke
```

## Why this isn't an automated test

The subagent prompts live as prose inside `.claude/commands/ingest.md` and are executed via the Agent tool. Automating the full round-trip would require spinning up Claude Code itself, which is beyond the test-runner's scope. Manual QA suffices for this surface — log regressions to `master_notes.md` (Scope: kit).
```

- [ ] **Step 4: Verify files parse as markdown**

Run: `poetry run python -c "from pathlib import Path; [print(p, p.stat().st_size) for p in Path('tests/fixtures/ingest-smoke').glob('*.md')]"`
Expected: three files listed with non-zero sizes.

- [ ] **Step 5: Commit**

```bash
git add tests/fixtures/ingest-smoke/
git commit -m "$(cat <<'EOF'
test(ingest): add ingest-smoke fixture for manual QA

Two synthetic sources with a planted numeric conflict (50.2% vs 62.1%
on AlpacaEval, identical eval setup). Canonical smoke target for
validating changes to /ingest end-to-end. Not an automated test — the
subagent prompt lives as prose inside .claude/commands/ingest.md, so
the full round-trip requires running Claude Code on the fixture and
eyeballing the review packet.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Self-Review

Ran through the plan against the spec one more time:

- **Spec coverage:** Every spec section maps to a task.
  - Architecture → Task 4 (prose)
  - Subagent contract → Task 4 (prose with literal template)
  - Orchestrator aggregation + review packet → Task 1 (aggregate()) + Task 4 (packet template)
  - Persistence + resume → Task 2 (`run.json`, `compute_dispatch_list`) + Task 3 (clear tool)
  - `/research` coordination → Task 5
  - DOMAIN-SLOT boundaries → Task 4 preserves the takeaway-prompts slot verbatim
  - CLAUDE.md edit → Task 6
  - Error handling → Task 4 (table in prose)
  - Testing (`tools/ingest_plan.py`) → Tasks 1, 2 (+ Task 3 for `clear_ingest_cache.py`)
  - Integration smoke → Task 7

- **Placeholder scan:** No "TBD", no "implement later", no "similar to Task N". All code blocks are complete. One small thing — Task 4's step 3 says "Grep for DOMAIN-SLOT markers"; that's a verification action, not a placeholder.

- **Type consistency:** `compute_dispatch_list`, `load_run_state`, `save_run_state`, `aggregate`, `parse_summary`, `SummarySchemaError`, `INGEST_SCHEMA_VERSION`, `IngestPlan`, `PagePlanEntry`, `CrossRef`, `MergeCandidate` — names match across tasks, tests, and the `ingest.md` Bash snippets.

- **Dependency order:** Task 1 → Task 2 (shared module), Task 1/2 → Task 4 (orchestrator references the module). Task 3 independent of 1/2. Tasks 5/6/7 independent of each other; 5/6 reference behavior defined in Task 4. Smoke fixture (Task 7) is standalone.
