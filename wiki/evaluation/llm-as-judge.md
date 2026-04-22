# LLM-as-Judge: When and How

LLM-as-judge is the scaling tool for evaluation *once* [[error-analysis]] has surfaced the actual failure modes. Applied too early, it calibrates against imagined failures and produces confident but misleading metrics.

## Preconditions

- **100+ human-labeled examples** before defining the judge. *(Hamel / Shreya 2026-01, practitioner-consensus.)*
- A **failure taxonomy** from [[error-analysis]].
- A **scoped, narrow question** — one failure mode per judge, not "is this response good?"

## Label schema

**Binary pass/fail**, not Likert scales. Practitioner rationale:

- Likert midpoints hide uncertainty — annotators cluster at 3/5 when unsure, which is noise.
- Binary forces a decision; qualitative critique fields capture nuance.
- Faster to annotate; requires smaller samples for the same statistical effect size.

*(Hamel / Shreya 2026; evidence class: practitioner-consensus with cited consulting-sample experience.)*

## Calibration protocol

1. Hold out human labels (~20% stratified slice).
2. Run the judge on the held-out set.
3. Measure agreement — **target >90% alignment** with human judgment.
4. If misaligned, refine the judge prompt or narrow the question; re-measure.
5. **Re-calibrate weekly** — criteria drift as you see more outputs.

*(Hamel / Shreya 2026; cites Shankar et al. "Who Validates the Validators?" arXiv, on criteria drift.)*

## Known biases

- **Option-ordering bias** in multi-choice judges.
- **Self-preference bias** — the judge model favors outputs from its own model family.
- **Formatting / verbosity bias** — longer responses scored higher.
- **Mitigation:** narrow scope, blind positioning, validate per-model, compare judgments across judge models.

## When *not* to use LLM-as-judge

- Before [[error-analysis]]. You'll be measuring imagined failures.
- For nuanced multi-dimensional quality. Use multiple scoped binary judges, not one "holistic" judge.
- When cheaper deterministic alternatives exist. Use the [[failure-modes#the-cost-hierarchy|cost hierarchy]]: assertions → reference checks → judge.

## Judge-model choice

Start with capable models (GPT-4o-class, Claude Sonnet-class at 2025–2026 tier). Optimize cost only after calibration is locked in. Weaker judges save money but re-open the 90%-alignment gap. *(Hamel / Shreya 2026-01, practitioner-consensus.)*

## Source

- `raw/research/effective-agentic-patterns/05-hamel-llm-evals-faq.md` — Hamel Husain and Shreya Shankar, 2026-01-15. Cites Shankar et al. "Who Validates the Validators?" arXiv.

## Related

- [[error-analysis]] — prerequisite
- [[failure-modes]] — cost hierarchy and what judges cannot catch
- [[benchmarks]] — why public benchmarks are not a judge substitute
