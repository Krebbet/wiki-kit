# One-Shot OPD: Data Efficiency in On-Policy Distillation

Tsinghua-led mechanistic study (arXiv:2609.04172, "Rethinking On-Policy Distillation of LLMs II: One Training Example") showing that on-policy distillation (OPD) trained on a *single query* recovers most of full-data OPD's gain, and explaining why via two new instruments — **state coverage** (data side) and **absorption rate** (algorithm side). Headline framing: OPD is "data-overfed but algorithm-starved." Not a new training algorithm — a diagnostic framework applied to standard dense per-token teacher/student OPD.

## Method

State coverage represents each visited state (prompt, prefix) by the teacher's final-layer hidden vector, clustered via PCA + K-means (K=200) against a full-data-OPD reference run; coverage is the fraction of reference clusters a given setting's rollouts reach. Absorption rate v_t = (d_t − d_{t+1})/d_t tracks how fast the teacher–student gap closes regardless of data volume. The paper extends the one-shot-RLVR experimental design to OPD and to multi-teacher OPD (MOPD).

## Results

One-shot OPD (math) recovers 72–87% of full-data OPD's gain depending on training length; a single query reaches 71.5% of full-data state-cluster coverage, and 16 semantically-diverse queries reach 98.9% and match full-data validation accuracy. Absorption rate declines at the same pace whether trained on 1, 4, 16, or ~17K queries — the pace is a property of the OPD algorithm, not the dataset. Robust across model families (R1-Distill-1.5B, Llama-3.2-3B, OLMo-3-7B) and domains (math, code, instruction-following, agentic tool use). Content-light stress test: empty-template and off-domain WildChat queries reach near-baseline performance at 1/3–1/2 the rollout tokens — task content isn't required, only that the input induces a useful reasoning trajectory. Against one-shot RLVR on the same query, OPD's 1000-step validation gain is >2× RLVR's, since OPD's dense per-token signal persists after RLVR's GRPO advantage collapses (rollout groups become unanimous).

Code released: github.com/Thinking-Space/One-Shot-OPD, built on veRL.

## Applicability

Anyone running OPD/MOPD post-training pipelines can likely cut curated-query volume drastically — 16 semantically-diverse queries per domain (BGE-M3 embedding-cluster diversity) reportedly match full-dataset training. Compute footprint is modest (1.5B–7B students, 300–1000 steps) — reproducible without frontier-scale compute. Less relevant to RLVR-only or SFT-only pipelines.

## Related

- [[dopd-dual-on-policy-distillation]] — algorithmic-variant sibling; this source explains the mechanism underlying why sparse/limited data suffices.
- [[flux-opd]] — both reduce OPD's dependence on curated data, via different levers (reward decomposition vs. query-set sufficiency).
- [[u-opsd-unsupervised-self-distillation]] — parallels the "labels are dispensable" theme from the query/content side rather than the reward side.
- [[anti-self-distillation]] / [[rlsd-self-distilled-rlvr]] — algorithmic OPSD-variant siblings on distinct axes.
- [[ttpo-test-time-policy-opt]] — both study when/why OPD-style dense signal beats RLVR-style outcome signal.
- [[reasonmaxxer]] / [[high-entropy-tokens-rlvr]] — parallel "the real signal is much sparser than assumed" findings in RLVR.
