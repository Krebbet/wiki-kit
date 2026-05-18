# EP-GRPO — Entropy-Progress Aligned GRPO with Implicit Process Guidance

EP-GRPO (Song Yu et al., Southwest University, arXiv:2605.04960) is a drop-in GRPO replacement that abandons GRPO's uniform token-level advantage in favour of three orthogonal mechanisms — entropy-gated outcome modulation, an implicit per-token process signal from policy divergence, and cumulative-entropy-bucketed normalisation — all derived **without any external PRM, extra sampling, or auxiliary model**. It targets three empirically documented GRPO credit-assignment failures and reports +26.4% avg accuracy over GRPO at 3B scale (+11.9% at 7B) on five math benchmarks at GRPO-parity wall-clock.

## Source
- [`raw/research/weekly-2026-05-17/04-ep-grpo-implicit-process-guidance.md`](../../../raw/research/weekly-2026-05-17/04-ep-grpo-implicit-process-guidance.md) — captured 2026-05-17 (arXiv:2605.04960)

## The three GRPO failures it targets (Fig. 2 empirics)

1. **Uniform token granularity** — high-entropy tokens matter 3.5× more (perturbation drops accuracy 3.5× vs low-entropy tokens) yet GRPO weights all tokens equally.
2. **Polarity misalignment** — 51.5% of *correct* steps inside failed sequences receive negative advantage; 6.6% of steps in winning trajectories are actually wrong.
3. **Zero-variance collapse** — 58.77% of training steps yield all-identical group rewards ($\hat A_i = 0$), going dark; the fraction *rises* through training.

## Method

Final token advantage $\hat A_{i,t}^{\text{final}} = \hat A_{i,t}^{\text{outcome}} + \hat A_{i,t}^{\text{progress}}$:

- **Entropy-gated outcome** (Eq. 18–19): $W_{i,t} = \sigma\!\big(\gamma\,(H_{i,t}-\mu_H)/\sigma_H\big)$ scales the sequence-level GRPO advantage, amplifying gradient at high-entropy decision pivots, suppressing low-entropy derivation.
- **Implicit progress** (Eq. 20–25): token log-ratio $s_{i,t} = \lambda(\log\pi_\theta - \log\pi_{\text{ref}})$, polarity-anchored by $d_i = \text{sign}(\hat A_i)$ when $\text{std}(\mathbf r)>0$, degrading to $\text{sign}(r_i - \theta_{\text{reward}})$ at zero variance. Normalised within $K=10$ **cumulative-entropy buckets** indexed by a logical-progress coordinate $\tau_{i,t} = S_{i,t}/S_{i,|o_i|}$ — bucketing by accumulated entropy, not physical token position.
- **Zero-variance degradation**: the progress term stays alive on policy divergence when $\hat A_i = 0$, sustaining gradient flow with no extra sampling.

**Theorem VI.1 (Eq. 27):** EP-GRPO gradient $=$ GRPO gradient $+\ \eta\nabla_\theta F$, with $F = \tfrac{\beta}{2}\mathbb{E}_{i,t}[\Lambda_{i,t}(\log\pi_\theta/\pi_{\text{ref}})^2]$ — an entropy-weighted squared-log-ratio regulariser, i.e. high-entropy tokens get stronger implicit KL anchoring. Implementation: LoRA rank-32, TRL, $G=8$, 8K Skywork-OR1 problems, 1000 steps, Qwen2.5-3B/7B.

## Results

| Metric | EP-GRPO | GRPO |
|---|---|---|
| Avg acc, Qwen2.5-3B (MATH500/AMC23/Minerva/AIME24/25) | **22.93%** | 18.14% (+26.4%) |
| Avg acc, Qwen2.5-7B | **30.34%** | 27.11% (+11.9%) |
| Pass@16 AIME25 (3B) | **38.20%** | 9.69% |
| AMC23 (3B) | **39.53%** | DeepSeek-R1-671B 33.91% |

Wall-clock ≈ GRPO; output ~20% longer.

## Where it sits in the wiki

- A post-GRPO credit-assignment variant in the [[_overview]] family alongside [[dapo]], [[dr-grpo]], [[gspo]]; the cumulative-entropy bucketing + gradient-equivalence theorem extend the mechanistic picture in [[../rlvr-mechanics/deepseekmath-grpo]].
- Derives an **implicit, annotation-free process signal** — same destination as [[../process-reward-models/pav-rewarding-progress]] and [[../rlvr-mechanics/learning-to-think]] but from policy divergence rather than a prover or Fisher signal. Claims to supersede PRPO / Step-GRPO without an external PRM (see [[../process-reward-models/_overview]]).
- The entropy-pivot hypothesis (high-entropy = strategic decision point) directly operationalises the informal "high-entropy decision pivot" framing in [[../synthesis/proposed-method]]; the cumulative-entropy progress coordinate is a candidate dense-reward layer for $R_w$.

## Conflict / unsubstantiated claim

EP-GRPO §II-C frames Dr. GRPO's learned bias as a "heuristic" and positions its own zero-variance handling as the principled alternative — but **provides no head-to-head experiment** ([[dr-grpo]] is absent from Table II). This is an asserted-but-unbenchmarked relative-merit claim, not a source-vs-source contradiction; recorded here, not as a conflict file. Direct comparators RL-ZVP / GTPO / SEED-GRPO are likewise not benchmarked.

## Limitations

1. Math-only (5 arithmetic-reasoning benchmarks).
2. LoRA rank-32 only; full-FT behaviour unknown.
3. ~200 warm-up steps needed before implicit signals stabilise; weaker bases may be longer/unstable.
4. Bucket statistics computed from $\pi_{\theta_\text{old}}$ — lag noise on fast-shifting distributions (unstated).
5. Polarity-anchoring (Table I sign rules) is a symbolic heuristic assuming $s_{i,t}$ sign is diagnostic; the reference policy may itself be noisy.

## Related
- [[_overview]] — post-GRPO RL-optimizer family
- [[dapo]] — data-level zero-variance handling (dynamic sampling); EP-GRPO is the signal-level alternative
- [[dr-grpo]] — learned-bias zero-variance fix; EP-GRPO asserts (unbenchmarked) superiority
- [[gspo]] — sibling post-GRPO objective
- [[../rlvr-mechanics/deepseekmath-grpo]] — base GRPO analysis this critiques/extends
- [[../process-reward-models/_overview]] — claims to supersede PRPO/Step-GRPO without external PRM
- [[../process-reward-models/pav-rewarding-progress]] — progress-as-advantage parallel
- [[../rlvr-mechanics/learning-to-think]] — annotation-free process-reward sibling
- [[../synthesis/proposed-method]] — entropy-pivot signal as $R_w$ dense-reward candidate
- [[../../weekly-briefs/2026-05-17]] — brought in by the 2026-05-17 weekly sweep
