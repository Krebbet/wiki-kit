# Agent Topology Taxonomy

Multi-agent systems vary along an orthogonal axis to the per-agent reasoning loop: **how agents connect**. The January 2026 arXiv taxonomy survey names four topologies, each with a different sweet spot and failure mode.

## The four topologies

- **Chain / waterfall** — agents pass work sequentially with fixed handoffs. Example frameworks: **MetaGPT**, **ChatDev**. Fits rigid multi-stage workflows with clear handoffs (software-engineering pipelines).
- **Star / hub-and-spoke** — a central controller dispatches to specialist workers. Example: **AutoGen**. Fits heterogeneous tool integration and human-in-the-loop oversight.
- **Mesh / swarm** — decentralized, dynamic collaboration. Fits ideation and debate — used in **MAD** (multi-agent debate) and similar.
- **Explicit workflow graphs** — typed state machines with declared transitions. Examples: **LangGraph**, **Swarm**. Fits production systems needing debuggability, checkpointing, and safety guardrails.

*(arXiv 2601.12560, 2026-01, literature-review synthesis; practitioner-consensus in current industry adoption.)*

## When each breaks

- **Chain** — a single early failure cascades downstream; no recovery path.
- **Star** — central controller is a single point of failure and a bottleneck.
- **Mesh** — task-decomposition quality degrades sharply at scale; coordination overhead swamps gains.
- **Graph** — most complex to design; still breaks on unmodeled states.

See [[failure-modes]] for more.

## The cost-depth tradeoff

Hierarchical architectures (e.g., **ReAcTree**) maximize reasoning depth but incur *exponential* token overhead relative to linear chains. This is a live constraint for any deep-tree decomposition — budget accordingly. *(arXiv 2601.12560, cited experiments.)*

## Standardization signal

**Model Context Protocol (MCP)** is named in both Anthropic's 2024–2025 writing and the 2026 arXiv taxonomy as the emerging cross-framework standard for tool discovery and governance. A rare sticky convention in a field that churns — see [[framework-skepticism#mcp-exception]]. *(Emerging, 2024–2026.)*

## Relation to Anthropic's five patterns

The Anthropic pattern vocabulary (see [[building-effective-agents]]) maps onto these topologies without conflict:

- **Orchestrator-workers** → typically **star**.
- **Prompt chaining** → **chain**.
- **Evaluator-optimizer** → either **chain** (single critic pass) or a small **mesh** (debate).
- **Routing** → a shallow **star**.
- **Parallelization** → trivial **star** with identical workers.

The taxonomy paper does not explicitly engage Anthropic's framework; this mapping is *synthesis* across sources — Claude's reading of the corpus, not a source claim.

## Long-horizon context loss

A cross-cutting failure mode that no single topology eliminates: as a task grows in scope or duration, agents ship surface-level fixes that violate deeper project conventions — the kind of mistake a contributor with full context would never make. The wiki has converging evidence on the **diagnosis**, a stable **vocabulary** for the design space, and several distinct **mitigation classes**.

### Diagnosis

- **Empirical**: [[swe-bench-pro]] shows performance degrades monotonically with lines-changed and files-touched, and frontier models take a 5–8 point hit moving from public to private (unfamiliar) codebases — a direct measurement of the context-transfer gap. [[agents-md-eval]] adds a second empirical surface: in well-documented mid-sized Python repos, *adding* context files via the agent's own `/init` command can *reduce* success rate ~3% and inflate cost >20% — exploration inflation, not non-compliance.
- **Practitioner**: [[anthropic-internal-study]] names the "cold start problem" as the main friction limiting wider delegation; >50% of engineers can fully delegate only 0–20% of work. The study also flags the *paradox of supervision* — AI use erodes the deep skills needed to catch these mistakes.
- **Infrastructure**: [[mcp-infrastructure]] documents this as a protocol gap too — context bloat, async task lifecycle, and result-retention windows are 2026-roadmap priorities precisely because today's substrate doesn't reliably preserve context across long-running work.

### Vocabulary

[[memory-architectures]] gives the design space a stable taxonomy: a *write–manage–read loop*, three orthogonal axes (temporal scope, representational substrate, control policy), and five mechanism families — *context-resident compression*, *retrieval-augmented stores*, *reflective self-improvement*, *hierarchical virtual context*, *policy-learned management*. Subsequent mitigation pages classify into this taxonomy.

### Mitigation classes

