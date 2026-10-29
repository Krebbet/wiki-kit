# Anthropic and Opaque: license-and-hire deal (2026-10)

Around 2026-10-13, Anthropic struck a deal with Opaque (Opaque Systems, a confidential-computing / "confidential AI" startup) to license its technology and hire part of its team; terms were not disclosed. Trade press disagrees on the structure (license plus acquihire, outright acquisition, wind-down, or open-source continuation), so treat the structure as unsettled. Thin and secondary-sourced: the only captured source is a short Constellation Insights item (2026-10-28) leaning on a CEO blog post. Signal: Anthropic is buying confidential-AI capability for on-prem and sovereign enterprise deployments. Watch; do not rely on Opaque as a standalone vendor until the structure is clear.

## What is known

- **Deal date:** ~2026-10-13 (per the task brief; the captured Constellation item is dated 2026-10-28 and gives no deal date). Terms undisclosed (Constellation, 2026-10-28).
- **Announcement:** CEO Aaron Fulkerson (ex-ServiceNow) posted on opaque.co that a "new agreement with Anthropic ... carries OPAQUE's work forward". The post does not say whether Opaque continues as an independent company or product. No Anthropic statement is quoted in the source.
- **Opaque background (Constellation, 2026-10-28):** spun out of Berkeley research; confidential computing and "verifiable AI"; partnered with Nvidia, Intel, Microsoft and Google; closed a $24M Series B at a $300M valuation (date not given); rolled out a security framework adopted in Europe and the UAE; recently published open standards for sovereign AI and on-prem deployments (undated beyond "recent months"). No product, pricing or technical detail is given.
- **Rationale (Constellation's analyst framing, 2026-10-28, not an Anthropic statement):** Anthropic increasingly courts enterprises that want on-prem deployments, open models and sovereign AI architectures. Fits the enterprise push in [[landscape/anthropic-enterprise-distribution-2026-05]].

## Deal structure: sources disagree

| Outlet | Characterisation | Notes |
|---|---|---|
| Constellation Insights (2026-10-28) | License plus acquihire: Anthropic licenses Opaque and brings on some of the team | Captured in raw; headline says "licenses, releases ... in acquihire" |
| Dealroom | Acquisition | Not captured in raw; attribution as relayed, unverified here |
| AIWeekly | Wind-down | Not captured in raw; attribution as relayed, unverified here |
| iThome | Open-source work continues as "AgenTrust" | Single source, not captured in raw; unverified |

Only the Constellation item is in the raw corpus. The other three characterisations are second-hand and should be re-verified before being relied on. If a primary Anthropic or Opaque statement settles it, log the outcome in `conflicts/`.

## Read-through

- Same license-and-hire pattern as [[landscape/groq-nvidia-acquihire-2026-06]], which tends to leave the original company hollowed out (pattern inference, not a source claim for Opaque).
- Client risk (inference, not in any source): Opaque as a standalone vendor may be unsupported or absent going forward. Check contract and roadmap status before building on it.
- Nvidia, an Opaque hardware partner, is also active in agent-security hardware: see [[landscape/nvidia-open-agent-safety-platform-2026-09]]. The verifiable-AI angle sits next to [[landscape/agent-identity-governance-2026-09]].
- Sovereign and on-prem demand is also visible in [[llms/cohere-aleph-alpha]].

## Open questions

- Is Opaque still operating as a company, and who owns the IP and customer contracts?
- Is the open-source work continuing (the AgenTrust claim)?
- Does Anthropic ship confidential-AI features in its own platform, and when?

## Source

- `raw/research/weekly-2026-10-28/02-anthropic-opaque-acquihire.md` (Constellation Insights, 2026-10-28)
- Dealroom, AIWeekly and iThome characterisations: relayed in the ingest brief, not captured in raw.

## Related

- [[llms/anthropic-claude-family]]
- [[landscape/anthropic-enterprise-distribution-2026-05]]
- [[landscape/anthropic-series-h-2026-05]]
- [[landscape/groq-nvidia-acquihire-2026-06]]
- [[landscape/agent-identity-governance-2026-09]]
- [[landscape/nvidia-open-agent-safety-platform-2026-09]]
- [[llms/cohere-aleph-alpha]]
