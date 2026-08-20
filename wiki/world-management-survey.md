# World Management Survey

The World Management Survey is a **double-blind interview instrument scoring 18 specific management practices from 1 to 5**, run by Bloom, Sadun & Van Reenen across **11,383 firms in 34 countries** (15,489 interviews, five waves 2004–2014, manufacturing, 50–5,000 employees). It is the second of two instruments in this batch that measure an **individual organisation** rather than a country, and it is the more portable of the two: it needs no documents, no public listing and no market data, only a trained interviewer and one honestly answering, correctly placed respondent. Two numbers carry most of its weight for this wiki. **Management explains roughly 30% of the cross-country TFP gap with the US** — ranging from ~6% (Zambia) to ~52–55% (France, UK). And, more importantly, **77% of the variation in management scores lies *within* country-and-industry**: only 13% is explained by the country a firm is located in and a further 10% by its 3-digit industry. That second figure is a direct, quantified statement that the right unit of analysis for at least one measurable dimension of institutional quality is **the individual organisation, not the nation** — which is why it is recorded prominently at [[open-questions]] Q90 rather than only here. The paper's own causal warrant is imported, not produced: its firm-level regressions are explicitly flagged as non-causal, and the causal evidence is cited from three external studies.

**Evidence tier note.** **(a) empirical** — a large original survey plus a structural model (the "Management as a Technology" model, estimated by Simulated Method of Moments), supplemented by MOPS, a closed-question US Census-linked survey used for age and productivity robustness. **Strongest**: the re-rater reliability check (a second interviewer scoring a second plant manager at the same firm, blind to the first — correlation **0.51, p = 0.001, n = 222**) and the robustness table (9 alternative specifications, correlation with baseline ≥ 0.85 in all but one). **Weakest**: the rejection of the rival "Management as Design" (contingency) view, which is run against "an extremely stylized version" of the Design model with one hand-picked functional form, and which the authors say is "certainly not meant to represent the wide range of Design approaches." **The causal claim is not this paper's.** Table 3's firm-level regressions are "conditional correlations... but are obviously not to be taken as causal"; the causal support is by citation to an RCT in Indian textile firms (Bloom et al. 2013: 1 SD of management → **10% TFP**), an RCT in Mexican SMEs (Bruhn, Karlan & Schoar 2016), and a Marshall Plan management-assistance natural experiment (Giorcelli 2016). **(c) wiki synthesis** is marked inline.

## The instrument

**[empirical]** **18 practices, each scored 1 ("worst practice") to 5 ("best practice")** against a written grid with worked examples anchored at 1, 3 and 5 (2 and 4 allowed, not separately anchored). The 18, verbatim by title:

1. Modern manufacturing, introduction — 2. Modern manufacturing, rationale — 3. Process problem documentation — 4. Performance tracking — 5. Performance review — 6. Performance dialogue — 7. Consequence management — 8. Target balance — 9. Target interconnection — 10. Target time horizon — 11. Targets are stretching — 12. Performance clarity — 13. Managing human capital — 14. Rewarding high-performance — 15. Removing poor performers — 16. Promoting high performers — 17. Attracting human capital — 18. Retaining human capital.

**Grouping**, at two granularities the source itself gives. Main text: three areas — **monitoring** (tracking internal operations and using the data for continuous improvement), **target setting** (whether targets are right, tracked and acted on), **incentives / people management** (whether promotion and reward are performance-based, and whether talent is systematically hired and retained). Appendix, more precisely: four sub-groups — operations (3), monitoring (5), targets (5), incentives (5). A later contrast (§4.5) collapses to two indices: **people management** (items 13–18) against **monitoring & targets** (items 1–12).

**Aggregation**: each item is z-scored, the 18 z-scores averaged per firm, and the firm average z-scored again — so results are reported in standard deviations of management. Principal-component aggregation gives "broadly similar" results.

## The double-blind protocol

**[empirical]** This is the paper's real methodological innovation, and it has two independent halves:

- **The respondent is blind**: told only that this is "an interview about management practices for a piece of work," never told they are being scored, never shown the grid.
- **The interviewer is blind**: given only company name, phone number and industry — no performance data. Because sampled firms are medium-sized and rarely covered by the business press, interviewers "should have few preconceptions." **The authors assert this and do not test it**, and it would plausibly fail for large, famous organisations.

Scoring is elicited through **open questions with follow-up probing** rather than closed items — "tell me how you monitor your production process," "what kinds of measures would you use to track performance?", "if I walked around your factory, could I tell how each person was performing?" — continuing "until the interviewer can make an accurate assessment." Respondents are **production or plant managers**, chosen deliberately as "senior enough to have an overview of management practices but not so senior as to be detached from day-to-day operations." No financial or performance data is ever requested from the interviewee; all of it comes from independent company accounts. Interviewers are trained students with business experience.

**Noise controls.** Time of day, day of week, interviewee seniority and tenure, interviewer identity, interview duration and an interviewer-coded reliability flag are all collected and entered as regression covariates to strip measurement noise — an unusually explicit treatment of the interview *process* as a source of error.

**Cost and response.** Roughly **2 completed interviews per day per interviewer at ~45 minutes each**, with the remaining ~6 hours spent on scheduling and repeated contact attempts. **41% response rate**, essentially uncorrelated with independently measured labour productivity (0.008, n.s.) and ROCE (−0.013, n.s.), but **significantly rising with firm size** (≈0.06–0.07 on log employment, significant at 1% in every specification) — corrected with an inverse-probability weight from a first-stage selection probit. That correction is material: dropping it moves the average TFP-share-explained from ~30% down to ~20%.

## The 77% finding

**[empirical]** Of total firm-level variation in management scores: **13% is explained by the country the firm is in, a further 10% by 3-digit industry, and 77% remains within country-and-industry** — i.e. between individual organisations facing the same national environment and the same sector.

**[wiki synthesis] Why this matters more than the headline TFP number.** This wiki has now recorded, across several batches, that its evidence for institutional claims is almost entirely country-level scalars while its register and its framework operate at institution level — most sharply at [[open-questions]] Q90, which puts the problem as a fork: either nobody has run the disaggregation (a property of the *literature*), or institutional environments are irreducibly national (a property of the *object*). Bloom et al. supply the complement to that finding: on an instrument that scores organisations directly, **most of the variation is not national**. A country with one first-rate plant and one badly run one does not have a management level; it has a distribution, and the distribution's spread dominates its mean.

That is direct evidence for the first limb of the fork on at least one measurable dimension. It does not settle Q90 — management practice is not the same object as the legal and coercive order that the "property of the object" limb is about, and this paper aggregates upward only for its TFP section. But it establishes that the country-level-only pattern in the wiki's other evidence is **not forced by the nature of institutions**, because here is an instrument that does the disaggregation and finds the action below the national level.

**A tension worth keeping visible.** [[organizational-economics-of-the-state]] carries the "Weberian Facts": **country fixed effects explain 73%** of variation in bureaucratic structure. Here country explains 13%. Opposite-signed messages about how much of institutional quality is national — on different instruments, in different sectors, measuring different objects (bureaucratic structure against management practice), and neither designed to test the other. Do not average them; note that the answer depends on what is being scored, and that no one has run both on the same organisations.

The paper also decomposes the country score itself into an unweighted firm-average term and an Olley-Pakes size covariance ("reallocation") term: of the average management gap with the US, **~70% is differences in the average level and ~30% is differences in reallocation** — how strongly better management is rewarded with market share.

## What it predicts

**[empirical]** Firm level, per 1 SD of management z-score (Table 3):

