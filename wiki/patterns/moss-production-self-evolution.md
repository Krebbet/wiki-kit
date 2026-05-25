# MOSS: Production Self-Evolution via Source-Level Harness Rewriting

MOSS (arXiv 2605.22794) is a production self-evolution system that extends agentic self-improvement beyond text-mutable artifacts — skills, prompts, memory, workflow graphs — to the agent harness source itself: routing, hooks, state management, dispatch. It combines directed failure-batch evidence curation drawn from live user sessions, ephemeral-container runtime verification of candidate harness images, and a user-consent-gated in-place container swap with a 90-second health-probe rollback window. On the OpenClaw production agent, a single cycle rewrites three harness files (177 insertions, 1 deletion) in the tool-result mediator and before-tool-call hook chain, lifting the four-task claweval grader mean from 0.2526 to 0.6100. These numbers are collect-but-confirm: same four tasks serve as both the failure batch and the post-evolution test set — the authors acknowledge this is controlled and non-generalizing. The claweval grader is an external tool independent of MOSS's internal scoring, which adds modest credibility, but the same-batch-in/out design inflates expected gains versus organic evaluation. Code is released; reproducibility in principle is possible but multi-cycle behavior and organic-traffic validation have not been reported.

## Core Thesis

Source-level modification of the harness is argued to be Turing-complete and a strict superset of every text-mutable evolution scope. Where skills, prompts, memory, and workflow graphs are reachable by string substitution, the harness's own routing, hooks, and dispatch logic is not. A tool-result mediator or before-tool-call hook that systematically mishandles a case class cannot be corrected by rewriting a prompt; it requires changing the code that runs the prompt. MOSS targets that layer.

### Table 1 coverage claim

MOSS's Table 1 positions it as the only application-level self-evolving system covering all four evolution scopes: Skill, Prompt, Memory, and Harness. Five comparators — Hermes Agent, SkillClaw, GenericAgent, EvoAgentX — each leave Harness unchecked.

**Framing gap to note honestly:** [[patterns/agentic-harness-engineering]] (AHE, arXiv 2604.25850) also evolves the harness layer — tools, middleware, memory, system-prompt components — via an observability-driven automatic loop, ten iterations on Terminal-Bench 2. AHE is not cited in MOSS; Table 1 omits it. MOSS's implicit distinction is *production-deployed application-level substrate* versus *academic minimal scaffold* (AHE's NexAU seed harness on a controlled benchmark). That distinction is real — AHE operates with no user-consent gate, no container swap lifecycle, and no evidence curation from organic user sessions. But AHE does evolve harness source, which MOSS's "no prior system" framing obscures. Treat AHE as a parallel academic-setting harness-evolver, not an absence from the field.

## Architecture: Five Components

1. **moss-gateway container.** User-facing agent plus in-container evolution service plus bind-mounted `moss` CLI. The user's live container; swapped in-place on `moss evo apply`.
2. **host-daemon.** Asyncio process on the host supervising the full lifecycle: trial-worker orchestration, coding-agent invocation, auto-scan over session JSONLs, container swap execution.
3. **Pluggable external coding-agent CLI.** Claude Code, OpenAI Codex, DeepSeek-TUI, or OpenCode — selected at config time; per-stage override supported. MOSS delegates the act of editing; it does not own it.
4. **Ephemeral trial workers.** N containers from the candidate image, network- and mount-isolated from the live container. No user-state mount. Replay the failure batch autonomously to produce graded scores.
5. **Seven-stage pipeline.** Locate → Plan → Plan-Review → Implement → Code-Review → Task-Evaluate → Verdict. Verdict returns one of: `CONVERGED`, `NEED_MORE_WORK`, `FUNDAMENTAL_LIMIT_MODEL`, `FUNDAMENTAL_LIMIT_ARCHITECTURE`. A plateau guard forces convergence when no keypoint improves over N consecutive iterations.

What is frozen: the host-daemon, stage-ordering logic, and swap mechanics. The base model (DeepSeek V3.2 in the case study) is unchanged throughout.

## Evidence Curation: Directed Failure Batches, Not Benchmark Fitness

The key departure from academic self-evolution loops (Darwin, HyperAgents, SICA) is how evolution is triggered and what it optimizes. MOSS does not run a continuous fitness signal against a benchmark. Instead:

- **Automated curation.** A cron job runs `moss evo catch-up` over session JSONLs, scoring keypoints and appending weak or missing chunks to the open batch.
- **User-directed curation.** The user runs `moss evo flag` from conversation to add a specific failing exchange to the batch.
- **Threshold sealing.** The open batch seals at a configurable chunk count (default 8) and triggers a new evolution cycle.

Evolution is anchored to fixing this directed batch. The coding-agent pipeline is given the batch as ground truth and the harness source as its workspace. It must demonstrate — via trial-worker replay — that the candidate image lifts batch scores before the verdict can be `CONVERGED`.

## Deployment Lifecycle

Convergence does not auto-promote. The user invokes `moss evo apply` (via conversation or directly). The host-daemon performs an in-place container swap:

