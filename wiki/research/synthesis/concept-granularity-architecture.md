---
name: concept-granularity-architecture
description: Initial hypothesis — middle-layer representations should operate on variable-granularity concept units that can dynamically merge or split, rather than on a fixed per-token grid. Motivated by REASONMAXXER's finding that only 1-4% of tokens carry the corrective signal and that the rest are transport overhead for human-readable grammar.
type: hypothesis
status: initial
---

# Hypothesis — Concept-Granularity Middle Layers

*Editorial hypothesis surfaced 2026-05-13 from a /query conversation about REASONMAXXER and the RL-as-selection-not-learning thesis. Initial sketch only — to be fleshed out into an architectural design as supporting evidence accumulates.*

## One-paragraph hypothesis

A transformer that operates on the same fixed per-token grid from input to output is paying for representational uniformity it does not use. [[../rlvr-mechanics/rethinking-rl-sparse-selection]] shows that **0% of RL-promoted tokens lie outside the base top-5 and only 1.0–4.1% of token positions are reranked at all**, with reranking concentrated at positions of 5–12× higher entropy. Read in reverse: ~96–99% of generated tokens are *transport overhead* — surface grammar required to communicate to a human, but not where the model's decision-making lives. The hypothesis is that **internal representations should be concept-granular and variable-length**: middle layers should be free to *merge* embeddings of consecutive filler tokens into denser concept-units and *split* a single decision-point token's representation into multiple concept-units when the information content warrants. The decoder-side mechanism re-expands these concept-units back into a token-stream for human-readable output. Compute concentrates where information does, instead of being amortised uniformly across the position grid.

## Motivation from the corpus

- **[[../rlvr-mechanics/rethinking-rl-sparse-selection]]** — 1.0–4.1% positions reranked across GRPO/PPO/RLOO × three model families; mean promoted rank 2.14–2.39; 5–12× entropy localisation. Oracle intervention *only at reranked positions* recovers full RL pass@1. The decision-points-vs-overhead asymmetry is empirically sharp.
- **[[../rlvr-mechanics/rl-sparse-subnetwork]]** — RL touches 5–30% of weights; updates are sparse but full-rank. Parameter-side counterpart to the token-side sparsity above. Compute that matters lives in a small, consistent subset.
- **[[../in-context-learning-theory/icl-as-gradient-descent]]** — implicit ICL update is rank-1 outer product $(Wx - y)x^\top$. Argues the natural update primitive is *local and low-rank*, not global. A concept-granular middle layer would preserve this primitive directly.
- **[[../in-context-learning-theory/icl-bayesian-inference]]** — per-token information theorem: longer structured context carries more posterior signal per token *if structured*. Aligns with the idea that what carries posterior signal is the *concept content*, not the token count.
- **[[../in-context-learning-theory/induction-heads]]** — circuit-level reasoning happens at specific copy-completion heads, not uniformly across positions. The "units of cognition" inside a transformer are already non-uniform; the position grid hides this.
- **[[../concept-learning/recursive-concept-evolution]]** — concept-as-subspace operationalisation; spawn-on-failure with MDL gate. RCE already operates on concept-units rather than tokens at the concept-library level. The hypothesis lifts this to the middle layers themselves.
- **[[../concept-learning/concept-bottleneck-models]]** — concept-as-axis. Earlier, supervised version; provides the design principle that intervening on concepts (not tokens) is a useful primitive.
- **[[../rl-optimizers/latent-grpo]]** — first stable GRPO on continuous (vocabulary-superposition) latent reasoning chains; +4.27 Pass@1 with 3.31× shorter chains; documents Latent Mixture Non-Closure failure mode. **Closest existing corpus result to the proposal** — latent reasoning *is* concept-granular in spirit; it operates on continuous superpositions rather than discrete token sequences.

## General flow (sketch)

