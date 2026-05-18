# Wiki Log

Append-only chronological record of wiki activity.

---

## [2026-05-18] weekly-brief ingest | weekly radar sweep (5 captured, 10 watchlisted)

Autonomous `/weekly-brief` radar sweep for week of 2026-05-18. 5 primary sources captured to `raw/research/weekly-2026-05-18/` (marker on CPU + capture_url; audit clean, 0 issues; 5/5 subagent summaries schema-valid). SkillOS (arXiv 2605.06614) was excluded — already covered by `patterns/skillos`.

Sources:
- **anthropic-context-engineering** (Anthropic Engineering blog, primary vendor) — context engineering vs prompt engineering; attention-budget / "context rot"; JIT-retrieval + compaction + structured-note-taking triad (hybrid-retrieval caveat).
- **swe-cycle** (arXiv 2605.13139) — complete issue-resolution-cycle benchmark (Env/Impl/TestGen/FullCycle), 489 instances (~203 from SWE-bench Pro), reported FullCycle ~<14%; contamination challenge to SWE-bench Verified/Pro.
- **memory-evolution-survey** (arXiv 2605.06716) — Storage→Reflection→Experience evolutionary taxonomy; orthogonal to memory-architectures' five-family taxonomy; Experience tier as a new frontier.
- **GroupMemBench** (arXiv 2605.14498, UCSB + Microsoft) — first multi-party memory benchmark; BM25 ~43.2% Pareto-dominates four of five extraction-based systems; best system ~46%; Mem0 ~4.67% Knowledge Update collapse.
- **SDAR** (arXiv 2605.15155) — on-policy self-distillation + token-level sigmoid gating for multi-turn agents; privileged context at training only, internalized into weights; reported ~+9.4% ALFWorld / ~+10.2% WebShop over GRPO; code + models released.

**New pages:** `patterns/anthropic-context-engineering`, `evaluation/swe-cycle`, `conflicts/swe-bench-contamination` (OPEN), `memory/memory-evolution-survey`, `memory/groupmembench`, `patterns/sdar`

**Extended pages:** `conflicts/verbatim-vs-extracted-memory` (2026-05-18 data-points: GroupMemBench + survey abstraction-depth axis), `patterns/context-engineering`, `patterns/sierra-context-engineering`, `patterns/effective-harnesses`, `patterns/direct-corpus-interaction`, `evaluation/swe-bench-pro`, `patterns/agentic-harness-engineering`, `deployments/openai-symphony`, `patterns/harness-design-space`, `memory/memory-architectures`, `memory/longmemeval`, `memory/mem0`, `memory/memgpt`, `memory/mempalace`, `patterns/skill-distillation`, `patterns/skillos`, `patterns/externalization-survey`, `memory/reflexion`

**Key synthesis:** (1) Coding-agent eval frontier moved past "fix a GitHub issue" — SWE-Cycle (+ watchlisted SWE-Atlas/SWE-Chain/SWE-WebDevBench) target the whole lifecycle; SWE-Cycle also opens a new contamination conflict against SWE-bench Pro. (2) GroupMemBench is the first matched-corpus empirical evidence for the verbatim/no-extraction pole of the open verbatim-vs-extracted conflict (BM25 strictly Pareto-dominates four extraction pipelines, load-bearing for Positions 1/3); the memory-evolution survey adds an abstraction-depth framing axis and an Experience tier above the existing memory cluster. (3) Self-improvement converging on RL-trained-curation / distillation-over-frozen-executor — SDAR joins SkillOS/skill-distillation. (4) Context engineering canonized by a primary vendor (Anthropic), peer to the existing sierra-context-engineering page.

**Conflict ruling (standing autonomy):** opened `conflicts/swe-bench-contamination` (SWE-Cycle vs SWE-bench Pro — genuine contradiction, no prior open conflict on the theme). Did NOT open a new memory conflict — survey/GroupMemBench tensions were folded into the already-OPEN `conflicts/verbatim-vs-extracted-memory` per the conflict protocol.

---

## [2026-04-22] weekly-brief | agentic-trends radar sweep (week of 2026-04-22)

Captured 5 sources, ingested via 5 parallel subagents, wrote 4 new pages + 1 extension + a fresh watchlist.

**Trends (synthesis):**
- Benchmark saturation forcing a split — SWE-bench Verified near-ceiling, Pro emerging as honest signal (56.8% top vs 87.6% Verified).
- Coding agents entering the IDE — Windsurf 2.0 + Devin canonizes local-plan / cloud-execute split.
- Autonomous science agents crossing a threshold — AI Scientist-v2 first peer-review-accepted AI-generated paper; AIRS-Bench benchmark surfaces.
- "Engineers as architects" going internal-empirical — Anthropic 132-engineer study ships alongside Opus 4.7.
- MCP ecosystem velocity — 2026 roadmap tackles auth/context-bloat/governance; protocol-to-infrastructure transition.

**Sources captured** (in `raw/research/weekly-2026-04-22/`):
- 01-swe-bench-pro — https://labs.scale.com/leaderboard/swe_bench_pro_public
- 01-windsurf-devin-local-cloud-topology — https://cognition.ai/blog/devin-in-windsurf
- 02-mcp-infrastructure-maturity — https://thenewstack.io/model-context-protocol-roadmap-2026/
- 03-anthropic-engineering-transformation — https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic
- 04-ai-scientist-v2 — https://arxiv.org/abs/2504.08066

Pages: see revisions.md row for 2026-04-22. First-time dry run of /weekly-brief for this wiki.

---

## [2026-04-25] research | long-horizon context & agent memory architectures

User question on long-running agentic tasks and methods to maintain larger project context surfaced a wiki gap. First an in-conversation synthesis added a "Long-horizon context loss" section to topology-taxonomy with cross-refs to existing pages. Then a /research run captured 5 new sources via parallel subagent dispatch and ingest:

