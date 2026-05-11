# Cursor — Continually Improving the Agent Harness (2026-04-30)

Cursor's engineering blog describes their iterative harness development methodology as the central lever for agent quality, asserting that the same model inside a well-tuned harness is *"noticeably faster, smarter, and more efficient"* than in a generic one. The post covers their eval stack, online A/B methodology, observability-driven reliability engineering, per-model customization, and mid-chat switching mitigations — and frames multi-agent orchestration as the harness challenge that defines the next phase of AI-assisted software engineering.

## Source

- Cursor Engineering Blog, "Continually improving our agent harness," 2026-04-30 — `raw/research/weekly-2026-05-08/01-cursor-agent-harness.md`. Authored by the Cursor team. Primary practitioner source.

## What Cursor evaluates the harness on

### CursorBench (offline)

Cursor maintains [[evaluation/swe-bench-pro|public benchmarks]] alongside CursorBench, their internal eval suite. CursorBench provides a fast, standardized, time-comparable read on quality. Acknowledged limitation: even the best benchmarks only approximate real usage.

### Keep Rate (online)

For a given set of agent-proposed code changes, Cursor tracks what fraction remain in the user's codebase after fixed time intervals. A drop signals users had to manually adjust output or re-run the agent — indicating lower-quality initial responses. The metric captures outcome, not just output.

### LLM-as-judge satisfaction (online)

A language model reads user follow-up responses to the agent's initial output and classifies semantic satisfaction. Examples used in the post: a user moving on to the next feature = strong positive signal; a user pasting a stack trace = reliable failure signal. This layer captures fuzzier quality dimensions that token or latency metrics miss.

### Tool reliability — 3 nines target

Tool call errors are treated as a broad bug surface. In a focused sprint, Cursor drove all tool calls to at least 2 nines (99%) and often 3 nines (99.9%) reliability — described as an order-of-magnitude reduction in unexpected errors.

## What changes harness quality

### Static → dynamic context evolution

When Cursor's coding agent launched in late 2024, models were weaker at choosing their own context. The harness compensated with heavy static context and guardrails:

- Folder layout of the codebase always in context
- Semantically-matched code snippets
- Compressed versions of manually attached files
- Lint and type errors surfaced after every edit
- File reads rewritten when the agent requested too few lines
- Per-turn tool-call caps

By publication date, *"that is mostly long gone."* Remaining static context is minimal: OS, git status, current and recently viewed files. The shift is framed as adaptation to increasing model capability — guardrails knocked down, replaced by agent-driven dynamic context fetching.

### Context rot

Accumulated tool call errors remain in context and degrade the quality of subsequent model decisions. Named explicitly as "context rot." The compounding effect is why error rates matter beyond their direct cost: even self-corrected errors pollute the context window.

Error taxonomy used in production:
- `InvalidArguments` — model mistakes
- `UnexpectedEnvironment` — contradictions in the context window
- `ProviderError` — vendor outages (e.g., `GenerateImage`, `WebSearch`)
- `UserAborted`, `Timeout` — expected operational states

Unknown errors are always treated as bugs and trigger fixed-threshold alerts. Expected errors are monitored with per-tool, per-model anomaly detection baselines, because different models fail tool calls at different rates.

### Per-model tool format provisioning

All harness abstractions are model-agnostic at the layer but heavily customized per model in practice:

- OpenAI models are trained on a patch-based file edit format
- Anthropic models are trained on string replacement

Giving a model the unfamiliar format *"costs extra reasoning tokens and produces more mistakes."* Cursor provisions each model with the format it saw during training.

Prompting customization goes deeper: OpenAI models described as *"more literal and precise in their instruction following"*; Claude described as *"a bit more intuitive and more tolerant to imprecise instructions."* Customization extends to individual model versions.

### Context anxiety (named model quirk)

One unnamed model developed a behavior Cursor calls "context anxiety": as its context window filled, it would begin refusing work, hedging that the task seemed too large. Mitigated via prompt adjustments. Noted as an example of genuine model quirks addressable at the harness layer.

### Mid-chat model switching

When a user switches models mid-conversation, Cursor automatically swaps to that model's harness (custom prompts and tools). The incoming model must apply its tools to a conversation history that is out of distribution from its training — produced by a different model with a different tool set.

