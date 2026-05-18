---
setup_approved: true
last_reviewed: 2026-05-18
---

# Watchlist

Surplus candidates from weekly radar sweeps that didn't make the capture cap but are worth revisiting if signal hardens. Each `/weekly-brief` run appends up to 10 entries; old entries age out as they get captured, get retired for lack of signal, or the author prunes.

---

## Week of 2026-05-18

Surplus from this week's sweep — the 5 captured items are recorded in `wiki/log.md` (Anthropic context-engineering, SWE-Cycle 2605.13139, Memory-Evolution Survey 2605.06716, GroupMemBench 2605.14498, SDAR 2605.15155). Items below are strong-fit but did not make the cap: the SWE-* benchmark cluster is over-represented this week (one captured as the cluster anchor), the skills cluster is largely already in the wiki, and the rest are single-signal or product/conference posts.

### Coding-agent evaluation
- **SWE-Atlas — Benchmarking Coding Agents Beyond Issue Resolution (Scale AI, arXiv 2605.08366)** — https://arxiv.org/abs/2605.08366 — Three-task suite (Codebase Q&A, Test Writing, Refactoring); open code + HF dataset; institutional weight. Strongest of the watchlisted SWE-* set; capture if it becomes the de-facto beyond-issue-resolution standard or a leaderboard forms.
- **SWE-Chain — Chained Release-Level Package Upgrades (arXiv 2605.14415)** — https://arxiv.org/abs/2605.14415 — 12 upgrade chains, 155 version transitions, 1,660 grounded requirements; long-horizon maintenance regime not covered by SWE-Cycle. Capture if cited as a distinct long-horizon-maintenance signal.
- **SWE-WebDevBench — Coding-Agent Platforms as Virtual Software Agencies (arXiv 2605.04637)** — https://arxiv.org/abs/2605.04637 — 68-metric framework for vibe-coding/full-stack-generation platforms. Pairs with willison-vibe-agentic-convergence; capture if the vibe-coding-eval theme recurs.
- **Workspace-Bench 1.0 — Agents on Workspace Tasks with File Dependencies (arXiv 2605.03596)** — https://arxiv.org/abs/2605.03596 — File-dependency-heavy office/workspace tasks; bridges repo-level and real workflows. Single-signal; flag if it gains traction.

### Skills / self-evolving agents
- **A Comprehensive Survey on Agent Skills (arXiv 2605.07358)** — https://arxiv.org/abs/2605.07358 — Consolidating survey defining skills as reusable procedural artifacts; would anchor the agent-skills/skillos/skill-distillation cluster. Capture if it becomes the canonical skills-survey citation (lower novelty than this week's captures).
- **Swarm Skills — Portable Self-Evolving Multi-Agent System Spec (arXiv 2605.10052)** — https://arxiv.org/abs/2605.10052 — Extends the Anthropic Skills standard with multi-agent semantics; relevant to agent-skills + topology-taxonomy. Capture if multi-agent skill specs gain adoption.
- **Skill1 — Unified Evolution of Skill-Augmented Agents via RL (arXiv 2605.06130)** *(carry-forward from 2026-05-11)* — https://arxiv.org/abs/2605.06130 — RL unified skill evolution; now part of the SkillOS/SDAR cluster. The comprehensive skills survey is the partial "comparison piece" trigger; capture Skill1 + survey together if a head-to-head against SkillOS/SDAR lands.

### Multi-agent / topology
- **Constraint Drift in LLM-Based Multi-Agent Systems (arXiv 2605.10481)** — https://arxiv.org/abs/2605.10481 — Names/formalizes safety-constraint erosion across long multi-agent trajectories; strong fit for topology-taxonomy long-horizon-loss + governance threads. Capture if a second source corroborates the failure mode.
- **Predictive Maps of Multi-Agent Reasoning — Successor-Representation Spectrum for Communication Topologies (arXiv 2605.11453)** — https://arxiv.org/abs/2605.11453 — Diagnostic for choosing chain/star/mesh before inference; directly extends topology-taxonomy. Capture if topology-selection-as-method recurs.

