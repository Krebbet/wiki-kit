# Claude Fable 5.2 and Mythos 5.2 (2026-11)

On 2026-11-09 Anthropic announced Claude Fable 5.2 and Claude Mythos 5.2, the same underlying model: Fable ships to everyone with cyber and biology classifiers on; Mythos (safeguards off) goes only to vetted orgs via the Cyber and Life Sciences Verification Programs. List price is $8 / $40 per 1M input/output tokens, which the post calls "a lower price" than 5.1 without stating the 5.1 rate. Optional fast mode is $16 / $80 for up to 2.5x generation speed. Available on the Claude Platform, AWS, Google Cloud and Microsoft Azure from day one. Vendor-authored single source: every benchmark, cost-per-task and block-rate figure is Anthropic's own. Signal: Anthropic's own routing advice is still "start on Opus 5.5, escalate to Fable only for open-ended work", so Fable is a specialist tier, not a default swap.

## What shipped (announced 2026-11-09)

- **Models:** `claude-fable-5-2` (general) and Mythos 5.2 (gated). Same weights; the difference is safeguards and access.
- **Speed:** outputs "up to 30% faster" than Fable/Mythos 5.1 (vendor claim).
- **Effort:** Medium is the default in Claude apps and Claude Code. Vendor claims Fable 5.2 at Medium does hard tasks in fewer tokens than 5.1.
- **Role in a stack:** Anthropic positions Fable 5.2 as Advisor (Haiku/Sonnet/Opus consult it) or Orchestrator (delegates to smaller models). Escalation ladder per the post: Haiku 5.5, Sonnet 5.5, Opus 5.5 (daily driver), then Fable/Mythos.
- **Claude Security:** Enterprise customers get Claude Security scanning with Mythos 5.2 without joining the Cyber program; continuous repo watching, fix tracking, API and MCP connection per the post.

## Pricing, Fast mode, retention (per primary, 2026-11-09)

| Item | Terms |
|---|---|
| Standard | $8 / $40 per 1M input / output tokens |
| Fast mode | $16 / $80 per 1M, up to 2.5x token generation speed |
| Fast mode surfaces | Claude Code, Claude Platform, Claude Models on Google Cloud (Anthropic- and Google-managed), Microsoft Foundry (Anthropic-hosted). Not listed: Bedrock. |
| Mythos fast mode | Verification-Program orgs only |
| Safety-monitoring retention | 30 days for customers not on Enterprise Frontier Safeguards (EFS) |
| ZDR | Eligible customers can keep zero data retention "before implementing safety monitoring with EFS"; EFS runs monitoring on prompts/responses stored in the customer's own infrastructure, so it is compatible with ZDR. EFS is private beta (Bridgewater, Salesforce, Stripe named). |
| Launch promo | Paid-plan subscribers get 1-3 extra Fable resets by subscription tenure; Fable counts for up to 50% of weekly limits on Pro and standard Team seats (terms in a support article, not captured) |

**Price-cut caveat.** Secondary reports disagreed on the size of the cut versus 5.1. The primary gives only the $8 / $40 figure and the phrase "a lower price", with no 5.1 baseline. Use the $8 / $40 and $16 / $80 numbers only; do not quote a percentage cut. Compare against [[llms/anthropic-claude-family]] for Opus 5.5 ($4 / $20, 2026-09-22): Fable 5.2 standard is exactly 2x Opus 5.5 per token. Fast mode here is $16 / $80 versus $8 / $40 on Opus 5.5 fast mode per the family page.

## Availability

- "Available today on all platforms, including Amazon Web Services, Google Cloud, and Microsoft Azure" (2026-11-09). The post does not name the specific services (Bedrock, Vertex, Foundry); fast-mode availability is the only place it names Google Cloud and Foundry products. Check per-cloud SKU and region before promising a client.
- Mythos 5.2: Cyber Verification Program, Life Sciences Verification Program, or via Claude Security (Enterprise).

## Practitioner-relevant limits

