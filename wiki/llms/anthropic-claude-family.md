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

## Compute infrastructure — Amazon deal (2026-04-20)

Announced 2026-04-20: Amazon adds **$5B** to its Anthropic stake (cumulative: **$13B**) in exchange for a **10-year, $100B AWS cloud commitment** covering up to **5 GW of compute** for Claude training and inference.

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

### Open questions

- Revenue-share terms: not disclosed.
- Whether Anthropic retains the ability to train on non-Trainium substrate (e.g. continued NVIDIA or Google TPU access via GCP) at scale: article language suggests preference, not exclusivity, but unclear.
- Inference-capacity floor across the 10-year term: 5 GW is the ceiling; commitment on delivery timing not specified.

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

## Related

- [[../landscape/llm-api-enterprise-share|llm-api-enterprise-share]]
- [[../landscape/ai-app-categories-2025|ai-app-categories-2025]]
- [[../thesis/ai-apps-layer-2026|ai-apps-layer-2026]]
- [[../thesis/agents-eating-saas|agents-eating-saas]]
- [[../landscape/ai-infrastructure-frontiers-2026|ai-infrastructure-frontiers-2026]]
- [[../landscape/google-cloud-agentic-partner-fund-2026-04|google-cloud-agentic-partner-fund-2026-04]]
- [[../landscape/agentic-compute-pricing-2026-04|agentic-compute-pricing-2026-04]]
- [[../conflicts/open-questions-2026-04|open-questions-2026-04]]
