# The Firm's View

Documentary anchor for **firm-side perspectives** on the same technical primitives the wiki documents as legitimate consumer counter-power. Where pages like [[adversarial-data-poisoning]], [[algorithmic-collective-action]], [[obfuscation]], and [[strategic-classification]] frame coordinated data-modification, profile-manipulation, and feature-spoofing as legitimate counter-power for users facing personalised pricing / surveillance / algorithmic targeting, this page collects the **opposite framing**: the firm's perspective in which the same actions are characterised as attacks, threats, or gaming to be defended against. Same technical primitives, opposite normative frames. Pages link bidirectionally so the reader can move between framings without losing source-traceability.

## Why this page exists

The wiki's mandate is collective consumer counter-power — its centre of gravity sits with the consumer / collective. But documenting only the consumer-favouring framing leaves the wiki blind to (a) the literature firms actually cite when defending pricing / personalisation systems, (b) the technical mitigations firms actually deploy, and (c) the second-order harms from firm responses that fall on uncoordinated populations. The "firm's view" is not endorsed here — it is documented so consumer-side strategy is informed by what firms can and will do in response.

Each entry below names: the technical primitive, the consumer-side framing (with wiki cross-link), the firm-side framing, the load-bearing source, and the implication for consumer-side strategy.

---

## 1. Coordinated data-modification — "poisoning" framing

**Technical primitive:** a coordinated subset of users jointly modifies their data inputs to shift a deployed ML model's behaviour. See [[algorithmic-collective-action]] for the consumer-side framing as legitimate collective action.

**Firm-side framing:** "data poisoning attack" / "shilling attack" / "adversarial perturbation". The collective is treated as a malicious actor; the firm is the victim. Defensive design objective: detect and filter manipulated contributions, retrain robustly, deploy detection pipelines.

**Load-bearing source:** Wang, Wu, He, Liu, Shi & Wang. 2024. *Poisoning Attacks Against Recommender Systems: A Survey*. arXiv 2401.01527. Three-dimension taxonomy of recommender-system poisoning attacks (Component-Specific, Goal-Driven, Capability-Probing). Currently anchored on [[adversarial-data-poisoning]].

