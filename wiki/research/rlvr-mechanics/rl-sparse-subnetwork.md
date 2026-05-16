# Reinforcement Learning Fine-Tunes a Sparse Subnetwork in Large Language Models

Balashov (preprint, July 2025) shows that RL fine-tuning of LLMs — across PPO, GRPO, ORPO, KTO, DPO, SimPO, PRIME — touches only **5–30% of parameters**, with the remaining 70–95% unchanged within numerical tolerance. The updated subnetwork is reproducible across seeds, datasets, and even algorithms, and freezing all other weights and re-training just that subnetwork recovers (and sometimes exceeds) full fine-tuned performance. Updates are sparse but *full-rank within each layer*.

## Method

- **Sparsity measurement.** Compute $s = \#\{i : |\theta_{\text{full},i} - \theta_{\text{init},i}| < \tau\} / |\theta|$ with $\tau = 1\text{e-}5$ (float16). Per-layer and per-matrix variants ($W_Q, W_K, W_V$, MLP, LayerNorm) computed separately.
- **Subnetwork extraction.** Build binary mask $m_i = \mathbb{1}[(\theta_\text{full} - \theta_\text{init})_i \neq 0]$, then re-fine-tune from $\theta_\text{init}$ with gradients masked: $g \leftarrow g \odot m$. Compare $\theta_\text{sub}$ vs $\theta_\text{full}$ on (i) win-rate / accuracy, (ii) fraction of weights matching within tol, (iii) L2 distance.
- **Update-rank analysis.** SVD of $\Delta W$ per layer; report rank as % of full rank.
- **Overlap analysis.** Compute one-sided overlaps $o_1 = |m^{(1)} \wedge m^{(2)}| / |m^{(1)}|$ across seeds/datasets/algorithms vs random baseline $(1-s_1)(1-s_2)$.
- **Causal probes.** Toggle KL regularisation, gradient clipping, on-policy vs off-policy data to isolate driver of sparsity.

## Claims

- Sparsity (Table 1, % weights unchanged after RL): Tulu-3 8B DPO 76.0; Tulu-3 70B DPO 87.6; Eurus-2 7B PRIME 95.2; DeepSeek-Math 7B GRPO 75.0; Llama-3 8B KTO 68.1; SimPO 75.0; ORPO 79.4; PPO 62.6; MathShepherd PPO 80.8. SFT counterparts sit at 6–15% sparsity (Fig 1).
- Update rank (Table 2): >99% of full rank on average across Tulu-3 (DPO), Eurus-2 (PRIME), Llama-3 (KTO), DeepSeek-Math (GRPO). Min-layer rank ≥91%. *Not low-rank* — distinct from LoRA's inductive bias.
- Sparsity vs rank are orthogonal axes of $\Delta W$. LoRA forces $\Delta W = AB$ with $\text{rank}\le r \ll \min(m,n)$ and dense support in $A,B$ — updates live in a low-dim subspace per layer. Balashov's RL updates have sparse support (5–30% nnz) but $\text{rank}(\Delta W) \approx \min(m,n)$ — the same nominal trainable-parameter savings as LoRA, but reached by entry-level sparsity rather than rank reduction. The authors call this "sparse but full-rank": "RL updates a small number of parameters that collectively span a high-dimensional subspace of each layer's weight space" — capable of representing nearly the full range of weight-space changes, just with far fewer nonzeros than a dense update. They frame this as RLHF acting as *implicit PEFT* (parallel to adapters/LoRA but by discovery, not design).
- Subnetwork-only retraining (Table 3, "Conjecture 1"): $\theta_\text{sub}$ matches $\theta_\text{full}$; PRIME case $\theta_\text{sub}$ 72.2% vs $\theta_\text{full}$ 69.8% on math test, level-5 hardness 45.5% vs 40.3%. >99.9% of $\theta_\text{sub}$ weights within 1e-4 of $\theta_\text{full}$.
- Cross-seed mask overlap ~60% vs ~37% chance; cross-algorithm overlap 30–60% vs <15% chance (Fig 6, Sec 5).
- Cross-domain (dataset) overlap, the most relevant variation for "is the alignment subnetwork shared across tasks": Tulu-3-8B + DPO trained on Tulu preference (dialogue alignment) vs PRIME rollouts (math-reasoning alignment) gives one-sided overlaps $o_1 = 26.7\%$, $o_2 = 67.1\%$ (asymmetric — sparsities $s_1 = 85.4\%, s_2 = 63.3\%$) vs chance $14.6\%, 36.7\%$ (Table 4). Above chance but markedly lower than same-data cross-seed; the authors call this a "partially consistent core subnetwork." Math vs reading-comprehension specifically is *not* tested; the authors speculate more off-distribution targets (e.g. teaching code from a non-code base) would lower both sparsity and overlap.
- LayerNorm parameters are ~100% unchanged across the board (Fig 3a). Sparsity is otherwise uniform across layers.
- Driver: on-policy/near-on-policy data distribution. Removing KL or clipping does not meaningfully densify updates (Sec 6).
- Transient updates peak mid-training then revert; final mask stabilises (Fig 5).

