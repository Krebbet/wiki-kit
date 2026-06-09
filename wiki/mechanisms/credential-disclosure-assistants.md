# Credential Disclosure Assistants

ETH Zurich empirically validates that EUDI Wallet users systematically overshare official identity credentials — ~20% would disclose their official ID to news websites — and demonstrates that a category-level "Credential Assistant" nudge cuts disclosure error rates from ~15% to ~7%, while residual risk at EU scale still exposes tens of thousands of users. The pattern generalises beyond EUDI: any credential or permission request context (OAuth, app permissions, DID/VC wallets) faces the same structural asymmetry between verifier self-registration and user-side decision support.

## Source

- **Raw capture:** `raw/research/weekly-2026-06-08/03-eudi-wallet-credential-disclosure.md`
- **Citation:** Zingg, Kostiainen, Lain, Bechtold, Nakatsuka, Čapkun. "Credential Disclosure in (EU) Digital Identity Wallets: Privacy Risks and Practical Mitigations." arXiv:2606.06354. ETH Zurich, 2026 (pre-print; venue likely CCS or USENIX Security). Methods: survey of 1,035 users + 27 experts across 166 websites / 14 credentials; simulated user study with 1,002 participants.

## The Oversharing Problem

The EUDI Wallet (operational target: late 2026) lets websites self-register which credential attributes they claim to need. The EUDI Wallet rejects requests exceeding what was registered, but there is no scalable enforcement mechanism preventing over-registration — directly mirroring the over-claiming pattern in privacy policies.

Empirically measured oversharing from the user survey (all unjustified cases):

- ~20% of users would disclose their official ID to news websites
- ~9% would disclose their official ID to search engine websites
- ~34% would disclose bank account validation to e-commerce websites (misidentified as usable for payment)
- ~31% accepted a medical records request from LinkedIn in the live disclosure scenario vs. ~0% who said they would do so in a survey

The gap between survey responses and live acceptance rates is systematic and large — across all unjustified credential-website pairs, users disclosed significantly more when responding to an actual request than when asked in a survey. This is the privacy paradox operating at credential-disclosure granularity, and it implies that usage-log data would amplify rather than correct oversharing.

At EUDI scale, even the post-intervention residual rate of ~7% means ~70,000 users at risk per 1 million users. The paper notes that the simulated environment excluded dark patterns and service-denial coercion, so real-world oversharing rates are likely worse.

## Why Users Overshare

Three identified mechanisms:

**1. Naming confusion.** Users connect the credential or website name to a plausible but incorrect use case. Wikipedia-like encyclopedia sites triggered disclosure of diploma (~10%) and university transcript (~7%) credentials because users associated the educational content with an educational identity requirement that does not exist.

**2. Purpose-unclear requests.** The current EUDI framework has no plan to allow websites to display a purpose for a credential request in the wallet UI. Without a stated purpose, users default to liberal disclosure. Notably, an extensive website-provided purpose *increased* unjustified disclosure (~22% with purpose vs. ~16% without) — verifiers can exploit purpose statements to inflate acceptance.

**3. Credential-function anchoring.** Users falsely assign a functional use to a credential based on its name. Bank account validation (which contains no payment execution data) was disclosed at ~32–34% rates to video game, e-commerce, and air travel sites because users believed it could be used for payment. The paper flags this as a previously undocumented mechanism that verifiers could deliberately exploit.

## The Credential Assistant

**What it is.** A UI nudge displayed at the moment of a credential disclosure decision. It shows either expert recommendations or crowdsourced user opinions on whether the credential is appropriate to share with the requesting website category. It is non-intrusive, displaying the same format regardless of credential sensitivity.

**How it works.** The assistant operates at the *website category* level rather than per-site (not scalable) or per-request-context (not feasible without stated purpose). Opinion data is collected via deliberate surveys of users and expert panels — not from usage logs. Expert sample: ~24 experts per category is sufficient for ±5pp precision at 95% confidence under the observed inter-class correlation of ~0.057, though high-disagreement categories may require 100+.

