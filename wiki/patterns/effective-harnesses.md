# Effective Harnesses for Long-Running Agents (Anthropic)

Anthropic's engineering blog account of how to make a frontier coding agent (Opus 4.5 on the Claude Agent SDK) make consistent incremental progress across many context windows, including for high-level prompts like "build a clone of claude.ai." Names two failure modes — *try-too-much (one-shotting)* and *declare-done-prematurely* — and describes a two-fold initializer-agent + coding-agent harness that corrects both. The headline claim is that **compaction is not sufficient**: even with a frontier model in a loop on a powerful SDK, agents need explicit handoff artefacts to bridge sessions. This page is the primary-source harness pattern long flagged in `master_notes.md` as the missing canonical reference.

## Source

- `raw/research/weekly-2026-04-27/03-03-anthropic-effective-harnesses.md` — captured 2026-04-27 from `https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents`.
- Companion code: `https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding`.

## The core failure modes

The post reports running Opus 4.5 in a loop on the Claude Agent SDK on the prompt "build a clone of claude.ai." Two failure modes appear:

1. **Try-too-much (one-shotting).** The agent attempts to implement too much at once, runs out of context mid-implementation, leaves work "half-implemented and undocumented." The next session has to "guess at what had happened" and burns substantial time recovering the basic working app.
2. **Declare-done-prematurely.** A later session "look[s] around, see[s] that progress had been made, and declare[s] the job done" — false-completion failure even though substantial features remain unbuilt.
3. **(Third failure mode introduced later in the post.) Mark-feature-complete without end-to-end testing.** Unit tests and `curl` pass but the actual user flow fails; mitigated by adding browser-automation tooling (Puppeteer MCP).

> "Compaction isn't sufficient … even a frontier coding model like Opus 4.5 running on the Claude Agent SDK in a loop across multiple context windows will fall short of building a production-quality web app if it's only given a high-level prompt."

## The two-fold harness

The two "agents" share the same system prompt and tools — only the initial user prompt differs.

### Initializer agent (one-shot, first run)

Writes:

- **`feature_list.json`** — 200+ entries for the claude.ai clone, all initially `"passes": false`. Schema: `{"description", "steps": [...], "passes": false}`. JSON is preferred over Markdown because "the model is less likely to inappropriately change or overwrite JSON files compared to Markdown files."
- **`init.sh`** — shell script that boots the development server.
- **Initial git commit** of the scaffold.
- **`claude-progress.txt`** — plain-text progress log appended every session.

### Coding agent (every subsequent session)

Standard open sequence (quoted from the post):

1. `pwd`
2. Read `claude-progress.txt`.
3. Read `feature_list.json`.
4. `git log`.
5. Run `init.sh`.
6. Basic end-to-end smoke test.
7. Review `tests.json`.
8. Pick **exactly one feature** to work on, marking incremental progress.

End-of-session: descriptive `git commit`, append a progress summary to `claude-progress.txt`, exit.

### Git as recovery substrate

Coding agents are prompted to commit incremental progress with descriptive messages and to use git itself to "revert bad code changes and recover working states of the codebase." This makes the version-control system part of the agent's memory and rollback layer, not just the human's.

### Discipline enforced by strong-worded prompting

> "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality."

The post is candid that the harness leans on prompt firmness, not architectural enforcement, to keep the coding agent honest about scope and tests.

## How this fits the existing wiki

