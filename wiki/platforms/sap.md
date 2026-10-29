# SAP (Joule Work, Joule Assistants, Business AI Platform)

At SAP Connect (2026-10-06) SAP presented Joule Work (a natural-language work interface), Joule Assistants (role- and process-specific execution agents) and SAP Business AI Platform as the parts of what it calls the "Autonomous Enterprise". Verdict: buy-by-default for existing S/4HANA shops, but sequence business cases by actual GA dates, not announcement language. Most capabilities are not GA until Q4 2026 to Q1 2027, and the new finance assistants are Early Adopter Care only. All quantified claims are vendor-reported; no pricing and no model or agent-architecture detail is disclosed (2026-10). Single trade-press source relaying SAP material.

## What it is (2026-10-06)

- **Joule Work:** natural-language interface for asking questions and completing work across SAP and third-party data. Customer rollout is "just beginning" (2026-10).
- **Joule Assistants:** carry out operational steps inside business workflows using the company's existing data, authorizations and audit trails. Named: Accounts Receivable (prioritizes collections by risk, recommends next steps), International Trade, Governance, Spend Analytics, Revenue Recognition, Disclosure, Sourcing (Novartis pilot), supply chain agents, customer experience assistants.
- **Other launches:** SAP Pay (payments service), SAP Reltio, and S/4HANA Cloud Public Edition integrations with Ariba and Sales Cloud.
- **Partners:** Moody's supplier risk data inside Ariba Supplier Lifecycle and Performance; expanded ORO Labs partnership for procurement orchestration across mixed system environments.

## Under the hood

Thin. SAP grounds Joule Work answers in SAP Knowledge Graph, which it says maps more than 7 million data fields (vendor claim, 2026-10). Assistants run on existing company data, authorizations and audit trails. No model, RAG or agent-architecture detail is given. The source does not mention which model vendor powers Joule (see [[landscape/anthropic-enterprise-distribution-2026-05]] for the earlier, unconfirmed Claude-as-reasoning-engine announcement).

Patterns worth stealing: per-assistant configurable autonomy bound to existing authorization and audit infrastructure; knowledge-graph grounding over ERP data fields; separating the interface (Joule Work) from execution (Assistants).

## GA timeline (per SAP innovation news guide, via erp.today, 2026-10-28)

SAP's release uses present tense for most capabilities; the guide's dates differ.

| Status | Capabilities |
|---|---|
| GA now (2026-10) | SAP Pay (US, UK); SAP Reltio; S/4HANA Cloud Public Edition integrations with Ariba and Sales Cloud; Joule Work initial rollout |
| GA Q4 2026 | Supply chain agents; International Trade and Governance Assistants; Moody's supplier risk data in Ariba |
| GA Q1 2027 | Customer experience assistants; Spend Analytics Assistant |
| Early Adopter Care Q1 2027 | Revenue Recognition, Disclosure and other new finance assistants |

## Deployment, customization, cost, limits

- **Deployment:** embedded in the SAP application estate; both customers reporting results run S/4HANA.
- **Customization:** customers set the autonomy level of each assistant; assistants inherit existing authorizations. Novartis co-developed the Sourcing Assistant with SAP.
- **Cost:** not stated. No pricing disclosed (2026-10).
- **Limits:** capabilities gated by the dates above. Results tie to S/4HANA and clean, consistent process and data (Nestle). Readiness may depend on hands-on vendor support (CONA Services).

## Vendor-claim caveats

All of the following are SAP-reported, unaudited, and relayed through one trade-press article (2026-10):

- 110,000 SAP employees use Joule Work, with a measured 20% internal productivity gain across finance, HR and procurement. Methodology and baseline not given.
- International Trade Assistant cut trade classification effort "by up to 50%" in early deployments; customers unnamed; "up to" is a ceiling, not a typical result.
- Knowledge Graph "more than 7 million data fields": a size figure, not a quality or accuracy measure.
- Customer evidence is vendor-curated. Nestle (140-country S/4HANA transformation) credits consistent processes and trusted data for the AR Assistant but gives no figures. Maschinenfabrik Reinhausen (Joule Work desktop early adopter program) says work that took up to an hour in S/4HANA "is now accessible in seconds through natural language" (single anecdote, 2026-10). Novartis is a pilot only.
- Analyst doubts on agent security: the source carries none. It only advises reviewing authorizations process by process before activating assistants. The security posture of autonomous assistants is unassessed here; evidence is thin.

## Build-vs-buy signals

For SAP shops, buy is the default path, but value is gated by S/4HANA, data quality and vendor support. Set autonomy levels before assistants execute work, and plan business cases around GA dates (the finance assistants are not production-GA before Q1 2027 at the earliest).

## Source

- `raw/research/weekly-2026-10-28/05-sap-connect-joule-work.md` — erp.today, "SAP Rolls Out Joule Work and New Assistants, With Most Arriving by Early 2027" (captured 2026-10-28); relays SAP's SAP Connect release (2026-10-06) and innovation news guide.

## Related

- [[landscape/anthropic-enterprise-distribution-2026-05]] — earlier SAP Joule + Anthropic announcement (2026-05-17, no GA); this page gives the later GA timeline
- [[platforms/workday]] — comparable ERP/HR-vendor agent front door and governed agents
- [[platforms/servicenow]] — comparable enterprise-platform agent governance and autonomy control
- [[platforms/salesforce]] — competing enterprise-suite agent platform (Agentforce)
- [[thesis/agents-eating-saas]] — incumbent suite vendors embedding agents
- [[landscape/databricks-data-ai-summit-2026-06]] — OpenSharing Protocol is backed by SAP
