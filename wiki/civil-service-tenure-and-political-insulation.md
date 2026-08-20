# Civil Service Tenure and Political Insulation

Guo Xu's review does the thing this wiki's other personnel sources do not: it **splits "civil service protection" into two structurally distinct margins and shows their welfare effects can point in opposite directions**. *Entry protections* (γ) are rule-based rather than politically discretionary selection — they change **who** is appointed, a composition mechanism. *Progression protections* (κ) are the cost imposed on a politician's ability to threaten or execute removal and demotion — they change the appointee's **behaviour conditional on being appointed**, a disciplining-threat mechanism. In his formal model the two are **welfare complements when the bureaucrat is less biased than the politician and welfare substitutes when the bureaucrat is more biased** (Proposition 4): the sign of the interaction flips on who is further from the social optimum. On top of that model sits a narrative review of roughly 25 natural- and quasi-experimental studies, whose headline the author states as a **net positive** effect of protections on public service delivery — and whose qualifications he states himself, including two null results, one negative, and an entrenchment counter-case that sits directly against his own framing. The paper is not an advocacy piece for maximal protection and should not be cited as one.

**Evidence tier note — mixed within one source, and the mix is the point.**
- **[model]** The two-stage politician–bureaucrat game (Section 2.2, formalised in Appendix A, Propositions 1–4). Stylised, a single dyad, no organisational size, no hierarchy. **Not tested by the author.**
- **[empirical — weakest tier]** The author's own 73-country 2020 cross-section (QoG + V-Dem composite indices). Explicitly flagged by him as correlational.
- **[empirical — strongest tier]** ~11 studies tabulated in the paper's own Table 1, using staggered difference-in-differences, close-election and population-threshold RDDs, and historical municipal panels.
- **[empirical — small-N field experiments]** Two randomised designs bearing indirectly on protections (promotion-criteria clarity and discretion). The author notes randomisation is rare here because "the focus on civil service institutions makes the use of experiments relatively harder."
- **The author's own caveat on the whole review**: reform events are rare, rarely isolated (the Pendleton Act also banned soliciting campaign contributions from bureaucrats), and **overwhelmingly concentrated in the United States**, which limits external validity.
- **Self-citation, flagged.** Guo Xu co-authors several of the underlying empirical papers he reviews (Xu 2018; Aneja & Xu 2024; Spenkuch, Teso & Xu 2023; Bellodi et al. 2026), so the review is not fully arms-length from its evidence base. The underlying studies do use independent identification strategies rather than a shared method.

## The two margins

