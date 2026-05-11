# Agent Development Lifecycle (LangChain, 2026-05-09)

LangChain's vendor framing post structuring agent development as a four-phase **Build → Test → Deploy → Monitor** cycle, with **Iterate** as the connecting motion and **Govern** as a wrapping concern. The post coins a clean three-layer typology of build tooling — **agent frameworks** (abstractions), **agent runtimes** (state + control flow + durability), **agent harnesses** (prompts + skills + MCP + hooks + middleware + optional FS) — that is articulated more clearly here than anywhere else in the wiki corpus. Vendor primary; self-positions LangChain / LangGraph / LangSmith / Deep Agents at each phase.

## Source

- LangChain Blog, "The Agent Development Lifecycle," 2026-05-09 — `raw/research/weekly-2026-05-11/01-langchain-agent-lifecycle.md`. Authored by LangChain (no byline in capture; voice consistent with Harrison Chase / LangChain leadership). Vendor primary.

## The lifecycle

> *Build → Test → Deploy → Monitor — the order is intentional. Testing should start before an agent reaches production, not after.*

The four phases form a closed loop: monitoring feeds traces back into evaluation datasets, which inform the next build. **Iterate** is named explicitly as the connecting motion; **Govern** wraps the loop with cost / tool-access / discoverability concerns at the org level.

For a single agent, the lifecycle stays lightweight. Across many agents, it becomes an infrastructure and governance challenge — shared ways to control cost, manage tool access, inspect tool calls, reuse context, and decide where humans need to be involved.

## Build — three layers of tooling

The post's most reusable contribution is the explicit three-layer typology:

| Layer | What it does | Examples named |
|---|---|---|
| **Agent frameworks** | Compose model calls, tools, prompts, retrieval, structured outputs, agent loops. Focus: *abstractions*. | LangChain, CrewAI |
| **Agent runtimes** | State, control flow, durability, human-in-the-loop. Focus: *execution*. | LangGraph |
| **Agent harnesses** | Prompts + skills + MCP servers + hooks + middleware + (optional) filesystem for longer-running tasks. Focus: *doing*. | Deep Agents, Claude Agent SDK |

The distinction matters because *"building an agent" can mean different things*. A simple tool-calling loop sits at the framework layer; a sophisticated long-running agent involves prompts + skills + MCP servers + middleware + retrievable context — a harness.

**No-code/low-code build path** named alongside: LangSmith Fleet, Claude Cowork, n8n. The post argues this matters because *"the person who understands the workflow needed is not always the person who writes the code."* Hooks and middleware are named as the engineering-control extension points across both code-first and no-code paths.

**Vocabulary tension worth flagging.** LangChain's *agent harness* layer has narrower scope (prompts / skills / MCP / hooks / middleware / sometimes a filesystem) than [[patterns/harness-design-space]]'s empirical *harness* (entry/control + context + tools + memory + safety) and the [[patterns/externalization-survey]]'s harness chapter. Both call it "harness." Reading either page, treat the term as overloaded.

## Test — datasets, metrics, simulations

Eval discipline is iterative, not preconditional: *"the goal is not to create a perfect eval suite on day one... the most valuable eval datasets are built from the hardest examples: first from development and dogfooding, then later from production."*

Four eval primitives:

- **Datasets** — preserve what teams learn; without them, the same failures reappear after prompt/model/tool changes.
- **Metrics** — split into *ground-truth correctness* (extraction / labeling / field updates) and *criteria-based* (grounded / followed policy / asked for clarification / efficient tool use).
- **Experiments** — what connect datasets and metrics to iteration; compare prompts, models, retrieval strategies, tool schemas, orchestration patterns against the same set.
- **Simulations** — for multi-turn agents, single-turn evals are insufficient; voice agents are an obvious example, but the pattern is broader (support agents, coding agents handling repo + tests + feedback, internal-ops agents).

## Deploy — runtimes, sandboxes, Context Hub

Production deployment requires:

- **Durable execution** — checkpoint + resume across failures. Off-the-shelf: LangSmith Deployment, AWS AgentCore, custom Temporal-based.
- **Human-in-the-loop** — pause for approval / clarification.
- **Sandboxes vs virtual filesystems**:
  - *Full sandboxes* (LangSmith Sandboxes, Daytona, E2B) when arbitrary code execution is needed.
  - *Virtual filesystem* (Deep Agents, optionally backed by Postgres or S3) when only file-as-working-memory is needed.
- **Prompt / Context Hub** — prompts, retrieval context, skills, task instructions are *not application code* and need to be versioned/reviewed/edited separately, often by non-engineers without a full deploy.

The Context Hub concept sits at the same architectural location as [[patterns/codified-context]]'s 660-line constitution and [[patterns/effective-harnesses]]'s `feature_list.json` + `claude-progress.txt`: structured artefacts that bridge between sessions and between human authors and the agent.

## Monitor — traces, signals, feedback

> *The agent improvement loop starts with a trace.*

Traditional ops metrics (latency / cost / error / uptime) are necessary but insufficient — an agent can return a technically successful response and still fail the task.

**Two flavors of trace-derived signals:**

- **LLM-as-judge** — was the response grounded? was policy followed? was tone correct? See [[patterns/sierra-monitor-eval-of-evals]] for one vendor's calibration methodology for *the judges themselves* — Chase's post asserts the LLM-judge mechanism without specifying how the judge is validated; Sierra fills exactly that gap.
- **Regex / programmatic** — forbidden tool calls, required phrases, known failure patterns.

