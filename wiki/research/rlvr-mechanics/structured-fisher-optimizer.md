# Towards Efficient Optimizer Design for LLM via Structured Fisher Approximation with a Low-Rank Extension

Gong et al. (Microsoft Research, Feb 2025, arXiv:2502.07752) propose structured Fisher information matrix (FIM) approximation as a systematic framework for designing memory-efficient LLM optimizers. The framework unifies Adam, Shampoo, and gradient normalization under different structural assumptions, and introduces RACS and Alice—two new optimizers achieving 2× speedups over Adam while maintaining comparable memory with reduced overhead.

## Method

Structured FIM approximation solves: min_F̃ ∈ H ||F̃ − F||²_F, where H encodes structural constraints (diagonal, Kronecker product, block diagonal). Natural gradient descent updates W ← W − λ Mat(F̃^{-1/2} ∇_θ L).

**RACS** (Row and Column Scaled SGD): Assumes H = {S ⊗ Q} with S, Q positive diagonal matrices. Solves via fixed-point iteration (Eq. 16) with 1-step power iteration, yielding row-column scaling at SGD-like memory m + n + 1.

**Alice**: Low-rank extension of Eigen-Adam (which uses block diagonal structure with shared eigenspace). Three-step framework: (1) **Tracking** (Eq. 17): project to rank-r subspace, reduce m² → r² memory; (2) **Switching** (Prop. 4, Alg. 2): mix leading eigenvectors with QR-complement basis to explore degenerate subspaces; (3) **Compensation** (Thm. 5.1, Eq. 20): full-rank update via diagonal scaling S of residual gradient in complement subspace. Update interval K amortizes eigenvalue decomposition cost. Alice-0 disables tracking for further efficiency.

## Claims

- Adam is optimal diagonal approximation to FIM (Prop. 1); Shampoo minimizes upper bound with Kronecker structure (Thm. 3.1); normalization/whitening are special cases of block diagonal structures (Prop. 2, Sec. 3.3).
- Alice achieves >2× speedup (training steps) vs. Adam across 60M–1.3B LLaMA: 2.22×, 2.00×, 2.45×, 2.82× (Table 2, rows 11–12).
- Effective throughput (wall-clock) >2× for Alice on 1B: 123,048 vs. 53,588 tokens/sec for Adam (Table 2, rows 15–16).
- RACS outperforms Apollo-mini/svd on 350M and 1.3B without explicit tracking; 1B RACS (2.98G memory) matches 7B 8-bit-Adam quality in 3.8 days vs. Apollo's 15 days (Table 4).
- Alice reaches on-par or better eval perplexity than 7B Apollo-trained model with 1B model and less memory (Table 4, Fig. 1).
- Ablations: switching strategy outperforms Gaussian/full-basis variants (Fig. 5b); optimal compensation beats heuristic Fira (Fig. 5c); tracking contributes stability but not critical when compensation enabled (Table 5).

## Relevance to the project

**Systematic FIM view.** This paper provides a unifying lens for second-order optimization via structured approximation, making explicit the connection between structural assumptions and optimizer behavior. For L2T's Fisher/SVD reward proxy ([[../rlvr-mechanics/learning-to-think]]), this work asks: *can we use cheaper/more-scalable Fisher approximations as a reward signal at LLM scale?* The answer is **partially affirmative but with important caveats.** RACS and Alice are *approximations to the full Fisher-based NGD*, not exact Fisher computation; they trade approximation quality for memory/speed. If your reward signal requires true Fisher structure (e.g., for uncertainty/importance weighting), simpler low-rank surrogates like RACS may be insufficient. However, Alice's compensation term (Eq. 20) does recover some full-rank information via orthogonal complement scaling—potentially richer than pure diagonal methods. **The paper does not address reward design or RL fine-tuning**; it is purely an optimization method for pretraining. Scaling from 1.3B to typical RL-scale models (13B+) is not empirically validated here.

**Efficiency at deployment scale.** The structured FIM view may inspire cheaper proxies for computing Fisher-based penalties or attention masks during single-sample updates. GaLore (shown equivalent to low-rank Eigen-Adam in Sec. 5.4) is already widely used; Alice shows measurable gains but at 1B scale. For concept-based fine-tuning on single samples, Fisher-weighted sparsity (e.g., mask which parameters to update) could leverage Alice's low-rank projections U_t to identify salient subspaces.

## Source

- arXiv: 2502.07752
- Raw markdown: `../../../raw/research/adjacent-reward-signals/04-structured-fisher-llm-optimizer.md`
- Raw PDF: `../../../raw/research/adjacent-reward-signals/pdfs/structured-fisher-llm-optimizer.pdf`

## Related

- [[learning-to-think]] — Fisher/SVD as reward signal; Alice offers approximate but scalable Fisher computation
- [[rl-sparse-subnetwork]] — low-rank projections (U_t, Alice's switching) as subnetwork selectors
- [[deepseekmath-grpo]] — fast adaptive optimizers enable efficient RL fine-tuning
