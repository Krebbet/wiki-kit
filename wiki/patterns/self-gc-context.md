# Self-GC: Self-Governing Context for Long-Horizon Agents

Self-GC (arXiv 2607.00692, Xiaohongshu, 2026) reframes agent context management as runtime lifecycle control over indexed objects rather than heuristic text cleanup. *(2026-07-05)* Where conventional systems treat agent history as a linear token buffer and apply chronological pruning or end-of-context summaries, Self-GC maps user turns and tool spans into addressable runtime objects with stable identifiers, then governs each object's lifecycle through three typed actions — fold, mask, prune — with harness-enforced sidecar recovery and cache-aware commit discipline. The paper reports 15+ percentage point gains over heuristic baselines on future-dependency preservation and describes a production A/B deployment at Xiaohongshu (May 25–30, 2026) showing 10–15% daytime average input token reduction with peaks near 20%. Numbers are from an arXiv preprint using private production-derived traces; an independent reproduction package has not yet been released.

## Indexed object model

Self-GC inserts a context-engine hook between the agent harness and model input construction. The hook assigns each span a session-local monotonic identifier:

- `conversation:user:k` — a user request and its following execution span
- `function:tool:n` — a tool-level span (tool call + result) that can be edited independently

Identifiers are injected as lightweight control metadata in header fields and XML boundary tags rather than as assistant prose, so the planner can target exact objects while the harness can replay, validate, and recover edits without fuzzy text matching. Assistant turns are not first-class GC targets; they are preserved or normalized whenever adjacent objects change. The full transcript is retained outside the active view for audit and recovery; Self-GC governs only the active prompt projection.

The index serves three roles: gives the planner stable targets, lets the harness track lifecycle state per object, and separates recovery paths from summary prose. A compressed active view can still point to byte-exact folded payloads in sidecar storage — the central difference from final summary compression.

## Fold/mask/prune actions

Each indexed object receives at most one lifecycle action per governance round:

- **Fold** — moves the exact payload to sidecar storage and leaves a compact recovery pointer attached to the relevant user message. Used for large stable bodies (generated reports, editable artifacts, evidence-bearing tool outputs) that a future turn may need to quote or revise exactly. Recovery pointers are control-plane metadata, not assistant prose, reducing the risk that later turns imitate fold tags.
- **Mask** — preserves structural boundary hints (object header and footer) while eliding repetitive or low-signal middle content. Used for browser snapshots, repeated log-like trace, or large tool outputs where structure matters but payload is recoverable by re-query.
- **Prune** — removes obsolete spans from the active view with no recovery guarantee. Appropriate only after the planner has confirmed the object carries no future dependency (e.g., a failed shell command whose output has been superseded).

The planner emits actions as an XML `gc_plan` block over existing object identifiers. It does not rewrite the conversation. The harness rehearses the plan locally — resolving targets, dropping invalid or cut-turn edits, normalizing overlapping actions, materializing the projected view, estimating token savings — before any edit reaches the live context. Accepted plans are held pending until a safe turn boundary, where the harness commits them, repairs object lineage to nearest surviving ancestors, and persists folded sidecars.

A cache-aware commit policy delays GC when prefix-cache disruption would outweigh savings. The commit benefit is approximated as `N_future * (C - C') - L_cache_break - L_GC`. A deployment regression found that immediate commit is positive-value once expected active-view pruning exceeds approximately 0.3 (30%); below that threshold, Self-GC defers the plan to cache expiry or the next task boundary. The threshold is an operating policy, not a universal constant.

## Performance results

All numbers are from an arXiv preprint using private production-derived traces; collect-but-confirm until a public reproduction package is available.

**Hard Set (33 sessions, high tool-pressure browser/shell/web-fetch traces):**

| Method | Prune rate | No-impact rate | 95% CI |
|---|---|---|---|
| Oldest-turn | 63.45% | 66.67% | [49.61, 80.25] |
| Tool-prune | 67.93% | 69.70% | [52.66, 82.62] |
| Tool-mask+prune | 61.90% | 54.55% | [37.99, 70.16] |
| Hybrid | 69.87% | 57.58% | [40.81, 72.76] |
| Self-GC | 43.95% | **84.85%** | [69.08, 93.35] |

