# Notion's Token Town (Latent Space, Simon Last + Sarah Sachs)

Practitioner case study from Latent Space's interview with Notion's Custom Agents team (2026). Notion launched Custom Agents after **four-to-five harness rebuilds** spanning 2022–2026, with two doctrinal lessons: *"build for what the model already understands, not for internal engineering convenience"* and an **explicit four-axis MCP-vs-CLIs framing** treating the two surfaces as complementary layers chosen on capability, determinism, permissioning, and pricing alignment. Resolves last week's watchlist entry on Notion's "Last Exam" evals.

> **Source caveat.** Latent Space podcast post (interview transcript with light editorial framing). This is a *secondary* source for Notion engineering — the substantive Notion engineering blog "5 Lessons from Building Custom Agents" is referenced in the post's footer but has not been captured separately. Direct quotes from Simon Last and Sarah Sachs in the transcript are higher-credibility than paraphrase; production claims should be flagged for primary-source confirmation.

## Source

- `raw/research/weekly-2026-05-04/02-notion-token-town.md` — captured 2026-05-04 from `https://www.latent.space/p/notion`.
- Companion (referenced but not captured): "5 Lessons from Building Custom Agents" on the Notion engineering blog; Sarah Sachs's "Token Town" notes-genre on running an AI eng team (see `https://x.com/sarahmsachs/status/2031473087791902991`).

## The 4-5 harness rebuilds

Reconstruction from the transcript (~00:47:43–00:54:00):

1. **Late 2022 — JavaScript coding agent.** First version exposed all of Notion's surface as JavaScript APIs and asked the model to write code. *"It just sucked at writing code. It wasn't that good."*
2. **Custom XML tool-calling DSL.** Tool-calling didn't exist as a model-level concept yet; Notion designed its own XML format that *"losslessly mapped to Notion blocks"* with mutation operations. Failed because *"we were catering way too much to what made sense for Notion and Notion's data model versus what the model wants."* The model didn't know the XML format and had to be prompted into it every turn.
3. **Notion-flavored Markdown.** Replaced lossless XML with a simpler Markdown variant: *"It has to be just simple Markdown at the core, and then we can add some enhancements. And it doesn't have to be a full lossless conversion."*
4. **SQL-lite database query layer.** Notion's API uses *"a crazy JSON format"* to query databases; scrapped that for the agent surface and exposed a SQLite-like query interface. *"The models are super good at that."* Underlying storage remains Postgres + a sharded SQL cluster — the agent surface deliberately diverges from the persistence layer.
5. **Tool-calling abstractions + research mode + few-shot prompting.** Sarah Sachs adds intermediate steps: tool-calling, then a *"research mode"* (not fully agentic tool-calling), then *"we moved away from few-shot prompting entirely to tool definitions."*
6. **Progressive tool disclosure (about-to-ship at recording time).** Latest harness has 100+ tools just for Notion; eager exposure became a problem (*"saying hello was thousands and thousands of tokens"*). Solution: tool search / progressive disclosure so the model only sees relevant tools per turn. Sarah names this as the lever that finally let tool ownership be **distributed across teams** instead of bottlenecked through a single five-or-six-person system-prompt-owner cohort. Internal name: "Agent 2.0."

## The "build for what the model understands" doctrine

Stated explicitly twice. *"Give the models what they want."* and *"Be savvy and really careful thinking about what the model wants in terms of its environment, and cater around that. And really try so hard not to expose it to any complexity about your system that's unnecessary."*

The XML→Markdown and JSON-database-format→SQL-lite migrations are the canonical examples.

This is a third-position data point for [[conflicts/agents-md-effectiveness]]: it suggests the right unit of analysis isn't *human-authored vs LLM-generated context* — it's **internal-engineering-convenience vs model-native representation**.

## MCP vs CLIs — the four axes

Simon Last is *"definitely bullish and excited about CLI"* but *"still bullish on MCP"* in specific environments. Explicit four-axis comparison:

| Axis | Winner | Detail |
|---|---|---|
| **Capability / bootstrap power** | CLIs | CLIs run in a terminal env, get pagination/cursor over long outputs, inherent progressive disclosure via `--help`. *"Inherently bootstrapped — if there's an issue, the agent can debug and fix itself within the same environment."* MCPs by contrast: *"if the transport gets messed up, the agent has no way to fix itself."* |
| **Permissioning** | MCPs | *"MCP inherently has a really strong permission model, like all you can do is call the tools. A CLI is a little bit murkier."* CLI re-encryption of API tokens, exfiltration risk, are *"real and hard to solve."* |
| **Determinism (for known tasks)** | CLIs | Sarah Sachs: *"Needing language to execute deterministic tasks feels wasteful, and requiring on a language model to interface with third-party providers seems wasteful for tasks that don't require it."* |
| **Pricing alignment (at scale)** | CLIs | Tied to Notion's usage-based credit pricing. *"If we can have our agents properly execute code that calls on CLI deterministically, it's a one-time cost. Versus constantly having a language model integrate with an MCP over and over and over and paying those repeated token fees, and it's happening outside the cache window."* |

