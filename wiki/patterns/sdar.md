# SDAR — Self-Distilled Agentic Reinforcement Learning (arXiv 2605.15155)

Zhejiang University + Meituan paper that combines on-policy self-distillation with GRPO-based RL for multi-turn agents via a **token-level sigmoid gate** that selectively incorporates teacher signals from privileged-context rollouts. The core insight: naive GRPO+OPSD fails in multi-turn settings (trajectory drift makes >50% of teacher tokens unreliable), so SDAR keeps RL as the primary objective and adds an auxiliary OPSD loss only where the teacher is more confident than the student. Crucially, privileged context (a retrieved SkillBank) is used **at training time only** and internalized into policy weights — no external skills or tools are needed at inference. SDAR reports beating GRPO baselines by ~+9.4 pp on ALFWorld (Qwen2.5-3B) and ~+10.2 pp on WebShop (Qwen2.5-7B), and outperforms even skill-augmented Skill-GRPO* (which does require skills at test time) on ALFWorld-3B (84.4 vs 80.5). All numbers are self-reported arXiv preprint — collect-but-confirm.

## Mechanism

**Training objective**: `L = L_GRPO + λ · L_SDAR` where `λ=0.01`. The OPSD auxiliary term uses a sigmoid gate `g_t = σ(β·Δ_t)` with `β=5.0`, where `Δ_t = log π_T(y_t|s_t+) − log π_θ(y_t|s_t)` is the log-probability gap between the teacher branch (same policy + retrieved skills) and the student on each sampled token. Positive gap (teacher more confident) → full distillation weight; negative gap (teacher less confident, e.g. bad skill retrieval) → soft attenuation. The RL advantage signal is left fully intact regardless — the distillation is strictly auxiliary.

**Why naive GRPO+OPSD fails**: Compounding trajectory drift in multi-turn settings makes the teacher's per-token supervision increasingly unreliable. SDAR's sigmoid gate recovers this by selectively trusting teacher tokens only where the teacher demonstrates higher likelihood on the student's own sampled output.

**Privileged context**: A SkillBank (retrieved skills) is injected into the teacher branch at training. The teacher is not a stronger external model — it is the same policy with augmented context. Negative teacher rejections can arise from imperfect skill retrieval, motivating the asymmetric sigmoid gate.

## Skills internalization finding

SDAR directly challenges the assumption that runtime skill access is load-bearing. Skill-GRPO drops from 60.2% to 28.9% on ALFWorld-3B when skills are removed at inference — underperforming vanilla GRPO. SDAR (84.4%) surpasses Skill-GRPO* (80.5%) on the same setting while using **no skills at test time**, demonstrating that the privileged context has been internalized into weights. Even random skill retrieval at training time outperforms GRPO baseline (+1.9/+1.6/+1.0 on ALFWorld/WebShop-Score/WebShop-Acc), validating that gains arise from the gating mechanics rather than retrieval quality.

## Reported results (self-reported, Qwen2.5, SDAR vs GRPO)

| Setting | SDAR | GRPO | Δ |
|---|---|---|---|
| ALFWorld (3B) | 84.4% | 75.0% | +9.4 pp |
| ALFWorld (7B) | 85.9% | 81.2% | +4.7 pp |
| WebShop-Acc (7B) | 82.8% | 72.6% | +10.2 pp |
| Search-QA avg (7B) | 49.0 | 42.0 | +7.0 |

Scales tested: Qwen2.5-3B, Qwen2.5-7B, Qwen3-1.7B. Code and fine-tuned models released at https://github.com/ZJU-REAL/SDAR — reproducibility positive.

## Position in the self-improvement landscape

SDAR belongs to the **distillation-back-into-weights** direction of the weights→context→harness arc ([[patterns/externalization-survey]]): privileged knowledge that exists at training (skill context) is compressed into policy parameters rather than carried as runtime context. This is the inverse of [[patterns/skillos]], which trains a separate curator to manage a live external SkillRepo at inference. Both address skill-conditioned RL on the same benchmarks (ALFWorld, WebShop) but differ on runtime footprint: SkillOS externalizes skills permanently; SDAR internalizes them permanently.

Contrasted with [[memory/reflexion]]: Reflexion is inference-time verbal RL (failure → verbal reflection → episodic buffer → retry). SDAR is post-training token-level RL. Both use self-generated signals to improve agents but at entirely different phases and granularities.

## Source

- `raw/research/weekly-2026-05-18/05-sdar-self-distilled-rl.md`

## Related

- [[patterns/skill-distillation]] — SDAR is a multi-turn-RL concrete instance of distillation-into-weights; extends that pattern's scope.
- [[patterns/skillos]] — parallel skill-conditioned RL approach; SkillOS manages skills at inference, SDAR internalizes them at training.
- [[patterns/externalization-survey]] — SDAR's training-only privileged context fits the "distillation back into weights" direction of the weights→context→harness arc.
- [[memory/reflexion]] — contrast case: inference-time verbal RL vs post-training token-level RL.
- [[patterns/effective-harnesses]] — both address multi-turn agent capability; SDAR via weight internalization, harnesses via structured context scaffolding.
