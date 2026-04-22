---
source: "raw/research/radar-2026-04/04-nested-learning.md"
slug: "04-nested-learning"
summarized_on: "2026-04-22"
schema_version: 1
---

# Nested Learning: The Illusion of Deep Learning Architecture (Behrouz et al., NeurIPS 2025)

## One-line
Google Research / Columbia paper proposing "Nested Learning" (NL), a unifying paradigm that re-casts both architectures and optimizers as nested systems of associative memories at different update frequencies, and uses it to derive a continual-learning sequence model called Hope (built from self-modifying Titans + a Continuum Memory System) plus a multi-scale Muon variant (M3).

<!-- DOMAIN-SLOT: takeaway-prompts -->
## Method
NL re-represents a model as an ordered set of nested optimization problems indexed by update-frequency levels. Three concrete contributions:
1. **Optimizers as associative memories.** Backpropagation is reframed as a self-referential associative memory mapping each layer's input to its local error signal (delta_l x̂_{l-1}^T). Adam, AdaGrad, RMSProp, SignSGD, NAdam, AMSGrad, RAdam, Lion, Shampoo/Soap, and Muon (NewtonSchulz orthogonalization treated as polynomial mapping to an orthogonal coordinate system) are decomposed into 2-level nested gradient-descent problems compressing the gradient stream. Adam is shown to be the optimal element-wise L2 associative memory for predicting gradient variance.
2. **New optimizer / update rules.** Delta Gradient Descent (DGD) replaces the Hebbian-style dot-product inner objective of GD with an L2 regression objective + Sherman-Morrison closed form, giving an adaptive state-dependent decay W_{t+1} = W_t(I - eta'_t x_t x_t^T) - eta'_t grad. Generalised Gradient Descent (GGD) family + Delta Momentum, Deep Momentum GD (DMGD, MLP-valued momentum), and Multi-scale Momentum Muon (M3 = Muon + Adam + multi-timescale momentum via CMS).
3. **Continuum Memory System (CMS) and Hope.** CMS replaces a Transformer's MLP block with a chain/aggregation of MLPs MLP^{f_1}, ..., MLP^{f_k}, each updated every C^{l} steps (different frequencies). Hope = a self-modifying Titans block (where K, V, Q, learning-rate eta_t, retention alpha_t, and the memory itself are all deep MLP associative memories that generate their own values v̂ = M_box(v_t), trained chunk-wise with parallelizable DGD updates) followed by CMS as the FFN. Variant **Hope-Attention** swaps the self-modifying Titans for softmax attention. Pre-trained Llama-3 MLPs can initialize CMS levels (Section 7.3, "Ad-hoc Level Stacking") for continual pre-training. Derives from: Titans (Behrouz 2025c), Miras (Behrouz 2025b), DLA / Atlas (Behrouz 2025a), TTT (Sun 2024), DeltaNet/RWKV-7 (Schlag 2021; Peng 2025), Muon (Jordan 2024), MAML (Finn 2017), Schmidhuber's self-referential weight matrix (1993, 2003), Allen-Zhu canon layers (2025).

## Results
- **Class-incremental text classification** (Llama-3-8B / 3B backbone + Hope-style MLP adaptation + 15B-token continual pretrain) on CLINC, Banking, DBpedia: Hope-enhanced model beats ICL, EWC, and InCA across all three (Figure 6).
- **Long-context QA / NIAH** (RULER MK-NIAH, LongHealth, QASPER, Figure 7 + Table 1): Hope beats DuoAttention and ICL; on RULER S-NIAH-1/2/3, MK-NIAH-1, MQ-NIAH, MV-NIAH at 4K/8K/16K Hope is best attention-free model (e.g. S-NIAH-3 16K: Hope 24.8 vs Titans 21.2 vs RWKV-7 5.8). Hope-Attention beats vanilla Transformer on S-NIAH-1 across all lengths (100/100/100 vs 88.6/76.4/79.8).
- **BABILong** (Figure 9): Hope maintains performance to 10M context where Titans/ARMT degrade after 1M.
- **Language modeling + commonsense** (Table 2). 760M / 30B tokens: Hope avg 52.28 vs Titans 51.68, Transformer++ 50.11. 1.3B / 100B tokens: Hope avg 58.04 vs Titans 56.82, Transformer++ 53.38, RWKV-7 55.30. Hope wins WikiText ppl (14.39 vs Titans 15.60 vs Transformer++ 17.92) and LMB ppl (10.08 vs Titans 11.41).
- **In-context recall** (Table 3, SWDE/NQ/DROP/FDA/SQUAD/TQA): Hope is best attention-free, narrows gap with Transformer (e.g. SWDE 65.9 vs Transformer 71.4, FDA 41.9 vs 67.3 — gap remains).
- **MAD synthetic** (Table 4): Hope beats Transformer on Compression (51.2 vs 49.4), Fuzzy ICR (52.1 vs 47.9), Selective Copying (99.7 vs 96.2), Memory (85.2 vs 83.7).
- **Formal language recognition** (Table 5): Hope and SRWM/LSTM solve Parity, (aa)*, (abab)*, a^n b^n, a^n b^n c^n, Shuffle-2 perfectly (100); Transformer and DeltaNet fail Parity-Bin1 (0).
- **Continual translation (CTNL, Manchu+Kalamang -> English)**: Hope-3 recovers ICL-no-forgetting performance under sequential continual learning where ICL collapses.
- **M3 optimizer**: On ViT 24M/86M ImageNet-21K, M3 beats AdamW and Muon on train/test loss (Figure 11). Training time on 140M and 1.3B LM is on-par with AdaMuon, slower than Muon (Figure 12).
- **Ablation** (Table 6): removing DGD, momentum, weight decay, CMS, or any inner projection of K/V hurts ppl + reasoning; q inner-projection is the only nearly neutral component.

## Applicability
- Continual pretraining / domain adaptation of existing Llama-class models: Section 7.3 shows you can lift a pretrained Transformer's MLP weights into the slowest level of a CMS and continue training (15B tokens demonstrated). Useful for in-house fine-tunes that need to retain old knowledge while absorbing new corpora.
- Small/medium LM training from scratch (760M-1.3B, 30-100B tokens shown) where long-context (>=1M) and continual learning matter.
- M3 as a drop-in optimizer for ViT and small/medium LMs when extra memory of long-past gradients is desired; cost is multiple momentum buffers.
- Prerequisites: chunk-wise parallel training infra similar to Titans / TTT (Sun 2024, Behrouz 2025c); ability to run Newton-Schulz orthogonalization; deep MLP memory blocks add parameters and ~Muon-class compute. Multiple momentum buffers => higher optimizer state RAM. No released weights or code in the paper itself.

## Novelty
Genuinely new framing rather than a single new trick. Closest prior work is the Behrouz/Google-Research thread (Titans 2025c, Miras 2025b, Atlas/DLA 2025a) plus Schmidhuber's self-referential weight matrix (1993) and Fast Weight Programmers (Schlag 2021). What's new vs Titans: (a) self-modification — K, V, eta, alpha, and the memory itself are all MLP associative memories that generate their own targets v̂ via M_box(v_t), trained with DGD; (b) Continuum Memory System replacing the FFN with a multi-frequency MLP chain; (c) explicit decomposition of Adam/Muon/Shampoo as nested associative memories, leading to M3. The general "architecture = optimization" view echoes deep-equilibrium, meta-learning-as-optimization (Akyurek 2022), and "Transformers learn in-context by gradient descent" (Von Oswald 2023), but pushed further into a unifying framework that absorbs hypernetworks, MAML, learned optimizers, and TTT as instances of "knowledge transfer between levels".

## Reproducibility
No code, weights, or paperswithcode entry mentioned in the captured PDF. Experiments depend on the Titans / Miras / Atlas codebase (Behrouz et al. 2025a/b/c); chunk-wise dual-form training procedure is referenced as identical to Sun et al. 2024 and Behrouz 2025c, both of which have partial open-source implementations in the community (Titans-PyTorch, etc.). Baseline numbers for RWKV-7, Comba, DeltaNet, RetNet, TTT, DLA, Titans are quoted from prior work; ablations are internal. Independent reproduction will require re-implementing self-modifying Titans + CMS from the equations.

## Adoption
NeurIPS 2025 acceptance + Google Research authorship suggests visibility. The Titans/Miras line is a deliberate research program from the same group (Behrouz et al.) that is increasingly cited in the modern-RNN / linear-attention community alongside Mamba, RWKV-7, DeltaNet, Comba. Too early at capture date (2026-04-22) to call it "widely adopted"; the paper itself is a synthesis flag rather than a community-adopted method. Worth tracking for follow-on Hope/CMS implementations and whether M3 lands in any open optimizer libs (vs Muon/AdaMuon momentum).

## Conflicts
The wiki currently has no substantive content pages (only `index.md` overview and `reference-sources.md`), so no contentful conflicts to flag. The paper does take positions that will conflict with future ingests if/when added:
- Claims "in-context learning is not emergent" — it is a direct consequence of having multiple NL levels (contradicts the Brown 2020 / Schaeffer 2023 emergent-capability framing).
- Claims test-time training and test-time memorization (Sun 2024; Wang 2025; Behrouz 2025b) are *just* parametric in-context learning and the train/test boundary is an artifact.
- Claims hybrid Transformer+SSM architectures are misleadingly described as "attention + RNN"; from NL they are Transformers with one extra computation level grafted onto MLP blocks.
- Reframes Adam as the optimal L2 associative memory for gradient-variance prediction — a stronger claim than the usual "adaptive learning rate" framing.
None of these contradict an existing wiki page yet.
<!-- /DOMAIN-SLOT -->

## Cross-ref candidates
- [[titans]] / [[behrouz-memory-line]] — direct lineage; Hope = self-modifying Titans + CMS. (Page does not yet exist; would need to be created.)
- [[modern-recurrent-architectures]] — parallels DeltaNet, RWKV-7, Comba, Mamba; Hope competes on the same benchmarks.
- [[continual-learning]] / [[catastrophic-forgetting]] — central claim is CMS reduces (not solves) catastrophic forgetting via multi-frequency memory.
- [[in-context-learning]] — paper redefines ICL as "any adaptation to a context flow at any level"; provides a non-emergent account.
- [[muon-optimizer]] / [[optimizers]] — derives Muon as polynomial mapping to orthogonal coordinate system; introduces M3 as multi-scale Muon+Adam.
- [[meta-learning]] / [[maml]] — MAML is a special case of NL knowledge transfer via initialization.
- [[hypernetworks]] — instance of NL "knowledge transfer via generation".
- [[fast-weight-programmers]] — direct ancestor (Schlag 2021, Schmidhuber 1992).
- [[test-time-training]] — paper subsumes TTT under parametric ICL.
- [[long-context-benchmarks]] — uses RULER NIAH and BABILong; Hope reaches 10M.
- [[scaling-and-emergence]] — paper argues against ICL-as-emergent.

## Conflict flags
- Claim: "In-context learning is the characteristic of having multiple nested levels ... per se it is not an emergent characteristic but a direct consequence of having multiple levels in the NL representation of the neural learning module."
  Contradicts: nothing currently in the wiki, but contradicts the standard Brown et al. (2020) / Wei et al. (2022) emergent-capabilities framing that future ingests are likely to reflect.
  Basis: Section 6, "In-Context Learning" subsection (around line 847-849 of the captured PDF).
- Claim: "Test-time training and test-time memorization are in fact instances of parametric in-context learning."
  Contradicts: nothing currently in the wiki; would conflict with any future page that frames TTT (Sun 2024) as a distinct paradigm.
  Basis: Section 6, "Test Time Training/Memorization are Instances of In-Context Learning" callout box.
- Claim: "Adam is the optimal associative memory with respect to the element-wise L2 regression objective" for compressing gradients.
  Contradicts: nothing yet; will conflict with future pages framing Adam purely as adaptive-LR / second-moment estimator without the AM lens.
  Basis: Section 1.2 ("Optimizers and Architectures as Learning Module") and Appendix B (Equation 101-102).

## Proposed page shape
- New page: **`research/nested-learning`** — overview of the NL paradigm, its three pillars (optimizers-as-AM, self-modifying memory, CMS), and the Hope architecture. One-stop entry that other pages link to.
- New page: **`research/hope-architecture`** — concrete spec of Hope and Hope-Attention (forward pass equations, chunk-wise parallel training, ablations), separated because it is the empirically evaluated artifact and likely to attract independent reimplementations.
- New page: **`optimizers/m3-multi-scale-muon`** — M3 algorithm (Algorithm 1), comparison to Muon/AdaMuon, ViT-21K results.
- New page: **`continual-learning/continuum-memory-system`** — CMS as an FFN replacement; nested vs sequential vs independent variants; ad-hoc level stacking from pretrained MLPs.
- Cross-link from a future **`optimizers/index`** page noting that backprop+Adam+Shampoo+Muon are all instances of nested associative memories (per NL).
- These four pages share the same source PDF and should each list it under `## Source` and link to each other in `## Related`.

Confirmation: wrote /home/david/code/wiki-ai-trends/raw/research/radar-2026-04/.ingest/04-nested-learning.summary.md. No truncation warning — full 1726-line source was read in chunks; only the references section beyond line ~1399 was skimmed (it is the bibliography).
