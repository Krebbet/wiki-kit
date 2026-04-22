# Error Analysis: The Evaluation Foundation

Hamel Husain and Shreya Shankar's most-repeated claim across the captured corpus: **everything else in evaluation is downstream of systematic error analysis on real traces**. Automated checks, LLM-as-judge, and benchmark suites scale only after you have identified your system's specific failure modes by reading its output by hand.

## The cycle

1. **Create a dataset** of actual traces from the system — real or realistically synthetic (grounded in real DB constraints). Target 100+ traces before stopping.
2. **Open coding** — read each trace and journal freeform notes on what went wrong. No categories yet.
3. **Axial coding** — cluster the notes into a failure-mode taxonomy. Three failure types typically account for 60%+ of problems. *(Practitioner-consensus from Hamel's consulting sample.)*
4. **Iterate to theoretical saturation** — keep reading until new traces surface no new failure modes.

*(Hamel / Shreya 2026, practitioner-consensus, grounded in consulting work across 50+ companies and 4,000+ students via the Hamel/Shreya evals course.)*

## Sampling strategy

Don't sample randomly. **Stratify** by:

- User type or persona.
- Feature or query category (e.g., temporal reasoning, multi-source fusion, ambiguous intents).
- Outlier signals — long sessions, low user-feedback scores, embedding outliers.

## Custom annotation tooling is table-stakes

Hamel prescribes building a **domain-intelligent annotation UI**:

- Full context on one screen.
- One-click labels.
- Keyboard navigation.
- Filtering and per-category views.

Built in hours with AI-assisted development. Cited result: **~10x faster iteration** than off-the-shelf eval platforms. *(Practitioner-consensus with cited qualitative data from Hamel's consulting sample.)*

## What error analysis *isn't*

- Not an LLM-as-judge pipeline. Judges come after error analysis — you need 100+ labeled examples first. See [[llm-as-judge]].
- Not a generic metric suite (helpfulness, coherence, BERTScore). Generic metrics create false confidence. See [[failure-modes#evaluation-traps]].
- Not outsourced. External annotators miss tacit domain knowledge. Exception: mechanical tasks (phone numbers, email addresses) or hired subject-matter experts embedded in the problem.

## Signal the error analysis is working

- Your previously-hypothesized failures account for the *minority* of what you actually see in traces.
- Your eval pass rate drops to ~70% on hard slices. If it's above 90%, you're not stress-testing. *(Hamel/Shreya, practitioner-consensus.)*
- Domain experts (non-engineers) can meaningfully participate — Hamel builds dedicated annotation UIs precisely to unlock this.

## Source

- `raw/research/effective-agentic-patterns/05-hamel-llm-evals-faq.md` — "LLM Evals: Everything You Need to Know" (Hamel Husain and Shreya Shankar, 2026-01-15).
- `raw/research/effective-agentic-patterns/04-hamel-field-guide.md` — "A Field Guide to Rapidly Improving AI Products" (Hamel Husain, 2026). Cites Shankar et al. "Who Validates the Validators?" arXiv.

## Related

- [[llm-as-judge]]
- [[failure-modes]]
- [[measurement-vs-architecture]]
- [[benchmarks]] — why public benchmarks are not a substitute