- **Sibling to [[anthropic-memory-tool]].** That docs page references this engineering post explicitly as "a detailed case study of this pattern in practice, including the initializer script, progress file structure, and git-based recovery." `claude-progress.txt` is a concrete instantiation of the memory-tool file pattern; the Initializer / Subsequent / End-of-session lifecycle in the docs maps one-to-one to the harness here.
- **Structural parallel to [[codified-context]].** Both use a warm-up / cold-start scaffold — Codified Context's 660-line constitution + 19-agent specialist pool + 34-doc cold KB versus this harness's progress file + feature list + scripted boot. Different artefacts, same architectural class: *materialise state in topology so the agent does not have to reconstruct it from raw history*.
- **Peer mitigation to [[context-folding]].** AgentFold proactively compresses the context window itself; this harness instead writes explicit handoff artefacts to the filesystem and lets each session start fresh. They are two different answers to the same long-horizon question; both belong on the long-horizon-context-loss mitigation taxonomy in [[topology-taxonomy]].
- **Within the [[memory-architectures]] survey**, this is a concrete instance of the *episodic log + structured working memory* family. The progress file is the episodic log; the feature list is the structured working memory.
- **Companion to [[claude-code-session-memory]]** — that page describes Anthropic's automatic background memory layer; this page describes Anthropic's *explicit* harness-level handoff. They are complementary: the automatic layer covers within-Claude-Code experience; the harness covers SDK-level long-running deployments.
- **Lightweight practitioner cousin — the markdown memory bank** — the convention catalogued at [[claude-code-memory-ecosystem]] (a `.claude/memory/` directory with `decisions.md` / `patterns.md` / `sprint.md`, loaded via a `CLAUDE.md` read-instruction and refreshed by an end-of-session write-back) is the same architectural move at Claude Code's native scale: explicit artefacts that bridge sessions, read fresh at the start of each context window. The memory-bank convention uses human-readable markdown rather than JSON, scopes to a single Claude Code project rather than a multi-session SDK loop, and relies on the practitioner (or the agent under instruction) for write-back discipline rather than a harness wrapper. Same pattern, different deployment tier.

## Open question raised by the post

The conclusion explicitly asks whether a single general-purpose coding agent or a multi-agent architecture (testing agent, QA agent, cleanup agent) yields better SDLC results. This question is directly addressed by [[skill-distillation]]'s F-predictor: when skill overlap is high, collapse to a single agent; when low, specialise. The post does not engage that framework but the question is the right one.

## Machine-evolved counterpart and multi-rebuild data points (2026-05-04 sweep)

Three new sources surfaced in the week of 2026-05-04 sit alongside this post in the same architectural class:

- **[[agentic-harness-engineering]] (arXiv 2604.25850)** is the *machine-evolved counterpart*: where Anthropic's harness is hand-designed, AHE evolves the same kind of artefacts (tools, middleware, memory, system prompt) automatically via an observability-driven loop. The AHE paper explicitly cites this post (ref [29]) as one of three primary harness-engineering sources it compares against. AHE's component-ablation finding sharpens the pattern's load-bearing claim: structural components (memory +5.6 pp, tools +3.3, middleware +2.2) carry the lift; the prose-level system prompt alone *regresses* by 2.3 pp. Read alongside this post: the `feature_list.json`/`init.sh`/`claude-progress.txt` artefacts are exactly the kind of *structural* component AHE confirms is load-bearing — and the system prompt warnings the post emphasises are exactly the layer AHE found to be most fragile.

- **[[openai-symphony]]** is the *extreme-scale multi-agent* realization. OpenAI's Frontier team operates the same architectural pattern with: six skills, an `agents.md` table-of-contents, `core_beliefs.md`, `tech_tracker` and `quality_score` markdown tables, and a single command `dollar_land` skill that drives PR → CI → conflict-resolution → merge-queue → main. Adds to this post's vocabulary: a **`rework` state** in the orchestrator (escalation → human reject → wipe work tree, restart, fix root cause in skills); **session-log harvesting** (daily agent loops over team-wide session logs that re-extract durable improvements back into skills/docs); the **1-minute build-loop discipline** as a generalizable harness primitive; the **on-policy harness vs off-policy scaffold** heuristic for which harness investments compound with model improvements vs which are prone to scrapping.

- **[[notion-token-town]]** is the *multi-rebuild counterpart*. Anthropic's harness is a single-shot design from a vendor; Notion's 4–5 rebuilds (2022–2026) show the same architectural class arrived at through iteration in production. Specifically: the *"give the model what it wants"* doctrine (XML→Markdown, Notion-JSON→SQL-lite for the agent surface), tool-distribution-via-progressive-disclosure when tool count crossed ~100, and the cautionary one-Anthropic-rep-asked-"is-Simon-trying-to-prove-string-theory" anecdote about a 17-day continuous coding-agent thread compacted *"like a hundred times"* before they realised it was a harness bug.

The [[externalization-survey]] (arXiv 2604.08224) provides the unifying vocabulary: this harness is one concrete instance of the survey's six harness dimensions (agent loop, sandboxing, oversight, observability, configuration, context budget) and explicitly an instance of the §8.3 "self-evolving harnesses" emerging direction once AHE-style evolution is layered on.

