# Dimensions of Institutional Variation

A standing register of every axis of institutional variation named by the sources this wiki has ingested, with — for each — who named it, how it would be measured on a real institution, and its status. This is the seed of the wiki's general analytical framework (project outcome 2); it is meant to be extended by every subsequent ingest, not rewritten. Nothing here is a finding: the register records what the literature *proposes* as an axis and what it would take to put a number on it. Entries currently come from four foundational New Institutional Economics sources (North ×2, Ostrom, Williamson) plus Libecap's NBER retrospective — a literature that is theory and comparative history, not empirical identification, with the single exception of Ostrom's experimental and meta-analytic work.

## How to read this

**Status values.** `candidate` — named by a source and operationalisable, but not yet doing predictive work in this wiki. `promoted` — meets the promotion criterion below. `rejected` — cannot currently be measured as stated, with the reason recorded; the row stays so the problem is visible rather than silently dropped.

**Promotion criterion [wiki synthesis].** An axis is promoted when (i) at least two independent sources name it, *and* (ii) a measurement procedure can be stated that could be run against an institution's primary documents, budget, personnel records, or observable behaviour, without needing access the analyst would not plausibly have. Both conditions, not either. Criterion (i) is deliberately weak evidence of importance — it is a prior, revisable as soon as an axis proves it earns its place by predicting something.

**Admissibility [lint check 11].** A dimension with no operationalisation is not admissible as part of the framework. Where none can be stated, the row says so explicitly and is marked `rejected`, with a note on what restatement would readmit it.

**Evidence tier.** Every row is (b) a theoretical proposal, except where the Named-by column marks Ostrom's experimental/meta-analytic findings or Libecap's own case work, which are (a) empirical. The operationalisation column is (c) wiki synthesis throughout — the sources rarely state how to measure what they name, and where they do it is noted.

## Register

### Rules and enforcement

| # | Dimension | Named by | Operationalisation | Status |
|---|---|---|---|---|
| D1 | **Formalisation** — formal written rules vs. informal constraints (norms, conventions, self-imposed codes) | North (JEP; framework); Ostrom (rules-in-use vs. formal organisation — 25% of coded fishery subgroups had no formal organisation at all) | Take a sample of consequential decisions; for each, code whether the binding constraint is documented and citable or unwritten practice. Report the ratio. | promoted |
| D2 | **Formal/informal change-speed differential** | North (framework): "formal rules may change over night, but informal constraints do not" | Elapsed time between a formal rule change and observed change in the corresponding behaviour. Requires a before/after behavioural measure, so only applicable where behaviour is observable. | candidate |
| D3 | **Enforcement party** — first party (self-imposed), second party (retaliation), third party (community sanction, state coercion) | North (framework, explicit three-way; JEP: personal/kin vs. impersonal state) | For a sample of rule violations, code who actually imposed the cost. Note the distinction from *who is nominally responsible for enforcement* — the gap between the two is itself the finding. | promoted |
| D4 | **Direction of monitor accountability** — monitors accountable to the users vs. to an external principal | Ostrom (design principles 4A/4B; **empirical**: local monitoring is the strongest single correlate of good resource condition) | Who appoints, pays, and can remove the monitor. Answerable from primary documents in most institutions. | promoted |
| D5 | **Sanction design** — externally imposed vs. participant-designed; graduated vs. fixed severity | Ostrom (design principle 5; **empirical**: self-designed sanctioning reached ~90% of optimal returns in lab CPR games, the best of any tested condition) | Read the sanction schedule: does severity escalate with repeat violation, and did the sanctioned population participate in setting it? | candidate |
| D6 | **Contract law regime** — court-enforced legal rules vs. private ordering/forbearance | Williamson | Will an external court hear a dispute arising inside this relationship? Measure as the share of disputes resolved by an external adjudicator vs. internally by fiat. | candidate |

### Decision rights and accountability