### Frameworks / product
- **LangChain Interrupt 2026 + Deep Agents v0.6** — https://www.langchain.com/blog/deep-agents-0-6 — Delta channels (≈100× checkpoint-storage reduction), typed streaming, open-weight harness profiles (Kimi/Qwen/DeepSeek). Concrete shipped harness mechanics; changelog-grade. Capture if a full architecture writeup explains the delta-channel design.

## Week of 2026-05-11

Surplus from this week's sweep — the 5 captured items are recorded in `wiki/log.md` (LangChain ADL 2026-05-09, Sierra Monitor 2026-05-07, AlphaEvolve impact 2026-05-07, SkillOS arXiv 2605.06614, Beyond Semantic Similarity arXiv 2605.05242). Items below either lacked a strong-enough single signal to make the cap, ride a thread already represented in this week's captures, or are vendor-partnership announcements without primary technical writeup.

- **Skill1 — Unified Evolution of Skill-Augmented Agents via RL (arXiv 2605.06130)** — https://arxiv.org/abs/2605.06130 — #2 alphaXiv trending (33 reactions); 97.5% on ALFWorld. Pairs with [[patterns/skillos]] as a twin self-evolving-skills entry; would extend [[patterns/skill-distillation]] cluster on the RL axis. Capture next week if a comparison piece against SkillOS lands or if a Skill1 + SkillOS unification paper appears.
- **LangChain — "Agent Observability Needs Feedback to Power Learning"** — https://www.langchain.com/blog/agent-observability-needs-feedback-to-power-learning — Same week as the captured ADL post. Argues traces+feedback are training signal, not just logs. Captured indirectly via the ADL Monitor section; flag for next week if it gets cited as a load-bearing prior.
- **TWIML 767 — "How to Find the Agent Failures Your Evals Miss" (Scott Clark, 2026-05-07)** — https://twimlai.com/podcast/twimlai/how-find-agent-failures-your-evals-miss — Production-observability framing for agent evals (telemetry → monitoring → online analytics). Names the offline-eval-vs-production-failure gap. Strong wiki-fit but podcast capture is comparatively expensive; flag for next week.
- **Cursor changelog: PR Review parallel agents (2026-05-07) + Context Usage Breakdown (2026-05-06)** — https://cursor.com/changelog/05-07-26 / https://cursor.com/changelog/05-06-26 — Concrete shipped features; parallel-agent topology + per-source context accounting (rules / skills / MCPs / subagents). Lower priority because changelog rather than full writeup; flag if a Cursor blog post explains the architecture.
- **VibeServe — Can AI Agents Build Bespoke LLM Serving Systems? (arXiv 2605.06068)** — https://arxiv.org/abs/2605.06068 — Outer-loop/inner-loop agent that designs custom vLLM-style serving stacks. First data point on agentic-engineering-on-infrastructure-code; complement to [[deployments/openai-symphony]]. Capture if the agentic-on-infra theme recurs.
- **PARNESS — Paper Harness for End-to-End Automated Scientific Research (arXiv 2605.05258)** — https://arxiv.org/abs/2605.05258 — Direct PaperOrchestra/AI-Scientist peer with DAG scheduler + four-field Agent contract + cross-run knowledge accumulation. Capture next week if it shows up in a comparison-of-paper-harnesses thread or extends [[paperorchestra]].
- **DTap — DecodingTrust-Agent Platform (arXiv 2605.04808)** — https://arxiv.org/abs/2605.04808 — Stanford / Bo Li / Percy Liang. 14 domains + 50+ simulated apps (Workspace, Slack, Paypal); first comprehensive agent red-team substrate. Wiki currently has zero observability-eval-substrate coverage; capture if a security-vertical thread opens.
- **Workspace-Bench 1.0 (arXiv 2605.03596)** — https://arxiv.org/abs/2605.03596 — 20.4k files, 388 cross-file tasks, 7,399 rubrics; top agent 68.7% vs human 80.7%. Long-horizon cross-file eval, peer to [[airs-bench]] in the eval cluster. Capture if a SOTA leaderboard climb is tracked here.
- **AI Co-Mathematician (arXiv 2605.06651, DeepMind)** — https://arxiv.org/abs/2605.06651 — #3 alphaXiv (40 reactions); stateful agent workbench for mathematicians. Domain-vertical agent deployment (math research); peer to [[ai-scientist-v2]] / [[paperorchestra]] / [[deployments/alphaevolve-impact]]. Capture if a math-vertical agent thread opens.
- **Agent supply-chain security thread (Trustfall + Snyk-Anthropic + Opsera-Cursor)** — https://www.helpnetsecurity.com/2026/05/07/trustfall-ai-coding-cli-vulnerability-research/ + https://sdtimes.com/ai/may-8-2026-ai-updates-from-the-past-week-coder-agents-launch-snyk-claude-partnership-opsera-cursor-partnership-and-more/ — Three independent same-week signals on coding-agent supply-chain security moving from research to vendor partnerships. Watch for either a published vuln writeup with mechanism detail or a vendor primary post explaining the partnership architecture.

