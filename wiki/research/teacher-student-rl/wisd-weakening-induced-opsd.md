# WISD: Weakening-Induced On-Policy Self-Distillation (Wu, Han, Cai; MIT/NVIDIA)

WISD reverses the OPSD recipe: instead of building a stronger self-teacher from privileged context, it keeps the original model $\pi_0$ as the strong member and builds a weaker copy $\pi_w$ by training-free low-bit quantization (RTN, 3-bit) or magnitude pruning ($\tau=1/6$). It then distills the token-level contrast $\log\pi_0-\log\pi_w$ on $\pi_0$'s own cached rollouts of unlabeled prompts, with no verifier, labels, or privileged information. Claims +4.0 (quant) / +5.5 (prune) pp average over five reasoning models on AIME24/25, HMMT25, LCB v5/v6. arXiv:2610.38681; code: github.com/jet-ai-projects/WISD.

Note: read from an ingest summary; appendices were not read directly.

## Method

- **Contrast:** $r_w(a|s)=\log\pi_0(a|s)-\log\pi_w(a|s)$ (Eq. 3). Tilted target $q_w\propto\pi_0\exp(r_w/\alpha)$ (Eq. 4); loss $\alpha\,\mathbb{E}_{s\sim d_{\pi_0}}\mathrm{KL}(\pi_\theta\Vert q_w)$ (Eq. 5), reverse KL, $\alpha=2$.
- **Offline (DOPD-style):** $\pi_0$ rolls out once (4 responses/prompt), frozen pair $(\pi_0,\pi_w)$ scores and caches supervision, student (init $\theta_0$) trains on the cache. Despite the name, rollout states are fixed $d_{\pi_0}$, not the evolving student.
- **Weakening:** attention/FFN (and MoE expert) projections only, group size 128; no calibration data. lr 1e-6, batch 64. 3,200 prompts per domain (SkyworkOR1 math, Klear-Reasoner code), separate math and code students.

## Results

| Result | Number |
|---|---|
| Models | Qwen3-4B, Qwen3.5-4B, OLMo-3-7B-Think, Qwen3.6-27B, Qwen3.6-35B-A3B |
| Avg gain | +4.0 (quant) / +5.5 (prune) pp; positive in 21 / 23 of 25 cells |
| Qwen3.5-4B 5-bench avg | 55.95 -> 67.23 (quant) / 69.34 (prune); HMMT25 57.7 -> 70.5, LCB v6 39.1 -> 56.7 (prune) |
| Qwen3.6-27B | prune +5.2 (76.58 -> 81.76); quant slightly negative (76.29) |
| Qwen3-4B 5-bench avg (prune) | 58.60 vs OPSD 52.70, SDPO 49.88, base 55.98 (baselines copied from papers, not re-run) |
| Controls (self-enhancing, T=2 weak) | stay near base (AIME24 72.8 / 73.1 vs 73.4): not just confidence reinforcement |

## Mechanism evidence

- Gradient allocation (64 Qwen3-4B trajectories, ThinkARM): over-allocated to Explore (22% of gradient vs 14.8% of tokens) and Verify (11% vs 8.1%), under-allocated to Implement (16% vs 28%). Reads as sharpening existing exploration/verification behaviour (selection), not new concepts; zero-divisor and coverage-check tokens are reinforced.
- Responses shorten (e.g. 30.0k -> 26.6k tokens on HMMT), so part of the gain may be length/truncation effects.

## Limitations

- Non-monotonic in weakening strength (Qwen3.5-4B HMMT: b=8 56.0, b=3 68.3, b=2 49.9; $\tau$: 1/16 60.9, 1/6 70.5, 1/4 54.8, 1/2 49.6). b and $\tau$ tuned on a test benchmark (HMMT25).
- GPTQ-3bit and plain W4A4 give no consistent gain: bit width does not predict the weak model's value. No mechanism theory for why quantization noise points toward better reasoning (could be generic sharpening or length shortening).
- Gain varies wildly by model (+11-13 on Qwen3.5-4B, -0.3 on Qwen3.6-27B quant); Qwen3.5-4B baseline may be under-optimised (30k-token generations). No forgetting or general-capability check; math/code only.

## Thesis relevance

- Teacher-free, privileged-info-free data point for [[conflicts/opsa-vs-opd-pattern-transfer]]: signal comes from a model-pair contrast, not a teacher or verifier. Training-time analogue of contrastive decoding (expert vs amateur), relevant to the R_w thread in [[research/decoding-time-steering/_overview]].
- Soft tension with [[research/teacher-student-rl/opsd-compresses-rlvr]] (compaction, not correction): WISD gets large accuracy gains, but also shortens responses, and may be eliciting states already supported.
- Not a single-sample study; 3.2k prompts, no prompt-count ablation ([[research/teacher-student-rl/one-shot-opd]] suggests far fewer might do).

## Source

- `raw/research/weekly-2026-10-30/01-wisd-weakening-induced-opsd.md` (arXiv:2610.38681, https://arxiv.org/abs/2610.38681)

## Related

- [[research/teacher-student-rl/opsa-teacher-free-self-adaptation]] — parallel teacher-free OPD-style gains; WISD cites OPSA as complementary
- [[research/teacher-student-rl/privileged-info-opsd]] — WISD removes privileged context entirely
- [[research/teacher-student-rl/opsd-compresses-rlvr]] — compaction vs capability gain
- [[research/teacher-student-rl/rlcsd]] — contrastive self-distillation by subtraction (hint-based vs weight-based)
- [[research/teacher-student-rl/sgsd-skill-gated-distillation]] — reference-free self-distillation
- [[research/teacher-student-rl/gift-gradient-informed-filtering]] — OPSD token filtering / gradient analysis
- [[research/teacher-student-rl/bsd-bridged-self-distillation]] — privileged-context self-teacher contrast
- [[research/teacher-student-rl/tgopd-verify-before-distill]] — verified-teacher gating; WISD uses no verifier
- [[research/teacher-student-rl/ida-opd-entropy-influence]]
- [[research/teacher-student-rl/opd-vs-offpolicy-kl-direction]]
- [[research/teacher-student-rl/reverse-kl-distillation-guarantees]] — theory for the reverse-KL objective
- [[research/teacher-student-rl/one-shot-opd]]
- [[research/decoding-time-steering/_overview]]
- [[research/rlvr-mechanics/rethinking-rl-sparse-selection]] — sparse token-level selection
- [[research/rlvr-mechanics/high-entropy-minority-tokens]] — fork tokens
- [[research/single-sample-rl-finetuning/rlsc-self-confidence]] — label-free self-signal; confidence-only controls fail to match
- [[research/rlvr-mechanics/deepseekmath-grpo]] — sparse outcome-reward baseline
- [[research/teacher-student-rl/_overview]]
- [[conflicts/opsa-vs-opd-pattern-transfer]]
- [[conflicts/adrs-vs-opsd-compaction]]
- [[../weekly-briefs/2026-10-30]] — brought in by the 2026-10-30 weekly sweep
