# Groq $650M Raise / Nvidia LPU Not-Acqui-Hire (2026-06)

Nvidia's December 2025 non-exclusive licensing deal for Groq's LPU IP — paired with the simultaneous defection of founder/CEO Jonathan Ross, president Sunny Madra, and core staff to Nvidia — gutted Groq's original business while enriching its investors. Six months later Groq has pivoted fully to a neocloud model, raised a fresh $650M (June 2026), rebuilt its executive bench, and is running 13 data centers serving five million developers. The LPU chip business is gone; the inference cloud business is what Groq is now.

## The Nvidia Deal (December 2025)

- **Structure:** Non-exclusive IP licensing agreement — Nvidia paid Groq investors for rights to LPU technology; simultaneously hired founder Jonathan Ross (ex-Google TPU co-creator), president Sunny Madra, and other senior employees. Classic "not-acqui-hire": IP and talent transferred, legal entity stays independent.
- **Nvidia outcome:** Announced the **Nvidia Groq 3 LPX inference hardware system** at GTC (March 2026), built on the acquired LPU IP.
- **Groq outcome:** IP gone, CEO and president gone, prior $6.9B valuation (September 2025 round: $750M) rendered moot. Remaining CEO: Doug Wightman (co-founder, stayed on).

## $650M Round (June 2026)

- **Amount:** $650M
- **Lead investors:** Disruptive (Dallas, late-stage; Alex Davis, also Groq's chairman) and Infinitum (Fort Lauderdale hedge fund)
- **New valuation:** Not disclosed; prior was $6.9B (September 2025)
- **Use of proceeds:** Neocloud expansion, talent replacement, infrastructure build-out

## Neocloud Pivot

The neocloud business was built under Sunny Madra (now at Nvidia) after Groq acquired his AI data analytics company Definitive Intelligence in 2024. It survived the executive exodus and is now Groq's entire business:

- **Scale (June 2026):** 13 data centers across North America, Europe, Middle East, and APAC
- **Developer reach:** 5M+ developers; thousands of AI companies
- **Throughput:** Trillions of tokens per week (self-reported, unaudited)

Groq operates in a crowded inference neocloud category. Baseten reportedly raising $1.5B (June 2026). See [[landscape/agentic-compute-pricing-2026-04]] for the broader inference compute economics backdrop.

## New Executive Bench

| Role | Person | Background |
|---|---|---|
| CEO | Doug Wightman | Co-founder; stayed post-deal |
| COO | Alan Rice | Previously xAI, Meta |
| CTO | Sinclair Schuller | Co-founded Apprenda (→ Red Hat); then Nuvalence (→ EY, 2024) |
| CPO | Rakesh Malhotra | ~decade in Microsoft cloud products |

## Comparable: Scale AI After Meta Deal

Scale AI CEO Jason Droege told Forbes that Scale rebounded after Meta's $14.3B not-acqui-hire (~12 months prior to June 2026) and is on track for $1B in revenue. The pattern — investors profit, entity survives as a stripped-down pivot — is repeating. Not-acqui-hires appear to be a durable mechanism for large players to acquire IP and talent without triggering antitrust scrutiny from a full acquisition.

## Conflict / Structural Notes

- Groq no longer has proprietary chip IP. Its "inference neocloud" differentiation is operational (multi-region, scale, developer tooling), not silicon. This is a weaker moat than the LPU was.
- The non-exclusivity of Nvidia's license means Groq theoretically retains rights to the LPU design — but with Ross and the engineering team at Nvidia, exercising those rights is practically infeasible.
- The $650M raise at undisclosed valuation, after a $6.9B prior, is a signal of significant step-down; investors and new money are betting on neocloud, not on a chip revival.

## Source

- Raw capture: `raw/research/weekly-2026-06-24/03-groq-650m-nvidia-acquihire-2026.md`
- URL: https://techcrunch.com/2026/06/22/ai-chipmaker-groq-confirms-650m-raise-re-staffs-after-nvidias-20b-not-acqui-hire-deal/
- Captured: 2026-06-24

## Related

- [[landscape/agentic-compute-pricing-2026-04]] — inference compute economics; agent workloads driving neocloud demand
- [[landscape/ai-infrastructure-frontiers-2026]] — inference-at-scale; Bessemer infra thesis
- [[llms/openai]] — OpenAI model platform; GPT-5.5 on AWS Bedrock as inference distribution comparison
- [[landscape/openai-microsoft-restructure-2026-04]] — IP and partnership restructuring patterns in frontier AI
- [[platforms/databricks]] — alternative restructuring pattern (contrast)