## Sample efficiency

Not the focus of the paper, but the implication is sharp: RL post-training is a *targeted micro-edit*, not a re-parameterisation. Performance-equivalent fine-tunes can in principle be obtained by training only the right ~10–30% of weights — which is also why RLHF preserves pretraining knowledge better than SFT. For single-sample regimes, this means the search problem is "find the small set of weights that encode the concept" rather than "diffuse the concept across the network."

## Relevance to the project

Strong empirical license for David's design: a concept-based learner does not need to update most of the model. The fact that the same subnetwork emerges across seeds and even across algorithms suggests an *intrinsic alignment-relevant subspace* in the pretrained model — analogous to a lottery ticket for behavioral alignment. Practical levers: (1) run a short RL probe to identify the mask, then restrict subsequent single-sample updates to it; (2) treat the sparse-but-full-rank pattern as a constraint distinguishing this approach from LoRA-style low-rank PEFT — concepts built on LoRA inherit a low-rank-per-layer inductive bias the alignment geometry itself does not require, arguing for mask-based PEFT at full rank instead; (3) the $\approx 100\%$ LN preservation is a useful sanity floor for any custom optimiser.

### Capacity bound: shared-knob RL→RL forgetting

The same finding that makes RL *protective* for pretraining (only 5–30% of weights move) implies a second, distinct forgetting risk that the paper does not test: **alignments stack into a fixed-capacity subnetwork**. If alignment A and alignment B both express themselves through largely the same mask (cross-seed overlap ~60%, cross-algorithm 30–60%, cross-domain 27%/67% — all from this paper), then sequential RLVR(A)→RLVR(B) on the same base must resolve at the contested coordinates: B overwrites whatever A had written in $\text{mask}(A) \cap \text{mask}(B)$. LayerNorm being ~100% locked rules out spilling to extra capacity. Two distinct forgetting frames coexist:

- *RL → pretraining* (the paper's protective-sparsity story): pretraining sits in the inert 70–95%, so RL's footprint can't overwrite it. Forgetting here is reweighting, not deletion ([[../single-sample-rl-finetuning/1-shot-rlvr]], [[../single-sample-rl-finetuning/rlvr-incentivizes-reasoning]]).
- *RL → RL* (the unaddressed frame): prior alignments live *in* the active 5–30%, so a new RL alignment competes for the same coordinates. Out-of-phase update directions on shared entries flip them to B's preferred sign.

Sparse-but-full-rank matters here too: interference depends on whether A's and B's preferred $\Delta W$ directions are compatible, not on a low-dim collision — the active subnetwork has high intrinsic dimensionality but the mask still bounds *which* coordinates can move. The cross-domain (dialogue vs math) overlap of 27%/67% is the closest empirical proxy for "out-of-phase" alignments and identifies the candidate interference sites; the paper does **not** run sequential RLVR(A)→RLVR(B) and re-evaluate A. That is the missing experiment.

Project implications: (a) sequential single-sample concept fine-tunes on the same base will accumulate interference unless contested coordinates are anchored — motivates EWC-Fisher per prior concept ([[../catastrophic-forgetting/ewc-gemma2-cpt]], [[../synthesis/proposed-method]] component **F**) keyed on each concept's held-out set; (b) candidate scheme is mask-aware: discover $\text{mask}(A)$ during RLVR(A), freeze $\text{mask}(A) \cap \text{mask}(B)$ during RLVR(B), or restrict B to $\text{mask}(A)^c \cap \text{mask}_\text{RL}$; (c) concept capacity per base is bounded — the design must either route concepts to disjoint mask regions or adopt task-vector merging ([[../synthesis/single-sample-concept-skeleton]] gap list).

## Source

- arXiv: 2507.17107
- Raw markdown: `../../../raw/research/single-sample-llm-learning/05-05-rl-sparse-subnetwork.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/05-rl-sparse-subnetwork.pdf`

## Related

- [[deepseekmath-grpo]] — one of the seven algorithms exhibiting the sparsity
- [[learning-to-think]] — uses low-rank Fisher proxy that aligns with the sparse-update geometry
- [[rstar-math]], [[math-shepherd]] — PRIME-style process-reward methods studied here
- [[../selective-finetuning/_overview]] **(added 2026-05-13)** — full theme on selective fine-tuning / behaviour-isolation methods. Balashov observes RL *spontaneously* uses 5–30% of weights; this theme contains the methods that *enforce* the sparsity prescriptively. Direct cousins:
- [[../selective-finetuning/skill-localization]] — Panigrahi ICML 2023: 0.01% of params carry >95% of fine-tuned skill; the SFT analogue of Balashov's RL finding
- [[../selective-finetuning/packnet]], [[../selective-finetuning/hat]] — pre-LLM continual-learning ancestors that enforce sparsity by mask
- [[../selective-finetuning/o-lora]] — modern LLM-era: orthogonal LoRA subspaces per task
- [[../selective-finetuning/rome]], [[../selective-finetuning/memit]], [[../selective-finetuning/alphaedit]] — locate-then-edit: surgical rank-one MLP updates rather than diffuse fine-tuning
