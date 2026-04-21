# Meta-Learning & Classic Few-Shot

Pre-LLM foundations for the question David's project asks of LLMs: *how can a model generalize from one (or a handful of) examples?* The papers here span the two dominant pre-LLM answers — gradient-based meta-learning (MAML) and metric-based meta-learning (Prototypical Networks) — plus a contrarian, prior-engineered approach that achieves one-shot generalization with no meta-training at all (Yu et al.).

## Papers

- [[maml]] — Finn, Abbeel, Levine (ICML 2017). Learn an initialization θ such that one SGD step on K examples solves a new task. Model- and task-agnostic; works for classification, regression, RL.
- [[prototypical-networks]] — Snell, Swersky, Zemel (NeurIPS 2017). Learn an embedding where classes are unimodal clusters; classify by nearest class mean. Equivalent to mixture-density estimation under Bregman divergences.
- [[learning-from-one-shot]] — Yu, Mineyev, Varshney, Evans (arXiv:2201.08815). Hand-craft a "distortable canvas" similarity that encodes visual invariances; 1-NN on this metric reaches near-human Omniglot/QuickDraw one-shot performance with zero pretraining.

## Cross-cutting synthesis

### Gradient-based vs metric-based meta-learning
- **Gradient-based (MAML).** The bet is on parameter geometry: meta-train so the loss surface is *sensitive* near θ, then a few SGD steps suffice. Works for any differentiable model and any task with a loss function (incl. RL). Cost: bi-level optimization, Hessian-vector products (or first-order approx).
- **Metric-based (Prototypical Networks).** The bet is on representation geometry: meta-train an embedding so that simple distance-based classifiers (nearest-prototype, nearest-neighbor) generalize from K samples. Works only when the downstream operation is well-served by a fixed simple inductive bias (one cluster per class). Far simpler to train.
- **Convergence in the one-shot limit.** Snell et al. note prototypical networks reduce to matching-network-style 1-NN when K=1; MAML's first-order approximation is also nearly identical to standard fine-tuning from a good init. At K=1 the algorithmic distinctions thin out — what matters most is the quality of θ or f_φ.

### Prior-engineered alternative
- Yu et al. show that for restricted, structured domains an *explicit* prior (here, a distortion metric over canvas transformations) can replace meta-training entirely. The implication: the role of meta-training is to *induce a useful prior from data* — if you have one already, you can skip it.

### Transfer to the LLM regime
- LLM in-context learning *is* a kind of forward-pass-only meta-learner: the pretraining objective induces an initialization in which a few examples in the prompt suffice. This makes pretrained LLMs the strongest empirical instantiation of MAML's vision (with tokens-in-context replacing SGD updates) — see [[../in-context-learning-theory/_overview]].
- Prototypical-network intuitions survive too: residual-stream features support implicit "concept prototypes" assembled from in-context support, and induction-head circuits implement nearest-token-pattern lookup analogous to 1-NN.
- The Yu et al. analogue for LLMs: the prior is no longer hand-engineered geometric distortions but the entire pretraining corpus, which already encodes a vast library of conceptual invariances. David's single-sample fine-tuning aims to *consolidate* a concept into weights using one example — banking on this pre-existing prior.

### What meta-learning does NOT solve (that David's project might)
1. **No curated task distribution.** MAML and protonets require p(T) at meta-train time. LLM users present a single sample with no analogue meta-batch. David's setup must work without one.
2. **Concept-level (not class-level) updates.** Meta-learning targets new *classes/tasks*; David targets new *concepts* — abstractions that may rewrite the model's behavior across many downstream tasks.
3. **Generative outputs, not classification.** The classical few-shot canon is overwhelmingly classification. Single-sample LLM training must update behavior in a generative output space; the right loss/divergence is open.
4. **Updating weights, not just outputs.** ICL leaves the model unchanged. David wants persistent, weight-level internalization of the new concept — a non-trivial step beyond test-time adaptation.
5. **Avoiding catastrophic interference.** Meta-learning sidesteps this via held-out tasks; one-sample SFT on a base LLM risks degrading unrelated capabilities. None of these papers grapple with that.

## Method comparison

| Method | What is meta-learned | Adaptation at test time | Pretraining required | One-shot result | Key cost |
|---|---|---|---|---|---|
| MAML | initialization θ | K samples + 1–few SGD steps | meta-train across p(T) | Omniglot 5w1s 98.7% | Hessian-vector products |
| Prototypical Networks | embedding f_φ | K samples → mean → nearest prototype | meta-train across p(T) | Omniglot 5w1s 98.8% | episodic data sampling |
| Distortable Canvas (Yu) | nothing — prior is hand-built | 1 sample + 1-NN on D_C | none | Omniglot 1-shot 6.75% err (near-human) | per-pair AMGD optimization |
| (LLM ICL, for context) | implicit, via pretraining | K samples in prompt | massive token corpus | varies by task | inference compute |

## Open questions

- Can MAML-style sensitivity be induced in LLMs *without* an explicit task distribution — perhaps via self-generated task synthesis?
- What is the right "distance" for prototypical-style updates over LLM hidden states or output distributions? KL? Embedding cosine? Behavior on a probe set?
- How much of an LLM's "few-shot ability" is inherited prior (cf. Yu et al.) vs latent meta-learning vs implicit Bayesian inference?
- Can second-order / implicit-gradient meta-learning (iMAML, Reptile) scale to 7B+ models cheaply enough to be useful for single-sample fine-tuning?
- Does a single-sample weight update interfere catastrophically with unrelated capabilities, and what regularizer (EWC-style? sparse subnetwork?) prevents it?

## Source

See individual paper pages: [[maml]], [[prototypical-networks]], [[learning-from-one-shot]].

## Related themes

- [[../in-context-learning-theory/_overview]] — LLMs as implicit few-shot learners; ICL as implicit gradient descent / Bayesian inference.
- [[../test-time-training/_overview]] — modern descendants of MAML's inner loop applied to deep networks at inference time.
- [[../rlvr-mechanics/_overview]] — RL-based single-sample updates (1-shot RLVR) as an alternative to supervised meta-adaptation.
