# BERT-of-Theseus: Compressing BERT by Progressive Module Replacing

BERT-of-Theseus trains a compact successor network by stochastically replacing predecessor modules with smaller successor modules during fine-tuning, using a linear curriculum that ramps the swap probability from near-zero to 1 over training. No auxiliary distillation loss is used — the sole objective is task cross-entropy; predecessor weights are frozen and never updated. This is the **closest direct analogue in the literature to G1 (swappable isolated block training)**: the Bernoulli gate is precisely the "isolated block" swap mechanism at training time, and a successor module must produce outputs compatible with frozen predecessor context on both sides. The method achieves 98.4% of BERT-base's GLUE dev macro score at 6 layers with at most 20 GPU hours per task, substantially outperforming KD baselines in the task-specific (no external corpus) setting.

## Method core

The predecessor $P = \{\text{prd}_1, \dots, \text{prd}_n\}$ is partitioned into $n$ modules; each has a compact substitute $\text{scc}_i$. At each forward pass, position $i+1$ draws an independent gate:

$$z_\ell(t) \sim \text{Bernoulli}(p(t))$$

and computes:

$$\mathbf{y}_{i+1} = z \cdot \text{scc}_i(\mathbf{y}_i) + (1 - z) \cdot \text{prd}_i(\mathbf{y}_i)$$

Only successor weights receive gradients. A linear curriculum scheduler

$$p_d = \min(1,\; kt + b)$$

ramps $p$ from a low base rate to 1, simultaneously acting as a warm-up (expected gradient contribution scales as $p_d \cdot \text{lr}$). Training proceeds in two phases: (1) the replacing stage above, then (2) a successor fine-tuning stage where all predecessor modules are discarded and $S = \{\text{scc}_1, \dots, \text{scc}_n\}$ is fine-tuned on the task alone. Default target is 12 → 6 layers (1.94× speed-up); 4- and 3-layer targets are also evaluated.

Curriculum scheduling is causally important: it outperforms constant-rate replacing by +6.7 CoLA / +1.9 MRPC. Anti-curriculum (starting at high $p$ and decreasing) degrades below even the constant-rate baseline, confirming the easy-to-hard ordering is the mechanism.

## Goal relevance

**G1 (swappable isolated blocks) — direct analogue.** The entire training procedure is defined by block-level interchangeability. A successor module is forced, at every forward pass where $z = 1$, to produce representations compatible with the frozen predecessor stack above and below it — with no additional coupling loss. This is the canonical prior-art instantiation of the isolation principle: Theseus achieves it via stochastic replacement under a frozen-context constraint. The key difference from G1 as a research goal is that Theseus targets compression (fixed 2:1 layer ratio, single final assembly) rather than a reusable pool of independently swappable blocks. See [[dcr]] for the direct successor that replaces the stochastic gate with a deterministic blend.

**G2 (dynamic per-block parameter allocation) — background evidence only.** The paper's layer-sensitivity analysis (Table 5) shows early modules are harder to compress (first-module replacement causes disproportionate harm: −3.37 QNLI vs. ≤−1.41 for modules 2–6), which is relevant empirical evidence for per-block allocation decisions, but the method uses a fixed grouping with no dynamic sizing.

**G3 (token-conditional routing) — not addressed.** The gate is per-batch, not per-token; the method cannot adapt to token-conditional routing without architectural changes.

## Credibility

- Venue: EMNLP 2020 (arXiv 2002.02925, Feb 2020)
- Code: public — https://github.com/JetRunner/BERT-of-Theseus; MNLI-compressed weights released
- Ablation rigor: strong — replacing rate sensitivity, curriculum vs. anti-curriculum vs. constant rate, per-module replacement impact, and 3/4/6-layer targets, all with 5-run medians on GLUE-dev

## Empirical claims

- Retains **98.4% / 98.3%** of BERT-base GLUE dev/test macro score at 6 layers (81.2 vs. 82.5 dev; 78.6 vs. 80.0 test).
- Outperforms vanilla KD (+2.7 dev macro), [[bert-pkd]] (+2.0), and [[distilbert]] (+4.7) in the task-specific (no external corpus) setting.
- [[tinybert]] and [[mobilebert]] excluded from direct comparison — data augmentation and non-standard block design, respectively, make comparisons uninformative; they represent a separate ceiling.
- Peak GPU memory ≈ fine-tuning BERT-base (at most 12 layers active simultaneously on V100 16 GB).
- Training cost: ≤20 GPU hours per task vs. 720 GPU hours for DistilBERT pretraining compression.

## Open questions / failure modes

- **Heterogeneous hidden sizes** — predecessor and successor must share hidden dimension; cross-size replacement requires explicit projection (noted as future work).
- **Pretraining compression** — evaluated only in task-specific setting; whether the method transfers to pretraining-scale compression without labeled signal is untested.
- **Module granularity** — the 2:1 layer grouping is fixed by hand; no search over groupings or irregular partitions.
- **Replacing rate vs. dataset size** — optimal $p$ varies per task; the paper offers no predictor for tuning it.
- **Anti-curriculum failure mechanism** — empirically strong but not fully explained beyond the "easy-to-hard" framing.
- **No token-level granularity** — gate is per-batch; adapting to token-conditional routing requires architectural changes.

## Source

- `raw/research/block-training-quantization/14-bert-of-theseus.md` (PDF capture)
- `raw/research/block-training-quantization/06-bert-of-theseus-abs.md` (arXiv abstract)

## Related

- [[dcr]] — direct successor; replaces stochastic Bernoulli gate with deterministic blend, addresses cold-start instability
- [[block-isolation-training]] — concept anchor; Theseus is the canonical module-replacement instantiation of the isolation principle
- [[iterative-layer-distill]] — heal-after-removal sibling; both rely on neighbor compensation when a block is altered
- [[layerskip]] — different isolation pressure (skip rather than swap)
- [[distilbert]] — KD baseline for compression
- [[bert-pkd]] — Patient KD baseline (intermediate-layer distillation alternative)
- [[tinybert]] — KD ceiling, excluded from direct comparison due to data augmentation
- [[mobilebert]] — non-standard block design, also excluded
- [[layerdrop]] — structured-dropout pruning baseline used in experiments
- [[pabee]] — early-exit complementary acceleration
