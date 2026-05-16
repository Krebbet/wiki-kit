---
name: sppo
description: Self-Play Preference Optimization — frames RLHF as a constant-sum two-player game; iterative multiplicative-weight update converges to Nash at O(1/√T). Captured for LLM-self-play family completeness; not load-bearing for single-sample concept learning.
type: research
---

# SPPO — Self-Play Preference Optimization

Wu, Sun, Yuan, Ji, Yang, Gu — UCLA / CMU. 2024. arXiv:2405.00675. Frames language-model alignment as a constant-sum two-player game over preference probabilities: each policy competes to maximise the probability of being preferred over its opponent. An iterative multiplicative-weight update is derived that converges (in average policy) to the Nash equilibrium at rate $O(1/\sqrt{T})$. Using only a 0.4B preference model (PairRM) and 60k UltraFeedback prompts, Mistral-7B reaches 28.53% length-controlled win rate against GPT-4-Turbo on AlpacaEval 2.0; Llama-3-8B reaches 38.77%.

**TL;DR:** Nash-convergent preference optimisation via self-play; key distinguisher from DPO/IPO is a per-response $L_2$ regression that independently drives winner log-ratio up and loser log-ratio down.

## Method

**Nash objective.** The von Neumann winner $\pi^*$ satisfies:

$$(\pi^*, \pi^*) = \arg\max_\pi \min_{\pi'} \mathbb{E}_{x}\!\left[\mathbb{E}_{y \sim \pi,\, y' \sim \pi'}\!\left[\mathbb{P}(y \succ y' \mid x)\right]\right]$$

**Iterative update.** At round $t$, sample $K=5$ responses per prompt from $\pi_t$, query PairRM for pairwise win rates, then minimise:

$$\ell_\text{SPPO}(y_w, y_l, x) = \left(\beta\log\frac{\pi_\theta(y_w|x)}{\pi_\text{ref}(y_w|x)} - \tfrac{1}{2}\right)^2 + \left(\beta\log\frac{\pi_\theta(y_l|x)}{\pi_\text{ref}(y_l|x)} + \tfrac{1}{2}\right)^2$$

This directly targets each response's absolute win rate — unlike symmetric DPO/IPO which only widen the relative gap and can leave loser log-ratio rising.

**Theorem 4.1 (Nash convergence).** Setting $\eta = \Theta(1/\sqrt{T})$, the duality gap of the average policy $\bar\pi_T = \frac{1}{T}\sum_t \pi_t$ satisfies $O(1/\sqrt{T})$.

## Claims

- Mistral-7B-SPPO Iter3: **28.53% LC win rate** vs GPT-4-Turbo on AlpacaEval 2.0 (base: 17.11%; iterative DPO: 26.39%).
- Llama-3-8B-SPPO Iter3: **38.77% LC win rate**, competitive with GPT-4 0613 and Llama-3 70B Instruct.
- MT-Bench: 7.59 (vs 7.51 base); Arena-Hard: 23.3 (vs 20.7 Snorkel/iterative DPO).
- No GPT-4 data; sole external supervision is PairRM (DeBERTa-V3-based, 0.4B parameters).
- Less length inflation than DPO/IPO baselines; robust to mini-batch size ($K=2$ vs $K=5$).

## Why this is *not* load-bearing for single-sample concept learning

Self-play here is operationally narrow: the current policy generates responses, a fixed external preference model judges them, and the policy is updated to raise win rates. There is no curriculum, no concept-specific reward signal, and no mechanism to install a novel concept from a small number of examples. Improving general instruction-following quality across a fixed 60k-prompt distribution is the entire scope. Replacing PairRM with a concept-specific verifier and redesigning the prompt distribution would be required before SPPO machinery could bear on the wiki's problem; neither is explored in the paper. Captured for completeness of the LLM self-play family.

## Source

- `../../../raw/research/self-play-concept-learning/.ingest/05-sppo.md`
- arXiv: https://arxiv.org/abs/2405.00675

## Related

- [[../rl-optimizers/dpo]] — SPPO explicitly contrasts its per-response regression against DPO's symmetric loss
- [[../rl-optimizers/_overview]] — preference optimisation subtree
- [[../self-improvement/self-rewarding-lm]] — LLM-as-judge alternative to a fixed preference model like PairRM
- [[spin]] — sibling: iterative DPO with moving reference, no game-theoretic framing
- [[_overview]] — self-play theme synthesis
