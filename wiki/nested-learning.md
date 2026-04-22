# Nested Learning + Hope

Google Research / Columbia paper (Behrouz et al., NeurIPS 2025) proposing **Nested Learning (NL)** — a unifying paradigm that re-casts both architectures and optimizers as nested systems of associative memories at different update frequencies — and uses it to derive a continual-learning sequence model called **Hope** (self-modifying Titans + a Continuum Memory System) plus a multi-scale Muon variant (**M3**). Consolidates four contributions into one page per the prune-to-10 plan.

## Method

NL re-represents a model as an ordered set of nested optimization problems indexed by update-frequency levels. Three concrete contributions:

### 1. Optimizers as associative memories

Backpropagation is reframed as a self-referential associative memory mapping each layer's input to its local error signal (`Δ_l x̂_{l-1}^T`). Adam, AdaGrad, RMSProp, SignSGD, NAdam, AMSGrad, RAdam, Lion, Shampoo/Soap, and Muon (Newton-Schulz orthogonalization treated as polynomial mapping to an orthogonal coordinate system) are decomposed into 2-level nested gradient-descent problems compressing the gradient stream. **Adam is shown to be the optimal element-wise L2 associative memory for predicting gradient variance.**

### 2. New optimizer / update rules

- **Delta Gradient Descent (DGD)** replaces the Hebbian-style dot-product inner objective of GD with an L2 regression objective + Sherman-Morrison closed form: `W_{t+1} = W_t(I - η'_t x_t x_t^T) − η'_t ∇` — adaptive state-dependent decay.
- **Generalised Gradient Descent (GGD)** family, **Delta Momentum**, **Deep Momentum GD (DMGD)** (MLP-valued momentum).
- **Multi-scale Momentum Muon (M3)** = Muon + Adam + multi-timescale momentum via CMS.

### 3. Continuum Memory System (CMS) and Hope

CMS replaces a Transformer's MLP block with a chain of MLPs `MLP^{f_1}, ..., MLP^{f_k}`, each updated every `C^l` steps (different frequencies).

**Hope** = a self-modifying Titans block (where K, V, Q, learning-rate `η_t`, retention `α_t`, and the memory itself are all deep MLP associative memories that generate their own values `v̂ = M_box(v_t)`, trained chunk-wise with parallelizable DGD updates) followed by CMS as the FFN. Variant **Hope-Attention** swaps the self-modifying Titans for softmax attention.

Pre-trained Llama-3 MLPs can initialize CMS levels (Section 7.3, "Ad-hoc Level Stacking") for continual pre-training.

Derives from: Titans (Behrouz 2025c), MIRAS (Behrouz 2025b), DLA / Atlas (Behrouz 2025a), TTT (Sun 2024), DeltaNet/RWKV-7, Muon (Jordan 2024), MAML (Finn 2017), Schmidhuber's self-referential weight matrix (1993, 2003).

## Results

- **Class-incremental text classification** (Llama-3-8B / 3B + Hope-style MLP adaptation + 15B-token continual pretrain) on CLINC, Banking, DBpedia: Hope-enhanced model beats ICL, EWC, and InCA across all three.
- **Long-context QA / NIAH** (RULER MK-NIAH, LongHealth, QASPER): Hope beats DuoAttention and ICL; on RULER S-NIAH-3 16k Hope **24.8** vs Titans 21.2 vs RWKV-7 5.8. Hope-Attention beats vanilla Transformer on S-NIAH-1 across all lengths (100/100/100 vs 88.6/76.4/79.8).
- **BABILong**: Hope maintains performance to **10M context** where Titans/ARMT degrade after 1M.
- **LM + commonsense (Table 2)**:
  - 760M / 30B tokens: Hope avg **52.28** vs Titans 51.68, Transformer++ 50.11.
  - 1.3B / 100B tokens: Hope avg **58.04** vs Titans 56.82, Transformer++ 53.38, RWKV-7 55.30.
  - WikiText ppl: Hope **14.39** vs Titans 15.60 vs Transformer++ 17.92.
  - LMB ppl: Hope **10.08** vs Titans 11.41.
