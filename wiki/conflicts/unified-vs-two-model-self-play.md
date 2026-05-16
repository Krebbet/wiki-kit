---
name: unified-vs-two-model-self-play
description: Conflict — R-Zero claims unified-model (single LLM in two roles) self-play collapses after one iteration, requiring two independent base-LLM copies. AZR and LSP both run unified-model self-play successfully. Resolution candidate: stabiliser presence (mode diversity vs quality reward vs hard architectural separation).
type: conflict
status: open
---

# Conflict — Unified-Model vs Two-Model Self-Play Stability

## Position A — [[../research/self-play/r-zero]] (Huang et al., arXiv:2508.05004, Aug 2025)

R-Zero uses **two independent base-LLM copies** for Challenger and Solver roles. Appendix D ablation directly compares this setup against a unified-model variant (single shared model in both roles).

**R-Zero claim:** the unified-model variant **collapses after one iteration**, with lower pseudo-label accuracy throughout. The two-model split is presented as the *stability mechanism* — without it, training fails.

## Position B — [[../research/self-play/azr]] + [[../research/self-play/language-self-play]]

[[../research/self-play/azr]] (Zhao et al., arXiv:2505.03335) uses **one shared model** in both proposer and solver roles. Trains successfully. **No KL leash** (Table 3: `KL Loss = False`, `KL Reward = False`). AZR-Coder-7B reaches +15pp OOD math from code-only training. Three task modes (deduction / abduction / induction) provide diversity.

[[../research/self-play/language-self-play]] (arXiv:2509.07414) uses **one shared model** in both Challenger and Solver roles. Trains successfully on Llama-3.2-3B-Instruct. Game is **general-sum** rather than zero-sum: both players receive a 0–7 quality self-reward from the reference model in addition to their adversarial reward. The paper explicitly notes that **without** the quality reward, the Solver hacks by answering everything in Python.

[[../research/self-play/sqlm]] (Chen et al., arXiv:2508.03682) also uses **one shared model**. Goldilocks gate $R_P = \mathbb{1}[0 < \lvert\{y_i = y_\text{maj}\}\rvert < N]$. No reported collapse.

[[../research/self-play/spice]] (Liu, Jin et al., arXiv:2510.24684) also uses **one shared model**. Variance-at-50% reward. No reported collapse.

## Tension

R-Zero's Appendix D claim — *unified-model self-play collapses* — is in direct empirical contradiction with at least four other papers (AZR, LSP, SQLM, SPICE) that successfully train unified-model self-play. R-Zero's claim cannot be that unified self-play *generally* collapses; it must be that *unified self-play under R-Zero's specific reward shape* collapses.

## Editorial reading — stabilisers as the load-bearing axis

The four working unified-model papers each have a distinct *stabiliser* against collapse:

| Paper | Unified-model | Stabiliser |
|---|---|---|
| [[../research/self-play/azr]] | yes | **Task-mode diversity** — three reasoning modes (deduction / abduction / induction) prevent collapse to a single trivial pattern. No KL. |
| [[../research/self-play/language-self-play]] | yes | **Quality self-reward** — 0–7 score from reference model, added to both players. Makes the game *general-sum*; both have an incentive in joint quality, not just adversarial outcome. |
| [[../research/self-play/sqlm]] | yes | **Goldilocks gate hard floor** — proposer reward is binary; trivially-easy and impossible questions both get $R_P = 0$. Topic-string conditioning prevents drift. |
| [[../research/self-play/spice]] | yes | **Structural information asymmetry** — Reasoner doesn't see document $d$; questions must be answerable from the doc. Corpus grounding prevents both hallucination and trivialisation. |

R-Zero's reward shape — symmetric uncertainty $r = 1 - 2\lvert\hat{p} - 1/2\rvert$ + BLEU repetition penalty — has no comparable hard floor or general-sum incentive, no task-mode partition, no structural asymmetry, no topic conditioning. The repetition penalty is a *soft* diversity signal but the symmetric peak at 0.5 means the proposer has no anchor when both halves of the curve are accessible — it can drift either direction.

**Hypothesis:** unified-model self-play is *always* collapse-prone; success requires an explicit stabiliser. R-Zero's two-model split is *one* stabiliser; the other four papers found *different* stabilisers that work in one model.

If true, the architectural choice (one model vs two) is not the load-bearing axis — the *stabiliser presence* is.

## Resolution status

**Open.** *(2026-05-10 update.)* [[../research/teacher-student-rl/mad-opd]] (arXiv:2605.01347) adds an adjacent data point from the OPD-supervision angle: **MT-OPD** (naive multi-teacher averaging without debate) underperforms single-teacher OPD on code in 4/6 configs due to per-token gradient interpolation across incompatible code paths — i.e. multi-model can be *worse* than unified when no stabiliser (the debate transcript + softmax confidence weights, in MAD-OPD's case) is present. This is consistent with the editorial reading: the **stabiliser**, not architectural multiplicity, is the load-bearing axis. MAD-OPD's success comes from a debate-transcript stabiliser; MT-OPD's failure shows multi-model alone is not the answer.

The four working self-play papers each pre-date or are concurrent with R-Zero, but none directly tests R-Zero's reward shape under unified-model architecture. The empirically clean test would be: take R-Zero's reward shape exactly, run unified vs two-model with all else held fixed, vary the stabiliser. None of the captured papers does this.

Until then, the wiki should:
- Treat R-Zero's "unified collapses" claim as **scope-restricted** — it holds for R-Zero's reward shape, not as a universal claim.
- Treat **stabiliser presence**, not architectural separation, as the load-bearing design axis when designing inner-loop self-play.
- For [[../research/synthesis/proposed-method]]: if the inner loop uses a unified-model self-play structure, an explicit stabiliser must be chosen — task-mode diversity, quality self-reward, hard Goldilocks floor, or structural asymmetry — not omitted.

## Related

- [[../research/self-play/_overview]] — covers the architectural decision in §"Other structural axes"
- [[../research/self-play/r-zero]] — Position A
- [[../research/self-play/azr]] — Position B (mode diversity stabiliser)
- [[../research/self-play/language-self-play]] — Position B (quality reward stabiliser)
- [[../research/self-play/sqlm]] — Position B (Goldilocks hard floor)
- [[../research/self-play/spice]] — Position B (structural asymmetry)
- [[../research/synthesis/proposer-reward-shapes]] — comparison table of proposer-reward shapes; stabiliser column candidate
- [[../research/synthesis/proposed-method]] — design decision input
- [[../research/teacher-student-rl/mad-opd]] — MT-OPD failure mode (multi-teacher without stabiliser) (2026-05-10)

## Source

Conflict between captured wiki pages (cross-source tension, no single raw doc):
- Position A (unified collapses): [[../research/self-play/r-zero]] (Appendix-D collapse), [[../research/teacher-student-rl/mad-opd]] (MT-OPD failure without stabiliser)
- Position B (unified works with a stabiliser): [[../research/self-play/azr]], [[../research/self-play/language-self-play]], [[../research/self-play/sqlm]], [[../research/self-play/spice]]
