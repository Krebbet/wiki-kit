---
name: r-zero
description: R-Zero trains two independent copies of a base LLM (Challenger and Solver) in a co-evolutionary GRPO loop from zero curated data. The Challenger earns a symmetric Goldilocks reward peaking at 50% solver accuracy plus a BLEU-cluster diversity penalty; the Solver trains on majority-voted pseudo-labels filtered to the 30–70% accuracy band. Appendix D ablation shows the unified single-model variant collapses after one iteration — R-Zero's direct empirical challenge to AZR and LSP.
type: research
---

# R-Zero: Self-Evolving Reasoning LLM From Zero Data

Chengsong Huang, Wenhao Yu, Xiaoyang Wang, Hongming Zhang, Zongxia Li, Ruosen Li, Jiaxin Huang, Haitao Mi, Dong Yu. Tencent AI Seattle Lab / WashU / UMD / UT Dallas. *R-Zero: Self-Evolving Reasoning LLM From Zero Data*. arXiv:2508.05004, August 2025. Two independent base-LLM copies co-evolve through a self-generated math curriculum with zero curated data. The Challenger is rewarded for pushing the Solver to near-50% accuracy; the Solver trains on difficulty-filtered, majority-voted pseudo-labels. This is the **two-model** branch of the proposer/solver family — and the paper most directly contesting the unified-model designs of [[azr]] and [[language-self-play]].

## Method

**Architecture.** $Q_\theta$ (Challenger) and $S_\phi$ (Solver) are initialised from the same base checkpoint but maintained as fully separate parameter sets. No gradient flow between them at any point; interaction is purely through sampled data.

**Co-evolution loop.** Challenger trains for 5 steps → difficulty-filtered dataset constructed → Solver trains for 15 steps → repeat (3 iterations in main experiments). Both sides use GRPO (Group Relative Policy Optimization).

**Challenger reward.** Given $m$ Solver rollouts on question $x$, empirical Solver accuracy is:

$$\hat{p}(x; S_\phi) = \frac{1}{m}\sum_{j=1}^{m} \mathbf{1}\{y_j = \tilde{y}(x)\}$$

Uncertainty (Goldilocks) reward — symmetric, peaks at $\hat{p} = 0.5$:

$$r_{\text{uncertainty}}(x;\phi) = 1 - 2\left|\hat{p}(x; S_\phi) - \frac{1}{2}\right|$$

BLEU-cluster diversity penalty (discourages repetitive question clusters of size $|C_k|$ in a batch of $B$):

$$r_{\text{rep}}(x_i) = \lambda \frac{|C_k|}{B}, \qquad \lambda = 1$$

Composite reward (clipped at zero; zero if format check fails):

$$r_i = \max\!\left(0,\ r_{\text{uncertainty}}(x_i;\phi) - r_{\text{rep}}(x_i)\right)$$

The $r_\text{uncertainty}$ form is theoretically motivated via a KL-divergence lower bound: $D_\text{KL}(S_\phi \| S^*) \geq \frac{\hat{p}(1-\hat{p})}{2\beta^2}$, maximised at $\hat{p}=0.5$ (Appendix F).

**Solver reward.** Binary: $r_j = 1$ if answer matches majority-vote pseudo-label $\tilde{y}_i$, else 0. A candidate question enters the Solver training set only if $|\hat{p}_i - 1/2| \leq 0.25$ (i.e., 3–7 of 10 majority-vote answers agree), enforcing a 30–70% accuracy band and discarding likely ill-posed questions.

**Appendix D ablation — unified model.** A "Single-R-Zero" variant shares one model for both roles (matching AZR/LSP design). It peaks at step 15 and collapses immediately after, with pseudo-label accuracy lower at every stage (63.4% vs. 71.0% at step 15). The paper interprets this as internal bias: a single model that both sets and solves questions develops overconfidence that corrupts difficulty calibration.

## Claims

- Qwen3-4B-Base: $+6.49$ on math benchmarks (42.57 → 49.93 after 3 iterations); $+7.54$ on general-domain reasoning (abstract: 23.61 → 31.15).
  - **Caveat:** the $+7.54$ figure from the abstract may refer to a specific subset; Table 2 overall-average delta computes as approximately $+4.81$ (31.15 − 26.34). Verify against the paper before citing the headline number.
- Qwen3-8B-Base: $+5.08$ math, $+2.52$ general.
- OctoThinker-3B (Llama-3.1 lineage): $+2.68$ math.
- Outperforms AZR on Qwen3-4B (math 49.93 vs. 46.42; general 31.15 vs. 29.33) and Qwen3-8B math. AZR wins on OctoThinker-3B general (16.03 vs. 11.12).
- R-Zero pre-training then SFT on math12k yields $+2.35$ points over SFT-alone (sequential beats concurrent mixing).

## Why this is load-bearing

**Architecture decision.** Any future self-play inner loop must choose: one model or two. R-Zero is the strongest current evidence for two-model stability, but [[azr]] and [[language-self-play]] succeed with one. The open question is whether collapse is intrinsic to unified models or is stabiliser-dependent — see [[../../conflicts/unified-vs-two-model-self-play]].

**Reward shape taxonomy.** Adds row 8 to [[../synthesis/proposer-reward-shapes]]: symmetric Goldilocks $r_\text{uncertainty}$ plus BLEU-cluster diversity penalty. Functionally identical to SPICE's Bernoulli-variance signal; distinct from [[sqlm]]'s hard Goldilocks gate (filter vs. soft reward).

## Limitations

- Verifiability constraint: the co-evolution depends on objectively checkable answers (math/code). Open-ended or subjective tasks are out of scope.
- Iteration collapse: performance degrades after 3–4 iterations across all sizes; pseudo-label accuracy falls from 79% to 63% over 3 rounds. Root cause is multi-factorial (pseudo-label drift + diversity loss on self-synthesized data).
- "Zero data" requires a base with substantial latent math capacity. Gains on weak-capacity bases (OctoThinker-3B general) are modest or below AZR.
- Doubles GPU memory vs. unified-model designs.
- $+7.54$ headline figure ambiguous — see Claims caveat above.

## Source

- `../../../raw/research/self-play-quality-extraction/.ingest/04-rzero.md`
- `../../../raw/research/self-play-quality-extraction/01-04-rzero.md`
- arXiv: https://arxiv.org/abs/2508.05004

## Related

- [[azr]] — unified-model sister; same zero-data framing, doesn't collapse; direct architectural contrast
- [[language-self-play]] — unified-model sister with quality self-reward stabiliser; also doesn't collapse
- [[sqlm]] — Goldilocks gate as hard filter rather than soft reward; same 50%-target intuition
- [[spice]] — two-role design with structural asymmetry; compare stability mechanisms
- [[../synthesis/proposer-reward-shapes]] — reward shape taxonomy; R-Zero adds the BLEU-penalised Goldilocks row
- [[../../conflicts/unified-vs-two-model-self-play]] — open conflict: R-Zero claims unified collapses; AZR + LSP use unified successfully
- [[_overview]] — self-play theme overview
