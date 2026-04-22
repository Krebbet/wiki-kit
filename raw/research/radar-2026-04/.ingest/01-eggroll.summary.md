---
source: "raw/research/radar-2026-04/01-eggroll.md"
slug: "01-eggroll"
summarized_on: "2026-04-22"
schema_version: 1
---

# Evolution Strategies at the Hyperscale (EGGROLL)

## One-line
EGGROLL (Sarkar et al., Oxford FLAIR/WhiRL + MILA + NVIDIA, arXiv 2511.16652) is a low-rank Evolution Strategies algorithm that scales black-box / zeroth-order optimisation to billion-parameter neural nets, claiming ~100x throughput over naive ES while matching or beating GRPO on LLM reasoning fine-tuning and enabling stable pretraining of pure-int8 RNN language models.

<!-- DOMAIN-SLOT: takeaway-prompts -->
## Method
Standard Gaussian ES samples a full-rank perturbation matrix `E ∈ R^{m×n}` per population member, requiring a separate batched matmul per worker (arithmetic intensity capped at 1, GPU-throttled). EGGROLL instead samples two thin matrices `A ∈ R^{m×r}`, `B ∈ R^{n×r}` per worker (with r as low as 1) and forms the rank-r perturbation `E = (1/√r) A Bᵀ`, analogous to LoRA but for ES rather than gradient-based fine-tuning. Key tricks:
- A counter-based deterministic RNG (Salmon et al. 2011 / JAX) reconstructs `A`, `B` on demand from a seed `ς`, so perturbations need not be stored.
- The forward pass is rewritten as `u(M + σE)ᵀ = uMᵀ + (σ/√r)(uB)Aᵀ`, sharing the base matmul `uMᵀ` across the whole population and turning per-worker perturbation work into the same kernel batched-LoRA inference servers like vLLM use — high arithmetic intensity.
- Update aggregation `Σ E_i f_i` is computed as `(diag(f)A)ᵀ B` at r=1, never materialising individual `E_i`.
- A Gaussian approximate score function `Ŝ(E) = -E` is used despite the true score of the rank-r distribution being intractable; central limit theorem + the linearisation analysis below justify it.
- Although each perturbation is rank-r, the aggregated update has rank `min(Nr, m, n)` — full-rank in all reported experiments.
Builds directly on Salimans et al. 2017 OpenES, LoRA (Hu et al. 2022), counter-based PRNG (Salmon et al. 2011), and is contemporary with Qiu et al. 2025 ("ES at scale: LLM fine-tuning beyond RL") and Korotyshova et al. 2025 (ESSA / CMA-ES on LoRA SVD bases).

Theory contribution: a high-dimensional analysis of Gaussian ES showing three regimes governed by perturbation scale `σ_d` vs dimension `d`:
- Regime I (Linearisation, `σ_d = o(d^{-1/2})`): ES gradient converges to true gradient `∇f(µ)` at rate `(σ_d √d)^α` (Theorem 1). This is an NTK-style result for ES on broad (possibly discontinuous) objectives.
- Regime II (Critical, `σ_d ≍ d^{-1/2}`): retains odd higher-order derivatives.
- Regime III (Divergence, `d^{-1/2} = o(σ_d)`): provably diverges on smooth cubic objectives (Theorem 2).
Plus Theorem 4: EGGROLL's low-rank update converges to true Gaussian ES update at `O(r^{-1})` (faster than the central limit `O(r^{-1/2})` because symmetry zeros odd cumulants, leaving the 4th-order Edgeworth term to dominate).

