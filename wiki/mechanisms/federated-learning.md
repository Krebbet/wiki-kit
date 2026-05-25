# Federated Learning

Mechanism page for **federated learning (FL)** + **secure aggregation** as the substrate technology for cooperative consumer-data pooling without a trusted central aggregator. FL lets multiple parties (consumers, member-owned cooperatives, federated nodes) collaboratively train a useful model — fair-price detector, price-discrimination auditor, fraud detector — without any single party seeing raw consumer data. The natural alternative substrate to ClawNet's centralised cloud orchestrator (per [[clawnet-readout]] risk #1) and the missing technical layer underneath [[data-cooperatives]]. Anchored on Rahman 2025 *Federated Learning: A Survey on Privacy-Preserving Collaborative Intelligence* (arXiv 2504.17703). **Capture status: secondary survey.** Load-bearing wiki claims should cite the foundational primary work via this survey — see Source section.

## Core mechanism

**Federated Learning lifecycle** (FedAvg, McMahan et al. 2017): (1) server distributes the current global model *w* to a selected subset of *K* clients; (2) each client *k* trains locally for *E* epochs on private data *D_k*, computing updated weights *w_k*; (3) server aggregates via weighted average *w := (1/n) Σ_k n_k w_k* where *n_k* is local data size. **No raw data leaves client devices.** Convergence depends on data heterogeneity, client participation, and aggregation noise.

**Secure aggregation** (Bonawitz et al. 2017): cryptographic protocol where each client secret-shares its gradient across a threshold of peers; the server collects shares and reconstructs only the *sum* of contributions, never any individual update. Eliminates the "trusted aggregator" assumption — no single party sees raw data *or* raw updates. Cost: small cryptographic overhead. Benefit: structural rather than promissory privacy.

## Privacy / threat landscape — survey synthesis

| Mechanism | What it protects against | Cost |
|---|---|---|
| **Differential Privacy (DP-SGD; Abadi et al. 2016)** | Statistical inference about individual training data from released model | Accuracy / utility tradeoff; severe on small or skewed datasets. ε noise scale also doubles as ACA-suppression — see [[the-firms-view\|§2]]. |
| **Secure Aggregation (Bonawitz et al. 2017)** | Server learning individual client updates | Cryptographic overhead; client coordination overhead |
| **Homomorphic Encryption** | Computation on encrypted updates | Computationally intensive; impractical at consumer-scale |
| **Trusted Execution Environments (Intel SGX et al.)** | Hardware-isolated processing | Limited availability; vendor trust required |
| **Byzantine-robust aggregation** (Krum, Trimmed Mean, Median, FoolsGold; Blanchard et al. 2017) | Malicious / poisoned client updates | Also filters legitimate minority-group contributions; see [[the-firms-view\|§5]] for dual-use framing |

**Threat catalogue** documented by the survey:
- **Gradient inversion attacks** (Zhu et al. 2019, "Deep Leakage from Gradients"): deep-learning-based reconstruction of private training data from raw shared gradients. Real, not theoretical. Counter: secure aggregation eliminates raw-gradient exposure.
- **Backdoor attacks**: poisoned client updates inject targeted misclassifications.
- **Data leakage via unprotected gradients**: per-update statistical inference.
- **Model poisoning**: malicious clients degrade global-model performance.

## Two deployment regimes

**Cross-device FL**: millions of unreliable mobile clients, large communication cost, device heterogeneity. Examples: Google Gboard, Apple Siri suggestions.

**Cross-silo FL**: fewer but more powerful institutional clients, emphasis on security and trust. Examples: hospitals (NVIDIA Clara), banks (fraud-detection consortia). **The cross-silo regime is the structural fit for [[data-cooperatives]] and federated [[platform-cooperatives]]**: a federation of regional consumer cooperatives jointly training a price-discrimination detector without any cooperative seeing another's raw member data.

## How this maps onto the wiki

