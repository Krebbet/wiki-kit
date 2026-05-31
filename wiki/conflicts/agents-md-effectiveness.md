# Conflict (OPEN): Are AGENTS.md / context files actually helpful?

> **Status: OPEN.** This page documents a live disagreement between two 2026 papers ingested 2026-04-25 in the long-horizon-context sweep. The two studies use different methodologies, target different scales, and reach opposite headline conclusions. Possible reconciling factors are described below, but they are *not* a verified consensus — neither paper directly tests the conditions of the other.

## The two positions

**[[../patterns/codified-context]]** (arXiv 2602.20478) — argues structured context infrastructure is *load-bearing* and should *scale*. Position: single-file manifests break beyond ~1,000 lines; the answer is *more* structured context, not less.

> "LLM-based agentic coding assistants lack persistent memory: they lose coherence across sessions, forget project conventions, and repeat known mistakes. ... a 100,000-line system cannot [be described in a single prompt]."

**[[../evaluation/agents-md-eval]]** (arXiv 2602.11988) — argues most context files *hurt* coding-agent performance. Position: omit LLM-generated context files; keep human-written context to *minimal requirements only*; do not include codebase overviews.

> "Across multiple coding agents and LLMs, we find that context files tend to reduce task success rates compared to providing no repository context, while also increasing inference cost by over 20%. ... unnecessary requirements from context files make tasks harder."

The headline conclusions are opposed. Both papers are 2026, both rigorous within their own methodology, and both address coding agents on real software-engineering tasks.

## Method differences (this is where the disagreement actually lives)

The two papers do not share a methodology. The differences are large enough that "who is right" is not the right question — they answer different questions.

| Dimension | Codified Context | AGENTS.md eval |
|---|---|---|
| **Study design** | Single-author, single-project experience report | Cross-repo benchmark with controlled interventions |
| **Scope of evidence** | One 70-day project, no controls | 138 instances across 12 repos + SWE-bench Lite, three settings |
| **Codebase scale** | 108k lines of C# in a real-time distributed simulation | Avg ~3,300 files in the AGENTbench Python repos; SWE-bench Lite skews to popular projects |
| **What "context" means** | A *system*: 660-line constitution + 19 specialist agents (~9.3k lines) + 34-doc cold KB (~16.3k lines) over MCP, totalling ~26k lines | A *file*: AGENTS.md or CLAUDE.md at repo root, ranging from auto-generated to developer-written |
| **Who authors the context** | Human-curated, continuously maintained over weeks | Three settings: none / LLM-auto-generated via `/init` / developer-committed |
| **Outcome measured** | Qualitative case studies + interaction-pattern stats; no controlled before/after | Patch resolution success rate + cost + behavioural deltas |
| **Causal claims** | Explicitly disclaimed by the author ("observational") | Yes — the benchmark is an experiment with three arms |
| **Language coverage** | C# only | Python only |

These are not minor methodological disagreements. They are different studies with different evidence types — one descriptive case report, one cross-sectional benchmark — that happen to weigh in on overlapping but non-identical claims.

## Possible reconciling factors (tentative)

The contradiction *may* dissolve along three axes, but none of these has been directly tested:

1. **Codebase scale.** AGENTS.md eval's repos are mid-sized; Codified Context's is large. Plausibly the curve is non-monotonic and Codified Context inhabits a regime AGENTS.md eval doesn't sample. *Untested.*
2. **Documentation quality.** AGENTS.md eval's documentation-removal ablation shows LLM-generated context becomes helpful (+9%) when all `.md`/`docs/` are stripped. Codified Context's KB documents may be qualitatively different — encoding institutional knowledge that doesn't live anywhere else, similar to the stripped-docs regime. *Plausible but unverified.*
3. **Author of the context.** AGENTS.md eval shows developer-written context gives +4%; LLM-generated gives −3%. Codified Context's constitution is explicitly human-curated. The Lulla et al. (2026) figures Codified Context cites (−29% runtime, −17% tokens) likely also come from human-authored context, consistent with AGENTS.md eval's recommendation. *Aligned but not directly compared.*

If all three factors are at play, the two positions could be saying *the same thing* under different conditions: structured context helps when (a) the model cannot reconstruct the information from priors or existing docs, and (b) the context is human-curated. But this is a hypothesis, not a finding.

## New data points (week of 2026-04-27)

Two sources from the 2026-04-27 weekly sweep add evidence on the same question without resolving it:

