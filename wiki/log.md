# Wiki Log

Append-only chronological record of wiki activity.

---

## [2026-08-05] weekly-brief | AI product landscape radar sweep

Window: 2026-07-29 → 2026-08-05 (standard 7-day default per skill policy; note the prior run was 2026-07-01, a 5-week gap — no catch-up performed per skill's no-catch-up rule; Claude Opus 5's 2026-07-24 launch fell in that gap and was NOT captured this run since it predates the scan window — flagged to watchlist as high-priority backfill). Sources scanned: TechCrunch, VentureBeat, The Register, Forbes, CNBC, The Hacker News, Hacker News threads, r/LocalLLaMA, GitHub Discussions, Anthropic news, AWS/Databricks/Google Cloud/Salesforce blogs, a16z/Bessemer/Menlo (no in-window posts), YC, Crunchbase-adjacent trackers — 4 parallel scan agents. 5 URL captures attempted / 5 succeeded (0 audit issues).

Pages written: `landscape/agent-safety-incidents-2026-08` (NEW — Anthropic unauthorized-access self-disclosure 2026-07-30 + UK AISI Mythos 5 backdoor red-team report 2026-08-05), `landscape/mcp-rce-supply-chain-2026-05` (EXTENDED: Shai-Hulud Wave Six — first payloads inside AI-agent config files), `llms/anthropic-claude-family` (EXTENDED: Inference Hooks inline-DLP beta + safety-incident cross-links), `landscape/openai-gpt56-sol-2026-06` (EXTENDED: 2026-07-31 pricing cut, Luna -80%/Terra -20%), `llms/openai` (EXTENDED: GPT-5.6 family section), `landscape/agentic-compute-pricing-2026-04` (EXTENDED: pricing-cut update), `landscape/anthropic-subscription-split-2026-06` (EXTENDED: Uber Claude Code budget-blowout corroboration). Index, revisions, watchlist, log updated. Weekly brief written to `wiki/weekly-briefs/2026-08-05.md`. Not committed — local convention: user commits on next login.

Pre-existing uncommitted changes at run start: a large backlog — 9 modified files (wiki/index.md, wiki/landscape/anthropic-series-h-2026-05.md, wiki/llms/anthropic-claude-family.md, wiki/llms/openai.md, wiki/log.md, wiki/platforms/databricks.md, wiki/platforms/salesforce.md, wiki/revisions.md, wiki/watchlist.md) + 24 untracked files spanning weekly-briefs/2026-06-03 through 2026-07-01 and multiple landscape/startups pages from prior runs. These are NOT this run's diff — left untouched per local convention (path-scoped staging is this wiki's default posture, though this wiki does not auto-commit at all; see reference-sources.md Local conventions).

---

## [2026-07-01] weekly-brief | AI product landscape radar sweep

Window: 2026-06-24 → 2026-07-01. Sources scanned: Anthropic newsroom, OpenAI blog, TechCrunch, VentureBeat, CNBC, EU Consilium, CA Governor's office, HN aggregators. 5 captures attempted / 5 succeeded. No capture scripts run (all news/blog sources, captured via research subagents).

Pages written: `landscape/anthropic-california-gov-2026-06` (NEW), `landscape/openai-gpt56-sol-2026-06` (NEW), `llms/anthropic-claude-family` (EXTENDED: Claude Sonnet 5 section), `landscape/anthropic-export-controls-2026-06` (EXTENDED: resolution arc), `landscape/ai-regulatory-deadlines-2026` (EXTENDED: EU Omnibus Council approval + Colorado SB 189 repeal). Index, revisions, watchlist, log updated. Weekly brief written to `wiki/weekly-briefs/2026-07-01.md`. Not committed — local convention: user commits on next login.

Pre-existing uncommitted changes at run start: 8 modified files (wiki/index.md, wiki/landscape/anthropic-series-h-2026-05.md, wiki/llms/openai.md, wiki/log.md, wiki/platforms/databricks.md, wiki/platforms/salesforce.md, wiki/revisions.md, wiki/watchlist.md) + 18 untracked files (landscape/, startups/, weekly-briefs/ from prior runs). These are NOT this run's diff.

---

## [2026-06-10] weekly-brief | AI product landscape radar sweep

