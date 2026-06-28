# Agent Communication Protocols Taxonomy (arXiv 2606.19135)

*"A Technical Taxonomy of LLM Agent Communication Protocols"* — TU Munich, June 2026. A rigorous five-dimension taxonomy applied to nine actively maintained open-source LLM agent communication protocols using Nickerson et al.'s iterative method (5 iterations). Predicts the field converges on a federated, OSI-style layered protocol stack rather than a single dominant protocol.

## Five Taxonomy Dimensions

| Dimension | Values |
|-----------|--------|
| **Counterparty** | context / agent / hybrid |
| **Payload** | structured+artifacts / conversation-focused / hybrid |
| **Interaction state** | stateless / session-state |
| **Discovery mechanism** | static / centralized / partially-centralized / decentralized / hybrid |
| **Schema flexibility** | single / multiple / evolving |

## Nine Classified Protocols

| Protocol | Counterparty | Payload | State | Discovery | Schema |
|----------|-------------|---------|-------|-----------|--------|
| MCP (Anthropic) | context | structured+artifacts | stateless | static | multiple |
| A2A (Google) | agent | hybrid | session-state | centralized | multiple |
| LAP (LangChain) | agent | hybrid | session-state | static | multiple |
| agents.json | context | structured+artifacts | stateless | static | single |
| Agora (Oxford) | agent | hybrid | session-state | decentralized | evolving |
| ANP (Agent Network) | agent | hybrid | session-state | hybrid | evolving |
| LMOS (Eclipse) | agent | hybrid | session-state | hybrid | multiple |
| ACP (BeeAI/IBM) | agent | hybrid | session-state | centralized | multiple |
| agntcy | agent | hybrid | session-state | centralized | multiple |

**Key pattern**: all seven agent-to-agent protocols use session-state and hybrid payloads; both context protocols (MCP, agents.json) are stateless with structured-only data. This is not coincidence — it reflects the bandwidth-vs-tractability trade-off in agent deliberation.

## The Agent Communication Trilemma

No protocol can simultaneously maximize:
- **Versatility** (rich semantics, adaptive communication)
- **Efficiency** (low token overhead, predictable schema)
- **Portability** (platform-independent, broadly adoptable)

MCP maximizes portability + efficiency at the cost of versatility. Agora and ANP maximize versatility with evolving schemas at token-cost. Most protocols (A2A, LMOS, ACP) occupy the middle with hybrid payloads and multiple static schemas.

## Key Trends Observed

- **Schema flexibility is evolving**: 7 of 9 protocols support multiple predefined schemas; Agora and ANP enable runtime *evolving* schema negotiation (plain-text Protocol Documents negotiated before each session) — a move toward adaptive communication.
- **Discovery is the lagging dimension**: decentralized peer-to-peer discovery is rare (only LMOS uses a hybrid approach); 4 of 9 rely on static configuration, 4 of 9 on centralized registries. This is a bottleneck if the Internet of Agents paradigm scales.
- **Cross-cutting gap**: no protocol addresses privacy safeguards, compliance checks, or policy enforcement — highlighted as critical for healthcare and HR deployments.

## Federated Layered Stack Prediction

Long-term convergence is predicted toward an OSI-style layered stack:
- **Discovery layer**: agents.json (or equivalent) — static resource manifests
- **Tool-execution layer**: MCP — structured, stateless, portable tool calls
- **Deliberation layer**: ANP / Agora — session-aware, schema-evolving agent-to-agent communication

Short-term pressure exists toward protocols that unify agent-to-agent and agent-to-context counterparty types.

## Conflict Flags

- **MCP is stateless by design** and was designed for agent-to-context (tool/data) communication, not agent-to-agent. This is technically correct per Anthropic's own docs. [[mcp-infrastructure]]'s 2026 roadmap discussion and [[mcp-multi-agent-framework]]'s multi-agent use patterns describe extended/future use cases that go beyond MCP's design intent. Distinction: MCP-as-designed (context counterparty, stateless) vs. MCP-as-used (extended via A2A or application-layer patterns).
- **A2A and MCP are complementary, not competing** (Google's explicit statement): [[mcp-infrastructure]] should not imply A2A integration is a settled MCP roadmap item — it is an unendorsed vendor proposal (as of the paper's publication).

## Source

- Raw: `raw/research/weekly-2026-06-28/04-llm-agent-protocol-taxonomy.md`
- arXiv: https://arxiv.org/abs/2606.19135
- Captured: 2026-06-28

## Related

- [[mcp-infrastructure]] — MCP is one of the nine classified protocols; MCP-as-designed vs. MCP-as-used distinction
- [[mcp-multi-agent-framework]] — context-retention failures map to interaction-state and schema-flexibility dimensions
- [[patterns/topology-taxonomy]] — protocol choice maps to MAS topology concerns (hierarchical vs. equi-level)
- [[patterns/externalization-survey]] — protocols are the "protocols" externalization layer; this taxonomy operationalizes it
- [[deployments/openai-symphony]] — MCP-skepticism on token-economic grounds maps to the portability/efficiency axis
- [[case-studies/notion-token-town]] — four-axis MCP-vs-CLIs framing re-interpretable via counterparty + payload dimensions