Synthesis: *"There's not really a conflict here. There's just different layers of the stack and different abstractions."* MCP wins for narrow, lightweight, tightly-permissioned tools and the long-tail of third-party connectors; Notion ships an MCP server *and* an MCP client. CLIs win for capability-heavy bootstrapping where self-debug matters and per-turn token cost would dominate. Notion built Slack and (Notion) Mail integrations natively in-house rather than via MCP for quality control on the high-traffic search path; uses MCP for Linear and GitHub.

## 100+ tools and progressive tool disclosure

Latest agent has *"over 100 tools just for all the crazy Notion stuff."* Tool list is publicly inspectable: *"You can ask the agent and we'll tell you. … We don't think our system prompt is our secret sauce."* Plans to publish a tool benchmark.

**Tool naming collision** is a real failure mode: *"We have crazy things where we write two tools that have the same title and the agent crashes."* Anthropic models couldn't handle two tools with the same name; OpenAI GPT-5.2 *"could figure this out"* — discovered through a sev. (Anecdotal but a concrete fragility data point.)

**Distributed tool ownership** is the velocity lever. Pre-progressive-disclosure, the system prompt was a single string maintained by 5–6 people because *"all context is not created equal — the higher up it is in your examples, the more the model listens."* Moving to (a) tool definitions per team and (b) progressive disclosure let every team own its own tool + tool definition + eval. Sarah: *"The biggest lever on how we've scaled."* Cost: the AI team had to transition from center-of-excellence to platform team *"overnight."*

## Evals — Notion's "Last Exam" + Model Behavior Engineer

Three eval tiers:

1. **Regression / unit-test-equivalent in CI.**
2. **Launch-quality evals at 80–90% pass per user journey.**
3. **Headroom / frontier evals deliberately calibrated to ~30% pass rate** — exists because earlier evals *"saturated and we weren't able to really give insightful feedback other than it wasn't worse."*

Full-time staff dedicated to headroom evals: a data scientist, a Model Behavior Engineer, an evals engineer. Headroom evals are also fed back to Anthropic and OpenAI as pre-release model-snapshot feedback.

**Model Behavior Engineer (MBE)** is a distinct function. Started as *"data specialists"* (linguistics PhD dropout + Stanford new grad) doing manual yes/no labelling of Google Sheets outputs for Simon. Evolved into a permanent role distinct from software engineering. Now build agents-that-write-evals and LLM judges; do failure triage; supply taste-and-instinct judgment. *"We have very firm conviction that … you don't need an engineering background to be the best at this job."*

