# Process Reward Models & Step-Level Supervision

Theme overview for PRM research: how to give a reward model credit signals that target *intermediate* reasoning steps rather than only final outcomes, why that helps, and how far it can be automated. Centred on math reasoning (GSM8K, MATH) where the four canonical works in this theme were developed, but the design principles extend wherever a task decomposes into steps whose individual correctness matters.

## Papers

- [[training-verifiers-gsm8k]] — Cobbe et al. 2021. Foundational ORM recipe; 6B verifier ≈ 175B finetune; introduces GSM8K and token-level value-function scoring.
- [[process-outcome-feedback]] — Uesato et al. 2022 (DeepMind). First direct process-vs-outcome comparison; outcomes match on final-answer error but only process supervision (or its emulator) achieves low *trace* error; ORMs surprisingly emulate PRMs.
- [[lets-verify-step-by-step]] — Lightman et al. 2023 (OpenAI). PRM800K; 800K human step labels on GPT-4 traces; PRM 78.2% on MATH-500; active learning 2.6x; PRM > ORM > majority at every N.
- [[math-shepherd]] — Wang et al. 2023 (PKU/DeepSeek). MCTS-rollout automatic step labels (no humans); beats PRM800K on MATH at matched generator; step-by-step PPO lifts Mistral-7B 77.9 → 84.1% GSM8K.
- [[pav-rewarding-progress]] — Setlur et al. 2024 (Google / DeepMind / CMU). PAV: process credit = step-level *advantage* under a complementary prover policy, not step correctness. >8% test-time search gain and 5–6× RL sample efficiency vs ORMs.

## Cross-cutting synthesis

### The process vs outcome reward debate
The four papers stake out a coherent trajectory:
- Cobbe (2021) shows automatic outcome verification scales remarkably well — 30x effective parameters from a single best-of-N verifier — but doesn't ask whether reasoning is correct.
- Uesato (2022) sharpens the question by separating *trace error* from *final-answer error*: the two are decoupled. Outcome supervision is label-efficient for final answers (~1–4 tokens/question); process supervision (or a learned emulator) is required for trace correctness. Critically: ORMs trained only on terminal correctness implicitly learn step-credit assignment when the task is hard to spuriously satisfy (math), agreeing with PRM step labels 85% vs 77% with their own ORM labels. *This implicit emulation may not transfer to domains with shortcut solutions* — directly relevant when the project's target domains are not auto-verifiable.
- Lightman (2023) overturns Uesato's "outcome ≈ process" final-answer-error tie by scaling everything (model, labels, dataset hardness): at 800K labels and MATH-difficulty, process supervision wins outright on final-answer error too.
- Wang (2023) closes the loop by showing the human label cost is illusory — MCTS-style auto-labels match or beat PRM800K. The 2024-onward PRM literature is downstream of this insight.

### Scaling of PRM annotation
Three regimes have been demonstrated to work, ordered by human cost:
1. **Heavy human (PRM800K):** 800K labels, GPT-4-scale. Required to settle the process-wins question on MATH but not necessary for the effect.
2. **Light human (Uesato):** ~10K labels suffice to move trace error from 14% to 3.4%.
3. **Zero human (Math-Shepherd):** N rollouts/step from a strong completer; soft estimation gives partial-credit labels that align with humans within a few percent. Cost shifts from labour to inference compute.

### Method comparison

| Paper | Reward signal | Annotation cost | RL? | Best result |
|---|---|---|---|---|
| Cobbe 2021 | Terminal correctness (token-level value head) | Auto (final-answer check) | No (rerank only) | 6B + verifier ≈ 175B SFT on GSM8K |
| Uesato 2022 | Per-step human / ORM-emulated | ~10K human step labels | Expert-iteration; ORM-RL, PRM-RL | 12.7% / 3.4% final/trace error on GSM8K |
| Lightman 2023 | Per-step human (positive/neutral/negative) | 800K labels (PRM800K) | No (rerank only) | 78.2% best-of-1860 on MATH-500 |
| Wang 2023 | Per-step auto via MCTS rollouts (HE/SE) | Zero human; N completer rollouts/step | Step-by-step PPO + rerank | 89.1% / 43.5% GSM8K / MATH (Mistral-7B) |

### Transfer to other domains
- All four works are math-only. Uesato explicitly cautions that the ORM-emulates-PRM finding may be domain-specific to the absence of spurious solutions in math.
- Math-Shepherd's MCTS-rollout label requires (a) a verifiable terminal signal and (b) a completer good enough to produce informative rollouts. Translating to non-math domains needs a substitute terminal verifier (test pass / proof check / human preference / model-judge) and an analogous notion of "potential to reach correctness."
- For the project (concept-based learning, not necessarily math): the strongest transferable claim is **step-level credit assignment is what makes the trace correct**, and this is largely independent of how step labels are generated.

## Open questions

- When does outcome supervision *fail* to implicitly emulate process supervision? Uesato hypothesises spurious-solution domains; this has not been systematically mapped.
- Does PRM-RL retain its trace-error advantage as generators are pushed past current SOTA on MATH/GSM8K, or is the gap closing?
- Math-Shepherd's HE labels have ~86% human agreement at N=4 but degrade as N grows (false positives accumulate). Is there a principled N-selection criterion?
- Iterative PRM bootstrap (re-train PRM on its own corrected rollouts) is suggested by both Lightman and Wang but neither demonstrates stable iteration. Open.
- Active learning: Lightman's 2.6x gain depends on having a "current best PRM" to surface convincing wrong solutions. How does this interact with cold-start?
- All evidence is on closed numerical-answer tasks. Free-form correctness (proofs, code, natural language argumentation) is uncharted for PRMs.
- Process labels at the *concept-component* granularity (rather than reasoning step) — does the same machinery apply when "step" is replaced by "sub-claim" or "predicate"? Directly relevant to the project.

## Source

See individual paper pages: [[lets-verify-step-by-step]], [[math-shepherd]], [[process-outcome-feedback]], [[training-verifiers-gsm8k]], [[pav-rewarding-progress]].

## Related themes

- [[../single-sample-rl-finetuning/_overview]] — companion theme; PRMs supply the dense reward signal that single-sample RL needs to be well-defined.
- [[../rlvr-mechanics/_overview]] — RL with verifiable rewards mechanics; PRMs are a richer instantiation of the verifiable-reward family.
