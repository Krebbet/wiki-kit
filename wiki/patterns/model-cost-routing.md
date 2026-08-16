# Model cost routing (Switchyard)

LangChain benchmarked NVIDIA's open-source Switchyard router against its own Deep Agents eval suite (145 multi-step agentic tasks) and found that only 7% of turns actually needed a frontier model (Claude Opus 4.8) — routing the rest to a 30B open-weight model (Nemotron 3.5 Lightning) cut total cost 74% for roughly a 6-point accuracy hit. The post proposes a general decision rule — the *minimum offload* formula — for when per-turn model routing is worth adopting on a given workload, and is explicit that its own headline numbers don't statistically beat simply running the cheap model on everything. Vendor blog source; collect-but-confirm on absolute benchmark magnitudes, mechanism/methodology is trustworthy.

## Results

| Arm | Accuracy | Cost |
|---|---|---|
| Nemotron 3.5 Lightning alone | 77.7% | $0.72 |
| Claude Opus 4.8 alone | 86.0% | $11.45 |
| Switchyard-routed | 80.0% | $3.00 |

Nemotron handled 93% of model calls for 10.4% of spend; Opus handled 7% of calls for 68.4% of spend — a per-call cost ratio of roughly 87×. The routed arm was 74% cheaper than Opus-only at ~6 accuracy points lower (noise floor ~2.7 points across runs, so the gap is real).

**Escalating hard tasks to Opus only scored 2.3 points better than running the cheap model on everything** — smaller than run-to-run noise, so "routing beats naive cheap-model-only" is *not* statistically supported on this workload. The value came entirely from routing easy traffic away from the frontier model, not from correctly identifying hard traffic to escalate.

**Variance is real and directional**: frontier-traffic share ranged 4.1–9.1% (mean 6.9%) across five runs; per-run savings ranged 68.5–81.1%; cost ranged $2.16–$3.61 with nothing changed except which turns escalated. LangChain advises budgeting to the top of the range, not the mean.

## The hidden cost: the judge itself

The small classifier/judge model (Gemini 3.1 Flash Lite) runs on every turn until escalation and consumed 21.2% of routed spend — the second-largest line item, about a third of Opus's total cost, and it gets no prompt-caching benefit. LangChain flags it as the most obviously improvable lever in the setup.

## Minimum-offload formula

```
minimum offload = judge cost / (expensive cost − cheap cost)
```

For LangChain's pairing: $0.64 judge cost / $10.73 price gap = 5.9% required offload to break even; they cleared it 16× over (93% actual offload). If the two candidate models are close in price, the formula can demand more than 100% offload — routing cannot pay off unless the cheap model is effectively free to run (e.g., self-hosted on owned hardware).

## Routing mechanics and taxonomy

Escalation-mode LLM classifier: every task starts on the cheap model; the judge votes per turn; two consecutive negative verdicts (`confirmations = 2`) act as a one-way door that promotes the task to the frontier model for the rest of the session.

Three routing approaches are named: (1) **LLM classifier** (capability/escalation/custom submodes) — an extra model call per turn, higher accuracy potential, the mode benchmarked here; (2) **stage router** (heuristic, reads tool-call/error/token signals) — zero extra model calls, near-zero latency, not benchmarked in this post but noted as well-suited to dense tool-call agents like coding agents; (3) **prefill-activation MLP** (routes on model internals) — research-stage only.

**When not to use routing**: latency-sensitive workloads (the judge adds ~700ms/turn) and short workloads (escalation needs multi-turn trajectories to accumulate signal before it can fire).

## Methodology and caveats

The Deep Agents eval suite spans customer support (policy-constrained dialogue), on-call incident investigation, and multi-step workflow automation, drawing scenarios from τ²-bench airline, the Berkeley Function Calling Leaderboard, FRAMES, and Nexus. LangChain flags the suite as accuracy-saturated — only 8 points separate the 30B model from the frontier model on it — and explicitly cautions this is "a measurement of one workload, not a forecast for yours."

Two integration paths exist: a standalone Switchyard proxy server with TOML config (reproduces the benchmarked numbers), and a new experimental `SwitchyardRoutingMiddleware` for Deep Agents (in-process, no separate service, routing trace exposed via `response_metadata["switchyard"]`). The middleware is not yet published as a package, requires Python 3.12+ and deepagents 0.7.4+, and does **not** reproduce the blog's headline numbers since it currently uses different routing algorithms (stage router / random / noop) than the LLM-classifier escalation mode used for the benchmark.

## Source

- LangChain Blog, "How many of your agent's calls actually need a frontier model?" (2026-08-11) — https://www.langchain.com/blog/switchyard-agent-routing-benchmark

## Related

- [[coding-agents/langchain-deep-agents]] — this benchmark runs directly on that project's eval suite and integration surface; add a short pointer from that page to here
- [[patterns/agentic-harness-engineering]] — parallel cost/performance optimization effort on an agent harness, via harness-component evolution rather than runtime model routing
- [[patterns/agent-development-lifecycle]] — the Monitor phase and Build→Test→Deploy→Monitor→Iterate framing is a natural home for a cost-routing instance; same vendor voice
- [[evaluation/osworld-v2]] — parallel token/cost-efficiency tradeoff data point from a different angle (nonlinear token-efficiency curve vs. this page's cost/accuracy curve)
- [[evaluation/adk-arena]] — parallel efficiency finding (Claude Code resolving tasks at 8–10× fewer tokens); another instance of "cost efficiency varies enormously and is worth measuring explicitly"
