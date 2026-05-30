---
setup_approved: 2026-04-23
---

# Watchlist

Running list of offerings / companies / signals surfaced during weekly radar sweeps that didn't merit full capture and ingest but are worth tracking for future research. Oldest at the top; most recent at the bottom.

## Convention

Each entry: `[YYYY-MM-DD] <topic / name> — <1-2 sentence reason> — <URL or pointer>`.

Cleanup policy: after ~3 months with no second signal, entries can be pruned during `/lint` or left as cold references. Entries that graduate to full pages can be left here with a `→ [[page-name]]` pointer, or removed.

---

## 2026-04-22 — weekly sweep

### Model releases this week (2026-04-15 → 2026-04-22)

- **Gemini 3.1 Ultra** — Google frontier model with 2M-token context window, native multimodal (text / image / audio / video). Landscape-level — when we next ingest on LLM-share, this should factor in. (Google release, April 2026.)
- **Gemini 3.1 Flash TTS** (2026-04-15) — "most controllable AI voice model"; granular natural-language control over speaking style, pace, pitch, emphasis. Relevant for voice-agent tooling.
- **xAI Grok 4.20** — factuality-focused release; highest factuality on news events published in prior 30 days per vendor-published benchmarks.
- **NVIDIA NeMoCLAW + OpenCLAW** — enterprise agent orchestration frameworks announced at GTC 2026. Track if they ship open-source.
- **ThinkingAI + MiniMax "Agentic Engine"** — joint enterprise-agent launch (2026-04-16). Signal-low; confirm substance.

### Funding this week

- **Bluefish $43M Series B** — agentic marketing / AI visibility control.
- **Synera $40M Series B** — agentic AI for industrial engineering workflows.
- **Hilbert $28M Series A** — agentic AI that automates growth decisions.

### YC W26 / recent YC launches to profile

- **Kuli** — AI agent for social media and influencer-marketing teams; watches every video and helps marketers launch 4x faster.
- **Bravi** — AI operating system for home-services businesses (already surfaced in [[yc-w26-ai-batch]] named-only).
- **Brickanta** — hundreds of construction-specific AI agents.
- **Lab0** — agentic systems that automate enterprise software implementation (months → weeks).
- **Runtime** — sandboxed environments + session observability + configurable guardrails for coding agents in enterprise. **Strong fit for [[ai-infrastructure-frontiers-2026]] harness tier + [[ai-apps-layer-2026]] coding agents.**

### Infrastructure / operational

- **Equinix Fabric Intelligence** (2026-04-15) — AI-native operational layer for enterprise networking. Not tracked yet; re-visit if a client has data-center / networking buy-side questions.

### Skipped from this run

- **OpenAI Codex enterprise scaling** (openai.com/index/scaling-codex-to-enterprises-worldwide/) — **capture timed out twice** (30s networkidle limit). Try again next week with a browser-saved mirror or a third-party summary. Content matters for [[llm-api-enterprise-share]] and [[ai-app-categories-2025]] coding-LLM share discussions.

---

<!-- Future weekly sweeps append here. Keep each run's section short. -->

## 2026-04-23 — weekly sweep (partial cycle, 72h window)

This run fired one day after the 2026-04-22 sweep, so the window is short; 9 items below are fresh signal in that 72h.

### Open-weight / local-model
- **Qwen3.6-27B** (2026-04-22) — Alibaba Apache-2.0 open-weight model; 27B dense beats Alibaba's own 397B MoE on SWE-bench Verified (77.2%); runs Q4-quantized in 16.8 GB on a single consumer GPU. Top of HN 919 pts. Collapses a tier that previously required cloud API or multi-GPU serving. **Strong counter-signal to [[landscape/agentic-compute-pricing-2026-04]]** — if $100+ Pro+ subscriptions become the only way to access Opus/GPT-5-class coding, local Qwen-class models become economically competitive for certain workflows.

### Vertical-agent funding this week
- **AcuityMD $80M Series C** (2026-04-21) — MedTech sales agent; ~$955M valuation; 400+ MedTech customers; StepStone-led, Benchmark/Redpoint/ICONIQ participating. Vertical-agent category entry with open-beta agentic layer (AcuityAI).

