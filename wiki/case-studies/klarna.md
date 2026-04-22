# Klarna — Customer-Service AI Assistant

One of the most-cited and most-instructive production LLM deployments of 2024–2026. Launched 2024 as an OpenAI-powered assistant on LangGraph + LangSmith; the initial metrics win (700 FTE equivalent, $40M projected profit impact) was followed in 2025 by a **strategic correction** — rehiring humans and moving to a hybrid model after domain-specific quality issues surfaced that the launch KPIs had missed. The correction is the lesson.

## 2024 launch — the headline wins

Stack: **OpenAI** LLM + **LangGraph** (multi-agent routing) + **LangSmith** (test-driven development, LLM-based evals, prompt iteration). Dynamic prompt tailoring per scenario; meta-prompting loop for automated prompt optimization.

Scope: payment queries, refunds, payment escalations across 85M users / 23 markets / 35+ languages.

Cited outcomes from the first ~9 months:

- **2.3M chats** handled in the first month.
- Average resolution time: **11 minutes → 2 minutes**.
- Automated ~70% of repetitive support tasks; 25% repeat-contact reduction.
- Work equivalent of **700 full-time staff**; replaced ~3,000 outsourced agents.
- CSAT parity with human agents on initial measurements.
- **$40M** projected profit impact for 2024.

*(Evidence class: customer-cited metrics, vendor blog source — LangChain, OpenAI. No independent verification. Marketing-tainted framing extractable from the underlying numbers.)*

## 2025 correction — the quieter story

By mid-2025, Klarna pivoted. Public signals of the correction:

- Actively **rehiring human agents** — reversing the outsourced-agent replacement.
- Shift to a **hybrid architecture**: AI autonomous on routine tier-one queries, humans on complex / sensitive / financial-services-specific cases. AI also *expanded upward* to handle some tier-two queries rather than being restricted to tier-one.
- Introduced 24/7 live chat in the app with a callback option for voice.
- CEO **Sebastian Siemiatkowski**: *"Cost was a predominant evaluation factor"* in the initial decision, producing *"lower quality"* than customers expected.

Post-correction metrics (mid-2025):

- AI still handles ~2/3 of chats (~1.3M/month), equivalent work to ~800 FTEs.
- 25% repeat-contact reduction retained.
- 2-minute resolution time retained for AI-handled cases.
- No published post-correction CSAT or NPS.

*(Evidence class: CEO direct quotes, Bloomberg / eMarketer / Business Insider reporting, Trustpilot / BBB sentiment data, combined with author synthesis in the PromptLayer post.)*

## Why the correction (causes)

Multiple failure signals converged, all under-weighted by the launch KPIs:

- **Metric-masked quality degradation.** CSAT parity at launch didn't surface later dispute-resolution, account-access, and edge-case failures.
- **Trustpilot 4.1/5 + 900+ BBB complaints** over three years — sentiment data the internal CSAT didn't capture.
- **Financial-services context sensitivity:** disputes, billing, account access require human judgment the AI couldn't resolve. Cost-optimized routing violated the implicit industry contract that money-sensitive issues deserve humans.
- **Prior understaffing amplified AI-failure visibility** — when the AI couldn't resolve a dispute, there was insufficient human capacity for graceful degradation.
- **Single-vendor OpenAI reliance** — no LLM-provider fallback meant no technical recovery path when the single-model approach fell short.

## Lessons this deployment encodes

- **Top-line metric success can mask domain-specific quality loss** — especially in high-stakes verticals. CSAT alone is insufficient signal. See [[failure-modes#metric-masked-quality-degradation]].
- **Escalation capacity is load-bearing.** Cutting human headcount below the capacity to absorb AI failures makes those failures customer-visible. Routing logic alone doesn't substitute for staffing. See [[escalation-vs-approval]].
- **Single-vendor lock-in limits graceful degradation.** Multi-model / multi-vendor architectures give recovery options when one model's behaviour drifts.
- **Financial services (and any regulated or high-stakes domain) warrants explicit human-judgment thresholds** — not just policy-flag routing but capacity planning.
- Klarna's *architectural* choice (LangGraph + LangSmith) held up; the failure was at the *policy and capacity* layer, not the technical one.

## Wiki-lever mapping

- **Measurement discipline** — CSAT-only measurement is the named anti-pattern. See [[error-analysis]], [[llm-as-judge]].
- **Topology** — LangGraph multi-agent routing (star pattern). See [[topology-taxonomy]].
- **Framework choice** — LangGraph + LangSmith, not direct API. See [[framework-skepticism]].
- **SLM / multi-model** — single-vendor OpenAI is the anti-pattern; [[slm-agents]]-style multi-model routing would have provided graceful degradation.
- **Escalation design** — see [[escalation-vs-approval]].

## Source

- `raw/research/production-slm-case-studies/01-langchain-klarna-case-study.md` — LangChain vendor-blog case study (~July 2025 metrics window). Marketing-tainted.
- `raw/research/production-slm-case-studies/02-promptlayer-klarna-human-hybrid.md` — PromptLayer blog on the strategic correction. Cites Bloomberg / eMarketer / Business Insider / OpenAI's own case study, combined with author synthesis.

## Related

- [[failure-modes]]
- [[measurement-vs-architecture]]
- [[framework-skepticism]]
- [[slm-agents]]
- [[topology-taxonomy]]
- [[escalation-vs-approval]]
- [[production-deployments]]
