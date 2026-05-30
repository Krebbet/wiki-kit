# DSAR and Data Deletion

California's data broker regulatory regime — CCPA plus the 2023 Delete Act — achieves only 9% full compliance across 522 registered brokers, with 43% blocking all privacy-rights exercise and 64% injecting design friction, per a 2026 FAccT audit (Gueorguieva, King, Panidapu, Ho; UW + Stanford RegLab). The paper documents the structural failure of individual Data Subject Access Request (DSAR) mechanisms when compliance is delegated to the regulated party without a private right of action, and identifies two systemic counter-mechanisms: California's DROP platform (active January 2026) enabling one-click deletion to all 500+ registered brokers simultaneously, and opt-out preference signals (Global Privacy Control / OOPS) being mandated at the browser layer by January 2027.

## Key findings

- **9% full compliance**: only 9% of the 522 registered California data brokers fully comply with CCPA and Delete Act requirements; 43% block exercise of all privacy rights.
- **Dark patterns as compliance shield**: 64% of brokers inject friction — excessive CAPTCHAs, redundant forms, broken links, mandatory identity verification for requests that legally cannot require it — operationalizing obstruction rather than exception.
- **Structural cause**: compliance correlates with being a corporate subsidiary (larger firms already under compliance pressure); CCPA's removal of the private right of action in 2018 was a direct industry concession that eliminated the enforcement mechanism individual DSAR depends on.
- **Silent duplicate fragmentation**: opaque corporate structures create nominally distinct shell brokers holding the same data, fragmenting deletion requests and requiring consumers to identify and submit to each entity separately.
- **Collective submission effect**: WebChoices (DAA's industry opt-out tool covering 97 brokers) delivers 58% more opt-out requests to participating brokers than individual submission — empirical benchmark for what centralized request infrastructure achieves.

## Mechanisms documented

**Individual DSAR (failed mechanism):** The right to request access, deletion, or opt-out directly from each data broker. Structurally dependent on broker self-compliance; without centralized enforcement or a private right of action, friction is a rational competitive strategy for brokers.

**DROP (California DELETE Request and Opt-out Platform):** Active January 2026. State-administered API allowing a single consumer submission to propagate deletion and opt-out requests to all 500+ registered brokers simultaneously, with mandatory 45-day processing cycles. Functions as collective-action infrastructure: each enrolled consumer multiplies request volume across the full broker population. Analogous in design logic to [[data-cooperatives]] — centralized negotiation/submission rather than individual bilateral requests.

**Global Privacy Control / OOPS (browser-layer opt-out):** Opt-out preference signal transmitted automatically by compliant browsers. Mandatory broker response required by January 2027 under California law. The Apple ATT parallel is empirically load-bearing: when privacy controls are surfaced prominently at the interface layer, consumer adoption is overwhelming — framing interface design as a determinative lever.

**Broker opacity-scoring index:** The paper (Appendix A.7) operationalizes a scoring index combining friction features, sensitive data categories held, and transparency compliance. Proposed as a public-facing tool or integration layer for existing privacy tools; could be used to prioritize enforcement or guide consumer avoidance.

**Legislative gap — private right of action:** The 2018 removal of CCPA's private right of action is identified as the structural missing piece. Class-action aggregation against brokers is explicitly recommended by the authors as a complement to DROP's administrative mechanism.

## Source

- `raw/research/weekly-2026-05-25/01-data-broker-compliance-california-2026.md` — FAccT '26 peer-reviewed empirical audit of all 522 registered California data brokers against CCPA and Delete Act requirements; primary empirical basis for this page (Gueorguieva, King, Panidapu, Ho; UW + Stanford RegLab; high trust).

## Related

- [[transparency-tools]] — DROP and GPC/OOPS are new instances of transparency/opt-out infrastructure; this page documents the failure mode that centralized infrastructure was designed to correct.
- [[collective-bargaining-for-data]] — WebChoices finding (58% more requests via collective submission) is empirical evidence that aggregated request infrastructure materially shifts broker behavior; DROP is the state-administered version of the same logic.
- [[data-cooperatives]] — DROP's design parallels the cooperative argument for centralized negotiation; state-administered collective action for data rights.
- [[obfuscation]] — broker dark patterns are the adversarial inverse: friction-as-defense against consumer rights exercise rather than friction-as-offense against surveillance.
- [[regulatory-responses]] — CCPA and the Delete Act are the regulatory substrate; the private right of action gap is a live legislative target.
- [[browser-fingerprinting]] — GPC/OOPS operates at the same browser-signal layer as fingerprinting countermeasures; the mechanisms interact.
- [[adversarial-data-poisoning]] — structural parallel: both this page and adversarial-data-poisoning document cases where the regulated/tracked party uses technical means to degrade the effectiveness of the extraction mechanism.
