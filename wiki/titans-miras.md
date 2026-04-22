# Titans + MIRAS

Google Research blog (Behrouz, Razaviyayn, Mirrokni; Dec 2025) consolidating two coupled contributions: **Titans** (arXiv:2501.00663) — an architecture with a deep-MLP long-term memory module that performs *test-time memorization* driven by a gradient-based "surprise" signal — and **MIRAS** (arXiv:2504.13173) — a unifying framework that recasts sequence models as associative-memory optimizers and admits non-MSE attentional biases.

## Method

**Titans architecture.** Augments attention with a *neural long-term memory module* implemented as a multi-layer perceptron whose parameters are updated *online during inference*. Update rule uses a "surprise" signal = the gradient of a memorization loss between the module's current prediction and the new key/value pair; large gradients (high surprise) trigger stronger writes. Two refinements:
- **Momentum** term fusing momentary and past surprise so non-surprising follow-on tokens linked to a surprising event are also retained.
- **Adaptive weight-decay forgetting gate** that bounds capacity in long streams.

The reference variant (**MAC** = Memory As Context) composes three layers — Contextual Memory (online-learned), Core (in-context attention), and Persistent Memory (fixed weights) — letting attention decide whether to consult the long-term summary.

**MIRAS framework.** Defines any sequence model by four design choices:
1. Memory architecture (vector / matrix / deep MLP).
2. Attentional bias (the inner objective the memory optimizes).
3. Retention gate (forgetting reframed as a regularizer balancing new vs past state).
4. Memory algorithm (the gradient-based optimizer used).

MIRAS argues virtually all prior models (Transformers, linear RNNs, SSMs) collapse to MSE / dot-product bias + retention; MIRAS opens non-Euclidean alternatives. Three concrete instantiations:
- **YAAD** — Huber-loss bias for outlier robustness.
- **MONETA** — generalized p-norm bias and retention.
- **MEMORA** — constrains memory to a probability-simplex map for stable updates.

Derives from Transformer attention, linear RNNs, Mamba-2, Gated DeltaNet, LongMem-style external memory, and the broader fast-weights / TTT lineage. Companion line: Google's [[nested-learning]] continual-learning paradigm.

## Results

Reported in the blog (numerical specifics deferred to the two arXiv papers):
- **LM (C4, WikiText) + zero-shot reasoning (HellaSwag, PIQA):** Titans and MIRAS variants beat Transformer++, Mamba-2, and Gated DeltaNet at "comparable sizes". No exact deltas in the post.
- **Memory-depth ablation (360M and 760M):** deeper memory MLPs ("LMM") yield monotonically lower perplexity than shallow memory ("MM") and Mamba as sequence length grows.
- **BABILong long-context reasoning:** Titans (MAC)-FT reportedly outperforms *all* baselines including GPT-4 despite "many fewer parameters", scaling to context windows >2M tokens.
- **Generalization:** validated on DNA / genomic sequences and time-series forecasting in addition to text.
- **Efficiency:** training remains parallelizable; inference is linear-time.

No parameter / token / FLOP totals are stated in the blog itself.

## Applicability

- Projects needing very long contexts (multi-document QA, full-codebase reasoning, genomics, long time series) without paying quadratic attention cost.
- Online / continual adaptation without offline fine-tuning — memory updates live during inference.
- Drop-in candidate where teams currently use Mamba-2, Gated DeltaNet, or RWKV-style linear recurrences.
- **Inference engineering caveat:** serving requires per-sequence mutable weights for the memory module, which complicates batched / KV-cache deployments.

Prerequisites: pretraining-class compute (comparison at 360M / 760M+ scale); a base codebase capable of online parameter updates inside the forward pass; no special RL infrastructure.

## Novelty

- New-ish primitive: framing forgetting as a *regularizer* in a unified online-optimization view; non-MSE / non-dot-product attentional biases (Huber, p-norm, simplex-projected). MIRAS as a taxonomy is the bigger conceptual contribution.
- Recombination: deep-MLP memory + gradient-driven write gating builds on TTT, fast-weight programmers, and external memory networks (LongMem cited).
- Closest prior: Mamba-2 and Gated DeltaNet (efficiency); LongMem and Transformer-XL-style memory (long context). What changed: replacing fixed-size compressed state with a *learnable network* trained online via a surprise gradient.

## Reproducibility

Two arXiv preprints (2501.00663 Titans, 2504.13173 MIRAS), neither journal-vetted. Blog links no code repo or weights release; no PapersWithCode entry mentioned. **Headline numbers (esp. "beats GPT-4 on BABILong") should be treated as unreplicated until weights or third-party runs surface.**

## Adoption

Google Research authorship; Titans paper had ~10 months in the wild before this consolidation. Blog references the sibling [[nested-learning]] paradigm, suggesting a coordinated Google Research push on continual / long-memory architectures. No external adopter citations in the post.

## Source

- `raw/research/radar-2026-04/01-05-titans-miras.md` — Google Research blog "Titans + MIRAS: Helping AI have long-term memory" (Dec 4, 2025). Captured 2026-04-22.

## Related

- [[test-time-training]] — Titans is the flagship "online parameter updates during inference" example; cluster page covers Titans, Hope, In-Place TTT.
- [[nested-learning]] — sibling Google Research paradigm; Hope = self-modifying Titans + CMS.
- [[conflicts/long-context-attention-vs-recurrent-memory]] — Titans' "beats GPT-4 on BABILong" claim.
- [[watchlist]] — Mamba-2, Gated DeltaNet, LongMem, BABILong referenced but not captured.