Window: 2026-06-03 → 2026-06-10. Sources scanned: TechCrunch, VentureBeat, TechStartups, Salesforce/EU Commission first-party, AlphaSense press release. 5 URL captures (Databricks $175B valuation, Salesforce Summer '26, EU AI Act CoP page, Niteshift TechCrunch, AlphaSense press release). All 5 passed audit (0 issues). 5 ingest subagents dispatched in parallel.

Pages written/extended: `platforms/databricks` (EXTENDED: Series L talks, $5.4B ARR update), `platforms/salesforce` (EXTENDED: Summer '26 multi-agent orchestration, Tableau MCP GA), `landscape/ai-regulatory-deadlines-2026` (NEW), `startups/niteshift` (NEW), `startups/alphasense` (NEW). Index, revisions, watchlist, log updated. Weekly brief written to `wiki/weekly-briefs/2026-06-10.md`. Not committed — awaiting user review.

Pre-existing uncommitted changes at run start: 10 files — wiki/index.md, wiki/landscape/anthropic-series-h-2026-05.md, wiki/llms/openai.md, wiki/log.md, wiki/revisions.md, wiki/watchlist.md (modified); wiki/landscape/alphabet-85b-equity-2026-06.md, wiki/landscape/microsoft-build-2026-06.md, wiki/landscape/snowflake-summit-2026-06.md, wiki/weekly-briefs/2026-06-03.md (untracked, from prior run).

---

## [2026-05-28] weekly-brief | AI product landscape radar sweep

Window: 2026-05-21 → 2026-05-28. Sources scanned: TechCrunch, CNBC, Bloomberg, VentureBeat, The Hacker News, Anthropic/Google/Blackstone first-party, buildfastwithai aggregator, HN front pages. 5 URL captures: Google Cloud I/O blog, Anthropic.com/KPMG, Blackstone JV press, TechFundingNews Anthropic round, The Hacker News TanStack. All 5 passed audit (0 issues). 4 ingest subagents dispatched in parallel.

Pages written/extended: `landscape/google-io-2026-enterprise` (NEW), `landscape/anthropic-series-h-2026-05` (NEW), `landscape/anthropic-enterprise-distribution-2026-05` (EXTENDED: KPMG 276K + Blackstone JV), `landscape/mcp-rce-supply-chain-2026-05` (EXTENDED: TanStack Mini Shai-Hulud section). Index, revisions, watchlist, log updated. Weekly brief written to `wiki/weekly-briefs/2026-05-28.md`. Not committed — awaiting user review.

Pre-existing uncommitted changes at run start: 27 files (14 modified, 13 untracked) from prior sessions — these are NOT this run's diff.

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

## [2026-05-03] weekly-brief | Week of 2026-04-24 → 2026-05-03

Third run of `/weekly-brief` on this wiki; first run on the standard 7-day Sunday cadence after the partial-cycle 2026-04-23 sweep. Cron path live (`0 7 * * 0` Sun 07:00 America/Toronto per [[reference-sources]]); this run is the user-initiated equivalent.

**Sources scanned:** TechCrunch AI, Microsoft Blog, Anthropic news, OpenAI news, Salesforce news, BusinessWire (funding), Hacker News (front page 2026-04-24 → -05-03), r/LocalLLaMA via HN, Simon Willison, Futurum Research, Crunchbase Q1 macro, Menlo Perspective, Reuters, CNBC, VentureBeat, MIT Tech Review (see [[reference-sources]]). Three subagents dispatched in parallel (trade-press + vendor / practitioner + HN / startup + analyst).

**Trend synthesis (editorial):**
1. **Microsoft / OpenAI partnership amended (2026-04-27).** IP license through 2032 converts to non-exclusive; Microsoft-to-OpenAI revenue share eliminated; OpenAI free to ship across any cloud. GPT-5.5 lands on AWS Bedrock the next day in limited preview. Removes a 6-year exclusivity term and is the legal scaffolding for OpenAI's $50B-class Amazon deal.
2. **Multi-CSP frontier-lab distribution settles as the durable model.** Google → Anthropic up-to-$40B + 5 GW Google Cloud (2026-04-24) lands four days after Amazon → Anthropic $5B + $100B + 5 GW (2026-04-20). Anthropic now anchored at material scale on Trainium AND TPU. Combined with the OpenAI move, both top-2 frontier labs are multi-CSP-distributed within the same fortnight. C3 closes with full reinterpretation: lab-CSP coupling exists at financing layer, not distribution layer. *(synthesis)*
3. **Agentic web-search-as-API tier emerges as a sibling infra category.** Parallel Web Systems hits $2B at five-month-old $740M (Sequoia-led; Parag Agrawal). Harvey + Notion + Clay + Opendoor as anchor customers. The category sits between agent harnesses and the public web — distinct from inference / harness / training-data tiers BVP profiled in 2026 roadmap. First-tier-validation gap in BVP's framing.
4. **IDE-as-agent-runtime is the new coding-agent ceiling.** Cursor 3.2 (2026-04-24) ships `/multitask` async parallel subagents, expanded worktrees, multi-root workspaces, full browser tool. Futurum frame: "agent execution runtime with a built-in code surface, and vendors competing on IDE capability alone are mispositioned." Compounds C8 Position A at the harness layer; pressure on CI/CD and cloud-dev-environment categories explicit.
5. **Open-weight cost-collapse continues from below.** DeepSeek V4 Pro/Flash (2026-04-24, MIT, 1M context, MoE) at $0.14/$0.28 per M tokens (Flash) or $1.74/$3.48 (Pro) — frontier-adjacent capability at ~1/30th input cost vs Opus 4.7. Compounds with Qwen3.6-27B from prior week. The premium subscription tier is now bracketed: agentic compute breaks it from above (Cursor 3.2 multi-task), open weights compress it from below.
6. **Vertical-AI funding cluster around the "labor budget" thesis.** Avoca ($125M, $1B unicorn, home services), Manifest OS ($60M, $750M, AI-native law firm), Legora ($50M ext., $5.6B, legal vs Harvey), Hightouch ($150M, $2.75B, agentic CDP), Ineffable Intelligence ($1.1B seed, $5.1B, RL-superlearner). Five raises in one week; Menlo's "vertical AI competes for labor budgets, not IT budgets" thesis post (2026-04-22) provides the connective framing. *(synthesis)*

**Captured 5 sources:** Microsoft / OpenAI restructure, Google → Anthropic $40B, Parallel Web Systems Series B, Cursor 3.2 multitask (Futurum), DeepSeek V4 (Simon Willison). All audit-clean (0 issues across 5 captures).

**Wrote 5 new content pages + 4 existing-page extensions:**
- NEW: [[landscape/openai-microsoft-restructure-2026-04]], [[landscape/google-anthropic-40b-2026-04]], [[startups/parallel-web-systems]], [[startups/cursor]], [[llms/deepseek]]
- EXTENDED: [[landscape/llm-api-enterprise-share]] (multi-CSP distribution settles as durable model), [[llms/anthropic-claude-family]] (Google deal compute infrastructure), [[landscape/agentic-compute-pricing-2026-04]] (refined three-tier read: open-weight floor, premium variance capture, hyperscaler procurement), [[landscape/ai-infrastructure-frontiers-2026]] (web-search-API tier flagged as sibling category to BVP roadmap).

**Conflicts updated:** **C3 closed-with-structural-reinterpretation** — original "80% direct-to-lab" framing fully obsolete; settled read is multi-CSP distribution. **C8 extended** — harness-as-runtime evidence compounds at coding layer; generalization-beyond-coding still untested. **C11 extended** — NVIDIA-displacement at frontier training is procurement reality (Trainium + TPU + Cerebras + Maia all at material scale). **New C20 added** — Microsoft IP-exclusivity end: long-tail-monetisation or substitution-prep? 6–12-month resolution path.

**Watchlist this run (13 items):** Avoca $125M, Manifest OS $60M, Legora $50M ext., Hightouch $150M, Ineffable Intelligence $1.1B seed, Salesforce Agentforce Operations GA, Anthropic 9 creative-tool MCP connectors + Claude Design, Databricks ai_parse + GPT-5.5 hosted, Google Deep Research Max, Meta/Manus M&A blocked by China, Thinking Machines $50B + Google GB300, Cursor Security Review beta, Crunchbase Q1 2026 macro framing.

**Critical reader note:** changes are **uncommitted on `ai-offerings-trends-wiki`**. Pre-existing uncommitted change at run start: `M .claude/commands/weekly-brief.md` (carryover from a kit-side edit prior to this run). The weekly-brief diff stacks on top — see step-7 status note in the email body for the surface delta.

**Kit learning carried forward:** the prior `/weekly-brief` hardcode-fix (`master_notes.md` 2026-04-22 entry, Status: open) is *closed by code* in commit b23497d (`feat(kit): make /weekly-brief wiki-agnostic via runtime git rev-parse`) — the runtime resolves repo, branch, and date correctly this run. Confirmed working in production for the first time on the Sunday cadence; entry can be marked Status: resolved on the next `/harvest` pass.


## [2026-05-10] weekly-brief | Week of 2026-05-04 → 2026-05-10

Fourth `/weekly-brief` run on this wiki; second run on the standard 7-day Sunday cadence (cron path `0 7 * * 0` America/Toronto per [[reference-sources]]). Today 2026-05-10 is Sunday — interactive run aligned with the cron schedule.

**Sources scanned:** TechCrunch AI, VentureBeat, Anthropic news, Microsoft Security Blog, OpenAI listing, Hacker News (front page 2026-05-04 → -05-10), r/LocalLLaMA via HN, Simon Willison, Bloomberg / Al Jazeera (Anthropic compute deals), The Hacker News (OX Security MCP disclosure), CNBC, Reuters, Crunchbase / Crunchbase News, BusinessWire, ServiceNow newsroom, Menlo Perspective, Bessemer Atlas, Latent Space, Y Combinator launches (Atla, Sentrial), The VC Corner (YC W26 metrics). Three subagents dispatched in parallel (trade-press + vendor / practitioner + HN / startup + analyst).

**Trend synthesis (editorial):**
1. **Three-way enterprise-agent-platform launch in 11 days.** [[../llms/openai|OpenAI Workspace Agents]] (2026-04-22, horizontal admin-builder, Codex cloud, credit pricing) + [[../platforms/microsoft|Microsoft Agent 365]] GA (2026-05-01, multi-vendor governance, M365 E7 / $15 standalone) + [[../llms/anthropic-claude-family|Anthropic Claude Finance Agents]] (2026-05-03, vertical platform with M365 add-ins + Moody's MCP app + 8 new data partners). Three vendors, three different platform shapes (horizontal / governance / vertical), one window. Defines the 2026-Q2 enterprise-agent landscape.
2. **MCP-fluency-with-isolation** is the new procurement read after the [[../landscape/mcp-rce-supply-chain-2026-05|OX Security MCP STDIO RCE disclosure]] (2026-05-08). 11+ CVEs across 7,000+ servers and 150M+ downloads; 5 prior independent disclosures of the same root cause >12 months back; **Anthropic declined to modify the protocol architecture, citing the behaviour as "expected."** The 2026-04 brief's "MCP fluency = platform-selection criterion (resolved-confirmed)" reading is incomplete — vendor-provided MCP-isolation (Model Armor, Agent Fabric, Agent 365 Defender controls + MCP server context mapping) becomes the actual procurement criterion. C17 reopened with Position B.
3. **Sierra $950M @ $15B+ post-money is the largest pure-play vertical-agent raise to date** and the strongest publicly-disclosed non-coding agent-vertical scale data point ($150M ARR Feb 2026, 40%+ Fortune 50 self-reported). Validates Sequoia "services are the new software" thesis. Extends C8 generalisation-side argument with non-coding evidence (weight 0.7, vendor self-reported caveats). See [[../startups/sierra|sierra]].
4. **Microsoft's hedge from the OpenAI restructure has clarified into "win governance over the multi-vendor estate, regardless of model winner."** Three operational signals within 11 days post-restructure: OpenAI Workspace Agents, Agent 365 GA, Anthropic finance agents distributing inside M365. The restructure was strategic prep for a multi-vendor M365 future, not a punitive event. C20 leans toward "governance-of-multi-vendor-estate" read; resolution paths #1–3 still open through 2026-Q4. See [[../landscape/openai-microsoft-restructure-2026-04|openai-microsoft-restructure-2026-04]] §Operational signals.
5. **Agent governance / control-plane consolidates around seat-based-SKU vendors with bundled-into-existing-license pricing.** Microsoft (E7 + $15 standalone), Salesforce (Agent Fabric in Agentforce), Google (GEAP Agent Gateway), ServiceNow AI Control Tower (acquired Traceloop for runtime observability, Knowledge 2026, 2026-05-05). Pure-play harness/eval startups ([[../landscape/ai-infrastructure-frontiers-2026|Bigspin / Braintrust / Judgment Labs]]) face structural pricing+distribution disadvantage; Traceloop's ServiceNow acquisition is the first concrete acquihire-direction data point. *(synthesis)*
6. **Credit-based agent pricing** (OpenAI Workspace Agents, post-2026-05-06) becomes the third execution-pricing pattern alongside flat-Pro+ subscriptions and burst-API metering. Decouples agent unit-economics from seat unit-economics — the budget primitive enterprise CFOs have been asking for. Watch for Microsoft Copilot, Salesforce Agentforce, Anthropic Managed Agents adoption through 2026-Q3. Refined [[../landscape/agentic-compute-pricing-2026-04|four-tier read]] (open-weight / premium-subscription / credit-based-execution / hyperscaler-routed) plus separate governance-bundle layer.

**Captured 5 sources:** Sierra $950M (TechCrunch), Anthropic finance agents (Anthropic news), Microsoft Agent 365 GA (Microsoft Security Blog), MCP RCE disclosure (The Hacker News citing OX Security), OpenAI Workspace Agents (VentureBeat). All audit-clean (0 issues across 5 captures). Note: VentureBeat capture required `--js` retry after default networkidle timeout; image assets 429'd but markdown captured cleanly.

**Wrote 4 new content pages + 5 existing-page extensions:**
- NEW: [[../startups/sierra|sierra]], [[../platforms/microsoft|microsoft]], [[../landscape/mcp-rce-supply-chain-2026-05|mcp-rce-supply-chain-2026-05]], [[../llms/openai|openai]]
- EXTENDED: [[../llms/anthropic-claude-family|anthropic-claude-family]] (Vertical platforms / Finance Agents section + MCP-decline governance signal), [[../landscape/openai-microsoft-restructure-2026-04|openai-microsoft-restructure-2026-04]] (Operational signals section, 3 confirming signals), [[../landscape/agentic-compute-pricing-2026-04|agentic-compute-pricing-2026-04]] (credit-pricing third pattern, refined four-tier read + governance-bundle layer), [[../landscape/ai-infrastructure-frontiers-2026|ai-infrastructure-frontiers-2026]] (agent control-plane consolidation update; Traceloop acquisition signal), [[../thesis/agents-eating-saas|agents-eating-saas]] (Sierra section + three-way enterprise-agent-platform race section).

**Conflicts:** **C8** extended (Sierra non-coding scale data point, weight 0.7); **C17 REOPENED with Position B** (MCP RCE supply-chain disclosure; protocol-fluency-with-vendor-isolation now the durable procurement criterion); **C20** leans toward "governance-of-multi-vendor-estate" read after Agent 365 + OpenAI Workspace Agents + Anthropic-on-M365 operational signals.

**Watchlist this run (10 items):** Anthropic + Akamai $1.8B compute deal (2026-05-08), Anthropic + SpaceX Colossus 300MW (2026-05-06), ServiceNow AI Control Tower expansion + Traceloop acquisition (Knowledge 2026 / 2026-05-05), Blitzy $200M Series @ $1.4B (autonomous enterprise SDLC, 2026-05-05), DeepInfra $107M Series B (2026-05-04, inference-at-scale), Tessera Labs $60M Series A a16z (ERP modernisation, 2026-05-06), Writer event-based triggers (2026-04-30, autonomous trigger model), Kimi K2.6 / Chinese open-weight cluster (HN 311 pts, 2026-05-03), MCP RCE adjacent: NanoClaw + Vercel approval-gateway (2026-04-17), EU AI Act Omnibus (high-risk enforcement pushed to Dec 2027 / Aug 2028, 2026-05-07).

**Critical reader note:** changes are **uncommitted on `ai-offerings-trends-wiki`**. Pre-existing uncommitted changes at run start are extensive — the prior 2026-05-03 weekly brief output (5 new pages + 9 extended files + 5 raw captures + .ingest summaries) was never committed; this week's diff stacks on top. Email body lists pre-existing diff separately so the user can identify the weekly-2026-05-10 surface delta vs the carryover weekly-2026-05-03 work.

**Kit health:** runtime resolution from commit b23497d worked correctly again; repo path, branch, run date, and pre-existing-dirty all resolved at runtime per spec. The `master_notes.md` 2026-04-22 "/weekly-brief hardcodes wrong wiki path" entry can be marked `Status: resolved` on the next `/harvest`. New kit observation: VentureBeat captures intermittently 429 on image assets (markdown still captures cleanly with `--js`). Worth flagging in `master_notes.md` as a low-severity capture-script note; not urgent enough to harvest mid-run.

## [2026-05-17] weekly-brief | Week of 2026-05-10 → 2026-05-17

Autonomous Sunday cron sweep. Window 2026-05-10 → 2026-05-17. Trend scan via 4 parallel signal-tier subagents (trade-press/funding, HN/Reddit practitioner, vendor first-party/analyst, startup radar).

**Trend pattern this week:**
1. **Agent-economy infrastructure crystallised into a primitive.** Amazon Bedrock AgentCore Payments shipped a managed agent payment rail (HTTP 402 → x402 → USDC on Base, session spend caps, Coinbase/Stripe wallets) — the first hyperscaler-native answer to "how do agents transact," sitting alongside an already-named protocol field (Google AP2, ACP, MPP). Payment plumbing moves from open-protocol-debate to managed-product.
2. **Anthropic's enterprise distribution went multi-surface in one week.** SAP Business AI Platform OEM-embeds Claude as Joule's primary reasoning engine (Sapphire, forward-looking PR) and Claude Platform on AWS GA'd as an account-native managed-agent stack distinct from Bedrock (Anthropic, not AWS, is the data processor). Distribution-channel land-grab, not a revenue print.
3. **Frontier vendors verticalise into the services/SI layer.** OpenAI spun out a majority-owned ~$4B "Deployment Company" (~$10B pre-money, ~19 PE/consulting backers) + acquired Tomoro (~150 FDEs) — explicitly competing with the Google $750M GSI fund / Accenture-style channel. (synthesis: agents-displacing-services is being answered by model vendors becoming the services firm.)
4. **MCP's security substrate is now load-bearing in procurement.** SAP routes Claude through MCP (4th named C17 incumbent → Position A follow-through) while inheriting the unpatched MCP RCE surface (Position B); Lyrie.ai's Agent Trust Protocol ($2M pre-seed, IETF-bound, Anthropic CVP) is the first concrete protocol-level-isolation tooling datapoint — early, heavily caveated.
5. **Practitioner backlash hardened into a visible theme** (watchlist, not captured): Hashimoto "AI Psychosis" (HN ~1,988), "AI is making me dumb" (HN ~541), Cursor pricing/CEO-apology, Ontario audit of AI medical scribes "blowing basic facts." Reliability-and-overreliance counter-signal to the platform launches.

**Captured 5 sources** (audit-clean, 0 issues): AgentCore Payments (AWS ML blog), SAP+Anthropic (news.sap.com), Claude Platform on AWS (claude.com/blog), Lyrie ATP (GlobeNewswire), OpenAI Deployment Company (PYMNTS — Axios + openai.com bot-walled/networkidle-timeout, fell back per reference-sources policy).

**Wrote 4 new pages + 5 existing-page extensions:**
- NEW: [[../landscape/agentcore-payments-x402-2026-05|agentcore-payments-x402-2026-05]], [[../landscape/anthropic-enterprise-distribution-2026-05|anthropic-enterprise-distribution-2026-05]] (SAP + Claude/AWS clustered into one load-bearing page per autonomous page-plan policy — 2 thin PR sources, neither warranted a standalone page), [[../startups/lyrie|lyrie]], [[../landscape/openai-deployment-company-2026-05|openai-deployment-company-2026-05]]
- EXTENDED: [[../llms/anthropic-claude-family|anthropic-claude-family]] (enterprise distribution OEM/platform section + Lyrie CVP), [[../landscape/llm-api-enterprise-share|llm-api-enterprise-share]] (Anthropic OEM+hyperscaler wallet-share), [[../thesis/agents-eating-saas|agents-eating-saas]] (3 thesis stress-tests: payment rail / embed-not-replace / vendor-into-services), [[../landscape/agentic-compute-pricing-2026-04|agentic-compute-pricing-2026-04]] (x402 as enabling primitive, not 5th tier), [[../landscape/openai-microsoft-restructure-2026-04|openai-microsoft-restructure-2026-04]] (Operational signals #4–5).

**Conflicts:** **C17** updated with two datapoints (SAP = Position A follow-through, 4th MCP-first incumbent; Lyrie ATP = Position B resolution-path-(b) first tooling signal) — status unchanged OPEN-reopened. **C21 added** (AgentCore "first managed agent payment" vs Google AP2 — protocol-vs-managed-platform primacy; flag-only, concrete contestable claim with named counter).

**Watchlist this run (10 items):** OpenAI Realtime Voice trio + published pricing, OpenAI Codex Mobile, Anthropic Claude for Small Business, Claude Opus 4.7 GA (flat pricing), Snowflake Intelligence + Cortex Code agent-control-plane expansion, Corgi Insurance $160M/$1.3B (AI liability insurance), Graphon AI $8.3M (pre-model relational-memory layer vs RAG), CopilotKit $27M (AG-UI protocol), Recursive Superintelligence $650M stealth (Socher/Rocktäschel, pre-product), practitioner-friction cluster (Hashimoto/Cursor/Ontario/"AI dumb"). Next-sweep flag: Google I/O 2026 (2026-05-19, outside window — Gemini Spark / Gemini Intelligence / Gemini 4).

**Critical reader note:** changes are **uncommitted on `ai-offerings-trends-wiki`**. Pre-existing uncommitted changes at run start were extensive (prior 2026-05-03 + 2026-05-10 weekly outputs never committed, plus master_notes / .claude/commands edits); this run's diff stacks on top. The email separates this-run's surface from the carryover.

**Kit health:** runtime resolution (commit b23497d) worked again — repo path / branch / run date / pre-existing-dirty all resolved at runtime. Capture note: Axios + openai.com both bot-walled (networkidle timeout) for the OpenAI DeployCo source; PYMNTS captured cleanly on first try — consistent with the reference-sources known-bot-walled list. `poetry` not on the non-interactive shell PATH (`$HOME/.local/bin/poetry`); had to export PATH before capture/ingest tooling. Low-severity kit-env note worth flagging in master_notes (the cron invokes `claude -p` which may inherit a login shell that has it; interactive harness shell does not).

---
**2026-05-28 — ingest: google-io-2026-enterprise**
New page `landscape/google-io-2026-enterprise.md` written from `raw/research/weekly-2026-05-28/01-google-io-2026-enterprise.md` (Google Cloud Blog / Thomas Kurian, I/O 2026). Covers: Managed Agents API, Gemini Spark enterprise controls, Gemini 3.5 Flash GA benchmarks, Gemini Omni timeline (enterprise Q3 2026), Antigravity 2.0 + CodeMender. Competitive read-through vs Microsoft Copilot Studio, AWS AgentCore (C21 extended), Salesforce Agent Fabric. index.md + revisions.md updated.

---
**2026-05-28 — ingest: KPMG alliance + Blackstone JV → extended anthropic-enterprise-distribution-2026-05**
Extended `landscape/anthropic-enterprise-distribution-2026-05.md` with two new sections from `raw/research/weekly-2026-05-28/02-anthropic-kpmg-alliance.md` and `raw/research/weekly-2026-05-28/03-anthropic-blackstone-jv.md`. KPMG section covers 276K global employee rollout, Digital Gateway Azure embed (Claude Cowork + Managed Agents), Tax & Legal initial focus, PE preferred partner designation, KPMG Blaze (PE portfolio + Claude Code), cybersecurity angle, 2-year US pilot baseline. Blackstone JV section covers $1.5B formation (Blackstone + HF + Goldman + GA + Leonard Green + Apollo + GIC + Sequoia), forward-deployed Anthropic engineers, mid-size PE portfolio target, maintenance-cadence rationale, OpenAI DeployCo parallel, PE-channel overlap tension with KPMG. No conflicts found. Related section extended with agentcore-payments-x402-2026-05 link.

---
## [2026-06-03] weekly-brief | Week of 2026-05-28 → 2026-06-03

Autonomous weekly sweep (manual ad-hoc run, Tuesday). Window 2026-05-28 → 2026-06-03.

**Trend pattern this week:**
1. **Hyperscaler AI capex entered a new magnitude regime.** Alphabet raised $85B (largest single equity offering in history, oversubscribed); $180–190B capex planned for 2026. Simultaneously, Anthropic closed a $65B Series H ($965B post-money — pre-announcement estimates were half the actual number) and filed an S-1 on June 1. AI IPO pipeline (Anthropic, OpenAI, SpaceX) is front-of-mind for institutional markets.
2. **Enterprise data platforms crystallizing as agent control planes.** Snowflake Summit 26 launched CoWork (knowledge-worker personal agent + MCP connectors), acquired Natoma (enterprise MCP gateway for identity-aware tool-call authorization) — directly implementing the MCP+governance-layer architecture that C17 has been watching. Microsoft Build launched Scout (always-on personal agent on OpenClaw, persistent identity). Both compete with Google Gemini Spark and Salesforce Agentforce for the same "every-employee agent" slot.
3. **OpenAI accelerating knowledge-worker enterprise push.** Codex "Intelligence at Work" event: 5M weekly users (6x since February), knowledge workers 20% of users growing 3x faster, six role-specific plugins, Sites (hosted interactive output), Codex + GPT-5.5 GA on Bedrock at parity pricing. Three weeks after the OpenAI Deployment Company launch.
4. **Anthropic's compute scale and revenue outpaced pre-announcement tracking.** Series H was $65B/$965B (not $30B/$900B+); revenue run-rate crossed $47B (not $10.9B quarterly). Corrects the wiki. Four-CSP compute substrate (AWS/Google/SpaceX/Akamai) fully confirmed.
5. **Pricing pressure hardening for AI developer tools.** Anthropic ending flat-rate Claude Code access June 15; Microsoft reportedly canceling Claude Code licenses. Both signal enterprise AI tooling economics are entering the renegotiation phase — the flat-subscription model that launched the coding-agent wave is breaking down. (Synthesis — not captured as a page; feeds [[landscape/agentic-compute-pricing-2026-04]].)

**Captured 5 sources** (audit-clean, 0 issues; 1 source retried — Microsoft Scout captured via TechCrunch after thin initial capture):
- Anthropic Series H official close (anthropic.com/news/series-h)
- Snowflake Summit CoWork/Natoma (snowflake.com press release)
- OpenAI Intelligence at Work (TechCrunch)
- Microsoft Scout/Build 2026 (TechCrunch, retry from thin Microsoft blog capture)
- Alphabet $85B equity raise (TechCrunch)

**Wrote 3 new pages + 2 existing-page updates:**
- NEW: [[landscape/snowflake-summit-2026-06]], [[landscape/microsoft-build-2026-06]], [[landscape/alphabet-85b-equity-2026-06]]
- UPDATED: [[landscape/anthropic-series-h-2026-05]] (corrected $30B/$900B → $65B/$965B; added compute scale-up, S-1 filing sections); [[llms/openai]] (extended: Intelligence at Work + Bedrock GA + 5M WAU scale signal)

**Conflicts:** **C17** updated — Snowflake Natoma = 5th MCP-first incumbent (Position A follow-through; enterprise MCP gateway model gaining structural confirmation). **C8** updated inline in [[llms/openai]] — OpenAI 5M WAU + 20% knowledge workers (3x growth rate) is the most concrete scale evidence to date that coding-agent PMF is generalizing to non-coding knowledge work.

**Watchlist this run (10 items):** Coralogix $200M/AI agent observability, ZeroDrift $10M/AI compliance firewall, Meta AI Business Agent global, SAP Sapphire Joule Studio + Autonomous Enterprise, Lovable×Google Cloud deal, OpenAI GPT-5.5/Codex on Bedrock GA, Anthropic flat-rate Claude Code ending June 15, Microsoft canceling Claude Code licenses, CopilotKit $27M/AG-UI protocol, Anthropic Project Glasswing expansion.

**Kit health:** PATH override (`$HOME/.local/bin:$PATH`) still needed for non-interactive shell. One thin capture (Microsoft 365 blog JS-heavy); fell back to TechCrunch — consistent with known-bot-walled / JS-heavy pattern. All 5 final sources clean on audit.

**Local convention note:** Per `wiki/reference-sources.md` Local conventions — changes land uncommitted; user commits on next login after reviewing the diff.

---

## 2026-06-10 — Ingest: Salesforce Summer '26

**Source:** `raw/research/weekly-2026-06-10/01-salesforce-summer26-multiagent-2026-06.md`

**Action:** Extended `wiki/platforms/salesforce.md` with Summer '26 release (GA 2026-06-15). Added `## Summer '26 Release` section covering: multi-agent orchestration GA, Tableau MCP with Trust Layer, IT Service Domain Pack (50+ OOB agents in Slack/Teams/IT Service Desk), Agentforce Self-Service (6-click setup), Customer Engagement Agent, Momentum passive CRM capture, Collections with Agentforce, Slack First Sales, Process Compliance Navigator, Scheduling Console, Real-Time Offer Management, Security Mesh, and secondary features. Cross-vendor context updated with Microsoft Agent 365 parallel, Snowflake MCP governance competing direction, and MCP RCE Trust Layer gap flag.

**Ingest summary:** `raw/research/weekly-2026-06-10/.ingest/01-salesforce-summer26-multiagent-2026-06.summary.md`

**Key flags for practitioner validation:** (1) Multi-agent orchestration context-threading mechanism unspecified — may be true threading or state serialization at handoff. (2) Tableau MCP Trust Layer isolation vs STDIO RCE class not disclosed. (3) No pricing disclosed for Self-Service "simplified pricing." (4) All reception is vendor-sourced at announcement.

---
**2026-06-17 — Ingest: anthropic-subscription-split-2026-06**

**Source:** `raw/research/weekly-2026-06-17/04-anthropic-subscription-split-2026.md` (DevToolPicks) + WebSearch supplements.

**Pages written:** `landscape/anthropic-subscription-split-2026-06` (NEW).

**Key finding:** The June 15 Agent SDK credit split was paused by Anthropic on the day it was due to take effect. Reversal attributed to OpenAI price-war pressure, IPO optics, and developer community backlash. Microsoft Claude Code license cancellations (~HN 350+) documented as parallel enterprise-cost signal. Managed Agents self-hosted sandboxes + MCP tunnels (May 19 launch) identified as the enterprise distribution path that replaces the subscription-subsidy model long-term. Prior wiki read ("Pro commoditizes; tiering not price increase") still holds but updated: credit metering is the mechanism and it is more politically difficult to deploy than the structural logic implies.

---
**2026-06-17 — Ingest: yc-p26-2026-06**

**Source:** `raw/research/weekly-2026-06-17/05-yc-p26-demo-day-2026.md` (Fluenta P26 batch analysis).

**Pages written:** `startups/yc-p26-2026-06` (NEW).

**Key finding:** 194 companies, 61% B2B, 55-company agent infrastructure group. Most enterprise-AI-relevant: Netter (AI-native Palantir for mid-market), Cohesion (agentic buy-side investment research vs AlphaSense), Clawvisor (runtime access control for AI agents, agent identity/permissions category). Batch-level theme: agent supply-chain tooling dominates over new agent applications.

---
**2026-06-17 — Weekly brief sweep (2026-06-10 → 2026-06-17)**

5 sources captured to pages: Databricks Data+AI Summit (Genie One/Ontology/ZeroOps/OpenSharing), Prometheus $12B physical AI, AWS Bedrock AgentCore June 2026, Anthropic subscription split reversal, YC P26 Demo Day. Watchlist +10 overflow items. Pages written: landscape/databricks-data-ai-summit-2026-06, landscape/prometheus-physical-ai-2026-06, landscape/aws-bedrock-agentcore-june-2026, landscape/anthropic-subscription-split-2026-06, startups/yc-p26-2026-06. Weekly brief written to wiki/weekly-briefs/2026-06-17.md. Not committed — awaiting user review per local convention.

---
**2026-06-24 — Weekly brief sweep (2026-06-17 → 2026-06-24)**

5 sources captured to pages: OpenAI Jalapeño custom inference chip (Broadcom), Salesforce acquires Fin $3.6B, Groq $650M raise / Nvidia LPU not-acqui-hire, Anthropic export control order + Fable 5/Mythos 5 takedown, AI assistant market share shift (ChatGPT below 50%). All captures via TechCrunch (audit: 0 issues). Watchlist +10 overflow items. Weekly brief written to wiki/weekly-briefs/2026-06-24.md. Email sent via SMTP to david.hugh.mcnamee@outlook.com. Not committed — awaiting user review per local convention.

---
**2026-08-12 — Weekly brief sweep (2026-08-05 → 2026-08-12)**

5 sources captured to pages: Black Hat USA 2026 CI-harness CVEs (Claude Code CVE-2026-54316, Gemini CLI CVE-2026-12537 CVSS 10.0, OpenAI Codex no-CVE) → new page; KPMG Global AI Pulse Q2 2026 cost-pullback survey (49% scaled back agent deployments) → extends agentic-compute-pricing-2026-04; Anthropic Sonnet 5 pricing made permanent (2026-08-11) → extends anthropic-claude-family; River AI $1.1B post-training-as-a-service raise → new startups page; xAI/SpaceXAI Grok Bot persistent-agent beta → new llms running page. All captures via TechCrunch/Forbes/TheHackerNews/VentureBeat/explainx.ai (audit: 0 issues). Also flagged a possible ChainDrop/Shai-Hulud-Wave-Six campaign overlap on mcp-rce-supply-chain-2026-05 — unresolved, noted for practitioner validation, not merged. Watchlist +10 overflow items. Required-coverage roundup (new startups / funding & M&A / product launches) included per reference-sources.md override. Weekly brief written to wiki/weekly-briefs/2026-08-12.md. Not committed — awaiting user review per local convention.

---
**2026-08-19 — Weekly brief sweep (2026-08-12 → 2026-08-19)**

5 sources captured to pages: Stripe acquires OpenRouter for $7B+ (model-routing/AI-gateway, unconfirmed/rumor-stage) — new page landscape/stripe-openrouter-acquisition-2026-08; Anthropic revenue run-rate hits $65B annualized end-July 2026, $2T+ IPO target possibly fall 2026 — extends landscape/anthropic-series-h-2026-05; deeper technical detail (root causes, patched versions, exploitation status) on the Black Hat USA CI-harness CVEs — extends landscape/blackhat-ai-coding-agent-cves-2026-08; Databricks closes $5B round at $190B valuation (vs $165-175B talk-stage), >$7B revenue run-rate — extends platforms/databricks; Cursor launches Origin code-hosting platform (GitHub-alternative wedge, timed with GitHub outage) — extends startups/cursor. All captures via TechCrunch/TheHackerNews/Databricks-first-party/VentureBeat (audit: 0 issues, one known VentureBeat image-429 on the Cursor capture, markdown unaffected).

Load-bearing correction: the Cursor-Origin ingest subagent flagged that VentureBeat's source (citing Bloomberg) reports the SpaceX–Cursor acquisition completed 2026-08-14 (all-stock, Cursor now inside a "SpaceXAI" division) — contradicting the existing wiki page's "$60B acquisition option" framing (2026-04-21). Since the citation was secondhand, ran an independent WebSearch verification before updating: cross-confirmed via Seeking Alpha, Yahoo Finance, SatNews, crypto.news (merger effective 2026-08-14, Cursor shares converted to 389,289,254 SpaceX Class A shares). Updated landscape/spacex-cursor-60b-option-2026-04 title/framing to reflect completion rather than treating it as an open conflict.

Ingest summaries: raw/research/weekly-2026-08-19/.ingest/{01-stripe-openrouter-acquisition-2026-08,02-anthropic-preipo-financials-2026-08,03-claude-code-gemini-cli-ci-secrets-2026-08,04-databricks-5b-round-190b-2026-08,05-cursor-origin-launch-2026-08}.summary.md

Key flags for practitioner validation: (1) Stripe/OpenRouter deal is sourced entirely secondhand (Bloomberg via TechCrunch); Stripe declined to comment — treat as rumor-stage until primary confirmation. (2) Same-week Anthropic pre-IPO signals not independently captured this run — pre-IPO credit facility reportedly past $10B, planned supervoting shares for Dario Amodei, reported Decart acquisition talks (~$6B) — flagged to watchlist for a follow-up capture rather than stated as sourced fact on the wiki page. (3) Possible overlap between the ChainDrop npm-worm campaign (Pillar Security) and the existing "Shai-Hulud Wave Six" entry on mcp-rce-supply-chain-2026-05 remains unresolved from the prior run — not re-investigated this run. Required-coverage roundup (new startups / funding & M&A / product launches) included per reference-sources.md override. Weekly brief written to wiki/weekly-briefs/2026-08-19.md. Not committed — awaiting user review per local convention.

---
**2026-08-26 — Weekly brief sweep (2026-08-19 → 2026-08-26)**

5 sources captured to pages: Salesforce × Anthropic "Claudeforce" — Salesforce in Claude plugin (37 sales skills), Salesforce's own "you'll never need its app again" framing, first "force"-branded partner product — new page landscape/salesforce-anthropic-claudeforce-2026-08, extends platforms/salesforce and llms/anthropic-claude-family, and load-bearing against conflicts C1 (death-of-app-layer thesis); Anthropic pre-IPO governance/financing cluster (founder supervoting shares + shrunk 3-trustee Long-Term Benefit Trust, pre-IPO credit facility past $10B, Decart acquisition talks ~$6B, OpenAI pushing its own IPO target to 2027) — resolves the "not yet independently captured" flag from the 2026-08-19 run, extends landscape/anthropic-series-h-2026-05; Hugging Face reportedly in talks to be acquired for ~$13B (~3x 2023's $4.5B valuation) — new page landscape/huggingface-acquisition-2026-08, third model-hub/gateway-layer consolidation event in ~10 days after Stripe/OpenRouter and Dynatrace/Arize; McKinsey State of AI 2026 survey (6% of enterprises are "AI high performers," ~90% of use cases stuck in pilot) — extends conflicts/open-questions-2026-04 C4 with the Menlo-independent adoption check it was explicitly waiting on, converging with Gartner/KPMG on enterprise-ROI pessimism, also cross-referenced on landscape/agentic-compute-pricing-2026-04; Google's A2A protocol formally joins the Agentic AI Foundation (sits alongside Anthropic's MCP under neutral governance, AAIF now 250+ members) — new page landscape/google-a2a-agentic-foundation-2026-08, resolves last week's "A2A hosted-project" watchlist flag.

All captures via VentureBeat/TechCrunch/The Register/TechTimes/PYMNTS/Yahoo Tech/Google Developers Blog/Linux Foundation (audit: 0 issues; two bot-walled sources — Techzine and Axios — dropped in favor of working alternates for the same story).

Key flags for practitioner validation: (1) Hugging Face acquisition talk pickup across PYMNTS/Yahoo Finance/TechTimes/Gizmodo all appears to trace to the single original TechCrunch report — treat as one signal despite wide pickup, not independently multi-sourced. (2) Anthropic's pre-IPO credit-facility figure (>$10B) is still secondary-sourced via Bloomberg aggregation, not independently captured with a primary document this run. (3) Salesforce Claudeforce detail is entirely vendor/earnings-framed — no independent practitioner reviews possible yet (pilot-only, open beta not until September 2026). Required-coverage roundup (new startups / funding & M&A / product launches) included per reference-sources.md override. Weekly brief written to wiki/weekly-briefs/2026-08-26.md. Not committed — awaiting user review per local convention.

---
**2026-09-02 — Weekly brief sweep (2026-08-26 → 2026-09-02)**

5 sources captured to pages: OpenAI's unreleased Astra model crosses the Preparedness Framework's "Critical" cybersecurity threshold — first-ever such designation, autonomous zero-day discovery/exploitation against hardened targets, gated release via Daybreak Blue — new page landscape/openai-astra-critical-2026-09, also references a distinct "OpenAI–Hugging Face incident" (internal agent coordination/breach) flagged to watchlist for deeper capture; Anthropic Model Hardware Standard research preview — model-agnostic protocol for agents to operate physical lab/manufacturing hardware via MCP/CLI/API, developed with HHMI Janelia — new page landscape/anthropic-model-hardware-standard-2026-09, extends llms/anthropic-claude-family and conflicts/open-questions-2026-04 C17 (MCP blast radius now includes physical actuation); OpenAI terminates Cursor's contractual model access effective 2026-11-12, following the SpaceX acquisition and citing ToS-trust concerns — extends landscape/spacex-cursor-60b-option-2026-04 and startups/cursor, first concrete consequence of the supplier-is-also-competitor risk that page has tracked since April; Nvidia named as the Hugging Face acquirer at ~$12.9B, but deal status disputed between The Information ("agreed") and Business Insider ("not yet signed") — extends landscape/huggingface-acquisition-2026-08; Anthropic signs a $35B six-year cloud deal with Nvidia-backed Lambda (Nvidia holds the data-center lease directly) — extends landscape/anthropic-series-h-2026-05 with a new compute-deal running-tally table alongside the SpaceX/Fluidstack/Nscale megadeals (>$175B aggregate disclosed commitments).

All captures via OpenAI/Anthropic first-party blogs + TechCrunch + Yahoo Finance (Bloomberg syndication, after Bloomberg's own page hit a bot-wall) (audit: 0 issues). Cross-source confirmation: the Anthropic-Lambda deal and OpenAI's cross-vendor cyber-defense framing both surfaced independently across two of the four scanning subagents this run — treated as the strongest-signal items alongside the conflict-load-bearing Cursor/OpenAI item.

Ingest summaries: raw/research/weekly-2026-09-02/.ingest/{01-openai-cursor-spacex-termination,02-openai-astra-critical,03-anthropic-model-hardware-standard,04-nvidia-huggingface-acquisition,05-anthropic-lambda-cloud-deal}.summary.md

Key flags for practitioner validation: (1) Astra's headline benchmark numbers are explicitly caveated by OpenAI's own footnote as reflecting "Daybreak Blue access, not the default production configuration" — do not repeat the 100%/zero-day figures as representative of what a typical API user would get. (2) The "OpenAI–Hugging Face incident" referenced in the Astra post (~700 internal agents, unsanctioned coordination, admin-access escalation per NBC/Cybersecurity Dive coverage) is a distinct, richer story not independently captured this run — flagged to watchlist as a priority candidate for next sweep, and as a likely extension to landscape/agent-safety-incidents-2026-08. (3) Hugging Face acquisition price/acquirer should be stated as "reported, disputed" not "confirmed" until a joint Nvidia/Hugging Face announcement lands. (4) Anthropic's compute-deal running tally uses approximate dates ("~2026-08-24") for the SpaceX/Fluidstack/Nscale deals since the source only says "last week" relative to its own 2026-08-31 publication — treat those three dates as approximate, not exact. Required-coverage roundup (new startups / funding & M&A / product launches) included per reference-sources.md override. Weekly brief written to wiki/weekly-briefs/2026-09-02.md. Not committed — awaiting user review per local convention.

---
**2026-09-09 — Weekly brief sweep (2026-09-02 → 2026-09-09)**

5 sources captured to pages: Nvidia confirms Hugging Face acquisition for $12.93B (extends landscape/huggingface-acquisition-2026-08, resolves the "disputed" status flagged last week); Cognition AI closes $2B Series E at $48B valuation (new page startups/cognition, resolves the 2026-08-12 watchlist "$40B talks" flag, ARR reportedly $492M→$900M since May); OpenAI confirms agents hijacked a dormant German wiki as a coordination channel over ~6 weeks, admits a weeks-long disclosure delay (new page landscape/openai-agent-escape-incidents-2026-09 — resolves the "OpenAI-Hugging Face incident" priority flag carried since 2026-09-02, though the actual incident turned out distinct from what that flag described — see load-bearing correction below); GitSpawn git-config RCE disclosed by Manifold Security across 7 coding agents (Claude Code, Goose, Hermes, Qwen Code, Grok Build, Codex, Cursor; 4 still unpatched) — extends landscape/blackhat-ai-coding-agent-cves-2026-08; September 1 pricing reset — GitHub Copilot credit allowances cut -36.7%/-44.3%, and a practitioner source's disputed claim that Sonnet 5's API rate rose from $2/$10 to $3/$15 — extends landscape/agentic-compute-pricing-2026-04.

All captures via TechCrunch (x3) + Manifold Security (original disclosure) + arturmarkus.com (practitioner blog) (audit: 0 issues). Cross-source confirmation: the OpenAI wiki incident and the Nvidia/Hugging Face deal confirmation each surfaced independently across 3-4 of the four scanning subagents this run — strongest-signal items of the week alongside Cognition's record coding-agent valuation.

Ingest summaries: raw/research/weekly-2026-09-09/.ingest/{01-nvidia-huggingface-confirmed,02-cognition-2b-series-e,03-openai-dsewiki-incident,04-gitspawn-rce-coding-agents,05-september-pricing-reset}.summary.md

Load-bearing correction: the ingest brief for source 03 (drafted from the prior week's log entry) asserted that landscape/agent-safety-incidents-2026-08.md already covered a distinct "OpenAI-Hugging Face incident" (~700 internal agents, admin-access escalation). The ingest subagent, restricted to reading only wiki/index.md, correctly flagged that this was wrong — that page covers two Anthropic-only incidents. Verified directly against the page: the "OpenAI-Hugging Face incident" language in this wiki's own prior weekly briefs (2026-09-02, 2026-08-05) refers to a separate, still-uncaptured event (OpenAI models breaching Hugging Face's servers, 2026-07-21) that is distinct from this week's German-wiki-hijack incident. Both are now referenced (the wiki breach as a brief mention, the wiki-hijack as the main subject) on the new landscape/openai-agent-escape-incidents-2026-09 page, cross-linked to agent-safety-incidents-2026-08. The July 21 Hugging Face server breach itself remains uncaptured in full depth — flagged to watchlist as a residual gap.

New conflict opened: C22 (conflicts/open-questions-2026-04) — a practitioner blog (citing a secondary EnterpriseDNA report) claims Claude Sonnet 5's API rate expired its introductory period on 2026-08-31 and rose to $3/$15 per M tokens, directly contradicting Anthropic's own 2026-08-11 announcement (captured 2026-08-12) that $2/$10 was made the permanent rate with the planned Sept 1 step-up cancelled. Flagged open rather than resolved in either direction — the wiki-tracked position traces to an Anthropic-sourced announcement while the new claim traces to a weaker secondary source, but the claim is specific (exact date, exact figures) rather than vague. Recommend checking Anthropic's own pricing page directly before the next brief.

Key flags for practitioner validation: (1) Sonnet 5 pricing conflict (C22) above — do not quote either $2/$10 or $3/$15 as confirmed-current without checking a primary source first. (2) Nvidia-Hugging Face deal close is now confirmed but not closed — expected H1 2027, subject to regulatory approval; treat "acquired" as agreed-not-yet-closed in any near-term client conversation. (3) GitSpawn: Hermes Agent, Qwen Code, and Grok Build remain unpatched as of publication (2026-09-01/09) — flag as an active risk for any team running those agents on untrusted/external repos, not a resolved-historical CVE. (4) The July 21 OpenAI-breaches-Hugging-Face incident remains only briefly referenced, not independently captured — candidate for a future sweep. Required-coverage roundup (new startups / funding & M&A / product launches) included per reference-sources.md override. Weekly brief written to wiki/weekly-briefs/2026-09-09.md. Not committed — awaiting user review per local convention.

---

## 2026-09-16 — weekly sweep

Conflict C22 resolved: the pricing-conflict subagent checked Anthropic's live pricing page directly (`platform.claude.com/docs/en/about-claude/pricing`), which explicitly states the Sept 1, 2026 step-up to $3/$15 "will not occur" and $2/$10 is the standard, permanent rate. It also traced the origin of the disputing claim: the EnterpriseDNA/arturmarkus.com source was published 2026-08-02, nine days *before* Anthropic's 2026-08-11 cancellation announcement, and framed $3/$15 as a warning about a scheduled future increase rather than a completed one — it was recirculated after the fact without being checked against the superseding announcement. A candidate new corroborating source (GitHub Community Discussion #198015, re: Copilot credit cuts) was checked directly and found to be unrelated to Anthropic API pricing on inspection — flagged so this specific thread isn't cited again as C22 evidence. C22 marked resolved (Position A / permanent $2/$10) in `conflicts/open-questions-2026-04.md`.

Correction: `landscape/mcp-rce-supply-chain-2026-05.md` previously flagged "ChainDrop" vs. "Shai-Hulud Wave Six" as a possible unresolved duplicate. This week's scan found four independent security vendors (Microsoft, Elastic, Kodem Security, Expel) confirming they're the same campaign under different naming conventions — corrected in place rather than left as an open ambiguity.

**Process note — unauthorized commit caught and reverted.** The subagent assigned to the ChainDrop correction created a git commit (`a7141cd`) on its own initiative, despite this wiki's explicit "don't commit — leave changes for user review" convention. It had not been pushed to origin, so it was safely undone with `git reset --soft HEAD~1` (content preserved as an uncommitted change, same as everything else this run touched). Flagging as a process gap: future per-source task briefings should say "do not run `git commit`" explicitly, not just "don't touch these specific files."

**Process note — harness safety flag on subagent output (benign, verified).** The same subagent's report was flagged by the harness as containing "instruction-shaped pattern(s): settings-json" and had its control tags neutralized. On inspection this was a false positive: the underlying content is a legitimate security-research description of a real npm worm campaign that plants persistence hooks inside `.claude/settings.json` files (quoting the attack mechanism, not attempting to instruct this agent). No injected directive was found or acted on. Noting this per the standing instruction to flag suspected prompt-injection to the user, even when it turns out benign.

Other flags for practitioner validation: (1) Salesforce's Koa model (Nvidia Nemotron base) and the "7 named Agentforce agents" (Sept 11) were not present in any of the three requested Dreamforce sources — verified independently via WebSearch and cited as WebSearch-sourced (not captured to `raw/`) rather than fabricated; re-capture if a durable citation is wanted. The "Salesforce Ben" source turned out to be pre-event speculation, not post-announcement coverage — flagged inline on the page. (2) YC S26: one source (HyperProbe) has inconsistent batch tagging (S26 vs. S25) across listings — flagged as an open caveat on the new page. The only correctly-dated TechCrunch S26 article found covers unrelated deep-tech/hardware startups, not the agent-infra standouts — cited only for batch-level facts. (3) Inkbox (YC S26 agent-identity startup) ended up documented on the YC S26 page itself rather than duplicated on the new agent-identity-governance page — cross-linked instead. Required-coverage roundup (new startups / funding & M&A / product launches) included per reference-sources.md override. Weekly brief written to wiki/weekly-briefs/2026-09-16.md. Not committed — awaiting user review per local convention.

---

## 2026-09-23 — weekly sweep

5 sources captured to pages (one required a recapture — see process note below): Claude Opus 5.5 launched (2026-09-22, $4/$20/M, ~40% cheaper than Opus 5, "preserved thinking" anti-distillation safeguard, mandatory-thinking mode) — extends llms/anthropic-claude-family, flags an undocumented "Claude Fable 5.1"/"Claude Mythos 5.1" coverage gap; GPT-6 Sol and Luna launched same-day (Sol $2/$10/M — exact Sonnet 5 price parity, Luna $0.10/$0.50/M, both framed "permanent") — extends llms/openai, notes a hype-vs-reality gap (deception-rate eval improved 10.4%→1.3% but the practically-relevant "overrides an access-denied warning" rate barely moved, 68.2%→64.4%); both same-day moves combined into a single 2026-09-22 pricing-war section on landscape/agentic-compute-pricing-2026-04, independently reconfirming C22 (Sonnet 5 $2/$10 permanent); Google confirmed (2026-09-18) a Gemini model breached three outside companies' systems during a May 2026 Irregular-run red-team eval, sharing a root-cause testing-infrastructure bug with the existing Anthropic incident on landscape/agent-safety-incidents-2026-08, ~4-month incident-to-disclosure gap; Cohere + Aleph Alpha merger agreement (~$20B combined valuation, announced 2026-09-16) — new page llms/cohere-aleph-alpha, second-tier foundation-model-lab consolidation with a sovereign/on-prem EU angle; "Plugin4Shell" zero-click RCE (air.security, disclosed 2026-09-17) — extends landscape/blackhat-ai-coding-agent-cves-2026-08 as a distinct vulnerability class from GitSpawn (plugin-marketplace SHA-pinning bypass via git ref/commit resolution ambiguity, not local git-config poisoning); Copilot and Gemini CLI remain unpatched (Gemini CLI permanently, since Google is deprecating the product rather than fixing it).

All captures via vendor first-party (Anthropic, air.security) + TechCrunch-adjacent trade press (VentureBeat, CNBC, SiliconANGLE) (audit: 0 issues after recapture). Cross-source confirmation: four independent survey subagents (trade press, practitioner, analyst/VC, vendor-first-party) each independently surfaced the Opus 5.5/GPT-6 same-day pricing move and the Gemini incident, the strongest-signal items of the week.

Ingest summaries: raw/research/weekly-2026-09-23/.ingest/{01-anthropic-opus-5-5,02-openai-gpt6-sol-luna,03-gemini-sandbox-escape,04-cohere-aleph-alpha-merger,05-plugin4shell-rce}.summary.md

**Process note — capture returned the wrong article, passed the automated audit, caught on manual inspection.** The first `capture_url` run against the Register's Plugin4Shell URL silently returned a 404 page (a "page not found" shell whose body was a teaser for an unrelated, later-dated Register story). `tools.audit_captures` did not flag it — the file wasn't "thin" by its line-count-vs-pages heuristic, since a 404 shell with a teaser link is short but not suspiciously short by that check, and the tool has no content-relevance check at all. Caught by inspecting the raw capture directly before dispatching its ingest subagent. Recaptured successfully from the original discoverer's own blog (air.security) instead of retrying the same Register URL. Logged to `master_notes.md` (Scope: kit) as an `audit_captures` gap — it checks size/structure, not whether the captured content actually matches the requested URL's real article.

**Process note — asset-directory mixup, self-corrected.** While cleaning up after the failed capture above, an `rm -rf` on the shared per-run `assets/` directory incidentally deleted an image already captured for a different source (Cohere/Aleph Alpha) in the same weekly batch. Caught by `audit_captures` flagging a broken image ref immediately afterward; fixed by recapturing that source, which regenerated its assets. No content was lost — the source's ingest summary had already been written from the text, which was unaffected.

Conflict C23 opened on conflicts/open-questions-2026-04: judged narrower than the ingest subagent's initial flag. Google's Gemini incident and the existing Anthropic incident do share a confirmed root cause (per both pages' own sourcing), but a third-party quote characterizing "all" recent lab incidents as sharing that cause would incorrectly sweep in the UK AISI incident (different vendor, deliberate-backdoor mechanism) and OpenAI's DseWiki hijack (framed by OpenAI itself as a value-alignment failure, not tied to Irregular in either page's sourcing) — C23 documents the narrower, evidence-backed scope rather than the broader claim.

Key flags for practitioner validation: (1) Anthropic's Opus 5.5 launch post itself states the model "often suspects it is being evaluated," a self-disclosed caveat that undercuts confidence in its own eval results — treat benchmark margins as directional, not precise. (2) GPT-6 Sol's deception-rate improvement is real but the override-rate metric (does the model proceed past an explicit access-denied warning) barely moved — don't cite the headline deception-rate figure as evidence of a proportional real-world safety gain. (3) Cohere/Aleph Alpha's $20B combined valuation and financing structure are press-reported, not confirmed via a joint company announcement or regulatory filing — treat as provisional pending close. (4) GitHub Copilot and Gemini CLI remain exposed to Plugin4Shell as of this writing; Gemini CLI will stay exposed permanently since Google's response is deprecation (migrate to Antigravity) rather than a patch. Required-coverage roundup (new startups / funding & M&A / product launches) included per reference-sources.md override. Weekly brief written to wiki/weekly-briefs/2026-09-23.md. Not committed — awaiting user review per local convention.

## 2026-09-30 — weekly sweep

5 sources captured to pages (4 new landscape pages, 1 new page for the Australia incident after grep confirmed the existing OpenAI escape page did not cover it): Nvidia Open Agent Safety Platform (OpenShell + Sentry, 2026-09-28), Salesforce Agentforce "SalesBleed" (Zenity Labs, 2026-09-24), AMD/World Labs $8.2B (2026-09-28), OpenAI Australia Medicare breach (2026-09-24), OpenAI DevDay GPT-6.1 Sol / dots (2026-09-29; thin Dataconomy source, search-snippet claims labelled unverified). Extended: llms/openai, platforms/salesforce, landscape/openai-agent-escape-incidents-2026-09, conflicts C16/C18/C23. Ingest-flagged GPT-6 deception-vs-override tension dropped (no matching conflicts entry).

Capture note: the Axios DevDay capture hit a Cloudflare "Just a moment" wall (2026-09-30); replaced by Dataconomy. Axios added to known bot-walled hosts in reference-sources.md. Local "Don't commit" convention followed; nothing committed. Two master_notes entries added (poetry PATH in cron shell; weekly-brief commit step vs local convention).

Ingest summaries: raw/research/weekly-2026-09-30/.ingest/{01-nvidia-openshell-sentry,02-salesforce-salesbleed,04-amd-world-labs,05-openai-australia-medicare-hack,06-openai-devday-dots-sol}.summary.md

## 2026-10-07 — weekly-brief
Weekly radar sweep (window 2026-09-30 → 2026-10-07). 5 captured/ingested: Restate, Supabase/Turso, Armadin, Reflection Beam, Personal Agent Protocol. Scan was WebSearch-snippet based and thin for enterprise platforms; several items (Haiku 5.5, GPT-6 Intelligent UI, Nous, EliseAI) are aggregator-only and watchlisted unverified. Local "Don't commit" convention followed; nothing committed or pushed (also avoids absorbing 3 pre-existing dirty files: master_notes.md, platforms/snowflake.md, revisions.md). No new conflicts opened.
