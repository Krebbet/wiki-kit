# Sierra — "Who Monitors the Monitors?" Eval-of-Evals (2026-05-07)

Sierra's vendor post on the calibration loop behind production agent **Monitors** — the always-on LLM-as-judge layer that scores every conversation. The load-bearing methodology claim is *eval-of-evals*: each monitor definition is grounded in team-labeled examples, scored by multiple models in parallel, and refined until model-vs-model and model-vs-human agreement are consistently achieved with clear rationale. Multi-model disagreement is read as a signal that the *definition* is malformed, not that one model is wrong. Vendor primary; companion to the prior week's [[patterns/sierra-context-engineering]].

## Source

- Sierra Engineering Blog, "Who monitors the monitors?", 2026-05-07 — `raw/research/weekly-2026-05-11/02-sierra-monitor-the-monitors.md`. Vendor primary. Short post (56 lines).

## The Monitors product

Always-on LLM-as-judge over every customer conversation. Production agents emit conversations fast enough that single misses (e.g. subtle rising frustration, a customer-supplied detail the agent missed) won't be caught by sample-based human review. Monitors run continuously as the quality and customer-sentiment signal layer.

**Two tiers:**
- *Sierra-authored* — out-of-the-box monitors for common patterns: looping, increasing frustration, false transfers.
- *Customer-authored* via Agent Studio — natural-language authoring surface for business-specific signals. Same calibration pipeline applies regardless of authorship.

## The eval-of-evals calibration loop

The substantive contribution. Sierra's monitor-build flow is: **definition → team-labeled examples → multi-model scoring → disagreement-driven refinement → consistent agreement + clear rationale = production-ready.**

Three explicit inputs to the calibration loop:

1. A precise behavioural definition of what to detect.
2. Hand-curated examples from real conversations.
3. Team-created labels on those conversations.

Multiple models score the conversations independently. **Disagreement among models, or disagreement against team labels, is the signal that the definition is too broad / too narrow / missing context** — not that one model is "wrong." Edge cases are fed back into the training/eval set until *models agree consistently and the reasoning behind each flag is clear*.

This is structurally distinct from a single-rubric LLM-as-judge: the iteration target is the *monitor definition*, not the judge model.

> *Multi-model agreement is the gating signal — not single-judge accuracy.*

## Rationale surfacing as a trust requirement

Every flagged conversation comes with the monitor's rationale visible to a human reviewer, not just a verdict. Accuracy is described as *necessary but insufficient*: trust requires the reviewer can see what was picked up on and decide whether to act.

This is the same observability commitment AHE ([[patterns/agentic-harness-engineering]]) makes through its three pillars — Sierra's rationale-surfacing maps to AHE's *experience pillar* on the agent side, and is the human-supervised counterpart on the monitoring side.

## The build → observe → understand → improve flywheel

Sierra positions Monitors as one node in a continuous improvement loop with two other named products:

- **Monitors** — *observe*: surface where agents fall short.
- **Explorer** — *understand*: cluster behaviours / interpret root causes.
- **Ghostwriter** — *act*: generate changes ("agents as a service" framing).

Monitors began as a standalone eval layer; this post repositions them as the surfacing engine for the rest of the Sierra build platform.

The flywheel as marketing vs methodology — the *eval-of-evals* methodology stands on its own; the architectural-loop claim is bundled with three named Sierra products. Treat the methodology and the product framing as separable.

## Worked example: WISMO

Sierra's chosen illustration is a "Where is my order" (WISMO) flow where the user's frustration is signalled subtly:

> User: Where is my order? It was supposed to arrive yesterday.
>
> Agent: Let me check that for you. Can you confirm your order number?
>
> User: I already gave it above.
>
> Agent: Can you please share your order number so I can look into this?
>
> User: omg can you please just return my item

Politeness marker, no profanity, no explicit complaint — but sarcasm and a pivot from "find my order" to "just return my item." Sierra explicitly names *this kind* of nuance (politeness markers + sarcasm + intent pivot) as the monitor's job.

## Industry-specific custom monitor examples

Sierra cites three:

- **Financial services** — flag unauthorized investment advice; language raising fair lending concerns.
- **Healthcare** — confirm sensitive calls are routed to the right *clinical pathway*.
- **Travel** — agent surfaces loyalty benefits at the right conversational moment.

