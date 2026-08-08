---
name: grpo-length-invariance-impossibility
description: Impossibility theorem — no length-weighting function f(L) is simultaneously gradient-unbiased and length-invariant under outcome-only reward + group-mean baseline; GRPO and Dr. GRPO are the two forced extremes of one Pareto frontier
type: research
---

# On the Impossibility of Unbiased and Length-Invariant Policy Optimization with Outcome Rewards

Ding et al. (Alibaba / Tsinghua), arXiv:2607.23364. Proves that under outcome-only reward with a group-mean baseline (the GRPO/Dr. GRPO/RLOO family), no length-based gradient-weighting function $f(L)$ can be simultaneously gradient-unbiased (P1) and length-invariant (P2): GRPO ($f(L)=1/L$) and Dr. GRPO ($f(L)=1$) are not a broken-optimizer-vs-fixed-optimizer pair but the two provably-forced extremes of a single Pareto tradeoff $f_\alpha(L) = L^{\alpha-1}$, $\alpha \in [0,1]$. Dr. GRPO's "unbiasedness" is technically correct but incomplete: removing length normalization eliminates gradient *bias* at the cost of introducing severe length *dependence* — a wrong-but-longer trajectory can capture up to 99.9% of a group's gradient magnitude, and on DeepSeek-R1-Zero's own reported statistics the incorrect/longer response class already captures ≈62.3% of gradient versus a balanced 50%.

## Method

### Unified weighted gradient estimator

Both GRPO and Dr. GRPO are instances of one estimator over a group of $G$ i.i.d. rollouts $\{o_1,\dots,o_G\}$ for a prompt, with per-trajectory length $L_i = |o_i|$, group-mean-baselined advantage $\tilde{A}_i = R_i - \text{mean}(\{R_j\})$, and summed per-token score function $S_i = \sum_t \nabla_\theta \log \pi_\theta(o_{i,t}\mid q, o_{i,<t})$:

$$\hat{g}_f = \frac{1}{G}\sum_{i=1}^G f(L_i)\,\tilde{A}_i\, S_i$$

- $f(L) = 1/L$ → GRPO (per-response length normalization, Shao et al. 2024, see [[../rlvr-mechanics/deepseekmath-grpo]]).
- $f(L) = 1$ → Dr. GRPO (no length normalization, see [[dr-grpo]]).

### Two properties, one contradiction

- **P1 (trajectory-level correctness / gradient-unbiasedness).** $\mathbb{E}[\hat{g}_f] = c \cdot \nabla J$ for some constant $c$ independent of trajectory length.
- **P2 (length neutrality).** $f(L) \cdot \Gamma(L; a)$ is length-independent, where $\Gamma(L; a)$ is the typical magnitude of the score-sum $S_i$ at fixed advantage $a$ and length $L$.

**Theorem 6.** No $f$ satisfies P1 and P2 simultaneously whenever $\Gamma$ genuinely varies with $L$ (the typical case — trajectory length correlates with the score function whenever the policy controls EOS timing). Proof sketch: Step 1 constructs a fixed-length-realizable policy and uses the REINFORCE identity plus i.i.d. group sampling to show $\mathbb{E}[R_j S_i] = 0$ for $j \ne i$, which forces $f(L) \equiv \text{const}$ for P1 to hold. Step 2 shows P2 forces $f(L)$ to co-vary with $L$ whenever $\Gamma$ does. These two requirements on $f$ are structurally irreconcilable.

### The Pareto frontier

Corollary 8 characterizes the full tradeoff family $f_\alpha(L) = L^{\alpha - 1}$:

| $\alpha$ | $f_\alpha(L)$ | Identity | Regime |
|---|---|---|---|
| 0 | $1/L$ | GRPO | Length-invariant per-token weight; gradient-**biased** whenever length correlates with the score function (Corollary 12, closed form) |
| 1 | $1$ | Dr. GRPO | Gradient-**unbiased** (matches RLOO up to constant, Remark 1); **not** length-invariant |
| $(0,1)$ | $L^{\alpha-1}$ | — | Partial bias / partial length-dependence, tunable |

The origin of the tradeoff plot (zero bias on both axes) is unreachable — this is the content of the impossibility theorem, not an engineering gap to be closed by a smarter $f$.

### Quantified length bias (Corollary 9, $G=2$, binary reward)

For a two-trajectory group with lengths $L_1, L_2$ and ratio $r = L_\text{long}/L_\text{short}$, the longer trajectory's share of total gradient magnitude under Dr. GRPO is:

$$w_\text{long} = \frac{r}{1+r} \;\to\; 1 \text{ as } r \to \infty$$

| Length ratio $r$ | Dr. GRPO $w_\text{long}$ | GRPO $w_\text{long}$ |
|---|---|---|
| 1:1 | 50% | 50% |
| 10:1 | ~91% | 50% |
| 100:1 | ~99% | 50% |

GRPO's per-token normalization holds this flat at 50/50 by construction (that flatness is exactly its P2 length-invariance, purchased at the cost of P1). **Worked extreme (Example 10):** a correct 10-token response paired with an incorrect 10,000-token response in the same group — under Dr. GRPO the wrong-but-longer trajectory captures **99.9%** of the group's gradient magnitude, "nearly completely drowning out the reinforcement of the correct answer."

