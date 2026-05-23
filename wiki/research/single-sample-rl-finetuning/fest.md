# FEST — Few-shot-guided RLVR via Randomly Selected Demonstrations

FEST (Yang et al., UIUC, arXiv:2605.15012) is a demonstration-guided RLVR algorithm that pushes the SFT-data floor for hybrid SFT+RL to **128 randomly sampled** expert traces — 2–400× fewer than HPT (~10K), ReLIFT (8.6K), or LUFFY (46K) — while beating all of them on six math benchmarks. It jointly optimises semi-online DPO on the tiny expert set against GRPO on a large *answer-only* RL set, with a per-rollout adaptive $\beta$ keyed to solvability and a decaying weight that anneals from SFT-dominant to RL-dominant. Its load-bearing theoretical contribution is a gradient decomposition showing semi-online DPO $\approx$ weighted SFT $+$ REINFORCE-with-negative-reward, which motivates the FEST-GRPO variant that swaps the REINFORCE term for GRPO to remove the sequence-vs-token gradient-magnitude mismatch.

## Source
- [`raw/research/weekly-2026-05-17/01-fest-fewshot-rlvr-guidance.md`](../../../raw/research/weekly-2026-05-17/01-fest-fewshot-rlvr-guidance.md) — captured 2026-05-17 (arXiv:2605.15012)

## Method

Joint objective $L = c \cdot L^E + L^I$:

- **$L^I$** — standard DAPO-style GRPO on an answer-only dataset $D^I$ (~46K problems; only outcomes, no traces). Critic-free, group-relative, binary verifiable reward (exact-match math).
- **$L^E$** — semi-online DPO on a 128-example trace set $D^E$: expert CoT traces are preferred $y^+$; on-policy rollouts are non-preferred $y^-$.
- **Adaptive $\beta$ by solvability** (Eq. 5): $\beta_1$ if the model cannot solve the problem at all, $\beta_2$ if it can but this rollout failed, $\beta_3$ if the rollout was correct. Authors report robustness across $\beta \in [0.001, 0.1]$; long-chain reasoning needs smaller $\beta$ than standard DPO due to larger log-ratio magnitudes.
- **Decaying weight $c$** — anneals $L^E$ down over training; an implicit soft curriculum (SFT-dominant → RL-dominant) and an implicit forgetting-preventer. Removing it collapses avg to 28.83 (Table 5).

**Gradient decomposition (Eq. 4):** $\nabla L^E$ splits into a supervised term $\nabla\log\pi_\theta(y^+\mid x)$ and an on-policy negative-reward REINFORCE term $-\nabla\log\pi_\theta(y^-\mid x)$, each weighted by $\beta\,\sigma(\beta(r^- - r^+))$. **FEST-GRPO** replaces the REINFORCE term with GRPO, eliminating the sequence-level (DPO) vs token-level (GRPO) gradient-magnitude mismatch. Negative RL (pushing away from $y^-$) redistributes mass toward other feasible solutions rather than memorising the 128 traces — the mechanism that lets random (not LIMO-curated) demonstrations work.

Three components are each ablated-necessary: supervised signal (expert guidance beyond binary RLVR), on-policy signal (mitigates exposure bias, expands the learning basis of the sparse $D^E$), decaying weight (prevents overfitting to 128 examples).

**What is and isn't the centerpiece (clarification).** The salient-sounding mechanism — the per-rollout adaptive $\beta$ keyed to whether the model can solve *that* question (Eq. 5, three solvability tiers) — is a *robustness heuristic*, not the load-bearing contribution (Limitations #5; not in the ablated-necessary trio; $\beta$ is DPO's KL/temperature on the implicit-reward log-ratio, distinct from the global decaying weight $c$). The actual centerpiece is the **gradient decomposition** (semi-online DPO $\approx$ weighted-SFT $+$ negative-REINFORCE → FEST-GRPO) plus the **negative-RL-redistributes-mass** mechanism that is *why* 128 *randomly* selected traces beat curated-10K baselines. A reader meeting the adaptive-$\beta$-by-solvability first will tend to over-rank it.

