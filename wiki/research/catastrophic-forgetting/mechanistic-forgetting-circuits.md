# Mechanistic Origins of Catastrophic Forgetting: Circuit-Level RL vs. SFT Comparison

RL (Dr.GRPO) preserves 72.5% of base-model attention-head circuits after two epochs of science-QA fine-tuning vs. SFT's 59.0%, and this circuit-level divergence better predicts capability retention than output-space KL divergence. The key mechanistic finding: RL acts as a **distributed adaptor** (broad circuit retention, causally engaged heads) while SFT acts as a **compressor** (concentrates adaptation into specialist heads, loses prior capabilities faster). This provides the circuit-level substrate that [[research/catastrophic-forgetting/rls-razor]] identified behaviorally but lacked mechanistically.

*This page covers arXiv:2605.28860. See [[research/catastrophic-forgetting/mechanistic-forgetting]] for arXiv:2601.18699 (gradient interference / representational drift / loss-landscape flattening account).*

## Method

Three-phase pipeline on Qwen2.5-3B-Instruct (Task A = SciKnowEval science QA; Task B = retention benchmarks):

**Phase I — Behavioral comparison.** Train $\pi_\text{SFT}$ (completion-only cross-entropy) and $\pi_\text{RL}$ (Dr.GRPO refining $\pi_\text{SFT}$: group size 64, μ=2 refinement steps, binary domain-specific rewards, no explicit KL penalty).

**Phase II — Circuit identification via Differential Binary Masking (DBM).** For each of $\pi_\text{base}$, $\pi_\text{SFT}$, $\pi_\text{RL}$, learn a soft mask over attention heads:

$$\tilde{a}_h = (1 - m_h)a_h^\text{base} + m_h a_h^\text{source}$$

Masks are annealed toward binary. Triplets (x_base, x_source, y_target) encode counterfactuals (answer-key swaps, molecule swaps, task-type swaps). Mask objective:

$$\mathcal{L}_\text{DBM} = -\log P(y_\text{target}|x, \tilde{a}) + \lambda \sum_h m_h$$

**Phase III — Cross-model comparison.** Circuit faithfulness $F(C|M)/F(M)$ (Eq. 3). Per-head mask shift:

$$\Delta m_h(M) = m_h^M - m_h^\text{base}, \quad M \in \{\pi_\text{SFT}, \pi_\text{RL}\}$$

Vulnerable heads: $C_\text{vuln} = \{h : m_h^\text{SFT} < m_h^\text{RL} - \delta\}$. Differential Causal Mediation (DCM) measures causal signal carried by the retained circuit on the answer-key counterfactual.

## Key findings

- At high new-task score (NTS > 65%), **RL retains 72.5% of base circuit heads vs. SFT 59.0%** after 2 epochs (13.5 pp gap).
- RL circuit size ~296 heads (51.4%) vs. SFT ~265 (46.0%); base = 297 (51.6%).
- **RL base-circuit head overlap 68% vs. SFT 52%** (Figure 4/8 pairwise matrix: Base∩RL=200 heads vs. Base∩SFT=153 heads).
- RL DCM scores higher than SFT at both epochs (15.8 vs. 10.4 at Ep1; 10.6 vs. 6.3 at Ep2) — RL's retained heads carry more causal signal.
- **RL has larger output-space KL from base than SFT while retaining more capability** — KL is a misleading proxy for internal forgetting in this setting.
- SFT produces a tight cluster of high-necessity/high-sufficiency "critical specialist" heads (Figure 3); RL maintains a flat distribution tracking the base model.
- RL circuit recovery between epochs: 69.8% → 72.5% (Ep1 → Ep2), suggesting RL dynamics can partially recover circuits during continued training.

## Mechanistic account

- **SFT = compressor:** drives adaptation into a small number of specialist heads with high necessity and sufficiency for the new task. Those heads become critical, and when new-task accuracy rises further, they displace base-model functionality.
- **RL = distributed adaptor:** spreads task adaptation across a broader subgraph that maintains more overlap with the base circuit. The causally engaged heads (high DCM) are distributed rather than concentrated, making the circuit more robust to forgetting base capabilities.
- **KL is insufficient:** the output-space behavioral divergence (KL) does not predict circuit retention. RL can have higher KL while retaining more circuits — the internal and behavioral divergence measures dissociate.

## Critical caveat on experimental symmetry

$\pi_\text{RL}$ is initialized from $\pi_\text{SFT}$ (two-stage protocol), not from $\pi_\text{base}$ directly. This confounds clean attribution: circuit differences may partly reflect the extra training steps RL receives. The SFT vs. RL comparison is not symmetric; matched-accuracy comparison across conditions is not clearly stated. Flagged in the paper; worth noting when citing the 13.5 pp circuit retention gap as causal evidence.

## Key limitations

- Single model (Qwen2.5-3B-Instruct); no cross-architecture or cross-scale validation.
- Circuit analysis restricted to attention heads; MLP layers not analyzed.
- Narrow task set (science QA); multilingual, factual recall, safety, tool-use not covered.
- RL shows slower task adaptation (lower NTS at matched epochs) — the mechanistic preservation comes at a performance cost.

## Key figures

- **Figure 1:** Circuit retention trajectories over 2 epochs for high-NTS models: SFT 100%→63.5%→59.0%; RL 100%→69.8%→72.5%. DCM values in footer.
- **Figure 2:** Performance–preservation trade-off across NTS levels; 15.8 pp gap at peak NTS.
- **Figure 3:** Necessity–sufficiency scatter: SFT clusters in high-N/high-S quadrant ("critical specialists"); RL tracks base model (distributed).
- **Figures 5–6:** Layer-wise retained vs. forgotten heads; SFT forgotten heads concentrate mid-to-late layers.
- **Eq. 3:** Circuit faithfulness $F(C|M)/F(M)$.
- **Eq. 4:** Per-head mask shift $\Delta m_h(M)$.

## Source

- `raw/research/weekly-2026-06-26/03-mechanistic-forgetting-circuits.md` (arXiv:2605.28860)

## Related

- [[research/catastrophic-forgetting/mechanistic-forgetting]] — companion page; arXiv:2601.18699 covers gradient interference / representational drift / loss-landscape flattening; this page adds circuit-level DBM analysis
- [[research/catastrophic-forgetting/rls-razor]] — behavioral account this paper mechanistically grounds: RL's Razor shows RL forgets less; this paper provides the circuit-level "why"
- [[research/catastrophic-forgetting/_overview]] — extends the three nested RL-locality constraints with a circuit-level dimension
- [[research/rl-optimizers/dr-grpo]] — Dr.GRPO is the RL algorithm used; paper characterizes Dr.GRPO's training dynamics at the circuit level
- [[research/rlvr-mechanics/rl-sparse-subnetwork]] — Balashov finds RL updates only 5–30% of weights; complementary weight-level vs. head-level view of RL's sparse modification pattern
- [[research/selective-finetuning/_overview]] — SFT-as-compressor finding parallels skill-localization work (Panigrahi: 0.01% params carry >95% skill)
- [[research/synthesis/fine-tuning-best-practices]] — adds mechanistic evidence supporting the SFT→RLVR ordering recommendation
- [[research/weekly-briefs/2026-06-26]] — brought in by the 2026-06-26 weekly sweep
