# Wiki Log

Append-only chronological record of wiki activity.

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