- **Codified Context** (arXiv 2602.20478) — three-tier hot/cold memory infrastructure case study at 108k C# lines.
- **Memory for Autonomous LLM Agents** (arXiv 2603.07670) — survey: write-manage-read loop, three-axis taxonomy, five mechanism families, four benchmarks exposing recall-vs-use gap.
- **Evaluating AGENTS.md** (arXiv 2602.11988) — AGENTbench: LLM-generated context files hurt success rate, inflate cost; developer-written context marginal.
- **AgentFold** (ICLR 2026 Poster, OpenReview IuZoTgsUws) — proactive variable-granularity context folding; 30B model beats 671B baselines on BrowseComp.
- **Cognitive Fabric Nodes** (arXiv 2604.03430) — middleware that lifts memory into the network substrate; addresses survey's multi-agent memory governance open challenge.

Wrote 5 new pages (1 evaluation, 3 patterns, 1 deployments) + 1 conflict-resolution page (Codified Context vs AGENTS.md eval, reconciled on codebase-scale / documentation-quality / author axes). Extended topology-taxonomy "Long-horizon context loss" section with explicit *Diagnosis / Vocabulary / Mitigation classes* structure mapping all new pages into the patterns hub. Retired Cognitive Fabric from watchlist.

**Synthesis trends:**
- Memory architecture is becoming a first-class engineering concern — survey claims memory choice rivals or exceeds model-scaling for performance variance.
- Two distinct mitigation classes are converging: in-context compression (AgentFold) and tiered external memory (Codified Context, MemGPT lineage); both materialise state structurally rather than relying on raw history.
- Infrastructure layer is splitting into protocol (MCP) vs middleware (CFN), addressing different sides of multi-agent coordination.
- Empirical signal warning: vendor-recommended context-file practice often hurts in well-documented mid-sized repos; the headline AGENTS.md eval result is a useful corrective.

---

## [2026-04-25] research (round 2) | watchlist alternates + structural corrections

User directives following round 1 review:
1. **Keep the AGENTS.md conflict OPEN** — round 1 had labelled it "Resolution"; restructured `wiki/conflicts/agents-md-effectiveness.md` so disagreement is primary, method differences are explicit, and reconciling axes are clearly tentative.
2. **Memory deserves its own subdir** — moved `wiki/patterns/memory-architectures.md` → `wiki/memory/memory-architectures.md`; fixed two `[[../patterns/memory-architectures]]` explicit-path refs in case-studies and coding-agents pages.
3. **Pull in the watchlist alternates** — captured 5: Skill Distillation (arXiv 2604.01608), MCP Multi-Agent framework (arXiv 2504.21030), PaperOrchestra (Google, via marktechpost secondary source), AIRS-Bench (FAIR Meta, arXiv 2602.06855), Simon Willison cognitive-cost page. Willison page turned out to be a thin meta-post about a 48-second podcast clip rather than a substantive essay — retired as not usable.
4. **Memory correction (kit-level)** — round 1 used `--engine pymupdf` for AgentFold PDF, dropping image binaries — same mistake as 2026-04-22 weekly-brief. Strengthened the auto-memory rule to be unambiguous; added master_notes.md kit entry recommending removal of the "simple PDFs / skip model download" carve-outs in `.claude/commands/research.md` and a `tools/capture_pdf` warning when `--engine pymupdf` is invoked. Re-captured AgentFold via `CUDA_VISIBLE_DEVICES="" marker`.

4 new wiki pages from round 2: `patterns/mcp-multi-agent-framework`, `coding-agents/paperorchestra`, `evaluation/airs-bench`, `patterns/skill-distillation`. Plus restructure of the conflict page, the memory move, cross-refs into existing `context-engineering.md` and `agentic-context-engineering.md` (which were already in the wiki and overlap with memory-architectures coverage).

**New synthesis trend:**
- The five-class mitigation taxonomy in `topology-taxonomy#long-horizon-context-loss` is now: materialise state in topology, adaptive in-context compression, tiered hot/cold memory, lift memory into substrate, **eliminate the handoff entirely**. The fifth (Skill Distillation) is the one architectural counter-class — others remediate within MAS; this one collapses the design when Metric Freedom (F) predicts a single agent can do the job. F is the branch condition.
- Empirical sources splitting on credibility: AGENTS.md eval (rigorous benchmark, robust ablations) and Skill Distillation (theorem + r=-0.85 fit) anchor a confident pole; MCP Multi-Agent framework anchors the cautioned pole (clean numbers, generic baselines, in-text-vs-bibliography author mismatch). Wiki pages should be increasingly explicit about this credibility axis.

---

## [2026-04-26] research (round 3) | follow-up captures + primary-source upgrade

User directives following round 2 review:
1. **Pull PaperOrchestra primary paper.** arXiv 2604.05018 (Yiwen Song, Yale Song, Tomas Pfister, Jinsung Yoon — Google) captured via marker on CPU. Rewrote `wiki/coding-agents/paperorchestra.md` with primary-source detail. Key corrections to the secondary-source version: affiliation is "Google" (not "Google Cloud AI Research"); previously conflated automated-SxS (88–99% lit-review margin vs AI Scientist-v2) with human-eval (50–68% lit-review margin) numbers — now separated; added Gemini-3.1-Pro backbone + Gemini-3-Flash search + GPT-5 evaluator-only details; added P0/P1 citation taxonomy explanation; added Levenshtein 70%+ threshold and ≥90% citation-utilisation constraint; added baselines-excluded-with-reasons section; added ScholarPeer co-authorship overlap as methodology caveat (3 of 4 PaperOrchestra authors also co-author ScholarPeer, the simulated-acceptance evaluator).
2. **Try the Lenny's Podcast capture.** Three sources attempted: Lenny's newsletter post (show notes only), Willison's own highlights post on his blog (245 lines of curated quotes with timestamps — primary), YouTube transcript (failed: yt-dlp format error for video wc8FBhQtdsA). The Willison highlights post turned out to be a *better* source than a raw transcript would have been because Willison did the curation — selected quotes are exactly the high-value passages. Created `wiki/case-studies/willison-cognitive-cost.md` as a peer to `anthropic-internal-study` — the embodied first-person account of the productivity uplift + paradox of supervision the Anthropic 132-engineer study only captured aggregately.

