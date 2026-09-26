# Self-Play Pretraining with Zero Data

Cowsik, Dolev, Li et al. (arXiv:2609.30063, Sept 2026). Pretrains randomly-initialized transformers with **zero human/natural data** by having a generator co-evolve with a learner via self-play over programs for a universal Turing machine (UTM). Zero-shot loss on held-out natural data (text, images, speech, music, DNA) scales predictably with self-play compute, despite no natural data ever entering training.

## Method

Two same-architecture decoder-only transformers, byte-level tokenization, both randomly initialized (*tabula rasa*):
- **Generator** proposes programs for a minimal Brainf*ck-like UTM; executing a program with a random input tape yields a byte sequence.
- **Learner** trains via standard next-token cross-entropy on the generator's outputs.
- **Generator RL objective**: KL-regularized policy gradient (GRPO-style) toward a fixed uniform "Solomonoff-style" program prior. The reward is the key novelty — a preconditioned **gradient-alignment score** between the learner's gradient on a candidate program's output and the learner's actual recent parameter movement, computed via forward-mode autodiff (JVP) to avoid materializing full gradients. This avoids the failure mode of naive "difficulty" rewards (arbitrarily hard-to-predict sequences, e.g. injected random bytes, score high but carry no learnable structure) — reward instead concentrates on programs at the frontier of what the learner can *currently* learn.
- **Expert iteration**: reward-weighted SFT of the generator over the round's program pool (fresh + mutated + replayed programs) counters catastrophic forgetting.

Directly builds on Grau-Moya et al. 2024 (fixed universal-prior UTM program sampling) and Bloem 2025 (zero-natural-data universal pretraining from iterated random computation) — the contribution here is making the program-sampling distribution *adaptive* (RL-trained) rather than fixed.

## Results

Models ≤25M params, context 4096, up to 34.36B training tokens. Compute-optimal power-law fit `L(C) = E + AC^-α` (bits/byte) per held-out dataset.

- Predictable power-law zero-shot scaling on natural data across modalities, with exponents comparable to *direct* natural-data pretraining — despite zero natural data in training.
- Fixed universal-prior sampling (no adaptivity) scales substantially more slowly than self-play — access to UTM program space alone is insufficient; the adaptive curriculum is load-bearing.
- PCFG pretraining beats self-play on text/code (language-matched inductive bias), but self-play substantially outperforms PCFG on images, music, audio, speech.
- Self-play discovers Fibonacci/geometric/quadratic/cubic program families by round 256–512, vs. an expected first-appearance round >53,000 under the fixed uniform prior (across 1.64×10⁸ uniform-prior draws, only arithmetic sequences were ever found).
- In-context learning: the self-play learner reaches ~100% on REVERSE STRING, STACK, ASSOCIATIVE RECALL and learns MAX/MIN/SUM in-context; PCFG- and universal-prior-trained models fail broad ICL.

## Applicability

Research-scale proof of concept (≤25M params, 4K context) — not yet a practical alternative to natural-data pretraining. Requires RL infrastructure for GRPO-style generator training, JVP tooling for the gradient-alignment reward, and a program-pool/replay-bank system; no natural validation signal exists, so the authors use a small amount of natural-data loss purely for model selection (flagged by them as limited leakage). Explicitly positioned as a *complement* to natural-data pretraining — e.g. bootstrapping universal predictive structure (copying, recursion, hierarchical composition) once natural data becomes expensive or exhausted, not a replacement.

## Reproducibility

No released training-pipeline code or model weights found in the paper body. The only released artifact is a third-party forward-mode JVP attention kernel used for reward computation, not the self-play codebase itself. No PapersWithCode entry.

## Source

- raw/research/weekly-2026-09-26/05-self-play-pretraining-zero-data.md
- arXiv: https://arxiv.org/abs/2609.30063

## Related

- [[reinforcement-pretraining]] — closest architectural parallel: both apply GRPO-family RL directly at the pretraining stage, but RPT rewards next-token prediction against a real corpus while this source removes natural data entirely.
- [[evolution-fine-tuning]] — parallel theme of internalizing a self-generated/search-derived curriculum into model weights, via evolutionary search trajectories rather than UTM self-play.
- [[skill-self-play]] — shares the co-evolutionary self-play RL loop structure and GRPO training, applied to agentic skill acquisition rather than from-scratch pretraining.

Consistent with (not contradicting) [[reinforcement-pretraining]]: the paper explicitly states universal/zero-data pretraining is not a replacement for natural-data pretraining, matching RPT's continued reliance on a real corpus as reward source.
