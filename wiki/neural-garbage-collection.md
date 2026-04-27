# Neural Garbage Collection (NGC): Learning to Forget while Learning to Reason

Stanford (Li, Hamid, Fox, Goodman, 2026; arXiv:2604.18002). End-to-end RL training of KV-cache eviction *jointly* with chain-of-thought reasoning, using outcome-based task reward alone. 2–3× KV cache compression with minimal accuracy loss on math reasoning; first method to unify eviction and token gradients under a single reward signal.

## Method

Extends RLVR / Dr. GRPO by treating KV cache evictions as additional discrete actions sampled alongside tokens. Per eviction round (every δ tokens):

1. Score KV entries via softmax over attention weights from the **w=5 most recent queries**.
2. Coarsen scores to contiguous **blocks of size b=32** (paged-KV-aligned).
3. Sample which blocks to evict via **Gumbel-top-k** subset sampling (Kool et al. 2019).

Eviction log-probability (Eq. 2) is optimized by the same group-normalized advantage used for token generation. **No auxiliary objectives.** A **replay attention mask** (§4.5) reproduces the exact per-layer visibility pattern from rollouts in a single forward pass, correcting the off-policyness that dynamic cache mutation introduces. A **staircase eviction-rate curriculum** (Eq. 6) gradually increases pressure over ~100 training steps. Optional **budget-aware interoception**: inject the eviction rate as a structured prompt tag for cross-budget generalization.

Base: DeepSeek-R1-Distill-Qwen-1.5B trained with Dr. GRPO on Countdown (250 steps) and DAPO-17k (469 steps).

## Results

| Benchmark | NGC | SnapKV | KNorm | Full-cache |
|---|---|---|---|---|
| Countdown pass@1 (1.5B, 50% evict) | **49.6%** | 21.2% | 7.8% | ~53% |
| AMC 2023/2025 (50% evict) | NGC ≫ | near-zero | near-zero | upper |
| AIME 2025 (50% evict) | NGC ≫ | near-zero | near-zero | upper |

- At 2–3× cache reduction, NGC approaches the no-eviction upper bound on AMC/AIME (Figure 8, pass@32).
- **Ablations**: Targeted KV Dropout (no replay mask) → 2.5% (collapse). Token log-probs only (no eviction gradient) → 35.7% vs NGC 49.6%. Both components essential.
- Budget-aware interoception adds 8–13% at aggressive budgets beyond training distribution (Figure 6).

## Novelty

Genuinely novel mechanism. Prior KV compression methods are inference-time heuristics (SnapKV, KeyDiff, KNorm, StreamingLLM) or supervised distillations (Breadcrumbs, Memento). NGC is the **first to train eviction end-to-end from task reward** within RLVR with no auxiliary objectives. Closest prior: DeepSeek Sparse Attention (separate KL-trained indexer, detached gradients) — NGC unifies eviction and token gradients under a single reward signal and removes the warm-up stage. The replay-mask trick for off-policy correction in dynamic-KV settings is itself a technical contribution.

## Reproducibility

No code released as of capture. Base model and training datasets (DeepSeek-R1-Distill-Qwen-1.5B, Countdown, DAPO-17k) are public, so reproduction is feasible with moderate compute.

## Source

- `raw/research/weekly-2026-04-27/03-neural-garbage-collection.md` — arXiv:2604.18002.

## Related

- [[triattention]] — both reduce KV cache pressure during reasoning; TriAttention is **training-free** pre-RoPE pruning, NGC is **end-to-end RL-trained** eviction. Parallel approaches with opposite tradeoffs (no fine-tuning vs task-specific RL).
- [[rlsd-self-distilled-rlvr]] — both extend RLVR/GRPO with additional action-space objectives; RLSD adds a teacher-weighting signal, NGC adds cache-eviction gradients; share Dr. GRPO base.
- [[token-gradient-cancellation]] — concurrent GRPO-line work fixing intra-group gradient dynamics; complementary to NGC's action-space extension.
- [[eggroll]] — RL-vs-ES axis on the same lineage of reasoning-RL.
