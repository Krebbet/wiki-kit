# Branch-Train-Merge: Embarrassingly Parallel Training of Expert Language Models

BTM (Li et al., UW / Meta AI, 2022) trains a forest of fully-independent *Expert LMs* (ELMs), each a complete GPT-style model specialised to a single provenance-defined domain, with zero parameter sharing and zero inter-model communication after an initial shared seed phase. New experts are added iteratively via a three-step loop — branch (initialise from a posterior-weighted average of existing experts), train (fine-tune in isolation on the new domain), merge (add to the forest) — and at inference the forest is queried either by output-probability ensembling or by collapsing to a single model via posterior-weighted parameter averaging. At 1.3B parameters per ELM (64 experts, 22.4B total), the ensembled forest matches a monolithic 1.3B TRANSFORMER-LM trained at ~2.5× the compute, while branched training runs 33% faster than synchronised training by eliminating cross-GPU communication.

## Method core

**Architecture.** ELMFOREST $\mathcal{E} = \{\theta_i\}_{i=1}^{k}$; each $\theta_i$ is a full GPT-style LM (125M–1.3B params). No parameter sharing across ELMs. Domains are defined by document *provenance*, not task label.

**Step 0 — Seed.** Train a single LM $\theta_\text{seed}$ on a heterogeneous corpus. Required for parameter averaging to be numerically well-behaved; benefits averaging more than ensembling. Seed corpus choice is robust (even training on JavaScript alone beats a compute-matched monolithic baseline). Optimal compute split: 40–60% to seed phase.

**Step 1 — Branch.** Initialise new ELM $\theta_{k+1}$ as a posterior-weighted parameter average of existing experts:

$$\theta_{k+1} \leftarrow \sum_{i=1}^{k} w_i \, \theta_i$$

Weights $w_i = p(D = i \mid \mathbf{x}_{<t})$ computed on a validation sample from the new domain.

**Step 2 — Train.** Fine-tune $\theta_{k+1}$ on domain $d_{k+1}$ with standard cross-entropy. No communication with other ELMs. Multiple ELMs can be added in a parallel batch; iterations can also proceed asynchronously.

**Step 3 — Merge.** $\mathcal{E}' = \mathcal{E} \cup \{\theta_{k+1}\}$.

**Inference — ensembling.** Domain variable $D$ introduced alongside each sequence; next-token distribution marginalised over experts:

$$p(X_t \mid \mathbf{x}_{<t}) = \sum_{j=1}^{n} p(X_t \mid \mathbf{x}_{<t}, D = j) \cdot p(D = j \mid \mathbf{x}_{<t}) \tag{1}$$

Domain posterior by Bayes' rule:

