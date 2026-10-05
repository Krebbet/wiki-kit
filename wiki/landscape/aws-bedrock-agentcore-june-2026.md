# AWS Bedrock AgentCore (2026)

Amazon Bedrock AgentCore is a suite of seven composable, enterprise-grade services for deploying and operating AI agents at production scale — any framework (LangGraph, CrewAI, Strands, custom), any model, any cloud or on-premises target. It reached general availability on 2025-10-13, adding VPC, PrivateLink, CloudFormation, and resource tagging across all services at GA. The June 2026 AWS NY Summit extended the platform with a managed web search tool and a fully managed Knowledge Bases (RAG) service, both targeting the "grounded agent" gap that had required custom integrations before.

---

## Architecture: 7 services

**AgentCore Runtime** — Serverless, session-isolated execution environment. Accepts any Python-based agent framework via a three-line SDK integration (`BedrockAgentCoreApp`). Builds and deploys containerized agents to ECR; CLI (`agentcore launch`, `agentcore invoke`) covers local testing through cloud deployment. Session isolation is the primary security primitive: each user session runs in its own protected environment. VPC-only network config GA since 2025-10-13.

**AgentCore Memory** — Dual-mode memory store: short-term (session conversation turns, retrieved with `list_events`) and long-term (semantic extraction policies for user preferences, facts, and summaries, retrieved with `retrieve_memories`). Memory stores are namespace-partitioned and encrypted. Long-term strategies are applied to events at write time; strategies can be added to existing stores and apply forward only.

**AgentCore Observability** — Step-by-step trace visualization for agent executions, built on OpenTelemetry. Ships built-in CloudWatch dashboards (session count, latency, token usage, error rates, component-level breakdowns). Integrates with Datadog, LangSmith, and Langfuse via standard OTel export. AgentCore Evaluations (automated quality assessment, continuous production traffic monitoring, A/B testing for agent versions) reached GA 2026-03. Optimization capabilities (recommendations, batch evaluations) remain in preview as of mid-2026.

**AgentCore Identity** — Secure token vault for agent-to-service authentication. Supports OAuth 2.0 (Google Workspace, Salesforce, Slack, GitHub, and others) and API key providers. Integrates with Amazon Cognito, Okta, and Microsoft Entra ID. The `@requires_access_token` decorator handles token retrieval and renewal in agent code without storing credentials in agent logic. Provides workload identities — distinct, authenticated agent identities separate from user identities. **Update (2026-09):** each AgentCore Gateway now provisions its own managed OAuth 2.0 three-legged-authorization (3LO) consent portal, removing the need for developers to self-host OAuth callback infrastructure when agents call third-party tools (GitHub, Salesforce, Slack, etc.); handles post-consent session binding for thin/IDE-embedded clients that can't natively present consent URLs. AWS frames this as removing "undifferentiated heavy lifting," not a new identity/governance primitive — see [[landscape/agent-identity-governance-2026-09]] for the broader agent-identity/governance category this sits alongside.

**AgentCore Gateway** — Transforms AWS services (via Smithy models), Lambda functions, and third-party APIs (via OpenAPI specs) into MCP-compatible agent tools. Handles auth, throttling, request/response transformation, multitenancy, and tool selection (semantic ranking of most relevant tools per task). The managed web search announced at NY Summit 2026 (see below) is delivered as a built-in connector target on Gateway via MCP.

**AgentCore Browser** — Managed, headless browser instances for web automation workflows. Scales horizontally; browser sessions are isolated per agent session. Browser profiles (cookies, localStorage) stored in S3 Standard from 2026-04-15. Intended for integrations that expose no programmatic API.

**AgentCore Code Interpreter** — Sandboxed Python execution environment for agent-generated code. Isolated per session; no persistent state between invocations unless explicitly passed.

---

## June 2026 additions (AWS NY Summit, 2026-06-17)

**Managed Web Search** — Fully managed tool that grounds agent responses in current web knowledge. Exposed as a built-in connector on AgentCore Gateway via MCP: agents send natural-language queries, receive snippets, source URLs, titles, and publication dates. Runs inside the customer's secured AWS environment with no data egress to third parties. Resolves the previous pattern of wiring Perplexity, Brave, or custom search APIs through Identity + Gateway manually.

**Amazon Bedrock Managed Knowledge Bases (GA, 2026-06-17)** — Fully managed RAG pipeline service. Key capabilities: native data connectors (S3, SharePoint, Confluence, Google Drive), Smart Parsing for automatic multi-format ingestion, and an Agentic Retriever for complex multi-step queries. Integrates with AgentCore Gateway as a callable tool. Removes the previously common pattern of self-managing vector stores (OpenSearch, Pinecone) and ingestion pipelines for enterprise RAG.

---

## Pricing model

Consumption-based, no upfront commitments, no minimum fees. Each service billed independently; 12 distinct billing lines total (11 AgentCore-specific, plus underlying Bedrock model invocations billed separately at standard Bedrock rates).

Key rates (current as of 2026-06):

| Service | Rate |
|---|---|
| Runtime | $0.0895 / vCPU-hour + $0.00945 / GB-hour (active compute only; idle I/O wait excluded) |
| Memory | $0.25 / 1K records stored (model usage for extraction billed separately at Bedrock rates) |
| Identity | $0.000025 / authorization request |
| Browser profiles | S3 Standard rates (from 2026-04-15) |

