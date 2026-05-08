# LangChain Deep Agents

LangChain's April 2026 blog post and `deepagents` open-source library, which generalize the Claude Code harness into four reusable components — **detailed system prompt, planning tool, sub-agents, and a file system** — and ship them as a vertical-agnostic library on top of LangGraph. Position implicitly: a competitor to (and abstraction of) the Claude Agent SDK. The post coins "shallow vs deep" as the axis along which a tool-calling loop becomes capable of long-horizon planning, and names Deep Research, Manus, and Claude Code as the canonical deep-agent examples. Capture is useful as both a primary anchor for that taxonomy and as a concrete general-purpose harness library a practitioner can `pip install`.

## Source

- `raw/research/weekly-2026-04-27/04-05-langchain-deep-agents.md` — captured 2026-04-27 from `https://www.langchain.com/blog/deep-agents`.

## Shallow vs deep

> "Using an LLM to call tools in a loop is the simplest form of an agent. This architecture, however, can yield agents that are 'shallow' and fail to plan and act over longer, more complex tasks."

Deep agents, by contrast, "dive deep on topics" — capable of planning more complex tasks and executing over longer time horizons. Deep Research, Manus, and Claude Code are cited; vertical-specific deep agents have emerged across coding, research, and customer support.

## The four components

The thesis: every deep agent in the wild combines four things.

1. **Detailed system prompt.** Reconstructed Claude Code system prompts are described as "long and complex," containing tool-use instructions and few-shot examples. The post emphasises that prompt engineering remains load-bearing — *"Prompting matters still!"*
2. **Planning tool (no-op Todo list).** Notably, the planning primitive in Claude Code is a *no-op*:
   > "Claude Code uses a Todo list tool. Funnily enough — this doesn't do anything! It's basically a no-op. It's just context engineering strategy to keep the agent on track."
   The Todo tool exists purely to materialize the agent's plan in its own context; nothing externalizes from it.
3. **Sub-agents.** Claude Code can spawn focused sub-agents for context management and prompt shortcuts. The post identifies sub-agent spawning as the *primary mechanism* for "going deep."
4. **File system.** Claude Code uses the file system not just to write code but "to jot down notes" — the FS becomes shared workspace and memory across the main agent and sub-agents. Manus is cited as another deep agent that makes "significant use" of the file system for memory.

## The `deepagents` library

`pip install deepagents`. Built over a weekend. Includes:

- A system prompt "inspired by Claude Code, but modified to be more general."
- A no-op Todo planning tool.
- Sub-agent spawning, with hooks for custom override.
- A **virtual file system implemented via LangGraph agent state** — *not a real disk FS*. The library "uses the agents state (a preexisting LangGraph concept)" as the storage substrate.
- An accompanying `open_deep_research` reference implementation.

The LangGraph backbone is the persistence layer. **Durable execution is not explicitly claimed**; the virtual FS via state is the persistence mechanism, not a durable-execution runtime.

## Where the abstraction is shaky

- **Virtual FS ≠ real FS.** Claude Code and Manus actually use a real disk filesystem with persistent files; `deepagents` uses LangGraph state. The post claims architectural equivalence, but this is *underargued*. State is ephemeral relative to the host process's lifetime; a real FS persists across processes and survives crashes (combined with git, as [[anthropic-effective-harnesses]] uses it). Practitioners adopting `deepagents` for long-running deployments should evaluate this carefully.
- **No-op Todo as "planning tool" framing.** Calling a no-op a "planning tool" is generous; it's better described as **a structured slot in the prompt that the model writes its plan into, returned to itself on the next turn**. This is meaningful (it materialises plan as context state) but is not external planning.

## How this fits the wiki

- **Counterpart to [[anthropic-effective-harnesses]].** Anthropic's harness post is the *primary-source case study* of running Claude Code-style harnesses for long-running agents; LangChain's Deep Agents is *the open-source generalization*. Pair as harness-design canon: one source on what a frontier-vendor's own harness looks like, one on what an OSS abstraction over it looks like.
- **Counterpart to [[claude-code-session-memory]].** Deep Agents' file-as-notes pattern and no-op Todo tool are direct lifts of mechanisms documented there. Cross-link explicitly so a reader navigating from "what does Claude Code do?" can land on "how do I get something like this in my own stack?"
- **Tension with [[skill-distillation]].** Deep Agents endorses sub-agent spawning as the core mechanism for depth and complexity. The Metric Freedom predictor in [[skill-distillation]] argues for collapsing multi-agent into single-agent when skill overlap is high. The two positions are not directly contradictory (Deep Agents could in principle be deployed as a single agent), but the rhetorical centre of mass is different. Worth tracking whether a future paper engages this directly.
- **Slots into the [[topology-taxonomy]] long-horizon-context-loss synthesis.** The shallow/deep axis maps onto existing topology distinctions: deep agents sit at the orchestrator-with-sub-agents end of the spectrum.

## Conflict flag (sub-agents vs skill-distillation)

Recorded but not load-bearing for an open conflict file: this source is the prescriptive-OSS-library side; [[skill-distillation]] is the empirical predictor side. They can coexist (different regimes) but a future post that argues one *over* the other on a shared workload would warrant opening `wiki/conflicts/sub-agents-vs-collapse.md`. Not opening one this week.

## Related

- [[anthropic-effective-harnesses]] — primary-source counterpart; same harness-design problem, vendor view vs OSS-library view.
- [[claude-code-session-memory]] — Claude Code's automatic memory layer; Deep Agents lifts the file-as-notes and no-op Todo patterns from here.
- [[anthropic-memory-tool]] — file-system-as-shared-memory pattern; Deep Agents' virtual FS is a lightweight analogue.
- [[codified-context]] — both treat system prompt + file-system KB as core context infrastructure; Deep Agents adds the no-op planning tool as a third element.
- [[skill-distillation]] — sub-agent spawning vs single-agent collapse; soft tension flagged.
- [[topology-taxonomy]] — shallow/deep axis maps onto the long-horizon-context-loss orchestrator-end of the topology spectrum.
- [[mcp-multi-agent-framework]] — sub-agent spawning + file-system collaboration overlaps with MCP multi-agent coordination.
- [[paperorchestra]] — concrete deep-agent in another domain; specialist sub-agents as the depth mechanism.
- [[ai-scientist-v2]] — hierarchical experiment manager fits the four-component model.
