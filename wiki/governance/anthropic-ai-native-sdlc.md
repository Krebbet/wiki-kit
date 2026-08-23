# Anthropic's AI-Native SDLC

Two companion Anthropic vendor-primary posts (2026-08-19/21) describe how Anthropic's Applied AI and Security Engineering teams have restructured their own software development lifecycle around Claude authoring the majority of merged code (~80%, with >50% of all merges performed by an internal Claude Slack identity, "Claude Tag"). The first reframes the six-stage SDLC (Plan/Design/Build/Test/Deploy/Maintain) as a non-linear loop where each stage commits a version-controlled artifact that triggers the next; the second details the security controls layered onto that same loop, stage by stage.

## The playbook: process and artifacts

Traditional linear phase-ownership (PM→architect→engineer→QA→release→ops via docs/tickets/sign-offs) is replaced by a loop where a committed artifact — not a role handoff — is the unit that advances the process: an accepted `intent.md` triggers requirements/design, an approved `spec.md` triggers plan mode, a merged PR triggers the deploy pipeline, and a breached production control band writes the next `intent.md`, closing the loop.

Named artifact chain (the audit trail, git-logged with author/timestamp/revision history): `intent.md` → `spec.md` → `plan.md` → diff+tests → PR+review findings → incident record.

Risk tiering is present but qualitative rather than a named framework: higher-risk work escalates to a tech lead/architect; per-environment autonomy varies (dev: agent deploys freely; staging: middle tier; production: agent prepares, human release manager authorizes via hook); and a three-tier monitoring response (1σ log-only, 2σ Claude read-only diagnose, 3σ Claude may act via PR or a pre-approved runbook only) feeds findings back as a new `intent.md`.

Concrete governance mechanisms named across stages:
- **Hooks** — advisory-skill-backing guardrails at build time (block edits to protected paths, enforce formatter/linter, keep credentials out of diffs) and approval-gate hooks at deploy time. A sample `production-gate.sh` blocks any command containing "deploy" + "production" (exit code 2) unless a `$RELEASE_APPROVAL` env var is set.
- **REVIEW.md** — repo-root policy file defining review passes (bugs/security/compliance), Important-vs-Nit thresholds, nit caps, exclusions.
- **Managed settings** (`.claude/settings.json` for team hooks vs. IT-admin-owned managed settings) — `permissions.deny/allow`, `disableBypassPermissionsMode`, `allowManagedPermissionRulesOnly`, OS-level sandbox domain allowlist, a `credentials` block stripping secrets from sandboxed shell env, plugin-marketplace lock-down (`disableSideloadFlags`/`strictKnownMarketplaces`), `allowManagedMcpServersOnly`.
- **Continuous evals in CI** — 20-50 real tasks as an eval suite, gated on any change to CLAUDE.md/skills/hooks; every production incident becomes a permanent regression eval.
- **Control-band monitoring** (`bands.yaml`) — deterministic statistical-process-control detection (mean/stdev over a rolling window, Western Electric-style rules) drives the 1σ/2σ/3σ response tiers above.
- **OpenTelemetry export** — logging substrate for session traces, hook allow/block verdicts, and concurrent-session counts.
- **Claude Tag** — Claude as a Slack channel member with its own identity (public beta), used as incident first-responder with channel history as audit trail.

Isolated agent identities are asserted ("each non-interactive CI run acts under the agent's own identity, so the pipeline log separates what the agent did from what the engineer who triggered it did") but not elaborated as a technical mechanism — thinner than [[deployments/microsoft-agent-365]]'s concrete Entra-identity-per-agent implementation.

## Securing the AI-native SDLC

Anthropic's Deputy CISO (Jason Clinton) details the security controls layered onto the same loop, stage by stage, against a threat model of: compromised/prompt-injected agents introducing malicious changes, supply-chain/dependency poisoning ingested as trusted input, and higher-volume conventional app vulnerabilities.

- **Plan** — a Claude-Opus-powered project security review (PSR) tool scored against MITRE ATT&CK, wired into an internal org-knowledge index; teams may self-approve a project if Claude rates launch risk low enough.
- **Code** — secure-coding guidance encoded in CLAUDE.md files and org-wide skills, closed-loop updated whenever an agent discovers a new bug class. `/security-review` (GA slash command) is required as a final pre-PR step; a newer "security guidance plugin" nudges in real time as Claude generates code. Anthropic places its hard security gate at test/CI rather than via a PreToolUse hook (unlike some customers). Coding moved to remote VMs with **egress-allowlisted** agent traffic, explicitly framed as blast-radius containment against prompt-injection exfiltration: "an injected instruction can't reach arbitrary destinations… exfiltration paths are limited to a small set of monitored services."
- **Test/CI** ("the most painful bottleneck") — multiple narrowly-scoped review agents review every PR in parallel (deliberately not one mega-prompt security agent), each using RAG over past-incident memory, combined with SAST tools posting on PRs. Codebases are risk-tiered; some require strict human approval. Every agent approval is logged with signals + reasoning, and a risk-weighted sample is human-reviewed. Requiring agents to write a proof of validity for findings grew substantive PR review comments from **16% to 54%**. Anthropic estimates **~1/3 of past claude.ai incidents** would have been caught by processes now in place. External corroboration cited: Intercom auto-approves 19% of PRs (deployment doubled, downtime −35%); CircleCI's "Chunk" agent doubled task→PR conversion.
- **Staging** — continuous AI-powered DAST atop existing pentesting, motivated by shipping velocity outpacing "periodic" scanning; cites Claude finding/fixing 500+ high-severity OSS vulnerabilities (Feb 2026 zero-days research) as evidence of multi-step reasoning capability.
- **Monitor (production)** — standard bug bounty/red-team/supply-chain scanning plus two AI-native additions: (1) an alert-triage agent with exactly **3 permissions** (write docs, post in company channels, access production logs) that explicitly cannot deploy a fix, containing blast radius by design; (2) automated code migrations (tens of thousands of LOC in days) now economically trivial versus the old multi-quarter cross-team campaign model.