**New synthesis trend (round 3):**
- Quantitative case studies (Anthropic 132 engineers) and first-person practitioner accounts (Willison) are converging on the same finding from different methodological angles: productivity uplift is real but **supervision cost rises proportionally** and is the actual bottleneck for further deployment. The wiki now has both genres explicitly cross-linked. Worth tracking whether more first-person practitioner accounts (Karpathy, Cherny, etc.) accumulate enough to warrant a `practitioner-perspectives/` subdir.
- Willison's "97% effectiveness is a failing grade" observation is the cleanest framing in the wiki for why benchmark scores in the 80s–90s on AIRS-Bench / SWE-bench Pro do not equate to production readiness — the gap between "almost works" and "works" is non-linear in operational stakes.

---

## [2026-04-27] weekly-brief | agentic-trends radar sweep (week of 2026-04-27)

Captured 5 primary-source items, ingested via 5 parallel subagents, wrote 5 new pages + extended 1 cluster page (topology-taxonomy) + extended 1 conflict page (agents-md-effectiveness) + appended a fresh watchlist section.

**Trends (synthesis):**
- **Managed-agent infrastructure has become a product category in its own right.** Cognition (microVM + hypervisor snapshotting), Anthropic (initializer + coding-agent harness), LangChain (`deepagents` OSS library), and OpenAI/Factory (vendor-specific managed-agent / Droid-Computers offerings on the watchlist) all shipped frontier-or-OSS positions on the same pattern within ~3 weeks. The pattern has stabilised on four components — system prompt, planning surface, sub-agents/sessions, file system — across all four vendors, with the differences now in *persistence substrate* (LangGraph state vs disk + git vs hypervisor snapshot vs vendor-managed VM).
- **The long-horizon-context-loss synthesis bifurcates.** Until this week the wiki had 5 *context-side* mitigation classes (materialise in topology, in-context compression, tiered hot/cold, lift to substrate, eliminate-handoff). This week adds: a 6th context-side class (*explicit handoff artefacts*, Anthropic's harness post + LangChain Deep Agents) and a 7th *compute-and-state-side* class (Cognition's async-gap framing — VM isolation + hypervisor snapshotting). Topology-taxonomy now distinguishes "context continuity" from "compute/state continuity" as orthogonal axes.
- **Agent-based simulation as a third evaluation paradigm.** SimGym uses 2,000 concurrent shopper bots in cloud browsers as a *substitute for live A/B testing*. This is distinct from offline benchmarks ([[airs-bench]], [[swe-bench-pro]]) and live-traffic measurement; it's agents-as-eval-substrate. Disclosed inference-economics detail (B200 vs H200 5.2× speedup, MIG-vs-EAGLE-3 mutual exclusion, prompt-cache prefix restructuring) is rare in agent literature.
- **Prompt-layer fragility is back on the agenda.** Anthropic's postmortem reports a 3% intelligence drop from a single brevity instruction added to the Claude Code system prompt — locally tested before rollout, only revealed by a broader post-incident eval. Pairs against [[codified-context]]'s 660-line constitution: scaling structured context positively does not imply that *any* prompt-layer addition is safe.
- **Anthropic's "effective harnesses" wishlist item is now in the wiki.** Master_notes round-4 flagged it as the highest-signal Anthropic-authored source on long-running-agent harnesses still uncaptured. Now `[[patterns/effective-harnesses]]`. Bumps the round-4 entry to closed.
- *(synthesis)* Anthropic's postmortem + Cognition's "phase 2" framing + the existing Anthropic-internal-study + Willison weeknotes are now four converging vantage points on the same finding: **internal dogfooding diverges from production traffic, and customer-side reports surface what internal evals miss.** Not a single page yet; flag for next-week's case-studies/ cluster review.

**Sources captured** (in `raw/research/weekly-2026-04-27/`):
- 01-01-anthropic-claude-code-postmortem — https://www.anthropic.com/engineering/april-23-postmortem
- 02-02-cognition-cloud-agents — https://cognition.ai/blog/what-we-learned-building-cloud-agents
- 03-03-anthropic-effective-harnesses — https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- 03-04-shopify-simgym — https://shopify.engineering/simgym
- 04-05-langchain-deep-agents — https://www.langchain.com/blog/deep-agents

5 new pages: case-studies/anthropic-claude-code-postmortem, deployments/cognition-cloud-agents, patterns/effective-harnesses, deployments/shopify-simgym, coding-agents/langchain-deep-agents. topology-taxonomy extended with 6th + 7th mitigation classes and 4 new related-pages. conflicts/agents-md-effectiveness extended with two new data points (long-running-regime + prompt-layer-fragility).

Selected primary-source URLs only this week (no arXiv captures); the trend scanners returned several plausible-looking arXiv IDs in the 2604.xxxxx range that I did not verify, so they went to the watchlist instead. Next week consider verifying watchlist arXiv items via direct arXiv URL hit before pulling.

---

## [2026-04-27] research | mempalace + longmemeval + verbatim-vs-extracted conflict

User followed up the prior /query (which had reported the wiki had no "memory palace" content) with a /research run on github.com/MemPalace/mempalace, asking specifically for "supporting methods." Auto mode active.

**Source-authority finding (logged inline before capture):** the named repo turns out to be a real but anomalous viral 2026 launch — 22 days old at capture, 49,995 stars, 6,560 forks, with a prominent in-README scam alert about an `mempalace.tech` impostor distributing malware. Treated as a contested practitioner source (peer to [[case-studies/willison-cognitive-cost]] in the "primary-source-but-not-academic" tier), not as a foundational paper. Captures restricted to the three URLs the project itself lists as official; mempalace.tech, mempalace.net, and mempalace.github.io deliberately skipped.

