# Anthropic Claude Model Family

Running page for Anthropic's Claude model family — release timeline, per-model capability / pricing, deployment surfaces, and safety / governance notes. Updated on each release ingest. For enterprise share and adoption see [[llm-api-enterprise-share]]; for coding-LLM specifics see [[ai-app-categories-2025]].

## Release timeline

| Date | Model | Notes |
|---|---|---|
| (prior) | Claude Sonnet 3.5 | Cited as the start of Anthropic's coding lead by Menlo (June 2024) — see [[open-questions-2026-04]] C5 for the "18 months" framing. |
| (prior) | Claude Sonnet 4.5 / Opus 4.5 | "75% of Anthropic customers on Sonnet 4.5 or Opus 4.5 in production" per a16z 2026-04 (see [[llm-api-enterprise-share]]). Referenced in practitioner HN thread as "10–30 min sessions without going wrong" (Opus 4.5) — see [[agents-eating-saas]]. |
| 2026-04-16 | **Claude Opus 4.7** | Replaces Opus 4.6 as default Opus across Claude products. See detail below. |
| 2026-04-20 | **Amazon $5B → Anthropic; $100B / 10-yr AWS commit** | Compute underwriting for Claude's 2026–2036 roadmap. See "Compute infrastructure" below. |
| TBD | Claude Mythos Preview | Referenced in Opus 4.7 launch as a more capable but limited-availability model; Anthropic discloses Opus 4.7 is "less broadly capable than Claude Mythos Preview." |

## Current flagship: Claude Opus 4.7 (2026-04-16)

**One-line:** direct upgrade to Opus 4.6 focused on hard software engineering, long-running agentic tasks, higher-resolution vision, and a new `xhigh` effort level — same pricing, available across Claude products, Claude API, Amazon Bedrock, Google Cloud Vertex AI, and Microsoft Foundry on the same day.

### What's new (per Anthropic 2026-04-16)

- **New `xhigh` effort level** between `high` and `max` — user-facing UX knob for reasoning-vs-latency tradeoff. Default in Claude Code for all plans.
- **Stronger self-verification** — "devises ways to verify its own outputs before reporting back"; "proofs on systems code before starting work."
- **Improved multi-turn thinking** at higher effort on later turns in agentic settings.
- **File-system-based memory** across sessions (cheaper alternative to ever-growing context windows).
- **Stricter literal instruction-following** — can break legacy prompts written for prior models.
- **Updated tokenizer** — 1.0–1.35x input-token expansion depending on content type.
- **Differential training to reduce cyber capabilities** relative to Mythos Preview; automatic cyber-use blocking with **Cyber Verification Program** for legitimate security researchers.

### Pricing (unchanged from Opus 4.6)

- **$5 per million input tokens.**
- **$25 per million output tokens.**
- Net token usage reported favorable on internal coding evals; input tokens can rise 1.0–1.35x due to new tokenizer; output tokens rise at high effort.

### Hard limits (2026-04-16)

- **Vision: images up to 2,576 pixels on the long edge** (~3.75 megapixels; >3× prior Claude models). Meaningful for computer-use agents, document extraction, technical-diagram workflows.
- Rate limits and context window not specified in the release post — re-check Anthropic API docs before quoting.

### Customization / agent hooks

- **Task budgets** (public beta on Claude API) — token-spend guidance across long runs.
- **Claude Code `/ultrareview` slash command** — 3 free uses for Pro / Max plans.
- **Auto mode** extended to Max users — Claude makes decisions on user's behalf for longer unattended runs.

### Vendor-published benchmark lifts vs Opus 4.6 (2026-04-16)

*All numbers are Anthropic-curated partner quotes; not independent leaderboards.*

