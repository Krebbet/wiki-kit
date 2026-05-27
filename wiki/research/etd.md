# Encode, Think, Decode (ETD)

ETD (Koishekenov et al., arXiv Oct 2025) enhances LLM reasoning by identifying a contiguous "thinking" sub-block of layers via angular-distance analysis and looping only that block $k$ times at inference, leaving the surrounding encoder and decoder layers unmodified. Applied to OLMo-2 1B Base via mid-training only, it yields +28.4% on GSM8K and +36% on MATH relative to baseline. An adaptive variant (ACT router) learns per-token halting probabilities end-to-end.

## Method core

### E/T/D partition

The model's $L$ layers are partitioned into three contiguous segments — latent Encoder $E$, Thinker $T$, latent Decoder $D$ — using the mean angular distance between consecutive layer outputs. The angular distance between representations at layers $\ell$ and $\ell+n$ is:

$$
d\!\left(x^{(\ell)}, x^{(\ell+n)}\right) = \frac{1}{\pi} \arccos\!\left(\frac{x_T^{(\ell)} \cdot x_T^{(\ell+n)}}{\|x_T^{(\ell)}\|\,\|x_T^{(\ell+n)}\|}\right)
$$

where the inner product is over the hidden dimension for the **final token** $T$ of the sequence (the only position that attends to all prior tokens under causal masking), and $1/\pi$ normalizes the result to $[0,1]$. This is averaged over 10,000 C4 validation examples.

**Kneedle algorithm** (Satopaa et al., 2011) is applied to the sequence $\{d(l, l+1)\}_{l=0}^{L-1}$ to find the layer where the angular-distance curve transitions from steep to gradual decline — that index becomes the $E/T$ boundary. The same procedure applied in reverse from the last layer gives the $T/D$ boundary.

For OLMo-2 1B (16 layers): E = layers 0–6 (7 layers), T = layers 7–10 (4 layers), D = layers 11–15 (5 layers). Configuration notation: $N_E\text{-}N_T\text{*}k\text{-}N_D$ = **7-4\*k-5**.

### Iteration

During inference, the T block is applied $k$ times ($k = 1 \ldots 5$ tested). No new parameters are introduced; the same pretrained weights execute $k$ times. The forward pass through $L_{\text{eff}} = N_E + k \cdot N_T + N_D$ effective layers uses $N_E + N_T + N_D$ distinct parameter layers.

Formally, the output after $k$ iterations is:

$$
x^L = x^0 + \sum_{l=0}^{N_E-1} f(x^l, \theta^l) + \sum_{j=1}^{k}\sum_{l=N_E}^{N_E+N_T-1} f\!\left(x^{l+(j-1)N_T}, \theta^l\right) + \sum_{l=N_E+N_T}^{L-1} f\!\left(x^{l+(k-1)N_T}, \theta^l\right)
$$

### Training

Only the **mid-training stage** is re-run: $5 \times 10^{10}$ tokens ($\approx 1.25\%$ of total pretraining compute), same data mixture and hyperparameters as OLMo-2. The model is initialized from the end-of-stage-1 checkpoint. No LoRA, no new data, no architectural changes. OLMo-2's standard mid-training uses 3 random data orders and averages the resulting models; ETD uses one order.

### Adaptive variant (ACT)

A lightweight linear+sigmoid **router** is appended to the T block output. After each iteration $t$, the router produces a halting weight $w_t \in (0,1)$. Accumulated halting probability:

$$
H_t = \sum_{j=1}^{t} w_j
$$

Computation halts when $H_t \geq 1 - \varepsilon$ ($\varepsilon = 0.01$); maximum iterations $N_{\max} = 10$. The final T-block output (not a weighted mixture) is passed to $D$. The router is a single linear layer with sigmoid, initialized randomly, trained end-to-end with standard LM loss. No regularization term is added beyond the task loss.

## Goal relevance

| Goal | Relevance | Notes |
|------|-----------|-------|
| **G3** (token-conditional routing) | **High** | The ACT adaptive variant is a direct low-complexity instance of G3: a per-token router decides how many T-block passes to apply, varying effective depth per token. |
| **G1** (block isolation / swappability) | **Medium** | The E/T/D partition is a principled hand-designed block pool; T is the reusable compute unit. The angular-distance selection criterion provides an objective method for identifying which sub-block is the "thinking" core. |
| **G2** (dynamic parameter allocation) | Not applicable | ETD does not modify which parameter blocks are active; it repeats the same T block. |

## Key insight for this wiki

