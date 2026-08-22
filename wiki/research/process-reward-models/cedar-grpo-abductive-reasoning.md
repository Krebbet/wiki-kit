---
name: cedar-grpo-abductive-reasoning
description: CEDAR-GRPO adds two LLM-judged trace-level process rewards (evidence coverage, evidence-to-explanation directionality) to correctness-only GRPO; abductive-reasoning gains transfer to 11 held-out tasks and unrewarded process metrics improve as a side effect, while correctness-only GRPO measurably suppresses them
type: research
---

# CEDAR-GRPO: Process-Aware Reinforcement Learning for General Abductive Reasoning in LLMs

Salimi, Parnian, Adim et al. (Sharif University / U. Tehran), arXiv:2608.14791. Vanilla GRPO (critic-free, group-relative, $G=4$) with a composite reward $R = r_{cor} + r_{cov} + r_{dir}$ layered on top of outcome correctness. Structured output `⟨think⟩β⟨/think⟩⟨answer⟩α⟨/answer⟩`. Trained on 2,400 domain-neutral abductive-reasoning instances (hypothesis-generation + hypothesis-selection tasks), evaluated zero-shot on 11 held-out tasks spanning clinical diagnosis, code debugging, long-context investigation, and non-abductive controls.

## Method

- $r_{cor} = V_d(\alpha(y), g) \in \{0,1\}$ — dataset-specific exact/set-match/execution verifier on the answer span only.
- $r_{cov} = \frac{1}{m}\sum_j z_j$ — fraction of $m$ LLM-extracted observation details from the prompt explicitly addressed in the reasoning span $\beta(y)$.
- $r_{dir} \in \{0, 0.5, 1\}$ — whether the trace reasons evidence→explanation (1), explanation-back-to-evidence (0), or mixed (0.5).

Both process rewards are scored by a fixed frozen judge (gpt-oss-120b, temp 0.0) from the prompt and $\beta(y)$ only — never from the answer $\alpha(y)$, avoiding leakage. This is **trace-level**, not step-level, credit assignment: one judged score per full reasoning span, not per token/step, computed by an LLM judge rather than a trained PRM.

## Results

Across 4 backbones (Qwen3-4B, Qwen3-8B, DeepSeek-R1-Distill-Qwen-7B, Llama-3.1-8B-Instruct) × 11 held-out tasks: CEDAR-GRPO beats both the base model (avg **+7.4 pts**) and correctness-only GRPO ("Cor-GRPO", avg **+2.7 pts**) on *every* model/task combination — max **+30.8 pts** (MuSR-Murder, DeepSeek-R1-Distill-Qwen-7B, 26.4%→57.2%).

**Process-metric side effect (the paper's strongest concept-vs-pattern evidence):** 5 of 7 tracked process metrics (Branchiness, Backtracking, Differential Elimination, Prior Invocation, Uncertainty Markers) were *never directly rewarded* yet all increase under CEDAR-GRPO — exploration of alternatives and epistemic hedging emerge as side effects of rewarding only coverage + directionality. Correctness-only GRPO *narrows* two of them (Branchiness 1.22→1.16, Prior Invocation 0.59→0.53) — optimizing for the right final answer alone measurably suppresses exploratory reasoning behavior relative to baseline, while the composite reward reverses this. Directionality itself drops under Cor-GRPO (0.21→0.16) despite improved accuracy — outcome-only RL converging on a shortcut that decouples correctness from sound reasoning structure.

## Limitations

- **Circularity risk (unresolved by the authors' own admission):** the training rewards (coverage, directionality) and the evaluation process metrics (Table 2/3) are both LLM-judged. The paper doesn't fully separate "the judge got better at scoring" from "the policy got better at abduction"; authors call for human evaluation.
- Small training pool (2,400 instances); data-scale question examined only via model-count, not data-count, ablations.
- All backbones 4–8B; scale untested.
- Evaluation is closed-form/benchmark-style; unclear how far gains extend to open-ended interactive explanation.
- Unaddressed by this pass (Appendix D.5 not read): reward-hacking screening is cited as ruling out verbosity/hedging exploits, but the observed rise in Uncertainty Markers (0.87→1.37) is exactly the kind of metric that could conflate genuine epistemic calibration with the judge simply rewarding hedging language.

## Relation to the wiki

The Cor-GRPO Directionality regression (0.21→0.16 despite rising accuracy) is a corroborating data point for [[spurious-rewards-rlvr|../rlvr-mechanics/spurious-rewards-rlvr]]'s finding that GRPO amplifies whatever behavior correlates with reward regardless of reasoning soundness — a second, independent instance of outcome-only RL producing a reasoning shortcut. Closest existing wiki pattern for the reward design itself is [[exprl-mid-training]]: both use an LLM-judge-scored dense signal computed from something never given to the policy (ExpRL: hidden reference → judge rubric; CEDAR-GRPO: prompt's observation details → judge coverage/directionality score), avoiding step-level human labels via LLM-as-judge process signal.

**Naming note:** [[../self-play/azr]] also uses "abduction," but for the code/logic-puzzle triplet mode (infer input from program+output) — a different formalization from CEDAR-GRPO's classical NLP sense (evidence→best-explanation inference). Not a substantive overlap, just a term collision worth remembering when cross-indexing.

## Source

- `raw/research/weekly-2026-08-21/03-cedar-grpo.md`

## Related

- [[../rl-optimizers/deepseekmath-grpo]] — CEDAR-GRPO's unmodified optimizer; the contribution is reward design only, not advantage/clipping/KL mechanics.
- [[lets-verify-step-by-step]] — cited direct inspiration; contrast: PRM800K is human step-labeled and step-level, CEDAR-GRPO is LLM-judged and trace-level.
- [[process-outcome-feedback]] — cited direct inspiration; Uesato's process-vs-outcome distinction is the conceptual ancestor of the Cor-GRPO vs CEDAR-GRPO comparison here.
- [[exprl-mid-training]] — closest existing wiki pattern: LLM-judge-scored dense reward from information withheld from the policy.
- [[../rlvr-mechanics/spurious-rewards-rlvr]] — parallels the Cor-GRPO shortcut-convergence finding (accuracy up, Directionality down).
- [[../self-play/azr]] — naming collision only ("abduction" used in a different formal sense), not a substantive overlap.
- [[../../weekly-briefs/2026-08-21]] — brought in by the 2026-08-21 weekly sweep
