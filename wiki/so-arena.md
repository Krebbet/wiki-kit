# SO-Arena: Capability and Reliability of System One Models

NUS (arXiv:2611.15777, Nov 2026; code `holdrain/SO-Arena`). Benchmark of 21 no-CoT "System One" decision models (single forward pass, distribution over predefined outcomes) on 2,919 tasks across 11 domains and 5 capability families. Scores capability (hardest tiers, equal domain weights) separately from decision reliability (option-order stability + missing-answer recognition). Headline: best System One models trail GPT-6 Luna by ~10 points but run tens of times faster, and capability rank does not predict reliability rank.

## Benchmark design

- **Sources**: 40 public datasets/environments (GoEmotions, MATH500, GPQA Diamond, Mind2Web, BFCL, ToolSandbox, BrowseComp-Plus, VirtualHome). Labels reviewed manually and by LLM; questionable items dropped; model-derived references flagged.
- **Split**: 2,300 static (choice / yes-no / score) + 619 environment-based (100 single-step web judgments, 237 reference-route multi-step web, 282 interactive BFCL/ToolSandbox episodes). Agentic split into action selection vs. completion verification.
- **Tiers**: 9 of 11 domains have difficulty tiers, defined per domain and not calibrated across domains (paper's own caveat).
- **Capability C**: equal-weight mean over domains of score on the hardest tier (hard + very hard for Math).
- **Reliability R = sqrt(S*N)**, zero unless both exceed chance. S: chance-corrected agreement across 12 option reorderings (consistency, not correctness). N = 2*AUC-1 for ranking p_null = 1 - p(inc) higher on copies with the correct option removed.

## Results

- C: GPT-6 Sol 82.3, Luna 79.7; System One best GLiDE 70.2 and KnowLine-31B 70.2, then Sieve-31B-v3 67.7, Decider-27B 66.7. Jev API 1.14 60.4, JevAny-27B 58.4, OpenAI Decisions 53.6, 0.4B Laya 30.9.
- Latency: all open-weight System One models <0.3 s/task on one H100.
- Gap is domain-shaped: near parity with Luna on knowledge, sentiment, retrieval; GLiDE within 4 points on intent, safety, verification, tools, web; large on Math, Science, Code. Thinking helps most in Math/Science (StartLux Auto Math 50.8 to 92.5).
- Reliability (18 System One models): S is 0.83-0.94 for 14 models, 0.68-0.72 for SII-4B, Kev-4B, OpenAI Decisions, 0.35 for Laya. N spans near-chance to ~0.8 and is only loosely tied to size or capability. Top R: JevAny-27B and Jev API 1.14, ranked 8th and 6th in capability among 18 (the abstract's "best model ranks seventh in reliability" is not cross-checked here).

## Caveats

- Cross-domain tiers uncalibrated; C emphasises hardest tiers only.
- Models run in developer-documented settings, with exceptions (Laya full option length; SII-4B with flash-linear-attention for latency); StartLux Instant scored with its own null output. Closed APIs are timed over the network, so latency is not like-for-like.
- Single paper, no independent reproduction; some listed models are unfamiliar vendor releases (details unverified).

## Source

- `raw/research/weekly-2026-11-14/04-so-arena.md` (arXiv 2611.15777)

## Related

- [[jev-as-a-judge]] — evaluates Jev API 1.14 and Jev-style decision-only models; complements its cascade finding (confidence-gated use) with order-stability and null-recognition measures.
- [[evolutionary-search-eval-rigor]] — same thesis: single aggregate scores hide the structure that matters.
