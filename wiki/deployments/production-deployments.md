# Production Deployments — Catalog

Cross-lever catalog of named production LLM-application deployments: who is using which wiki-documented levers and with what measured outcome. Previously an acknowledged gap; populated by the 2026-04-22 `production-slm-case-studies` research run with per-company pages under `case-studies/`.

**Status:** populated but incomplete. Coverage is strongest where lab blogs, vendor case studies, and academic synthesis have surfaced; still thin on independent third-party replications, self-published enterprise engineering blogs, and post-mortems of failed deployments.

## Covered deployments

| Deployment | Lever(s) | Measured outcome | Case page |
|---|---|---|---|
| **Klarna** customer-service assistant | LangGraph multi-agent routing; LangSmith evals; eventual hybrid (escalation) | 2.3M chats/month; 11→2 min resolution; 700 FTE equivalent; $40M projected. Correction: rehiring humans after CSAT-masked quality loss. | [[klarna]] |
| **Cursor Fast Apply** | SLM-style task-specific FT (Llama-3-70b); speculative-decoding variant; data flywheel | ~1,000 tok/s at 70B; 13× speedup vs vanilla; 9× vs prior GPT-4 deployment | [[cursor-fast-apply]] |
| **Perplexity** answer engine | SLM-default multi-model routing; classifier-based intent routing; Vespa retrieval; RAG with strict grounding | No published latency/cost numbers in the captured source | [[perplexity]] |
| **Google OCTO** (WeatherNext / AI Co-Scientist / Game Arena) | Google-built; evaluation-as-architecture framing; atomicity-as-infrastructure | No external validation; Google framing only | See *Google OCTO retrospective* below |
| **Stanford 51-deployment playbook** — 41 organizations across logistics, translation, financial services, semiconductor, food delivery, retail banking, tech services, healthcare, manufacturing | Academic synthesis — multimodel strategies, escalation, measurement, data-as-asset, orchestration-as-moat | 77% of hardest challenges non-technical; escalation 71% gains vs approval 30%; 42% treat technology as commodity | [[stanford-51-enterprise-playbook]] |

### Representative named outcomes from the Stanford synthesis

- **Logistics** invoice processing: 7→2 FTEs; 85% accuracy; >$1M value; 8 weeks to production.
- **Translation services** recruiting: +83% intake, +79% screening, +75% conversion.
- **Financial services** marketing: 97.6% time-to-market reduction.
- **Semiconductor** field service: 40h → <1h data gathering; 95%+ complete data.
- **Technology services** security ops: 6 → 1.5 FTEs; 4.5 FTEs redeployed.

See [[stanford-51-enterprise-playbook]] for the full list and methodology.

## Google OCTO retrospective (2025)

Google Cloud Office of the CTO's 2025 retrospective ("AI grew up and got a job"). Named deployments all Google-built: **WeatherNext** (weather forecasting, launched 2025), **AI Co-Scientist** (hypothesis generation via ELO-scored tournament), **Game Arena** (multi-agent wargaming sandbox). Zero external customers named; treat as internal best-practice crystallization, not empirical market survey.

Useful framing claims (evidence class: Google OCTO synthesis, unvalidated externally):

- Shift from "chatbots" to stateful autonomous agents with tools and memory.
- **Atomicity as infrastructure** — treat transaction coordination as deterministic system design, not prompting. Agent undo stacks, checkpointing. See [[failure-modes#atomicity-failure-in-multi-step-workflows]].
- **Evaluation as architecture** — real-time autoraters integrated into pipelines enable self-correction before error cascade.
- **Dynamic simulation over static benchmarks** — wargaming agents in adversarial Game Arena scenarios before live deployment.
- **Trust deficit — not capability — as the deployment bottleneck.** Identity and governance frameworks are still immature.

Source: `raw/research/production-slm-case-studies/04-google-cloud-octo-lessons-2025.md` (Grannis et al., 14 OCTO engineers cited).

## Lever → deployment index

| Lever | Exemplified by |
|---|---|
| [[building-effective-agents\|5-pattern vocabulary]] | Anthropic Cookbook (generic); Stanford 51 (implicit — majority use multi-step orchestration) |
| [[topology-taxonomy]] | Klarna (star via LangGraph); Perplexity (chain + star cascade); MetaGPT / ChatDev (chain, named in surveys) |
| [[reasoning-frameworks]] | Perplexity (reasoning-model routing on complex queries); Cursor Composer (RL-trained) |
| [[error-analysis]] / [[llm-as-judge]] | Hamel consulting sample (Hex, Honeycomb, NurtureBoss, Rechat, GitHub Copilot — named, per-company metrics not on wiki); Google OCTO (live autoraters); Klarna (LangSmith LLM-based evals) |
| [[slm-agents]] | **Perplexity** (full exemplar); **Cursor Fast Apply** (task-specific FT at 70B); NVIDIA Nemotron family (lab-blog cited) |
| [[context-engineering]] | Klarna (dynamic prompt tailoring, meta-prompting); Perplexity (strict RAG grounding) |
| [[agentic-context-engineering\|ACE]] | Benchmarked only in the ACE paper; no named production deployment yet |
| [[fine-tuning-vs-context-engineering]] | Cursor (FT path); Perplexity (FT-SLM + context on LLM); Stanford (mixed — "open-source adoption + FT on domain data for specialized / regulated functions") |
| [[agentic-engineering]] | Claude Code, OpenAI Codex, Cursor (tools — Simon's usage self-documented) |
| [[framework-skepticism\|MCP]] | Stanford 51 — one telecom case indexes equipment-type knowledge bases via MCP |
| [[escalation-vs-approval]] | Stanford 51 quantification; Klarna cautionary tale |

## What remains uncovered

- **Independent third-party replication** of ACE headline claims, SLM-survey Table II, and Stanford's escalation-vs-approval gap.
- **Dollar figures at production volumes** — still ratios-only in most sources. Klarna's $40M is one of the few absolute figures and is projected, not audited.
- **Per-company outcomes in Hamel's consulting sample** — companies named (Hex, Honeycomb, NurtureBoss, Rechat, GitHub Copilot), per-deployment outcomes not.
- **Failed-deployment post-mortems** — Stanford's 61% prior-failure statistic names categories but not specific post-mortems.
- **Enterprise self-published engineering blogs** — strongest case studies usually come from engineering teams directly; this corpus is skewed to vendor and academic sources.
- **Named practitioners on FT-vs-RAG** (Eugene Yan, Hamel, Chip Huyen, Shreya) — still not surfaced.

## Queued research

- *`/research Eugene Yan Hamel Chip Huyen Shreya fine-tuning RAG practitioner blog`* — named-practitioner FT-vs-RAG.
- *`/research LLM agent post-mortem production incident`* — failure-mode corpus from the operations side.
- *`/research enterprise engineering blog LLM agent case study`* — company-published technical write-ups.

## Source

No new raw sources on this page. Aggregates across `production-slm-case-studies/` and prior runs; see the individual case-study pages for source traceability.

## Related

- [[klarna]]
- [[cursor-fast-apply]]
- [[perplexity]]
- [[stanford-51-enterprise-playbook]]
- [[escalation-vs-approval]]
- [[ft-vs-context-engineering]]
- [[enterprise-data-integration]]