---

## Week of 2026-05-08

Surplus from this week's sweep — the 5 captured items are recorded in `wiki/log.md` (Cursor harness 2026-04-30, Sierra context engineering 2026-05-05, Willison convergence 2026-05-06, Anthropic finance agents 2026-05-05, arXiv 2604.18071 Architectural Design Decisions). Items below either lacked verified primary URLs or were lower-priority within this week's selection heuristic.

- **Holo3 (H Company) — OSWorld-Verified SOTA** — https://hcompany.ai/holo3 — Open-weight MoE (35B-A3B, Apache 2.0) reportedly took OSWorld-Verified at 82.6% Apr 29, overtaking Claude Mythos Preview. First open-weight model to lead the computer-use leaderboard. Capture if a primary writeup or H Company technical post drops.
- **AgentFlow — Synthesizing Multi-Agent Harnesses for Vulnerability Discovery (arXiv 2604.20801)** — https://arxiv.org/abs/2604.20801 — Typed graph DSL auto-synthesizes multi-agent harness topology + coordination for security tasks; 84.3% on TerminalBench-2 + 10 Chrome zero-days. Direct harness-engineering complement to AHE on the security-vertical axis.
- **Coordination as an Architectural Layer for LLM-Based Multi-Agent Systems (arXiv 2605.03310)** — https://arxiv.org/abs/2605.03310 — Empirical position paper: 41–87% of MAS production failures are coordination-driven, not model-driven. Proposes coordination as a separable architectural layer testable via prediction markets. Strong wiki-fit for topology-taxonomy if claims hold up under closer reading.
- **Terminus-4B (arXiv 2605.03195)** — https://arxiv.org/abs/2605.03195 — Microsoft post-trained 4B Qwen3 subagent for terminal execution; cuts main-agent token use 30% with no perf loss on SWE-bench Pro. Concrete data point for the skill-distillation / subagent-specialization thread.
- **HeavySkill — Heavy Thinking as the Inner Skill in Agentic Harness (arXiv 2605.02396)** — https://arxiv.org/abs/2605.02396 — Frames extended chain-of-thought as a learnable harness-internal skill via RL; outperforms best-of-N. Bridges agentic-harness-engineering and skill-distillation.
- **ARIS — Autonomous Research via Adversarial Multi-Agent Collaboration (arXiv 2605.03042)** — https://arxiv.org/abs/2605.03042 — Open-source research harness using adversarial cross-model review to prevent unsupported claims in long-running autonomous research loops. 92 HuggingFace upvotes. Adjacent to PaperOrchestra (already in wiki); may extend rather than displace.
- **Agent Capsules — Quality-Gated Granularity Control for Multi-Agent LLM Pipelines (arXiv 2605.00410)** — https://arxiv.org/abs/2605.00410 — Runtime system that intelligently merges/separates agent calls; 51% token reduction with quality gates, no training required. Practical harness-efficiency angle.
- **SWE-WebDevBench — Evaluating Coding Agent Platforms as Virtual Software Agencies (arXiv 2605.04637)** — https://arxiv.org/abs/2605.04637 — First multi-dimensional eval of vibe-coding platforms as full dev agencies (68 metrics across PM/eng/ops). All 6 platforms fail below 60% engineering quality and 65% security. Pairs with the convergence-of-vibe-and-agentic thread.
- ~~**AlphaEvolve — Scaling Impact Across Fields (DeepMind)** — https://deepmind.google/blog/alphaevolve-impact/~~ — Captured and ingested 2026-05-11 → [[deployments/alphaevolve-impact]]. URL verified live; year-in-production report for the Gemini-powered evolutionary coding agent (TPU silicon design, Spanner LSM compaction, Klarna 2× training, FM Logistic 10.4% routing, Schrödinger 4× MLFF). Vendor-stated quantitative claims; structural deployment claims credible.
- **Karpathy — Sequoia Ascent 2026 (Software 3.0 / Agentic Engineering)** — https://karpathy.bearblog.dev/sequoia-ascent-2026/ — Frames "Software 3.0" with context window as the primary programming lever; distinguishes vibe coding (raises floor) from agentic engineering (raises ceiling). Cross-referenced from the Willison post; capture if it becomes load-bearing.

