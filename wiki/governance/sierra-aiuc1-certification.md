# Sierra Achieves AIUC-1 Certification

Sierra vendor blog post (2026-09-17) announcing its chat and voice agent platform is independently certified against AIUC-1, a recurring, adversarial-testing-based trust standard for AI agents — the wiki's first documented instance of this certification category, distinct from static compliance frameworks (SOC 2, ISO 27001/42001) and from vendor-internal governance stories like [[governance/anthropic-ai-native-sdlc]] or Microsoft Agent 365's governance plane.

## What was certified, and by whom

Two distinct evaluators reviewed Sierra's platform: AIUC (the Artificial Intelligence Underwriting Company) itself ran adversarial and behavioral testing directly against live Sierra agents, while Schellman — an independent auditor — reviewed Sierra's technical, legal, operational, and governance controls and attested that Sierra met all applicable AIUC-1 requirements. Recertification cadence: technical evaluations recur at least quarterly, with a full audit annually.

## What AIUC-1 covers

Unlike static compliance paperwork, AIUC-1 is pitched as testing how agents *actually behave* — including adversarial manipulation attempts, attempts to exfiltrate protected or sensitive information, attempts to push an agent beyond its authorized scope, and (for voice agents) a range of real-world voice conditions. Sierra positions it as complementary to, not a replacement for, SOC 2 Type II, ISO 27001, and ISO 42001: those validate security/AI-management *systems*, while AIUC-1 adds recurring technical/behavioral testing specific to agent conduct.

## Why Sierra pursued it

Sierra frames its customer base as heavily regulated — claiming over 40% of the Fortune 50, one in three leading banks, and five of the ten largest healthcare companies — doing high-stakes agentic work: patient care coordination, technical troubleshooting, insurance claims resolution, mortgage refinancing. The certification targets enterprise security/risk/compliance/AI-governance buyer teams who need independent validation that the underlying platform is safe, not just that the customer configured their agent correctly. Sierra frames this explicitly as differentiation as "agents move from answering questions to taking meaningful actions."

## Disclosed architecture

Sierra describes a "defense-in-depth" agent lifecycle with layered controls: grounded content plus customer-defined policies shape behavior; "Supervisors" evaluate live conversations in real time and can correct, block, or escalate responses; and deterministic (non-model-judgment) guards enforce hard requirements like authentication and access control. The post gives no deeper technical detail — no architecture diagrams beyond a lifecycle graphic, no test-suite pass-rate metrics, no detail on what AIUC's test suite actually contains.

This is a single short vendor blog post with no independent benchmark numbers — **collect-but-confirm**, per this wiki's source-authority convention for vendor claims without third-party verification.

## Related

- [[patterns/sierra-context-engineering]] — same vendor; this certification layers a trust/audit story on top of the already-documented context-engineering platform.
- [[patterns/sierra-monitor-eval-of-evals]] — Sierra's "Supervisors evaluate conversations in real time" plausibly connects to Sierra's documented Monitor/eval-of-evals product, though this source doesn't confirm they're the same subsystem.
- [[deployments/microsoft-agent-365]] — parallel agent-trust/governance infrastructure from a platform-governance angle (cross-cloud registry, identity-per-agent, runtime blocking) rather than third-party certification.
- [[deployments/mcp-infrastructure]] — parallel but distinct governance vector: protocol-level auth infrastructure (DPoP, Workload Identity Federation) vs. AIUC-1's behavioral/adversarial certification.
- [[governance/org-control-layer]] — OCL's runtime policy-enforcement layer (role/gate/escalate/audit) is conceptually adjacent to Sierra's "Supervisors + deterministic guards," though one is a research architecture and the other a vendor product description.
- [[governance/anthropic-ai-native-sdlc]] / [[governance/claude-code-auto-mode]] — thematically adjacent agent-trust/safety governance, but a different layer (model/harness vendor governance vs. third-party agent-platform certification).

## Source

- `raw/research/weekly-2026-09-20/03-sierra-aiuc1-certification.md` — captured 2026-09-20 from `sierra.ai/blog/sierra-achieves-aiuc-1-certification` (2026-09-17). **Vendor primary.**
