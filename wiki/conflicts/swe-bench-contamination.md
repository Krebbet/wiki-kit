# Conflict: SWE-bench contamination resistance vs SWE-Cycle contamination detection

**Status:** OPEN — SWE-Cycle's contamination filter challenges SWE-bench Pro's primary differentiator claim; the underlying contamination statistic derives from a third-party source (Liang et al.) not yet independently replicated in the wiki.

SWE-bench Pro presents contamination resistance via GPL/private-repo sourcing as its central design commitment and uses this to argue its solve rates reflect genuine agent capability. SWE-Cycle's dataset construction pipeline removes 128 instances from its aggregated source pool — including instances drawn from Pro — on contamination grounds, citing ~35% exact 5-gram match on reference patches and ~76% buggy-file localization accuracy without repo access. These two positions cannot both be fully correct.

## Position A — SWE-Cycle: contamination is substantial and applies even to Pro instances

From SWE-Cycle (arXiv 2605.13139, Section 3.1, Contamination Detection): the benchmark removes 128 of its initial instances via contamination filtering applied uniformly across all three source pools (SWE-bench Verified, SWE-bench Pro, SWE-bench Multilingual). The reported statistics — ~35% exact 5-gram match rate on reference patches and ~76% buggy-file localization accuracy without any repo access — suggest that published solve rates on SWE-bench Verified and Pro are substantially inflated by memorization.

SWE-Cycle sources this contamination statistic from Liang et al. 2025, "The SWE-bench Illusion" (ref [18] in the paper). The filter is applied as a first-stage preprocessing step before lifecycle-complexity and test-reliability filters.

**Implication:** if contamination inflates results even in Pro's GPL/private-repo instances, then the solve-rate gap between Verified and Pro understates the total inflation in Verified, and Pro's absolute solve rates are not a clean signal of genuine capability.

## Position B — SWE-bench Pro: contamination-resistant sourcing as primary differentiator

From the SWE-bench Pro benchmark ([[evaluation/swe-bench-pro]]): tasks are drawn from GPL-licensed open-source repositories and 18 private startup codebases. The use of copyleft licensing and proprietary code creates legal and access barriers against inclusion in training corpora. The private-set results (performance drops sharply on proprietary codebases: Claude Opus 4.1 falls from 22.7% → 17.8%; GPT-5 from 23.1% → 14.9%) are presented as confirming that public-set scores still overstate real-world applicability — but within the framework that Pro's overall design resists contamination.

**Implication:** GPL and private-repo gating operationalizes contamination defense at dataset-construction time. The Pro leaderboard solve rates (23–59% range for frontier models) are presented as reflecting genuine capability in a contamination-resistant setting.

## Working position

This conflict is unresolved. Key considerations:

- SWE-Cycle's contamination statistic is not first-party to the SWE-Cycle authors — it is cited from Liang et al. 2025 ("The SWE-bench Illusion"), which is not yet captured in this wiki. Until that paper is ingested and its methodology assessed, the ~35% 5-gram match and ~76% localization figures should be treated as collect-but-confirm.
- GPL/private-repo gating (Position B) prevents future training contamination but does not address contamination from repositories that were already public and indexed before the benchmark was constructed. The two positions may be addressing different contamination vectors rather than the same one.
- The practical implication regardless of resolution: absolute solve-rate comparisons across SWE-bench Verified, SWE-bench Pro, and SWE-Cycle are not directly comparable until contamination filtering is applied uniformly and from a consistent methodology. Practitioners should treat leaderboard rankings as directional, not precise.

Resolution rule: escalate to curator ruling once Liang et al. 2025 is ingested and its contamination detection methodology can be assessed against Pro's sourcing claims.

## Source

- `raw/research/weekly-2026-05-18/02-swe-cycle.md`

## Related

- [[evaluation/swe-cycle]] — source of Position A; SWE-Cycle applies the contamination filter in its dataset construction pipeline.
- [[evaluation/swe-bench-pro]] — source of Position B; contamination-resistant sourcing is Pro's primary differentiator claim.
