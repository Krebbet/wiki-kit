---
setup_approved: 2026-04-23
seeded: false
---

# Watchlist

Persistent radar for this wiki. Populated by `/weekly-brief` (up to 10 entries per run as surplus beyond the ≤5 captures) or by hand. **Intentionally empty at setup**; do not pre-seed.

**Format:** under each section header, one bullet per item: `- <title> — <≤12-word why / status>`. No URLs, no multi-sentence descriptions.

**Lifecycle:** added by the weekly brief or by the user; promoted to full ingest when ≥2 watchlist entries converge on a theme OR the user tags an item as load-bearing; retired silently after 90 days without promotion.

**Sections:** created on first use. The brief adds under the most relevant existing section header; if none fits, it creates a new one matching the theme.

---

## Self-play

- Self-Distilled RLVR (RLSD, arXiv:2604.03128) — RLVR direction × self-distillation magnitude hybrid; OPSD-adjacent
- Seirênes (arXiv:2605.11636) — adversarial self-play w/ evolving in-loop distractors; shared-param verifiable-reasoning RL. **User-tagged load-bearing 2026-05-19: strong self-play exemplar — evaluate/ingest when building any self-play-inclusive proposal.** Promotion triggered (user tag) but deferred per instruction; pull in at proposal time. Hub pointer: [[research/synthesis/proposer-reward-shapes#Candidates earmarked for self-play-inclusive proposals]].

## Post-GRPO RL optimizers

- Kernelized Advantage Estimation (arXiv:2604.28005) — kernel-smoothed nonparametric value est, post-GRPO variance fix
- Step-Level Advantage Selection (SAS, arXiv:2604.24003, ACL 2026 Findings) — zero-advantage gating on low-confidence steps
- Reinforcement-Aware Knowledge Distillation (RLAD, arXiv:2602.22495) — Trust Region Ratio Distillation replaces KL anchor
- Adaptive Power-Mean Policy Optimization (APMPO, arXiv:2605.04066) — generalised power-mean objective + feedback-adaptive clipping; +3.0pp over GRPO
- Search-driven Reward Function Optimization (arXiv:2605.02073) — frames reward-function specification itself as a search target; meta reward shaping

## Process reward models

- Process Reward Agents (PRA, arXiv:2604.09482) — frozen domain-expert PRM as inference-time search guide; 80.8% MedQA Qwen3-4B
- IOP / IOP-GSPO (arXiv:2605.05226) — internalising outcome supervision into process supervision via audit gating; +4.9–6.9% over GSPO
- Controllable Verifiable Process Data Synthesis for PRMs (arXiv:2605.02395) — symbolic chain + template-aware error injection; principled PRM training-data generator
- VPS — Correct Answers from Sound Reasoning (arXiv:2605.12519) — jointly optimise accuracy + reasoning soundness; adaptive reward weighting as implicit curriculum
- GRPO-VPS (arXiv:2604.20659, ICLR 2026) — model-free verifiable process reward via answer-belief probing per step; +2.6pp, −13.7% length

## Teacher-student RL

- Rethinking On-Policy Distillation (arXiv:2604.13016) — necessary conditions for OPD success; mechanistic phenomenology
- Temporal Curriculum in OPD (TCOD, arXiv:2604.24005, Tongyi) — temporal curriculum scheduling within multi-turn OPD-RL
- Uni-OPD (arXiv:2605.03677) — unifying LLM/MLLM OPD via dual-perspective student-exploration + teacher-order-consistency; 16-benchmark sweep
- Near-Policy OPD (arXiv:2605.05940) — async generation + Δ-IFD selective packing; 8.1× speedup over RL-based OPD
- UniSD (arXiv:2605.06597) — systematic ablation of self-distillation components (EMA / contrastive / feature-matching) across 6 benchmarks/models

## RLVR mechanics

- LLMs Explore by Latent Distilling (arXiv:2604.24927) — latent-space distillation as RL exploration mechanism
- When Can LLMs Learn to Reason with Weak Supervision? (arXiv:2604.18574) — RLVR under scarce data + noisy rewards
- ~~Learning from Less (arXiv:2604.18381)~~ — paper-not-ingest; **datasets retained as test-data references** (Counting / Graph Reasoning / Spatial Reasoning, all programmatic + verifiable). See [[research/concept-evaluation/_overview#Test-dataset references]]. Capture: `raw/research/dataset-references/01-learning-from-less.md`. (2026-05-14)
- ResRL (arXiv:2605.00380) — SVD projection of negative-sample gradients orthogonal to positive subspace; +9.4 Avg@16 over NSR
- FREIA (arXiv:2605.04065) — Free-Energy-Principle unsupervised RL reasoning, no external reward; consensus + novelty terms; pairs w/ uPRM

## Self-improvement

- Reflect, Retry, Reward (arXiv:2505.24726) — reward self-reflection tokens on retry-success; up to +34.7%, no synthetic data

## Test-time training and curriculum

- Test-Time Curricula for Targeted RL (TTC-RL, arXiv:2510.04786) — automatic task-specific test-time curricula; 1.8× AIME25; ICLR 2026 re-surfacing

## Variable-granularity / concept-level architectures

*Seeded 2026-05-13 by [[research/synthesis/concept-granularity-architecture]] hypothesis. Watchlist targets are categorical (entire research lines) rather than specific arxiv IDs; promote individual papers as they surface. Closest current coverage: [[research/rl-optimizers/latent-grpo]].*

- Funnel Transformer / hierarchical-pooling LMs — variable-length internal representations
- Mixture-of-Tokens / Mixture-of-Depths — differentiable per-position compute routing
- Token-merging in language (ToMe-style, beyond vision) — merge/split primitives mid-stack
- Continuous-latent reasoning successors to Latent-GRPO — variable-length latent chains
- Entropy-routed compute allocation — concentrate FLOPs at high-entropy positions
- Byte-level + learned chunking — sub-token granularity as a different attack on the same problem
- Counter-evidence — uniform per-position compute as necessary; collapse modes for variable-length middle stacks
- Latent-GRPO (arXiv:2604.27998) — GRPO into continuous latent (non-token) reasoning space; RL-instability fix for latent reasoning
- Continuous Latent Contexts (arXiv:2605.09867) — constant-depth transformers implement weighted-majority / Q-learning via latent context tokens
- When to Think, When to Speak (arXiv:2605.03314) — RL-trained private/public disclosure policy; "silence tax"; tested on MoE Qwen3-30B-A3B

## Decoding-time / activation steering

*Seeded 2026-05-12; promoted to full theme 2026-05-13 via /research run. Theme now lives at [[research/decoding-time-steering/_overview]] with 13 per-paper pages + theme overview + [[research/synthesis/decoding-time-shapes]] synthesis. Watchlist entries cleared into corresponding wiki pages; only the still-open deep-dive remains.*

- REASONMAXXER deep-dive — rank-8 $W_O$ LoRA mechanism vs decoding-time reweighting equivalence ([[research/rlvr-mechanics/rethinking-rl-sparse-selection]] hook); still open as a /research target
- Activation-steering cluster (arXiv:2605.03907 PSR / 2605.05892 flow-based / 2605.06342 key-orthogonal) — mini-trend; promote as one bundled /research run

---

## Related

- [[reference-sources]] — what the weekly brief scans + local conventions for this wiki
- [[index]] — wiki-wide page catalog
- [[weekly-briefs/2026-05-17]] — most recent weekly sweep
- [[weekly-briefs/2026-05-10]] — prior weekly sweep
