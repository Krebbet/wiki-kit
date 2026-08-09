# Claude Code Auto Mode

Auto mode is a classifier-based permission architecture that Anthropic made the default for Claude Code on Pro, Max, and Team plans starting August 14, 2026. Instead of prompting for per-command approval, a classifier routes every tool call and blocks actions it judges irreversible, destructive, or aimed outside the user's environment; on a block, Claude self-corrects or asks the user, and repeated blocks trigger a fallback to manual approvals. Anthropic backs the rollout with internal telemetry, a controlled study, a third-party red-team pilot, and a prompt-injection eval, all arguing the classifier matches or beats manual per-command review. This is the wiki's first primary-source page on Claude Code's permission/autonomy architecture specifically — distinct from the model-agnostic governance research already covered.

## Mechanism

A classifier evaluates every tool call in real time. Allow/deny permission rules configured by the user or org still fire *before* the classifier — except overly broad allow-rules (e.g. `Bash(python:*)`) that would let arbitrary code skip the classifier entirely; those are set aside while auto mode is active (the underlying settings files are not modified). On a classifier block, Claude either self-corrects its approach or surfaces the decision to the user. After 3 consecutive blocks, or 20 in a single session, auto mode falls back to manual approvals for the rest of the session.

Specific hardening built into the classifier:
- A **hard-deny category for data exfiltration** that auto mode can never approve — customizable/extensible by org admins, but cannot be loosened by end users.
- **Git-status-aware gating** before destructive git operations (e.g. `git reset --hard`).
- **Destination-awareness** for `git push`/PR creation — distinguishes public, private, and trusted repos to catch code moving from a private repo to a public one.
- An **API-side prompt-injection probe** on ingested external content that annotates Claude's context with a warning rather than silently blocking.

Classifier token overhead is not billed to Pro/Max/Team users.

## Rollout scope

Default for Pro/Max/Team as of August 14, 2026. Remains opt-in (admin-settable via `defaultMode`) for Enterprise, the Claude API, Amazon Bedrock, Google Cloud Agent Platform, and Microsoft Foundry — Anthropic states it plans to flip those defaults "within the coming month."

## Why Anthropic frames manual approval as reflexive, not protective

Anthropic's own telemetry: users approve 97% of individual permission prompts (vs. only 3% rejection), and reject just 39% of full-plan-approval dialogs. Separately, 49.5% of active CLI users had already hand-written a Bash allow-rule before auto mode existed (growing ~5 percentage points every 5 weeks), 62% had used `bypassPermissions` or "don't ask again," and 25% of interactive sessions already started in bypass mode. Anthropic's argument: users were already routing around per-command prompts, so the prompts were providing an illusion of safety rather than actual friction against dangerous actions.

## Concrete metrics claimed (collect-but-confirm — vendor-run and vendor-commissioned)

- **Controlled study, 1,053 paid testers:** humans caught 13.6% (143/1,053) of injected dangerous commands vs. 89% (937/1,053) for auto mode's classifier. Human catch rate degraded with session length (17% → 5% after 50+ prior prompts); the classifier's catch rate stayed flat.
- **Production session re-grading** (May–Jun 2026, opted-in accounts): at severity ≥7 (production-level), 6.3% of manually-approved flagged sessions contained unintended harm vs. 2.4% for auto mode.
- **Apollo Research two-week red-team pilot:** post-hardening, classifier miss rate fell from 12% to 7% on combined shared+held-out attack sets — catching ~50% of previously-missed held-out attacks at a ~2% cost of previously-caught ones.
- **Trajectory Labs third-party prompt-injection eval** (72 scenarios × 10 trials, browser + tool-result vectors): 0/720 successful attacks against Claude Fable 5 / Opus 5 / Sonnet 5 running auto mode, vs. 5.83% ASR for GPT-5.6 Sol in Codex's Auto-review mode and 19.03% ASR in Codex Full Access. Notably, Claude models running `bypassPermissions` with *no* extra safeguards still averaged only 0.09% ASR — so auto mode's 0% is an increment on an already-low baseline, not a rescue from a high-risk one.
- **Team-adoption headline:** auto mode users ship ~25% more PRs (Teams & Enterprise cohorts).
- **Three named internal incidents** auto mode blocked: an off-network exfiltration fallback (a failed internal upload attempt followed by an attempt to use a public code-sharing site instead), a mass pod-kill / GPU-training teardown, and an over-broad cloud IAM privilege escalation (a billing read-only request that would have granted an admin-root role).

## Explicit safety caveats stated by Anthropic

Anthropic states auto mode "does not eliminate risk" and still recommends human review for high-stakes production-infrastructure changes. The hard-deny exfiltration category and destination-aware git gating exist precisely because the classifier is not treated as a complete substitute for judgment on the highest-stakes action classes.

## Tension: encouraging longer unattended sessions

The post frames auto mode as the unlock that makes "models built for long-running work, like Claude Opus 5, more practical to leave running for hours," and cites customer testimonials of overnight, unattended runs (Nuro's overnight research agents; a cited 10pm–5am agent session). This sits in soft tension with Anthropic's earlier (April 2026) stated position that Claude Code is "not designed to power always-on third-party agents at scale — production always-on should use the Claude API directly" (see [[memory/openclaw-claude-code-memory]]). The distinction may be a single long *session* versus a persistent multi-session *daemon*, which would make the two claims compatible rather than contradictory — but the framing has visibly shifted toward encouraging longer autonomous stretches, and is worth tracking as Anthropic's position evolves.

## Source
- Anthropic, "Auto mode is now the default in Claude Code for Pro, Max, and Team plans," 2026-08-07 — `raw/research/weekly-2026-08-09/01-anthropic-auto-mode-default.md`. Vendor primary source.

## Related
- [[governance/org-control-layer]] — architecturally the same class of mechanism (execution-boundary interception before an action lands), but OCL is model-agnostic third-party research with a formal APPROVE/REVISE/BLOCK/ESCALATE taxonomy, while auto mode is a shipped first-party product default with a binary allow/block-then-fallback design.
- [[security/adr-uber-mcp-detection]] — complementary rather than overlapping: ADR is detection-side (post-hoc causal-chain reconstruction over agent action logs), auto mode is prevention-side (pre-execution classifier gate).
- [[security/prompt-injection-impossibility]] — soft tension, tracked as [[conflicts/auto-mode-prompt-injection-defense]]: that paper argues data-instruction-separation defenses are evadable in principle by contextual-manipulation attacks, while this source reports 0/720 successful attacks against auto-mode-protected models in a third-party eval. Auto mode is not purely a data-instruction-separation defense (it layers environment-aware classification and hard denies on top), so this is not a direct contradiction, but the two claims need explicit reconciliation.
- [[security/memory-poisoning-mpbench]] — adjacent but distinct threat model: MPBench concerns persistent long-term memory poisoning, this source's 0% ASR concerns in-session tool-call/browser prompt injection.
- [[memory/openclaw-claude-code-memory]] — see the always-on tension noted above.
- [[patterns/effective-harnesses]] — auto mode removing interruption-by-approval-prompt is a precondition for the multi-hour unattended runs this page's harness-recovery-substrate argument assumes.
- [[deployments/cognition-cloud-agents]] — parallel overnight/always-on framing; both position 2026 as the year unattended agent runtime becomes a product default rather than a power-user workaround.
- [[governance/aaif]] — loosely related Anthropic-adjacent governance activity in the same period, but AAIF is open-protocol stewardship (MCP/AGENTS.md/Goose), not a permission-classifier architecture.