- **CursorBench**: 58% → 70%.
- **Rakuten-SWE-Bench**: 3× more production tasks resolved.
- **Factory Droids**: +10–15% task-success lift.
- **Notion**: +14% at fewer tokens, 1/3 the tool errors.
- **Hex (internal)**: +13% with 4 tasks neither Opus 4.6 nor Sonnet 4.6 could solve.
- **Databricks OfficeQA Pro**: 21% fewer errors.
- **XBOW visual-acuity**: 54.5% → 98.5% — cleanest vision-improvement datapoint.
- **Harvey BigLaw Bench**: 90.9% at high effort.
- **Finance Agent, third-party GDPval-AA**: state-of-the-art per vendor.
- **Replit**: "same quality at lower cost" (no specific number).
- Devin quote: "works coherently for hours"; Genspark cites **loop resistance** as the top production differentiator.
- Headline **SWE-bench Verified 80.8% → 87.6%** appears in third-party coverage (e.g. MIT Tech Review round-ups) but the extractable text of the Anthropic launch post does not quote it verbatim — the figure lives inside chart images. Treat as vendor-claimed-but-chart-image-only until a cleanly-sourced quote surfaces.

### Safety notes

- Honest disclosures in the launch post: **Opus 4.7 is explicitly *not* Anthropic's most capable model** — "less broadly capable than Claude Mythos Preview."
- Alignment writeup concedes "largely well-aligned and trustworthy, though not fully ideal."
- **Modest regression vs Opus 4.6 on controlled-substance harm-reduction responses** — worth flagging as a release-to-release safety delta rather than an absolute regression.
- **Cyber Verification Program** required for legitimate pentesting / red-team use after new automatic cyber-use blocking.

## Compute infrastructure — Amazon deal (2026-04-20) and Google deal (2026-04-24)

Within five days, Anthropic stacked **two material hyperscaler compute deals** that together commit >10 GW of compute capacity over 5–10 years across two substrates (AWS Trainium + Google Cloud / TPU). Combined notional spend at retail rates >$130B+. See [[../landscape/google-anthropic-40b-2026-04|google-anthropic-40b-2026-04]] for the Google-side detail.

### Amazon deal (2026-04-20)

Amazon adds **$5B** to its Anthropic stake (cumulative: **$13B**) in exchange for a **10-year, $100B AWS cloud commitment** covering up to **5 GW of compute** for Claude training and inference.

### Deal terms

| Element | Detail |
|---|---|
| New Amazon investment | $5B |
| Cumulative Amazon stake | $13B |
| AWS cloud commit | >$100B over 10 years |
| Compute capacity | Up to 5 GW |
| Chip preference | Trainium2, Trainium3 (GA Dec 2025), Trainium4 (pending) + option rights on future Amazon chips |
| Adjacent valuation signal | VC offers (not closed) valuing Anthropic at **$800B+** mid-April 2026 |

### Why it matters

- **Frontier training on Trainium, not Nvidia.** Anthropic's 2026–2036 training runs are structurally committed to Trainium-series silicon. Material NVIDIA-displacement signal at frontier-training layer, compounding Microsoft/AMD + Google/TPU moves. See [[open-questions-2026-04]] C11.
- **Structural CSP coupling — not incidental.** Equity + cloud-commit bundling is now the dominant hyperscaler-lab financing template. Parallels: Amazon contributed $50B into OpenAI's $110B round (Feb 2026); OpenAI↔Azure (primary); Google Cloud↔Gemini (vertical).
- **C3 "direct-to-labs" re-read.** If Claude training *and* inference ride on AWS Trainium, enterprises buying "direct from Anthropic API" are running on AWS compute regardless of procurement channel. The lab-vs-CSP dichotomy in C3's 80% figure likely masks this substrate dependence. Direct-API and Bedrock buyers both sit on AWS iron — only the billing surface differs. See [[../landscape/llm-api-enterprise-share|llm-api-enterprise-share]] and [[open-questions-2026-04]] C3.
- **Model cadence tied to Trainium roadmap.** Trainium3 GA Dec 2025; Trainium4 pending. Future Claude frontier models' timing is now a function of Amazon's silicon schedule, not purely Anthropic's research cadence.

### Open questions (Amazon deal)