- **[[../patterns/effective-harnesses]]** — Anthropic's primary-source case study of long-running coding agents on the Claude Agent SDK. Recommends structured context files (`feature_list.json`, `claude-progress.txt`) as essential scaffolding for cross-session work. Notably the harness is *agent-authored during work* (the initializer agent writes the artefacts, the coding agent updates them) rather than human-pre-generated, and JSON is preferred over Markdown because "the model is less likely to inappropriately change or overwrite JSON files compared to Markdown files." Three reconciling-axis candidates surface: (a) **task type** — long-running multi-session work vs single-session well-documented repos; (b) **authorship trajectory** — agent-during-work vs LLM-pre-generated-via-`/init`; (c) **format** — structured JSON with a fixed schema vs free-text Markdown.
- **[[../case-studies/anthropic-claude-code-postmortem]]** — Bug 3 of the postmortem reports that adding a single brevity instruction to the system prompt (≤25 words between tool calls, ≤100-word final responses) produced a 3% intelligence drop on broader post-incident evals for both Opus 4.6 and Opus 4.7. This does not directly contradict [[../patterns/codified-context]] (which scales a 660-line constitution positively), but it adds an empirical data point on **prompt-layer fragility**: even a well-intentioned, locally-tested addition to the system prompt can introduce measurable regression. The fragility is at the prompt-layer, not at the file-layer that AGENTS.md eval and Codified Context primarily disagree about — so it sharpens rather than resolves the conflict.

Net: the case for "structured context helps under (a) long-running multi-session, (b) agent-authored, (c) JSON-structured" conditions is stronger after this week. The case for "any free-text addition to the system prompt is risky" is also stronger. Neither is a controlled experiment against the AGENTS.md eval methodology.

## New data points (week of 2026-05-04)

Three new sources from the 2026-05-04 weekly sweep extend the conflict on different axes; together they sharpen but do not resolve it.

- **[[../patterns/agentic-harness-engineering]] (arXiv 2604.25850)** — *fourth distinct position*: machine-evolved, multi-component harness with a strict component ablation. Single-component swap-in over the NexAU0 seed: **+memory only +5.6 pp; +tools only +3.3 pp; +middleware only +2.2 pp; +system_prompt only −2.3 pp** on Terminal-Bench 2. *Factual harness structure transfers across tasks/models, prose-level strategy does not.* This is independent corroboration (machine-evolved, controlled) of the prompt-layer-fragility data point from the postmortem (Bug 3, also a 2.3–3% drop from a small system-prompt change). The position is distinct from the existing four because (a) authorship is iteratively *machine*, (b) the unit is the *whole harness* including code/tools/memory/middleware, not just text, (c) prompt-layer additions are empirically the *weakest* layer.

- **[[../deployments/openai-symphony]] (Latent Space, May 2026)** — *positive corroboration of the agent-authored / continuously-distilled regime*. OpenAI Frontier's Symphony harness uses six skills + agents.md TOC + `core_beliefs.md` + `tech_tracker` + `quality_score` and ships >1500 PRs with 0% pre-merge human review. Distinguishing primitives: a `rework` state in the orchestrator (escalation triggers full work-tree wipe + skills-update), and **session-log harvesting** as a distillation loop (full team session logs slurped to blob storage; daily agent loops over them re-extract durable improvements back into skills/docs). Sits between Codified Context (positive) and AGENTS.md eval (negative) by sharpening the "agent-authored / continuously-distilled" axis with a second corroborating source beyond Anthropic's effective-harnesses post.

- **[[../case-studies/notion-token-town]] (Latent Space, May 2026)** — proposes a **newly surfaced reconciling axis: representation-fit-to-model-priors**. Notion's wins over four-to-five harness rebuilds did not come from changing the *authorship* of context (still mostly engineering team) but from changing the *representation*: lossless XML → simple Markdown with extensions, Notion-API JSON → SQL-lite for the agent surface (storage stays Postgres). Doctrine: *"give the models what they want"* / *"really try so hard not to expose it to any complexity about your system that's unnecessary."* This suggests the existing conflict's load-bearing axis (human-vs-LLM-authorship) may be the *wrong* axis. The right axis may be **how closely the surface representation matches what the model has seen most often in pretraining**. *Untested as a controlled finding* — flag as a candidate axis, not a resolution.

Combining the three: the wiki's current best characterisation of *when context infrastructure works* is now: structural components (memory, tools, middleware) helps; prose-level system-prompt additions hurts at the margin; the surface representation should be model-native rather than internal-engineering-convenient; agent-authored continuously-distilled artefacts beat human-pre-generated ones; long-running multi-session regimes benefit more than single-session well-documented ones. None of these are individually controlled against the AGENTS.md eval methodology; the AHE component ablation is the closest to a controlled experiment that points the same direction.