### Frontier-research funding
- **NeoCognition $40M seed** (2026-04-21) — self-learning agent research; Cambium Capital / Walden Catalyst / Vista Equity / Ion Stoica (Databricks co-founder). Specialization / self-learning angle; watch for concrete product vs. research thesis.

### Google Cloud Next '26 Day 2 — items not captured as separate pages
(Core GEAP launch is captured at [[landscape/google-cloud-next-2026-day2]]; these are parallel announcements referenced inside that page's competitive context.)
- **Chrome AI Co-Worker** — browser-as-agent, "auto browse" feature for enterprise Chrome. Puts Cursor, Anthropic Computer Use, and browser-agent startups on notice.
- **Workspace Intelligence + Workspace Studio** — semantic layer over Gmail/Docs/Drive/Meet + no-code agent builder. Direct competitor to Microsoft Copilot Studio.
- **TPU 8t + TPU 8i** — 8th-gen TPUs, training/inference split; TPU 8t scales to 9,600-chip superpods. Relevant for hyperscaler infrastructure tracking.

### Coding-agent tooling
- **Zed parallel agents** (2026-04-22, HN 264 pts) — native multi-agent parallelization in the editor; signals agent-native IDE tooling maturing beyond single-thread coding assistance.
- **"Over-editing" empirical study** (nrehiew blog, 2026-04-22, HN 400 pts) — 400-problem dataset quantifying over-edit rates across frontier models. GPT-5.4 Levenshtein distance 0.395 vs Claude Opus 4.6 at 0.060 — Claude significantly less disruptive. RL training shown to improve minimality without degrading code quality. Supports C8 practitioner side; also a clean practitioner benchmark to cite.

### China AI infrastructure
- **EVAS Intelligence ¥1.5B Series B** (2026-04-22) — ~$211M; China state-backed + Heli Capital; RISC-V TPU-architecture for large-model training. Significant China-domestic AI chip scale-up; geopolitical relevance for enterprise AI supply chain.

### Covered inline, not in watchlist
- **Anthropic Claude Code removed from Pro plan (tested, reverted, 2026-04-21)** — captured narratively inside [[landscape/agentic-compute-pricing-2026-04]] alongside the GitHub Copilot event.

---

## 2026-05-03 — weekly sweep

### Vertical-AI funding cluster (single-week)

- **Avoca $125M Series B / $1B valuation** (2026-04-27) — AI voice/SMS/chat agents for HVAC, plumbing, roofing, auto. Meritech + General Catalyst-led; Kleiner Series-A lead. Tracking $1B in jobs booked this year. **Home-services vertical-agent unicorn**; first concrete proof point for Menlo's "labor-budget vertical AI" thesis (https://menlovc.com/perspective/software-finally-gets-to-work-the-opportunity-in-vertical-ai/).
- **Manifest OS $60M Series A / $750M valuation** (2026-04-28) — Menlo Ventures + Kleiner Perkins co-lead. Largest Series A in legal-tech history per company. AI-native law firm OS with **fixed-price outcomes pricing model** explicitly attacking the billable-hour structure. Strong fit for [[thesis/agents-eating-saas]] narrow-deep-vertical wedge.
- **Legora $50M Series D extension / $5.6B valuation** (2026-04-30) — Atlassian + NVentures (Nvidia VC arm — first legal-tech bet) co-lead. $866M raised since 2023. Swedish legal AI; explicit Harvey rivalry intensification. Watch for Nvidia inference-acceleration positioning angle.
- **Hightouch $150M Series D / $2.75B valuation** (2026-04-27) — Goldman Sachs Growth + Bain Capital Ventures co-lead. Repositioning as **"agentic CDP"** — agents that autonomously run marketing campaigns against customer-data infrastructure. Largest marketing-data-platform round of the window.

### Frontier-research funding

- **Ineffable Intelligence $1.1B seed / $5.1B valuation** (2026-04-27) — David Silver (former DeepMind RL lead, AlphaGo). Sequoia + Lightspeed-led; Nvidia, Google, DST, Index, British Business Bank, UK Sovereign AI Fund. **Largest seed round in European history.** Mission: pure-RL "superlearner" without human-labeled data, targeting superintelligence. Pre-product; track for benchmark / preprint emergence over 2026-Q3.

### Vendor first-party — major launches not captured

- **Salesforce Agentforce Operations (GA, 2026-04-29)** — multi-agent orchestration across ERP / email / compliance workflows; vendor-claimed 70% faster cycle times, 80% reduction in manual data entry. Salesforce Flows integration enters beta in May. Direct extension of [[platforms/salesforce]] Agentforce / Headless 360 trajectory.
- **Anthropic 9 Claude connectors for creative tools (2026-04-28)** — MCP-based connectors for Adobe (Photoshop, Premiere, After Effects), Blender, Ableton, Autodesk Maya. New **Claude Design** product for rapid UI mockups. Educational partnerships with RISD, Ringling, Goldsmiths. Vertical-expansion-via-MCP signal — track if professional creative tools become a distinct Anthropic revenue line.
- **Databricks ai_parse SQL function + GPT-5.5 hosted model API (~2026-04-28)** — direct competitive counterpunch to Snowflake's Agentic Document Analytics. See https://databricksreleasehub.com/. Track for next [[platforms/databricks]] update.
- **Google Deep Research Max (2026-04-21, edge-of-window)** — Gemini 3.1 Pro-powered autonomous research agent with native MCP support and structured analytical visualizations. Direct enterprise answer to OpenAI Deep Research.

### M&A / regulatory

- **Meta–Manus $2B acquisition blocked by China (2026-04-27)** — China NDRC vetoes cross-border M&A of Singapore-based agentic AI startup with Chinese engineering roots. **First major CCP veto of cross-border AI M&A**; sets regulatory precedent for any AI-agent company with Chinese-founder DNA. Watch for follow-on rulings on smaller deals.
- **Thinking Machines Lab (Mira Murati) seeking $50–55B valuation + new Google Cloud GB300 deal (~2026-04-22 / 28)** — multi-billion-dollar GB300 cluster commit on Google Cloud (TechCrunch exclusive). Continues the multi-CSP frontier-lab pattern (see [[landscape/openai-microsoft-restructure-2026-04]], [[landscape/google-anthropic-40b-2026-04]]).

### Macro / Q1 framing

- **Crunchbase Q1 2026: $300B global VC, $242B (80%) to AI; late-stage $100M+ rounds up 205% YoY across 158 companies** — macro context for Q2 deal velocity. https://news.crunchbase.com/venture/record-breaking-funding-ai-global-q1-2026/

### Practitioner-tier / coding-agent ecosystem

- **Cursor Security Review beta (2026-04-30)** — first major IDE shipping always-on AI security agents in PR flow (auth regressions, prompt injection, privacy). Teams / Enterprise plans only. Build-vs-buy friction surface for security tooling vendors.
- **DeepSeek V4-class enterprise distribution** — net-new page [[llms/deepseek]]; track for Menlo's next enterprise-share survey datapoint on whether Chinese open-weight share moves past 1% of total LLM API spend.

### Skipped / not pursued this run

- **Anthropic Claude Code postmortem (2026-04-23)** — three engineering missteps publicly disclosed (reasoning effort downgrade, thinking-cache bug, verbosity cap). Edge-of-window; transparency signal but already covered narratively in [[landscape/agentic-compute-pricing-2026-04]] context.
- **OpenClaw GitHub trending (310k stars, ~60k in 72h)** — open-source local agent runner. Skipped as primarily consumer / enthusiast; not enterprise-fit. Note 17% of third-party skills found malicious — supply-chain risk pattern worth flagging if it surfaces in enterprise tooling.

---

## 2026-05-10 — weekly sweep

### Anthropic compute deals (multi-CSP continuing)

- **Anthropic + Akamai $1.8B compute deal (2026-05-08)** — Bloomberg + Solutions Review. Signals Anthropic diversifying away from Google/AWS infrastructure dependency; Akamai gains a major committed AI workload anchor. Compounds the multi-CSP frontier-lab pattern from [[landscape/google-anthropic-40b-2026-04]] / [[landscape/openai-microsoft-restructure-2026-04]]. Akamai's edge-CDN distribution may matter for inference-at-scale latency.
- **Anthropic + SpaceX Colossus 300MW (2026-05-06)** — Al Jazeera. Anthropic gains access to 220K+ Nvidia GPUs at SpaceX Memphis; notable given Musk's active OpenAI lawsuit. Adds a fourth substrate (after AWS Trainium + Google Cloud + Akamai) to Anthropic's compute footprint. Track for whether this moves into the [[llms/anthropic-claude-family]] compute-infrastructure section as a captured page next sweep.

### Enterprise agent governance / control plane

- **ServiceNow AI Control Tower expansion + Traceloop acquisition (Knowledge 2026, 2026-05-05)** — ServiceNow newsroom + The Register + Fortune. Agent kill switches; 30 new cloud integrations across AWS / GCP / Azure + SAP / Oracle / Workday; Traceloop acquired for runtime agent observability. **First concrete acquihire data point** for the pure-play harness/eval startups → bundled-into-existing-SKU governance vendors pattern flagged in [[landscape/ai-infrastructure-frontiers-2026]] update this run. ServiceNow joins the Microsoft Agent 365 / Salesforce Agent Fabric / GEAP Agent Gateway competitive set.

### Vertical-AI / coding-agent funding

- **Blitzy $200M Series @ $1.4B (2026-05-05)** — Crunchbase / Northzone-led. Autonomous enterprise SDLC (thousands of parallel agents); SWE-Bench Pro 66.5%; "dozens of Global 2000 enterprises" claimed. Distinct from Cursor/consumer vibe-coding — explicitly enterprise-SDLC-replacement positioning. Worth a [[startups/blitzy]] page if a second source confirms revenue / customer detail.
- **DeepInfra $107M Series B (2026-05-04)** — HPC Wire / Crunchbase / 500 Global + Georges Harik. Open-source model inference cloud; 190+ models; **5 trillion tokens/week**; **~30% of tokens from agentic workloads**; 25× volume growth since Series A. NVIDIA participated. Inference-at-scale validation for [[landscape/ai-infrastructure-frontiers-2026]] §Inference inflection point.
- **Tessera Labs $60M Series A (2026-05-06, a16z-led)** — BusinessWire. Multi-agent ERP modernisation; vendor-agnostic, pre-trained on thousands of org landscapes; compresses multi-year ERP overhauls to weeks. a16z partner Seema Amble joins board. **a16z direct ERP-disruption bet** — extends the vertical-AI funding cluster from prior week (Avoca / Manifest OS / Legora / Hightouch).

### Vendor first-party — novel mechanism not captured deeply

- **Writer event-based triggers (2026-04-30)** — BusinessWire + VentureBeat. Agents fire on business signals from Gmail/Gong/Slack/SharePoint **without human invocation**; adds BYOK + Datadog observability. Direct shot at Salesforce/Microsoft horizontal agent surfaces. **Novel mechanism: autonomous event-triggered agents** — distinct primitive from request-response or scheduled agents. Worth a comparison entry next time we extend [[platforms/salesforce]] competitive context.
- **NanoClaw + Vercel approval-gateway (2026-04-17, surfaced this week as MCP-isolation context)** — VentureBeat + SiliconAngle. Policy-gated credential injection (Rust gateway intercept; agent never sees real key) across 15 messaging apps. **Novel control-plane primitive for agent authorization** — direct mitigation pattern for [[landscape/mcp-rce-supply-chain-2026-05]] supply-chain risk. Worth tracking as alternative-protocol / wrapper-protocol candidate.

### Open-weight / Chinese frontier

- **Kimi K2.6 (Moonshot AI, 2026-05-03)** — HN 311 pts. Open-weight 1T-parameter MoE (32B active, modified MIT) took 1st in a live sliding-tile coding contest above GPT-5.5 and Claude Opus 4.7 (7-1-0); 58.6% SWE-bench Pro at ~5–6× lower token cost. Compounds DeepSeek V4 (last week) and Qwen3.6-27B into a coherent **Chinese open-weight wave** narrative. If GLM-5.1 + MiniMax M2.7 also confirm at frontier-adjacent capability per build-fast-with-AI's 2026-05 leaderboard, the open-weight tier in [[landscape/agentic-compute-pricing-2026-04]] §Refined four-tier read needs a Q3 update.
- **Anthropic Claude Opus 4.7 postmortem (2026-04-23)** — HN **1,959 pts, 1,452 comments** — highest-volume cross-venue item in the window. Adaptive thinking regression + product fragmentation complaints; 25-word system-prompt cap reverted 2026-04-20; usage limits reset 2026-04-23. Also covered narratively in [[llms/anthropic-claude-family]] as a release-quality signal. Worth aggregating practitioner-complaint pattern via startupfortune.com piece for [[landscape/agentic-compute-pricing-2026-04]] practitioner-friction context.

### Regulatory

- **EU AI Act Omnibus provisional agreement (2026-05-07)** — EU Council. **High-risk enforcement pushed to Dec 2027 / Aug 2028** — biometrics, critical-infra, employment categories. 16-month delay; compliance timelines now concrete enough for enterprise planning. Worth a regulatory-page if the Omnibus formalises later in 2026; for now flag in client-advisory context.

---

## 2026-05-17 — weekly sweep

Window 2026-05-10 → 2026-05-17. Overflow from a moderately active week; 5 items captured to pages, these 10 tracked.

### Vendor first-party — launches not captured deeply
- **OpenAI Realtime Voice trio** (2026-05-11→14) — GPT-Realtime-2 (128K ctx, GPT-5-class reasoning in live audio), GPT-Realtime-Translate (70+ langs), GPT-Realtime-Whisper (streaming STT). Published pricing $32/$64 per 1M audio in/out tokens. First GPT-5-class audio API; sets voice-agent cost reference. Multi-outlet (OpenAI + TechCrunch). Enables enterprise contact-center voice agents — track for next [[llms/openai]] update.
- **OpenAI Codex Mobile** (2026-05-15) — Codex agent controllable from ChatGPT iOS/Android (start tasks, review diffs, approve commands); 4M weekly Codex users cited. CLI→mobile async human-in-loop. HN ~481. Incremental surface expansion; watch as Claude Code mindshare contest.
- **Anthropic Claude for Small Business** (2026-05-13) — 15 prebuilt agentic workflows + ~12 connectors (QuickBooks/PayPal/Stripe/HubSpot/Canva/Docusign) via Claude Cowork. HN ~535 (skeptical comment tone). Down-market packaging move after the enterprise push; not novel-mechanism but a segmentation signal.
- **Claude Opus 4.7 GA** (2026-05) — stronger long-running coding/agents, higher-res vision; pricing held flat ($5/$25 per 1M). Cadence signal vs OpenAI GPT-5.x; already noted on [[llms/anthropic-claude-family]].
- **Snowflake Intelligence + Cortex Code expansion** — NL Skills builder, MCP connectors (Gmail/Jira/Salesforce/Slack), Cortex Code over AWS Glue + Databricks + Postgres without migration, managed MCP Server GA. Snowflake "agent control plane" positioning vs Databricks/Salesforce. Multi-outlet. Track for next [[platforms/snowflake]] update (note: core announce ~2026-04-21, sustained window coverage).

### Funding / new entrants
- **Corgi Insurance $160M Series B / $1.3B** (2026-05-06, TCV-led) — YC-backed; modular AI-liability insurance (algorithmic bias, hallucinated output, adversarial-model, synthetic-media). $630M→$1.3B in 4 months. New insurance category around AI deployment risk; watch as a build-vs-buy risk-transfer signal.
- **Graphon AI $8.3M seed** (2026-05-14, Novera-led; Perplexity Fund, Samsung Next) — "pre-model intelligence layer": persistent relational memory graph replacing isolated RAG retrieval, reasoning beyond the 1M-token ceiling. Novel-mechanism RAG-alternative claim; verify substance vs framing.
- **CopilotKit $27M Series A** (2026-05-05, Glilot/NFX/SignalFire) — AG-UI protocol, a companion to MCP standardising agent↔app-UI comms (streaming, frontend tool calls, shared state). Customers incl. Deutsche Telekom, DocuSign, Cisco. Protocol-layer play adjacent to [[landscape/mcp-rce-supply-chain-2026-05]] / C17.
- **Recursive Superintelligence $650M stealth / $4.65B** (2026-05-13, GV+Greycroft; Nvidia, AMD) — Richard Socher + Tim Rocktäschel; recursively self-improving models, "Level 1" autonomous training targeted mid-2026. Pre-product, research-adjacent (like Ineffable Intelligence). Track for benchmark/preprint emergence, not product yet.

### Practitioner-friction cluster (counter-signal)
- **AI-overreliance backlash hardening** — Mitchell Hashimoto "AI Psychosis" (HN ~1,988 / ~1,165 comments, top thread of week, + Simon Willison) on MTTR-only AI mandates; "AI is making me dumb" (HN ~541); Cursor pricing hikes + free-tier cap + CEO public apology over overage billing; Ontario auditors find AI medical scribes "routinely blow basic facts" (HN ~309, regulated-vertical reliability floor). Aggregate practitioner-reality counter-weight to the week's platform launches; feeds [[thesis/agents-eating-saas]] reality-check + [[landscape/agentic-compute-pricing-2026-04]] friction context.

### Next-sweep flag
- **Google I/O 2026 (2026-05-19, outside window)** — Gemini Spark (always-on autonomous agent in Gemini app: inbox triage, bookings; Google warns it "may share info / make purchases without asking"), Gemini Intelligence (Android OS-level agentic rebuild), expected Gemini 4. Pre-I/O leaks ran the week of 2026-05-14 across 5+ outlets. Capture-priority candidate for the 2026-05-24 sweep.

---

## 2026-05-28 — weekly sweep

Window 2026-05-21 → 2026-05-28. 5 sources captured to pages (Google I/O enterprise, Anthropic Series H, KPMG+JV extension, TanStack supply chain extension). These 9 tracked.

### Regulatory / policy
- **White House AI executive order scrapped (2026-05-21)** — Trump pulled a voluntary 90-day pre-launch review framework EO hours before signing; cited competitiveness concerns; NSA model-testing provision specifically flagged. Regulatory clarity for enterprise risk-assessment paused indefinitely. — NBC News + WaPo + CNBC.
- **Trump quote:** "I didn't like certain aspects... could have been a blocker." Watch for revised EO or Congressional action in Q3.

### Funding / M&A
- **OpenAI IPO confidential S-1 filing (2026-05-22)** — Goldman Sachs + Morgan Stanley leading; $852B–$1T target valuation; public roadshow window September 2026; $25B annualized revenue; $1.22 loss per $1 revenue Q1 2026 (i.e. loss-making at IPO). Same week as SpaceX S-1. — Fortune + CNBC.
- **Rhoda AI $450M Series A (stealth exit, 2026-05-xx)** — FutureVision robotic intelligence platform; video-predictive control; out-of-stealth only. No revenue/customer detail disclosed. — fundup.ai.

### Vendor first-party / platform
- **Microsoft Copilot Studio computer-use GA (2026-05-13, one week before window)** — first hyperscaler to GA computer-using agents (vision + reasoning on live interfaces, no API required); Claude Sonnet 4.5 + OpenAI CUA as production models; Azure Key Vault credential storage + Purview audit logging; human-in-loop via Outlook. Direct parallel to Anthropic Managed Agents (AWS) and Google Managed Agents API. — Microsoft + DevOps.com.
- **Andrej Karpathy joins Anthropic pretraining (2026-05-19)** — working under Nick Joseph; focus: use Claude to accelerate pretraining research (model-training-AI-training loop). Highest-profile AI talent move of 2026 so far. Confirms Anthropic pretraining ambition is expanding, not plateauing. — TechCrunch + CNBC + Axios.
- **OpenAI $25B annualized revenue / $1.22 loss per $1 revenue (Q1 2026)** — confirmed by IPO filing context; losing money at scale while raising at $852B–$1T. Contrast with Anthropic Q2 2026 first operating profit. Watch as OpenAI public roadshow approaches for detailed P&L disclosure.
- **Google I/O 2026 creative-platform integrations (2026-05-21)** — Adobe (Photoshop etc.), Canva (Magic Layers), CapCut (coming soon) integrated directly into Gemini app as named connectors. Google occupying the creative-workflow distribution channel previously targeted by Anthropic's 9 MCP creative connectors (April 2026). Pattern: hyperscalers wrapping third-party tools via model-native connectors. — buildfastwithai.

### Practitioner signal
- **KPMG Blaze (Claude Code for legacy IT)** — mentioned in KPMG alliance announcement as planned product for portfolio company IT modernization; no pricing/GA date; zero practitioner signal yet. Track if it surfaces in any G2 / GitHub issue / HN thread over next 60 days.
