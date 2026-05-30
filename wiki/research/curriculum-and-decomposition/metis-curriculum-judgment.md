# METIS: Internalizing Curriculum Judgment for LLM Reinforcement Fine-Tuning

METIS (METacognitive Internalized Self-judgment) is a closed-loop curriculum framework for LLM reinforcement fine-tuning that eliminates external curriculum selectors by having the policy itself predict prompt informativeness via in-context learning, then reinforcing those predictions from realized rollout outcomes. The key proxy is within-prompt reward variance $v_\theta(x) := \text{Var}_{y \sim \pi_\theta(\cdot|x)}[r(x,y)]$, which generalizes pass-rate heuristics to both binary and continuous rewards and is maximized at intermediate difficulty ($p = 0.5$ in the binary case). Across math reasoning, code generation, and agentic function-calling benchmarks, METIS consistently matches or beats the best external-curriculum baseline (PCL) at only ~3.9% per-step overhead, delivering up to 67% wall-clock reduction.

## Method

**Informativeness signal.** In group-relative RFT (GRPO-style), the mean squared group-relative advantage on prompt $x$ equals the empirical reward variance $v(x) = \frac{1}{n}\sum_i(r_i - \bar{r}(x))^2$. This vanishes when all $n$ rollouts agree (either all succeed or all fail) and peaks when rollouts are maximally split. For binary rewards this recovers the $p(1-p)$ intermediate-difficulty heuristic; for continuous rewards ($r \in [0,1]$) it remains a valid dispersion measure with no regime-specific modification needed.

**Self-judgment via ICL.** At each iteration, the policy receives a calibration memory $M_t = \{(x_k, v(x_k))\}_{k=1}^K$ of the $K$ most recent prompt–variance pairs from training history, plus a candidate prompt. It emits a short chain-of-thought ending in a boxed numeric prediction $\hat{v}_\theta(x) \in [0, 0.25]$. The training batch is then $S_t = \text{Top-}B_{x \in C_t}\ \hat{v}_\theta(x)$ over a pool $C_t$ of size $mB$. Critically this is a *pre-rollout* forward judgment, replacing post-hoc variance filtering that requires $n$ full rollouts per candidate just to measure the filter.

**Judgment reward and joint optimization.** After rolling out the selected prompts and computing realized $v(x)$, METIS scores the pre-rollout prediction with a squared-error calibration reward:

$$R_\text{judge}(x) = 1 - \left(4(\hat{v}_\theta(x) - v(x))\right)^2$$

Judgment tokens are updated via REINFORCE with a moving-average baseline $b_t$:

$$\nabla_\theta J_\text{judge} = \frac{1}{|S_t|} \sum_{x \in S_t} (R_\text{judge}(x) - b_t)\, \nabla_\theta \log \pi_\theta(\hat{v}_\theta(x) \mid \text{ctxt}(x))$$

Total loss: $\mathcal{L}_\text{total} = \mathcal{L}_\text{policy} + \lambda\, \mathcal{L}_\text{judge}$. With $\lambda = 0.01$ (default), the judgment calibration improves throughout training without destabilizing the task loss; $\lambda = 1$ collapses predictions to the max-variance shortcut $\hat{v} = 0.25$.

**Calibration memory size.** $K = 3$ exemplars is the sweet spot: $K = 0$ causes 87.6% parse failures (the model attempts to solve the candidate prompt rather than predict its variance), while $K = 9$ adds marginal context noise without calibration gain.

## Key Results

All runs use GRPO on VERL + vLLM on 96× H200s; reported as best validation pass@1 reached within a wall-clock budget.

**Math reasoning (DAPO-17k → AIME24/25, MATH500, Minerva):**

| Model | Method | Avg ↑ | Time ↓ | ΔT% |
|---|---|---|---|---|
| Qwen3-8B-Base | No Curriculum | 34.9 | 32.6h | — |
| Qwen3-8B-Base | PCL (best baseline) | 35.4 | 17.3h | −46.9% |
| Qwen3-8B-Base | **METIS** | **35.7** | **15.7h** | **−51.8%** |
| Qwen3-4B-Base | No Curriculum | 26.4 | 13.5h | — |
| Qwen3-4B-Base | PCL | 26.8 | 11.8h | −12.6% |
| Qwen3-4B-Base | **METIS** | **27.9** | 8.4h | **−37.8%** |

**Code generation (CodeContests+ → LCBv6, HumanEval, MBPP, BCB):**

