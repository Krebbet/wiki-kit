# GSM-Symbolic: Understanding the Limitations of Mathematical Reasoning in Large Language Models

Mirzadeh et al. (Apple & Washington State University; arXiv 2410.05229, 2024) introduce GSM-Symbolic, a symbolic-template-based benchmark for evaluating mathematical reasoning in LLMs. Rather than relying on fixed test sets like GSM8K, they generate diverse question variants to probe whether models truly reason or merely pattern-match. Their core finding: all SOTA LLMs exhibit high variance across equivalent problem instances and catastrophic performance drops when facing out-of-distribution patterns—suggesting reasoning is brittle pattern-matching, not formal logic.

## Method

GSM-Symbolic is built from 100 handcrafted symbolic templates derived from GSM8K test examples. Each template identifies variables (with constrained domains), explicit conditions (e.g., divisibility to ensure whole-number answers), and uses common proper names for standardization. Automated checks verify no original values leak into templates, solutions remain correct, and at least two models solve each generated question. The authors deliberately select numerical ranges aligned with the original GSM8K to isolate logical reasoning from arithmetic capability.

Evaluation uses 100 templates, sampling 50 instances per template for 5000 total examples across 50 independent datasets. Standard protocol: Chain-of-Thought (CoT) prompting with 8-shot greedy decoding. Models span open (2B–27B: Llama3-8b, Gemma2-9b, Phi-3.5-mini, etc.) and closed (GPT-4o, GPT-4o-mini, o1-mini, o1-preview) classes. The authors also introduce GSM-Symbolic-Minus-1 (GSM-M1), GSM-Symbolic-Plus-1 (GSM-P1), and GSM-Symbolic-Plus-2 (GSM-P2) by removing or adding clauses to vary difficulty. Finally, GSM-NoOp adds seemingly relevant but mathematically irrelevant clauses to probe true concept understanding.

## Claims

- **High variance across equivalent instances** (Sec. 4.1): Gemma2-9b shows >12% gap between worst and best performance across 50 datasets; Phi-3.5-mini variance also substantial. GSM8K reported metrics fall outside the distribution center, suggesting data contamination (Fig. 2).

- **Performance drops from GSM8K to GSM-Symbolic** (Sec. 4.1, Fig. 3): Closed models (GPT-4o, o1-preview) show larger absolute drops if their GSM8K accuracy is right-skewed on the Symbolic distribution, indicating potential overfitting to contaminated training data.

- **Numerical sensitivity > name sensitivity** (Sec. 4.2, Fig. 4): Models robust to changing proper names (small variance) but highly sensitive to numerical value changes. Original GSM8K performance much closer to name-only-changed distribution, confirming reliance on surface pattern-matching.

- **Performance degrades with clause count** (Sec. 4.3, Fig. 6): As difficulty increases (GSM-M1 → GSM-Symbolic → GSM-P1 → GSM-P2), accuracy declines and variance increases consistently across all models. Rate of accuracy drop accelerates, faster than linear in steps, suggesting pattern-matching breaks under complexity.

- **Catastrophic failure on irrelevant information** (Sec. 4.4, Fig. 8a): Adding seemingly relevant but operationally irrelevant clauses causes up to 65% performance drop (Phi-3-mini >65%, o1-preview significant decline). Models blindly convert statements into operations (e.g., treating "discount" as multiplication) without semantic understanding.

- **In-context examples don't fix irrelevance blindness** (Sec. 4.4, Fig. 8b–8c): Even with 8 shots from GSM-Symbolic showing the correct reasoning chain, performance on GSM-NoOp remains depressed, suggesting models cannot selectively ignore irrelevant information. Counterintuitively, some weaker models outperform stronger ones on NoOp-NoOp (all shots from GSM-NoOp).

## Relevance to the project

**Evaluation primitive for concept understanding vs memorisation**: GSM-Symbolic directly targets the core question: do LLMs *understand* mathematical concepts or memorise training patterns? The variance across equivalent instances and sensitivity to irrelevant clauses are diagnostic signals that a model has not grasped the conceptual core—only the surface regularities. This maps cleanly to your `Evaluate(S, c)` battery: a concept is "understood" if the model generalizes to unseen instantiations; if performance collapses on semantically equivalent variants (e.g., numeric substitutions, added irrelevant facts), the model has memorised patterns, not internalised the concept.

**Plug into procedural and qualitative concept evaluation**: For procedural concepts (e.g., "long division", "syllogistic reasoning"), GSM-Symbolic's template-based generation can be adapted: create symbolic templates of the procedure, vary parameters (dividend, operands, logical premises), and measure robustness to numerical perturbations and spurious clauses. For qualitative concepts (e.g., "irony", "contradiction"), a similar probe—generate near-equivalent examples with irrelevant but plausible noise—can reveal whether the model has semantic grasp or only surface-token mimicry. The GSM-NoOp design is especially portable: any concept-learning system should fail catastrophically if it cannot filter irrelevant information.

**Limitations and caveats**: (a) Sample size: 5000 questions per benchmark is modest for characterising the full performance distribution of large models; statistical power may be limited for fine-grained comparisons. (b) Cost and iteration: symbolic template curation is labour-intensive (100 templates from manual annotation); scaling to diverse concept domains may be slow. (c) Format-vs-substance: GSM-Symbolic probes reasoning *within* natural-language math contexts. Whether findings generalise to other modalities (code, symbolic logic, visual reasoning) is open. (d) Contamination resistance: The paper shows GSM8K contamination is likely in SOTA models, but GSM-Symbolic itself, if published pre-training, could be contaminated by future models; freshness and version-locking of evaluation sets is critical. (e) Grain of measurement: numeric perturbations and clause addition are coarse-grained probes; finer manipulations (word order, synonym substitution) might reveal additional brittleness or unexpected robustness.

## Source

- arXiv: 2410.05229
- Raw markdown: `../../../raw/research/concept-understanding-eval/01-gsm-symbolic.md`

## Related

- [[_overview]] — concept-evaluation theme overview
- [[math-perturb]] — extends the symbolic-perturbation idea to advanced (level-5) MATH problems with hard solution-path-breaking variants
- [[counterfactual-tasks]] — same memorisation-vs-abstraction question via counterfactual content rather than symbolic templates
- [[../synthesis/recursive-concept-learning]] — direct payload for **E1** (multi-axis evaluation battery); the GSM-NoOp design is a candidate axis
- [[../synthesis/proposed-method]] — closes gap #3 (sibling-set construction) and gap #6 (LLM concept-probe metric) for math; symbolic-template variants are a concrete sibling-set generator
- [[../concept-learning/recursive-concept-evolution]] — MDL on siblings; symbolic templates are the math-domain operationalisation
- [[../single-sample-rl-finetuning/rlvr-incentivizes-reasoning]] — CoT-Pass@K shares the format-vs-substance diagnostic frame
