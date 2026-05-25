# Agent-Mediated Negotiation — Empirical Evidence

Mechanism page documenting **what LLM agents can actually do in multi-agent negotiation settings** — the empirical reality check for the agent-mediated coordination programme on [[clawnet-readout]] and [[decentralized-agent-identity]]. ClawNet and DID/VC architectures specify identity, governance, and trust primitives, but neither tests whether the actual *negotiation behaviour* of LLM agents holds up under cooperative, competitive, and adversarial conditions. This page anchors on two benchmark studies: Liu, Gu & Song 2026 *AgenticPay* (buyer-seller negotiation) and Abdelnabi et al. 2024 *LLM-Stakeholders Interactive Negotiation* (multi-stakeholder cooperative + competitive + adversarial). Both qualify the optimism in [[clawnet-readout]] in specific, well-defined ways.

## What the two benchmarks measure

| | AgenticPay (Liu, Gu & Song 2026) | LLM-Deliberation (Abdelnabi et al. 2024) |
|---|---|---|
| **arXiv** | 2602.06008 | 2309.17234 |
| **Venue** | arXiv preprint (2026) | NeurIPS 2024 Datasets & Benchmarks |
| **Setting** | Buyer–seller negotiation, multi-product, many-to-many markets | Multi-stakeholder negotiation games (cooperative + competitive + adversarial / "malicious" conditions) |
| **Tasks** | 111 (31 basic + 80 realistic across 10 business scenarios in 4 economic domains) | Multi-stakeholder testbeds with explicit cooperation/competition/maliciousness operationalisation |
| **Agents** | Buyers + sellers with private constraints + product-dependent valuations; multi-round natural-language bargaining | Multiple stakeholders with assigned positions; multi-issue negotiation |
| **Models** | Claude Opus 4.5, GPT-5.2, Gemini-3-Flash, Qwen3-14B, Llama-3.1-8B | GPT-3.5, GPT-4 (and others) |
| **Evaluation** | GlobalScore = D·deal + W·welfare + E·efficiency − F·failure penalty | Agreement rate, payoff achievement, manipulation susceptibility |

## Headline empirical findings

### AgenticPay — frontier capability + universal buyer disadvantage

| Model | GlobalScore | Deal rate | Avg rounds | Notes |
|---|---|---|---|---|
| Claude Opus 4.5 | **86.9** (highest) | 100% | 3.7 | Zero timeouts, zero overflow |
| GPT-5.2 | 81.7 | 100% | ~3.8 | Frontier-tier |
| Gemini-3-Flash | 82.2 | ~100% | ~3.8 | Frontier-tier |
| Qwen3-14B | 63.9 | 79.3% | ~10 | 20.7% timeout |
| Llama-3.1-8B | 32.5 | 51.4% | 15.0 | 48.6% timeout, 10.8% overflow |

**Three load-bearing findings.**

1. **Frontier proprietary models negotiate competently.** Claude / GPT / Gemini achieve 100% deal rates with rapid convergence (3.7–3.8 rounds).
2. **Open-weight models fail at the "last mile."** >40% of Qwen / Llama failures occurred when price gap was *<$5*. Agents could find the bargaining zone but could not execute final concessions. Material implication for ClawNet-style deployments depending on open-weight models for privacy / decentralisation.
3. **Universal buyer disadvantage at the frontier.** All models showed 20–40+ point gaps favouring SellerScores over BuyerScores. Claude Opus: SellerScore 76.1 vs BuyerScore 63.5. GPT-5.2: 81.1 vs 58.5. The paper notes "persuasive selling content predominates over strategic purchasing guidance" in training data.

**Domain brittleness.** Financial Asset negotiations exposed all models' weakness in reasoning about risk; Gemini-3-Flash dropped 20.2 points (88.3 → 68.1) from Professional Services to Financial Assets.

**Personality effects.** Buyer personality significantly impacts outcomes — "Busy Professional" buyer scores ranged 65.9–92.7 depending on seller personality.

### LLM-Deliberation — adversarial collapse

| Condition | Success rate (GPT-4) |
|---|---|
| Cooperative negotiation | **81%** |
| One greedy adversarial agent introduced | **27%** |

**Three load-bearing findings.**

1. **LLMs cooperate well; collapse under adversarial pressure.** A single greedy agent drops cooperative success from 81% → 27%. Targeted adversarial attacks isolate agents and force unfavourable outcomes.
2. **Score leakage is significant.** GPT-3.5: 25% leakage. Theory-of-mind reasoning capacity gaps: GPT-3.5 ~42%, GPT-4 ~61%. Agents leak strategy and are vulnerable to deception.
3. **Heterogeneity is a liability.** Mixed-population experiments (GPT-3.5 + GPT-4) show weak agents drag down strong ones. **Consumer coalitions with heterogeneous models are worse off than if all members had GPT-4.** Directly undermines naive scalability assumptions.

## How this qualifies [[clawnet-readout]]

The wiki's [[clawnet-readout]] is optimistic about agent-mediated coordination as a substrate for several lever clusters (DSAR coordination, demand-strike commitment, group-buy, CBI bargaining). The two benchmarks qualify that optimism in specific, well-defined ways:

1. **Frontier capability is real but proprietary.** Claude Opus / GPT-5 work; Llama / Qwen do not (yet). Privacy- or decentralisation-motivated deployments insisting on open-weight models will face the open-weight failure modes documented here. Cooperative deployments using a frontier model concentrate vendor dependency.