- **In-context recall (Table 3)** SWDE/NQ/DROP/FDA/SQUAD/TQA: Hope is best attention-free; gap with Transformer remains on FDA (41.9 vs 67.3).
- **MAD synthetic (Table 4)**: Hope beats Transformer on Compression (51.2 vs 49.4), Fuzzy ICR (52.1 vs 47.9), Selective Copying (99.7 vs 96.2), Memory (85.2 vs 83.7).
- **Formal language recognition (Table 5)**: Hope and SRWM/LSTM solve Parity, (aa)*, (abab)*, a^n b^n, a^n b^n c^n, Shuffle-2 perfectly (100); Transformer and DeltaNet fail Parity-Bin1 (0).
- **Continual translation (CTNL, Manchu+Kalamang → English)**: Hope-3 recovers ICL-no-forgetting under sequential continual learning where ICL collapses.
- **M3 optimizer**: On ViT 24M/86M ImageNet-21K, M3 beats AdamW and Muon on train/test loss. Training time on 140M and 1.3B LM is on-par with AdaMuon, slower than Muon.
- **Ablation (Table 6)**: removing DGD, momentum, weight decay, CMS, or any inner projection of K/V hurts ppl + reasoning; q inner-projection is the only nearly neutral component.

## Applicability

- **Continual pretraining / domain adaptation** of existing Llama-class models: lift a pretrained Transformer's MLP weights into the slowest level of a CMS and continue training (15B tokens demonstrated). Useful for in-house fine-tunes that need to retain old knowledge while absorbing new corpora.
- **Small/medium LM training from scratch** (760M–1.3B, 30–100B tokens shown) where long-context (≥1M) and continual learning matter.
- **M3 as a drop-in optimizer** for ViT and small/medium LMs when extra memory of long-past gradients is desired; cost is multiple momentum buffers.

Prerequisites: chunk-wise parallel training infra similar to Titans / TTT; Newton-Schulz orthogonalization; deep MLP memory blocks add parameters and ~Muon-class compute. Multiple momentum buffers ⇒ higher optimizer state RAM. **No released weights or code in the paper itself.**

## Novelty

Genuinely new framing rather than a single new trick. What's new vs Titans:
- **Self-modification** — K, V, η, α, and the memory itself are all MLP associative memories that generate their own targets `v̂` via `M_box(v_t)`, trained with DGD.
- **Continuum Memory System** replacing the FFN with a multi-frequency MLP chain.
- **Explicit decomposition of Adam/Muon/Shampoo** as nested associative memories, leading to M3.

The "architecture = optimization" view echoes deep-equilibrium, meta-learning-as-optimization (Akyurek 2022), and "Transformers learn in-context by gradient descent" (Von Oswald 2023), but pushed further into a unifying framework absorbing hypernetworks, MAML, learned optimizers, and TTT as instances of "knowledge transfer between levels."

## Reproducibility

No code, weights, or paperswithcode entry mentioned in the captured PDF. Experiments depend on the Titans / MIRAS / Atlas codebase (Behrouz et al. 2025a/b/c); chunk-wise dual-form training procedure is referenced as identical to Sun et al. 2024 and Behrouz 2025c, both of which have partial open-source community implementations. Independent reproduction will require re-implementing self-modifying Titans + CMS from the equations.

## Adoption

NeurIPS 2025 acceptance + Google Research authorship. The Titans/MIRAS/Atlas line is a deliberate research program from the same group, increasingly cited in the modern-RNN / linear-attention community alongside Mamba, RWKV-7, DeltaNet, Comba. Too early at capture date (2026-04-22) to call it "widely adopted"; the paper is a synthesis flag rather than a community-adopted method.

## Source

- `raw/research/radar-2026-04/04-nested-learning.md` — Nested Learning paper PDF (arXiv:2512.24695). Captured 2026-04-22.

## Related

- [[titans-miras]] — direct ancestor; Hope = self-modifying Titans + CMS.
- [[test-time-training]] — NL subsumes TTT under parametric ICL; cluster page covers Titans, Hope, In-Place TTT.
- [[conflicts/icl-emergent-vs-nested-levels]] — NL's "ICL is not emergent" claim.
- [[conflicts/ttt-distinct-vs-parametric-icl]] — NL's claim that TTT is parametric ICL.
- [[watchlist]] — DeltaNet, RWKV-7, Muon, Shampoo, MAML referenced but not captured.
