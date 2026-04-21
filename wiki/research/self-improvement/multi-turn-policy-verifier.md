# PAG: Multi-Turn Reinforced LLM Self-Correction with Policy as Generative Verifier

Yuhua Jiang, Yuwen Xiong, Yufeng Yuan, Chao Xin, Wenyuan Xu, Yu Yue, Qianchuan Zhao, Lin Yan. Tsinghua / ByteDance Seed. arXiv:2506.10406. Unified multi-turn RL framework where a single LLM alternates policy (solution generation) and verifier roles. Selective revision mechanism: revise only when self-verification detects error, avoiding model collapse. Achieves 65.2% on MATH500 (1.5B), surpasses SCoRe, eliminates warm-up phase; verifier outperforms majority voting and human-scale evaluators on RewardBench.

## Method

PAG frames multi-turn self-correction as a single trajectory with alternating policy and verifier segments. For input $x$, the policy generates attempt $\hat{y}_1$; then the verifier produces self-verification $\hat{v}^2$ evaluating correctness. If $C(\hat{v}^2, \hat{y}_1, x) = 1$ (verified correct), stop; else generate revised attempt $\hat{y}_2$. Training objective combines attempt and verification rewards:

$$\max_\theta \mathbb{E}_{x \sim p(x)} \left[ \mathbb{E}_{\tau_x \sim \pi_\theta} \left[ \sum_i \widehat{R}_y(\hat{y}_i, x) + \sum_j \widehat{R}_v(\hat{v}_{j+1}, \hat{y}_j, x) \right] \right]$$

**Turn-independent optimization:** Values from later turns are not backpropagated to earlier turns (turn-level discount = 0), preventing reward hacking where verifier learns to always trigger revisions. **RoleAdvNorm:** Normalize advantages separately for policy vs. verifier roles, preventing cross-role contamination. **Reward shaping:** Bonus $\alpha(R_y(\hat{y}^t, x) - R_y(\hat{y}^{t-1}, x))$ explicitly incentivizes improvement between attempts. Extends PPO to multi-turn via concatenated trajectory; trained end-to-end from instruction-tuned models, no warm-up phase required.

## Claims

- PAG achieves 65.2% Acc.@final on MATH500 (Qwen 1.5B), vs. 63.9% (SCoRe), 62.4% (SingleTurn); 36.7% on Llama3-8B, significantly above baselines (Table 1).
- State-of-the-art across diverse math benchmarks: 82.3% on MATH500, 37.2% on MinervaMath, 18.4% on AIME2024 with Qwen 7B (Table 2, avg 38.3%).
- Eliminates model collapse: answer change ratio remains high during training; Direct MultiTurn collapses to ~0 (Figure 3), while PAG maintains selective revision.
- Verifier accuracy 81.7% on self-generated MATH500 (1.5B); on RewardBench mathprm: 86.6 score for 7B, exceeding GPT-4 (76.3) and Llama-3.1-70B (76.4) despite 7B base model (Table 3, Figure 4).
- PAG self-verify Best-of-N outperforms majority voting by 1–1.5% (Figure 5); demonstrates that PAG training produces better verifiers than standard baselines, contrary to prior findings.
- Sequential self-correction sampling 4× more compute-efficient than parallel sampling: K=8 sequential + 1 correction outperforms K=32 parallel (Figure 8).
- Scaling training turns from 2→4 yields 1% improvement in Acc.@final at 8 inference attempts, with marginal gains suggesting efficient learning (Figure 9).

## Relevance to the project

PAG exemplifies single-sample, concept-based fine-tuning through *role unification*: one model learns two tightly coupled concepts (generation and verification) from ground-truth labels on a single training set. No warm-up, no auxiliary reward model, no multi-stage curriculum—just raw multi-turn RL on task labels. The selective revision mechanism is the key innovation: conditioning revision on the model's own judgment (self-verification) is a learnable concept that prevents collapse.

For single-sample scenarios, PAG is highly efficient: improvements come from better *organization* of learning (multi-turn trajectories) rather than more data. The generative verifier capability is particularly valuable for concept-based fine-tuning: the model learns to verify its own reasoning, enabling adaptive sampling strategies like best-of-N at inference with a single model.

Limitation: PAG requires external ground-truth to assign training rewards; cannot bootstrap purely self-supervised. Applicability to domains without clear correctness labels (open-ended text, code review) unclear. Limited to 2 training turns in main experiments; scalability to longer horizons untested.

## Source

- arXiv: 2506.10406
- Raw markdown: `../../../raw/research/adjacent-reward-signals/03-multi-turn-policy-verifier.md`
- Raw PDF: `../../../raw/research/adjacent-reward-signals/pdfs/multi-turn-policy-verifier.pdf`

## Related

- [[star]] — bootstrapping reasoning via self-generated trajectories
- [[self-rewarding-lm]] — joint policy and reward learning
- [[rstar-math]] — multi-turn RL with outcome rewards
- [[../process-reward-models/lets-verify-step-by-step]] — generative verification and PRM training
- [[../process-reward-models/math-shepherd]] — step-level feedback in multi-turn
- [[../single-sample-rl-finetuning/_overview]] — dense RL on single dataset
- [[../rlvr-mechanics/_overview]] — PPO stability and multi-turn trajectories
- [[../synthesis/single-sample-concept-skeleton]] — framework for unified fine-tuning
