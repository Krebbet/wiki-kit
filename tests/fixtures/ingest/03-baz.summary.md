---
source: "raw/research/demo/03-baz.md"
slug: "03-baz"
summarized_on: "2026-04-21"
schema_version: 1
---

# Baz: Another Preference Method

## One-line
Baz is another preference-optimization objective with a DPO-like structure.

## Method
Preference optimization via a modified DPO loss with margin term.

## Results
Small gains over DPO on three benchmarks.

## Applicability
Drop-in DPO replacement.

## Novelty
Refinement of DPO.

## Reproducibility
Code pending; weights released.

## Adoption
Single-lab result so far.

## Conflicts
Claims AlpacaEval score higher than what Bar reports on the same setup.

## Cross-ref candidates
- [[dpo]] — derives from
- [[rlhf]] — background

## Conflict flags
- Claim: Baz reports 72.1 on AlpacaEval under standard settings.
  Contradicts: [[dpo]] which cites 70.8 for the same eval.
  Basis: Table 2, page 6.

## Proposed page shape
- New page: baz-preference-method
