# Algorithmic Collective Action

Foundational mechanism page for the **Algorithmic Collective Action (ACA)** research programme: the formal study of how a coordinated subset of platform users can shape a deployed ML model by jointly modifying their data. ACA inverts the ML-security framing of "data poisoning" — the same technical primitives are reframed as legitimate counter-power for users facing a learning system that personalises against them. Anchored on Hardt, Mazumdar, Mendler-Dünner & Zrnic 2023 (foundational), Baumann & Mendler-Dünner 2024 (recsys empirical case), and Karan, Karahalios, Vincent & Sundaram 2025 (multi-collective dynamics). The firm-side counter-perspective on the same primitives — attack taxonomies, differential-privacy defences, adaptive-learning recovery, threshold-tightening with disparate impact — is documented separately on [[the-firms-view]].

## What ACA is

A **collective** is a fraction α of a learning system's user population that coordinates by jointly modifying its members' data inputs to shift the deployed model's behaviour toward a collective goal. The firm observes a mixture distribution P = αP* + (1−α)P₀ where P* is the collective's chosen distribution; the collective's *success* S(α) is the fraction of relevant outcomes the deployed model maps to the collective's target. The framework formally treats the collective as a legitimate strategic actor — not an adversary — operating under the same rules as the firm.

The political reframing is load-bearing: where ML security literature treats coordinated data modification as "poisoning" / "shilling" / "adversarial perturbation" (firm = victim), ACA literature treats it as "collective action" / "strike" / "rebalancing" (collective = legitimate stakeholder). Same technical primitives, opposite normative frames. See [[the-firms-view]] for the firm-side framing of the same mechanisms.

## Foundational result — Hardt, Mazumdar, Mendler-Dünner, Zrnic 2023

ICML 2023; arXiv 2302.04262. The paper proves "algorithmic collectives of exceedingly small fractional size can exert significant control over a platform's learning algorithm" and validates this empirically.

**Three settings analysed:**

1. **Classification (Theorem 1, Corollary 2 — feature-label strategy).** Collective of size α succeeds at planting a signal g(x) → y* if α ≥ critical-mass threshold proportional to (1−ϵ)Δ + 2ϵ)ξ / (1 − S* + ((1−ϵ)Δ + 2ϵ)ξ), where ξ = P₀(X*) is signal uniqueness, Δ is the suboptimality gap of y* under P₀, ϵ is classifier suboptimality. **Lower ξ → lower critical mass.**
2. **Feature-only strategy (Theorem 3).** When the collective can only manipulate features, not labels, success is lower-bounded by 1 − (1 − pα)[(1−(1−ϵ)p)ξ] where p = inf P₀(y* | x). Positivity constant p directly degrades achievable success.
3. **Risk minimisation + gradient-based learning (Theorems 7 + 10).** Under strong convexity, success is bounded by a gradient-neutralising condition. Under nonconvexity, an adaptive **gradient-control strategy** can reach any target θ* provided a low-gradient path exists from θ₀ to θ* under P₀.

**"Blessing of dimensionality":** high-dimensional data with many weak signals lowers the collective's threshold — randomising base-distribution labels from 0% → 30% reduces critical mass by ~5×.

**Empirical validation** (Section 5): 30,000 resumes from a freelancer skill-classification platform; 2000+ DistilBERT training runs.
- Strategy 1 (feature-label): >90% success with <0.5% of dataset (~125 modified resumes).
- Strategy 2 (feature-only): ~90% success at 10% of target class.
- Token-placement insensitivity: signal location within the resume is largely irrelevant if the planted token is unique within the corpus.
- Classifier optimality matters: success curve steepens with training depth — the more optimal the classifier, the smaller the required collective.

**Economic framing (§6):** participation is individually irrational without side payments, but past critical mass the collective becomes self-sustaining (S(α) − c > γS(α)). Connects to Olson 1965 collective-action theory — investment targets are pre-critical-mass coordination cost.

