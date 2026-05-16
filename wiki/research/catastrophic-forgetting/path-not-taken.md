---
arxiv: "2511.08567"
title: "The Path Not Taken: RLVR Provably Learns Off the Principals"
captured_on: "2026-05-16"
theme: catastrophic-forgetting
---

# The Path Not Taken: RLVR Provably Learns Off the Principals

Chen et al. (2025, arXiv:2511.08567) give the first parameter-level mechanistic account of RLVR's optimization geometry. The core finding: RLVR does **not** modify the weight matrices along their principal (high-singular-value) directions — it routes updates into low-curvature, off-principal subspaces, leaving the pretrained spectral structure nearly intact. The observed update sparsity (36–92% of weights unchanged in bf16) is a downstream artifact of this geometry interacting with finite-precision storage, not a primary phenomenon. The mechanism is formalized as the **Three-Gate Theory** (KL Anchor → Model Geometry → Precision).

## Source

- arXiv: 2511.08567 — "The Path Not Taken: RLVR Provably Learns Off the Principals"
- Raw capture: `raw/research/rlvr-forgetting/02-02-path-not-taken.md`

## Method

### Three-Gate Theory

**Gate I — KL Anchor.** Every on-policy RL step implicitly imposes a per-step policy-KL leash. Proposition 3.1 (M-projection bound): for a one-step update $\theta^+$,

$$D_{\mathrm{KL}}(\pi_{\theta^+} \| \pi_\theta) \;\leq\; (1 + o(1))\, D_{\mathrm{KL}}(\tilde{q}_\beta \| \pi_\theta),$$

where $\tilde{q}_\beta \propto \pi_\theta \exp(R/\beta)$ is the soft-reward oracle. Proposition 3.2 translates this to a Frobenius bound on the weight update $\Delta W$: for any block $W \subset \theta$,

$$\|\Delta W\|_F \;\leq\; \sqrt{2K/\mu}\,(1 + o(1)),$$

where $K$ is the per-step KL budget and $\mu$ is the minimum Fisher eigenvalue on the update subspace.

**Gate II — Model Geometry.** The KL bound constrains the step size but not its direction. Gate II supplies the direction: a well-pretrained model has a highly structured singular spectrum. A layer-wise curvature proxy $S_W \succeq \mu_W I$ means the KL leash double-constrains movement into high-curvature (principal) directions. Three spectral consequences follow (Theorem 3.3 / Corollaries 3.4–3.5):

