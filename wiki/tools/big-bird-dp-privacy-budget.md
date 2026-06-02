# Big Bird: DP Privacy Budget Manager for the W3C Attribution API

Big Bird is a **differential-privacy budget manager** that enforces global device-epoch individual differential privacy (IDP) across all web domains querying the browser's W3C Attribution API, implemented in Rust and integrated into Firefox's Attribution prototype. It solves the core architectural flaw in the current W3C standard: treating each querying domain in isolation allows cross-querier adaptive attacks and, critically, permits Sybil domains to exhaust a shared budget (denial-of-service against the privacy guarantee itself). The Firefox implementation makes this deployed infrastructure rather than theory.

## Problem it solves

The W3C Privacy Sandbox Attribution Reporting API is the ad-tech industry's replacement for third-party cookies as a cross-site measurement mechanism — it lets advertisers attribute conversions (purchases, sign-ups) to ad impressions across sites while ostensibly adding privacy protections. The current design enforces IDP per domain independently. This fails in two ways:

1. **Cross-querier adaptivity:** advertiser domains can coordinate queries to exploit the independent-budget assumption.
2. **Sybil depletion:** an attacker controlling many cheap domains can exhaust the shared global privacy budget, denying its benefits to legitimate queriers.

## Mechanism

Big Bird's key insight is that benign Attribution workloads have **stock-and-flow structure**: impressions create potential privacy loss; conversions realize it. Meaningful budget consumption should be tied to genuine user actions across distinct web domains, not to the number of querying domains.

Enforcement components:
- **Privacy-loss-based quotas** per impression site and per conversion site — limits how much of the global budget any single site can consume.
- **Per-user-action cap** on how many site quotas can be activated per event — ensures adversarial impact scales with real user interactions, not Sybil domain count.
- **Global device-epoch IDP** enforced jointly across all domains, replacing the per-domain isolation that the current spec uses.

The result: formal resilience to depletion attacks + maintained utility for benign advertisers even under active attack.

## Implementation and evaluation

- **Language:** Rust.
- **Integration:** Firefox Attribution prototype (browser-level, not extension-level — requires browser vendor buy-in).
- **Evaluation:** theoretical proofs + empirical runs on real ad-tech data.
- **Venue:** arXiv 2506.05290, CS.CR (Cryptography and Security). Submitted June 2025, revised May 2026 (v3). Lead: Pierre Tholoniat.

## Relevance to consumer counter-power

The W3C Attribution API is being standardized as the privacy-safe cross-site measurement layer to replace third-party cookies. Its practical effect is to preserve advertiser surveillance capability inside a DP wrapper that may or may not provide meaningful protection. Big Bird is significant from a counter-power lens for three reasons:

1. **The current W3C spec is architecturally unsound** — the privacy guarantee it advertises does not hold under realistic multi-domain adversary models. Big Bird documents this formally. Advocates and regulators pushing back on Privacy Sandbox can cite this structural flaw.
2. **Browser-level enforcement is the leverage point** — browser vendors (Firefox, Chrome) are the chokepoint. A browser that ships Big Bird's budget model constrains advertiser surveillance scope at the platform layer, upstream of any user action.
3. **Sybil resilience matters for collective action** — counter-power coalitions that relied on the Attribution API's stated DP guarantees for data-sharing arrangements would be exposed to depletion attacks without something like Big Bird. The mechanism protects the integrity of the privacy budget as a shared resource.

The Firefox integration is the key signal: this is an academic result with an open path to production deployment, not shelf-ware.

## Source

- `raw/research/weekly-2026-06-01/08-big-bird-dp-privacy-budget.md`
  - **Origin:** arXiv abstract page for arXiv:2506.05290v3 (*Big Bird: Resilient Privacy Budgeting Across Untrusted Web Domains*). Captured 2026-06-01.
  - **Audience:** CS security/privacy researchers, browser standards engineers.
  - **Purpose:** mechanism proposal + formal analysis of W3C Attribution API privacy guarantees.
  - **Trust:** peer-reviewed academic preprint (arXiv CS.CR). Formal claims (IDP soundness, depletion resilience) are proven in the paper; empirical claims evaluated on real ad-tech data. The architectural flaw diagnosis of the current W3C spec is the load-bearing claim for this wiki — traceable to the abstract and the formal analysis in the full paper.

## Related

- [[browser-fingerprinting]]
- [[obfuscation]]
- [[privacy-badger]]
- [[adversarial-data-poisoning]]
- [[the-firms-view]]