## Empirical case study on a deployed system — Baumann & Mendler-Dünner 2024

arXiv 2404.04269. The cleanest empirical demonstration of ACA against a production recommender system: a Deezer transformer model for automatic playlist continuation (APC), trained on the Spotify Million Playlist Dataset (980K train / 20K val / 20K test).

**Mechanism:** collective members own playlists and insert one target song with Levenshtein distance ≤ 1 (single-edit constraint). Two strategies:
- **InClust** — insert the target song immediately before high-frequency anchor songs in the collective's playlists (exploits embedding-space clustering).
- **DirLoF** — insert after low-frequency songs across the training data (exploits long-tail dominance of weak signals).
- **Hybrid** combines both.

**Empirical results:**
- **0.025% of playlists (≈250 playlists) → 25× amplification** of target-song recommendations downstream; 40× more than an average song at equivalent training frequency.
- 1% collective with InClust → ~10× amplification; with Hybrid, <0.01 NDCG/R-precision loss across the recommender.
- Random baseline insertion: only 3–4× amplification at α = 0.001–0.002 (vs. 16–22× for DirLoF).
- **Authenticity preserved:** at α = 1%, target-song recommendations replace relevant songs in <15% of cases; no systematic harm to non-target artists; participant own-recommendation quality stable.
- **Information-efficiency (DirLoF):** 1% collective using *2024 scraped Spotify stream counts* (as a proxy for 2010–2017 training-era popularity) achieves >85% of full-information amplification — real-world feasibility without platform internals.

**Normative framing in the paper:** explicitly positioned as legitimate counter-power for emerging artists against recommender-driven concentration ("Justice at Spotify" framing), not as an adversarial attack. Model performance loss < 0.01 NDCG points — low externality.

## Multi-collective dynamics — Karan, Karahalios, Vincent & Sundaram 2025

arXiv 2505.00195. Extends Hardt et al. 2023's single-collective framework to settings where two or more distinct collectives simultaneously act on the same ML system with potentially divergent objectives.

**Headline finding:** "Two collectives that each achieved ~100% success when acting alone dropped to ~25% efficacy in mutual presence when their strategies conflicted" (Abstract). Conversely, aligned-objective collectives (both promoting or both demoting) exhibit constructive synergy.

**Constructiveness score** CT(c_i, c_j): positive when c_j boosts c_i's objective, negative under interference. Two promoters → CT > 0; promoter + demoter → opposite-signed CTs (mutual interference).

**Other results:**
- **Collective size dominates homogeneity** — size variations exceed homogeneity effects 3–5× in determining success (Figure 5).
- **Demoting is easier than promoting** under limited collective size — removing items from a top-k ranking requires fewer defections than inserting them.
- **Three-collective scenarios** show magnified interference: a third collective can suppress the original pair's efficacy by an additional 10–30%.
- **Unintended interactions** arise from model internals (e.g., DistilBERT tokenizer treats "100" and "101" identically) — collectives cannot easily predict ex ante which combinations will conflict.

**Implication for the wiki:** real-world consumer counter-power involves multiple concurrent collectives (e.g., one pushing for price reductions, another demanding product recall, environmental advocates, labour advocates). Single-collective ACA results do not transfer directly.

## Multi-collective dynamics: statistical bounds (Battiloro et al. 2026)

arXiv 2605.06749. Harvard/Mila/ISTA preprint (Battiloro, Greiner, Rancati et al.; six authors across Harvard, Mila/LawZero, ISTA, UBC, Padova). Delivers the **first formal statistical lower bounds** on per-collective and global ACA success for M competing or collaborating collectives simultaneously manipulating a shared classifier's training data. Generalises Gauthier et al. ICML 2025 from M=1 to arbitrary M; reduces to the M=1 case as a sanity-check confirmed in the appendix. Published as a NeurIPS 2025 non-archival workshop precursor.

