# TEMPO: Scaling Test-Time Training for Large Reasoning Models

Zhang, Kong, Wu, Hu, M. Wu, Yang, Cheng, Luo, Cui, C. Zhang (Tianjin / Tongyi Lab / CUHK / Shanghai AI Lab, arXiv:2604.19295). Test-time training framework that interleaves **EM-style critic recalibration on labelled data (E-step)** with **policy refinement on unlabelled test questions (M-step)**, achieving sustained AIME 2024 gains of **+18.1 pp** (OLMO3-7B 33.0 → 51.1) and **+23.5 pp** (Qwen3-14B 42.3 → 65.8) over RLVR baselines while preserving pass@k. Reframes prior TTT methods (TTRL, EMPO) as "M-step-only" degenerate variants whose self-generated reward drifts; reintroducing the E-step tightens the ELBO and unlocks scaling beyond ~100 steps.

## Source
- [`raw/research/weekly-2026-05-03/01-tempo-test-time-training.md`](../../../raw/research/weekly-2026-05-03/01-tempo-test-time-training.md) — captured 2026-05-03 (arXiv:2604.19295)

## Method

Two networks: actor $\pi_\theta$ + critic $V_\phi$. Initialised from RLVR (PPO/GRPO) on labelled set $D_L$.

- **E-step (critic calibration):** Trained on $D_L$ via MSE against binary correctness $I$:
  $$\mathcal{L}_\text{critic}(\phi) = \mathbb{E}_{(x,y,I)\sim D_L}\|V_\phi(x,y_t)-I\|_2^2.$$
- **M-step (policy refinement):** On unlabelled test set $D_u$, use $V_\phi(x, y_T)$ as terminal reward and intermediate $V_\phi(x, y_{1:t})$ as token-level baselines. Advantage $A_t = R - V_\phi(x, y_{1:t})$. Loss (Eq. 12) is policy gradient with GSPO dual-clip for off-policy stabilisation.

Alternation = EM. Frozen-critic ablation plateaus at ~100 steps (Figure 6); the recalibration step is load-bearing for sustained scaling.

## Empirical headline (Table; deltas vs. RLVR-only baseline)

| Model | AIME24 | AIME25 | BBH | AGI Eval | ZebraLogic | GPQA-D Avg@8 |
|---|---|---|---|---|---|---|
| OLMO3-7B | +18.1 | +10.7 | +21.4 | +24.5 | +12.9 | +10.5 |
| Qwen3-14B | +23.5 | +7.5 | — | — | — | — |

Outperforms TTRL and EMPO on every benchmark; pass@k preserved while baselines collapse.

## Sample efficiency

- **$D_L$:** DAPO-Math-17K (17k labelled examples) for math; Dolci-RL-Zero-General (12.8k) for general reasoning. **Not single-sample / few-shot** — labelled calibration set must be maintained throughout deployment.
- **Compute overhead:** 2× single-model TTT (actor + critic).

## Where it sits in the wiki

- Extends [[../test-time-training/_overview]] as a TTT method that updates weights at test time *with* a labelled anchor — bounded the design space alongside [[ttt-few-shot]] (per-input synthetic SFT) and [[algorithm-distillation]] (in-context RL, no weights update).
- Diagnoses the failure mode of [[../self-improvement/_overview]]-style self-rewarding loops (TTRL/EMPO): without recalibration, critic drift kills diversity.
- Critic = token-level value function trained on outcome labels — closest to [[../process-reward-models/math-shepherd]].
- M-step uses [[../rl-optimizers/gspo]]'s sequence clip; initial RLVR phase uses [[../rl-optimizers/dapo]]-Math-17K corpus.

## Tension flagged (not blocking)

TEMPO claims sustained pass@k while baselines collapse. [[../self-play/invisible-leash]] (Theorem C.1) implies on-policy gradient updates cannot expand support beyond base. TEMPO reports pass@k *maintained*, not improved beyond base — Stage-1-scoped consistent with the [[../self-play/two-stage-dynamic]] refinement, but the 350-step run may be probing Stage-2 territory. Worth tracking; not a clean conflict.

## Limitations

1. 2× memory/compute vs. single-model TTT.
2. Requires $D_L$ throughout deployment — distribution and size affect critic OOD.
3. Not validated on code generation.
4. No formal convergence guarantees for the alternation.
5. Some Qwen3-14B pass@k deltas negative on OlymMath / AIME 26 despite avg@k positive — diversity-vs-mode tradeoff partially survives.

## Related

- [[_overview]] — TTT theme overview
- [[ttt-few-shot]] — Akyürek et al. per-input synthetic-SFT TTT
- [[algorithm-distillation]] — in-context RL TTT
- [[../self-improvement/_overview]] — self-generated reward loops TEMPO diagnoses
- [[../rl-optimizers/gspo]] — sequence-clip used in M-step
- [[../rl-optimizers/dapo]] — DAPO-Math-17K labelled corpus
- [[../process-reward-models/math-shepherd]] — automated step labels parallel
- [[../teacher-student-rl/soar-edge-of-learnability]] — bilevel meta-RL with outer recalibration
- [[../self-play/invisible-leash]] — diversity-vs-base tension
- [[../self-play/two-stage-dynamic]] — Stage-1/Stage-2 framing
- [[../../weekly-briefs/2026-05-03]] — brought in by the 2026-05-03 weekly sweep
