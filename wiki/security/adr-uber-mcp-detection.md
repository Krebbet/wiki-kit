# ADR: Uber's Agentic Detection and Response System for MCP Security

ADR (Agentic Detection and Response) is a production-deployed enterprise security framework from Uber (MIT + Uber + Oxford; MLSys 2026 Industry Track) that addresses the MCP-native threat surface created by IDE agents such as Cursor, Cline, and Claude Code. It pairs a lightweight endpoint sensor that reconstructs full causal chains from local SQLite/JSONL caches with a two-tier LLM detection pipeline and an offline evolutionary red-teaming engine. Deployed across 7,200+ corporate endpoints for 10+ months, ADR has surfaced hundreds of credential exposures across 26 categories; a subsequent prevention-hook layer achieved 97.2% precision on confirmed positives. The paper also introduces ADR-Bench, a 302-task author-constructed benchmark where ADR reports F1=0.800 / precision=1.000 versus three baselines at F1=0.178–0.366 — figures that are collect-but-confirm pending independent replication. This is the wiki's first entry covering agent-security and runtime detection, and directly closes the observability and audit-trail gap named across the MCP infrastructure and harness-design pages.

---

## Threat Model: MCP-Native Attacks

ADR's threat model is explicitly MCP-native, not a reframing of classic prompt injection. The attack surface it targets includes:

- **Indirect prompt injection (Agent Flayer pattern)**: malicious content in enterprise data (e.g., a Jira ticket) routes through an MCP connector into the agent's reasoning, causing credential exfiltration via an HTTP tool call. Multi-stage, crosses tool boundaries.
- **Tool shadowing**: a malicious MCP server registers a tool with the same name as a legitimate one; the agent invokes the shadow silently.
- **Tool rug pull**: a trusted MCP server's tool behavior changes after the agent has already established trust in it.
- **Control-flow hijacking**: injected instructions alter the agent's action sequence mid-task.
- **Code interpreter abuse**, **supply chain compromise**, **malicious agent collusion**, **semantic data poisoning**, **long-term goal hijacking**.

The ADR threat framework organizes these into five tactics and 17 techniques — broader coverage than the 3–6 techniques in prior benchmarks.

---

## System Architecture

### ADR Sensor (Endpoint Agent)

A lightweight process running **hourly on each endpoint at 0.182s average per run**. Rather than intercepting at the MCP gateway layer, it parses the **local SQLite and JSONL caches** written by Cursor, Cline, and Claude Code to reconstruct the full causal chain: user prompt → agent reasoning → MCP tool calls → environmental context. This design choice is deliberate: MCP gateway interception would miss reasoning traces and environmental context, and is incompatible with streaming transports. Telemetry is forwarded to the backend over TLS with 13-month retention; least-privilege access and a legal/privacy/risk review are documented in the paper.

### ADR Detector (Two-Tier Online Pipeline)

**Tier 1 — fast triage (GPT-4o):** High-recall flagging of suspicious signals. Routes 40.7% of tasks at $0.017/task / 2.3s latency without escalation.

**Tier 2 — deep reasoning (Claude Sonnet 4):** Applied to escalated sessions. Uses three MCP context providers: source-code inspection, threat-intelligence lookup (curated repository tagged `[EAS]` or `[CURATED]`), and policy verification. Average $0.029/task / 29.7s.

Overall average: **$0.024/task** versus LlamaFirewall's $0.459/task — roughly a 19× cost reduction. Ablation shows that removing Tier 1 raises ADR-Bench recall (0.667→0.805) and F1 (0.800→0.868) but adds 2 false positives, 29% higher cost, and 52% higher latency — the two-tier tradeoff is deliberate precision-first tuning for enterprise audit.

### ADR Explorer (Offline Evolutionary Red-Teaming)

Three sub-agents — Red-Teaming Agent, Eval Agent, Threat Intelligence Agent — running an evolutionary loop with fitness function **F = ε × σ × τ^α** (α=1.2), where ε is execution depth, σ is semantic naturalness, and τ is impact. Convergence is guaranteed by the constraint **ρ × µ < 1.0** on expansion rate and acceptance probability. Explorer is used pre-deployment and continuously to discover novel attack variants; the Threat Intelligence Agent feeds findings back into the curated repo consumed by Tier 2.

### Prevention Hooks

Distinct from detection: pre-prompt hooks implemented inside Cursor and Claude Code using **regex + entropy thresholds** to block known credential patterns before they leave the endpoint. These are not the detection system — they handle static credential patterns and fail for attacks requiring causal reasoning. They operate as a shift-left complement to the detection pipeline.

---

## Production Deployment at Uber

**Authority note:** The production deployment description below is primary source evidence from the Uber security team, published in an industry-track venue (MLSys 2026). It carries substantially higher credibility than the ADR-Bench benchmark figures in the next section.

| Dimension | Value |
|---|---|
| Duration | 10+ months in 2025 |
| Endpoints | 7,200+ unique corporate MacBooks (Intel + ARM) |
| Daily sessions | 10,000+ agent sessions |
| Credential exposures | Hundreds across 26 categories, inadvertently shared outside the enterprise network |
| Prevention-layer precision | 97.2% on 206 true positives / 6 FPs across 212 unique credentials from hundreds of thousands of MCP sessions |

**Production review queue breakdown (Tier-2-escalated sessions):**
- 34% true positives — mostly credential exposures
- 17% true-positive-non-malicious — Uber offensive-security / pentest teams
- 49% false positives — largely complex multi-file codebase sessions escalated conservatively

