# Anti-Self-Distillation (AntiSD)

arXiv:2605.11609 (Xiaohongshu / CAS, 2026-05-25). AntiSD proves via a per-token PMI identity (Lemma 2) that standard on-policy self-distillation structurally suppresses deliberation tokens ("Wait", "Let", "Maybe") during reasoning RL: the default KL-descent SD signal equals conditional PMI(y_t; c | x, y_<t), so tokens where the teacher is *more* confident than the student (high PMI, already implied by the privileged context) are rewarded while high-entropy deliberation tokens (negative PMI) are penalised. AntiSD corrects this by *ascending* Jensen–Shannon divergence instead, yielding per-token advantage A_t = −φ(u_t) where φ(u) = ½(softplus(u) − log 2) and u_t is the teacher/student log-ratio; the JSD f-divergence derivative caps the advantage at ½ log 2, absorbing u_t ≤ −20 spikes on the deliberation side while maintaining a linear penalty on shortcut tokens. An entropy-triggered Schmitt-trigger gate (auto-calibrated from 5 warmup steps at λ=0) disables the term when teacher median per-token entropy falls below τ_down = 0.93·H_warm and re-enables at H_warm, preventing Qwen-family collapse (~step 90 without the gate). Combined objective: A_i,t = A_i^seq + λ·(−φ(u_i,t)), λ_max = 0.5, additive. The summed per-token contributions telescope to sequence-level PMI(y;c|x), placing AntiSD in the potential-based reward shaping framework (Ng et al. 1999) — the shaping term leaves the optimal-policy set invariant. Privileged context c is sampled from the same batch rollout group (fallback: dataset reference solution). Headline results across five Qwen3/OLMo-3 models (DAPO-Math-17k, 200 steps, avg@32 on AIME 2024/2025/2026 + HMMT 2025 + avg@4 MinervaMath): AntiSD reaches GRPO baseline accuracy in 2–10× fewer steps and exceeds it by up to +11.5 pp (Qwen3-4B-IT-2507: GRPO 51.3 → AntiSD 62.8, 10× speedup; default SD 45.9, below the base model). Default SD collapses on every model tested, often dramatically (Qwen3-8B: SD 30.6 vs GRPO 57.4).

## Method

On-policy self-distillation (OPD family): same network is both student π_S (conditioned on x) and teacher π_T (conditioned on x plus privileged context c — a verified peer rollout and a correctness feedback string). Per-token log-ratio u_t = log π_T(y_t|x,c,y_<t) − log π_S(y_t|x,y_<t) equals PMI(y_t; c | x, y_<t) by Bayes' rule. Default SD descends this KL, reinforcing shortcut tokens and suppressing deliberation. AntiSD ascends JSD: −φ(u_t) is bounded (JSD is symmetric and bounded by log 2), providing gradient stability absent from raw KL ascent. Entropy gate auto-calibrates threshold from 5 warmup steps; no per-model tuning required. Implementation requires two forward passes per token (same model, different context prefix), no extra parameters, no separate reward model. Framework: verl.

## Results

Table 1 (5-benchmark Avg, 200 on-policy steps):

| Model | GRPO | AntiSD | Default SD | Speedup |
|---|---|---|---|---|
| Qwen3-8B | 57.4 | **65.7** (+8.3) | 30.6 | 5.0× |
| Qwen3-4B-IT-2507 | 51.3 | **62.8** (+11.5) | 45.9 | 10.0× |
| OLMo3-7B-IT | 43.0 | **48.3** (+5.3) | 41.1 | 9.5× |
| OLMo3-7B-TK | 64.1 | **66.2** (+2.1) | 62.6 | 2.0× |
| Qwen3-30B-A3B | 59.1 | **66.8** (+7.7) | 34.5 | 2.9× |

Pass@32 lead on HMMT 2025 sustained (Figure 3) — coverage expansion, not diversity collapse. Code reasoning (Qwen3-8B, avg@10): +1.2 pp HumanEval+ (40.4→41.6), +2.3 pp MBPP+ (61.0→63.3) over GRPO.

Continual AntiSD (Table 4): resuming from GRPO@200 checkpoint on Qwen3-8B reaches 65.0 Avg in +30 post-resume steps vs 180 from-base steps — stackable on a saturated GRPO checkpoint.

Ablations (Table 3, Qwen3-4B-IT-2507): JSD ascent > reverse-KL ascent (62.8 vs 49.5); additive composition > multiplicative (62.8 vs 56.5); gate essential for Qwen family.

## Applicability

Drop-in for default SD in any RLVR/GRPO pipeline that produces verified rollouts. Prerequisites: group-rollout setup with at least some correct rollouts (to sample c); two forward passes per token (same model, different context prefix); per-token advantage support in training framework; 5 warmup steps for gate auto-calibration. No per-model threshold tuning. Applicable to code reasoning (smaller gains). Not yet tested on multi-turn agentic or multimodal settings.

## Conflict note: not a flat contradiction of [[rlsd-self-distilled-rlvr]]

AntiSD's claim that "default self-distillation is harmful" applies to the standard KL-descent instantiation. [[rlsd-self-distilled-rlvr]] (Zhao et al., arXiv:2601.18734) decouples direction from magnitude via the teacher/student evidence ratio — a different instantiation of the SD family that improves over GRPO (+2.32% avg, RLSD@200 beats GRPO@400). Both papers agree vanilla KL-descent SD is broken for math; they differ on the correct fix. These are different SD variants; the conflict is about baseline instantiation, not an outright contradiction between the two approaches.

## Reproducibility

Code: `github.com/FloyedShen/AntiSD`. Public WandB: `wandb.ai/brain-cog/AntiSD`. Full hyperparameters in Appendix B (Table 5); self-teacher context templates in Appendix C. No independent reproduction observed at capture. HF Daily Papers #1 the week of 2026-05-25.

## Source

- `raw/research/weekly-2026-05-25/04-anti-self-distillation.md` (arXiv:2605.11609)

## Related

- [[rlsd-self-distilled-rlvr]] — on-policy self-distillation fix via decoupled direction/magnitude (evidence ratio); different SD instantiation, both beat GRPO on math
- [[token-gradient-cancellation]] — per-token credit assignment in GRPO; AntiSD's PMI framing complements DFPO's gradient-exchangeability condition
- [[tempo-test-time-rl]] — deliberation/search preservation in reasoning RL via E-step recalibration; shared concern about training collapse suppressing search tokens
- [[reasonmaxxer]] — RL modifies only high-entropy decisions; AntiSD's finding that SD suppresses high-entropy deliberation tokens runs parallel
- [[delta-token-credit]] — sibling per-token RL-credit paper surfaced the same week; complementary credit-assignment angle
- [[latent-grpo]] — per-token GRPO stabilization in continuous-token space; AntiSD fixes polarity of distillation signal in discrete-token space
