# Beyond Accuracy: Behavioral Testing of NLP Models with CheckList

Ribeiro, Wu, Guestrin, Singh (ACL 2020, Best Paper; arXiv 2005.04118). A task-agnostic methodology for comprehensive behavioral testing of NLP models, inspired by software engineering principles. Proposes a capability × test-type matrix (MFT/INV/DIR) to systematically expose failures in models that appear to solve benchmarks. Includes tooling for templated test case generation at scale.

## Method

CheckList operationalizes behavioral testing through a two-dimensional test matrix: capabilities (rows) and test types (columns). Users fill cells with test cases covering linguistic phenomena (vocabulary, NER, negation, coreference, temporal reasoning, SRL, logic, etc.) that should be manifested in the task at hand.

Three test types structure the evaluation. **Minimum Functionality Tests (MFT)** are simple, focused sanity checks—e.g., "I didn't love the food" should be negative sentiment. Templates + lexicons generate large numbers of diverse instances (via masked language model suggestions). **Invariance Tests (INV)** apply label-preserving perturbations and expect predictions to remain stable—e.g., swapping location names in a sentiment analysis task should not change output. **Directional Expectation Tests (DIR)** expect monotonic or monotone changes—e.g., adding "You are lame" should not increase (or should decrease) sentiment. INV and DIR allow testing on unlabeled data, breaking dependence on ground-truth labels.

The tooling abstracts test generation: templates with placeholder fill-ins (via RoBERTa suggestions or manually curated lexicons), general-purpose perturbations (typos, entity swaps, name changes), and reusable test suites across models and teams. User studies show practitioners with CheckList created twice as many tests and found nearly three times as many bugs (in 2 hours) compared to unaided controls.

## Claims

1. Held-out accuracy overestimates model performance; systematic behavioral testing on specific capabilities reveals critical failures missed by benchmarks (§3: SOTA models with >91% accuracy fail basic negation, NER, coreference).

2. Commercial sentiment analysis models (Microsoft, Google, Amazon APIs) from extensively tested production systems contained previously unknown bugs discovered in a ~5-hour CheckList session (§4.1).

3. MFT failure rates isolate capability gaps independently of dataset bias: BERT/RoBERTa achieve >93% SST-2 accuracy yet fail 54.2% of negation MFTs and >98% on complex negation structures (§3, Table 1).

4. Perturbation-based tests (INV/DIR) enable unlabeled-data evaluation: checking invariance to entity swaps or monotonicity of directional edits does not require ground-truth labels, scaling testing to real-world distributions.

5. User study (18 practitioners, 2 hours, QQP task): Cap.+templ. condition generated 13.5±3.4 tests vs. 5.8±1.1 unaided; 198±96 test cases/test vs. 7.3±5.6 unaided; discovered 6.2±0.9 bugs (severity≥3) vs. 2.2±1.2 (§4.2, Table 4).

6. The capability list (Vocabulary, NER, Taxonomy, Robustness, Fairness, Temporal, Negation, Coreference, SRL, Logic) is task-agnostic and reusable, though domain/task-specific capabilities must be added by users.

7. Behavioral testing decouples from implementation—applied to BERT, RoBERTa, three commercial APIs, all revealing non-overlapping bug profiles on the same tasks.

8. Tested models fail systematic checks for core linguistic phenomena (negation, temporal order, coreference, active/passive) that are prerequisites for task competence, suggesting benchmark accuracy relies on spurious correlations or dataset-specific shortcuts.

## Relevance to the project

CheckList provides the methodological scaffolding for `Evaluate(S, c)` in the Recursive Concept Learning framework. MFT maps to "does the model apply concept *c* under minimal, clean examples?"; INV maps to "does application of *c* remain stable under label-preserving surface perturbations?"; DIR maps to "does the model respect the monotonic direction/logical implications of *c*?" Together, they form a three-axis behavioral signature for procedural concepts (e.g., negation, temporal order, agent/patient role).

For qualitative/non-procedural concepts (e.g., "supply and demand"), INV gains new meaning: the core mechanism (excess supply → price decline) should be invariant to natural language variation—different wordings of the supply shock should yield the same directional outcome. DIR becomes the monotonicity check: adding supply pressure should monotonically weaken the demand signal. Thus CheckList's matrix naturally extends from discrete linguistic phenomena to continuous economic/physical concepts.

User study results (2× tests, 3× bugs in 2 hours) establish the feasibility cost baseline for manual checklist authorship. For teacher-LLM auto-generation of MFT/INV/DIR matrices over procedural concepts, this suggests: (1) the semantic burden of generating clean instances (MFT) and well-crafted perturbations (INV/DIR) is high enough that LLMs must be scaffolded (templates, lexicons, via prompts); (2) the ceiling on finding bugs is task-dependent, but structured matrix thinking yields consistent, multiplicative improvements; (3) reusability across models and tasks (as shown in the three tasks tested) implies that once a concept's matrix is authored, it can be systematized and shared, reducing marginal cost for subsequent learners.

## Source

- arXiv: 2005.04118
- Raw markdown: `../../../raw/research/concept-understanding-eval/05-checklist-behavioral.md`

## Related

- [[_overview]] — concept-evaluation theme overview
- [[contrast-sets]] — sibling behavioral-testing paper; CheckList = capability matrix at scale via templates, Contrast Sets = manual local-boundary perturbations
- [[skill-mix]] — sibling methodology paper for *compositional* skill testing
- [[../synthesis/recursive-concept-learning]] — the methodological *frame* for **E1** — the MFT/INV/DIR triplet is the canonical structure for a multi-axis battery
- [[../synthesis/proposed-method]] — gap #3 (sibling-set construction); INV templates *are* sibling-set generators
- [[../concept-learning/concept-bottleneck-models]] — CBM tests at the *concept* level; CheckList tests at the *capability* level — adjacent operationalisations
