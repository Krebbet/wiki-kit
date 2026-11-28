# Weight-Space Programming of In-Context Learning (Skianis & Likas)

Frontier-LLM agents editing a small model's weights from 16 examples, without gradients, mostly write the ICL task vector into the weights, often as a few format-gated MLP key-value units. Finished runs are statistically indistinguishable from few-shot fine-tuning; the parity weakens or reverses under strict-data, unfinished-run and unseen-wording accounting. arXiv:2611.26841.

Note: written from the structured summary; references and most of Appendix A were skipped.

## Construction

Let $v$ = few-shot minus zero-shot residual at the final token. Take a near-silent MLP unit $j$; set $W_{gate}[j]=W_{up}[j]=\alpha k$ ($k$ = probe for the format's final token) and $W_{down}[:,j]=v/(\alpha\,\mathrm{silu}(\alpha))$. The unit adds $v$ when $k\cdot x\approx1$ and about nothing otherwise. A median of four such units in runs using this construction.

## Results (Qwen2.5-0.5B, six word-mapping tasks, mean %)

| Method (16 examples) | Accuracy |
|---|---|
| Unedited zero-shot | 0–3 |
| 16-shot ICL | 89.3 |
| Editors, finished runs only | 88.5–93.0 |
| Adam / context distillation / LoRA / rank-1 | 86.5 / 88.0 / 87.9 / 88.2 |
| Scripted gated task vector (1 unit) | 59.2 |

## Qualifiers on "matches fine-tuning"

- Means exclude unfinished runs (counting them, Opus falls to 80.5). Non-significance over 3 splits is not equivalence.
- Editors add outside knowledge (34/69 audited runs typed their own pairs). Strict 16-pair runs: Gemini 0.7–2.5 below fine-tuning, Astra 5.5–7.2 below.
- Unseen Q/A wording: editors ~13–31, gradient baselines ~48–62, ICL 89.
- Keys detect the **format**, not the task: summed single-task edits mostly break each other.
- Baseline grids are small; main study kernel was unsandboxed (authors' audit found no test-set access). Larger-model results are single-seed on different tasks.
- Sparse edits under 100K parameters showed no >5% perplexity rise (0/44); larger ones sometimes did.

## Bearing on the thesis

A gradient-free, few-example imprinting reference point for [[../synthesis/proposed-method]] *(synthesis)*: a "concept" written as a gated task vector transfers across held-out items when a rule exists (arithmetic), stores lookups otherwise, and fails to generalise across wording. Wording invariance is a cheap test any candidate method should pass. The paper's weak "implicit rank-1" baseline is a simplified construction and does not refute the equivalence on [[icl-implicit-weight-update]].

## Source

- raw/research/weekly-2026-11-27/05-icl-task-vector-editing.md (arXiv:2611.26841)

## Related

- [[_overview]]
- [[icl-implicit-weight-update]]
- [[../selective-finetuning/ff-kv-memories]]
- [[../selective-finetuning/rome]]
- [[../selective-finetuning/memit]]
- [[../decoding-time-steering/actadd]]
- [[../moe-adapters/moram]]
- [[../synthesis/proposed-method]]
- [[../../weekly-briefs/2026-11-27]] — brought in by the 2026-11-27 weekly sweep
