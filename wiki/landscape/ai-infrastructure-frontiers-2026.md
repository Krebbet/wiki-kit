# AI Infrastructure Frontiers 2026

Bessemer Venture Partners' 2026 thesis declares the centre of gravity in AI infrastructure has shifted from training-time engines of intelligence (models, compute, training data) to the **"nervous system"** that lets AI sense, remember, adapt, and operate in the real world — structured as five frontiers: harness infrastructure, continual learning, RL platforms, inference-at-scale, and world models.

> **Source disclosure:** Bessemer Venture Partners is a VC firm actively investing in this category. The company selection is not independent. Bessemer states that "certain companies mentioned may be current or former portfolio companies" but does not disclose which, per-company. Treat all BVP infra roadmap picks as interested framing, not neutral analysis. See [[open-questions-2026-04]] for tracked conflicts.

## 1. "Harness" infrastructure

**Category:** tooling that wraps models in a compound system — memory / context management, evaluation, observability — so a deployed agent stays grounded, doesn't quietly drift, and behaves reliably in production (BVP 2026).

**What's novel:**
- Plug-and-play semantic memory layers that replace hand-rolled RAG — cross-session context, user preferences, long-term memory.
- Conversational-failure-aware observability: real-time production monitoring against golden datasets, LLM-as-a-judge, semantic metrics (not just latency / error codes / thumbs).
- BVP names a failure taxonomy: **"confidence trap", "drift", "silent mismatch"**.

**Named companies:**

| Company | Technique | Notes |
|---|---|---|
| Bigspin.ai | Pre-deployment testing + real-time production monitoring vs golden datasets | — |
| Braintrust | Semantic metrics / LLM-as-a-judge evals | Already in [[ai-app-categories-2025]] infra list |
| Judgment Labs | Evals / LLM-as-a-judge | Already in [[ai-app-categories-2025]] infra list |

**Claim to fact-check:** BVP cites an arXiv paper claiming **"78% of AI failures are invisible"** and that these patterns **"persist across 93% of cases even with more powerful models"**, with arXiv ID `2603.15423`. The ID format is suspect (arXiv IDs use YYMM prefix, so `2603` would imply March 2026 — plausible, but the number-suffix format should be verified before this claim moves into any advisory deck). See [[open-questions-2026-04]] C12.

## 2. Continual learning systems

**Category:** systems that let a deployed model keep learning after training — accumulating knowledge and skills across tasks without catastrophic forgetting, replacing the "frozen weights + growing KV cache" model (BVP 2026).

**What's novel:**
- Architectural moonshots rethinking transformers for learning-at-inference.
- Test-time training via sliding-window transformers that compress context into weights.
- **Cartridges** — long context pre-trained into small KV caches once, reused across inference requests.
- New governance primitives needed: rollback to stable weight checkpoints, full lineage tracking of weights / data / hyperparameters, isolation for safe experimentation.

**Named companies and research:**

| Company / Research | Technique |
|---|---|
| **Learning Machine** | New architecture + training paradigm for inference-time learning; "meta skill of how to learn." Pre-product per source. |
| **Core Automation** | Rethinking transformer attention so memory emerges naturally. |
| Stanford + NVIDIA TTT-E2E | Sliding-window transformer (research, not a company); cited arXiv `2512.23675` (Dec 2025). |
| Cartridges methodology | Stanford "scaling intelligence" lab (research). |
| **Sublinear Systems** | Racing on context limitations (no further detail in source). |

**Open question flagged by BVP:** which point on the spectrum (moonshot architecture vs incremental transformer patches) wins is undetermined. New benchmarks are needed beyond needle-in-haystack to measure continual-learning vs in-context learning. See [[open-questions-2026-04]] C14 *(to be added)*.

## 3. Reinforcement learning platforms

**Category:** tooling stack for teaching agents through interaction — environments, RL-as-a-service, and platform infrastructure — needed because static human-labeled datasets cannot teach multi-step autonomous decisioning with delayed consequences (BVP 2026).

**What's novel (per BVP):**
- Framed as the **successor to human-labelling vendors**. BVP contrasts "first wave" (data labelling) with "next wave" (interaction-based learning).
- Three-layer stack asserted: (a) environment building and experience curation, (b) RL-as-a-service, (c) platform infrastructure.

**Named — but with a capture gap:** the source names three prior-wave data-platform vendors — **Mercor**, **Turing**, **micro1** — and positions them as insufficient for the next wave. Per-layer company names for the RL-platform stack itself **appear to be truncated in the captured source** (the layer bullets are present but no companies are listed under them). See reader notes below.