- **Materialise state in the topology** — [[ai-scientist-v2]] makes each tree-search node a tuple (script, plan, error trace, metrics, figures, VLM feedback, status), with a four-stage manager enforcing coherence across stages and a VLM as second-look quality gate. *(Branching topology, planning-time materialisation.)*
- **Adaptive in-context compression** — [[context-folding]] (AgentFold) emits a folding directive concurrently with each tool call, choosing granular condensation or deep consolidation per step. Context stays at ~7k tokens after 100 turns, scales to 500+. *(Single-chain topology, retrospective materialisation; instance of context-resident compression.)*
- **Tiered hot/cold memory infrastructure** — [[codified-context]] runs a 660-line always-on constitution + 19 specialist agents (~9.3k lines) + 34-doc cold KB (~16.3k lines) over MCP, validated on a 108k-line C# system. *(Instance of hierarchical virtual context.)*
- **Lift memory out of agents into the substrate** — [[cognitive-fabric-nodes]] proposes middleware that intercepts and rewrites every inter-agent message, with memory as functional substrate rather than per-agent store. *(Addresses the multi-agent memory governance open challenge.)*
- **Eliminate the handoff entirely** — [[skill-distillation]] (CUHK, April 2026) introduces *Metric Freedom (F)*, a predictor computable from baseline runs that says when a multi-agent pipeline can be collapsed into a single-agent skill without loss. Empirically: r = −0.85 between F and skill-distillation lift across 18 task-metric pairs. When F is high, no amount of within-MAS context preservation matches what a single agent + tools achieves at 1.4–8× lower cost and 3–15× lower latency. *(The other four mitigation classes are remediation; this one is elimination. F is the branch condition.)*
- **Explicit handoff artefacts (initializer + coding-agent pattern)** — [[effective-harnesses]] (Anthropic, April 2026) names two failure modes — *try-too-much* and *declare-done-prematurely* — and corrects them with a two-fold harness: an initializer agent writes `feature_list.json` (200+ entries, structured JSON) + `claude-progress.txt` (plain-text log) + `init.sh` + an initial git commit; every subsequent coding agent reads them, runs a smoke test, works on **exactly one feature**, commits with descriptive messages, and appends progress before exit. Headline claim: **compaction is not sufficient** — even Opus 4.5 in a loop on the Claude Agent SDK fails on `"build a clone of claude.ai"` without explicit handoff artefacts. *(Sixth mitigation class. Sibling to context-resident compression and tiered hot/cold memory; the artefacts persist outside the context window rather than within it.)* [[langchain-deep-agents]] generalises the same pattern into an OSS library with four reusable components (system prompt, no-op planning tool, sub-agents, file system) on LangGraph.

A seventh adjacent class addresses the *compute-and-state* side of the same long-horizon problem rather than the *context* side: [[cognition-cloud-agents]] argues that containerised agents cannot survive the *async gap* of real SDLC work (PR open → CI wait → review → retest → push) without burning compute to stay alive. The fix is **VM-level isolation with hypervisor-level snapshotting** — full machine state (memory, process trees, filesystem) snapshotted on idle, resumed on trigger. Distinct mitigation axis; same long-horizon symptom space.

An eighth class operates as a **meta-mitigation** that runs on top of any of the others: [[agentic-harness-engineering]] (arXiv 2604.25850, April 2026) automatically *evolves* the harness via an observability-driven loop — component / experience / decision observability + a change manifest verified against next-round task-level deltas, with file-level rollback. Lifts Terminal-Bench 2 pass@1 from 69.7% (single-shell-tool seed) to 77.0% in ten iterations, beating both the human-designed Codex-CLI harness (71.9%) and self-evolving prompt-only baselines ACE (68.9%) and TF-GRPO (72.3%) using the same base model throughout. The frozen harness transfers across model families (+5.1 to +10.1 pp). **The component ablation is load-bearing for several wiki claims**: +memory only +5.6 pp, +tools only +3.3, +middleware only +2.2, **+system_prompt only −2.3 pp**. Prose-level strategy doesn't transfer; structural components carry the lift. Self-evolving-harness-via-observability-loop is plausibly a refinement of the explicit-handoff-artefacts class (the artefacts are now machine-discovered) or a new meta-class spanning all of the above.

A **policy-learned variant of the explicit-handoff-artefacts class** lands as [[skillos]] (arXiv 2605.06614, May 2026): frozen executor + RL-trained curator over an external Markdown SkillRepo. The curator emits `insert_skill` / `update_skill` / `delete_skill` calls; trained with GRPO over **grouped task streams** so that skill edits made during early trajectories are evaluated by their effect on later related tasks. +5.5 to +13.8 pp absolute SR on ALFWorld across executor scales (Qwen3-8B → Gemini-2.5-Pro), +7.1 pp cross-family transfer to Gemini-3.1-Flash-Lite. Headline architectural finding mirrors AHE's: the **8B-RL-trained curator beats Gemini-2.5-Pro-as-curator-without-RL** — executor-grounded training matters more than curator scale. Sits alongside [[effective-harnesses]] and [[langchain-deep-agents]] in the explicit-handoff-artefacts class but with the curation policy *learned* rather than prompt-driven.

