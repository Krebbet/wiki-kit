# MIDATA

MIDATA is a Swiss nonprofit **health data cooperative** founded in 2015, operating a member-owned data platform for citizen-directed stewardship of health data. The OECD-cited canonical example of a consumer [[data-cooperatives|data cooperative]], built on open-source infrastructure developed at ETH Zurich and Bern University of Applied Sciences.

## Structure and economics

- **Legal form:** Nonprofit cooperative, Switzerland.
- **Ownership:** Data account holders may become cooperative members and govern the coop at the general assembly.
- **Revenue model:** Nonprofit. Net profits are reinvested into services on the platform. Operates with an explicit "no financial incentives" model, "similar to citizen science platforms or blood donation" (per midata.coop).
- **Data model:** Personal data stored on the MIDATA platform. Data account holders grant selective access to researchers and clinical studies on a per-request basis; all datasets encrypted, only account holders have access to their individual data, all access logged.

## Federation model

MIDATA Switzerland actively supports "the foundation of regional or national MIDATA cooperatives that share the data platform infrastructure." Per the midata.coop/cooperative page:

> The MIDATA model enables the construction of regional/national cooperatives which, by a set of common rules, permit global research projects to be set up and carried out in a fair and democratic manner.

This is the **second-level cooperative / federation-first architecture** pattern — the same scaling blueprint the OECD featured in the [[coopcycle]] case on [[platform-cooperatives]]. Each national MIDATA coop is autonomous but shares platform infrastructure and common governance rules.

## Open source

The MIDATA platform is built on **Open MIDATA Server**, released under GNU GPL v3.0. Developed at ETH Zurich and Bern University of Applied Sciences (BFH). This is one of the few consumer data coops with a fully public technical stack.

## Scope

- Focus: **health data**, smartphone-app-based services.
- Ecosystem: startups, IT providers, research groups can connect mobile apps to the platform. Apps may offer data-based services to members and collect data for research.
- Explicit "open innovation ecosystem" positioning.

## Counter-power mechanism

MIDATA is a consumer [[data-cooperatives|data cooperative]] in the orientation-toward-governance sense, not the orientation-toward-bargaining sense (per the Mendonça et al. coop / union distinction on [[data-cooperatives]]). The coop's purpose is to steward member-contributed health data for collectively-agreed use (medical research, clinical studies), *not* to negotiate better consumer terms with a specific corporate counterparty.

**Relationship to dynamic pricing:** MIDATA does not directly counter any pricing mechanism on [[dynamic-pricing-overview]]. Its value to this wiki is as the **structural template** — the working example of the coop model cited in both the Ada Lovelace 2021 report and the Mendonça et al. 2025 survey as the canonical use case.

## Scope and limitations

- **Single-domain (health).** No generalisation yet to pricing-surveillance or tenant-screening domains, which are the specific counter-power use cases this wiki tracks.
- **Research-oriented, not market-oriented.** Members donate data for research; the coop does not negotiate commercial terms on their behalf.
- **Thin capture of primary source.** The midata.coop/cooperative page is compact (~3KB captured); the Articles of Association PDF was linked but not separately captured in this run.

## Source

- `raw/research/consumer-data-pooling/01-04-midata-cooperative.md`
  - **Origin:** MIDATA (midata.coop) — primary organisational source; the "Cooperative" about-page.
  - **Audience:** potential members, researchers, cooperatives-movement readers.
  - **Purpose:** organisational self-description: values, governance, legal basis.
  - **Trust:** primary org source; compact but load-bearing for structural claims (founding year, nonprofit status, federation model, open-source platform).
- `raw/research/consumer-data-pooling/05-01-ada-legal-mechanisms.md` — Ada Lovelace 2021 report cites MIDATA as a reference case.
- `raw/research/consumer-data-pooling/06-02-arxiv-data-coops-governance.md` — Mendonça et al. cite MIDATA as their first application-example ("the most famous").

## Related

- [[data-cooperatives]]
- [[platform-cooperatives]]
- [[coopcycle]]
- [[regulatory-responses]]
