# Unlearnable Trajectories (GHOST)

GHOST is a manifold-aligned data-poisoning framework that lets individuals publish check-in location trajectories which look like genuine human mobility yet deny any downstream ML model the ability to learn next-location predictors from them — while resisting adversaries who try to strip the protection using leaked (clean, perturbed) pairs. It extends the unlearnable-examples paradigm, previously confined to image domains (see [[nightshade-glaze]]), to discrete sequential data, and is the first plausibility-and-purification-aware unlearnable-examples method for next-POI prediction.

## Source

- `raw/research/weekly-2026-06-08/02-ghost-unlearnable-trajectories.md` — Yu, Idris, Guan & Zhou (Fudan / U. Malaya / Tongji), *GHOST: Plausible Yet Unlearnable Trajectories via On-Manifold Substitution for Next-POI Privacy*, arXiv 2606.03711, June 2026. Peer-review-pending preprint from established institutions; evaluated on standard benchmarks; code not released as of capture date. **Trust: high for empirical claims on stated benchmarks; architecture-transferability and discrete Schrödinger-bridge adversary left for future work.**

## Mobility Data Extraction Context

Releasing a check-in trajectory dataset is, structurally, releasing a strong predictor of every contributor's future whereabouts. Next-POI models trained on public datasets such as Foursquare TSMC2014 and Gowalla achieve individual-level next-location accuracy sufficient to support commercial profiling, surveillance, and targeted harassment — purposes entirely outside the original research intent. The extraction is involuntary and structural: the temporal regularity that makes these datasets scientifically valuable is exactly what makes them privately dangerous, and the danger materialises the moment the data leave the publisher's hands.

This is the mobility-domain instance of the same dynamic that Nightshade/Glaze address in the image domain: a contributor publishing data inadvertently arms downstream ML extraction against themselves. Machine unlearning does not solve it — it operates post hoc and requires a cooperative model owner. Any third party can train an arbitrary model on the released data. A defence must act at release time.

## What GHOST Is

GHOST is a **bilevel optimisation** that produces a perturbed dataset from a clean one through position-wise POI substitution. At each perturbable position in each session, every candidate replacement POI is scored by two signals combined linearly:

- **Adversarial term** — the negative log-likelihood the surrogate victim model assigns to the clean next-POI label after the candidate is substituted at that position. A candidate that makes the genuine next location maximally surprising scores high.
- **Manifold term** — the log-likelihood of the candidate under a frozen *trajectory language model* (a transformer pre-trained on real check-in sequences and then frozen). A candidate that lies in the high-density region of real human mobility scores high.

The combined score is: `score(p') = α · adv(p') + β · mani(p')`, with recommended weights `(α, β) = (2.0, 0.5)`.

A candidate is sampled from a low-temperature softmax over this score (`τ = 0.3`). The surrogate victim is then re-fitted on the updated perturbed data, and the loop repeats for `T_outer = 5` rounds.

Hard **plausibility constraints** bound the candidate set before any adversarial scoring:
- Geographic: haversine distance ≤ 1.0 km from original POI.
- Semantic: category(substitute) = category(original). This constraint is never relaxed, even in sparse neighbourhoods.
- Speed: implied travel speed between consecutive perturbed POIs ≤ 60 km/h (enforced as a context-dependent runtime mask).

## Key Mechanism: Stochastic Manifold Substitution vs. Deterministic

The paper's central design insight is that **the same prior that guarantees plausibility also makes purification fail**.