| # | Dimension | Named by | Operationalisation | Status |
|---|---|---|---|---|
| D7 | **Locus of rule-making authority** — are those affected by a rule authorised to change it? | Ostrom (design principle 3) | Fraction of individuals materially affected by a rule who hold a formal vote or veto over changing it. Compute from the constitutive documents. | candidate |
| D8 | **Residual claimancy / incentive intensity** — does the decision-maker's own income vary with the surplus their decision generates? | Libecap (**own case work**: politicians and bureaucrats "are not direct residual rent claimants"); Williamson (incentive intensity, strong vs. weak) | Read the compensation and budget rules: what fraction of the surplus (or loss) from a decision accrues to the decision-maker? Binary at minimum (residual claimant / not), continuous where pay is formula-linked. | promoted |
| D9 | **Discretion vs. rule-boundedness** — how much of the decision space is unreviewable judgement | Libecap (**own case work**: regulators preserve discretion by choosing revocable permits over transferable rights); North (framework: institutions "lower the price of acting on one's ideas" — voting systems, lifetime judicial tenure) | Share of consequential allocations made by discretionary determination vs. by formula, auction, or entitlement. Also: count decisions with no reviewable standard. | promoted |
| D10 | **Constraint on the top decision-maker** — arbitrary vs. structurally shackled | North (JEP: ruler shackling, Glorious Revolution; self-restraint "seldom successful for very long") | Count of independent actors able to block an expropriative act, and whether any has ever exercised it. Market-priced alternative in D11. | promoted |
| D11 | **Property-right / entitlement security** — full transferable right vs. revocable use right | Libecap (**own case work**, with the sharpest measure in these sources); Ostrom (five-right bundle: access, withdrawal, management, exclusion, alienation); North | Two methods. (i) Code which of the five rights the holder actually has. (ii) **Market-priced**: the lease-to-sale price ratio of the entitlement estimates the discount for expected future erosion — US ITQ ratio ≈ 2× New Zealand's, implying ~50% probability of erosion. Method (ii) is the only operationalisation in these sources that yields a number from market data. | promoted |
| D12 | **Exit / voice** — can the governed leave, and can they contract differently? | Ostrom (citizens "vote with their feet"; incorporated communities can renegotiate contracts with producers; neighbourhoods inside a large city can do neither) | Count of substitutable providers reachable at acceptable switching cost, and whether the governed unit holds a renegotiable contract or is administratively assigned. | candidate |
| D13 | **Recognition by higher authority** — does the surrounding state recognise this body's right to make its own rules? | Ostrom (design principle 7) | Is the rule-making power recognised in statute or higher-court doctrine, and how often has it been overridden in the last N years? Override frequency is the better measure — formal recognition alone is cheap. | candidate |

### Structure of the field

| # | Dimension | Named by | Operationalisation | Status |
|---|---|---|---|---|
| D14 | **Polycentricity** — many formally independent decision centres vs. a single hierarchical authority | Ostrom (**empirical**: metropolitan producer multiplicity raises technical efficiency for direct services); North (JEP: fragmented competitive polities vs. centralised bureaucratic monopoly) | Count formally independent decision centres with authority over the same domain; add a concentration index of output or budget across them. Ostrom's metro-services work does exactly this. | promoted |
| D15 | **Nesting depth** — single-layer vs. multi-layer governance | Ostrom (design principle 8) | Count governance layers between the individual participant and the highest body with binding authority over the same activity. | candidate |
| D16 | **Number and heterogeneity of parties** | Libecap (**own case work**, following Olson); Ostrom (user-group size as an SES variable) | Count the parties holding a veto or a claim; measure dispersion of their per-unit costs or asset values (coefficient of variation). Libecap's oil cases operationalise this directly through lease-holder counts and cost heterogeneity. | promoted |
| D17 | **Governance mode** — market / hybrid / hierarchy | Williamson | For a given transaction, code the three governance attributes (D6, D8, and administrative fiat) and read off the mode; or observe the make-or-buy outcome directly. | candidate |
| D18 | **Administrative command and control (fiat)** — strong under unified ownership, weak in market exchange | Williamson | Can one party direct the other's action without renegotiation and without recourse? Test on observed disputes: were they settled by instruction or by bargaining? | candidate |

### Attributes of what is being transacted

