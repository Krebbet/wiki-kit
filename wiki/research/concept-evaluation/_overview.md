# Concept Evaluation

Theme covering *methods for evaluating whether an LLM has actually understood a concept* — as opposed to memorising patterns that satisfy a test set. The unifying question across all nine sources: given that a model passes a test, **what additional evidence proves the model applies the concept correctly across scenarios it has not seen?**

The theme exists because the project's three method proposals ([[../synthesis/proposed-method]], [[../synthesis/concept-curriculum-method]], [[../synthesis/recursive-concept-learning]]) all assume an $\text{Evaluate}(S, c)$ primitive that does this discrimination. None of those methods can be validated without it. This theme is the captured prior art.

## Pages

| Page | Type | One line |
|---|---|---|
| [[gsm-symbolic]] | benchmark | Symbolic templates over GSM8K; numeric perturbations expose pattern-matching; up-to-65% drop on irrelevant clauses (NoOp). |
| [[math-perturb]] | benchmark | 279 hard-perturbed level-5 MATH problems where the original solution path no longer applies; large drops on SOTA models. |
| [[counterfactual-tasks]] | framework | Pair every default task with a counterfactual variant (base-9, modified chess); gap = procedure-vs-abstraction. |
| [[skill-mix]] | benchmark | Random k-subsets from N skills; combinatorial explosion ⇒ memorisation infeasible by construction. The compositional retest. |
| [[checklist-behavioral]] | methodology | Capability × test-type matrix (MFT/INV/DIR); the canonical frame for behavioural testing. |
| [[contrast-sets]] | methodology | Manual, label-flipping, local-boundary perturbations; up-to-25% performance drop vs raw test set. |
| [[causal-abstraction]] | theory | IIA as non-behavioural concept-fidelity metric; high task accuracy + low IIA exposes "right answer, wrong reason". |
| [[control-tasks-probes]] | methodology | Selectivity = probe accuracy − random-label control; floor for any probing-based concept claim. |
| [[embers-autoregression]] | diagnostic | Task / output / input probability shape LLM accuracy; *why* eval-of-understanding is hard. |

## The five evaluation modalities in this corpus

| Modality | Question | Sources | Where it plugs into RCL |
|---|---|---|---|
| **Symbolic perturbation** | Does perf survive numeric / template variation of the same concept? | [[gsm-symbolic]], [[math-perturb]] | E1 axis for procedural concepts |
| **Counterfactual variation** | Does the abstraction survive when surface conditions are out of training distribution? | [[counterfactual-tasks]] | E1 axis for procedure-vs-abstraction |
| **Local-boundary contrast** | Does the model flip prediction on a minimal label-flipping edit? | [[contrast-sets]], [[checklist-behavioral]] (INV/DIR) | E1 axis (B6 dataset workstream) |
| **Compositional combination** | Does the model combine $k$ concepts that no training example combines? | [[skill-mix]] | RCL **G2** (compositional root retest) |
| **Internal-representation probe** | Does an internal probe of the concept satisfy a non-trivial selectivity / IIA criterion? | [[control-tasks-probes]], [[causal-abstraction]] | E1 axis when probing internals; alternative to MDL |

## Cross-cutting themes

**Behavioural vs representational evaluation.** Five sources test *behaviour* under perturbation ([[gsm-symbolic]], [[math-perturb]], [[counterfactual-tasks]], [[contrast-sets]], [[checklist-behavioral]]); two test *representation* via internal probes or interventions ([[control-tasks-probes]], [[causal-abstraction]]); one is a methodological prior on both ([[embers-autoregression]]); one is the cross-concept compositional case ([[skill-mix]]). The behavioural tools are domain-portable but only diagnose surface mastery; the representational tools detect "right answer, wrong reason" but cost interpretability machinery. RCL's $\text{Evaluate}(S, c)$ should compose both — a single behavioural axis is provably insufficient (Embers), and a single representational axis ([[control-tasks-probes|Hewitt&Liang]]) is provably under-specified.

**The MDL-on-siblings primitive needs a sibling generator.** [[../concept-learning/recursive-concept-evolution]] introduces MDL on siblings as the canonical concept-vs-pattern test; [[../synthesis/proposed-method]] flags gap #3: *what is a sibling?* Three captured papers answer this directly: [[contrast-sets]] (manual local perturbations), [[gsm-symbolic]] (symbolic templates), [[counterfactual-tasks]] (counterfactual content). Contrast-sets is the closest fit — small, local, label-flipping — and is the recommended sibling-generator for the RCL Phase-0 build-out (workstream B6).

**Diagnosing "understanding" requires controlling for output probability.** [[embers-autoregression]] shows that output-probability shifts can produce ~40-percentage-point swings on tasks the model "understands" by other measures. Any $\text{Evaluate}(S, c)$ that does not pair high-prob and low-prob output variants is unreliable as a concept-understanding signal. This is a foundational caveat across all behavioural axes in the theme.

