# LoopRPT: Reinforcement Pre-Training for Looped Language Models

LoopRPT (Tang et al., arXiv Mar 2026; Harbin/Tsinghua/HKUST) is the first framework to apply Reinforcement Pre-Training (RPT) to looped language models. Standard RL paradigms assign signals to output tokens; [[ouro]]-style looped LMs perform reasoning implicitly across recurrent latent steps, making token-level rewards structurally mismatched. LoopRPT reframes next-token prediction as a next-token reasoning task and routes RL signals directly to intermediate latent iterations via an EMA teacher, noisy rollouts, and a difficulty-aware time penalty. Trained on OMNI-MATH competition math at 1.4B and 2.6B scale, it achieves Pareto dominance in accuracy–compute trade-offs over baseline Ouro and over Qwen3-1.7B with CoT.

## Method core

The framework has four tightly coupled components, all applied only to hard-token positions identified by entropy.

**Entropy-based hard-token selection.** An EMA teacher $\bar{\theta}$ computes per-token entropy $H_t = -\sum_v p_{\bar{\theta}}(v \mid x_{<t}) \log p_{\bar{\theta}}(v \mid x_{<t})$. The top-$\rho$% highest-entropy positions within each example are designated hard tokens; all subsequent losses are masked to these positions. Easy tokens yield weak RL signal and are excluded to avoid diluting gradient updates.

**Step-wise rewards with EMA teacher (momentum 0.995).** The teacher defines a reference exit step $t_\text{ref} = \min\{k : \sum_{j \le k} \pi_{\bar{\theta}}(j) \ge \tau\}$ — the first step where cumulative exit probability exceeds threshold $\tau$. The teacher log-probability at $t_\text{ref}$ is the per-token baseline $b_\text{ref} = \ell_{\bar{\theta}}^{(t_\text{ref})}$. The step-wise reward for student step $k$ is:

$$R(k) = \underbrace{\ell_\theta^{(k)} - b_\text{ref}}_{\Delta_\text{acc}(k)} - \underbrace{\lambda_t (k - t_\text{ref})}_{C(k)}$$

The accuracy gain $\Delta_\text{acc}(k)$ measures how much better the student predicts the ground-truth token at step $k$ versus the teacher at its reference step. The difficulty-aware time penalty $C(k)$ uses a token-dependent coefficient $\lambda_t = \lambda_\text{base}(1 + \lambda_\text{scale}(1 - d_t))$, where $d_t = \text{Clamp}(H_t / \log|V|, 0, 1)$ is normalized teacher entropy. Easier tokens (lower $d_t$) incur larger $\lambda_t$, so the penalty pushes easy tokens toward earlier exits while leaving hard tokens more room to iterate.

**Noisy latent rollouts (GRPO).** Because looped-LM reasoning is implicit in latent space — there are no discrete action tokens — on-policy variability is induced by injecting Gaussian noise $\epsilon^{(k)} \sim \mathcal{N}(0, \sigma^2 I)$ into the recurrent hidden states across $G$ rollouts. Each rollout samples an exit step $t^{(g)} \sim \pi_\theta^{(g)}$ and observes reward $r^{(g)} = R(t^{(g)})$. Group-wise GRPO normalization $A^{(g)} = (r^{(g)} - \text{mean}_g[r^{(g)}]) / (\text{std}_g[r^{(g)}] + \epsilon)$ stabilizes the policy-gradient loss:

$$\mathcal{L}_\text{PG} = -\mathbb{E}_g\!\left[A^{(g)} \log \pi_\theta^{(g)}(t^{(g)})\right]$$

**Step-weighted representation learning.** A deterministic (noise-free) forward pass computes per-step log-probabilities $\ell_\theta^{(k)}$ and exit weights $\pi_\theta(k)$. The step-advantage $A'(k) = (R(k) - \mu_R)/\sigma_R$ is used to upweight steps with positive reward. The representation objective:

$$\mathcal{L}_\text{rep} = -\sum_{k=1}^K w_k \ell_\theta^{(k)}, \quad w_k = \pi_\theta(k)\!\left[1 + \text{ReLU}(A'(k))\right]$$

pushes early steps to predict correctly, not merely to exit.

**Full objective:**

$$\mathcal{L} = \alpha\,\mathcal{L}_\text{PG} + \beta\,\mathcal{L}_\text{rep} + \gamma\,\mathcal{L}_\text{ent} + \delta\,\mathcal{L}_\text{KL}$$

$\mathcal{L}_\text{ent}$ is an exit-distribution entropy bonus preventing premature collapse to a single step. $\mathcal{L}_\text{KL}$ is a trust-region penalty computed from token-level step-wise log-probability ratios between student and EMA teacher.

## Contrast with RLTT

LoopRPT and [[rltt]] bracket the RL training timeline for looped LMs:

| | LoopRPT | RLTT |
|---|---|---|
| Stage | Pre-training | Fine-tuning |
| Reward source | Corpus NTP (RPT paradigm) | Verifiable task rewards |
| Target | General latent reasoning quality | Specific benchmark accuracy |
| Labels required | None — intrinsic corpus signal | Task-specific verifiable answers |

They are complementary: LoopRPT improves the backbone's latent representations before task-specific RLTT specialization.

## Experimental setup

- **Base model:** [[ouro]] architecture at 1.4B and 2.6B. Teacher and student both initialized from the same Ouro base; teacher is maintained as EMA (momentum 0.995) of student.
- **Training data:** OMNI-MATH (4,228 competition-level math problems; 200 held out for validation).
- **Evaluation:** zero-shot on MMLU, MMLU-Pro, BBH, ARC-C, HellaSwag, Winogrande, GSM8K, MBPP, HumanEval (via lm-eval-harness).

## Key results

**Next-token reasoning (OMNI-MATH hard bucket, Ouro-2.6B):**
- Accuracy: +2.89 pts (34.35 → 37.24, adaptive exit)
- Average inference steps: 3.51 → 2.28 (−1.23 steps)
- Peak accuracy (all 4 loops forced): +3.58 pts

**Baseline comparison:** Qwen3-1.7B with CoT prompting collapses to 10.70% on easy tokens (vs 47.49% vanilla), demonstrating that explicit CoT is harmful for next-token reasoning tasks. Ouro-2.6B + LoopRPT (adaptive): 37.24% on hard tokens.

**Downstream (2.6B):** GSM8K 81.76 → 85.36; MBPP+ +2.91; HumanEval+ gains.

**Ablation (1.4B, hard split):** Every component contributes. Removing $\mathcal{L}_\text{rep} + \mathcal{L}_\text{ent}$ causes the largest degradation (accuracy and efficiency). Removing token selection reduces steps slightly but hurts hard-split accuracy, confirming the selective gradient allocation matters. Removing the time penalty leaves accuracy roughly intact but raises average steps, confirming it is the primary driver of adaptive-exit efficiency.

**Per-step analysis:** LoopRPT improves prediction accuracy at every latent step, with the largest gains at steps 1–2. This confirms it improves intermediate representation quality rather than just gate calibration.

## Relation to Exp 1

LoopRPT is a pre-training technique operating on a parameter-shared looped backbone; it is incompatible with Exp 1's frozen-weight router setup. Relevant as a future technique: if Exp 1's router succeeds in identifying productive routing signals from [[huginn]]'s latent steps, LoopRPT-style continued pre-training could improve the quality of those representations at each step, making routing signals more discriminable and reducing the number of steps required for confident exits.

## Goal relevance

| Goal | Relevance | Notes |
|------|-----------|-------|
| **G3** (token-conditional routing) | **High** | Directly trains adaptive halting via per-step RL; the first principled RL recipe for latent-step routing in looped LMs. |
| **G1** (block isolation / swappability) | Low | Pre-training technique on parameter-shared backbone; not aimed at block isolation. |
| **G2** (dynamic parameter allocation) | Not applicable | Compute allocation is dynamic at inference but the method does not concern parameter partitioning. |

## Credibility

arXiv preprint (Mar 2026), not peer-reviewed. Harbin Institute of Technology / Tsinghua / HKUST. Ablation is thorough and component-wise. Tested only on the [[ouro]] architecture; results on non-looped recurrent models (e.g., [[huginn]]) are not reported. The OMNI-MATH training corpus is narrow (math competition problems); generalization to broader pre-training mixtures is unverified.

## Open questions / failure modes

- Ouro-only validation: whether the method transfers to other looped or depth-recurrent architectures (e.g., Huginn, Universal Transformers) is untested.
- The exit gate's training signal depends on the EMA teacher's $t_\text{ref}$; if the teacher is systematically miscalibrated early in training, $b_\text{ref}$ will be a noisy baseline.
- Forced-depth evaluation shows non-monotonic accuracy as depth increases for medium/hard tokens — additional iterations can degrade performance, which is a known risk of looped architectures that LoopRPT does not fully resolve.
- No wall-clock inference benchmark: step-count reductions do not directly translate to throughput gains when the exit gate itself adds per-step overhead.
- Training data is math-only; whether RPT corpus rewards generalize to code or general text domains at scale is open.

## Source

- `raw/research/recurrent-reasoning/03-looprpt-abs.md` (arXiv:2603.19714)
- `raw/research/recurrent-reasoning/09-looprpt-pdf.md`

## Related

- [[ouro]] — base architecture; LoopRPT is instantiated exclusively on Ouro and relies on its exit-gate mechanism.
- [[rltt]] — complementary RL method for looped LMs: fine-tuning (task rewards) vs. LoopRPT's pre-training (corpus rewards). Together they bracket the RL training timeline.
- [[huginn]] — depth-recurrent LM without a looping backbone; LoopRPT is not directly applicable but motivates analogous latent-step RL for Huginn if routing signals become the training target.
- [[act]] — Adaptive Computation Time (Graves 2016); foundational prior work on learned halting that LoopRPT's exit policy extends via RL rather than a differentiable halting unit.
- [[pondernet]] — learned pondering mechanism; closest architectural precursor to the exit gate LoopRPT trains.
- [[mod]] — Mixture-of-Depths; token-conditional compute allocation in the depth dimension via top-$k$ routing, contrasting with LoopRPT's RL-trained exit in a recurrent (weight-shared) setting.
