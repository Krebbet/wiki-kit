# MATH-Perturb: Benchmarking LLMs' Math Reasoning Against Hard Perturbations

**arXiv:2502.06453** | Huang et al. (Princeton, Google) | 2025

Large language models exhibit impressive performance on mathematical reasoning benchmarks, but whether this reflects true reasoning or memorization remains unclear. This paper constructs MATH-P-Simple and MATH-P-Hard—two paired benchmarks of 279 perturbed problems derived from level-5 MATH dataset problems—to separate understanding from memorization through systematic perturbation strategies.

## Method

**Perturbation Construction:**
- **MATH-P-Simple** (simple perturbation): Non-essential modifications that preserve underlying reasoning patterns and solution strategies. Example: changing numerical coefficients while keeping the problem structure and solving method identical.
- **MATH-P-Hard** (hard perturbation): Fundamental changes to problem formulation that invalidate the original solution path. Example: changing from finding all integer $n$ to finding the smallest integer $n$ in a floor-division equation—requiring different reasoning despite similar surface structure.

**Curation Protocol:**
Each of 279 problems underwent minimal-edit perturbation (verified via embedding distance and cosine similarity) by human annotators. For hard perturbations, strategies included: changing required output format (e.g., single value vs. all values), modifying constraints (e.g., different divisor in floor operations), and altering problem conditions. All evaluations used zero-shot Chain-of-Thought without tools, verified via symbolic equivalence checking.

## Claims

- **All tested models drop 10–25% on MATH-P-Hard vs. original:** o1-mini −16.49%, gemini-2.0-flash-thinking −12.9%, Claude-3.5-Sonnet ≈−13%, indicating hard perturbations effectively probe reasoning robustness (Table 1).
- **Models suffer only slight drops on MATH-P-Simple:** Test-split drops ≤5% for most models (Table 1), showing improved robustness against simple perturbations vs. prior work (Srivastava et al. 2024), though train-split errors persist.
- **Memorization is a major failure mode:** 20–47% of problems show failures on MATH-P-Hard despite success on easier versions (§3.2). Manual inspection attributes 40% of o1-mini errors and 25% of Claude-3.5-Sonnet errors to memorization.
- **Three distinct memorization patterns identified:** (1) ignoring modified assumptions and reverting to original problem logic (Figure 5); (2) blindly applying techniques without assessing applicability (Figure 1); (3) outputting the desired answer from the original problem rather than the modified one (Figure 6).
- **Mode collapse is minor:** <10% of total errors collapse to identical original answers except for three models, indicating memorization is primarily active reasoning-strategy mismatch, not simple answer recall.
- **Problem diversity across 7 math subjects:** Benchmark spans algebra, counting, geometry, number theory, and other domains (Table 3), with edit-distance distributions validating non-trivial modification (Figure 4).

## Relevance to the project

**Evaluation primitive for understanding vs. memorisation:**
MATH-Perturb provides a direct diagnostic: a model that understands a concept should degrade gracefully and predictably when the problem's core assumptions change, whereas memorized shortcuts produce characteristic failure signatures. For single-sample concept learning, a "hard perturbation" of a learned concept (e.g., a learned visual feature detector, a math reasoning pattern) tests whether the model has internalized the underlying principle or merely locked onto surface patterns. This framework operationalizes the concept evaluation battery's core question: *does this model understand concept $c$ or merely memorize problem instances?*

**Hard-perturbation protocol for teach-then-test:**
The teach-then-test paradigm—fine-tune on a single example of a concept, then probe with perturbed variants—directly mirrors MATH-Perturb's methodology. After teaching a concept via one sample, hard perturbations would test whether the learned concept transfers to fundamentally different problem formulations. Figure 5 and Figure 6 exemplify the exact failure modes to expect: a model may "understand" a concept at the surface but fail to apply it when context shifts. This provides a concrete evaluation template for the Recursive Concept Learning `Evaluate(S, c)` step.

**Limitations as a concept probe:**
MATH-Perturb is task-specific (mathematical reasoning) and relies on human-curated perturbations; scaling to arbitrary concept domains requires problem-specific annotation. Memorization detection here is post-hoc (manual inspection of 20 cases per model) and not fully automated, limiting scalability. Additionally, the paper does not test whether models that pass hard perturbations would succeed on OOD concepts in new domains—hard perturbations remain in-domain (math → math), whereas true concept generalization must cross domains. For wiki purposes, this highlights the need for generalizable perturbation strategies that extend beyond task-parameter changes.

## Source

- arXiv: 2502.06453
- Raw markdown: `../../../raw/research/concept-understanding-eval/02-math-perturb.md`

## Related

- [[_overview]] — concept-evaluation theme overview
- [[gsm-symbolic]] — direct ancestor; MATH-Perturb scales the symbolic-perturbation pattern to the harder MATH dataset and adds the *hard*-perturbation distinction (original solution path no longer applies)
- [[counterfactual-tasks]] — sibling memorisation-vs-abstraction probe via counterfactual content
- [[../synthesis/recursive-concept-learning]] — **E1** axis: hard-perturbation pass-rate is the sharpest test of "the student applies the right concept, not the memorised solution path"
- [[../synthesis/proposed-method]] — gap #6 (LLM concept-probe metric) — hard perturbations are the concrete metric for advanced math concepts
- [[../single-sample-rl-finetuning/1-shot-rlvr]] — 1-shot RLVR uses MATH problems; MATH-Perturb is the canonical retest battery for any MATH-trained model