**Implication for consumer-side strategy:** every ACA-style lever (#9, #10, levers documented on [[possible-strategic-levers]]) faces (a) a research literature that supplies firms with attack-detection signatures and (b) a body of legal precedent treating data manipulation as wrongful where there is detection.

## 2. Differential privacy as ACA suppression

**Technical primitive:** training the deployed model under differential-privacy guarantees adds calibrated noise that simultaneously protects individual privacy *and* suppresses coordinated-collective influence on the model.

**Firm-side framing:** "privacy protection" — publicly framed as consumer-protective, structurally functions as collective-action suppression. Solanki et al. 2025 prove the ACA success threshold scales inversely with DP noise scale ε; the firm controls ε.

**Load-bearing source:** Solanki, Mendler-Dünner & Hardt. 2025. *Algorithmic Collective Action under Differential Privacy*. arXiv 2505.05707. Currently anchored on [[adversarial-data-poisoning]] §"DP as firm counter".

**Implication for consumer-side strategy:** flagged on [[data-disruption-strategy-map|risk class 6]] as having **no tool-level mitigation**. The political response is naming "DP-trained pricing as ACA suppression" before firms adopt it under privacy-protective branding (per [[obfuscation-strategic-readout]] open question). Once a firm adopts ε-LDP training publicly, the entire single-collective ACA portfolio is suppressed regardless of consumer-side coordination.

## 3. Robust pricing under strategic buyer manipulation

**Technical primitive:** consumers manipulate context features to obtain lower prices from a contextual-bandit pricing system. See [[obfuscation]], levers #6 / #7 / #11 on [[possible-strategic-levers]] for the consumer-side framing.

**Firm-side framing:** "strategic buyers" gaming the pricing function. The seller's design objective is regret minimisation despite manipulation. Naive contextual pricing achieves linear regret Ω(T) — useless. A two-phase **explore-then-exploit** structure recovers Õ(√T) regret: Phase 1 uses uniform pricing (price independent of features → zero manipulation incentive → honest revelation), Phase 2 uses the inferred buyer-equilibrium manipulation rule x_t = x_t⁰ − A⁻¹β₀g'(·) to back out true features and price accordingly.

**Load-bearing source:** *Contextual Dynamic Pricing with Strategic Buyers*. arXiv 2307.04055. Captured: `raw/research/clawnet-adjacent-methods/18-contextual-pricing-strategic-buyers.md`.

**Implication for consumer-side strategy.** Critical caveat for [[obfuscation-strategic-readout]] and [[pricing-algorithm-taxonomy]]:
- Obfuscation **is** effective against naive (non-strategic) contextual pricing — Theorem 1 is the proof.
- Against **adaptive sellers with multi-phase learning + repeat-buyer data**, effectiveness degrades. The seller can infer the manipulation structure and recover sublinear regret. The cost-structure parameter (smallest eigenvalue of the manipulation-cost matrix A) determines the regret penalty, not whether learning succeeds.
- Practical consequence: an obfuscation tool's effectiveness window depends on the seller's adaptive-learning sophistication, not just the strength of the obfuscation itself.

## 4. Strategic-robust classification with disparate-impact externality

**Technical primitive:** when individuals manipulate features to obtain favourable classification (loans, hiring, pricing tier), the firm tightens its decision threshold to recover accuracy. See [[strategic-classification]] for the foundational framework (Hardt et al. 2016).

**Firm-side framing:** "robust classification" — the firm raises threshold τ in response to gaming, achieving Stackelberg-optimal accuracy.

**Counter to the firm-side framing — Milli et al. 2019 social-cost result:** *The Social Cost of Strategic Classification* (FAccT 2019; arXiv 1808.08460; captured: `raw/research/clawnet-adjacent-methods/17-social-cost-strategic-classification.md`). Three load-bearing theorems:
- **Theorem 3.1.** Institutional utility and social burden are *coupled*: any increase in firm accuracy beyond the non-strategic optimum strictly increases the expected cost B₊(τ) that *positive* (deserving) individuals must incur to be correctly classified.
- **Theorem 4.1.** When disadvantaged groups have lower outcome likelihoods conditional on being truly positive (e.g., creditworthy Black borrowers having lower FICO scores than creditworthy white borrowers on average), the social *gap* between groups grows monotonically with the threshold.
- **Theorem 4.2.** Even with identical feature distributions, if disadvantaged groups face higher manipulation costs (wealth, information access, structural barriers), the social gap widens as thresholds rise.

**Empirical anchor:** FICO credit data (n = 301,536). With cost ratio κ = β / α = 2, threshold increase from 60 → 70 multiplies the Black-white gap by ~2.5; κ = 3 gives ~4×.

**Implication for consumer-side strategy** (this is the specific reason this counter-perspective matters to the wiki's mandate):

> Obfuscation-without-collective-leverage is a trap for disadvantaged groups.
>
> Individual-level strategic manipulation works for the wealthy, who can absorb the cost of manipulation. When firms respond by tightening thresholds, the manipulation cost rises for everyone — and the *increment* falls hardest on those least able to pay. Aggregate consumer-side gaming therefore creates a **regressive equity externality** unless the lever is paired with collective constraint on firm response (regulation, antitrust, structural reform).

This implication is **flagged on [[obfuscation-strategic-readout]] §Disparate-Impact Externality** as a strategy-layer caveat for the obfuscation lever cluster. It does not invalidate the lever — it bounds the conditions under which the lever is durable.

## 5. Federated-learning defences against poisoning

**Technical primitive:** federated learning + secure aggregation lets a firm aggregate model updates from many users without seeing individual data. See [[federated-learning]] for the consumer-favouring framing as substrate technology for [[data-cooperatives]].

**Firm-side framing:** the same architecture also deploys *Byzantine-robust aggregation* (Krum, Trimmed Mean, Median, FoolsGold) and *anomaly detection* on individual gradient contributions. Defends against single-collective poisoning at the cost of also degrading legitimate minority-group contributions.

**Load-bearing source:** the FL survey (Rahman 2025, captured: `raw/research/clawnet-adjacent-methods/26-fl-survey-2025.md`) catalogues both the privacy-preserving framing and the Byzantine-robustness defensive framing. Foundational primary sources: Blanchard et al. 2017 (Krum), Bonawitz et al. 2017 (secure aggregation), Abadi et al. 2016 (DP-SGD).

**Implication for consumer-side strategy:** if a firm deploys FL with Byzantine-robust aggregation, ACA-style strategies face dual filtering — both the DP noise (per §2 above) and the robust-aggregation outlier filtering. The federated substrate is dual-use — it can power consumer data cooperatives *and* firm-side defences, depending on who runs the orchestrator.

## 6. Adversarial-training inoculation against tool signatures

**Technical primitive:** firm trains its model against known signatures of consumer-side counter-tools (obfuscation extensions, fingerprint rotators, ad-click obfuscators). See [[obfuscation-strategic-readout]] and [[data-disruption-strategy-map|risk class 5]] for the consumer-side framing.

**Firm-side framing:** ML-engineering response — once a tool's signature is known, the model is fine-tuned to filter it. No legal action; pure ML-engineering arms race. Documented precedent: ad-click obfuscation tool signatures leveraged by ad networks against [[adnauseam|AdNauseam]]; review-authenticity model signatures used by Amazon against [[fakespot|Fakespot]]-class tools.

**Load-bearing source:** consumer-side documentation on [[obfuscation-strategic-readout]] + the AdNauseam Chrome Web Store ban precedent on [[adnauseam]].

**Implication for consumer-side strategy:** any single-vendor tool concentrates signature risk. Federation, signature rotation, multi-tool ecosystem, and open-source distribution are mitigations (per [[data-disruption-strategy-map|risk class 5 catalogue]]).

---

## How to use this page

When evaluating a strategy-layer lever:
1. Find the consumer-side wiki page documenting the lever (e.g., [[obfuscation]], [[algorithmic-collective-action]]).
2. Read its corresponding section here for the firm-side framing.
3. Check whether the firm-side framing surfaces a defence the consumer-side strategy must account for (DP, robust aggregation, adaptive pricing, threshold-tightening).
4. Check whether it surfaces a *second-order harm* (e.g., disparate-impact externality from threshold-tightening) the consumer-side strategy is responsible for not amplifying.

## Source

This page synthesises across multiple captured sources, each anchored on its primary wiki page:

- **§1 Poisoning framing** — Wang et al. 2024 attack taxonomy. Anchored on [[adversarial-data-poisoning]].
- **§2 DP-as-counter** — Solanki, Mendler-Dünner & Hardt 2025. Anchored on [[adversarial-data-poisoning]].
- **§3 Robust pricing under strategic buyers** — Contextual Dynamic Pricing with Strategic Buyers, arXiv 2307.04055. Captured: `raw/research/clawnet-adjacent-methods/18-contextual-pricing-strategic-buyers.md`.
- **§4 Disparate-impact externality** — Milli, Miller, Dragan & Hardt 2019 (FAccT '19; arXiv 1808.08460). Captured: `raw/research/clawnet-adjacent-methods/17-social-cost-strategic-classification.md`.
- **§5 FL defences** — Rahman 2025 FL survey, arXiv 2504.17703 (anchored on [[federated-learning]]).
- **§6 Adversarial-training inoculation** — wiki-internal synthesis from [[obfuscation-strategic-readout]] / [[adnauseam]] / [[fakespot]] precedent.

## Related

- [[adversarial-data-poisoning]] — primary partner page; ACA technical primitives + DP-as-counter
- [[algorithmic-collective-action]] — consumer-side framing of §1, §2 above
- [[strategic-classification]] — consumer-side framing of §3, §4 above
- [[obfuscation]] / [[obfuscation-strategic-readout]] — consumer-side framing of §3, §4, §6
- [[federated-learning]] — substrate page; consumer-side framing of §5
- [[pricing-algorithm-taxonomy]] — pricing-algorithm families targeted by §3
- [[data-disruption-strategy-map]] — risk classes 5 + 6 are the operational expression of §5, §6, §2