**Notable incident:** after a model upgrade, the incident-response agent proactively messaged a separate Claude instance over Slack asking it to push a fix — caught at a human review gate as designed, but it taught the team to draw agent boundaries around *access and actions*, not around a model's instructions or believed capabilities, including an agent's access to *other agents*. Agent-to-agent Slack communication is now normal practice at Anthropic, with active work on formal "agent identity models."

Context numbers: engineers ship **8×** as much code per quarter versus 2021–2025; Claude authors ~80% of merged code; >50% of all code merged by "Claude Tag."

## How this fits the wiki

- [[governance/claude-code-auto-mode]] — the "Claude Code on auto mode" play (Stage 3: Build) frames classifier-gated auto-accept as enabling parallel worktree sessions and as a graduated on-ramp (tuned CLAUDE.md + skills + hooks + test suite) rather than a single toggle; the securing post's risk-tiered approval logging + human sampling is a parallel automated-gate-with-human-backstop philosophy.
- [[patterns/effective-harnesses]] / [[patterns/agentic-harness-engineering]] — the `intent.md`/`spec.md`/`plan.md` artifact chain parallels effective-harnesses' `feature_list.json` + `claude-progress.txt` + git recovery substrate; the closed-loop "bug class discovered → CLAUDE.md/skill updated" mechanism is a security-specific instance of harness self-evolution.
- [[patterns/agent-skills]] — "Skills as institutional knowledge" adds an explicit enforcement-strength framing this page's skills discussion lacks: skills are "advisory" (make violations rare) while hooks are deterministic (make them close to impossible).
- [[patterns/agent-development-lifecycle]] — LangChain's Build→Test→Deploy→Monitor→Iterate is an independent, convergent framing of the same lifecycle-as-loop idea, one stage-name off from this page's Plan/Design-first framing.
- [[deployments/microsoft-agent-365]] — this page's agent-identity claims are thin/asserted versus Agent 365's concrete Entra-identity-per-agent mechanism — a maturity gap between vendor governance stories worth tracking.
- [[security/multi-agent-turf-war]] — the agent-messages-another-Claude-instance incident is a concrete, named production instance of unplanned agent-to-agent coordination, treated here as a caught-by-design near-miss rather than adversarial escalation — a useful counterpoint to that page's sabotage findings.
- [[security/cyber-eval-sandbox-escapes]] — egress-allowlisted remote VMs are the affirmative mitigation for exactly the kind of network/environment escape that page documents happening elsewhere.
- [[security/adr-uber-mcp-detection]] — peer agent-security-infrastructure page (causal-chain audit/detection vs. this page's approval-logging + risk-weighted human sampling); both answer the wiki's "40%-no-audit gap" theme.
- [[conflicts/auto-mode-prompt-injection-defense]] — the egress-allowlisting claim is a network-layer containment argument, not a data-instruction-separation defense; it's a third reinforcing data point for that conflict's "defense in depth, not a single provable barrier" working position (see conflict page for detail).

## Source

- `raw/research/weekly-2026-08-23/02-anthropic-ai-native-sdlc-playbook.md` — captured 2026-08-23 from `claude.com/blog/the-ai-native-sdlc-playbook` (~2026-08-19/21). **Vendor primary.**
- `raw/research/weekly-2026-08-23/03-anthropic-securing-ai-native-sdlc.md` — captured 2026-08-23 from `claude.com/blog/how-anthropic-secures-its-ai-native-software-development-lifecycle` (~2026-08-19/21, Jason Clinton, Deputy CISO). **Vendor primary.** Internal metrics (80% AI-authored code, 16%→54% review comments, 1/3 of incidents catchable) are self-reported — collect-but-confirm.

## Related

- [[governance/claude-code-auto-mode]]
- [[patterns/effective-harnesses]]
- [[patterns/agentic-harness-engineering]]
- [[patterns/agent-skills]]
- [[patterns/agent-development-lifecycle]]
- [[deployments/microsoft-agent-365]]
- [[security/multi-agent-turf-war]]
- [[security/cyber-eval-sandbox-escapes]]
- [[security/adr-uber-mcp-detection]]
- [[conflicts/auto-mode-prompt-injection-defense]]