A candidate **ninth class — high-resolution direct-substrate retrieval** — lands as [[direct-corpus-interaction]] (arXiv 2605.05242, May 2026): the agent searches the raw corpus via terminal tools (`grep` / `rg` / `head` / `cat`) instead of querying a vector index, moving semantic interpretation downward into the LLM at query time. Reduces context burden by fetching evidence on demand at high resolution; +11 pp accuracy and −29.4% cost on BrowseComp-Plus with matched Sonnet 4.6. Mechanism is **interface resolution** rather than recall — DCI surfaces fewer gold documents on average but localises within them more precisely (within-doc 48.4 vs 21.7). Operates at workspace / project scale; degrades sharply above ~200K docs. Distinct mitigation axis from compression / tiered memory: rather than compressing or tiering the context window, DCI keeps it lean by trusting the agent to fetch precisely what it needs from the substrate.

Two further additions from the week of 2026-05-04 enrich the long-horizon-context mitigation space without forming new top-level classes:

- **Progressive tool disclosure** (from [[notion-token-town]]): when the surface-area tool count crosses ~100, eager schema injection inflates per-turn cost (Notion: *"saying hello was thousands and thousands of tokens"*). Tool-search / progressive disclosure caps per-turn schema and is also the unlock that lets tool ownership be *distributed* across teams. Sibling to [[context-folding]] but at the *tool-schema* layer rather than the trajectory layer.
- **Manager-agent topology** (also Notion): empirical motivation — 30+ custom agents on one go-to-market team produced 70+ blocked-on-things notifications/day; a manager agent with invocation rights over the others reduces this to ~5 by triaging and unblocking. Practitioner data point on multi-agent coordination beyond the four classical topologies.

## Cross-cutting framings (not mitigation classes per se)

A separate axis from the long-horizon-context-loss mitigation work is **organisational blast radius**: governance, identity, audit, and policy across an enterprise's agent fleet. [[microsoft-agent-365]] (GA 2026-05-01) is the first vendor product to ship a *governance-and-identity substrate* — Entra identity per agent, Purview labels, Defender runtime policy, Intune device management, and (public preview) cross-cloud registry sync to AWS Bedrock + Google Cloud Gemini Enterprise. Architecturally analogous to how [[cognitive-fabric-nodes]] lifts memory out of agents into the substrate; here the substrate handles identity/policy/audit. Different problem from long-horizon context loss (organisational vs cognitive) but a peer architectural move (lift X out of the agent into shared infrastructure).

A separate framing from [[openai-symphony]] (Latent Space interview, May 2026) and [[notion-token-town]] is **code for agent legibility, not human readability**. Symphony writes *"10,000-engineer-level"* architecture (500 npm packages) for a 7-person team because each person operates ~10–50 agent instances and the marginal cost of agent-friendly decomposition is paid in tokens (cheap), not in human reading time. Notion's tool-naming-collision findings and 5-rebuild story are the same shape at the *interface representation* layer. This is plausibly a meta-mitigation that complements all of the above: design the substrate the agents are reading and writing for the agent's cognitive limits, not for the engineering team's habits. The [[externalization-survey]] (arXiv 2604.08224) provides a unifying vocabulary for the same observation under "harness as cognitive environment."

[[anthropic-claude-code-postmortem]] (April 23 2026) is a counterweight on the prompt-layer side of the same design space: a single brevity instruction added to the Claude Code system prompt (≤25 words / ≤100 words) caused a 3% intelligence drop on broader post-incident evals, and a thinking-block caching bug corrupted exactly the cross-session reasoning-history layer described in [[claude-code-session-memory]]. Selective context pruning at the API primitive level is harder to get right than mitigation papers typically suggest.

