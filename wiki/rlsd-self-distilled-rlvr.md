# RLSD — Self-Distilled RLVR

Post-training paradigm that fixes on-policy self-distillation's structural failure by repurposing the self-teacher's **Bayesian evidence ratio as a per-token credit-magnitude multiplier**, while keeping gradient *direction* anchored exclusively to the verifier reward. Drop-in replacement for GRPO's uniform token advantage; **+2.32% avg over GRPO** across five multimodal-reasoning benchmarks, with RLSD@200 steps beating GRPO@400 steps. Yang et al., IIE/CAS + JD.COM, arXiv:2604.03128 (Apr 2026, revised Apr 8).

## Method

**Base paradigm:** GRPO (Group Relative Policy Optimization, DeepSeekMath). RLSD is a drop-in replacement for GRPO's uniform token advantage.

**Problem diagnosed (Theorem 1 + §A.6):** On-policy self-distillation (OPSD) fails because its teacher conditions on privileged information `r` (e.g. a verified reasoning trace) that the student cannot observe. The OPSD objective contains an irreducible mutual-information gap `I(Y_t; R | X, Y_<t) > 0` that the student can never eliminate; per-sample gradients carry an `r`-specific deviation term whose variance is proportional to this MI. The student is driven to encode `x → r` correlations in its parameters — the "**privileged-information leakage**" failure.

**RLSD solution:** Decouple *direction* from *magnitude* in the policy gradient.

- **Direction** (which tokens are reinforced/penalised): governed entirely by the environment verifier reward `R(x, y)`, same sign as GRPO.
- **Magnitude** (how much credit each token receives): modulated by the Bayesian evidence ratio `P_T(y_t) / P_S(y_t)` — teacher (conditioned on `r`) over student (conditioned on `x` only) log-probs. Computed via a single extra forward pass with the same model weights but privileged context prepended.

**Token weight formula:**

```
Δt = sg(log π_θ(y_t | x, r, y<t) − log π_θ(y_t | x, y<t))
w_t = exp(sign(A) · Δt) = (P_T(y_t) / P_S(y_t))^sign(A)
Â_t = A · clip(w_t, 1 − ε_w, 1 + ε_w)
```

The `stop-gradient` on `Δt` ensures the teacher ratio enters only as a scalar weight, never as a gradient direction. When `A > 0` (correct trajectory), tokens the teacher supports get more credit; when `A < 0` (incorrect), tokens the teacher favours bear more blame. Sign of `A` is never flipped (`exp > 0` always).

**λ-schedule:** linear interpolation from uniform advantage (λ=0) to full reweighting (λ=1) over first 50 steps, then decay back to uniform — softening the cold-start.

**Privileged info required:** only the ground-truth final answer — not a full reasoning trace. Less demanding than OPSD, which needs a verified trace from a larger model.

**Implementation:** VERL + EasyR1. Teacher parameters synced with student every 10 steps, frozen between syncs.

## Results

Evaluated on **Qwen3-VL-8B-Instruct**, trained on MMFineReason-123K (difficult-only subset of MMFineReason-1.8M), 4×8×H200 for 200 steps.

| Method | MMMU | MathVista | MathVision | ZeroBench | WeMath | **Avg** |
|---|---|---|---|---|---|---|
| Base LLM | 62.44 | 73.80 | 47.37 | 19.76 | 54.10 | 51.49 |
| GRPO | 65.11 | 76.20 | 48.82 | 22.60 | 56.57 | 53.86 |
| OPSD | 63.82 | 75.10 | 47.53 | 21.06 | 54.95 | 52.49 |
| SDPO | 65.11 | 74.00 | 47.27 | **25.15** | 52.19 | 52.74 |
| GRPO+OPSD | 63.22 | 75.90 | 48.52 | 22.16 | 54.76 | 52.91 |
| **RLSD** | **67.22** | **78.10** | **52.73** | 24.85 | **58.00** | **56.18** |

Key deltas (Table 2, Figure 1):

