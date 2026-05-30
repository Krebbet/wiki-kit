# Conflict: Differential Privacy Deployment Trustworthiness

**Status:** Open — awaiting user ruling.
**Filed:** 2026-05-25
**Pages affected:** [[dp-audit-methodology]], [[the-firms-view]], [[algorithmic-collective-action]]
**Sources in tension:** `02-apple-dp-audit-sp2026.summary.md` (Position A — empirical audit evidence); `the-firms-view` §4 Solanki 2025 (Position B — firm DP-as-ACA-suppression framing); watchlist claim "DP-as-firm-counter to ACA — concrete deployment evidence" (implicit Position B)

---

## The dispute

**Not a dispute about whether DP works in theory.** Both positions agree that correctly-implemented low-epsilon DP provides meaningful privacy guarantees. The dispute is whether real-world DP deployments — specifically the largest shipped DP deployment in existence (Apple's DifferentialPrivacy.framework) — actually provide those guarantees, and whether "DP deployed" should be treated as a positive case for consumer privacy counter-power or as an instance of privacy theater.

---

## Position A — Empirical audit evidence (Apple DP audit, IEEE S&P 2026)

*Source: `raw/research/weekly-2026-05-25/02-apple-dp-audit-sp2026.md`. Distinguished Paper, IEEE S&P 2026.*

Apple's DifferentialPrivacy.framework on macOS Sonoma 14.2 / Sequoia 15.6 has DP violations in **5 of 9 audited mechanisms**, affecting 68–87% of collected data by property count. Specific failures:

1. **PRNG non-uniformity** — floating-point bugs in Apple's Gaussian noise generator, known in the academic literature since 2012, produce non-uniform sampling that reduces effective epsilon. The same bug was independently found in Google's histogram protocol. Neither company has patched its production deployment.
2. **Intentionally disabled local DP** — Apple's SecAgg protocols (Prio++Metadata, Prio++Metrics) hard-code local DP off. Disclosed to Apple; Apple confirmed this as "intentional." The protocols collect raw sensitive property data before applying aggregation.
3. **Epsilon values of 6–8 on sensitive properties** — enable >99.75% membership inference success. Apple's public ε=2 claim applies only to a subset of mechanisms and is not applied uniformly.
4. **Secret-share exposure** — on-device analytics logs expose raw secret shares in plaintext; reconstruction demonstrated from real leaked logs found on GitHub, Pastebin, and Reddit.
5. **Post-disclosure response** — Apple deprecated the broken mechanisms after disclosure, then reclassified the findings as "expected behaviour" without a CVE or public security advisory.

**Implication:** The largest deployed DP system fails its own guarantees for most of the data it collects. Claiming DP compliance as a consumer protection mechanism, without independent audit, is not a meaningful guarantee.

---

## Position B — Watchlist / strategy-layer implicit claim

*Source: `wiki/watchlist.md` → "Forward-looking themes: DP-as-firm-counter to ACA — concrete deployment evidence"; `wiki/the-firms-view` §4 documenting Solanki 2025's DP-as-ACA-suppression framing.*

The watchlist entry anticipates that concrete DP deployment evidence will be relevant for evaluating whether firms use DP to suppress Algorithmic Collective Action (ACA). The Solanki 2025 paper (documented in `the-firms-view`) shows that high-epsilon DP can suppress the signal gradients that ACA relies on — but this requires correctly-implemented DP to actually function. The implicit assumption is that deployed DP works as specified.

The conflict: if deployed DP routinely fails its own epsilon guarantees (Position A), then:
- Firms cannot use DP-as-ACA-suppression effectively (weakens the ACA threat model from [[the-firms-view]])
- Claimed DP compliance cannot be relied on as consumer protection (harms the "DP-as-counter-power" framing)
- Both the threat and the counter are weaker than the existing wiki framing implies

---

## Resolution options

1. **Distinguish claimed from audited DP.** Update the watchlist and strategy layer to require a distinction between DP-as-claimed (marketing) and DP-as-audited (verified low-epsilon implementation). Apple's case becomes the failure-mode anchor, not a positive deployment example.
2. **Update ACA threat model.** If real deployed DP reliably fails, the Solanki-based ACA threat in [[the-firms-view]] is weaker than stated — ACA signal leaks through broken DP. Note this in [[the-firms-view]] and [[algorithmic-collective-action]].
3. **Open a new forward-looking theme.** Add "DP audit as counter-power mechanism" to the forward-looking themes in watchlist — the reverse-engineering + Bayesian membership-inference technique is a replicable accountability tool (see [[dp-audit-methodology]]).

**Resolution rule:** Pending user ruling. The evidence clearly favours Position A for Apple's specific deployment. The question is how broadly to extend the "DP deployment is unreliable without audit" framing across the wiki.
