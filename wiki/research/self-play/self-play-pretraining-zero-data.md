# Self-Play Pretraining with Zero Data

Cowsik, Dolev, Li, De Luca, Cohen, Goodman, Levine (arXiv:2609.30063) pretrain two randomly-initialized decoder-only transformers — a Learner (next-token prediction) and a Generator (RL) that emits programs for a universal Turing machine (UTM) — entirely from **zero natural data**, and find predictable zero-shot power-law scaling on held-out natural datasets (text, images, music, speech, DNA) plus emergent in-context learning on algorithmic tasks.

## Method

Byte-level UTM program search, following Grau-Moya et al. 2024's non-adaptive baseline but making the generator adaptive. Each round: sample $N$ programs from generator $g_\phi$, execute on the UTM with a random input tape to get byte sequences, take a learner gradient step on next-token loss over program outputs, then update the generator via RL + expert iteration.

**Generator reward** (Eq. 2): $r_i = |\langle\nabla_\theta L(y_i;\theta_e), P_e \odot \delta\theta_e\rangle|$ — a preconditioned gradient-alignment score between the gradient a candidate program induces in the learner and the learner's own recent parameter trajectory. This is a **learning-progress reward against the learner's own trajectory**, not a task-success or difficulty signal — and the authors explicitly reject a naive "prediction-difficulty" reward as degenerate (arbitrarily hard-to-predict programs can be made by injecting random bytes with no useful structure).

RL objective: KL-regularized expected reward vs. a uniform Solomonoff-style program prior, GRPO-style batch-level advantage with a sequence-level importance-ratio correction for off-policy replay samples. An expert-iteration step (reward-weighted SFT of high-reward programs back into the generator) mitigates catastrophic forgetting of the generator itself.

**Theoretical framing** — a decomposition of pretraining loss (extending the Chinchilla ansatz) splitting **contingent information** $D_c$ (facts/symbols specific to one dataset) from **universal predictive structure** $D_u$ (regularities — copying, recursion, hierarchical composition — shared across data-generating processes). Self-play holds $D_c=0$ throughout and searches program space for exactly the $D_u$ term.

## Results

- Across text, images, music, speech, and DNA, self-play shows universal zero-shot power-law scaling in compute, with exponents comparable to directly training on the corresponding natural modality (DNA is an exception).
- Against a fixed non-adaptive universal prior (same UTM program space, i.i.d. sampling): scales substantially slower — access to the program space alone isn't sufficient, the generator must learn where to allocate compute.
- Against a PCFG prior: PCFG wins on text/code (matched inductive bias) but transfers weakly to images/music/audio/speech, where self-play wins — self-play trades peak in-domain performance for broader universality.
- Emergent zero-shot ICL on held-out algorithmic tasks (REVERSE STRING, STACK, ASSOCIATIVE RECALL near 100% with enough demonstrations; MAX/MIN/SUM tasks show an interpretable copy-prior → low-bits-correct → high-bits-correct strategy shift) — with **zero gradient updates at eval time**.
- Discovers recognizable mathematical program families (arithmetic, Fibonacci, geometric, quadratic, cubic) far earlier than expected under uniform program sampling (e.g. Fibonacci at round 512 vs. an expected >53,000).

All confined to models <25M params, 4K context, 34.36B max token budget — unknown whether scaling persists at larger scale.

## Limitations (acknowledged)

- Self-play "cannot recover contingent information" — explicitly not a replacement for natural data, only isolates the universal-structure term.
- Loses to a hand-designed PCFG prior on the one domain (text/code) that prior specializes for.
- DNA is an unexplained exception to the cross-modality exponent match.
- Hyperparameter selection used validation loss on real corpora (DCLM+DNA) despite zero natural data entering gradient updates — acknowledged as "limited leakage."
- Forward-mode-AD reward computation's engineering cost isn't quantified; K-seed ensembling is used throughout the scaling frontier, potentially masking single-model variance.

## Relation to the wiki's self-play and RLVR corpus

This is a genuinely different regime from the wiki's existing self-play/RLVR corpus: pretraining from random initialization on zero natural data, vs. RLVR post-training of an already-capable base model. Its "self-play discovers universal structure the learner didn't have before" finding is **not** in tension with the Invisible Leash family's "RLVR only reweights existing base-model probability mass" claim — there is no pre-existing base-model mass here to reweight. Readers should not conflate the two settings.

The generator's reward — gradient-alignment against the learner's own trajectory — is a concrete, gradient-based operationalization of "propose at the frontier of the learner's competence," the same design principle as [[asymmetric-self-play]]'s Alice/Bob time-based reward, but computed directly from training dynamics rather than task outcomes. It's a 13th entry for [[../synthesis/proposer-reward-shapes]]'s comparison table.

## Source

- arXiv: [2609.30063](https://arxiv.org/abs/2609.30063) — "Self-Play Pretraining with Zero Data"
- Captured via 2026-09-25 weekly sweep: `raw/research/weekly-2026-09-25/01-self-play-pretraining-zero-data.md`

## Related

- [[_overview]] — self-play theme overview; add as a 13th proposer-reward-shape entry, first at the pretraining-from-random-init stage
- [[asymmetric-self-play]] — same "propose at frontier of competence" template, gradient-based vs. time-based operationalization
- [[info-gain-self-play]] — shares the epiplexity metric for judging self-play/synthetic-data quality (verify whether the same underlying Finzi et al. citation)
- [[understanding-self-play]] — independent confirmation, in the pretraining regime, of "the proposer is the critical component"
- [[../in-context-learning-theory/_overview]] — a fifth, orthogonal origin story for ICL: emergent from zero-natural-data synthetic pretraining
- [[../rlvr-mechanics/deepseekmath-grpo]] — generator's policy-gradient estimator is GRPO-style with a sequence-level importance-ratio extension
- [[../synthesis/proposer-reward-shapes]] — comparison table, candidate for a 13th row
- [[../../weekly-briefs/2026-09-25]] — brought in by the 2026-09-25 weekly sweep