- Revenue-share terms: not disclosed.
- Whether Anthropic retains the ability to train on non-Trainium substrate (e.g. continued NVIDIA or Google TPU access via GCP) at scale: article language suggested preference, not exclusivity. **Resolved partial 2026-04-24:** the Google deal answers it — Anthropic does retain non-Trainium scale, materially.
- Inference-capacity floor across the 10-year term: 5 GW is the ceiling; commitment on delivery timing not specified.

### Google deal (2026-04-24)

Per TechCrunch citing Bloomberg (2026-04-24):

| Element | Detail |
|---|---|
| Headline figure | "Up to $40B" |
| Committed now | $10B at $350B Anthropic valuation |
| Contingent | $30B on milestone-hit (terms not disclosed) |
| Compute | 5 GW Google Cloud capacity over 5 years (with room to scale further) |
| TPU | Adds to a prior Anthropic ↔ Google ↔ Broadcom partnership for "multiple gigawatts" of TPU starting 2027 (Broadcom 8-K cited 3.5 GW) |
| Distribution | Anthropic Claude Opus / Sonnet / Haiku already live in Google Cloud Model Garden via GEAP (2026-04-22) — see [[../landscape/google-cloud-next-2026-day2|google-cloud-next-2026-day2]] |
| Adjacent valuation signal | Bloomberg reports $800B+ secondary-market interest mid-April; CNBC reports $900B-valuation talks 2026-04-29; potential IPO as soon as October |

### Combined compute footprint (after both deals)

- AWS Trainium: up to **5 GW**, 10-yr horizon, training preferred.
- Google Cloud: up to **5 GW** general-purpose, 5-yr horizon.
- Google ↔ Broadcom TPU partnership: ≥3.5 GW from 2027.
- CoreWeave: separate datacenter capacity deal in early April (terms not captured).
- Total contracted capacity ceiling: **>13 GW** over 5–10 years.

### Implication for C3 ("direct-to-labs" hosting model)

The 2026-04-23 update read this as "lab-CSP coupling tightens; substrate determines billing surface." That's now too narrow:

- Anthropic is multi-CSP-distributed by design.
- Both top-2 frontier labs (Anthropic, OpenAI) are multi-CSP within the same fortnight.
- The right enterprise procurement question is now "**which lab on which CSP via which billing surface and at what price/perf?**" — no exclusivity to claim either way.

See [[../conflicts/open-questions-2026-04|C3]] for the full reinterpretation, [[../landscape/openai-microsoft-restructure-2026-04|openai-microsoft-restructure-2026-04]] for the parallel OpenAI move.

## Vertical platforms — Claude Finance Agents (2026-05-03)

Anthropic's **first vertical-platform play**, launched 2026-05-03 (announced via news.anthropic.com/news/finance-agents). Marks the move from foundation-model-API to vertical-stack: ten ready-to-run agent templates + Microsoft 365 add-ins + expanded data-partner ecosystem.

### Ten agent templates (all distributed via Claude Cowork plugins, Claude Code plugins, OR Claude Managed Agent cookbooks)

KYC screening, pitchbook building, earnings review, financial model building, market research, valuation review, GL reconciliation, month-end close, statement audit, meeting prep.

### Architecture (per Anthropic 2026-05-03)

Each agent template packages **three components**:

1. **Skills** — instructions and domain knowledge for the task.
2. **Connectors** — governed, real-time access to partner data.
3. **Subagents** — additional Claude models called by the main agent for sub-tasks (e.g., comparables selection, methodology checks).

