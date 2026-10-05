# Cursor (Anysphere)

Coding-agent IDE; **Anysphere** is the parent company. Profiled here from **Cursor 3.2 (2026-04-24)** onwards, when the product reframed itself as an **"agent execution runtime"** rather than an editor with AI features. **SpaceX completed its $60B all-stock acquisition of Cursor on 2026-08-14** (confirmed by multiple independent outlets — Bloomberg, Seeking Alpha, Yahoo Finance — superseding the earlier "option" framing; see [[../landscape/spacex-cursor-60b-option-2026-04|spacex-cursor-60b-option-2026-04]]); Cursor now operates as a wholly-owned subsidiary inside a division called **SpaceXAI**.

## Origin: code-hosting platform launch (2026-08-17)

Cursor began rolling out **Origin**, an agent-native code-hosting platform (repos, PRs, CI/deploy integrations), inside a new "Codebase tab" in the editor — timed three days after the SpaceX deal closed and coinciding with a 6h42m GitHub outage (~20% error rates on PRs/issues/API; the 7th GitHub status-page incident in 15 days). Per VentureBeat (2026-08-17):

- **What it does.** Teams name a codebase (becomes part of its URL) and push over the CLI; Origin wraps Git with storage, permissions, checks, and full PR machinery (timelines, commits, checks, files changed, review/comment/merge) — inside the editor. Agents "operate in the same surface as the code and the pull requests they are modifying" (Cursor changelog), so a developer can hand an agent a review comment and have it revise the PR in place.
- **Not a GitHub replacement (yet) — a mirror wedge.** Origin runs in "sync mode": connect a GitHub org, and repos appear alongside Origin-native ones; GitHub stays the system of record, pushes still go there, PR comments sync bidirectionally within seconds, and access permissions mirror GitHub's existing settings. This is a **near-zero-risk adoption wedge** — it mirrors an existing system and breaks nothing on abandonment, while giving Cursor first-mover claim on developer attention before asking for system-of-record status.
- **Day-one CI/deploy partners:** Vercel (auto preview deploy per PR; Pro/Enterprise), Depot and Buildkite (run existing GitHub Actions workflows *unchanged* — lowering switching cost to near-zero).
- **Governance flag:** default is **opt-out, not opt-in** for paid users — orgs that made no affirmative decision may have proprietary code mirrored to a new host by default. Pricing, security architecture, data-handling terms, and migration tooling are unpublished as of this capture. Source explicitly frames Origin as "a beta, not a migration."
- **Motivating internal metric:** per RuntimeWire, 35% of PRs merged inside Cursor are opened by agents running autonomously in cloud VMs — a forge built for human-authored PRs breaks down once a third of merges are machine-opened.
- **Context:** GitHub reliability has been under sustained strain (257 incidents May 2025–Apr 2026 per LeadDev, CEO resigned Aug 2025 and not replaced, GitHub's CoreAI-org EVP reportedly warned that Claude Code/Cursor "could eventually make GitHub obsolete"). Prior defections: Zig → Codeberg, Ghostty (52K+ stars) announced leaving GitHub. GitHub's countermove, Agent HQ, orchestrates third-party agents (Anthropic, OpenAI, Google, Cognition, xAI) inside GitHub — described by the source as "conceding the agent layer while keeping the substrate."
- **Unpatched parallel vulnerability:** Mindgard disclosed (July 2026) that Cursor executes a malicious `git.exe` planted in a Windows project root on open, no prompt required — a repo-poisoning flaw first reported December 2025. Cursor declined to patch, citing a "shared-responsibility model"; no CVE issued. The same flaw class is unpatched in GitHub Copilot CLI, Gemini CLI, and OpenAI Codex — parallel to the harness-trust-boundary pattern in [[../landscape/blackhat-ai-coding-agent-cves-2026-08|blackhat-ai-coding-agent-cves-2026-08]].
- **Lineage:** Cursor acquired Graphite (stacked-PR code review) in December 2025 for a price "well above" its $290M Series B valuation; Graphite co-founder Tomas Reimers leads Origin's development.

### SpaceXAI ownership — model-routing/guardrails risk flagged

Analyst Jason Andersen (Moor Insights & Strategy, pre-deal-close): "xAI's models and treatment of guardrails are very different than what Cursor has stood for" — a direct concern about Cursor's code/data now sitting under the same corporate umbrella as xAI's models. See [[../llms/xai-grok-family|xai-grok-family]] for SpaceXAI organizational context.

**Update 2026-09-02 — OpenAI terminates model access.** OpenAI is cutting off Cursor's contractual access to OpenAI models effective 2026-11-12, citing an inability to trust SpaceX/Musk-affiliated entities' ToS compliance. Cursor retains Claude access. Full detail and why it matters for the harness-vs-model thesis: [[../landscape/spacex-cursor-60b-option-2026-04|spacex-cursor-60b-option-2026-04]].

## Cursor 3.2 (2026-04-24) — the IDE-as-runtime reframe

### What shipped

Per Anysphere's changelog and Futurum Research's analyst review (Mitch Ashley, 2026-04-29):

- **`/multitask`** — async subagents in parallel. Cursor breaks larger tasks into smaller chunks and assigns them to **multiple subagents executing simultaneously**, rather than serializing them in a queue. Users can redirect already-queued messages into multitask execution mid-run.
- **Worktrees, expanded.** Agents Window now isolates background tasks across different branches. Users can promote any branch into the local foreground with one click — a single-click branch swap from agentic background work to foreground manual review.
- **Multi-root workspaces.** A single agent session can target a reusable workspace composed of multiple folders / repositories. Cross-repo refactors that previously required manual repo-by-repo orchestration are now in-scope for one agent invocation.
- **Browser tool (full rollout).** Native browser navigation with screenshot + DOM access; rolls out to all paid plans (was experimental).
- **Plan mode.** New explicit planning step; auto-accepts edits during Plan generation but pauses on the next ambiguity.

### Strategic re-framing (Futurum analyst take)

> "Cursor is an agent execution runtime with a built-in code surface, and vendors competing on IDE capability alone are mispositioned against it. The IDE category no longer captures what the product does or where its strategic gravity sits."

The product center has shifted from the **editor** to the **Agents Window**. The editor is now a single view inside a broader agent-execution system. This compounds Cursor 2.5's introduction of subagents-spawning-child-subagents and Cursor 3.0's Agents Window architecture.

### Cited benchmark lift

Cursor 3.2 is reported to deliver **~37% improvement on SWE-bench Multilingual** versus Composer 1.5 (per Futurum citing Cursor's release materials). Vendor / vendor-adjacent claim — not independent verification — but consistent with the multi-agent-orchestration class of techniques the release implements.

## Why this matters strategically

### The harness-vs-model thesis (C8) keeps compounding

Per [[../conflicts/open-questions-2026-04|C8]] and the 2026-04-23 brief, Cursor is the canonical harness-class evidence point: a coding-IDE company validated at $60B (SpaceX option, see [[../landscape/spacex-cursor-60b-option-2026-04|spacex-cursor-60b-option-2026-04]]) without owning a frontier model. Cursor 3.2 doesn't change that thesis — it **deepens it**:

- The IDE is no longer "the surface a developer types into"; it's "the runtime where agentic work executes, gets isolated, and reconciles."
- The reframe pulls the strategic gravity *toward* the harness layer and *away from* the model. The model becomes one tool the runtime uses.
- This is the precise mechanism C8's "harness > model" wing predicts: the value capture migrates to the orchestrator.

### Direct competitive pressure on adjacent categories

Per Futurum, Cursor's 3.2 architecture creates pressure on:

- **CI/CD vendors** — async subagents move "large refactors, multi-file features, and complex bug reproductions" *into the dev runtime, before any pipeline trigger fires*. The pipeline still runs build/test, but the cognitive heavy lift moves left.
- **Cloud developer environments** (Coder, Gitpod, GitHub Codespaces) — multi-root workspaces + worktrees encroach on the workspace-isolation primitive these products sell.
- **Coding-assistant peers** (GitHub Copilot, Anthropic Claude Code, Codeium) — the "IDE with AI features" framing is now a strictly weaker position; they need to either follow into runtime territory or accept a positioning downgrade.

### Governance and observability gap (Futurum-flagged risk)

Parallel subagents fanning out across branches and repositories with a **limited enterprise control surface** is the analyst-flagged risk. Specifically:

- No native enterprise admin view of "all parallel subagent sessions running across this org right now."
- No first-class audit log of multi-agent intermediate artefacts (subagent thinking, tool calls, partial commits).
- Worktree isolation is per-developer-machine, not per-org-policy; cross-developer governance is by-IDE-config, not centrally controlled.

This is the wedge for [[../landscape/ai-infrastructure-frontiers-2026|ai-infrastructure-frontiers-2026]] harness-tier startups (Bigspin, Braintrust, Judgment Labs) to attach as **agentic IDE governance** — the enterprise-tier value Cursor itself is not (yet) capturing.

## Build-vs-buy implications

- **Coding-agent decision criterion shift.** "Does it have an editor?" is no longer the right question. Better: "Does it run subagents in parallel? Does it isolate them? Does it reconcile multi-repo changes? Does it expose a governance surface for enterprise?"
- **Pricing tier signal.** `/multitask` parallelism implies **multiplied compute consumption** per developer-hour vs serialized subagents. Combined with the broader compute-pricing pressure (see [[../landscape/agentic-compute-pricing-2026-04|agentic-compute-pricing-2026-04]]), Cursor's pricing should keep tiering up at the high end. Expect Pro+ / Enterprise per-seat costs to rise as multi-task-default workflows propagate.
- **For enterprise rollout:** governance gap is real. Pair Cursor enterprise plans with a harness-tier observability vendor unless / until Cursor ships its own admin surface.

## Hype-vs-reality delta

- The "agent execution runtime" framing comes from Anysphere's marketing language; Futurum endorses it. Independent practitioner confirmation will surface in HN / Reddit threads over 4–6 weeks. Watch [[../watchlist|watchlist]] for follow-up signal.
- The 37% SWE-bench-Multilingual lift is **vendor-curated**; pair with leaderboard runs before quoting in client material.
- The "competitor pressure on CI/CD" claim is analyst inference, not market data — directionally plausible but not yet validated by CI/CD-vendor revenue impacts.

## Conflict-flag cross-refs

- **C8 (coding agents = AGI for near-term enterprise tasks)** — supports Position A specifically at the **harness-as-runtime** layer. The capability is real and compounding; the unanswered C8 question (does it generalize beyond coding?) is unchanged. Origin (2026-08-17) deepens this: Cursor moving beyond the IDE into owning the whole dev-platform stack (hosting + PRs + CI/CD + agents-in-the-loop) is a stronger harness-as-runtime data point than the 2026-04 evidence, plus a concrete build-vs-buy wedge argument (GitHub/Copilot lock-in vs. a zero-risk mirror-adoption path).

## Source

- `raw/research/weekly-2026-05-03/04-cursor-3-2-multitask.md` (Futurum Research, 2026-04-29)
- VentureBeat, 2026-08-17: `raw/research/weekly-2026-08-19/05-cursor-origin-launch-2026-08.md` (Origin launch, SpaceX deal completion, git.exe vulnerability)
- WebSearch verification, 2026-08-19: SpaceX/Cursor deal completion cross-confirmed via Seeking Alpha, Yahoo Finance, SatNews (merger effective 2026-08-14; Cursor's shares converted to 389,289,254 SpaceX Class A shares)

Adjacent (not captured in this batch):
- Cursor changelog — https://cursor.com/changelog/04-24-26
- Prior Cursor 3.0 / Composer 1.5 release notes (cited inline)

## Related

- [[../landscape/spacex-cursor-60b-option-2026-04|spacex-cursor-60b-option-2026-04]]
- [[../landscape/agentic-compute-pricing-2026-04|agentic-compute-pricing-2026-04]]
- [[../landscape/ai-infrastructure-frontiers-2026|ai-infrastructure-frontiers-2026]]
- [[../thesis/ai-apps-layer-2026|ai-apps-layer-2026]]
- [[../thesis/agents-eating-saas|agents-eating-saas]]
- [[../conflicts/open-questions-2026-04|open-questions-2026-04]] (C8)
- [[../landscape/blackhat-ai-coding-agent-cves-2026-08|blackhat-ai-coding-agent-cves-2026-08]] — parallel git.exe repo-poisoning flaw
- [[../llms/xai-grok-family|xai-grok-family]] — SpaceXAI ownership context