Rough production estimate: a moderate-traffic customer support agent at 10K conversations/month (~5 turns each) runs $50–$200/month in AgentCore infrastructure, plus $200–$800/month in model inference depending on model selection.

Preview period (ended 2025-09-16): all AgentCore services were free to use. Standard CloudWatch pricing applies for Observability trace ingestion (CloudWatch Application Signals pricing plan).

---

## Deployment model

Enterprise security posture baked in at GA (2025-10-13):

- **VPC isolation** — VPC-only network config for agents that need to reach customer-VPC resources or connected services.
- **AWS PrivateLink** — All AgentCore service endpoints accessible without traversing the public internet.
- **CloudFormation support** — Full IaC parity; agent infrastructure codeable and repeatable.
- **Resource tagging** — Standard AWS cost allocation and governance tags on all AgentCore resources.
- **IAM execution roles** — Auto-created via CLI; scoped to Bedrock invocation by default, extensible to S3, DynamoDB, and other resources.
- **Session isolation** — Each user session runs in a separate protected environment; the primary guard against data leakage in multi-tenant deployments.

Regions as of preview announcement: US East (N. Virginia), US West (Oregon), Asia Pacific (Sydney), Europe (Frankfurt). GA region parity not confirmed in available sources; check AWS docs for current coverage.

---

## Competitive position

**vs Salesforce Agent Fabric (Agentforce)** — Agentforce wins when the core system of record is Salesforce CRM (sales, service, commerce workflows). AgentCore wins when engineers author agents in arbitrary frameworks against arbitrary backends. Agentforce is higher-abstraction and lower-flexibility; AgentCore is lower-abstraction and higher-flexibility. The populations rarely compete for the same workload in practice.

**vs Microsoft Agent365 / Azure AI Foundry** — Azure AI Foundry (Agent Service GA, 2025-05) is the build-and-run layer; Agent365 (launched 2025-11) is the cross-vendor enterprise control plane with deep Microsoft 365 and SharePoint ACL synchronization — the killer feature for enterprise governance across mixed agent estates (Foundry + Agentforce + open-source). AgentCore offers no cross-vendor control plane equivalent. Conversely, AgentCore's framework agnosticism and VPC/PrivateLink model are stronger for AWS-native engineering teams; Agent365 is stronger for Microsoft-first enterprises running mixed agent vendors under unified governance.

**vs Google Vertex AI Agent Builder (GEAP)** — Google's stack is tightly coupled to Gemini models and Vertex-hosted OSS; AgentCore is explicitly model-agnostic (any Bedrock model or external model). Google's strength is integration depth within Google Cloud (BigQuery, Workspace, Search); AWS's strength is breadth of AWS service integration and the managed payment rail (AgentCore Payments, preview 2026-05-17). Neither has a comparable managed web search tool and managed Knowledge Bases offering as of mid-2026 — AWS NY Summit 2026 is the first hyperscaler to bundle both as fully managed GA services in one agent platform.

**Differentiator summary:** AgentCore's defensible moat is the combination of (a) framework/model agnosticism at runtime, (b) enterprise network isolation (VPC, PrivateLink) without configuration overhead, (c) the managed payment rail (x402/Coinbase/Stripe, preview), and (d) the June 2026 additions of managed web search + Knowledge Bases that close the grounding gap. The weakness is the absence of a cross-vendor governance control plane — enterprises running agents on multiple clouds need Agent365 or a custom layer on top.

A common Fortune 500 pattern emerging in mid-2026: Azure Foundry for IT-led workflows, Agentforce for customer-facing CRM agents, AgentCore for engineering-authored agents — with Agent365 as the cross-platform governance layer.

---

## Conflict flags

**C21 (AgentCore Payments primacy):** The existing [[landscape/agentcore-payments-x402-2026-05]] page documents the contested "first managed agent payment capabilities" claim against Google AP2. The June 2026 NY Summit updates do not resolve this conflict. AgentCore Payments remains in preview; no new payment-specific capabilities were announced at NY Summit. No update to C21 warranted from this source.

---

## Source

- `raw/research/weekly-2026-06-17/03-aws-bedrock-agentcore-2026.md` — original AWS preview blog (captured 2026-06-17); updated notes: GA confirmed 2025-10-13, Discord link updated 2026-05-12
- AWS NY Summit announcement blog (2026-06-17): https://aws.amazon.com/blogs/aws/top-announcements-of-the-aws-summit-in-new-york-2026/
- AgentCore Web Search announcement (2026-06-17): https://aws.amazon.com/blogs/aws/announcing-web-search-on-amazon-bedrock-agentcore-ground-your-ai-agents-in-current-accurate-web-knowledge/
- Managed Knowledge Bases GA announcement (2026-06-17): https://aws.amazon.com/blogs/aws/introducing-amazon-bedrock-managed-knowledge-base-for-faster-more-accurate-enterprise-ai-applications/
- AgentCore pricing page: https://aws.amazon.com/bedrock/agentcore/pricing/
- AgentCore Identity managed consent portal (2026-09): `raw/research/weekly-2026-09-16/03-aws-agentcore-identity.md` — https://aws.amazon.com/about-aws/whats-new/2026/09/amazon-bedrock-agentcore/

---

## Related

[[landscape/agentcore-payments-x402-2026-05]] [[landscape/google-cloud-next-2026-day2]] [[landscape/microsoft-build-2026-06]] [[platforms/databricks]] [[landscape/agent-identity-governance-2026-09]]
