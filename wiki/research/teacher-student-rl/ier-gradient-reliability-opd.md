# IER: Information-Efficiency Ratio for OPD Token Selection

Sheng, Ye, Wang, Wang, Gu, Kang (MBZUAI/Ant Group, arXiv:2609.24432) derive the information-efficiency ratio (IER) — a Fisher-geometry signal-to-noise measure of single-sample gradient reliability in sampled-token on-policy distillation (OPD) — and show that combining IER with existing usefulness-based token selectors lets sparse OPD match or exceed full (all-token) OPD at token budgets as low as **0.1%–1%**.

## Method

Standard sampled-token OPD optimizes reverse KL $D_{KL}(p\|q)$ between student $p$ and teacher $q$ next-token distributions at each student-generated prefix, estimated from one sampled token $a$. The local gradient is $g=\mathbb{E}_p[\rho(a)\phi_a]$ where $\rho(a)=\log(p_a/q_a)$ and $\phi_a = e_a - p_a$. A control-variate baseline $b$ gives estimator $g_b(a) = (\rho(a)-b)\phi_a$.

Under **Fisher-information geometry** (not naive Euclidean MSE), the squared signal is $\|g\|^2_{F^+} = \mathrm{Var}_p[\rho(a)]$, and the noise under baseline $b$ decomposes cleanly, giving a closed-form variance-minimizing baseline $b^\star$. **IER is defined as Signal/Noise under $b^\star$**; its reciprocal is the relative MSE of the gradient estimator. Since full-vocabulary IER is intractable, it's approximated on a candidate set built from student and teacher top-K logits plus the sampled token. Tokens are ranked by normalized IER and combined with a normalized usefulness score via soft logical operators — OR (select if reliable *or* useful) and AND (select only if *both*).

The authors explicitly note **reliability and usefulness are orthogonal axes**: high IER does not indicate high usefulness of the supervision, and usefulness/IER rankings correlate highly overall (Spearman) but pick substantially different tokens in their top-10% (low Jaccard overlap).

## Results

Across strong-to-weak (JustRL-Nemotron-1.5B → OpenMath-Nemotron-1.5B) and big-to-small (JustRL-Qwen3-4B → Qwen3-1.7B) math distillation, and a medical distillation pair, adding IER improves five heuristic usefulness selectors (Prefix, Entropy, TIP, TA-OPD, CA-SoftOR) in most settings at small budgets:

- At **0.1% budget**, IER alone approaches/exceeds full OPD (Bayes@32: 58.9 vs. 59.9 on AIME26; exceeds full OPD on 3/4 Qwen3-pair benchmarks).
- TIP+IER-AND at 0.1% outperforms full OPD consistently on the Qwen3 pair.
- On HealthBench at 0.1% budget (~1 token/trajectory), IER alone reaches 45.25 overall vs. full-OPD's 45.77, while Prefix alone gives essentially no improvement (38.30) — Prefix+IER-OR recovers most of the gap.

**Not monotonic in budget** — going from 1% to 50–80% often gives little benefit or *degrades* performance; mechanism unclear.

## Limitations (acknowledged)

- Gains are selector- and setting-dependent; combinations with Entropy-based selection often don't help and sometimes hurt.
- Both usefulness scores and candidate-set IER are approximations with no guarantee of better selection.
- Requires teacher logit/vocabulary access at every prefix — not applicable to black-box/API teachers.
- All evaluated teacher-student pairs share the same tokenizer/family (Nemotron↔Nemotron, Qwen3↔Qwen3) — no cross-tokenizer or cross-family test.

## Bearing on the OPSA-vs-OPD-dual-nature conflict

This is a **third independent mechanistic account** for why a small fraction of tokens can carry (nearly) all of OPD's useful gradient signal, alongside [[opsa-teacher-free-self-adaptation]]'s low-logp-suppression account and the cross-mode-capability-access account in [[privileged-info-opsd]]. IER's mechanism is estimator-noise/gradient-reliability under Fisher geometry — orthogonal to both. It **neither confirms nor refutes** teacher-content-dependence directly: IER-selected tokens still depend on the teacher's distribution through $\rho(a) = \log(p_a/q_a)$, so this is compatible with (does not contradict) [[opd-dual-nature-generalization]]'s teacher-identity-dependent transfer claim, just adds a reliability filter on top of it. Recorded in [[../../conflicts/opsa-vs-opd-pattern-transfer]] as a third axis — "which tokens matter and why" now has token-suppression, cross-mode-capability, and estimator-reliability as three distinct, non-exclusive candidate answers.

Structurally, this mirrors the RLVR-side finding in [[../rlvr-mechanics/high-entropy-minority-tokens]] (top-20% entropy tokens drive effective gradient signal) and [[../rlvr-mechanics/rethinking-rl-sparse-selection]] (RL reranks only 1.0–4.1% of token positions) — a cross-regime corroboration that effective training signal concentrates in a tiny token subset, in distillation as well as RLVR.

## Source

- arXiv: [2609.24432](https://arxiv.org/abs/2609.24432) — "1% of Tokens Can Be Enough: On Gradient Estimation in On-Policy Distillation"
- Captured via 2026-09-25 weekly sweep: `raw/research/weekly-2026-09-25/05-opd-1pct-tokens-gradient-estimation.md`

## Related

- [[_overview]] — teacher-student-rl theme overview, OPD subtree
- [[opsa-teacher-free-self-adaptation]] — first mechanistic account (low-logp-token suppression) for OPD's sparse-token sufficiency
- [[privileged-info-opsd]] — second mechanistic account (cross-mode capability access)
- [[opd-dual-nature-generalization]] — teacher-identity-dependent transfer; compatible with, not contradicted by, IER's reliability filter
- [[ida-opd-entropy-influence]] — sibling reliability-gated OPD design, different granularity/math
- [[tgopd-verify-before-distill]] — prompt-level reliability gating vs. this paper's token-level gating
- [[uecr-grpo-entropy-calibrated-credit]] — 2026-09-25 sibling capture, same conflict file
- [[../rlvr-mechanics/high-entropy-minority-tokens]] — RLVR-side structural parallel: sparse token subsets carry effective gradient signal
- [[../rlvr-mechanics/rethinking-rl-sparse-selection]] — cross-regime corroboration of sparse effective-signal tokens
- [[../../conflicts/opsa-vs-opd-pattern-transfer]] — extended 2026-09-25 with this paper's third mechanistic axis
- [[../../weekly-briefs/2026-09-25]] — brought in by the 2026-09-25 weekly sweep
