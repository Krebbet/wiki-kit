# Agent Failure Modes

Working catalog of failure modes documented across the captured corpus. Useful for eval design, guardrail placement, and knowing which slice of traffic to read first during [[error-analysis]].

## Control-flow failures

- **Infinite loops and local-optima blindness** — agent fails to recognize it is stuck or to escalate. *(arXiv 2601.12560, 2026-01.)*
- **Cascading errors in chains** — one early wrong step propagates downstream; sequential tool use is especially vulnerable. *(arXiv 2508.17692, 2025-08.)*
- **Asynchronous-task brittleness** — performance collapses on tasks requiring sustained async coordination; cited 47% → 11% success drop in the taxonomy paper. *(arXiv 2601.12560.)*

## Tool-use failures

- **Hallucination in action** — agent invokes a tool with fabricated arguments after a retrieval miss; downstream state corruption. *(arXiv 2601.12560.)*
- **Tool-description sensitivity** — autonomous zero-shot selection is fragile when tool docs are ambiguous. Invest in tool documentation and schema clarity. *(arXiv 2508.17692.)*
- **Visual grounding drift** — GUI agents hallucinate UI coordinates; dynamic layouts accelerate drift. *(arXiv 2601.12560.)*

## Security failures

- **Indirect prompt injection via tool outputs or scraped content** — classic "confused deputy" pattern. Expands sharply with native computer-use and broader tool surfaces. *(arXiv 2601.12560; mechanism documented, prevalence speculative.)*
- **Tool-injection via poisoned OpenAPI / MCP specs.** A malicious tool description crafted to steer argument generation. *(arXiv 2510.03847, 2025-10.)*
- **Cross-tool data exfiltration.** Chained tool calls leak data across trust boundaries. *(arXiv 2510.03847.)*
- **Schema-shaped malicious args.** Guided decoding produces syntactically valid but semantically hostile arguments — validators pass, policy should have rejected. *(arXiv 2510.03847.)*
- **Replay of cached tool responses out of policy context.** Caching layers surface prior responses in situations their original authorization no longer covers. *(arXiv 2510.03847.)*

## SLM-specific failure modes

- **Overfitting narrow training traces.** Fine-tuned SLMs that passed in-distribution evals fail on held-out end-to-end tasks. Mitigation: adversarial tool inputs, schema fuzzing, out-of-distribution probes before rollout. *(arXiv 2510.03847, 2025-10.)*
- **Validator-semantic gap.** Validators enforce schema compliance, not correctness; a schema-valid call can still be wrong. Adds silent-failure risk to [[slm-agents|validator-first architectures]]. *(arXiv 2510.03847.)*
- **Router miscalibration.** Uncertainty-aware SLM→LLM routing drifts under distribution shift; mis-routed queries either burn LLM budget unnecessarily or leak through to SLMs that can't handle them. *(arXiv 2510.03847.)*
- **Benchmark-to-production transfer gap.** Measured SLM gains on public benchmarks may not transfer; API surfaces and tool behaviours drift. *(arXiv 2510.03847.)*

## Model capability limits

- **Comprehension-generation asymmetry.** Models understand complex contexts well but generate equally sophisticated long-form outputs poorly. GAIA: 15% model vs 92% human on tool-integrated reasoning. Root cause unclear — may be architecture, training, or a fundamental limit. *(arXiv 2507.13334, 2025-07; survey synthesis.)*
- **Middle-token loss.** Accuracy degrades when relevant information sits mid-sequence in long contexts; start / end positions are privileged. *(arXiv 2507.13334.)*
- **ACE failure without reliable execution feedback.** Self-improving context frameworks that lack a clean success/failure signal accumulate noise and degrade below baseline. *(arXiv 2510.04618, 2025-10.)*

## Architecture-level failures

- **Central-controller bottleneck** in star topologies — throughput limited by a single LLM.
- **Decomposition collapse at scale** in mesh topologies — task-decomposition quality degrades sharply beyond modest agent counts. *(arXiv 2508.17692.)*
- **Cost-depth trap** — hierarchical reasoning maximizes depth at *exponential* token cost. See [[topology-taxonomy#the-cost-depth-tradeoff]].

### Atomicity failure in multi-step workflows

Non-atomic multi-step operations cause data corruption when an intermediate step commits and a later step fails (the Google OCTO example: "paying a vendor before updating a record"). Treat transaction coordination as deterministic system design, not prompting; implement agent undo stacks and checkpointing. *(Google OCTO 2025 retrospective framing — lab synthesis, mechanism well-documented elsewhere.)*

### Single-vendor graceful-degradation failure

Single-LLM-provider architectures have no recovery path when the chosen model's behaviour drifts or a specific failure mode surfaces. Multi-vendor routing (see [[slm-agents]]) is the structural hedge. Evidenced by [[klarna|Klarna's post-launch difficulty]] adapting their OpenAI-only stack to financial-services edge cases. *(Case-study evidence.)*