## Where this fits the wiki

- Sierra's *eval-of-evals* fills exactly the gap left open in [[patterns/agent-development-lifecycle]]'s Monitor-phase abstraction: Chase says "an LLM-judge can score whether the agent answered the question, followed policy, used the right tone" without saying how the judge itself is validated. Sierra's calibration loop is the concrete vendor instantiation.
- [[case-studies/cursor-agent-harness]]'s Keep Rate + LLM-judge satisfaction signal is a peer methodology with a different calibration mechanism (Cursor: Keep Rate + judge as separate signals; Sierra: judge calibrated against multi-model + team-labeled agreement before deployment). Both vendors converge on LLM-judge-in-production but reach reliability via distinct paths.
- [[case-studies/notion-token-token]]-style 3-tier eval taxonomy (regression / launch-quality / "Last Exam" headroom) maps approximately to Sierra's launch-quality + production-monitoring layer; Sierra's eval-of-evals calibration is a mechanism Notion's account doesn't describe. Notion's MBE role is the closest org analogue to Sierra's "team labels examples" function.
- [[case-studies/anthropic-claude-code-postmortem]] Bug 3 (3% eval drop from a single brevity instruction) is empirical evidence for *why* always-on production monitoring matters: a single prompt-layer change produced a measurable but subtle production-quality drop.
- Offline benchmarks ([[evaluation/airs-bench]], [[evaluation/swe-bench-pro]], [[evaluation/agents-md-eval]]) sit at a different layer from Sierra Monitors — Monitors are an in-production observation surface, not a benchmark.

## Caveats and open questions

- **No calibration metrics disclosed.** The post asserts iteration continues "until the models agree consistently" but doesn't share inter-model agreement %, F1 vs human, or false-positive/false-negative rates. For a vendor source claiming methodology rigor, this is the missing quantitative anchor.
- **"Multiple models" is unspecified** — same-family ensemble vs cross-family? Same-vendor vs Anthropic + OpenAI + open-source? The agreement-is-the-signal mechanism's strength depends on this.
- **Post-deployment label-revision loop is undescribed.** The pre-production calibration loop is detailed; how production reviewer disagreements feed back into definitions over time is not.
- **No per-conversation cost data.** Always-on LLM-judge across every conversation is a first-order operating cost; the post is silent on token economics.
- **Customer-authored monitors going through "the same evaluation process"** is asserted but unspecified — does Sierra supply the team-labeled examples, or does the customer? If the customer, how does Sierra guarantee label quality?
- **Adjacent tension** (not a hard conflict) with [[case-studies/cursor-agent-harness]]'s null result on swapping a more expensive model for context summarization. Different layers (judge calibration vs context summarization), but both bear on whether multi-model methodology lifts production quality or only in narrow regimes.

## Related

- [[patterns/sierra-context-engineering]] — companion vendor post (2026-05-05). Context engineering = build-phase architecture; Monitors = observe-phase eval layer. Both belong to one Sierra platform narrative.
- [[patterns/agent-development-lifecycle]] — concrete vendor instantiation of the Monitor phase; fills the unspecified judge-validation gap.
- [[case-studies/cursor-agent-harness]] — peer LLM-as-judge methodology with a different calibration mechanism.
- [[case-studies/notion-token-town]] — 3-tier eval taxonomy peer; MBE role analogue.
- [[case-studies/anthropic-claude-code-postmortem]] — empirical case for why production monitoring matters.
- [[patterns/effective-harnesses]] — Sierra's flywheel is the operational counterpart to a single-shot harness design.
- [[patterns/agentic-harness-engineering]] — observability pillars overlap; Sierra's loop is the human-in-the-loop counterpart to AHE's machine-driven one.
- [[patterns/topology-taxonomy]] — Monitors-with-rationale + Explorer + Ghostwriter as a human-supervised observability loop, peer to AHE's machine-driven self-evolving variant.
- [[evaluation/airs-bench]] / [[evaluation/swe-bench-pro]] / [[evaluation/agents-md-eval]] — offline benchmark peers at a different layer (offline capability vs online production observation).
