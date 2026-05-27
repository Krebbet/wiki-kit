# The Lottery Ticket Hypothesis for Pre-trained BERT Networks

Sparse *winning ticket* subnetworks exist within BERT at 40–90% sparsity that, when trained in isolation from the pre-trained initialization $\theta_0$, match or exceed full-model fine-tuning performance across GLUE and SQuAD. The pre-trained initialization itself serves as the rewinding point — no downstream warmup required, a meaningful departure from prior LTH work on large-scale networks. Subnetworks found via masked language modeling (MLM) are *universal* at 70% sparsity, transferring to all downstream tasks; task-specific subnetworks transfer only narrowly.

## Method core

**Iterative Magnitude Pruning (IMP)** with rewind to the pre-trained initialization $\theta_0$:

1. Fine-tune the full pre-trained network $f(x;\, \theta_0, \gamma_0)$ to convergence on task $\mathcal{T}$.
2. Prune the 10% of lowest-magnitude weights globally; rewind remaining weights to $\theta_0$.
3. Repeat until target sparsity $s$.
4. Return the sparse subnetwork $f(x;\, m \odot \theta_0)$ defined by mask $m$.

A **winning ticket** is a subnetwork $f(x;\, m \odot \theta_0)$ that, when trained from $\theta_0$, achieves performance within one standard deviation of the dense baseline. A **universal subnetwork** is a winning ticket for multiple tasks simultaneously (with task-specific heads $\gamma^{T_i}$). The universality claim holds at 70% sparsity via MLM-derived masks; at task-optimal sparsities the MLM ticket stays within 0.5–2.6 pp of per-task performance.

The key departure from prior LTH work (LSTMs, Transformers, ResNets at scale): those required rewinding to an early training checkpoint $\theta_i$ rather than to the original init. Pre-trained BERT weights are already a sufficient rewinding point — rewinding to $\theta_i$ does not improve, and sometimes hurts (STS-B, RTE).

## Goal relevance

**G1 (isolated block training) — directly relevant.** IMP identifies a sparsity-mask-defined subnet that trains in isolation — without the rest of the full network active — and matches dense performance. The isolation primitive is a weight mask rather than a block boundary, but the core question — *can a smaller subnet train to full accuracy when trained alone?* — is answered affirmatively. This is a direct prior-art datapoint for whether [[block-isolation-training]] can work without global gradient flow.

**G2 (per-block parameter allocation) — indirectly relevant.** IMP implicitly learns a layer-wise parameter budget: some layers end up denser than others. The paper does not analyze per-layer sparsity patterns in detail, but the resulting allocation is a form of learned block-level budget.

**G3 (token-conditional routing) — not relevant.**

## Credibility

Published at EMNLP 2020 (Chen et al.). Experiments cover all 11 GLUE tasks plus SQuAD v1.1 using BERT-BASE. Controls are tight: random pruning and random reinitialization both degrade substantially (e.g., −15 pp on MNLI at 70% sparsity), confirming that both the mask structure and the pre-trained init are load-bearing. No conflicts with other wiki sources identified.

## Empirical claims

| Claim | Finding |
|---|---|
| Winning tickets exist at $\theta_0$ | Yes — 40–90% sparsity across all 11 GLUE tasks |
| IMP mask is necessary | Yes — random pruning degrades substantially (e.g., −15 pp on MNLI at 70%) |
| Random reinitialization degrades | Yes — same magnitude as random pruning |
| Rewinding to $\theta_i$ improves over $\theta_0$ | No — sometimes hurts (STS-B, RTE) |
| Downstream tickets transfer broadly | Rarely — only 3 source tasks transfer to >2 other tasks at 70% sparsity |
| MLM ticket is universal at 70% | Yes — matches same-task performance on all 10 downstream tasks |
| Transferability correlates with training-set size | Yes — WNLI/MRPC (smallest) transfer to 0–1 tasks; MNLI/SQuAD/MLM (largest) transfer to 3–10 |
| One-shot magnitude pruning of $\theta_0$ | Produces transfer close to SQuAD IMP but worse than MLM IMP |

## Open questions / failure modes

- **Unstructured sparsity only.** Results do not translate to wall-clock speedups without sparse kernel support; structured pruning (heads, layers) is explicitly left to concurrent work (Prasanna et al. 2020).
- **BERT-BASE encoder only.** No decoder, no causal LM, no evidence the hypothesis extends to autoregressive generation at scale.
- **Small-dataset instability.** STS-B, WNLI, RTE (≤5760 training examples) show high variance; rewinding occasionally breaks these tasks.
- **IMP is computationally expensive.** Requires multiple full fine-tuning passes per sparsity level; framed explicitly as a scientific study, not a practical compression pipeline.
- **Universality is sparsity-specific.** The universal-ticket claim is strongest at 70%; at task-optimal sparsities (which differ per task) the MLM ticket stays within 0.5–2.6 pp but the strict universality framing weakens.
- **2020 vintage.** Predates scaling to GPT-2/GPT-3; no evidence LTH holds at billion-parameter causal-LM scale.

## Source

- `raw/research/selective-replacement-and-training/22-lottery-ticket-bert.md` (PDF capture)
- `raw/research/selective-replacement-and-training/11-lottery-ticket-bert-abs.md` (arXiv abstract)

## Related

- [[sheared-llama]] — LLM-scale structured-pruning successor; sparse-subnet → structured-prune evolution
- [[brecq]] — different isolation primitive: block reconstruction vs sparsity mask
- [[shortgpt]] — block-pruning sibling
- [[sleb]] — training-free pruning sibling; contrasts with IMP's find-and-retrain loop
- [[block-isolation-training]] — concept anchor; sparsity-mask isolation is a flavour of isolated training
- [[modular-deep-learning]] — survey context
