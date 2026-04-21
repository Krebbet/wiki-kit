# Unleashing the Reasoning Potential of Pre-trained LLMs by Critique Fine-Tuning on One Problem

Wang et al. (2025) show that *supervised* critique fine-tuning derived from a single seed problem matches or beats 1-shot RLVR with roughly 1/15–1/20 the compute. They generate ~100 candidate solutions to one problem with diverse open models, then ask 7 strong teacher LLMs to critique each, yielding ~600 (problem, candidate) -> critique training pairs. Fine-tuning on that single-problem critique set lifts Qwen2.5-Math-7B by +14.9% on average across six math benchmarks and +16% on three BBEH logic subtasks.

## Method
- Pick one seed problem from DeepScaleR (the same $\pi_1$, $\pi_2$, $\pi_{13}$, $\pi_{1209}$ slots used in 1-shot RLVR).
- Generate 100 candidate solutions via 10 generators (Qwen2.5-Math-7B-Instruct, Qwen3-4B/8B/14B/32B, MiMo-7B-SFT/RL, R1-Distill-Qwen-32B, Phi-4-reasoning, Phi-4-reasoning-plus).
- Ask 7 teacher models (Claude 3.5/3.7 Sonnet, GPT-4.1/4.1-Mini, GPT-4o, o1, o3-Mini) to critique each candidate. Filter for consistency, keep 600 (x, y) -> c examples.
- Standard SFT on input = (problem $x$, candidate $y$) → output = critique $c$. Full-parameter tuning, lr 5e-6, cosine schedule, batch 512.

## Claims
- Qwen2.5-Math-7B: base 27.3% → CFT-1ex 42.2% (avg over 6 math benchmarks); on Minerva 17.3% → 40.4% (+23.1), OlympiadBench 17.5% → 39.3% (+21.8) (Tab. 2).
- CFT (1 ex) 42.2% beats RLVR (1 ex) 40.2% on Qwen2.5-Math-7B; comparable or better on Llama-3.2-3B-Instruct (+2.1) and Qwen2.5-14B; slightly under on Qwen2.5-Math-1.5B (32.8 vs 33.8) (Tab. 2).
- Compute: ~5 GPU-hours to surpass 75% on MATH-500 vs >120 GPU-hours for 1-shot RLVR (Fig. 4).
- Gains generalize cross-domain: +16% average on three BBEH logic subtasks (Causal Understanding, DisambiguationQA, Time Arithmetic) (Fig. 1).
- Seed robustness (Tab. 3): all four seeds work; medium-difficulty seed ($\pi_1$, model scoring 49/100 on it) gives the strongest learning signal (42.2 vs 36.3 for the very-hard $\pi_{1209}$).
- Generator diversity matters (Tab. 4): mixing 10 generators (42.2) beats either Phi-4-Reasoning-Plus alone (38.7) or Qwen2.5-Math-7B-Instruct alone (37.6).

## Sample efficiency
The training problem count is literally one. Diversity is injected on the *solution* side (100 attempts × 7 critiques) so the 600-row dataset spans many failure modes for a single concept. This reframes "single sample" as "single problem, many candidate trajectories, dense corrective signal" — closer to teaching the model to *evaluate* one concept than to solve it. Stable SFT loss (vs unstable RL) makes runs reproducible and cheap.

## Relevance to the project
Direct evidence that a *single concept* — when surrounded by many wrong ways to engage with it and explicit critique — is enough to reshape model reasoning, including out-of-domain. For David's concept-learning design, this validates the idea that the unit of learning can be a problem-as-concept rather than a corpus, and suggests two design knobs: (a) deliberate diversity over solution attempts (multiple students) and (b) high-quality, structured negative-feedback signal (multiple judges) rather than just an answer key. The seed-difficulty result (medium >> easy or hard) is a concrete recipe constraint.

## Source
- arXiv: 2506.03295
- Raw markdown: `../../../raw/research/single-sample-llm-learning/02-02-critique-ft-one-problem.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/02-critique-ft-one-problem.pdf`

## Related
- [[1-shot-rlvr]]
- [[rlvr-incentivizes-reasoning]]
- [[../critique-self-correction/_overview]]
- [[../process-reward-models/_overview]]
