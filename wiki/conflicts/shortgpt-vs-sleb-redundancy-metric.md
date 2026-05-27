# Conflict — ShortGPT vs SLEB on the redundancy metric for transformer-block elimination

**Status:** documented (no winner ruling); the conflict is a **missing head-to-head**, not contradictory evidence on the same benchmark.

**Date opened:** 2026-04-30 (during the second `/research+ingest` run that ingested ShortGPT — the wiki had previously forward-flagged the disagreement when [[sleb]] was ingested in the first run).

## The disagreement

[[shortgpt]] and [[sleb]] both want to eliminate redundant transformer blocks based on a redundancy score, but they reach opposite conclusions about which scoring metric to use.

### ShortGPT's position

ShortGPT defines **Block Influence (BI)**:

$$
\mathrm{BI}_i = 1 - \mathbb{E}_{X,t}\,\frac{X_{i,t}^\top X_{i+1,t}}{\|X_{i,t}\|_2\,\|X_{i+1,t}\|_2}
$$

— the expected angular distance between a layer's input and output activations on the residual stream (§3.1, Eq. 1). A block whose input and output point in nearly the same direction has done little work and is a candidate for removal. ShortGPT claims (§4.3) that BI outperforms three competing metrics: **Relative Magnitude**, **norm-based importance**, and **sequential one-by-one removal**.

### SLEB's position

[[sleb]] tested an angular-similarity metric structurally equivalent to BI (their **Metric¹**) and explicitly demoted it in favour of **perplexity-delta-based scoring** (Metric² and Metric³), which directly measures the calibration-set perplexity change when a block is removed. SLEB's argument is that activation-similarity proxies the wrong quantity — two layers can have high cosine similarity on the residual stream while still being load-bearing for downstream perplexity, because cosine throws away magnitude and the residual stream's compositional structure does not reduce to direction.

## Why this is a missing-head-to-head, not a head-to-head loss

Neither paper ran the comparison the other paper would consider decisive:

| Comparison | ShortGPT ran it? | SLEB ran it? |
|---|---|---|
| BI / cosine vs Relative Magnitude | yes (BI wins) | — |
| BI / cosine vs perplexity-delta | **no** | yes (perplexity-delta wins) |
| Both metrics on the same model + calibration set + eval suite | **no** (different setups) | **no** (different setups) |

ShortGPT's §4.3 metric comparison does not include a perplexity-delta competitor; SLEB's metric comparison does not test on the LLaMA family ShortGPT uses. The model checkpoints differ, the calibration sets differ, the downstream evaluation suites differ. So neither paper's "winner" claim survives transposition to the other paper's setup.

## What both agree on

- The transformer-block stack is meaningfully redundant: 25–40% of blocks can be removed at modest perplexity cost across both setups.
- Some sort of input-output-on-the-residual-stream signal is informative.
- The remaining blocks need *some* recovery training (or at least a calibrated mixed-precision compensation step) for production-quality output, though both papers' headline numbers are training-free or near-training-free.

## What this conflict implies for G1

The wiki owner's **G1** experiment (training isolated transformer blocks for swappability) only depends on the redundancy metric indirectly — block elimination is a different operation from block isolation. But the metric question matters for *which blocks* you'd choose to swap first, or which positions tolerate block replacement with least collateral damage.

**Practical recommendation** *(synthesis)*: until a head-to-head appears, treat both metrics as reasonable signal and prefer perplexity-delta for the **selection decision** (it directly measures the quantity you ultimately care about) while keeping cosine BI as a **diagnostic / cheap proxy** when perplexity-delta is too expensive to compute (e.g., during NAS or large architecture sweeps). Both metrics agree on the same handful of "obviously redundant" blocks (typically middle layers); they disagree most on the borderline cases, which is where any G1 experiment would actually be sensitive.

## Resolution status

**Open.** No winner ruling. The conflict is recorded for awareness; if a future paper runs the head-to-head on a common benchmark, this file should be updated with the result.

## Source

- `raw/research/selective-replacement-and-training/24-shortgpt.md` — ShortGPT (BI definition §3.1 Eq. 1; metric comparison §4.3)
- `raw/research/block-training-quantization/17-sleb.md` — SLEB (Metric¹/²/³ comparison)

## Related

- [[shortgpt]] — primary advocate of cosine-similarity BI
- [[sleb]] — primary advocate of perplexity-delta scoring
- [[iterative-layer-distill]] — successor to ShortGPT; uses ShortGPT-style importance signal *and* recovery training, sidestepping the metric debate by adding a heal step
- [[sheared-llama]] — orthogonal direction (end-to-end learned mask, no explicit metric ranking)
- [[block-isolation-training]] — concept anchor; this conflict bears on which blocks are best candidates for swap-and-train experiments
