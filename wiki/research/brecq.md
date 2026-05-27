# BRECQ: Pushing the Limit of Post-Training Quantization by Block Reconstruction

BRECQ is a post-training quantization framework that optimizes weight rounding block-by-block using a Fisher-weighted output-distortion objective, achieving INT2 PTQ quality competitive with quantization-aware training using only 1024 calibration images. The headline result — ResNet-18 W2 at 66.3% top-1 versus AdaRound's 55.96% — establishes block-granularity reconstruction as the correct operating point for PTQ. The core theoretical insight is that the full-network Hessian overfits with few samples, while the layer-diagonal Hessian ignores intra-block cross-layer dependencies; block-diagonal is the empirically optimal middle ground.

## Method core

No architectural change to the target model — BRECQ is a calibration algorithm that runs on a frozen pretrained network. It operates on one block at a time, minimizing the output discrepancy between the quantized block and the FP block, weighted by a diagonal Fisher Information Matrix (FIM) approximation of the output Hessian.

The objective for block $\ell$ (spanning layers $k$ through $\ell$) is:

$$
\min_{\hat{\mathbf{w}}} \mathbb{E}\!\left[\Delta \mathbf{z}^{(\ell),\mathsf{T}}\,\operatorname{diag}\!\left(\left(\tfrac{\partial L}{\partial \mathbf{z}_1^{(\ell)}}\right)^{\!2},\ldots,\left(\tfrac{\partial L}{\partial \mathbf{z}_a^{(\ell)}}\right)^{\!2}\right)\Delta \mathbf{z}^{(\ell)}\right]
$$

where $\Delta \mathbf{z}^{(\ell)} = \mathbf{z}^{(\ell)} - \hat{\mathbf{z}}^{(\ell)}$ is the output discrepancy and the diagonal FIM weights each output channel by its squared gradient, acting as a channel-importance mask. This is a Gauss-Newton approximation to the task loss Hessian, restricted to the block-diagonal structure.

Weight rounding is learned via AdaRound (learnable floor/ceil per weight). Activation quantization scales are learned via LSQ-style STE. Mixed precision is handled post-hoc: a genetic algorithm searches over $\mathbf{c} \in \{2,4,8\}^n$ using pre-computed per-layer Fisher sensitivities, subject to a hardware latency/size budget $H(\mathbf{c}) \le \delta$.

The "block" granularity is architecture-defined (ResNet bottleneck, MobileNetV2 inverted residual). Layers outside block boundaries (first conv, final FC) fall back to layer-wise reconstruction. BN statistics are folded and frozen before calibration begins.

## Goal relevance

- `G1` — **Direct and strong.** BRECQ's inner loop is precisely "optimize this block in isolation to match the FP block's outputs; advance to the next block." This is the strongest empirical validation in the PTQ literature that a block can be calibrated in isolation given fixed inputs from its neighbours, then re-inserted into the full stack without cascading error. The block-diagonal Hessian approximation is the theoretical justification: intra-block weight dependencies matter, inter-block dependencies can be ignored without significant accuracy loss. The wiki owner's G1 experiment (isolated block training + re-insertion) is structurally identical to BRECQ's calibration loop — BRECQ establishes the lower-bound on what such isolation can achieve.

- `G2` — **Indirect / relevant.** The mixed-precision extension (Section 3.4) learns per-block and per-layer bitwidth allocations driven by block-level Fisher sensitivity, which functions as a learned parameter-budget signal per block. Conceptually adjacent to dynamic parameter allocation, though expressed as bitwidth rather than parameter count.

- `background` — The second-order analysis (Gauss-Newton / Fisher approximation, block-diagonal Hessian) provides the theoretical framing for why block-level isolation works at all, and when cross-block gradient signal is expected to matter. Relevant background for reasoning about inter-block dependency in architectures with long-range attention.

## Credibility

