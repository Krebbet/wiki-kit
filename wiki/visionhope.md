# VisionHOPE

VisionHOPE (Peng, Zhang et al., CASIA/UCAS/Mininglamp, arXiv 2609.33325, Sept 2026) is a generic visual backbone built on the self-referential HOPE construction from [[nested-learning]]. Each scan holds five coupled within-image linear memories (content, key, value, learning-rate, retention) updated by retained Delta Gradient Descent, with a provably non-expansive step-size control. It matches or slightly beats CNN/ViT/SSM/TTT backbones on ImageNet-1K, COCO and ADE20K at cost linear in token count. Gains over the closest baseline (H-ViT^3, a TTT model) are about 0.0-0.3 pp at most scales, with no seeds or variance reported.

## Method

- Derives from [[nested-learning]] (associative memory, Delta Gradient Descent (DGD), self-referential HOPE). [[titans-miras]] is cited as related work.
- The per-scan SRNL module holds five linear memories: content M^m (d x d), key M^k, value M^v (d x d), and row-vector learning-rate m^eta and retention m^alpha (1 x d). Then k_t = M^k x_t, v_t = M^v x_t, eta_t = phi(m^eta x_t), alpha_t = phi(m^alpha x_t).
- Each memory generates its own target (v^ = M^box v_t) and updates by retained DGD with an L2 objective (SR-DGD): M_t = M_{t-1}(alpha_t I - eta_t k_t k_t^T) - eta_t g_t k_t^T. W_q stays outer-parameterized and reads from the content memory. The memories are linear L2 recurrences, whereas original HOPE used MLP memories.
- **Stability problem:** the self-referential update has no non-expansion guarantee.
- **Stability-matched step-size control:**
  - L2-normalize keys.
  - Apply a soft injection cap, eta_inj = (1-alpha)/r_t, with eta_bar = eta_inj(1 - exp(-eta/eta_inj)).
  - Apply a spectral clamp, eta_spec = alpha/||k||^2, and use eta~ = min(eta_bar, eta_spec).
  - This gives ||A_t|| <= alpha_t and ||B_t|| < 1-alpha_t, hence ||T_t|| < 1 and ||M_t||_F <= ||M_{t-1}||_F. The proof extends to chunk-boundary states.
- **2D adaptation:** NL chunking is aligned to image rows/columns across four VMamba-style directional scans. Chunk length is W for row-major scans and H for column-major scans. Each direction has its own SRNL with learned initial states. Outputs are fused with learned channel-wise scales.
- **Block:** Norm -> Proj_in -> DWConv -> VisionHOPE operator -> Proj_out, plus an FFN, in two pre-norm residual branches. Variants are hierarchical (-T/-S/-B) and plain (P-VisionHOPE).

## Results

All models trained from scratch on ImageNet-1K.

- **ImageNet-1K, hierarchical, 224px, Top-1:**

  | Model | Top-1 | Params / FLOPs | Closest baseline |
  |---|---|---|---|
  | -T | 84.1 | 27M / 4.9G | ties RMT-S 84.1; H-ViT^3-T 84.0 |
  | -S | 85.2 | 53M / 9.8G | H-ViT^3-S 84.9; RMT-B 85.0 |
  | -B | 85.6 | 91M / 17.3G | H-ViT^3-B 85.5; RMT-L 85.5; VSSD-B 85.4 |

  Margins over the best baseline are 0.0-0.3 pp.
- **Plain models:**
  - P-VisionHOPE-T 78.4 (6M) vs Vision-TTT-T 77.7.
  - P-VisionHOPE-S 82.3 vs ViT^3-S 81.6 and Vision-TTT-S 81.8.
  - P-VisionHOPE-B 83.4 vs Mamba-R-B 83.0 and ViT^3-B 82.6.
  - Gains are larger here, 0.4-0.8 pp.
