# The Slave Trade and the Origins of Mistrust

Nunn & Wantchekon show individuals whose ancestral ethnic group was more heavily raided during Africa's slave trades (1400–1900) report **lower trust today** — in relatives, neighbours, and local government — than individuals from less-exposed groups, using 2005 Afrobarometer data (17 countries, ~21,700 respondents) matched to ethnicity-level historical slave-export estimates. This is a historical shock, centuries old, still legible in present-day informal-institution quality — a rare case where the persistence claim is quantified and decomposed rather than merely asserted.

**Evidence tier note.** **[empirical]** — individual-level OLS with ethnicity clustering (185 clusters) and country fixed effects, plus 2SLS using historic distance-from-coast as an instrument, plus falsification tests on non-African samples.

## Magnitude and channel decomposition

**[empirical]** Trust in relatives −.131, neighbours −.156, local council −.109 (all significant); IV estimates similar or larger. The paper explicitly decomposes an **internal (cultural transmission)** channel from an **external (institutional legacy)** channel using a mover/non-mover design: comparing ethnicity-based slave-exposure (tracks the individual regardless of where they now live) against location-based exposure (tracks the place, for the 45% of respondents living away from their ancestors' historic territory) — the ethnicity-based coefficient is "always at least twice the magnitude" of the location-based one, yielding the paper's headline estimate that **the internal/cultural channel accounts for about 75% of the total effect.**

**[empirical]** The authors are explicit about what this design can and cannot separate: **"Our analysis is not able to distinguish between these different transmission mechanisms and different explanations for the persistent impact of slave trade on a culture of mistrust."** It separates *individual-carried* from *place-carried* effects, which is a proxy for cultural-vs-institutional, not a direct test — genetic selection (differential emigration of more-trusting individuals during the trade) is considered and not ruled out, though cited twin studies put trust's heritability at only 10–20%.

## Identification

**[empirical]** Reverse causation and omitted variables are addressed three ways: 2SLS with historic coastal distance as an instrument (controlling for *current* coastal distance to block an income-via-proximity confound); falsification on non-African samples (Asiabarometer, World Values Survey), where the coast-trust relationship is null; and a within-Africa placebo showing the coast-trust relationship appears only in slave-trade-exposed regions.

## Relevance to the institutional-legacy channel

**[wiki synthesis]** Half of the effect on trust in local council specifically runs through perceived council quality/corruption — a directly institutional channel, not purely normative — which the authors read as evidence that a historical shock to norms *and* a historical degradation of local institutions can both persist and compound, rather than one being reducible to the other. This is a genuinely joint norms-and-institutions persistence result, useful ballast against reading any single source in this job as settling norms-first or institutions-first cleanly.

## Source

- `raw/research/schooling-norms-and-institutional-formation/04-nunn-wantchekon-slave-trade-mistrust.md` — Nathan Nunn & Leonard Wantchekon, "The Slave Trade and the Origins of Mistrust in Africa," NBER Working Paper 14783, 2009 (*American Economic Review* 101(7), 2011).

## Related

- [[determinants-of-trust]] — Alesina & La Ferrara's contemporary community-level trust determinants; this paper is the historical-persistence analogue.
- [[economics-of-cultural-transmission]] — Bisin & Verdier's formal vertical-transmission model is the mechanism this paper's "internal channel" implicitly invokes without formally testing.
- [[maghribi-traders-reputation-mechanism]] — the opposite historical case: a shock (trade opportunity, not violence) that built durable trust-based cooperation rather than eroding it.
- [[colonial-rule-and-trust-in-traditional-leaders]] — the paper's coercion-stigma channel is explicitly modelled on this page's transmission mechanism ("in the same way that Nunn and Wantchekon (2011) show slave-trade-era insecurity became a durable norm of mistrust").
