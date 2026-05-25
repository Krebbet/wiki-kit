# Agentic Harness Engineering (AHE)

Primary-source 2026 paper (arXiv 2604.25850, Qi Ji Zhi Feng et al.) introducing **observability-driven automatic evolution** of coding-agent harnesses. Ten iterations on Terminal-Bench 2 lift pass@1 from 69.7% to 77.0%, beating both the human-designed [Codex-CLI harness](https://github.com/openai/codex) (71.9%) and self-evolving baselines ACE (68.9%) and TF-GRPO (72.3%) — using the same base model throughout. The frozen Terminal-Bench-evolved harness then transfers across model families (+5.1 to +10.1 pp on three other bases) and reduces SWE-bench-verified token usage by 12% at equal-or-better success. The wiki's machine-evolved counterpart to Anthropic's hand-designed [[effective-harnesses]].

## Source

- `raw/research/weekly-2026-05-04/04-agentic-harness-engineering.md` — captured 2026-05-04 from `https://arxiv.org/pdf/2604.25850` via marker on CPU.
- Code: `https://github.com/china-qijizhifeng/agentic-harness-engineering`. Built on `https://github.com/nex-agi/NexAU`.

## Problem framing

Modern coding-agent harnesses bundle system prompt, tools, middleware, skills, sub-agents, and long-term memory — all *model-external*, all *editable*, increasingly *load-bearing*. But the optimal harness is model-specific and harness engineering is still hand-craft. Authors argue the bottleneck for automating it is **observability**, not agent capability (Sec. 1).

## Three observability pillars

1. **Component observability.** The NexAU substrate exposes seven decoupled, file-level component types at fixed mount points so each failure pattern maps to one file and every edit is git-revertible.
2. **Experience observability.** An *Agent Debugger* distils millions of raw rollout tokens into per-task analyses + a benchmark-level overview, with original traces available via progressive disclosure.
3. **Decision observability.** Every edit ships a manifest entry naming failure evidence, root cause, targeted fix, and **predicted fixes/regressions**. The next round verifies; ineffective edits are rolled back at file granularity (Sec. 3).

The Evolve Agent operates under three guardrails: writes only inside `workspace/`; runs/, tracer, verifier, and LLM config are read-only; seed system prompt marked non-deletable. All three exist to block shortcuts like disabling the verifier or raising the reasoning budget.

## Headline empirical result

Ten iterations on Terminal-Bench 2 (89 tasks; ~32 hours; k=2 rollouts/task), all three role-agents (Code Agent, Agent Debugger, Evolve Agent) sharing one base model (GPT-5.4 high):

| System | pass@1 |
|---|---|
| opencode | 47.2% |
| terminus-2 | 62.9% |
| ACE (self-evolving baseline) | 68.9% |
| **NexAU0 seed (single shell tool, no middleware)** | **69.7%** |
| Codex-CLI (human-designed) | 71.9% |
| TF-GRPO (self-evolving baseline) | 72.3% |
| **NexAU + AHE (10 iters)** | **77.0%** |

The seed is *deliberately minimal* — a single shell tool, no middleware, no skills, no sub-agents — to avoid contaminating attribution. Every component AHE adds must earn its place against measured rollouts (Sec. 3.1, Sec. 4.2).

## Cross-benchmark and cross-model transfer

**SWE-bench-verified (frozen Terminal-Bench-evolved harness):** 75.6% aggregate vs 75.2% (NexAU0 seed), 74.6% (ACE), 74.2% (TF-GRPO) — at **461k tokens/trial vs 526k seed (−12%), 582k TF-GRPO (−21%), 679k ACE (−32%)**. Gains concentrate on the largest repos (django, sphinx-doc); regressions are confined to the three smallest repos where pass@1 variance exceeds per-repo gain (Sec. 4.3, Table 2).

**Cross-model transfer:** five positive pass@1 gains, +2.3 to +10.1 pp, across GPT-5.4 (medium/xhigh), qwen-3.6-plus, gemini-3.1-flash-lite-preview, deepseek-v4-flash. **Cross-family gains dominate within-family**: deepseek +10.1, qwen +6.3, gemini +5.1. Authors interpret: bases further from saturation lean more on the coordination patterns AHE bakes into tools/middleware/memory; a stronger base re-derives them from prompt at low marginal cost (Sec. 4.3, Fig. 3).

## The component ablation: prose loses, structure wins

Swapping a single AHE-evolved component into the NexAU0 seed:

| Component swapped in | pass@1 vs seed |
|---|---|
| **+memory only** | **+5.6 pp (75.3%)** |
| +tools only | +3.3 pp (73.0%) |
| +middleware only | +2.2 pp (71.9%) |
| **+system_prompt only** | **−2.3 pp (67.4%)** |

Authors' interpretation: *factual harness structure transfers across tasks/models, prose-level strategy does not.* The 79-line "universal discipline" system prompt is only executable when the other three components are present (Sec. 4.4.1, Table 3).

This is a load-bearing finding for the wiki — see "Cross-cutting implications" below.

## Non-additive interaction

The three positive single-component gains sum to +11.1 pp, but full AHE only delivers +7.3 pp. On *Hard* tasks, memory-only (63.3%) actually exceeds full AHE (53.3%). Memory, middleware, and prompt all push toward the same closure-style verification, so stacking them spends turns on redundant re-checks. The Evolve Agent optimises an aggregate dominated by 55 *Medium* tasks → converges to a Medium-heavy trade-off (Sec. 4.4.1).

## Self-attribution: reliable for fixes, blind to regressions

Cross-iteration **fix-precision 33.7% / fix-recall 51.4%** — ~5× random baselines (6.5% / 10.6%).
Cross-iteration **regression-precision 11.8% / regression-recall 11.1%** — only ~2× random (5.6% / 5.4%).

The agent can justify why an edit *should help* but cannot reliably name which tasks the same edit is *about to break*, producing the non-monotone steps in the evolution curve. **Authors flag regression foresight as the clearest direction for future self-evolution loops** (Sec. 4.4.2).

## Concrete components AHE evolved

- **Memory** — adds 12 boundary-case lessons (performance margins, queued-over-limit cancellation, evaluator-style closure verification, source-packaging layout).
- **Tools** — becomes a 1364-line shell that auto-surfaces contract hints from files near each command.
- **Middleware** — adds a finish-hook that forces one evaluator-isomorphic closure check before declaring done.
- **System prompt** — 79 lines of universal discipline.

## Limitations the authors call out

1. **Benchmark scope.** Only Terminal-Bench 2 + SWE-bench-verified; broader languages, repository-scale deployments, and human-in-the-loop workflows untested.
2. **Evolution operating point.** AHE's step budget and per-task timeout were fitted to GPT-5.4 high; cross-model numbers conflate harness portability with operating-point coupling, and within-family gain is non-monotone across reasoning tiers.
3. **Self-modification governance.** Bounded workspace + manifest + rollback, but no complete guardrail stack — long-horizon harness cleanup and stronger misuse prevention remain incomplete; positioned as a controlled research prototype.

## Distinguished from prior self-evolution work

GEPA, ACE, ExpEL, Self-Refine target *prompts/playbooks* only. Voyager, AlphaEvolve, AFlow, ADAS edit *program structure*. AHE jointly tunes the **full harness as a combinatorial whole** so cross-component trade-offs become legible to the optimizer — explicitly named as the missing capability in earlier prompt-only loops (Sec. 2.2). Authors cite Sutton's Bitter Lesson (ref [34]) as motivation for letting the optimizer discover methodology from rollouts rather than fixing it by hand.

The paper explicitly compares against three concurrent harness-engineering primary sources: OpenAI's Codex-CLI write-up (ref [18]), Anthropic's "Effective harnesses for long-running agents" (ref [29] — see [[effective-harnesses]]), and LangChain's "Improving Deep Agents with harness engineering" (ref [40] — see [[langchain-deep-agents]]).

## Cross-cutting implications

- **Open conflict — [[conflicts/agents-md-effectiveness]] gains a fourth distinct position.** AHE is *machine-evolved, multi-component, non-prompt-centric*: the prose-layer specifically *regresses* (−2.3 pp) while tools/middleware/memory each lift on their own. That's a different position from human-authored AGENTS.md, LLM-generated context files via `/init`, and agent-authored JSON-structured handoff (effective-harnesses).
- **Empirical reinforcement of [[case-studies/anthropic-claude-code-postmortem]] Bug 3.** The postmortem found a single brevity instruction caused a 3% intelligence drop. AHE's "+system_prompt only −2.3 pp" finding is the second independent 2026 data point that prose-level prompt edits are fragile and underperform structural (tools/middleware/memory) edits.
- **[[topology-taxonomy]] long-horizon-context-loss mitigation classes** gain a meta-class: *self-evolving harness via observability-driven evolution loop*. Applies on top of any of the existing classes (materialise-state, adaptive compression, tiered hot/cold, lift-into-substrate, eliminate-the-handoff, explicit-handoff-artefacts, VM-snapshotting). Could also slot as a refinement of "explicit handoff artefacts" since the artefacts are now machine-discovered.

## SWE-Cycle benchmark framing for the autonomy gap

SWE-Cycle (arXiv 2605.13139) provides a formal benchmark framing for the long-horizon coding-agent autonomy gap that observability-driven harness evolution tries to close. Its FullCycle task requires agents to handle environment reconstruction, implementation, and test generation in a single autonomous session without pre-configured scaffolding — exactly the coherence regime AHE's evolved middleware and memory components target. The reported <14% FullCycle solve rate quantifies how far agents remain from the full-lifecycle autonomy that AHE's harness evolution is designed to close.

## Extension note (2026-05-25)

**MOSS as production counterpart** — MOSS (arXiv 2605.22794, [[patterns/moss-production-self-evolution]]) is the production-deployment counterpart to AHE. Both run an LLM-driven loop that evolves the agent harness itself, but the two systems diverge sharply on signal source and deployment model. AHE is observability-driven and benchmark-gated: the evolution loop runs against Terminal-Bench 2, uses minimal scaffolds, and produces no deployed artifact. MOSS is driven by directed real-user failure batches and carries a full production deployment lifecycle: ephemeral-container verification → user-consent-gated in-place container swap → 90-second health-probe rollback. MOSS rewrites harness source code (routing, hooks, state management); AHE evolves discrete harness components (tools, memory, middleware, system prompt) within a read-only-outside-workspace boundary.

**Framing gap to note honestly.** MOSS's Table 1 claims no prior application-level self-evolving system touches the harness and does not cite AHE. AHE clearly does evolve the harness layer. The reconciliation MOSS implies is "academic minimal scaffolds (AHE) vs application-level production substrates (MOSS)" — a plausible distinction, but it leaves AHE as the academic-setting precedent that MOSS's novelty claim overlooks rather than engages.

## Related

- [[effective-harnesses]] — Anthropic's hand-designed counterpart; AHE explicitly cites it (ref [29]).
- [[topology-taxonomy]] — extended with self-evolving harness as a new mitigation class.
- [[conflicts/agents-md-effectiveness]] — extended with AHE as a fourth position.
- [[anthropic-claude-code-postmortem]] — independent corroboration on prompt-layer fragility.
- [[codified-context]] — same shape of finding ("structure outside the prompt carries the value") via human curation rather than machine evolution.
- [[skill-distillation]] — both use evidence-driven attribution before mutating architecture (F predictor vs change-manifest verification).
- [[context-folding]] — peer mitigation; tunes in-context compression at runtime while AHE tunes the surrounding scaffold offline.
- [[langchain-deep-agents]] — peer harness pattern; AHE's seven NexAU component types extend deepagents' four.
- [[memory-architectures]] — AHE's `LongTermMEMORY.md` is a machine-evolved instance of the *episodic + structured working memory* family.
- [[evaluation/swe-bench-pro]] — eval ecosystem context (AHE reports SWE-bench-verified transfer numbers).
- [[evaluation/swe-cycle]] — formal benchmark framing for the full-lifecycle autonomy gap AHE's harness evolution targets.
- [[evaluation/airs-bench]] — peer 2026 long-horizon agent benchmark.
- [[externalization-survey]] — places AHE under the "self-evolving harnesses" emerging direction (§8.3).
- [[skillos]] — closest peer 2026 self-evolving system; same frozen-base + RL-on-external-structure pattern, scoped to skills only (vs whole-harness here). Different attribution mechanism (grouped-task downstream rewards vs change-manifest verification). Independent confirmation that **executor-grounded training matters more than curator scale** (8B-RL beats Gemini-2.5-Pro-without-RL) parallels AHE's structural-components-carry-the-lift finding.
- [[agent-development-lifecycle]] — vendor-side (LangChain) Build → Test → Deploy → Monitor framing; AHE is the machine-evolved automation of the Monitor → Iterate → Build feedback loop.
- [[patterns/moss-production-self-evolution]] — production counterpart; same LLM-driven harness-evolution loop, failure-batch signal instead of benchmark, full container-swap deployment lifecycle. MOSS rewrites harness source code where AHE evolves discrete harness components.
