# KnowRL vs Sakana RLT — minimal-sufficient hints vs maximal-context + plausibility regularisation

## Positions

**Position A — Sakana RLT ([[../research/teacher-student-rl/sakana-rlt]]).** Give the teacher the full (question, solution) pair, let it generate detailed "connect-the-dots" think-token explanations for the student, and regularise the teacher with a KL-to-student-prior loss $r^{KL}$ that keeps the explanation plausible given just the question (without the solution). The 7B RLT-teacher beats 670B+ teacher pipelines specifically because it can exploit the full solution context to teach effectively while $r^{KL}$ prevents it from leaking the answer verbatim.

**Position B — KnowRL ([[../research/teacher-student-rl/knowrl]]).** Decompose the guidance into *atomic knowledge points* (KPs) and use Constrained Subset Search to find the *minimal-sufficient* KP subset — the fewest KPs that still unlock the problem for the student. KnowRL explicitly uses **no KL loss** during training; Figures 1b/3 show that full-KP injection sometimes *regresses* performance on subsets. The principle: more teacher context is not better; too much guidance introduces redundancy and inconsistency, hurting the student's ability to internalise the reasoning.

## Resolution rule

*(Open — no ruling yet.)*

The two positions target *different* student-capability regimes and different hint *shapes*:
- **RLT** provides a full worked solution in the teacher's prompt; the teacher's output is a free-form explanation; the student consumes the explanation. The hint is *dense, unstructured, full-context*.
- **KnowRL** provides atomic discrete KPs as explicit prefix context; the student is expected to use only the KPs it needs. The hint is *sparse, structured, subset-selected*.

The conflict may partially dissolve because the mechanisms are solving different subproblems:
- RLT's $r^{KL}$ regulariser prevents the *teacher* from trivially parroting the solution in its explanation.
- KnowRL's CSS prevents the *training signal* from being diluted by redundant hints.

But as a **hint-design principle**, they disagree: *maximise* context + regularise for plausibility (RLT) vs *minimise* hints to atomic necessity + don't regularise (KnowRL).

**What would resolve it:** an ablation on the same base student that compares (a) RLT-style full-solution-in-prompt + $r^{KL}$, (b) KnowRL-style minimal-KP subset, (c) hybrid (KP-selected minimal context + plausibility regularisation). KnowRL's Figure 1b suggests (b) outperforms full injection; no captured source tests (c).

**Relevance to the project's curriculum-method design ([[../research/synthesis/concept-curriculum-method]]):**
- Step (b) "Per-concept packet construction" uses RLT-shaped (Q, E, A) triples — closer to Position A.
- But if KnowRL's minimal-sufficiency result generalises, the textbook-body portion of the packet should be *pruned* to essential KPs rather than full chapter prose.
- An explicit design choice in the project is now whether the student training loop sees *full textbook* (RLT-compatible), *minimal-KP subset* (KnowRL-compatible), or a curriculum from sparse → dense (analogous to [[../research/single-sample-rl-finetuning/cbrl]]'s annealing, but applied to hint *density* rather than hint *probability*).

## Source

Surfaced via the 2026-04-23 weekly sweep. KnowRL (arXiv:2604.12627) Sec 4.2 and Figs 1b/3 — see `## Conflicts raised` in [[../research/teacher-student-rl/knowrl]].

## Related

- [[../research/teacher-student-rl/knowrl]] — Position B paper
- [[../research/teacher-student-rl/sakana-rlt]] — Position A paper
- [[../research/teacher-student-rl/saha-teacher-explanations]] — adjacent (inference-time teacher explanation with Theory-of-Mind; provides a *third* position on hint density)
- [[../research/teacher-student-rl/rlt-followups-2026]] — OPSD/SDPO use privileged-info teacher context similar to RLT
- [[../research/synthesis/concept-curriculum-method]] — project method directly affected by this resolution
- [[../research/synthesis/proposed-method]] — reference-grounded variant where textbook-in-context aligns with Position A
- [[../weekly-briefs/2026-04-23]] — brought in by the 2026-04-23 weekly sweep
