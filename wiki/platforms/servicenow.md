# ServiceNow

ServiceNow (enterprise workflow/ITSM incumbent) announced "AI Passport" on ~2026-10-15/21: a cryptographically signed, per-agent runtime authority credential for AI agents and MCP servers, issued by its "Super Intelligence Control Tower", alongside a broader AI-governance suite (shadow-AI discovery, cost governance, policy enforcement). NVIDIA is a "design and launch partner" for the enforcement layer. **Evidence is thin:** one vendor-derived write-up (Help Net Security, captured 2026-10-21), no GA date, no pricing, no independent testing, and most governance features are future-tense ("will enable", "will manage").

**Tier:** enterprise platform. **Working read (2026-10-21):** a large incumbent entering the agent identity/governance category; credible mainly for existing ServiceNow shops where CMDB/GRC data is the moat. Treat as announced, not shipped.

## What it does (vendor-stated)

- **AI Passport:** each agent gets a signed credential checked at runtime against its authorized scope; in-scope agents "operate freely". On drift: graduated responses (redirect, restrict, reconnect with context), plus a kill switch said to act "at machine speed". Scoped delegation narrows at each hop; precision revocation; audit trail with "full compliance signatures". For third-party agents it builds a verifiable permissions record rather than trusting the agent's own claims. Framed as prevention ("Shift Zero", "secure by design").
- **Super Intelligence Control Tower:** issues passports and holds the audit record.
- **Governance suite (announced alongside):** shadow-AI detection; 400+ out-of-box connectors that "will enable" AI discovery; access mapping to real entitlements; continuous observability of agent traces; cost governance by user/department/runtime; value intelligence; AI Cost Management in ITAM (frontier-model, embedded-SaaS-AI, hyperscaler and GPU costs, overrun alerts; "will integrate"); Operational Resilience solution for financial institutions (triage/contain/revoke within regulatory incident windows).

## Techniques and hooks

- Signed credentials on unnamed "open specifications"; any IdP, governance product or enforcement point can issue/verify (unverified: specs not named or linked).
- Authority grounded in CMDB, GRC policies and workflow approvals.
- Enforcement at edge/infrastructure, e.g. NVIDIA OpenShell; NVIDIA building a production implementation on the Open Agent Safety Platform (see [[landscape/nvidia-open-agent-safety-platform-2026-09]]).
- Policy enforcement configurable as alert-to-throttle-to-block (future tense).

## Costs and limits

No pricing given. Q4 2026 availability appears only in secondary ledger notes (2026-10-15), not the captured source. No GA date; open-spec interoperability unverified.

## Reception

Vendor and partner quotes only: Jon Sigler (ServiceNow), Itay Ozery (NVIDIA). LTM's CISO says LTM runs 1,500 agents, each with an employee ID and manager, and expects to use the Control Tower as "single system of record" (forward-looking wording). ServiceNow's own 2026 Banking AI Maturity Index: 100% of banks use AI, 24% have matching governance (vendor survey).

## Takeaways

- Parallels Microsoft Agent 365 ([[platforms/microsoft]]), AgentCore Identity ([[landscape/aws-bedrock-agentcore-june-2026]]) and the startup Lyrie ATP ([[startups/lyrie]]); see [[landscape/agent-identity-governance-2026-09]].
- Worth stealing: signed per-agent scope verified per hop; graduated enforcement ladder; binding authority to CMDB/GRC rather than self-declaration; HR-style agent identity (employee ID plus manager).
- Build-vs-buy: buy-leaning for existing ServiceNow customers; portability depends on the unproven open-spec claim. Follow-up: confirm GA date, named specs, which features have shipped.

## Source

- `raw/research/weekly-2026-10-21/01-servicenow-ai-passport.md` — Help Net Security, "ServiceNow gives AI agents a passport, and limits on what they can do", captured 2026-10-21. Vendor-only content; no primary ServiceNow page captured.

## Related

[[landscape/agent-identity-governance-2026-09]] [[landscape/nvidia-open-agent-safety-platform-2026-09]] [[startups/lyrie]] [[platforms/microsoft]] [[landscape/microsoft-build-2026-06]] [[landscape/aws-bedrock-agentcore-june-2026]] [[landscape/snowflake-summit-2026-06]] [[landscape/agent-safety-incidents-2026-08]] [[landscape/mcp-rce-supply-chain-2026-05]] [[landscape/agentic-compute-pricing-2026-04]] [[thesis/agents-eating-saas]] [[landscape/salesforce-agentforce-salesbleed-2026-09]]
