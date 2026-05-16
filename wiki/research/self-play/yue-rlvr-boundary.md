---
name: yue-rlvr-boundary
description: Yue et al. 2025 — systematic empirical demonstration across 6 RLVR algorithms and 4 model families that RLVR improves pass@1 but is consistently surpassed by the base model at large pass@k; all algorithms cluster within ~1.3 pts while remaining 40+ pts from base-model upper bound; distillation uniquely expands the reasoning boundary.
type: research
---

# Does RLVR Really Incentivize Reasoning Capacity Beyond the Base?

Yang Yue, Zhiqi Chen, Rui Lu, Andrew Zhao, Zhaokai Wang, Yang Yue, Shiji Song, Gao Huang. LeapLab, Tsinghua University / Shanghai Jiao Tong University. arXiv:2504.13837, April 2025. Project page: https://limit-of-RLVR.github.io. Preprint; >120 citations as of mid-2025; the canonical empirical paper establishing the pass@k inversion across six RLVR algorithms.

RLVR-trained models outperform base models at pass@1 but are consistently surpassed as $k$ grows to tens or hundreds. All six tested RLVR algorithms cluster within ~1.3 points of each other and remain >40 points below the base-model sampling upper bound. Distillation — unlike RLVR — genuinely expands the reasoning boundary by introducing patterns absent from the base model's support.

## Method

**Models.** Qwen2.5-7B, 14B, 32B (base and math variants); LLaMA-3.1-8B; Qwen2.5-7B-Instruct and DeepSeek-R1-Distill-Qwen-14B (coding baseline); Qwen2.5-VL-7B (visual reasoning); Mistral-Medium-3 / Magistral-Medium (preliminary near-frontier pair).

**Six RL algorithms.** PPO, GRPO, Reinforce++, RLOO, ReMax, DAPO — all reimplemented under the VeRL framework for fair comparison. KL term removed by default following the DAPO/Oat-Zero convention; a KL-ablation is also run.

**Benchmarks.** Math: GSM8K, MATH500, Minerva, OlympiadBench, AIME24, AMC23, Omni-MATH-Rule (in/out-of-domain split). Coding: LiveCodeBench (Aug 2024–Jan 2025, 279 problems), HumanEval+, MBPP+. Visual: MathVista-TestMini, MathVision-TestMini (multiple-choice questions removed).

**pass@k methodology.** $k$ swept 1 through 256 (and up to 1024 for AIME24). Sampling temperature 0.6, top-p 0.95, max 16,384 tokens. Unbiased low-variance estimator following Chen et al. (2021). Zero-shot for base models (no few-shot prompting); correct CoTs on hard problems ($< 5\%$ average accuracy) verified manually.

## Claims

**1. The pass@k inversion (headline result).**

At small $k$ (e.g., $k = 1$): RLVR > base across all benchmarks. As $k$ grows to tens or hundreds: base catches up and surpasses RLVR. On **Minerva with Qwen2.5-32B** the base model leads RLVR by approximately **9%** at $k = 128$. On Oat-Zero/DAPO the RLVR model starts ~30% above the base at $k = 1$ but is eventually surpassed. As Omni-MATH-Rule training steps increase, pass@1 rises (26.1 → 42.5) while pass@256 progressively decreases — coverage and precision move in opposite directions.

**2. RLVR-solvable problems are a near-subset of base-solvable problems.**

AIME24 at $k = 1024$: base solves what RLVR solves (63.3%), base solves but RLVR fails (13.3%), **RLVR solves but base fails (0.0%)**, neither (23.3%). MATH500 at $k = 128$: 92.4% / 3.6% / 1.0% / 3.0%. The RLVR-solvable set is essentially a subset of the base-solvable set.

**3. All six algorithms cluster within ~1.3 pts, remain >40 pts from optimal.**

Sampling Efficiency Gap $\Delta\text{SE}$ = (RL pass@1) − (base pass@256). On Omni-MATH in-domain: GRPO 43.9, RLOO 42.6 — minor variation but all consistently >40 points. Preliminary Magistral-Medium experiments confirm the same inversion: RLVR solves ~7–8 more problems at $k = 1$ on AIME24/25 but the gap narrows with $k$.

