# The Measurement-Validity Framework (Munck & Verkuilen)

**This is the anchor page of the `measuring-institutions` batch, and it is the only artifact in that batch that transfers to this wiki intact.** Munck & Verkuilen decompose the construction of any social-science index into **three sequential, independently-gradable stages** — **conceptualisation** (what attributes does the concept have, and are they the right ones), **measurement** (what indicators tap those attributes, and how good are they), **aggregation** (how are indicator scores combined into a score, and does the combining rule express a theory) — each with its own tasks and its own standards of assessment. They then grade nine country-level democracy indices against it and find that even the best fail at least one stage and the worst fail all three. **Every substantive claim in the source is country-level and none of it transfers. The diagnostic itself is level-agnostic**: it is drawn from general measurement theory (Bollen's latent-variable methodology, Kaplan on concept formation, Guttman on scaling), nothing in the abstract statement of the three stages requires the object being measured to be a country, and it can be run unchanged against a register row, an institution-level instrument, or an institution's own internal scorecard. That is why it anchors this batch: the batch's data is inadmissible here and this method is not.

**Evidence tier note.** **(b) model** — a methodological and conceptual paper, not an empirical study. Its "evidence" is (1) a taxonomy assembled from prior methodology literature and (2) a systematic comparative content-analysis of nine indices' stated definitions, indicator lists, coding manuals and aggregation formulas, scored against that taxonomy. One genuinely quantitative exercise: a nonlinear principal-components decomposition of six index series 1973–1990, used to show that pairwise correlations mask a real second dimension on which Freedom House diverges from the others (69%/26% variance split). **Strongest**: the index-by-index audit is exhaustive, transparent about its criteria, and checked against each index's own published documentation. **Weakest, and the authors say so**: the standards of assessment are avowedly not rule-governed — "there is no hard and fast rule" for what attributes a concept must include, and quoting Guttman, "there is no point in arguing about what a 'correct' definition is" — so the grading rests on expert judgment, not a mechanical procedure. **(c) wiki synthesis** is marked inline, and the level-transfer argument above is wiki synthesis, not a claim the authors make.

## The three stages

**[model]**

| Stage | The task | What a failure looks like |
|---|---|---|
| **Conceptualisation** | Identify the concept's attributes and arrange them in an explicit tree by level of abstraction | Maximalism, minimalism, redundancy, conflation |
| **Measurement** | Select indicators for each leaf attribute; establish their validity, reliability and replicability; choose a measurement level | Single non-cross-checked indicators, unrecognised source bias, unjustified scale level, unpublished coding rules |
| **Aggregation** | Combine indicator scores upward, at a justified level, by a rule that expresses a theory of how the components relate | Collapsing to one scalar without a dimensionality test; an additive/multiplicative/weighted rule chosen by default and never stress-tested |

The stages are **sequential and independently gradable** — this is the framework's real contribution. An index can have an excellent concept and a worthless aggregation rule, and lumping the two into "it's a bad index" loses the information about which repair is needed.

## The twelve named failure modes

**[model]** Preserved precisely, because this is the checklist:

**Conceptualisation**
1. **Maximalist definition** — including theoretically irrelevant or overburdening attributes. Freedom House smuggling socioeconomic rights, "freedom from gross socioeconomic inequalities" and property rights into a democracy concept.
2. **Minimalist definition** — omitting a theoretically relevant attribute. Far more widespread than maximalism among the nine indices; most omit participation, or "offices" (are positions actually filled by election), or agenda-setting power of elected officials.
3. **Conceptual redundancy** — two same-level attributes that tap one underlying aspect, so it is counted twice under two labels. Polity IV's competitiveness/regulation-of-participation pair, and its competitiveness/openness-of-executive-recruitment pair.
4. **Conceptual conflation** — a lower-level attribute filed under the wrong higher-level branch, bundling it with manifestations of a different concept. Arat filing "offices" and "agenda-setting" under participation; Freedom House's 9- and 13-item checklists assembled with "little thought about the relationship among components".

**Measurement**

5. **Single-indicator / non-cross-checked measurement** — failure to use multiple indicators and establish their cross-system equivalence.
6. **Unrecognised measurement error and source bias** — treating an indicator as a neutral record when the record-generating process has its own drivers. Their examples are exact and travel well: reported rape rates track cultural willingness to report, not incidence; reported corruption tracks press freedom, not corruption.
7. **False objective/subjective dichotomy** — Vanhanen's claim to use only "simple, objective, quantitative indicators" (vote share, turnout) "overstated the contrast between subjective and objective indicators" and ignored the subjective judgment embedded in choosing which objective proxy to use.
8. **Unjustified measurement-level choice** — nominal, ordinal or interval picked by assertion rather than by theory plus testing. Bollen declaring democracy continuous as self-evident; ACLP calling that "ludicrous"; neither arguing from evidence.
9. **Non-replicability** — no published coding rules, sourcing detail, coder identity or count, intercoder-reliability test, or disaggregate data. Freedom House and Gasiorowski worst; **only two of nine indices ran and reported intercoder reliability tests at all**.
10. **Reliability mistaken for validity** — high inter-index correlation or high intercoder agreement read as evidence of validity when it is at most evidence of reliability. Shared bias produces both without validity. Compounded empirically: most of the nine indices draw on the *same underlying coded source data* (Arthur Banks), so cross-index correlation partly reflects shared source contamination rather than independent confirmation.

**Aggregation**

11. **Unjustified aggregation to the highest possible level** — collapsing a multidimensional concept into one scalar to enable off-the-shelf regression, without testing whether the attributes are unidimensional. Their own PCA finds a real second dimension separating Freedom House from ACLP/Gasiorowski/Polity IV — direct evidence the collapse throws away real structure in at least one case.
12. **Unjustified or untested aggregation rule** — additive, multiplicative or weighted chosen with no explicit theory of how the attributes relate (necessary? sufficient? substitutable? complementary?) and essentially never stress-tested against an alternative. Freedom House (unweighted addition over an unstructured checklist), Vanhanen (unweighted multiplication, no justification for equal weights), Polity IV (weighted addition, weights unjustified, plus double-counting from unresolved redundancy). **Hadenius is the sole exception praised for justifying, formalising *and* testing the robustness of his rule.**

## The design requirements, restated as things to do

**[model]** The authors are prescriptive about method. Every one of these is one on which some existing index does well and another badly, so each is demonstrably achievable rather than aspirational:

(a) state the concept's attributes and their level-of-abstraction tree explicitly, avoiding maximalism and minimalism; (b) select indicators for validity — multiple, cross-system-equivalent, error-minimising, cross-checkable — and report reliability tests; (c) justify the measurement-level choice against data availability and test its implications rather than asserting it; (d) publish coding rules, sourcing detail, coder count and identity, and intercoder-reliability results; (e) publish disaggregate component-level data, not just the final index; (f) justify the level of aggregation against a dimensionality test, not just parsimony; (g) make the aggregation rule the formal expression of an explicit theory of how the components relate, and test its robustness against alternative rules.

## The complication this puts on D90

**[model]** The paper directly attacks the objective/subjective dichotomy as overstated — failure mode 7 above — and the argument is not a quibble. Choosing an "objective" quantitative proxy still embeds a subjective judgment about what to measure and how to operationalise it, and the proxy can still be a poor, biased stand-in. Their position: **the objective/subjective split is not the operative validity distinction; source bias and construct validity are.** A document-based indicator is not automatically immune, because what drives an institution to *write down* a rule, as against following it, is itself a reporting-type confound of exactly the kind failure mode 6 describes.

**[wiki synthesis]** This cuts against a naive reading of [[dimensions-of-institutional-variation]] **D90** and has been recorded on that row. D90 as written treats durable-rule/document-based measurement as the sound side and outcome/perception measurement as the suspect side, and D110's document-scored instrument is gated only on D90(iii) partly for that reason. Munck & Verkuilen would say both sides need the same interrogation. The wiki already holds the mechanism that makes their point concrete: [[institutional-myths-and-decoupling]] is precisely an account of formal structure adopted as ceremony — a rule written down *because* writing it down buys legitimacy, which is a visibility-driven record-generating process, not a measurement of practice. **D90's three limbs stay as they are; what changes is that limb (iii) is no longer a check on the perception measure alone, it is a check on both measures against each other, with neither privileged as the criterion.**

## Running the framework on this wiki's own instruments

**[wiki synthesis]** The framework is worth what it catches, so here is what it catches on the four instruments this wiki holds. None of this is in the source.

- **[[world-management-survey]] (D111).** Conceptualisation: the 18-item rubric encodes a specific lean-manufacturing conception of good management, developed with a consultancy — a **maximalism/conceptualisation** question the authors' own defence (an F-test on predictive equivalence across countries, p = 0.642) does not address, because that tests prediction, not concept. Measurement: strong — published grid, disclosed coder training, an actual reported re-rater reliability test (r = 0.51), and process-noise covariates. Aggregation: z-score each item, average, z-score again — an **unweighted additive rule with no stated theory of how the 18 relate**, which is failure mode 12 exactly, though the authors do report that principal-component aggregation gives "broadly similar" results, which is a partial robustness test.
- **[[corporate-governance-index-and-firm-control-rights]] (D110).** Conceptualisation: eight named mechanism families, explicitly enumerated — the best-specified concept tree in the wiki. Measurement: document-coded, replicable, with a worked template; the authors disclose that coding is "a noisy measure" and that some provisions were inferred. Aggregation: **24 items, one point each, no strength gradation, no weighting theory** — the authors say so, and it is failure mode 12 again.
- **[[weberian-structure-and-growth]].** The ten-item Weberianness Scale is a textbook **conceptualisation-stage failure** in these terms: a minimalist definition driven by measurability rather than theory, whose authors state in a footnote that they deliberately excluded rule-governed jurisdiction because it is "a double-edged sword… producing rigidity and organizational sclerosis." Excluding an attribute of the concept because you dislike its consequences is failure mode 2 with a stated motive.
- **[[governance-indicators-and-their-construction]].** Conceptualisation: six categories with, in the authors' own framing, a typology rather than a theory connecting them — and Arndt & Oman put it harder, that the concept "does not emerge from, or imply, a theory of governance". Measurement: perception-exclusive by written policy; reliability handled well, validity unaddressed. Aggregation: the one stage WGI does better than anyone, with a derived rule and a propagated interval — though its own equal-weighting check shows the rule barely matters.

**The pattern is worth stating.** Across four instruments, **the measurement stage is where this wiki's sources are strongest and the aggregation stage is where they are weakest** — every one of them combines components additively with equal weights and no theory of how the components relate, and only WGI tests robustness to an alternative rule. That is a finding about the field's instruments and it is the reason D120 is registered.

## What the authors disclaim

**[model]** Recorded because a checklist that overclaims is worse than none:

- Conceptualisation has **no algorithmic answer**. The framework rules out the two extremes; it does not adjudicate between reasonable alternative conceptualisations.
- The standards for measurement-level selection are similarly open-ended, and the authors call them "the more open-ended suggestion" rather than a decision rule.
- Their own PCA is illustrative, not dispositive — it shows correlation tests can mask multidimensionality, not what the true dimensionality is.
- Their own grading reflects expert judgment applied to their own criteria, consistent with their claim that conceptualisation is "an open, evolving activity".
- **They explicitly refuse a moratorium**: "having a data set on democracy, even if it is partially flawed, is better than not having any data set at all." The framework is for repair, not abolition.
- Their preference for a procedural, Dahl-style conception of democracy over a maximalist rights-and-outcomes one is itself a conceptual-camp choice argued on methodological grounds, not a neutral audit position.

Their closing line is the one to keep: "one cannot slight the task of measurement hoping that mathematical statistics will somehow offer a solution to a problem it is not designed to tackle."

## Source

- `raw/research/measuring-institutions/05-crit-munck-verkuilen-democracy-indices.md` — Gerardo L. Munck & Jay Verkuilen, "Conceptualizing and Measuring Democracy: Evaluating Alternative Indices", *Comparative Political Studies* 35(1), 2002, 5–34. https://www.almendron.com/tribuna/wp-content/uploads/2017/11/conceptualizing-and-measuring-democracy-evaluating-alternative-indices.pdf

## Related

- [[critiques-of-governance-indicators]] — Arndt & Oman, kept as a **separate page rather than merged**, and that page states the reason: this framework grades an index's *construction* and is level-agnostic; theirs catalogues an index's *consumption* by investors, donors and academics and does not descend below the nation-state. The two taxonomies overlap on three items and diverge on the rest; the mapping is on that page.
- [[dimensions-of-institutional-variation]] — **D120**, the measurement-construction audit this framework generates, aimed at an institution's own internal KPI system; and **D90**, which carries the objective/subjective complication above.
- [[governance-indicators-and-their-construction]] — the instrument this framework's aggregation stage rates highest and its conceptualisation stage rates lowest.
- [[v-dem-measurement-model]] — the instrument that best satisfies the measurement-stage requirements: published rules, disclosed coder counts, reliability apparatus, disaggregate output, and an aggregation rule that is the formal expression of a stated theory.
- [[world-management-survey]] and [[corporate-governance-index-and-firm-control-rights]] — the wiki's two institution-level instruments, run through the checklist above.
- [[weberian-structure-and-growth]] — the wiki's clearest conceptualisation-stage failure, with the exclusion stated in the source's own footnote.
- [[institutional-myths-and-decoupling]] — the mechanism that makes failure mode 6 bite on document-based measurement: a rule written down because writing it down buys legitimacy.
- [[does-institutions-growth-survive-identification]] — this framework supplies the vocabulary for locating *where* a contested index fails, which that conflict currently states only as "the indices do not measure institutions".
- [[open-questions]] — **Q120**, the audit question this page generates, and **Q90**.