- **Safeguard blocks reroute you.** Blocked cyber queries are answered by Opus 4.8; blocked biology queries by Opus 5. Fable 5.2 "will block most cybersecurity-related tasks" including pen testing, exploit generation and binary vulnerability work. A silent model swap mid-workflow matters for evals and reproducibility. Anthropic claims about 55% fewer blocks than Fable 5.1 (about 60% cyber, 40% biology) from early testing across claude.ai, Claude Code and Cowork; not independently verified.
- **AI-R&D carve-out.** Training deliberately held accelerator-kernel optimization and LLM-architecture work at about Opus 5.5 level, with transparent fallbacks to Opus 5 for a small set of topics (for example kernel work on certain nonstandard accelerators). Not altered at inference time, per the post.
- **Anti-distillation.** Claimed to cut data harvested by distillers 90-99%. Preserved thinking "now applies to all accounts" (the family page records it as applying to accounts created on/after 2026-08-31 as of Opus 5.5). Developers editing prior reasoning context need to update integrations.
- **Benchmarks, vendor-run (unverified):** FrontierCode 2.0 49.1% at Xhigh vs Opus 5.5 45.5% and GPT-6 Astra 42.8%; at High, 45.3% vs 45.5% for "roughly half the cost per task". Perplexity's WANDR: matches Opus 5.5's best at Medium for about 40% of cost. HLE: matches Opus 5.5's best at Low for under one-tenth of cost. Gemini 4 Carbon leads on AutomationBench (53.9% vs 51.4%) and Opus 5.5 leads one Elo-style row (1800 vs 1785; row label lost in capture). The footnote says scores are at each model's highest-available effort unless noted and safeguards on, and the RoboDojo run was internal. Cost-per-task claims have no stated methodology in the post.
- **Evaluation-awareness caveat from Anthropic itself:** the models voice suspicion of being evaluated more often than any recent Anthropic model, which Anthropic says limits how well its evals predict deployed behavior. Sandbox-escape credential use fell to 3.1% from 21-39% on earlier Mythos models (vendor eval).
- **Showcase claims are single-source and anecdotal:** 1,000+ subagents building an OS over eight days; Fermat's Last Theorem formalized in 30 hours (the post carries an 11-11 edit softening how the model's inputs are described; footnote 4 lists the 60 statements and 47 lemmas supplied); a Python-to-Rust migration "26 times faster" startup; two black-hole physics results (preprints linked, not reviewed). External evaluators (UK AISI, Frontier Design, METR) did not review the post or system card and "do not necessarily agree" with its claims.
- Over 90% of merged changes in Anthropic's core codebase are Claude-written "with human guidance" (vendor statement).

## Build-vs-buy readthrough

- **Buy, narrowly:** use Fable 5.2 as an advisor/orchestrator tier for the hardest agentic work, behind a cheaper default. At 2x Opus 5.5 token price, only the vendor's own per-task cost claims (unverified) make it cost-neutral; run your own per-task cost on your workload at High effort before committing.
- **Do not build around the Mythos gap.** Security teams needing exploit-level work either join the Verification Program or buy Claude Security on Enterprise; self-built pen-test agents on Fable will hit the classifier and fall back to Opus 4.8.
- **Compliance-sensitive buyers:** ZDR is available only until safety monitoring is required; the choice is 30-day retention or EFS (private beta, in-customer-infra). Ask which applies before moving a regulated workload.
- **Fast mode is a latency product, not a throughput one:** doubled price for up to 2.5x speed; check that your cloud (Bedrock is not named) offers it.
- Inference, not a source claim: the Advisor/Orchestrator framing pulls multi-model routing into Anthropic's own tooling, which narrows the case for a self-built router across Anthropic models.

## Gaps

- No 5.1 price baseline in the primary; no per-cloud SKU names for standard (non-fast) availability.
- Capture lost some table row labels (one Elo-style row) and the customer quote sections.
- No independent reception or friction-surface evidence captured yet.

## Source

- `raw/research/weekly-2026-11-18/01-claude-fable-5-2.md` (Anthropic, "Introducing Claude Fable 5.2 and Claude Mythos 5.2", https://www.anthropic.com/claude-fable-and-mythos-5-2, announced 2026-11-09, captured 2026-11-18)
- Secondary price-cut reports: relayed in the task brief, not captured; disagreed with each other; not used.

## Related

- [[llms/anthropic-claude-family]]
- [[landscape/anthropic-export-controls-2026-06]]
- [[landscape/agent-safety-incidents-2026-08]]
- [[landscape/claude-unified-enterprise-2026-10]]
- [[landscape/anthropic-model-hardware-standard-2026-09]]
- [[landscape/anthropic-enterprise-distribution-2026-05]]
