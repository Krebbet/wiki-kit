# Code Review at Anthropic (Claude Code Team)

An Anthropic vendor-primary post (claude.dev blog, 2026-10) describes how the Claude Code team reviews code when Claude writes ~90% of it and Anthropic's monorepo goes from ~2,500 changes/day (May) to 30,000+ (Sept). The goal is reframed as minimum human review time with no increase in reverts or incidents: review runs continuously rather than as an end-of-road gate, most PRs merge with at most one human (who can be the author), and risk tiers decide where people are still required. The post reports merged PRs more than doubled June to September while reverts fell by more than 40% (self-reported, no baseline; collect-but-confirm).

## Layered flow

1. **Pre-PR verification** — give Claude something runnable, review in a fresh-context subagent, internal bug-hunt/simplify/e2e skills. Boris Cherny's claim is that verification makes results 2-3x better (practitioner claim, unquantified method).
2. **CLAUDE.md and REVIEW.md** — code-owner-written, short, cap nits, require file+line evidence, list skip paths, summary opens with a finding count. See [[patterns/agents-md]].
3. **Automated PR review** on every PR.
4. **Security review** gating merge.
5. **CI plus PR template** (how tested, how to undo).
6. **Risk-tiered human approval** (below).
7. **Merge queue, feature flags, staged channels** (employees, latest, stable), on-call, incident review.

## Verified-findings design

Multiple agents search in parallel; a separate group votes on each finding. Style and cleanup findings are dropped (A/B tested). Severity tags: Important / Nit / Pre-existing. Substantive review-comment share on internal PRs went 16% to 54% at research-preview launch (vendor-stated; the same figure appears in [[governance/anthropic-ai-native-sdlc]]). Every finding must be fixed or resolved with a reason; no merge with open bug or security findings. Quick / Standard / Deep modes are set per repo.

## Risk tiers

| Tier | Examples | Human approval |
|---|---|---|
| Low | docs, copy, flagged additive changes | none |
| Medium | typical changes | one person |
| High | sensitive paths | two people |

The change, not the author, sets the tier (classifier); a second classifier can escalate. Only trusted authors get lighter paths. An agent's approval never fills a human slot, and the person prompting the agent counts as a required reviewer. Approval binds one commit and is invalidated by unvouched later commits.

## Feedback loop and evals

- Incidents become a daily-run eval: past incident PRs, fix-forwards, reverts, engineer-confirmed bugs.
- Noise is measured by classifying author response (fixed / wrong / intentional / don't care) plus runs on known-clean PRs. Stated priority: real bugs first, fewer review rounds second.
- **Convergence failure:** one CLI PR went 50+ overnight review/fix rounds; ~59% of later flags were code present since the first pass (git blame). The team now tracks rounds-to-pass alongside recall and changed re-review policy. Nightly review agents also run over existing code.

## Open gaps

- No circuit breakers yet that tighten approval when revert/incident numbers move; engineers want them before more zero-human merges. Revert detection still relies on authors, on-call, and dashboards.
- Knowledge transfer (review's second job) has no formal process: on-demand Claude-written explainers and visual artifacts per code slice, open Slack channels, authors usually fix what they land, unneeded PRs closed or reshaped early.

## Why it matters

- Contrast with [[deployments/openai-symphony]]: OpenAI's greenfield 0% pre-merge human review versus Anthropic keeping humans for medium/high risk and refusing to count agent approval as human. A difference in philosophy, not a factual contradiction.
- Same classifier-gated-trust idea as [[governance/claude-code-auto-mode]], applied to merges rather than tool calls.
- Multi-agent finding generation plus voting parallels [[deployments/devin-security-swarm]]; incident-derived eval calibration parallels [[patterns/sierra-monitor-eval-of-evals]].
- "Fix at the source" (a recurring flag becomes a CLAUDE.md, skill, or lint change) is observability-driven harness evolution ([[patterns/agentic-harness-engineering]], [[patterns/agent-skills]]).
- Verify-before-done addresses the premature-declare-done failure in [[patterns/effective-harnesses]]; rounds-to-pass is a process-discipline metric akin to [[evaluation/rigorbench]].
- Anthropic's short, owner-maintained context files, checked for reviewer compliance, are a data point for [[conflicts/agents-md-effectiveness]].
- Incident reviews asking which layer should have caught the issue echo [[case-studies/anthropic-claude-code-postmortem]]; trust framing echoes [[case-studies/willison-vibe-agentic-convergence]].

## Source

- `raw/research/weekly-2026-10-18/01-claude-code-review-at-anthropic.md` — captured 2026-10-18 from the claude.dev blog. **Vendor primary.** Practice descriptions are trustworthy; quantitative claims (2x merged PRs, >40% fewer reverts, 16%->54%, 90% Claude-written, 2,500 -> 30,000+ changes/day, 59%) are self-reported and collect-but-confirm.

## Related

- [[governance/anthropic-ai-native-sdlc]]
- [[governance/claude-code-auto-mode]]
- [[patterns/agents-md]]
- [[patterns/agent-skills]]
- [[patterns/agentic-harness-engineering]]
- [[patterns/effective-harnesses]]
- [[patterns/sierra-monitor-eval-of-evals]]
- [[evaluation/rigorbench]]
- [[conflicts/agents-md-effectiveness]]
- [[deployments/openai-symphony]]
- [[deployments/devin-security-swarm]]
- [[case-studies/anthropic-claude-code-postmortem]]
- [[case-studies/willison-vibe-agentic-convergence]]
