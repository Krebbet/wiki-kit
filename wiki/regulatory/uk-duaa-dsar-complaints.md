# UK Data (Use and Access) Act 2025, Section 103: Mandatory DSAR Complaint Procedure

Section 103 of the UK Data (Use and Access) Act 2025 (in force 19 June 2026, per S.I. 2026/82 reg. 3(a)) inserts a mandatory internal complaint mechanism into the Data Protection Act 2018 (ss. 164A–164B). Any UK data controller must now: (1) provide an accessible electronic complaint form; (2) acknowledge complaints within 30 days; (3) respond without undue delay; and (4) report complaint volumes to the ICO on demand. The existing Article 77 UK GDPR right to complain directly to the ICO is displaced as the *first* step — controllers are now the mandatory first port of call.

## Structural significance

The UK approach is structurally distinct from the California DROP Act model ([[dsar-and-data-deletion]]). Rather than building a state-operated deletion portal (as California did for data brokers), the UK mandates that every controller build and operate its own complaint infrastructure — then requires them to report aggregate complaint volume to the regulator.

This has two counter-power implications:

1. **Lower individual complaint friction.** Web-submitted complaints cannot be rejected on form grounds; the 30-day acknowledgement SLA is enforceable; non-response is ICO-reportable. DSAR coordination tooling (e.g., a browser extension that files complaints on behalf of users) can now promise a legally mandated response timeline.

2. **Complaint-volume reporting as a targeting signal.** Once Secretary of State regulations activate s.164B reporting, the ICO will hold aggregate complaint-volume data per controller. This data — if published or obtainable via FOI — would allow third-party DSAR coordination services to identify high-complaint controllers (platforms with high non-compliance rates) and prioritise mass-complaint campaigns where enforcement pressure is weakest.

## Design inputs for DSAR coordination tooling

- Frame non-acknowledgement (>30 days) as an ICO-reportable violation; include the reporting pathway in any DSAR coordination tool aimed at UK controllers.
- The mandatory electronic form requirement means no fax/letter gatekeeping — web or API submission is legally sufficient.
- Track when s.164B reporting regulations land (date not yet confirmed); this is the trigger for complaint-volume public data.
- UK algorithmic pricing operators (hotel RMS vendors, surveillance-pricing retailers) are covered alongside all other controllers — the mechanism applies to the full universe of UK GDPR-governed processing.

## Source

- `raw/research/weekly-2026-06-22/04-uk-duaa-dsar-complaints.md`
  - **Origin:** UK primary legislation (legislation.gov.uk); commencement confirmed by S.I. 2026/82.
  - **Audience:** Legal practitioners and regulated entities.
  - **Purpose:** Codify mandatory pre-ICO internal complaint resolution.
  - **Trust:** Primary legislation — authoritative. Captured text is a web scrape with UI boilerplate noise; substantive provisions (ss. 164A–164B) are clearly legible in the source.

## Related

- [[dsar-and-data-deletion]] — California DROP Act model; UK s.103 is a distinct structural approach
- [[regulatory-responses]] — broader EU/UK regulatory action landscape
- [[data-disruption-strategy-map]] — DSAR-coordination lever now has UK statutory backbone
- [[barriers-to-evidence]] — s.164B complaint-volume reporting as partial counter to evidence-access asymmetry
- [[noyb]] — noyb's model-complaint strategy strengthened by s.164A mandatory response obligation