## Results
- **Throughput (Fig. 2a):** EGGROLL reaches up to 91% of pure batch-inference throughput on billion-parameter models at large population sizes, ~100x over naive ES.
- **Pure int8 RNN pretraining (Fig. 2b, EGG model, 6L-256D):** Trained on minipile, character-level. With population size up to `2^20 = 1,048,576` and data batch 16, EGG hits 3.40 bits/byte test cross-entropy vs. 3.58 for an fp32 6L-256D Transformer with backprop SGD on the same data batch. Largest pop run uses ~180x backprop's GPU-hours, demonstrating compute-only scaling in data-limited regimes. Population is 3 orders of magnitude larger than Salimans et al. 2017's max of 1440, on a single GPU.
- **Tabula-rasa RL (16 envs across Navix, Craftax, Brax, Kinetix, Jumanji; 3-layer 256-unit MLP policy, 10 seeds, normalised by PPO):** EGGROLL competitive on 7/16, underperforms 2/16, outperforms 7/16 vs OpenES, with substantial wall-clock wins (Fig. 4a).
- **LLM reasoning fine-tuning vs GRPO:**
  - Countdown task on RWKV-7 1.5B, single GPU (Fig. 4b): EGGROLL 35% vs GRPO 23% validation accuracy at equal wall-clock. EGGROLL runs 1024 parallel generations/GPU (618 updates) vs GRPO's 64 (915 updates).
  - GSM8K on RWKV-7 7B, 8 GPUs (Fig. 5a): EGGROLL beats GRPO; 8192 parallel generations (1024/GPU, 260 updates) vs GRPO's 256 (32/GPU, 340 updates).
  - 14B RWKV-7 on DeepScaleR, 32 GPUs × 12h, 5000-token thinking budget: AIME24 13% → 30%, AIME25 7% → 33%, HMMT25 11% → 13%. GRPO infeasible at this scale due to Adam optimiser memory. On 7B with 128 GPUs × 24h, beats GRPO.
  - Also matches GRPO on Qwen Transformer fine-tuning (Section L) and can directly optimise pass@k (a known GRPO limitation citing Yue et al. 2025).
- **int8 distillation (Fig. 6):** Per-channel int8 quantised RWKV-7 7B distilled from fp model on GSM8K via KL fitness, recovers nontrivial GSM8K validation accuracy from a 0%-baseline starting point.
- **Other applications:** Finance world-model fine-tuned to high-frequency trading agent optimising PnL directly (Section M); MARL results (Section N.1).

