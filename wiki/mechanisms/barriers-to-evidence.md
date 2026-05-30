# Barriers to Evidence in Algorithmic Harm Litigation

AI developers and deployers systematically block algorithmic harm litigation by controlling all seven forms of evidence access — a structural "privatization of proof" documented by Cen, Ismael, and Zheng (CMU/Berkeley/Stanford, FAccT 2026) across hiring, healthcare denial, insurance, criminal sentencing, immigration, and copyright cases. The paper counters with a three-part proportionality test anchored to each cause of action, plus a fungibility taxonomy showing that partial access proposals can substitute for refused full-disclosure demands.

## Seven access asymmetries

The paper catalogs seven dimensions on which defendants hold an information monopoly:

1. **Model access** — weights, architecture, and inference code are trade secrets; plaintiffs cannot reproduce or probe the decision function. Defendants invoke IP protection and infeasibility arguments to block production entirely.
2. **Data access** — training corpora and inference-time input distributions are proprietary; without them, plaintiffs cannot establish disparate impact or reconstruct what the model learned.
3. **Documentation access** — design specifications, model cards, audit reports, and internal evaluations are withheld under trade secrecy; their absence makes it impossible to identify what the developer knew about failure modes.
4. **Log access** — decision logs (inputs, outputs, confidence scores, timestamps) are the most granular per-person evidence of harm but are frequently deleted, never retained, or rendered unavailable. The NYT v. OpenAI litigation produced a "sandbox gambit": OpenAI provided VM access to plaintiffs, then deleted the results before they could be preserved.
5. **Expertise asymmetry** — defendants field in-house ML teams and well-resourced expert witnesses; plaintiff-side litigators lack equivalent technical capacity to frame discovery requests, evaluate disclosures, or challenge expert testimony.
6. **Compute access** — replication of model behavior at scale requires compute the plaintiff cannot afford; this renders independent audit or reproduction studies infeasible even where raw data were disclosed.
7. **Infrastructure access** — proprietary MLOps pipelines, versioning systems, and deployment stacks are opaque; plaintiffs cannot establish what version of a model was running at the time of a contested decision, enabling version-deprecation defenses.

Collectively these create a Catch-22: plaintiffs cannot satisfy the evidentiary threshold needed to compel discovery, but without discovery they cannot demonstrate that threshold is met. Cases collapse before trial, not on the merits. Documented examples include Mobley v. Workday (hiring), Lokken v. UnitedHealth (healthcare denial), Huskey v. State Farm (insurance), Loomis/COMPAS (sentencing), Mehrara/Chinook (immigration), and NYT v. OpenAI (copyright).

## The proportionality test

The paper proposes a three-part test for courts adjudicating AI evidence-access disputes, importing existing federal discovery doctrine (Rule 26 proportionality, Zubulake cost-shifting, spoliation/adverse inference) into a single AI-specialized framework:

1. **Assess asymmetry degree** — inventory which of the seven access dimensions are at issue and how severe the information gap is on each. The degree of asymmetry determines how far the court should shift the burden toward disclosure.
2. **Apply cause-of-action baseline** — compare requested access against the minimum access necessary to reproduce the elements of the specific claim. Discovery demands beyond the baseline are subject to proportionality trimming; demands at or below it are presumptively appropriate. This step prevents defendants from defeating all AI cases via blanket trade-secrecy claims while also constraining maximalist discovery demands.
3. **Evaluate alternatives and adverse-inference option** — the producing party may propose a functionally equivalent alternative (sandbox, query access, redacted documentation, structured evaluation sets) or accept an adverse inference instruction in lieu of disclosure. Courts weigh the alternative's adequacy against the baseline; an inadequate alternative combined with refusal to disclose triggers adverse inference.

## Fungibility of access types

The paper's central technical insight is that the seven access types are partially substitutable. Model access, data access, compute, logs, and documentation are not independent requirements; in many cases a combination of lower-sensitivity disclosures can substitute for a refused high-sensitivity one:

