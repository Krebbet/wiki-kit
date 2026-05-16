# Evaluating Models' Local Decision Boundaries via Contrast Sets

Gardner et al., EMNLP Findings 2020 (arXiv 2004.02709). **Summary:** Contrast sets are small, expert-constructed collections of inputs that locally perturb test instances to change the gold label, revealing whether a model's decision boundary aligns with the true boundary. Authors created contrast sets for 10 diverse NLP datasets and show models drop significantly in performance (up to 25%) despite not being explicitly adversarial.

## Method

Contrast sets operationalize the idea of "minimally contrastive examples" by having dataset authors (ideally, the original creators) manually perturb test instances in small but label-flipping ways. The core recipe: sample a pivot x from the test set, generate x' similar to x (according to task-specific distance), where y' ≠ y. A contrast set C(x) is any sample from the local decision boundary around x—defined as the partition of input space into labels within distance ε. The model is evaluated on *contrast consistency*: whether it makes correct predictions on all elements of a contrast set simultaneously.

Critically, contrast sets differ from adversarial examples: adversarial perturbations change input while preserving the gold label (testing model robustness), whereas contrast sets change the input *and* the label (testing whether the model's boundary matches the true boundary). The authors recommend *model-agnostic*, post-hoc construction by experts to avoid biasing toward particular models' failure modes. They created contrast sets for 10 datasets spanning visual reasoning (NLVR2), sentiment analysis (IMDb), temporal relation extraction (MATRES), syntactic parsing (UD), argument mining (PERSPECTRUM), reading comprehension (DROP, QUOREF, ROPES, BoolQ), and event understanding (MC-TACO).

## Claims

- **Up to 25% performance drop:** On DROP with MTMSN, contrast consistency degrades from 79.9% (original) to 54.2% (contrast), a 25.7 percentage point drop. (Table 2)
- **Consistent degradation across all 10 datasets:** Every model evaluated performed significantly worse on contrast consistency than on original test set accuracy, indicating systemic overfit to dataset artifacts.
- **Dependency parsing severely affected:** Biaffine + ELMo achieves 64.7% accuracy on original UD test but only 17.3% contrast consistency on PP-attachment contrasts—despite 95.7% unlabeled attachment score on Penn Treebank.
- **Humans succeed where models fail:** Human performance is comparable on contrast sets vs. original test sets (Table 3: IMDb 93.9% vs. 94.3%, PERSPECTRUM 90.3% vs. 91.5%), confirming contrast sets are not inherently harder—models are overfit.
- **Cost is manageable:** Constructing ~1,000-example contrast sets for most datasets required 17–50 hours of expert annotation (1–3 min per example), though complex tasks (parsing) took ~15 min per example.
- **Fine-grained error analysis:** Contrast sets can be labeled by phenomenon targeted, enabling detailed error diagnosis (e.g., MATRES shows models do better on appearance order than temporal conjunction words).
- **Not explicitly adversarial:** Perturbations are designed by task experts without a model in the loop, avoiding bias toward particular models and reflecting the true decision boundary instead.

## Relevance to the project

**Sibling-set construction for MDL:** Contrast sets are a concrete, well-defined recipe for constructing the "sibling sets" needed for component V (gap #3 sibling-set construction) in the proposed-method.md. Rather than paraphrase-based data augmentation, contrast sets flip the label minimally—exactly the kind of hard negative that a teacher LLM or human would recognize as a genuine alternative concept boundary.

**Evaluation axis for Recursive Concept Learning:** The "contrast consistency" metric—whether the model's predictions align across a local neighborhood of label-flipping perturbations—is a natural axis for Evaluate(S, c) in the recursive concept-learning loop. A concept c is well-defined if held-out contrast sets maintain consistency. This is stronger than accuracy on i.i.d. test data and captures whether the learner has truly internalized the concept boundary or merely memorized spurious correlations.

**Manual-to-automated transition:** The paper relies on human experts to construct contrast sets (17–50 hours per 1,000 examples). For scaling single-sample concept learning, the question is whether a teacher LLM can generate contrast sets, and how to audit them for faithfulness. The Gardner et al. result that humans achieve near-identical performance on contrast sets suggests that a high-quality LLM prompt for contrast generation (grounded in the concept definition and known sibling phenomena) could be reliably validated by sampling consistency on a small pilot batch. The challenge: ensuring the LLM-generated perturbations reflect true decision boundaries rather than spurious artifacts.

## Source

- arXiv: 2004.02709
- Raw markdown: `../../../raw/research/concept-understanding-eval/06-contrast-sets.md`

## Related

- [[_overview]] — concept-evaluation theme overview
- [[checklist-behavioral]] — sibling behavioral-testing paper; CheckList = templated coverage matrix, Contrast Sets = manual local-boundary perturbations
- [[gsm-symbolic]] — symbolic templates are the math-domain analogue of contrast sets at scale
- [[../synthesis/recursive-concept-learning]] — **E1** axis (contrast-set pass-rate); also the concrete recipe for **B6** in the Phase-0 dataset workstream
- [[../synthesis/proposed-method]] — **closes gap #3** (sibling-set construction). The "siblings" in component **V** are exactly contrast sets. Strongest direct linkage of any captured paper to a wiki gap.
- [[../concept-learning/recursive-concept-evolution]] — MDL on siblings is operationally meaningful only with a contrast-set-quality sibling pool
