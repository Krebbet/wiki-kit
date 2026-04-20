# In-context Learning and Induction Heads

Olsson et al. (Anthropic, 2022) argue that *induction heads* — pairs of attention heads implementing the rule `[A][B] … [A] → [B]` — are the dominant mechanistic substrate of in-context learning (ICL) in transformers of every size with ≥2 layers. The case is built from a sharp training-time phase change in which induction heads, ICL ability, and a visible bump in the loss curve all co-emerge within a 2.5e9–5e9 token window (~1–2% of training for large models). Six lines of evidence — co-occurrence, architectural co-perturbation, ablation, qualitative generality, mechanistic plausibility, and small→large continuity — are presented; small attention-only models get strong causal evidence, large models with MLPs only correlational.

## Method

- **Definition.** An induction head must satisfy two empirical properties on a repeated random-token sequence: (1) *prefix matching* — attend to past tokens that were followed by the current/recent token; (2) *copying* — its output increases the logit of the attended token.
- **Mechanism (small models).** Composition of two heads across layers: a "previous-token head" smears prior content forward, then the actual induction head queries on that smeared key to find prior occurrences of the current token and copies their successor.
- **ICL score.** Loss(token 500) − loss(token 50), averaged across documents — a length-difference proxy for "learning from context".
- **Phase-change probes.** Per-token loss vector PCA across snapshots; ablations of candidate heads at test time; "smeared-key" architecture (`k_j ← σ(α) k_j + (1−σ(α)) k_{j−1}`) that lets even 1-layer models express induction.
- **Generalised induction.** Hypothesised "fuzzy" form `[A*][B*] … [A] → [B]` where `A*≈A` in some embedding — accounts for translation, abstract pattern completion, etc.

## Claims

- ICL score jumps from <0.15 nats to ~0.4 nats inside a narrow window, then is roughly flat for the rest of training across model sizes (Fig. 1, Model Analysis Table).
- Induction-head prefix-matching score and ICL score co-emerge at the same training step in every multi-layer model studied; one-layer models develop neither.
- Smeared-key architecture *causes* induction heads (and the ICL bump) to form earlier, in lockstep — strong interventional support for the mechanistic link.
- Direct ablation of induction heads in small attention-only and small-with-MLP models removes most of the ICL effect (Argument 3).
- Per-token analysis on Harry Potter prose: post-phase-change models predict repeated spans much better and *worse* on first-time appearances after the same prefix — the qualitative signature of pattern copying.
- Over 75% of final ICL is acquired during the phase change.

## Sample efficiency

The induction-head circuit, once formed, performs ICL from a *single* prior occurrence: seeing `[A][B]` once anywhere in context is enough to bias the next `[A]` toward `B`. The "fuzzy" generalisation lets one demonstration of an abstract pattern (e.g. one French→English pair) prime completion of similar pairs. Sample efficiency is essentially "1 in-context example per concept", but the circuit itself only forms after billions of pretraining tokens — the meta-learner is expensive, the meta-task is one-shot.

## Relevance to the project

If the dominant ICL mechanism is a *content-addressable copy circuit*, then a single fine-tuning example can in principle imprint a concept by writing the right `[A]→[B]` association into the weights that this circuit reads. This reframes single-sample fine-tuning as "install a key/value pair the induction circuit will retrieve" rather than "shift a global decision boundary". The phase-change phenomenology also warns: useful representations may need a base model that has *already* crossed the induction transition before single-shot edits will generalise.

## Source

- arXiv: 2209.11895 (transformer-circuits.pub/2022/in-context-learning-and-induction-heads)
- Raw markdown: `../../../raw/research/single-sample-llm-learning/10-A-1-induction-heads.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/A-1-induction-heads.pdf`

## Related

- [[icl-as-gradient-descent]] — alternative mechanistic story; von Oswald shows induction heads as a special case of GD-in-attention
- [[icl-bayesian-inference]] — competing/complementary explanation at the distributional level
- [[function-class-icl]] — Garg et al. observe a similar sharp ICL phase change in small synthetic settings
