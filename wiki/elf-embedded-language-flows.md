# ELF: Embedded Language Flows

MIT (Kaiming He et al.). Continuous diffusion LM operating entirely in continuous embedding space via Flow Matching, discretizing only at the final step (t=1) through a shared-weight denoiser-decoder. ELF-B (105M) achieves Gen.PPL ~24 at 32 steps on OpenWebText — beating discrete DLMs MDLM (~60+) and Duo (~50+) and all evaluated continuous DLMs at the same step budget, including distilled variants MDLM+SDTT and Duo+DCD — using 45B training tokens vs ~550B+ for baselines (10× fewer). WMT14 De-En BLEU 26.4 (vs AR 25.2, MDLM 18.4, Duo 21.3); XSum R1/R2/R-L 36.0/12.2/27.8 (vs AR 30.5/10.2/24.4). No distillation, no separate decoder, no per-step discrete supervision.

## Method

Continuous-time Flow Matching (rectified flow lineage: Lipman, Liu) over contextual embeddings. Tokens encoded via frozen pretrained T5-small (35M, dim 512, bottlenecked to 128). Single transformer `net_θ` with shared weights trained on two interleaved objectives:

- **MSE denoising** (x-prediction, 80%): continuous embedding-space regression.
- **Cross-entropy decoding** (20%): applied only at a special final-step corruption; discretization through unembedding matrix W at t=1 only.

CFG adapted to language via **self-conditioning** (intermediate embedding prediction as conditioning signal; single forward pass, zero inference overhead) — novel in this model class (from Chen; image-domain training-time CFG from Zheng, Dao). SDE-inspired sampling (small per-step noise injection) outperforms ODE in few-step regime. No separate decoder at inference.

Sizes: ELF-B 105M / ELF-M 342M / ELF-L 652M. Training: TPUs (Google TRC), Muon optimizer, lr=2e-3, batch 512.

## Results

| Task | Metric | ELF-B | AR baseline | MDLM | Duo |
|---|---|---|---|---|---|
| OpenWebText uncond. | Gen.PPL @32 steps | ~24 | — | ~60+ | ~50+ |
| WMT14 De-En | BLEU | **26.4** | 25.2 | 18.4 | 21.3 |
| XSum | R1/R2/R-L | **36.0/12.2/27.8** | 30.5/10.2/24.4 | 33.4/11.6/25.8 | — |

Scaling improves Gen.PPL–entropy frontier (Fig 6). Beats distilled discrete DLMs in few-step regime without distillation (Fig 7b). 10× training-token efficiency over baselines (Fig 7c).

## Novelty

Key architectural contribution: **shared-weight denoiser-decoder** that repurposes the flow's final time step as the discrete decoder, keeping the entire trajectory continuous while eliminating a separate decoder module. Prior continuous DLMs either (a) apply per-step CE supervision tying trajectory to discrete space (Diffusion-LM, CDCD, DiffuSeq, FLM, LangFlow) or (b) use separate decoders (LD4LG line). "Discretize only at t=1" is the distinguishing structural choice. CFG via self-conditioning in this class is also novel. Closest prior: FLM/FMLM, LangFlow (concurrent, per-step CE supervision).

Central positioning claim: a properly designed *continuous* DLM can match or beat *discrete* DLMs — challenges prevailing community consensus. Not currently contradicted by any wiki page in this collection.

## Positioning vs [[coladlm]]

ELF and [[coladlm]] are parallel, not contradictory, continuous-latent diffusion-LM approaches attacking the same open problem from different angles:

- **CoLa-DLM**: causal Text VAE → block-causal DiT prior → separate decoder; emphasis on compute-optimal scaling with compressed latents.
- **ELF**: direct embedding-space Flow Matching with a shared-weight denoiser-decoder; no compression VAE, no separate decoder; emphasis on data efficiency and few-step generation quality.

The two differ on compression strategy (explicit VAE bottleneck vs. frozen encoder embeddings), decoder architecture (separate vs. shared-weight), and scaling emphasis (FLOPs/token efficiency vs. token efficiency).

## Reproducibility

Code: https://github.com/lillian039/ELF. Preprint: arXiv:2605.10938 (2026-05-18). Weights not confirmed released. No paperswithcode entry. WMT14/XSum baselines reproduced from public codebases (‡ in Table 1). Concurrent with FLM, LangFlow, DFM, CFM (mutual citations).

## Source

`raw/research/weekly-2026-05-18/01-elf-embedded-language-flows.md` (arXiv:2605.10938)

## Related

- [[coladlm]] — parallel continuous-latent DLM; causal VAE + DiT prior + separate decoder; compute-optimal scaling
- [[tidar]] — discrete diffusion LM; different lineage, relevant for discrete vs. continuous comparison context
- [[latent-grpo]] — latent-space RL for language; orthogonal method, overlapping interest in continuous latent language representations