**4. Mode-sharpening confirmed by perplexity analysis.**

$\text{PPL}_\text{Base}(\mathbf{Y}_\text{RL} \mid x)$ — perplexity of RL-generated responses under the base model — closely matches the lower tail of the base model's own perplexity distribution and decreases monotonically as RL training progresses. RLVR is mode-finding within the base model's existing support, not mode-creation.

**5. Distillation uniquely expands capacity.**

DeepSeek-R1-Distill-Qwen-7B shows pass@k curves **consistently above** both the base and the RLVR model on Minerva across all $k$ values including large $k$. Distillation introduces teacher reasoning patterns absent from the base model. Temperature-raising to match base-model entropy only partially recovers RLVR pass@k — entropy reduction is a contributing but not complete cause of coverage loss.

## Why this is load-bearing for single-sample concept learning

This is the **empirical foundation for Position A** in [[../../conflicts/invisible-leash-vs-spiral-transfer]], independent of [[invisible-leash]] but converging on the same conclusion via a different measurement lens.

The 0.0% uniquely-RLVR-solvable result on AIME24 is the sharpest quantitative statement in the corpus: no problem was solved by RLVR but not by the base at the $k = 1024$ sampling budget. This makes the leash concrete rather than theoretical.

For [[../synthesis/proposed-method]]: RLVR-style gradient updates can sharpen but cannot introduce reasoning patterns absent from the base. This forces genuine concept expansion into two channels — (a) distillation from a teacher that knows the concept, or (b) a mechanism that injects a new prior (reference-in-context, curriculum scaffolding that builds prerequisite sub-skills before the target). The curriculum-as-escape-hatch framing from the Discussion section (Sec. 4.1) connects directly to [[../synthesis/concept-curriculum-method]]: curricula that build prerequisite meta-skills before hard problems may allow RLVR to lift performance from near-zero, but only by priming latent capacity that was already in the base model.

## Limitations

- **Proprietary model access.** OpenAI-o1, DeepSeek-R1-Zero at practical throughput cannot be evaluated; all conclusions are from open-source or API-accessible models.
- **Scale upper bound unclear.** Whether the inversion persists at very large compute budgets dedicated purely to RL is an open question; Magistral-Medium experiments are preliminary.
- **Math guessing caveat.** At very large $k$, a model can reach a correct answer via an incorrect CoT. Hard-problem manual inspection mitigates but does not fully eliminate this.
- **Non-math tasks start from instruction-tuned base.** Coding and visual experiments use instruction-tuned models rather than pure base models, making the zero-RL comparison less clean.
- **Rapidly evolving field.** The paper acknowledges process rewards, agentic RL, and AlphaEvolve-style high-level search as possible mitigations not yet tested.

## Source

- `../../../raw/research/self-play-quality-extraction/.ingest/02-yue-rlvr-boundary.md`
- `../../../raw/research/self-play-quality-extraction/08-02-yue-rlvr-boundary.md`
- arXiv: https://arxiv.org/abs/2504.13837

## Related

- [[invisible-leash]] — formal theoretical companion; Theorem C.1 + Cor. C.2 are the proof of what this paper measures empirically
- [[understanding-self-play]] — mechanistic companion: proposer-is-critical finding provides the mechanism behind the pass@k inversion
- [[two-stage-dynamic]] — refinement that scopes the boundary to Stage 1 and specifies Stage 2 distillation / curriculum as the escape
- [[../single-sample-rl-finetuning/rlvr-incentivizes-reasoning]] — Wen et al. (2506.14245, *later* than this paper): **direct counterpoint** — argues via CoT-Pass@K that RLVR *does* extend the reasoning boundary, contra this paper's pass@k inversion
- [[../../conflicts/invisible-leash-vs-spiral-transfer]] — this paper is a primary exhibit for Position A
- [[../synthesis/concept-curriculum-method]] — curriculum-as-escape-hatch framing connects here
- [[../synthesis/proposed-method]]
- [[_overview]]
