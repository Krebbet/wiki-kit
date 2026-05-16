# Curriculum and Decomposition

Theme covering *prior art for choosing what to teach next and decomposing concepts into prerequisites*. The unifying question across the nine sources: **given a learner with partial mastery, how does a teacher decide what concept to surface or train next?** Four sub-fields converge here — knowledge tracing (mastery inference from response history), prerequisite-graph learning (text-driven concept dependency inference), hierarchical RL (temporal abstraction over sub-policies), and curriculum learning (easy-to-hard ordering, automatic curricula, open-ended evolution).

The theme exists because [[../synthesis/recursive-concept-learning]] (RCL) entered with several "no corpus method" gaps in its design — D1 (diagnostic decomposition), E3 (concept identity), curriculum-level credit assignment (gap #1), and **D2** (learnability filter / `MAX_DEPTH`). After this ingest five of those gaps move from "no corpus" to "concrete prior art".

## Pages

| Page | Type | One line |
|---|---|---|
| [[dkt]] | model | RNN over student response history; +25% AUC over Bayesian KT; implicit prereq-discovery via influence function. |
| [[auto-kc-generation]] | model (LLM-based) | LLM-generated knowledge components beat human-written labels on KT (AUC 0.816 vs 0.797). The strongest single corpus signal that LLM diagnostic decomposition is feasible. |
| [[lecturebank]] | dataset | 1352 NLP-domain lectures + 208 manually-labelled prereq-concept pairs. The canonical NLP-domain prereq benchmark. |
| [[concept-prereq-relations]] | method | PREREQ — pairwise-link LDA + Siamese network for asymmetric prereq inference; F=59-60 on universities + MOOCs. |
| [[options-framework]] | theory | Sutton-Precup-Singh $\langle I, \pi, \beta \rangle$ option triple + SMDP framing. The HRL canon. |
| [[bengio-curriculum]] | theory | Curriculum learning as continuation method for non-convex optimisation; the original ICML 2009 paper. |
| [[curriculum-survey]] | survey | Soviany et al. 2022 IJCV — taxonomy across 200+ curriculum-learning papers. |
| [[acl-deep-rl-survey]] | survey | Portelas et al. 2020 — RL-specific curriculum survey; LP, ALP-GMM, teacher-student bandits. |
| [[poet]] | algorithm | Co-evolving environments + agents + transfer attempts; emergent stepping-stone curriculum with no predetermined target. |

## Four sub-fields, one map

| Sub-field | Question | Sources | Where it plugs into RCL |
|---|---|---|---|
| **Knowledge tracing** | Given response history, what's the student's mastery of concept $c$? | [[dkt]], [[auto-kc-generation]] | Backend for $V$.Evaluate confidence calibration; backbone for D1 when the teacher is itself an LLM doing KT |
| **Prereq-graph learning** | Given a concept, what other concepts must be learned first? | [[lecturebank]], [[concept-prereq-relations]], [[auto-kc-generation]] | Direct payload for **D1** (Decompose) and **E3** (Identity); seeds the teacher prompt with prior structure |
| **Hierarchical RL** | How do we frame a sub-policy with its own start, internal logic, and termination? | [[options-framework]] | RCL's $\text{LearnConcept}(p)$ is structurally an option; intra-option learning is the canonical mechanism for **curriculum-level credit assignment** (gap #1) |
| **Curriculum learning** | What ordering of training data / tasks helps? | [[bengio-curriculum]], [[curriculum-survey]], [[acl-deep-rl-survey]], [[poet]] | Theoretical frame for "decompose to prereqs first"; LP / ALP-GMM as **D2** learnability filters; POET as the closest-spirit-match for failure-driven lazy DAG expansion |

## Cross-cutting themes

**Failure-driven decomposition is the single missing piece across all four sub-fields.** [[lecturebank]] and [[concept-prereq-relations]] learn prereqs from text occurrence and document order, not from observed student errors. [[dkt]] learns from response history but the *concept set* is fixed; it cannot propose new prereqs. [[auto-kc-generation]] generates KCs from problem text rather than failure traces. [[options-framework]] assumes options are *given*. [[poet]] mutates environments randomly with no diagnostic. RCL's D1 — "infer the missing prereq from the student's failure trace" — sits in a gap none of these papers fill. The 2025 LLM-KT result ([[auto-kc-generation]]) is the strongest signal that an LLM teacher can do this *competitively with human experts when seeded with problem text*; whether that extends to *failure-trace input* is open.

**Two notions of "curriculum" co-exist in the corpus.** Pre-built (Bengio's hand-authored ordering, LectureBank's expert-labelled DAG) and emergent (POET's mutation+filter, ACL's learning-progress signal). RCL is on the emergent side, but with a *goal-directed* teacher rather than POET's random mutation. This combination — emergent + goal-directed — is structurally novel; the closest existing instances are [[acl-deep-rl-survey]]'s teacher-student bandits.

**Credit assignment is the recurring unsolved problem.** In KT, the question is "which past response best predicts future mastery"; in HRL it's "which option deserves credit for the cumulative reward"; in RCL it's "which missing prereq caused the parent failure". [[options-framework]]'s intra-option learning is the most direct theoretical tool but assumes a Markov state that curriculum state lacks. None of these four sub-fields offers a curriculum-level credit-assignment method that lifts cleanly to RCL.

**The 2025 LLM signal is decisive.** [[auto-kc-generation]] shows GPT-4o-generated KCs beat human-written labels on KT performance (AUC 0.816 vs 0.797, p < 0.05). This is the first paper in the wiki demonstrating that an LLM teacher does fine-grained concept-decomposition *better* than human experts on a downstream learning task. RCL's D1 viability rests on this finding generalising to failure-trace-conditioned inputs.

## Open questions for the project

- **Does the LLM-KC-generation result extend to failure-trace input?** [[auto-kc-generation]] generates KCs from problem text. RCL's D1 requires generating prereqs from a *student failure trace*. No corpus paper has tested this; closest is [[../teacher-student-rl/saha-teacher-explanations]] but it's per-instance, not curriculum-level.
- **Curriculum-level credit assignment.** [[options-framework]] gives the SMDP frame but the curriculum-state Markov assumption fails in practice. [[acl-deep-rl-survey]]'s LP signal sidesteps the credit-assignment question by using a surrogate objective. Open.
- **How to use DKT/KT for confidence calibration at small N.** [[dkt]] requires substantial response history per student; RCL operates with 5–10 items per concept. Few-shot KT is an open empirical question.
- **POET-style transfer-attempt at the concept level.** [[poet]]'s "does agent B solve environment A?" check is a candidate analogue of "did training prereq c1 also unlock parent c?" — but the parent retest in RCL is the only step that exercises this, and it's binary (PASS/FAIL) rather than gradient-of-improvement. Whether finer-grained "improvement transfer" is measurable is open.

## Source PDFs

All under `../../../raw/research/rcl-gap-fillers/`:

- `01-dkt.md` (arXiv 1506.05908)
- `02-lecturebank.md` (arXiv 1811.12181)
- `03-concept-prereq-relations.md` (arXiv 1811.12640)
- `04-options-framework.md` (AIJ 1999, no arXiv)
- `05-bengio-curriculum.md` (ICML 2009)
- `06-poet.md` (arXiv 1901.01753)
- `07-curriculum-survey.md` (arXiv 2101.10382)
- `08-acl-deep-rl-survey.md` (arXiv 2003.04664)
- `09-auto-kc-generation.md` (arXiv 2502.18632)

## Related themes

- [[../synthesis/recursive-concept-learning]] — primary consumer; this theme fills D1, E3, D2, and gap #1 (curriculum credit assignment)
- [[../concept-evaluation/_overview]] — sibling theme on evaluation primitives; concept-evaluation supplies the `Evaluate(S, c)` axes, this theme supplies the *what to teach next* logic
- [[../teacher-student-rl/_overview]] — modern teacher-student RL inherits the ACL teacher-student bandit frame ([[acl-deep-rl-survey]]) and extends it to LLM-scale
- [[../concept-learning/_overview]] — concept-as-architectural-commitment vs concept-as-prereq-node — adjacent ontologies; RCE's spawn-on-failure is POET's mutation+filter at the concept-library level
- [[../single-sample-rl-finetuning/data-efficiency-rft]] — the wiki's data-side curriculum coverage; this theme adds the algorithmic/methodological side
