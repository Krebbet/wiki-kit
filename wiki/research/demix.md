# DEMix Layers: Disentangling Domains for Modular Language Modeling

DEMix (Gururangan et al., 2021) replaces every FFN sublayer in an autoregressive transformer with a collection of domain-specialist FFN experts — one per training domain — routed deterministically at the document level. Attention and embedding parameters are shared; all domain-specific capacity lives in the FFN experts. The result is a model that is explicitly modular at FFN granularity: experts can be added post-training, initialised from a nearest-domain neighbour, trained in isolation, or removed without touching any other component. At inference, when the domain is known the routing is a hard selector; when unknown it becomes a parameter-free Bayesian posterior over expert likelihoods.

## Method Core

Each DEMix layer replaces the standard sublayer $\mathbf{h}_{t,\ell} = \text{FFN}(\mathbf{h}_{t,\ell-1})$ with the general MoE formulation

$$\mathbf{h}_{t,\ell} = \sum_{j=1}^{n} g_j(\mathbf{h}_{t,\ell-1}) \cdot \text{FFN}_j(\mathbf{h}_{t,\ell-1})$$

During training the routing weights collapse to a hard indicator on the document's domain label $d \in D$:

$$g_j(\mathbf{h}_{t,\ell}) = \begin{cases} 1 & \text{if } j = d \\ 0 & \text{otherwise} \end{cases}$$

All tokens in a sequence share the same expert; there is no per-token routing decision. Every FFN layer is replaced — interleaving shared and expert layers was found to hurt heterogeneous domains. Each $\text{FFN}_j$ is a two-layer MLP of the same dimensions as the original FFN; at 125M–1.3B params/GPU the total parameter count is $8\times$ the base FFN budget while FLOPs/GPU and throughput remain comparable to dense training (GPUs are partitioned by domain, reducing all-reduce scope from $n$-GPU to $(n/8)$-GPU).

At inference, when the domain is unknown or mixed, $g_j$ becomes a posterior:

$$g_j = p(D_t = j \mid \mathbf{x}_{<t}) = \frac{p(\mathbf{x}_{<t} \mid D_t = j) \cdot p(D_t = j)}{\sum_{j'} p(\mathbf{x}_{<t} \mid D_t = j') \cdot p(D_t = j')}$$

Three prior strategies are evaluated: **uniform** (no adaptation), **updating** (exponentially-weighted moving average of posteriors), and **cached** (prior estimated from ~100 held-out sequences of the target distribution). Cached prior is consistently best; smaller DEMix models match larger dense baselines on novel domains under this strategy.

## Goal Relevance

**G1 (block-isolation / swappable components) — direct.** Each expert is trained with no gradient flow to or from other experts through the FFN, making DEMix the clearest FFN-granularity analogue of isolated-block training. Post-training modularity operations are formally defined: *add* (initialise new expert from nearest neighbour, train in isolation, freeze everything else; ~10% of full DAPT compute, no forgetting); *remove* (deactivate expert, route via remaining mixture; zero retraining); *mix* (Bayesian ensemble; no new parameters).

**G3 (token-conditional routing) — negative result / contrast case.** DEMix deliberately avoids learned per-token routing. Routing is domain-conditional and deterministic during training; at inference the weights are a parameter-free posterior, not a learned softmax router. The paper frames this as the key distinction from [[token-conditional-routing]] approaches (Switch Transformer, GShard). Combining domain-level and per-token routing is listed as future work. DEMix is therefore a useful ablation axis: modularity benefits without routing complexity, at the cost of requiring domain labels.

**G2 (dynamic parameter allocation) — not addressed.**

## Credibility

Peer-reviewed arXiv preprint (2021); UW / FAIR / AI2 authorship. Code publicly released at https://github.com/kernelmachine/demix. Results span 125M–1.3B parameter scales across eight training and eight held-out domains.

## Empirical Claims

- In-domain perplexity (avg across 8 training domains): DEMix matches or beats dense at all tested scales; gains are clearest at 125M. Heterogeneous domains (WEBTEXT, REALNEWS, REDDIT) sometimes prefer dense, suggesting coarse provenance labels can be suboptimal.
- Novel-domain perplexity (8 held-out domains): DEMix with cached prior outperforms all dense baselines; largest gain on TWEETS (~67% improvement across model sizes).
- DEMIX-DAPT vs. DENSE-DAPT: DEMix-DAPT prevents catastrophic forgetting entirely (original-domain PPL unchanged) while matching or beating DENSE-DAPT on the target domain for domain-aligned targets (CORD-19, ACL PAPERS).
- Expert removal: perplexity on the removed domain rises to near-parity with a model retrained from scratch without that domain. Full forgetting is not achieved — shared attention and embeddings retain residual domain signal.

## Open Questions / Failure Modes

- Requires explicit domain labels at training time; granularity of provenance metadata matters and coarse labels can be suboptimal (WEBTEXT/REALNEWS/REDDIT result).
- Shared attention and embeddings are exposed to all domains — expert removal cannot guarantee full domain erasure.
- Evaluation limited to autoregressive LM perplexity; no downstream task results.
- Scaling behaviour of domain-conditional routing vs. dense and vs. learned-routing MoE at frontier scale is unknown; experiments cap at 1.3B params/GPU.

## Source

- `raw/research/selective-replacement-and-training/28-demix.md` (PDF capture)
- `raw/research/selective-replacement-and-training/09-demix-abs.md` (arXiv abstract)

## Related

- [[btm]] — full-model granularity analogue: BTM trains entirely separate expert LMs per domain with no shared parameters; DEMix is the within-model FFN-layer version with shared attention
- [[btx]] — learned-routing variant built on BTM's expert bank; per-token routing where DEMix uses domain-conditional deterministic routing
- [[sparse-upcycling]] — dense-init MoE alternative: also converts dense FFNs into expert pools but starts from a pretrained checkpoint and uses learned token routing
- [[mod]] — token-routing alternative using depth-routing (early exit / layer skipping) rather than expert specialisation
- [[block-isolation-training]] — FFN-granularity isolated training; DEMix implements the strongest form — each expert sees only its own domain's gradient
- [[token-conditional-routing]] — domain-conditional routing flavour: DEMix is a deliberate counter-example (deterministic domain label, not learned per-token)
- [[modular-deep-learning]] — survey context; DEMix is a concrete instance of the add/remove/compose modularity ideal at FFN granularity