**Why deterministic baselines break.** A deterministic protection map (such as PGD's all-adversarial argmin) produces a fixed mapping from clean POI to substitute POI. An adversary with access to a small sample of (clean, perturbed) pairs — even as few as 5% leakage — can reconstruct this map via a frequency-table inverter (`p̂(clean | perturbed) = argmax of empirical conditional`) or a Schrödinger-bridge denoiser (BridgePure), recovering most of the original signal. The map's predictable structure is what the adversary inverts.

**Why stochastic on-manifold substitution defeats purification adversaries.** Three attackers are modelled:
- **A2 (Denoising-bridge)**: trains a sequence denoiser from leaked pairs, applies it to recover clean data.
- **A3 (Frequency-table inverter)**: builds an empirical context-free `p̂(clean | perturbed)` lookup table from leaked pairs.
- **A4 (Bigram-adaptive)**: same as A3 but exploits one step of perturbed context.

GHOST's manifold-prior substitution defeats all three via the same structural argument:

1. *Optimal denoiser collapses on on-manifold inputs.* Because every substituted POI is already a plausible check-in that some real user could have made in that context, the denoiser has nothing statistically distinguishable to remove. The conditional expectation `E[clean | perturbed]` approaches the marginal prior over plausible POIs at that position — i.e., the optimal denoiser approaches the identity.

2. *Frequency-table inversion degenerates to uniform.* Because GHOST samples stochastically over a manifold-weighted softmax, a single clean POI maps to multiple plausible substitutes with comparable probability. The empirical `p̂(clean | perturbed)` is therefore high-entropy and its argmax has high error. The inverter also cannot distinguish "this POI is a perturbation of something else" from "this POI was genuinely visited."

No explicit entropy-floor randomisation is used or needed. Ablations confirm that adding an entropy floor on top of the manifold term degrades all three protection metrics — the manifold prior already supplies the necessary dispersion, and the legacy heuristic is redundant and actively harmful.

## Empirical Results

Evaluated on Foursquare-NYC and Foursquare-TKY (TSMC2014 release), the standard category-aware POI benchmarks. Victim is a two-layer causal Transformer following STAN. Three seeds per configuration.

**Primary results (acc@1):**

| Setting | NYC clean | NYC GHOST-protected | Best adversarial restore (NYC) |
|---|---|---|---|
| No protection | 0.1379 | — | — |
| GHOST | 0.1379 | 0.0544 | 0.0733 (A4 bigram) |
| PGD (deterministic baseline) | 0.1379 | 0.0566 | 0.0755 (A3 frequency-table) |

- GHOST reduces victim acc@1 from 0.1379 → 0.0544 on NYC (protection gap Δprot = 0.0835).
- Best adaptive purifier (bigram A4) only restores to 0.0733 on NYC and 0.1014 on TKY — GHOST achieves the lowest A4-restored accuracy on both datasets.
- GHOST has the best headline Δmean (0.0735 NYC) among all methods, leading PGD by 0.29 pp.
- On the protection-vs-purification-resistance Pareto plane, GHOST is the unique Pareto-optimal method on NYC and jointly occupies the Pareto front with PGD on TKY (within 1σ).
- Manifold overhead: adding the trajectory LM term costs only ~11–14% additional compute over a pure adversarial baseline. The LM is pre-trained once per dataset and disk-cached.
- Leak-ratio sweep: at r = 0.20 (20% leaked pairs), GHOST's A3 survival gap stays below 0.04 and retains a consistent edge over PGD across the entire sweep.

## Generalisation: The Unlearnable-Examples Paradigm Applied to Sequential Data

The unlearnable-examples (UE) paradigm — originally introduced for continuous image pixel spaces — had not previously been applied to discrete, plausibility-constrained sequential data. Direct ports of image-domain UE to POI trajectories fail on two counts: (1) unconstrained substitution produces implausible trajectories that break downstream services and alert auditors; (2) deterministic maps are vulnerable to purification adversaries that image-domain work did not model.

GHOST's contribution is threefold: formalising a plausibility-constrained threat model for sequential UE, proposing the manifold-prior substitution score as a structural replacement for entropy-floor randomisation, and demonstrating Pareto-optimal protection under a three-adversary threat model.

The same design principles generalise beyond location data to **any structured behavioral sequence** where perturbations must remain on the real-data manifold to survive service compatibility checks and adversarial purification: browsing trajectories, purchase-history sequences, health sensor logs, ride-share route logs.

**Relationship to [[nightshade-glaze]]:** Nightshade/Glaze poison image training data from the creator's side by injecting adversarial signal into images before release, denying style/concept learning to downstream models while appearing visually intact. GHOST does the same for location trajectories: the user-side publisher poisons the mobility training signal before release, denying next-POI learning while the trajectory remains behaviorally plausible. The structural parallels — manifold alignment, plausibility constraints, purification resistance as a first-class design goal — are direct.

**Relationship to machine unlearning:** GHOST takes the complementary, proactive route to machine unlearning. Machine unlearning removes specific data influence post hoc from an already-trained model — it requires cooperative model owners and has been shown to struggle to suppress poisoning influence once absorbed. GHOST prevents the condition machine unlearning is designed to remediate. The two are complementary in a defence-in-depth posture.

## Design Principles for Consumer-Side Tools

From the GHOST analysis, three actionable design principles for consumer data-collection counter-tools:

1. **Plausibility first, or the tool fails twice.** Any tool operating on structured behavioral sequences must constrain perturbations to the real-data manifold. Failing to do so causes both auditability failure (anomalous outputs detected and filtered by downstream services) and purification failure (adversary can train a denoiser on off-manifold noise).

2. **Release-time is the only viable point of intervention.** Post-hoc mechanisms (machine unlearning, deletion requests) require cooperative model owners and are fragile against absorbed poisoning. Consumer tools that act before data reaches the model are structurally more robust.

3. **Stochastic many-to-many maps defeat lookup-table adversaries; deterministic maps do not.** Any consumer obfuscation tool using a deterministic perturbation function is vulnerable to an adversary with as few as 5% leaked (clean, obfuscated) pairs. Re-perturbation cycling (releasing a fresh stochastic perturbation on each release cycle) further amortises the leakage budget, because adversaries must re-collect pairs from scratch each cycle.

## Related

[[obfuscation]], [[nightshade-glaze]], [[adversarial-data-poisoning]], [[data-disruption-strategy-map]], [[possible-strategic-levers]], [[strategic-classification]]
