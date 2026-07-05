# LangChain RLMs in Deep Agents *(2026-07-05)*

LangChain has added recursive language model (RLM)-style programmatic orchestration to its Deep Agents library via a code interpreter and dynamic subagents. The core idea, drawn from MIT CSAIL research, is that instead of injecting a large input into a model's context window, the model treats the input as a variable in a REPL and writes code to chunk, dispatch, and recurse over it. This sidesteps context rot — the performance degradation that accumulates as context windows fill — and makes deterministic, scalable pipelines practical at inputs two or more orders of magnitude beyond a single context window.

## The RLM approach

Recursive language models (RLMs), proposed in arxiv:2512.24601 by Alex Zhang and collaborators at MIT CSAIL, reframe the relationship between a model and its input. Rather than injecting the full prompt into the context window, the model loads it as a variable inside a REPL and writes code to peek into, decompose, and recursively call itself over segments of it. This gives the orchestrator the same primitives available for processing large datasets — grep, partition, map, reduce — enforced by code rather than model judgment.

Two properties follow from moving orchestration into code:

- **Deterministic coverage.** A `for b in batches` loop touches every batch by construction. A plain model reasoning turn-by-turn cannot reliably sustain iterations at scale without losing track.
- **Bespoke pipeline shapes.** Because the orchestration is code, it can branch, parallelize, or sequence in whatever shape the task demands, unconstrained by what a model can carry out through tool calls alone.

The paper's REPL approach is strict: the entire prompt is loaded into the interpreter and recursed on directly, with recursive calls being plain LM calls rather than agents with tool access or persistent state.

## Deep Agents implementation

LangChain's Deep Agents implementation is closer to *recursive agents (RA)* than strict RLMs: each dispatched subagent has its own tool access and context state, not just a bare LM call. The RLM paper motivated the capability and architecture; the implementation is the library's own extension of that pattern.

Dynamic subagents require two components:

1. **QuickJS code interpreter middleware** — a secure, lightweight runtime installed via `pip install -U "deepagents[quickjs]"` and passed as `CodeInterpreterMiddleware` to `create_deep_agent`.
2. **Subagent definitions** — Deep Agents ships a general-purpose subagent; custom subagents can be configured with their own names, descriptions, and system prompts.

Dynamic subagents are triggered when the word `"workflow"` appears in the user prompt. A canonical example dispatches one summarizer subagent per page of a 300-page document using `Promise.all` over a mapped array of `task()` calls.

Mixed-model orchestration is a first-class feature: the orchestrator and subagents can run on different models. A frontier model can orchestrate open-weight subagents (e.g., GLM 5.2, Nemotron) for cost optimization, or the arrangement can be flipped for deep-research-style workflows.

LangChain cross-references Claude Code's six dynamic-workflow patterns — fan-out-and-synthesize, classify-and-act, adversarial verification, generate-and-filter, tournament, loop-until-done — as a useful vocabulary for the code patterns that emerge once a model has a REPL environment.

## Performance data

LangChain ran a proof-of-concept (explicitly not a comprehensive benchmark) on the OOLONG AgNews task: thousands of headlines with dates and users attached, no visible topic label, requiring classification into four categories and aggregation across the full set. Scores are averaged across the question set using OOLONG's scoring (exact match for categorical answers, partial credit for numeric answers on a 0–1 scale).

**Collect-but-confirm** — these are vendor-run scores on a single proof-of-concept workload with no task-specific prompt optimization; treat directionally rather than as production benchmarks:

| Context length | Plain agent | RLM-enabled agent |
|---|---|---|
| 64k | 0.58 | 0.67 |
| 128k | 0.44 (often refuses to answer) | 0.79 |

At 64k the plain agent mostly keeps up, with lower latency. At 128k the plain agent frequently declines to compute rather than returning a wrong answer. The RLM-enabled agent at 128k uses fewer tokens overall but costs more due to higher output token volume (generated orchestration code). LangChain notes these numbers likely undersell RLM potential since the workload received no task-specific tuning.

## Source

- LangChain blog — "How to Use RLMs in Deep Agents" (2026-07-05): https://www.langchain.com/blog/how-to-use-rlms-in-deep-agents
- MIT CSAIL RLM paper: arxiv:2512.24601
- OOLONG benchmark: arxiv:2511.02817
- Deep Agents dynamic subagents docs: https://docs.langchain.com/oss/python/deepagents/dynamic-subagents

## Related

- [[coding-agents/langchain-deep-agents]] — the base Deep Agents library this extends
- [[patterns/anthropic-context-engineering]] — context rot is the motivating problem RLMs address
- [[patterns/context-engineering]] — RLMs as a mechanism alongside JIT retrieval and compaction
- [[patterns/topology-taxonomy]] — programmatic orchestration adds an execution-layer dimension to agent topology
- [[patterns/skill-distillation]] — RLMs invert skill-distillation: recurse one model into many vs. collapse many into one
