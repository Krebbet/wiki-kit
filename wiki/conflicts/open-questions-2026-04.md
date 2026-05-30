# Open Questions — 2026-04 Ingest Batch

Consolidated list of claims flagged during the first-batch ingest (6 sources on enterprise AI landscape, 2026-04-22). Each row is a claim that contradicts consensus, contradicts another source, or is asserted without an independent cross-check. None resolved yet; revisit as new sources land.

Convention: **Status** = `open` (needs more evidence or a ruling), `watching` (may resolve itself with time), or `resolved: <outcome>`.

## Flags

### C1 — "Death of the app layer" narrative

- **Claim:** Improving foundation models will eat third-party applications.
- **Source:** Silicon Valley conventional wisdom (pre-2026).
- **Contradicted by:** a16z 2026-04 CIO survey — data shows *continued migration toward* third-party apps, even in DIY-friendly categories like knowledge management and workflow automation.
- **Status:** open — a16z's own data contradicts a widely-held thesis; worth tracking whether Menlo-style portfolio data and independent practitioner sources agree through 2026.
- **Update 2026-04-22 (second ingest):** HN practitioner evidence (see [[agents-eating-saas]]) nuances — not resolves — this. Displacement is **real but slow**, triggered by vendor-side friction (renewal-price spikes, API deprecation) rather than AI capability. At-risk cohort is narrowed to **wide-shallow + PE-owned + renewal-hiking SaaS** (especially niche ERP / CRM >$100k/yr). Narrow-deep + proprietary-data SaaS (Datadog / Tailscale / Stripe-class) is safe. [[lio]] is a concrete "agents execute the workflow" vendor instance in procurement. New axis introduced: **narrow-deep vs wide-shallow** — tracked independently.

### C2 — Enterprise fine-tuning in decline (not rising)

- **Claim:** Enterprises are fine-tuning *less*, not more, over time. Startups diverge (still fine-tuning open-source).
- **Source:** a16z 2025-05, reinforced 2026-04 ("fading in enterprise").
- **Contradicts:** Common assumption that enterprises with proprietary data will increasingly fine-tune.
- **Status:** watching — a16z attributes decline to prompt engineering + cross-model routing. Flag for reversal if RL-fine-tuning or post-training techniques mature.

### C3 — ~80% of enterprises hosting directly with labs

