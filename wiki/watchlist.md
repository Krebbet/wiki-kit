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