- **+4.69%** over Base LLM (avg).
- **+2.32%** over GRPO (avg); **+3.91%** on MathVision, +1.9% on MathVista.
- **+3.27%** over GRPO+OPSD.
- **RLSD @ 200 steps outperforms GRPO @ 400 steps** (faster convergence, Fig. 1b).
- RLSD maintains higher entropy throughout training vs. GRPO's entropy collapse (Fig. 5b).
- Clip ratio stabilises at 3–6% (Fig. 5c).

Scale: 8B-param VLM; 4K max context; training data ~123K samples; 32 nodes × H200.

## Applicability

- **Direct use case:** any GRPO-based post-training pipeline for reasoning models where ground-truth answers are available. Drop-in: replace the uniform advantage with `Â_t`. Extra cost: one forward pass per rollout response (authors say negligible vs. generation).
- **Multimodal reasoning:** demonstrated on VLMs (Qwen3-VL-8B). Authors claim consistent gains on pure text reasoning, video understanding, and other model families in preliminary results (not yet in this version).
- **Prerequisites:** (1) GRPO or compatible RLVR infra; (2) dataset with verifiable answers (binary reward sufficient); (3) the privileged info is just the correct answer string — no distillation traces from a larger teacher; (4) ~32 H200-class GPUs at 8B scale, though the method is architecture-agnostic.
- **Not applicable when** no verifiable reward signal exists (open-ended generation without ground truth).

## Novelty

Genuinely new paradigm combining RLVR and self-distillation by separating direction from magnitude. The key insight — use the teacher's evidence ratio *only* as a magnitude signal, never in the gradient direction — is theoretically motivated and proven to be structurally immune to MI leakage (Appendix A.6).

Closest prior work:

- **OPSD** (Ye et al.; Kong et al.) — same self-teacher setup but uses distribution matching, shown here to fail.
- **SDPO** (Kong et al.) — similar self-distillation premise, uses the previous successful rollout as privileged context.
- **GRPO** (Shao et al., DeepSeekMath) — the base RL method.
- **TRRD** (concurrent) — also identifies the KL-reward conflict but injects teacher probabilities into the importance ratio (trust region), not the advantage magnitude; different mechanism.
- **PPO value functions / process reward models** — also do token-level credit, but require auxiliary networks; RLSD uses one free forward pass.

What changed: prior self-distillation methods use distribution matching as the loss; RLSD **abandons distribution matching entirely** and re-uses the self-teacher only as a Bayesian evidence ratio weighting existing GRPO advantages. This provably avoids the MI gap.

## Reproducibility

- Paper: arXiv:2604.03128 (April 2026).
- **No code repo or released weights** in this preprint version.
- Implementation described as based on VERL and EasyR1 (both public frameworks).
- Authors note this is an early release with "limited experiments"; fuller version forthcoming.
- No paperswithcode entry at capture time. No independent reproduction reported.

## Adoption

Very recent (April 2026). No citation count or community adoption signal visible yet. Concurrent work (TRRD) cited, indicating the problem space is active. Not yet on any leaderboard.

## Conflicts

- **OPSD is actively harmful, not merely weaker.** The paper's Theorem 1 claim — that on-policy self-distillation under information asymmetry is structurally ill-posed — is a strong theoretical position. No existing wiki page covers OPSD directly, so no conflict file is opened; if a future source argues OPSD-style methods are viable at scale, that would be the counterposition.

## Source

- `raw/research/weekly-2026-04-22/02-self-distilled-rlvr.md` — Self-Distilled RLVR paper PDF (arXiv:2604.03128). Captured 2026-04-22.

## Related

- [[eggroll]] — both papers engage with the question of what can replace or augment GRPO for post-training reasoning. RLSD argues GRPO's *direction* signal is the reliable anchor and improves only the magnitude; EGGROLL argues ES can *replace* GRPO at scale. Parallel debate about GRPO's role.
- [[conflicts/grpo-vs-evolution-strategies]] — the broader RL post-training landscape RLSD inhabits; RLSD's stance reinforces Position A (gradient-RL remains the direction anchor).
- [[watchlist]] — OPSD, SDPO, TRRD referenced but not captured.
