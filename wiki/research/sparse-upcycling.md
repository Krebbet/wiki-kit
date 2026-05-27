# Sparse Upcycling: Training Mixture-of-Experts from Dense Checkpoints

Given a pretrained dense transformer, sparse upcycling replaces each of a chosen subset of MLP layers with a pool of $E$ identical expert copies plus a randomly-initialised router, then resumes training from the modified checkpoint. The resulting MoE outperforms both dense continuation and MoE-from-scratch at any compute budget below roughly 100% of the original dense pretraining cost, establishing copy-and-train as a compute-efficient bootstrap for expert pools and providing a clean canonical instance of per-token learned routing through a block pool.

## Method core

**Structural surgery.** A subset of MLP layers (default: half) are expanded into MoE layers. All other parameters — layer norms, attention, embeddings, output head — are copied verbatim from the checkpoint.

**Expert initialisation.** Each expert in a new MoE layer is an identical copy of the original MLP weights. With $E$ experts per layer ($E = 32$ default), the original MLP is replicated $E$ times. Adding independent Gaussian noise to the copies at init was tested and found neutral-to-harmful; expert diversity emerges through routing pressure, not forced perturbation.

**Router initialisation.** The router is the *only* newly randomly-initialised parameter — it receives no warm start from the checkpoint.

**Continued training.** Training resumes using the original hyperparameters (learning rate schedule, batch size, weight decay). Optimizer state from the dense checkpoint can optionally be resumed; this helps vision models, provides no benefit for language models.

**Routing variant.** The choice of routing scheme is conditioned on inference regime:

- **Expert Choice** (encoder / vision): each expert selects the top-$T$ tokens from the full batch, $T = C \cdot n / E$ with capacity factor $C = 2$ default. Outperforms Top-$K$ on a per-compute-time basis for encoders.
- **Top-$K$ token routing** ($K = 2$, decoder): avoids train/inference distribution mismatch between batch teacher-forcing and autoregressive single-token generation, where Expert Choice is inapplicable.

The Expert Choice formulation can be read as the dual of Top-$K$: instead of each token selecting $K$ experts, each expert selects $T$ tokens, enforcing exact load balance by construction.

## Goal relevance

**G1 — swappable isolated blocks.** The upcycling recipe is precisely "replace an MLP block with a pool of alternatives and train." Copy-init experts demonstrably beat random-init experts at limited compute, confirming that a block pool benefits from a warm shared starting point. The original MLP weights survive and differentiate under routing pressure without catastrophic forgetting, validating [[block-isolation-training]] as a viable G1 bootstrap strategy.

**G2 — dynamic per-block parameter allocation.** Ablations over number of MoE layers, $E$, and $C$ constitute an empirical map of per-block capacity allocation. More upcycled layers and more experts improve quality but also deepen the initial quality dip and raise runtime; $(E=32, C=2, \text{half-layers})$ is a robust operating point across scales.

**G3 — token-conditional routing.** Top-$K$ / Expert Choice routing through a per-layer expert pool is the canonical G3 primitive. Routing emerges purely from the randomly-initialised router trained under continued training — no handcrafted routing signal. This paper and [[token-conditional-routing]] jointly anchor G3 in this literature batch.

## Credibility

- **Venue / year:** ICLR 2023 (arXiv 2212.05055, December 2022)
- **Authors:** Google Research — Komatsuzaki, Puigcerver, Lee-Thorp, Riquelme, Mustafa, Ainslie, Tay, Dehghani, Houlsby
- **Code:** vision — `github.com/google-research/vmoe`; language — `github.com/google-research/t5x/tree/main/t5x/contrib/moe`
- **Ablation rigor:** strong — router type, number of MoE layers, $E$, $C$, expert init (copy / random / copy+noise), optimizer state reuse, router weight normalisation, amount of dense pretraining at start of upcycling; both vision and language modalities
- **Scale:** T5-Base/Large/XL (SuperGLUE); ViT-B/32, B/16, L/32, L/16 (ImageNet)
- **Replication risk:** low — two independent codebases, two modalities, multiple scales, results consistent; strong alignment with [[v-moe]] and [[switch-transformer]] prior art

