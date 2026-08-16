# GPT-5.6's trained-in agentic primitives

OpenAI's "builder's guide to GPT-5.6" (vendor primary, co-authored by four OpenAI staff drawing on startup production experience) argues that GPT-5.6 makes frontier-level agent performance dramatically cheaper through smarter model selection plus three new Responses API primitives — reasoning persistence/native compaction, native multi-agent orchestration, and programmatic tool calling — that are trained end-to-end into the model rather than bolted on as harness-side techniques. This is a notable counterpoint to the wiki's harness-centric pattern cluster: where [[patterns/effective-harnesses]], [[patterns/agentic-harness-engineering]], and [[coding-agents/langchain-rlms]] treat compaction, orchestration, and code-based tool-calling as things you build into the surrounding scaffold, OpenAI's claim is that the model-plus-API layer is absorbing them directly.

## Native multi-agent orchestration

Enabling multi-agent in the Responses API lets a primary agent spawn parallel subagents that pursue objectives independently and pass output back for final synthesis — described as the mechanism behind ChatGPT's "ultra" capability setting. It's steerable: explicit instructions on when to spawn subagents reduce wasted token spend. Customer quotes cited: Qualia ("GPT-5.6 Sol just clicked" on multi-agent research) and Obvious ("best orchestrator we've seen... threw six specs at it at once").

## Reasoning continuity and native compaction

Reasoning can now persist across model turns, and native compaction compresses long-running conversations, letting the model maintain coherence across longer task horizons "without getting confused or having to reconstruct prior context." OpenAI frames this explicitly as a trained-in architectural capability, not a harness-side technique — a materially different position from the wiki's existing "compaction isn't sufficient" / compaction-as-first-lever discussion in [[patterns/effective-harnesses]] and [[patterns/anthropic-context-engineering]].

## Programmatic tool calling

The model writes JavaScript to orchestrate tools — filtering, aggregating, and running tool calls in parallel, processing outputs outside the model's context window, reserving tokens for judgment rather than mechanical work. Example target use case cited: an agent retrieves 100 filings, filters by date, identifies relevant transactions — the filtering/combining shouldn't consume context. This closely parallels LangChain Deep Agents' QuickJS-based programmatic orchestration (see [[coding-agents/langchain-rlms]]), but here shipped as a native, trained-in production primitive rather than a framework-level proof of concept.

## Benchmark and cost numbers

- **Agents' Last Exam**: GPT-5.6 Sol at "low" reasoning effort outperformed GPT-5.5 at "high" reasoning effort, harness held constant. See [[evaluation/agents-last-exam]] for the prior GPT-5.5-era baseline this extends.
- **BrowseComp**: GPT-5.5 (Extra High) scored 84.36% at $33.27 total cost (three months prior); GPT-5.6 Luna (Extra High) scored 84.04% — essentially the same score — at $1.33, roughly a 25× cost reduction for equivalent performance.
- **ARC-AGI-3**: GPT-5.6 Sol scored 13.3% with a standard harness; after enabling retained reasoning + compaction, the same model jumped to 38.3% while using ~6× fewer output tokens, with no changes other than the two primitives.
- Prompt cache TTL extended to a minimum of 30 minutes across the entire model family; cache breakpoints can now be set deterministically within context.

## Model-selection economics

OpenAI's claim is that smaller 5.6-family models (Terra, Luna) now approach flagship (GPT-5.4/5.5)-level performance on long-horizon/tool-calling tasks at much lower cost — where flagship-at-highest-reasoning was previously categorically necessary for long-horizon work. Example given: legal-tech memo extraction can move from a frontier model to Terra/Luna for cost savings without a corresponding capability cliff.

## Source

- OpenAI, "The builder's guide to GPT-5.6" (2026-08-13) — https://openai.com/index/builders-guide-to-gpt-5-6/

## Related

- [[coding-agents/langchain-rlms]] — same "move deterministic work into code" idea; here it's a native, trained-in production primitive rather than a framework-level proof of concept
- [[patterns/code-as-agent-harness]] — programmatic tool calling is a concrete production instance of "code as runtime substrate," extended here with a vendor-native example
- [[patterns/effective-harnesses]] and [[patterns/anthropic-context-engineering]] — OpenAI's claim that compaction is trained into the model itself, not a harness-side technique, is a materially different position worth flagging against these pages' framing
- [[patterns/topology-taxonomy]] — native multi-agent orchestration is another vendor-native instance of the multi-agent/manager-agent topology class, comparable to [[deployments/openai-symphony]]'s custom-built orchestrator
- [[deployments/openai-symphony]] — same vendor, prior primary source on a custom-built multi-agent orchestrator; this guide describes a native API version of similar capability
- [[evaluation/agents-last-exam]] — this page cites new GPT-5.6 Sol results on the same benchmark; a same-benchmark, newer-model data point worth appending there
- [[patterns/harness-design-space]] and [[patterns/agentic-harness-engineering]] — model-vendor-native primitives absorbing prior harness-level design choices is a data point for the "where does capability live" discussion in these pages
- [[patterns/model-cost-routing]] — same week's other cost-engineering thread; different mechanism (frontier-vs-cheap routing vs. cheaper-frontier-model-itself) toward the same goal of lower agent spend