- 90-second probe window: 4 health checks, sampled every 5 seconds, 3 consecutive passes required to commit.
- Rollback target: an independent last-known-good image record. Rollback is automatic if the probe window fails.
- User-state volume (sessions, memory, credentials, agent configs) is mounted from the host filesystem and survives the swap intact.

The full lifecycle — evidence curation → ephemeral verification → consent gate → swap → health probe → rollback — distinguishes MOSS from AHE's benchmark-gated score comparison, which has no deployment surface and no user in the loop.

## Substrate Portability

Any substrate providing five primitives can host MOSS without MOSS code changes: shell tool, filesystem read, periodic scheduling, webhook-to-agent delivery, system-prompt injection. Control surface is exposed as nine `moss evo` CLI subcommands via system-prompt injection and an on-disk capability document the agent reads on demand. Async events (evolution-converged, evolution-failed, apply-complete) are delivered via webhook.

## Case Study Result

OpenClaw (production multi-channel agent, DeepSeek V3.2 base). Single cycle. Four failure-batch tasks.

| Task | Pre-evolution | Post-evolution | Δ |
|---|---|---|---|
| T138_restock_chain_check | — | 0.9049 (3/3 trials above 0.75) | largest gain |
| T137zh | — | — | +0.2354, 1/3 trials passing |
| **Mean (4 tasks)** | **0.2526** | **0.6100** | **+0.3574** |

The fix landed in the tool-result mediator and before-tool-call hook chain — harness code unreachable by any text-mutable evolution scope.

**Authority and reproducibility caveat.** These are the authors' own runs. No baseline from any other self-evolving system on the same substrate is presented. The same four tasks are both the failure batch used to drive evolution and the test set used to measure gain — expected gains are inflated versus an independent evaluation set. Single cycle; multi-cycle behavior is unreported. Code is available on GitHub, supporting reproducibility in principle. Treat as proof-of-concept until independent multi-cycle, organic-traffic evaluation is available.

## Positioning Against Peer Systems

- **vs [[patterns/agentic-harness-engineering]]:** Both evolve harness source. AHE is benchmark-gated (Terminal-Bench 2), benchmark-driven (fitness signal), no production deployment lifecycle, no user-consent gate. MOSS is production-failure-batch-driven, has a full deployment lifecycle (swap + health probe + rollback), and requires explicit user consent to promote a candidate. AHE's case for harness evolution is statistically stronger (ten iterations, cross-model transfer, token efficiency gains). MOSS's case for *production deployment* around harness evolution is not covered by AHE at all.
- **vs [[patterns/skillos]]:** SkillOS applies RL curation to the skill layer (text-mutable) over a frozen executor. MOSS targets the harness layer that SkillOS leaves unchanged. SkillOS uses downstream reward signal; MOSS uses LLM-as-coding-agent with keypoint evaluation. Both are frozen-base + evolved-scaffold, but at different layers of the stack.
- **vs [[patterns/sdar]]:** SDAR internalizes skills into model weights via distillation — the opposite end of the [[patterns/externalization-survey]] arc. SDAR leaves zero runtime artifacts; MOSS leaves modified harness source code that outlives the session. MOSS maximizes externalization; SDAR eliminates it.
- **vs [[deployments/openai-symphony]]:** Symphony distills session-log signal into `agents.md` (a text-mutable artifact). MOSS extracts signal from session JSONLs and feeds a harness rewrite pipeline. Both curate from execution traces; the output layer is categorically different.
- **vs [[patterns/harness-design-space]]:** The 70-project empirical survey identifies five harness design dimensions. MOSS adds a sixth — self-evolution scope — not present in that taxonomy.

## Source

- `raw/research/weekly-2026-05-25/03-moss-self-rewriting.md` — primary capture.
- arXiv 2605.22794 — "MOSS: Self-Evolution through Source-Level Rewriting in Autonomous Agent Systems."
- Code: https://github.com/dav-joy-thon/MOSS

## Related

- [[patterns/agentic-harness-engineering]] — parallel academic-setting harness-evolver; benchmark-gated, no production deployment lifecycle; MOSS's "no prior system" claim omits it.
- [[patterns/skillos]] — skill-layer-only peer; both frozen-base + evolved-scaffold.
- [[patterns/sdar]] — weights-internalization endpoint of the externalization arc; opposite of MOSS.
- [[patterns/externalization-survey]] — places self-evolving harnesses as an emerging direction; MOSS is the production instantiation.
- [[patterns/topology-taxonomy]] — self-evolving-harness mitigation class; MOSS is a concrete production instantiation with full deployment lifecycle.
- [[patterns/effective-harnesses]] — Anthropic's hand-designed static harness counterpart; thematically adjacent, not self-evolving.
- [[patterns/harness-design-space]] — 70-project empirical taxonomy; MOSS's self-evolution scope is a sixth dimension not covered there.
- [[deployments/openai-symphony]] — parallel trace-to-artifact curation; Symphony targets text-mutable `agents.md`, MOSS targets harness source.
