# MAI-Thinking-1: Microsoft's Distillation-Free Reasoning Model

Microsoft AI's first in-house reasoning model: a sparse MoE with 35B active parameters (~1T total) trained on clean, commercially-licensed data with **no synthetic/distilled data from any third-party model**, reaching 97.0% on AIME 2025 and 94.5% on AIME 2026. Announced at Microsoft Build 2026. No weights or paper released as of 2026-06-06. Represents an explicit methodological position against the distillation-heavy approach dominating mid-size reasoning model development.

## Method

**Architecture.** Sparse MoE, 35B active / ~1T total parameters, 256k token context. Supports function calling, multi-layer instruction following (developer + user layers), Chat Completions API. Deployed via Microsoft Foundry.

**Pre-training.** ~30T tokens of clean, commercially-licensed text. AI-generated content explicitly excluded. No distillation from GPT, Claude, or any third-party model at any training stage. Microsoft's stated rationale: distillation-trained models are fundamentally constrained by teacher design decisions and lack steerability; "capabilities should be learned, not inherited."

**Post-training — "Hill-Climbing Machine."** RL-based, using an in-house co-designed pipeline where data, reward functions, compute, and evaluation environments are iteratively improvable. Agentic coding capability developed via deterministic, executable training environments graded by real test suites (multi-step SWE: read code, edit files, run tests, observe failures, recover).

**Safety-integrated RL.** Unsafe compliance and unnecessary refusal are treated as defects within the same reward aggregation, weighted by potential harm severity. Safety is not a separate post-hoc layer — it is part of the hill-climbing reward loop alongside capability training.

## Results

- AIME 2025: 97.0%
- AIME 2026: 94.5%
- SWE-Bench Pro: comparable to Claude Opus 4.6 (exact score not in announcement text; image table)
- Human side-by-side preference (1,276 tasks, Surge professional raters): preferred over Claude Sonnet 4.6
- Baselines listed in comparison table: Claude Sonnet 4.6, Claude Opus 4.6, GPT-5.4 (numeric scores not extractable from announcement)

**Caveat:** All results from the announcement only. No paper, no code, no model weights, no independent verification. Benchmark comparison tables are images; exact competitor scores are not extractable.

## Applicability

Enterprise developer and coding-assistant workflows where data provenance matters (compliant, auditable, no distilled-from-competitor-model risk). Requires API access via Microsoft Foundry/Azure — no open-source release. 256k context; Think-mode depth not specified. Not usable in contexts requiring locally-deployed weights.

## Source

- Announcement: https://microsoft.ai/news/introducing-mai-thinking-1/ (2026-06-03)
- No arXiv, no code, no weights as of 2026-06-06
- Venue: Microsoft Build 2026 announcement

## Related

- [[reasonmaxxer]] — both pursue reasoning via RL without distillation; compare training-loop design and AIME headroom
- [[scalelogic]] — MoE scaling efficiency; MAI's 35B-active/~1T-total ratio is a data point for active-vs-total parameter curves
- [[llamarl]] — production RL post-training methodology; compare safety-integrated RL vs separate safety stage
- [[token-gradient-cancellation]] — MoE routing may interact with gradient cancellation in RL; flag for architecture-level cross-check
