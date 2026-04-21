# Self-Improvement, Self-Play, Synthetic-Data Fine-Tuning

Methods that make a model train on data it generated itself, optionally curated by itself, optionally over many iterations. The unifying question: **where does the supervision actually come from when there is no external teacher?**

## Papers in this theme
- [[star]] — STaR (Zelikman et al., 2022). Iterated rationale generation + answer-conditioned rationalization, fine-tuned on rationales whose final answer matches ground truth.
- [[self-rewarding-lm]] — Self-Rewarding LMs (Yuan et al., 2024). LLM-as-a-Judge replaces the frozen RM; Iterative DPO improves both generation and judging ability.
- [[rstar-math]] — rStar-Math (Guan, Zhang et al., 2025). MCTS rollouts + code-execution filter + step-level Process Preference Model, evolved over four rounds; small models beat o1-preview on competition math.
- [[multi-turn-policy-verifier]] — PAG (Jiang et al., Tsinghua / ByteDance Seed, 2025). Single LLM alternates policy and verifier roles in multi-turn RL; selective revision avoids collapse; 65.2% MATH500 at 1.5B; verifier outperforms majority voting on RewardBench.

## Cross-cutting synthesis

**Where the supervision comes from.** All three methods are *bootstraps*: they start from a non-trivial base capability and convert cheap signals into expensive-looking training data.

| Mechanism | STaR | Self-Rewarding LM | rStar-Math |
|---|---|---|---|
| Verifier | gold answer match | LLM-as-a-Judge (self) | code execution + gold answer + PPM |
| Variability source | temperature + answer-conditioned rationalization | temperature on response *and* judge | MCTS branching + multiple rollouts |
| Curation signal | 0/1 answer correct | scalar 1–5 rubric | per-step Q-value + preference pairs |
| Training objective | SFT on filtered rationales | DPO on preference pairs | SFT on top-Q trajectories + Bradley-Terry on step pairs |
| Iterations reported | until plateau (~16-46) | 3 | 4 |
| Base scale | GPT-J 6B | Llama 2 70B | Qwen2.5-Math 1.5B / 7B, Phi3 3.8B |
| Domain reach | math, CQA, arithmetic | open-ended instruction following | competition math only |

**Rejection sampling is the common substrate.** STaR rejects on answer match. Self-Rewarding LMs reject implicitly via judge-score ranking (top vs bottom). rStar-Math rejects at *two* granularities: per-step (code executes? PPM preference) and per-trajectory (correct final answer?). The lesson is consistent: variability without a verifier degrades training (STaR §5 explicitly warns that high-temperature sampling alone is counterproductive because correct answers via wrong reasoning poison the signal).

**Self-rewarding loops.** Two failure modes recur: (i) saturation when the verifier hits the ceiling of the policy, and (ii) reward hacking when judge and policy share parameters. Self-Rewarding LMs sidesteps (i) for three iterations by training the judge to improve in lockstep; rStar-Math sidesteps (ii) by grounding the verifier in code execution + gold answers, not just self-judgement.

**Self-play scaling.** rStar-Math is the only paper here that does true tree-search self-play; STaR is closer to expert-iteration (Anthony et al. 2017) with a fixed expert; Self-Rewarding LMs is iterative DPO with a learned, co-evolving judge. The ordering by sample-efficiency-per-FLOP appears to be rStar-Math > STaR > Self-Rewarding LMs, but this trades off against generality (rStar-Math only does math; Self-Rewarding LMs does open-ended instruction following).

**Where the supervision actually comes from.** Stripping back: STaR depends on `(x, y)` pairs (the answer is the verifier); Self-Rewarding LMs depends on a tiny hand-curated rubric prompt plus seed instruction data; rStar-Math depends on `(x, y)` pairs, a Python interpreter, and a curriculum of progressively harder problems. None of these are "free" — they are *cheaper* substitutes for human reasoning annotations.

## Method comparison table
See the table above. Headline: each method amplifies a small seed by ~10²–10⁴ effective examples through model-generated variants, gated by a verifier whose strictness determines downstream quality.

## Open questions
- **Single-shot extreme.** None of these papers tests `|D| = 1`; STaR uses ~10 worked rationales as seed but thousands of question/answer pairs as the unsupervised pool. Can the loop close on a single concept-bearing example, or does it need a question distribution to bootstrap from?
- **Concept-level vs token-level variability.** All three vary at the token level. Concept-based learning may need *concept-level* perturbation operators that the verifier can still score.
- **Verifier provenance.** Code execution (rStar-Math) is the only fully external verifier. Self-judges saturate / hack; gold-answer verifiers exclude domains without crisp answers. What's the equivalent for "concept correctness"?
- **Saturation dynamics.** All three plateau within a handful of rounds. Why? Distribution shift in the seed pool, or fundamental ceiling of policy ⊕ verifier?
- **Length / style hacking.** Self-Rewarding LMs generations grew from 1092 → 2552 tokens; STaR rationales drifted from few-shot style without anchoring prompts. Self-improvement loops appear to bias toward verbosity.

## Source

See individual paper pages: [[star]], [[self-rewarding-lm]], [[rstar-math]], [[multi-turn-policy-verifier]].

## Related themes
- [[../single-sample-rl-finetuning/_overview]] — RL on a single problem (RLOOE, 1-shot RLVR); shares the "amplify one example" goal but uses RL rather than supervised self-distillation.
- [[../critique-self-correction/_overview]] — Self-Refine, Reflexion, Constitutional AI; same self-judge primitive used at inference rather than training time.
- [[../process-reward-models/_overview]] — Lightman et al., Math-Shepherd, Uesato; the verifier side of the rStar-Math equation, used externally rather than self-trained.