| # | Dimension | Named by | Operationalisation | Status |
|---|---|---|---|---|
| D19 | **Asset specificity** — physical, human, site-specific, dedicated, brand-name, episodic/temporal | Williamson (central variable; explicitly a *design* variable — specificity can be engineered down at a cost in performance) | Redeployability: the fraction of the asset's value recoverable in its next-best use if the current counterparty disappeared. Estimable from resale/secondary-market data for physical assets; considerably harder for human and site specificity, where the honest answer is that no method in these sources measures it. | candidate |
| D20 | **Uncertainty / disturbance frequency** — outlier disturbances requiring unprogrammed adaptation | Williamson | Count consequential unprogrammed adaptations per unit time over the relationship's history: contract amendments, emergency deviations, renegotiations. | candidate |
| D21 | **Frequency of transaction** | Williamson (named as one of the three canonical attributes; not elaborated) | Transactions per period between the same parties. Trivial to measure, currently doing no work in this wiki. | candidate |
| D22 | **Complexity** — drives contractual incompleteness via bounded rationality | Williamson | Weakly measurable: share of foreseeable contingencies left unspecified in the governing document, or count of decision points requiring judgement rather than lookup. Both proxies are analyst-dependent; flagged as a soft measure. | candidate |
| D23 | **Nature of the good or resource** — subtractability of use × difficulty of exclusion (both continuous), plus boundability, observability, heterogeneity | Ostrom (four-way goods typology: private / public / toll / common-pool); Libecap (**own case work**, Table 1: small/boundable/observable/homogeneous vs. large/valuable/unobservable/heterogeneous/migratory) | Score subtractability and exclusion cost on continuous scales rather than assigning a goods category. For a physical resource, additionally code boundary observability and unit heterogeneity. | promoted |
| D24 | **Risk vs. uncertainty** — is the downside actuarially priceable? | North (JEP: marine insurance, portfolio diversification as the institutions that convert uncertainty into priced risk) | Does an insurance or hedging market exist for this exposure, and at what price? Existence of a price is the measure. | candidate |

### Information and measurement

| # | Dimension | Named by | Operationalisation | Status |
|---|---|---|---|---|
| D25 | **Measurability of output and information flow** | North (JEP: the Suq lacks "institutions devoted to assembling and distributing market information" — no price quotations, no standardised weights and measures); North (framework: accuracy of information feedback to decision-makers); Ostrom (aggregated vs. individualised information; ease of measuring the resource — river vs. forest); Libecap (cost of verifying heterogeneous claims) | Can a third party verify the output at acceptable cost? Score on three components: existence of standardised units, published prices or performance statistics, and independent audit. The most-cited axis in the foundations set. | promoted |
| D26 | **Information rules** — mandated channels and disclosure | Ostrom (rules-in-use type 4) | Enumerate what must be disclosed, to whom, on what cadence; then measure compliance rate rather than the rule alone. | candidate |

### Scale, time and duration

| # | Dimension | Named by | Operationalisation | Status |
|---|---|---|---|---|
| D27 | **Scale of the transacting domain** — village → regional bazaar → long-distance → national → international | North (JEP; also names rising trade volume as a *cause* of institutional investment) | Geographic and counterparty reach of the typical transaction; share of transactions with non-repeat, non-kin counterparties. | candidate |
| D28 | **Organisational size** | Williamson (limits to firm size: bureaucratic ploys and political positioning rise with size); Ostrom (producer scale; small-to-medium cities monitor better; **empirical**: scale effects *invert* by service type — direct services benefit from many producers, indirect/support services from few) | Headcount, budget, and number of hierarchical layers — trivially measurable. The problem is not measurement but that no source here states a threshold or tests a within-organisation prediction. Measurable, unlinked. | candidate |
| D29 | **Time horizon** — expected duration of the interaction | Ostrom (microsituational variable: longer anticipated horizon raises cooperation); Williamson (longer contracts accumulate more consequential disturbances) | Expected duration of the relationship; contract length; tenure of the decision-makers. Note the two sources predict *opposite signs* — longer horizon helps cooperation, and simultaneously raises disturbance exposure. | promoted |
| D30 | **Time-to-correction and rent dissipated before it** | Libecap (**own case work**: 4–9 years to negotiate unitization across seven Texas fields; ITQ regimes adopted only when stocks near collapse; ~25% of 1914 US oil production value lost, ≈ $1.34bn in 2018 dollars) | Years from recognition of the problem to adoption of a corrective rule, and the value lost in that interval. Requires a dated problem-onset, which is often contestable — say which event is being used. | promoted |

### Legitimacy and beliefs

