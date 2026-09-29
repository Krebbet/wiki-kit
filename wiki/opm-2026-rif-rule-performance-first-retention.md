# OPM 2026 Final RIF Rule: Performance-First Retention

The US Office of Personnel Management's final regulations on reduction in force (5 CFR part 351; 91 FR 49178, 3 Aug 2026, corrected 91 FR 54794), announced in a 2026-09-02 memo to agency heads, replace seniority-first release ordering with a performance-first register and collapse bump-and-retreat into a single assignment right. This page records the rule's design mechanism only. It is a case of a large-scale move from a seniority-weighted to a performance-weighted personnel rule, with no outcome evidence yet.

**Evidence tier note.** The source is a primary regulatory document, but only the agency's memo plus its "RIF Basics" and eight FAQ attachments; it is not the rule text or the Federal Register preamble, and the attachments state that the rule, the CFR and statute control. It contains no data, no evaluation, no base rate and no rationale for the design. Everything below is therefore a description of a specification, tier **[model]** at best, not **[empirical]**. Any claim about effects is **[wiki synthesis]** and flagged as such.

## The mechanism

**[model]** Ranking for release runs in four steps, within a competitive level (interchangeable positions) inside a competitive area (an org unit or geographic location) of one agency, with separate registers by tenure group:

1. Total score = performance credit (three most recent ratings in a four-year window) plus veterans' preference points.
2. Tenure subgroup I ranks above II.
3. Earlier service computation date.
4. Agency discretion if still tied.

Ratings convert to points as Level 5 = 7, Level 4 = 5, Level 3 = 3, Levels 1-2 = 0, a steeply non-linear map in which a Level 2 counts the same as a Level 1. Missing ratings are imputed by rule (modal rating if none, average if two, multiply by three if one). The old practice of converting performance into "artificial years of service" is dropped. Veterans' preference is reduced to a points supplement (5 for 30%-plus disabled, 3 for other preference eligibles); the FAQ says this does not guarantee a preference eligible ranks ahead of every non-preference eligible.

## Other design changes

- **Displacement rights:** bump and retreat replaced by one assignment right, capped at 3 grades below (5 for 30%-plus disabled preference eligibles), requiring a Level 2 or higher current rating; mandatory for the competitive service, discretionary for the excepted service. A job-analysis-based skills assessment applies, not relying principally on automated self-assessment, waived by five years of same-work at Level 3 or higher.
- **Coverage:** initial probationers, trial-period employees, temporary appointments of a year or less, Schedule C and G are excluded from ranking and assignment rights (they get modified notice).
- **Competitive-area control:** defined by the agency head or designee, not delegable below headquarters; OPM pre-approval only if set or materially modified within 90 days before notices; a single area may combine units to widen competition. A 180-day whole-area abolition shortcut skips registers and assignment rights.
- **Appeals:** OPM for notices issued on or after 2026-09-02, MSPB for earlier notices. **[model]** This moves the adjudicator, which changes the veto-point inventory on a workforce reduction ([[veto-points-and-bureaucratic-autonomy]]).
- **Guardrails named:** discriminatory, retaliatory, politically motivated or pretextual use is barred (351.204); performance or conduct terminations must go through 5 CFR part 11, not RIF; records preserved two years; a 50-or-more-separations trigger adds notification duties.

## What the source does not say

The memo names manipulation of competitive-area boundaries, disguised performance terminations, ad hoc conversion of awards into RIF credit and erosion-of-duties reclassification as failure modes. It is silent on rating inflation or compression and on uneven rater standards across units. **[wiki synthesis]** That silence matters: once ratings of record set release order they become a high-stakes measure, which is the Holmstrom-Milgrom distortion concern in [[multitask-incentive-theory]] and the predicted management response described in [[blame-avoidance-and-negativity-bias]]; the source neither claims nor tests this. The rule relies on ratings of record as valid performance measures without addressing rater reliability, and the non-linear rating-to-points map is an aggregation step of the kind [[measurement-validity-framework]] would audit.

## Bearing on the wiki

**[wiki synthesis]** The rule moves the progression margin, not the entry margin, of protection in Xu's decomposition ([[civil-service-tenure-and-political-insulation]]): it changes what accrued tenure buys in a RIF, while the probationary and trial-period exclusions operate at the entry margin. It is consistent with, not evidence for, the priced downside of seniority rules recorded in [[personnel-economics-of-the-state]], and it places discretion in the rating and area-definition steps, where that page's discretion-versus-rules sign flip applies. As a lever it belongs in [[reform-levers]] at tier (ii) or (iii) at most, never tier (i): no evidence accompanies it. Candidate register axes (not added this run): retention basis in layoffs (seniority, performance, veterans' supplement), and scope of layoff competition (competitive-area definition).

## Scope

US federal executive-branch RIFs under 5 CFR part 351; applies by notice-issuance date (earlier notices under the old rules); agency-specific statutes may differ; emergency shutdown furloughs excluded. The memo says further OPM guidance is promised. No comparison with private-sector layoff practice is made. The design premise (performance-based retention over seniority-based, with stated commitment to merit-system principles) is inferred from the mechanism; the source states no argument for it.

## Source

- `raw/research/weekly-2026-09-29/03-opm-final-rif-rule-2026.md` — OPM (Director Kupor) memorandum to agency heads, "Final Regulations on Reduction in Force (5 CFR part 351)," 2026-09-02, with "RIF Basics" and FAQ attachments. https://www.opm.gov/chcoc/latest-memos (captured via local download and `capture_pdf`).
- Derived summary: `raw/research/weekly-2026-09-29/.ingest/03-opm-final-rif-rule-2026.summary.md`.

## Related

- [[civil-service-tenure-and-political-insulation]] — the entry/progression protection decomposition this rule acts on.
- [[personnel-economics-of-the-state]] — seniority rules, discretion versus rules, selection.
- [[multitask-incentive-theory]] — ratings as a high-stakes measure.
- [[measurement-validity-framework]] — the rating-to-points aggregation step.
- [[blame-avoidance-and-negativity-bias]] — predicted rating-inflation response (wiki synthesis only).
- [[veto-points-and-bureaucratic-autonomy]] — the MSPB-to-OPM appeal shift and the 90-day pre-approval gate.
- [[red-tape]] — procedural safeguards and documentation burden.
- [[reform-levers]] — performance-first retention as a lever candidate with no outcome evidence.
- [[whitehall-monitor-2026-case-profile]] — a same-week UK case of civil-service personnel-rule design (pay progression, exit schemes).
