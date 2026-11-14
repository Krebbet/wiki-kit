# Weight-Space Programming

Weight-Space Programming (Takehi, Teoh, Zhang, Khattab; MIT CSAIL, blog post 2026-11-02) is the claim that a frontier LLM (GPT-6 Astra) can read, write and edit another network's weights like code, with no gradients or training loop. Headline result: editing 0.016% of Qwen3.5-0.8B's weights lifted MATH-500 from 7.9% to 48.1%. It is a concept demo on a closed vendor model, not a peer-reviewed method; critics say the edits were already known.

## Method

- The LLM gets raw weights (or a Python sandbox holding the tensors) plus a natural-language spec, and reasons about what each component computes. Gradients and training loops are disallowed in the reported runs; the concept itself does not forbid them.
- Read experiments: names the training game of PPO nets, the shape a DDPM draws, and the training language of 7.2M-param char-LMs, finding every induction head (a known Elhage et al. analysis, reproduced by weight multiplication).
- Write experiments: fixes a PPO car policy (3.5% of weights, 1024/1024 episodes); writes MinAtar nets zero-shot; writes a 1.5M-param Go net (243→512×6→82) layer by layer, improving with up to 50 forward passes.
- Qwen3.5-0.8B edit: with a 10/25/50 forward-pass budget on GSM8K/MATH prompts, Astra diagnoses reasoning loops (flagged in Qwen's own model card) and edits 131,072 weights to suppress them.

## Results

| Qwen3.5-0.8B | MATH-500 | GSM8K | IFEval | Hit token limit |
|---|---|---|---|---|
| Base | 7.9 | 13.8 | 21.0 | 93.0 |
| Edited, 10 passes | 12.3 | 25.7 | 49.0 | 87.2 |
| Edited, 25 passes | 14.1 | 25.1 | 39.9 | 86.4 |
| Edited, 50 passes | 48.1 | 67.1 | 62.3 | 33.1 |

- An independent rebuild from the released logs (Hugging Face, Ahsen Khaliq) reportedly gives 51.0% MATH-500.
- MinAtar one-shot: Breakout 517.4 vs 25.3 for PPO-500M; Seaquest 53.1 vs 88.9; Asterix 53.2 vs 55.2. Go net at 50 passes beats an equal-size PPO net trained on 20M games.
- Negative results: Gemma 3 270M (rarely loops) did not improve (6.8 → ≤7.7 MATH-500); weights alone could not distinguish sycophantic from normal fine-tunes, though attention patterns on self-written prompts did, 3/3.

## Caveats

- The Qwen gain is loop removal, not new capability: 93% of base answers hit the token limit. The Gemma null result supports this reading. Compare [[deletion-tuning]] for the targeted-edit angle.
- Blog post, not a paper; not peer reviewed. Baselines are admittedly weak (fixed-budget PPO), and the authors concede the approach may only compose known interpretability steps.
- Depends on a closed vendor model (GPT-6 Astra); no open-model reproduction of the capability itself, only of the released edited weights.
- Skeptics argue the edits were already known techniques. Results are non-monotone in budget (10 and 25 passes barely help), so the 50-pass number is fragile.
- Logs are fully released (prompts, code, outputs, evals), which makes the claims auditable. An addendum (2026-11-12) lists replications, robot-policy and quantum-circuit extensions, and a benchmark (IWIBench).

## Source

- raw/research/weekly-2026-11-14/05-weight-space-programming.md (https://rikiyat.github.io/blog/weight-space-programming/)

## Related

- [[deletion-tuning]]
- [[seal-self-adapting]]
- [[program-as-weights]]
- [[evolution-fine-tuning]]
- [[evolutionary-search-eval-rigor]]
