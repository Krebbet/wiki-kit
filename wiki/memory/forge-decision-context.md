# Forge Decision Context (forge_dc)

Forge Decision Context (forge_dc; Vahdat & Vaezipoor, NeurIPS 2026 listing) is a behavioral/procedural memory system that compiles human corrections and self-assessed tool-call failures into imperative `RULE` directives and injects them at the decision points where they apply. On DC-Bench (a new 71-scenario, 9-dimension benchmark built from real agent traces) the authors report 95% rule compliance versus 55% for naive retrieval, using roughly 10x fewer injected tokens per query. **Abstract-only evidence; self-built benchmark; collect-but-confirm.**

## Claims (from the abstract)

- **Problem:** agents do not learn from corrections across sessions, so a user re-fixes the same mistake every conversation. Existing memory systems store facts (preferences, entities, history), not procedural knowledge.
- **Mechanism:** capture behavioral signals from (a) human corrections and (b) self-assessed tool-call failures; compile them into imperative RULE directives; inject them proactively at the decision point, before any output exists.
- **Headline finding, "Only Rules Rule":** the same correction an agent applied in-session is often ignored when surfaced as descriptive text in retrieved memory, but followed reliably as an imperative rule. Format at use time matters, not only what is stored.
- **Compared against** four predecessor approaches (unnamed in the abstract).

## Why it matters for this wiki

- It is a *use-time format* argument for compilation, orthogonal to the storage-time verbatim-vs-extracted debate in [[conflicts/verbatim-vs-extracted-memory]]: raw retrieval can win at storage/recall while compiled directives win at compliance. It also fits the recall-vs-use gap documented in [[memory/memory-architectures]] ("retrieved but not followed").
- It is a tension (not a contradiction) with [[evaluation/learn2play-bench]], where raw interaction histories beat rule-extracting memory on one backbone; the tasks differ (hidden-rule games vs. behavioral corrections), so likely reconcilable by task type.
- A concrete procedural-memory instance for the Experience tier of [[memory/memory-evolution-survey]]; a candidate behavioral-memory class for [[proposals/memory-system-architecture]].
- Risk (wiki-side inference, not a source claim): compiled rules from corrections are a write path into agent behaviour, so provenance and write-gating matter; compare [[security/memory-poisoning-mpbench]].

## Caveats

- Abstract-only: no mechanism detail, baselines, DC-Bench construction, or code/data status.
- Unclear whether "compliance" measures real task success or only rule-following; N=71 scenarios.

## Source

- `raw/research/weekly-2026-11-15/03-decision-context.md` (https://neurips.cc/virtual/2026/169598)

## Related

- [[conflicts/verbatim-vs-extracted-memory]]
- [[memory/memory-architectures]]
- [[memory/memory-evolution-survey]]
- [[evaluation/learn2play-bench]]
- [[proposals/memory-system-architecture]]
- [[security/memory-poisoning-mpbench]]
- [[conflicts/agents-md-effectiveness]] — imperative-vs-descriptive instruction framing