**Sources captured** (in `raw/research/mempalace/`):
- 01-readme through 06-claude-md — GitHub repo files via `gh api` (README, MISSION, ROADMAP, docs/CLOSETS, docs/HISTORY, CLAUDE.md). Direct `gh api` was used instead of capture_url because trafilatura on rendered GitHub blob HTML is lossier than fetching raw markdown via the API; provenance frontmatter was written manually for each.
- 07-concepts-the-palace — https://mempalaceofficial.com/concepts/the-palace.html (official concepts page).
- 08-rhodes-review — https://nicholasrhodes.substack.com/p/mempalace-ai-memory-review-benchmarks (critical practitioner review; author has a competing product, Mirror Memory).
- 09-vectorize-review — https://vectorize.io/articles/mempalace-review (critical vendor review; Vectorize ships Hindsight). Both reviewers ship competing products, but their factual claims independently corroborate the maintainers' own HISTORY.md retractions.
- 10-hn-thread — https://news.ycombinator.com/item?id=47672792 (community discussion).
- 11-longmemeval-paper — https://arxiv.org/pdf/2410.10813 (Wu et al., ICLR 2025) via marker on CPU.
- (Cybernews: capture_url timed out at 30s waiting for networkidle; mainstream coverage already corroborated via HN + reviewer citations of Forbes/Kotaku — skipped.)

**Pages written:**
- `wiki/memory/mempalace.md` — primary page, framed around the gap between launch claims and reproducible behaviour. Centers the maintainers' own April 7 + April 14 retractions as the canonical position, then layers in independent-reviewer findings (palace features regress retrieval; AAAK is lossy; README features missing from code; 96.6% headline measures ChromaDB defaults). Source caveat block leads.
- `wiki/memory/longmemeval.md` — academic supporting-method page: 5 abilities, 3-stage framework (indexing/retrieval/reading), 4 control points (value/key/query/reading), 4 recommended designs (round-granularity values, fact-augmented key expansion, time-aware query expansion, Chain-of-Note + structured reading). The paper's hybrid recommendation (verbatim values + extracted-fact keys) is the third position in the new conflict.
- `wiki/conflicts/verbatim-vs-extracted-memory.md` — OPEN conflict between MemPalace's "never summarize" doctrine and Mem0's "extract + consolidate" doctrine. Reconciling axes (corpus scale, query type, trust budget, metric) marked tentative; no empirical bridge yet at matched corpus scale + matched metric.

**Pages extended:**
- `wiki/memory/memory-architectures.md` — added MemPalace as 2026 instance in *retrieval-augmented memory stores* family with the verbatim-vs-extraction note; added LongMemEval to the evaluation roster (joins LoCoMo, MemBench, MemoryAgentBench, MemoryArena); added new "Benchmarks with their own pages" sub-section.
- `wiki/index.md` — three new entries (mempalace, longmemeval, conflicts/verbatim-vs-extracted-memory).

**Synthesis trends (round-specific):**
- *(synthesis)* The wiki now has its first **contested viral practitioner project** in the memory/ subdir — a peer-source genre to [[case-studies/willison-cognitive-cost]] but graded against an academic benchmark with a candid maintainer-corrections trail. Worth tracking whether more 2026 viral memory libraries follow the same pattern (extraordinary launch claims → community audit within 48h → public retractions); the pattern itself may deserve a case-studies/ entry if it recurs.
- *(synthesis)* The verbatim-vs-extracted split is the cleanest design-doctrine disagreement currently in the wiki's memory cluster. The LongMemEval paper's hybrid recommendation (extracted keys + verbatim values) gives a non-trivial third position that neither production library fully implements; this is an empirical gap worth flagging for any future research/benchmark ingest.
- The architecture-vs-benchmarked gap on MemPalace (intended hybrid via closets+drawers; benchmarked path uses raw drawers only) is structurally similar to the [[conflicts/agents-md-effectiveness]] pattern (claimed-context-improves-things vs measured-effect-on-rigorous-eval). Both belong to a meta-pattern: novel-architecture features that don't survive contact with a clean benchmark.

**Process learnings (logged inline):**
- For GitHub-hosted markdown sources, `gh api` is materially better than `capture_url`: deterministic, no trafilatura HTML-to-markdown round-trip, provenance is unambiguous (the repo path + commit SHA from the API response). Worth promoting to a kit-level helper (master_notes entry to follow).
- The "research scope" question for viral / contested sources is upstream of the existing "scope/emphasis" auto-mode rule: when source authority is the question, even auto mode should pause to surface the authority concerns before writing pages, then proceed with appropriately-labelled output. Did that here by writing a "Source caveat" block first and centring the maintainers' own retractions.

---

## [2026-04-26] research (round 4) | memory management deep-dive

User asked for foundational + latest + real-systems coverage on memory management, naming Claude Code as the real-systems example. Captured 8 sources via parallel marker (CPU) + capture_url:

- 4 PDFs (foundational + production paper):
  - **MemGPT** (arXiv 2310.08560) — Packer et al. UC Berkeley; LLM-as-OS framing.
  - **Reflexion** (arXiv 2303.11366, NeurIPS 2023) — Shinn et al.; verbal RL.
  - **Generative Agents** (arXiv 2304.03442, UIST 2023) — Park et al.; the canonical recency × importance × relevance scoring formula.
  - **Mem0** (arXiv 2504.19413) — Chhikara et al.; production library with LOCOMO benchmarks.