## Architectural principle vs operational lesson: compaction and structured state

[[patterns/anthropic-context-engineering]] describes compaction as "typically the first lever in context engineering to drive better long-term coherence" — an architectural-principle framing about where to start. This page's headline claim — "compaction isn't sufficient" — is the operationally-learned refinement: starting with compaction is right, but it does not complete the picture for multi-session SDK-level agents. This is not a contradiction. The Anthropic post itself introduces structured note-taking as compaction's necessary complement in the same document; `feature_list.json` and `claude-progress.txt` are one concrete instantiation of that companion technique, evolved from production failure.

## Conflict with [[agents-md-eval]]

This source recommends structured context files (`feature_list.json`, `claude-progress.txt`) as essential scaffolding for long-running agents. [[agents-md-eval]] finds LLM-generated context files reduce success ~3% and inflate cost >20% in well-documented repos. Possible reconciling axes — task type (long-running multi-session vs single-session well-documented), authorship (here the *agent* writes the artefacts during work, in agents-md-eval the artefacts are pre-generated), and file format (JSON vs Markdown AGENTS.md) — but no empirical bridge yet. Tracked in [[conflicts/agents-md-effectiveness]].

## Related

- [[anthropic-memory-tool]] — sibling Anthropic primitive; this post is the canonical case-study referenced from those docs.
- [[codified-context]] — structural parallel in cold-start / warm-up scaffolding; different mitigation class within the same family.
- [[context-folding]] — peer mitigation for long-horizon context loss via in-context compression instead of explicit handoff.
- [[claude-code-session-memory]] — complementary background-memory layer.
- [[memory-architectures]] — survey peer; this is a concrete *episodic log + structured working memory* instance.
- [[topology-taxonomy]] — long-horizon-context-loss mitigation table; the two failure modes (try-too-much, declare-done-prematurely) and the init/coding split are entries.
- [[skill-distillation]] — directly addresses the post's open single-vs-multi-agent question via Metric Freedom.
- [[mcp-multi-agent-framework]] — overlapping context-retention failure typology; both use MCP tooling (Puppeteer MCP).
- [[langchain-deep-agents]] — peer harness pattern; LangChain's Deep Agents library generalises Claude Code's harness into four reusable components.
- [[conflicts/agents-md-effectiveness]] — open conflict; this source is a new data point on the structured-context-file question.
- [[agentic-harness-engineering]] — machine-evolved counterpart; explicitly cites this post.
- [[openai-symphony]] — extreme-scale multi-agent realization with session-log distillation and rework-state.
- [[notion-token-town]] — multi-rebuild practitioner counterpart from a non-Anthropic vendor.
- [[externalization-survey]] — unifying vocabulary for harness as cognitive environment.
- [[agent-development-lifecycle]] — vendor-side LangChain framing of Build → Test → Deploy → Monitor; the Anthropic harness here is one concrete instance of the Lifecycle's "agent harness" build-tooling layer.
- [[sierra-monitor-eval-of-evals]] — Sierra's flywheel (build → observe → understand → improve) is the operational counterpart to the single-shot harness design here; sustains a deployed agent over time.
- [[skillos]] — learned-curation counterpart: the `feature_list.json` / `claude-progress.txt` artefacts here are hand-prompted; SkillOS demonstrates the curation policy can be RL-trained against downstream success.
- [[direct-corpus-interaction]] — both reject the abstracted-API-mediates-everything posture; Anthropic's harness ships explicit progress files, DCI ships explicit corpus traversal — distinct flavours of the same anti-mediation move.
- [[patterns/anthropic-context-engineering]] — conceptual parent; this harness is a concrete production instantiation of the JIT/compaction/note-taking triad; the "compaction isn't sufficient" lesson is the operational refinement of the post's architectural-principle ordering.
- [[claude-code-memory-ecosystem]] — practitioner landscape of Claude Code memory conventions; the markdown memory-bank pattern (`.claude/memory/` + `CLAUDE.md` read-instruction + session write-back) is the lightweight cousin of this page's `feature_list.json` / `claude-progress.txt` substrate.
