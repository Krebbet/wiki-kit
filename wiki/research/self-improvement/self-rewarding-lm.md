# Self-Rewarding Language Models

Yuan, Pang, Cho, Li, Sukhbaatar, Xu, Weston (Meta / NYU, 2024). Replaces the frozen reward model in RLHF/DPO with the LLM itself acting as judge via *LLM-as-a-Judge* prompting. Iterative DPO on self-generated preference pairs improves both instruction following *and* the model's reward-modeling ability across iterations, removing the human-preference bottleneck.

## Method
- Two skills bundled in a single model: instruction following and LLM-as-a-Judge scoring (additive 5-point rubric on relevance, coverage, usefulness, clarity, expertise — see Figure 2).
- Seed: small human IFT (3,200 Open Assistant prompts) + EFT (1,630 evaluation examples derived by self-generating CoT scores and keeping ones that agree with human rankings).
- Iteration loop (`M_t → M_{t+1}`):
  1. Generate new prompts via 8-shot self-instruct (using a fixed Llama 2-Chat 70B for the prompt step only).
  2. Sample `N=4` candidate responses per prompt at T=0.7.
  3. Self-score each candidate with the LLM-as-a-Judge prompt; average over 3 sampled judgments.
  4. Build preference pairs (highest vs lowest score, drop ties) and train via DPO.
- `M_2` adds 3,964 self-generated AIFT(M_1) pairs; `M_3` adds 6,942 AIFT(M_2) pairs. Base model: Llama 2 70B.

## Claims
- AlpacaEval 2.0 win rate vs GPT-4 Turbo: **9.94% (M_1) → 15.38% (M_2) → 20.44% (M_3)** — surpasses Claude 2 (17.19%), Gemini Pro (16.85%), GPT-4 0613 (15.76%) (Table 1).
- Head-to-head over IFT test set: M_3 beats SFT baseline 62.5% vs 9.8%; beats M_2 47.7% vs 12.5% (Figure 3).
- Reward-modeling ability *also* improves: pairwise accuracy 65.1% (SFT) → 78.7% (M_1, +EFT) → 80.4% (M_2) → 81.7% (M_3); Spearman 0.253 → 0.349 (Table 4).
- MT-Bench: 6.85 → 7.25 overall (Table 2). Math/code/reasoning gains are smaller (3.93 → 4.17), reflecting Open Assistant seed bias.
- NLP benchmarks held roughly flat — no alignment-tax collapse (Table 3). Generation length grows: 1092 → 1552 → 2552 tokens.

## Sample efficiency
The scarce ingredients are ~3.2k IFT prompts and ~1.6k EFT evaluations; everything else (preference data, prompts after iter 1) is bootstrapped. Per-seed amplification: for each new prompt `x_i`, the model generates `N=4` candidates and `3` independent judge passes — i.e., 12 forward calls produce one preference pair. The "auxiliary variability" comes from temperature sampling at both the response and judge stages, with the judge collapsing variance into a scalar that filters which variants enter training. Importantly, the *judge itself* improves — so later iterations not only get more data but get *better-curated* data from the same seed prompts. Open question (authors flag): saturation, length bias, and reward-hacking when the judge is the same family as the policy.

## Relevance to the project
Self-Rewarding LMs operationalise the auxiliary-variability idea at the *preference* level: a single seed prompt is recast into many candidates, then collapsed into a (winner, loser) pair via a self-judge. For David's concept-based fine-tuning, this is a template for closing the loop without external reward — the concept itself is judged by the model under a rubric prompt. The key empirical caveat: gains concentrate in open-ended generation tasks (writing, roleplay, extraction) and *do not* transfer to math/reasoning under the Open Assistant seed distribution, which suggests the variability mechanism here is mostly stylistic; reasoning amplification may need verifier-grounded judges (cf. [[rstar-math]]).

## Source
- arXiv: 2401.10020
- Raw markdown: `../../../raw/research/single-sample-llm-learning/21-D-2-self-rewarding-language-models.md`
- Raw PDF: `../../../raw/research/single-sample-llm-learning/pdfs/D-2-self-rewarding-language-models.pdf`

## Related
- [[star]]
- [[rstar-math]]
- [[_overview]]