```
INPUT TOKENS  x_1 ... x_T
        │
        ▼
EMBED        e_1 ... e_T              ← standard per-token embedding
        │
        ▼
EARLY LAYERS (per-token grid)         ← retain token alignment while concepts crystallise
        │
        ▼
COMPRESSOR   {e_1 ... e_T} → {c_1 ... c_K}    K ≤ T
   • merge consecutive filler tokens into a single concept-unit
   • split high-entropy tokens into multiple concept-units when warranted
   • routing decision conditioned on local entropy / information content
        │
        ▼
MIDDLE LAYERS (concept grid)          ← variable-length, K ≪ T typical
   • attention + FFN on concept-units c_1 ... c_K
   • where the "1-4% decision tokens" computation actually happens
   • concept-units can be merged / split further across layers if needed
        │
        ▼
EXPANDER     {c_1 ... c_K} → {h_1 ... h_T}   restore token-level positions
   • each concept-unit emits a span of contextualised hidden states
   • decoder-style reconstruction: the concept-unit is the latent; the token span is the realisation
        │
        ▼
LATE LAYERS (per-token grid)          ← token-level fluency / format
        │
        ▼
DECODE       y_1 ... y_T              ← standard next-token prediction
```

**Reading the diagram.** The token-grid is preserved at the *boundary* (embedding in, decoding out) for compatibility with standard pretraining and human-readable output, but the *middle* of the network operates on a variable-length concept grid. The compressor decides where to merge or split based on local information content; the expander undoes this so the late layers can produce a token stream.

## Why this should connect to the RL-as-selection thesis

If REASONMAXXER's finding is that **RL only matters at ~1–4% of token positions**, and those positions are where actual decisions are made, then a concept-granular middle layer **directly exposes those decision points** as their own concept-units. The RL signal would no longer need to find a needle in a haystack of filler positions; it would be applied to a much shorter sequence of concept-units, each of which is a decision-of-record.

Speculative implication: the [[../rl-optimizers/bolt-kl-rlvr-boltzmann|BOLT Theorem 6]] one-shot saturation $\beta\log(1/\pi^*(S_N|x))$ is a *token-level* bound. At the concept-level, the relevant $\pi^*$ is over concept sequences, which are exponentially shorter. The coverage requirement $N \gtrsim 1/p_\gamma$ may relax accordingly. This is unverified.

## Important supporting mechanisms (what would have to work)

| Mechanism | Status | Closest corpus precedent |
|---|---|---|
| **Merge operator** — combine consecutive token embeddings into a single concept-unit | Not yet captured | None — explicit gap |
| **Split operator** — expand a single token's embedding into multiple concept-units | Not yet captured | None — explicit gap |
| **Routing signal** — when to merge vs split, computed from local information content | Partial — entropy gating shown viable in [[../rlvr-mechanics/rethinking-rl-sparse-selection]] | Entropy threshold $H_t > \tau$ recovers oracle |
| **Concept-unit attention** — middle-layer attention over variable-length concept sequences | Not yet captured | — |
| **Expander operator** — re-realise concept-units as token spans | Not yet captured | Vague analogue: Latent-GRPO's discrete decoding step |
| **End-to-end differentiability** — merge/split routing must be trainable | Not yet captured | Vague analogue: Latent-GRPO's Gumbel + STE for latent reasoning |
| **Stability under variable-length internal sequence** | Open | Latent-GRPO documents *Latent Mixture Non-Closure* as the analogous failure mode |

## Gaps

1. **No captured paper does exactly this.** [[../rl-optimizers/latent-grpo]] is the closest in spirit — continuous latent reasoning, vocabulary superposition, shorter chains — but it operates on a *fixed* sequence length of latents; it doesn't dynamically merge or split. The merge/split primitive specifically is not in the corpus.

2. **The merge/split routing is itself a discrete decision.** End-to-end training likely requires either a relaxation (Gumbel-softmax + STE, à la Latent-GRPO) or a separately trained routing head. The wiki has no captured method for differentiable variable-length sequence routing.

3. **Pretraining compatibility.** Standard pretraining is token-by-token next-token prediction. A concept-granular middle layer trained from scratch would need a pretraining signal that's compatible with variable-length internal sequences. Open: distil into the architecture from a fixed-grid teacher? Train the compressor/expander as autoencoder warm-up?

4. **Decoder alignment.** When the expander produces $T$ hidden states from $K$ concept-units, the alignment between concept-unit $c_k$ and token-span $[h_{i_k}, h_{i_k+1}, ..., h_{i_{k+1}-1}]$ is itself a decision. No captured prior covers this.

5. **Concept-unit interpretability.** The hypothesis is that concept-units carry decision-level information. Whether they actually do, or whether they degenerate into arbitrary compressions, is an empirical question. [[../concept-evaluation/causal-abstraction]] (IIA) is the candidate probe — if concept-units have IIA at a target abstraction, the hypothesis is on track.

