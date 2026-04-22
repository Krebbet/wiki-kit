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
_PAGE_SHAPE_NEW_RE = re.compile(r"^-\s*New page:\s*([^—\n]+?)(?:\s*—\s*(.+))?$", re.MULTILINE)
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


_CONCEPT_STOPWORDS = frozenset(
    {
        "a", "an", "the", "and", "or", "but", "is", "are", "was", "were", "be",
        "been", "being", "of", "in", "on", "at", "to", "for", "with", "by", "from",
        "as", "this", "that", "these", "those", "it", "its", "has", "have", "had",
        "also", "another", "both", "only", "than", "then", "some", "any", "all",
        "new", "via", "like", "over", "under", "into", "onto", "upon", "each",
        "when", "where", "while", "about", "before", "after", "same",
    }
)


def _extract_concepts(summary: dict[str, Any]) -> set[str]:
    """Extract normalized "named concepts" from a parsed summary.

    Concepts are the union of:
      - cross-ref page names (lowercased),
      - significant tokens from the one-line (length >= 4, not stopwords).
    """
    concepts: set[str] = set()
    for ref in summary["cross_ref_candidates"]:
        concepts.add(ref["page"].strip().lower())
    for token in re.findall(r"[a-zA-Z][a-zA-Z0-9]+", summary["one_line"]):
        low = token.lower()
        if len(low) >= 4 and low not in _CONCEPT_STOPWORDS:
            concepts.add(low)
    return concepts


def _populate_merge_candidates(plan: IngestPlan, parsed: list[tuple[Path, dict[str, Any]]]) -> None:
    new_proposals = [
        (s["frontmatter"]["slug"], _extract_concepts(s))
        for _path, s in parsed
        if s["proposed_page_shape"]["kind"] == "new"
    ]
    seen: set[frozenset[str]] = set()
    for i in range(len(new_proposals)):
        for j in range(i + 1, len(new_proposals)):
            slug_i, concepts_i = new_proposals[i]
            slug_j, concepts_j = new_proposals[j]
            shared = concepts_i & concepts_j
            if len(shared) >= 2:
                key = frozenset({slug_i, slug_j})
                if key in seen:
                    continue
                seen.add(key)
                plan.merge_candidates.append(
                    MergeCandidate(
                        slugs=sorted([slug_i, slug_j]),
                        shared_concepts=sorted(shared),
                        reason=f"both propose NEW pages and share {len(shared)} named concepts",
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
