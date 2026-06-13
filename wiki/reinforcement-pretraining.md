# Reinforcement Pre-Training (RPT)

RPT reframes next-token prediction as an RL reasoning task with verifiable binary rewards, showing consistent power-law scaling of prediction accuracy with compute and a stronger foundation for downstream reinforcement fine-tuning than standard distilled pre-training.

## Method

RPT treats each context position x<t in a pre-training corpus as an RL episode. The policy is prompted to produce a chain-of-thought reasoning sequence c_t followed by a predicted token y_t. G=8 responses are sampled per context.

**Reward function:** Binary and verifiable. Reward = 1 if the byte sequence of the predicted token exactly matches the corresponding ground-truth prefix at valid token boundaries (cumulative byte lengths of the true tokens), else 0. The text corpus itself is the verifier — no annotated answers or separate reward model required.

**Optimization:** GRPO (same as RLVR fine-tuning), KL penalty = 0.

**Data and token filtering:** OmniMATH (4,428 competition-level math problems). Tokens filtered by entropy threshold using DeepSeek-R1-Distill-Qwen-1.5B as proxy, creating three difficulty splits: easy (entropy >0.5), medium (entropy >1.0), hard (entropy >1.5). Entropy gating ensures neither trivial (low-entropy, near-deterministic) nor uninformative (high-entropy, random) tasks.

**Training:** Base: DeepSeek-R1-Distill-Qwen-14B. LR = 1×10⁻⁶, batch size 256, max sequence length 8192, temperature 0.8, 1000 steps. Implementation: verl + vllm.

Ablations (Appendix A) tested first-token matching, dense rewards, conditional dense rewards — all comparable to prefix matching, suggesting the binary reward is robust rather than finely tuned.

## Results

**Next-token prediction accuracy (held-out):**
- Easy (>0.5): 45.11% vs baseline 41.60% (+3.51 pp)
- Medium (>1.0): 33.56% vs 29.46% (+4.10 pp)
- Hard (>1.5): 23.75% vs 20.43% (+3.32 pp)

**Downstream RL fine-tuning (Skywork-OR1 subset):**
- Baseline: 51.2% → 52.7% after RL fine-tuning
- RPT-14B: 56.3% → 58.3% after RL fine-tuning (starts ~5 pp higher before fine-tuning)

**Zero-shot general tasks:**
- SuperGPQA: RPT-14B 39.0% vs baseline 36.1%, vs R1-Distill-Qwen-32B 37.2%
- MMLU-Pro: RPT-14B 71.1% vs baseline 68.9%, vs R1-Distill-Qwen-32B 56.5%

**Scaling law fits** (P(C) = A/C^α + P*):
- Easy: α≈0.35, R²≈0.98
- Medium: α≈0.32, R²≈0.97
- Hard: α≈0.28, R²≈0.96

**Reasoning pattern analysis:** RPT-generated CoTs show 161.8% more hypothesis patterns and 26.2% more deduction patterns vs standard problem-solving traces; lower reliance on breakdown patterns.

## Applicability

Experiments at 14B scale only; scalability unconfirmed. Pre-training corpus limited to mathematical documents (OmniMATH); generalization to general web text unverified. Requires a reasoning-capable base model (R1-Distill-Qwen-14B was used; effect on standard base LMs unknown). G=8 rollout overhead per token position makes effective compute higher than equivalent CLM steps.

## Novelty

Moves RL signal to the pre-training phase itself, using the corpus as an implicit verifier — no labeled fine-tuning data required. Structural novelty: generating CoT *before* predicting each next token. First demonstration of power-law scaling for RL-based pre-training (not just CLM). The prefix-matching reward converts any text corpus into a verifiable reward signal without external annotation.

Prior RLVR (DeepSeek-R1, DAPO, etc.) applies RL *after* pre-training using domain-specific annotated answer sets. RPT is the first to apply RL at the pre-training stage itself.

## Reproducibility

- arXiv: 2506.08007 (cs.CL, 2025-06-09)
- Institutions: Microsoft Research, Peking University, Tsinghua University
- Authors: Qingxiu Dong, Li Dong, Yao Tang, Tianzhu Ye, Yutao Sun, Zhifang Sui, Furu Wei
- No code or weight release stated
- Venue: preprint

## Source

- raw/research/weekly-2026-06-13/03-reinforcement-pretraining.md
- arXiv: https://arxiv.org/abs/2506.08007

## Related

- [[spurious-rewards-rlvr]] — GRPO clipping-bias question applies; same uncertainty about whether gains are reward learning or clipping artifact; RPT uses different model family (R1-Distill-Qwen) than spurious-rewards (Qwen2.5-Math)
- [[high-entropy-tokens-rlvr]] — RPT's entropy-gated token filtering closely parallels entropy-selective gradient masking; both identify high-entropy tokens as the informative signal
- [[rlvr-incentivizes-reasoning]] — RPT extends the "RL incentivizes reasoning" claim to the pre-training stage; Theorem 1 about GRPO increasing correct CoT probability applies here
- [[scalelogic]] — both establish power-law RL scaling curves; ScaleLogic measures RL fine-tuning scaling by task expressiveness, RPT measures RL pre-training scaling by token entropy
- [[delta-token-credit]] — per-token credit assignment; RPT uses binary prefix reward per position, DelTA uses discriminative contrast; complementary mechanisms