The 49% FP label rate applies only to the Tier-2-escalated review queue, not the full session stream. The paper explicitly identifies these as "hard-benign" conservative escalations on complex but legitimate sessions — an intentional precision/recall operating point choice, not a system failure. This is separate from the ADR-Bench zero-FP claim (different measurement regime; see below).

Threat emulation exercises validated the end-to-end pipeline: an internal CTF (shell tool injection → malicious `curl|python3` detected by correlating LLM reasoning logs with MCP telemetry) and an Agent Flayer emulation (multi-stage prompt injection traced across tool boundaries).

---

## ADR-Bench (Collect-but-Confirm)

**Authority note:** ADR-Bench was constructed by the ADR authors, and all baseline comparisons were run by the ADR authors using official open-source releases on the same hardware. Absolute F1 figures and the claimed 2–4× advantage over baselines should be treated as **collect-but-confirm** pending independent replication on this benchmark.

| System | Precision | Recall | F1 | False Positives |
|---|---|---|---|---|
| **ADR** | **1.000** | **0.667** | **0.800** | **0** |
| ALRPHFS | 0.400 | 0.333 | 0.366 | 34 |
| GuardAgent | 0.500 | 0.143 | 0.222 | 30 |
| LlamaFirewall | 0.250 | 0.119 | 0.178 | 40 |

On AgentDojo (93 tasks, 38 malicious — a public benchmark, not author-constructed): ADR detects all 38 attacks with 3 false alarms (F1=0.962); ALRPHFS F1=0.877, GuardAgent F1=0.740, LlamaFirewall F1=0.771. The public-benchmark results are stronger evidence than ADR-Bench.

**ADR-Bench design:** 302 tasks (42 malicious = 13.9%, 260 benign = 86.1%); 133 MCP servers across 14 categories; 729 distinct tools; average 28.5 MCP tool calls per task. Attack coverage: 5 tactics, 17 techniques. Malicious tasks sourced from Uber SOC telemetry and red-team intel (enterprise identifiers replaced with stand-ins). Enterprise policy store in YAML, accessible via MCP endpoint; publicly released with runnable MCP registry.

**Tactic-level detection on ADR-Bench (precision-first operating point):**
- Initial Access & Execution: 68% (13/19)
- Permission Abuse: 20% (1/5) — lowest coverage, active gap
- Security Control Bypass: 100% (5/5)
- Reasoning & Data Manipulation: 56% (5/9)
- Operational Impact: 100% (4/4)

Source-code MCP removal is the highest-impact ablation (recall −14%, F1 −15.5%), confirming that source-context is load-bearing for the deep-reasoning path.

---

## Implications for the Wiki's Existing Coverage

**Audit gap (see [[deployments/mcp-infrastructure]], [[patterns/harness-design-space]]):** The [[deployments/mcp-infrastructure]] page names the lack of audit trails as a governance gap in MCP deployments; [[patterns/harness-design-space]] quantifies the 40%-no-audit figure. ADR Sensor's causal-chain telemetry is a concrete, production-validated answer to that gap. The sensor architecture — reading local caches rather than intercepting at the gateway — is a practical deployment pattern any enterprise running Cursor or Claude Code could replicate.

**Vendor governance-plane peer ([[deployments/microsoft-agent-365]]):** Microsoft Agent 365 provides identity-per-agent (Entra), Defender runtime blocking, and MCP server inventory from the platform/vendor side. ADR is an endpoint-sensor + LLM-detection alternative from a single large enterprise's security team. These are complementary positions on the same governance problem.

**Production scale peer ([[deployments/cognition-cloud-agents]]):** Both are large-scale production enterprise deployments — Cognition addresses async/state/infrastructure; ADR adds the security/detection layer.

**ADLC instantiation ([[patterns/agent-development-lifecycle]]):** ADR Explorer + pre-deployment regression on ADR-Bench is a concrete implementation of the ADLC's Test phase; the prevention hooks are a shift-left within the Monitor phase.

**Safety dimension data point ([[patterns/harness-design-space]]):** ADR-Bench provides empirical data on the "safety" design dimension. The precision-first Tier-1/Tier-2 split is a concrete answer to the audit-gap operating point question the harness-design-space page raises.

---

## Source

- Raw capture: `raw/research/weekly-2026-05-25/04-adr-agentic-detection.md`
- arXiv: [2605.17380](https://arxiv.org/abs/2605.17380) — Chenning Li et al. (MIT + Uber Technologies + University of Oxford)
- Code + ADR-Bench: [github.com/uber/ADR](https://github.com/uber/ADR)
- Venue: MLSys 2026 Industry Track

---

## Related

- [[deployments/mcp-infrastructure]] — ADR Sensor is a concrete detection/audit substrate for the observability and governance gap this page names; causal-chain telemetry closes the EDR blind spot in MCP deployments
- [[deployments/microsoft-agent-365]] — vendor governance-plane peer: Entra identity + Defender runtime blocking vs. ADR endpoint sensor + LLM detection
- [[patterns/harness-design-space]] — ADR-Bench provides empirical data for the "safety" design dimension; Tier-1/Tier-2 split is a concrete answer to the 40%-no-audit gap
- [[deployments/cognition-cloud-agents]] — production scale peer; Cognition = async/state/infra, ADR = security/detection layer
- [[patterns/agent-development-lifecycle]] — ADR Explorer instantiates the Test phase; prevention hooks instantiate shift-left within Monitor