A separate framework-paper, [[mcp-multi-agent-framework]], proposes a four-layer reference architecture and six MCP server patterns at the application layer (downstream of [[mcp-infrastructure]]'s protocol roadmap); its empirical claims should be treated cautiously but its **four-manifestation typology of context retention failures** (boundary discontinuity, temporal discontinuity, prioritisation failure, cross-modal integration) is the sharpest naming available for what specifically goes wrong.

The cost-depth tradeoff above sets the ceiling: deeper hierarchical decomposition recovers some context at exponential token cost, so memory- and stage-discipline (not just more depth) is where the leverage lives. Three of the five mitigation classes (Codified Context, AgentFold, Skill Distillation) explicitly trade compute or architecture for context preservation rather than depth.

There is a live disagreement on whether *context files specifically* help: see [[../conflicts/agents-md-effectiveness]] for the resolution (codebase scale, documentation quality, and author all matter).

## Local/cloud hybrid: Windsurf + Devin

Cognition's Windsurf 2.0 integration with Devin canonizes the local-plan / cloud-execute split as a coding-agent product pattern. The local agent (Cascade) runs on the developer's machine with a ceiling bounded by attention; the cloud agent (Devin) operates asynchronously in its own infrastructure, opening PRs and running QA over minutes or hours. A one-click handoff sends a plan from Windsurf to Devin; review and touch-ups happen in the IDE as the orchestration surface. This topology is no longer left to users to wire manually — it ships as a primitive in the product.

- **Local agent (Cascade)** — runs on the user's machine; ceiling is the developer's attention.
- **Cloud agent (Devin)** — runs in its own infra; works for minutes-to-hours past the "async valley of death"; opens PRs, runs tests, QAs via computer vision.
- **Handoff** — one-click plan-to-Devin from Windsurf; PR review happens back in IDE; local agent can pick up touch-ups.
- **Why it's a topology variant, not just a product** — the local/cloud split defines agent lifetime and parallelism, not just UI; this post is the clearest primary-source articulation of that split yet.

Source: `raw/research/weekly-2026-04-22/01-windsurf-devin-local-cloud-topology.md` (Cognition blog, 2026-04).

## Source

- `raw/research/effective-agentic-patterns/08-arxiv-2601-12560-agentic-ai-taxonomy.md` — "Agentic Artificial Intelligence: Architectures, Taxonomies, and Evaluation of LLM Agents" (Arunkumar V, Anna University; Gangadharan G.R., NIT Tiruchirappalli; Rajkumar Buyya, University of Melbourne; arXiv 2601.12560, January 2026).
- `raw/research/effective-agentic-patterns/01-anthropic-building-effective-agents.md` — Anthropic engineering blog.

## Related

- [[building-effective-agents]]
- [[reasoning-frameworks]]
- [[failure-modes]]
- [[framework-skepticism]]
- [[ai-scientist-v2]] — tree-search multi-agent variant surfaced the same week; stage-manager + node-tuple pattern is the wiki's clearest long-horizon-context mitigation
- [[swe-bench-pro]] — empirical degradation curve with patch scale and unfamiliar-codebase penalty
- [[anthropic-internal-study]] — cold-start problem and paradox-of-supervision as practitioner-side framing
- [[mcp-infrastructure]] — async task lifecycle and context-bloat as infrastructure-level expression
- [[memory-architectures]] — taxonomy backbone (write-manage-read loop, five mechanism families)
- [[codified-context]], [[context-folding]], [[cognitive-fabric-nodes]], [[skill-distillation]], [[effective-harnesses]] — the five 2026 *context*-side mitigation classes
- [[cognition-cloud-agents]] — the *compute-and-state* mitigation class (VM isolation + hypervisor snapshotting); answers the async-gap rather than the context-window problem
- [[langchain-deep-agents]] — OSS generalization of the explicit-handoff pattern into a four-component library
- [[anthropic-claude-code-postmortem]] — counterweight on prompt-layer fragility; selective context pruning failure mode in production
- [[shopify-simgym]] — embarrassingly-parallel correlated-traffic multi-agent topology variant; 2,000 cloud-browser bots
- [[mcp-multi-agent-framework]] — four-manifestation typology of context retention failures
- [[airs-bench]] — research-agent eval surfacing context overflow as primary failure mode
- [[agentic-harness-engineering]] — eighth mitigation class: machine-evolved harness via observability-driven loop (Terminal-Bench 2 69.7→77.0%; +memory only +5.6 pp, +system_prompt only −2.3 pp)
- [[skillos]] — policy-learned variant of explicit-handoff-artefacts: RL-trained Markdown-skill curator (+5.5 to +13.8 pp ALFWorld)
- [[direct-corpus-interaction]] — candidate ninth mitigation class: high-resolution direct-substrate retrieval (BrowseComp-Plus +11 pp at −29.4% cost)
- [[agent-development-lifecycle]] — process-lens framing of Build → Test → Deploy → Monitor across all topology choices
- [[sierra-monitor-eval-of-evals]] — human-supervised observability loop, peer to AHE's machine-driven self-evolving variant
- [[microsoft-agent-365]] — governance-and-identity substrate as a separate axis from long-horizon context loss (organisational blast radius)
- [[openai-symphony]] — multi-Codex orchestration; "code for agent legibility, not human readability" framing
- [[notion-token-town]] — progressive tool disclosure + manager-agent topology + 5-rebuild data point on representation-fit
- [[externalization-survey]] — unifying vocabulary (memory + skills + protocols + harness as cognitive environment)
- [[alphaevolve-impact]] — single-agent + evaluator at vendor scale; positive data point for high-Metric-Freedom = single-agent
