# Wiki Log

Append-only chronological record of wiki activity.

---

## [2026-04-22] bootstrap | AI product landscape — enterprise & startup offerings

Initial bootstrap. Schema and commands tailored for tracking AI offerings across two tiers (enterprise platforms and startups), with a descriptive, practitioner-oriented lens: what products actually do, what techniques they use under the hood, how they deploy, their customization hooks, real running costs, hard limits, and market reception. Four working uses: radar for new offerings, engineering intel on how teams build these products, market-reception tracking (hype vs reality), and build-vs-buy advisory for clients. Voice: terse, expert, facts-first, no hedging. Ground-truth sources (G2, HN, Reddit, GitHub issues, Stack Overflow) weighted as first-class evidence over vendor marketing. Ready to receive first source.

## [2026-04-22] research + ingest | Enterprise AI landscape 2026

Topic: "most used enterprise technologies and offerings". Captured 6 sources via `/research`: a16z arms-race 2026, Menlo Ventures state-of-AI 2025 (PDF), Deloitte state-of-AI 2026, a16z notes-on-AI-apps 2026, a16z 100-CIOs 2025 baseline, SaaStr Databricks-vs-Snowflake. **Two McKinsey sources** (State-of-AI 2025 PDF, Trust 2026 HTML) **blocked by bot-walls** — HTTP/2 protocol error on HTML, read-timeout on PDF; dropped per user choice.

Dispatched 6 subagents in parallel to produce structured `.ingest/*.summary.md` files (main context never read raw sources). All 6 summaries validated against `tools.ingest_plan.parse_summary` schema.

Aggregated into **7 wiki pages** via a consolidated plan (subagents originally proposed 12; folded overlapping landscape posts into time-stamped single pages):

- `landscape/enterprise-ai-market-2025-2026.md` — market size, buy-vs-build, deployment depth, 2025→2026 time-series.
- `landscape/llm-api-enterprise-share.md` — Anthropic 40% / OpenAI 27% / Google 21% spend share (Menlo), production-adoption (a16z), wallet-share shift, hosting-model.
- `landscape/ai-app-categories-2025.md` — departmental ($7.3B), vertical ($3.5B), horizontal ($8.4B); coding as $4B standout.
- `platforms/databricks.md`, `platforms/snowflake.md` — paired offering pages from SaaStr source.
- `thesis/ai-apps-layer-2026.md` — a16z editorial framing.
- `conflicts/open-questions-2026-04.md` — 10 flagged claims (death-of-app-layer contradiction, fine-tuning decline, direct-to-lab hosting shift, "95% AI initiatives fail", Anthropic leaderboard framing, $37B scope mismatch, Cursor $200M figure, "AGI for near-term enterprise tasks" claim, $1B coding-startup revenue, Snowflake NRR "stabilized" dispute).

**Kit-level learnings** logged to `master_notes.md`:
- `audit_captures` reports false-positive broken image refs for `capture_pdf --engine pymupdf` outputs (path-resolution mismatch between capture and audit).
- Parallel Bash tool calls cascade-cancel on a single error; research captures should wrap each command in `; echo "---exit=$?"` to prevent lost batches.

## [2026-04-22] research + ingest | Emerging agentic startups

Topic: "what are some emerging startups with interesting agentic technologies that solve real problems". Captured 6 sources via `/research`: TechCrunch Lio (2026-03 $30M Series A, a16z-led, procurement agents), TechCrunch Trace (2026-02 $3M seed, YC S25, London, knowledge-graph orchestration), Extruct AI YC W26 breakdown (199 companies), HN thread "AI agents are starting to eat SaaS" (1,428 lines, practitioner debate), HN thread "Do AI Agents Make Money in 2026?" (skeptical practitioner thread), Bessemer Venture Partners AI-Infrastructure Roadmap 2026. **GeekWire source blocked** by Cloudflare bot-wall — dropped; logged to `master_notes.md`.

Dispatched 6 subagents in parallel; all summaries validated against `tools.ingest_plan.parse_summary` schema.

Wrote **9 new wiki pages**:

- `landscape/yc-w26-ai-batch.md` — YC W26 cross-cut (199 companies, 9 categories, agentic clusters, standouts).
- `landscape/ai-infrastructure-frontiers-2026.md` — Bessemer 5-frontier thesis (harness, continual learning, RL platforms, inference-at-scale, world models).
- `thesis/agents-eating-saas.md` — practitioner-grounded counter-weight to a16z apps-will-win framing (consolidates HN threads 04 + 05).
- `startups/lio.md`, `startups/trace.md` — funding-announcement-derived stubs (both single-sourced, vendor-PR adjacent).
- `startups/pocket.md`, `startups/confluence-technologies.md`, `startups/ndea.md`, `startups/runanywhere.md` — YC W26 standouts with concrete-enough signal for their own pages.

**Updated 3 existing pages**:

