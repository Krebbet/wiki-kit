# Single-sample RL fine-tuning

This cluster centers on the surprising finding that reinforcement learning with verifiable rewards (RLVR) on **one** training example can match the reasoning gains of full-set RLVR on capable base LLMs — and on the contemporaneous theoretical and methodological work that makes the result intelligible. The papers collectively argue that, given a strong base model, post-training is largely an *amplification* of latent reasoning rather than the *installation* of new skills, and that the data axis of RL fine-tuning can be compressed dramatically when you target examples whose current-policy success rate is interior (not 0 or 1) and whose correct-CoT prior is well-formed.

For David's concept-based, single-sample fine-tuning thesis this is the closest live research vein. None of these papers explicitly frames learning as concept acquisition, but each carves out a mechanism — exploration amplification, dense critique, latent CoT prior, adaptive difficulty — that maps directly onto a concept-learning workflow.

## Papers in this theme
- [[1-shot-rlvr]] — RLVR with literally one math problem matches full-set RLVR; introduces post-saturation generalization, cross-category transfer, and the variance-based example-selection rule.
- [[critique-ft-one-problem]] — Replaces RL with critique SFT on one seed problem (100 candidate solutions × 7 teacher critiques), matching or beating 1-shot RLVR at 1/15–1/20 the compute.
- [[rlvr-incentivizes-reasoning]] — Theoretical and empirical case that GRPO truly extends the reasoning boundary; introduces CoT-Pass@K and a logic-prior theorem $\alpha > \beta$ that explains why single-shot RL works.
- [[data-efficiency-rft]] — DOTS + Rollout Replay: online adaptive-difficulty selection (target $p\!=\!0.5$) with attention-based difficulty prediction, cutting GRPO time 23–62%.
- [[deepseek-r1]] — Foundational pure-RLVR demo on DeepSeek-V3-Base: AIME pass@1 15.6 → 77.9 with no SFT; emergent self-reflection; the format reward and `<think>` scaffolding that later 1-shot work isolates.
- [[reft]] — ReFT (Luong et al., ByteDance, 2024). SFT warm-up + PPO sampling many CoT paths per problem, learning from correct *and* incorrect rollouts; +10–12% over SFT on math from the same training data, no external RM.

## Cross-cutting themes

**Amplification beats teaching.** Wang et al. (1-shot RLVR), Wen et al. (RLVR theorem), and DeepSeek-R1 converge on the same picture: reasoning is largely *latent in the base model*; post-training adjusts the probability of expressing it. The 1-shot result is the cleanest demonstration — the seed example $\pi_1$ is *easy* for the base model — and the Wen et al. theorem ($\mathbb{E}[\hat A \mid \text{CoT correct}]>0$ whenever the logic prior $\alpha>\beta$ holds) explains why even one outcome-reward signal is enough to push the policy in the right direction. The implication for concept learning: the question is not "can a single example install a concept?" but "can a single example reliably amplify a latent concept the base model already half-knows?"

**Format vs substance.** Both 1-shot RLVR and DeepSeek-R1 find that the `<think>` template / format reward alone delivers a large fraction of the apparent gain (Qwen2.5-Math-1.5B: 36.0 → 65.0 on MATH500 with format reward only; 1-shot RLVR pushes that to 73.6 — an 8.6-point genuine non-format delta). Wen et al.'s CoT-Pass@K and Wang et al.'s critique-of-critique design are two different responses to this: measure CoT correctness, or train on CoT critique. Any single-sample method needs an explicit story for how it separates the two.

**Diversity and exploration are load-bearing.** 1-shot RLVR shows entropy loss is essential for post-saturation generalization; DOTS explicitly targets $p=0.5$ to maximize gradient variance; CFT injects diversity by sampling 10 candidate generators. Across all four methodological papers, the *one* sample is paired with mechanisms that prevent collapse to a degenerate trajectory — entropy bonus, candidate-mix, replay buffer, or critique noise. A naive single-sample SFT does not work; a single-sample method *with structured exploration* does.

**Disagreement on whether RL adds new capability.** The Yue et al. claim (cited throughout) that RLVR only re-weights base distributions has not been retracted. Wen et al. argue it does extend the boundary once you measure CoT correctness; the 1-shot RLVR paper sits closer to "amplification" without resolving the question. CFT sidesteps it: even if RLVR is just amplification, dense critique SFT achieves the same amplification more cheaply.

## Method comparison table

| Paper | Method | Sample cost | Concept-learning evidence | Notes |
|---|---|---|---|---|
| 1-shot RLVR (Wang et al.) | GRPO/PPO with single duplicated example | 1 prompt, ~1.4k steps before overfit | Cross-category transfer (Geometry → Algebra/NT); ARC gains from math-only training | Variance-based seed selection; entropy loss critical |
| Critique-FT-one-problem (Wang et al.) | SFT on (problem, candidate) → critique | 1 problem × 100 solutions × 7 critiques = 600 rows | Cross-domain (math → BBEH logic +16%); seed-difficulty matters (medium > easy/hard) | ~5 GPU-hr vs >120 for 1-shot RLVR |
| RLVR-incentivizes-reasoning (Wen et al.) | DAPO recipe + CoT-Pass@K analysis | 17k math problems (full RLVR) | Implicit: theorem says single steps move $p_c$ in the right direction | Logic prior $\alpha-\beta$ as concept-prior diagnostic |
| Data-efficiency RFT (Sun et al.) | DOTS (target $p\!=\!0.5$) + Rollout Replay | Full pool, but 23–62% less wall-clock | None directly; relevant as concept-difficulty scorer | Attention-over-reference cheap difficulty proxy |
| DeepSeek-R1 (DeepSeek-AI) | Pure GRPO + format reward; multi-stage R1 | ~320k prompt-rollouts (R1-Zero) | Emergent self-reflection from outcome-only RL on strong base | The reference experiment; defines the regime |

## Open questions

- What is the *minimum* concept-prior $\alpha-\beta$ a base model must have for single-sample RL to succeed? No paper measures this directly; David could.
- 1-shot RLVR's seed selection by historical variance vs CFT's medium-difficulty rule vs DOTS's $p\!=\!0.5$ — are these the same criterion under different names? The math suggests yes, but no paper unifies them.
- Does single-sample RL transfer to *non-verifiable* concepts (style, tone, soft skills)? All five papers rely on verifiable math/code outcome rewards.
- How much of the gain is genuinely cross-concept generalization vs. format/template learning? The 8.6-point non-format delta in 1-shot RLVR is the only clean number on this; needs replication on other domains.
- Does the single-example regime hold for *small* models (1–7B trained from scratch, without DeepSeek/Qwen-scale pre-training)? Existing results all ride on strong, math-pretrained backbones.

## Source
See individual paper pages.

## Related
- [[../rlvr-mechanics/_overview]]
- [[../process-reward-models/_overview]]
- [[../self-improvement/_overview]]
- [[../critique-self-correction/_overview]]
- [[../data-efficient-survey/limited-data-ft-survey]]