**Theorems 3.1 / 4.1.** Theorem 3.1 gives per-collective lower bounds on success probability as a function of that collective's mass, its feature strategy, its label target, and the competing mass of other collectives. Theorem 4.1 gives the global success bound across all M collectives. Together they define a mass-ratio tradeoff frontier: shifting mass toward one collective raises its success bound at the expense of others — the frontier is explicitly quantified.

**Label alignment is the dominant success driver.** This is the single most actionable finding for strategy design. Fragmented collectives targeting different labels at shared feature values strongly cancel each other: mass without label coordination produces near-zero global success in adversarial multi-collective scenarios. The paper's M=4 simulation (N=200K, ᾱ=0.4) with high mass entropy and high label entropy drives the global success guarantee near zero. Constructive synergy — improving all collectives' outcomes — requires aligning on the same target label or on complementary, non-interfering feature regions.

**Computability hierarchy.** The bounds are computable by each collective with only partial inter-collective knowledge, across three tiers:
- **Worst-case:** each collective knows only the total competing mass — sufficient to compute a lower bound.
- **Intermediate:** a trusted aggregator publishes a single "others" conflict term aggregating all competing collectives' interference, without revealing individual collective positions. This is the design-relevant tier — a privacy-preserving coordinator role that enables each collective to compute tighter bounds without inter-collective disclosure.
- **Best-case:** full inter-collective knowledge (impractical in adversarial settings; bounds as a theoretical benchmark).

**Signal planting and unplanting.** The framework covers both directions: collectives can plant a signal (bias toward a target class) and unplant one (remove an existing association). The bounds apply symmetrically.

**No code released.** Only synthetic climate-adaptation simulations are included in the appendix; no consumer-ACA implementation artifacts are available.

