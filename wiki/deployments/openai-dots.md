# OpenAI Dots — Always-On ChatGPT Agents

OpenAI launched "Dots" at DevDay on 2026-09-29: always-on, goal-driven ChatGPT agents powered by GPT-6 Astra, each with its own cloud computer, reachable from ChatGPT, Slack and Teams. It is the productized follow-up to the "o" always-on agent teaser and puts OpenAI alongside Cursor, Cognition and Claude Code in the persistent cloud-agent category. **Press-tier sourcing**: everything below comes from SiliconANGLE's write-up of OpenAI's launch post and help doc, so all product claims are vendor-stated and collect-but-confirm. There are no benchmarks and no isolation or sandbox detail.

## What was announced

- **Architecture (as reported):** each Dot runs on GPT-6 Astra with a dedicated cloud computer the user can open to watch it work. With permission it can also operate on the owner's laptop. More than 4,000 apps are reachable through OpenAI plugins.
- **Always-on, goal-driven:** the user hands over a goal and the agent carries it across several concurrent projects, learning owner preferences from feedback.
- **Channel-portable context:** message or call the agent in ChatGPT (desktop/web/mobile) or Slack/Teams. Context follows the agent across channels, so a project can move from ChatGPT to a Slack team without re-briefing.
- **Proactive research:** with no task assigned the agent looks for ways to help, with its app connections restricted to read-only in this mode.
- **Safety controls:** actions touching accounts or sharing information must clear an "auto-review". A monitoring system can pause or stop an agent. OpenAI says agents "can still make mistakes". An early tester's agent drafted an invoice and waited for approval before sending.
- **Specialist agents (preview):** employer-provisioned, each with its own identity and credentials for one defined job (procurement and invoice processing tested internally). Customers start with focused pilots alongside OpenAI engineers. Microsoft is working so these can be governed through [[deployments/microsoft-agent-365]].
- **Internal dogfooding (vendor-stated, no numbers):** agents start investigating bugs reported in OpenAI's Slack and turn new designs into working apps.
- **Availability:** rolling out from 2026-09-29 to ChatGPT Pro and Business Premium. Pro in the EEA, Switzerland and the UK is excluded. Enterprise/Edu/Healthcare get a beta once an admin enables it. One agent is included at no extra cost, and usage does not count against plan allowances for the first month. Extra agents and more capacity are planned at undisclosed prices.

## Where it sits in the wiki

- **Same pattern as the cloud-agent vendors:** a dedicated machine per agent and a standing-goal rather than chat-turn model parallels [[deployments/cognition-cloud-agents]], [[deployments/cursor-cloud-agents]] and [[deployments/claude-code-projects]]. Meta's Muse personal agent (see [[coding-agents/meta-muse-code]]) also runs on a dedicated cloud computer, so the category now has all four frontier-adjacent vendors.
- **Action-layer gating:** auto-review, the read-only proactive mode and monitor-and-pause are another defense layer in the style of [[governance/claude-code-auto-mode]]. No attack-success data is given, so it adds nothing resolving to [[conflicts/auto-mode-prompt-injection-defense]].
- **Containment context:** the "pause or stop" monitoring claim sits against OpenAI's record in [[security/cyber-eval-sandbox-escapes]]. Treat it as an unverified assertion until independent evaluation exists.
- **Internal adoption now productized:** extends [[deployments/openai-agents-transforming-work]] from internal Codex adoption to a general ChatGPT surface, on the primitives described in [[patterns/openai-gpt-5-6-agentic-primitives]].
- **Plugin ecosystem:** the 4,000+ app count relates to the packaging work in [[patterns/agent-plugins-spec]].

## Open questions

- No primary OpenAI source was captured. The DevDay recap page returned only its intro (and a JS-rendered retry returned nearly nothing), so a primary-source check is pending.
- Isolation model, latency, cost per agent-hour and failure rates are all undisclosed.

## Source

- `raw/research/weekly-2026-10-04/01-openai-dots.md` — SiliconANGLE, 2026-09-29 (secondary press)

## Related

- [[deployments/cursor-cloud-agents]]
- [[deployments/cognition-cloud-agents]]
- [[deployments/claude-code-projects]]
- [[deployments/microsoft-agent-365]]
- [[coding-agents/meta-muse-code]]
- [[governance/claude-code-auto-mode]]
- [[conflicts/auto-mode-prompt-injection-defense]]
- [[security/cyber-eval-sandbox-escapes]]
- [[patterns/agent-plugins-spec]]
