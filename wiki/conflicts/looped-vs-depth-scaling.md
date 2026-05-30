# Conflict — Looping vs Depth-Scaling Tradeoff

**Status:** open
**Opened:** 2026-04-24
**Ruling:** frame as open; comparison bases differ (iso-param vs iso-FLOP vs iso-token) and papers do not explicitly reconcile.

## The question

Does architectural looping (applying the same weight-tied block L times) trade perplexity/general-LM quality for reasoning ability, or does it overcome the perplexity penalty at sufficient training scale?

## Position A — looping trades perplexity for reasoning

### Latent-Thoughts (05)

Saunshi et al. run an explicit **iso-FLOP** comparison at 1B–1.5B scale on the Pile (250B tokens). A k-layer block looped L times — denoted (k ⊗ L) — is matched against a non-looped (kL ⊗ 1) baseline at identical compute. Result: looped models cover only **34–50% of the perplexity gap** to the iso-FLOP non-looped baseline across all tested block sizes (k ∈ {4, 6, 8, 12}). On closed-book QA (memorization), performance tracks the perplexity deficit closely (~37–58% gap). On reasoning tasks — math word problems, reasoning primitives — looped models **outperform** the iso-FLOP baseline for all parameter budgets; e.g., (12 ⊗ 2) scores 34.3% on math word problems vs. 29.3% for the 24-layer baseline at 50% of the parameters. The perplexity penalty is attributed directly to the parameter count reduction (looped models have 1/L the parameters at iso-FLOP). The tradeoff is sharp, quantified, and explicit.

### Universal Transformer (04) — precursor

Dehghani et al. demonstrate that weight-tied recurrent-depth transformers (UT-base) outperform standard Transformer-base on algorithmic tasks (Copy, Reverse, Addition, LTE), bAbI QA (0.23 vs 15.2 average error), LAMBADA (perplexity 142 vs 7321 for standard Transformer), and WMT14 En-De MT (28.9 vs 28.0 BLEU, iso-param). However, all experiments are at **pre-GPT-era, modest scale** (Transformer-base comparable; no >1B validation). The LAMBADA result shows a large gain, but LAMBADA is a cloze task with strong reasoning demands — not a clean general-LM perplexity benchmark. The perplexity tradeoff identified by Latent-Thoughts at modern LM scale is **not quantified** by UT; the scale gap makes direct reconciliation impossible.

## Position B — looping overcomes perplexity penalty at scale

### Ouro / Looped Language Models (06)

Ouro pre-trains a 1.4B LoopLM (N-layer stack, 4 recurrent steps, effective depth ~96 layers) on **7.7T tokens** with a learned entropy-regularized adaptive exit gate. On general LM benchmarks: Ouro-1.4B matches or exceeds Qwen3-4B on BBH (71.02 vs 70.95), GSM8K (78.92 vs 72.86), and MATH500 (82.40 vs 59.60); Ouro-2.6B exceeds all tested ≤8B dense baselines on MATH500 (90.85 vs best 83.20). Ouro-6 further confirms that bits-per-parameter for factual knowledge is **identical** between looped and non-looped models (~2 bits/param regardless of loops), but manipulation/reasoning gains are real.

**Critical caveat:** Qwen3 was trained on **36T tokens** (4.7× more); the favorable comparison is therefore on **token-efficiency**, not iso-FLOP or iso-param. At matched training compute or matched parameters, the comparison may differ substantially. Ouro does not run an iso-FLOP-controlled ablation at 1B+ scale.

## Why the comparison is hard

*Editorial.* The three papers use incompatible axes:

- **Latent-Thoughts**: iso-FLOP — same compute, looped vs. non-looped, 1B scale. The perplexity penalty is directly measured and attributed to parameter reduction.
- **Ouro**: implicit token-efficiency framing — 1.4B looped vs. 4B dense, with the looped model trained on far fewer tokens. "Matches" a larger model with fewer tokens, not fewer FLOPs or fewer parameters at equal data.
- **Universal Transformer**: small-scale (base-model era), iso-param on MT; perplexity comparison against modern non-looped models is unavailable.

No paper in this batch runs a controlled **iso-param, iso-FLOP, iso-token** comparison of a looped vs. non-looped model at 7B+ scale on both general LM perplexity and reasoning benchmarks simultaneously.

## Possible resolutions (editorial)

Three framings consistent with current evidence:

1. **Position A (LT) is correct**: looping structurally trades perplexity for reasoning due to the parameter-count reduction at iso-FLOP. The gap is real and does not close at scale — Ouro's favorable results are explained by the token-efficiency framing, not by overcoming the tradeoff.
2. **Position B (Ouro) is correct**: at sufficient training scale and with an adaptive exit gate, looped models match dense models on general LM benchmarks and beat them on reasoning. LT's iso-FLOP framing understates the practical value of parameter efficiency.
3. **Both correct, different axes**: looping trades per-parameter expressiveness for per-FLOP expressiveness. At iso-FLOP (same compute, LT's frame), worse perplexity because fewer parameters; at iso-param (same capacity, Ouro's implicit frame at smaller scale), better reasoning with competitive general LM. The tradeoff is real but axis-dependent.

## What would resolve this

*Editorial.* A controlled experiment matching a looped model and a non-looped model on all three axes simultaneously — **iso-param, iso-FLOP, iso-token** — at ≥7B scale, evaluated on both general LM perplexity and a diverse reasoning benchmark suite. Neither Latent-Thoughts (iso-FLOP only, 1B) nor Ouro (token-efficiency framing, no iso-FLOP ablation) provides this. The community has not run it.

## Related
- [[universal-transformer]]
- [[looped-transformers-and-reasoning]]
- [[looped-language-models]]

## Source
- `raw/research/thesis-foundations/04-universal-transformers.md`
- `raw/research/thesis-foundations/05-latent-thoughts-looped.md`
- `raw/research/thesis-foundations/06-ouro-looped-lm.md`