- **Subspace rotation bounded** (Wedin's sin-$\Theta$ theorem):
$$\max\!\left(\|\sin\Theta(U_k(W_0), U_k(W^+))\|_2,\; \|\sin\Theta(V_k(W_0), V_k(W^+))\|_2\right) \;\leq\; \frac{\|\Delta W\|_2}{\gamma_k},$$
where $\gamma_k = \sigma_k(W_0) - \sigma_{k+1}(W_0)$ is the singular-value gap.

- **Singular-value stability:** $|\sigma_k(W^+) - \sigma_k(W_0)| \leq \|\Delta W\|_2$.

- **Top-$k$ Ky Fan norm stability:** $\bigl|\|W^+\|_{(k)} - \|W_0\|_{(k)}\bigr| \leq k\,\|\Delta W\|_2$.

Net effect: RLVR updates avoid high-energy principal directions and instead concentrate in off-principal, low-magnitude weight positions.

**Gate III — Precision.** bfloat16's 7-mantissa-bit format suppresses micro-updates below the unit-in-last-place (ULP) threshold. Off-principal updates are disproportionately small; they fall below ULP and register as zero-change, producing the *apparent* sparsity. Increasing the learning rate scales these sub-ULP updates above the threshold, largely eliminating measured sparsity — confirming sparsity is an artifact of precision, not zero gradients.

### Empirical definition: bf16-aware update sparsity

$$\mathrm{sparsity}_{\mathrm{bf16}}(\theta^0,\theta^1;\eta) \;=\; 1 - \frac{\|\theta^1 - \theta^0\|_{0,\eta}^{\mathrm{bf16}}}{n}, \quad \eta = 10^{-3}.$$

A weight is *unchanged* iff $|\hat{w}_i - w_i| \leq \eta\max(|w_i|,|\hat{w}_i|)$, equivalent to bitwise equality under bf16 (Def. 2.1–2.2).

### Principal-weight proxy

High-curvature directions are proxied by **principal weights** $M_{\mathrm{princ}}^{(k)} = \mathrm{Top}_\alpha(s_{ij}^{(k)})$, where $s_{ij}^{(k)} = |W_0^{(k)}(i,j)|$ is the magnitude after rank-$k$ SVD reconstruction of $W_0$. Overlap of the RLVR update mask with $M_{\mathrm{princ}}$ is *sub-random* across all tested layers, algorithms, and model families.

## Claims

1. **Sparsity is a readout, not a cause.** RLVR sparsity (36–92% unchanged weights in bf16) results from the optimization bias plus finite precision; it is not intrinsic to RL or zero gradients.
2. **Model-conditioned optimization bias.** For a fixed pretrained model, RLVR concentrates updates in the same stripe-like row/column patterns regardless of dataset or RL algorithm (Jaccard overlap ~0.55–0.60 vs. random baseline ~0.41–0.47, Table 2).
3. **Off-principal routing.** RLVR update masks show sub-random overlap with $M_{\mathrm{princ}}$; SFT update masks show super-random overlap — the two regimes are *disjoint*.
4. **Spectral preservation.** RLVR leaves singular-value profiles near-identical to the base model; SFT distorts them substantially (principal-angle curves and normalized spectral shift, Fig. 4).
5. **Geometry is causal.** Disrupting the pretrained geometry via orthogonal rotations or head permutations collapses update-locality overlap to a random baseline in intervened layers only, while untouched layers remain high (Fig. 6).
6. **SFT-era PEFT misaligns with RLVR.** Restricting updates to principal weights (as SFT priors do) produces the *worst* RL KL trajectory; freezing principal+large-magnitude weights while updating non-principal, low-magnitude ones (~70% of parameters) closely matches dense RLVR.
7. **PiSSA fails for RL.** Principal-targeted LoRA (PiSSA) gives no accuracy gain over standard LoRA on RLVR and collapses at learning rates needed to match full-parameter performance.
8. **Generality.** The off-principal signature persists across math, code, agents (WebSearch, SWE-bench, planning), and RLHF (DPO, SimPO), multiple model families (Qwen, LLaMA, Mistral), and MoE architectures.

## Strengths / Novelty

- First *parameter-level* mechanistic account linking RL optimization to weight evolution; prior work was policy-level or distributional.
- Theoretical chain is tight: KL leash (Prop. 3.1–3.2) → spectral geometry (Thm. 3.3, Cor. 3.4–3.5) → precision filter (Cor. 3.6) — each gate independently testable.
- Causal isolation via geometry-scrambling intervention (Sec. 4.3) is methodologically clean.
- Directly actionable: the "safe mask" ($M_{\mathrm{low}} \cup M_{\mathrm{princ}}^c$) derived from base weights alone tracks dense RLVR with 70% of parameters.
- Breadth of model suite (1.5B–30B, dense + MoE, math/code/agents/RLHF) makes the finding robust.

## Weaknesses / Limits

- All models are post-training checkpoints (base → RLVR); no analysis of RLVR applied on top of *another domain's RLVR* (the stacking scenario most relevant to this wiki).
- Principal-weight proxy ($M_{\mathrm{princ}}$) depends on rank-$k$ SVD reconstruction; choice of $k$ and $\alpha$ may shift overlap statistics.
- Theory in Sec. 3 assumes $\log \pi_\theta$ is $C^3$ and Fisher $\succeq \mu I$ on the update subspace — strong regularity conditions not verified empirically.
- The "safe mask" experiment uses a fixed one-shot mask; dynamic refreshing (necessary for long training) is left as future work.
- Paper does not directly measure forgetting of other skills — the forgetting-prevention implication is inferred from spectral stability, not demonstrated on multi-task benchmarks.

## Relevance to this wiki's project

**The user's reallocation question:** "When you stack skills with RLVR, does it just move optimization from one skill to another (zero-sum reallocation)?"

This paper gives the most direct mechanistic answer: **the reallocation framing is approximately correct but the mechanism is more specific than zero-sum**. RLVR does not overwrite the principal directions (the high-energy, cross-skill-relevant subspace). Instead it operates in the *complementary* off-principal subspace — low-curvature, low-magnitude weights that are less load-bearing for existing behavior. This is structurally better than zero-sum: two RLVR passes targeting the same off-principal subspace could still interfere, but they are far less likely to clobber each other's principal structure than two SFT passes would.

**Three implications for single-sample concept installation ($R_w$):**

1. *Preferred installation space.* The off-principal, low-magnitude subspace is where RLVR naturally writes. $R_w$ should target exactly this region — installing a new concept into low-curvature weights minimizes spectral disruption to prior skills. This is the mechanistic basis for selective installation in [[../synthesis/proposed-method]].

2. *Stacking is not obviously zero-sum.* Because each RLVR pass avoids the principal directions, successive concept installations may be near-orthogonal in update space — not guaranteed (they share the same off-principal pool), but far more benign than dense SFT stacking. Whether the off-principal pool is finite and depletable is the open question.

3. *Forgetting risk is asymmetric.* A concept learned via RLVR that lives off-principal is at risk from *SFT* (which targets principal directions and could destroy the spectral context the off-principal concept relies on) more than from subsequent RLVR. This asymmetry matters for the SFT → RLVR pipeline ordering.

**Connections to companion pages:**

- [[rls-razor]] (forthcoming) — "RL's Razor" (KL-minimality principle) and this paper's Gate I are two framings of the same KL anchor effect. RL's Razor says RL finds the KL-minimal improvement; this paper says that translates to off-principal weight updates. Together they are the distributional and geometric views of the same phenomenon.
- [[../rlvr-mechanics/rl-sparse-subnetwork]] (Balashov) — finds RLVR activates a sparse subnetwork; this paper explains *why* that subnetwork is sparse and *where* it lives (off-principal). Balashov's sparse subnetwork ≈ this paper's $M_{\mathrm{low}} \cup M_{\mathrm{princ}}^c$ mask.
- [[../rlvr-mechanics/rethinking-rl-sparse-selection]] (REASONMAXXER) — token-level sparsity (RL reranks 1–4% of positions within the base top-5). That is distributional sparsity; this paper is weight-space sparsity. They are complementary: off-principal weight updates produce off-principal token routing changes.
- [[../self-play/invisible-leash]] — Invisible Leash asks how far RLVR pulls the model from its base; this paper answers: not far in principal-direction space. The leash is tightest along the directions that matter most (high-curvature), which is exactly what keeps support skills intact.

## Connections to the wiki

- [[_overview]] — adds mechanistic grounding for "RLVR-induced forgetting is mild" claims
- [[ewc-gemma2-cpt]] — EWC protects high-Fisher (≈ high-principal) weights; this paper shows RLVR voluntarily avoids them — the two mechanisms converge on the same protected set from opposite directions
- [[rft-mitigates-forgetting]] — RFT forgetting reduction may partly be because RFT (verifiable-reward RL) shares RLVR's off-principal geometry
- [[mechanistic-forgetting]] — off-principal routing is the mechanistic underpinning worth connecting to circuit-level forgetting accounts
- [[../selective-finetuning/_overview]] — the safe-mask finding ($M_{\mathrm{low}} \cup M_{\mathrm{princ}}^c$ reproduces dense RLVR with 70% of params) is directly relevant to parameter-efficient selective fine-tuning
- [[../synthesis/proposed-method]] — off-principal sparsity is the mechanistic basis for the $R_w$ selective-installation hypothesis

## Related

- [[rls-razor]]
- [[ewc-gemma2-cpt]]
- [[rft-mitigates-forgetting]]
- [[rft-data-perspective]]
- [[mechanistic-forgetting]]
- [[empirical-forgetting]]
- [[_overview]]
- [[../rlvr-mechanics/rl-sparse-subnetwork]]
- [[../rlvr-mechanics/rethinking-rl-sparse-selection]]
- [[../self-play/invisible-leash]]
- [[../synthesis/proposed-method]]
- [[../selective-finetuning/_overview]]
