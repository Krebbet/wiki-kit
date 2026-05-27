# Learning to Grow Pretrained Models for Efficient Transformer Training (LiGO)

LiGO (Wang et al., arXiv 2303.00980) learns a linear operator $\mathbf{M}$ that maps the vectorised parameters of a small pretrained transformer $\Theta^{(\text{small})}$ to a warm initialisation for a larger model via $\Theta^{(\text{new})} = \mathbf{M}\,\text{vec}(\Theta^{(\text{small})})$. $\mathbf{M}$ is learnt in ~100 SGD steps on pretraining data — negligible overhead — and subsumes all prior function-preserving init schemes ([[bert2bert]], Net2Net, StackBERT) as non-learnt special cases. Across BERT, RoBERTa, GPT-2, DeiT, and CaiT it yields 22–55% FLOPs savings versus training from scratch with downstream quality matching or exceeding the scratch baseline.

## Method core

The growth operator is decomposed depth-first then width-first:

$$\mathbf{M} = \mathbf{L}_{\text{depth}}\,\mathbf{R}_{\text{width}}$$

$\mathbf{R}_{\text{width}}$ is block-diagonal — one block per source layer — lifting weight matrices from width $D_1$ to $D_2$. $\mathbf{L}_{\text{depth}}$ is a $L_2 \times L_1$ array of diagonal matrices, blending all source layers into each target layer. In full Kronecker-factorised form (Eq. 8):

$$\mathbf{M} = (\mathbf{w} \otimes \mathbf{I})\bigl(\bigoplus_l \mathbf{A}_l \otimes \mathbf{B}_l\bigr)$$

where $\mathbf{w} \in \mathbb{R}^{L_2 \times L_1}$ holds layer-blending scalars (tied across neurons), and per-layer $\mathbf{A}_l, \mathbf{B}_l \in \mathbb{R}^{D_2 \times D_1}$ expand weight matrices as $\mathbf{B}_l \mathbf{W}_l \mathbf{A}_l^\top$. This reduces total learnable parameters in $\mathbf{M}$ to $O(L_1 L_2 + L_1 D_1 D_2)$, making 100-step SGD feasible. The factorisation coincides with Monarch / butterfly sparsification (Dao et al., ICML 2022). For aligned residual streams, input-dimension matrices across Q/K/V/O/FFN are further tied to a single $\mathbf{B}^{(\text{emb})}$.

## Goal relevance

**G1 (block isolation / function-preserving growth).** Primary. LiGO produces a function-*approximating* (not strictly function-preserving) initialisation via a learnt linear operator. Per-layer Kronecker blocks $(\mathbf{A}_l, \mathbf{B}_l)$ are per-block parameter choices with a direct analogue to [[block-isolation-training]] thinking; unlike FPI-based schemes, backprop flows globally after init, so isolation is at initialisation only.

**G2 (per-block parameter allocation).** Secondary. $\mathbf{A}_l, \mathbf{B}_l$ are learnt independently per source layer — a weak form of heterogeneous per-block budget. Uniform growth ratios are used throughout in all reported experiments, leaving non-uniform allocation unexplored.

**G3 (token-conditional routing).** Not relevant.

## Credibility

Four institutions (UT Austin, MIT-IBM Watson, MIT, Columbia); arXiv 2023, ICLR-era. Results span two language model families and two ViT families with consistent FLOP savings. Ablation confirms 100-step learning budget is sufficient; 10 000 steps erodes net gains. No confirmed proceedings venue noted in source — treat as strong preprint.

## Empirical claims

| Growth task | FLOPs saved vs. scratch |
|---|---|
| BERT-Small → BERT-Base | 44.7% |
| BERT-Base → BERT-Large | 45.2% |
| RoBERTa-Small → RoBERTa-Base | 47.2% |
| GPT2-Base → GPT2-Medium | 22.5% |
| DeiT-S → DeiT-B | 55.4% |
| CaiT-XS → CaiT-S | 52.6% |

Downstream quality (GLUE, SQuAD, ImageNet transfer) matches or slightly exceeds scratch in all cases. Combined with layer-drop / token-drop / staged training adds 4–8% further FLOP reduction.

## Open questions / failure modes

- Only uniform growth ratios evaluated; heterogeneous per-block growth (different $D_2/D_1$ per layer, or growing only selected blocks) is unexplored.
- Growth operator learnt on pretraining data with a fixed 100-step budget — potentially sensitive to distribution shift between the learning phase and subsequent training.
- Not evaluated on instruction-tuned or RLHF-trained models where parameter geometry may differ from pretraining checkpoints.
- Compute ceiling at ~345M parameters (GPT-2 Medium scale); scalability to billion-parameter models unverified.

## Source

- `raw/research/selective-replacement-and-training/20-ligo.md` (PDF capture of arXiv 2303.00980, captured 2026-04-30)
- `raw/research/selective-replacement-and-training/04-ligo-abs.md` (arXiv abstract)

## Related

- [[bert2bert]] — predecessor (hand-crafted FPI; LiGO learns the linear operator)
- [[sheared-llama]] — opposite direction (pruning + recovery)
- [[block-isolation-training]] — concept anchor
- [[modular-deep-learning]] — survey context