**Framing tension:** BVP's explicit "first wave / next wave" language implies Mercor / Turing / micro1 are being superseded. This runs ahead of publicly-available evidence. Tracked as [[open-questions-2026-04]] C15 *(to be added)*.

## 4. Inference inflection point

**Category:** production-grade inference optimisation — serving, routing, caching, scheduling, and edge / on-device deployment — now rivaling training in compute demand and economic importance as agents move from prototype to production (BVP 2026).

**Date-stamped claim:** Jensen Huang at **GTC 2026 keynote** — "the inflection point of inference has arrived" (NVIDIA Vera Rubin / Groq-3 LPX cited as current-generation hardware).

**What's novel:**

| Technique | Named company | Notes |
|---|---|---|
| KV-cache reuse / recomputation elimination | **TensorMesh** (via LMCache) | Multi-turn / agentic workloads where same context processed repeatedly. |
| SGLang-based routing / scheduling for multi-turn conversations | **RadixArk** | — |
| vLLM performance boundary-pushing for high-throughput serving | **Inferact** | — |
| Heterogeneous inference purpose-built for agentic systems | **Gimlet Labs**; NVIDIA Groq-3 LPX for Vera Rubin | — |
| Edge / on-device AI (consumer, robotics, physical AI, defence) | WebAI, FemtoAI, PolarGrid, Aizip Mirai, OpenInfer, Perceptron | — |
| Defence edge AI (denied-comms environments) | TurbineOne, Dominion Dynamics, Picogrid, Breaker | — |

**Prior-roadmap pioneers (2024, positioned as already-won / commoditised by BVP):** **Fal, Together, Baseten, Fireworks** — all already listed in [[ai-app-categories-2025]] infra section without a "next-wave" annotation. BVP's framing implicitly claims this 2024 cohort has either "won" or been commoditised — see [[open-questions-2026-04]] C11 for tracked framing tension.

**YC W26 overlap**: [[runanywhere]] (on-device inference, claimed fastest on Apple Silicon) fits the edge / on-device cluster; not a BVP 2026 pick but directionally consistent.

**Update 2026-05-03 — agentic-web-search-as-API tier emerges as a sibling category, not in BVP's roadmap.** Parallel Web Systems (Sequoia $100M Series B / $2B post-money, 2026-04-29; Parag Agrawal, ex-Twitter CEO) sells web-search and research APIs purpose-built for AI-agent consumption, with named anchor customers Harvey, Notion, Clay, Opendoor + undisclosed banks / hedge funds and >100k developers. See [[../startups/parallel-web-systems|parallel-web-systems]]. This is a distinct infra-tier from inference / harness / training-data: it sits between agent harnesses (Cursor, Claude Code) and the public web. Competitors include Tavily, Exa, Linkup, Brave Search API. BVP's 2026 roadmap omits the category — first-tier-validation gap. Track for additional rounds in this space over Q3 2026.

**Update 2026-05-10 — agent governance / control-plane consolidation around seat-based-SKU vendors.** BVP's harness-frontier framing (above) named Bigspin / Braintrust / Judgment Labs as 2026 picks. The shipping reality this week: governance / control-plane is consolidating around vendors with **existing seat-based monetisation**, bundled at near-zero marginal cost to the buyer:

- **Microsoft Agent 365 GA (2026-05-01)** — bundled in M365 E7 or USD 15/user/month standalone. Discovers / observes / governs agents across Microsoft + non-Microsoft estates (AWS Bedrock + Google Cloud registry sync in preview). See [[../platforms/microsoft|microsoft]].
- **Salesforce Agent Fabric** (2026-04-15 launch; covered in [[../platforms/salesforce|salesforce]]) — multi-vendor agent control plane bundled into Agentforce.
- **Google GEAP Agent Gateway + Agent Identity + Registry** (2026-04-22; see [[google-cloud-next-2026-day2]]) — bundled in GEAP.
- **ServiceNow AI Control Tower** (Knowledge 2026, 2026-05-05; not separately captured) — agent kill switches + 30 new cloud integrations + Traceloop acquisition for runtime observability.

The pattern: governance + observability ships as a **bundled feature** of the existing platform, not a separate startup purchase. **Pure-play harness/eval startups** (Bigspin, Braintrust, Judgment Labs, Traceloop pre-acquisition) face a structural pricing and distribution disadvantage against the bundled-into-existing-SKU pattern. BVP's harness-frontier picks may be **acquihire-targets rather than standalone-revenue plays** through 2026-2027 — Traceloop's ServiceNow acquisition (2026-05-05) is the first concrete data point in this direction.

