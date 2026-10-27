# Threshold Manipulation in Colombian Public Procurement

Espinal Maya and Jimenez Londono (arXiv 2610.28965, Oct 2026) use the full Colombian procurement record (SECOP I/II, 2011-2026) to show that buyers set estimated contract values just below the legal cutoffs that trigger more competitive procedures, that elected territorial buyers do this more than appointed national ones, and that bunched contracts draw fewer bidders and smaller discounts. It is the largest real-world instance in the wiki of a bright-line rule being gamed at the margin, and a non-Anglosphere test of the rules-versus-discretion trade-off.

**Evidence tier note.** Status: **un-refereed arXiv preprint** ("comments welcome"). Tier (a) for the existence of bunching, which is strongly identified; tier (a) but descriptive for the cost of bunching; the accountability explanation for the elected/appointed gap is closer to (b)/(c). The lead author discloses a financial interest (co-founder of firms consulting for Colombian public entities), and AI tools were used for code and editing, with a self-run 512-check verification battery that is not independent.

## The design and the bunching result

**[empirical]** Unit: the procurement process, matched to an entity-year threshold. 8,569,218 SECOP II processes; about 512k competitive-procedure processes matched to an entity-year threshold; 2,579 entities in the small-purchase window and 1,565 in the tender window. Thresholds are entity-specific (five legal budget bands, set in minimum wages) and move every January (3.5-23%), while the round numbers that usually confound bunching estimates stay fixed. The tender cutoff is set by budget band; the small-purchase cutoff is 10% of it.

**[empirical]** Excess mass: 49,631 processes below the small-purchase cutoff (86% of the mass in the last 5% below it) and 3,157 below the tender cutoff. The spike follows the threshold, not round numbers: it vanishes with wrong-year thresholds, appears only at each entity's own band, and is an order of magnitude smaller for procedures with no value cap. Excess value over 2015-2026 is roughly COP 2.9tn (US$0.7bn) at the small-purchase cutoff and COP 2.0tn at the tender cutoff.

## Who bunches

**[empirical]** Territorial governments (elected mayors and governors) bunch more than appointed national agencies at the small-purchase cutoff: b = 37.3 vs 22.3, and 28.2 for national agencies after reweighting for budget band, object and year. At the tender cutoff the reweighted gap is not significant. Regional environmental authorities, which are appointed but territorial, bunch like national agencies (24.3). Bunching is strongest in the smallest budget band (b = 48.7 at 280 SMMLV vs 21.1 at 1000 SMMLV). The contrast is therefore not a clean elected-versus-appointed one, because territorial entities concentrate in the lowest band.

**[empirical, reversal]** This reverses the Italian result the authors cite (Coviello et al. 2026), where appointed administrations manipulate and elected ones do not.

**[model]** The authors' proposed mechanism: governors and mayors cannot be immediately re-elected, so electoral discipline is absent by construction, and donors are repaid with small contracts. The support is thin: the mayor's margin of victory does not predict bunching, and donor linkage is too sparse to test (0.76% vs 0.47%). The accountability mechanism is asserted, not tested.

## What bunching costs

**[empirical, descriptive]** At the tender cutoff, bunched processes draw 3.52 bidders against 6.97 just above, with discounts of 4.6% against 8.7%, and 46.2% end above the avoided threshold after award additions (up to a 50% legal cap). At the small-purchase cutoff the bidder count barely changes, but winners shift to recurrent suppliers (28.7% vs 19.3%) and individuals (24.4% vs 12.8%). Against non-manipulated processes of the same value, the bidder gap at the tender cutoff largely vanishes (-0.20, not significant), so part of the apparent cost is selection into bunching. Selection is acknowledged by the authors; bounds are left to a later version.

## Rule design, displacement and levers

- **Indexation does not help.** Colombia's annually indexed, entity-specific thresholds bunch about 3x more at the lower cutoff than Chile's fixed UTM cutoff, similar at the upper one. The Colombian small-purchase route strips almost every requirement; Chile's equivalent is still a tender. **[wiki synthesis]** What matters is how large the procedural cliff is at the line, not how the line is indexed.
- **Post-award crossing.** The rule is satisfied at award and defeated afterwards through additions: form without function, a pattern in [[isomorphic-mimicry-and-capability-traps]].
- **Displacement to the open door.** The four-month electoral ban on direct contracting pushes activity into small purchases (+18% during the ban) and front-loads direct contracts (+209% in the two weeks before it), with a net effect of -26% that is not significant. The electoral-ban result rests on four treated cycles, via randomisation inference.
- **Reform observations (not tested effects on outcomes).** Raising the small-purchase ceiling (debated in Colombia, done in Chile in 2024) widens the room for manipulation: after the Chilean cutoff was abolished in 2024 there was no bunching (B = -49, not significant), and the Compra Agil ceiling rise cut 30-100 UTM tenders by 82% as they moved to the direct channel. See [[reform-levers]].

## Caveats

**[empirical]** 93% of threshold assignments use the entity's own self-declared threshold; the budget-only subsample is smaller and gives b = 19.0 vs 31.5. Placebos are not exactly zero (a focal-number effect of about a tenth). Standard errors are about five times larger with band-year clustering. The missing mass above the cutoff explains only 31% of the small-purchase excess; the rest is unidentified (splitting is present but small). SECOP II became mandatory for municipalities only in 2022, so earlier territorial coverage is partial and self-selected. Public sector only; no output, quality or delivery measure, so no claim about production. No organisational age or size variable beyond budget band, so nothing citable on age-decay. The summarising pass read about 470 of 560 source lines; the remainder is appendix and robustness material.

**Ideological priors.** No stated camp; a mainstream public-economics framing with a mild reading that discretion at the margin is costly.

## Source

- `raw/research/weekly-2026-10-27/01-colombia-procurement-threshold-manipulation.md` (arXiv 2610.28965, Espinal Maya and Jimenez Londono, "Discretion at the Margin: Threshold Manipulation and Electoral Bans in Colombian Public Procurement").

## Related

- [[dimensions-of-institutional-variation]] — rules vs discretion, elected vs appointed buyers and threshold design as candidate dimensions; a large-N instance of bright-line gaming.
- [[critiques-of-governance-indicators]] — bright-line thresholds invite gaming there too.
- [[red-tape]] — thresholds as the burden/discretion trade-off.
- [[personnel-economics-of-the-state]] — rules vs discretion with an unstable sign.
- [[state-capacity-and-level-of-government]] — territorial buyers worse at the small-purchase margin.
- [[regulator-career-incentives-and-revolving-doors]] — another un-refereed bunching study of a state actor.
- [[state-demand-and-preferential-allocation-in-hungarian-construction]] — procurement favouring connected suppliers.
- [[isomorphic-mimicry-and-capability-traps]] — form without function after award.
- [[reform-levers]] — threshold-raising and ban-displacement observations.
- [[regulatory-capture]] — donor-repayment channel, asserted.
