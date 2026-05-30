# ReasonMaxxer: RL as Sparse Policy Selection

USC (Akgül, Neiswanger, Prasanna) + DEVCOM ARL (Kannan), arXiv:2605.06241, May 2026. Token-level analysis across four base/RL pairs (Qwen2.5-1.5B/7B, Qwen3-4B; GRPO/PPO/RLOO) shows RL modifies only 1–4% of token positions, never outside the base model's top-5 candidates, always at high-entropy decision points. The entire correction is representable in a rank-32 LoRA (0.27–0.49% of parameters). ReasonMaxxer operationalises this: entropy-gated contrastive fine-tuning on 50 problems, single epoch, single GPU, minutes of wall-clock — $4–$25 vs. $200–$103,000 for full RL, matched or exceeded performance across 3 model families × 6 scales × 6 math benchmarks. This directly conflicts with the GRPO-gradient-fix literature ([[token-gradient-cancellation]], [[rlsd-self-distilled-rlvr]]) which invests in making RL better; ReasonMaxxer argues RL was unnecessary to begin with.

## Method

**Token-level divergence analysis.** For each of four base/RL pairs, every position is classified as UNSHIFTED (base and teacher agree), RERANKED (teacher promotes a token already in base top-5), or SHIFTED (teacher prefers a token outside base top-5). Results: SHIFTED ≈ 0% in all pairs; RERANKED = 1.0–4.1%; mean rank of teacher's preferred token = 2.14–2.39. Entropy at reranked positions is 5–12× higher than at unchanged positions (Table 2).

**Oracle causality experiment.** During deterministic base-model generation, replace only reranked positions with the teacher's preferred token → fully reproduces teacher pass@1. Replace with random top-20 tokens → no improvement over base. This establishes causality: RL's accuracy gain is entirely attributable to ~1–4% of token positions.

**Entropy as teacher-free proxy.** Using only a threshold τ on base-model entropy (no teacher) to select intervention sites, then substituting the teacher's token: matches teacher exactly on Qwen2.5-7B GRPO, closely approaches it on PPO, with 1.2–8.3% token budget. The *where* of RL's correction is predictable from base entropy alone; only the *which* requires learning.

**Low-dimensionality probe.** KL-LoRA distillation: rank-32 adapter on all attention projections (QKVO), trained on 100 problems to minimise KL to teacher. Reproduces teacher accuracy on MATH-500 and GSM8K across all four pairs, using 0.27–0.49% of model parameters. A rank-8 output-projection-only adapter further approximates this within a few points.

**ReasonMaxxer algorithm.**
1. Sample K=20 rollouts per problem from frozen base on 150 problems; retain ~50 with mixed success (pass rate strictly in (0,1)).
2. Mark decision points: positions where base-model entropy H_t > τ (model-family-specific threshold).
3. Train rank-32 LoRA with two losses: advantage-weighted contrastive cross-entropy at decision points (Eq. 6 — positive weight on correct-trajectory tokens, negative on incorrect); KL-anchor loss to frozen base everywhere else (Eq. 7).
4. Single epoch, single GPU. Ablation: removing the negative suppression term (positive-only SFT) yields ~half the total gain over base (MATH-500: 0.298 → 0.398 vs. full ReasonMaxxer 0.502 on Qwen2.5-1.5B).

**Backbones tested:** Qwen2.5 (1.5B, 7B, Math-7B, 32B), Qwen3 (0.6B, 4B), DeepSeek-R1-Distill-Qwen-1.5B, Mistral-7B-v0.1.

## Results

- **Qwen2.5-1.5B MATH-500:** ReasonMaxxer 50.2% vs. SimpleRL-Zoo 49.6% ($4 vs. $200); avg across 6 benchmarks 28.2% vs. 28.7%.
- **Qwen2.5-7B MATH-500:** 70.6% vs. SimpleRL-Zoo 65.6% ($5 vs. $600); ReasonMaxxer avg 47.2% vs. Open-Reasoner-Zero 48.5% ($5 vs. $6,300).
- **Qwen2.5-32B avg:** ReasonMaxxer 44.0% vs. Open-Reasoner-Zero 43.6% ($25 vs. $103,000).
- **DeepSeek-R1-Distill-1.5B MATH-500:** ReasonMaxxer 66.2% vs. STILL-3 53.6%, DeepScaleR 50.2% ($4 vs. $2,268 / $4,500).
- **Qwen3-0.6B avg:** ReasonMaxxer 27.8% vs. GRPO 20.0% ($4 vs. $100).
- **Qwen3-4B avg:** ReasonMaxxer 47.6% vs. General-Reasoner 40.6% ($4 vs. $4,600).
- Oracle correction (causal, teacher token at reranked positions): reproduces RL pass@1 exactly across all pairs. Random top-20 substitution at same positions: no improvement.
- Training data: 50 problems vs. ~8,000 (SimpleRL-Zoo GRPO) or ~57,000 (Open-Reasoner-Zero).
- Cost range: $4–$25 (ReasonMaxxer) vs. $200–$103,000 (RL baselines); ~2–3 orders of magnitude.

