# RLVR Implicitly Incentivizes Correct Reasoning in Base LLMs

Wen et al. (2025) push back on the Yue et al. claim that RLVR only re-weights base-model trajectories. Using a CoT-correctness-aware metric (CoT-Pass@K) verified by a separate LLM judge, they show RLVR truly *extends* the reasoning boundary on AIME 2024/2025 and on competitive-coding tasks. They also give a clean GRPO theorem: as long as a base model has a correct-CoT advantage prior ($\alpha > \beta$), GRPO with answer-only rewards monotonically increases the probability of generating correct reasoning chains.

## Method
- New metric **CoT-Pass@K**: a sample counts as correct only if both final answer *and* intermediate CoT pass an LLM judge (DeepSeek-R1-0528-Qwen3-8B), with any/all/majority voting strategies.
- Theoretical setup: factor each response into CoT $c_i$ and answer $a_i$, with verifiable reward $R(y_i)=\mathcal{I}_{\text{Ans}}(a_i)$. Define logic prior $P(\text{Ans}=1\mid \text{CoT}=1)=\alpha > \beta = P(\text{Ans}=1\mid \text{CoT}=0)$.
- **Theorem 1 (informal):** Under the prior assumption and standard GRPO advantage $\hat{A}(y_i) = (R(y_i) - \mu_Y)/\sigma_Y$, $\mathbb{E}[\hat{A}\mid \text{CoT correct}] > 0$ and $\mathbb{E}[\hat{A}\mid \text{CoT incorrect}] < 0$, so the GRPO update monotonically increases $p_c^\theta = P(\text{correct CoT})$.
- Reproduced DAPO recipe on Qwen2.5-32B and tracked per-prompt $P(CA)$, $P(CC|CA)$ across training.
- Quality-of-CoT proxy: SFT a fresh base model on rollouts from each RLVR checkpoint and measure resulting Pass@1.

## Claims
- On AIME 2024/2025 the CoT-Pass@K curves of DAPO-Qwen-32B stay above the Qwen2.5-32B base for all $K$ up to 1024 — a persistent boundary expansion that vanilla Pass@K hides because the base model often guesses the (small integer) AIME answers via wrong CoTs (Fig. 2).
- Code (LiveCodeBench v1–v6): AceReason-Nemotron-7B retains a Pass@K gap over R1-Distill-Qwen-7B at large K (Fig. 3).
- Training dynamics: $P(CC|CA)$ rises throughout DAPO training and CoT-Pass@K on AIME generalizes from very early steps (Fig. 4, Fig. 5).
- SFT on RLVR-checkpoint CoTs reaches near-DAPO Pass@1 — i.e. the upgraded reasoning *can* be re-distilled (Fig. 6).
- Failure mode: when the logic prior fails (base model has wrong knowledge that still yields correct answers), GRPO can reinforce bad CoTs — proposed root cause of R1-Zero's readability/multilingual issues.

## Sample efficiency
Not a single-sample paper, but it explains *why* very small RLVR datasets (including 1-shot) can move the needle: each gradient step's expected sign is determined by a base-model prior that already strongly differentiates correct vs incorrect reasoning. A handful of well-formed verifiable problems is enough to engage that prior; the data-hungry work is implicitly done by pre-training.

## Relevance to the project
Provides the theoretical scaffolding that makes single-sample RL plausible. For David: (1) the $\alpha-\beta$ gap is the formal currency of "concept already understood, just under-expressed" — a target metric for diagnosing whether a base model can learn a concept from one example; (2) the failure mode (high $\beta$) is a clean test for when single-shot training will *backfire* and reinforce confident wrongness; (3) CoT-Pass@K is a direct evaluation tool for concept-level generalization, more honest than answer-only Pass@K, and cheap to compute via an LLM judge.

## Source
- arXiv: 2506.14245
- Raw markdown: `../../../raw/research/single-sample-llm-learning/03-03-rlvr-incentivizes-reasoning.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/03-rlvr-incentivizes-reasoning.pdf`

## Related
- [[1-shot-rlvr]]
- [[deepseek-r1]]
- [[../rlvr-mechanics/_overview]]
- [[../process-reward-models/_overview]]