## Evaluation traps

- **Generic-metric false confidence** — helpfulness, coherence, BERTScore, ROUGE miss domain-specific failures. Fine for exploration; dangerous for decisions. *(Hamel / Shreya 2026-01, practitioner-consensus.)*
- **Likert-scale midpoint hiding** — annotators park uncertainty at 3/5. See [[llm-as-judge#label-schema]].
- **Eval pass rate above 90%** — signal you are not stress-testing. Aim for ~70% baseline on hard slices. *(Hamel / Shreya.)*
- **Eval-driven development without error analysis** — building evals for hypothesized failures rather than observed ones; the failure surface is too large to guess. *(Hamel 2026.)*
- **Outsourced annotation** — external annotators lose tacit domain knowledge; superficial rubric compliance.

### Metric-masked quality degradation

Top-line KPIs (CSAT parity, resolution-time reduction) can hide domain-specific quality loss until customer-sentiment signals catch up. Named and instantiated by [[klarna|Klarna's 2025 correction]] — their CSAT parity at launch didn't surface the dispute-resolution and account-access failures that later forced rehiring. Mitigation: vertical-specific eval slices, independent sentiment monitoring (Trustpilot / BBB / support-channel meta-review), and domain-specialist human review of *hard slices* rather than average-case sampling. *(Case-study evidence, 2024–2025.)*

## Organizational failure modes

- **Staff-function resistance (Legal / HR / Risk / Compliance).** Stanford's 51-deployment study finds staff functions resist 35% of deployments, more than end-users at 23%. Persuasion doesn't work; OKR mandates do. Engaging legal / compliance early (before production) shifts the blocker earlier where it's cheap to resolve. *(Stanford 2026-03, academic synthesis. See [[stanford-51-enterprise-playbook]].)*
- **Escalation capacity shortfall.** Using an escalation-style architecture (AI autonomous with human exception review) without sufficient human staffing to absorb the exception volume. Klarna's post-launch visibility of dispute failures was partly this. *(Case study. See [[klarna]], [[escalation-vs-approval]].)*
- **Sponsor discontinuity through failure.** Stanford finds the *same* executive sponsor led failed and successful attempts in every tracked recovery case — sponsor turnover after a failed pilot tends to kill the thread entirely. *(Stanford 2026-03.)*
- **Wrong problem chosen.** 14% of Stanford's failed-first-attempt cases: solution seeking problem, unrealistic day-one-perfection expectations. *(Stanford 2026-03.)*

## The cost hierarchy

Cheaper checks catch more failure modes per dollar. Apply in order:

1. **Assertions / regex** — deterministic, free.
2. **Reference-based checks** — cheap once references exist.
3. **LLM-as-judge** — only after 100+ labels and weekly calibration. See [[llm-as-judge]].

Invert intuitively: invest most eval-engineering effort at the cheap end. *(Hamel / Shreya, practitioner-consensus.)*

## Source

- `raw/research/effective-agentic-patterns/05-hamel-llm-evals-faq.md` — Hamel / Shreya 2026-01.
- `raw/research/effective-agentic-patterns/04-hamel-field-guide.md` — Hamel 2026.
- `raw/research/effective-agentic-patterns/08-arxiv-2601-12560-agentic-ai-taxonomy.md` — Arunkumar V et al., 2026-01.
- `raw/research/effective-agentic-patterns/09-arxiv-2508-17692-agentic-reasoning-survey.md` — Bingxi Zhao et al., 2025-08.
- `raw/research/fine-tuning-vs-context-slms/03-arxiv-2507-13334-context-engineering-survey.md` — Lingrui Mei et al., 2025-07 (comprehension-generation asymmetry, middle-token loss).
- `raw/research/fine-tuning-vs-context-slms/04-arxiv-2510-03847-slm-agentic-systems-survey.md` — Raghav Sharma, Manan Mehta, 2025-10 (SLM-specific failure modes, expanded security surface).
- `raw/research/fine-tuning-vs-context-slms/05-arxiv-2510-04618-agentic-context-engineering.md` — Qizheng Zhang et al., 2025-10 (ACE failure without feedback).
- `raw/research/production-slm-case-studies/02-promptlayer-klarna-human-hybrid.md` — Klarna correction (metric-masked degradation, single-vendor failure, escalation capacity shortfall).
- `raw/research/production-slm-case-studies/04-google-cloud-octo-lessons-2025.md` — Google OCTO (atomicity failures).
- `raw/research/production-slm-case-studies/06-stanford-enterprise-ai-playbook-51.md` — Stanford 51-deployment study (organizational failure modes).

## Related

- [[error-analysis]]
- [[llm-as-judge]]
- [[topology-taxonomy]]
- [[benchmarks]]
- [[slm-agents]]
- [[context-engineering]]
- [[agentic-context-engineering]]
- [[klarna]]
- [[stanford-51-enterprise-playbook]]
- [[escalation-vs-approval]]
