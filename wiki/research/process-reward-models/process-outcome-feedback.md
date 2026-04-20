# Solving Math Word Problems with Process- and Outcome-Based Feedback

Uesato et al. (DeepMind) run the first head-to-head comparison of process-supervised vs outcome-supervised training of LMs on a natural-language reasoning task (GSM8K), evaluating both *trace error rate* (any wrong reasoning step in a final-answer-correct solution) and *final-answer error rate*. Headline finding: outcome supervision and process supervision yield essentially the same final-answer error, but only process supervision (or a reward model that emulates it) achieves low trace error. Cuts final-answer error 16.8 → 12.7 and trace error 14.0 → 3.4. Surprisingly, ORMs trained only on terminal correctness end up agreeing more with PRM step-labels than with their own ORM labels — i.e., ORMs implicitly learn step-level credit assignment.

## Method
- Base: 70B Chinchilla-style pretrained LM. SFT and RL via expert iteration.
- Reward models trained as token-classifier LMs predicting correct/incorrect after each step.
  - **ORM:** every step gets the label of the full solution's final-answer correctness (Cobbe-style).
  - **PRM:** per-step human annotations of whether prefix-so-far is correct; ~10K step labels on 1560 model samples (530 problems).
- Decoding: N=96 samples per question; majority voting or RM-weighted voting.
- RL via expert iteration with three policy-improvement variants:
  - **Final-answer RL:** filter samples by final-answer correctness (STaR-style).
  - **ORM-RL:** select highest-ORM-score solution.
  - **PRM-RL:** treat each step as an episode; pick highest-PRM-score among M=96 next-step candidates.
- Selective prediction: abstain on lowest-RM-score x% of inputs.

## Claims
- Final-answer error: outcome-only ≈ process-based both without RM (23.5 vs 22.3) and with RM (16.6 vs 14.8). Outcome supervision is more label-efficient at this metric (1–4 tokens vs hundreds).
- Trace error: outcome RL inflates wrong-reasoning-correct-answer cases (12.4% Few-shot+Final-Answer-RL with ORM rerank vs 3.5% SFT+PRM rerank).
- ORM ≈ PRM emulator: ORM step predictions agree with PRM labels 85% vs only 77% with the ORM labels themselves (Fig. 4). Authors hypothesise it's easier to recognise correct steps than to internally simulate the final answer.
- Best system: SFT + ORM-RL + ORM rerank → 12.7 final-answer / 3.4 trace; SFT + PRM-RL + PRM rerank → 12.9 / 3.8 (Table 1).
- Selective prediction: abstain 30% → final-answer error 14.1 → 2.7 (5x reduction with PRM).
- OOD on MATH pre-algebra: 64.6% error — much better than GPT-3 (92.3%) but worse than Minerva (29%); supervision type doesn't change OOD trend.

## Sample efficiency
- Process-supervision data: only 1560 solutions × ~6 steps = 9856 step labels — orders of magnitude smaller than PRM800K, yet yields the lowest trace error in the paper.
- Outcome supervision is the most label-cheap (≤4 tokens/question) but loses on trace metrics.
- 70B base; expert-iteration RL is the dominant compute. Few-shot+RL converges in 5 epochs.

## Relevance to the project
The pivotal "process vs outcome" baseline that [[lets-verify-step-by-step]] and [[math-shepherd]] both build on. Three findings shape the project's reward design:
1. **Outcome reward implicitly learns step-credit when the outcome is hard to fake** — for math/reasoning, a verifier of terminal correctness still ends up grading reasoning. This may not transfer to domains with shortcut/spurious solutions, which is exactly the regime where concept-component rewards add value.
2. **Trace correctness is a separable metric** that outcome reward never optimises directly. If the project cares about *correct conceptual decomposition*, not just answer-correct outputs, process-style supervision is necessary.
3. **Reward model + RL > reward model alone** — gains compound, but only modestly on top of strong SFT initialisation; suggests the leverage point for small models is the SFT-initialised + step-level RL combo.
Note also the small-data PRM proof-of-concept (1.5K solutions): process labels do not need to be million-scale to move trace error.

## Source
- arXiv: 2211.14275
- Raw markdown: `../../../raw/research/single-sample-llm-learning/18-C-3-uesato-process-outcome-feedback.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/C-3-uesato-process-outcome-feedback.pdf`

## Related
- [[lets-verify-step-by-step]]
- [[math-shepherd]]
- [[training-verifiers-gsm8k]]
- [[_overview]]