## New data points (week of 2026-05-15)

Two from the agentic-skills-personalities research sweep; neither opens a new conflict — both *strengthen the regime-dependence reconciling axis*.

- **[[../patterns/agent-skills]] (Anthropic primary sources: engineering blog + best-practices docs + Complete Guide + Claude Code docs)** — Anthropic's canonical statement of the *favorable regime's preconditions*. Skills are the same idea AGENTbench tested (packaged instruction/procedural context) but deliberately on the opposite side of every reconciling axis the conflict already names: **human/Claude-A-authored** (not LLM-auto-generated), **progressively disclosed / lazily loaded** (not always-on flat context), **evaluation-tested before documentation is written**, and **code-bearing** (deterministic scripts over prose where possible). Crucially the vendor guidance *itself* prescribes the anti-bloat discipline ("the context window is a public good"; "only add context the model doesn't already have"; SKILL.md <500 lines / <5,000 words; offload to `references/`). This is not a contradiction of AGENTbench — it is the vendor articulating exactly the conditions under which context infrastructure plausibly helps, and is best read as a candidate *reconciling lever* (disciplined progressive disclosure) rather than a fifth position. The Claude Code lifecycle detail ("skill body costs nothing until invoked" vs always-on CLAUDE.md) is a concrete mechanism for the always-on-vs-on-demand sub-axis.

- **[[../patterns/agent-personas]] (Zheng et al. 2311.10054; Hu et al. 2603.18507)** — a system-prompt-layer empirical data point that *sharpens* the prompt-layer-fragility thread (Bug 3, AHE +system_prompt −2.3 pp). Adding a persona to the system prompt is net-negative on knowledge tasks (MMLU 68 vs 71.6), net-positive on alignment/safety generation, and ≈ zero on mixed workloads (the gains and losses cancel — which is *why* the older study found an aggregate null). The reconciliation (Hu et al.) is that the effect is **task-type dependent**, recoverable only via conditioned routing (PRISM), not a static prompt addition. This is the cleanest empirical statement yet that prose added at the system-prompt layer is regime-dependent and fragile — consistent with, and independent corroboration of, the conflict's existing "prose-level system-prompt additions hurt at the margin" characterisation.

## New data points (week of 2026-05-31)

One source from the 2026-05-31 weekly sweep adds a major institutional data point without resolving the effectiveness question.

- **[[../governance/aaif]] (OpenAI blog, 2026-05-31)** — OpenAI, Anthropic, and Block co-founded the Agentic AI Foundation under the Linux Foundation, with AGENTS.md donated by OpenAI as one of three inaugural projects. This is the clearest vendor-institutional position to date: AGENTS.md is framed as essential production infrastructure for agentic AI interoperability, and the format's direction is now governed by a neutral foundation rather than a single company. The announcement cites 60,000+ open-source project adoptions since August 2025, alongside named adopters across every major coding-agent tool (Cursor, Devin, GitHub Copilot, Gemini CLI, VS Code, Jules, Amp, Factory, Codex). The adoption numbers are vendor-stated and do not address effectiveness.

**What this adds to the conflict:** AAIF formalization is a vendor-institutional commitment to context files as production infrastructure. This significantly raises the cost of the field settling on "omit context files" as a general recommendation — large-scale adoption and Linux Foundation governance create ecosystem momentum that is independent of benchmark effectiveness. The conflict now has a new axis: **adoption/governance momentum** (AAIF position: context files are load-bearing, open-standard infrastructure) versus **controlled benchmark results** (AGENTbench: LLM-generated context files reduce success ~3% and inflate cost >20%). The AAIF announcement does not engage the benchmark evidence; the benchmark evidence does not engage the production adoption scale. The conflict remains open.

## What's still genuinely open

