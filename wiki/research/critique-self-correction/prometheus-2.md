# Prometheus 2

Prometheus 2 is an open-source 7B/8x7B evaluator LM that mirrors human and GPT-4 judgments on both direct assessment and pairwise ranking, achieving Pearson r=0.685 on MT Bench and 85.5% agreement on HHH Alignment (Table 3–4, 2405.01535). Trained via weight merging of models fine-tuned separately on direct and pairwise formats, Prometheus 2 unifies two evaluation paradigms without performance degradation—a key gap vs prior evaluator LMs locked to single formats.

## Method

Direct assessment: Maps (instruction, response, reference, criteria) → (verbal feedback, 1-5 score). Pairwise ranking: Maps (instruction, response_m, response_n, criteria) → (comparative feedback, winner).

**Data**: The PREFERENCE COLLECTION (200K pairwise instances) augments the FEEDBACK COLLECTION (100K direct assessment) by pairing responses and generating contrastive verbal feedback via GPT-4. Both share 1K custom evaluation criteria, 20K instructions, 20K references.

**Training recipe**: Train two specialist evaluator LMs on separate formats (Mistral-7B or Mixtral-8x7B base), then merge via DARE-Linear merging (Eq. 3). Critically, merging outperforms joint training, revealing no negative task transfer when combining formats.

**Key finding**: Weight merging unifies formats while preserving individual performance; joint training on both formats simultaneously degrades both (Table 5–6). This suggests direct and pairwise evaluation are complementary tasks whose weights interfere during joint training but cooperate in weight space.

## Claims

**Direct assessment**: **Pearson r=0.685 (Mixtral-8x7B) vs GPT-4-1106 on MT Bench** (Table 3)—outperforms Prometheus-13B (0.404) and Auto-J (0.432) by >0.2 units.

**Pairwise ranking**: **85.5% agreement with humans on HHH Alignment** (Table 4)—Prometheus-2-8x7B matches PairRM on in-domain test, exceeds it on out-of-domain.

**Unified performance**: **Weight merging exceeds single-format training** (Table 5)—on Vicuna Bench, merging achieves 0.666 Pearson (Mistral-7B) vs 0.537 direct-only, 0.548 pairwise-only.

**Generalization**: **Halves the gap with proprietary LMs** on out-of-domain tests; on FLASK, Prometheus-2-8x7B reaches 0.626 Pearson vs Prometheus-1's 0.470 (human correlation 0.679).

**Custom criteria**: **1K instance-wise evaluation criteria** beyond helpfulness/harmlessness, enabling fine-grained, task-specific evaluation (first work on criteria-aware pairwise ranking).

**No ensembling effect**: Merging two models trained on different formats outperforms merging two trained on the same format (Table 6)—benefit is from format diversity, not model averaging.

## Relevance to the project

Prometheus 2 advances critique-based evaluation from simple scalar rewards toward richer, criteria-conditioned feedback. In single-sample, concept-based fine-tuning, this is critical: rather than a generic "good/bad" signal, Prometheus 2 enables concept-level critique (e.g., "correct factually, but explanation is opaque") at eval time, supporting refinement loops that target specific failure modes. The unified pairwise+direct pipeline also mirrors the dual-signal setup in RL (preference pairs + outcome labels).

However, Prometheus 2 is an **evaluator LM, not a critic-finetuned model**. It doesn't self-critique or refine; it judges others. For single-sample fine-tuning, this provides a plug-in reward/feedback signal but doesn't directly teach the model to critique itself (contrast: Critic-CoT, which trains critique capability).

## Source

- arXiv: 2405.01535
- Raw markdown: `../../../raw/research/adjacent-reward-signals/06-prometheus-2.md`
- Raw PDF: `../../../raw/research/adjacent-reward-signals/pdfs/prometheus-2.pdf`

## Related

- [[self-refine]] — Self-Refine uses LLM feedback to iteratively improve outputs; Prometheus 2 provides higher-fidelity feedback signal with custom criteria.
- [[reflexion]] — Reflexion requires environment rewards; Prometheus 2 offers an open, criteria-aware alternative for dense evaluation feedback.
- [[constitutional-ai]] — Constitutional AI uses rule-based critique; Prometheus 2 enables learned, flexible criteria-based evaluation.
- [[../process-reward-models/_overview]] — Prometheus 2 evaluates outcome-level quality with custom rubrics; process reward models target step-level supervision.