- `conflicts/open-questions-2026-04.md` — revised C1 and C8 with practitioner evidence; added C11 (BVP next-wave inference inflation), C12 (arXiv citation fact-check), C13 (practitioner revenue skepticism vs Menlo spend), C14 (continual-learning winner), C15 (RL-platforms category leadership), C16 (world models as substrate vs niche). Total conflicts: 16.
- `landscape/ai-app-categories-2025.md` — added emerging-agent-platforms subsection (Lio, Trace); pointer to new infra-frontiers page.
- `thesis/ai-apps-layer-2026.md` — added "Practitioner friction surface (2026-04)" section with narrow-deep vs wide-shallow framing and pointer to agents-eating-saas.

**Kit-level learning** logged to `master_notes.md`: GeekWire is a Cloudflare-bot-walled host (repro with `--js`); belongs on the known-blocked-hosts list in `research.md`.

**Summary of the topic answer:** emerging agentic startups with real traction fall into three clusters. **(1) Vertical agents with domain-specific workflow automation** (procurement / medical billing / legal / insurance / care ops) — [[lio]] is the canonical example; [[yc-w26-ai-batch]] names many more at YC W26. **(2) Agent infrastructure** — observability ([[ai-infrastructure-frontiers-2026]] harness tier: Bigspin, Braintrust, Judgment Labs), orchestration ([[trace]]), inference-at-scale (TensorMesh, RadixArk, Inferact), on-device ([[runanywhere]]). **(3) AGI research labs** reopening the foundation-model race outside the big labs — [[ndea]] (Chollet, $43M), [[confluence-technologies]] (ARC-AGI-2 at 97.9%). **Critical counter-weight**: [[agents-eating-saas]] practitioner threads document that autonomous-agent revenue is largely vaporware; CAPTCHAs, spam-filtering and distribution — not intelligence — are the bottleneck. The agents that monetise are narrow single-workflow replacers. Build-vs-buy implication for clients: treat vertical-workflow agents (Lio-class) as credible buy candidates on narrow scope; treat horizontal-agent-platform pitches skeptically until they ship customers.

## [2026-04-22] weekly-brief | Week of 2026-04-15 → 2026-04-22

First (interactive) run of `/weekly-brief` — adapted from the kit-shipped paper-focused template to this wiki's product/offerings domain. Signal sources used: TechCrunch AI, Hacker News, trade-press (The Register, Diginomica, VentureBeat), vendor first-party blogs (Anthropic, Salesforce, C3, Google Cloud Press Corner), MIT Technology Review "10 things that matter in AI." See new [[reference-sources]] page for the scaffolded signal hierarchy.

**Trend synthesis for the week (editorial):**
1. **Densest model-release window in history** per MIT Tech Review — Opus 4.7 (2026-04-16), Gemini 3.1 Ultra + Flash TTS (2026-04-15), Grok 4.20 all inside two days.
2. **Agentic GTM race among hyperscalers** — Google Cloud's $750M partner fund is a pointed counter-move to Anthropic's direct-to-enterprise motion; Big 4 / GSI subsidies, pre-release Gemini access for McKinsey / BCG / Deloitte / Accenture.
3. **Incumbent "become-the-infrastructure" pivot goes loud** — Salesforce Headless 360 exposes the entire platform as APIs / MCP tools / CLI commands; Agent Fabric claims multi-vendor agent governance.
4. **Platform-coupled coding agents** emerging as a third category alongside bare-metal (Cursor/Codex/Claude Code) and Harvey-class vertical agents — C3 Code is the first instance profiled here.
5. **Agent infra sub-layer commercialising** — Runtime (YC W26) offers sandboxed-env + session-observability + guardrails for enterprise coding-agent deployment; watchlist entry.
6. **Vertical-agentic funding continues** — Bluefish $43M, Synera $40M, Hilbert $28M in a single week.

**Captured 4 sources (OpenAI Codex enterprise scaling was dropped — capture timed out 2× at 30s networkidle; logged to watchlist). Wrote 4 new content pages plus 2 scaffolding pages (watchlist, reference-sources). Updated 4 existing pages. Added 3 new open questions (C17, C18, C19); extended C3 and C5 with new data.**

**Critical reader note:** changes are **uncommitted on main**. Pre-existing uncommitted changes from bootstrap + two prior /research runs this session are also present — the weekly-brief diff is layered on top of that larger uncommitted body. The Gmail draft (step 8) includes a prominent commit reminder.

**Kit-level learning** flagged in prior session: `/weekly-brief` command is configured for a different wiki (hardcoded `cd /home/david/code/wiki-ai-trends`, branch `ai-trends-wiki`, ML-paper-focused signal hierarchy). For this wiki, the cron invocation needs adjustment and the signal hierarchy diverges. Created [[reference-sources]] to codify the domain-appropriate signal list. Harvest candidate: the kit's `/weekly-brief` scaffold could ship a `wiki/reference-sources.md` template that `/bootstrap` fills in based on the wiki's domain — currently each wiki reinvents this.

## [2026-04-23] weekly-brief | Week of 2026-04-21 → 2026-04-23 (partial cycle)

Second run of `/weekly-brief` on this wiki; fired one day after the 2026-04-22 inaugural sweep, so the window is 72h rather than a full week. Signal still plentiful — this week's news cycle ran hot.