- **Claim:** ~80% of enterprises comfortable hosting directly with the frontier labs (vs via CSPs) by 2026-04, up from ~40% in March 2024.
- **Source:** a16z 2026-04.
- **Contradicts:** "CSPs (AWS Bedrock / Azure AI / Vertex) are the default enterprise procurement path" assumption.
- **Status:** open — big if true. Verify against AWS / Azure / GCP earnings disclosures on AI-workload share; check whether "hosting directly" in the survey includes or excludes proxy-via-CSP-connector arrangements.
- **Update 2026-04-22 (weekly brief):** live counter-signal — Google Cloud announced a **$750M fund for 120,000 partners** at Cloud Next '26 to subsidize GSI-intermediated agentic deployments, with FDE embedding at Accenture / Capgemini / Cognizant / Deloitte / HCLTech / PwC / TCS (see [[../landscape/google-cloud-agentic-partner-fund-2026-04|google-cloud-agentic-partner-fund-2026-04]]). Not a hard contradiction (Gemini API is still the underlying model; GSIs sit on top) but a live tension: if direct-to-lab is dominant, why is Google investing $750M in channel? Possible reconciliations: (a) "direct" = API-contract-direct but deployment help still comes from SIs; (b) GCP specifically lags in direct-to-lab share and is compensating via channel; (c) agentic deployments require more integration labor than pure API consumption, making SIs structurally necessary. Watch for Anthropic / AWS / Azure counter-moves within 6–12 months.
- **Update 2026-04-23 (weekly brief):** the anticipated Anthropic/AWS counter-move arrived. Amazon added $5B to its Anthropic stake (total $13B) in exchange for a 10-year, $100B AWS cloud commitment covering up to **5 GW of compute** with Trainium2–4 chip preference (2026-04-20; see [[../llms/anthropic-claude-family|anthropic-claude-family]]). This is **strong evidence for a new Position B** — *direct-to-lab procurement masks CSP substrate lock-in*. Enterprises buying "direct from Anthropic API" are running on AWS Trainium iron regardless of procurement channel; Bedrock and direct-API buyers both sit on the same compute substrate. Separately (2026-04-22), Google's Gemini Enterprise Agent Platform launch bundles Anthropic Claude Opus/Sonnet/Haiku into the GCP **Model Garden** as a first-class buy path (see [[../landscape/google-cloud-next-2026-day2|google-cloud-next-2026-day2]]); L'Oréal explicitly names "multi-LLM flexibility" as a purchasing criterion for GCP. Labs are simultaneously available via direct API, via home-CSP (Anthropic→AWS, OpenAI→Azure), and via third-CSP (Claude on GCP). The dichotomy is false at the compute substrate layer; useful question becomes **"whose iron + whose billing surface?"** not "direct or not?". Status shift: **watching → open with structural reinterpretation**. Recommend re-framing any enterprise client discussion of hosting-model choice around compute substrate and billing surface, not "lab-direct vs CSP" as a binary.
- **Update 2026-05-03 (weekly brief) — multi-CSP distribution settles as the durable model.** The 2026-04-23 reading ("CSP substrate lock-in masked by direct-to-lab procurement") was itself too narrow. Both top-2 frontier labs are now multi-CSP-distributed at material scale within the same fortnight:
  1. **Microsoft ↔ OpenAI partnership amended (2026-04-27).** Microsoft's IP license through 2032 is now **non-exclusive**; Microsoft no longer pays revenue share to OpenAI; **OpenAI can serve all products to customers across any cloud provider**. Azure remains primary first-launch venue. See [[../landscape/openai-microsoft-restructure-2026-04|openai-microsoft-restructure-2026-04]].
  2. **GPT-5.5 + OpenAI frontier family on AWS Bedrock (2026-04-28)**, limited preview, GA "within weeks". OpenAI now distributes via Azure + AWS Bedrock + direct API.
  3. **Google → Anthropic up-to-$40B + 5 GW Google Cloud (2026-04-24)** — adds GCP-substrate compute on top of the existing AWS Trainium $100B / 5 GW commit. Anthropic now anchored to AWS *and* Google Cloud at material scale. See [[../landscape/google-anthropic-40b-2026-04|google-anthropic-40b-2026-04]].
  
  The settled read: **lab-CSP coupling is real at the financing layer (equity-plus-compute structured deals) but explicitly multi-CSP at the distribution layer.** Enterprises can buy any frontier lab through any of the top-3 hyperscalers within 6 months. Status: **resolved-with-structural-reinterpretation** — the original C3 framing ("80% direct-to-lab" vs "CSPs default") is fully obsolete; replaced by "**which lab on which CSP via which billing surface and at what price/perf?**" as the durable enterprise procurement question. Close C3 on this read; new follow-up question moved to [[#C20]] re: Microsoft IP exclusivity end.

### C4 — "95% of AI initiatives fail"

- **Claim:** 95% of AI initiatives fail (attributed to MIT, circulated summer 2025).
- **Source:** Widely cited; Menlo (2025-12-09) positions against it.
- **Contradicted by:** Menlo's demand-side adoption data and 47% AI-deal conversion rate.
- **Status:** open — need the primary MIT source and a Menlo-independent adoption check before ruling.

### C5 — Anthropic "18 months atop coding leaderboards"

- **Claim:** Anthropic has led LLM coding leaderboards for 18 months since Claude Sonnet 3.5 (June 2024).
- **Source:** Menlo 2025-12-09.
- **Contradicted by:** Public leaderboards (SWE-bench Verified etc.) showing closer gaps; Gemini 3 Pro (Nov 2025) and others have led various evals per model cards.
- **Status:** open — Menlo framing, not a leaderboard-log fact. Treat as editorial; prefer cited benchmark runs when recording Anthropic-coding claims elsewhere.
- **Update 2026-04-22 (weekly brief):** Claude Opus 4.7 release (2026-04-16; see [[anthropic-claude-family]]) adds concrete vendor-published benchmark lifts vs Opus 4.6: CursorBench 58→70, Rakuten-SWE-Bench 3× more production tasks, Factory Droids +10–15%, Hex +13%, Notion +14%, Databricks OfficeQA Pro 21% fewer errors, XBOW visual-acuity 54.5→98.5. Vendor-curated partner quotes, not independent leaderboards. SWE-bench Verified 80.8→87.6 is cited in trade press but chart-image-only in the Anthropic launch post. Supporting evidence for Anthropic's coding lead but does not resolve Menlo's vague "18 months" framing.

### C6 — $37B enterprise AI spend (scope mismatch)

- **Claim:** $37B enterprise generative AI spend in 2025.
- **Source:** Menlo 2025-12-09.
- **Scope:** Explicitly excludes hyperscaler inference revenue, chip revenue (Nvidia), and embedded-AI-feature revenue (e.g., Intuit Assist).
- **Disagrees with:** IDC / Gartner-style headline totals that include those (would be larger).
- **Status:** not a contradiction — scope mismatch. Note scope when reconciling across sources.

### C7 — Cursor "$200M revenue before first enterprise sales rep"

- **Claim:** Cursor reached $200M revenue before hiring its first enterprise sales rep.
- **Source:** Menlo 2025-12-09.
- **Problem:** Widely re-reported with varying figures and dates.
- **Status:** open — need a Cursor-specific source (founder interview, official disclosure) to nail down the precise timing and revenue figure.

### C8 — Coding agents as "AGI for near-term enterprise tasks"

- **Claim:** General coding agents are effectively "AGI for the near-term purposes of most enterprise tasks."
- **Source:** a16z Notes 2026-04.
- **Contradicted by:** Common practitioner view that current agents still fail on long-horizon, ambiguous, or integration-heavy enterprise work.
- **Status:** open — actively flag counter-evidence in practitioner blogs, Hacker News threads, GitHub issue volume on current agents. This is the kind of claim where user-reported friction is the decisive evidence.
- **Update 2026-04-22 (second ingest) — trending toward refuted at specifics:** HN practitioner threads (see [[../thesis/agents-eating-saas|agents-eating-saas]]) provide concrete counter-evidence. Agents fail on **ERP book-closing** (late-cycle accounting), **maintenance-period tracking** (inconsistent source data), **timezone-aware business logic**, **authentication / compliance surfaces requiring IT tickets per system**, and **long-horizon / >100k-line programs**. `swe-rebench` / `swebench-pro` show a wall on maintenance even as greenfield expands. Second practitioner thread on agent revenue ([[../thesis/agents-eating-saas|agents-eating-saas]] §Autonomous-agent revenue reality) adds: **intelligence is not the bottleneck** — CAPTCHAs, spam-flagging of cold outreach, and zero distribution are. Status: open but trending toward **refuted-at-specifics**; watch for updated a16z claim or concrete counter-evidence.
- **Update 2026-04-23 (weekly brief):** two market signals from opposite directions, both supporting Position A at the coding use case:
  1. **SpaceX option to acquire Cursor for $60B (2026-04-21).** Market willing to pay 30x ARR for a coding *harness* that has no proprietary frontier model — i.e., the harness is real and enterprise-adopted at scale. See [[../landscape/spacex-cursor-60b-option-2026-04|spacex-cursor-60b-option-2026-04]]. Counter-signal inside the same source: SpaceX IPO-theater framing, no moat.
  2. **GitHub paused Copilot Pro signups (2026-04-21).** Agent-mode workloads consume compute at rates that break flat-subscription economics — direct evidence that individual developers are running enough production-scale coding-agent workflows to stress vendor infrastructure. See [[../landscape/agentic-compute-pricing-2026-04|agentic-compute-pricing-2026-04]].
  The failure mode has shifted: C8's debate is no longer "do agents work?" (they work well enough to break pricing) but "can we afford to run them, and do they generalize beyond coding?" Position A strengthened at the coding use case; the **generalization-beyond-coding** side of the original C8 claim remains untested. Status: refuted-at-specifics-for-non-coding, supported-for-coding; continue watching.
- **Update 2026-05-03 (weekly brief):** harness-as-runtime evidence keeps compounding at the coding use case. Cursor 3.2 (2026-04-24) ships `/multitask` async parallel subagents, expanded worktrees, multi-root workspaces — Futurum analyst frame: "Cursor is an agent execution runtime with a built-in code surface, and vendors competing on IDE capability alone are mispositioned against it." Vendor-curated 37% SWE-bench Multilingual lift over Composer 1.5. See [[../startups/cursor|cursor]]. C8 Position A at the coding-harness layer continues to compound; the generalization-beyond-coding side of C8 remains untested in this run.
- **Update 2026-05-10 (weekly brief) — first concrete non-coding evidence at scale.** Sierra ($950M Series D / $15B+ post-money, 2026-05-04; Tiger Global + GV; Bret Taylor) reports **$150M ARR (Feb 2026) across customer-experience agents** spanning mortgage refinancing, insurance claims processing, product returns, nonprofit fundraising — at a self-reported 40%+ Fortune 50 penetration. See [[../startups/sierra|sierra]]. This is the **strongest publicly-disclosed non-coding agent-vertical scale data point to date**, but with caveats: (i) all figures are vendor self-reported; (ii) Bret Taylor's dual role as Sierra CEO and OpenAI chairman is a conflict-of-interest surface; (iii) "billions of interactions" framing is unaudited. Weight at 0.7 — strengthens generalisation-side evidence but does not close the conflict. Concurrent same-week launches of [[../llms/openai|OpenAI Workspace Agents]] (admin-builder), [[../llms/anthropic-claude-family|Claude Finance Agents]] (vertical), and [[../platforms/microsoft|Microsoft Agent 365]] (governance) are vendor *bets* on non-coding agent traction, not yet evidence of scale. Status updated: **trending toward refuted-at-specifics-resolved with caveats** — the original "general agents = AGI for near-term enterprise tasks" framing is too strong; the durable read is "**vertical-deep agents work at scale within regulated workflows; horizontal-general agents remain unproven outside coding**." Continue tracking through 2026-Q3 for Sierra-class non-coding proof points beyond Sierra itself.

### C9 — ">$1B new coding-startup revenue in 2025"

- **Claim:** Coding startups generated ">$1B of new revenue in 2025 alone."
- **Source:** a16z Notes 2026-04 — specific but unsourced in the post.
- **Directionally consistent with:** Menlo's $4.0B 2025 departmental-coding spend figure (but that includes incumbents, not just startups).
- **Status:** open — corroborate with revenue disclosures from named coding startups (Cursor, Anysphere, Claude Code enterprise line, etc.).

### C10 — Snowflake NRR "stabilized at 125%"

- **Claim:** Snowflake 125% NRR has "stabilized" (management framing, 2025-12-03).
- **Source:** Snowflake Q3 FY26 earnings, via SaaStr 2025-12-03.
- **Contradicted by:** SaaStr's reading of the 158 → 171 → 135 → 127 → 125 multi-quarter trend.
- **Status:** watching — resolves with FY27 earnings: does NRR bottom at 125%, drop further, or re-accelerate?

### C11 — BVP "next-wave" inference inflation

- **Claim:** The 2024 inference-infrastructure cohort (**Fireworks, Baseten, Together, Fal**) has either "won" or been commoditised; the 2026 frontier is **TensorMesh, RadixArk, Inferact, Gimlet Labs**.
- **Source:** Bessemer Venture Partners, AI Infrastructure Roadmap 2026 (see [[ai-infrastructure-frontiers-2026]]).
- **Problem:** Bessemer is an active VC in this category and does not disclose which 2026 names are portfolio. "First wave → next wave" framing is the standard VC re-pitch pattern. The 2024 names still appear in [[ai-app-categories-2025]] as current-layer infra.
- **Status:** open — worth independent confirmation (Fireworks / Baseten / Together / Fal revenue disclosures; independent benchmarks of TensorMesh / RadixArk / Inferact / Gimlet Labs). Do not adopt BVP's first-wave / next-wave framing in client advisory without a second source.
- **Update 2026-04-23 (weekly brief):** adjacent but orthogonal signal — Anthropic's $5B/$100B/10-yr AWS deal commits to Trainium2/3/4 silicon (see [[../llms/anthropic-claude-family|anthropic-claude-family]]). Independent of BVP's "inference wave" framing, this is a material frontier-training volume bet against NVIDIA at the lab layer. Combined with Microsoft/AMD and Google/TPU moves, custom-silicon substitution is accelerating at hyperscaler scale. BVP's taxonomy operates at the *inference* layer; the relevant 2026 story may be **training-silicon de-GPU-ification** as much as inference-startup bifurcation. Note as signal; do not update the specific wave-1/wave-2 claim either direction without benchmark data.
- **Update 2026-05-03 (weekly brief):** the de-GPU-ification thesis strengthens. Anthropic-side: Google ↔ Anthropic up-to-$40B + 5 GW GCP (2026-04-24) adds TPU-substrate scale on top of Trainium (see [[../landscape/google-anthropic-40b-2026-04|google-anthropic-40b-2026-04]]). OpenAI-side: TechCrunch (2026-04-27) cites the Amazon deal at "$50B-class" plus a $20B+ Cerebras commit (Reuters, 2026-04-17) — meaning OpenAI's frontier training is now spread across Azure (NVIDIA + Maia) + AWS + Cerebras silicon. Both top-2 labs are explicitly multi-vendor at the silicon layer. NVIDIA-displacement at frontier training is no longer hypothesis; it's procurement reality. C11's specific "wave-1 / wave-2 inference startups" claim still requires direct revenue / benchmark data — not addressed by this signal.

### C12 — "78% of AI failures are invisible" (arXiv citation suspect)

- **Claim:** "78% of AI failures are invisible" and "these patterns persist across 93% of cases even with more powerful models."
- **Source:** BVP cites arXiv `2603.15423`.
- **Problem:** The arXiv ID format is suspect — needs verification that the paper exists, is legitimate, and actually supports the claims BVP attributes to it. `2603.15423` implies March 2026 per the YYMM prefix convention; plausible but worth checking.
- **Status:** open — fact-check before any promotion to client material. If the paper is real and supports the claim, upgrade to a referenced fact; if not, remove from [[ai-infrastructure-frontiers-2026]].

### C13 — Practitioner revenue skepticism vs enterprise-spend figure

- **Claim A** (HN practitioners, 2026-04): "Few, if any, are currently legitimately making money using AI Agents directly. Most of the money is in courses and bootcamps."
- **Claim B** (Menlo Ventures, 2025-12-09, see [[enterprise-ai-market-2025-2026]]): $37B enterprise generative AI spend in 2025; $19B at the application layer; ≥10 products at $1B+ ARR, 50 at $100M+ ARR.
- **Tension:** If most spend is going to **model APIs, copilots, and hosted-vendor products** (which Menlo's scope captures) rather than **autonomous agents monetising per-task revenue**, the two claims can both be true. The open question is what share of the $19B app-layer spend is actually going to **agents** specifically vs **copilots / chat products / vertical AI apps**.
- **Status:** open — resolve by decomposing Menlo's app-layer spend into copilot / vertical-AI / agent-platform buckets and comparing to HN practitioner revenue framing. Menlo's data (see [[../landscape/ai-app-categories-2025|ai-app-categories-2025]]) gives copilots **$7.2B of $8.4B horizontal AI** — an indirect answer: most spend is **copilots and vertical AI**, not autonomous agents. Consistent with HN view; practitioner claim is likely correct but scoped to autonomous-agent-as-business, not to agent-feature-embedded-in-app spend.
- **Update 2026-04-23 (weekly brief):** both sides reinforced simultaneously this week:
  - **Bubble-side:** SpaceX $60B option on Cursor at an implied ~30x ARR multiple (see [[../landscape/spacex-cursor-60b-option-2026-04|spacex-cursor-60b-option-2026-04]]); article's own framing concedes IPO value-add motivation and SpaceX "losing money."
  - **Real-spend side:** GitHub Copilot Pro signup pause because agent workloads are consuming compute at "order-of-magnitude" higher rates than 6 months prior (see [[../landscape/agentic-compute-pricing-2026-04|agentic-compute-pricing-2026-04]]). Vendors tier their products — Pro+ is now ">5X Pro limits" — implying real consumption variance, not hollow subscription revenue.
  Refined read: the Menlo-vs-HN revenue-reality split is probably resolving toward a **three-tier picture**: (1) copilots and vertical-AI apps = $15B+ real spend; (2) agentic coding tools = real spend but mis-priced at the subscription tier, forcing 2026 repricing; (3) autonomous agent-as-business = still vaporware outside narrow verticals. The bubble is specifically in the **valuation** layer (SpaceX 30x on Cursor), not the **revenue** layer.

### C14 — Which continual-learning architecture wins?

- **Claim:** BVP positions continual-learning systems (test-time training, cartridges, sliding-window transformers, meta-learning-at-inference) as a real 2026 frontier — see [[ai-infrastructure-frontiers-2026]] §2.
- **Open question flagged by BVP itself:** which point on the spectrum (moonshot new architectures vs incremental transformer patches) wins is undetermined; new benchmarks beyond needle-in-haystack are needed.
- **Status:** open — no resolution path in current sources. Watch for: published benchmark comparing Learning Machine / Core Automation / Sublinear Systems / Stanford-NVIDIA TTT against frozen-weights baselines on a multi-session task.

### C15 — RL-platforms category leadership

- **Claim:** BVP positions **Mercor, Turing, micro1** as "first wave" (human-labelling) and insufficient for the next wave (interaction-based learning / RL platforms).
- **Problem:** Mercor, Turing, and micro1 are still actively selling data-labelling services at scale in 2026. BVP's framing is forward-looking and self-interested.
- **Status:** open — requires a second source (independent market-share data, or a Mercor / Turing quarterly revenue disclosure) to confirm whether the category is truly bifurcating or BVP is talking its book.

### C16 — World models: substrate or robotics-only niche?

- **Claim:** BVP asserts world models could extend beyond robotics / AVs into defence, healthcare, industrial ops, enterprise planning — see [[ai-infrastructure-frontiers-2026]] §5.
- **Status:** open — BVP explicitly flags this as unproven in their own source. Watch for non-robotics production deployments of Reka, Decart, World Labs, or AMI Labs.

### C17 — "Everything as MCP / API / CLI" — industry norm or Salesforce-specific?

- **Claim:** Salesforce Headless 360 (2026-04-15) pivots the platform to expose every capability as APIs / MCP tools / CLI commands for agents. See [[../platforms/salesforce|salesforce]].
- **Open question:** does this pattern spread to Microsoft Dynamics, SAP, Oracle, Workday, ServiceNow, HubSpot within 12 months?
- **Implications:** if yes, **structural pivot** that reshapes build-vs-buy — incumbents collectively refuse to be disintermediated, and agents become a *layer over* existing SaaS rather than a *replacement for* it. This directly affects [[../thesis/agents-eating-saas|agents-eating-saas]]'s three-way framing. If no, it's a single-vendor defensive play.
- **Status:** watching — 12-month horizon. Flag any Microsoft / SAP / Oracle / Workday / ServiceNow / HubSpot headless-API / MCP-tool announcement as a direct signal.
- **Update 2026-04-23 (weekly brief) — upgraded from single-vendor watching to emerging industry norm.** Two independent vendors shipped structurally identical MCP-first patterns within 8 days of Salesforce:
  1. **Snowflake Intelligence + Cortex Code (2026-04-21)** — MCP connectors (Gmail, Jira, Salesforce, Slack, Google Suite) for business-user agent; MCP + ACP support + VS Code extension + Claude Code plugin for builder agent; Agent SDK (Python + TypeScript). See [[../platforms/snowflake|snowflake]].
  2. **Google Cloud Gemini Enterprise Agent Platform (2026-04-22)** — Agent Gateway as unified API connectivity layer; ADK with native MCP integration (L'Oréal quote: "through Model Context Protocol, they are securely connected"); Agent Studio programmatic export; Agent Identity + Registry + Gateway governance trio. See [[../landscape/google-cloud-next-2026-day2|google-cloud-next-2026-day2]].
  Three major platforms (one CRM incumbent, one data-platform incumbent, one hyperscaler) converging on the same "everything as MCP / API / CLI for agents" pattern within one week is decisive. C17's original 12-month watch window is effectively pre-concluded at <2 weeks: **this is the industry norm, not a Salesforce defensive play.** Status: **trending toward resolved-confirmed** — watch the remaining named candidates (Microsoft Dynamics, SAP, Oracle, Workday, ServiceNow, HubSpot) for follow-through; expect most to ship equivalents by end-Q3 2026. Implication for client advisory: **MCP fluency is now a platform-selection criterion**, not an optional integration question.
- **Update 2026-05-10 (weekly brief) — REOPENED with Position B: MCP RCE supply-chain disclosure.** OX Security disclosed (2026-05-08) that Anthropic's MCP STDIO transport enables RCE by design across all 4 reference SDKs (Python/TypeScript/Java/Rust), affecting **>7,000 publicly accessible servers, >150M downloads**, with **11+ CVEs assigned this batch** and **5 prior independent disclosures of the same root cause stretching back >12 months**. **Anthropic declined to modify the protocol architecture, citing the behaviour as "expected."** See [[../landscape/mcp-rce-supply-chain-2026-05|mcp-rce-supply-chain-2026-05]] for full incident detail.

  **Position A (resolved-confirmed, 2026-04-23 update):** MCP fluency is now a platform-selection criterion across the enterprise stack — Salesforce + Snowflake + Google all converged within 8 days. Evidence remains accurate; nothing in the disclosure undermines the standardisation reality.

  **Position B (new, this run):** MCP fluency means **inheriting an unfixed protocol-level RCE surface** across all 4 reference SDKs; vendor-provided MCP-isolation (Google Model Armor + Agent Gateway, Salesforce Agent Fabric, Microsoft Agent 365 Defender controls + MCP server context mapping, Snowflake Cortex sandboxing) becomes the **actual procurement criterion**, not raw MCP support. Pure MCP adoption without isolation is now a CVE-inheritance risk.

  **Both positions are simultaneously true.** The wiki position evolves to "**MCP-fluency-with-isolation**" rather than "MCP-fluency." Practical consequences:
  1. Microsoft's [[../platforms/microsoft|Agent 365 MCP server context mapping]] (June 2026 preview) becomes a load-bearing differentiator, not a footnote.
  2. Google's [[../landscape/google-cloud-next-2026-day2|Model Armor]] dual-purpose (governance + CVE defence) framing is now the right read.
  3. Pure-play harness/eval startups ([[../landscape/ai-infrastructure-frontiers-2026|Bigspin, Braintrust, Judgment Labs]]) without an MCP-isolation story face an uphill differentiation battle vs bundled-into-existing-SKU governance vendors.
  4. Alternative protocols (A2A, ANP, proprietary connector frameworks like OpenAI Workspace Agents' connector layer — see [[../llms/openai|openai]]) gain a clean differentiation pitch: "adopt our protocol and you don't inherit MCP's RCE surface."
  5. **Anthropic-vendor-risk discussion** must include the protocol-shepherd-declined-to-fix governance signal, not just model-quality signals.

  Status: **OPEN — reopened with Position B**. Resolution path is whether (a) Anthropic eventually patches the reference implementation under industry pressure (12-month watch), or (b) MCP-isolation tooling becomes universal enough that the substrate vulnerability becomes a non-issue at the procurement layer.

- **Update 2026-05-17 (weekly brief) — two datapoints, one per position.**
  1. **C17 follow-through (Position A):** SAP — a named C17 watch-candidate — confirms the pattern. The SAP Business AI Platform / Joule + Claude announcement (SAP Sapphire, 2026-05) routes Claude to SAP enterprise systems "and other tools connected through **MCP**." That is the 4th named incumbent (after Salesforce / Snowflake / Google) shipping MCP-first agent connectivity; the original 12-month watch is now effectively concluded for the major-platform tier. Caveat: forward-looking PR, no GA. See [[../landscape/anthropic-enterprise-distribution-2026-05|anthropic-enterprise-distribution-2026-05]].
  2. **Position B resolution-path-(b) signal:** Lyrie.ai (stealth-exit, $2M pre-seed, 2026-05-11) proposes the **Agent Trust Protocol (ATP)** — an open cryptographic standard for agent identity / scope / attestation / revocation, slated for IETF submission, MIT reference impl, accepted into Anthropic's Cyber Verification Program. This is an early instance of the resolution-path-(b) bet (protocol-level isolation/trust tooling emerging around MCP's substrate). Heavily caveated: $2M pre-seed, IETF *in-process not ratified*, "SSL/TLS-for-agents" framing is vendor marketing. Tracks as a watch signal, not a resolution. See [[../startups/lyrie|lyrie]].

  Net: Position A's "industry norm" reading strengthens (SAP follow-through); Position B's resolution-path-(b) gains its first concrete tooling datapoint but nowhere near universality. Status unchanged: **OPEN — reopened with Position B**.

### C18 — Salesforce Agent Fabric multi-vendor governance — real or marketing?

- **Claim:** Salesforce Agent Fabric is a multi-vendor agent control plane with deterministic orchestration and centralized governance across non-Salesforce LLMs / agents / tools (2026-04-15; see [[../platforms/salesforce|salesforce]]).
- **Problem:** single-source vendor launch post. If real, it's a major land-grab for the control-plane tier over competing harness startups (Bigspin / Braintrust / Judgment Labs in [[../landscape/ai-infrastructure-frontiers-2026|ai-infrastructure-frontiers-2026]]). If Salesforce-agents-only with superficial multi-vendor branding, it's marketing.
- **Status:** open — verify by testing Agent Fabric against a non-Salesforce agent (OpenAI Codex, Claude Code, or an independent vendor agent) in the next research pass or via a practitioner post / G2 review.
- **Update 2026-04-23 (weekly brief):** indirect signal. Google's **GEAP Agent Gateway + Agent Identity + Agent Registry** (2026-04-22; see [[../landscape/google-cloud-next-2026-day2|google-cloud-next-2026-day2]]) is structurally identical to Salesforce Agent Fabric — multi-vendor, cross-environment governance with centralized control plane. GEAP explicitly governs "every agent — whether built on Agent Platform or sourced from our partner ecosystem." Snowflake's Cortex Code also ships multi-vendor (AWS Glue, Databricks, Postgres, Claude Code plugin) (see [[../platforms/snowflake|snowflake]]). Independent convergence from two more vendors on the control-plane pattern **increases confidence the architectural category is real** (i.e., genuine enterprise demand), but does not directly resolve whether Salesforce's specific implementation is actually multi-vendor or superficial. Status unchanged — still needs a practitioner test. Adjacent verdict: the control-plane **tier** is real and hyperscaler-table-stakes; whether any specific vendor's multi-vendor claim holds up is a per-vendor question.

### C20 — Microsoft IP-exclusivity end: Azure tail-revenue or accelerating substitution?

- **Claim:** Microsoft's amended OpenAI partnership (2026-04-27) converts Microsoft's IP license through 2032 to **non-exclusive** and **eliminates Microsoft's outbound revenue share to OpenAI**, while preserving Azure's first-launch primacy and OpenAI→Microsoft revenue share through 2030 (subject to a total cap, new term). See [[../landscape/openai-microsoft-restructure-2026-04|openai-microsoft-restructure-2026-04]].
- **Open question:** is Microsoft monetising a long tail (IP optionality + ongoing revenue share + Azure infrastructure capture) while OpenAI's IP advantage gradually erodes — or is this an early signal that **Microsoft expects OpenAI's IP advantage to narrow faster than its own distribution advantage compounds**, and is proactively reducing exposure to a single-supplier dependency?
- **Implications:** If "long-tail monetisation" — Microsoft is locking in revenue while it still has leverage; expect continued Microsoft-Copilot first-party investment and Muse Spark series acceleration. If "preparing for substitution" — watch for Microsoft 365 Copilot adopting non-OpenAI frontier models (Claude, Gemini) within 6–12 months and corresponding deprecation of OpenAI-exclusive marketing language.
- **Status:** open. Resolves over 6–12 months by:
  1. Whether Microsoft 365 Copilot ships meaningful non-OpenAI model integration as a first-class feature (not just experimental).
  2. Whether Muse Spark / future Microsoft proprietary models materialize as distribution defaults inside Microsoft surfaces (vs OpenAI as the default).
  3. Whether OpenAI's enterprise spend share ([[../landscape/llm-api-enterprise-share|llm-api-enterprise-share]]) shows continued share decline through 2026.
- **Update 2026-05-10 (weekly brief) — leans toward "governance-of-multi-vendor-estate" read.** Three operational signals within 11 days strengthen Position A (governance bundling, not pure long-tail):
  1. **OpenAI Workspace Agents launch (2026-04-22)** — successor to Custom GPTs in ChatGPT Enterprise; Codex-powered cloud harness; credit pricing from 2026-05-06. OpenAI moves enterprise spend up the value chain into agent-platform territory; the diversification the restructure was strategic-prep for is now operational. See [[../llms/openai|openai]].
  2. **Microsoft Agent 365 GA (2026-05-01)** — Microsoft's enterprise agent governance / control plane, bundled in M365 E7 or USD 15/user/month standalone. Explicitly governs **OpenAI agents (now non-exclusive), Anthropic agents, OpenClaw, Claude Code, partner agents** when those agents touch the M365 estate. See [[../platforms/microsoft|microsoft]]. Microsoft monetises governance over the multi-vendor estate it has just unlocked, regardless of which model vendor wins long-term.
  3. **Anthropic Claude Finance Agents inside M365 (2026-05-03)** — Anthropic launches its first vertical platform with Excel/PowerPoint/Word add-ins (Outlook coming) — distributing inside Microsoft 365 estate within 8 days of the restructure. Third-party AI on Microsoft surfaces is now operational reality. See [[../llms/anthropic-claude-family|anthropic-claude-family]].

  Read: Microsoft's hedge is **"win governance over the multi-vendor estate, regardless of the model winner."** Less "preparing for substitution" or "tail-monetising IP optionality"; more "**collect rent on every agent that touches M365, whoever built it.**" Resolution paths #1 (non-OpenAI model in M365 Copilot) and #2 (Muse Spark) remain open; #3 (OpenAI share decline) is the trailing indicator. Status remains open through 2026-Q4 but the early signal favours the governance-bundling read.

### C19 — C3 Code self-commissioned benchmark

- **Claim:** C3 Code scores 9.2/10 overall vs Palantir AIP / AI FDE 7.7, OpenAI Codex 6.0, Claude Code 5.2 — including 10/10 on "Domain Intelligence" vs Claude Code's 3 (C3-commissioned evaluation, 2026-03-20; see [[c3-ai]]).
- **Problem:** vendor-run evaluation with vendor-selected dimensions, vendor-chosen judge (Claude), documentation as the only input, and category mismatch (general-purpose coding agent vs domain-specific enterprise platform).
- **Status:** flag-only — do not cite the 9.2 as a standalone comparison. Only quote as "C3-reported" when discussing C3's own positioning. If an independent benchmark comparing these categories emerges, update here.

### C21 — AgentCore Payments "first managed agent payment" vs Google AP2 primacy

- **Claim:** Amazon Bedrock AgentCore Payments (preview, 2026-05-17) is "the first managed payment capabilities purpose-built for autonomous agents" (AWS first-party blog). See [[agentcore-payments-x402-2026-05]].
- **Contradiction:** the same source lists Google's **AP2** (Agent Payments Protocol, announced Cloud Next '26, 2026-04-22; see [[google-cloud-next-2026-day2]]) alongside x402 / ACP / MPP as existing "pioneering" agent-commerce protocols — i.e. AWS claims a "first" in a field it simultaneously acknowledges has prior art.
- **Crux (load-bearing):** the claim turns entirely on the **protocol-vs-managed-platform** distinction. AP2 is an open protocol spec; AWS's claim is for a *managed* rail (hosted settlement, wallet provisioning, session spend caps). Whether that distinction makes "first managed" defensible is unresolved and the source does not unpack it.
- **Status:** flag-only — do not repeat "first managed agent payments" as fact; attribute as "AWS-claimed." Resolution signal: an independent comparison of AP2-managed offerings (Google) vs AgentCore Payments, or a Google managed-AP2 GA announcement, would settle primacy. Not a speculative-future conflict — concrete contestable vendor claim with a named counter.

## Process note

Per `wiki/CLAUDE.md`, conflicts should be elevated for rulings. For this first batch, most items don't have enough triangulating evidence for a ruling — they're *opened* flags, not *resolved* conflicts. Revisit when:

- A second independent source covers the same claim.
- Primary data (earnings transcript, benchmark leaderboard log, MIT paper) surfaces.
- Time passes enough to settle a "watching" item (e.g., Snowflake's next earnings).

## Source

Claims captured across:

- `raw/research/enterprise-ai-landscape-2026/01-a16z-arms-race-2026.md`
- `raw/research/enterprise-ai-landscape-2026/02-menlo-state-2025.md`
- `raw/research/enterprise-ai-landscape-2026/04-a16z-notes-2026.md`
- `raw/research/enterprise-ai-landscape-2026/06-saastr-databricks-snowflake.md`
- `raw/research/weekly-2026-04-23/01-google-cloud-next-2026-day2.md`
- `raw/research/weekly-2026-04-23/02-snowflake-intelligence-cortex-code-2026-04.md`
- `raw/research/weekly-2026-04-23/03-spacex-cursor-60b-option-2026-04.md`
- `raw/research/weekly-2026-04-23/04-github-copilot-pro-plan-2026-04.md`
- `raw/research/weekly-2026-04-23/05-anthropic-aws-5b-100b-2026-04.md`
- `raw/research/weekly-2026-05-03/01-openai-microsoft-restructure.md`
- `raw/research/weekly-2026-05-03/02-google-anthropic-40b.md`
- `raw/research/weekly-2026-05-03/04-cursor-3-2-multitask.md`
- `raw/research/weekly-2026-05-03/05-deepseek-v4.md`
- `raw/research/weekly-2026-05-10/01-sierra-950m-series-d.md`
- `raw/research/weekly-2026-05-10/02-anthropic-finance-agents.md`
- `raw/research/weekly-2026-05-10/03-microsoft-agent-365-ga.md`
- `raw/research/weekly-2026-05-10/04-mcp-rce-vulnerability.md`
- `raw/research/weekly-2026-05-10/05-openai-workspace-agents.md`
- `raw/research/weekly-2026-05-17/01-agentcore-payments-x402-2026-05.md`
- `raw/research/weekly-2026-05-17/02-sap-anthropic-business-ai-2026-05.md`
- `raw/research/weekly-2026-05-17/03-claude-platform-on-aws-2026-05.md`
- `raw/research/weekly-2026-05-17/04-lyrie-agent-trust-protocol-2026-05.md`
- `raw/research/weekly-2026-05-17/05-openai-deployment-company-2026-05.md`

## Related

- [[enterprise-ai-market-2025-2026]]
- [[llm-api-enterprise-share]]
- [[ai-app-categories-2025]]
- [[databricks]]
- [[snowflake]]
- [[ai-apps-layer-2026]]
