# DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning

DeepSeek-AI (2025) demonstrates that pure RL with verifiable rewards on a strong base model (DeepSeek-V3-Base, 671B MoE) can elicit long-chain-of-thought reasoning *without* any supervised fine-tuning cold start. The R1-Zero variant shows RLVR alone driving AIME 2024 pass@1 from 15.6% → 77.9% (cons@16: 86.7%) and exhibiting an emergent "aha moment" of self-reflection. The full R1 pipeline adds cold-start SFT, two RL stages, and rejection sampling to fix readability and language-mixing issues.

## Method
- **R1-Zero:** GRPO directly on DeepSeek-V3-Base. Reward = rule-based accuracy + format reward (`<think>...</think><answer>...</answer>`); no neural reward model. Hyper-params: lr 3e-6, KL coeff 0.001, sampling temp 1.0, 16 rollouts per prompt, max length 32k → 64k after step 8.2k, batch 32 questions × 16 = 512, 10,400 total steps.
- **R1 pipeline (Fig. 2):** (1) cold-start SFT on a few thousand conversational long-CoT examples; (2) first RL stage with language-consistency reward to fix language mixing; (3) rejection sampling + SFT mixing reasoning and non-reasoning data; (4) second RL stage combining rule-based reasoning rewards, model-based helpfulness/safety rewards, and language reward; preference reward only in the last 400 of 1700 steps to avoid reward hacking.
- **Distillation:** smaller dense models (Qwen, Llama) supervised on R1-generated reasoning traces.

## Claims
- DeepSeek-R1-Zero: AIME 2024 pass@1 15.6% → 77.9% during pure RL; cons@16 86.7%; MATH-500 pass@1 95.9% (Fig. 1, Tab. 3).
- DeepSeek-R1 final: MMLU 90.8, MMLU-Pro 84.0, AIME 2024 79.8, MATH-500 97.3, Codeforces percentile 96.3 (rating 2029), LiveCodeBench 65.9, SWE-Verified 49.2 (Tab. 3).
- Emergent behaviors during R1-Zero RL: response length grows monotonically (Fig. 1b); explicit self-reflection ("wait, that's an aha moment") appears spontaneously (Tab. 2).
- Distilled checkpoints (R1-Distill-Qwen-1.5B/7B/32B, R1-Distill-Llama-8B/70B) inherit much of R1's reasoning while remaining cheap to serve.
- Failure modes of R1-Zero motivating the multi-stage pipeline: poor readability and English/Chinese mixing in CoTs.

## Sample efficiency
Not single-sample: 10k steps × 32 unique questions/step ≈ 320k prompt-rollouts. But it is the *foundational existence proof* that outcome-only RL on a capable base model can grow reasoning, with no SFT bootstrap and no PRM. Every later "1-shot" or "small-data" RLVR result is essentially asking: how far can the data axis be compressed while the R1-Zero phenomenon survives?

## Relevance to the project
The reference point that frames the entire single-sample line. Three transferable observations: (1) **format reward as scaffolding** — a substantial fraction of R1-Zero's early gain is structural (the `<think>` template), echoing the format-reward baseline in 1-shot RLVR; (2) **emergent self-reflection from outcome-only signal** suggests cognitive behaviors aren't taught, they're un-suppressed — the same mechanism David is targeting at concept granularity; (3) **language/readability failure modes** show that pure outcome rewards on a strong base will reinforce whatever shortcut works, including unreadable ones, so concept-level evaluation (cf. CoT-Pass@K) needs to go beyond final-answer correctness.

## Source
- arXiv: 2501.12948
- Raw markdown: `../../../raw/research/single-sample-llm-learning/26-F-2-deepseek-r1.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/F-2-deepseek-r1.pdf`

## Related
- [[1-shot-rlvr]]
- [[rlvr-incentivizes-reasoning]]
- [[../rlvr-mechanics/deepseekmath-grpo]]
- [[../rlvr-mechanics/_overview]]
- [[../self-improvement/_overview]]
