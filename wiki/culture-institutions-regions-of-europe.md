# Culture and Institutions: Regions of Europe

Tabellini tests the culture/institutions/development triad **within** countries rather than across them — 69 European sub-national regions, 8 countries — using regional literacy circa 1880 and regional political-institution history (1600–1850, coded on a Polity-style constraints-on-the-executive scale) as instruments for present-day culture (trust, respect for others, sense of individual control, versus obedience, from World Values/Eurobarometer surveys). Culture instrumented this way predicts regional output: the ~50-point culture gap between Lombardy and Southern Italy implies a predicted output gap of roughly one-third of the EU15 average, "almost half of the observed income difference."

**Evidence tier note.** **[empirical]** — 2SLS with country fixed effects, first-stage F≈13 (≈9 in the growth specification), Sargan overidentification tests that do not reject in main specifications — though the paper's own bootstrap/Monte Carlo power analysis shows those tests have real limits (~60–70% power to detect one invalid instrument, near-zero power if both are invalid).

## The methodological advance: country fixed effects remove the confound cross-country designs cannot

**[empirical]** "Separating the effect of culture from that of institutions is more credibly done in the sample of European regions, where one can control for common political and economic institutions at the national level, and where unobserved heterogeneity is less problematic." Formal national/legal institutions have been identical within each country for 150+ years; regional variation in *historical* political institutions and literacy still varies. **[wiki synthesis]** This is a genuine advance on the level-of-analysis problem this wiki's register has flagged repeatedly (D90 and its neighbours) — a design that isolates historical-culture variation net of contemporaneous national institutional differences, something no cross-country study in this wiki (AJR, Rodrik, Glaeser et al.) attempts.

## The sequencing question, stated as an open assumption by the author himself

**[empirical]** Tabellini does not claim to have settled schooling/culture/institution sequencing — he states the threat to his own design directly: **"A special case of a violation of our assumptions... would occur if the true model was one in which history influences output, which in turn affects culture, with no direct effect of the historical variables on culture"** — exactly the reverse of his postulated chain (history → culture → output). His own mitigation is thin by his own admission: a 13-observation test using Italy's 1946 anti-monarchy referendum as an early proxy for culture, which "cannot dispel all doubts." **[wiki synthesis]** This is important for [[schooling-and-institutional-quality]]'s Q94: Tabellini supplies a genuinely independent, sub-national design supporting a culture/human-capital-upstream reading — but explicitly, in his own words, does not close the sequencing question any more definitively than Glaeser et al.'s Table 12 does.

## Cross-country validation, using AJR's own instrument

**[empirical]** A separate ~50-country cross-country check instruments culture with % Protestant (1980) or, notably, **log settler mortality — AJR's own instrument** — and finds culture predicts both output per worker and Hall-Jones's property-rights index strongly: "variation in culture between Sweden and Uganda can explain over two thirds of the difference in output per worker, and almost all of the difference in institutional outcomes." **[wiki synthesis]** This is the same instrument the AJR camp uses to argue institutions are fundamental, here loading on *culture* instead — directly analogous to [[schooling-and-institutional-quality]]'s Table 11 finding that settler mortality loads more on schooling than institutions, from an independent author using an independent culture measure.

## Neither culture nor institutions crowned primary

**[model]** Tabellini's own conclusion refuses the framing this whole debate keeps reaching for: **"There is no primacy of formal institutions over culture. On the contrary, both are likely to interact and to shape the actual functioning of real world institutions."**

## Source

- `raw/research/schooling-norms-and-institutional-formation/05-tabellini-culture-institutions-regions-europe.md` — Guido Tabellini, "Culture and Institutions: Economic Development in the Regions of Europe," IGIER Working Paper 292, 2005 (*Journal of the European Economic Association*, 2010).

## Related

- [[schooling-and-institutional-quality]] — Q94's governing debate; Tabellini's sub-national design answers one of that page's own "what would strengthen or kill it" requests, without resolving the underlying sequencing question.
- [[institutions-human-capital-development]] — a cross-country instrument-based rebuttal of the same broad thesis, from the opposite camp.
- [[dimensions-of-institutional-variation]] — bears on D90's level-of-analysis problem as a genuine sub-national design.