| Wiki anchor | Why FL is substrate-relevant |
|---|---|
| [[data-cooperatives]] | Documents the *organisational form* of consumer data pooling. FL provides the *technical mechanism* that makes pooling trustworthy without a central operator. The OECD-cited [[midata]] coop and the OPAL architecture mentioned on [[data-cooperatives]] are FL-adjacent. |
| [[collective-bargaining-for-data]] | A CBI that bargains on behalf of consumers needs aggregate insight (price-discrimination evidence, model-bias evidence) without exposing per-member data. FL + secure aggregation produces exactly that aggregate. |
| [[clawnet-readout]] | Risk #1 (centralised operator trust) is structurally addressed by FL — shifts the trust assumption from "operator behaves honestly" to "no single party can see raw data even if it tries." Cooperatively-owned ClawNet variant should be FL-substrate'd. |
| [[markup-citizen-browser]] | Citizen Browser's panelist-with-redaction pipeline is conceptually FL-adjacent (per-panelist data minimisation before central analysis). FL formalises the same pattern. |
| [[possible-strategic-levers\|Lever #1 — many-consumer counterbalance]] | Substrate technology underneath the cooperative or CBI implementing the lever. |
| [[the-firms-view\|§5]] | The *firm-side* dual use of the same substrate — Byzantine-robust aggregation as poisoning defence. Consumer-side and firm-side use the same primitives differently. |

## Key tensions / caveats for consumer deployment

1. **Differential privacy is dual-use.** Consumer-favouring framing: protects per-member data. Firm-favouring framing: suppresses [[algorithmic-collective-action|ACA]] (Solanki et al. 2025; ε noise scale inversely proportional to achievable α). A consumer-cooperative FL deployment chooses ε; a firm FL deployment chooses ε too. Same mechanism, different deployment context.
2. **Byzantine-robustness is dual-use.** Consumer-favouring framing: defends against malicious member-cooperative-internal poisoning. Firm-favouring framing: filters out [[algorithmic-collective-action|coordinated minority influence]] including legitimate ACA-style action. See [[the-firms-view|§5]].
3. **Secure aggregation requires client coordination.** Cross-device FL with millions of intermittent clients faces dropout problems; cross-silo FL with stable institutional clients is more straightforward.
4. **Statistical heterogeneity (non-IID) is first-order.** Convergence speed and accuracy suffer without personalisation, clustering, or robust aggregation.
5. **No standardised benchmarks yet** (LEAF, OARF emerging). Limits cross-method comparison.

## Source

**Primary anchor (survey):**
- Rahman. 2025. *Federated Learning: A Survey on Privacy-Preserving Collaborative Intelligence*. arXiv 2504.17703v3. Captured: `raw/research/clawnet-adjacent-methods/26-fl-survey-2025.md` + `07-fl-survey-2025-abs.md`. Trust tag: arXiv preprint, single-author survey, comprehensive coverage of the FL privacy-preservation literature.

**Foundational primary work referenced via the survey** — to cite directly when wiki claims are load-bearing:
- McMahan et al. 2017 — *Communication-Efficient Learning of Deep Networks from Decentralized Data* (AISTATS) — FedAvg architecture.
- Bonawitz et al. 2017 — *Practical Secure Aggregation for Privacy-Preserving Machine Learning* (ACM CCS) — secure aggregation protocol.
- Abadi et al. 2016 — *Deep Learning with Differential Privacy* (ACM CCS) — DP-SGD.
- Zhu et al. 2019 — *Deep Leakage from Gradients* (NeurIPS) — gradient-inversion attack.
- Blanchard et al. 2017 — *Machine Learning with Adversaries: Byzantine Tolerant Gradient Descent* (NeurIPS) — Krum + Byzantine-robust aggregation.

These primary sources are not yet captured in `raw/`. Future research-queue entry: capture foundational FL papers when a development plan needs them as load-bearing citations.

## Related

- [[data-cooperatives]] — primary organisational anchor; FL is the substrate
- [[collective-bargaining-for-data]] — bargaining lane; FL is the aggregation substrate
- [[clawnet-readout]] — FL is a structural mitigation for ClawNet's centralised-operator-trust risk
- [[data-market-mechanism-design]] — Shapley-based revenue distribution sits *above* the FL aggregation layer
- [[decentralized-agent-identity]] — complementary substrate (identity layer; FL is data-sharing layer)
- [[the-firms-view]] — §5 dual-use framing of the same mechanisms
- [[adversarial-data-poisoning]] — Byzantine-robust aggregation is a firm-side defence against ACA-style poisoning
