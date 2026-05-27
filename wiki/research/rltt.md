# Rewarding Latent Thought Trajectories (RLTT)

RLTT (Williams & Tureci, Princeton preprint Feb 2026; arXiv:2602.10520) is a reinforcement learning framework for [[ouro]]-style Looped Language Models (LoopLMs) that distributes reward across the full latent reasoning trajectory rather than assigning credit only to the terminal loop. Applied to Ouro-2.6B-Thinking with T_max=4 fixed loops, RLTT yields +14.4% on MATH-500, +16.6% on AIME24, +10.0% on BeyondAIME, and +34.3% on GSM8K over a compute-matched GRPO baseline, while also transferring to non-math benchmarks (GPQA: +18.7%) without any non-math supervision.

## Core problem: credit-assignment mismatch

A LoopLM generates each token $y_j$ by running shared-weight transformer blocks for $T_{\max}$ iterations, producing a latent thought trajectory $h_j^{(1)} \to \cdots \to h_j^{(T_{\max})}$ and a corresponding sequence of per-loop next-token distributions:

$$P_\theta^{(t)}\!\bigl(y_j \mid x, y_{<j}\bigr) = \mathrm{Softmax}\!\bigl(g(h_j^{(t)})\bigr), \quad t = 1, \ldots, T_{\max}$$

Standard GRPO assigns reward only through $P_\theta^{(T_{\max})}$, the terminal distribution. Intermediate latent states $t < T_{\max}$ receive no direct gradient signal; the learning signal must back-propagate through all loop iterations from a single bottleneck. Ouro's own authors noted that RLVR post-training failed to produce significant gains under this formulation.

## RLTT objective

RLTT replaces the single log-probability in the REINFORCE-style gradient with a weighted sum over all loops:

$$\nabla_\theta J_{\mathrm{RLTT}} = \mathbb{E}\!\left[\frac{1}{g}\frac{1}{|y|} \sum_i \sum_j \sum_t \omega_t \cdot \nabla_\theta \log P_\theta^{(t)}\!\bigl(y_{i,j} \mid x, y_{i,<j}\bigr) \cdot \hat{A}_i\right]$$

where $\omega_t \geq 0$ are per-loop weights satisfying $\sum_{t=1}^{T_{\max}} \omega_t = 1$, $g$ is the number of rollouts per prompt, and $\hat{A}_i = (r_i - \mathrm{mean}(\{r_k\})) / \mathrm{std}(\{r_k\})$ is the GRPO group-normalized advantage. KL regularization is applied only at the terminal loop against a frozen reference:

$$J_{\mathrm{RLTT}}(\theta) = J_{\mathrm{RLTT\,PG}}(\theta) + \beta\, D_{\mathrm{KL}}\!\bigl[P_\theta^{(T_{\max})}(\cdot) \;\|\; P_{\mathrm{ref}}^{(T_{\max})}(\cdot)\bigr]$$

This ensures every intermediate latent state receives a direct gradient while general language modeling ability is preserved via the terminal-loop KL penalty.

## Loop weighting strategies

Three deterministic weight schedules are evaluated (weights given loop count, no tuning required):

| Strategy | $\omega_t$ | Rationale |
|---|---|---|
| **Exit PDF** | $p_{\mathrm{exit}}(t \mid x)$ from Ouro's learned exit head | Credits loops proportional to Ouro's internal confidence that computation terminates at step $t$ |
| **Progressive** | $t^\alpha / \sum_{s=1}^{T_{\max}} s^\alpha$, $\alpha \geq 0$ | Later loops (closer to terminal distribution) receive more weight |
| **Uniform** | $1 / T_{\max}$ | Treats every loop as an equally valid draft; maximally encourages early-loop correctness |

**Ablation finding (Appendix A.3):** Performance differences across weighting strategies are modest relative to the RLTT–GRPO gap. The fundamental gain comes from exposing RL signal to the full trajectory; the precise credit allocation is a second-order consideration. Exit PDF was used for the primary experiments.