| # | Dimension | Named by | Operationalisation | Status |
|---|---|---|---|---|
| D31 | **Perceived legitimacy and equity** | Ostrom ("whether users consider the system to be legitimate and equitable" is named as one of the three things that actually explain forest condition) | Direct: survey the governed. Revealed: voluntary compliance rate in the absence of monitoring — the cleaner measure, since it is behavioural. | candidate |
| D32 | **Trust / expected reciprocity** | Ostrom (posited as the central mediating variable between situational structure and cooperation) | Behavioural elicitation via standardised cooperation games, or observed voluntary contribution rates. Ostrom explicitly notes no settled theory of the individual underlies this, so the measure currently outruns the theory. | candidate |
| D33 | **Mental models of decision-makers** | North (framework: institutional change is filtered through subjective and possibly incorrect mental models) | Partially measurable: code the stated rationales in decision documents against the actual payoff structure and score divergence. This is a proxy for stated belief, not held belief, and no source proposes a method. Retained as candidate only because the proxy is at least executable. | candidate |
| D34 | **Adaptive efficiency** | North (framework, named in passing) | **No operationalisation available.** As stated, "the capacity of an institution to adapt well" is defined by the outcome it is meant to explain, and North supplies no independent indicator. Would be readmissible if restated as an observable — e.g. rate of rule revision per unit of measured performance shortfall, or elapsed time from a detected performance failure to a rule change. Recorded rather than dropped, per lint check 11. | rejected |

## What this register does not yet contain

**[wiki synthesis]** The gap is structural and worth stating, because it is the gap between this literature and what this wiki is for. The foundations-NIE sources supply axes describing *rule-sets, transactions, and resource regimes*. They supply almost nothing describing the **internal composition of a single organisation**. Specifically absent from all five sources:

- selection and promotion criteria for personnel (who ends up inside — [[open-questions]] Q4);
- mandate clarity and multiplicity of objectives;
- funding source and its stability;
- hierarchy layer count as a behavioural variable rather than a size proxy;
- age of the organisation as distinct from age of the rule-set (see [[path-dependence]]);
- career incentives, tenure structures, and internal labour markets.

D28 is measurable but currently unlinked to any tested prediction; the rest are not in the register because no source here names them. They should be the first things a later ingest of organisational-theory or bureaucratic-politics sources adds.

**Second-hand marking.** Where the Named-by column cites Libecap, the entry draws on **his own** oil, fisheries, and groundwater case work. Libecap's summaries of North elsewhere in that paper are second-hand and are not used as a naming source in this register.

## Source

- `raw/research/foundations-nie/01-north-institutions-jep.md` — Douglass C. North, "Institutions", *Journal of Economic Perspectives* 5(1), 1991, 97–112. https://web.pdx.edu/~nwallace/EHP/NorthInstitutions.pdf (JSTOR: http://www.jstor.org/stable/1942704)
- `raw/research/foundations-nie/02-north-institutional-change-framework.md` — Douglass C. North, "Institutional Change: A Framework of Analysis". https://econwpa.ub.uni-muenchen.de/econ-wp/eh/papers/9412/9412001.pdf
- `raw/research/foundations-nie/03-ostrom-nobel-polycentric.md` — Elinor Ostrom, "Beyond Markets and States: Polycentric Governance of Complex Economic Systems", Nobel Prize Lecture, 8 Dec 2009. https://www.nobelprize.org/uploads/2018/06/ostrom_lecture.pdf
- `raw/research/foundations-nie/04-nber-north-transaction-costs.md` — Gary D. Libecap, "Douglass C. North: Transaction Costs, Property Rights, and Economic Outcomes", NBER Working Paper 24585, May 2018. https://www.nber.org/system/files/working_papers/w24585/w24585.pdf — **North-attributed content in this source is second-hand.**
- `raw/research/foundations-nie/05-williamson-nobel-transaction-cost.md` — Oliver E. Williamson, "Transaction Cost Economics: The Natural Progression", Nobel Prize Lecture, 8 Dec 2009. https://www.nobelprize.org/uploads/2018/06/williamson_lecture.pdf

## Related

- [[what-is-an-institution]] — fixes what these axes are predicated of; the three competing definitions imply three different things being measured.
- [[polycentric-governance]] — the single largest contributor of axes (rules-in-use, goods typology, property-rights bundle, design principles) and the only source with empirical backing for any of them.
- [[governance-structures]] — supplies D6, D17, D18, D19, D20, D21, D22.
- [[transaction-costs]] — supplies D3, D8, D16, D25 and the reason measurability matters.
- [[credible-commitment]] — supplies D10 and the market-priced operationalisation in D11, the sharpest measure in the register.
- [[path-dependence]] — supplies D2 and D30, and explains why an axis can be measurable yet frozen in practice.
- [[open-questions]] — Q2 is the question this register exists to answer; Q3 asks which of these axes are genuinely invariant across the public/private divide.
