# SGS — Scaling Self-Play with Self-Guidance

Bailey, Wen, Dong, Hashimoto, Ma (Stanford, arXiv:2604.20209). Tripartite **Conjecturer / Solver / Guide** self-play architecture: a frozen Guide LLM scores synthetic problems on relevance + elegance to prevent the Conjecturer's reward-hacking collapse onto disjunctive, irrelevant problems. After 200 rounds of self-play on Lean4, **a 7B model surpasses 671B pass@4**; fitted scaling-law asymptote 67.1% vs. 60.3% for the strongest RL baseline (REINFORCE$^{1/2}$). The cleanest "fix the proposer" intervention in the self-play subtree to date.

## Source
- [`raw/research/weekly-2026-05-03/02-sgs-scaling-self-play-self-guidance.md`](../../../raw/research/weekly-2026-05-03/02-sgs-scaling-self-play-self-guidance.md) — captured 2026-05-03 (arXiv:2604.20209)

## Architecture (three roles, shared base)

| Role | Function | Reward |
|---|---|---|
| **Conjecturer** $g_\phi$ | Generates $\tilde{x} \sim g_\phi(\cdot\mid x)$ conditioned on each unsolved target $x$ | $R_\text{synth} = R_\text{solve} \cdot R_\text{guide}$ |
| **Solver** $\pi_\theta$ | Solves problems via REINFORCE$^{1/2}$ (log-likelihood on correct rollouts where solve rate $\leq 0.5$) | task-verifier (Lean4 type-check) |
| **Guide** | Frozen LLM scoring $\rho(x, \tilde{x}) \in [0,1]$ on relevance + elegance (simple conclusion, no redundant premises, no disjunction explosion) | — (frozen after 2k SFT examples from GPT-4.1-mini) |

- $R_\text{solve} = 1 - s(\tilde{x})$ for problems in the bottom-70% non-zero-solve-rate tier (Goldilocks-like band).
- $R_\text{guide}$ multiplicatively gates Conjecturer reward — if the Guide says the problem is degenerate, no signal flows.

## Empirical headline

- **Lean4 D3k (3,323 problems).** At 6.3M generations, 7B SGS exceeds DSPv2-671B pass@4.
- **Scaling law (sigmoidal):** asymptotic solve rate **67.1% (SGS)** vs. **60.3% (REINFORCE$^{1/2}$ baseline)** — a 7-point gap.
- **Plateau escape:** SGS reaches 10% on problems the RL baseline never solves (0% after 8M generations).
- **Ablations:** No-Guide → 65.5% asymptote; No-Problem-Conditioning → no improvement over RL; Frozen-Conjecturer → Solver saturates fixed distribution.

## Where it sits in the wiki

- **Tenth proposer-reward shape** (extends [[proposer-reward-shapes]] beyond the existing nine) — Guide is a *frozen-language-model relevance-and-elegance scorer*, structurally distinct from AZR's solve-rate-parity, R-Zero's symmetric+BLEU, LSP's general-sum quality reward, SPICE's structural asymmetry, SQLM's hard Goldilocks gate.
- Realises [[understanding-self-play]]'s "proposer is the critical component" finding at scale.
- **Component C/D candidate** for [[../synthesis/proposed-method]]: Guide-style frozen LLM scorer as a substitute / augment for RLT's $r^{KL}$ plausibility term.
- Sister to [[azr]] (three modes), [[r-zero]] (two-model), [[spice]] (info-asymmetry), [[sqlm]] (hard Goldilocks). Closest competitor: STP (Dong & Ma 2025) — conditioned on solved problems, not unsolved.

## RL connection — REINFORCE not GRPO

SGS deliberately uses REINFORCE$^{1/2}$, not group-objective methods. Authors find **grouped objectives (CISPO) cause Solver entropy collapse** → solve rates concentrate at 0 and 1 → Conjecturer is starved of intermediate-difficulty signal. REINFORCE$^{1/2}$ maintains stable Solver entropy across 200 rounds. Cross-link: [[two-stage-dynamic]] — entropy preservation as a load-bearing hyperparameter.

## Conflict touchpoints

| Conflict | SGS evidence |
|---|---|
| [[../../conflicts/invisible-leash-vs-spiral-transfer]] | SGS makes progress where RL baseline plateaus (10% vs. 0% on hardest tier). Mechanism is a *better proposer*, not Solver-support expansion — Stage-1-scoped, **compatible with Position A (Invisible Leash)**. |
| [[../../conflicts/unified-vs-two-model-self-play]] | SGS uses *separate* Conjecturer / Solver / Guide weights (consistent with R-Zero's collapse finding). Tied-weights variant not ablated; doesn't directly resolve the conflict. |

## Limitations

1. **Guide is frozen** — authors flag insufficient resolution for hardest problems; learned Guide deferred to future work.
2. Domain limited to **verifiable formal math** (Lean4); natural-language extension requires learned verifiers.
3. Without Problem Conditioning: Conjecturer drifts to hard-but-irrelevant problems; conditioning is load-bearing.
4. Without Guide: Conjecturer collapses to disjunctive, overly long conclusions by iter ~100 (>80% disjunctive vs. <10% baseline).

## Related

- [[_overview]] — self-play subtree
- [[invisible-leash]] / [[yue-rlvr-boundary]] — Position A foundation
- [[two-stage-dynamic]] — entropy preservation as Stage-2 prerequisite
- [[understanding-self-play]] — proposer-criticality finding SGS realises
- [[azr]] / [[r-zero]] / [[spice]] / [[sqlm]] / [[language-self-play]] — sibling proposer-reward shapes
- [[asymmetric-self-play]] / [[alphazero]] — pre-LLM ancestors
- [[../synthesis/proposed-method]] — Guide as candidate for component C/D
- [[../synthesis/proposer-reward-shapes]] — tenth shape
- [[../../conflicts/invisible-leash-vs-spiral-transfer]] — Stage-1 compatible
- [[../../conflicts/unified-vs-two-model-self-play]] — three-model variant
- [[../../weekly-briefs/2026-05-03]] — brought in by the 2026-05-03 weekly sweep
