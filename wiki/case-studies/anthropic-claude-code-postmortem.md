# Anthropic Claude Code Quality Postmortem (April 2026)

Anthropic's April 23 2026 engineering postmortem on user reports of Claude Code degradation between February and April 2026. Three independent bugs in Claude Code, the Claude Agent SDK, and Claude Cowork combined to produce broad inconsistent regression; the API and inference layer were unaffected. All three were resolved by April 20 (v2.1.116) and Anthropic reset usage limits for all subscribers on April 23. The artefact is a primary-source case study in how production agent harnesses fail in ways that *individually* survived Anthropic's internal evals, dogfooding, unit tests, e2e tests, and code review — and a candid account of what was changed in response.

## Source

- `raw/research/weekly-2026-04-27/01-01-anthropic-claude-code-postmortem.md` — captured 2026-04-27 from `https://www.anthropic.com/engineering/april-23-postmortem`.

## The three bugs

### Bug 1 — Reasoning-effort default downgrade (severity: high)

When Opus 4.6 launched in Claude Code (February 2026), default reasoning effort was `high`. Occasional very long tail latencies caused the UI to appear frozen, so Anthropic silently dropped default effort to `medium` and communicated the change only via an in-product dialog. Users reported Claude Code "felt less intelligent." UI mitigations (startup notices, an inline effort selector, re-addition of *ultrathink*) did not recover user behaviour.

- **Reverted:** April 7.
- **Current defaults:** `xhigh` for Opus 4.7, `high` for all other models.
- **Discovery channel:** user feedback and public reports. Not caught by internal evals or dogfooding before rollout.

### Bug 2 — Thinking-block caching bug (severity: high)

Shipped March 26 as an efficiency improvement: on cache-miss resume after >1 hour idle, clear old thinking sections via the `clear_thinking_20251015` header with `keep:1`. The implementation flag persisted for every subsequent turn in the session instead of firing once. After the idle threshold crossed once, each turn discarded all but the most recent reasoning block; mid-tool-use follow-ups dropped even the current turn's reasoning.

Symptoms: forgetfulness, repetition, odd tool choices, faster-than-expected usage-limit drain (continuous cache misses each turn).

The bug evaded detection because two unrelated concurrent experiments masked it across testing pipelines: an internal message-queuing experiment, and a display change that suppressed thinking output in the CLI. It only reproduced in stale (>1 hour idle) sessions — a corner case absent from automated tests.

Discovery took over a week of investigation. Anthropic back-tested the offending PRs through their Code Review tool with two backends: **Opus 4.7 (with full repository context) found the bug; Opus 4.6 did not.** Fixed April 10 (v2.1.101). Mitigation going forward: expanding the customer-facing Code Review tool to include additional repository context.

### Bug 3 — System-prompt verbosity constraint (severity: medium)

Added in preparation for the Opus 4.7 launch (April 16) to curb its known verbosity:

> "Length limits: keep text between tool calls to ≤25 words. Keep final responses to ≤100 words unless the task requires more detail."

Passed multiple weeks of internal testing with no regressions in the eval set run at the time. Post-incident ablation with a broader eval suite revealed a **3% intelligence drop for both Opus 4.6 and Opus 4.7.** Reverted April 20 (v2.1.116).

Mitigation going forward: broader per-model evals for every system-prompt change; ablation of every line; new prompt-audit tooling; model-specific changes gated to the target model in `CLAUDE.md`; soak periods and gradual rollouts for any change that could affect intelligence.

## Why the combined signal was hard to read

Each bug affected a different traffic slice on a different schedule, so the aggregate degradation looked diffuse and inconsistent rather than attributable to a single root cause. Internal dogfooding diverged from the public build (feature-branch differences), so internal staff did not consistently see the same surfaces customers saw.

## Process changes Anthropic announced

- Larger share of internal staff using the exact public build going forward.
- Customer-facing Code Review tool gets additional repository context (the same lever that let Opus 4.7 find Bug 2).
- Tighter system-prompt change controls: per-model evals, line-by-line ablation, gated rollouts.
- Public visibility via @ClaudeDevs on X and GitHub threads.

## Implications for the wiki

- **Bug 2 is a concrete failed implementation of selective context pruning.** It corrupts exactly the layer that [[claude-code-session-memory]] describes (background extraction, cross-session reasoning history). It pairs against [[context-folding]]'s claim that proactive variable-granularity folding is safe at scale — selective pruning at the API primitive level is not.
- **The `clear_thinking_20251015` + `keep:1` primitive** is part of the same memory-tool API surface documented in [[anthropic-memory-tool]]. The postmortem is a real-world failure-mode addendum to that contract.
- **Bug 3's 3% intelligence drop from a single brevity instruction** is a hard data point on prompt-layer fragility. It does not flatly contradict [[codified-context]] (which scales a 660-line constitution positively), but it raises a credibility caveat: even a well-intentioned, locally-tested addition to the system prompt can introduce measurable regression. See [[conflicts/agents-md-effectiveness]] for where this lands in the open conflict.
- **The internal-dogfooding gap** parallels themes in [[anthropic-internal-study]]'s "engineer as orchestrator" findings — internal tooling diverged from the public build, and customer-side reports surfaced what internal evals missed. The cognitive-load pattern in [[willison-cognitive-cost]] (4 parallel agents, "wiped out by 11am") is a practitioner-side consequence of the same Bug-2 usage-limit drain.

## Related

- [[anthropic-internal-study]] — same Anthropic-internal production context; 132-engineer study on Claude adoption and the engineer-as-orchestrator role shift.
- [[willison-cognitive-cost]] — practitioner-facing account of the same period; usage-drain experience aligns with Bug 2's continuous cache-miss pattern.
- [[anthropic-memory-tool]] — the API primitive (`clear_thinking_20251015`) that Bug 2 misused.
- [[claude-code-session-memory]] — the layer Bug 2 corrupted.
- [[context-folding]] — peer mitigation approach for cross-window degradation; Bug 2 is a counterexample of naive selective pruning.
- [[codified-context]] — production constitution case; Bug 3 is a counterweight on prompt-layer fragility.
- [[conflicts/agents-md-effectiveness]] — open conflict; this case adds a prompt-fragility data point.
- [[mcp-infrastructure]] — Code Review's expanded repository context lands in the same governance/observability theme as the MCP 2026 roadmap.
