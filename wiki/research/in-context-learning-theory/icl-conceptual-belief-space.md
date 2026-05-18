# Stories in Space — ICL as Trajectories in Conceptual Belief Space

Bigelow et al. (arXiv:2605.12412) argue that LLM in-context learning is geometrically a **smooth trajectory through a low-dimensional conceptual belief space** — Gärdenfors' conceptual spaces lifted from points to probability distributions. On a frozen Llama-3.1-8B-instruct, belief dynamics over freeform story text are well-described by trajectories on structured manifolds (RMSE 0.09), the behaviour manifold and the residual-activation manifold share the *same* hierarchical geometry ($r=.92$), the LLM's emotion geometry matches the human Russell–Mehrabian valence–arousal plane ($r=.93$), and causal activation steering shifts beliefs in a way whose cross-concept entanglement is **predicted by inter-concept manifold distance**. No training; pure interpretability.

## Source
- [`raw/research/weekly-2026-05-17/05-icl-conceptual-belief-space.md`](../../../raw/research/weekly-2026-05-17/05-icl-conceptual-belief-space.md) — captured 2026-05-17 (arXiv:2605.12412)

## Framework

- Conceptual space $\mathcal{C} = A_1 \times \cdots \times A_n$ (Gärdenfors, Eq. 1); **conceptual belief space** $\mathcal{B} = P(A_1) \times \cdots \times P(A_n)$ — the distribution-valued lift (Eq. 2).
- Belief elicitation (Eq. 3): after each sentence $x_{1:t}$, prompt the model to rate concept $c$ on 0–10; estimator $y_{t,c} = \tfrac{1}{10}\sum_{i=0}^{10} i\cdot p(y=i\mid x_{1:t}, q_c)$.
- UMAP+PCA on the behavioural matrix $Y$ and activation matrix $Z^\ell$ extracts manifolds $M^y$, $M^z$; ridge-regression + isotonic-calibrated linear probes predict $\hat y_{t,c}$ from $z_{\ell,t}$.
- Steering: $\tilde z_\ell = z_\ell + \alpha v_{c,\ell}$ via probe-weight or Difference-in-Means vectors, **simultaneously across a 7-layer span** (single-layer is corrected away by later layers).

## Findings

| Claim | Evidence |
|---|---|
| Beliefs trace low-dim structured manifolds | RMSE 0.09 (Emotions/Genres), 0.11 (Arbitrary) at $\ell=9$ |
| Behaviour ≅ activation geometry | Pearson $r=.92$ (Emotions), $r=.89$ (Genres), $p<.001$ |
| LLM emotion space ≅ human valence–arousal | $r=.93$, $p<.001$ vs Russell–Mehrabian 1977 |
| Steering entanglement ∝ manifold distance | $r=.65$ Emotions; within-cluster only for structured domains |

## Why it matters for this wiki

- The strongest concept-acquisition-over-pattern-matching evidence in the [[_overview]] / [[../concept-learning/_overview]] corpus: the model tracks emotion/genre beliefs continuously across story text **without being told which concepts to track**, linearly decodable from layer-9 residuals even when the prompt has no concept vocabulary; and the geometry is human-like, implying an absorbed conceptual topology rather than surface co-occurrence.
- A *dynamical* geometric operationalisation of [[icl-bayesian-inference]] (Xie et al.) — ICL as a belief trajectory, the empirical complement to the distributional Bayesian framing — and a dynamical extension of [[../decoding-time-steering/linear-rep-hypothesis]].
- For [[../synthesis/proposed-method]]: if concept beliefs are linearly decodable from residual activations, the $R_w$ reweighting prior has a concrete geometric target; steering entanglement predictable from manifold distance is a new design constraint for cross-concept interference. Adds a new consideration to [[../synthesis/decoding-time-shapes]] (manifold-geometry-predicts-entanglement) on top of its 13-mechanism table.

## Conflict / scope qualifier

§5 / App. F: single-layer steering is **ineffective** here (later layers nullify it); a 7-layer span is required. This is in tension with [[../decoding-time-steering/actadd]] and [[../decoding-time-steering/caa]], both of which report effective *single-layer* residual-stream steering. Likely model/domain-scoped (Llama-3.1-8B-instruct + probe vectors vs GPT-2/Llama-2 + DIM; the paper itself resolves single-layer via DIM). A **partial conflict / scope qualifier**, not a fundamental contradiction — recorded here and noted on [[../synthesis/decoding-time-shapes]] rather than opened as a conflict file (no existing open conflict on steering-layer-count).

## Limitations

1. Three hand-picked domains × 6 concepts each — tiny vocabulary (emotion trees have ~135 nodes).
2. Concepts treated as unitary, non-compositional, story-global (not character-scoped).
3. Arbitrary domain shows weaker structure ($r=.71$) and steering ($r=.42$) — method depends on domain geometry.
4. Single model, no family/size ablation.
5. 7-layer steering span is an empirical patch with no theoretical account.

## Follow-up leads
- Gärdenfors 2000 (*Conceptual Spaces*) — cognitive-science foundation, not yet on wiki.
- Wurgaft et al. 2026 (arXiv:2605.05115, manifold steering) — more rigorous sister paper; high-priority.
- Bigelow et al. 2025 (arXiv:2511.00617) — direct predecessor (dual nature of ICL & activation steering).

## Related
- [[_overview]] — ICL theory; geometric / belief-dynamics sub-thread
- [[icl-bayesian-inference]] — Xie et al.; this is its dynamical geometric complement
- [[../decoding-time-steering/_overview]] — steering methodology this extends
- [[../decoding-time-steering/actadd]] — single-layer steering tension (scope qualifier)
- [[../decoding-time-steering/caa]] — base→chat middle-layer geometry; structural predecessor
- [[../decoding-time-steering/linear-rep-hypothesis]] — Park et al.; dynamically extended here
- [[../concept-evaluation/control-tasks-probes]] — Hewitt & Liang probe methodology; 0.09 RMSE data point
- [[../concept-learning/_overview]] — "concept as region in a structured space" inside a frozen LLM
- [[../synthesis/proposed-method]] — geometric target for the $R_w$ prior
- [[../synthesis/decoding-time-shapes]] — manifold-distance-predicts-entanglement design note
- [[../../weekly-briefs/2026-05-17]] — brought in by the 2026-05-17 weekly sweep
