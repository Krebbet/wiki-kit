# ILO Platform Worker Convention (ILC-114, 2026)

The ILO's 114th International Labour Conference (Geneva, 1–11 June 2026) is conducting its second and final discussion on a draft Convention and Recommendation on decent work in the platform economy (ILC.114/Report V(4)). If adopted, it will be the first binding international labour standard targeting platform-economy extraction mechanisms — algorithmic management opacity, employment misclassification, social-protection exclusion, and the absence of collective bargaining rights for gig workers.

## Source

- `raw/research/weekly-2026-06-08/05-ilo-platform-worker-convention.md`
  - **Origin:** ILO official committee page, 114th International Labour Conference, Geneva, 2026.
  - **URL:** https://www.ilo.org/international-labour-conference/114th-session-international-labour-conference/committees-114th-session-international-labour-conference/standard-setting-committee-decent-work-platform-economy-2026
  - **Captured:** 2026-06-08.
  - **Trust:** Primary institutional source; ILO treaty-making process with publicly logged amendments. Authoritative on procedure and document structure; final text and adoption outcome pending as of capture date.
- `raw/research/weekly-2026-06-08/.ingest/05-ilo-platform-worker-convention.summary.md` — ingest summary with actionability analysis.

## What It Is

The Standard-Setting Committee on Decent Work in the Platform Economy is the ILO's mechanism for translating tripartite negotiations (governments, employer groups, worker organizations) into binding international labour standards. A **Convention**, once adopted by the Conference and ratified by member states, imposes enforceable national-law obligations. The companion **Recommendation** is non-binding guidance.

The draft text under second discussion in ILC-114 is ILC.114/Report V(4). Amendments were submitted through an online portal across five days (1–5 June 2026), organized by article cluster:

- 1 June: Preamble and Arts. 1–7, 12, 24
- 2 June: Arts. 8–11 and 13–15
- 3 June: Arts. 16–23
- 4 June: Recommendation Preamble and Paras. 1–11
- 5 June: Recommendation Paras. 12–19

Final text and adoption vote: expected by 11 June 2026. **Status as of 2026-06-08: outcome pending.**

## Key Provisions

Four provision clusters are directly relevant to counter-power tooling and the wiki's themes:

**Algorithmic management transparency and appeal (Arts. 8–15 area).** The draft mandates disclosure of automated decision-making systems used for task allocation, dynamic pricing, performance scoring, and deactivation — and requires a right to human review and appeal of automated decisions. This is the gig-economy equivalent of GDPR Art. 22 automated-decision rights, applied specifically to the employment context.

**Employment classification presumption.** The Convention establishes a presumption-of-employment framework, shifting the burden to platforms to demonstrate that workers are genuinely independent contractors. Portable worker profiles and earnings records become **evidence infrastructure** under this frame — a direct design input for portable-worker-ID tooling.

**Social protection portability.** Platforms are required to contribute to social security schemes for platform workers. This creates the legal frame for collective-pool and portable-benefits designs (see [[solidarity-stack-readout]]).

**Collective bargaining rights.** Platform workers gain the right to organize and bargain collectively. Worker-representative structures — including cooperative governance bodies — qualify as representative parties under a ratified Convention, strengthening the legal standing of [[drivers-cooperative]], [[coopcycle]], and similar cooperative models.

## Ratification Status and Timeline

- **ILC-114 second discussion:** 1–11 June 2026.
- **Adoption vote:** expected before 12 June 2026 close of Conference.
- **Post-adoption:** ILO Conventions enter into force after a threshold number of member-state ratifications (typically two). Ratification timelines vary widely — months to years.
- **Monitoring:** ILO tracks ratification status per Convention at normlex.ilo.org. No ratifications on record as of capture date; the Convention has not yet been adopted.

Early-ratifying countries are the highest-leverage initial deployment targets for compliance tooling.

## Tooling Hooks

The Convention's mandates open concrete design space for counter-power tooling:

1. **Algorithmic audit / wage-transparency tools.** The algorithmic-transparency articles provide a regulatory specification baseline. A wage or deactivation audit tool (e.g., WAO FareShare-type) built to ILO disclosure standards is portable across all ratifying jurisdictions — a compliance-compliance dividend for open tooling.

2. **DSAR-equivalent rights for workers.** The appeal and human-review requirements function as a worker-facing data-subject-access-request right targeted at algorithmic decisions. Tooling that packages and submits these requests (analogous to GDPR DSAR tools on the consumer side) becomes a legal-compliance utility post-ratification.

3. **Portable worker profile / earnings record.** Employment-status determination under the Convention requires documentary evidence of the worker–platform relationship. Portable, worker-controlled work-history records become both a compliance product and an organizing infrastructure.

4. **Social-protection pool design.** The social-protection portability mandate is a regulatory opening for collective portable-benefits systems — a design input to [[solidarity-stack-readout]] and related portable-benefits work.

5. **Ratification monitoring feed.** Tracking which states ratify, and when, is actionable intelligence for deployment sequencing. A lightweight normlex scraper feeding the [[regulatory-responses]] page would keep the wiki current.

## Relationship to Existing Wiki Positions

No conflict with existing wiki positions identified. The Convention reinforces the wiki's core framing that regulatory instruments and technical counter-power tools are complementary rather than competing approaches. It is the most significant new entry in the [[regulatory-responses]] landscape — the first binding international standard for platform work.

## Related

[[platform-cooperatives]], [[drivers-cooperative]], [[coopcycle]], [[opencourier-protocol]], [[regulatory-responses]], [[collective-bargaining-for-data]], [[solidarity-stack-readout]]