---

## Week of 2026-05-04

Surplus from this week's sweep — the 5 captured items are recorded in `wiki/log.md` (AHE arXiv 2604.25850, Externalization Survey arXiv 2604.08224, Microsoft Agent 365 GA, Notion Token Town podcast, OpenAI Symphony podcast). Items below either lacked verified primary URLs or were lower-priority within this week's selection heuristic.

- **SGH — Structured Graph Harness (arXiv 2604.11378)** — https://arxiv.org/abs/2604.11378 — Hu Wei, April 13 2026. Lifts control flow from implicit context into an explicit static DAG; scheduler-theoretic framework for LLM agent execution. Three commitments: immutable plan-version execution; planning/execution/recovery layered separation; strict escalation protocol on recovery. Overlaps AHE on the harness/execution axis but addresses a different sub-question (control-flow representation vs harness-component evolution). Capture next week if a second source corroborates the DAG-vs-loop framing or it appears in topology-taxonomy discussions. Verified URL.
- **Together AI CoderForge-Preview** — Together AI's open-source test-verified coding-agent dataset; fine-tuned Qwen-3 32B from 23.0% to 59.4% pass@1 on SWE-Bench Verified. Open-source training-side data point on the model-improvement vs harness-improvement question. Lower wiki-fit (data/training, not architecture) but on-trend for the SLM-coding-agent thread. URL not directly verified this week.
- **DeepSeek V4-Flash** — 284B total / 13B active MoE, MIT-licensed, priced at Haiku-tier rates through DeepSeek API. Vendor model release. Worth tracking as a frontier-open model that AHE explicitly tested cross-family transfer on (+10.1 pp the largest cross-family gain).
- **Qwen3.6-27B agentic coding** (carries from 2026-04-27) — https://qwen.ai/blog?id=qwen3.6-27b — Still no primary deep-dive captured. AHE used qwen-3.6-plus in cross-family transfer table; would benefit from a primary source page if a 2026 deep-dive blog drops.
- **ROMA — Recursive Open Meta-Agent Framework** — long-horizon multi-agent decomposition into subtask trees that run in parallel. arXiv ID surfaced via VoltAgent's curated 2026 list but URL not directly verified this week. Worth verifying if the recursive-decomposition theme recurs.
- **RecursiveMAS** — recursive multi-agent in latent space (vs text); +20.2% accuracy claimed, 2.4x inference speedup vs text-based recursive multi-agent. arXiv ID not verified this week.
- **GLM-5V-Turbo** — multimodal foundation model integrating visual perception into agentic reasoning/planning/tool-use; vendor claims ~8x improvement on MMSearch-Plus; outperforms Claude Opus 4.6 on Design2Code. Vendor benchmark claim — collect-but-confirm per source-authority-weighting memory. Lower priority unless a multimodal-agent thread opens on the wiki.
- **Anthropic Skills format (markdown + scripts as agent skills)** (carries from 2026-04-27) — Externalization Survey explicitly cites "Anthropic's Introducing Agent Skills (Oct 2025)" as the canonical industrial implementation. Worth pulling the primary Anthropic post to a peer page next round; with the externalization-survey skills chapter now in the wiki, a primary Anthropic Skills post would close a load-bearing gap.
- **Notion engineering blog "5 Lessons from Building Custom Agents"** — referenced in the Notion Token Town podcast post footer; not yet captured. Would upgrade the [[case-studies/notion-token-town]] page from secondary (Latent Space) to primary-and-secondary. Capture when located.
- **OpenAI Frontier "harness engineering" essay + Symphony / "ghost library" spec** — referenced throughout the Symphony Latent Space episode; not yet captured. Would upgrade [[deployments/openai-symphony]] from secondary to primary-and-secondary. Capture when located.

