# From Gradients to Capabilities: Understanding Multi-Teacher On-Policy Distillation

arXiv:2610.02179 (Zhu, Huang, Zhang, Yang, Jin, Sun, You; submitted 2026-10-01). Diagnostic study of multi-teacher OPD (MOPD) on Qwen3-1.7B with four RL-trained domain teachers (same init as student), plus SmolLM3-3B checks. Compares raw gradients, optimizer updates and learning curves. Four findings: loss-averaging mode implicitly weights responses; Adam's first moment collapses gradient differences; BF16 rounding hides most of the update; and a top-64 intersection-KL gradient matches full-vocabulary KL but its task effect flips sign with the averaging rule. Companion to [[dn-mopd-domain-normalized]], which attacks the same "how strongly does each teacher count" question with a fix.

## Source

- `raw/research/weekly-2026-10-02/01-multi-teacher-opd-gradient-diagnosis.md` (arXiv abs-page capture; abstract only, no full-text body)

## Findings

| Factor | Observation |
|---|---|
| Loss averaging | Token averaging upweights long responses; equalising domain contributions still keeps this within-domain length weighting |
| Optimizer | Adam first moment shrinks differences: update cosine 0.83 between teachers, 0.96 between averaging rules, despite differing raw gradients |
| Precision | ~97% of FP32 master weights differ from init, only 7-11% of BF16 weights do (rounding hides small updates) |
| Estimator | Top-64 intersection-KL gradient ≈ full-vocab KL gradient (Qwen); math accuracy +2.6 pts vs sampled-token PG under response averaging, -2.1 pts under global token averaging |

Takeaways for this wiki:
- The estimator comparison (sampled-token PG vs truncated full-distribution KL) is only meaningful conditional on the averaging rule; OPD variant comparisons that do not control it are confounded. Relevant to the sampled-token OPD debate in [[opsa-teacher-free-self-adaptation]] and [[ida-opd-entropy-influence]].
- Length weighting is an implicit, uncontrolled reweighting of domains/prompts, a plausible contributor to the routing "seesaw" reported in [[opd-dual-nature-generalization]].
- Update-space similarity of 0.83 between different teachers is a (small-scale, 1.7B) data point that teacher identity moves parameters less than raw-gradient differences suggest; it does not settle [[../../conflicts/opsa-vs-opd-pattern-transfer]] (different measurement: update cosine, not transfer behaviour).
- BF16 masking of small updates is a caveat for any sparse-update claim measured on BF16 weights ([[../rlvr-mechanics/rl-sparse-subnetwork]]); FP32 master-weight diffs differ ~10x.

Caveat: ingested from abstract only; no ablation tables or domain list available.

## Related

- [[dn-mopd-domain-normalized]] — paired MOPD paper: rescale per-domain feedback by measured spread
- [[_overview]] — teacher-student-rl cluster (MOPD sits in the OPD subtree)
- [[opd-dual-nature-generalization]] — routed MOPD seesaw
- [[mad-opd]] — debate-ensemble multi-teacher design (structurally distinct)
- [[opsa-teacher-free-self-adaptation]] — sampled-token OPD mechanism debate
- [[ier-gradient-reliability-opd]] — gradient-geometry view of OPD
- [[../rlvr-mechanics/deepseekmath-grpo]] — response vs token averaging in GRPO-family losses
- [[../rl-optimizers/_overview]] — optimizer-level effects on RL updates
- [[../../weekly-briefs/2026-10-02]] — brought in by the 2026-10-02 weekly sweep
