# Deterministic Continuous Replacement: Fast and Stable Module Replacement in Pretrained Transformers

DCR replaces [[bert-of-theseus]]'s stochastic Bernoulli gate with a deterministic annealed blend $\alpha(t)$, eliminating gate-induced gradient variance during cold-start module replacement in frozen transformer backbones. A trainable student block $S_\ell$ is blended with a frozen teacher block $T_\ell$ at the residual branch; $\alpha(t)$ decays deterministically from 1 (teacher-only) to 0 (student takeover), providing a smooth, variance-free loss path. An optional Deep Feature Guidance (DFG) auxiliary loss — an L2 penalty on the teacher–student output difference — adds negligible overhead since both outputs are already computed for the blend. Controlled ablations on ViT-Small/CIFAR-100 show faster interface cosine-similarity convergence and earlier accuracy recovery compared to all stochastic-gating and [[knowledge-distillation]] baselines, though scope is tightly constrained (see Limitations).

## Method core

DCR blends frozen teacher $T_\ell$ and trainable student $S_\ell$ outputs on the residual branch with a global deterministic scalar gate $\alpha(t) \in [0,1]$:

$$x_{\ell+1}(t) = x_\ell(t) + \bigl[\alpha(t)\,T_\ell(h_\ell(t)) + (1-\alpha(t))\,S_\ell(h_\ell(t);\theta_\ell)\bigr]$$

with $\alpha(0)=1$ (teacher-only) annealing to $\alpha(T)=0$ (student takeover). The *aggr20* schedule transitions $1.0 \to 0.3$ over the first 10% of training, then $0.3 \to 0.0$ over 10–20%, holding at 0.0 thereafter.

**Contrast with BERT-of-Theseus:** Theseus uses a hard Bernoulli gate $z_\ell(t) \sim \mathrm{Bernoulli}(p(t))$ per forward pass. This introduces gate-induced gradient variance $p(1-p)\,\mathbb{E}\|a(S_\ell;X)\|^2$ (Proposition 2 in paper, where $a := J_{G_\ell}^\top \partial S_\ell/\partial\theta_\ell$). DCR's deterministic gate makes this term exactly zero. Stochastic soft gates (Gumbel-Softmax) still incur a $\mathrm{Var}(r)\,\mathbb{E}\|a\|^2$ residual. DCR additionally avoids curvature bias from stochastic mixing through nonlinearities (Proposition 3) and provides a Lipschitz-bounded smooth loss path (Proposition 4).

**Deep Feature Guidance (DFG):** Optional auxiliary loss $\mathcal{L}_\mathrm{DFG} = \sum_{\ell \in \mathcal{I}} \|S_\ell(h_\ell) - T_\ell(h_\ell)\|_2^2$, annealed on the same aggr20 schedule, controlled by weight $\lambda$. Near-zero marginal overhead since teacher outputs are already materialized for the blend.

## Goal relevance

**G1 (primary) — high.** DCR directly addresses the cold-start stability bottleneck in swappable-block training: integrating a randomly re-initialized student into a frozen backbone without destabilizing downstream layers. This is the precise mechanism needed when [[block-isolation-training]] isolated blocks must re-enter a frozen backbone without corrupting its output distribution.

**G2 / G3 — not addressed.** No dynamic parameter allocation (G2) or token-conditional routing (G3) content. The blend gate is global (not per-token or per-layer adaptive); per-layer adaptive $\alpha$ is flagged as future work.

## Credibility

- Venue: NeurIPS 2025 ScaleOPT **Workshop** (not main track)
- Code: not released — "will be released in a future extended version"
- Weights: not released
- Replication: none; single institution (Bradbury Group, independent non-profit)
- Ablation rigor: partial — controlled self-replacement ablation isolates stability from representational mismatch; baselines include Theseus-Bernoulli, Theseus-Gumbel, Theseus-Gumbel+DFG, KL distillation; **single seed only** (authors flag this explicitly); ViT-Small/CIFAR-100 only

## Empirical claims

- DCR and DCR+DFG achieve higher interface cosine similarity (residual output alignment) than all stochastic baselines throughout training; largest gains in mid and late blocks (Blocks 7, 11 of ViT-Small/16).
- DCR variants reach target accuracy sooner in both epoch and wall-clock time on CIFAR-100 vs. stochastic gating and distillation baselines; final accuracies comparable across all methods (~78–80%).
- DCR+DFG overhead over standard DCR is negligible — teacher outputs already materialized.
- Stochastic baselines (BERN, GUM) exhibit "gate-induced starvation": delayed deep-layer convergence from mid-training variance.
- Authors explicitly frame results as "feasibility evidence rather than definitive benchmarking."

## Open questions / failure modes

- Global $\alpha(t)$ schedule: no per-layer or progressive schedules explored; may be suboptimal for deep architectures with varied layer sensitivity.
- Theory is local/conditional (frozen tail, fixed input distribution per step) — not full training-dynamics guarantees.
- No compute-saturated regime experiments (large LLMs, diffusion transformers) despite this being the stated efficiency motivation.
- Scope limited to pre-norm residual transformers (ViT-Small); batch-norm or other normalization schemes flagged as potentially different.

## Limitations

1. **Workshop paper, not main track.** NeurIPS 2025 ScaleOPT is a workshop venue; the paper has not passed main-track peer review. Results should be treated as preliminary.
2. **Single seed only.** All reported numbers are single-seed. Authors acknowledge this explicitly. No error bars or variance estimates exist; the statistical reliability of any claim is unknown.
3. **No code released.** Reproducibility is entirely dependent on the methods description; no independent replication has been attempted.
4. **Heterogeneous-operator experiments: zero empirical support.** The paper's stated motivation is swapping standard attention for efficient alternatives like [[linformer]] and [[performer]]. No such experiment appears anywhere in the paper. This gap between stated motivation and actual evidence is significant.
5. **Self-replacement only.** Every experiment replaces a block with a re-initialized copy of the *same* operator (attention → re-initialized attention). The paper does not demonstrate DCR stability under any representational mismatch between teacher and student operators.

## Source

- `raw/research/block-training-quantization/15-dcr.md` (PDF capture)
- `raw/research/block-training-quantization/07-dcr-abs.md` (arXiv abstract)

## Related

- [[bert-of-theseus]] — direct predecessor; DCR replaces the Bernoulli gate with a deterministic blend
- [[block-isolation-training]] — concept anchor; DCR addresses cold-start stability for swappable-block training
- [[knowledge-distillation]] — explicit baseline; DCR avoids full teacher forward pass cost
- [[linformer]] — cited as target heterogeneous operator for future DCR work (no current empirical support)
- [[performer]] — same as above