## Empirical claims

- Upcycled T5-Large and T5-Base outperform dense continuation by 1.5–2 absolute points on SuperGLUE using only 46% and 55% additional compute (relative to original dense pretraining cost), respectively.
- ViT-B/16 ImageNet 10-shot: reaching +1% accuracy over the dense checkpoint requires 58% extra training via dense continuation but only 13% via sparse upcycling.
- MoE-from-scratch requires ~120% of the original dense budget to match the upcycled model on language; upcycling dominates at any budget below ~100%.
- Dense upcycling (depth tiling / warm-started deeper dense) improves faster initially but plateaus below sparse upcycling on both per-step and per-compute-time bases.
- Expert init ablation: random-init experts underperform copy-init at limited budget; both converge at ~100% additional compute.
- Copy + noise: small noise has negligible effect; large noise hurts; init perturbation does not substitute for training-driven diversity.
- Expert Choice beats Top-$K$ per train-time for the encoder (roughly matched per step; Top-$K$ is slower in wall-clock).
- Gains are consistent regardless of how converged the original dense checkpoint is (ablated across multiple ViT-B/16 dense checkpoints).

## Open questions / failure modes

- **Large compute regime.** At > ~100% of the original dense training budget, MoE-from-scratch begins to close or overtake the upcycled model. Upcycling is compute-efficient, not unconditionally superior.
- **Expert collapse / diversity.** The paper shows experts differentiate under routing pressure but does not quantify expert utilisation or load balancing beyond the capacity factor. Whether experts genuinely specialise or remain near-identical at convergence is uncharacterised.
- **Decoder routing mismatch.** Top-$K$ routing in the decoder is a workaround, not a principled solution; Expert Choice is incompatible with autoregressive single-token inference. A token-conditional routing scheme that works at inference time without this mismatch is left as future work.
- **Noise non-benefit.** Why copy+noise fails where ensemble perturbations often help is not explained mechanistically.
- **Heterogeneous expert shapes.** All experts are assumed identical MLPs. Block-pool architectures with heterogeneous expert designs are unexplored.
- **MoE layer placement.** The sensitivity to the within-model placement pattern of upcycled layers is not fully ablated (language: interspersed; vision: last-few-blocks).
- **Single-seed language ablations.** Some language ablation configurations appear to use single seeds; variance is not reported.

## Source

- `raw/research/selective-replacement-and-training/19-sparse-upcycling.md` (PDF capture)
- `raw/research/selective-replacement-and-training/06-sparse-upcycling-abs.md` (arXiv abstract)

## Related

- [[btx]] — cousin: Branch-Train-MiX trains branches independently then merges into an MoE, vs. Sparse Upcycling which copies then routes; both are upcycling-adjacent
- [[btm]] — pre-BTX context
- [[demix]] — domain-conditioned expert activation (experts activated by domain posterior rather than per-token learned router); deterministic vs. learned contrast
- [[mod]] — Mixture-of-Depths: routes tokens to *skip layers* (depth-conditional) rather than to expert pools (width-conditional); complementary G3 mechanism
- [[block-isolation-training]] — copy-and-train as a block-pool bootstrap; sparse upcycling is the strongest empirical evidence for this G1 strategy
- [[token-conditional-routing]] — primary G3 instantiation in this literature batch; Expert Choice and Top-$K$ routing here should populate the per-token-router taxonomy
- [[modular-deep-learning]] — survey context
- [[switch-transformer]] — queued; canonical MoE-from-scratch baseline that sparse upcycling outperforms at limited budget
- [[v-moe]] — queued; vision MoE from which the vision upcycling setup (BPR, Expert Choice) derives; sparse upcycling as V-MoE warm-started from dense ViT