| Outcome | Effect |
|---|---|
| Sales, labour controlled only | +35.6 log points (≈43% higher labour productivity) |
| Sales, capital and full controls | +15.9 log points |
| Sales, full **firm fixed effects** | +3.5 log points, still significant — the authors call this "a very tough test given the likelihood of attenuation bias" |
| Productivity (Olley-Pakes) | +23.1 log points |
| Employment | +40.2 log points (≈49%) |
| ROCE | +1.005 pp |
| 5-year sales growth | +4.3% |
| ln(Tobin's Q), listed firms only | +0.030 |
| Probability of death/bankruptcy | **−9.0 pp** (probit marginal effect) |

Country level: **≈30% of the cross-country TFP gap with the US**, from ~6% (Zambia) to ~52–55% (France, UK) — higher in richer and OECD countries, lower in low-income ones, where the authors note "these countries have much greater problems than just management quality." Within-country: management accounts for ~30–38% of the 90th/10th-percentile TFP spread in the US and UK.

## Age, scale and competition

**[empirical]** Unusually for this wiki's sources, there is a real age finding:

- **Management level rises and dispersion falls with plant age** (confirmed in MOPS, strongest for plants ≤5 years old against older). The mechanism offered is **selection**: badly managed young establishments either improve or exit, shrinking the left tail. This is survivor composition, not within-plant improvement, and should not be read as an institution getting better as it ages.
- **Structural estimates**: management **depreciation rate δM = 13.3% (SE 5.5%)**, similar to the 10% calibrated for physical capital; **adjustment cost γM = 0.207 (SE 6.5%)** against capital's γK = 0.189, so management is somewhat *harder* to change than physical capital — rising to 0.290 (≈50% above capital) if given the same resale-loss friction. The authors read this as consistent with organisational-resistance accounts and cite Cyert & March (1963).
- Loose corroboration, the authors' own and not a formal test: average plant-manager tenure is **6.4 years in post, 13.0 at the company**, implying rough quit rates of 15% and 7% that bracket the estimated depreciation.
- **Scale**: 1 SD of management is associated with **268 extra employees in the US but only 68 in southern Europe** — a much weaker size–management covariance, pointing at competition and market frictions in how strongly good management is rewarded with market share.
- **Competition**: tougher competition (lower Lerner margins, higher import penetration) raises both average management and the size–management covariance.

**[wiki synthesis]** The δM = 13.3% estimate is the closest thing this wiki holds to a *measured decay rate for an organisational capability*. It is model-derived rather than directly observed, it is about management practice rather than about an institution's overall function, and it points the opposite way from Chandler's claim at [[organizational-capabilities-and-the-m-form]] that capability outlives its personnel — depreciation at 13% a year means it does not, absent continuous reinvestment. Two sources, opposite signs, different objects and no shared measurement; recorded, not filed.

## What it does not measure

**[empirical]** Load-bearing for how the wiki uses this instrument.

- **None of the 18 items is a decentralisation or authority-allocation item.** Confirmed by direct search of the source: "decentralized" appears once, in a footnote citing *other* papers. **This instrument measures how well monitoring, targets and incentives are executed — not who decides.** It supplies no measurement whatever for the decision-rights axes at [[formal-and-real-authority]] or [[decision-rights-and-authority-theory-of-the-firm]]. (A later WMS wave reportedly fields decentralisation questions in other papers; that instrument is not documented here and must not be attributed to this source.)
- **No public/private comparison is run.** The frame is 90% private, 10% publicly listed firms, manufacturing only. The paper cites Chong, La Porta, Lopez-de-Silanes & Shleifer (2014) as showing the manufacturing score correlates with separately collected scores in retail, healthcare, schools and **government services** — but that is **an appeal to an unread external paper, not evidence in this source.** The one ownership comparison actually made is domestic against **multinational-subsidiary** firms: foreign subsidiaries score higher in almost every country, robust to size, age and industry.
- **The rubric encodes a particular conception of good management** — just-in-time, autonomation, flexible manpower, formalised target cascades, individualised performance-based promotion, reward and dismissal. The instrument "was first developed by an international consulting firm" (identified in the acknowledgements as McKinsey; the authors disclose the partnership and disclaim McKinsey funding for the tool). **[wiki synthesis]** Nothing in the source interrogates whether this rubric penalises non-Western or relational management styles. The authors' own defence is indirect: an F-test on management×country interaction dummies fails to reject equal coefficients across countries (p = 0.642), which they read as evidence the measure is not simply picking up Anglo-Saxon bias. That is a test of predictive equivalence, not of rubric neutrality.
- **Selection into the sample is size-related** (corrected, not eliminated), and the performance regressions **omit privately held firms in the US, Canada and India specifically**, because private firms there do not publish detailed accounts.
- **No institutional-pathology content** — no capture, ossification or goal displacement. The nearest analogue is competitive exit of the badly managed.

## Portability: scoreable tomorrow, with a different failure mode

**[empirical, with the extension marked]** What a lone analyst needs to score one organisation:

1. A **trained interviewer** who has internalised the 18-item grid and its 1/3/5 anchors — the source's own interviewers were students with business-context training, not specialists.
2. **One live respondent in the right role** — senior enough to see across functions, close enough to still see day-to-day operations.
3. **~45 minutes of interview**, though effective cost is far higher once scheduling is counted.
4. Discipline to run the **double-blind protocol** and to probe with open questions rather than closed items.

**Not needed**: public listing, charter or bylaws, market data, or any public record of the organisation at all. Performance data was used only for external validation and is not a scoring input.

**[wiki synthesis] The contrast with a document-based instrument is the useful part.** [[corporate-governance-index-and-firm-control-rights]] trades on documents existing and being accurate; this trades on a respondent being reachable and honest. That flips the generalisability profile. It works identically on a **private firm with no disclosures** — most of the 11,383 are private — and, untested, in principle on a **public bureau**, since nothing in the design requires a shareholder or a market. But its validity now rests on respondent honesty, availability and role-fit, and on interviewer skill and consistency (r = 0.51 between independent interviewers, not perfect). A charter-based instrument fails when no document exists, or when the document is **decoupled** from actual practice — the failure mode at [[institutional-myths-and-decoupling]]. This one fails when no honest, correctly placed respondent can be reached, or when the interviewer cannot get past scripted answers. **Different failure modes, neither strictly better.** Registered as [[dimensions-of-institutional-variation]] **D111**, `promoted`, gated by D90.

## Source

- `raw/research/theory-of-the-firm/08-bloom-sadun-vanreenen-management-technology.md` — Nicholas Bloom, Raffaella Sadun & John Van Reenen, "Management as a Technology?", NBER Working Paper 22327, revised 2016. https://www.nber.org/system/files/working_papers/w22327/revisions/w22327.rev0.pdf

## Related

- [[dimensions-of-institutional-variation]] — supplies **D111** (management-practice quality), the register's first live-respondent institution-level axis, gated by D90.
- [[corporate-governance-index-and-firm-control-rights]] — the batch's other institution-level instrument, with the opposite portability profile and the opposite failure mode.
- [[open-questions]] — **Q90**, where the 77% finding is recorded as evidence on the fork between a literature problem and a property of the object; also Q115.
- [[organizational-economics-of-the-state]] — the 73% country-fixed-effects "Weberian Fact", pointing the opposite way on a different instrument and a different object.
- [[institutional-myths-and-decoupling]] — the failure mode a document-based instrument has and this one does not; and the failure mode this one has instead.
- [[weberian-structure-and-growth]] — the wiki's other structured-scoring instrument for institutional quality, but scored at country level by 126 outside experts rather than by interviewing insiders.
- [[multitask-incentive-theory]] — the "consequence management", "rewarding high-performance" and "removing poor performers" items are concrete scorable proxies for constructs that page treats formally.
- [[personnel-economics-of-the-state]] — the public-sector counterpart tradition, with randomised designs and a different measurement mode.
- [[organizational-capabilities-and-the-m-form]] — Chandler's capability-outlives-personnel claim against this source's 13.3% annual depreciation estimate.
- [[knowledge-hierarchies-and-the-cost-of-scale]] — both give scale- and age-dependent predictions about internal organisation, from different mechanisms.
- [[governance-structures]] — this source's structural model is framed explicitly against the "Design"/contingency camp that Williamson's cost-economising presumption exemplifies; the authors' own honest conclusion is a hybrid.
