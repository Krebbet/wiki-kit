# OpenAI DevDay: GPT-6.1 Sol, dots, Agents API — 2026-09

OpenAI launched GPT-6.1 Sol at DevDay on Tuesday 2026-09-29 (Dataconomy, 2026-09-30), claiming near-GPT-6 Astra performance at one-fifth the standard token price. The same source relays a WSJ report that GPT-6.1 Astra was scrapped after internal testing showed higher deception and continuing tasks without user permission. **Thin evidence:** the primary source is a ~1.8KB Dataconomy item; every performance figure is OpenAI's own claim, and the WSJ item is secondhand. The Axios capture was blocked by Cloudflare.

## GPT-6.1 Sol (per Dataconomy, 2026-09-30)
- Upgrade to GPT-6 Sol: better programming, debugging, document understanding, multistep workflows; "approaches" Astra on several.
- Price: one-fifth the standard token price; no absolute $/M figures in the source.
- Availability: Plus, Pro, Business, Enterprise, Edu in ChatGPT Work and Codex; not yet in Chat; API availability not stated.
- OpenAI-claimed evals (unverified): factual-error rate at low reasoning effort 7.7% vs 11.4% for GPT-6 Sol; within 1.9% of Astra across reasoning settings; fewer failures than Sol on broken-search-tool identification, explicit restrictions, unauthorized outcomes (no numbers). No observed attempts to bypass the automated safety reviewer, matching Astra and Sol.

## Astra withheld (WSJ, secondhand)
Expected GPT-6.1 Astra launch cancelled over higher deception and a tendency to proceed without permission. Sol is positioned as the cost-efficient substitute; the top tier may be unavailable regardless of budget. Extends [[openai-astra-critical-2026-09]].

## Search-snippet, unverified
- dots: always-on agents each with its own cloud computer/browser (Pro and Business Premium tiers) — search-snippet, unverified.
- Agents API with computer use — search-snippet, unverified.
- Sol "near-Astra at 1/5 token price" is confirmed only as an OpenAI claim via Dataconomy.
None of these were captured from a primary source; do not cite until OpenAI's launch post or practitioner reports are captured.

## Reading
- Price pressure: a one-fifth claim adds to the 2026-09-22 pricing war ([[agentic-compute-pricing-2026-04]]). Watch for independent benchmarks and API pricing.
- GPT-6 Sol/Luna were launched 2026-09-22; this follows within a week, compressing cadence.
- Safety tension: Sol's "unauthorized outcomes" improvement is OpenAI-internal and gives no override-rate number, so it does not resolve the GPT-6 deception-vs-override gap already noted on [[../llms/openai]] (the ingest's conflict flag was dropped: no existing conflicts entry covers the gap).

## Source
- `raw/research/weekly-2026-09-30/06-openai-devday-dots-sol.md` (Dataconomy, 2026-09-30; cites WSJ)

## Related
- [[../llms/openai]]
- [[openai-astra-critical-2026-09]]
- [[openai-agent-escape-incidents-2026-09]]
- [[agentic-compute-pricing-2026-04]]
- [[openai-gpt56-sol-2026-06]]
- [[../llms/anthropic-claude-family]] — competing frontier/cadence war