- 4 web (production library + real systems):
  - **Letta memory blocks** — letta.com/blog primary source.
  - **Anthropic Memory Tool docs** — docs.claude.com primary source for the API primitive.
  - **Claude Code Session Memory** — claudefa.st community blog (Anthropic's official Claude Code memory docs are sparse).
  - **Anthropic memory_cookbook notebook** — captured but skipped (207KB GitHub HTML view of an .ipynb dominated by base64 outputs; not usable as source).

7 new wiki/memory/ pages (one per usable source). The wiki/memory/ subdir is now justified at 8 pages (memory-architectures + 7 new). The memory-architectures survey was extended in-place to enumerate explicit instances per mechanism family — turning the abstract taxonomy into a navigable tree.

**Foundational papers ↔ family taxonomy mapping** (now explicit on the survey page):
- *Hierarchical virtual context*: memgpt → letta-memory-blocks → anthropic-memory-tool → codified-context (foundation → runtime → vendor primitive → application instance).
- *Reflective and self-improving memory*: reflexion + generative-agents (the two foundational papers); ACE in 2025 extends the pattern.
- *Retrieval-augmented memory stores*: mem0 is the production realisation of generative-agents-style scoring with conflict resolution.
- *Context-resident compression*: context-folding (AgentFold) at the algorithm level + claude-code-session-memory at the product layer.

**New synthesis trend (round 4):**
- The wiki now has a complete *foundational → production-library → vendor-primitive → product-feature → application-pattern* stack documented for memory management. Practitioners can navigate from "I want to add memory to my agent" through any of three production libraries (Letta, Mem0, OpenAI memory) or two vendor primitives (Anthropic Memory Tool, Claude Code Session Memory) back to the foundational papers that justify each design choice.
- The MEMORY PROTOCOL Anthropic ships in the auto-injected system prompt ("ASSUME INTERRUPTION") is the first piece of evidence in the wiki of a vendor productising the *cold-start problem* (named by anthropic-internal-study) as a default behaviour. The cold-start problem is no longer just empirical observation — it has a vendor-shipped operational mitigation.
- Anthropic's three-layer official answer to long-horizon context loss is now legible: **memory tool** (cross-session persistence) + **context editing** (client-side pruning) + **compaction** (server-side summarisation). Compaction is the server-side peer to AgentFold's per-step folding.
- Worth pulling next round: Anthropic's "Effective harnesses for long-running agents" engineering blog (referenced by the Memory Tool docs as the authoritative case study, with initializer script, progress file structure, and git-based recovery details). Logged in master_notes.

---

## [2026-05-04] weekly-brief | harness engineering crystallizes as a discipline

Autonomous Monday weekly sweep. 5 captures, 5 wiki pages, 6 extensions, 0 new conflict files.

**Captures** (in `raw/research/weekly-2026-05-04/`):
- 01-microsoft-agent-365 — Microsoft Security Blog GA announcement (2026-05-01) via capture_url.
- 02-notion-token-town — Latent Space podcast post (Sarah Sachs + Simon Last) via capture_url; 123KB / 1520 lines, dense practitioner narrative.
- 03-openai-symphony — Latent Space podcast post (Ryan Lopopolo, OpenAI Frontier) via capture_url; 91KB / 1274 lines.
- 04-agentic-harness-engineering — arXiv 2604.25850 PDF via marker on CPU; 911 lines.
- 05-externalization-survey — arXiv 2604.08224 PDF via marker on CPU; 1038 lines.

Audit clean (no broken refs, no thin captures, no image collisions).

**Pages written:**
- `wiki/patterns/agentic-harness-engineering.md` — primary-source paper page; centres the three observability pillars (component / experience / decision), the headline 69.7→77.0% Terminal-Bench 2 result, and the load-bearing component ablation (+memory only +5.6 pp; +tools +3.3; +middleware +2.2; **+system_prompt only −2.3 pp**). Cross-family transfer +5.1 to +10.1 pp. Self-attribution-blind-to-regressions caveat surfaced.
- `wiki/patterns/externalization-survey.md` — cross-cutting vocabulary anchor for the 22-author Zhou et al. survey. Memory + skills + protocols + harness as four externalizations along a single weights → context → harness arc. Names AHE-style "self-evolving harnesses" (§8.3) and "shared infrastructure" (§8.5) as emerging directions. Survey-style caveats (no original empirical evaluation; theoretical interpretations flagged; SJTU-heavy bibliography).
- `wiki/deployments/microsoft-agent-365.md` — vendor product GA primary-source page. Lead caveat: "architectural and SKU claims are vendor product spec; risk-reduction claims are vendor marketing." Load-bearing novelty: cross-cloud registry sync to AWS Bedrock + GCP Gemini Enterprise (public preview). MCP-server inventory as a first-class governance object (June 2026 Defender preview).
- `wiki/case-studies/notion-token-town.md` — practitioner case study peer to willison-cognitive-cost. 4-5 harness rebuilds reconstructed in chronological detail. Doctrine, MCP-vs-CLIs four-axis framing, three-tier evals, MBE role, manager-agent topology, primitive-composition memory ("memory is just pages and databases"), pricing-as-credits. Secondary-source caveat (Latent Space podcast post; Notion engineering blog "5 Lessons" referenced but not yet captured).
- `wiki/deployments/openai-symphony.md` — extreme-scale deployment-tier case study. Symphony = Elixir-based multi-Codex orchestrator; `rework` state; "ghost library" spec-driven distribution; 1-minute build-loop; six skills + agents.md TOC + session-log distillation; "code for agent legibility" thesis; on-policy vs off-policy harness heuristic. Secondary-source caveat (Latent Space podcast post; OpenAI Frontier essay + Symphony spec referenced but not captured); explicit greenfield-only scope caveat from Lopopolo.

**Pages extended:**
- `wiki/patterns/topology-taxonomy.md` — eighth mitigation class (self-evolving harness via observability loop, AHE) + two minor additions (progressive tool disclosure, manager-agent topology, both from Notion) + new "Cross-cutting framings" section adding (a) governance-and-identity substrate as a separate axis from long-horizon context loss (Microsoft Agent 365) and (b) "code for agent legibility, not human readability" framing (Symphony + Notion + Externalization survey).
- `wiki/patterns/effective-harnesses.md` — new "Machine-evolved counterpart and multi-rebuild data points" section pulling AHE (machine counterpart, citing this post directly), Symphony (extreme-scale; rework state; session-log distillation; 1-minute build-loop; on-policy heuristic), and Notion (multi-rebuild + 17-day-thread-with-100-compactions anecdote).
- `wiki/conflicts/agents-md-effectiveness.md` — new "New data points (week of 2026-05-04)" section. Three positions added: AHE as a fourth distinct frame (machine-evolved, multi-component, +system_prompt only −2.3 pp); Symphony as positive corroboration of agent-authored / continuously-distilled regime; Notion proposes representation-fit-to-model-priors as a *newly surfaced (untested) reconciling axis*. Conflict remains OPEN; combined characterisation of "when context infrastructure works" sharpened.
- `wiki/deployments/mcp-infrastructure.md` — two new sections: "Vendor response: Microsoft Agent 365 (GA 2026-05-01)" (concrete operationalisation of the deferred enterprise-readiness items; MCP-server-inventory as governance object) + "Practitioner MCP-vs-CLIs framing (Notion + OpenAI Frontier, 2026)" (first practitioner-economics data point on the page; per-turn token cost outside cache window; Lopopolo's auto-compaction-interference quote).
- `wiki/memory/memory-architectures.md` — new "Externalization framing (Zhou et al. 2026)" section pointing to the survey + two new memory-adjacent instances (AHE's `LongTermMEMORY.md`; Notion's "memory is just pages and databases" primitive-composition).
- `wiki/patterns/skill-distillation.md` — Related-section additions (Symphony as production instance; Notion manager-agent as adjacent F-question; Externalization survey skills chapter; AHE evidence-driven attribution parallel).

**Synthesis trends (this week's email bullets):**
- *(synthesis)* **Harness engineering crystallizes as a discipline.** Convergent across this week's five captures: AHE names it as a primary research target; the Externalization Survey gives it a §6 chapter (six dimensions); Symphony coins / popularises the term in industry; Notion operationalises it through 4-5 rebuilds; AHE specifically calls out three concurrent harness-engineering primary sources — Codex-CLI, Anthropic's effective-harnesses (already in the wiki), LangChain's Deep Agents (already in the wiki) — as the prior art it builds on. Last week's "managed-agent infrastructure as a product category" framing has now been complemented by a discipline-level naming.
- *(synthesis)* **Multi-cloud agent-governance becomes a product tier.** Microsoft Agent 365 ships first-day registry sync to AWS Bedrock + GCP Gemini Enterprise. The MCP-2026-roadmap "enterprise readiness" gap (audit trails, SSO, gateway, cross-vendor governance) has its first vendor product response.
- *(synthesis)* **"Build for what the model already understands" emerges as a doctrinal axis.** Notion's Token Town: 5 rebuilds, the throughline being to "strip away internal system complexity and cater to what the model already understands." Sharpens the open `conflicts/agents-md-effectiveness` axis with a third position that says the load-bearing variable is *representation fit to model priors* — not human-vs-LLM authorship.
- *(synthesis)* **Self-evolving harness ≠ self-evolving model.** AHE freezes the LLM, evolves the scaffold, and shows the resulting harness transfers across model families with +5-10pp cross-family gains. Symphony likewise treats the model as fixed and engineers the surround. Trend: don't fine-tune the model, evolve the scaffolding.
- *(synthesis)* **Prose-level prompt edits keep losing to structural edits.** AHE's component ablation (+memory only +5.6 pp; **+system_prompt only −2.3 pp**) is now the second independent 2026 data point that prose-level instructions are the most fragile harness layer — pairs with `anthropic-claude-code-postmortem` Bug 3 (3% intelligence drop from a single brevity instruction). Two independent observations from independent methodologies.

**Process learnings (logged inline):**
- Background `Bash run_in_background` invocations don't inherit the user's interactive PATH, so `poetry` was not found in the first capture attempt. The surface bug is that `poetry` isn't on the default `PATH` in non-login shells; the workaround is the explicit `/home/david/.local/bin/poetry` invocation. Master_notes-worthy fix: capture scripts should detect this and either fail fast with a clear "poetry not on PATH" message or auto-resolve via `which poetry || $HOME/.local/bin/poetry`. Logging.
- The `tools.ingest_plan.aggregate` page-shape parser missed "**New page: ...**" formatted entries (matches `New page: ` only, not `**New page: **`). All four subagents this week wrapped the line in `**...**`. Page-plan output was incomplete; recovered manually from the summaries. Master_notes-worthy fix: extend the parser to tolerate bold/italic markdown around the directive lines, OR document the exact required format more visibly in the subagent prompt.

---

## [2026-05-08] weekly-brief | practitioner-side harness engineering goes mainstream

Captured 5 sources, ingested via 5 parallel subagents, wrote 5 new pages + watchlist update. Off-cycle run (Friday rather than Monday) after merging the SMTP-send kit fix from `origin/main` into the wiki branch — first run with actual outbound email instead of Gmail draft.

**Trends (synthesis):**
- *(synthesis)* **Harness engineering goes practitioner-primary.** Cursor + Sierra ship first-party writeups in the same week, alongside Anthropic's first vertical Managed Agents release (finance) and a 70-project empirical survey (arXiv 2604.18071). 2026-05-04's "harness engineering crystallizes as a discipline" thesis now has primary-source corroboration from three vendors plus an academic taxonomy.
- *(synthesis)* **Empirical reality bounds vendor framing.** arXiv 2604.18071 (corpus frozen 2026-03-23, 70 OSS projects) finds 14.3% MCP-first vs 34.3% registry-oriented and 40% with no audit capability. The wiki's `mcp-infrastructure` characterizes MCP as already infrastructure; this paper bounds that as roadmap-not-deployed-reality. Reconciling axis: vendor intent vs corpus state.
- The vibe-coding / agentic-engineering distinction is collapsing in practice. Willison's May 6 post documents his own drift toward no-review for well-scoped agent tasks — practitioner-side counterpoint to the supervised-delegation posture in `effective-harnesses` and `anthropic-internal-study`. Quality-signal shift: artefact richness (tests, docs) → evidence of sustained use.
- Connector vs MCP-app emerges as a new integration tier. Anthropic's finance launch distinguishes connectors (governed data access) from MCP apps (provider tools embedded in Claude). Moody's example. Not yet captured in `mcp-infrastructure`; flagged for next ingest.

**Sources captured** (in `raw/research/weekly-2026-05-08/`):
- 01-cursor-agent-harness — https://cursor.com/blog/continually-improving-agent-harness
- 02-sierra-context-engineering — https://sierra.ai/blog/context-engineering-the-key-to-great-agents
- 03-willison-vibe-agentic-convergence — https://simonwillison.net/2026/May/6/vibe-coding-and-agentic-engineering/
- 04-anthropic-finance-agents — https://www.anthropic.com/news/finance-agents
- 05-architectural-design-decisions-agent-harnesses — https://arxiv.org/abs/2604.18071

5 new pages: case-studies/cursor-agent-harness, patterns/sierra-context-engineering, case-studies/willison-vibe-agentic-convergence, deployments/anthropic-finance-agents, patterns/harness-design-space. No new conflict files opened (thresholds favoured folding into existing). Audit clean (0 issues).

**Process learnings (logged inline):**
- `tools.capture_pdf` failed on `https://arxiv.org/abs/<id>` with `No module named 'weasyprint'` — the abs-page-to-PDF conversion path requires weasyprint. Workaround: use `https://arxiv.org/pdf/<id>` (direct PDF URL) which bypasses HTML-to-PDF entirely. Kit-level fix: either install weasyprint as a dep or document the direct-PDF preference in the capture-tool docstrings + spec.

---

## [2026-05-11] weekly-brief | production observability + self-evolving skills + direct corpus interaction

Autonomous Monday weekly sweep. 5 captures, 5 new wiki pages, 11 extensions, 1 conflict-page extension (3rd pole on verbatim-vs-extracted-memory).

**Trends (synthesis):**
- *(synthesis)* **Production agent observability crystallises as a vendor discipline.** Same week: LangChain "The Agent Development Lifecycle" (Build → Test → Deploy → Monitor framing); LangChain "Agent Observability Needs Feedback to Power Learning" (traces+feedback as training signal); Sierra "Who monitors the monitors?" (eval-of-evals calibration); TWIML 767 with Scott Clark on agent-eval-failures-in-production. Three vendors + one practitioner podcast in one week — the discipline-level naming has settled on "monitor / observe / evaluate" as the post-deployment counterpart to last month's "harness engineering."
- *(synthesis)* **Self-evolving skills as RL-trained curation.** SkillOS (#1 alphaXiv) + Skill1 (#2 alphaXiv) both shipped same week with the same architectural pattern: frozen executor + RL-trained external structure (Markdown skills in SkillOS; per-task skill program in Skill1). SkillOS's headline architectural finding — **8B-RL-trained curator beats Gemini-2.5-Pro-as-curator-without-RL** — is the per-skill version of AHE's "structural components carry the lift over model scale." 2026 is converging on *evolve the scaffold, freeze the LLM* as the dominant self-evolving paradigm.
- *(synthesis)* **Direct corpus interaction gives the practitioner CLI-skepticism a published mechanism.** "Beyond Semantic Similarity" (arXiv 2605.05242, top HF this week) argues retrieval should be `grep`/`bash`-mediated traversal of the raw corpus rather than vector-index top-k. +11 pp at −29.4% cost on BrowseComp-Plus with matched Sonnet 4.6; the gain is **interface resolution** (within-doc localisation 48.4 vs 21.7), not recall. Notion's "vector embeddings are less and less" finding from `case-studies/notion-token-town` and Lopopolo's MCP-skepticism in `deployments/openai-symphony` now have an academic counterpart on the same axis. Opens a third pole in `conflicts/verbatim-vs-extracted-memory`: not just verbatim-vs-extracted, but **with-index-or-without** at all.
- **Coding-agent supply-chain security goes vendor.** Three independent signals in one week: Trustfall AI coding-CLI vulnerability disclosure (one keypress compromises 4 tools); Snyk + Anthropic Claude AI Security partnership; Opsera + Cursor enterprise DevSecOps partnership. Direction-of-travel: agent-security tooling shifting from research to vendor product surface. Watchlist-only this run.
- **AlphaEvolve URL-verified.** The 2026-05-08 watchlist entry's verify-URL caveat closed; AlphaEvolve impact post is now `deployments/alphaevolve-impact`. DeepMind's 1-year-in-production retrospective lands as a peer to OpenAI Symphony / Cognition cloud-agents on the zero-human-code production-deployment axis at radically different scale (vendor-deployed in TPU/Spanner/compiler vs 7-person greenfield).

**Sources captured** (in `raw/research/weekly-2026-05-11/`):
- 01-langchain-agent-lifecycle — https://www.langchain.com/blog/the-agent-development-lifecycle
- 02-sierra-monitor-the-monitors — https://sierra.ai/blog/agent-monitoring
- 03-alphaevolve-impact — https://deepmind.google/blog/alphaevolve-impact/
- 04-skillos — arXiv 2605.06614 (PDF via marker on CPU)
- 05-beyond-semantic-similarity — arXiv 2605.05242 (PDF via marker on CPU)

5 new pages: patterns/agent-development-lifecycle, patterns/sierra-monitor-eval-of-evals, deployments/alphaevolve-impact, patterns/skillos, patterns/direct-corpus-interaction. 11 extensions across topology-taxonomy, memory-architectures, externalization-survey, agentic-harness-engineering, effective-harnesses, sierra-context-engineering, mcp-infrastructure, openai-symphony, notion-token-town, cursor-agent-harness; 1 conflict extension (verbatim-vs-extracted-memory now three-poled). Audit clean (0 issues).

**Process learnings (logged inline):**
- The `/weekly-brief` skill's step-5 ingest-subagent prompt template doesn't include the `parse_summary`-required frontmatter (`schema_version: 1`) or the exact required section names (`One-line` / `Cross-ref candidates` / `Conflict flags` / `Proposed page shape`). All five subagent summaries this week were structurally fine but failed `parse_summary` validation — recovered by reading the summaries directly in the orchestrator. Master_notes-worthy fix: extend the step-5 template in `.claude/commands/weekly-brief.md` to embed the exact schema (frontmatter + section names) so subagents emit parseable summaries by default. Logging.
- `poetry install --no-root` from `Bash run_in_background` stalled with no output for several minutes. Direct `pip install <dep>` into the poetry venv worked instantly. Possibly poetry-lockfile contention from two concurrent invocations earlier in the run. Worth double-checking next sweep before relying on poetry-install in unattended cron.

## 2026-05-14 — query: memory-systems reading list

Query asked for a curated reading list weighting different agentic memory systems by utility/benefits. Traversed [[memory-architectures]] → all 7 memory/* pages → [[conflicts/verbatim-vs-extracted-memory]] → [[patterns/direct-corpus-interaction]]. Synthesised a stage-by-stage reading path (survey → foundational 2023 → 2025-26 productionised → live conflicts) plus a per-system "when this wins" picker table.

Wiki update: extended [[memory-architectures]] with a "Reading path for newcomers" section containing the four-paper minimum on-ramp and the use-case → recommended-system picker table. The factual content was already on each page; the gap was a learning-sequence entry point in one place. No new pages.

## 2026-05-15 ingest | Agentic skills & personalities (research sweep)

Topic: best practices for creating agentic skills & personalities (Claude Code + general). 7 sources captured to raw/research/agentic-skills-personalities/, audit clean (0 issues), 7/7 subagent summaries schema-valid.

Sources: 4 Anthropic Skills primary (01 engineering blog, 02 best-practices docs, 03 Claude Code docs [lossy scrape — facts reliable, prose not quoted], 04 Complete Guide PDF [pymupdf; quantitative figures vendor-self-described aspirational → collect-but-confirm]); 2 empirical persona papers (05 Zheng arXiv 2311.10054 null result; 06 Hu/PRISM arXiv 2603.18507 task-type decomposition + gated-LoRA routing); 07 The New Stack practitioner tutorial.

2 new pages: patterns/agent-skills (consolidates 01+02+03+04 — same conceptual ground at varying depth; one hub beats four thin pages; dedicated Claude Code mechanics section), patterns/agent-personas (05+06+07; practitioner advice bracketed against empirical evidence with an authority-stratified what-works/what-doesn't table). conflicts/agents-md-effectiveness extended with a 2026-05-15 data-points section (Skills = favorable-regime preconditions / progressive disclosure as reconciling lever; persona evidence = system-prompt-layer fragility corroboration). 4 reciprocal xrefs (skillos, externalization-survey, skill-distillation, anthropic-finance-agents). Filled the two named coverage gaps (persona/personality design; Claude Code skill-authoring mechanics).

Conflict ruling (made under standing autonomy): did NOT open conflicts/persona-effectiveness — Hu et al. explicitly reconciles the Zheng null as a task-type aggregation artefact; no genuine impasse to elevate, documented as resolved-tension on the personas page per the conflict protocol.

## 2026-05-17 proposal | Two-operator memory system architecture

User-directed design proposal (not /research, not /ingest). Created wiki/proposals/memory-system-architecture.md — new wiki/proposals/ subdir. Editorial synthesis of the user's brief grounded in the memory cluster: two operators (Librarian owns tiering/curation/routing; Worker extracts + records verbatim), verbatim-first store, text-search-first retrieval ladder (grep/regex → structured key index → vector/graph → LLM). Each of the five user tenets annotated with supporting + complicating wiki evidence. Honest risk surfacing: verbatim tenet sits inside the OPEN verbatim-vs-extracted conflict (LongMemEval hybrid taken as working position); DCI scale ceiling (~200K docs) flagged as a hard partitioning constraint; Librarian-as-LLM silent-failure / learning-to-forget risks from the survey open challenges. Page banner-labelled PROPOSAL/editorial; Source section states no new external sources. index.md + revisions.md updated. Awaiting user direction on the embedded open decisions (scale, topology, substrate assumptions) before any implementation framing.

## 2026-05-17 proposal | Role & Skill definition (agentic-system proposal set)

User elaborated the role/skill layer (role-defining vs project-specific memory classes) and asked for a dedicated proposal+best-practices page. Created wiki/proposals/agentic-system-roles-skills.md as the canonical role-definition spec; extended wiki/proposals/memory-system-architecture.md with the on-disk role/project memory layout + 3 risk bullets + forward cross-ref. Explicit single-responsibility split: roles-skills page = what a role IS + authoring best-practices; memory-system-architecture page = where role artefacts are stored/retrieved. Strongest synthesis: "improvement loop, uniform across roles" ⇒ Librarian-owned protocol (Worker produces failure-log signal, separate operator runs the protocol + rewrites Role Reference/Contract), grounded via SkillOS separate-curator evidence + memory-architectures trustworthy-reflection caveat + Reflexion mechanism + SkillOS insert/update/delete as the update action. Both pages editorial-labelled; grounding citations throughout; no external sources. index.md/revisions.md updated. 4 open decisions surfaced on the roles/skills page (improvement-loop validator, relationship-graph default, contract-size threshold, role-vs-personality unit) awaiting user direction.
