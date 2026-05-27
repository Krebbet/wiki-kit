# bert2BERT: Towards Reusable Pretrained Language Models

bert2BERT is a function-preserving growth method that initialises a larger transformer from a smaller pretrained one, then continues pretraining — saving 45–47% of compute versus training from scratch. The two key operators are **FPI** (Function-Preserving Initialization, a width-expansion map that preserves the network function exactly up to a LayerNorm rounding gap) and **AKI** (Advanced Knowledge Initialization, a cross-layer variant that breaks the weight symmetry FPI introduces and accelerates convergence). Depth-wise expansion stacks the widened model $k = \lfloor L^t / L^s \rfloor$ times; a two-stage pretraining schedule then fine-tunes bottom-prefix sub-models before full-model training. The result is validated on BERT$_\text{BASE}$ (110M) and GPT$_\text{BASE}$ (117M); [[ligo]] (ICLR 2023) later extends it to larger scales with a learned linear operator in place of the fixed random-sampling map.

## Method core

**Function-Preserving Initialization (FPI).** Transfers source model $S(L^s, D^s)$ to target $T(L^t, D^t)$ ($L^s \le L^t$, $D^s \le D^t$). Each weight matrix $\mathbf{W} \in \mathbb{R}^{d^w_\text{in} \times d^w_\text{out}}$ is expanded to $\mathbf{U} \in \mathbb{R}^{d^u_\text{in} \times d^u_\text{out}}$ via index-mapping functions

$$g_\text{in}(i) = \begin{cases} i & i \in [1, d^w_\text{in}] \\ f(\{1,\ldots,d^w_\text{in}\}) & i \in (d^w_\text{in}, d^u_\text{in}] \end{cases} \qquad g_\text{out}(j) = \begin{cases} j & j \in [1, d^w_\text{out}] \\ f(\{1,\ldots,d^w_\text{out}\}) & j \in (d^w_\text{out}, d^u_\text{out}] \end{cases}$$

where $f(\cdot)$ is uniform sampling. The expanded matrix $\mathbf{U} = \text{EXPN}(\mathbf{W}; g_\text{in}, g_\text{out})$ rescales duplicated rows by their copy-count $C_{g_\text{in}(i)}$ to preserve the linear map:

$$\widetilde{U}_{(i,*)} = \frac{1}{C_{g_\text{in}(i)}} \mathbf{W}_{(g_\text{in}(i),*)}, \qquad U_{(*,j)} = \widetilde{U}_{(*,g_\text{out}(j))}$$

MHA applies EXPN head-wise with consistency constraints $\{g^e_\text{out} = g^{q|k|v}_\text{in};\ g^{q|k|v}_\text{out} = g^o_\text{in};\ g^{q|k|v}_\text{in} = g^o_\text{out}\}$. LayerNorm parameters are index-mapped without rescaling, introducing a small deviation from strict FPI due to mean/variance recomputation over the expanded dimension — empirically negligible at tested scales but uncharacterised for large width ratios.

**Advanced Knowledge Initialization (AKI).** Breaks the weight symmetry that FPI creates (all expanded neurons in a row are identical at init) by filling the out-dimension of layer $l$ with parameters from both layer $l$ and layer $l{+}1$ of the source:

$$U^l_{(*,j)} = \begin{cases} \widetilde{U}^l_{(*,j)} & j \in [1, d^s_\text{out}] \\ \widetilde{U}^{l+1}_{(*,g^{l+1}_\text{out}(j))} & j \in (d^s_\text{out}, d^t_\text{out}] \end{cases}$$

Motivation: adjacent transformer layers have similar functionality (Jawahar et al. 2019; Clark et al. 2019), so upper-layer weights constitute high-level knowledge rather than noise. Empirically, AKI converges faster than FPI despite a higher initial loss. Using lower-layer knowledge (instead of upper) performs worse — direction matters; no theoretical explanation is given.

**Depth-wise expansion.** Post-width-expansion, the widened model is stacked $k = \lfloor L^t / L^s \rfloor$ times; residual layers come from the top of the widened model. Identical to StackBERT stacking applied after width growth.

**Two-stage pretraining.** Stage 1 trains bottom-$l_b$-layer prefixes of $T$ (one sub-model sampled per step, updating only its top $l_b$ layers; $l_b = 3$, $E_b = 5$ epochs optimal for BERT$_\text{BASE}$). Stage 2: standard full-model training. Over-training stage 1 ($E_b = 20$) collapses efficiency from 45.2% to 25.4% — the paper conjectures "source knowledge is destroyed" but offers no mechanism.

## Goal relevance

