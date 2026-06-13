# Magistral — Mistral's Pure-RL Reasoning Model

Mistral AI's first dedicated reasoning model, trained with pure GRPO-based RL (no distillation from external reasoning models), achieving 73.6% pass@1 on AIME'24 from a 26.8% base — a ~175% absolute improvement — while preserving multimodal, instruction-following, and function-calling capabilities.

## Method

**Algorithm: Modified GRPO**

Magistral uses GRPO with five targeted modifications:

1. **No KL divergence term.** Eliminates the reference model copy, reducing memory and compute overhead.
2. **Loss normalization across groups.** Token-wise losses are summed across all tokens and all generations in a batch, then divided by total token count (not per-sequence), avoiding length-bias.
3. **Two-stage advantage normalization.** Group-level: Â_i = r_i − μ. Minibatch-level: Â_i^norm = (Â_i − Â^mean) / Â^std. Zero-advantage groups are filtered.
4. **Clip-Higher strategy.** Asymmetric clipping: ε_low (standard), ε_high = 0.26–0.28 (relaxed). Allows exploration of rare reasoning steps; entropy-bonus approaches were tried and found unstable (math-only: entropy collapsed; mixed: exploded). Clip-Higher from [[dapo]] adopted here.
5. **Filtered non-diverse groups.** Groups where all rollouts share the same reward are dropped.

**Reward Design (four components):**

- Formatting (0.1): requires exactly one `<think>...</think>` block, `\boxed{}` for math, language-tagged code blocks.
- Correctness (0.9): math via SymPy normalization; code via execution against 20 randomly-selected test cases (C++: 10s compile / 4s exec; Python: 4s exec). Binary; partial credit (proportional test-pass) was trialed and yielded −2% LCB — discarded.
- Length penalty: linear ramp 0 → −0.1 over l_cache tokens before l_max; −0.1 flat above l_max.
- Language consistency (0.1): fastText classifier validates problem, `<think>` block, and final answer share the same language. Applied to 10% of training data translated into FR/ES/IT/DE/ZH/RU.

**Staged difficulty curriculum (Magistral Medium):** three hyperparameter stages progressively increasing dataset difficulty, max completion length (16k → 24k → 32k tokens), and batch size (8k → 4k → 2k sequences).

**Data:** 38k math problems (filtered from 699k via two-stage difficulty scoring) and 35k code problems (filtered + auto-generated test cases; duplicated for Python and C++).

**Infrastructure:** Three asynchronous worker pools — Trainers, Generators (rollouts), Verifiers (reward) — operate concurrently. Mid-flight weight updates via NCCL GPU-to-GPU broadcast (<5s). Sequences packed by descending length (19% padding reduction). Stability constraint: n_async / n_batch ≤ 2, n_batch ≥ 1024.

**Magistral Small (24B):** Cold-start SFT from Magistral Medium's own outputs, then RL. The only cold-start data is from Mistral's own model; no external reasoning model distillation.

## Results

**Magistral Medium (pure RL from Mistral Medium 3):**
- AIME'24 pass@1: 26.8 → 73.6 (vs. DeepSeek-R1 79.8)
- AIME'24 maj@64: 43.4 → 90.0
- AIME'25 pass@1: 21.2 → 64.9 (vs. DeepSeek-R1 70.0)
- AIME'25 maj@64: 30.0 → 83.3
- MATH-500: 91.0 → 94.3 (vs. DeepSeek-R1 97.3)
- GPQA: 59.6 → 70.8 (vs. DeepSeek-R1 71.5)
- LiveCodeBench v5: 29.1 → 59.4 (vs. DeepSeek-R1 65.9)
- Humanity's Last Exam: 4.4 → 9.0 (vs. DeepSeek-R1 8.6 — Magistral exceeds R1 here)

**Magistral Small 24B (SFT + RL):**
- AIME'24 pass@1: 70.7 (SFT+RL); SFT-only 65.4; RL-only 65.8
- AIME'24 maj@64: 90.0 (SFT-only) / 86.7 (RL-only) / 83.3 (SFT+RL)
- MATH-500: 95.9 (SFT+RL)
- GPQA: 68.2 (SFT+RL)

**Cross-domain transfer ablation (24B model):**
- Math-only RL: AIME'24 +30.3, LiveCodeBench +15.6 (strong out-of-domain transfer to code)
- Code-only RL: AIME'24 +17.5, LiveCodeBench +20.0

**RL on text improves vision (unexpected):**
- MMMU: +5% → 70%
- MMMU-Pro-Standard: +4.4% → 57.9%
- MMMU-Pro-Vision: +12% → 52.1%

**Multilingual (AIME'24 pass@1):** EN 73.6 | FR 68.5 | ES 69.3 | DE 66.8 | ZH 63.7 | RU 65.0. ~5–10% degradation vs English despite language-consistency reward.

## Applicability

Binary correctness reward is critical — partial credit (proportional pass-rate) was counterproductive. Compute: staged training at 16k–32k context with async multi-GPU infrastructure; not suitable for single-GPU fine-tuning at this scale. RL on text does not degrade multimodal capability — safe to apply without a vision-specific RL stage. Pure RL works at medium scale; 24B models benefit from cold-start SFT from a stronger RL-trained model.

## Novelty

End-to-end RL reasoning without distillation from external reasoning models. Key new elements: language-consistency reward with fastText validation, async three-pool infrastructure with mid-flight NCCL weight updates, Clip-Higher validated as more reliable than entropy-bonus for entropy stability. The unexpected +12% MMMU-Pro-Vision gain from text-only RL is a notable generalization result.

Builds on: GRPO (Shao et al., 2024), Clip-Higher from [[dapo]], staged curriculum pattern from DeepSeek-R1.

## Reproducibility

- arXiv: 2506.10910 (cs.CL, 2025-06-12)
- Magistral Small weights: https://huggingface.co/mistralai/Magistral-Small-2506 (Apache 2.0)
- Magistral Medium: API-only via Mistral (weights not released)
- Training code and datasets: not released

## Source

- raw/research/weekly-2026-06-13/01-magistral.md
- arXiv: https://arxiv.org/abs/2506.10910

## Related

- [[spurious-rewards-rlvr]] — Magistral's pure GRPO; clipping-bias amplification mechanism may partly explain gains
- [[rlvr-incentivizes-reasoning]] — Theorem 1 (GRPO monotonically increases correct CoT probability) provides theoretical backing
- [[conflicts/sparse-policy-selection-vs-gradient-cancellation]] — large-scale applied data point for the RL-for-reasoning debate; pure-RL-without-distillation succeeds
- [[high-entropy-tokens-rlvr]] — Clip-Higher in Magistral targets exploration at rare/high-entropy steps; connects to entropy-focused intervention literature
- [[anti-self-distillation]] — Magistral's no-external-distillation approach is the applied complement to AntiSD's theoretical case against KL-descent self-distillation on deliberation tokens
- [[rlsd-self-distilled-rlvr]] — RLSD argues for on-policy self-distillation; Magistral Medium's pure-RL is the contrasting data point
- [[polar-rl-harness]] — comparable async decoupled-rollout RL infrastructure design
