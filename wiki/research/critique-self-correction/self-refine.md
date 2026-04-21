# SELF-REFINE: Iterative Refinement with Self-Feedback

Madaan et al., 2023. A single frozen LLM alternates between FEEDBACK and REFINE prompts on its own output, with no training, no extra model, and only few-shot exemplars supplying the supervision. Demonstrates ~20% absolute average improvement across 7 generation tasks (dialogue, code optimization, sentiment reversal, acronym generation, constrained generation, math, code readability) on GPT-3.5/ChatGPT/GPT-4.

## Method
- Three task-specific few-shot prompts: `p_gen` (initial), `p_fb` (feedback), `p_refine` (revision). Same model `M` plays all three roles.
- Iterate: `y_0 = M(p_gen ‖ x)`; for each step `t`, `fb_t = M(p_fb ‖ x ‖ y_t)`; `y_{t+1} = M(p_refine ‖ x ‖ y_0 ‖ fb_0 ‖ … ‖ y_t ‖ fb_t)`. History of prior `(y, fb)` pairs is kept in-context to avoid repeating mistakes.
- Stopping condition is task-specific: max 4 iterations or a model-emitted stop indicator (e.g. a numeric quality score in `p_fb`).
- Crucially, prompts demand feedback that is **specific** (cite the offending span) and **actionable** (propose the fix), not generic.

## Claims
- Table 1: SELF-REFINE beats base across all 7 tasks. Largest gains on Dialogue Response with GPT-4 (25.4 → 74.6, +49.2), Constrained Generation with GPT-4 (15 → 45, +30), Sentiment Reversal with GPT-4 (3.8 → 36.2, +32.4). Code Optimization (GPT-4) +8.7.
- Math Reasoning is the lone near-no-op (GSM8K +0–0.2). Failure mode: ChatGPT produces "everything looks good" feedback for 94% of math instances; gains return (+5%) when an external verifier flags wrong answers (App. H.1).
- Table 2 ablation: actionable feedback > generic feedback > no feedback (e.g. Sentiment Reversal: 43.2 / 31.2 / 0).
- 1-vs-k comparison (Fig. 6, App. H): SELF-REFINE beats *all* k=4 sampled outputs from the same base, ruling out "more samples" as the explanation.
- Negative result with weaker models: Vicuna-13B fails to follow the feedback prompt format and ignores even oracle feedback. Self-refine appears to require an instruction-tuned base of at least GPT-3.5 calibre.

## Sample efficiency
The "seed" is just three few-shot prompts (≈ 6–8 exemplars total per task) plus the input `x`. Supervision is amplified entirely at inference: the critique signal manufactures its own gradient direction in token-space. No training data, no labels, no reward model. The substitution is striking — a handful of demonstration triples `⟨x, y, fb⟩` plus quadruples `⟨x, y, fb, y'⟩` produces gains comparable to fine-tuning. The catch: the base model must already be capable enough to (i) detect its own errors and (ii) follow specific revision instructions. Small/weak models lack both, so the seed→performance amplification is contingent on base-model self-evaluation capability.

## Relevance to the project
The "feedback as decomposed sub-rewards" pattern is directly relevant. SELF-REFINE shows that a single LLM can produce per-aspect critiques (e.g. for Acronym Generation: numerical scores per quality dimension, then a balanced selection across iterations). This is a model for decomposing a single concept-bearing example into multiple component sub-signals: instead of one scalar "did the model get it", a critique can emit `{principle_match, generality, contrast, edge_case}` scores. Two cautions: (1) the math failure mode warns that self-critique requires the model to *be able to detect* the error class — concept-level errors may be invisible to the same policy that produced them; (2) Vicuna-13B failure suggests that for 1–13B models, critique would need to come from a separate, more capable judge rather than the policy itself.

## Source
- arXiv: 2303.17651
- Raw markdown: `../../../raw/research/single-sample-llm-learning/27-G-1-self-refine.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/G-1-self-refine.pdf`

## Related
- [[constitutional-ai]]
- [[reflexion]]
- [[../self-improvement/star]]
- [[../process-reward-models/_overview]]