**[model]** The model treats protections literally as a **transfer of formal authority from politician to bureaucrat** (citing Aghion & Tirole's formal-vs-real-authority distinction) at two separate points:

| | **Entry margin (γ)** | **Progression margin (κ)** |
|---|---|---|
| What it is | Rule-based competitive selection vs. politically discretionary appointment | Cost to the politician of removing, demoting or threatening the incumbent |
| What it changes | The **type** of bureaucrat appointed | The appointee's **behaviour**, given appointment |
| Mechanism class | Selection / composition | Disciplining threat / insulation |
| Failure if absent | Patronage — unqualified loyalists | Political interference, turnover cycles |
| Failure if excessive | — | "Deep state": an insulated bureaucrat more biased than the politician, made worse by protection |

**Proposition 4 is the load-bearing result.** The two are complements when the bureaucrat is *less* biased than the politician — protection at one margin raises the value of protection at the other — and substitutes when the bureaucrat is *more* biased. **The model's welfare verdict is ambiguous and its sign depends on a quantity nobody measures**: relative bias. The author says so.

**[empirical] The decomposition matters, and one case resolves it.** Aneja & Xu (2024) study the Pendleton Act's rollout at the US Post Office (1883–1893) with staggered difference-in-differences and attribute the performance gains to **reduced political interference and turnover — the progression margin — not to improved selection via competitive exams**, for which they find only limited evidence. The effect is strongest in election years. This is the wiki's cleanest instance of a bundled reform being decomposed and the tenure limb, not the exam limb, doing the work. It bears directly on what [[weberian-structure-and-growth]] cannot separate: Evans & Rauch's ten-item scale is never decomposed, and Rauch's civil-service treatment bundles merit hiring with just-cause tenure.

**[wiki synthesis]** These are two different axes and this wiki had only one of them. [[dimensions-of-institutional-variation]] **D70** (personnel selection and recruitment mechanism) is the entry margin, measured entirely at the front door. The progression margin is registered separately as **D100**, with the distinction stated there.

## The cross-country correlation, and why it carries little weight

**[empirical — correlational, and the author says so]** 73 countries, 2020, using QoG and V-Dem composite indices:

| Relationship | Slope | SE | p |
|---|---|---|---|
| Protections index → log GDP per capita (PPP) | **3.503** | 0.537 | < 0.001 |
| Career-progression index → recruitment index (the "clustering" fact) | **0.833** | 0.074 | < 0.001 |

The second is the more interesting one: countries that protect entry also protect progression, so the two margins the model separates are **empirically bundled in the cross-section**, which is exactly why single-reform natural experiments are needed to tell them apart.

Three caveats, all the author's: (i) a **de jure / de facto measurement gap** — 59 countries constitutionally enshrine merit exams, but legal text has "surprisingly low" predictive power for de facto protections; (ii) subjective-expert-coder **halo bias** across sub-indices; (iii) aggregation masking within-country heterogeneity, including "pockets of effectiveness". The relationship is "strongest and tightest" among democracies and weakens in the autocratic subsample once Singapore — the sole strong-protection autocracy — is dropped. Run this through [[dimensions-of-institutional-variation]] D90's measurement-validity gate before using it for anything.

## The reform inventory, reported whole

**[empirical]** The author's tally across Table 1 is **mostly positive, with two nulls and one negative** — plus a separate entrenchment counter-case discussed below. This page reports the negative and null cases with the reasons the source gives, because a review whose headline is "net positive" is only usable if the exceptions travel with it.

**Positive:**
- **Aneja & Xu (2024)**, Pendleton Act at the Post Office, staggered DiD — improved delivery performance, driven by reduced turnover and interference, strongest in election years.
- **Spenkuch, Teso & Xu (2023)**, US federal personnel linked to voter registration, 1997–2021 — protected positions show **no partisan hiring or firing cycle**, against large cycles among "at the pleasure" political appointees.
- **Estrada (2019)**, Mexican teachers, quasi-random assignment — discretionary hires perform significantly worse on value-added.
- **Mocanu (2025)**, Brazil's 1988 reform — blinded written exams reduce the gender hiring gap **and** raise the rate at which women apply: an applicant-pool effect, not only a screening effect.
- **Ornaghi (2019)**, US police departments, 1970 population-threshold RDD; **Bostashvili & Ujhelyi (2019)**, state highway-spending volatility; **Rauch (1995)**, US municipal infrastructure (see [[weberian-structure-and-growth]]); **Xu (2018)**, British colonial administration; **Liu & Zhang (2025)**, disaster-relief response speed.

**Null:**
- **Moreira & Pérez (2024)**, US customs offices, 1883 — the reform **reduced electoral turnover cycles but produced no revenue gain**. Author's stated reason: exemptions let politicians route around the rule via classified positions. **De jure change without de facto change.**
- **Riaño (2025)**, Colombian anti-nepotism regulation, 2015 — disclosed close family ties among new hires fell **15%**, and this did **not** translate into measured gains in hire quality or agency performance. The lever worked on its narrow target and did not move the outcome. The author flags this himself as a qualification rather than a success.

**Negative:**
- **Leucht (2024)**, Tammany-era NYPD — significant **non-compliance** with competitive-exam selection despite the statute, and officers hired through non-compliant patronage networks correlate with later voter support for the incumbent party. The formal rule did not bind, and the hiring channel that survived it produced political returns.

## The entrenchment counter-case

**[empirical — and it sits against the paper's own headline]** **Bazzi et al. (2025)**, Indonesian villages: in a setting where bureaucratic turnover is normally *low* — i.e. de facto protection is already high — election-induced turnover "shakes things up", produces bureaucrats better informed about villager preferences, and **improves service delivery**. Less protection, better outcome.

The author names this as the mirror-image failure mode to political interference and **does not resolve it**. It is the empirical face of the model's ambiguity: if the incumbent bureaucrat is more biased than the incoming political principal, protection is welfare-reducing.

**[wiki synthesis]** Two of the author's own three stated qualifications compound this and should be quoted rather than paraphrased away. First, **the evidence is stacked toward frontline, measurable roles** — teachers, health workers, police, mail carriers — because their output can be measured, while senior bureaucrats and mid-level managers, where preference misalignment is argued to matter most, are understudied ("more evidence on senior bureaucrats is urgently needed"). Second, **almost every studied reform is extensive-margin from a low base** — introducing protections where few existed — so effects may be non-linear and are **not extrapolable to already-highly-protected systems** (US federal civil service: >99% covered; UK higher still). The author states this as an open question rather than extrapolating. Third, cost-side evidence — turnover disruption, procurement misalignment, entrenchment — is real but is not weighed against the benefits, because no study has a counterfactual for both.

**Read together: the review's headline is a directional finding about moving from very little protection to some, on frontline roles with measurable output, mostly in the United States.** It is not evidence that more protection is better in a system that already has a lot.

## Failure modes named

**[empirical/model, mapped to this wiki's vocabulary]**

| The source's term | What it is | Wiki mapping |
|---|---|---|
| **"Deep state"** (the author's own scare-quoted term) | An insulated, unaccountable bureaucrat implementing an agenda more biased than the politician's; protections make it worse | Principal-agent drift |
| **Patronage / spoils** | Barbosa & Ferreira (2023): turnover-induced patronage explains **more than half** the rise in Brazilian public employment since redemocratisation. Colonnelli et al. (2020): winning-mayor supporters are significantly more likely to hold a public job and "much less likely to be qualified" | Rent extraction, with the *politician* exploiting the bureaucracy rather than an outside interest capturing a regulator — see [[regulatory-capture]] |
| **Favouritism; loyalty over competence** | Prendergast & Topel (1996); Egorov & Sonin (2011) on "dictators and their viziers" | Selection under discretion |
| **Influence activities / "yes men"** | de Janvry et al. (2023), RCT: Chinese civil servants experimentally shown which supervisor controls their promotion reallocate effort toward that supervisor — a **measured** cost of discretionary promotion | The influence-cost channel on [[multitask-incentive-theory]] |
| **Non-compliance / de facto evasion** | Leucht (2024); Moreira & Pérez (2024) — see above | The de jure/de facto gap, [[institutions-as-fundamental-cause]] |
| **Entrenchment / excessive insulation** | Bazzi et al. (2025) — see above | — |
| **Time inconsistency** | Solved rather than caused by protections here; the Kydland–Prescott logic, protections-as-commitment-device | [[credible-commitment]] |

## Power, and a direct tension the author names

**[empirical]** Bureaucrats are not elected and are accountable to the public only via the "long route" running through elected politicians. But **Ujhelyi (2014a)** shows that if civil-service reform raises bureaucrat quality, voters become **less able to infer politician quality** from public-good outcomes — outcomes become less sensitive to political effort — so the reform **erodes electoral accountability even as it improves service delivery**. That is a real tension between who exercises decision rights and who the institution is nominally accountable to, and it is stated inside a paper arguing for the net benefit of protections. Bears on [[open-questions]] Q11.

## Public/private: a precise two-part argument, and where it blurs

**[model — the source is unusually explicit here, so it is worth carrying whole]** The author argues civil-service protections are **not** simply a public-sector instance of general personnel economics, for two reasons:

1. Public organisations exist to deliver goods where markets fail, so **both** mission and policy-preference alignment (**horizontal** traits) and ability (**vertical** traits) matter for public personnel, whereas standard personnel economics weights vertical traits more heavily. Registered as [[dimensions-of-institutional-variation]] **D101**.
2. Private organisations have a stable dominant objective (profit); the public sector's governing principal has policy preferences that **swing with political turnover** — principal instability with no clean private analogue.

Consequently the source splits its own mechanisms across the sector line:

- **General to any employer** (imported from outside the public-sector literature): the moral-hazard / human-capital trade-off underlying job security — tenure buys investment in job-specific human capital (Becker; Carmichael) at the cost of weakened career-incentive discipline (Holmström; Shapiro & Stiglitz).
- **Public-sector-specific**: protection against a principal whose preferences swing with elections.

**[wiki synthesis] The author then blurs the line he has just drawn.** He offers **central bank independence** (Rogoff 1985) and **judicial independence** (Hanssen 2004) as analogies for the insulation mechanism — treating them as structurally the same commitment-device logic applied to a different kind of biased agent. Those are public bodies, so the analogy does not cross the sector line; but it does show the mechanism is a *design pattern* rather than a property of civil services, which weakens the claim that it is specific to the elected-principal case. **Unresolved in the source.** Recorded against [[open-questions]] Q3 and Q38.

## The Weber gap

**[wiki synthesis]** This source is the wiki's most direct available empirical engagement with the Weberian prescription of tenure as a component of rational-legal authority — and **it is not Weber, and cannot stand in for him.** The wiki does not hold Weber's own text (scanned image, OCR failed). This paper's only link to Weber is a **single footnote** on Prussia stating that Weber, "greatly influenced by the Prussian experience, saw the rule-based bureaucracy as superior but likewise worried about the loss of control" — Guo Xu's own gloss on an untranslated 1922 German edition, not a quotation. Even that one link is second-hand and unverified against primary text. The paper otherwise reaches "Weberian bureaucracy" through the same operationalised proxies used elsewhere in this batch — Evans & Rauch's survey scale and Besley et al.'s "Weberian facts" — so **the proxy problem recurs rather than being resolved**. See [[weberian-structure-and-growth]].

## What this source does not contain

**[wiki synthesis]**

- **No organisational size or age variable anywhere.** This is the one axis genuinely silent in the paper. The nearest analogue is **seniority level within a bureaucracy** — a claim about hierarchical rank, not about institution size or age — and the author flags it as an evidence gap, not a finding.
- **No pooled effect size.** The headline is a qualitative synthesis across single-reform studies, not a meta-analysis. Do not quote it as one.
- **No test of the model.** Propositions 1–4 are untested by the author, and the quantity the welfare sign turns on — relative bias of bureaucrat and politician — is not measured anywhere.
- **Scope**: heavily US-concentrated by the author's own admission (Pendleton Act 1883, state highway reforms 1960–1989, municipal reforms 1902–1931, police departments 1970), with non-US extensions in the UK judiciary, Mexico, Brazil, Colombia, Ecuador, Indonesia, India, historical British Empire and Imperial China.

## Source

- `raw/research/bureaucracy-and-public-choice/07-guo-xu-civil-service-protections.md` — Guo Xu, "The Economics of Civil Service Protections", NBER Working Paper 35568, July 2026. https://www.nber.org/system/files/working_papers/w35568/w35568.pdf (http://www.nber.org/papers/w35568)

## Related

- [[personnel-economics-of-the-state]] — the base this source explicitly builds on (Finan, Olken & Pande); this page narrows that literature to the tenure/protection slice and adds a formal model plus a reform-evaluation inventory that page does not cover.
- [[weberian-structure-and-growth]] — the empirical Weberian camp's other two papers; this page performs the entry/progression decomposition they bundle, and Rauch (1995) appears in this source's Table 1.
- [[organizational-economics-of-the-state]] — the systems-level agenda from the same research programme; independent-agency design there is the same insulation logic applied one level up.
- [[credible-commitment]] — progression-margin protection is the shackling logic applied to an individual appointment rather than to a sovereign's property-rights promise; the source's own central-bank and judicial-independence analogies make the connection explicit.
- [[institutions-as-fundamental-cause]] — the de jure/de facto gap this source measures directly (constitutional merit-exam text with "surprisingly low" predictive power; exam statutes routed around via classified positions) is AJR's abstract distinction made concrete at the level of personnel rules.
- [[incentives-under-multiple-principals]] — Dixit's noncooperating principals and this source's *preference-swinging* principal are complementary accounts of why public incentive design differs structurally from private.
- [[multitask-incentive-theory]] — the moral-hazard cost side of tenure ("job security limits the extent to which career incentives can be used") is the same mechanism as fixed pay being the rational response to unmeasurable tasks, reached from a different literature; de Janvry et al.'s yes-men RCT is a measured instance of the influence-cost channel.
- [[regulatory-capture]] — patronage here is capture with the direction reversed: the politician extracting jobs from the bureaucracy, rather than an outside interest capturing a regulator.
- [[political-economy-of-public-sector-reform]] — the author's concluding section reaches the same concentrated-cost/diffuse-benefit and elite-bargain obstacles, applied to civil-service-reform *adoption* rather than implementation.
- [[reform-levers]] — supplies candidate tier-(i) additions with their own quasi-experimental evidence: rule-based entry selection, progression-margin protection, promotion-criteria transparency; and one honest non-lever, anti-nepotism disclosure, which hits its target and does not move the outcome.
- [[dimensions-of-institutional-variation]] — supplies **D100** (progression-margin protection, distinct from D70) and **D101** (horizontal vs. vertical selection trait).
- [[open-questions]] — bears on Q3 and Q38 (the public/private argument and where it blurs), Q4 (selection now measured beyond the front door), Q11 (the Ujhelyi accountability-erosion result) and Q102.