Plus distribution-side features:
- **MCP apps** (e.g., Moody's) — embed provider tools directly inside Claude. Differentiated tier above plain connectors.
- **Claude Managed Agents** — long-running sessions (multi-hour deal close), per-tool permissions, managed credential vaults, full audit log in Claude Console. Public beta on the Claude Platform.
- **Microsoft 365 add-ins** — Excel, PowerPoint, Word (GA); Outlook coming soon. Context carries automatically across M365 apps.
- **Dispatch feature** — voice or text in Claude Cowork, off-desk task assignment.

### Data-partner ecosystem (2026-05-03)

| Existing partners | New (this launch) | Special tier |
|---|---|---|
| FactSet, S&P Capital IQ, MSCI, PitchBook, Morningstar, Chronograph, LSEG, Daloopa | Dun & Bradstreet, Fiscal AI, Financial Modeling Prep, Guidepoint (100K+ expert transcripts), IBISWorld, SS&C Intralinks (DealCenter AI data rooms), Third Bridge, Verisk | **Moody's MCP app** — credit ratings + 600M+ public/private companies |

### Vendor-cited benchmark

Anthropic claims Claude Opus 4.7 leads the **Vals AI Finance Agent benchmark at 64.37%**. Vendor-cited; Vals's independence not separately verified in this run; flag for cross-confirmation.

### Named customers (2026-05-03)

Citadel (Excel coverage models), FIS (AML investigations from days to minutes; credit decisioning, fraud prevention, deposit retention agents), BNY (Eliza + Claude "digital employees"), Carlyle (firm-wide), Mizuho (meeting prep, client insights), Travelers (Claude Code, engineering productivity), Walleye Capital (100% of 400 employees on Claude Code), Hg (Excel for due diligence and financial modeling).

### Strategic timing

Launches **8 days** after the Microsoft–OpenAI exclusivity restructure (2026-04-27) and **2 days** after Microsoft Agent 365 GA (2026-05-01). Anthropic distributing inside Microsoft 365 estate (Excel/PowerPoint/Word add-ins) is **operational confirmation** that the restructure was strategic prep enabling third-party AI distribution on M365 — not a punitive event. See [[../landscape/openai-microsoft-restructure-2026-04|openai-microsoft-restructure-2026-04]] for the operational-signals discussion.

Same-week parallelism with [[openai|OpenAI Workspace Agents]] (2026-04-22) and [[../platforms/microsoft|Microsoft Agent 365 GA]] (2026-05-01) defines the **three-way enterprise-agent-platform race** (vertical / horizontal / governance).

### Pricing

Not disclosed in source. Plans referenced: all paid Cowork/Code plugin tiers; Managed Agents in public beta on Claude Platform.

### Hype-vs-reality

- "Ten ready-to-run templates" — each is explicitly a **reference architecture** requiring firm-specific adaptation (modeling conventions, risk policies, approval flows). "Ready-to-run" is aspirational for production use.
- Vals Finance Agent benchmark is vendor-cited; no third-party replication.
- M365 integration described as cross-app context carry — not clear whether this is deep API integration or surface-level add-in (same class as Microsoft Copilot add-ins).
- Moody's MCP app coverage figure (600M+ public and private companies) — sourced from Anthropic announcement, not independently verified.

### Build-vs-buy signals

For mid-market financial firms:
- **Anthropic Finance Agents** — fastest to deploy if already on Claude; broad data-partner ecosystem; Moody's MCP app is a genuine lock-in surface.
- **[[../platforms/salesforce|Salesforce Agentforce]] / Financial Services Cloud** — same-week-class Agentforce Operations GA (2026-04-29); deep Salesforce CRM data advantage; different workflow surface.
- **Microsoft Copilot Studio** — incumbent in M365, but Anthropic now competes directly in Excel/PowerPoint/Word/Outlook.
- **In-house on Claude API** — maximum control, months of engineering.

Lock-in surfaces for Anthropic: Moody's MCP app data exclusivity (unconfirmed), Claude Platform credential vaults, Claude Console audit log (compliance workflow dependency).

## Enterprise distribution — OEM and platform expansion (week of 2026-05-11)

Three new distribution datapoints in the same week; all vendor-sourced, none independently verified.

### SAP Business AI Platform / Joule (announced 2026-05-17, SAP Sapphire)

SAP named Claude as the **primary reasoning and agentic engine** for the new SAP Business AI Platform, embedded inside Joule for finance, HR, procurement, and supply chain workflows. Architecture: Claude-powered agents coordinate across S/4HANA, SuccessFactors, Ariba, and external systems via MCP. Described verticals include public sector, healthcare, life sciences, utilities.

**Caveat:** Source is a joint press release (2026-05-17). All claims are forward-looking — "plans to expand," "will collaborate." No GA date, no pricing, no named customer deployments. "Hours of manual effort now takes minutes" is unsubstantiated vendor copy. SAP retains an "open ecosystem" position (any model supported), but designating Claude as "primary" creates switching friction. MCP as the integration layer carries the supply-chain RCE risk documented at [[../landscape/mcp-rce-supply-chain-2026-05|mcp-rce-supply-chain-2026-05]] — relevant for any enterprise pursuing regulated SAP workflows over MCP.

Pattern note: the SAP partnership (ERP) and the Finance Agents launch (2026-05-03) together establish a recurring OEM-embed distribution model distinct from direct-API consumption. See [[../landscape/llm-api-enterprise-share|llm-api-enterprise-share]] for wallet-share implications.

### Claude Platform on AWS — GA (2026-05-11)

Anthropic's own managed-agent stack (not Bedrock) is now GA on AWS. Full feature set: Claude Managed Agents (beta), Advisor strategy (beta), Web search + Fetch, Code execution (Python in-API), Files API (beta), Skills (beta), MCP connector (beta), Prompt caching, Citations, Batch. Models available at GA: **Opus 4.7, Sonnet 4.6, Haiku 4.5**. Billing via AWS invoice, retires against existing AWS commitments; supports most AWS commercial regions plus global and U.S. inference geographies.

**Key non-obvious constraint:** data is **processed outside the AWS boundary** — Anthropic is the data processor, not AWS. Workloads requiring all data to stay inside AWS infrastructure (HIPAA, FedRAMP, EU data sovereignty) must use the Bedrock path, not this one. Vendor blog frames this as a "choice"; it is a hard limitation for regulated industries.

Distribution angle: AWS billing integration (commit retirement) lowers procurement friction without Marketplace-grade reseller overhead. Same-day feature parity vs. Bedrock's historically slower rollout is a meaningful differentiator for teams chasing bleeding-edge agent capabilities. Bedrock customers seeking migration must contact account executives — existing private-offer discounts cannot be applied retroactively.

**Caveat:** Source is an Anthropic launch post (2026-05-11); no independent customer quotes or pricing specifics.

### Lyrie.ai — Anthropic Cyber Verification Program (CVP) acceptance (2026-05-11)

Lyrie.ai (OTT Cybersecurity LLC, Dubai; $2M pre-seed, stealth exit 2026-05-11) was accepted into **Anthropic's Cyber Verification Program (CVP)** — the same dual-use security researcher program introduced with Opus 4.7's automatic cyber-use blocking. CVP acceptance is a lightweight Anthropic endorsement signal for agent-security tooling; not a partnership or certification. Lyrie's core artifact is the **Agent Trust Protocol (ATP)**, an MIT-licensed open standard for agent identity, scope, attestation, delegation, and revocation submitted to IETF. See [[../startups/lyrie|lyrie]].

## Governance signal — declined to fix MCP STDIO RCE (2026-05-08)

OX Security disclosed a by-design RCE in Anthropic's MCP reference SDKs (Python/TypeScript/Java/Rust) affecting **>7,000 publicly accessible servers, >150M downloads**, with **11+ CVEs** assigned this disclosure batch and **5 prior independent disclosures of the same root cause** stretching back >12 months. **Anthropic declined to modify the protocol architecture, citing the behaviour as "expected."**

This is the load-bearing fact for Anthropic-vendor-risk discussion: the protocol shepherd is positioning STDIO-config-to-command as intended behaviour. Defence falls to implementers (sandboxing, network isolation, untrusted-input handling). Combined with vendor-provided MCP-isolation tooling shipping into the same enterprise estate ([[../platforms/microsoft|Microsoft Agent 365]] Defender controls, [[../landscape/google-cloud-next-2026-day2|GEAP Model Armor]], [[../platforms/salesforce|Salesforce Agent Fabric]]), the durable read is "**MCP-fluency-with-isolation**" rather than "MCP-fluency."

See [[../landscape/mcp-rce-supply-chain-2026-05|mcp-rce-supply-chain-2026-05]] for the full incident page.

## Techniques worth stealing

- `xhigh` effort level as a **discoverable, user-facing UX knob** for reasoning-vs-latency.
- **Task budgets** as a cost-governance primitive for long agent runs.
- **File-system-based cross-session memory** as a cheaper alternative to ever-growing context windows.
- **Self-verification-before-reporting** pattern (e.g., Rust TTS→speech-recognizer verification loop).

## Hype-vs-reality delta

- All benchmark numbers are **Anthropic-curated partner quotes**; no head-to-head against GPT-5.4 or Gemini 3.1 Pro is shown in extractable text.
- The "hours-long agentic session" framing is new-release marketing territory — see [[agents-eating-saas]] for the Opus 4.5 practitioner baseline ("10–30 minute sessions without going wrong") against which 4.7 should be measured once HN / Reddit reports accumulate.
- Price held flat at $5/$25 is a **positive signal** for deployed Claude customers and undercuts the "raise prices with every release" pattern.

## Build-vs-buy signals

- For deployed Claude customers, **near-drop-in upgrade** — but mind tokenizer expansion (1.0–1.35× input) and higher output-token count at high effort.
- Vision-resolution step-change (3× prior Claude) materially improves **computer-use agents**, **document-extraction pipelines**, **technical-diagram workflows**. XBOW's 54.5 → 98.5 visual-acuity lift is the cleanest signal.
- **Auto mode + task budgets** close the gap between "chat model you call" and "managed agent harness" — reduces the need for third-party harness tooling for simpler use cases. Watch [[ai-infrastructure-frontiers-2026]] harness tier for the counter-move.
- For build-vs-buy advisory: if the client is already Claude-first, 4.7 is a no-brainer upgrade. If comparing Claude vs GPT-5.4 vs Gemini 3.1 Pro for a new deployment, **don't rely on Anthropic's partner benchmarks alone** — wait for independent SWE-bench / BFCL / GDPval-AA runs before advising.

## Source

- `raw/research/weekly-2026-04-22/02-anthropic-opus-4-7.md`
- `raw/research/weekly-2026-04-23/05-anthropic-aws-5b-100b-2026-04.md` (TechCrunch, 2026-04-20)
- `raw/research/weekly-2026-05-03/02-google-anthropic-40b.md` (TechCrunch citing Bloomberg, 2026-04-24)
- `raw/research/weekly-2026-05-10/02-anthropic-finance-agents.md` (Anthropic news, 2026-05-03)
- `raw/research/weekly-2026-05-10/04-mcp-rce-vulnerability.md` (The Hacker News citing OX Security, 2026-05-08)

## Related

- [[../landscape/llm-api-enterprise-share|llm-api-enterprise-share]]
- [[../landscape/ai-app-categories-2025|ai-app-categories-2025]]
- [[../thesis/ai-apps-layer-2026|ai-apps-layer-2026]]
- [[../thesis/agents-eating-saas|agents-eating-saas]]
- [[../landscape/ai-infrastructure-frontiers-2026|ai-infrastructure-frontiers-2026]]
- [[../landscape/google-cloud-agentic-partner-fund-2026-04|google-cloud-agentic-partner-fund-2026-04]]
- [[../landscape/agentic-compute-pricing-2026-04|agentic-compute-pricing-2026-04]]
- [[../landscape/mcp-rce-supply-chain-2026-05|mcp-rce-supply-chain-2026-05]]
- [[../platforms/microsoft|microsoft]] (Agent 365 governs Anthropic finance agents in M365)
- [[../platforms/salesforce|salesforce]] (competitor for financial-services agents)
- [[openai|openai]]
- [[../conflicts/open-questions-2026-04|open-questions-2026-04]]
- [[../landscape/anthropic-enterprise-distribution-2026-05|anthropic-enterprise-distribution-2026-05]]
- [[../startups/lyrie|lyrie]]
