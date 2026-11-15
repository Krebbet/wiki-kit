# DeepSeek Super-Agent (prototype)

DeepSeek's Harness team released "Super-Agent", an open-source prototype coding agent, around 2026-10-31 (outlets differ: Oct 31 vs Nov 1/2). Press describes it as a proactive/ambient agent that monitors developer group chats for coding problems and volunteers fixes (often as pull requests) without being summoned, positioned against Claude Code and Codex. **Press-only stub page: no benchmarks, licence, repo URL or model backend in the captured article; collect-but-confirm.** Upgrade after reading the GitHub manual / WeChat announcement.

## What the sources say

- **Mechanism:** ambient agent watching developer group chats; stated aim from the repo manual (quoted second-hand): "Take as little human attention as possible, and give as much value as possible." No detail on tools, sandboxing, permissions or model.
- **Org context:** the DeepSeek Harness team (formed earlier in 2026) builds the software layer around the model; it follows DeepSeek's MIT-licensed Harness v0.1 (Aug 2026), per search coverage (secondary).
- **Release:** open-source with a GitHub user manual; one outlet (RuntimeWire) says MIT-licensed research code and that the public prototype differs from DeepSeek's private internal implementation, with some designs unimplemented. Another outlet describes web/API access, which conflicts with the prototype framing.
- **Evidence tier:** Digital Trends (quoted second-hand) calls it a prototype, not proof DeepSeek has overtaken rivals. Treat the "rival to Claude Code" framing as press framing.

## Safety note (wiki-side inference)

Unprompted action over ingested chat content implies chat-read access and unsolicited posting, a prompt-injection and data-exposure surface of the kind tracked in [[conflicts/auto-mode-prompt-injection-defense]] and [[security/cyber-eval-sandbox-escapes]]. The permission model is unaddressed in the article.

## Source

- `raw/research/weekly-2026-11-15/05-deepseek-super-agent.md` (Entrepreneur India press piece)

## Related

- [[deployments/deepseek-v4-1-flash]] — same vendor; any link between the model and this harness is unconfirmed
- [[coding-agents/cognition-swe-2]] — another competing coding-agent offering
- [[conflicts/auto-mode-prompt-injection-defense]]
- [[security/cyber-eval-sandbox-escapes]]
