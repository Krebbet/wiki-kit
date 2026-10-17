# LoGRA: Low-Rank Gradient Sketches for LLM RL

LoGRA (arXiv:2610.06647, NVIDIA) is an RL post-training method that accumulates random-projection low-rank gradient sketches directly during backprop (never materializing the full d x k gradient) and controls step size with a predicted-KL budget. Reported: average training memory -21.8% (1.5B) and -45.7% (7B) at accuracy parity with dense Adam, and 27B RL on one 8xH100 node where dense Adam OOMs. Three seeds on the main table, one on the 27B run; no independent reproduction.

## Method

- Per selected weight matrix W (d x k; attention + MLP projections only, 196 matrices in a 28-layer 1.5B model), sample a random projection A (r x k, Rademacher +-1/sqrt(r), not learned). Sketch S = G A^T (d x r) is accumulated in fp32 by projecting layer inputs before multiplying by backward derivatives.
- Update W <- W - alpha*eta*U*A, merged into weights (no persistent adapter). A is refreshed each update with a fresh seed, so the cumulative update is not rank-limited.
- Policy sync: trainer sends alpha*eta*U plus the seed; the rollout engine regenerates A and applies the same update. Payload d*r instead of d*k (cf. weight-sync cost in [[llamarl]]).
- RowAdam: per-row second moment only (beta2=0.95), no first moment, renormalized to the sketch Frobenius norm. Main runs use rank-256 RowAdam; the 27B long run uses SGD sketch updates.
- Predicted-KL step control (TRPO-motivated): alpha = min(alpha_max, sqrt(delta/q(D))), q(D) from the variance of the logit rate of change along the proposed update (JVP; finite-difference probe at 27B). Budget delta cosine-annealed 2e-4 to 2e-5. "Mismatch subtraction" of the rollout-vs-trainer logprob gap is a heuristic.
- Setup: PPO with verifiable rewards, 1 response/prompt, global running reward baseline, NVIDIA Molt library, FSDP on 4 GPUs + 4 generation engines. Lineage: GaLore/GaLore2, Flora, LoRA, motivated by "LoRA Without Regret" (RL needs little information per sample).

## Results

- DAPO-Math-7.5K train, MATH-500 eval, 3 seeds. 1.5B: avg mem 9.18 to 7.18 GiB, Pass@1 peak 63.77 (dense) to 67.87, updates/h 54.28 vs 55.44. 7B: avg mem 31.82 to 17.29 GiB (peak 31.85 to 22.26), Pass@1 72.48 vs 72.33 (parity).
- 27B ("Qwen3.8-27B" as named in the source; model name unverified): dense OOMs at the first Adam state allocation; LoGRA 51.54 GiB avg / 53.88 peak, Pass@1 71.52, 6.99 updates/h over 200 updates. Reasoning-Gym Hard (single seed, >1,100 steps): held-out macro 39.69% to 62.94% (peak 65.52%), response length 8,312 to 4,705 tokens, truncation 34.72% to 12.95%.
- Ablations (Qwen2.5-Math-1.5B): rank dominates (rank 4 to 256 = +3.0-3.95 pp). At r=256 fixed Rademacher 68.50 / refreshed 68.31 / refreshed Gaussian 67.42, so projection refresh and distribution give no consistent benefit, undercutting Flora's motivation here. Gradient reconstruction cosine is only 0.046 (r=4) to 0.348 (r=256).
- vs LoRA (rank 256, 1.5B, 300 steps): memory 7.18 vs 13.21 GiB, but LoRA is more accurate (Pass@1 70.45 vs 68.47) and slightly faster; the authors concede no accuracy or speed advantage, with confounded optimizers/schedules.
- KL control (2 seeds, 800 steps, SGD): large constant budget degrades (63.43), small constant 71.03, annealed 71.47, no control 70.30. The no-control baseline is stable; the authors say this does not show KL control is necessary.

## Caveats

- Short horizon (accuracy peaks in the first 200 updates); the 27B comparison has no dense accuracy baseline by construction; 27B long run is one trajectory.
- Memory win is vs full-weight dense Adam, not vs LoRA-style RL, where LoRA is competitive on accuracy.
- Needs a custom backward hook (Molt); attention/MLP matmuls only, embeddings and norms frozen.

## Applicability

Memory-constrained RLVR on single-node hardware where full-weight training is wanted but Adam state does not fit. Predicted-KL control is separable and could be attached to other optimizers. Low-information-per-sample motivation is consistent with [[reasonmaxxer]] (RL change fits sparse/low-rank) and Position A of [[conflicts/sparse-policy-selection-vs-gradient-cancellation]]. Alternative memory-light routes to full-model RL: [[eggroll]], [[es-solution-coverage]]. Contrast: [[magistral]] runs no-KL GRPO, LoGRA an explicit KL budget. Code: github.com/skzhang1/labs-molt (logra branch); same NVIDIA group as [[polar-rl-harness]].

## Source

- raw/research/weekly-2026-10-17/03-logra.md
- https://arxiv.org/pdf/2610.06647

## Related

[[eggroll]], [[es-solution-coverage]], [[polar-rl-harness]], [[llamarl]], [[reasonmaxxer]], [[rlvr-incentivizes-reasoning]], [[magistral]], [[delta-token-credit]], [[program-as-weights]], [[conflicts/sparse-policy-selection-vs-gradient-cancellation]]
