# GitHub Copilot local sandboxing GA (2026-10-07)

GitHub made local sandboxing for Copilot GA on 2026-10-07 in Copilot CLI, the Copilot app, and VS Code sessions using Agent Host. It restricts what agent-initiated tools and commands can reach on the developer's machine, is included at no extra cost, and runs on Microsoft's MXC. **Use it if you're on Copilot** (free, org-enforceable); but this is a vendor-only changelog with no independent testing, so treat escape resistance as unproven.

## What it does (vendor changelog, 2026-10-07)

- Restricts filesystem (readable/modifiable paths), network (internet, local network), and credential access (Git credentials, GitHub CLI credentials) for agent-run tools and commands.
- Can sandbox local MCP servers and language servers "where supported".
- Policies are set by the developer or organization; enterprise-managed settings can require sandboxing and enforce policies developers cannot weaken.
- Built on Microsoft eXecution Container (MXC, github.com/microsoft/mxc), which translates one common policy into native OS controls on Windows, macOS and Linux.
- Isolation applies to tool execution regardless of which model Copilot uses.
- Cost: included with GitHub Copilot, no additional charge (2026-10-07).

## Gaps

No data on escape resistance, performance overhead, or per-OS feature parity. MCP and language-server coverage is conditional. The docs link mentions cloud and local sandboxes; the cloud side is not described. Copilot-only: says nothing about other agents.

## Techniques worth stealing

One declarative policy compiled to per-OS sandbox primitives; tool isolation separate from the model layer; an org-enforced policy floor; credential-level gating as a distinct control.

## Source

- `raw/research/weekly-2026-11-04/01-github-copilot-local-sandboxing.md` (github.blog changelog, 2026-10-07, captured 2026-11-04)

## Related

- [[landscape/microsoft-project-perception-guardian-agents-2026-10]] — MXC in Microsoft's enterprise governance story
- [[platforms/microsoft]] — Microsoft platform profile
- [[landscape/nvidia-open-agent-safety-platform-2026-09]] — parallel agent sandbox layer
- [[landscape/gemini-at-work-agent-2026-10]] — Google Agent Sandbox parallel
- [[landscape/blackhat-ai-coding-agent-cves-2026-08]] — coding-agent RCE threat class
- [[landscape/mcp-rce-supply-chain-2026-05]] — MCP threat class that local sandboxing targets
- [[landscape/agentic-compute-pricing-2026-04]] — Copilot pricing context
