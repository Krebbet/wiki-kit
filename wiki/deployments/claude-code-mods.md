# Claude Code Mods

Claude Code "Mods" are TypeScript/JavaScript plugins that run inside the Claude Code harness (CLI and Desktop), hook events such as prompts, tool calls and interface rendering, and can observe, re-render or take over default handling. A Latent Space practitioner post frames them as an early user-programmable "Attention Interface" and as "middleware for the agent harness", contrasts them with ChatGPT Intelligent UI and Cursor PR Routing & Approval, and reports candid downsides: noise, token cost and an unsandboxed trust surface. The source is a secondary, n=1 practitioner account; Anthropic and competitor facts are relayed from their docs and are collect-but-confirm.

## Mechanism

- A mod is a Claude Code plugin of TS/JS functions that respond to harness events (prompt, tool call, interface render) and may observe, modify rendering, or handle the event instead of the default behavior.
- Claude Code ships a built-in skill, `plugin-authoring`, so Claude can write a mod from a plain-language request (skill-driven self-customization).
- Per Anthropic's docs (relayed secondhand), six mods ship built in: `agents-md` (loads AGENTS.md as project instructions), `diff` (takes over the /diff pane), `plugin-authoring`, `sec-default` (guards org-managed settings from user-installed mods), `telemetry`, and `you-should-know` (the only one off by default). Implication: parts of Claude Code are themselves implemented as mods.

## You Should Know and Next Steps Supervisor

- `you-should-know` runs a side agent observing the main agent and surfaces missed items above the prompt. Anecdote: it flagged that the file being edited (CompareView.swift) and about 45 others had uncommitted work, so discarding demo edits would have lost earlier work. Single anecdote; no measured precision or recall.
- The author's own Next Steps Supervisor (third-party, part of the open-source ModSmith plugin by the author) triggers after turns that edit files, run commands, or make 8 or more tool calls. Since install on Oct 15, 99 of 111 turns (about 89%) met the bar, so it fires almost every turn and the author starts skimming it.
- Cost, per the mod's own README: about 5-6k input-equivalent tokens per check on a 50k-token session, more when the cache is cold, because each check forks and re-reads the conversation.

## Attention-interface framing

The post's design axis is who authors the attention interface:

| Approach | Author | Notes (vendor-sourced via secondary writeup) |
|---|---|---|
| ChatGPT Intelligent UI | The model | Shipped with GPT-6 on Oct 7; generates charts, forms and checklists from an OpenAI-built component library; minimal user control |
| Cursor PR Routing & Approval | The team, via policy | Reviewer assignment by ownership and commit history; auto-approve low-risk PRs (risk score vs threshold); Bugbot/Security findings; repo policy files. A PR that edits an approval policy cannot relax review on itself, because policy is read from the base branch. Cursor docs say it "does not replace a full code review" |
| Claude Code Mods | The user plus the agent, in code | Programmable, local, per-user |

The author bets the harness becomes a platform others build on (browser analogy) and proposes that the harness mine session transcripts to suggest mods. All of this is speculative opinion.

## Downsides

- **Noise:** a supervisor that fires on about 89% of turns stops being a signal.
- **Cost:** forked side-agent checks re-read the conversation and are cache-dependent (see [[patterns/claude-platform-cost-optimization]]).
- **Trust:** per Anthropic docs, a mod can read and write files, see every prompt and spend usage; mods are not sandboxed, and built-in mods keep running under `--safe-mode`. The author would read third-party mod code before installing. This is an unsandboxed extension surface and a supply-chain risk, in contrast to policy-enforced containment ([[security/microsoft-execution-containers]]).

## Evidence quality

Practitioner opinion (Latent Space, Oct 2026) with first-hand use over 111 turns; no controlled evaluation. ModSmith code is open source on GitHub. Anthropic's public Claude Mods documentation is the stronger primary source and is worth capturing to confirm the built-in list and the trust claims.

## Source

- `raw/research/weekly-2026-10-25/03-claude-mods-latent-space.md` — Latent Space, "Claude Mods: Flipping the Harness Inside Out" (Oct 2026). Secondary practitioner post; vendor facts relayed secondhand, collect-but-confirm. Analyst summary at `raw/research/weekly-2026-10-25/.ingest/03-claude-mods-latent-space.summary.md`.

## Related

- [[patterns/agent-plugins-spec]] — Mods are code-executing Claude Code plugins; the spec's lack of a permission model or signing in v1 matches the "mods aren't sandboxed" caveat
- [[governance/claude-code-auto-mode]] — another Anthropic attention/approval control surface; `sec-default` can sit beside classifier-gated permissions
- [[governance/claude-code-review-at-anthropic]] — risk-tiered human approval; "a PR cannot relax its own review policy" echoes agent approval never counting as a person's
- [[patterns/harness-design-space]] — adds a user-programmable middleware axis to the entry/control and safety dimensions
- [[patterns/externalization-survey]] — harness-as-platform framing
- [[patterns/agent-skills]] — the built-in `plugin-authoring` skill lets Claude author mods
- [[deployments/cursor-cloud-agents]] — Cursor's approval-agent direction for agent-written PR streams
- [[deployments/openai-dots]] — OpenAI's parallel agent/UI direction
- [[patterns/claude-platform-cost-optimization]] — cache-dependent cost of forked side-agent checks
- [[patterns/harness-self-evolution-survey]] — transcript-mined mod suggestions are a user-level self-evolution loop
- [[security/microsoft-execution-containers]] — policy-enforced containment versus unsandboxed in-process mods