## Memory overhead

RLTT's only additional compute is a weighted sum across loops (linear in $T_{\max}$); per-loop logits are already produced during the forward pass. The practical cost is **memory**: retaining per-loop log-probabilities scales linearly with $T_{\max}$.

In the authors' setup (4 × H200 140GB, VERL framework, vLLM rollouts), this forced `ppo_max_token_len_per_gpu` to 8192 — half of GRPO's 16384 — compensated by additional gradient accumulation mini-steps. Wall-clock training time was 10% **lower** than GRPO (49.05 h vs 54.42 h), attributable to emergent response-length shortening under RLTT (shorter responses = fewer tokens processed per step).

## Base model and training setup

- **Model:** Ouro-2.6B-Thinking (LoopLM with learned early-exit head)
- **Hardware:** 4 × H200 140GB GPUs
- **Framework:** VERL (distributed RL) + vLLM (rollout acceleration)
- **Loop depth:** $T_{\max} = 4$ fixed — Ouro's native adaptive early-exit disabled during training (flagged as a limitation)
- **Training data:** MATH dataset only (Hendrycks et al., 2021)
- **Steps:** 140; rollouts per prompt: 8; max generation length: 2048
- **KL coefficient:** $\beta = 10^{-3}$; binary 0–1 reward

## Key results

All figures are RLTT vs. GRPO under identical training and inference conditions; statistical significance confirmed via paired t-tests (p < 0.05, temperature T=0.2, 10 seeds):

### Math benchmarks (zero-shot)

| Benchmark | GRPO | RLTT | Delta |
|---|---|---|---|
| MATH-500 (2048-token budget) | 71.6% | 86.0% | **+14.4%** |
| AIME24 (3072-token budget) | 16.7% | 33.3% | **+16.6%** |
| BeyondAIME (3072-token budget) | 6.0% | 16.0% | **+10.0%** |
| GSM8K (512-token budget) | 59.7% | 94.0% | **+34.3%** |

### Non-math zero-shot transfer (trained on MATH only)

| Benchmark | GRPO | RLTT | Delta |
|---|---|---|---|
| GPQA | 19.7% | 38.4% | **+18.7%** |
| MMLU-ST | 86.1% | 89.6% | +3.5% |
| ARC-C | 93.7% | 94.4% | +0.7% |
| MBPP | 61.3% | 64.6% | +3.3% |

### Budget-constrained inference (MATH-500)

| Token budget | GRPO | RLTT |
|---|---|---|
| 1024 tokens | 42.4% | **78.4%** |
| 2048 tokens | 71.6% | 86.0% |
| 4096 tokens | 80.8% | 89.8% |

RLTT's advantage holds at 4096 tokens, well beyond the 2048-token training horizon, ruling out overfitting to a specific budget.

## Loop-level analysis

RLTT outperforms GRPO at every loop count (1–4), with the largest absolute margins at 1–2 loops — directly confirming that RLTT improves early-loop latent reasoning, not just terminal-loop prediction. On MATH-500: RLTT 1-loop = 37.4% vs GRPO 1-loop = 32.4%; RLTT 2-loop = 81.2% vs GRPO 2-loop = 66.2%. On GSM8K: RLTT 1-loop = 59.4% vs GRPO 1-loop = 33.2%.

## Why it works

Two complementary mechanisms (Section 6):

1. **Token-efficient reasoning.** Distributing reward across loops favors policies that rapidly converge internally, eliminating late-stage token-level correction. Theorem A.5 (Appendix A.8) formally shows that trajectory-level credit assignment induces weakly shorter optimal decoding lengths than terminal-only credit under diminishing-returns assumptions on reward vs. response length.

2. **Richer gradient signal.** Gradient signal-to-noise ratio (GSNR) is significantly higher for RLTT on AIME24 and BeyondAIME — the hardest benchmarks where rewards are sparse and the credit-assignment bottleneck is most severe. On easier tasks (GSM8K), RLTT's lower GSNR reflects gradient saturation from near-ceiling mastery, not optimization failure.

