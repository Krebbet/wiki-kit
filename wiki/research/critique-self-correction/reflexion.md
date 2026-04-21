# Reflexion: Language Agents with Verbal Reinforcement Learning

Shinn et al., 2023. "Verbal RL": instead of updating weights, the agent stores natural-language self-reflections in an episodic memory buffer that is prepended in subsequent trials. Modular triple (Actor / Evaluator / Self-Reflection) lets sparse environment rewards be amplified into specific textual lessons. Achieves 91% pass@1 on HumanEval (vs 80% GPT-4 baseline), +22% on AlfWorld, +20% on HotPotQA.

## Method
- Three LLMs (often the same base): **Actor** `M_a` (policy), **Evaluator** `M_e` (scores trajectories), **Self-Reflection** `M_sr` (turns scalar reward + trajectory into verbal summary).
- Loop: trial `t` produces trajectory `τ_t`; evaluator gives scalar `r_t = M_e(τ_t)`; self-reflection emits `sr_t = M_sr(τ_t, r_t, mem)`; `sr_t` appended to `mem`. `mem` is bounded (Ω = 1–3 entries) to fit context.
- **Evaluator instantiations** per task:
  - Reasoning (HotPotQA): exact-match against gold answer.
  - Decision-making (AlfWorld): hand-written heuristic (loop detection / step budget) + LLM binary classifier.
  - Programming (HumanEval, MBPP, LeetcodeHard): self-generated unit-test suite (CoT-prompted, AST-validated, sample n ≤ 6 tests). Note: avoiding ground-truth tests preserves pass@1 eligibility.
- Self-reflection acts as a "semantic gradient": converts binary success into actionable verbal lesson (which action `a_i` was wrong, what `a'_i` would have done).

## Claims
- Programming (Table 1): HumanEval Python 80.1 → **91.0**; HumanEval Rust 60.0 → 68.0; MBPP Rust 70.9 → 75.4; LeetcodeHard Python 7.5 → 15.0. MBPP Python *underperforms* base (80.1 → 77.1) due to high false-positive rate (16.3%) of self-generated tests vs HumanEval's 1.4% (Table 2).
- AlfWorld: 130/134 tasks solved over 12 trials; ReAct baseline plateaus, hallucination rate stuck at 22%.
- HotPotQA: +20% over baselines; +14% even on CoT(GT) which already has gold context. Self-reflection ablation (Fig. 4c): adds +8% absolute over episodic-memory-only baseline.
- Table 3 ablation (HumanEval Rust 50 hardest): self-reflection without test generation = 0.52 (worse than 0.60 base — agent can't tell when to stop and over-edits); test generation without reflection = 0.60 (no improvement); both together = 0.68. Verbal lesson is the load-bearing piece.

## Sample efficiency
Reflexion exemplifies "single-shot RL without weight updates." Each task gets at most ~12 trials, each gated by a sparse binary signal that is verbally amplified. There is no fine-tuning, no preference dataset, no reward model — only the base policy plus an episodic textual memory of size 1–3. The credit-assignment substrate is the LLM's ability to read its own trajectory and synthesise where it went wrong. This is the closest analogue to single-sample concept learning in this cluster: one task instance, a handful of attempts, a verbally articulated lesson, transferred across attempts. The cost is that gains live in the prompt context (lost on session reset) rather than in weights — Reflexion is test-time learning, not parameter learning.

## Relevance to the project
Three transferable ideas. (1) **Verbal credit assignment**: a binary "did the concept apply correctly?" signal can be converted into a structured textual lesson which then conditions the next attempt — this is a substitute for dense per-step rewards when only a single example is available. (2) **Self-generated unit tests as variability + verifier**: the agent fabricates its own evaluation harness, which is exactly the structure needed to convert one concept into a battery of sub-checks. The MBPP cautionary tale (false-positive tests poison the loop) translates: bad self-generated checks are worse than no checks. (3) **Bounded episodic memory** as an alternative to gradient-based weight updates — relevant if the goal is to learn from one example without overfitting it: the lesson is constrained to ~1–3 textual entries rather than absorbed into the weights. For weight-based fine-tuning, Reflexion's verbal traces could serve as auxiliary supervision per single example (one example → multiple verbalised attempts → SFT on the lesson, not just the answer).

## Source
- arXiv: 2303.11366
- Raw markdown: `../../../raw/research/single-sample-llm-learning/29-G-3-reflexion.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/G-3-reflexion.pdf`

## Related
- [[self-refine]]
- [[constitutional-ai]]
- [[../self-improvement/star]]
- [[../process-reward-models/_overview]]
