---
name: legal-reasoning-competitive-ablation-negative-result
description: Controlled ablation isolating the competitive component of adversarial self-play (live adversary + verifiable survival reward) from an otherwise-identical legal-argument RLVR curriculum finds no reliable benefit across four independent tests plus a strengthened-adversary pilot — competition itself is inert once curriculum/data are held fixed
type: research
---

# Does the Competitive Component of Adversarial Self-Play Improve Legal Reasoning? A Controlled Negative Result

Kim, preprint 2026-08-02, arXiv:2608.01559. An adversarial case-pack RLVR curriculum for legal-argument generation (attack → weakness diagnosis → defense → student argumentation → judge simulation → rebuttal), with a **survival reward**: student drafts, adversary rebuts, both sides' cited authorities are checked by a citation verifier, fabricated citations auto-score zero. The self-play adversary is a periodically-refreshed frozen copy of the student. Posed as RLVR, not SFT imitation, per the standard finding that imitation degrades an already-capable student.

**Controlled variable:** treatment = live adversary + survival reward; control = identical setup, matched compute, minus the competitive component.

## Method — four tests, one pilot

1. Bootstrap on the primary held-out metric.
2. Two-seed replication.
3. Paired per-case adversarial-robustness test.
4. Blinded head-to-head judgment by an independent judge model (position-bias guarded, binomial test).
5. Follow-up pilot: deliberately strengthens the adversary via genuine multi-round self-play (refreshed to latest student checkpoint each round; verified-citation strength rises 56→62 across rounds) to rule out "the adversary was too weak."

## Results — no benefit detected in any test

| Test | Result |
|---|---|
| Bootstrap | Small effect, CI includes zero (~0.41) |
| Two-seed | Directionally positive but non-significant (seed-42 +0.0042, seed-7 +0.0068); doesn't survive Test 3 |
| Paired robustness, n=18 | ~+29% advantage for competitive run |
| Paired robustness, n=29 | **Sign reverses**: Δ≈−0.0069, CI≈[−0.021, 0], n.s. (28/29 tied) |
| Blinded judgment | 28:29:9 → **49%** win rate, p≈1.000 |
| Strengthened-adversary pilot | 32:32:2 → **50%** win rate, p≈1.000 |

The n=18→n=29 sign reversal is the paper's headline methodological pitfall — a small adversarial eval set (n=18) manufactured a large, illusory, sign-flipping effect that vanished on a larger paired set.

## Two reusable methodological pitfalls

1. **The "n=18 mirage"** — small adversarial eval sets can produce large, confident-looking, sign-flipping effects that don't survive modest expansion (n=18→29 here).
2. **Verifiable-reward metric collapse** — a citation-overlap "retained" score silently degenerates into plain recall when the adversary's behavior doesn't match the metric's implicit assumption (that it cites the same authorities as the gold answer) — a concrete instance of reward/metric misspecification distinct from model misbehavior.

## Limitations (acknowledged)

- Pilot-scale, underpowered — explicitly not claimed as definitive refutation; the paper cannot bound the true effect tightly enough to assert it is exactly zero.
- Single task domain (legal only), limited seeds, one adversary/reward instantiation.
- Calls for higher-powered replication: ≥5 seeds, pre-registered primary metric, explicit power analysis, ≥1 additional domain.

## Relation to the wiki

This is the self-play theme's first controlled ablation isolating **the competitive mechanism itself** from **curriculum/data construction**, and it finds only the latter matters — competition is inert once curriculum and compute are held fixed. Directionally consonant with [[understanding-self-play]]'s mechanistic anchor ("the proposer is the critical component; the solver only re-weights base-model probability mass") — the live adversary + survival reward here is a solver-facing competitive mechanism, and it adds nothing once curriculum/data are fixed. Not a strict instance of the AZR-style proposer/solver split though, so it's consonant rather than identical.

The same author's companion coding-domain paper (arXiv:2607.08255, "Compete Then Collaborate") reaches the same structural conclusion in a different domain — value comes from verifiable-environment construction, not competition/answer-pooling — and this legal-domain paper explicitly positions itself as reconfirming that finding.

## Source

- `raw/research/weekly-2026-08-21/04-self-play-legal-reasoning-negative-result.md`

## Related

- [[_overview]] — first controlled ablation directly targeting the theme's mechanistic-anchor question, from a non-math/code domain (legal).
- [[understanding-self-play]] — directionally consistent with "proposer critical, solver reweights"; a different, complementary angle (competition-vs-curriculum rather than support-expansion-vs-reweighting).
- [[invisible-leash]] — Theorem C.1's support-reweighting argument and this paper's competitive-mechanism null are different but complementary evidence for de-emphasizing the solver/competitive side.
- [[spice]] — a different concrete instantiation of "adversarial structure drives the gain, not raw competition" (structural information-asymmetry rather than head-to-head competition).
- [[spiral]] — contrast, not refutation: SPIRAL claims game self-play *does* transfer (+10.5% across 8 benchmarks) via a different domain and structure (symmetric self-play game vs. adversary-attacks-student here) — a domain-boundary data point.
- [[skill-self-play]] — different failure mode: that page shows unguided self-play can fail to bootstrap weak backbones at all; here self-play bootstraps fine, the competitive component specifically just doesn't help.
- [[../teacher-student-rl/_overview]] — via the cited companion coding-domain paper (arXiv:2607.08255), framed as a multi-teacher curriculum result.
- [[../../weekly-briefs/2026-08-21]] — brought in by the 2026-08-21 weekly sweep