- **COCO (Mask R-CNN 1x), box AP / mask AP:** 47.9/43.1 (T), 49.5/44.2 (S), 50.5/45.0 (B). B ties MILA-B and beats H-ViT^3-B (50.0/44.6).
- **ADE20K (UPerNet) mIoU:** 49.4 (T) vs H-ViT^3-T 48.0; 50.3 (S) vs 50.2; 51.8 (B) vs 51.7. The gain is large only at -T.
- **Efficiency (A100, BF16, batch 8, 224-1280px):** linear in N like Vim, quadratic for DeiT. P-VisionHOPE-B at FLOPs similar to Vim-B has higher throughput and lower memory. Figure annotations read roughly 4.42x throughput, -52.8% FLOPs and -94.6% memory at the highest resolution. **These figures are approximate: the labels were partly garbled in extraction.**
- **Ablations (P-VisionHOPE-S, full 82.3):**

  | Ablation | Result |
  |---|---|
  | no adaptive K/V and no adaptive dynamics | 81.7 |
  | no DGD | 81.9 |
  | no soft injection cap | NaN divergence |
  | no spectral clamp | 82.3 (no change; very low activation rate) |
  | hard injection clamp | 81.8 |
  | soft spectral cap | 81.9 |
  | 1-way scan | 81.6 |
  | 2-way scan | 81.9 |
  | 4-way fixed-sum | 82.1 |
  | shared initial states | 82.0 |

## Applicability

- Candidate for vision backbone work that wants a linear-cost, attention-free alternative to ViT/Vim, especially high-resolution dense prediction.
- The stability-matched step-size control is a transferable trick for any self-referential or fast-weight recurrence where the memory generates its own step sizes or targets, including NL/Titans/HOPE language models. The soft injection cap is mandatory (NaN without it). The spectral clamp rarely fires.
- Prerequisites: a VMamba-style multi-direction scan implementation and chunked DGD kernels.

## Novelty / caveats

- **Recombination and transfer.** It ports HOPE's self-referential memory to vision (linear L2 memories instead of MLPs), adds a new non-expansion stability result, and adds row/column-aligned chunking over four scans.
- **Delta vs prior work:**
  - Vision-TTT and ViT^3 ([[test-time-training]]) adapt an inner learner, but their representation maps and update rule are outer-parameterized.
  - VMamba/Vim use a fixed token-to-transition mapping.
  - Here key, value, learning rate and retention are themselves evolving within-image memories.
- **Gains are marginal against the closest baseline.** H-ViT^3 (TTT) is the closest baseline, and several gaps are <=0.3 pp with no seeds or variance reported. "Best or tied-best in every panel" is accurate but the margins are small. Plain-model and ADE20K-T gains are larger.
- Pretraining is ImageNet-1K only, with no large-scale pretraining or comparison to modern foundation backbones.
- The "first generic visual backbone as self-modifying learning system" claim is self-asserted.
- Efficiency numbers come from a single A100 and are approximate (garbled extraction).
- Fresh preprint with no third-party uptake visible.

## Reproducibility

- Code: github.com/PSRben/VisionHOPE (linked in the abstract). Weights are not mentioned in the visible text.
- Configs, training protocols and extra results are in appendices C.1-C.6. The ingest read a truncated source (mostly references and appendices), so those details are unverified here.
- Hardware measurements are on a single A100.

## Source

- raw/research/weekly-2026-10-03/04-visionhope-self-modifying-backbone.md (arXiv 2609.33325)

## Related

- [[nested-learning]] - parent framework; VisionHOPE is its first vision instantiation, with linear memories and an added stability fix.
- [[titans-miras]] - associative-memory-as-optimizer lineage.
- [[test-time-training]] - the TTT cluster (ViT^3, H-ViT^3, Vision-TTT) that VisionHOPE is compared against.
- [[in-place-ttt]] - LLM-side fast-weight adaptation.
- [[gated-deltanet-2]] - same delta-rule family with decoupled gates.
- [[mamba-3]] - SSM-side successor; vision Mamba variants are baselines.
- [[conflicts/ttt-distinct-vs-parametric-icl]]
- [[conflicts/ssm-vs-associative-memory-taxonomy]]
- [[conflicts/fixed-state-ssm-long-context]]
- [[watchlist]]