6. **Sample efficiency claim is speculative.** The argument that BOLT's coverage wall relaxes at concept granularity (exponentially shorter $\pi^*$ support) is plausible but unverified — it assumes concept-units factorise reasoning in a way that token-grids do not. No corpus paper measures this.

7. **Compute trade-off unknown.** Variable-length middle layers reduce $K$ relative to $T$ on average, but the compressor and expander themselves cost compute. Net throughput vs. quality trade-off is empirical.

## Watchlist targets (what to look for)

Categories of paper that, if captured, would either supply primitives or invalidate the hypothesis:

- **Variable-length internal representations** — funnel transformers, mixture-of-tokens, dynamic token pruning, hierarchical autoencoders applied mid-stack.
- **Differentiable sequence routing** — Mixture-of-Depths, expert-choice routing, learned token-merging in vision (ToMe and successors) re-applied to language.
- **Latent reasoning successors to [[../rl-optimizers/latent-grpo]]** — anything that extends continuous-superposition reasoning to variable-length latent sequences.
- **Concept-level training signals** — work that supervises representations at a sub-token or super-token granularity (BPE alternatives, byte-level + chunking).
- **Entropy-routed compute** — methods that route compute to high-entropy positions (echoes [[../rlvr-mechanics/rethinking-rl-sparse-selection]]'s entropy gating).
- **Cross-token-merging during fine-tuning** — anything that retroactively merges/groups token positions for downstream tasks.
- **Counter-evidence** — papers showing that uniform per-token compute is provably or empirically necessary, or that variable-length middle layers cause representational collapse.

## Relation to the wiki's other method proposals

- [[proposed-method]] is an *RL training procedure* on a standard transformer; this hypothesis is an *architectural* change. Composable — proposed-method's RL components would presumably run on top of a concept-granular architecture, with the concept-units exposing the 1-4% decision points directly.
- [[concept-curriculum-method]] and [[recursive-concept-learning]] are curriculum/decomposition strategies orthogonal to the model architecture. A concept-granular middle layer would presumably make their concept-level operations cleaner.
- [[single-sample-concept-skeleton]] composes primitives at the training-loop level; this hypothesis composes primitives at the architecture level. Different abstraction layer, same project frame.

## Next steps (when promoting from hypothesis to design)

This page is intentionally thin. Promotion criteria:

- **At least one captured corpus paper** demonstrates a working merge or split primitive at the middle-layer level of a language model (not vision-only).
- **A concrete loss formulation** for the merge/split routing decision that has been empirically tried.
- **A documented failure mode catalogue** comparable to [[../rl-optimizers/latent-grpo]]'s Latent Mixture Non-Closure — what *doesn't* work and why.

Until then, this page stays as initial sketch, watchlist target generator.

## Source

Editorial hypothesis. Surfaced 2026-05-13 from a /query thread on REASONMAXXER and the RL-as-selection-not-learning thesis. No corpus paper proposes exactly this architecture; the supporting findings are cited inline.

## Related

- [[../rlvr-mechanics/rethinking-rl-sparse-selection]] — primary motivating result (1-4% reranked tokens, 0% shifted outside base top-5, 5-12× entropy at reranked positions)
- [[../rlvr-mechanics/rl-sparse-subnetwork]] — parameter-side sparsity counterpart
- [[../rl-optimizers/latent-grpo]] — closest existing corpus result (continuous latent reasoning, vocabulary superposition, shorter chains)
- [[../rl-optimizers/bolt-kl-rlvr-boltzmann]] — speculative connection: coverage wall may relax at concept granularity
- [[../concept-learning/recursive-concept-evolution]] — concept-as-subspace at the concept-library level
- [[../concept-learning/concept-bottleneck-models]] — concept-as-axis with intervention
- [[../in-context-learning-theory/induction-heads]] — circuits as non-uniform units of cognition
- [[../in-context-learning-theory/icl-as-gradient-descent]] — rank-1 outer-product update as natural primitive
- [[../in-context-learning-theory/icl-bayesian-inference]] — per-token-information theorem
- [[../concept-evaluation/causal-abstraction]] — IIA as candidate concept-unit probe
- [[proposed-method]] — composable training procedure (RL on top of the architecture)
- [[concept-curriculum-method]] — orthogonal curriculum proposal
- [[recursive-concept-learning]] — orthogonal failure-driven decomposition
- [[single-sample-concept-skeleton]] — earliest editorial composition; primitive-level