- Venue / year: ICLR 2021 (arXiv 2102.05426)
- Code released: yes — https://github.com/yhhhli/BRECQ
- Weights released: no (calibration runs in 0.4–3.2 GPU-hours; models not distributed)
- Ablation rigor: **strong** — Table 1 directly ablates layer / block / stage / network granularity on two architectures with variance; first/last-layer sensitivity and calibration set size ablated in Appendix B.1, B.2
- Replication status: well-cited in PTQ literature; independently reproduced and extended in follow-on work (ADAROUND+ variants, Q-BERT derivatives)

## Empirical claims

**Weight-only quantization (activations FP), ImageNet top-1:**
- ResNet-18 W4: 70.70% (FP: 71.08%; AdaRound: 68.71%; gap 0.38pp)
- ResNet-18 W2: 66.30% (AdaRound: 55.96%; +10.3pp — first viable INT2 PTQ result)
- MobileNetV2 W2: 59.67% (AdaRound: 32.54%)

**Fully quantized (W/A), ImageNet top-1:**
- ResNet-18 4W4A: 69.60% (PACT QAT: 69.2%, DSQ QAT: 69.56% — both require full 1.2M-image dataset and ~100 GPU-hours vs. 0.4 GPU-hours for BRECQ on 1024 images)
- MobileNetV2 4W4A: 66.57% (PACT: 61.40%, DSQ: 64.80%)
- ResNet-18 2W4A: 64.80% (all other PTQ methods collapse to ~0.1%)

**Object detection, MS COCO:**
- Faster-RCNN ResNet-50 4W8A: 38.29 mAP (FP: 38.55; <0.3 mAP degradation)
- Faster-RCNN ResNet-50 2W8A: 34.23 mAP (AdaRound: 19.63)

**Hardware / compute:** 1024 calibration images; single GTX 1080Ti; ResNet-18 quantization in ~20 minutes. Adam, $2\times10^4$ iterations per block, lr=$10^{-3}$.

## Open questions / failure modes

- **Transformer applicability not demonstrated.** All experiments are CNNs. Transformer blocks (attn → MLP with two residual paths) have different inter-layer dependency structure; whether the block-diagonal Hessian approximation holds as tightly is an open empirical question.
- **Calibration data dependency.** 2-bit accuracy improves ~5pp as calibration set grows; ZeroQ-style distilled data underperforms real data significantly at W2 — not fully data-free at low bitwidth.
- **No W2A2.** 2W4A demonstrated; 2W2A not viable with this method.
- **Block granularity is architecture-defined, not learned.** No mechanism to discover optimal reconstruction granularity automatically; architectures without clear block boundaries fall back to layer-wise.
- **Mixed precision search is post-hoc and approximate.** Genetic algorithm over pre-computed sensitivity lookup table; joint optimisation of bitwidth and rounding policy is not performed.
- **Inter-block dependency entirely ignored by design.** Empirically acceptable for CNNs; no guarantee for architectures with global receptive fields (e.g., full-sequence attention spanning all blocks).

## Source

- raw/research/block-training-quantization/21-brecq.md (PDF capture, marker engine)
- raw/research/block-training-quantization/01-brecq-abs.md (arXiv abstract page)

## Related

- [[block-isolation-training]] — concept anchor; BRECQ's block-by-block reconstruction is the strongest empirical case for the G1 isolation principle
- [[gptq]] — leading PTQ baseline; both block-sequential, GPTQ uses Hessian for weight rounding, BRECQ uses Fisher-weighted output reconstruction
- [[awq]] — alternative PTQ via activation-aware scaling, no reconstruction
- [[omniquant]] — block-wise SGD-learned clipping + equivalent transforms; direct lineage from BRECQ
- [[spinquant]] — learned rotations; layered on top of GPTQ-style weight quantization
- [[adaround]] — direct predecessor: layer-wise rounding optimization that BRECQ extends to block granularity
- [[fisher-information-matrix]] — theoretical backbone of the second-order error analysis