---

## Week of 2026-04-27

Surplus from this week's sweep — the 5 captured items are recorded in `wiki/log.md`. Items below either lacked verified URLs (mostly arXiv 2604.* IDs that the trend scanners returned without my having directly confirmed) or were lower-priority within this week's selection heuristic.

- **OpenAI: "The next evolution of the Agents SDK" + AgentKit** — https://openai.com/index/the-next-evolution-of-the-agents-sdk/ + https://openai.com/index/introducing-agentkit/ — Vendor parallel to Anthropic Managed Agents and LangChain Deep Agents; visual builder + sandbox-aware orchestration. Surface for next week if a comparison-of-frameworks page becomes worth writing.
- **Factory AI Droid Computers** — https://factory.ai/news/droid-computers — Persistent per-Droid VMs (managed cloud or BYOM) with full filesystem/credential/memory snapshots. Direct Cognition cloud-agents counterpart. Capture next week if differentiation becomes clearer or a deployment case lands.
- **Cursor 3 with parallel agents window** — https://cursor.com/blog/cursor-3 — First major IDE to ship a dedicated multi-agent topology UI (worktrees, cloud, SSH). Lower priority because it's a UI change, but worth a topology-taxonomy entry if a teardown lands.
- **Vending-Bench 2 / Andon Labs** — https://andonlabs.com/blog/openai-gpt-5-5-vending-bench — Long-horizon autonomous-business benchmark; real deployments at Anthropic and xAI offices exposed social-engineering and hallucinated-identity failure modes. Strong wiki fit (peer to AIRS-Bench in long-horizon eval cluster). Capture next week if confirmed live.
- ~~**Notion "Last Exam" headroom evals + multi-harness rebuild** — https://www.latent.space/p/notion~~ — Captured and ingested 2026-05-04 → [[case-studies/notion-token-town]]. Three-tier eval taxonomy (regression / launch-quality / "Last Exam" headroom @ ~30% pass) documented; primary Notion engineering blog "5 Lessons from Building Custom Agents" still outstanding (re-flagged in the 2026-05-04 watchlist section).
- **arXiv 2604.02460 — Single-agent under equal token budget beats multi-agent** — https://arxiv.org/abs/2604.02460 — VentureBeat coverage + Reddit threads; information-theoretic argument via Data Processing Inequality across Qwen3, DeepSeek-R1, Gemini 2.5. Would extend [[skill-distillation]] cluster directly. arXiv ID surfaced by trend-scanner but not verified end-to-end this week.
- **arXiv 2604.21816 — Tool Attention / dynamic MCP gating** — https://arxiv.org/abs/2604.21816 — Quantifies MCP eager schema injection overhead (10k–60k tokens/turn) and demonstrates 95% reduction via selective gating. Code released. Direct extension of [[mcp-infrastructure]] context-bloat thread. Verify URL before next-week capture.
- **arXiv 2604.22748 — Agentic World Modeling: Foundations, Capabilities, Laws** — https://arxiv.org/abs/2604.22748 — HuggingFace trending; unified levels-and-laws taxonomy spanning RL, web agents, multi-agent sim, scientific discovery. May overlap [[topology-taxonomy]]; evaluate fit before capture.
- **Qwen3.6-27B agentic coding** — https://qwen.ai/blog?id=qwen3.6-27b — 27B dense model claimed to surpass prior 397B variants on agentic coding benchmarks; would shift the efficiency frontier for self-hosted coding agents. Lower priority unless it directly affects a benchmark page.
- **Anthropic Skills format (markdown + scripts as agent skills)** — flagged via Latent Space "AIE Europe Debrief"; potential canonical packaging format for skills. Watch for Anthropic primary post.

