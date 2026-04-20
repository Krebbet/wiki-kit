# Reinforcement Learning Fine-Tunes a Sparse Subnetwork in Large Language Models

Balashov (preprint, July 2025) shows that RL fine-tuning of LLMs — across PPO, GRPO, ORPO, KTO, DPO, SimPO, PRIME — touches only **5–30% of parameters**, with the remaining 70–95% unchanged within numerical tolerance. The updated subnetwork is reproducible across seeds, datasets, and even algorithms, and freezing all other weights and re-training just that subnetwork recovers (and sometimes exceeds) full fine-tuned performance. Updates are sparse but *full-rank within each layer*.

## Method

- **Sparsity measurement.** Compute `s = #{i : |θ_full,i − θ_init,i| < τ} / |θ|` with τ = 1e-5 (float16). Per-layer and per-matrix variants (W_Q, W_K, W_V, MLP, LayerNorm) computed separately.
- **Subnetwork extraction.** Build binary mask `m_i = 𝟙[(θ_full − θ_init)_i ≠ 0]`, then re-fine-tune from θ_init with gradients masked: `g ← g ⊙ m`. Compare θ_sub vs θ_full on (i) win-rate / accuracy, (ii) fraction of weights matching within tol, (iii) L2 distance.
- **Update-rank analysis.** SVD of ΔW per layer; report rank as % of full rank.
- **Overlap analysis.** Compute one-sided overlaps `o_1 = |m^(1) ∧ m^(2)| / |m^(1)|` across seeds/datasets/algorithms vs random baseline `(1−s_1)(1−s_2)`.
- **Causal probes.** Toggle KL regularisation, gradient clipping, on-policy vs off-policy data to isolate driver of sparsity.

## Claims

- Sparsity (Table 1, % weights unchanged after RL): Tulu-3 8B DPO 76.0; Tulu-3 70B DPO 87.6; Eurus-2 7B PRIME 95.2; DeepSeek-Math 7B GRPO 75.0; Llama-3 8B KTO 68.1; SimPO 75.0; ORPO 79.4; PPO 62.6; MathShepherd PPO 80.8. SFT counterparts sit at 6–15% sparsity (Fig 1).
- Update rank (Table 2): >99% of full rank on average across Tulu-3 (DPO), Eurus-2 (PRIME), Llama-3 (KTO), DeepSeek-Math (GRPO). Min-layer rank ≥91%. *Not low-rank* — distinct from LoRA's inductive bias.
- Subnetwork-only retraining (Table 3, "Conjecture 1"): θ_sub matches θ_full; PRIME case θ_sub 72.2% vs θ_full 69.8% on math test, level-5 hardness 45.5% vs 40.3%. >99.9% of θ_sub weights within 1e-4 of θ_full.
- Cross-seed mask overlap ~60% vs ~20% chance; cross-algorithm overlap 30–60% vs <15% chance (Fig 6, Sec 5).
- LayerNorm parameters are ~100% unchanged across the board (Fig 3a). Sparsity is otherwise uniform across layers.
- Driver: on-policy/near-on-policy data distribution. Removing KL or clipping does not meaningfully densify updates (Sec 6).
- Transient updates peak mid-training then revert; final mask stabilises (Fig 5).

## Sample efficiency

Not the focus of the paper, but the implication is sharp: RL post-training is a *targeted micro-edit*, not a re-parameterisation. Performance-equivalent fine-tunes can in principle be obtained by training only the right ~10–30% of weights — which is also why RLHF preserves pretraining knowledge better than SFT. For single-sample regimes, this means the search problem is "find the small set of weights that encode the concept" rather than "diffuse the concept across the network."

## Relevance to the project

Strong empirical license for David's design: a concept-based learner does not need to update most of the model. The fact that the same subnetwork emerges across seeds and even across algorithms suggests an *intrinsic alignment-relevant subspace* in the pretrained model — analogous to a lottery ticket for behavioral alignment. Practical levers: (1) run a short RL probe to identify the mask, then restrict subsequent single-sample updates to it; (2) treat the sparse-but-full-rank pattern as a constraint distinguishing this approach from LoRA-style low-rank PEFT; (3) the ~100% LN preservation is a useful sanity floor for any custom optimiser.

## Source

- arXiv: 2507.17107
- Raw markdown: `../../../raw/research/single-sample-llm-learning/05-05-rl-sparse-subnetwork.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/05-rl-sparse-subnetwork.pdf`

## Related

- [[deepseekmath-grpo]] — one of the seven algorithms exhibiting the sparsity
- [[learning-to-think]] — uses low-rank Fisher proxy that aligns with the sparse-update geometry
- [[rstar-math]], [[math-shepherd]] — PRIME-style process-reward methods studied here