| Model | Method | Avg ↑ | Time ↓ | ΔT% |
|---|---|---|---|---|
| Llama-3.1-8B-Instruct | No Curriculum | 38.8 | 19.2h | — |
| Llama-3.1-8B-Instruct | PCL | 39.7 | **5.3h** | −68.5% |
| Llama-3.1-8B-Instruct | **METIS** | **40.4** | 5.4h | **−67.9%** |

**Agentic function-calling (BFCL v3, Qwen3-4B-Instruct):** METIS improves overall accuracy from 46.7 → 49.8, with gains across all 5 subsplits, at minimal added wall-clock cost.

**Per-step overhead:** METIS adds ~3.9% wall-clock overhead and ~5.1% throughput drop vs. No Curriculum; PCL drops throughput by ~58% (separate value model running alongside GRPO). ADCL inflates wall-clock by ~68% (extra re-estimation rollouts that never update the policy).

**Competence-frontier tracking:** On an easy pool (MATH), METIS re-anchors its selected batch mean reward near $p \approx 0.5$ even after the pool is largely mastered, where other methods drift toward $p \approx 1$. On a hard pool (DAPO-17k), it identifies the occasional solvable prompts faster. This bidirectional self-regulation — approaching from below or above — is the behavioral signature that the policy has internalized the informativeness criterion.

## Ablations

| Variant | Avg (Qwen3-4B+DAPO) | Fail. rate |
|---|---|---|
| No Curriculum | 26.4 | — |
| PCL | 26.8 | — |
| METIS w/o ICL ($K=0$) | 26.4 | 87.6% |
| METIS w/o $\mathcal{L}_\text{judge}$ ($\lambda=0$) | 27.2 | 2.2% |
| **METIS** ($K=3$, $\lambda=0.01$) | **27.9** | **0.3%** |
| METIS ($\lambda=1$) | 25.5 | 0.3% |

The two components are complementary: ICL is necessary for parseable predictions; $\mathcal{L}_\text{judge}$ is necessary for calibrated differentiation across the candidate pool.

## Relation to GRPO Difficulty Bias

METIS drops the per-prompt std-normalization from GRPO (following Liu et al. 2025 "Understanding R1-Zero-like training"), which has been shown to introduce a difficulty bias. The group-relative advantage with dropped std is exactly $v(x)$, the variance signal METIS exploits. This is consistent with [[../rl-optimizers/dr-grpo]] (std removal fixes normalization bias) but note that [[../rl-optimizers/mcpo]] argues the residual $p(1-p)$ weight persists even after std is removed — METIS explicitly uses the $p(1-p)$ signal as the *selection criterion* rather than trying to remove it, which is a different design choice.

## Limitations

- Relies on the policy's in-context learning capacity; weaker backbones (e.g. very small models) may fail to follow the variance-prediction format. The ablation shows this is a binary threshold — the model either engages with the meta-task or ignores it entirely.
- Single-seed results only (96 H200s × up to 40h per run; ~20K H200-GPU-hours total).
- Training stability gains are observed qualitatively but not formally quantified.

## Source

- arXiv: https://arxiv.org/abs/2605.11235
- Capture: `../../../raw/research/weekly-2026-05-30/03-metis-curriculum-judgment.md`
- Authors: Han Zheng, Yining Ma, Karthick Gunasekaran, Bharathan Balaji, Zheng Du, Shiv Vitaladevuni, Cathy Wu (MIT / Amazon AGI)

## Related

- [[_overview]] — curriculum-and-decomposition theme overview; METIS is the first LLM-RFT-era paper in this section
- [[bengio-curriculum]] — original continuation-method framing; METIS's variance-frontier tracking is the dynamic, closed-loop descendant
- [[acl-deep-rl-survey]] — ALP/LP signals in teacher-student bandits are the structural ancestor of within-prompt variance as a curriculum signal
- [[../synthesis/concept-curriculum-method]] — METIS's variance-based selection could replace or augment the step (c) schedule in the concept-curriculum method; the competence-frontier tracking is exactly what that method's per-concept training loop needs
- [[../rl-optimizers/dapo]] — METIS trains on DAPO-17k; DAPO's Dynamic Sampling (discard all-correct groups) is an inferior coarser version of METIS's variance-selection
- [[../rl-optimizers/dr-grpo]] — drops per-prompt std normalization; METIS adopts the same choice and repurposes the resulting raw variance as the selection signal
- [[../rl-optimizers/mcpo]] — MCPO argues $p(1-p)$ bias persists after std-removal; METIS treats that signal as a feature, not a bug
- [[../single-sample-rl-finetuning/data-efficiency-rft]] — data-side curriculum coverage; METIS adds the algorithmic closed-loop selection perspective
- [[../weekly-briefs/2026-05-30]] — brought in by the 2026-05-30 weekly sweep