---

## Week of 2026-04-22

- ~~**AIRS-Bench (Meta)** — https://arxiv.org/abs/2602.06855~~ — Captured and ingested 2026-04-25 → [[evaluation/airs-bench]].
- ~~**Cognitive Fabric Nodes — smart multi-agent middleware** — https://arxiv.org/abs/2604.03430~~ — Captured and ingested 2026-04-25 → [[deployments/cognitive-fabric-nodes]].
- ~~**From Multi-Agent to Single-Agent: Skill Distillation** — https://arxiv.org/abs/2604.01608~~ — Captured and ingested 2026-04-25 → [[patterns/skill-distillation]]. F predictor turns out to be load-bearing; r=-0.85 with skill-distillation lift.
- ~~**Advancing Multi-Agent Systems via MCP** — https://arxiv.org/html/2504.21030v1~~ — Captured and ingested 2026-04-25 → [[patterns/mcp-multi-agent-framework]]. Empirical section flagged as low-credibility; vocabulary kept (four-manifestation typology of context retention failures).
- ~~**PaperOrchestra (Google)** — https://www.marktechpost.com/2026/04/08/google-ai-research-introduces-paperorchestra~~ — Captured and ingested 2026-04-25 → [[coding-agents/paperorchestra]]. Secondary source only; primary Google paper not yet captured.
- **Claude Mythos Preview (security-focused model)** — https://red.anthropic.com/2026/mythos-preview/ — Anthropic's security-specialized model; Project Glasswing for critical software. Low wiki-fit (product news) but watch for agentic-security-testing framing.
- **Devin new self-serve pricing plans** — https://cognition.ai/blog/new-self-serve-plans-for-devin — Product news, but free-tier removal + Ask-Devin charging signals Cognition's commercial pivot. Monitor for production-deployment case studies.
- ~~**Simon Willison: "The cognitive cost of coding agents"** — https://simonwillison.net/2026/Apr/3/cognitive-cost/~~ — The /Apr/3/ page is a thin podcast-clip meta-post; the substance lives in the **/Apr/2/lennys-podcast/** highlights post (245 lines of curated quotes with timestamps) and the Lenny's Newsletter post. Captured both 2026-04-26 → [[case-studies/willison-cognitive-cost]]. YouTube transcript fetch failed (yt-dlp format error); raw audio not captured. Note: PaperOrchestra primary paper (arXiv 2604.05018) also captured 2026-04-26 to upgrade [[coding-agents/paperorchestra]] from secondary source.
- **Latent Space / Moonlake — interactive multimodal world models** — https://www.latent.space/p/ainews-top-local-models-list-april — Symbolic reasoning + action-conditioned simulation for long-horizon planning; out of scope for current wiki unless a planning mechanism paper surfaces.
- **SWE-rebench** — https://swe-rebench.com — Alternative contamination-resistant coding benchmark; less visibility than SWE-bench Pro this week, worth checking next sweep.

---

## Related

- [[reference-sources]] — the upstream radar these candidates came from.
- [[log]] — weekly-brief run history with trend-synthesis bullets.
