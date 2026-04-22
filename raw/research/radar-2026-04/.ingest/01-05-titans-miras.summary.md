---
source: "raw/research/radar-2026-04/01-05-titans-miras.md"
slug: "01-05-titans-miras"
summarized_on: "2026-04-22"
schema_version: 1
---

# Titans + MIRAS: Helping AI have long-term memory

## One-line
Google Research blog (Dec 4, 2025) introducing Titans (an architecture with a deep-MLP long-term memory module that performs test-time memorization driven by a gradient-based "surprise" signal) and MIRAS (a unifying theoretical framework that recasts sequence models as associative-memory optimizers and admits non-MSE attentional biases / retention gates).

<!-- DOMAIN-SLOT: takeaway-prompts -->
## Method
Two coupled contributions:

- **Titans architecture (arXiv:2501.00663)** — Augments attention with a *neural long-term memory module* implemented as a multi-layer perceptron whose parameters are updated *online during inference* (test-time memorization). Update rule uses a "surprise" signal = the gradient of a memorization loss between the module's current prediction and the new key/value pair; large gradients (high surprise) trigger stronger writes. Two refinements: (i) a **momentum** term that fuses momentary and past surprise so non-surprising follow-on tokens linked to a surprising event are also retained; (ii) an **adaptive weight-decay forgetting gate** that bounds capacity in long streams. The reference variant (MAC = Memory As Context) composes three layers — Contextual Memory (online-learned), Core (in-context attention), and Persistent Memory (fixed weights) — letting attention decide whether to consult the long-term summary.
- **MIRAS framework (arXiv:2504.13173)** — Defines any sequence model by four design choices: (1) memory architecture (vector / matrix / deep MLP), (2) attentional bias (the inner objective the memory optimizes), (3) retention gate (forgetting reframed as a regularizer balancing new vs. past state), (4) memory algorithm (the gradient-based optimizer used). MIRAS argues virtually all prior models (Transformers, linear RNNs, SSMs) collapse to MSE / dot-product bias + retention; MIRAS opens the door to non-Euclidean alternatives. Three concrete instantiations: **YAAD** (Huber-loss bias for outlier robustness), **MONETA** (generalized p-norm bias and retention), **MEMORA** (constrains memory to a probability-simplex map for stable updates).

Derives from / contrasts with: Transformer attention, linear RNNs, Mamba-2 (SSMs), Gated DeltaNet, LongMem-style external memory, and the broader "fast weights" / test-time training lineage. Companion line: Google's "Nested Learning" continual-learning paradigm (linked from the post).

## Results
Reported in the blog (numerical specifics deferred to the two arXiv papers; figures referenced):

- **Language modeling (C4, WikiText) + zero-shot reasoning (HellaSwag, PIQA)**: Titans and the MIRAS variants (YAAD, MONETA, MEMORA) beat Transformer++, Mamba-2, and Gated DeltaNet at "comparable sizes" on accuracy and perplexity (no exact deltas in the post).
- **Memory-depth ablation (Fig: 360M and 760M scales)**: deeper memory MLPs ("LMM") yield monotonically lower perplexity than shallow memory ("MM") and Mamba as sequence length grows.
- **BABILong long-context reasoning**: Titans (MAC)-FT reportedly outperforms *all* baselines including GPT-4 despite "many fewer parameters", and scales to context windows >2M tokens (Fig: accuracy vs. sequence length).
- **Generalization**: Validated on DNA / genomic sequences and time-series forecasting in addition to text.
- **Efficiency**: Training remains parallelizable; inference is linear-time.

No parameter / token / FLOP totals are stated in the blog itself.

## Applicability
- Projects that need *very long contexts* (multi-document QA, full-codebase reasoning, genomics, long time series) without paying quadratic attention cost.
- Projects exploring *online / continual adaptation* without offline fine-tuning — the memory module updates live during inference.
- A natural drop-in candidate where teams currently use Mamba-2, Gated DeltaNet, or RWKV-style linear recurrences.
- Prerequisites: pretraining-class compute to train the architecture from scratch (the comparison is at 360M / 760M+ scale, suggesting accessible-but-nontrivial budgets); a base codebase capable of online parameter updates inside the forward pass; no special RL infrastructure required (the "surprise" signal is a self-supervised gradient, not an RL reward).
- Inference engineering caveat: serving requires per-sequence mutable weights for the memory module, which complicates batched / KV-cache-style deployments.

## Novelty
Genuinely new *combination*, with one arguably new primitive:

- **New-ish primitive**: framing forgetting as a *regularizer* in a unified online-optimization view, and using non-MSE / non-dot-product attentional biases (Huber, p-norm, simplex-projected). MIRAS as a taxonomy is the bigger conceptual contribution.
- **Recombination**: deep-MLP memory + gradient-driven write gating builds on test-time training, fast-weight programmers, and external memory networks (LongMem is explicitly cited).
- **Closest prior**: Mamba-2 and Gated DeltaNet (linear-recurrent SSMs with gating) for the efficiency angle; LongMem and Transformer-XL-style memory for the long-context angle; what's changed is replacing fixed-size compressed state with a *learnable network* trained online via a surprise gradient.

## Reproducibility
- Two arXiv papers exist (2501.00663 Titans, 2504.13173 MIRAS) — preprints, not journal-vetted.
- Blog does not link a code repo or weights release; no PapersWithCode entry mentioned.
- No independent reproduction is cited in the source.
- Verdict: claims are checkable in principle from the papers but not yet plug-and-play; treat headline numbers (esp. "beats GPT-4 on BABILong") as unreplicated until weights or third-party runs surface.

## Adoption
- Authored by Google Research (Behrouz, Razaviyayn, Mirrokni); the Titans paper (Jan 2025) had ~10 months in the wild before this consolidation post, plenty of time for community pickup.
- Blog references a sibling Google post on "Nested Learning" as a related paradigm, suggesting this is part of a coordinated Google Research push on continual / long-memory architectures.
- The post itself does not cite external adopters, downstream forks, or leaderboard placements; independent uptake signal from this source alone is weak.

## Conflicts
- Implicit tension with the **fixed-size-state suffices** position underlying Mamba-2 / SSM advocacy: the post explicitly argues fixed-size compression "cannot adequately capture the rich information in very long sequences."
- Implicit tension with **scaling-pure-attention** advocates (GPT-4-class long-context via attention + tricks): the BABILong claim asserts a much smaller Titans beats GPT-4 on very long contexts.
- Wiki currently has no pages staking out either of these positions, so no active wiki conflict to flag — re-check once architecture pages exist.
<!-- /DOMAIN-SLOT -->

## Cross-ref candidates
- [[long-context-architectures]] — would be a parallel/anchor page; this source is a direct contribution.
- [[test-time-training]] / [[test-time-memorization]] — Titans is a flagship example of online parameter updates during inference.
- [[state-space-models]] / [[mamba-2]] — Titans positions itself as a successor that fixes the "fixed-size compression" weakness.
- [[gated-deltanet]] — named baseline that Titans claims to beat.
- [[linear-rnns]] — class Titans is competing with on speed.
- [[associative-memory]] — MIRAS recasts all sequence models as associative-memory optimizers.
- [[continual-learning]] / [[nested-learning]] — sibling Google Research line cited in the post.
- [[surprise-driven-learning]] / [[gradient-as-signal]] — the "surprise = gradient norm" framing.
- [[babilong-benchmark]] — headline result lives here.
- [[long-context-benchmarks]] — covers BABILong + the >2M-token claim.

(None of these pages exist yet per `wiki/index.md` — they are *candidate* names for future pages.)

## Conflict flags
- Claim: "Titans outperforms all baselines, including extremely large models like GPT-4" on BABILong despite "many fewer parameters", and "scale[s] effectively to context window sizes larger than 2 million tokens."
  Contradicts: (no existing wiki page yet) — will potentially contradict any future [[long-context-scaling]] or [[gpt-4-long-context]] page that takes the position that scale + attention dominate at extreme context lengths.
  Basis: "Extreme long-context recall" section of the blog; figure caption "Performance of Titans on extreme long-context reasoning."
- Claim: Fixed-size recurrent states (Mamba-2, SSMs) "cannot adequately capture the rich information in very long sequences."
  Contradicts: (no existing wiki page yet) — flag for any future [[state-space-models]] or [[mamba-2]] page that endorses the fixed-state-is-sufficient stance.
  Basis: Second paragraph of intro and "Conclusion" section.

## Proposed page shape
- **New page**: `titans-architecture` — a dedicated page for the Titans MAC architecture (long-term memory MLP, surprise gradient, momentum, adaptive weight decay), with the BABILong / 2M-token claim front-and-center and the inference-engineering caveats called out.
- **New page**: `miras-framework` — separate page for MIRAS as a *taxonomy of sequence models* (memory architecture / attentional bias / retention gate / memory algorithm), with the YAAD / MONETA / MEMORA variants as subsections. Justification: MIRAS is a conceptual lens that will be referenced from many architecture pages independently of Titans.
- **New page**: `test-time-memorization` — broader concept page covering online parameter updates during inference, with Titans as the primary worked example and prior art (fast weights, test-time training, LongMem) as background.
- These three should cross-link tightly; MIRAS should link out to future per-architecture pages (Mamba-2, Gated DeltaNet, Transformer++) once they exist so the taxonomy has anchors.
