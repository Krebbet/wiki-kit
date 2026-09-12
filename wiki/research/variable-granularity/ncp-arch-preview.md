# NCP-ArchPreview: Next-Concept Prediction at Frontier Scale

NCP-ArchPreview (arXiv:2609.10715, Shanghai AI Lab / SJTU LUMIA Lab) is an 8.9B-parameter latent-space LM built on OLMo-3-7B that adds a joint **Next-Concept-Prediction (NCP)** objective — predicting a compressed, product-quantized "concept" vector alongside standard next-token prediction — scaled to 5.73T pretraining tokens. It matches OLMo-3-7B's final pretraining loss at only **51.3% of its training tokens** and beats it by **+2.45 points** downstream macro-average (+5.99 GSM8K).

## Method

Three-module backbone: 16-layer Token Encoder → 8-layer Concept Module → 16-layer Token Decoder (32 total token-level layers, matching OLMo-3-7B's 32; the Concept Module runs on the compressed sequence at <1/4 the FLOPs of an equivalent token-level stack).

**Concept formation:** mean-pool every **$k=4$** consecutive token hidden states into a continuous concept vector — a *fixed*, uniform compression factor, not input-adaptive. Concepts are vector-quantized via **product quantization**: each vector split into 32 segments, each independently assigned to its nearest of 128 codewords, giving combinatorial capacity from small per-segment codebooks.

**Prediction:** the Concept Module autoregressively predicts the *next* concept from concept history, producing a softmax distribution per PQ segment and taking the **expectation over codebook entries** (not argmax/hard sample) as a differentiable soft prediction. Predicted concepts are repeated $k$ times, causally shifted, and injected into the Token Decoder via elementwise residual addition. A hierarchical residual mechanism (intra- and cross-module dense connections, MUDDFormer-style) supplements this.

Joint loss: $L_{total} = L_{NTP} + \alpha L_{NCP} + \beta L_{VQ}$ — standard causal-LM cross-entropy, MSE between soft-predicted and stop-gradiented true concept, and a VQ codebook-fitting loss.

## Results

Pretraining efficiency, matched against OLMo-3-7B on identical data:

| Stage | Tokens to match loss | Downstream Δ |
|---|---|---|
| Stage-1 (5.73T tokens) | 51.3% (1.95× speedup) | +2.45pt macro-avg (GSM8K +5.99, MATH-avg +3.75, PiQA +8.60) |
| Stage-2 (100B mid-training) | 66.2% (1.51× speedup) | +0.59pt (code regresses −0.65, attributed to mid-training mix skew) |

Parameter/compute-aligned ablations and progressive component ablation (Vanilla → +Concept Module → +Residual → +NCP) show monotonic loss improvement, isolating gains to the architecture+objective rather than raw capacity. A scaling-law study (varying encoder/concept/decoder *depth*, not chunk size) reports a 1.74× Pareto compute-efficiency improvement.

**Lightweight domain adaptation.** Freezing the 8.9B backbone and updating only the **17M-parameter VQ codebooks + concept-prediction heads** (no added parameters, unlike LoRA) on domain-specific corpora improves target-domain metrics (code avg +2.65, math avg +4.27, TriviaQA EM +9.19) with **markedly less general-capability forgetting** than full fine-tuning or parameter-matched LoRA (general avg on math adaptation: VQ +0.39 vs. LoRA −0.42 vs. Full −0.97), at 1.5–2× higher training throughput. The gain is smaller on knowledge adaptation specifically because VQ leaves backbone FFN "key-value memory" parameters untouched and so cannot rewrite factual associations directly.

## What this is not

This is a trillion-token **pretraining-efficiency** result, not a single-sample or few-shot demonstration — orthogonal to the wiki's single-sample regime except via the VQ-adaptation angle above. No RL, reward signal, or on/off-policy content anywhere in the pipeline. No explicit interpretability/compositionality probing of the learned concepts — the "concept-level" claim is architectural/objective-based (an explicit multi-token-span prediction target), inferred from loss/benchmark deltas rather than concept-manipulation experiments.

## Relation to the concept-granularity architecture hypothesis

[[../synthesis/concept-granularity-architecture]] proposes that middle layers should operate on *variable-granularity* concept units, formed by a merge/split decision process over local information content. NCP-ArchPreview validates the weaker, general claim — an explicit concept-level prediction objective in a middle module improves training efficiency and downstream capability at frontier scale — but it does **not** implement the hypothesis's core mechanism: concept units are a fixed, uniform $k=4$-token grid produced by mean-pooling, with no boundary-decision loss and no "decision points vs. transport overhead" analysis. The paper's own Related Work section explicitly places BLT/H-Net/DLCM (not this paper) in the dynamic-chunking camp. This is a **scope-boundary marker, not a confirmation**: the variable-granularity mechanism specifically remains untested by any corpus source.

## Relation to other wiki entries

- [[../rl-optimizers/latent-grpo]] — methodological parallel, not RL-related: both solve "how to keep a discrete/quantized latent target differentiable," NCP-ArchPreview via per-segment softmax-weighted expectation over PQ codebook entries, Latent-GRPO via vocabulary-superposition/Gumbel-STE relaxation, applied in a pretraining MSE objective vs. an RL (GRPO) objective respectively.
- [[../selective-finetuning/_overview]] — the 17M-param VQ-only adaptation is a new data point in the "behaviour is isolable in a small parameter subset" cluster, complementary to the theme's knowledge-editing/skill-localization/PEFT entries.
- [[../catastrophic-forgetting/_overview]] — the VQ-adaptation general-average retention numbers are a clean forgetting-vs-plasticity data point for the theme's architectural-avoidance-of-interference thread, in the spirit of the moe-adapters theme's "avoid interference by construction" answer.

## Source

- arXiv: [2609.10715](https://arxiv.org/abs/2609.10715) — "NCP-ArchPreview Technical Report: Moving towards Latent Space Language Models through Next Concept Prediction"
- Direct scale-up of ConceptLM (Liu et al., 2026); closest continuous-space precedent is Meta's Large Concept Model (Barrault et al., 2024)
- Captured via 2026-09-11 weekly sweep: `raw/research/weekly-2026-09-11/02-ncp-arch-preview.md`

## Related

- [[hierarchical-reasoning-model]] — sibling variable-granularity entry (architectural inductive bias, different mechanism — recurrence vs. concept quantization)
- [[../synthesis/concept-granularity-architecture]] — motivating hypothesis; this paper is a scope-boundary marker, not a confirmation
- [[../rl-optimizers/latent-grpo]] — differentiable-discrete-latent methodological parallel
- [[../selective-finetuning/_overview]] — VQ-only adaptation as a new low-forgetting PEFT data point
- [[../catastrophic-forgetting/_overview]] — forgetting-vs-plasticity data point
- [[../../weekly-briefs/2026-09-11]] — brought in by the 2026-09-11 weekly sweep
