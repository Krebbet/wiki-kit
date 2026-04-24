# Lio

AI-native "virtual procurement workforce" executing the full enterprise procurement workflow end-to-end — reading documents, evaluating suppliers, negotiating terms, running compliance checks, and completing transactions — rather than assisting a human. $30M Series A, Andreessen-Horowitz-led, announced 2026-03-05. Positioned as a buy-side replacement for BPO spend and legacy procurement suites (SAP Ariba, Oracle).

**Tier:** startup (YC Spring '23 cohort). **Stub — single-source page; extend when customer case studies, G2 / practitioner reviews, or follow-on coverage arrive.**

## What it does

AI agents that execute the enterprise procurement workflow end-to-end instead of helping humans do it faster. Named steps in source (TechCrunch 2026-03-05): reading documents, evaluating suppliers, negotiating terms, running compliance checks, cross-referencing budgets, completing transactions.

## Techniques under the hood

- Described as "agentic infrastructure" — a platform of AI agents that operate across and on top of existing enterprise systems (ERP, contract management, supplier databases, email).
- Orchestrates unstructured documents and repetitive workflows across multiple back-office systems.
- No further architectural detail in source — no model disclosures, no RAG / planner / multi-agent topology specifics. Cross-system orchestration is the apparent wedge *(editorial)*.

## Deployment model

Integration layer over customer ERP / contract management / supplier database / email. Source does not specify SaaS vs on-prem vs VPC. *Re-check before quoting.*

## Customization hooks

Not specified in source.

## Running costs

Not specified in source.

## Hard limits

Not specified in source — no accuracy, human-in-the-loop threshold, or failure-mode claims.

## Market reception (2026-03-05)

- **$30M Series A** led by **Andreessen Horowitz**, with SV Angels, Harry Stebbings, and Y Combinator participating. **$33M total raised to date.**
- **Founded 2023** by **Vladimir Keil** (CEO), **Lukas Heinzmann**, **Till Wagner**.
- YC **Spring 2023** cohort.
- **Vendor-quoted customer claims (unverified):**
  - "Already helping companies manage billions in enterprise spend."
  - One unnamed global manufacturer "automated 75% of its previously outsourced procurement operations within six months."
- Use of fresh capital: U.S. expansion + agent-capability investment (founder's stated plan).

## Hype-vs-reality delta

All results are **founder-quoted** — no independent verification, no named customer, no baseline for what "automated" means (full-auto vs supervised). Treat as marketing until corroborated by a G2 review, practitioner post, or named customer case study. The "75% in six months" claim is exactly the flavour that [[open-questions-2026-04]] C8 is watching.

## Techniques worth stealing

- **Cross-system orchestration as the wedge** — the procurement workflow is not a single point-tool; its value is tying together ERP + contract + supplier + email silos. Generalisable framing for other back-office verticals.
- **"Agents execute the workflow" positioning** vs "software helps humans do the workflow faster" — clean reframe for any vertical agent pitch.

## Build-vs-buy signals

Founder's named competitors:
- **Legacy procurement suites**: SAP Ariba, Oracle.
- **BPO providers** (business-process outsourcing).
- **Consulting firms**.

Lio pitches itself as a **replacement for BPO spend**, not a feature bolt-on. Implication for advisory: a client currently outsourcing procurement to BPO or running heavy Ariba / Oracle customisation has a new line-item to evaluate — **but the source gives no pricing, integration timeline, or limits data to make a real buy-recommendation yet.** Re-visit when a second source lands.

## Reader notes

- Source is a single TechCrunch funding announcement — vendor-PR-adjacent. All product claims are founder / CEO quotes.
- Relevant for [[open-questions-2026-04]] C1 (agents-eat-apps narrative — Lio is a concrete "agents execute the workflow" instance) and C8 (AGI-for-near-term-tasks — the "75% automated" claim).
- Ingest batch context: appeared in the 2026-04-22 "emerging agentic startups" research run alongside HN practitioner threads that directly skepticise this claim type — see [[agents-eating-saas]].

## Source

- `raw/research/emerging-agentic-startups-2026/01-techcrunch-lio-series-a.md`

## Related

- [[ai-app-categories-2025]]
- [[ai-apps-layer-2026]]
- [[enterprise-ai-market-2025-2026]]
- [[agents-eating-saas]]
- [[trace]]
- [[open-questions-2026-04]]
