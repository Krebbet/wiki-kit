# Parameter-Efficient Transfer Learning for NLP (Houlsby Adapters)

Sequential bottleneck modules inserted into each Transformer layer of frozen BERT achieve within 0.4% of full fine-tuning on GLUE while training only ~3.6% as many parameters (1.3× total parameter footprint vs. 9× for full fine-tuning). Published at ICML 2019, this is the foundational PEFT baseline for NLP; the architectural pattern — a small inserted module, frozen backbone, per-task learned weights — defines the "adapter" lineage that subsequent methods (notably [[lora]]) react against.

## Method core

Two adapters per Transformer layer: one inserted after the multi-head attention output projection, one after the FFN output projection, both placed before the subsequent layer norm and residual add. Each adapter is a bottleneck:

$$h \leftarrow W_\text{up} \cdot \sigma(W_\text{down} \cdot h) + h, \quad W_\text{down} \in \mathbb{R}^{m \times d},\ W_\text{up} \in \mathbb{R}^{d \times m}$$

Parameter cost per adapter: $2md + d + m$; with $m \ll d$ this is $\approx 2md$. At $m=64$, $d=1024$ (BERT$_\text{LARGE}$): ~2.1% trained params across 24 layers.

The skip connection makes the module an approximate identity at init. **Initialization is critical:** weights drawn from $\mathcal{N}(0, 10^{-2})$ (truncated); performance degrades if init std exceeds $\sim 10^{-2}$.

Frozen: all original BERT weights. Trained: adapter weights + task-specific layer norms + classification head.

## Goal relevance

**G1 (swappable isolated blocks) — partial.** The adapter is an isolated inserted piece, not a replacement for the Transformer sublayer itself. The backbone residual stream is always active — the adapter modulates rather than replaces. This is a weaker form of block isolation: useful as a lower bound on what a tiny per-layer insert buys, and as a contrast when defining what full block isolation means. See [[block-isolation-training]].

**G2 (dynamic per-block parameter allocation) — partial.** Bottleneck dimension $m$ is a per-task, potentially per-layer, hyperparameter. The paper shows the optimal $m$ varies by task (e.g., 256 for MNLI, 8 for RTE) and that performance is robust across two orders of magnitude of adapter size (0.5%–8%). This is a static budget choice at training time, not dynamic allocation during inference — but it establishes that per-layer parameter budget is independently tunable.

**G3 (token-conditional routing) — not relevant.**

## Credibility

ICML 2019 (peer-reviewed, top-tier). Experiments on BERT$_\text{LARGE}$ (330M, 24 layers) across GLUE (9 tasks, test server), 17 additional classification tasks (BERT$_\text{BASE}$), and SQuAD v1.1. Seeds and hyperparameters swept; s.e.m. reported. Baselines include full fine-tuning, top-$k$ layer fine-tuning, layer-norm-only tuning, and an AutoML sweep (>10k models/task). Code released at `https://github.com/google-research/adapter-bert`.

Caveats: encoder-only (BERT), 2019 vintage. No decoder-only or autoregressive experiments. Concurrent work (PALs, Stickland & Murray 2019) uses a different architecture under multi-task training; comparison is indirect.

## Empirical claims

| Claim | Evidence | Confidence |
|---|---|---|
| Adapters within 0.4% of full fine-tuning on GLUE (80.0 vs. 80.4) at 3.6% trained params | GLUE test server, BERT$_\text{LARGE}$, sizes {8, 64, 256} | High |
| Fixed size 64 → 79.6 GLUE (–0.4) at 2.1% trained params | Same | High |
| 17-task suite: adapters 0.4% behind fine-tuning at 1.14% trained params/task (1.19× total vs. 17×) | Table 2, BERT$_\text{BASE}$, mean ± s.e.m. | High |
| SQuAD v1.1: F1 = 90.4 (adapters, size 64) vs. 90.7 (full fine-tune) | Validation set, Fig. 5 | High |
| Lower-layer adapters (layers 0–4) removable without significant MNLI drop | Ablation heatmap Fig. 6 — single task, no retraining | Medium (task-specific) |
| Near-identity init necessary; std $> 10^{-2}$ degrades performance | Robustness sweep over $[10^{-7}, 1]$ | High |
| Layer-norm-only tuning (40k params, BERT$_\text{BASE}$) is ~3.5–4% below full fine-tune | §3.4 comparison | High |
| SMS spam outlier: adapters 95.1 ± 2.2 vs. fine-tune 99.3 ± 0.2 | Table 2 | High |

## Open questions / failure modes

- **Decoder-only / autoregressive models:** All experiments encoder-only. Whether post-attn + post-FFN insertion points are optimal for causal LMs is unaddressed here; subsequent work (AdapterHub, LLM-Adapters) partially answers this but is out of scope.
- **Inference latency:** Sequential bottleneck adds forward-pass cost per token per layer. LoRA avoids this by merging weights at inference; adapters cannot. Relevant for deployment.
- **Layer-norm coupling:** Training task-specific layer norms alongside adapters creates coupling between backbone stats and adapter outputs — could cause instability when hot-swapping adapters across tasks at inference time.
- **Task interference:** Paper explicitly avoids multi-task settings. Whether shared-backbone adapters from different tasks interfere at inference is not studied.
- **Small-data instability:** SMS spam result suggests higher variance and lower accuracy on very small datasets with high baseline accuracy.
- **G1 relevance limit:** The skip connection means the backbone residual is always active. Adapter isolation is not block isolation; the adapter modulates, it does not replace.

## Source

- `raw/research/selective-replacement-and-training/26-adapters-houlsby.md` (PDF capture)
- `raw/research/selective-replacement-and-training/02-adapters-houlsby-abs.md` (arXiv abstract)

## Related

- [[lora]] — successor: parallel low-rank decomposition rather than sequential bottleneck; merges at inference, eliminating latency overhead; dominant PEFT method today
- [[bert-of-theseus]] — concurrent independent work (2019–2020); replaces whole modules rather than inserting bottlenecks; neither paper cites the other
- [[modular-deep-learning]] — canonical PEFT module in the survey's taxonomy; provides taxonomic context for the adapter lineage
- [[block-isolation-training]] — insert-and-train as weak block isolation; useful contrast for defining what full block replacement/swap means
