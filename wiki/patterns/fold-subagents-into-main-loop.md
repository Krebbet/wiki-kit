# Fold Subagents into the Main Agent Loop

Anthropic Applied AI's guidance (claude.com, captured 2026-10-25) argues that many enterprise multi-agent designs (routers, planners, one subagent per team or domain) should be folded into a single agent loop that uses skills for progressive context disclosure and tool search for progressive tool disclosure. Subagents stay only for three conditions: measurable context bloat, parallel work needing fresh discardable contexts, and tool-selection or instruction conflicts. This is vendor-primary design guidance with a sales incentive (it promotes single-loop, skills, and claude-api tooling); the decision criteria are usable as stated, but the performance comparisons are internal, unnamed, and unquantified (vendor-claimed, collect-but-confirm).

## Target design

- One model, one context window, an open-ended tool loop. The model writes and revises its own plan in context and emits parallel tool-call batches; the harness enforces only limits (turn and cost budgets, write gates).
- Ordering and domain procedure move into skills. Hard limits (validation, approval gates, per-user permission checks, memory lookup) move into tools that return plain-language refusals or instructions the model can act on.
- Code is kept only for cheap always-relevant loads (e.g. entity resolution) and mechanical work. Knowledge bases sit behind search tools or skill reference files, not code-retrieved-and-pasted context.

## When to keep a subagent

1. Measurable degradation from context bloat in a single loop.
2. Parallel tasks that need fresh, discardable context windows.
3. Tool-selection trouble or conflicting system-prompt instructions.

Heuristic: split by context, not by problem type. Give a subagent work that needs little from the rest and returns a compact result (independent research paths, clean-interface components, black-box verification). Problem-type splits produce a "telephone game" of lossy handoffs. Full handoff only when the subagent must talk to the user directly.

## Staged fold-in method

1. Build a small end-to-end eval first (shared central set plus per-skill sets owned by the contributing team); even about 10 golden examples is enough to start. Track routing accuracy while an orchestrator exists, then skill-loaded/tool-called accuracy after folding.
2. Merge tightly coupled specialists first (chained, same data, often called together).
3. Optionally wrap kept subagents as tools of the main agent for a baseline without rewriting them (shared response schema, main agent verifies conclusions).
4. Fold one at a time: prompts become skills, API calls become MCP tools; compare eval with and without. Keep the subagent only if the folded version scores worse.

Run each task more than once and inspect which tasks flipped, not just the aggregate score. The post's anecdote: in a sample support agent, folding one subagent into another cut latency but broke a previously passing process (the main agent held the order-lookup tool and answered without asking the shipping specialist for the delivery date), visible in 1 of 2 runs.

## Numbers (few, mostly unquantified)

- One customer saw roughly 2x faster runtime for a single loop vs their multi-agent harness (vendor-claimed, unnamed).
- Progressive disclosure cut Claude Code's system prompt by over 80% for more advanced models (cited from a separate claude.dev post).
- Tool choice degrades past 30-50 tool definitions in the prompt.
- A single agent with skills "frequently" beat both one-prompt and subagent designs on quality, "often" at lower cost and latency; no figures.

## Organizational failure modes

Subagent sprawl (hundreds of overlapping subagents, no owners), "Frankenprompt" (every team appends to the system prompt), overly localized evals, context loss between agents, and latency; architecture mirrors the org chart (Conway's law). Remedy: one small central team owns the system prompt and end-to-end quality and vets every tool, skill, and eval; per-team DRIs own skills with evals.

## Model-trend claim and tooling

The post asserts that from Opus 4.5 onward models manage far more in one loop, and that rigid multi-agent structure often blocked new models from taking on more work (vendor-asserted, no measurement shown). A migration kit is released at github.com/anthropics/single-agent-loop-kit, chaining claude-api skills (build-eval, prompt-audit to flag instructions written for older models, hillclimb for folded-vs-kept comparison, cost-optimize) plus /skill-creator and /skill-doctor (skill cost and usage audit). The article has no data tables or eval datasets.

## Tension with other wiki pages

The default-against-subagents stance sits against [[deployments/anthropic-finance-agents]] (skills + connectors + subagents packaging), [[patterns/harness-design-space]] (Multi-Agent Orchestrator is the most common pattern, 31.4% of a 70-project survey), and [[coding-agents/langchain-deep-agents]] / [[patterns/deep-agents-context-engineering]] (subagents as a core context-isolation technique). This is most likely a scope narrowing, not a hard contradiction: the post targets enterprise multi-team customer agents and explicitly exempts research, verification, and parallel workloads. Not elevated to `conflicts/`; revisit if a curator ruling is wanted.

## Source

- `raw/research/weekly-2026-10-25/01-fold-subagents-into-main-loop.md` — Anthropic Applied AI, "Building agents: When to fold subagents into your main agent loop" (claude.com, captured 2026-10-25). Vendor primary.

## Related

- [[deployments/anthropic-commerce-agents]] — the cited concrete single-loop-plus-skills deployment; this page is the generalizing guidance.
- [[patterns/skill-distillation]] — practitioner, eval-driven counterpart to collapsing multi-agent into single-agent (no Metric Freedom predictor).
- [[patterns/topology-taxonomy]] — the context-split rule and fold-in decision step extend the mitigation classes.
- [[patterns/agent-skills]] — skills as the replacement unit for specialist subagent prompts; DRI-owned skills with evals.
- [[patterns/anthropic-context-engineering]] — progressive disclosure vs sub-agent technique; default shifts away from sub-agents.
- [[patterns/claude-platform-cost-optimization]] — same claude-api subcommands reused for fold-in comparison.
- [[patterns/sierra-context-engineering]] — progressive disclosure as load-bearing mechanism.
- [[deployments/mcp-infrastructure]] — tool search, deferred loading, and the 30-50 tool threshold.
- [[case-studies/notion-token-town]] — progressive tool disclosure; simpler loops move more easily to the next model.
- [[deployments/anthropic-finance-agents]], [[patterns/harness-design-space]], [[coding-agents/langchain-deep-agents]], [[patterns/deep-agents-context-engineering]] — the subagent-default tension noted above.