**G1 (block-isolation training / selective replacement).** bert2BERT is the growth direction: train small, expand, continue. G1 is the converse: train individual blocks in isolation and reinsert into a fixed full model. The FPI result is directly load-bearing for G1 — it proves that weight-level function-preservation across architectural boundaries is tractable in transformers. Any G1 implementation that needs to upsize a replaced block (e.g., grow a single layer's width to fit a wider pool slot) can apply $\text{EXPN}$ directly.

Caution: bert2BERT grows all layers simultaneously; G1 requires keeping other layers frozen while one block trains. The two-stage sub-model sampling loosely approximates block-local training but still passes gradients through the full bottom prefix — not true gradient isolation. See [[block-isolation-training]].

**G2 (per-block parameter allocation).** Depth-growth factor $k$ and width-growth ratio $D^t / D^s$ are per-block scaling choices. The paper's comparison of width-only growth $S(12, 512) \to T(12, 768)$ vs. joint growth from a smaller source $S(6, 512) \to T(12, 768)$ is directly informative: the latter still saves 23.9% but with larger source-to-target gap, consistent with diminishing returns when the source is much smaller than the target.

**G3 (token-conditional routing).** Not relevant.

## Credibility

arXiv preprint (2021), Tsinghua + Huawei Noah's Ark. Core FPI claim is substantially validated by [[ligo]] (ICLR 2023), which explicitly extends bert2BERT and cites it as direct prior work. Results are mean ± std over 3 runs; BERT$_\text{BASE}$ and StackBERT reimplementations match published numbers; MSLT reimplementation diverges (different optimizer) — flagged by authors. No released code at time of capture; reproducibility depends on downstream replication. Evaluation is narrow: BERT$_\text{BASE}$ (110M) and GPT$_\text{BASE}$ (117M) on GLUE / SQuAD / perplexity only; no experiments above 117M params.

## Empirical claims

| Claim | Evidence | Caveat |
|---|---|---|
| bert2BERT (AKI + 2-stage) saves 45.2% FLOPs over from-scratch BERT$_\text{BASE}$ | 4.0 vs 7.3 ×10¹⁹ FLOPs; avg GLUE 85.7 vs 85.5 | 3 runs, GLUE dev set only |
| AKI converges faster than FPI despite higher initial loss | Table 2: AKI 38.4% saving vs FPI 30.4% | BERT$_\text{BASE}$ only |
| FPI preserves source MLM loss almost exactly | $S(12,384) \to T$: FPI loss 1.89 = source 1.89; $S(12,512) \to T$: 1.70 vs 1.67 | Gap attributed to LayerNorm recomputation |
| bert2BERT saves 47% FLOPs for GPT$_\text{BASE}$ | 2.6 vs 4.9 ×10¹⁹ FLOPs; perplexity on PTB/WT2/WT103 comparable | Single run; no std reported |
| Sub-model training optimal at $E_b = 5$; over-training destroys efficiency | $E_b$=5 → 45.2%; $E_b$=20 → 25.4% | Ablation on one architecture only |
| $S(6,512) \to T(12,768)$: 23.9% saving despite 3× size gap | Table 3; bert2BERT avg 85.5 vs DirectCopy 84.2 | Single run; no std |

## Open questions / failure modes

1. **Optimal source-to-target ratio.** Authors flag this explicitly. $S(6,512) \to T(12,768)$ already shows diminishing returns when source is small relative to target.
2. **LayerNorm FPI gap.** Strict function-preservation breaks at LayerNorm due to mean/variance recomputation. Called negligible at tested scales; magnitude at large width ratios (e.g. $D^s = 256 \to D^t = 4096$) is unknown.
3. **AKI direction asymmetry.** Upper-layer knowledge accelerates convergence; lower-layer does not. No theoretical explanation. Open whether this holds in pre-LN (GPT-style) vs. post-LN (BERT-style) architectures.
4. **Sub-model overfitting mechanism.** $E_b = 20$ collapses efficiency. "Source knowledge destroyed" is a conjecture, not a mechanistic account. Directly relevant for G1: block-local training that runs too long relative to the rest of the model may exhibit the same collapse on reinsertion.
5. **Scaling.** All experiments ≤117M. [[ligo]] extends to larger scales with a learned $\mathbf{P}$ operator, implying the fixed random-sampling map of FPI/AKI may not hold for much larger width ratios.
6. **Homogeneous architecture requirement.** Source and target must be the same family (BERT or GPT). Cannot grow, e.g., from a narrow dense BERT into a wide MoE layer.
7. **FPI symmetry degeneracy.** All expanded neurons in a row are identical at init → degenerate gradients early in training. AKI partially addresses this via cross-layer mixing; full degeneracy dynamics are uncharacterised.

## Source

- `raw/research/selective-replacement-and-training/16-bert2bert.md` (PDF capture)
- `raw/research/selective-replacement-and-training/03-bert2bert-abs.md` (arXiv abstract)

## Related

- [[ligo]] — successor (ICLR 2023); replaces hand-crafted random-sampling $g_\text{in}/g_\text{out}$ with a learned linear operator $\mathbf{P}$; explicitly motivated as fixing bert2BERT's FPI limitations at larger scale
- [[bert-of-theseus]] — opposite direction: compression via Bernoulli module replacement vs. growth; both show transformer blocks can be substituted while preserving task performance
- [[sheared-llama]] — orthogonal: structured pruning + continued pretraining (shrink then recover) vs. growth + continue; both avoid training large models from scratch
- [[block-isolation-training]] — concept anchor; FPI is the function-preserving block-growth primitive that makes isolated-block reinsertion tractable
- [[modular-deep-learning]] — survey context; bert2BERT's FPI is a modular-growth primitive (new blocks are copies of existing ones — a form of module reuse)
