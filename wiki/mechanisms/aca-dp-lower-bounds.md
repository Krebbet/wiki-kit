# ACA Under Differential Privacy: Lower Bounds on Collective Success

Formal characterisation of the trade-off between a firm's differential-privacy (DP) deployment and consumers' ability to exercise Algorithmic Collective Action (ACA). Solanki, Bhange, Aïvodji & Creager 2025 derive lower bounds on collective success as a joint function of collective size α, noise multiplier σ, and clipping threshold C under DP-SGD training. The core finding: DP imposes a structural floor on the critical mass a collective must reach, scaling inversely with the privacy budget. This formalises the "DP-as-firm-weapon" hazard documented qualitatively in [[the-firms-view]] and [[adversarial-data-poisoning]]. A side result — ACA crowds out membership-inference-attack signal, improving empirical privacy even for non-DP models — is the one consumer-favourable reversal the paper surfaces.

## Source

- [Crowding Out The Noise: Algorithmic Collective Action Under Differential Privacy](https://arxiv.org/abs/2505.05707) — Solanki, Bhange, Aïvodji & Creager. arXiv 2505.05707 (cs.LG / cs.CR). v1 May 2025; v2 May 2026. Academic ML/security; intended audience: ACA researchers, privacy-mechanism designers. Also published with DOI [10.1145/3805689.3806475](https://doi.org/10.1145/3805689.3806475) (ACM). Trust: **high** — theoretical bounds with multi-dataset empirical validation (MNIST, CIFAR-10, Bank Marketing); reduces to the Hardt et al. 2023 baseline at σ=0 as a sanity-check. No code repository linked from abstract page.

## Setup

The paper inherits Hardt et al. 2023's ACA frame (see [[algorithmic-collective-action]]): a collective of fraction α of training contributors applies a **feature-label strategy** h(x, y) = (g(x), y*), planting a chosen signal g and target label y* into their data. Success S(α) = Pr[f(g(x)) = y*] measures how often the trained classifier assigns the target label to signal-bearing inputs.

The extension: the firm trains with **DP-SGD** (Abadi et al. 2016), adding calibrated Gaussian noise at each gradient step, parameterised by noise multiplier σ and per-sample clipping threshold C. This is the mechanism firms can deploy — publicly as privacy protection, structurally as collective-action suppression.

## Main Theorems

**Theorem 1 (Hardt et al., reproduced).** Without DP, collective success after T steps is lower-bounded by a term proportional to C(α) ∝ α: success grows monotonically with collective size.

**Theorem 2 (new).** Under DP-SGD, the lower bound acquires an additional negative term driven by σ and C:

> S_T(α, σ, C) ≥ −(1 − ηB(α,C))^T ‖θ₀ − θ*‖ − σC · f₁(B, T, η) · f₂(d, δ)

The authors conclude: "the success of the collective is inversely proportional to noise scale σ." Higher privacy (smaller ε, larger σ) strictly raises the critical mass required for effective ACA.

**Clipping threshold C** has competing influences: it enters B(α, C) positively (helping the first term) but linearly amplifies the noise penalty. Net effect on collective success is ambiguous — determined by which influence dominates at a given (α, σ) operating point. This is an open analytical question the paper does not resolve with a closed-form expression.

**Economic analysis (§5).** A stylised model integrates utility and participation costs. Finding: under DP training, the minimum viable collective size rises, and the participation incentive required to recruit each additional member also rises. The two effects compound — DP imposes a *cost-of-coordination* tax, not just a technical barrier.

## Empirical Validation

Tested across three datasets:

| Dataset | Model | Signal g | Key finding |
|---|---|---|---|
| MNIST | ResNet18 (private from scratch) | Pixel patch | Higher privacy requires larger α to approach 100% success |
| CIFAR-10 | ResNet18 (private fine-tuning) | Grid perturbation | Same qualitative pattern |
| Bank Marketing | Feedforward NN, tabular | Feature offset | Same qualitative pattern |

Clipping values C ∈ {1, 5, 10} tested. All three datasets confirm the qualitative prediction of Theorem 2: increasing σ monotonically raises the critical mass needed to achieve a target success level.

## Side Result: ACA Improves Empirical Privacy

A non-obvious consumer-favourable finding (§4.4): coordinated data modification crowds out the per-member signal that membership-inference attacks (MIA) exploit. On CIFAR-10 with a LiRA attack, a collective of α=1% reduces MIA AuC from 81.78% to ~50.23% — effectively random-chance — even without DP. "Collective action during training improves empirical privacy by increasing the robustness to MIA."

*Editorial note:* This is not a strategic reversal that undoes the DP-suppression result. DP still raises the critical-mass threshold. The MIA result means that a collective exercising ACA gets a privacy co-benefit as a side effect — useful for coalition recruitment ("join the collective, protect yourself from the firm's data-mining"), but it does not lower the coordination bar imposed by DP.

## Relationship to Other Sources

**Confirms and formalises the "DP-as-firm-weapon" finding.** [[adversarial-data-poisoning]] already documents this paper's core claim in full — Theorem 2, the CIFAR-10 / MNIST / Bank Marketing empirical results, and the strategic implications. The present page extracts the mechanism in isolation so it can be cross-linked from strategy and DP-substrate pages.

**Relationship to Battiloro et al. 2026 (arXiv 2605.06749).** Battiloro et al. derive statistical lower bounds for M competing collectives without a DP assumption — they vary M and label entropy. Solanki et al. fix M=1 and vary the firm's DP parameters. The two papers are orthogonal: Battiloro extends the multi-collective dimension; Solanki extends the firm-defence dimension. Neither contradicts the other.

**Relationship to [[the-firms-view]] §2.** That page documents DP-as-counter as a structural suppression mechanism with "no tool-level mitigation." Solanki et al. are the primary source for that entry. The MIA side result is the only partial counter — it does not provide a tool-level mitigation for the suppression effect but does provide a recruitment argument.

**Relationship to [[data-disruption-strategy-map]] risk class 6.** That page already flags this paper as confirming the "DP-trained pricing as ACA-suppression" risk with no tool-level mitigation. The political response — pre-emptive naming of DP adoption as ACA-suppression before firms adopt it under privacy-protective branding — is documented there as a Tier 3 long-game lever.

## Code

No code repository linked from the arXiv abstract page (v1 or v2). The paper is classified cs.LG / cs.CR. No Hugging Face, GitHub, or DagsHub links surfaced.

## Strategic Implications

*(editorial / synthesis — the captured source does not explicitly target consumer pricing)*

1. **Critical-mass estimates from the non-DP literature must be revised upward when the target firm deploys DP-SGD.** Solanki et al.'s empirical 1–10% collective size figures (already captured in [[data-disruption-strategy-map]]) apply to σ=0 or low-σ regimes. A firm deploying strict DP (small ε) shifts the required collective fraction upward by an amount determined by the noise penalty term in Theorem 2. The exact multiplier is dataset-dependent and not given as a closed-form expression.

2. **DP deployment is detectable, not just speculated.** If a firm announces DP-SGD adoption under privacy-regulation framing, this paper's Theorem 2 provides grounds to assert publicly that the adoption simultaneously suppresses ACA. This is the "pre-emptive naming" move in [[data-disruption-strategy-map]] Tier 3, item 6.

3. **Clipping threshold C is an adversarial parameter, not a neutral hyperparameter.** Firms can tune C to maximise the noise penalty on collectives while maintaining acceptable model accuracy. C is not directly observable by consumers. This creates an information-asymmetry problem: consumers cannot independently verify the operating ε or C without model auditing — see [[transparency-tools]] and [[dsar-and-data-deletion]] for the disclosure leverage that might surface it.

4. **The MIA side result supports coalition recruitment framing.** Participants in an ACA collective get empirical privacy protection as a co-benefit (MIA AuC → 50%). This is a valid recruitment argument that does not require claiming ACA will succeed against DP — it claims ACA protects participants regardless.

5. **Tier placement unchanged.** The feature-label ACA tool (Tier 2, item 5 in [[data-disruption-strategy-map]]) remains Tier 2. DP deployment by a target firm would further delay or block that tool's effectiveness. Firm DP adoption is a condition to monitor for each target platform before committing to a Tier 2 build.

## Related

- [[algorithmic-collective-action]] — foundational ACA frame (Hardt et al. 2023, Baumann 2024, Karan et al. 2025, Battiloro et al. 2026); this page documents the DP-suppression extension
- [[adversarial-data-poisoning]] — primary anchor for this paper; full theorem statements, empirical tables, and strategic synthesis already there
- [[the-firms-view]] — DP-as-ACA-suppression documented as firm-side defensive primitive (§2); no tool-level consumer mitigation
- [[data-disruption-strategy-map]] — risk class 6 (DP-trained pricing); Tier 3 political framing lever; Tier 2 ACA tool caveated on DP adoption
- [[federated-learning]] — DP-SGD is a federated learning substrate; Byzantine-robust aggregation compounds the suppression effect (dual-filter hazard)
- [[obfuscation]] — collective obfuscation under DP: the noise crowding-out effect is what Solanki et al. exploit; DP attenuates it
- [[collective-bargaining-for-data]] — collective action framing; participation-cost economics from §5 connects to coalition-formation theory