**Six dashboard-tracked metric families** named: usage, feedback, latency, cost, tool calls, evaluator scores — plus alerting on rising latency, increasing costs, failing tools, declining feedback, policy-violation spikes.

**Feedback** is stored *with* traces: LLM judges, regex signals, human reviewers, direct user feedback via API. LangSmith binds user feedback to the underlying run so "user unhappy" can be traced back to "agent used the wrong tool three steps earlier."

## Govern

Three named org-level challenges that scale with agent count:

- **Cost** — budgets, usage monitoring, per-agent + per-team + per-model attribution.
- **Tool access** — audit trails on every tool call (which agent / inputs / outputs / authorizing user-or-policy); HITL as governance mechanism by-design.
- **Discoverability and reuse** — shared prompts / skills / tools / sources / policies, especially load-bearing for skills.

> *Lightweight controls work for one agent; as organizations deploy more agents, governance becomes necessary.*

This connects directly to [[deployments/microsoft-agent-365]]'s vendor-product framing of agent-governance-as-product-tier and [[deployments/mcp-infrastructure]]'s 2026 roadmap items (audit trails, SSO, gateway, cross-vendor governance).

## Where this lifecycle sits relative to other 2026 framings

The Build → Test → Deploy → Monitor framing is generic and not load-bearing on its own — most production teams already operate something like this implicitly. What is genuinely useful and not articulated this clearly elsewhere is the **frameworks vs runtimes vs harnesses** typology and the explicit naming of *Context Hub* as a deployment-layer concern.

Compare:

- [[patterns/effective-harnesses]] — Anthropic's hand-designed initializer + coding-agent harness. Concrete instance of LangChain's "agent harness" layer; `feature_list.json` / `claude-progress.txt` artefacts match the Context Hub concept.
- [[patterns/agentic-harness-engineering]] — AHE is the *machine-evolved* operationalisation of the Monitor → Iterate → Build flow; observability-driven harness evolution is what the lifecycle calls the monitoring → evaluation → next-build feedback flow, automated.
- [[patterns/sierra-context-engineering]] — Sierra's eight-block taxonomy + progressive disclosure is a context-management practice in the Build phase; the sibling Sierra post on monitoring instantiates the Monitor phase.
- [[patterns/externalization-survey]] — the survey's memory + skills + protocols + harness arc is the *substance* lens; the lifecycle is the *process* lens. Both arrive at the same load-bearing externalisations.
- [[case-studies/cursor-agent-harness]] — Cursor's CursorBench + Keep Rate + LLM-judge + automated-Linear-ticket loop is the lifecycle's Test + Monitor phases instantiated in production.

## Caveats

- Vendor primary; the post is also a positioning document for LangChain / LangGraph / LangSmith / Deep Agents. Treat the layer typology as conceptually load-bearing, the product mentions as marketing.
- The post implicitly endorses structured external context (Context Hub, versioned prompts/skills) without engaging the AGENTbench negative result (see [[conflicts/agents-md-effectiveness]]). Adds vendor weight to the "structured context helps" position without controlled evidence.
- The post still treats prompts as a load-bearing Build-phase artefact that belongs in the Context Hub, but [[patterns/agentic-harness-engineering]]'s component ablation (+system_prompt only −2.3 pp) and [[case-studies/anthropic-claude-code-postmortem]]'s Bug 3 (3% intelligence drop from a single brevity instruction) both suggest the prompt layer is the most fragile externalisation. Reconcilable — prompts may be the *least* load-bearing externalised artefact but still externalised — but the lifecycle post does not acknowledge prompt-layer fragility.
- Two prior LangChain posts referenced inline ("Agent observability powers agent evaluation," "Traces start agent improvement loop") are load-bearing for the monitor → eval flywheel argument and not yet captured. Flagged for the watchlist.

## Related

- [[patterns/sierra-monitor-eval-of-evals]] — same-week vendor convergence; Sierra is the concrete Monitor-phase instantiation that fills the LangChain post's unspecified judge-validation gap.
- [[patterns/effective-harnesses]] — Anthropic's hand-designed harness; concrete instance of the harness layer; `feature_list.json` artefacts match the Context Hub concept.
- [[patterns/agentic-harness-engineering]] — machine-evolved Monitor → Iterate → Build automation.
- [[patterns/externalization-survey]] — substance lens to the lifecycle's process lens.
- [[patterns/sierra-context-engineering]] — Build-phase practice; Sierra ships the same lifecycle through both posts in 2026-05-05/05-07.
- [[patterns/harness-design-space]] — empirical 70-project counterpart with broader "harness" definition; vocabulary tension worth noting.
- [[coding-agents/langchain-deep-agents]] — LangChain's own four-component generalisation; canonical example in the harness layer.
- [[case-studies/cursor-agent-harness]] — Test + Monitor phases instantiated in production.
- [[case-studies/anthropic-internal-study]] — engineer-to-orchestrator role shift aligns with agents-as-repeatable-practice framing.
- [[patterns/topology-taxonomy]] — multi-agent topology choices belong in the Build phase; lifecycle layering is orthogonal to topology.
- [[deployments/microsoft-agent-365]] — vendor-product instantiation of Govern.
- [[deployments/mcp-infrastructure]] — Govern overlap on audit / discoverability.
- [[conflicts/agents-md-effectiveness]] — Context-Hub framing implicitly endorses structured context; vendor-prescriptive position.