$$p(D = j \mid \mathbf{x}_{<t}) = \frac{p(\mathbf{x}_{<t} \mid D = j) \cdot p(D = j)}{\sum_{j'=1}^{k} p(\mathbf{x}_{<t} \mid D = j') \cdot p(D = j')} \tag{2}$$

Prior $p(D=j)$ is a cached EMA ($N=100$ dev sequences, decay $\lambda = 0.3$), fixed at test time per domain. Domain posterior is **sparse** at scale: top-8 ELMs out of 64 suffice with negligible loss.

**Inference — parameter averaging.** Collapse forest to a single model: $\theta = \sum_{i=1}^{k} w_i \, \theta_i$. Uniform $w_i = 1/k$ fails badly. Argmax (one-hot) helps only at small scale. Posterior-weighted is best; consistently beats TRANSFORMER-LM at no additional inference cost and approaches ensembling as the number of domains grows. Requires shared seed initialisation — without it, perplexity is in the thousands.

## Goal relevance

**G1 — STRONG.** BTM is the clearest large-scale existence proof that independently-trained model components can be recombined without joint training. Each ELM's gradient flow touches only its own parameters — no global backprop across experts. The seed phase plays the role of establishing a shared initialisation that makes parameter averaging work, directly analogous to the shared trunk a block pool would branch from. The domain-specialisation requirement (random splits consistently underperform domain splits) has a block-level analogue: blocks trained on diverse data or positions may need matching at merge time. See [[block-isolation-training]].

**G3 — STRONG.** Equations 1–2 constitute a soft sequence-conditional router: weights $p(D=j \mid \mathbf{x}_{<t})$ are context-derived and sparse. Posterior-weighted parameter averaging is a static approximation of this routing (weights fixed per validation set). Both mechanisms validate that context-conditional combination of independently trained components is viable and effective. BTM's routing is sequence-level rather than token-level, but the structure is identical to a soft MoE router at coarser granularity; [[btx]] replaces it with a learned token-level gate. See [[token-conditional-routing]].

**G2 — Not directly relevant.** BTM does not address per-block compute allocation or depth-adaptive inference.

## Credibility

arXiv preprint (2208.03306, 2022) — **not peer-reviewed at time of capture**. Directly validated post-hoc by [[btx]] (ICML 2023), its successor, which builds on and extends these empirical findings. Core DEMIX baseline comparison is against a concurrent peer-reviewed result (Gururangan et al. 2022).

## Empirical claims

| Scale (per ELM) | TRANSFORMER-LM PPL | Ensemble PPL | Avg (posterior) PPL |
|---|---|---|---|
| 125M | 22.5 | 19.8 | degrades at this scale without high seed budget |
| 350M | 18.5 | 16.7 | ~17.5 |
| 750M | 17.0 | 15.0 | ~15.5 |
| 1.3B | 16.3 | 14.6 | ~14.9 |

- Branched training is 33% faster (updates/s) at 1.3B scale due to eliminated cross-GPU communication.
- 64-expert ELMFOREST (22.4B total params) matches a 1.3B TRANSFORMER-LM at ~40% of compute.
- Domain specialisation is load-bearing: random-split ensembles consistently worse than domain-split ensembles at matched parameter count.
- Seed compute optimal at 40–60% of total; ensembling is robust across 20–80%; averaging requires ~60–70%.

## Open questions / failure modes

- **Domain posterior requires validation data.** A held-out sample per domain is needed to compute weights. A block-pool analogue for "domain" is unclear; a learned or hash-based router avoids this requirement — see [[btx]].
- **Uniform averaging fails.** Posterior-weighted averaging is non-trivial infrastructure; naive weight-averaging of independently trained LMs produces worse-than-baseline results without domain-informed weights.
- **Random-split ensembles are poor.** Benefit derives from domain specialisation, not from ensembling more parameters. This constrains the G1 analogy: block isolation is only useful if blocks specialise to something meaningful (layer position, data mixture, etc.).
- **Domain definition is heuristic.** Provenance-based domains are coarse; finer or unsupervised splits are left for future work (partially addressed in [[btx]]).
- **Scales studied are modest.** All experiments ≤ 22.4B total parameters; behaviour at larger per-expert scales is uncharted.

## Source

- `raw/research/selective-replacement-and-training/25-btm.md` — PDF capture
- `raw/research/selective-replacement-and-training/07-btm-abs.md` — arXiv abstract
- arXiv: 2208.03306 · Code: https://github.com/hadasah/btm · Captured: 2026-04-30

## Related

- [[btx]] — direct successor; replaces ensemble/averaging with a learned sparse MoE gate (ICML 2023)
- [[demix]] — same domain-expert idea but intra-model granularity (feedforward layers only inside a shared backbone); BTM outperforms at matched compute
- [[sparse-upcycling]] — different path to an expert pool: copies from a dense checkpoint vs BTM's independent training
- [[modular-deep-learning]] — survey context; BTM sits at the extreme "no shared parameters" end of the modular spectrum
- [[block-isolation-training]] — BTM is the model-level existence proof for independent component training; the block-level analogue is G1's open question
- [[token-conditional-routing]] — Eqs. 1–2 are a sequence-conditional soft router; sparse domain posterior at 64 experts foreshadows token-level MoE/MoD sparsity