## Headline results (Qwen2.5-Math-1.5B)

| Metric | FEST-GRPO | Pure RL | Best demo-guided baseline |
|---|---|---|---|
| Avg@8 (6 math benchmarks) | **42.38** | 39.79 | <42.38 (HPT/ReLIFT/LUFFY/CHORD/SRFT/MIFO) |
| Pass@8 (exploration ceiling) | **61.06** | 59.67 | RL-G 54.84 |
| OOD MMLU-Pro (FEST-DPO) | **38.68** | 34.81 | — |

Benchmarks: AIME24/25, AMC23, MATH-500, OlympiadBench, Minerva. Robust across three random 128-splits and across LIMOv2 as $D^E$. Works down to 64 shots (FEST-GRPO more stable at 64; FEST-DPO scales better toward 512).

## Where it sits in the wiki

- **Lowest SFT-data floor in the demonstration-guided RLVR family** — the natural low-data endpoint of the [[_overview]] theme, below [[cbrl]]'s in-context annealing and [[critique-ft-one-problem]]'s single-seed critique. *Not* single-sample (the answer-only $D^I$ is still ~46K); the few-shot reduction is only on the trace component.
- The semi-online DPO $\approx$ weighted-SFT + negative-REINFORCE decomposition is a concrete gradient-taxonomy result that extends [[../rl-optimizers/dpo]] and slots into the unified post-training framework (HPT Table 7) alongside [[../rl-optimizers/gspo]].
- Mechanistically descended from [[../self-play/spin]]'s semi-online DPO / IPM adversarial framing, retargeted to few-shot RLVR.
- The HPT-G / ReLIFT-G mid-training collapse (naively stacking RL on overfitted $D^E$) is a concrete skill-stacking interference failure mode for [[../catastrophic-forgetting/_overview]]; FEST's decaying weight is the implicit fix.

## Conflict raised

FEST §4.1 observation (ii) + Table 2 fn. 3: *"Contrary to findings in prior work [HPT, ReLIFT, LUFFY], we observe that pure RL remains a formidable baseline when the learning rate is optimized"* (1e-6 → 5e-6, RL reaches 39.79 ≈ ReLIFT on full 46K). This contradicts the implicit demonstration-necessity stance of the [[_overview]] theme. Filed: [[../../conflicts/fest-tuned-rl-vs-demonstration-necessity]].

## Limitations

1. Single base model (Qwen2.5-Math-1.5B); scale generalisation unstated.
2. Math-only; code / instruction-following deferred.
3. Still requires a large answer-only $D^I$ (~46K) — the few-shot claim is narrowly about the trace set.
4. No concept-learning evidence — gains are benchmark accuracy, not transfer or compositional tests.
5. Three $\beta$ values to set; adaptive scheme is a heuristic.

## Related
- [[_overview]] — single-sample / data-efficient RLVR theme; FEST is its low-trace endpoint
- [[cbrl]] — sibling cold-start fix from the low-data direction (in-context demo annealing vs DPO objective)
- [[critique-ft-one-problem]] — single-seed critique SFT; adjacent data-efficiency neighbour
- [[../rl-optimizers/dpo]] — the gradient decomposition extends this page
- [[../rl-optimizers/gspo]] — same unified gradient taxonomy (HPT Table 7)
- [[../self-play/spin]] — mechanistic ancestor (semi-online DPO / IPM)
- [[../catastrophic-forgetting/_overview]] — HPT-G/ReLIFT-G collapse is a skill-stacking failure mode
- [[../synthesis/proposed-method]] — decaying-weight semi-online DPO as a sparse-demo integration primitive
- [[../../conflicts/fest-tuned-rl-vs-demonstration-necessity]] — Position A (tuned-LR pure RL is formidable)
- [[../../weekly-briefs/2026-05-17]] — brought in by the 2026-05-17 weekly sweep
