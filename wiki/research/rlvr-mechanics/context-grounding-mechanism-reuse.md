# Context-Grounding Gains Are Mediated by Pre-existing Machinery

Prakhar Gupta & Vaibhav Gupta (arXiv:2609.00925) audit nine post-training arms — five GRPO reward variants, three SFT recipes, and DPO — trained from one Qwen2.5-1.5B checkpoint on context-grounding-under-knowledge-conflict, and find via causal head-knockout and a base-estimated steering direction that the gains, **including DPO's near-ceiling gain**, largely reuse machinery already present in the starting instruction-tuned model rather than building new machinery. This is the reuse-not-installation thesis extended for the first time in this wiki's corpus beyond RLVR-for-reasoning to SFT and DPO.

## Method

Nine complete post-training recipes from one Qwen2.5-1.5B-Instruct checkpoint: 5 GRPO variants (answer-F1 reward; +evidence-emphasizing prompt; +citation-F1; +contrastive context-utility reward $\log p(ans|q,ctx) - \log p(ans|q)$; reward = producing the in-context counterfactual answer), 3 SFT arms (no-conflict control; KAFT-style mixture; 78%-conflict), and DPO (ConFiQA preference pairs). Key comparisons extended to Qwen2.5-3B/7B, Llama-3.2-3B, Phi-3.5-mini.

Two causal-audit tools, both **estimated before any training**:
1. A difference-in-means "grounding direction" — mean last-position residual on follow-context minus follow-memory items, at the probe-selectivity-optimal layer.
2. Per-head knockout to find each arm's top-8 causal heads independently, compared for overlap with the base model's own top-8 and with cross-task (matched recall) controls.

Steering: add/subtract the base direction at the last generation position, norm-calibrated across model families, always compared against matched-norm random directions.

## Results

- GRPO gains are small and mostly not seed-robust — only one of five variants survives multiple-comparison correction; equivalence tests bound the surviving GRPO gain below the conflict-SFT gain even though GRPO clearly improves its own rewarded metric.
- Conflict-SFT improves grounding moderately (+.062 over base).
- **DPO drives grounding near ceiling** (+.378 to +.599 across 5 models in 3 families, paired McNemar p≤2.5e-25 everywhere) — the largest behavioral shift in the paper.
- **Mechanism-reuse evidence, independent of effect size:** independently-discovered top-8 causal heads for conflict-SFT, DPO, and GRPO variants recover 7–8/8 of the *base model's own* top-8 heads at both 1.5B and 3B, while a matched parametric-recall control task shares 0/8 heads. The DiM grounding direction estimated from the base model alone stays cosine .915–.987 aligned with directions independently re-estimated inside every trained arm, across all scales/families — and stays aligned (cosine ≥.968) throughout DPO training even as grounding rises to 90% of its final value by step 160/800.
- **Causal confirmation:** adding the base-estimated direction to the untrained base model lifts grounding (+.109); subtracting it from trained DPO/conflict-SFT suppresses most of their measured gains (−.276 DPO, −.405 SFT). Steering the untrained base model alone (zero additional training) recovers **35–40% of DPO's full-training gain** on identical items, with capability side-effects within one standard error.
- A 200-example supervised warm start raises rollout coverage and grounding, but running the identical GRPO recipe on top adds only +.001 (p=.91) — the advantage-collapsed training fraction stays at ~62% regardless. Structurally the same "many rollouts land in a dead zero-advantage zone" failure as the wiki's GRPO mastered-prompts cluster.

## Limitations (acknowledged)

- Lexical-containment metric only moderately agrees with an LLM judge (κ=.507), lower on intervention outputs than training-arm outputs — SFT/GRPO contrasts rest on the lexical metric alone.
- Mechanistic (head/direction) audits cover only 6 of 9 arms; interventions are single-seed; causal claims are about head *sets*, not full circuits; extends only to 7B and one behavior domain.
- "Pre-existing" is defined relative to the instruction-tuned starting checkpoint, not the raw pretrained model.
- Recipes bundle objective+data+budget together — comparisons are between complete recipes, not a clean ablation of the training objective alone.
- Author's explicit scoping: the null GRPO result is bounded to on-policy full-model training from a base policy with low rollout coverage on its training distribution; they exclude synthetic-coverage recipes and frozen-backbone gate-module recipes from the claim.

## Extends the wiki's "RL is selection not learning" thesis

This independently derives the reuse-not-installation account via a **different causal method** (attention-head knockout + activation-direction steering) than the token-logit-rank analysis in [[rethinking-rl-sparse-selection]] — and, notably, extends it beyond RLVR to SFT and DPO. DPO produces the *largest* behavioral change in the paper yet shows the same 7/8 head-overlap and direction-alignment as the small-effect GRPO arms: effect size and mechanism-reuse are decoupled. This is arguably the cleanest cross-paper corroboration of the reuse claim yet, and for a non-reasoning behavior (context grounding vs. math) — [[rethinking-rl-sparse-selection]]'s "0% of shifted tokens land outside base top-5" / "rank-32 LoRA replicates RL" findings are the token/parameter-level analogues of this paper's "7-8/8 causal heads reused" / "steering alone recovers 35-40% of DPO's gain with zero training" findings.

Also a new data point for [[../decoding-time-steering/_overview]]'s cross-source finding that offline activation reweighting suffices — the first instance in the wiki's steering corpus of steering benchmarked directly against a matched full post-training run (DPO) on identical items, rather than against a static behavioral benchmark.

Possible (not confirmed) tension with [[../catastrophic-forgetting/mechanistic-forgetting-circuits]]'s claim that RL retains more base circuit heads than SFT (72.5% vs. 59.0%) — this paper finds conflict-SFT arms *also* recover 7/8 of the base model's grounding-specific causal heads, nearly matching GRPO/DPO. The two papers measure different behaviors/granularities, so this may not be a true conflict, but the numbers are close enough to warrant a follow-up look.

## Source

- arXiv: [2609.00925](https://arxiv.org/abs/2609.00925) — "Context-Grounding Gains Are Mediated by Pre-existing Machinery: Auditing GRPO, SFT, and DPO"
- Captured via 2026-09-25 weekly sweep: `raw/research/weekly-2026-09-25/03-context-grounding-preexisting-machinery.md`

## Related

- [[_overview]] — rlvr-mechanics theme overview; extends the "RL is selection not learning" thesis to SFT and DPO
- [[rethinking-rl-sparse-selection]] — token/parameter-level analogue of this paper's head/direction-level reuse evidence
- [[deepseekmath-grpo]] — GRPO base method audited here as 5 reward-shape variants
- [[../decoding-time-steering/_overview]] — new data point: offline steering vs. a matched full DPO run
- [[../catastrophic-forgetting/mechanistic-forgetting-circuits]] — possible tension in RL-vs-SFT circuit-retention numbers, flagged for review
- [[../../conflicts/mcpo-vs-dapo-mastered-prompts]] — another instance of the advantage-collapse/mastered-prompts failure mode
- [[../selective-finetuning/rome]] — shares the CounterFact knowledge-conflict evaluation protocol
- [[../rl-optimizers/dpo]] — multi-scale/multi-family DPO effect-size table
- [[../../weekly-briefs/2026-09-25]] — brought in by the 2026-09-25 weekly sweep
