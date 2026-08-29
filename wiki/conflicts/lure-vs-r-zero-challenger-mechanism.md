# LURE vs R-Zero — is R-Zero's challenger a learned frontier-positioning policy or a post-hoc rejection filter?

## Positions

**Position A — LURE ([[../research/self-play/lure-pursuit-evasion]]).** LURE's introduction and related-work section characterise R-Zero's curriculum mechanism as **post-hoc rejection filtering with no learned positioning**: "existing zero-data self-play... gives its curriculum no explicit difficulty axis... learnability is enforced only post hoc, by probing each candidate with solver rollouts and rejecting those whose empirical solve rate falls outside a fixed band." On this reading, R-Zero's challenger authors problem text without any frontier-seeking training signal, and quality control happens entirely by discarding out-of-band candidates after the fact — costing "a probe of solver rollouts per candidate." LURE positions its own pursuit-evasion evader (RL-trained to converge on $p \approx 1/2$) as the first *learned* frontier-positioning mechanism, in contrast to this hand-tuned filtering baseline.

**Position B — R-Zero ([[../research/self-play/r-zero]]).** The wiki's own R-Zero page documents the Challenger as trained via GRPO on the **Goldilocks reward** $r_\text{uncertainty}(x;\phi) = 1 - 2\left|\hat{p}(x;S_\phi) - \tfrac{1}{2}\right|$ — a continuous, symmetric reward that peaks at 50% solver accuracy and is used as a genuine RL training signal for the Challenger, theoretically motivated via a KL-divergence lower bound maximised at $\hat p = 0.5$ (Appendix F). This is mathematically equivalent (up to a factor of 2) to LURE's own capture-frontier reward $\min(p, 1-p)$. Separately, R-Zero also applies a **post-hoc band filter** ($|\hat p_i - 1/2| \le 0.25$) when constructing the Solver's training set — but that filter operates on top of an already frontier-trained Challenger, not instead of one.

## Tension

If Position B's reading is correct, LURE's related-work characterisation omits that R-Zero's challenger training objective is *already* frontier-seeking via RL — making LURE's claimed core novelty ("learned vs. hand-tuned positioning") narrower than stated in the paper's own framing. The two mechanisms (Goldilocks-reward RL training vs. capture-frontier-reward RL training) would then be near-identical in objective, differing mainly in the **downstream credit structure** (LURE's planner-executor pursuer gets dense per-step verifier-progress credit; R-Zero's Solver gets sparse binary reward) rather than in how the curriculum-generating side is trained.

## Resolution rule

*(Open — no ruling yet.)* Possible reconciliations, none yet checked against the primary R-Zero source (arXiv:2508.05004):

- LURE's characterisation may be accurate if, in practice, R-Zero's Goldilocks-reward RL training is weak/under-trained relative to the band filter's effect on final data composition — i.e. the filter does most of the real work and the RL signal is close to vestigial. Not tested by either paper.
- LURE and R-Zero may simply be talking past each other: LURE's related-work paragraph may be summarising R-Zero's *net effect* (filtered dataset) rather than its *training mechanism* (Goldilocks RL), in which case this is an imprecise literature characterisation rather than a genuine mechanistic disagreement.
- If R-Zero's Goldilocks reward and LURE's capture-frontier reward are indeed equivalent RL objectives, LURE's genuine novelty would narrow to the **dense process-credit** side (verifier-progress reward for the pursuer/solver) rather than the curriculum-positioning side — worth checking whether LURE's own ablations (isolating curriculum vs. credit vs. stabilisation contributions) actually attribute LURE's gains to the credit mechanism rather than the curriculum mechanism, which would support this reconciliation.

**What would resolve it:** re-read R-Zero (arXiv:2508.05004) directly to confirm whether the Goldilocks-reward Challenger training and the post-hoc band filter are both load-bearing in R-Zero's actual pipeline, or whether one dominates; then re-check LURE's ablation results (which of curriculum / credit / stabilisation actually drives its reported gains over R-Zero) to see whether its novelty claim survives under the corrected characterisation.

## Source

Surfaced via the 2026-08-28 weekly sweep. LURE (arXiv:2608.21871), Introduction and Related Work, in `raw/research/weekly-2026-08-28/.ingest/04-lure-pursuit-evasion-self-play.summary.md`, checked against the wiki's existing [[../research/self-play/r-zero]] page (itself sourced from arXiv:2508.05004).

## Related

- [[../research/self-play/lure-pursuit-evasion]] — Position A paper
- [[../research/self-play/r-zero]] — Position B paper (wiki's existing characterisation)
- [[../research/self-play/_overview]] — self-play theme overview; both papers belong to the proposer/curriculum design cluster
- [[unified-vs-two-model-self-play]] — separate open conflict also centred on R-Zero's design claims
- [[../weekly-briefs/2026-08-28]] — brought in by the 2026-08-28 weekly sweep
