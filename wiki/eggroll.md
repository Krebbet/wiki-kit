# EGGROLL — Evolution Strategies at the Hyperscale

Low-rank Evolution Strategies that scales black-box / zeroth-order optimisation to billion-parameter nets, claiming ~100× throughput over naive ES, matching or beating GRPO on LLM reasoning fine-tuning, and enabling stable pretraining of pure-int8 RNN language models. Sarkar et al., Oxford FLAIR/WhiRL + MILA + NVIDIA, arXiv:2511.16652.

## Method

Standard Gaussian ES samples a full-rank perturbation `E ∈ R^{m×n}` per population member; arithmetic intensity is capped at 1 (GPU-throttled). EGGROLL samples two thin matrices `A ∈ R^{m×r}`, `B ∈ R^{n×r}` (r as low as 1) and forms `E = (1/√r) ABᵀ` — LoRA-shaped perturbations for ES rather than gradient-based fine-tuning.

Key tricks:
- Counter-based deterministic RNG (Salmon et al. 2011) reconstructs `A`, `B` on demand from a seed; perturbations need not be stored.
- The forward pass is rewritten `u(M + σE)ᵀ = uMᵀ + (σ/√r)(uB)Aᵀ`, sharing the base matmul `uMᵀ` across the population — the same kernel batched-LoRA inference servers (vLLM-style) use. High arithmetic intensity.
- Update aggregation `Σ E_i f_i` computed as `(diag(f)A)ᵀ B` at r=1, never materialising individual `E_i`.
- Gaussian approximate score function `Ŝ(E) = -E` is used despite the true rank-r score being intractable; CLT + the linearisation analysis below justify it.
- Per-perturbation rank is r, but the *aggregated* update has rank `min(Nr, m, n)` — full-rank in all reported experiments.

Theory: high-dimensional analysis of Gaussian ES with three regimes governed by perturbation scale `σ_d` vs dimension `d`.
- Regime I (Linearisation, `σ_d = o(d^{-1/2})`): ES gradient converges to true gradient `∇f(µ)` at rate `(σ_d √d)^α` (Theorem 1) — NTK-style result for ES on broad (possibly discontinuous) objectives.
- Regime II (Critical, `σ_d ≍ d^{-1/2}`): retains odd higher-order derivatives.
- Regime III (Divergence, `d^{-1/2} = o(σ_d)`): provably diverges on smooth cubic objectives (Theorem 2).
- Theorem 4: EGGROLL's low-rank update converges to true Gaussian ES update at `O(r^{-1})` (not `O(r^{-1/2})` — symmetry zeros odd cumulants, leaving the 4th-order Edgeworth term).

Builds on: Salimans et al. 2017 OpenES, LoRA (Hu 2022), counter-based PRNG (Salmon 2011). Concurrent: Qiu et al. 2025 (ES at scale), Korotyshova et al. 2025 (ESSA / CMA-ES on LoRA SVD bases).

## Results

- **Throughput (Fig. 2a):** up to 91% of pure batch-inference throughput on billion-parameter models at large population sizes — ~100× over naive ES.
- **Pure int8 RNN pretraining (Fig. 2b, EGG model, 6L-256D RNN, char-level minipile):** With population `2^20 = 1,048,576`, data batch 16, EGG hits **3.40 bits/byte** test cross-entropy vs **3.58** for an fp32 6L-256D Transformer with backprop SGD. ~180× backprop's GPU-hours. Population is 3 orders of magnitude beyond Salimans 2017's max (1440), on a single GPU.
- **Tabula-rasa RL** (16 envs across Navix, Craftax, Brax, Kinetix, Jumanji; 3-layer 256-unit MLP policy, 10 seeds, normalised by PPO): EGGROLL competitive on 7/16, underperforms 2/16, outperforms 7/16 vs OpenES with substantial wall-clock wins.
- **LLM reasoning fine-tuning vs GRPO:**
  - Countdown on RWKV-7 1.5B, single GPU (Fig. 4b): **EGGROLL 35% vs GRPO 23%** validation accuracy at equal wall-clock. 1024 parallel generations/GPU (618 updates) vs GRPO's 64 (915 updates).
  - GSM8K on RWKV-7 7B, 8 GPUs (Fig. 5a): EGGROLL beats GRPO; 8192 parallel generations vs GRPO's 256.
  - 14B RWKV-7 on DeepScaleR, 32 GPUs × 12 h: AIME24 13% → 30%, AIME25 7% → 33%, HMMT25 11% → 13%. **GRPO infeasible at this scale due to Adam optimiser memory.**
  - Matches GRPO on Qwen Transformer fine-tuning; can directly optimise pass@k (a known GRPO limitation per Yue et al. 2025).
- **int8 distillation (Fig. 6):** Per-channel int8 RWKV-7 7B distilled from fp model on GSM8K via KL fitness, recovers nontrivial accuracy from a 0%-baseline.

## Applicability

Best fit when:
- Gradients are unavailable, ill-defined, or expensive (low-precision/quantised models, neurosymbolic systems, outcome-only RL rewards).
- Base model has a small inference-time state — RWKV/SSM/RNNs are ideal because constant state size lets enormous inference batches share compute. Transformers benefit less; KV cache eats the population budget (paper notes this explicitly).
- Training is GPU-bound and parallelisable across many cheap perturbations rather than memory-bound on optimiser state — avoids Adam's 2× parameter memory. This made 14B RWKV-7 RL fine-tuning feasible where GRPO was not.
- Pass@k or other non-decomposable rewards are the real objective.

Prerequisites: a JAX-style codebase with deterministic counter-based PRNG and batched-LoRA-style kernels; enough parallel GPU compute for population sizes ~1k–~1M. For pretraining specifically, large population is necessary — population=2 underperforms badly, ruling out MeZO-style 2-point estimators.

## Reproducibility

Code at <https://eshyperscale.github.io/>. No third-party reproduction yet (arXiv Nov 2025). An "emergent log-linear scaling law for EGG loss vs int8 OPs" reported community-side by Andreas Kirsch (cited in acknowledgements).

## Adoption

Authored by an Oxford FLAIR/WhiRL + MILA + NVIDIA + NormaCore group (Foerster, Whiteson, Courville). Compute donated by Isambard-AI and JASMIN. Cites Qiu 2025 and Korotyshova 2025 as concurrent ES-for-LLMs work — an active "ES vs RLHF/GRPO for post-training" subfield is forming.

## Source

- `raw/research/radar-2026-04/01-eggroll.md` — EGGROLL paper PDF (arXiv:2511.16652). Captured 2026-04-22.

## Related

- [[test-time-training]] — sibling fast-weight / online-update line (different objective; same concern about pretrained LLM adaptation).
- [[conflicts/grpo-vs-evolution-strategies]] — EGGROLL's central positioning claim.
- [[watchlist]] — Salimans 2017 OpenES, MeZO, Qiu 2025, Korotyshova 2025 referenced but not captured.