## Applicability
Best fit for projects where:
- Gradients are unavailable, ill-defined, or expensive (low-precision/quantised models, neurosymbolic systems with non-differentiable modules, outcome-only RL rewards).
- The base model has a small inference-time state (RWKV / SSM / RNNs are ideal because the constant state size lets enormous inference batches share compute; transformers benefit less because KV cache eats the population budget — paper explicitly notes this).
- Training compute is GPU-bound and parallelisable across many cheap perturbations rather than memory-bound on optimiser state (avoids Adam's 2x parameter memory; this is what made 14B RWKV-7 RL fine-tuning feasible where GRPO was not).
- Pass@k or other non-decomposable rewards are the real objective.
Prerequisites: a JAX-style codebase comfortable with deterministic counter-based PRNG and batched-LoRA-style kernels; access to enough parallel GPU compute to run population sizes from ~1k to ~1M; for pretraining specifically, large population size is necessary (population=2 underperforms badly, ruling out MeZO-style 2-point estimators).

## Novelty
Genuinely new at the systems/algorithms intersection rather than a pure theoretical step. The low-rank-perturbation idea has prior art:
- Garbus & Pollack (GECCO 2025) optimise a low-rank factorisation directly with neuroevolution — but their parameter update is restricted to low rank regardless of population. EGGROLL keeps perturbations low-rank but the *aggregated update* is full-rank `min(Nr, m, n)`.
- Choromanski et al. 2019 use a low-rank PCA-found search space — small populations, different goal.
- Jin et al. 2024 do ES over LoRA matrices; Yu et al. 2025 project perturbations to low-rank subspace — but these target SFT memory savings, not throughput, and report fine-tuning-only results.
- Qiu et al. 2025 (ES at scale) and Korotyshova et al. 2025 (ESSA / CMA-ES on SVD bases) reach LLM fine-tuning territory but use small population (~hundreds of unique perturbations) and many rollouts per perturbation; EGGROLL's contribution is making *per-generation perturbation* affordable so population = inference batch size.
The high-dimensional ES linearisation theorems (three regimes, NTK-style result for discontinuous objectives, `O(r^{-1})` rank-convergence rate via Edgeworth expansion) appear to be the first such characterisation for ES at LLM scale.

## Reproducibility
- Code: <https://eshyperscale.github.io/> (linked in abstract). Not yet checked for license/quality.
- Weights: not stated in main text; AIME-trained 14B RWKV-7 plausibly released given the project page exists, but unverified here.
- Independent reproduction: too new (arXiv Nov 2025) for a third-party reproduction. An "emergent log-linear scaling law for EGG loss vs int8 OPs" was reported community-side by Andreas Kirsch (cited tweet in acknowledgements), suggesting at least one external eyeball.

## Adoption
Authors are an Oxford FLAIR/WhiRL + MILA + NVIDIA + NormaCore group around Foerster, Whiteson, Courville — high-visibility lab cluster. Compute donated by Isambard-AI and JASMIN. Cites Qiu et al. 2025 and Korotyshova et al. 2025 as concurrent ES-for-LLMs work, indicating an actively-forming subfield ("ES vs RLHF/GRPO for post-training") rather than an isolated paper. Acknowledgements cite community engagement around the first arXiv release. Too early for paperswithcode leaderboard data.

## Conflicts
None against this wiki — wiki currently has no pages on RL post-training, ES, GRPO, or recurrent LLMs to contradict. The paper itself takes a contested stance worth tracking: it positions ES as a viable alternative to GRPO/RLHF for LLM reasoning (potential future conflict if/when wiki captures the GRPO orthodoxy from DeepSeek/Shao et al. 2024). Also weakly contests the "transformers are the right substrate for RL post-training" assumption by leaning hard on RWKV's constant-state inference batching.
<!-- /DOMAIN-SLOT -->

## Cross-ref candidates
- [[evolution-strategies]] — would be the natural anchor page; doesn't yet exist. EGGROLL extends the Salimans et al. 2017 OpenES line.
- [[lora]] / [[low-rank-adaptation]] — direct structural analogy; EGGROLL is "LoRA-shaped perturbations for ES".
- [[grpo]] / [[rl-post-training]] — primary baseline beaten on countdown, GSM8K, AIME; key positioning claim.
- [[rwkv]] / [[recurrent-llms]] / [[state-space-models]] — RWKV-7 is the workhorse model; the paper's compute argument hinges on small recurrent state.
- [[ntk]] / [[neural-tangent-kernel]] — Theorem 1 is explicitly framed as an NTK-style linearisation result for ES.
- [[zeroth-order-optimisation]] / [[mezo]] — MeZO (Malladi et al. 2023) is the closest 2-point ES baseline; paper argues 2-point methods can't pretrain.
- [[quantised-training]] / [[int8-training]] — EGG demonstrates pretraining with no fp anywhere; relevant to any future page on low-precision training.
- [[pass-at-k]] — paper claims direct optimisation of pass@k, contra a documented GRPO limitation (Yue et al. 2025).
- [[neuroevolution]] — broader umbrella; cites Such et al. 2018 and Garbus & Pollack 2025 as nearest neighbours.

## Conflict flags
(none) — wiki has no pages other than `[[reference-sources]]` so nothing to contradict yet. Flag for future: EGGROLL claims ES can match or beat GRPO on LLM reasoning at scale, which will conflict with any future page that treats GRPO/RLHF as the default post-training method.

## Proposed page shape
- New page: `evolution-strategies-at-scale` — covers EGGROLL specifically: low-rank perturbation trick, the three-regime convergence analysis, the empirical results vs GRPO. This is the headline content.
- New page: `evolution-strategies` — short anchor/overview page on classical ES (Rechenberg, Salimans et al. 2017, CMA-ES) so EGGROLL has somewhere to link "back" to. Stub-sized initially.
- Extend (when those pages exist) [[grpo]] with a section "Contested by ES-based post-training" pointing to EGGROLL, Qiu et al. 2025, Korotyshova et al. 2025.
- Extend (when it exists) [[rwkv]] / [[recurrent-llms]] with a note on why constant-state recurrent models are the natural substrate for population-based fine-tuning.
- Optional: a `quantised-training` page seeded by the int8 EGG result if/when more int-only pretraining work shows up — single source is too thin alone.