### DeepSeek-R1-Zero corroboration (Example 11)

Using Liu et al.'s (Dr. GRPO paper) own reported R1-Zero-style statistics — correct responses averaging 4,965 tokens, incorrect averaging 8,206 tokens (ratio ≈ 1:1.65) — the incorrect/longer class captures **≈62.3%** of gradient under Dr. GRPO, a 24.6pp skew off the balanced 50% baseline. This is a single-step calculation from reported summary statistics, not a live re-run, but the paper argues the skew is a "necessary condition" for the observed length-growth trend and compounds over hundreds of training iterations.

### GRPO's own bias, in closed form (Corollary 12)

The impossibility cuts both ways: GRPO's gradient bias is nonzero whenever trajectory length correlates with the score function $S_i$ — "generally always the case since the policy determines when EOS is generated." Eq. 36 gives the bias term explicitly; Corollary 13 generalizes the general-$G$ weight share to $w_i \propto |o_i| \cdot |\tilde{A}_i|$.

## Claims and scope

This is a theory paper — no training runs, no benchmarks, no sample-efficiency numbers. All quantitative results (Table 1, Examples 10–11) are analytic/worked cases evaluated on reported statistics, not measured on a live policy. Scope is explicitly narrow:

- **Outcome reward only.** The advantage is a single scalar broadcast to every token. Under process/step-level reward the per-token advantage is no longer constant and the authors flag the impossibility analysis as not directly extending — future work.
- **Length-only weighting functions.** $f(L)$ depends solely on trajectory length. Finer-grained schemes — token-position-, context-, or score-geometry-dependent weighting — are explicitly out of scope and not ruled out by this theorem.
- **Single-step gradient analysis.** No modeling of multi-step training dynamics or PPO-style clipping interactions.
- **No proposed fix.** Only qualitative guidance: prefer smaller $\alpha$ (toward GRPO) when length variance is high; larger $\alpha$ (toward Dr. GRPO) early in training; consider curricula over $\alpha$.

## Relevance to the project

This is a structural ceiling on the entire post-GRPO length-bias-fix lineage ([[dr-grpo]], DAPO's overlong reshape, [[gspo]]): no member of that family can be both unbiased and length-neutral simultaneously — the choice is a knob, not a bug to be engineered away. For single-sample / small-$G$ training this matters more than at large $G$: with $G=1$–$2$ the length-ratio extremes in Table 1 above are not asymptotic curiosities but the literal per-step gradient composition, so the choice between GRPO-like and Dr.-GRPO-like weighting has an outsized, non-averaged-out effect on which trajectory's gradient dominates a given step. Remark 1 (Dr. GRPO's advantage ≡ RLOO advantage up to a constant) means this impossibility result applies unmodified to [[rloo]]-style baselines as well.

**Not a resolution of the std-normalization conflict.** This paper's impossibility theorem concerns *length*-based gradient weighting only. It is structurally parallel to — but mechanistically separate from — the std(R)-normalization / difficulty-bias axis raised in `[[../../conflicts/mcpo-vs-dr-grpo-std-fix]]` ([[mcpo]] vs. [[dr-grpo]]). The authors explicitly disclaim overlap (§5): std(R) normalization contributes to *difficulty* bias independent of whether length normalization is used, and point to a separate paper, Yang et al. 2026, "Your Group-Relative Advantage Is Biased" (arXiv:2601.08521, not yet in this wiki), as the one studying that axis. This page should not be read as bearing on, resolving, or contradicting the std-fix conflict — it is a second, independent "no single done-right fix" result on a different axis of the same GRPO-family objective.

## Source

- `raw/research/weekly-2026-08-07/03-outcome-reward-impossibility.md`

## Related

- [[dr-grpo]] — this source formalizes and sharpens the critique of Dr. GRPO's "unbiased"/"done right" framing: unbiasedness is real (P1 holds) but incomplete, since length-invariance (P2) is provably sacrificed
- [[../rlvr-mechanics/deepseekmath-grpo]] — the other pole of the tradeoff ($\alpha=0$); this source formally quantifies GRPO's own gradient bias (Corollary 12), not previously captured on that page
- [[mcpo]] — MCPO's difficulty-bias critique of Dr. GRPO is a parallel "no single fix is complete" result on the *std/difficulty* axis; mechanistically independent of this paper's *length* axis (see disclaimer above)
- [[rloo]] — impossibility result extends to RLOO directly (Remark 1: Dr. GRPO's advantage ≡ RLOO advantage up to a constant factor)
- [[_overview]] — adds a formal theoretical ceiling on the entire post-GRPO length-bias-fix lineage (Dr. GRPO, DAPO's overlong reshape, GSPO)
- [[../rlvr-mechanics/_overview]] — reinforces the "reward is the bottleneck, not the optimizer" theme: even optimizer-side length-bias fixes are provably constrained once the reward is outcome-only
- [[../../weekly-briefs/2026-08-07]] — brought in by the 2026-08-07 weekly sweep