2. **Buyer disadvantage is structural.** Even at the frontier, LLMs systematically advantage sellers in price negotiation. **Consumer-counter-power deployments using off-the-shelf agents will inherit this bias and amplify the very asymmetry the wiki's mandate is to combat.** This is a critical caveat for ClawNet-style buyer-side coordination. Mitigation candidates:
   - Domain-specific fine-tuning toward buyer-favourable strategies.
   - Human-in-the-loop oversight for buyer-side concessions.
   - Asymmetric agent design: stronger negotiation-strength budget for buyer agents.

3. **Adversarial collapse threatens consumer-firm negotiation.** Consumer-firm negotiation is *inherently* adversarial — firms are profit-maximising counterparts, not cooperative partners. The Abdelnabi 81%→27% collapse under one greedy agent is the scenario that maps directly onto consumer-counter-power use cases. Mitigations:
   - **Cryptographic commitments** binding agents to disclosed strategies.
   - **Formal verification** of negotiation constraints.
   - **Shift away from strategic negotiation** toward information aggregation (DSAR coordination, probe-and-publish) where the adversarial dynamic doesn't directly bite.
   - **Regulatory substrate** constraining firm behaviour (less realistic in current US/EU enforcement landscape — see [[buyer-cartels-antitrust]] caveats).

4. **Heterogeneity penalty constrains coalitional design.** A consumer cooperative whose members run different LLMs faces the heterogeneity penalty — weak-model members reduce coalition outcomes for strong-model members. Either standardise on one frontier model (vendor lock-in) or absorb the penalty.

5. **Long-horizon strategic reasoning remains the frontier constraint.** Both papers explicitly identify multi-round strategic reasoning as the open capability gap. ClawNet's bilateral-approval-at-every-initiation pattern is structurally aligned with shorter horizons (each session re-bounded), which mitigates this gap somewhat — but extended consumer-firm negotiations are exactly the use case that suffers most.

## Caveats specific to the benchmarks

- **Both benchmarks are synthetic.** Real consumer-firm negotiations involve longer institutional relationships, reputation signalling, and repeated interactions. Outcomes in repeated games may differ from one-shot evaluation here.
- **AgenticPay frontier-model results dated 2026.** Capability evolves rapidly; results may change with model generation.
- **Abdelnabi 2024 model selection is older (GPT-3.5 / GPT-4 era)**; contemporary frontier models likely perform better but the *relative* adversarial-collapse pattern may persist.

## How this maps onto the wiki

| Wiki anchor | What this page qualifies |
|---|---|
| [[clawnet-readout]] | Adds empirical capability evidence; sharpens the readout's optimism with the buyer-disadvantage + adversarial-collapse + heterogeneity-penalty caveats. |
| [[decentralized-agent-identity]] | Same caveats apply to DID/VC-architected deployments — the negotiation behaviour is independent of the identity substrate. |
| [[agent-interop-protocols]] | A2A transport assumes negotiation behaviour is the agents' problem — these benchmarks tell you what behaviour actually obtains. |
| [[possible-strategic-levers\|Lever #1, #4, #14, #16, #26]] | The wiki's strategy-layer levers that depend on agent-mediated coordination inherit the capability + bias profile documented here. |
| [[data-disruption-strategy-map\|Tier 1 #1 (DSAR coordination)]] | Notably, DSAR coordination is **structurally not a negotiation** — it is information aggregation. The benchmarks here suggest DSAR coordination is a *better* fit for current LLM agent capability than direct buyer-seller bargaining. |

## Source

- Liu, Gu & Song. 2026. *AgenticPay: A Multi-Agent LLM Negotiation System for Buyer–Seller Transactions*. arXiv 2602.06008. UC Berkeley (SafeRL-Lab). Captured: `raw/research/clawnet-adjacent-methods/19-agenticpay-2026.md` + `08-agenticpay-2026-abs.md`. Trust tag: arXiv preprint, comprehensive benchmark with 111 tasks across 10 scenarios, 5 frontier + open-weight models tested.
- Abdelnabi, Gomaa, Sivaprasad, Schönherr & Fritz. 2024. *Cooperation, Competition, and Maliciousness: LLM-Stakeholders Interactive Negotiation*. NeurIPS 2024 Datasets & Benchmarks Track. arXiv 2309.17234. Captured: `raw/research/clawnet-adjacent-methods/22-llm-deliberation-abdelnabi.md` + `09-llm-deliberation-abdelnabi-abs.md`. Trust tag: peer-reviewed NeurIPS, multi-stakeholder benchmark with explicit adversarial conditions.

## Related

- [[clawnet-readout]] — primary partner; the substrate this page provides empirical reality checks for
- [[decentralized-agent-identity]] — alternative architecture; same negotiation-behaviour caveats apply
- [[agent-interop-protocols]] — transport substrate (orthogonal layer)
- [[data-disruption-strategy-map]] — Tier 1 #1 (DSAR coordination) is structurally a better fit for current LLM agent capability than negotiation
- [[possible-strategic-levers]] — strategy-layer levers depending on agent-mediated coordination inherit the capability + bias profile documented here
- [[the-firms-view]] — none directly; firm-side framing of agent negotiation would emphasise the seller-favouring bias as a feature, not a bug