Mitigations:
- Custom injected instructions tell the new model it is taking over mid-chat and steer it away from calling tools from its predecessor's toolset
- Conversation summarization at switch time tested as a cache-penalty mitigation; found to lose detail on complex tasks
- Subagents (fresh context windows) named as the preferred alternative for complex mid-session model switches

Cache miss at switch time is structural: caches are provider- and model-specific.

### Summarization model A/B test — null result

Cursor tested a more expensive model for context summarization and *"observed it made a negligible difference in agent quality that wasn't worth the higher cost."* Idea was shelved. This result sits adjacent to [[patterns/context-folding]]'s argument that proactive variable-granularity folding is load-bearing — the specific summarization strategy tested may differ.

### Automated observability loop

A weekly Cloud Agent Automation searches logs, surfaces new or recently spiked issues, and creates or updates tickets in a Linear backlog with investigation notes. Cursor describes this as part of instantiating an *"automated software factory"* for the harness.

## Notable claims and findings

- **Harness quality > model selection.** The harness and model together determine agent quality; the post frames harness tuning as the primary lever distinct from model swaps.
- **Static context was not a permanent solution.** The late-2024 guardrail-heavy design is explicitly described as a response to weaker models — not an architecture Cursor would choose today.
- **Dynamic context shift is practitioner-confirmed.** The trajectory from heavy static to agent-driven dynamic context in production, at scale, corroborates [[patterns/context-engineering]]'s direction and extends [[patterns/effective-harnesses]]'s account of compaction limits.
- **Summarization model upgrade → negligible quality diff.** Vendor-stated A/B result in production. Load-bearing null finding: not all harness components respond to model quality upgrades.
- **Tool reliability is a first-class harness metric.** 3-nines target and the error taxonomy are described as part of the software quality process, not a one-time audit.
- **Per-model tool format provisioning matters measurably.** Extra reasoning tokens and more mistakes when the format is unfamiliar — vendor-stated.
- **Multi-agent future = harness challenge.** Cursor explicitly frames orchestration logic (dispatch, task framing, result stitching) as living in the harness rather than any individual agent.

## Open questions / future work named by source

- Multi-agent orchestration: how the harness will learn to dispatch across specialized agents (planner, fast-edit, debug) and stitch results into a coherent workflow
- Expanding ways for agents to dynamically pull context and interact with the world
- Scaling subagent support — users can already directly request a subagent with a specific model

## Related

- [[patterns/effective-harnesses]] — initializer + coding-agent harness; this page adds Keep Rate / LLM-judge metrics + per-model tool provisioning, context rot, and context anxiety
- [[patterns/agentic-harness-engineering]] — AHE evolves harnesses via observability automatically; Cursor describes manual but observability-instrumented iteration; both conclude harness quality dominates model selection
- [[patterns/externalization-survey]] — static→dynamic shift maps directly onto the weights→context→harness externalization arc; dynamic context fetching = skill externalization
- [[patterns/context-engineering]] — primary practitioner articulation of guardrail-removal direction; this page is concrete production evidence
- [[patterns/topology-taxonomy]] — multi-agent future direction (planner + fast-edit + debug) adds practitioner corroboration of the specialised-agent topology direction
- [[case-studies/notion-token-town]] — parallel: multi-generational harness rebuilds, per-model tuning, 100+ tools with progressive disclosure vs. Cursor's per-model tool format provisioning
- [[deployments/openai-symphony]] — both name "code/context for agent legibility" but from opposite directions: Symphony designs the codebase for agents, Cursor designs the harness per model
- [[patterns/codified-context]] — direct contrast: codified-context relies on 660-line static constitution + 34-doc cold KB; Cursor's trajectory is explicitly away from heavy static context toward dynamic fetching
- [[patterns/context-folding]] — Cursor's summarization-model-no-diff null result sits adjacent to AgentFold's variable-granularity argument; the strategies tested may differ
- [[patterns/sierra-monitor-eval-of-evals]] — peer LLM-as-judge methodology with a different calibration mechanism (Cursor: Keep Rate + judge as separate signals; Sierra: judge calibrated against multi-model + team-labeled agreement before deployment)
- [[patterns/agent-development-lifecycle]] — concrete production instantiation of the Lifecycle's Test + Monitor phases (CursorBench + Keep Rate + LLM-judge + automated-Linear-ticket loop)
