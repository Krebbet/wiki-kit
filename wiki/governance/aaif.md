# Agentic AI Foundation (AAIF)

The Agentic AI Foundation (AAIF) is a directed fund under the Linux Foundation, co-founded in May 2026 by OpenAI, Anthropic, and Block, with Google, Microsoft, AWS, Bloomberg, and Cloudflare as supporting members. AAIF provides neutral stewardship for open, interoperable agentic AI infrastructure — principally the three project donations its co-founders brought to the foundation: AGENTS.md (OpenAI), the Model Context Protocol / MCP (Anthropic), and Goose (Block). Its founding rationale is preventing ecosystem fragmentation as agent systems move from prototypes into production tools handling real business and consumer work.

## Source

- `raw/research/weekly-2026-05-31/05-openai-agentic-ai-foundation.md` (captured 2026-05-31 from https://openai.com/index/agentic-ai-foundation/)

## Structure and membership

- **Legal form:** directed fund under the Linux Foundation (non-profit), following the governance model used for Linux Kernel, Kubernetes, Node.js, and PyTorch.
- **Co-founders:** OpenAI, Anthropic, Block.
- **Supporting members:** Google, Microsoft, AWS, Bloomberg, Cloudflare.
- **Governance model:** Linux Foundation neutral stewardship — no single company controls direction; contributions governed by community-led standards development.

## Donated open standards

| Project | Donor | Description |
|---|---|---|
| AGENTS.md | OpenAI | Lightweight Markdown format for per-project agent instructions; see [[patterns/agents-md]] |
| Model Context Protocol (MCP) | Anthropic | Agent-to-tool integration protocol; see [[deployments/mcp-infrastructure]] |
| Goose | Block | Open-source agentic framework |

## Mission and rationale

AAIF was created at the moment agent systems crossed from experimentation into production. The founding post identifies two compounding risks at that crossing:

1. **Fragmentation risk** — without common conventions, agent development splits into incompatible silos that limit portability, safety, and progress.
2. **Control risk** — each open standard was previously steered by a single vendor; as adoption grows, single-vendor control of foundational infrastructure becomes a governance liability.

The Linux Foundation model addresses both: proven neutral governance at scale, no single company with veto authority, community-led evolution.

The AAIF announcement coincides with AGENTS.md reaching 60,000+ open-source adopters and Codex reportedly contributing to more than two million merged GitHub pull requests (both vendor-stated figures — collect-but-confirm). The timing is deliberate: formalize governance at the adoption inflection, not after.

## Related

- [[patterns/agents-md]] — the AGENTS.md standard donated by OpenAI; format design, adoption landscape, effectiveness conflict
- [[deployments/mcp-infrastructure]] — MCP donated by Anthropic; governance now upstream in AAIF rather than Anthropic
- [[deployments/microsoft-agent-365]] — Microsoft is a supporting AAIF member; relevant to its multi-cloud governance framing
- [[deployments/openai-symphony]] — OpenAI Frontier harness built on AGENTS.md + skills; now under AAIF governance
- [[conflicts/agents-md-effectiveness]] — AAIF institutionalises the vendor-favorable position on context files just as the open conflict on effectiveness remains unresolved
