# DN-MOPD: Domain-Normalized Multi-Teacher On-Policy Distillation

arXiv:2609.35347 (Li et al., submitted 2026-09-28; code github.com/LiXin97/DN-MOPD). Standard MOPD routes each prompt to its domain's RL specialist but ignores how strongly each specialist's token feedback moves the shared student. On Qwen3.5 at three sizes, the MOPD student fails to beat one taught by the single best specialist and recovers little of the math specialist's advantage, because instruction-following feedback is several times more spread out than math feedback and dominates updates. DN-MOPD keeps routing and rescales each domain's feedback by its measured spread.

## Source

- `raw/research/weekly-2026-10-02/05-dn-mopd-domain-normalized.md` (arXiv abs-page capture; abstract only)

## Claims

- Routing decides *who* teaches; magnitude decides *how loudly*. Unnormalised per-domain feedback scale makes high-variance domains (instruction following) dominate the shared student's gradient.
- DN-MOPD improves average over MOPD on six public benchmarks at every model size, across 3 seeds and 2 answer-length limits; recovers most of the lost math gain.
- Fixed-weight controls: the gain comes mainly from turning *down* instruction-following feedback, not turning up math; fixed weights near the DN-measured ones perform comparably (so the measurement, not the online adaptivity, is the load-bearing part).

## Comparison with the other multi-teacher OPD papers

| Paper | Multi-teacher mechanism | Failure mode addressed |
|---|---|---|
| [[mad-opd]] | Debate ensemble, confidence-weighted $w_k$ | Naive averaging below single-teacher on code |
| [[opd-dual-nature-generalization]] | Prompt-routed teacher per domain | Mixture-dependent seesaw |
| [[mopd-gradient-diagnosis]] | Diagnostic (loss averaging, Adam, BF16) | Hidden implicit weighting of responses/domains |
| this page | Routed + per-domain spread normalisation | Domain feedback-scale imbalance |

The seesaw in [[opd-dual-nature-generalization]] and the scale-imbalance here are likely the same phenomenon seen from two sides (domain share vs domain gradient magnitude); [[mopd-gradient-diagnosis]]'s length-weighting finding adds a third implicit weight. No contradiction with existing wiki claims; it refines "routing" as an incomplete specification.

Relevance to the project: any multi-signal OPD/RL stack (e.g. the R_w primitives composed in [[../synthesis/proposed-method]]) needs per-signal scale control, not just selection.

Caveat: abstract only; spread statistic definition (std of per-token feedback? advantage?) not captured.

## Related

- [[mopd-gradient-diagnosis]] — paired gradient-level diagnosis of MOPD
- [[_overview]] — teacher-student-rl cluster
- [[mad-opd]] — debate-ensemble multi-teacher
- [[opd-dual-nature-generalization]] — routed MOPD seesaw
- [[sequential-opd-then-rl]] — alternative to joint multi-teacher training
- [[gc-opd-group-calibrated]] — group-calibrated teacher-signal scaling in single-teacher OPD
- [[../weekly-briefs/2026-10-02]] — brought in by the 2026-10-02 weekly sweep