- **No empirical bridge between the regimes.** The AGENTS.md eval does not test 100k+ line repos. Codified Context does not test what would happen if its KB were stripped or auto-generated. A paper that runs AGENTbench-style controls against a Codified-Context-style infrastructure at scale would resolve this directly.
- **Cross-language generalisation.** Both papers are language-restricted (Python, C#). Niche-language coverage may differ.
- **Maintenance overhead.** Codified Context reports ~1–2 hours/week to maintain ~26k lines of context infrastructure; AGENTS.md eval doesn't measure long-term maintenance cost in either direction.
- **Definition of "context file."** AGENTS.md eval treats any single `AGENTS.md` / `CLAUDE.md` as the unit; Codified Context treats context as a *system* that includes specialist agents and a retrieval-served KB. These may not be commensurable, and the field doesn't yet have a vocabulary that distinguishes them cleanly.
- **Causal vs descriptive evidence.** Codified Context cannot rule out that any structured project setup at this scale and effort level would have produced similar results. AGENTS.md eval cannot generalise its negative result beyond mid-sized Python repos.

## Practical guidance — *while the conflict remains open*

Without a direct empirical bridge, anyone deciding what context to ship for a coding agent has to act on probabilistic guesses:

| Condition | What the available evidence supports |
|---|---|
| Mid-sized, well-documented Python repo, LLM-auto-generated context | AGENTS.md eval directly recommends *skipping* the context file. |
| Mid-sized repo, human-written context | AGENTS.md eval supports keeping it minimal — tooling instructions only. |
| Sparsely documented repo, any author | AGENTS.md eval ablation suggests context files become helpful (+9%). |
| 100k+ line system with institutional knowledge that doesn't exist in any source file | Codified Context's tiered approach is one validated *case study* — not a controlled finding. |

Use this table as a starting position, not a conclusion. The conflict remains open until someone publishes a study that spans both regimes with consistent methodology.

## Sources

- `raw/research/long-horizon-context/01-01-codified-context.md` (https://arxiv.org/abs/2602.20478)
- `raw/research/long-horizon-context/03-03-agents-md-eval.md` (https://arxiv.org/abs/2602.11988)
- `raw/research/weekly-2026-04-27/03-03-anthropic-effective-harnesses.md` — added 2026-04-27 as a new data point on the agent-authored / JSON-structured / long-running regime.
- `raw/research/weekly-2026-04-27/01-01-anthropic-claude-code-postmortem.md` — added 2026-04-27 as a new data point on prompt-layer fragility (Bug 3, 3% intelligence drop).
- `raw/research/weekly-2026-05-04/04-agentic-harness-engineering.md` — added 2026-05-04 as a fourth distinct position (machine-evolved, multi-component, +system_prompt only −2.3 pp).
- `raw/research/weekly-2026-05-04/03-openai-symphony.md` — added 2026-05-04 as positive corroboration of agent-authored / continuously-distilled regime.
- `raw/research/weekly-2026-05-04/02-notion-token-town.md` — added 2026-05-04, proposes representation-fit-to-model-priors as a newly surfaced (untested) reconciling axis.
- `raw/research/agentic-skills-personalities/01-01..04-04` (Anthropic Skills primary sources) — added 2026-05-15 via [[../patterns/agent-skills]]; vendor articulation of the favorable-regime preconditions + progressive disclosure as a reconciling lever.
- `raw/research/agentic-skills-personalities/05-05-helpful-assistant-personas.md`, `06-06-prism-expert-personas.md` — added 2026-05-15 via [[../patterns/agent-personas]]; system-prompt-layer fragility corroboration (persona effect is task-type-dependent, ≈ zero naive net).
- `raw/research/weekly-2026-05-31/05-openai-agentic-ai-foundation.md` — added 2026-05-31; AAIF institutionalises AGENTS.md as a vendor-neutral open standard; adds adoption/governance-momentum axis to the conflict.

## Related

- [[../patterns/codified-context]]
- [[../evaluation/agents-md-eval]]
- [[../patterns/effective-harnesses]] — agent-authored handoff artefacts; new data point on long-running regime.
- [[../case-studies/anthropic-claude-code-postmortem]] — prompt-layer fragility data point.
- [[../patterns/topology-taxonomy#long-horizon-context-loss]]
- [[../case-studies/anthropic-internal-study]] — names the cold-start problem that motivates both positions.
- [[../patterns/agentic-harness-engineering]] — machine-evolved fourth position; +system_prompt only −2.3 pp ablation.
- [[../deployments/openai-symphony]] — positive corroboration; six skills + agents.md + session-log distillation at OpenAI Frontier.
- [[../case-studies/notion-token-town]] — representation-fit-to-model-priors as a newly surfaced reconciling axis.
- [[../patterns/agent-skills]] — vendor articulation of the favorable-regime preconditions; progressive disclosure as a candidate reconciling lever (2026-05-15).
- [[../patterns/agent-personas]] — system-prompt-layer fragility corroboration; persona effect is task-type-dependent (2026-05-15).
- [[../governance/aaif]] — AAIF formalises AGENTS.md as an open standard under the Linux Foundation; the institutional commitment adds an adoption/governance-momentum axis to the conflict (2026-05-31).
- [[../patterns/agents-md]] — dedicated page on the AGENTS.md format, design rationale, and governance trajectory.
