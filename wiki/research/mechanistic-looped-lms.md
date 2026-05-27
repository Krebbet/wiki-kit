# A Mechanistic Analysis of Looped Reasoning Language Models

**Authors:** Hugh Blayney, Álvaro Arroyo, Johan Obando-Ceron, Pablo Samuel Castro, Aaron Courville, Michael Bronstein, Xiaowen Dong (Oxford / Mila / Montreal / AITHYRA).

**Venue:** arXiv 2604.11791, April 2026. Preprint; no peer-review record at time of ingest.

Mechanistic study of latent-state dynamics in cyclic-recurrence looped Transformers (Huginn-0125, Ouro 1.4B, retrofitted Llama/OLMo). The central result: each layer in a cyclic recurrent block converges to a *distinct* fixed point, so the full recurrent block traces a consistent cyclic trajectory in latent space — not a single fixed point — within 1–2 iterations for models with input injection. As a direct consequence, attention patterns stabilize rapidly across recurrences, and hidden states $h^{(k)}$ become nearly iteration-invariant per layer, making step-number information in $h^{(k)}$ effectively unobservable after the first few iterations.

## Core findings

**1. Cyclic fixed-point convergence (Prop. 4.1 + empirical §4.1)**

For a $k$-stacked recurrent block $S_k$, if $S_k(\mathbf{X}') = \mathbf{X}'$ is a fixed point of the full block, then the hidden state after each individual layer $\ell \in \{1,\ldots,k\}$ is itself a fixed point under the cyclic permutation of blocks. Each layer converges to a *distinct* fixed point $\mathbf{X}'_\ell$; the cycle $\mathbf{X}'_1 \to \mathbf{X}'_2 \to \cdots \to \mathbf{X}'_k \to \mathbf{X}'_1$ is a consistent trajectory, not collapse to a single point.

**Convergence rates** (from Fig. 3 / Fig. 4):

- **Ouro 1.4B** (no input injection, Sandwich norm on residual stream): successive-iteration differences decay rapidly but the model does **not** reach a fixed point even at 128 recurrences. Limiting behavior is quasi-periodic (orbits/sliders), not a true fixed point. Non-fixed-point tokens are rare (≤ 0.02% without system prompt, up to 0.14% with long persona prompt) but the residual stream never fully stabilizes.
- **Huginn-0125** ($(2,4,2)_I$, 32 train loops, input injection, Sandwich norm on residual): converges to cyclic fixed point **immediately following the prelude** — within 1–2 recurrences. Fixed-point behavior confirmed by norm of deviation from the 128th-recurrence approximate fixed point approaching zero rapidly (Fig. 4).
- **Retrofitted Llama / OLMo** ($(4,6,4)_I$ or $(4,8,4)_I$, 32 train loops, input injection, pre-norm only): same as Huginn — cyclic fixed point reached within 1–2 recurrences post-prelude. The latent-space PCA trajectory perfectly overlaps in recurrences 16–32 (Fig. 5), confirming fixed-point lock-in.

**2. Attention pattern convergence (Prop. 4.2 + Fig. 2)**

Given bounded residual streams (guaranteed by pre-norm or sandwich norms) and weight-tied attention matrices across recurrences, the Lipschitz bound on attention-pattern change is:
$$\|S_\ell(\mathbf{X}_{\ell,t}) - S_\ell(\mathbf{X}_{\ell,t-1})\| \leq L_\text{sm} \frac{2B\kappa_\ell}{\sqrt{d}} \|\mathbf{X}_{\ell,t} - \mathbf{X}_{\ell,t-1}\|$$
where $\kappa_\ell = \|W_{Q,\ell}W_{K,\ell}^\top\|$ and $L_\text{sm} = 1/2$ (Nair 2025). As $\|\mathbf{X}_{\ell,t} - \mathbf{X}_{\ell,t-1}\| \to 0$, attention patterns freeze. The Frobenius-norm attention-similarity matrices (Fig. 2) show strong diagonal structure across all three models — same-layer attention patterns across different recurrences are most similar — confirming layer-wise, not block-wise, fixed-point structure.

**3. Stages of inference (§5)**

Recurrent blocks mirror the feedforward stages-of-inference structure (Lad et al. 2024; Queipo-de Llano et al. 2025): ColSum concentration (attention mixing metric) cycles through the same low→high→low pattern with each recurrent iteration. In sandwich (prelude+coda) architectures, the prelude performs the initial stage and the coda the final stage *once*; the recurrent block repeats only the "middle" stages. Huginn-0125 does **not** show clear stages of inference — its repeated residual-stream normalization suppresses the residual-magnitude growth that drives attention-sink formation and stage emergence. Small-scale training experiments (§5.1) confirm stages self-organize even without training biases (no recurrence schedule, no per-recurrence loss terms).

**4. Stability under test-time extrapolation**

Models with input injection (Huginn, Retrofitted Llama): each layer freezes early and maintains constant inference stages for arbitrarily many test-time recurrences — no degradation. Ouro (no input injection): ColSum concentration continues to drift at recurrence 128 (Fig. 11), and performance degrades when generalizing beyond training recurrence counts (Zhu et al. 2025, Tab. 10). Fixed-point convergence is load-bearing for OOD generalization.

## Fixed-point convergence: implications for routing

**Why $h^{(k)}$ cannot signal iteration number after convergence**

Let $h^{(k)}_\ell$ denote the residual stream after layer $\ell$ at recurrence $k$. For models with input injection (Huginn, retrofitted Llama/OLMo), $h^{(k)}_\ell \to h^{(\infty)}_\ell$ within $k \approx 1$–$2$ recurrences. For $k \geq 2$, $\|h^{(k)}_\ell - h^{(k-1)}_\ell\| \approx 0$. A router observing $h^{(k)}_\ell$ therefore sees identical inputs at steps $k = 2$ and $k = 7$ (or $k = 30$) — the states are geometrically indistinguishable. The paper makes this concrete with Fig. 4: even computing cosine similarity of $h^{(k)}_\ell$ to the (approximate) fixed point $h^{(\infty)}_\ell$, input-injection models reach $\cos \approx 1$ by $k = 2$–$3$.

**Cosine similarity of adjacent hidden states as a routing diagnostic**

Cosine similarity $\cos(h^{(k)}, h^{(k-1)})$ is a valid proxy for convergence rate (App. D.1 — "Cyclic Similarity"), and the paper uses this metric (Fig. 24 reference, cosine-similarity analogue of Fig. 3). However, for routing *per se*, the relevant question is not just convergence rate but whether *any* feature of $h^{(k)}$ encodes $k$. By the cyclic fixed-point result, after 1–2 iterations $h^{(k)}$ is determined entirely by the fixed-point cycle and contains no further $k$-dependent variation. Cosine similarity of adjacent states is therefore a conservative bound: even before it asymptotes, the signal useful for routing has already been lost.

**What information might remain in $h^{(k)}$ near convergence**

Almost none, for input-injection models post-convergence:

- The fixed-point value $h^{(\infty)}_\ell$ does encode *position within the cycle* (i.e., which layer $\ell$ within the recurrent block), but this is fixed architecture structure, not iteration count.
- Tokens in the very early transient ($k \leq 2$) retain $k$-dependent variation. After that, $h^{(k)}$ contains no monotone iteration signal.
- Residual-stream *magnitude* in Ouro (no input injection) continues to change slowly with $k$, since Ouro does not reach a true fixed point. Magnitude could in principle encode a weak step signal for Ouro-class models, but the magnitude change is small and non-monotone (orbit / slider behavior).

**Mitigation: step conditioning**

The paper does not itself propose a mitigation, but the finding directly motivates the step-index conditioning used by LoopFormer ($(t, \Delta t)$ embeddings) and Mixture-of-Recursions. Providing $(k, k_\text{max})$ as an explicit side-channel input to each recurrent block — or to the router — restores the iteration signal that $h^{(k)}$ no longer carries. Without this, any router trained to distinguish "step 3 of 8" from "step 7 of 8" via $h^{(k)}$ alone is solving an essentially impossible inference problem for input-injection architectures.

**Precision update on the Exp 1 proposal**

The proposal text "may be nearly identical" understates the finding. For Huginn-0125 and retrofitted Llama/OLMo: $h^{(k)}_\ell$ is **provably and empirically indistinguishable** from $h^{(k')}_\ell$ for any $k, k' \geq 2$ (to within numerical precision), not merely similar. The cyclic fixed point is exact, not approximate, in the limit.

## Attention pattern analysis

Attention patterns exhibit the same cyclic fixed-point structure as the residual stream (Prop. 4.2, Fig. 2). Each layer's attention matrix $A_{\ell,k}$ becomes layer-periodic: $A_{\ell,k} \approx A_{\ell,k'}$ for all $k, k' \geq k_0$ where $k_0 \approx 1$–$2$.

The Frobenius-norm cross-attention similarity heatmaps (Fig. 2) reveal:
- **Diagonal dominance:** same layer at different recurrences has minimal norm difference; off-diagonal blocks (different layers within the block, same recurrence) show larger norms, confirming distinct per-layer fixed points.
- **No degradation at higher recurrences:** the diagonal structure is equally strong at recurrences 16–32 as at 0–16.

The ColSum concentration metric (fraction of attention mass concentrated on few token positions) cycles predictably within each recurrent block: early layers show high concentration (sink-like), middle layers lower concentration (mixing), late layers returning to concentration (compression). This cycle repeats identically in each of the 8 tested recurrences for retrofitted Llama (Fig. 7, Fig. 11). The cyclic mixing stages are input-dependent (computed on GSM8k, 256 examples) but structurally invariant to recurrence count.

**Huginn-0125 exception:** Huginn's repeated normalization of the residual stream (both before attention and after MLP — the Sandwich norm on $\hat{X}$) suppresses residual magnitude growth, preventing the massive-activation onset that triggers sink formation and stage separation (Fig. 9). Huginn therefore lacks distinct inference stages despite having strong cyclic fixed-point convergence. This is a norm-structure artifact, not a general property of input-injection models.

## Goal relevance

| Goal | Relevance | Notes |
|------|-----------|-------|
| **G1** (isolated block training) | Low | Paper does not address block isolation or swappability. Fixed-point convergence does imply block outputs are decoupled from iteration count, which could simplify isolated training, but this is not studied. |
| **G2** (dynamic per-block parameter allocation) | Low-Medium | The stability-extrapolation result (§5.2) suggests that models reaching fixed points generalize better to varying recurrence counts. Relevant if G2 involves variable-depth execution at inference time. |
| **G3** (token-conditional routing) | **Critical** | The cyclic fixed-point finding is the primary mechanistic obstacle to Experiment 1. A router trying to observe $h^{(k)}$ and emit a halting decision faces degenerate inputs: $h^{(k)} \approx h^{(k')}$ for $k, k' \geq 2$. Step conditioning ($(t, \Delta t)$-style; see [[loopformer]]) is the necessary intervention. Also: the stages-of-inference result suggests that if a router exists, it should specialize by position within the recurrent block, not uniformly across all layers. |

## Credibility

arXiv preprint (2604.11791), April 2026. Oxford / Mila / Montreal / AITHYRA. No peer-review record at time of ingest. Code adapted from Karpathy's nanochat (public); model checkpoints via HuggingFace (Huginn, Ouro, McLeish retrofitted series). Main theoretical results (Props. 4.1, 4.2) have complete proofs in App. A. Empirical results on 256 GSM8k test examples; non-reasoning results (HellaSwag) in App. E.4 show no change in conclusions. Non-fixed-point behavior (Ouro orbits/sliders) characterized via heuristic algorithm — absolute percentages depend on threshold hyperparameters, but the qualitative conclusion (rare; prompt-length-correlated) is robust across settings. Small-scale training experiments (§5.1) at 512 model dim, 3.7B tokens — treat with caution re: scale generalization.

## Empirical claims

- Ouro 1.4B: successive-layer cosine similarity converges within $k \leq 5$ iterations but does not reach a true fixed point; non-fixed-point tokens ≤ 0.14% (rare).
- Huginn-0125 and retrofitted Llama/OLMo: cyclic fixed point reached within $k \approx 1$–$2$ recurrences post-prelude; 0% non-fixed-point tokens for retrofitted models under all tested prompts.
- Input injection is the primary architectural driver of fixed-point stability; pre-norm without input injection reaches a *degenerate* fixed point (all layers converge to the same point — action of each block tends to zero). Ouro's norm structure (Sandwich on outputs rather than residual stream) prevents fixed-point convergence even with input injection.
- Stages of inference (ColSum concentration cycles) are stable for arbitrary recurrence counts in fixed-point models; drift continuously in Ouro.
- Stages of inference emerge without explicit training pressure: small models trained with constant 4 recurrences and no per-recurrence loss develop recurrent-block-wise inference stages that match feedforward baselines.
- Huginn-0125 does not exhibit stages of inference due to repeated residual-stream normalization suppressing magnitude growth.
- Orbits and sliders (non-fixed-point limiting behaviors) occur at intermediate layers when they occur at the block level; orbits and sliders do not co-occur on the same token (conditional co-occurrence matrix, Fig. 14).

## Open questions

1. **Why does Ouro's norm prevent fixed-point convergence?** Analytically unresolved. The paper demonstrates the empirical difference but does not establish a theoretical mechanism.
2. **Is fixed-point convergence desirable for reasoning?** The paper notes (§6 Limitations) that stable fixed-point behavior may be *restrictive* for reasoning tasks — an open question. Input-injection models extrapolate better, but whether the fixed point limits representational capacity is not studied.
3. **Step-conditioning sufficiency.** If $(k, k_\text{max})$ embeddings are injected, does the router become learnable? The paper does not test any routing mechanism.
4. **Scale dependence of non-fixed-point frequency.** Ouro's small non-fixed-point token rate at standard prompts — does this increase at larger model scale, longer context, or harder reasoning prompts?
5. **Intermediate-layer fixed-point analysis for Ouro.** The paper shows intermediate layers exhibit orbit behavior when the block-level output does (App. C.2), but does not quantify whether specific intermediate layers are more stable than others.

## Source

- `raw/research/loop-challenges/02-mechanistic-looped-abs.md`
- `raw/research/loop-challenges/12-mechanistic-looped-pdf.md`

## Related

- [[huginn]] — primary empirical subject; input injection + sandwich norm; fast cyclic fixed-point convergence
- [[loopformer]] — $(t, \Delta t)$ step conditioning is the canonical mitigation for the hidden-state observability problem documented here
- [[universal-transformers]] — predecessor to cyclic recurrence; weight-tied blocks; cited as early fixed-point observation context
- [[experiments/exp1-router-replication]] — the experiment this page most directly informs; fixed-point finding is Technical Challenge 2 (hidden-state observability)
