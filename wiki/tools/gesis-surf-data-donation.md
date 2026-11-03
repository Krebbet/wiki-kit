# GESIS Surf (Consented Web-Browsing Data Donation)

GESIS Surf is an open-source (MIT) research infrastructure for longitudinal, consented collection of web-browsing data: a Chrome/Firefox extension (TypeScript, Manifest V3), a Django REST backend with PostgreSQL, and ELK logging, deployed in Docker. It passively captures clicks, scroll events, page metadata and full HTML snapshots inside a hierarchical session model, links them to panel survey responses, and has run with 1,000+ participants over 2+ years in the GESIS Panel.dbd. Privacy is enforced at the point of collection: strict opt-in with recorded consent, plus server-managed per-domain rules evaluated on-device before any transmission. It is a researcher-run donation model: no participant governance, pooling, bargaining or compensation layer is described.

## Structure

- **Operator:** GESIS (Leibniz Institute for the Social Sciences) and Univ. Mannheim; authors Ramirez, Mangold, Stier. Code: github.com/gesiscss/gesis_surf_extension (v2.0.0, MIT).
- **Per-domain privacy modes:** `default` (full capture fallback), `full_allow`, `only_host` (hostname only, content masked, no HTML capture), `full_deny` (domain and content suppressed), `private` (user-activated pause, 15-minute auto-expiry). Rules fetched at login and cached locally (IndexedDB, `chrome.storage.local`).
- **Minimization:** `only_host`/`full_deny` block HTML snapshots and mask referrer/target; `private` blocks all content events. Policy evaluated by on-device services, so backend configuration cannot override it.
- **Consent and compliance:** extension inactive until informed consent is recorded and the user logs in; consent version stored per record; GDPR records of processing and data-protection-officer review built in as reusable components.
- **Positioning:** against commercial tracking panels (opaque governance) and narrow short-term academic tools.

## Limits

- Researcher-side trust assumed; no independent evaluation of privacy guarantees or data quality in the paper.
- Full-URL and HTML capture under default rules is high re-identification risk; no cohort-level safeguards stated.
- No member control over downstream use, which is the gap a [[data-cooperatives|data cooperative]] would fill.

## Design inputs *(editorial)*

- The five-mode per-domain scheme and on-device policy services are a candidate template for a collective's donation client feeding [[collective-bargaining-for-data]] or [[data-market-mechanism-design]] pools.
- Closest operational analogue is [[markup-citizen-browser]] (paid panel, platform-feed audits); Surf adds open code and general-purpose collection.

## Source

- `raw/research/weekly-2026-11-02/03-gesis-surf-data-donation.md` (arXiv 2610.41441, captured 2026-11-02).

## Related

[[data-cooperatives]], [[collective-bargaining-for-data]], [[data-market-mechanism-design]], [[markup-citizen-browser]], [[transparency-tools]], [[regulatory-responses]], [[dsar-and-data-deletion]]
