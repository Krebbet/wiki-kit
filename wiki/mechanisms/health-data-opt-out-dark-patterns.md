# Health Data Opt-Out Dark Patterns

Patient intake software used at approximately 1 in 6 US patient visits (Phreesia) and practice-management networks (Privia Health, athenahealth) systematically deploy two dark-pattern classes — obstruction and visual interference — that coerce consent to health information exchange (HIE) data sharing even when the same privacy notice explicitly describes an opt-out right. The combination renders opt-out procedurally impossible at point of care, forcing asynchronous email follow-up that carries data-leakage risk in the gap. HIPAA does not prohibit requiring acknowledgment as a condition of treatment, creating a legal void that HHS's current proposed rule would worsen (removing signature requirements rather than mandating opt-out symmetry). FTC has narrow jurisdiction over for-profit entities; HHS has the broader mandate. The identified structural fix — "symmetry of choice" (opt-out link co-located with opt-in trigger) — is technically trivial but not yet required by rule.

## Mechanism detail

### Vendor stack and scale

Three-vendor architecture is typical at independent clinics: a patient-intake platform (Phreesia), a practice-management network (Privia Health), and an EHR/billing platform (athenahealth). Each deflects responsibility for interface design to the others. Phreesia processes consent flows for ~17% of all US patient visits; Privia affects 5.2 million patients across ~5,000 providers in 15 states. Neither disclosed to The Markup's investigation who controls the opt-out interface configuration.

### Dark pattern taxonomy (health intake context)

**Obstruction:** The UI presents "I accept" as the only actionable button. An error blocks forward progress unless clicked. The privacy notice describes an opt-out right but provides no mechanism to exercise it within the flow — only an email address requiring asynchronous follow-up. This directly parallels the hard-to-cancel subscription pattern the FTC and CFPB have targeted under "unfair or deceptive practices."

**Visual interference:** Opt-out instructions are positioned outside the UI flow entirely (off-screen or in auxiliary documentation). The patient must exit the interface, locate a separate form, submit it, and await processing — during which HIE sharing may already occur. The privacy notice's own language acknowledges pre-opt-out disclosures are irrevocable.

### Legal architecture

- **HIPAA baseline:** Sharing patient data in HIEs is federally legal. Providers must offer patients a chance to opt out but are not required to make it easy. HIPAA does not require patients to sign the notice of privacy practices (NPP); providers need only document why a signature wasn't obtained. However, HIPAA also does not prohibit requiring NPP acknowledgment as a condition of treatment — a gap HHS acknowledges was "never envisioned."
- **State variation:** Florida and New York require explicit opt-in consent for HIE sharing. Arizona and Maryland permit opt-out-by-default with notice. Virginia (site of the primary documented case) has no additional requirement beyond the federal baseline. Many states follow HIPAA floor rules.
- **HHS proposed rule (2025–26):** Proposes eliminating the written-acknowledgment requirement. Legal experts interviewed describe this as moving in the wrong direction — removing friction without mandating opt-out symmetry leaves the dark pattern intact.
- **FTC jurisdiction:** FTC has authority over for-profit healthcare entities under Section 5 (unfair or deceptive acts/practices). The "cannot reasonably avoid the resulting injury" standard used in consumer finance applies directly to maze-like opt-out structures. FTC jurisdiction does not extend to non-profit hospitals; HHS retains that mandate.

### Data flow risk

HIE opt-out is prospective only. Once shared, records (lab results, diagnoses, prescriptions) are visible to any provider querying the exchange. In states where abortion care is criminalized, HIE records constitute a traceability vector for prosecutorial discovery. GuardDog (admitted to accessing records "under the guise of treatment" and routing them to personal injury law firms) illustrates commercial misuse under the same HIPAA-permissible sharing regime.

## Identified intervention points

**Regulatory:** HHS could amend HIPAA regulations to require: (1) opt-out mechanism co-located with opt-in trigger (symmetry of choice), (2) no forward progress gating on NPP signature. The HHS Office for Civil Rights director acknowledged this as a "considerable" intervention when asked directly. OCR has authority to act via rulemaking without Congressional action.

**FTC enforcement:** For-profit clinics and their vendors are within FTC jurisdiction. The "cannot reasonably avoid injury" unfair-practices standard maps cleanly to obstruction dark patterns. Active FTC rulemaking on dark patterns (cancel-as-easy-as-subscribe) creates a hook for healthcare-specific extension.

**Vendor leverage:** Because Phreesia and athenahealth serve a large fraction of independent clinics, a single interface change propagates to millions of patients. This is the structural parallel to Apple ATT: interface-layer change by a dominant platform achieves population-scale privacy improvement without individual consumer action.

**Open-source reference implementation:** Former federal health IT officials (Savage) proposed a government-funded open-source intake interface with correct opt-out design, available as a free drop-in for clinics. Federal health IT office competitions focused on intake UX are an existing procurement mechanism.

## Tooling opportunity

This sector surfaces two distinct tool targets:

1. **Healthcare DSAR/opt-out automation:** A symmetry-of-choice enforcement tool — analogous to California's DROP platform but targeted at HIE opt-outs — could automate the asynchronous email/form submission step, provide audit trail of pre-opt-out disclosure windows, and flag vendors/clinics that gate treatment access on NPP signature. Dark-pattern detection audit tooling (screenshot analysis of intake flows against obstruction/visual-interference criteria) could generate a compliance scorecard across Phreesia/athenahealth deployments, creating FTC referral-ready documentation.

2. **FTC rulemaking comment infrastructure:** The current HHS proposed rule and any FTC dark-patterns rulemaking extension to healthcare are active comment targets. Coordinated consumer comment campaigns (parallel to net-neutrality aggregation) with documented dark-pattern evidence would strengthen the rulemaking record. Evidence of the CFPB/FTC consumer-finance standard applying in healthcare is legally specific enough to be actionable in comments.

## Source

- `raw/research/weekly-2026-06-01/04-phreesia-health-data-dark-patterns.md` — The Markup / CalMatters investigative report by Alex Rosenblat (May 27, 2026); primary empirical basis; includes documented patient experience, expert legal analysis (Strahilevitz/U Chicago, Tovino/Oklahoma, Konnoth/UVA, Greene/DWT, Savage, Jaromin/NCSL), and vendor non-response; high trust.

## Related

- [[dsar-and-data-deletion]] — direct structural parallel: dark patterns as compliance shield; the 64% friction-injection rate in data brokers replicates in healthcare intake; DROP platform is the analogous collective infrastructure this sector lacks.
- [[surveillance-pricing-retail]] — extraction mechanism parallel: both sectors use opaque vendor stacks to obscure who controls the extraction interface; responsibility deflection is the same evasion pattern.
- [[barriers-to-evidence]] — FTC enforcement challenges apply here: for-profit/non-profit jurisdictional split, documentation burden, and vendor responsibility deflection are the same structural barriers documented in other FTC dark-pattern contexts.
- [[regulatory-responses]] — HHS proposed rule, HIPAA baseline, and state opt-in/opt-out variation are the regulatory substrate; the signature-requirement removal proposal is a live regression to track.
- [[noyb]] — GDPR dark-pattern enforcement precedent (ORF.at cookie-banner ruling) established "symmetry of choice" as an enforceable standard in the EU; the Strahilevitz framing explicitly invokes this standard as the US target.
- [[auto-enrollment-opt-out]] — structural inverse: healthcare intake is auto-enrollment into HIE sharing; this page documents the dark-pattern layer that defeats the nominal opt-out right that auto-enrollment regimes depend on.