**Effectiveness.**
- Expert recommendations condition: error rate dropped from ~15% to ~7% (significant at p ≤ 0.05 by Fisher's exact test for 3 of 4 tested designs)
- Average mistake reduction: ~8 percentage points across designs
- Low confidence (51–55% recommend to disclose) had near-zero nudging effect; standard confidence (81–85%) produced significant effect; high confidence (91–95%) produced no additional improvement over standard

**Demographic adaptation.** Users aged 18–29 responded more strongly to user-opinion framing; users aged 50+ responded more strongly to expert-recommendation framing. A demographically adaptive display style would outperform a uniform one.

**Data sourcing principle.** Usage data must not be used to train a disclosure recommendation model. Because users overshare more when responding to live requests, usage logs would encode and propagate the oversharing pattern. Only deliberate surveys or expert panels yield clean signal.

**Residual risk.** The non-intrusive nudge leaves a ~7% error rate. For sensitive credentials, the paper recommends browser-warning-style interruption (a known, habituated UX pattern from SSL/phishing warnings) rather than inline nudges.

## Collective Norms as Counter-Power

The crowdsourced user-opinion component of the Credential Assistant is structurally equivalent to a disclosure-norms cooperative: a pooled collective resource that benefits members by aggregating privacy judgments across many individuals. Key properties of this mechanism:

- Opinion data is pre-collected via survey, not extracted from live behaviour, which keeps the collective resource from being polluted by verifier dark patterns or paid-accept campaigns
- The collective signal is applied at the moment of individual decision, converting diffuse social knowledge into actionable friction at the disclosure point
- The mechanism is independent of any individual user's domain expertise — the collective compensates for the knowledge asymmetry between the average user and a verifier's legal team

This directly parallels [[data-cooperatives]] as a structural form and [[collective-bargaining-for-data]] as a counter-pressure mechanism applied to identity infrastructure.

## Verifier Registry Audit Proposal

The EUDI framework requires verifiers to register all credential attributes they plan to request. There is currently no mechanism for scalable expert review of whether registrations are proportionate under GDPR Art. 5 (data minimisation).

The paper proposes using the Credential Assistant as a registry audit tool: compare registered attribute requests against the Credential Assistant's category norms, flag any registration requesting credentials for which the assistant would recommend non-disclosure, and route flagged registrations to human expert review. This converts what would be an exhaustive per-registrant manual audit into a triage pipeline.

From a counter-power standpoint, this is automated detection of over-claiming at the infrastructure level — the same pattern that [[noyb]] pursues through litigation, here operationalised as a continuous technical check. The collective disclosure-norm dataset becomes the evidentiary basis for enforcement referrals.

## Design Principles (Generalised)

These apply to any credential/permission disclosure assistant, not only EUDI:

1. **Category-level operation.** Per-site or per-context recommendations are not scalable. Category is sufficient for most cases; multi-service sites may need separate handling.
2. **Survey sourcing, not usage logs.** Usage data amplifies oversharing. Deliberate surveys and expert panels yield the accurate norms needed.
3. **Confidence threshold gating.** Display recommendations only at ≥81% confidence. Sub-55% confidence produces no nudging effect and wastes salience budget.
4. **Demographic framing.** Younger users: peer-opinion framing. Older users: expert-recommendation framing.
5. **Selective intrusiveness.** Non-intrusive nudges for low-stakes cases; browser-warning-style interruption for sensitive credentials (official ID, medical records, prescriptions).
6. **Registry audit integration.** The same dataset used for user nudging can power automated over-registration detection.

## Keyring / DID Wallet Connection

The Berkman Klein Keyring project (watchlisted as first production-grade consumer DID/VC wallet) faces the identical UX problem described here. The EUDI Wallet provides the cryptographic rail for selective disclosure of individually hashed attributes, but leaves the disclosure decision UI to member states. This paper's Credential Assistant is a concrete, empirically validated answer to the UX design gap that will affect any DID/VC wallet deployment, including Keyring. The two are technically orthogonal (Keyring is the wallet; Credential Assistant is the decision-support layer) and should be treated as complementary components. See [[decentralized-agent-identity]].

## Related

[[decentralized-agent-identity]], [[dsar-and-data-deletion]], [[collective-bargaining-for-data]], [[data-cooperatives]], [[noyb]], [[browser-fingerprinting]]