## Goal relevance

| Goal | Relevance | Notes |
|---|---|---|
| **G3** (token-conditional routing) | **High** | Direct technique for training looped LM reasoning with learned halting; the trajectory-level credit assignment insight applies to any architecture where intermediate latent states produce output distributions. |
| **G1** (block isolation / swappability) | Low | Not addressed; RLTT assumes full parameter updates on all shared blocks jointly. |
| **G2** (dynamic parameter allocation) | Not applicable | RLTT is an RL objective, not a parameter allocation method. |

## Relation to Exp 1

RLTT is **not applicable** to Exp 1 Phase 1 (frozen [[huginn]] weights + KL imitation from a teacher). It becomes relevant when: (a) Huginn weights are unfrozen for joint fine-tuning, and (b) the training objective shifts from KL imitation to outcome-based RL. The core credit-assignment insight — reward must reach intermediate latent steps, not only the terminal state — directly informs how to design RL objectives for the router once Exp 1 moves to RL post-training. The loop-level analysis result (largest gains at 1–2 loops) is particularly informative: it suggests the early recurrent iterations are the bottleneck under standard GRPO, and where trajectory-level signal would matter most in a [[huginn]]-style architecture.

## Credibility

Princeton preprint (Feb 2026), not peer-reviewed. Single base model (Ouro-2.6B-Thinking). Fixed $T_{\max}=4$ — Ouro's native adaptive early-exit is disabled during training, sacrificing per-token compute allocation. This is flagged by the authors as a limitation; future work is noted to explore integrating adaptive halting while preserving trajectory-level credit. Statistical significance established via paired t-tests (T=0.2, 10 seeds).

Comparison point: LSRL (Ren, 2025) applies per-depth process rewards to [[huginn]] by decoding each intermediate latent state and scoring with GPT-4.1 nano, yielding +4.27% on GSM8K — substantially smaller gains than RLTT, with significant additional computational and API overhead. RLTT's approach (no external verifier, no intermediate decoding) is architecturally cleaner.

## Open questions / failure modes

- Fixed $T_{\max}=4$ disables Ouro's learned exit mechanism; RLTT with adaptive halting remains unexplored.
- Memory cost scales linearly with $T_{\max}$; at deeper loop counts (e.g., $T_{\max}=32$ as in [[huginn]]) memory overhead becomes severe without architectural mitigation.
- All results are on a single 2.6B LoopLM. Scaling to larger models or architectures without a native per-loop output head (e.g., mid-training [[huginn]]) requires adaptation.
- GSNR results are mixed: RLTT improves GSNR on hard benchmarks but degrades it on easy ones — the metric is not a universal proxy for optimization quality.

## Source

- `raw/research/recurrent-reasoning/02-rltt-abs.md` (arXiv:2602.10520)
- `raw/research/recurrent-reasoning/07-rltt-pdf.md`

## Related

- [[ouro]] — base model used in all experiments; provides the per-loop exit probabilities used by the Exit PDF weighting strategy.
- [[huginn]] — recurrent-depth architecture (Geiping et al., 2025) analogous to Ouro; LSRL applies a related but weaker process reward to Huginn. RLTT is directly relevant to Huginn RL post-training when weights are unfrozen.
- [[act]] — Adaptive Computation Time; related approach to learned halting in recurrent architectures; Ouro's exit mechanism is a discrete analog.
- [[pondernet]] — learned probabilistic halting for recurrent networks; Exit PDF weighting in RLTT is conceptually related.
- [[looprpt]] — looped transformer research context; RLTT is the first RL framework specifically targeting the multi-step latent computation of LoopLMs.
- [[calm]] — per-token early exit via confidence; complementary: CALM routes at depth within a single forward pass, RLTT trains the multi-loop trajectory via RL.
