# ShortGPT: Layers in Large Language Models are More Redundant Than You Expect

ShortGPT introduces **Block Influence (BI)**, a training-free per-block importance metric derived from the cosine similarity between a transformer block's input and output hidden states in the residual stream. Blocks whose input/output representations are nearly identical contribute minimally to the representation and can be deleted outright. The full pruning pipeline is one-shot: compute BI on a calibration set, rank blocks ascending, remove the $k$ lowest. An optional post-training variant inserts lightweight MLP stubs in place of removed blocks and continues training. Evaluated on LLaMA 2 (7B, 13B), Baichuan2 (7B, 13B), RWKV-7B, and Mamba-2.8B, ~25% parameter removal retains ~87–92% of dense-model performance, consistently outperforming LLMPruner, SliceGPT, and LaCo at comparable sparsity ratios. Redundancy concentrates in middle-to-late layers; early layers and the final FFN (acting as part of the token classifier) are disproportionately important.

## Method core

### Block Influence (BI) — §3.1, Eq. 1

$$
\mathrm{BI}_i = 1 - \mathbb{E}_{X,t} \frac{X_{i,t}^\top X_{i+1,t}}{\|X_{i,t}\|_2 \|X_{i+1,t}\|_2}
$$

$X_{i,t}$ is the $t$-th token's hidden state entering block $i$; $X_{i+1,t}$ is the state leaving it (i.e., entering block $i+1$). The expectation is over calibration samples and sequence positions. BI is therefore $1 - \cos(X_i, X_{i+1})$: zero means a pure identity pass-through; one would mean the block inverts the hidden-state direction. Lower BI → higher similarity → remove first.

Under pre-LN (RMSNorm), hidden-state norm grows as $\|x_L\| = \Theta(\sqrt{L})$ while each block's residual contribution is $O(1)$ w.r.t. depth, giving $\cos(X_{L+1}, X_L) \geq \Theta\!\left(\sqrt{L/(L+1)}\right) - O\!\left(\sqrt{1/(L+1)}\right)$ — similarity approaches 1 for deep layers even at random initialisation (Appendix A). This explains why middle-to-late layers dominate the low-BI tail.

### One-shot layer removal (§3.2)

1. Collect hidden states on calibration set (PG19).
2. Compute BI per block via Eq. 1.
3. Sort ascending by BI; delete the $k$ lowest in one shot — no weight surgery.
4. **Optional (§4.6):** replace each removed block with a gated MLP stub (hidden size 2048) and continue training on 50B tokens with cosine LR.

## Goal relevance

| Goal | Relevance | Notes |
|---|---|---|
| **G1** — train isolated/swappable blocks | **Direct** | BI identifies blocks replaceable with nothing; §4.6's stub-insertion is structurally the same as [[block-isolation-training]]'s block-replacement primitive. |
| **G2** — per-block dynamic parameter allocation | **Adjacent** | BI is a per-block importance scalar; directly transferable as a budget signal (high-BI blocks get more parameters). Not the paper's framing. |
| **G3** — token-conditional routing | Not relevant | Pruning is static — same layers removed for all inputs. |

## Credibility

Published arXiv 2403.03853 (March 2024). Evaluates on four model families including non-transformer architectures (RWKV, Mamba). Direct head-to-head against LLMPruner, SliceGPT, and LaCo at matched sparsity. Theoretical justification for high cosine similarity in pre-LN models (Appendix A) is sound for randomly initialised models; extension to trained models is empirical (Figure 2), not formally proved. Venue: arXiv preprint; peer review status unknown at capture date.

## Empirical claims

- **LLaMA 2-13B, 24.6% removed**: BI-ShortGPT 91.64% relative performance; LLMPruner 70.67%, SliceGPT 63.20%, LaCo 86.36%.
- **LLaMA 2-7B, 27.1% removed**: 86.31% retention; XSum collapses to near-zero (generative task fragility — acknowledged limitation).
- **Non-transformer**: RWKV-7B and Mamba-2.8B support BI-based removal (Table 3); RWKV shows less inherent redundancy than Mamba or transformer models.
- **Quantisation orthogonality**: applying GPTQ before or after ShortGPT is additive (Tables 4–5).
- **Removed layers cluster in middle-to-late stack** (Table 9): LLaMA-2-7B removes layers 21–29 of 32.
- **Post-training recovery** (§4.6, Table 6): stub-insert + 50B token retraining partially recovers generative-task performance; tested only at 24% sparsity on LLaMA 2-7B.

## Open questions / failure modes

- Generative tasks (XSum, C3) are brittle at 25% pruning for 7B models; larger models (13B) more resilient. Cause: accumulated error in removed middle layers amplified over generation steps.
- Appendix A theory covers random initialisation only; no formal guarantee that the BI ordering is preserved through training dynamics.
- Post-training recovery not evaluated beyond LLaMA 2-7B at ~24% sparsity.
- BI does not distinguish between attention heads and FFN sub-blocks within a layer — importance is assigned at the whole-block level.

## Conflict with [[sleb]]

ShortGPT §3.1 / Eq. 1 defines BI as the sole importance metric and §4.3 (Figure 5) benchmarks it against Relative Magnitude, Norm/Reverse-order, and Sequential baselines — **perplexity-delta is not a competitor in §4.3**. ShortGPT concludes BI is best among metrics tested.

[[sleb]] (ICML 2024) explicitly evaluated input/output angular similarity as "Metric¹" — the cosine equivalent of ShortGPT's BI — and found it inferior to perplexity-based scoring ("Metric²/³") on their calibration setup. SLEB chose perplexity-delta as its primary importance criterion, explicitly demoting the cosine approach.

The conflict is not contradictory evidence — it is a **missing head-to-head**: ShortGPT never compares BI against PPL-delta; SLEB never uses the BI name but tests the equivalent. Different model families, calibration sets, and eval suites further complicate direct comparison. Both papers are internally consistent; the disagreement lives in the gap between their experimental designs.

See [[conflicts/shortgpt-vs-sleb-redundancy-metric]] for the full conflict record and resolution status.

## Source

- `raw/research/selective-replacement-and-training/24-shortgpt.md` — PDF capture (arXiv:2403.03853, captured 2026-04-30)
- `raw/research/selective-replacement-and-training/15-shortgpt-abs.md` — arXiv abstract

## Related

- [[sleb]] — CONFLICT TARGET (redundancy-metric disagreement; see [[conflicts/shortgpt-vs-sleb-redundancy-metric]])
- [[iterative-layer-distill]] — direct successor (extends ShortGPT with iterative removal + KL+MSE distillation per removal step)
- [[sheared-llama]] — LLM-scale structured-pruning sibling (end-to-end with dynamic batch loading; contrasts with ShortGPT's training-free one-shot approach)
- [[layerskip]] — orthogonal alternative (skip pressure applied during training rather than post-hoc static removal)
- [[block-isolation-training]] — concept anchor (§4.6 stub-insert + retrain is a degenerate instance)
- [[modular-deep-learning]] — survey context