## Why this matters

The "1–3% of tokens" finding is a mechanistic claim with a causal proof, not a correlation. It reframes the entire post-training stack: if RL's useful signal is confined to high-entropy branch points that the base model's own entropy function can locate, then the bulk of GRPO's computational investment — sampling thousands of rollouts, running on-policy updates, applying gradient uniformly across all tokens — is doing nothing load-bearing. The sparse-policy-selection view says reasoning improvement is a precision task, not a density task.

This finding is in direct tension with [[token-gradient-cancellation]] (DFPO). DFPO's gradient-exchangeability analysis identifies non-decision tokens' gradient cancellation failure as the bottleneck in GRPO, and its fix (Min-Replace / Adv-Orthogonal stop-gradients) operates on the assumption that the full token distribution is the relevant domain. ReasonMaxxer's oracle experiment undercuts this premise: if ~97% of tokens carry no useful RL signal at all, then fixing their gradient cancellation was never the bottleneck. The conflict is now filed at [[conflicts/sparse-policy-selection-vs-gradient-cancellation]]. Note the two are not strictly incompatible at different operating points — DFPO makes RL better; ReasonMaxxer replaces RL — but they cannot both be identifying the central problem.

[[rlsd-self-distilled-rlvr]] endorses RL's direction signal as the reliable anchor and improves only per-token magnitude weighting. ReasonMaxxer shows RL's direction signal is not needed: base-model entropy identifies the same positions, and advantage-weighted contrastive loss from base-model rollouts is sufficient. Both could be correct — RLSD improves GRPO, ReasonMaxxer replaces it — but they pull toward opposite conclusions about whether RL infrastructure is worth maintaining. [[gepa-reflective-prompt-evolution]] reaches a parallel conclusion from the prompt/inference side: 35× fewer rollouts, no weight updates, comparable gains. ReasonMaxxer and GEPA together form a coherent case that the sparse-signal hypothesis extends across both the weight-update and prompt-optimization axes.

## Reproducibility

- Code: https://github.com/farukakgul/ReasonMaxxer
- Training: single GPU (NVIDIA RTX Pro 6000 in their runs), minutes of wall-clock, 50 problems, 1000 sequences (20 rollouts × 50 retained problems), rank-32 LoRA, single epoch.

## Source

- `raw/research/weekly-2026-05-11/01-reasonmaxxer.md` — arXiv:2605.06241.

## Related

- [[token-gradient-cancellation]] — DFPO presupposes gradient-flow on all tokens is the design space; ReasonMaxxer empirically shows ~97% of those tokens carry no RL signal, undercutting the premise. See [[conflicts/sparse-policy-selection-vs-gradient-cancellation]].
- [[rlsd-self-distilled-rlvr]] — RLSD reweights per-token magnitude within RL; ReasonMaxxer eliminates RL. Complementary evidence for token-budget misallocation in GRPO; opposing conclusions about RL necessity.
- [[gepa-reflective-prompt-evolution]] — parallel sparse-signal argument from prompt-space: fewer rollouts, no weight updates. ReasonMaxxer (weight-update axis) + GEPA (prompt axis) = convergent evidence.
- [[latent-grpo]] — latent-space GRPO with three stabilization fixes; shares the "reduce RL overhead" direction but retains RL. Compare efficiency gains.
- [[tempo-test-time-rl]] — test-time RL as EM; also questions RLVR inefficiency but from the continual-learning angle.
- [[eggroll]] — Evolution Strategies as GRPO alternative at scale; another axis of the same conflict ([[conflicts/grpo-vs-evolution-strategies]]). ReasonMaxxer adds a third: RL-free contrastive fine-tuning.
- [[agentflow]] — Flow-GRPO broadcasts outcome reward across multi-turn modules; assumes RL is necessary at the trajectory level. ReasonMaxxer's result doesn't directly address multi-turn credit assignment but raises the question of whether the same sparse-correction pattern appears there.
