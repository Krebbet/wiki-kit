# Spurious Rewards: Rethinking Training Signals in RLVR

GRPO training with random or negatively-correlated rewards still yields large MATH-500 gains (+21.4 pp for Qwen2.5-Math-7B vs. +29.1 from real rewards), suggesting the improvement comes from a clipping bias in GRPO that amplifies high-prior pretrained behaviors rather than from learning the reward signal.

## Source

- `raw/research/weekly-2026-06-03/03-spurious-rewards-rlvr.md` (arXiv:2506.10947, June 2025)

## Method

The authors train Qwen2.5-Math-7B and other model families (Llama3, OLMo2) with GRPO under three reward conditions:
- **Ground-truth rewards** (standard RLVR)
- **Randomly assigned rewards** (no correlation with correctness)
- **Negatively-correlated rewards** (reward wrong answers, penalize correct ones)

They then analyze GRPO's PPO-style clip term, showing it introduces a systematic bias: the clipping mechanism preferentially amplifies behaviors already present in the model's pretrained distribution — regardless of reward label — because high-prior behaviors generate outputs that, when varied slightly, produce the cross-group variance that GRPO rewards.

**Case study**: "code reasoning" (expressing reasoning in code syntax without execution) is a high-prior behavior in Qwen2.5-Math models. Its frequency rises from 65% to >90% under spurious rewards — not because code reasoning is rewarded, but because GRPO's clipping amplifies it from the pretrained base.

## Results

- Ground-truth GRPO on Qwen2.5-Math-7B: **+29.1 pp** MATH-500.
- Random reward GRPO on Qwen2.5-Math-7B: **+21.4 pp** MATH-500 (73% of real-reward gain, from noise).
- Code-reasoning frequency: 65% → >90% under spurious rewards.
- **Model-dependent**: the effect fails for Llama3 and OLMo2, which lack the same amplifiable pretrained behaviors. Gain requires a model with a strong high-prior behavior that GRPO can surface.

## Novelty

Demonstrates for the first time that a significant fraction of RLVR gains on math benchmarks is attributable to a clipping artifact rather than reward-signal learning. Introduces "amplifiable pretrained behaviors" as a distinct causal mechanism. Warns that benchmark improvements on Qwen-family models may not reflect genuine capability acquisition — and may not generalize across model families.

Methodologically, this is the strongest evidence that RLVR gains can be decoupled from reward correctness, setting a floor on how much of any RLVR result is mechanistically meaningful.

## Conflict: Position D in the RLVR mechanistic debate

This paper adds a fourth position to [[conflicts/sparse-policy-selection-vs-gradient-cancellation]]:

- **Position A** ([[reasonmaxxer]]): RL is sparse policy selection at high-entropy positions; reward signal is real but narrow.
- **Position B** ([[token-gradient-cancellation]]): gradient cancellation across shared tokens is the bottleneck; the fix is structural (DFPO).
- **Position C** ([[delta-token-credit]]): most tokens are net-negative for learning; discriminative contrast reweighting is the fix.
- **Position D (this paper)**: reward signal can be random or inverted and large gains still occur; GRPO's clipping bias amplifies pretrained behaviors regardless of reward quality.

**Direct mechanistic conflict with Position A**: Position A (ReasonMaxxer) requires that RL is selecting from a meaningful policy signal at high-entropy positions. Position D says the signal can be noise and gains still appear — which undermines the "RL is discovering genuinely better policy choices" framing at its foundation.

**Direct mechanistic conflict with Position B**: Position B (DFPO) requires that gradient cancellation across shared tokens is the limiting factor. If reward content is irrelevant to GRPO's outcome, then fixing cancellation is also not the primary driver.

## Caveat

Position D is **model-family-dependent**. The effect requires a base model with amplifiable high-prior behaviors (Qwen2.5-Math has them; Llama3/OLMo2 do not). This limits how broadly the clipping-bias account applies — it may explain Qwen-family RLVR results without invalidating RLVR gains in model families where spurious rewards produce no gain.

## Related

- [[conflicts/sparse-policy-selection-vs-gradient-cancellation]] — position D in the four-way mechanistic debate about why RLVR works
- [[reasonmaxxer]] — position A; most directly contradicted by this paper's spurious-reward result
- [[token-gradient-cancellation]] — position B; clipping-bias account competes with gradient-exchangeability account
- [[delta-token-credit]] — position C; per-token discriminative contrast
- [[high-entropy-tokens-rlvr]] — position A extension with training-time intervention; the entropy-masking gains assumed real reward signal, which this paper puts in question
- [[scalelogic]] — "what you train on dominates how much"; if reward content is partial noise, the dominance claim weakens
