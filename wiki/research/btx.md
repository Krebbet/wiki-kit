# Branch-Train-MiX: Mixing Expert LLMs into a Mixture-of-Experts LLM

BTX (Sukhbaatar et al., FAIR/Meta, arXiv 2403.07816) is a three-stage recipe for constructing a sparse MoE from independently trained expert LLMs. It unifies [[btm]] (parallel expert training without a mix stage) and [[sparse-upcycling]] (MoE fine-tune without independent expert pre-training) into a single pipeline that outperforms both. Starting from a pretrained seed model, each copy is domain-fine-tuned in full isolation, then the resulting FFN sublayers are installed as MoE experts while attention parameters are averaged; a short MoE fine-tune trains the per-layer router. The approach is embarrassingly parallel in the expert-training phase and introduces only negligible new parameters (the router matrices $W_l$).

## Method core

**Branch.** Copy a pretrained seed LLM $N$ times. In the paper: Llama-2 7B → 4 copies (math, code, Wikipedia, generalist).

**Train.** Fine-tune each copy independently on domain data $D_i$ using the standard LM objective. No inter-expert communication; fully asynchronous. This is [[block-isolation-training]] applied at whole-model granularity.

**MiX.**

- *FFN parameters:* Each expert's feedforward sublayer at layer $l$ becomes one expert in a per-layer MoE. The assembled layer computes

$$FF_{\text{MoE}}^l(x) = \sum_{i=1}^{N} g_i(W_l x)\; FF_i^l(x)$$

where $W_l$ is a learned linear router and $g$ is sparse: default Top-2 with $g(W_l x) = \mathrm{SoftMax}(\mathrm{TopK}(W_l x))$.

- *Attention + remaining parameters* (embeddings, layer norms): averaged across all $N$ experts. Motivation: attention is assumed less domain-specialised than FFN.

- *MoE fine-tune:* Assemble then continue-train on a mixture of all domain data (80B tokens in the paper). The router $W_l$ learns [[token-conditional-routing]]; averaged attention weights recover domain generality.

**Load-balancing loss** (Switch Transformer formulation):

$$\mathcal{L}_{\text{LB}} = \alpha N \sum_{i=1}^{N} u_i p_i$$

where $u_i$ is the fraction of tokens routed to expert $i$ in the batch and $p_i$ is the mean soft-router probability for expert $i$. Without load balancing the Math expert dominates and the Code expert collapses; load balancing rescues it at a minor cost to math scores.

**Router variants (ablation):**

| Routing | Active params | Notes |
|---------|--------------|-------|
| Switch Top-1 | 6.7 B | Worst; token dropping at capacity |
| Sample Top-1 (Gumbel) | 6.7 B | Temperature-annealed; efficient |
| **Top-2** | **11.1 B** | **Default; best accuracy–efficiency** |
| Soft (all experts) | 19.7 B | Best accuracy, highest cost |

## Goal relevance

**G1 (block-isolation / swappability).** The branch-train stage is block-isolation training at whole-expert granularity — each copy trains with no cross-expert gradient. Crucially, *freezing expert FFN weights during the MoE fine-tune has negligible performance impact*, confirming that domain knowledge installed by isolated training survives the mix step. Strong evidence for the swappability goal.

**G3 (token-conditional routing).** The central contribution over [[btm]]. The router $W_l$ is trained post-hoc in a short fine-tune, showing that [[token-conditional-routing]] through a pool of independently-trained FFN blocks is cheaply bootstrappable. Token routing shows partial domain specialisation: code tasks route to the Code expert; knowledge tasks to the Wikipedia expert; math tasks split between Math and Code (GSM8K prefers Code + baseline; symbolic MATH prefers Math).

**G2 (per-block parameter allocation).** Expert count $N$ and active-expert count $k$ are explicit design choices. Splitting experiments (§3.3, §4.3.1) show that naively doubling expert count without matching capacity hurts, constraining granularity choices for G2.

## Credibility

Primary paper (arXiv 2403.07816, March 2024), FAIR at Meta. Llama-2 7B seed, controlled against BTM, sparse upcycling, and dense continued pre-training on matching compute budgets. Ablations are thorough (router variant, freeze vs. unfreeze FFN, blend, split). No peer-review venue listed at capture date.

## Empirical claims

BTX Top-2 (Llama-2 7B seed, 4 experts) on average across Math / Code / Knowledge / Reasoning / MMLU:

| Model | Average |
|-------|---------|
| Llama-2 7B (seed) | 40.7 |
| Dense continued pre-train | 44.5 |
| Sparse upcycling Top-2 | 46.3 |
| BTM Top-2 | 43.4 |
| **BTX Top-2** | **47.9** |
| Llama-2 13B | 45.4 |

BTX Top-2 beats Llama-2 13B overall at less than half the additional compute. In a compute-matched scenario vs. [[sparse-upcycling]] (same GPU-days), BTX trains on 533 B tokens vs. 252 B, yielding 47.9 vs. 47.3 average score — the throughput advantage of the parallel branch-train stage is load-bearing.

Blending expert FFN chunks (interleaving domain parameters naively) destroys performance, confirming that FFN specialisation is spatially cohesive within each expert module.

## Open questions / failure modes

- Load balancing loss trades expert utilisation against per-domain peak performance — the Math/Code collapse-and-rescue dynamic suggests the loss coefficient $\alpha$ is a sensitive hyperparameter requiring tuning per domain mix.
- Attention averaging is assumed safe; paper does not ablate against averaging only a subset of layers or against keeping per-expert attention and merging via a separate router.
- Splitting (finer expert granularity) underperforms Top-2 at 4 experts — unclear whether this degrades because of routing capacity budget or because specialised FFN knowledge is not factored at sub-block granularity.
- All results on Llama-2 7B; generalisability to other scales and architectures (e.g., GQA, RoPE variants) not established.
- The "generalist" fourth expert is the unmodified seed — its contribution relative to a domain-fine-tuned replacement is not isolated.

## Source

- `raw/research/selective-replacement-and-training/27-btx.md` (PDF capture, arXiv 2403.07816)
- `raw/research/selective-replacement-and-training/08-btx-abs.md` (arXiv abstract)

## Related

- [[btm]] — predecessor; ensemble/averaging at inference instead of learned MoE routing
- [[sparse-upcycling]] — cousin; dense-copy then MoE fine-tune without independent branch-train
- [[demix]] — domain-conditioned routing alternative; deterministic, not learned per-token
- [[mod]] — different routing primitive; depth (layer skipping) instead of FFN-expert selection
- [[block-isolation-training]] — independent expert training as the block-isolation instantiation
- [[token-conditional-routing]] — learned per-token softmax router; BTX is a primary exemplar
- [[modular-deep-learning]] — survey context
