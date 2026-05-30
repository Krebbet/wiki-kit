# Vision Banana: Image Generators are Generalist Vision Learners

Google DeepMind (arXiv:2604.20329, 2026-04-23). Lightweight instruction-tuning of a pretrained image diffusion model (Nano Banana Pro) on a small mixture of vision-task data, with all outputs recast as RGB images via decodable encodings, yields **zero-shot SOTA** generalist vision: beats SAM 3 on segmentation, Depth Anything V3 on metric depth, Lotus-2 on surface normals — all without specialist heads, custom losses, camera intrinsics, or sacrificing generation quality. Frames image-generation pretraining as the visual analogue of LLM pretraining: a generalist substrate that lightweight instruction-tuning can specialize.

## Method

The recipe is a generation-as-perception cast: every dense-prediction task is reformulated as RGB output that the prompt itself specifies how to decode.

- **Segmentation.** Per-category color fields specified via natural-language color maps in the prompt. Inverse trivially maps colors back to category masks.
- **Metric depth.** Bijective power-transform → RGB-cube-edge encoding (Barron 2025 power transform with λ=−3, c=10/3, then a Hilbert-style edge-walk through RGB space). Inverse recovers metric depth without camera intrinsics.
- **Surface normals.** Direct RGB mapping (xyz → RGB).

Training: instruction-tune Nano Banana Pro on a small vision-task mix added at low ratio to its original training distribution. No architectural change, no custom loss, no specialist head. Derives from Marigold (Ke 2024) / Lotus (He 2024) "diffusion-for-perception" lineage but uses (a) a far stronger base generator and (b) a strict prompt-decodable output format that enables direct metric benchmark scoring.

## Results

**Segmentation (Tables 2a–2d, zero-shot):**
- Cityscapes semantic mIoU **0.699** vs SAM 3 0.652 (+4.7 pp).
- RefCOCOg UMD val referring cIoU **0.738** vs SAM 3 Agent 0.734.
- ReasonSeg val gIoU **0.793** vs SAM 3 Agent 0.770.
- SA-Co/Gold instance pmF1 0.540 vs DINO-X 0.552 (on par; SA-Co not in training mix).

**Metric depth (Table 3, zero-shot, no intrinsics):**
- Avg δ1 across NYU/ETH3D/DIODE-Indoor/KITTI: **0.929** vs Depth Anything V3 0.918.
- Avg δ1 across 6 datasets: **0.882** vs UniK3D 0.823 (+6 pp), MoGe-2 0.802 (+8 pp).
- AbsRel 0.116 vs MoGe-2 0.144 (−20% relative).

**Surface normals (Table 4):** NYU mean angle error **15.549°** vs Lotus-2 16.558°; median 9.300° vs DSINE 10.190°. 3-dataset avg 18.928° vs Lotus-2 19.642°.

**Generation retention:** GenAI-Bench text-to-image win-rate vs unmodified NBP **53.5%** (slight improvement); ImgEdit editing win-rate 47.8% (effectively tied). Critical: dense-prediction instruction-tuning did *not* damage generation, where prior full-finetune approaches did.

Base model scale not disclosed (closed Google model).

## Why this matters

Vision Banana is the strongest empirical evidence to date that 2D image-generation training implicitly encodes structured 3D priors — depth and surface normals are recoverable to within margin of dedicated specialist models. The δ1=0.929 depth result without camera intrinsics is the load-bearing data point, because it shows the generator has internalized a metric notion of scene structure, not just a relative one.

This pushes back partially on [[moonlake-world-models]]'s position that pure 2D generative pretraining cannot capture 3D structural understanding ([[conflicts/pure-video-vs-3d-world-models]]). The push-back is **partial** — Moonlake's claim is specifically about *interactive* simulation (action-conditioned rollouts, object permanence under occlusion); Vision Banana shows static 3D priors. But the static-prior result is a necessary precondition for the harder interactive claim, and the strength of it (+6-8 pp δ1 over specialist models) is hard to dismiss as "incidental." Co-listed with World-R1 and PERSIST on the watchlist, the 3D-from-pixels camp now has three new entries this month.

Vision Banana is also a counter-paradigm to [[lejepa]]: LeJEPA argues SSL with isotropic-Gaussian regularization is the right route to a generalist vision substrate; Vision Banana argues *generative* pretraining is. Both make the discriminative-from-substrate move; the question is which substrate.

## Reproducibility

No code or weights released at capture date. Project page: vision-banana.github.io. Method is described precisely enough — power-transform + Hilbert-edge depth encoding (Eq. 1, λ=−3, c=10/3), surface-normal RGB mapping, prompt formats — that an open-base reproduction (FLUX, Stable Diffusion 3) is feasible. Real-world reproducibility gated on whether weaker open bases retain the 3D priors at usable strength.

## Source

- `raw/research/weekly-2026-05-04/03-vision-banana.md` — arXiv:2604.20329.

## Related

- [[moonlake-world-models]] — partial counter-position; Vision Banana is the strongest empirical evidence that 2D generative priors carry static 3D structure (depth, normals).
- [[sharp-view-synthesis]] — SHARP claims feedforward regression Pareto-dominates diffusion for nearby-view single-image 3D; Vision Banana pushes back on the diffusion side via metric depth from a generation-trained base.
- [[lejepa]] — alternative paradigm for generalist vision: SSL via isotropic-Gaussian regularization vs generative pretraining.
- [[conflicts/pure-video-vs-3d-world-models]] — extended this run with Vision Banana as partial Position B (static 3D priors from 2D generation).
- [[conflicts/regression-vs-diffusion-view-synthesis]] — adjacent debate, different scope (view synthesis vs dense prediction).
- [[watchlist]] — Marigold, Lotus / Lotus-2, Diception, SAM 3, Depth Anything V3, UniK3D, MoGe-2, DSINE referenced as baselines.