**Regime-dependence annotation on the Karan et al. ≤75% figure.** The existing [[algorithmic-collective-action#Multi-collective dynamics — Karan, Karahalios, Vincent & Sundaram 2025|Karan et al. 2025]] finding — "competing collectives suppress each other ≤75%" — reflects a two-collective scenario with partial feature overlap. That figure implies substantial residual success. Battiloro et al.'s four-collective high-entropy scenario produces near-zero global success — not a contradiction but a qualitatively different parameter regime. The ≤75% figure should be read as regime-specific, not as a floor on all multi-collective ACA. The Battiloro result extends the Karan finding: as M grows and feature/label entropy increase, suppression can approach total cancellation.

**Strategy-layer implication.** For the [[mechanism-synthesis-readout|Multi-Collective Adaptive-Pricing Disruption build]], label coordination is a prerequisite, not an optimisation: mass without label alignment is near-zero-return at M≥4 with high feature entropy. This strengthens the case for centralised label-coordination infrastructure (the trusted-aggregator "others" conflict term) as a first-order design requirement rather than a refinement. See also [[data-disruption-strategy-map]].

*(Source: `raw/research/weekly-2026-05-18/07-04-aca-multiple-collectives.md` — arXiv 2605.06749, submitted May 7 2026. Trust tag: high — strong mathematical derivations, reduces to prior work at M=1; NeurIPS 2025 non-archival workshop precursor.)*

## How this maps onto the wiki's lever inventory

| Wiki anchor | What ACA substrates |
|---|---|
| [[possible-strategic-levers\|Lever #10 — adversarial training-data injection]] | Direct technical anchor. The lever is the engineering instantiation of ACA. Hardt 2023's gradient-control strategy is the supervised-learning baseline; the bandit / online-learning extension remains the engineering gap (per [[adversarial-data-poisoning]] flag). |
| [[possible-strategic-levers\|Lever #9 — collective training-data withdrawal]] | Erasure-strategy variant of ACA (Hardt 2023, Theorem 5). |
| [[possible-strategic-levers\|Lever #14 — demand-strike coordinator]] + [[possible-strategic-levers\|#16 — threshold-triggered campaigns]] | The "critical-mass" framing in Hardt 2023 §6 is direct theoretical anchor for threshold-coordinator design. |
| [[adversarial-data-poisoning]] | Sister page — same technical primitives, framed as the firm's-eye view of the threat. Cross-references this page for the legitimate-weapon framing. |

## Conflicts / qualifications

- **Multi-collective interference (A3) qualifies single-collective optimism.** Real-world consumer-counter-power is rarely a single collective vs. a single firm; concurrent campaigns can suppress each other by 50–75%. Strategy-layer plans should account for the existing competitive landscape of consumer collectives.
- **Firm-side defences degrade single-collective success.** See [[the-firms-view]] for the catalogue: differential-privacy training (Solanki et al. 2025; DP noise scale ε inversely proportional to achievable α), Byzantine-robust aggregation, threshold-tightening (Milli et al. 2019 — with disparate-impact externality).
- **Authenticity-preserving variants minimise externalities** (Baumann 2024 demonstrates; <0.01 NDCG loss). This refines the "data poisoning destroys the model" framing: well-designed ACA can shift specific outcomes without degrading model performance broadly.

## Source

- Hardt, Mazumdar, Mendler-Dünner & Zrnic. 2023. *Algorithmic Collective Action in Machine Learning*. ICML 2023; arXiv 2302.04262. Captured: `raw/research/clawnet-adjacent-methods/13-aca-hardt-2023.md` + `01-aca-hardt-2023-abs.md`. Trust tag: peer-reviewed ICML, foundational paper of the ACA programme. Empirical validation on real freelance-platform data.
- Baumann & Mendler-Dünner. 2024. *Algorithmic Collective Action in Recommender Systems: Promoting Songs by Reordering Playlists*. arXiv 2404.04269. Captured: `raw/research/clawnet-adjacent-methods/16-aca-recsys-baumann-2024.md` + `02-aca-recsys-baumann-2024-abs.md`. Trust tag: ML conference paper, deployed-system evaluation against Deezer transformer on Spotify MPD.
- Karan, Karahalios, Vincent & Sundaram. 2025. *Algorithmic Collective Action with Two Collectives*. arXiv 2505.00195. Captured: `raw/research/clawnet-adjacent-methods/14-aca-two-collectives-2025.md` + `03-aca-two-collectives-2025-abs.md`. Trust tag: preprint, single research group (UIUC + SFU), theoretical framework + experimental validation on resume classification + MovieLens recsys.
- Battiloro, Greiner, Rancati et al. 2026. *A Statistical Framework for Algorithmic Collective Action with Multiple Collectives*. arXiv 2605.06749. Captured: `raw/research/weekly-2026-05-18/07-04-aca-multiple-collectives.md`. Trust tag: high — strong mathematical derivations, reduces to prior work at M=1; NeurIPS 2025 non-archival workshop precursor. Six authors across Harvard, Mila/LawZero, ISTA, UBC, Padova.

## Related

- [[the-firms-view]] — the firm-side framing of the same technical primitives (attack taxonomies + DP-as-counter + adaptive learning + threshold-tightening)
- [[adversarial-data-poisoning]] — sister page; technical attack taxonomy (Wang et al. 2024) + DP-as-firm-counter (Solanki et al. 2025)
- [[strategic-classification]] — alternative formal frame: individual-level strategic response by users to a firm's classifier (Hardt et al. 2016 + extensions)
- [[obfuscation]] — adjacent counter-power lever (per-user, not coordinated)
- [[possible-strategic-levers]] — strategy-layer lever inventory
- [[pricing-algorithm-taxonomy]] — which pricing-algorithm families ACA actually disrupts
- [[data-disruption-strategy-map]] — strategy matrix for choosing levers; label coordination flagged as prerequisite for Multi-Collective Adaptive-Pricing Disruption build
- [[mechanism-synthesis-readout]] — Multi-Collective Adaptive-Pricing Disruption build; label coordination as prerequisite noted
- [[complex-contagion]] — network-science layer for how a collective reaches critical mass
