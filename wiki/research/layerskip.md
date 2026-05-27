# LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding

A training recipe (layer dropout + early-exit loss with a shared LM head) that makes any prefix of transformer layers capable of producing useful outputs, enabling self-speculative decoding where early layers draft tokens and remaining layers verify — no auxiliary modules required. The method is applicable to pretraining from scratch, continual pretraining, and fine-tuning; it imposes a strong [[block-isolation-training]] pressure on later layers without making layers interchangeable.

## Method core

**Layer dropout** drops transformer layers stochastically per sample during training. For layer $l$ at training step $t$:

$$x_{l+1,t} = x_{l,t} + M(p_{l,t})\,f_l(x_{l,t})$$

where $M(p) \sim \text{Bernoulli}(1-p)$ is a per-sample mask. Dropout rate scales exponentially with depth:

$$p_{l,t} = S(t)\,D(l)\,p_{\max}, \qquad D(l) = e^{\frac{l \ln 2}{L-1}} - 1$$

so $D(0) = 0$ (first layer never dropped) and $D(L-1) = 1$ (last layer maximally dropped). For pretraining from scratch a curriculum $S_{\text{exp}}(t) = e^{\frac{t \ln 2}{T-1}} - 1$ ramps dropout up over time; for continual pretraining and fine-tuning, $S(t) = 1$.

**Early-exit loss** supervises a single shared LM head $g$ at every layer:

$$J(X,Y,t) = \sum_{l=0}^{L-1} \tilde{e}(t,l)\,J_{\text{CE}}(g(x_{l+1}), Y)$$

Loss weights $e(l)$ grow quadratically (later layers get higher weight). Two curricula determine which layers receive loss per iteration: *rotational* ($C_{\text{rot},R}$ — every $R$-th layer, cycling) or *gradual* ($C_{\text{grad}}$ — enable from last layer inward). No per-layer auxiliary heads are added; the final LM head is reused at all exit points.

**Self-speculative decoding** at inference: run the first $E$ layers auto-regressively to draft $d$ tokens, then verify all $d$ tokens in parallel using layers $E$ through $L-1$. A **KVQ cache** (standard KV cache for layers $0..E{-}1$ plus the exit query at layer $E{-}1$) lets the verification stage start from layer $E$ without recomputing earlier activations. This is not applicable to off-the-shelf models — LayerSkip training is a prerequisite.

Key hyperparameters: $p_{\max}$, $e_{\text{scale}}$, $R$, choice of $S(t)$ and loss curriculum.

## Goal relevance

**G1 (block-isolation / swappable blocks):** Directly relevant. Layer dropout imposes a strong isolation pressure — each layer must produce useful residual-stream activations independently of whether downstream layers execute. The exponential schedule concentrates this on later layers. This is the closest existing work to "training blocks to be independently capable." Isolation here is *vertical* (prefix self-sufficiency), not modular-swap: layers are skippable prefixes, not interchangeable units.

**G2 (dynamic per-block parameters):** Not addressed. The paper varies block *execution*, not block parameters.

**G3 (token-conditional routing):** Relevant as baseline. Each token exits at a globally fixed layer $E$; per-token dynamic exit is explicitly listed as future work (citing [[calm]]). LayerSkip trains the necessary capability — any prefix works — but does not attach a learned router. The exit-layer choice is the simplest possible routing decision: a single integer threshold.

## Credibility

- arXiv 2404.16710 (April 2024; revised October 2024). FAIR / GenAI / Reality Labs, Meta. Not peer-reviewed conference publication as of the captured PDF.
- Code released: https://github.com/facebookresearch/LayerSkip.
- Ablation rigor is strong: LD-only vs EE-only vs LD+EE across four training regimes (continual pretraining, pretraining from scratch, code fine-tuning, task fine-tuning), model sizes 1B–13B, multiple tasks. KVQ cache reuse and training token scaling also ablated.
- Large-scale experiments (Llama3 8B on 419B tokens) are not casually replicable, but open-source code enables community reproduction at smaller scale.

## Empirical claims

- LayerSkip continual pretraining of Llama2 7B: middle-layer (layer 16) BoolQ 75.7% vs 62.2% baseline; NaturalQuestions 4.07% vs 0.055% baseline — order-of-magnitude improvement at half depth.
- Llama3 8B middle-layer perplexity on Wikipedia: ~110,000× baseline → 12.2 after continual pretraining on 419B tokens; last-layer MMLU regression 66.5 → 60.5.
- Self-speculative decoding speedups on H100: 1.34×–2.16× (summarization, coding, semantic parsing). Best: 2.16× on CNN/DM abstractive summarization with Llama2 7B pretrained from scratch.
- Middle-layer perplexity *increases* during standard pretraining as token count grows; early-exit loss reverses this. Layer dropout alone partially reduces the increase.
- TOPv2 fine-tuned 1.5B: early exit at layer 12 gives 79.4% EM vs 0% baseline at same depth; self-speculative decoding restores full 82.9% EM at 1.64× speedup.

## Open questions / failure modes

- **Last-layer regression:** Llama3 8B MMLU 66.5 → 60.5, HumanEval 37.8 → 28.7 after continual pretraining. Attributed to Llama3's higher baseline token count making early-layer representations harder to calibrate retroactively. No solution offered; pretraining from scratch is preferable when possible.
- **Hyperparameter sensitivity:** $p_{\max}$, $e_{\text{scale}}$, and $R$ require per-model/task tuning. No principled transfer rule is given; transferred hyperparameters may underperform.
- **No per-token routing:** Draft exit layer $E$ is fixed globally at inference. Pairing with a confidence criterion (e.g., [[calm]]) is acknowledged as future work and is the gap between LayerSkip and a full G3 system.
- **Requires weight modification:** Not applicable to off-the-shelf models. Contrast [[draft-and-verify]], which requires no weight changes (though it cannot reuse the KV cache between draft and verify stages because skipped layers are non-contiguous).
- **Deeper models harder to retrofit:** Llama3 findings suggest earlier adoption (pretraining from scratch) is preferable.
- Pretraining from scratch with layer dropout requires an increased learning rate — one more tunable.

## Source

- `raw/research/block-training-quantization/23-layerskip.md` (PDF capture)
- `raw/research/block-training-quantization/09-layerskip-abs.md` (arXiv abstract)

## Related

- [[sleb]] — block-elimination cousin; LayerSkip trains blocks to be skippable, SLEB removes them training-free
- [[block-isolation-training]] — concept anchor; layer dropout is a strong block-isolation training pressure
- [[token-conditional-routing]] — concept anchor; LayerSkip's exit-layer choice is the simplest possible routing decision
- [[layerdrop]] — classic structured-dropout precursor (Fan et al. 2020); LayerSkip extends with depth-dependent schedule and early-exit loss
- [[mod]] — Mixture-of-Depths; learned per-token routing through layers, cited as a closer G3 approximation than LayerSkip
- [[calm]] — confidence-based per-token early exit; LayerSkip's natural router pairing (cited as future work in the paper)
- [[draft-and-verify]] — speculative decoding alternative that skips non-contiguous layers without weight modification