- Query access + decision logs often suffices to reconstruct behavioral patterns that would otherwise require weight access.
- Documentation (model cards, audit reports, internal evaluations) + structured evaluation sets can establish discriminatory impact without training-data access.
- Log slices covering the plaintiff class, combined with expert analysis, can establish causation without full model reproduction.

This fungibility makes negotiated partial access viable rather than all-or-nothing fights. It also implies that defendants who refuse all alternatives — including documentation and logs — are harder to distinguish from spoliation. For tooling design, it means access demands should specify substitutes acceptable to the requester rather than framing requests as take-it-or-leave-it weight disclosure.

## Actionable implications for DSAR and litigation strategy

**Framing DSAR requests around cause of action, not maximal transparency.** DSARs drafted as broad transparency demands are easier to refuse on proportionality grounds. Requests should identify the specific harm, map each requested data category to an element of the legal claim it supports, and name acceptable substitutes for each category. This mirrors the proportionality-test structure and pre-positions requests for judicial enforcement if refused.

**Document all seven access dimensions before filing.** Class-action complaints in cases like Lokken v. UnitedHealth and Huskey v. State Farm are vulnerable pre-trial because the access asymmetry is not fully articulated at the pleading stage. Complaint drafting should inventory which dimensions are at issue, what the plaintiff lacks, and why the deficit makes the cause-of-action elements unreachable without discovery — framing the privatization-of-proof Catch-22 explicitly so courts see the structural problem rather than a discovery dispute.

**Demand log retention orders early.** The NYT sandbox gambit and the general pattern of log deletion create spoliation exposure, but only if preservation obligations are triggered. Plaintiff-side litigators should move for log retention orders at the earliest stage — before the operative model version is deprecated or logs are deleted per routine retention policy. Regulatory channels (CFPB, state AG investigations) can demand preservation as a condition of investigation, independent of litigation.

**Name the "AI as guide not decision-maker" defense in the complaint.** Defendants in Huskey v. State Farm and similar cases defeat class certification by arguing the AI is advisory and final decisions are human. Complaints should plead facts that make this defense unavailable: decision velocity, documented override rates, incentive structures discouraging override, and any internal communications treating the AI output as dispositive.

**Build or access technical expert capacity.** The expertise asymmetry is a structural problem for plaintiff-side practice. Coordinated plaintiff teams (as in RealPage and Greystar class actions) can pool expert resources. Public-interest AI auditor pools, if funded, could extend this capacity to cases that cannot support retained experts — a policy target supported by this paper's framing.

**Use query access + logs as baseline ask in partial-access negotiations.** When full model or data access is refused, the fungibility taxonomy supports a fallback demand for: (a) query access to the production model or a preserved copy, (b) decision logs covering the plaintiff class, (c) model documentation and any internal audit reports. This combination is lower-sensitivity than weights or training data but sufficient to support most discrimination and due-process claims.

## Source

- `raw/research/weekly-2026-05-25/03-barriers-to-evidence-faccT2026.md` — Cen, Ismael, and Zheng (CMU/Berkeley/Stanford), FAccT 2026 (June 2026, Montreal). Academic paper systematizing evidence-access barriers in AI litigation across seven dimensions, with a three-part proportionality test and fungibility taxonomy for resolving AI discovery disputes.

## Related

- [[transparency-tools]] — transparency tools address the information gap at the consumer layer; this page addresses the evidentiary layer in litigation; both are responses to AI opacity
- [[dsar-and-data-deletion]] — DSAR strategy is directly constrained and informed by the proportionality test and fungibility taxonomy documented here
- [[collective-bargaining-for-data]] — collective bargaining for data access at the regulatory level is an upstream intervention on the same information monopoly that blocks litigation evidence access
- [[regulatory-responses]] — regulatory preservation orders and investigation demands are an alternative channel to litigation for triggering log retention obligations
- [[buyer-cartels-antitrust]] — RealPage and Greystar class actions are the active enforcement cases most affected by the privatization-of-proof dynamic; the access asymmetries documented here explain procedural fragility in those cases
