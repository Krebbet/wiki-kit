# Iterative Layer-wise Distillation for Efficient Compression of Large Language Models

Iteratively prunes the least-important transformer layer — scored by empirical quality drop on held-out tasks, not proxy metrics — then fine-tunes the surviving layers against the original teacher via a joint KL + MSE distillation loss, repeating until target depth is reached. Applied to Qwen2.5-3B, removing 8 of 36 layers (→ 2.47B params) costs only 9.7% aggregate quality, versus a >70% collapse for non-iterative [[shortgpt]]-style pruning. The iterative heal-after-removal loop is the key mechanism distinguishing the approach from single-pass depth reduction.

## Method core

At each round $r$, form $n$ one-layer-removed candidate models from the current student (depth $n$); evaluate each candidate across representative datasets; select layer $i^*$ minimising aggregate quality drop. Remove $i^*$, then fine-tune with:

$$\mathcal{L} = \frac{1}{100}\,\mathrm{KL}(p_\text{student} \| p_\text{teacher}) + \mathrm{MSE}(\hat{h}_\text{last-trainable},\, h_\text{last-trainable}) + \mathrm{MSE}(\hat{h}_\text{final},\, h_\text{final})$$

where $p$ are token-probability distributions over the vocabulary and $h$ are hidden states at the last trainable and final model layers. After fine-tuning, recalculate per-layer importance on the updated student and repeat. Importance scoring uses task-performance deltas (F-score, ROUGE across 7 heterogeneous datasets) rather than the Block Influence proxy $\mathrm{BI}_i = 1 - \mathbb{E}_{X,t}\frac{X_{i,t}^\top X_{i+1,t}}{\|X_{i,t}\|\|X_{i+1,t}\|}$ used by [[shortgpt]]. The ablation over ~18 loss variants establishes that the $\frac{1}{100}$ KL scaling is load-bearing: pure KL with no MSE terms recovers no quality beyond the no-fine-tuning baseline ($0.608$ vs $0.608$ for a 2-layer prune).

## Goal relevance

**G1 (swappable isolated blocks) — primary.** The paper's core problem — restoring a fixed-depth stack after removing block $i$ — is precisely the heal-after-removal training primitive that G1 needs. The joint KL + MSE fine-tuning step demonstrates that targeted local fine-tuning of adjacent layers recovers lost inter-layer dependency. The finding that middle layers 17–24 are systematically the cheapest to remove also maps directly to which block positions tolerate swapping with least collateral damage.

**G2 (dynamic per-block params) — background.** Per-layer importance variation supports adaptive-allocation intuitions; the method itself does not perform dynamic allocation.

**G3 (token-conditional routing) — not relevant.**

## Credibility

- **Venue / year:** arXiv preprint 2511.05085, captured 2026-04-30; no peer-review venue listed. Lomonosov MSU; Russia Science Foundation grant 25-11-00191.
- **Code:** public — https://github.com/kaengreg/layer-wise_distillation
- **Weights:** public — https://huggingface.co/kaengreg/Qwen2.5-2B-layerwise-distilled
- **Ablation rigor:** partial — 5 pruning strategies and ~18 loss variants systematically compared, but on a single model (Qwen2.5-3B) and one language pair (EN/RU). No multi-family validation.
- **Replication status:** single-lab; code and weights public; narrow language scope.

## Empirical claims

- Qwen2.5-3B (36 layers, Aggregate Score 0.636) → 28 layers (2.47B): Aggregate Score 0.574 (9.7% drop).
- Same model → 24 layers (2.16B): Aggregate Score 0.519 (18% drop).
- [[shortgpt]] baseline (no distillation, same 8-layer removal): Aggregate Score 0.175 (>70% drop).
- Iterative Block Influence + FT achieves 0.352 — roughly 2× [[shortgpt]] but far below iterative data-driven importance.
- Middle layers 17–24 are most frequently selected for removal; final layers are most damaging.
- Pure KL distillation alone fails to recover quality; MSE hidden-state terms are necessary.

## Open questions / failure modes

- **Scaling:** all experiments on one 3B model; generalisability to 7B+ or different families (LLaMA, Mistral) is untested.
- **Evaluation cost:** every round evaluates all $n$ one-layer-removed candidates across 7 datasets — $O(n^2)$ total evaluations; wall-clock cost not reported.
- **Russian-heavy evaluation:** 5 of 7 datasets are Russian-language; aggregate score may not transfer to English-centric or multilingual settings.
- **Data-evaluation distribution mismatch:** fine-tuning uses IlyaGusev/rulm (RU/EN blend); interaction with evaluation distribution is not ablated.
- **Non-contiguous removal:** the method selects individual layers globally rather than contiguous blocks; the pruned model is a non-contiguous subsequence, which complicates plug-in swapping in a modular setting.
- **Single-layer-per-step assumption:** removing 2+ layers per round is not compared; different step sizes may find different local optima.

## Source

- `raw/research/block-training-quantization/20-iterative-layer-distill.md` (PDF capture)
- `raw/research/block-training-quantization/10-iterative-layer-distill-abs.md` (arXiv abstract)

## Related

- [[bert-of-theseus]] — heal-after-removal predecessor; both rely on adjacent-layer fine-tuning to recover compromised dependencies
- [[block-isolation-training]] — concept anchor; iterative-layer-distill is the heal-after-removal training primitive that G1 needs
- [[shortgpt]] — direct predecessor (iterative method extends ShortGPT's importance scoring)
- [[sleb]] — alternative block-pruning approach (training-free)
- [[gptq]] — referenced in author's PTQ comparisons
- [[minillm]] — distillation baseline cited
- [[dcr]] — alternative module-replacement-style heal mechanism