Self-GC gives up some pruning depth in exchange for at least 15.15 percentage points of no-impact gain over the strongest heuristic.

**Production Suite (332 sessions, full production mix):**

| Method | Prune rate | No-impact rate | 95% CI |
|---|---|---|---|
| Oldest-turn | 40.19% | 87.46% | [83.46, 90.60] |
| Tool-prune | 47.76% | 77.71% | [72.93, 81.86] |
| Self-GC Qwen3.6-Plus | 31.51% | 92.77% | [89.47, 95.09] |
| Self-GC Qwen3.7-Max | 33.98% | **94.58%** | [91.59, 96.54] |
| Self-GC GLM-5.1 | 31.04% | 91.27% | [87.74, 93.85] |

All three planner backbones exceed 91% no-impact; planner-backbone differences are modest, supporting use of a mid-tier planner in production. Even the best planners propose touching the mandatory last turn in 4–8% of raw plans, which is why harness-enforced last-turn filtering is a required safety mechanism rather than an optional guard.

**Online production A/B (Xiaohongshu, May 25–30, 08:00–22:00):** account-level split (email first character ≥ o = Self-GC group) over `context-gc` and `skill-gc` traffic showed 10–15% daytime average input token reduction, peaks near 20%. The online log measures prompt-surface impact only; it does not constitute a matched billed-cost audit or a fully randomized quality experiment.

## Failure taxonomy

The appendix enumerates six dependency-centered failure categories. Each names what future action becomes unsupported, not merely which message type was removed:

1. **Evidence-detail loss** — exact rows, table values, metric definitions, SQL filters, stack frames, or sparse middle evidence are removed; the future turn can continue the story but cannot reproduce or audit the concrete result.
2. **Locator / handle loss** — file paths, document ids, task ids, callback URLs, wait handles, or final handoff links are pruned; the agent knows an artifact exists but cannot reopen, rerun, or deliver it.
3. **Behavioral-contract loss** — user corrections, schema rules, instruction files, policy constraints, or task-specific conventions are folded away; later edits drift from the requested rule even though the high-level task remains visible.
4. **Verbatim-source loss** — original wording, transcript spans, quotes, field labels, or generated bodies are replaced with prose summary; a restore, quote, or exact-copy request in a later turn fails.
5. **Live-state loss** — current blockers, corrected rerun results, active failure state, or latest successful handoff are pruned; the retained prefix looks complete while the real task is blocked or recently corrected.
6. **Recovery-routing loss** — folded content exists in sidecar storage but the active view lacks enough semantic route information to know when or what to recover; recovery is technically possible but practically undiscoverable.

Self-GC mitigates these via planner prompt rules (exclude live handles, instruction files, and evidence-bearing spans from GC candidates), few-shot calibration anchored to each failure type, and harness enforcement (required-retention anchors, sidecar pointers with routing metadata, last-turn filter).

## Source

- arXiv 2607.00692 — "Self-GC: Self-Governing Context for Long-Horizon LLM Agents," Xubin Hao, Hongjin Meng, Xin Yin, Jiawei Zhu, Chenpeng Cao (Xiaohongshu)
- Production A/B: Xiaohongshu, May 25–30, 2026
- Captured: `raw/research/weekly-2026-07-05/03-04-self-gc-context.md` (pymupdf; text complete, figures missing)

## Related

- [[patterns/context-engineering]] — Self-GC is a concrete production realization of JIT retrieval + compaction; adds harness-enforced object lifecycle where that pattern treats context as text
- [[patterns/anthropic-context-engineering]] — addresses the same context rot / attention-budget problem from a platform perspective; Self-GC adds the fold/mask/prune taxonomy and sidecar recoverability
- [[context-folding]] — AgentFold performs proactive context folding for web agents; Self-GC extends folding with typed lifecycle actions and harness-enforced sidecar recovery
- [[patterns/effective-harnesses]] — Self-GC's failure taxonomy directly names "compaction isn't sufficient" failure modes that harness design must guard against
- [[patterns/agentic-harness-engineering]] — Self-GC is implemented as a harness-portable context-engine hook; requires only turn/tool-span boundary exposure from the harness