**Sources scanned:** TechCrunch AI, Google Cloud Blog, Snowflake newsroom, The Register, Hacker News front page (2026-04-21 through -23), Simon Willison, r/LocalLLaMA via HN coverage, BusinessWire (funding), GitHub Changelog, VentureBeat, MIT Technology Review (see [[reference-sources]]).

**Trend synthesis (editorial):**
1. **Google's "everything is Gemini Enterprise" consolidation continues.** GEAP (Vertex AI rebrand) + Workspace Intelligence / Studio + Chrome AI Co-Worker all shipped same-day as Cloud Next '26 Day 2 (2026-04-22), stacked atop the $750M partner fund from 2026-04-21. Full enterprise-platform posture across compute → apps → browser; direct answer to Microsoft Copilot-everywhere stack.
2. **Agentic compute is breaking vendor pricing models in real time.** GitHub paused Copilot Pro signups and tightened Opus usage (2026-04-21); Anthropic tested removing Claude Code from Pro, reverted within a day after backlash (2026-04-21/22). Concrete evidence that real production use of coding agents is blowing through $20/mo economics. Direct counter-evidence for C17/C19 debate: agent adoption is economically-binding real, but monetization model unsettled. *(synthesis)*
3. **Snowflake counters Google with "agentic control plane" positioning.** Same-day 2026-04-21 keynote: Intelligence MCP-connector expansion + Cortex Code IDE plugins (VS Code, Claude Code) + cross-platform connectors (AWS Glue, Databricks, Postgres). Platform-vs-platform fight via MCP adoption depth, not model differentiation.
4. **Frontier labs are consolidating with hyperscalers, not diversifying.** Anthropic's new $5B from Amazon + $100B 10-year AWS commit (2026-04-20) cements AWS Trainium as primary training hardware. Material tension with C3: if direct-to-lab is the enterprise story, why are the labs themselves locking into specific CSPs? *(synthesis)*
5. **$60B for a harness, not a model.** SpaceX's option-to-acquire Cursor at $60B (2026-04-21) is this week's M&A shock. Validates C8 counter-thesis that harness/platform > model, but $60B at ~$2B ARR (~30x) reignites bubble-vs-reality debate.
6. **Open-weight coding collapses another tier.** Qwen3.6-27B (Apache 2.0) beats Alibaba's own 397B MoE on SWE-bench Verified (77.2%) while running Q4-quantized on a single consumer GPU. Compounds pricing-vs-economics story (item 2): if you can self-host frontier-adjacent coding locally, the $100+ API tier is a standing target.

**Captured 5 sources:** Google Cloud Next Day 2 (Gemini Enterprise Agent Platform), Snowflake Intelligence + Cortex Code, SpaceX/Cursor $60B option, GitHub Copilot Pro plan pause, Anthropic/AWS $5B/$100B. All audit-clean.

**Wrote 3 new content pages + 3 existing-page extensions:**
- NEW: [[landscape/google-cloud-next-2026-day2]], [[landscape/spacex-cursor-60b-option-2026-04]], [[landscape/agentic-compute-pricing-2026-04]]
- EXTENDED: [[platforms/snowflake]] (2026-04-21 Intelligence + Cortex Code section), [[llms/anthropic-claude-family]] (Compute-infrastructure section), [[landscape/llm-api-enterprise-share]] (lab-CSP coupling update)

**Conflicts updated:** C3 (strong Position-B evidence — direct-to-lab procurement masks AWS substrate lock-in); C8 (dual evidence — SpaceX $60B market signal + GitHub Copilot pause agent-scale signal, coding-agent adoption is real but generalization untested); C11 (Trainium displacement signal); C13 (bubble-vs-revenue-reality both sides reinforced; refined to three-tier read); **C17 upgraded from watching → trending-resolved-confirmed** (Google + Snowflake both adopt MCP-first pattern within 8 days of Salesforce — decisive); C18 (indirect architectural-category confirmation; Salesforce-specific multi-vendor claim still unverified).

**Watchlist this run (9 items):** Qwen3.6-27B (open-weight coding), AcuityMD $80M Series C (MedTech vertical agent), NeoCognition $40M seed, Google TPU 8t/8i, Chrome AI Co-Worker, Workspace Intelligence/Studio, Zed parallel agents, "Over-editing" empirical study (nrehiew), EVAS Intelligence ¥1.5B Series B (China RISC-V AI chip). Claude Code Pro test/revert captured inline in [[landscape/agentic-compute-pricing-2026-04]].

**Critical reader note:** changes are **uncommitted on `ai-offerings-trends-wiki`**. Pre-existing uncommitted changes from prior bootstrap + 2 prior /research runs + the 2026-04-22 weekly brief are all still present — this week's diff stacks on top. The email (step 8) includes a prominent commit reminder.

**Kit learning carried forward from 2026-04-22:** `/weekly-brief` command still hardcodes wrong wiki path (`/home/david/code/wiki-ai-trends`) and branch (`ai-trends-wiki`) and the wrong signal hierarchy. The brief template, commit reminder, and email subject line were all hand-fixed again this run; the kit-level fix proposed in `master_notes.md` remains **open** — worth prioritizing for the next `/harvest`.
