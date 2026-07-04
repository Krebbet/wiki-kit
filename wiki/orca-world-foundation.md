# Orca: The World is in Your Mind

Orca (BAAI, arXiv:2606.30534) is a general world foundation model (0.8B and 4B) that learns a unified world latent space from 125K hours of video and 160M event annotations using **Next-State-Prediction** — a unified modeling paradigm that replaces next-token, next-frame, and next-action prediction with explicit state-transition modeling. After pre-training, the backbone is permanently frozen; lightweight modality-specific decoders are attached and trained separately for text, image, and action readouts. On the PRICE-V0.1 real-world interaction benchmark Orca-4B scores 59.8±10.9 avg (vs. FLUX.2 [klein] 56.1±18.1 and FLUX.1-Kontext 40.9); on text generation it scores 51.8 avg across MVBench/TemporalBench/3DSRBench/SWITCH, beating all same-scale VLMs and all larger world models tested. Action generation on 5 real-robot OOD tasks surpasses π0.5 (32.4 vs. 29.4 avg rule-based) despite zero action-labeled data in pre-training — an emergent capability from video-only scaling.

## Method

**Encoder.** Built on a pre-trained Qwen3.5 VLM. Two pre-training paradigms operate jointly via learnable query vectors:

1. **Unconscious learning** (observation-only state transition): given frame v_t, Query 1 predicts the latent of the next adjacent frame v_{t+1} via a 2-layer MLP. Ground-truth latent from a frozen vision encoder. No labels. Captures dense physical regularities, motion, and natural dynamics.

2. **Conscious learning** (event-conditioned state transition): given v_t plus a language event description e_{t+Δ}, Query 2 predicts the latent of a target-event frame. Also includes standard VQA next-token prediction. Captures sparse, semantically meaningful transitions.

Pre-training loss: L = λ_obs·L_obs + λ_evt·L_evt + λ_vqa·L_vqa. All three components are necessary; ablations show removing any one degrades the corresponding readout disproportionately.

**Pre-training data:** 125K hours video (ego-centric interaction, exo-centric manipulation, action-free robot execution, natural dynamics) + 160M multi-level event annotations + 11.5M VQA pairs. Current experiments use only 1/10th of the video inventory; loss curves show no convergence plateau.

**Decoders (frozen backbone, trainable readout only):**
- Language: reuses the LM head directly.
- Vision: MLP adaptor + LoRA on frozen SD3.5 (multi-step denoising to pixel image).
- Action: MLP adaptor + DiT-based Action Expert (flow-matching, from scratch). Takes world latent, proprioception, and noisy action chunk; trained on 200 trajectories × 5 tasks.

Infrastructure: FlagScale with FSDP2, chunked cross-entropy loss, and FSDP allgather pre-fetching → 4.4× throughput vs. StarVLA baseline.

## Results

| Task | Orca-4B | Best baseline | Baseline size |
|------|---------|--------------|--------------|
| Text gen avg (4 benchmarks) | **51.8** | Qwen3.5-4B: 46.7 | 4B |
| Text gen avg (0.8B) | **40.8** | MiniCPM-V-4.6: 37.9 | 2B |
| Image pred PRICE-V0.1 avg | **59.8±10.9** | FLUX.2 [klein]: 56.1±18.1 | 4B+4B |
| Action gen avg (OOD) | **32.4** | π0.5: 29.4 | large, robot-pretrained |

Cross-benchmark capability gaps vs. Qwen3.5-4B: State Transition +12.27%, Commonsense Reasoning +5.19%, Dynamic Motion +8.52%, Spatial Relations +0.57%.

Scaling: pre-training loss decreases monotonically with data and model size (no plateau at 8K hours / 4B scale); all downstream readouts improve with more pre-training data.

## Limitations

- Vision + language only; no audio, tactile, force, or physical signals.
- State-transition supervision is event-level (minute-scale); no long-horizon modeling.
- ViT-space supervision target anchors the latent to a semantic embedding space rather than a native world space.
- Experiments limited to 0.8B / 4B; 4B shows readout trade-off as pre-training scales (language vs. vision vs. action compete for latent expressivity).
- Action tasks limited to short-horizon dual-arm manipulation (5 tasks, 200 trajectories each).
- Code not released.

## Source
- arXiv: 2606.30534
- Website: https://orca-wm.github.io
- Institution: Beijing Academy of Artificial Intelligence (BAAI)
- Captured: `raw/research/weekly-2026-07-04/05-orca-world-foundation.md`

## Related
- [[conflicts/pure-video-vs-3d-world-models]] — Orca's PRICE-V0.1 and action results are Position B evidence: pure video+language latent learning achieves competitive/best-in-class interactive world prediction without 3D representations.
- [[cosmos-3]] — NVIDIA omnimodal world model; both target general world modeling but Cosmos 3 uses a 3D-grounded dual-tower architecture vs. Orca's pure latent prediction.
- [[moonlake-world-models]] — Moonlake argues pure video cannot yield interactive simulators; Orca's real-world interaction results are directly relevant (though Orca is JEPA-style latent, not video diffusion).
- [[qwen-agentworld]] — Both use frozen Qwen-series VLMs as backbone; Qwen-AgentWorld targets agentic simulation, Orca targets physical world modeling.
- [[lejepa]] — JEPA-style latent prediction directly precedes Orca's unconscious learning paradigm.
