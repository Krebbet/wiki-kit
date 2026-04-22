---
source: "raw/research/demo/01-foo.md"
slug: "01-foo"
summarized_on: "2026-04-21"
schema_version: 1
---

# Foo: A Novel Method

## One-line
Foo introduces a two-stage training recipe combining SFT with outcome-based RL.

## Method
Two-stage: SFT on curated reasoning traces, then outcome-based RL with a learned reward model. Derives from InstructGPT.

## Results
Table 3: +4.2 pp on MMLU over the SFT-only baseline; matches GPT-4-level Arena scores at 70B.

## Applicability
Requires RL infra and a reward model. Base-model agnostic above 7B.

## Novelty
Novel combination; neither stage alone is new but the staging is.

## Reproducibility
Code released; weights on HF; no paperswithcode entry yet.

## Adoption
Cited by 3 follow-ups within 4 months.

## Conflicts
None with current wiki.

## Cross-ref candidates
- [[rlhf]] — extends with outcome-based variant
- [[sft]] — first stage is standard SFT

## Conflict flags
(none)

## Proposed page shape
- New page: foo-method — Foo is distinct enough from RLHF to warrant its own page
