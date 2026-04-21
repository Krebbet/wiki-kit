# REFT: Reasoning with REinforced Fine-Tuning

Trung Quoc Luong, Xinbo Zhang, Zhanming Jie, Peng Sun, Xiaoran Jin, Hang Li. ByteDance Research. arXiv:2401.08967. Two-stage approach: SFT warm-up (1–2 epochs) followed by PPO on ground-truth answer rewards. REFT samples multiple CoT paths per problem and learns from all (correct and incorrect) without external reward models, achieving 10–12% improvement over SFT on math benchmarks and 6–7% average gain from single-sample training data.

## Method

REFT comprises two stages. **Warm-up:** Standard supervised fine-tuning on $(x, e, y)$ tuples (question, chain-of-thought, answer) for 1–2 epochs, establishing baseline capability via maximum-likelihood loss $\mathcal{L}_{\text{SFT}}(\theta) = -\mathbb{E}_{e \sim \mathcal{D}}[\sum_t \log \pi_\theta(a_t | s_t)]$. **RL stage:** Online PPO trains on $(x, y)$ pairs only, sampling CoT trajectories $\hat{e} \sim \pi_\theta(x)$ and assigning binary/partial rewards by extracting the final answer and comparing to ground truth:

$$r(s_t, a_t, s_{t+1}) = \begin{cases} 1 & \text{if EXTRACT}(s_{t+1}) = y \\ 0.1 & \text{if extractable but } \neq y \\ 0 & \text{if not extractable} \end{cases}$$

Total reward incorporates outcome score plus KL divergence regularization: $r_{\text{total}} = r(s_t, a_t, s_{t+1}) - \beta \text{KL}(\pi_\theta(\cdot|s_t), \pi_\theta^{(0)}(\cdot|s_t))$. GAE and clipped objective optimize both policy and value head (initialized from warm-up checkpoint) across 300 RL epochs.

## Claims

- ReFT achieves 10-point improvement over SFT on GSM8K N-CoT (CodeLLAMA-7B: 53.3% vs. 43.6%) and 12-point on P-CoT (75.3% vs. 63.7%; Table 2).
- Average 6.7% gain across three datasets (GSM8K, SVAMP, MathQA) in N-CoT; 7.4% in P-CoT over SFT on same training data.
- ReFT + Voting reaches 63.2% (N-CoT) and 78.0% (P-CoT) on GSM8K; ReFT + Reranking achieves 81.2% P-CoT, surpassing GPT-3.5-turbo (78.0%) on same model budget (CodeLLAMA-7B).
- Offline and Online self-training baselines yield modest gains (1–2% on average; Figure 3 comparisons) compared to ReFT's 5–8% gains, demonstrating value of on-policy sampling and negative reward guidance.
- Small model scaling (Galactica-125M, Codegen-350M) shows consistent ReFT gains (6–8 points), indicating technique generalizes across model scales (Table 5).
- Reward hacking on MathQA MCQ (negative results resolved via numeric variant, Table 3): ReFT suffers when answer extraction is decoupled from reasoning correctness; numeric variants restore 3–5% gains.

## Relevance to the project

ReFT epitomizes single-sample fine-tuning: it improves a model on the exact training questions using only answer labels, no external reward models, and no data augmentation. The method learns from the same 7.5K training examples as SFT, yet PPO's on-policy sampling and advantage-weighted updates effectively extract richer learning signal. This directly addresses the thesis that RL from sparse, task-inherent labels (correctness) is more sample-efficient than SFT repetition. Partial rewards (0.1 for numeric answers) add nuance for sparse-reward domains.

Limitation: ReFT requires clear, extractable answers and fails in ambiguous settings (e.g., MCQ where reasoning and answer selection decouple). Generalization to open-ended generation without numeric/verifiable outcomes unclear. Dependency on ground-truth answers (not reasoning steps) limits applicability to process-based fine-tuning.

## Source

- arXiv: 2401.08967
- Raw markdown: `../../../raw/research/adjacent-reward-signals/02-reft-trung.md`
- Raw PDF: `../../../raw/research/adjacent-reward-signals/pdfs/reft-trung.pdf`

## Related

- [[1-shot-rlvr]] — RL from outcome rewards on single problem
- [[critique-ft-one-problem]] — single-example critique and fine-tuning
- [[data-efficiency-rft]] — rejection fine-tuning and sample efficiency
- [[deepseek-r1]] — scaling RL with process rewards and outcome optimization
- [[rlvr-incentivizes-reasoning]] — PPO for reasoning task improvements
- [[../process-reward-models/lets-verify-step-by-step]] — process models vs. outcome only
- [[../self-improvement/_overview]] — multi-stage RL training
