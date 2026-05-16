# Skill-Mix: A Flexible and Expandable Family of Evaluations for AI Models

SKILL-MIX tests whether LLMs can flexibly compose skills by randomly sampling k-subsets from N skills and asking models to generate text on a given topic demonstrating all k skills simultaneously. With N=101 skills and k ≥ 4, the combinatorial explosion (C(N,k) > 10^10) makes exact training-set memorization infeasible. Yu, Kaur, Gupta, Brown-Cohen, Goyal, and Arora demonstrate that GPT-4 achieves reasonable performance on k=5, suggesting genuine compositional generalization beyond "stochastic parrot" behavior. ArXiv 2310.17567 (2023).

## Method

**Protocol & Skill List.** SKILL-MIX uses N=101 language skills selected from logic, rhetoric, and theory of mind textbooks, filtered to avoid over-specialized or incomposable concepts. Each skill has a Wikipedia entry and definition comprehensible to college students. Skills include metaphor, modus ponens, red herring, and self-serving bias. A separate list of T=100 topics with low unigram frequency (~10^−6, e.g., "dueling," "gardening") ensures low probability in training corpora.

**k-subset sampling & generative task.** For each evaluation round, the framework samples a random k-subset of skills and one topic. The student model receives skill definitions with illustrative examples, then must produce 3-4 sentences on the topic demonstrating all k skills simultaneously. The student is allowed two generation rounds (with reflection) before final submission.

**Grading rubric.** Four criteria are evaluated: (1) k skills used correctly (~1 point each); (2) topical adherence (~1 point); (3) coherence/sensibility (~1 point); (4) sentence count ≤ k−1 (~1 point). Total possible score: k+3 points. Auto-grading uses GPT-4 or LLaMA-2-70B-Chat, with human spot-checking of rubric application.

**Combinatorial infeasibility.** For N=101, k=4: C(101,4)≈4×10^6 possible 4-tuples. For k=5: C(101,5)≈8×10^7. Each topic-skill combination (k skills + 1 topic) is unlikely in training unless the model memorized that exact instance. The joint probability of observing a specific k-tuple on a specific rare topic (unigram freq ~10^−6 each) in a training corpus is bounded by p_s^k × p_t × L, where p_s is average skill frequency, L is corpus token count. For k=5, estimated upper bound is ~0.07 on RedPajama; for k=6, ~0.001. Thus correct answers above this threshold provide evidence of genuine composition rather than recall.

## Claims

1. **Compositional generalization is measurable via k-subsets.** GPT-4 achieves reasonable performance on k=5 (36–38% "Ratio of Full Marks" depending on grader), demonstrating ability to compose 5 skills unseen in tandem during training.

2. **Larger models have higher saturation points.** Within the LLaMA-2 family (7B/13B/70B), saturation k increases with scale. LLaMA-2-70B-Chat performs better at k=3 than its 7B and 13B variants, corroborating Arora & Goyal's emergence theory.

3. **GPT-4 goes beyond stochastic parrot behavior.** At k=5, GPT-4's performance (α_5 ≈ 0.12) exceeds the stochastic parrot threshold (p_s^5 × p_t × L ≤ 0.07), meaning >1/3 of correct answers involve novel skill-topic combinations unseen in training.

4. **SKILL-MIX reveals "cramming for leaderboards."** Models ranked high on Open LLM Leaderboard (LLaMA-2 derivatives, Falcon-180B) perform poorly on SKILL-MIX (k=3+), worse than base LLaMA-2-70B-Chat. Suggests optimization for benchmark performance harmed compositional reasoning.

5. **Existing evaluations saturate quickly.** AlpacaEval, despite being only 6 months old when tested, shows 90%+ win rates for 13B models. SKILL-MIX avoids saturation via adjustable k and combinatorial task space.

6. **Auto-grading with human spot-checking is reliable.** GPT-4 and LLaMA-2-70B grading correlate with human judgments better than inter-human agreement, indicating consistent rubric application is feasible at scale.

7. **Family bias in LLM graders is significant.** LLaMA-2-70B assigns systematically higher scores to LLaMA-2-7B and LLaMA-2-13B than GPT-4 does, requiring human verification of grading for fairness.

8. **Skill selection impacts difficulty.** Filtering out common skills (≥5% corpus frequency, n=17 skills removed) substantially increases task difficulty for all models, improving discriminative power.

## Relevance to the project

**Skill-Mix as compositional root retest for RCL.** Recursive Concept Learning (RCL) aims to build concept DAGs where higher-order concepts compose lower-level skills. Skill-Mix provides a direct, quantitative test of whether fine-tuned models can actually *compose* their learned skills—not just apply them individually. A concept-based curriculum that claims to teach "metaphor + statistical reasoning + modus ponens" must pass Skill-Mix(k=3) on those exact skills as a verification that composition occurred. Skill-Mix differs from single-concept tests (e.g., "use metaphor correctly") by forcing simultaneous demonstration, eliminating the fallback of sequential or partial application.

**Scalability for small curricula.** For a small concept-learning project with 20–50 target skills, running Skill-Mix(k=2,3,4) requires only C(50,4)≈230k combinations—manageable with modest compute. Human grading 50–100 random samples per k provides reliable signal with 2–3 researchers. Unlike benchmark evaluations requiring large test sets, Skill-Mix's sampling approach allows rigorous evaluation on tight budgets.

**Extension to non-English domains (e.g., math concepts).** Skill-Mix generalizes beyond language skills. For a mathematics concept curriculum, "skills" could be proof techniques (induction, contradiction, modular arithmetic) and "topics" could be problem archetypes (graph colorability, number theory, combinatorial counting). The rubric adapts: does the solution employ all k proof techniques on the given problem type without relying on rote memorization? For code, skills = design patterns or algorithmic primitives; for music theory, skills = harmonic functions or voice-leading rules. The core insight—that random k-tuples exceed training-set diversity—holds across domains. Defining domain-specific skill descriptions with worked examples (analogous to Wikipedia entries for language) is the main engineering effort.

## Source

- arXiv: 2310.17567
- Raw markdown: `../../../raw/research/concept-understanding-eval/04-skill-mix.md`

## Related

- [[_overview]] — concept-evaluation theme overview
- [[checklist-behavioral]] — sibling methodology paper; CheckList tests one capability at a time, Skill-Mix tests $k$-way composition
- [[../synthesis/recursive-concept-learning]] — direct payload for **G2** (compositional root retest); the *only* concept-evaluation paper in the captured set that tests cross-concept composition
- [[../synthesis/proposed-method]] — addresses the implicit compositionality assumption — proposed-method has no compositional retest; Skill-Mix is the candidate
- [[../concept-learning/_overview]] — concept-learning theme; Skill-Mix is the concept-composition retest the theme was missing
- [[../teacher-student-rl/rlt-followups-2026]] — ExGRPO's "conceptual inversion" critique is structurally similar to the Skill-Mix combinatorial argument
