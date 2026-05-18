# OpenAI Symphony / Extreme Harness Engineering

Latent Space podcast interview with Ryan Lopopolo (OpenAI Frontier Product Exploration) on the five-month *zero-human-written-code* experiment: **>1M LOC, >1500 PRs, 5 months, 0% human-authored, 0% pre-merge human review**, all driven by an Elixir-based orchestrator called **Symphony** that supervises multiple Codex agents over Linear tickets and Slack notifications. Coins (or popularises) **harness engineering** as the discipline of building observability/context/structure rather than tuning prompts. The wiki's extreme-scale data point on autonomous coding.

> **Source caveat.** Latent Space podcast post (`https://www.latent.space/p/harness-eng`) — interview transcript, *secondary* source. The primary OpenAI engineering writeup ("the article" referenced throughout) and a separate published Symphony spec / "ghost library" are *not* captured in `raw/`. Lopopolo's headline numbers (1M LOC, 1500 PRs, 5 months, 5–10 PRs/engineer/day, 1B tokens/day) are practitioner-asserted in conversation, not from a first-party engineering blog. Treat as practitioner-asserted, not independently verified.

## Source

- `raw/research/weekly-2026-05-04/03-openai-symphony.md` — captured 2026-05-04 from `https://www.latent.space/p/harness-eng`.
- Companion (referenced, not captured): the OpenAI Frontier "harness engineering" essay; the Symphony / "ghost-library" Elixir reference implementation by Alex Kotliarskyi.

## The "zero human code" constraint as method

Lopopolo deliberately refused to write code himself for five months on an internal Frontier beta product. *"Starting with this constraint of I can't write the code meant that the only way I could do my job was to get the agent to do my job."* The first ~6 weeks were *"10x slower than I would be"*; payoff came from the forced investment in primitives and tooling rather than direct authorship.

## Scale claims

