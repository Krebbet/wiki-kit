# RRC: Ranking-Based Reward Construction for Generative Reward Models

Northeastern University / NiuTrans Research (arXiv:2608.06310). Diagnoses why generative reward models (GRMs) — which beat discriminative RMs on pairwise judgment benchmarks — barely help when plugged into RL: converting their output to a scalar via preference-token probability (PRC, the GenRM/GRAM-style default) throws away most of the signal, because GRMs are trained comparatively and their token probabilities reflect judgment confidence, not preference margin. RRC replaces probability-scalarization with **ranking-based** reward construction — deriving GRPO/DAPO-compatible scalar rewards directly from tournament-style pairwise rankings among sampled or anchor responses — and closes most of the gap between GRM judgment quality and GRM RL performance.

## Method

Standard pipeline (PRC — probability-based reward construction, used by GenRM, GRAM): concatenate prompt + sampled response + a greedy-decoded reference, ask the GRM which is preferred, take the predicted preference-token probability as the scalar reward for group-relative advantage estimation. RRC's diagnosis: this is a category error. GRMs are trained with cross-entropy on a preference token conditioned on *both* responses — a comparative objective — not to emit calibrated scalars. Under CoT-style judging, token probabilities collapse toward extremes or track confidence rather than margin, degrading the advantage signal fed to GRPO/DAPO.

RRC keeps the GRM but changes only the reward-construction step — two ranking-based constructions:

- **Self-Competitive Ranking (SCR):** for a sampled group of *m* responses from the current policy, query the GRM on all pairwise preferences, build a tournament graph, reward = win count. O(m log m) GRM calls per group.
- **Anchor-Guided Ranking (AGR):** compare each sampled response only against a small fixed anchor set of *n* responses drawn from a **frozen reference policy** (not the evolving policy), cutting calls to O(m·n). Anchor stability (vs. SCR's anchors drifting with the policy) is the mechanism RRC credits for AGR's edge.
- **Majority voting + conflict-aware ranking adjustment:** repeat GRM queries per pair (test-time scaling) and resolve cyclic/intransitive judgments with a Kemeny-rule-style minimum-weight-feedback-edge-set heuristic, producing a globally consistent ranking from noisy stochastic pairwise comparisons.

Resulting rewards drop straight into GRPO/DAPO group-relative advantage computation — no RL infrastructure change beyond the reward-construction call pattern. Backbones: LLaMA-3.2-3B/3.1-8B-Instruct as reward models (trained on HelpSteer3, 40.5K examples), LLaMA-3.1-8B-Instruct/Qwen2.5-7B-Instruct as policy.

## Results

8B-scale RM, thinking-enabled policy, GRM+RRC-AGR+voting@8 vs. GRM+PRC baseline vs. discriminative-RM baseline:

| Benchmark | Discrim. RM | GRM+PRC | GRM+RRC-AGR+voting@8 |
|---|---|---|---|
| AlpacaEval2 | 33.2 | 35.8 | **41.3** |
| ArenaHardV2 | 7.4 | 7.8/8.0 | **11.2** |
| WildBench | 49.8 | 48.3 | **59.8** |
| MMLU-Redux | 52.7 | 51.4/52.9 | **56.9/57.3** |
| MATH-500 | 42.0 | 41.2 | **48.6** |

Same pattern at 3B-scale RMs (PRC 31.4 AlpacaEval2 → RRC-AGR+voting@8 37.5–37.8). RRC-AGR ≥ RRC-SCR generally, especially combined with voting. Scaling is monotonic with diminishing returns in both vote count and anchor count *n*; anchor count saturates/slightly regresses at very large n (256), attributed to reduced anchor diversity. RL+RRC also beats offline preference-optimization baselines (DPO, SimPO). Notably, the RM-judgment-quality gap the paper starts from — GRM beats discriminative RM by +7.5%/+4.2% on RM-Bench/JudgeBench — only translated to +1.3% under PRC-based RL; RRC recovers most of the gap.

## Novelty

Refinement, not a new architecture — the only change is the reward-construction step, not the GRM, RL algorithm, or backbone. Prior GRM-in-RL work (GenRM, GRAM/GRAM-R²) sticks to PRC-style probability scalarization. RRC's contribution is (a) empirically pinning the ranking/scoring mismatch as the reason GRM judgment superiority fails to transfer to RL gains, and (b) making pairwise-ranking-to-scalar-reward conversion tractable at RL scale via anchor-guided sampling + Kemeny-style conflict resolution over noisy comparisons.

This is the seed of a **"reward model design for RL"** thread on this wiki — no existing page covers the generative-vs-discriminative reward model design question directly; prior entries on this optimizer family address token-level credit assignment ([[token-gradient-cancellation]], [[delta-token-credit]]) or the RL objective itself ([[vimpo]]), not how the reward scalar is constructed from an RM's output in the first place.

## Applicability

Any open-ended RL post-training loop (chat, instruction-following, non-verifiable-reward tasks) already using GRPO/DAPO-style group-relative sampling with a generative/CoT reward model. Requirements: an existing GRM or budget to train one on preference-with-rationale data (~40K-example scale sufficed here), inference budget for O(m log m) or O(m·n) extra GRM calls per RL step (voting multiplies further), group-sampling RL already in place. **Not applicable** to RLVR/verifiable-reward settings (math/code with ground-truth checkers) — this is squarely an open-ended-RL/subjective-reward technique.

## Reproducibility

Code released: github.com/wangclnlp/RRC. Public backbones (LLaMA-3.1-8B/3.2-3B-Instruct, Qwen2.5-7B-Instruct) and public preference dataset (HelpSteer3).

## Adoption

Too recent (Aug 2026) for citation/pickup signal. Recognizable NiuTrans/Northeastern lineage (same group as GRAM, GRAM-R², ESRL), and it engages an active generative-reward-modeling literature (RM-R1, Reward Reasoning Model, Think-RM) — a contested, active sub-area rather than a niche result.

## Source

`raw/research/weekly-2026-08-22/03-rrc-ranking-reward-construction.md` (arXiv:2608.06310)

## Related

- [[token-gradient-cancellation]] — adjacent problem, same GRPO/DAPO optimizer family: DFPO fixes token-level gradient-cancellation pathology for shared/template tokens within the RL objective itself; RRC operates one layer upstream, fixing how the reward scalar is *constructed* from a GRM's output before it ever reaches the advantage computation.
- [[delta-token-credit]] — same adjacency: DelTA reweights tokens via discriminator-contrast over gradient centroids (token-level discriminative reweighting); RRC reweights at the reward-model-output level (ranking-based reward construction). Parallel, composable layers of the same reward-shaping stack.
- [[vimpo]] — another drop-in GRPO reward/credit modification; VIMPO derives per-token value analytically from KL-regularized RL theory downstream of the reward signal, RRC constructs the reward signal itself upstream. Complementary rather than competing — both slot into the same GRPO/DAPO loop without infrastructure changes.
- [[debate-training-reward-hacking]] — parallel reward-signal-design-flaw thread: RRC fixes GRM judgment not transferring to scalar RL reward via naive scalarization; debate training fixes LLM-judge reward being outright hackable. Candidate anchor pair for a future "reward model / judge reliability for RL" cluster.