This **resolves the watchlist entry from week 2026-04-27** (Notion's Last Exam evals were flagged as a candidate).

## Self-configuring agents and the "flippy" UX

Custom agents can configure themselves: write their own system prompt, debug their own failures, edit their own instructions. The setup interaction is the same chat surface as the using interaction (single chat input does both — *"flippy"* is the internal name for this UX flip). Agents are explicitly **not allowed to edit their own permissions** — an admin-mode synchronous chat is required for that. The launch was delayed ~1 month to ship this UX over a previous separate-settings approach.

Simon: *"Imagine your agent can actually automate itself out of a job. Right? We would love if that were true."*

## Memory as pages, manager-agents

No built-in memory primitive. *"If you wanna give a memory, just give it a page and give it edit access to that page."* Same for inter-agent communication: agents file issues into a shared "issues" database that a manager agent reads. *"We didn't make any special concepts at all."* Deliberate primitive-composition design: don't invent new abstractions if existing data primitives can carry the semantics.

**Manager-agent topology.** A go-to-market team built 30+ custom agents and started getting 70+ blocked-on-things notifications/day. Notion shipped a manager-agent abstraction (about-to-ship at recording time) that has access to invoke all the other agents and reduces 70 notifications to ~5 by triaging and unblocking subagents. Direct relevance to multi-agent topology and the F-predictor question — see [[skill-distillation]].

## Pricing as Notion credits

Credits abstract over: token throughput × model tier × serving tier (priority vs async) × cache rate × non-token costs (web search, fine-tuned/open-source served on GPUs, future sandbox costs). Sarah: *"All tokens are not made equal."* "Auto" picks the right model for the task — explicitly framed as a robo-advisor analogy.

**Auto is *not* a margin-maximiser**: *"We aren't fully incentivised just for you to use as many tokens as possible. We're actually really interested in giving you the right tool for the job. A lot of the time, the right tool for the job is actually just writing code and not even using an agent at all."* Model selection is a deliberate counter-incentive against frontier-lab pricing trajectories.

## Org and cultural primitives

- **~50 people** on Core AI Capabilities & Infrastructure (Sarah's org); **30–40** on per-surface "packaging" teams (Custom Agents, Meeting Notes, Cortex chat).
- Company-wide mandate: every product surface team owns the tool definitions for the agent's interaction with that surface (e.g. the editor team that built CRDTs for offline mode also owns multi-agent block-editing conflict resolution).
- *"Anyone working on product engineering is tasked with making them work for customers that are humans and agents because over time the majority of our traffic will be coming from agents using our interface, not humans."*
- **Cultural primitives**: "Demos over memos" (Brian Levin). "Simon Vortex" (high-velocity prototype phase that senior engineers cycle in and out of, kept distinct from production). Security pulled in **first**, not last (counter to typical practice; Sarah cites Robinhood scar tissue). "Token Town" is Sarah's broader notes-genre on running an AI eng team.

## Engineer role transition

Simon: *"The human role becomes more about observing and maintaining the outer system. There's a string of agents flowing through, MeRPRs, what's going off the rails, what do I need to approve, is there a learning or memory mechanism that works."*

Sarah: every Notion engineer this summer went through *"the identity crisis that every manager goes through, where all of a sudden they realise their ability to write code is less important than their ability to delegate and context-switch."*

Direct echo of the [[willison-cognitive-cost]] and [[anthropic-internal-study]] findings.

## Notable anecdotes worth keeping

- Custom Agents was *"in alpha for a little bit"* before launch; rebuilt 4–5 times since 2022.
- One Anthropic account rep DM'd Sarah asking *"is Simon trying to prove string theory?"* after he hit context limits on a coding agent thread — it had been running for **17 days continuously** and had compacted *"like a hundred times"* before they realised it was a harness bug.
- Cross-vendor model quality variation: same advertised model serves differently through first-party vs Bedrock vs Azure — *"we hire subprocess to figure that out for us."*
- Subtle latency degradation during working hours observed across providers; quality degradation more often shows up across vendors of nominally the same model.
- Notion is *not* training a foundation model. Where Notion *does* fine-tune: enterprise-specific models (with ZDR / no-data-retention contracts) and **retrieval/ranking** for agent-driven search. The retrieval reframe is significant: *"the search load and the search traffic — majority of it's coming from agents, not humans"* on AI-enabled enterprise plans. Vector embeddings *"are less and less"* the right lever; query diversity (parallel exhaustive queries, model-generated query expansion) is replacing it.

## Roadmap-timing thesis ("agent lab")

Sarah's two skills for frontier-capability product work:
1. **Don't swim upstream** — quickly recognise when you're pressing against model capabilities vs missing infrastructure / context.
2. **Read where the river is flowing** — start building for capabilities that aren't here yet so the product is ready when they are.

The 4–5 rebuilds are themselves the operationalisation of this thesis — each rebuild marks a capability inflection that obsoleted the prior architecture.

## Related

- [[willison-cognitive-cost]] — peer practitioner case study; same engineer-role-transition observations from a different vantage (solo practitioner vs decacorn AI org).
- [[anthropic-internal-study]] — peer org-level case study; both observe the orchestrator-not-coder transition. Notion's MBE role is a concrete instance of the new-job-categories the Anthropic study predicts.
- [[anthropic-claude-code-postmortem]] — peer Anthropic case study; Bug 3's prompt-layer fragility (3% drop from a brevity instruction) cross-references Notion's tool-name-collision and 5-6-people-touching-the-system-prompt fragility findings.
- [[effective-harnesses]] — Anthropic's two-fold initializer-agent + coding-agent harness; Notion's 4-5 rebuilds + progressive tool disclosure is a multi-iteration counterpart.
- [[conflicts/agents-md-effectiveness]] — Notion's "build for what the model understands" doctrine reframes the conflict's axis.
- [[mcp-infrastructure]] — practitioner MCP-vs-CLIs four-axis comparison.
- [[topology-taxonomy]] — progressive tool disclosure as long-horizon-context-loss mitigation; manager-agent as multi-agent coordination pattern.
- [[agentic-context-engineering]], [[context-engineering]], [[codified-context]] — context-engineering peer cluster; "give the model what it wants" is the doctrinal counterpart at the *representation* layer.
- [[skill-distillation]] — Notion's manager-agent topology and "automate itself out of a job" framing relate directly to F-predictor.
- [[memory-architectures]] — "memory is just pages and databases" is a primitive-composition data point.
- [[cognition-cloud-agents]] — peer enterprise deployment; both ship usage-based pricing.
- [[paperorchestra]], [[ai-scientist-v2]] — peer multi-agent topologies (manager-agent + specialist subagents).
- [[openai-symphony]] — peer 2026 practitioner-narrative case study on harness engineering, captured the same week.