| Metric | Value |
|---|---|
| Internal team | 3 people |
| Codebase | ~1M LOC, greenfield Electron app + cloud backend |
| PRs | >1500 |
| Codex generations spanned | Codex Mini → 5.0 → 5.2 → 5.3 → 5.4 |
| End of December 2025 | ~3.5 PRs/engineer/day |
| After Codex 5.2 (Jan 2026) | 5–10 PRs/engineer/day |
| Daily token consumption | *"a billion tokens of intelligence a day"* (Vibhu's framing, confirmed by Lopopolo) |

At market public Codex pricing ≈ $2–3k/day; internal cost is much lower because OpenAI has *"no rate limits internally"* (Lopopolo's words). Treat the dollar conversion as illustrative.

## Harness engineering, not prompt engineering

*"When the agent failed, instead of prompting it better or to 'try harder,' the team would look at 'what capability, context, or structure is missing?'"* The thesis: prompt-tuning is the wrong unit of intervention; build observability + context + structured tooling so the agent can self-correct. swyx calls it *"the defining piece of this emerging discipline."*

The framing aligns with [[effective-harnesses]] and [[agentic-harness-engineering]] (which adds machine-evolution on top). Symphony is the *extreme-scale multi-agent orchestrated* realization.

## The 1-minute build-loop ratchet

When Codex 5.3 added background shells, the agent became *"less patient, less willing to block."* The team re-tooled the build chain (bespoke makefile → Bazel → Turbo → NX) to keep the inner loop **under one minute**. *"Because tokens are so cheap and we're so insanely parallel with the model, we can just constantly be gardening this thing to maintain these invariants."* Lopopolo notes a one-minute ceiling is unrealistic in a codebase *"where people have opinions"* — only viable because no humans had authorship taste at stake.

## Humans as the bottleneck → review collapses to post-merge

*"We've moved beyond even the humans reviewing the code as well. Most of the human review is post merge at this point. But post-post-merge, that's not even reviewed."* Synchronous human attention was the only fundamentally scarce resource; everything else (tokens, GPUs, parallelism) was elastic.

## Harness primitives

- **Six skills total**, named explicitly as small, high-leverage.
- A short top-level `agents.md` with table of contents.
- `core_beliefs.md` (team, product vision, customers).
- `tech_tracker` + `quality_score` markdown tables that hook Codex to review business logic against documented guardrails and propose follow-up work.
- Markdown trackers in lieu of a ticketing system early on.
- A `command`-based class that gives every business-logic chunk free tracing/metrics/observability.
- A single command `dollar_land` skill that drives PR → CI → conflict-resolution → merge-queue → main without human intervention.

## PR-loop autonomy and reviewer tuning

Code review agents post comments on PR sync; the authoring Codex is instructed to acknowledge and respond. **Tuning required**: early reviewer agents *"bullied"* authoring Codex into non-converging revision cycles; fix was to (a) bias reviewers toward merging unless P0/P1, (b) give the author flexibility to defer or push back. *"The reviewer agents were instructed to bias toward merging the thing to not surface anything greater than a P2 in priority."*

## Code for agent legibility, not human readability

Architecture is **"10,000-engineer level"** (500 npm packages) for a 7-person team — because each person operates ~10–50 agent instances. Standardising on a single `command` primitive matters more than how individual business logic looks. *"It's not appropriate for me to be in the weeds on every PR ... I have some representative sample of the code as it is written, and I have to use that to infer what the teams are struggling with."* Group-tech-leading-a-500-person-org analogy.

## Symphony — the orchestrator

**Elixir-based service** (chosen by the model, not by Lopopolo, because Beam's process supervision and gen_servers map naturally onto multi-agent orchestration). Manages multi-Codex spawn / supervise / rework / coordinate over Linear tickets and repos. Slack is the human notification surface.

Notable state: **`rework`**. When a PR is escalated to a human and the human rejects, *"the elixir service will completely trash the entire work tree and PR and start it again from scratch"* — and the team uses that escalation as a signal to fix the root cause in skills/docs before the next attempt.

### "Ghost library" / spec-driven distribution

Symphony itself is *distributed as a spec, not as source code*:

1. Codex reads the proprietary repo, writes a spec.
2. Spawn a fresh tmux + disconnected Codex to implement the spec.
3. Spawn another to compare implementation vs upstream and update the spec to reduce divergence.
4. Loop Ralph-style until high-fidelity reproduction.

Reference Elixir implementation by Alex Kotliarskyi. Lopopolo calls for a future where *"code is increasingly disposable"* and dependencies get inlined (*"end of bullshit plugins"*).

## Skill distillation via session-log harvesting

Codex is pointed at its own session logs to recommend better tool use; the team slurps full-team session logs into blob storage and runs **daily agent loops** over them to extract durable improvements back into the skills/docs. PR comments and failed builds are treated as the same kind of signal: *"the agent was missing context, figure out how to slurp it up and put it back in the repo."*

This is a *production* instance of [[skill-distillation]] in practice.

## Observability stack inverted

Instead of provisioning an environment that hosts the agent, *"we spawn the coding agent — that's the entry point. It's just Codex. And then we give Codex via skills and scripts the ability to boot the stack if it chooses to."* Local Victoria-Metrics stack (mise-managed Go binaries + a sliver of Python glue), set up in *"half an afternoon."*

## MCP scepticism (notable practitioner data point)

*"MCPs I'm pretty bearish on because the harness forcibly injects all those tokens in the context, and I don't really get a say over it. They mess with auto-compaction. The agent can forget how to use the tool."* The team replaced a Playwright MCP with a thin local-daemon CLI shim. **Significant data point against MCP-as-default for agent tool surfaces — explicitly token-economic, not security-economic.** Echoed (with different framing) in Notion's [[notion-token-town#mcp-vs-clis-the-four-axes]].

## CLI-first tool design for agents

GitHub's `gh` is praised as exemplary (token-efficient, agent-legible). The team wraps verbose tools (Prettier, pnpm recursive scripts, build outputs) to suppress success-noise and surface only failure deltas — the pattern the *human* developer-productivity team would historically build for sticky-note error parsing on Jenkins/Buildkite. *"You're going to want to patch dash-silent to prettier because the agent doesn't care that every file was already formatted."*

## What models still can't do (Codex 5.4 era)

- New-product zero-to-one from a mock with no existing screens — Lopopolo finds himself synchronously steering these.
- The "gnarliest refactorings" — tooling for monolith decomposition is where he's currently spending time.

*"Things that are hard and new is still something that the models need humans to drive ... but those other quadrants are largely solved."*

## Team-org changes that fell out

- Daily standups expanded to **45 minutes** because no single human knows the codebase state.
- Operating mode: *"AI-pilled and sprint ahead."*
- Heavy consultation with the Codex product team — many Symphony-internal patterns (skills, the Codex app, file attachments) fed back into shipped Codex products.

## Frontier framing

Frontier is OpenAI's enterprise platform for safely deploying observable, governable agents into businesses; Symphony is a building-block / proof-of-concept feeding that. Buyers are GRC, AI innovation office, security teams, IAM/IT. Internal data agent over the corporate data warehouse uses the same harness pattern.

## Harness vs training tension (Lopopolo's resolution)

The risk of investing in harness is that model improvements will obviate it. Lopopolo's heuristic: build harness components that are **on-policy** with what the model is already producing (tests, docs, CLI scripts) — those compound with model improvements. Bespoke off-policy scaffolds (e.g., *"an entire separate Rust scaffold around Codex to restrict its output"*) are prone to being scrapped. swyx draws the analogy to RL on-policy vs off-policy.

## Caveats Lopopolo raises

- **Greenfield-only scope.** *"Full recognition that all of this activity took in a completely greenfield repository. There should be no expectation that this applies generally."*
- The Electron app does *not* have continuous deploy: there is still a human in the loop for the release branch, with a human-blessed smoke test gate before distribution.
- Multi-human + multi-agent is *"an explosion of stuff"* — the 45-minute standups and the 10,000-engineer-architecture decomposition are the explicit mitigations.

## What generalizes vs what doesn't

**Generalizes**: the harness-engineering mindset, the 1-minute-build discipline, agent-legible CLIs, on-policy guardrails, session-log distillation, post-merge-only review for low-stakes domains.

**Probably doesn't generalize**: zero-human-code on brownfield/legacy code with real authorship taste constraints, autonomous merge in regulated/high-availability domains, the 10,000-engineer-architecture decomposition for a 7-person team (only viable because OpenAI had unmetered model access and a greenfield repo).

## Cross-cutting implications

- **[[conflicts/agents-md-effectiveness]] gains a corroborating data point.** Symphony is a *positive* data point for structured context-and-skills infrastructure at scale — six skills + agents.md TOC + `core_beliefs.md` + `tech_tracker` + `quality_score` work — but only with substantial harness investment, agent-authored maintenance, and on-policy guardrails. Sits between Codified Context (positive) and AGENTS.md eval (negative) by sharpening the *agent-authored / continuously-distilled* axis with a second corroborating source beyond Anthropic's effective-harnesses post.
- **MCP scepticism (vs [[mcp-infrastructure]] / [[mcp-multi-agent-framework]]).** Practitioner data point that at-scale teams may bypass MCP for token-economic reasons. Not a benchmarked refutation; corroborating data point with Notion's MCP-vs-CLIs framing (Notion captured the same week, see [[notion-token-town#mcp-vs-clis-the-four-axes]]).
- **Greenfield-only scope** caveat means [[anthropic-internal-study]]'s smaller-but-real productivity gains on existing systems are the realistic baseline; Symphony is an *upper bound* on autonomous-coding productivity achievable only under specific structural conditions.

## SWE-Cycle context for the zero-human-code regime

Symphony's large-scale zero-human-written-code experiment (>1M LOC, 0% human-authored) operates in precisely the full-lifecycle regime SWE-Cycle (arXiv 2605.13139) benchmarks: environment setup, implementation, and verification without human scaffolding. SWE-Cycle's reported <14% strict FullCycle solve rate on standard benchmark instances contextualizes how hard the Symphony regime actually is — and why the five months of harness investment, the 1-minute build-loop ratchet, and the reviewer-tuning work were necessary rather than incidental.

## Related

- [[effective-harnesses]] — direct architectural sibling; Anthropic's small-scale single-developer harness vs Symphony's multi-agent orchestrated extreme-scale.
- [[agentic-harness-engineering]] — the machine-evolved counterpart; Symphony is the human-team-driven version.
- [[cognition-cloud-agents]], [[shopify-simgym]], [[cognitive-fabric-nodes]], [[microsoft-agent-365]] — peer deployment-tier pages.
- [[anthropic-internal-study]] — engineer-role-shift counterpart; Symphony is the *furthest-along* case in the wiki (group-tech-leading-a-500-person-org framing).
- [[willison-cognitive-cost]] — first-person practitioner counterpart; same cognitive-bandwidth bottleneck at higher scale (45-min standups).
- [[anthropic-claude-code-postmortem]] — fragility counterpoint; reviewer-bullying tuning was discovered the hard way.
- [[notion-token-town]] — peer 2026 practitioner-narrative case study captured the same week; convergent on harness-as-discipline and MCP-skepticism.
- [[conflicts/agents-md-effectiveness]] — extended with Symphony as a corroborating data point.
- [[topology-taxonomy]] — Symphony as multi-Codex orchestration; "code for agent legibility" framing.
- [[skill-distillation]] — Symphony's session-log harvesting + daily team-level loops as production instance.
- [[mcp-infrastructure]] — extended with Lopopolo's MCP-skepticism quote.
- [[langchain-deep-agents]] — peer harness pattern; Symphony is what extreme harness investment looks like beyond the Deep Agents abstraction.
- [[externalization-survey]] — places Symphony under §6 (six harness dimensions) and §8.5 (shared infrastructure → ecosystem-scale).
- [[direct-corpus-interaction]] — academic counterpart to Lopopolo's CLI-first practitioner stance; DCI's `gh` praise + bash-as-search-interface analysis is the formal version of Symphony's MCP-skepticism on token-economic grounds.
- [[alphaevolve-impact]] — peer zero-human-code production agent at radically different scale (DeepMind vendor-deployed in TPU/Spanner/compiler vs Symphony's 7-person greenfield); both are positive data points for high-Metric-Freedom = single-or-orchestrated single-vendor-stack.
- [[evaluation/swe-cycle]] — benchmark for the full-lifecycle coding-agent regime Symphony operates in; reported <14% FullCycle solve rate contextualizes the difficulty of the zero-human-code constraint.
