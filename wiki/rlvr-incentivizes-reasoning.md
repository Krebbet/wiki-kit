# RLVR Implicitly Incentivizes Correct Reasoning in Base LLMs

GRPO-style RLVR provably increases the probability of generating correct chain-of-thought reasoning paths — not just re-weighting outputs toward correct answers — when the base LLM has sufficient knowledge and logic priors. Core contribution: the **CoT-Pass@K metric** and **Theorem 1**, which provide the first formal foundation for why verifiable-reward RL improves LLM reasoning. Adds Position E to [[conflicts/sparse-policy-selection-vs-gradient-cancellation]], resolving the "sampling efficiency only" empirical claim by attributing it to metric invalidity.

## Method

**CoT-Pass@K.** Pass@K conditioned on the intermediate reasoning chain being correct, not just the final answer. CoT correctness assessed using DeepSeek-R1-0528-Qwen3-8B as an LLM-as-a-CoT-Judge (3× per chain; any/majority/all-correct aggregation). Separates genuine reasoning from lucky answer guessing — systematic noise on math benchmarks where short integer answers are guessable.

**Theorem 1.** Under a "Logic Prior" assumption (correct CoTs yield correct answers with probability α, incorrect CoTs with β, α > β), the expected GRPO advantage satisfies:
- E[Â | correct CoT] = (1−p_c)(α−β)/σ > 0
- E[Â | incorrect CoT] = −p_c(α−β)/σ < 0

Therefore GRPO monotonically increases p_c (probability of generating a correct CoT). The driver is the gap α−β > 0. Failure modes arise when Logic Prior is violated (fatal knowledge errors, strong model biases) — explaining R1-Zero's readability/language-mixing issues.

**Training dynamics.** DAPO reproduced on Qwen2.5-32B (32 AMD MI300X, ~2 weeks via VERL). P(CC|CA)(q) (fraction of correct CoTs within correct answers) tracked per-prompt and increases from step 0, before P(CA)(q) saturates. Median P(CC|CA)(q) ≈ 0.70 at step 400 — non-negligible residual incorrect CoTs remain.

**SFT proxy validation.** SFT on DAPO-generated CoTs nearly matches DAPO-Qwen-32B Pass@1; SFT on base-model correct CoTs does not. Confirms RLVR generates CoT data inaccessible from the base model.

## Results

**AIME 2024/2025 (DAPO-Qwen-32B vs Qwen2.5-32B):**
- Standard Pass@K: base catches up / surpasses DAPO at moderate K (consistent with Yue et al. "sampling efficiency only").
- CoT-Pass@K: DAPO maintains a persistent gap across all K up to 1024 under all three aggregation strategies. Especially pronounced on AIME 2025 (post-cutoff, no contamination).

**Code (AceReason-Nemotron-7B vs DeepSeek-R1-Distill-Qwen-7B):** Pass@K improvement visible on medium/hard LiveCodeBench problems (v1–v6). For distilled LLMs, CoT-Pass@K shows no gap at large K — distilled models already saturate extractable math reasoning.

**Training onset:** CoT-Pass@K on AIME 2024 improves within first 20 steps (~320 gradient updates). P(CC|CA)(q) increases continuously.

## Applicability

Most effective for base LLMs with strong pre-existing knowledge and logic priors (large, well-pretrained, undistilled models). Logic Prior assumption (α → 1, β → 0) is the precondition for Theorem 1 to guarantee improvement — weaker prior states may need cold-start SFT. CoT-Pass@K is evaluation-expensive (3× LLM-judge calls per response) and requires a reliable verifier; not applicable to tasks without LLM-verifiable chains.

## Source

- arXiv: https://arxiv.org/abs/2506.14245 (Microsoft Research Asia / Peking University / CUHK / UCLA)
- Training: DAPO recipe (arXiv:2503.14476), DAPO-Math-17k dataset
- Eval: EvalHub (github.com/ysy-phoenix/evalhub)
- Venue: preprint

## Related

- [[conflicts/sparse-policy-selection-vs-gradient-cancellation]] — Position E: resolves Yue et al. empirically by metric invalidation
- [[reasonmaxxer]] — Position A in the same conflict; theoretically aligned, now with formal backing
- [[spurious-rewards-rlvr]] — Position D; Logic Prior failure mode partially validates spurious-rewards concern
- [[token-gradient-cancellation]] — Position B; CoT-level framing sidesteps token-level gradient analysis
- [[delta-token-credit]] — Position C; per-token credit assignment within CoT context
- [[high-entropy-tokens-rlvr]] — token-level forking points; possible interaction with α−β gap
- [[rlsd-self-distilled-rlvr]] — SFT-on-RLVR-CoTs experiment shows near-equivalence
- [[scalelogic]] — scaling RL for reasoning; paper argues RLVR scaling is as pivotal as pretraining scaling