Adjacent signal: **MCP isolation** is now load-bearing inside the governance bundle — see [[mcp-rce-supply-chain-2026-05]] for why Model Armor / Agent Fabric / Agent 365 Defender controls / Cortex sandboxing now have a dual-purpose framing (governance AND CVE-inheritance defence). Pure-play harness vendors without an MCP-isolation story face an uphill differentiation battle.

## 5. World models

**Category:** AI systems trained on real-world sensor / video / GPS data that simulate how the world evolves given a state and action — a substrate for physical-AI intelligence analogous to what LLMs are for text reasoning (BVP 2026).

**Three architectural paradigms (with hybrids emerging):**

| Paradigm | Technique | Named companies | Trade-offs |
|---|---|---|---|
| Video-based | Frame the problem as video generation, step-by-step in pixel space | Reka, Decart | Real-time interactive; physical-consistency weak over long horizons |
| Explicit 3D representation | Persistent 3D scene representations | World Labs | High spatial coherence, low inference cost; currently pre-generated / static (real-time on roadmap) |
| Latent predictive (JEPA) | Forecast future states in compressed latent space | AMI Labs | Compute-efficient, no pixel generation, reduced interpretability |

**Production users in AV:** Waymo, Wayve — simulating rare edge cases.

**Open question flagged by BVP:** which paradigm (or hybrid) dominates is undetermined. Whether world models extend cleanly beyond robotics / AVs into defence, healthcare, industrial ops, enterprise planning is asserted but unproven. See [[open-questions-2026-04]] C16 *(to be added)*.

## Cross-cuts worth flagging *(editorial)*

- **Companies in-frame** across BVP's five frontiers and prior wiki pages: Fireworks / Baseten / Together / Fal (in [[ai-app-categories-2025]]; BVP re-cites as 2024 pioneers); Braintrust / Judgment Labs (already in [[ai-app-categories-2025]]; BVP confirms the harness cluster).
- **New names not previously captured**: TensorMesh, RadixArk, Inferact, Gimlet Labs, Bigspin.ai, Learning Machine, Core Automation, Sublinear Systems, World Labs, Reka, Decart, AMI Labs; edge / defence cohort (WebAI, FemtoAI, PolarGrid, Aizip Mirai, OpenInfer, Perceptron, TurbineOne, Dominion Dynamics, Picogrid, Breaker).
- **Apps-vs-infra divergence** (cross-ref [[ai-apps-layer-2026]]): BVP is explicitly an infra-side thesis where a16z's is apps-side. Both frame the app layer as thriving; they disagree implicitly on where the durable moats sit (apps-layer feature surface vs harness + inference + world-model platforms).

## Reader notes

- **Capture gap**: the RL-platforms section (#3 above) appears structurally truncated in the captured source — layer names present but company-per-layer bullets missing. A targeted re-capture of `bvp.com/atlas/ai-infrastructure-roadmap-five-frontiers-for-2026` with `--js` or a browser-saved version is worth doing before this page is used for client advisory.
- BVP's portfolio-disclosure is generic; do not attribute portfolio status to any specific 2026 name without independent confirmation.
- Most individual companies here do not merit their own pages yet — queued as watchlist. Add pages as second sources (customer case studies, practitioner posts, independent benchmarks) arrive.

## Source

- `raw/research/emerging-agentic-startups-2026/06-bessemer-infra-roadmap.md`
- `raw/research/weekly-2026-05-03/03-parallel-web-systems-series-b.md`
- `raw/research/weekly-2026-05-10/03-microsoft-agent-365-ga.md` (Microsoft Security Blog, 2026-05-01 — agent control-plane consolidation)
- `raw/research/weekly-2026-05-10/04-mcp-rce-vulnerability.md` (The Hacker News citing OX Security, 2026-05-08 — MCP isolation as governance layer)

## Related

- [[ai-app-categories-2025]]
- [[enterprise-ai-market-2025-2026]]
- [[llm-api-enterprise-share]]
- [[ai-apps-layer-2026]]
- [[yc-w26-ai-batch]]
- [[runanywhere]]
- [[../startups/parallel-web-systems|parallel-web-systems]]
- [[../platforms/microsoft|microsoft]] (agent governance bundling)
- [[mcp-rce-supply-chain-2026-05]]
- [[open-questions-2026-04]]
