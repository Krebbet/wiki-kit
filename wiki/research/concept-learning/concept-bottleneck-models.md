# Concept Bottleneck Models

Koh, Nguyen, Tang, Mussmann, Pierson, Kim, Liang (Stanford / Google, ICML 2020). A *concept bottleneck model* (CBM) factors prediction as `x →_g c →_f y` where `c ∈ R^k` is a vector of human-specified concepts (e.g. "joint space narrowing", "wing colour"). The model is trained on triples `(x, c, y)` so that an intermediate layer of width `k` aligns component-wise with the concepts. At test time the model reads off `ĉ = g(x)`, then predicts `ŷ = f(ĉ)`. The bottleneck makes interpretation and *intervention* on individual concepts mechanically possible, and on OAI x-rays / CUB birds CBMs match end-to-end accuracy while exposing concept-level handles.

## Method

- Three training regimes: **independent** (train `g` on `(x,c)` and `f` on `(c,y)` separately, compose at test time); **sequential** (train `g`, then train `f` on the predicted `ĝ(x)`); **joint** (single weighted loss `L_Y(f∘g, y) + λ Σ L_{C_j}(g_j, c_j)`). `λ → 0` recovers a standard end-to-end model; `λ → ∞` recovers sequential.
- Architectural recipe is trivial: take any deep classifier, resize one intermediate layer to `k = #concepts`, and add the per-concept loss on that layer. Concept annotations are needed only at training time.
- **Test-time intervention.** Replace `ĉ_j` with the oracle's true `c_j` for any subset of concepts, propagate through `f`. For classification (CUB) intervene on logits at the 5th/95th percentile of the training distribution to approximate a binary edit. Concepts can be grouped (e.g. "wing colour" as one query) so a single human action can correct multiple binary attributes.
- Robustness mechanism: because each concept is shared across many `y` values, the `x → c` map sees concept-coherent distributional diversity that the spurious-correlation-driven `x → y` map does not.

## Claims

- **Task accuracy parity.** OAI: independent / sequential / joint RMSE 0.435 / 0.418 / 0.418 vs standard 0.441. CUB: joint 0.199 vs standard 0.175 (small gap closed by joint; bottleneck constraint not free on fine-grained classification but cheap).
- **Concept accuracy.** Bottleneck `g` predicts concepts much better than linear probes on a standard model: OAI concept RMSE 0.53 vs 0.68; CUB concept error 0.03 vs 0.09. Probes on SENN ([Melis & Jaakkola]) also fail to recover concepts post-hoc.
- **Test-time intervention.** OAI: querying just 2 of 10 concepts cuts RMSE from >0.4 to ≈0.3. CUB: large gains after intervening on several concept groups.
- **Intervenability ↔ training regime.** Independent bottleneck has the worst pre-intervention error but the best post-intervention error — because `f` was trained on true `c`, the test-time substitution is in-distribution. Joint bottleneck with `λ` too small fails to intervene at all (control: replacing `ĉ` with true `c` *increases* error).
- **Robustness on TravelingBirds.** Under train/test background swaps: standard 0.627 error, bottleneck models 0.48–0.50.
- **Theory (linear regression).** Asymptotic excess error ratio bound: `(k/d · σ²_Y + σ²_C) / (σ²_Y + σ²_C)`. Bottleneck wins when `k ≪ d` and concepts are less noisy than targets.
- **Data efficiency.** OAI sequential bottleneck reaches standard-model accuracy with ≈25% of the training data.

## Sample efficiency

CBMs are not single-sample learners in the LLM sense, but they are explicitly more *sample-efficient per `(x,y)` pair* in the regime where concept annotations are dense relative to inputs. The mechanism: the supervised concept signal forces `g` to learn a low-dimensional, semantically-aligned representation rather than discovering it implicitly from `y` alone. This converts annotation cost from labelling outputs to labelling concepts, which is often cheaper. The intervention story also makes a *single* test-time correction high-leverage: one concept fix at inference can flip the prediction. So the unit of sample efficiency is the *concept correction*, not the labelled example.

## Relevance to the project

The clearest operational definition of "learning a concept" in the literature: a concept *is* a designated coordinate of an internal layer trained to predict a human-specified label, with `f` constrained to depend on `x` only through `ĉ`. This makes "concept-based" a precise architectural commitment — the bottleneck — rather than a vague representational property. Two project-relevant lessons: (1) The independent-bottleneck result (better intervention because `f` saw true `c`) suggests that single-sample concept imprinting needs a *clean* concept channel, untainted by joint optimisation that lets the model route around the bottleneck. (2) The TravelingBirds robustness result shows concept routing as a counter to spurious-correlation pickup — analogous to the project's claim that concept-based learning generalises where pattern-matching does not. Limitation for transfer: CBMs require a fixed enumerated concept vocabulary at training time, which is exactly what David does *not* have for general LLM concepts. The architectural primitive (bottleneck + alignment loss) is the inspiration; the closed-vocabulary commitment must be relaxed (cf. [[recursive-concept-evolution]] for a dynamic-vocabulary alternative).

## Source

- arXiv: 2007.04612
- Raw markdown: `../../../raw/research/single-sample-llm-learning/30-H-1-concept-bottleneck-models.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/H-1-concept-bottleneck-models.pdf`

## Related

- [[recursive-concept-evolution]] — dynamic-vocabulary, low-rank-subspace counterpart; same concept-as-axis intuition without the closed concept set
- [[../meta-learning-few-shot/prototypical-networks]] — concepts as cluster centres in an embedding rather than supervised axes
- [[../in-context-learning-theory/icl-bayesian-inference]] — concepts as latent variables in a posterior; CBM makes them observed instead