ETD demonstrates that **not all layers benefit equally from iteration** — looping the entire model (0-16\*k-0) degrades performance vs. the 7-4\*k-5 selective configuration, even at matched FLOPs. The ablation comparing 7-4\*4-5 vs. 2-12\*2-2 vs. 0-16\*2-0 (Table 4 in the paper) makes this explicit.

The angular-distance criterion is immediately applicable to [[huginn]]: running $d(l, l+1)$ on Huginn's block outputs could identify which recurrent sub-layers are doing "thinking" vs. "encoding" work, potentially informing a more targeted router insertion point than the current "after entire core\_block" specification. ETD's finding that layers 1–6 of OLMo-2 1B function as an encoder (high angular change) while layers 7–10 plateau (low change) closely parallels the functional differentiation Huginn's architecture is designed to exploit.

## Empirical claims

All results are OLMo-2 1B Base, single seed, configuration 7-4\*k-5 unless noted.

| Benchmark | Baseline (k=1) | Best ETD | Δ (relative) | k |
|-----------|----------------|----------|--------------|---|
| GSM8K | 44.05% | 56.56% | +28.4% | 5 |
| MATH | 4.57% | 6.22% | +36.0% | 3 |
| Reading Comprehension (avg) | 52.19% | 58.5% | +12.1% | 5 |
| Multi-Disciplinary Reasoning (avg) | 45.0% | 50.58% | +12.4% | 5 |
| BBH | 31.8% | 33.49% | +5.3% | 5 |
| Factual Knowledge (avg) | 37.55% | 38.23% | +1.8% | 5 |

MATH is erratic above k=3: k=4 gives 3.73% (−18% vs. baseline), k=5 gives 4.33% (−5%). Low absolute accuracy (~4–6%) means small absolute fluctuations produce large relative swings; the paper does not explain this regression.

**Ablation (Table 4, matched FLOPs):**
- At 28 effective layers: ETD 7-4\*4-5 > 2-12\*2-2 on all six categories.
- At 32 effective layers: ETD 7-4\*5-5 > 0-16\*2-0 on all six categories.

**Adaptive-depth ETD:** Outperforms fixed k=5 on DROP and OpenBookQA with fewer average iterations. Matches the fixed-depth accuracy–iteration tradeoff curve on remaining tasks.

## Credibility

arXiv preprint (Oct 2025, arXiv:2510.07358). No code released. Single backbone (OLMo-2 1B) — OLMo-2 7B and 13B checkpoints exist but are not tested. Single seed vs. OLMo-2's 3-seed ensemble (reduces statistical power; no error bars reported). MATH regression at k>3 unexplained and potentially a signal that low-accuracy regimes amplify noise. Interpretability motivation draws on Gromov et al. (2024), which is a credible prior work.

## Open questions / failure modes

- No 7B results despite OLMo-2 7B availability. The optimal $N_E/N_T/N_D$ split likely changes with depth and may not generalize from 1B.
- MATH regression at k>3 is unexplained — possible interference between repeated T-block passes at low-accuracy regimes, or simple variance given the tiny absolute numbers.
- The Kneedle algorithm requires a sensitivity parameter $S$; robustness to this choice across model families is untested.
- Adaptive ACT router is trained with standard LM loss only — no explicit reasoning-quality supervision. Whether it learns to halt on reasoning vs. factual tokens as expected is not analyzed.
- No wall-clock efficiency numbers. Repeated T-block passes share parameters but not activations; KV-cache behavior under looping is not discussed.
- Results restricted to base models; applicability to instruction-tuned models is left as future work.

## Source

- `raw/research/recurrent-reasoning/10-etd-abs.md` (arXiv:2510.07358)
- `raw/research/recurrent-reasoning/11-etd-pdf.md`

## Related

- [[huginn]] — primary application target; ETD's angular-distance partition criterion could inform Huginn's router placement within the recurrent core block.
- [[loopformer]] — concurrent work on looped transformers; ETD distinguishes itself by restricting looping to interpretability-identified reasoning layers rather than all internal layers.
- [[act]] — Graves (2016) ACT mechanism is used directly for ETD's adaptive variant; ETD's $H_t \geq 1-\varepsilon$ halting condition is the standard ACT formulation.
- [[mod]] — complementary routing strategy: MoD routes tokens around layers (depth-skipping), ETD routes tokens into additional T-block repetitions (depth-amplifying); opposite use of per-token conditional compute.
- [[layerskip]] — training-time pairing: LayerSkip uses layer dropout to make intermediate representations viable exit points; ETD uses mid-training to make the T block viable as a repeated unit. Both avoid pretraining from scratch.
- [[adaponderlm]] — related adaptive-depth recurrent approach; ETD's ACT variant is simpler (no separate ponder network, no regularization term) and targets reasoning amplification rather than efficiency.