**Compositional combination is the only retest that scales beyond single-concept probes.** Eight of the nine sources test single-concept understanding under perturbation. [[skill-mix]] is the outlier — it tests cross-concept *combination* in a combinatorial space too large for memorisation. RCL's [[../synthesis/recursive-concept-learning]] **G2** (compositional root retest) and proposed-method's implicit compositionality assumption have no other corpus support.

**Behavioural-test-design is a research field, not just a battery.** [[checklist-behavioral]] argues — and the user-study supports — that *what tests are written* matters as much as *what model is tested*. The capability × test-type matrix gives the project a structured frame for E1; without it, the battery accretes ad hoc axes per concept.

## Open questions for the project

- **Sibling generation by LLM.** [[contrast-sets]] requires expert human authors at 17–50 hours per 1000 examples; can a frontier teacher LLM generate concept-faithful contrast sets, and how is faithfulness audited? Direct blocker for Phase-0 workstream B6.
- **Qualitative concept evaluation.** Eight of nine sources address procedural / well-defined-output concepts. Only [[checklist-behavioral]] generalises directly to qualitative concepts (e.g., sentiment, coherence) via INV/DIR. Whether MDL, IIA, or contrast-set machinery transfers to "supply and demand" or "idealism" is open. RCL **E2** deliverable.
- **Contamination resistance.** [[gsm-symbolic]] flags that any published evaluation set risks contamination; private-template generation is a partial answer. Phase-0 must version-lock its evaluation set away from any teacher-model training corpus.
- **Behavioural-vs-representational disagreement as a memorisation signal.** [[causal-abstraction]] asserts that high task accuracy + low IIA is a "right answer, wrong reason" signature. Is the converse useful — high IIA + low behavioural pass-rate = "concept installed but not used"? Open across the RCL design space.
- **Compositional retest at small N.** [[skill-mix]] uses N=101 skills, k≤5. For RCL's Phase-1 with 3 concepts, the analogue is k=2 over 3 = 3 pairs, plus k=3 = 1 triple — a tiny combinatorial space. Whether the methodology survives at N=3 is empirical.

## Source PDFs

All under `../../../raw/research/concept-understanding-eval/`:
- `01-gsm-symbolic.md` (arXiv 2410.05229)
- `02-math-perturb.md` (arXiv 2502.06453)
- `03-counterfactual-tasks.md` (arXiv 2307.02477)
- `04-skill-mix.md` (arXiv 2310.17567)
- `05-checklist-behavioral.md` (arXiv 2005.04118)
- `06-contrast-sets.md` (arXiv 2004.02709)
- `07-causal-abstraction.md` (arXiv 2301.04709)
- `08-control-tasks-probes.md` (arXiv 1909.03368)
- `09-embers-autoregression.md` (arXiv 2309.13638)

## Test-dataset references (not ingested as primary pages)

Sources whose datasets are useful as test-data resources for the project, but whose method/findings are not load-bearing enough to warrant a full per-paper page. Captures preserved in `raw/research/dataset-references/` for future targeted use.

| Source | Datasets | Properties | Captured |
|---|---|---|---|
| **Learning from Less** (arXiv:2604.18381) | (1) **Counting Problems** — templated sequence-counting with conditional filters + transformations; basic / conditional / threshold / arithmetic / extrema / bitwise operators; compositional depth 1–7 steps. (2) **Graph Reasoning** — procedurally-generated graph-theoretic problems (vertex cover, max clique, Hamiltonian path, graph metrics, etc.); 5–25 nodes; networkx-validatable. (3) **Spatial Reasoning** — 2D grid + particles + movement/rotation actions; absolute and relative-location queries; deterministic simulator ground-truth (extends Dsouza et al. 2025). | All three: programmatic ground-truth, controllable complexity, exact-match evaluation, no LLM-as-judge dependency. **Marked 2026-05-14**: paper itself low-relevance for this wiki's frame; datasets retained as future test-set candidates for concept-evaluation / RCL **E1**-style batteries. | `raw/research/dataset-references/01-learning-from-less.md` |

## Related themes

- [[../concept-learning/_overview]] — sibling theme; concept-as-architectural-commitment (CBM, RCE) where this theme is concept-as-evaluation-target
- [[../synthesis/recursive-concept-learning]] — primary consumer; **E1** battery and **G2** compositional retest both source from here
- [[../synthesis/proposed-method]] — gap #3 (sibling-set construction) closed by [[contrast-sets]]; gap #6 (LLM concept-probe metric) addressed across the theme
- [[../synthesis/concept-curriculum-method]] — §First-experiment four-part contract (memorisation-vs-understanding probes) sources from this theme
- [[../single-sample-rl-finetuning/rlvr-incentivizes-reasoning]] — CoT-Pass@K is a single-axis behavioural probe; this theme provides the broader battery
- [[../in-context-learning-theory/icl-bayesian-inference]] — Bayesian-ICL output-probability theory complements [[embers-autoregression]] empirics
